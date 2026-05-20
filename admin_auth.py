"""Lightweight admin authentication for the /admin endpoints.

Design:
- Admin password lives in env var ADMIN_PASSWORD (set on Railway)
- Admin sends password to POST /admin/login
- Server returns a signed session token (HMAC of timestamp + secret)
- Subsequent /admin/* requests send `Authorization: Bearer <token>`
- Tokens are valid for ADMIN_TOKEN_TTL_HOURS (default 24h)
- No DB tables needed — stateless via HMAC
"""
import hmac
import hashlib
import os
import time
from typing import Optional

from fastapi import HTTPException, Header, status

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
ADMIN_TOKEN_SECRET = os.environ.get("ADMIN_TOKEN_SECRET", "")
ADMIN_TOKEN_TTL_HOURS = int(os.environ.get("ADMIN_TOKEN_TTL_HOURS", "24"))


def _ensure_secret() -> str:
    """The HMAC secret. Falls back to ADMIN_PASSWORD if no dedicated secret is set."""
    secret = ADMIN_TOKEN_SECRET or ADMIN_PASSWORD
    if not secret:
        raise HTTPException(
            status_code=500,
            detail="Admin is not configured (ADMIN_PASSWORD not set on server)",
        )
    return secret


def verify_password(submitted: str) -> bool:
    """Constant-time comparison against env var."""
    if not ADMIN_PASSWORD:
        return False
    if not submitted:
        return False
    return hmac.compare_digest(ADMIN_PASSWORD, submitted)


def issue_token() -> str:
    """Create a signed token: <issued_at_epoch>.<hex_hmac>"""
    secret = _ensure_secret()
    issued_at = str(int(time.time()))
    sig = hmac.new(
        secret.encode("utf-8"),
        issued_at.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{issued_at}.{sig}"


def verify_token(token: str) -> bool:
    """Verify token signature and freshness."""
    if not token:
        return False
    try:
        issued_at_str, sig = token.split(".", 1)
        issued_at = int(issued_at_str)
    except (ValueError, AttributeError):
        return False

    secret = _ensure_secret()
    expected = hmac.new(
        secret.encode("utf-8"),
        issued_at_str.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(expected, sig):
        return False

    age_seconds = time.time() - issued_at
    if age_seconds > ADMIN_TOKEN_TTL_HOURS * 3600:
        return False
    return True


def require_admin(authorization: Optional[str] = Header(None)) -> None:
    """FastAPI dependency — raises 401 if request is not admin-authenticated."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin token required (Bearer)",
        )
    token = authorization[len("Bearer "):].strip()
    if not verify_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired admin token",
        )
