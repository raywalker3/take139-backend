"""Access code generation and management.

Codes look like:
  T139-7Q4XBA          (single,  $20)
  COUPLE-9KMRX2-A      (couple, $40, half 1 of 2)
  COUPLE-9KMRX2-B      (couple, $40, half 2 of 2)
  CONNECT-3PVH4N       (connect add-on, $10)

The random portion is 6 chars from an unambiguous alphabet (no 0/O/1/I/L).
"""
import random
import string
from datetime import datetime, timedelta
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from database import (
    AccessCode,
    CODE_KIND_SINGLE, CODE_KIND_COUPLE, CODE_KIND_CONNECT,
    CODE_STATUS_ACTIVE, CODE_STATUS_REDEEMED, CODE_STATUS_EXPIRED, CODE_STATUS_REVOKED,
    CODE_SOURCE_ADMIN, CODE_SOURCE_STRIPE, CODE_SOURCE_COMP,
)

# Unambiguous alphabet — no 0/O/1/I/L to avoid handwritten-code confusion
ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"

PRICE_CENTS = {
    CODE_KIND_SINGLE: 2000,    # $20
    CODE_KIND_COUPLE: 4000,    # $40 total (priced once per pair, both codes share)
    CODE_KIND_CONNECT: 1000,   # $10
}

PREFIX = {
    CODE_KIND_SINGLE: "T139",
    CODE_KIND_COUPLE: "COUPLE",
    CODE_KIND_CONNECT: "CONNECT",
}


def _random_token(length: int = 6) -> str:
    return "".join(random.choice(ALPHABET) for _ in range(length))


def _generate_unique(db: Session, prefix: str, suffix: str = "") -> str:
    """Generate a code with prefix that doesn't collide in DB."""
    for _ in range(50):
        code = f"{prefix}-{_random_token()}"
        if suffix:
            code = f"{code}-{suffix}"
        existing = db.query(AccessCode).filter(AccessCode.code == code).first()
        if not existing:
            return code
    raise RuntimeError(f"Could not generate unique code with prefix {prefix} after 50 tries")


def create_single_code(
    db: Session,
    *,
    source: str = CODE_SOURCE_ADMIN,
    batch_label: Optional[str] = None,
    notes: Optional[str] = None,
    expires_in_days: Optional[int] = None,
    price_cents: Optional[int] = None,
    stripe_session_id: Optional[str] = None,
    stripe_customer_email: Optional[str] = None,
) -> AccessCode:
    """Create one T139-XXXXX code."""
    code_str = _generate_unique(db, PREFIX[CODE_KIND_SINGLE])
    expires_at = (
        datetime.utcnow() + timedelta(days=expires_in_days)
        if expires_in_days else None
    )
    code = AccessCode(
        code=code_str,
        kind=CODE_KIND_SINGLE,
        status=CODE_STATUS_ACTIVE,
        source=source,
        price_cents=price_cents if price_cents is not None else PRICE_CENTS[CODE_KIND_SINGLE],
        batch_label=batch_label,
        notes=notes,
        expires_at=expires_at,
        stripe_session_id=stripe_session_id,
        stripe_customer_email=stripe_customer_email,
    )
    db.add(code)
    db.commit()
    db.refresh(code)
    return code


def create_couple_code_pair(
    db: Session,
    *,
    source: str = CODE_SOURCE_ADMIN,
    batch_label: Optional[str] = None,
    notes: Optional[str] = None,
    expires_in_days: Optional[int] = None,
    stripe_session_id: Optional[str] = None,
    stripe_customer_email: Optional[str] = None,
) -> Tuple[AccessCode, AccessCode]:
    """Create a paired COUPLE-XXXXX-A and COUPLE-XXXXX-B (one $40 purchase)."""
    # Generate a shared root token, then suffix A and B
    for _ in range(50):
        root = _random_token()
        code_a_str = f"COUPLE-{root}-A"
        code_b_str = f"COUPLE-{root}-B"
        a_exists = db.query(AccessCode).filter(AccessCode.code == code_a_str).first()
        b_exists = db.query(AccessCode).filter(AccessCode.code == code_b_str).first()
        if not a_exists and not b_exists:
            break
    else:
        raise RuntimeError("Could not generate unique couple code pair after 50 tries")

    expires_at = (
        datetime.utcnow() + timedelta(days=expires_in_days)
        if expires_in_days else None
    )

    # Both halves carry the full price ($40) on the A code; B is the sibling
    code_a = AccessCode(
        code=code_a_str,
        kind=CODE_KIND_COUPLE,
        status=CODE_STATUS_ACTIVE,
        source=source,
        price_cents=PRICE_CENTS[CODE_KIND_COUPLE],  # full $40 on the purchaser-facing A code
        batch_label=batch_label,
        notes=notes,
        sibling_code=code_b_str,
        expires_at=expires_at,
        stripe_session_id=stripe_session_id,
        stripe_customer_email=stripe_customer_email,
    )
    code_b = AccessCode(
        code=code_b_str,
        kind=CODE_KIND_COUPLE,
        status=CODE_STATUS_ACTIVE,
        source=source,
        price_cents=0,  # B is the sibling, included in A's price
        batch_label=batch_label,
        notes=notes,
        sibling_code=code_a_str,
        expires_at=expires_at,
        stripe_session_id=stripe_session_id,
        stripe_customer_email=stripe_customer_email,
    )
    db.add(code_a)
    db.add(code_b)
    db.commit()
    db.refresh(code_a)
    db.refresh(code_b)
    return code_a, code_b


