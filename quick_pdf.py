"""Admin quick-PDF generation.

Lets the admin build a Personal Report PDF, a Walkthrough PDF, or a
Couples Report PDF from a hand-selected (trigger, core_question,
mechanism, breakdown) tuple — without anyone taking the assessment.

Used for cases where Chris already knows someone's profile (counseling
clients, conference walk-ups, marketing samples, etc.) and just wants
the deliverable.

A "GhostSubmission" is an in-memory object that mimics the Submission
shape (the fields the PDF generator + walkthrough builders read), but
is never persisted to the database. Real assessment data is untouched.
"""
from __future__ import annotations
import json
import random
import string
from datetime import datetime
from typing import Optional


# Canonical option lists, sourced from the live content library + walkthroughs
# registry. These are the SINGLE source of truth the admin UI binds to.

TRIGGERS = [
    {"code": "DIS",  "name": "Disrespect"},
    {"code": "DISC", "name": "Disconnection"},
    {"code": "INJ",  "name": "Injustice"},
    {"code": "CTRL", "name": "Control"},
    {"code": "SHAM", "name": "Shame"},     # canonical key (was SHM legacy)
    {"code": "SIG",  "name": "Significance"},
]

CORE_QUESTIONS = [
    {"code": "COMP", "name": "Am I competent?"},
    {"code": "LOV",  "name": "Am I lovable?"},
    {"code": "PROT", "name": "Am I protected?"},
    {"code": "FREE", "name": "Am I free?"},
    {"code": "ACC",  "name": "Am I acceptable?"},
    {"code": "SIG",  "name": "Am I significant?"},  # canonical (was REM legacy)
]

# Legacy aliases we still accept on input — so admins typing 'SHM' or 'REM'
# from older docs don't get a 400. The validator normalizes these UP-FRONT
# (BEFORE the validity check) so downstream code always sees canonical keys.
_INPUT_ALIASES = {
    "SHM":   "SHAM",   # legacy trigger code
    "REM":   "SIG",    # legacy core question code
    "COURT": "ATTY",   # legacy breakdown
    "DISAP": "GHOST",  # legacy breakdown
}


def _canon(code: str) -> str:
    if not code:
        return code
    upper = code.strip().upper()
    return _INPUT_ALIASES.get(upper, upper)

MECHANISMS = [
    {"code": "ARCH",  "name": "The Architect"},
    {"code": "ISLE",  "name": "The Island"},
    {"code": "AMB",   "name": "The Ambassador"},
    {"code": "VAULT", "name": "The Vault"},
    {"code": "ADPT",  "name": "The Adapter"},
    {"code": "CAMP",  "name": "The Performance"},
]

# Canonical walkthroughs-registry breakdown keys (NOT the legacy COURT/DISAP).
BREAKDOWNS = [
    {"code": "ATTY",  "name": "The Attorney"},
    {"code": "GHOST", "name": "The Ghost"},
    {"code": "FLOOD", "name": "The Flood"},
    {"code": "MASK",  "name": "The Mask"},
    {"code": "VERD",  "name": "The Quiet Exit"},
    {"code": "PLEA",  "name": "The Plea"},
]


# Set lookups for fast validation.
_VALID_TRIGGERS = {t["code"] for t in TRIGGERS}
_VALID_CQ = {q["code"] for q in CORE_QUESTIONS}
_VALID_MECH = {m["code"] for m in MECHANISMS}
_VALID_BD = {b["code"] for b in BREAKDOWNS}


# Whimsical word pool for ghost pair codes.
_PAIR_WORDS = [
    "ANCHOR", "BEACON", "COMPASS", "EMBER", "FOREST", "HARBOR", "HEARTH",
    "JOURNEY", "LANTERN", "MEADOW", "PRAIRIE", "RIVER", "SAILOR", "SUNRISE",
    "VALLEY", "WILLOW",
]


def make_sample_pair_code() -> str:
    """A fake pair code in the same shape as a real one (WORD-####)."""
    word = random.choice(_PAIR_WORDS)
    digits = "".join(random.choices(string.digits, k=4))
    return f"{word}-{digits}"


