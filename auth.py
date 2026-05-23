"""Magic-link authentication for Take 139.

Flow:
1. User POSTs email to /auth/request-magic-link
2. Backend creates an AuthToken, emails the user a link
   https://take139.com/auth.html?token=XXX
3. User clicks link \u2192 /auth.html calls GET /auth/verify?token=XXX
4. Backend validates, marks token consumed, mints an AuthSession,
   returns {session_token, email} to the client
5. Client stores session_token in localStorage and sends it as
   X-Session-Token on every authenticated call (e.g. /auth/me)

Design rules:
- Tokens are single-use and expire in 15 minutes.
- Sessions live for 30 days; touched on every use.
- /auth/request-magic-link ALWAYS returns 200 to avoid leaking which
  email addresses are registered.
- We do NOT pre-register accounts. Any email can request a link; it
  only becomes \"useful\" once they've taken an assessment (because
  /auth/me looks up Submission rows by email).
"""
from __future__ import annotations
import os
import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
import bcrypt

from database import get_db, AuthToken, AuthSession, User


# ---- Password hashing ------------------------------------------------------
# Use bcrypt directly — simpler than passlib and avoids the passlib/bcrypt
# 4.x compatibility issue (passlib parses bcrypt.__about__ which moved).
# bcrypt has a hard 72-byte input limit; we truncate after that.
MIN_PASSWORD_LEN = 8
_BCRYPT_ROUNDS = 12  # ~250ms on a modern CPU, industry sweet spot for 2026
_BCRYPT_MAX_BYTES = 72


def _truncate(plain: str) -> bytes:
    """Encode + safely truncate to bcrypt's 72-byte limit."""
    b = plain.encode("utf-8", errors="ignore")
    return b[:_BCRYPT_MAX_BYTES]


def hash_password(plain: str) -> str:
    """Return a bcrypt hash string suitable for DB storage."""
    salt = bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(_truncate(plain), salt)
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: Optional[str]) -> bool:
    if not hashed or not plain:
        return False
    try:
        return bcrypt.checkpw(_truncate(plain), hashed.encode("utf-8"))
    except Exception:
        return False


def validate_password_strength(plain: str) -> Optional[str]:
    """Return None if password is OK, otherwise a user-friendly error message."""
    if not plain or len(plain) < MIN_PASSWORD_LEN:
        return f"Password must be at least {MIN_PASSWORD_LEN} characters long."
    if plain.strip() != plain:
        return "Password cannot start or end with a space."
    return None


# ---- User upsert helpers ---------------------------------------------------
def get_or_create_user(
    db: Session,
    email: str,
    name: Optional[str] = None,
) -> User:
    """Look up a User by email; if not present, create one. Updates name if
    we have one and the existing row doesn't.
    """
    email_norm = (email or "").strip().lower()
    user = db.query(User).filter(User.email == email_norm).first()
    if user is None:
        user = User(email=email_norm, name=(name or None))
        db.add(user)
        db.commit()
        db.refresh(user)
    elif name and not user.name:
        user.name = name
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == (email or "").strip().lower()).first()


def mark_email_verified(db: Session, user: User) -> None:
    if user.email_verified_at is None:
        user.email_verified_at = datetime.utcnow()
        db.add(user)
        db.commit()


def set_user_password(db: Session, user: User, new_plain: str) -> None:
    user.password_hash = hash_password(new_plain)
    db.add(user)
    db.commit()


# ---- Configuration ----------------------------------------------------------
SITE_URL = os.environ.get("SITE_URL", "https://take139.com").rstrip("/")
MAGIC_LINK_TTL_MIN = int(os.environ.get("MAGIC_LINK_TTL_MIN", "15"))
SESSION_TTL_DAYS = int(os.environ.get("SESSION_TTL_DAYS", "30"))


def _new_token(nbytes: int = 32) -> str:
    """URL-safe random token. 32 bytes \u2192 ~43 char base64url string."""
    return secrets.token_urlsafe(nbytes)