def create_connect_code(
    db: Session,
    *,
    source: str = CODE_SOURCE_ADMIN,
    batch_label: Optional[str] = None,
    notes: Optional[str] = None,
    expires_in_days: Optional[int] = None,
    price_cents: Optional[int] = None,
    stripe_session_id: Optional[str] = None,
    stripe_customer_email: Optional[str] = None,
) -> AccessCode:
    """Create one CONNECT-XXXXX code."""
    code_str = _generate_unique(db, PREFIX[CODE_KIND_CONNECT])
    expires_at = (
        datetime.utcnow() + timedelta(days=expires_in_days)
        if expires_in_days else None
    )
    code = AccessCode(
        code=code_str,
        kind=CODE_KIND_CONNECT,
        status=CODE_STATUS_ACTIVE,
        source=source,
        price_cents=price_cents if price_cents is not None else PRICE_CENTS[CODE_KIND_CONNECT],
        batch_label=batch_label,
        notes=notes,
        expires_at=expires_at,
        stripe_session_id=stripe_session_id,
        stripe_customer_email=stripe_customer_email,
    )
    db.add(code)
    db.commit()
    db.refresh(code)
    return code


def lookup_code(db: Session, code_str: str) -> Optional[AccessCode]:
    """Find a code by its string. Case-insensitive, trims whitespace."""
    if not code_str:
        return None
    normalized = code_str.strip().upper()
    return db.query(AccessCode).filter(AccessCode.code == normalized).first()


def is_redeemable(code: AccessCode) -> Tuple[bool, str]:
    """Check if a code can currently be used.

    Returns (ok, reason). If ok is False, reason explains why.
    """
    if code.status == CODE_STATUS_REDEEMED:
        return False, "This code has already been used."
    if code.status == CODE_STATUS_REVOKED:
        return False, "This code has been revoked."
    if code.status == CODE_STATUS_EXPIRED:
        return False, "This code has expired."
    if code.expires_at and code.expires_at < datetime.utcnow():
        return False, "This code has expired."
    if code.status != CODE_STATUS_ACTIVE:
        return False, f"This code is not active (status: {code.status})."
    return True, ""


def mark_redeemed(
    db: Session,
    code: AccessCode,
    *,
    submission_pair_code: Optional[str] = None,
    redeemed_by_email: Optional[str] = None,
) -> AccessCode:
    """Mark a code as redeemed by a specific submission/user."""
    code.status = CODE_STATUS_REDEEMED
    code.redeemed_at = datetime.utcnow()
    if submission_pair_code:
        code.redeemed_by_submission_pair_code = submission_pair_code
    if redeemed_by_email:
        code.redeemed_by_email = redeemed_by_email
    db.commit()
    db.refresh(code)
    return code


def revoke_code(db: Session, code: AccessCode, reason: Optional[str] = None) -> AccessCode:
    """Manually kill a code."""
    code.status = CODE_STATUS_REVOKED
    if reason:
        code.notes = (code.notes or "") + f"\n[REVOKED] {reason}"
    db.commit()
    db.refresh(code)
    return code


def sweep_expired(db: Session) -> int:
    """Mark codes past expires_at as expired. Returns number swept."""
    now = datetime.utcnow()
    q = db.query(AccessCode).filter(
        AccessCode.status == CODE_STATUS_ACTIVE,
        AccessCode.expires_at != None,  # noqa: E711
        AccessCode.expires_at < now,
    )
    count = 0
    for code in q.all():
        code.status = CODE_STATUS_EXPIRED
        count += 1
    if count:
        db.commit()
    return count


def code_to_dict(code: AccessCode) -> dict:
    """JSON-friendly representation for the admin UI."""
    return {
        "id": code.id,
        "code": code.code,
        "kind": code.kind,
        "status": code.status,
        "source": code.source,
        "price_cents": code.price_cents,
        "batch_label": code.batch_label,
        "notes": code.notes,
        "sibling_code": code.sibling_code,
        "stripe_session_id": code.stripe_session_id,
        "stripe_customer_email": code.stripe_customer_email,
        "created_at": code.created_at.isoformat() if code.created_at else None,
        "expires_at": code.expires_at.isoformat() if code.expires_at else None,
        "redeemed_at": code.redeemed_at.isoformat() if code.redeemed_at else None,
        "redeemed_by_submission_pair_code": code.redeemed_by_submission_pair_code,
        "redeemed_by_email": code.redeemed_by_email,
    }
