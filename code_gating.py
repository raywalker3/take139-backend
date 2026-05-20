"""Code gating helpers — enforce access codes on /submit and /pair/connect.

This module is the bridge between the AccessCode system (access_codes.py)
and the public submission endpoints in main.py.

Three rules enforced here:

1. ASSESSMENT GATE: /submit requires a 'single' or 'couple' kind code that
   is currently redeemable. Couple-A and Couple-B halves are each independently
   redeemable (so each spouse can take the assessment with their own half).

2. CONNECTION GATE: /pair/connect requires either:
   (a) a 'connect' kind code (the $10 add-on, single-use), OR
   (b) a 'couple' kind code whose sibling has ALSO been redeemed —
       this is the auto-pair flow for the $40 package.

3. RE-PAIR LOCK: A submission's pair_code can only ever appear in ONE
   CouplePair row. To bond with a different partner later, the user
   must purchase a fresh 'connect' code.
"""
from datetime import datetime
from typing import Optional, Tuple

from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import (
    AccessCode, CouplePair, Submission,
    CODE_KIND_SINGLE, CODE_KIND_COUPLE, CODE_KIND_CONNECT,
    CODE_STATUS_ACTIVE, CODE_STATUS_REDEEMED,
)
import access_codes as ac


# ────────────────────────────────────────────────────────────────────────
# Assessment gate — used by /submit
# ────────────────────────────────────────────────────────────────────────

def enforce_assessment_code(
    db: Session,
    code_str: Optional[str],
    user_email: Optional[str] = None,
) -> AccessCode:
    """Verify a code can be used to take the Take 139 assessment.

    Raises HTTPException if not. Returns the AccessCode row on success
    (NOT YET REDEEMED — call mark_assessment_code_consumed() after the
    submission is committed, so we never charge a code against a
    failed submission).
    """
    if not code_str:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "access_code_required",
                "message": (
                    "Take 139 requires a valid access code. Purchase one at "
                    "https://take139.com or use a code given to you."
                ),
            },
        )

    code = ac.lookup_code(db, code_str)
    if not code:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "code_not_found",
                "message": "We don't recognize that code. Check for typos and try again.",
            },
        )

    # Only single + couple codes are valid for the assessment
    if code.kind not in (CODE_KIND_SINGLE, CODE_KIND_COUPLE):
        raise HTTPException(
            status_code=400,
            detail={
                "error": "wrong_code_kind",
                "message": (
                    f"That code is a {code.kind} code — it can't be used to take "
                    "the assessment. You need a single or couple code."
                ),
            },
        )

    ok, reason = ac.is_redeemable(code)
    if not ok:
        raise HTTPException(
            status_code=410,
            detail={"error": "code_not_redeemable", "message": reason},
        )

    return code


def mark_assessment_code_consumed(
    db: Session,
    code: AccessCode,
    submission_pair_code: str,
    user_email: Optional[str] = None,
) -> None:
    """Mark the code as redeemed AFTER the submission was successfully stored.

    Called from /submit only after the Submission row has been committed.
    """
    ac.mark_redeemed(
        db, code,
        submission_pair_code=submission_pair_code,
        redeemed_by_email=user_email,
    )


# ────────────────────────────────────────────────────────────────────────
# Connection gate — used by /pair/connect
# ────────────────────────────────────────────────────────────────────────

def enforce_connection_code(
    db: Session,
    connection_code: Optional[str],
    me_pair_code: str,
    partner_pair_code: str,
) -> AccessCode:
    """Verify a code can authorise pairing me_pair_code with partner_pair_code.

    Three accepted patterns:

    (a) connect code, active — single-use, consumed on pairing
    (b) couple code (A or B) whose SIBLING has also been redeemed by
        a different submission — the auto-pair flow for the $40 package
    (c) admin-issued connect code marked source='admin' or 'comp' — same as (a)

    Returns the AccessCode that authorised it (so the caller can mark
    it redeemed and record the authorisation on the CouplePair row).
    """
    if not connection_code:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "connection_code_required",
                "message": (
                    "Connecting two profiles requires a Connection Add-On ($10) "
                    "or a Couple Package code. Visit https://take139.com to purchase."
                ),
            },
        )

    code = ac.lookup_code(db, connection_code)
    if not code:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "code_not_found",
                "message": "We don't recognize that connection code.",
            },
        )

    # CASE A: connect kind
    if code.kind == CODE_KIND_CONNECT:
        ok, reason = ac.is_redeemable(code)
        if not ok:
            raise HTTPException(
                status_code=410,
                detail={"error": "code_not_redeemable", "message": reason},
            )
        return code

    # CASE B: couple kind — must be ALREADY-REDEEMED (used by one spouse),
    # AND its sibling must ALSO be already-redeemed (used by the other spouse).
    # That's the proof that the $40 package authorises this specific bonding.
    if code.kind == CODE_KIND_COUPLE:
        if code.status != CODE_STATUS_REDEEMED:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "couple_code_not_yet_used",
                    "message": (
                        "Both spouses must first complete their own assessment "
                        "using their half of the couple code before you can connect."
                    ),
                },
            )
        if not code.sibling_code:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "couple_code_missing_sibling",
                    "message": "This couple code has no sibling on file. Contact support.",
                },
            )
        sibling = ac.lookup_code(db, code.sibling_code)
        if not sibling:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "couple_code_missing_sibling",
                    "message": "Could not find the sibling of this couple code.",
                },
            )
        if sibling.status != CODE_STATUS_REDEEMED:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "couple_code_sibling_not_used",
                    "message": (
                        "Your spouse hasn't completed their assessment yet. "
                        "They need to take Take 139 using their half of your "
                        "couple code first; then you can connect."
                    ),
                },
            )

        # Validate the two submissions the user is trying to connect are
        # the same two that redeemed the couple code halves
        a_paircode = code.redeemed_by_submission_pair_code
        b_paircode = sibling.redeemed_by_submission_pair_code
        used_pair = {a_paircode, b_paircode}
        wanted_pair = {me_pair_code, partner_pair_code}
        if used_pair != wanted_pair:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "couple_code_not_authorised_for_these_profiles",
                    "message": (
                        "This couple code was used by a different pair of profiles. "
                        "To connect THIS profile with that one, purchase a Connection Add-On."
                    ),
                },
            )
        return code

    # CASE C: single kind code can never connect
    raise HTTPException(
        status_code=400,
        detail={
            "error": "wrong_code_kind_for_connection",
            "message": (
                f"That's a {code.kind} code — connection requires a Connect "
                "Add-On ($10) or a Couple Package code."
            ),
        },
    )


