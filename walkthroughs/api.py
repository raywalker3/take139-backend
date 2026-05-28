"""Top-level API for walkthrough generation.

Dispatches to the right builder based on profile, with a graceful fallback
PDF for profiles/pairs that haven't been written yet.

Submission shape (what we expect from the Submission row):
    submission.name              -> str
    submission.email             -> str | None
    submission.pair_code         -> str (e.g. "ANCHOR-4829")
    submission.primary_mechanism -> short code (e.g. "ARCH", "ISLE", ...)
    submission.primary_breakdown -> short code (e.g. "ATTY", "FLOOD", ...)
    submission.primary_trigger   -> short code (e.g. "DIS", "SIG", ...)
    submission.core_question     -> short code (e.g. "PROT", "SIG", ...)
"""
from typing import Optional

from .base import ensure_fonts
from .personal import PERSONAL_REGISTRY
from .couples import COUPLES_REGISTRY
from .fallback import build_personal_fallback, build_couples_fallback


def _hydrate_submission_name(submission, db=None) -> None:
    """Ensure submission.name is populated before a walkthrough is rendered.

    Bug we are fixing: signed-in users could complete the assessment without
    the intake form re-asking for their name, leaving Submission.name as NULL.
    The walkthrough builders then fell back to defaults like 'Island' or
    'Architect', producing impersonal PDFs that called the user by their
    archetype instead of their actual name.

    Lookup order:
      1. submission.name (already set — nothing to do)
      2. User.name where User.email matches AccessCode.redeemed_by_email
      3. User.name where User.email matches submission.email
      4. AccessCode.redeemed_by_email local-part (e.g. 'carolyn' from
         'carolyn@example.com') as a humanizing last resort
      5. Leave None and let the builder default kick in

    Mutates the submission in place so every builder sees the resolved name.
    """
    if submission is None:
        return
    if submission.name and submission.name.strip():
        return  # already populated, leave it
    if db is None:
        return  # no DB session, nothing we can do

    # Local imports to avoid circular dependency with database.py at module load
    from database import User, AccessCode

    candidate_email = None

    # 2. Look up the access code used and find the user who redeemed it
    if submission.access_code_used:
        ac = (
            db.query(AccessCode)
              .filter(AccessCode.code == submission.access_code_used)
              .first()
        )
        if ac and ac.redeemed_by_email:
            candidate_email = ac.redeemed_by_email.strip().lower()

    # 3. Fall back to submission.email if available
    if not candidate_email and submission.email:
        candidate_email = submission.email.strip().lower()

    if candidate_email:
        user = db.query(User).filter(User.email == candidate_email).first()
        if user and user.name and user.name.strip():
            submission.name = user.name.strip()
            return

        # 4. Humanizing last resort: capitalize the email local-part. This
        # avoids the worst case (a walkthrough that calls Carolyn 'Island')
        # without inventing facts. 'carolyn.hilken@gmail.com' -> 'Carolyn'.
        local = candidate_email.split("@", 1)[0]
        # take just the first segment before '.' or '_' or '+'
        for sep in (".", "_", "+", "-"):
            local = local.split(sep, 1)[0]
        if local and local.isalpha():
            submission.name = local.capitalize()
            return

    # 5. Leave None; the builder's default ("Spouse", archetype name) will kick in.


def build_personal_walkthrough(submission, db=None) -> bytes:
    """Generate the personal walkthrough PDF for one submission.

    Looks up the (mechanism, breakdown) builder in the registry;
    if absent, returns the friendly fallback PDF.

    Pass `db` (a SQLAlchemy session) so we can resolve the user's real name
    when Submission.name is blank — a common case for signed-in users whose
    intake skipped re-asking. Without `db`, falls back to whatever name is
    on the Submission row (or the builder's default).
    """
    ensure_fonts()
    _hydrate_submission_name(submission, db)
    key = (
        (submission.primary_mechanism or "").upper(),
        (submission.primary_breakdown or "").upper(),
    )
    builder = PERSONAL_REGISTRY.get(key)
    if builder is None:
        return build_personal_fallback(submission)
    return builder(submission)


def build_couples_walkthrough(sub_a, sub_b, db=None) -> bytes:
    """Generate the couples walkthrough PDF for a paired submission.

    Tries both (mech_a, mech_b) orderings. If neither has a builder,
    returns the friendly fallback PDF.

    Pass `db` (a SQLAlchemy session) so we can resolve real first names for
    both partners when Submission.name is blank. Without `db`, falls back
    to whatever name is on each Submission row (or the builder's default).
    """
    ensure_fonts()
    _hydrate_submission_name(sub_a, db)
    _hydrate_submission_name(sub_b, db)
    mech_a = (sub_a.primary_mechanism or "").upper()
    mech_b = (sub_b.primary_mechanism or "").upper()

    # Try both orderings — the writer who composed the pair PDF made a choice
    # about which partner gets which color/voice; we preserve it.
    builder = COUPLES_REGISTRY.get((mech_a, mech_b))
    if builder:
        return builder(sub_a, sub_b)
    builder = COUPLES_REGISTRY.get((mech_b, mech_a))
    if builder:
        return builder(sub_b, sub_a)  # swap to match the writer's ordering

    return build_couples_fallback(sub_a, sub_b)


def has_personal_writeup(submission) -> bool:
    """Tells the caller whether a real walkthrough exists for this profile,
    vs. just the fallback. Useful for email copy ('your walkthrough is ready'
    vs. 'we'll send it to you within a few days')."""
    key = (
        (submission.primary_mechanism or "").upper(),
        (submission.primary_breakdown or "").upper(),
    )
    return key in PERSONAL_REGISTRY


def has_couples_writeup(sub_a, sub_b) -> bool:
    mech_a = (sub_a.primary_mechanism or "").upper()
    mech_b = (sub_b.primary_mechanism or "").upper()
    return (mech_a, mech_b) in COUPLES_REGISTRY or (mech_b, mech_a) in COUPLES_REGISTRY
