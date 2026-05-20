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


def build_personal_walkthrough(submission) -> bytes:
    """Generate the personal walkthrough PDF for one submission.

    Looks up the (mechanism, breakdown) builder in the registry;
    if absent, returns the friendly fallback PDF.
    """
    ensure_fonts()
    key = (
        (submission.primary_mechanism or "").upper(),
        (submission.primary_breakdown or "").upper(),
    )
    builder = PERSONAL_REGISTRY.get(key)
    if builder is None:
        return build_personal_fallback(submission)
    return builder(submission)


def build_couples_walkthrough(sub_a, sub_b) -> bytes:
    """Generate the couples walkthrough PDF for a paired submission.

    Tries both (mech_a, mech_b) orderings. If neither has a builder,
    returns the friendly fallback PDF.
    """
    ensure_fonts()
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