def mark_connection_code_consumed(
    db: Session,
    code: AccessCode,
    me_pair_code: str,
    partner_pair_code: str,
) -> None:
    """Consume the code after a successful pairing.

    For 'connect' codes: marked redeemed (single-use).
    For 'couple' codes: already redeemed, just record the pair_code in notes.
    """
    if code.kind == CODE_KIND_CONNECT and code.status == CODE_STATUS_ACTIVE:
        ac.mark_redeemed(
            db, code,
            submission_pair_code=f"{me_pair_code}+{partner_pair_code}",
        )
    # Couple codes were already marked redeemed at assessment time —
    # nothing more to do here.


# ────────────────────────────────────────────────────────────────────────
# Re-pair lock
# ────────────────────────────────────────────────────────────────────────

def check_repair_lock(
    db: Session,
    me_pair_code: str,
    partner_pair_code: str,
) -> None:
    """Reject the pairing if EITHER party is already paired to someone else.

    Idempotent rule: pairing me<->partner when that same pair already
    exists in CouplePair is fine (no-op). Pairing me<->X when me is
    already in a CouplePair with Y is blocked.
    """
    existing = db.query(CouplePair).filter(
        (CouplePair.pair_code_a == me_pair_code)
        | (CouplePair.pair_code_b == me_pair_code)
        | (CouplePair.pair_code_a == partner_pair_code)
        | (CouplePair.pair_code_b == partner_pair_code)
    ).all()

    for row in existing:
        ab = {row.pair_code_a, row.pair_code_b}
        wanted = {me_pair_code, partner_pair_code}
        if ab == wanted:
            # Same exact pair — idempotent, allowed
            continue
        # Different pair — one of these profiles is already bonded elsewhere
        already_bonded = me_pair_code if (me_pair_code in ab) else partner_pair_code
        raise HTTPException(
            status_code=409,
            detail={
                "error": "profile_already_paired",
                "message": (
                    f"The profile {already_bonded} is already paired with another partner. "
                    "To re-pair with a different person, purchase a Connection Add-On ($10) "
                    "at https://take139.com."
                ),
                "already_bonded_pair_code": already_bonded,
            },
        )


def record_couple_pair(
    db: Session,
    me_pair_code: str,
    partner_pair_code: str,
    authorised_by_code: Optional[str] = None,
) -> CouplePair:
    """Create the CouplePair row that locks this bond in.

    Idempotent: if the same pair already exists, returns the existing row.
    """
    existing = db.query(CouplePair).filter(
        ((CouplePair.pair_code_a == me_pair_code) & (CouplePair.pair_code_b == partner_pair_code))
        | ((CouplePair.pair_code_a == partner_pair_code) & (CouplePair.pair_code_b == me_pair_code))
    ).first()
    if existing:
        return existing

    cp = CouplePair(
        pair_code_a=me_pair_code,
        pair_code_b=partner_pair_code,
        authorised_by_code=authorised_by_code,
    )
    db.add(cp)
    db.commit()
    db.refresh(cp)
    return cp


# ────────────────────────────────────────────────────────────────────────
# Preflight check (used by frontend before user starts assessment)
# ────────────────────────────────────────────────────────────────────────

def check_code_preflight(db: Session, code_str: str) -> dict:
    """Quick validity check — no side effects.

    Returns a JSON-friendly dict telling the frontend whether the code is
    usable, what kind it is, and if it's a couple code, whether the sibling
    has been used yet.
    """
    if not code_str:
        return {"valid": False, "reason": "Please enter a code."}

    code = ac.lookup_code(db, code_str)
    if not code:
        return {"valid": False, "reason": "We don't recognize that code."}

    ok, reason = ac.is_redeemable(code)
    out = {
        "valid": ok,
        "kind": code.kind,
        "status": code.status,
        "reason": reason if not ok else "",
    }

    # Helpful extra context for couple codes
    if code.kind == CODE_KIND_COUPLE:
        sibling = ac.lookup_code(db, code.sibling_code) if code.sibling_code else None
        out["sibling_status"] = sibling.status if sibling else "unknown"
        # If the sibling exists and is redeemed, this is the second-spouse flow
        if sibling and sibling.status == CODE_STATUS_REDEEMED:
            out["is_second_spouse"] = True

    return out