class GhostSubmission:
    """In-memory stand-in for the SQLAlchemy Submission model.

    Implements only the attributes the PDF generator + walkthrough builders
    actually read. Created from admin form input — never persisted.
    """

    def __init__(
        self,
        name: str,
        primary_trigger: str,
        primary_core_question: str,
        primary_mechanism: str,
        primary_breakdown: str,
        email: Optional[str] = None,
        pair_code: Optional[str] = None,
    ):
        self.id = None
        self.name = (name or "Friend").strip() or "Friend"
        self.email = (email or "").strip() or None
        self.pair_code = pair_code or make_sample_pair_code()
        self.access_code_used = None
        self.primary_trigger = (primary_trigger or "").upper()
        self.primary_core_question = (primary_core_question or "").upper()
        self.primary_mechanism = (primary_mechanism or "").upper()
        self.primary_breakdown = (primary_breakdown or "").upper()
        # Pair / couple linkage — not relevant for ghost; PDFs work without it.
        self.paired_with_code = None
        self.paired_at = None
        # Empty intake / wrap-up answers — walkthrough text falls back to the
        # canonical (non-personalized) variant when wrap-up answers are absent.
        self.intake_json = json.dumps({"family_type": "", "atmosphere": []})
        self.answers_json = "{}"
        # Trigger-score breakdown for the bar chart. Pin the chosen trigger at
        # 100% and everything else at 0% so the visual still works.
        scores = {t["code"]: 0 for t in TRIGGERS}
        if self.primary_trigger in scores:
            scores[self.primary_trigger] = 100
        # The TRIGGERS list now uses 'SHAM' canonically; the SHM→SHAM
        # normalization that lived here for legacy clients is no longer
        # needed because _canon() runs upstream. Leaving the no-op so any
        # legacy caller that hand-builds a GhostSubmission still survives.
        if "SHM" in scores and "SHAM" not in scores:
            scores["SHAM"] = scores.pop("SHM")
        self.results_json = json.dumps({
            "primary_trigger": self.primary_trigger,
            "core_question": self.primary_core_question,
            "mechanism": self.primary_mechanism,
            "breakdown": self.primary_breakdown,
            "trigger_scores": scores,
            "home_desc": "",
            "wrapup_answers": None,
        })
        self.created_at = datetime.utcnow()
        self.emailed_to_user = False
        self.emailed_to_admin = False


class ValidationError(ValueError):
    """Raised when a quick-PDF input is invalid; caller maps to HTTP 400."""
    pass


def validate_profile(*, trigger: str, core_question: str,
                     mechanism: str, breakdown: str) -> None:
    t = _canon(trigger)
    cq = _canon(core_question)
    m = _canon(mechanism)
    b = _canon(breakdown)
    if t not in _VALID_TRIGGERS:
        raise ValidationError(f"Unknown trigger code: {trigger!r}")
    if cq not in _VALID_CQ:
        raise ValidationError(f"Unknown core-question code: {core_question!r}")
    if m not in _VALID_MECH:
        raise ValidationError(f"Unknown mechanism code: {mechanism!r}")
    if b not in _VALID_BD:
        raise ValidationError(f"Unknown breakdown code: {breakdown!r}")


def build_ghost_submission(
    *,
    name: str,
    trigger: str,
    core_question: str,
    mechanism: str,
    breakdown: str,
    email: Optional[str] = None,
) -> GhostSubmission:
    """One-line constructor with validation. Canonicalizes legacy aliases
    (SHM→SHAM, REM→SIG, COURT→ATTY, DISAP→GHOST) BEFORE building the ghost.
    Bug 2026-06-01: admin picking 'Shame' was sending 'SHM' but downstream
    code expects 'SHAM' — producing a manual PDF that didn't match the
    selected trigger.
    """
    trigger = _canon(trigger)
    core_question = _canon(core_question)
    mechanism = _canon(mechanism)
    breakdown = _canon(breakdown)
    validate_profile(
        trigger=trigger, core_question=core_question,
        mechanism=mechanism, breakdown=breakdown,
    )
    return GhostSubmission(
        name=name,
        primary_trigger=trigger,
        primary_core_question=core_question,
        primary_mechanism=mechanism,
        primary_breakdown=breakdown,
        email=email,
    )
