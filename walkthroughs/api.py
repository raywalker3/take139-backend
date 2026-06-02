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
from .couples_neutral import build_neutral_couples_walkthrough


# Which gender combination does each gendered pair file assume?
# Values are (gender_of_first_position, gender_of_second_position) in the
# registry key's order. If the actual pair doesn't match this, we route to
# the gender-neutral walkthrough instead so we never email someone a PDF
# where the prose calls them "he" when they are "she".
#
# All current pair files were written with male+female assumptions. As
# rewrites land, this table is what we update — set to None for any pair
# whose prose has been made gender-aware.
GENDER_ASSUMPTION = {
    ("ARCH", "ARCH"):  None,         # same-mechanism; prose is symmetric
    ("ARCH", "ISLE"):  ("M", "F"),   # Architect=M, Island=F (Chris+Carolyn)
    ("ARCH", "AMB"):   ("M", "F"),
    ("ARCH", "VAULT"): ("M", "F"),
    ("ARCH", "ADPT"):  ("M", "F"),
    ("ARCH", "CAMP"):  ("M", "F"),
    ("ISLE", "ISLE"):  None,
    ("AMB", "ISLE"):   ("M", "F"),
    ("ISLE", "VAULT"): ("M", "F"),  # Note: writer's positional choice may vary
    ("ADPT", "ISLE"):  ("M", "F"),
    ("ISLE", "CAMP"):  ("M", "F"),
    ("AMB", "AMB"):    None,
    ("AMB", "VAULT"):  ("M", "F"),
    ("ADPT", "AMB"):   ("M", "F"),
    ("AMB", "CAMP"):   ("M", "F"),
    ("VAULT", "VAULT"): None,
    ("ADPT", "VAULT"): ("M", "F"),
    ("CAMP", "VAULT"): ("M", "F"),
    ("ADPT", "ADPT"):  None,
    ("ADPT", "CAMP"):  ("M", "F"),
    ("CAMP", "CAMP"):  None,
}


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


# Normalization tables so frontend code-name drift never breaks the dispatch.
# The frontend assessment emits codes like COURT/DISAP/REM for breakdowns the
# backend registry was originally keyed under ATTY/GHOST/VERD. Mismatches
# silently fall through to the friendly fallback, which means a user with a
# perfectly valid combination (e.g. ISLE+COURT) gets a generic stub instead of
# their real walkthrough — AND the email never sends, because PDF generation
# is upstream of the email send block in /submit.
_BREAKDOWN_ALIAS = {
    "COURT": "ATTY",   # Courtroom → Attorney (canonical registry key)
    "DISAP": "GHOST",  # Disappear → Ghost
    "REM":   "VERD",   # Remember-everything → Verdict-rendering
}
_MECHANISM_ALIAS = {
    "CAMP":  "ADPT",   # Campsite → Adapter (legacy code, just in case)
    "PERF":  "AMB",    # Performance → Ambassador (legacy code, just in case)
}


def _normalize_mechanism(m: str) -> str:
    m = (m or "").upper()
    return _MECHANISM_ALIAS.get(m, m)


def _normalize_breakdown(b: str) -> str:
    b = (b or "").upper()
    return _BREAKDOWN_ALIAS.get(b, b)


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
        _normalize_mechanism(submission.primary_mechanism),
        _normalize_breakdown(submission.primary_breakdown),
    )
    builder = PERSONAL_REGISTRY.get(key)
    if builder is None:
        # Helpful diagnostic in Railway logs for future drift detection.
        print(
            f"[WALKTHROUGH] No personal builder for {key} "
            f"(original: mech={submission.primary_mechanism!r}, "
            f"breakdown={submission.primary_breakdown!r}). Falling back."
        )
        return build_personal_fallback(submission)
    return builder(submission)


def _gender_match(actual: tuple, assumed: tuple) -> bool:
    """True iff the actual gender pair matches the assumed pair exactly.

    Both partners must have a known gender ('M' or 'F'). If either side is
    None, 'X', or anything else, we say no — and route to neutral.
    """
    if not assumed:
        return False  # safe default: no assumption known
    g_a, g_b = actual
    if g_a not in ("M", "F") or g_b not in ("M", "F"):
        return False
    return (g_a, g_b) == assumed


def build_couples_walkthrough(sub_a, sub_b, db=None) -> bytes:
    """Generate the couples walkthrough PDF for a paired submission.

    Routing logic:
      1. If both partners have known genders matching the writer's assumed
         gender combo, use the specific gendered walkthrough.
      2. Otherwise (any unknown gender, same-mechanism, or gender combo that
         doesn't match the prose), use the gender-neutral walkthrough.
      3. If we don't have either (no mechanism keys at all), fall through to
         the 'in preparation' fallback.

    Pass `db` (a SQLAlchemy session) so we can resolve real first names for
    both partners when Submission.name is blank.
    """
    ensure_fonts()
    _hydrate_submission_name(sub_a, db)
    _hydrate_submission_name(sub_b, db)
    mech_a = _normalize_mechanism(sub_a.primary_mechanism)
    mech_b = _normalize_mechanism(sub_b.primary_mechanism)

    g_a = (getattr(sub_a, "gender", None) or "").upper() or None
    g_b = (getattr(sub_b, "gender", None) or "").upper() or None

    # Same-mechanism pairs have no gender assumption — prose is symmetric
    # for those, so we use the gendered file for any combo.
    if mech_a == mech_b:
        builder = COUPLES_REGISTRY.get((mech_a, mech_b))
        if builder:
            return builder(sub_a, sub_b)
        return build_neutral_couples_walkthrough(sub_a, sub_b)

    # Cross-mechanism: check both registry orderings, gate on gender match
    key_ab = (mech_a, mech_b)
    key_ba = (mech_b, mech_a)

    if key_ab in COUPLES_REGISTRY:
        assumed = GENDER_ASSUMPTION.get(key_ab)
        # If assumption is None, the writer has marked the file as fully
        # gender-aware; use it for any combo.
        if assumed is None or _gender_match((g_a, g_b), assumed):
            return COUPLES_REGISTRY[key_ab](sub_a, sub_b)

    if key_ba in COUPLES_REGISTRY:
        assumed = GENDER_ASSUMPTION.get(key_ba)
        # Note: in the swapped case, sub_b takes the first position in the
        # writer's file, so the gender check is (g_b, g_a).
        if assumed is None or _gender_match((g_b, g_a), assumed):
            return COUPLES_REGISTRY[key_ba](sub_b, sub_a)

    # We have a written walkthrough but the gender combo doesn't match.
    # Use the substantive neutral version, NOT the 'coming soon' fallback.
    print(
        f"[COUPLES WALKTHROUGH] Routing to neutral for ({mech_a}, {mech_b}) "
        f"with genders ({g_a}, {g_b}). Writer's assumption didn't match."
    )
    return build_neutral_couples_walkthrough(sub_a, sub_b)


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