def get_client_ip(request: Request) -> Optional[str]:
    """Best-effort IP for audit logging. Respects X-Forwarded-For (Railway)."""
    if request is None:
        return None
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    try:
        return request.client.host if request.client else None
    except Exception:
        return None


# ---- Magic-link token lifecycle --------------------------------------------
def create_magic_link_token(
    db: Session,
    email: str,
    purpose: str = "signin",
    requester_ip: Optional[str] = None,
    ttl_minutes: Optional[int] = None,
) -> AuthToken:
    """Create + persist a single-use auth token. Returns the row."""
    ttl = ttl_minutes if ttl_minutes is not None else MAGIC_LINK_TTL_MIN
    now = datetime.utcnow()
    row = AuthToken(
        token=_new_token(32),
        email=email.strip().lower(),
        purpose=purpose,
        created_at=now,
        expires_at=now + timedelta(minutes=ttl),
        consumed_at=None,
        requester_ip=requester_ip,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def build_magic_link_url(token: str) -> str:
    """Public URL the user clicks to verify a token."""
    return f"{SITE_URL}/auth.html?token={token}"


def consume_token(db: Session, token: str) -> Optional[AuthToken]:
    """Validate + consume a magic-link token.

    Returns the AuthToken row on success, None on any failure (expired,
    already-consumed, not found). We intentionally collapse all failure
    modes to None so the caller returns a generic error \u2014 we don't
    want to leak which case failed.
    """
    if not token:
        return None
    row = db.query(AuthToken).filter(AuthToken.token == token).first()
    if not row:
        return None
    if row.consumed_at is not None:
        return None
    if row.expires_at < datetime.utcnow():
        return None
    row.consumed_at = datetime.utcnow()
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


# ---- Session lifecycle ------------------------------------------------------
def create_session(
    db: Session,
    email: str,
    requester_ip: Optional[str] = None,
    ttl_days: Optional[int] = None,
) -> AuthSession:
    """Mint a new long-lived session for an email."""
    days = ttl_days if ttl_days is not None else SESSION_TTL_DAYS
    now = datetime.utcnow()
    row = AuthSession(
        session_token=_new_token(48),
        email=email.strip().lower(),
        created_at=now,
        expires_at=now + timedelta(days=days),
        last_seen_at=now,
        revoked=False,
        requester_ip=requester_ip,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_session(db: Session, session_token: str) -> Optional[AuthSession]:
    """Look up + validate an active session. Updates last_seen_at on hit."""
    if not session_token:
        return None
    row = db.query(AuthSession).filter(AuthSession.session_token == session_token).first()
    if not row:
        return None
    if row.revoked:
        return None
    if row.expires_at < datetime.utcnow():
        return None
    # Touch last-seen so an active user's session keeps rolling forward.
    row.last_seen_at = datetime.utcnow()
    db.add(row)
    db.commit()
    return row


def revoke_session(db: Session, session_token: str) -> bool:
    """Sign-out: mark the session revoked."""
    row = db.query(AuthSession).filter(AuthSession.session_token == session_token).first()
    if not row:
        return False
    row.revoked = True
    db.add(row)
    db.commit()
    return True


# ---- FastAPI dependency: require a signed-in user --------------------------
def require_session(
    x_session_token: Optional[str] = Header(default=None, alias="X-Session-Token"),
    db: Session = Depends(get_db),
) -> AuthSession:
    """FastAPI dependency. Raises 401 if no valid session header."""
    sess = get_session(db, x_session_token or "")
    if sess is None:
        raise HTTPException(status_code=401, detail="Sign in to continue.")
    return sess


def optional_session(
    x_session_token: Optional[str] = Header(default=None, alias="X-Session-Token"),
    db: Session = Depends(get_db),
) -> Optional[AuthSession]:
    """Same as require_session but returns None instead of raising."""
    return get_session(db, x_session_token or "")
