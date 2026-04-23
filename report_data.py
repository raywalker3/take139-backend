"""Build the full context dictionary passed into the PDF/email templates.

This module reads from content.py (which loads content_library.json extracted
from the live frontend) so the PDF report mirrors exactly what the user sees
on-screen at the end of the assessment.
"""
from datetime import datetime
from typing import Optional

from content import (
    TRIGGERS,
    CORE_QUESTIONS,
    MECHANISMS,
    BREAKDOWNS,
    ORIGIN_STORIES,
    REFLECTION_QUESTIONS,
    PRAYERS,
    PERSONALIZED_TEMPLATES,
    TRIGGER_LABELS,
    MECHANISM_NAMES,
    BREAKDOWN_NAMES,
    article_for,
    lookup_wrapup_text,
    lowerstart,
)


# ─── Helpers for trigger score key normalization ───

# The frontend may send either SHM or SHAM for shame. Normalize to SHM for lookup.
_TRIGGER_KEY_ALIASES = {
    "SHAM": "SHM",
    "SHM": "SHM",
    "DIS": "DIS",
    "DISC": "DISC",
    "INJ": "INJ",
    "CTRL": "CTRL",
    "SIG": "SIG",
}

# Legacy breakdown codes we may still receive; map to the current frontend codes.
_BREAKDOWN_KEY_ALIASES = {
    "ATTY": "COURT",
    "COURT": "COURT",
    "DISAP": "DISAP",
    "FLOOD": "FLOOD",
    "GHOST": "GHOST",
    "VERD": "VERD",
    "PLEA": "PLEA",
}


def _norm_trigger_key(k: str) -> str:
    return _TRIGGER_KEY_ALIASES.get(k.upper(), k.upper())


def _norm_breakdown_key(k: str) -> str:
    return _BREAKDOWN_KEY_ALIASES.get(k.upper(), k.upper())


# ─── Personalized paragraph rendering ───

def _render_personalized(category: str, profile_key: str, wrapup_answers: Optional[dict]) -> str:
    """Fill in [SELECTED_REASON] and [TOP_RANKED] placeholders in the
    personalized template for a mechanism or breakdown.

    wrapup_answers is expected to be a dict like:
      { "mechanism": {"mc": "a", "rank": [3,0,1,4,2]},
        "breakdown": {"mc": "b", "rank": [2,1,0,3,4]} }
    (where "rank" is a list of item indexes in rank order — most-true first)

    If no wrapup answers are supplied, we still emit the template but with
    generic fallbacks so the paragraph reads naturally.
    """
    try:
        template = PERSONALIZED_TEMPLATES[category][profile_key]
    except KeyError:
        return ""

    if not template:
        return ""

    short_key = "mechanism" if category == "mechanisms" else "breakdown"
    answers = (wrapup_answers or {}).get(short_key) or {}

    # [SELECTED_REASON] — the label of the MC option the user picked
    mc_value = answers.get("mc")
    selected_reason = None
    if mc_value:
        selected_reason = lookup_wrapup_text(category, profile_key, "mc", mc_value)

    # Fallback when no answer supplied — use a generic phrase derived from the MC prompt
    if not selected_reason:
        selected_reason = "what this pattern has been doing for you under the surface"
    else:
        selected_reason = lowerstart(selected_reason.rstrip("."))

    # [TOP_RANKED] — the top-ranked item text
    rank_value = answers.get("rank")
    top_ranked = None
    if rank_value:
        items = lookup_wrapup_text(category, profile_key, "rank", rank_value)
        if items:
            top_ranked = items[0]

    if not top_ranked:
        top_ranked = "something deeper than the moment itself"
    else:
        top_ranked = lowerstart(top_ranked.rstrip("."))

    return (
        template
        .replace("[SELECTED_REASON]", selected_reason)
        .replace("[TOP_RANKED]", top_ranked)
    )


# ─── Prayer rendering ───

def _prayer_paragraphs(profile_key: str) -> list:
    """Split a prayer string (with \\n\\n separators) into paragraph list."""
    raw = PRAYERS.get(profile_key, "")
    if not raw:
        return []
    return [p.strip() for p in raw.split("\n\n") if p.strip()]


# ─── Trigger scores → sorted list of {name, score} ───

def _build_trigger_score_list(trigger_scores: dict) -> list:
    """Return list of {name, score} sorted highest-first for the score chart."""
    out = []
    for code, label in TRIGGER_LABELS.items():
        # score lookup — handle both SHM and SHAM
        score = 0
        for k in (code, "SHAM" if code == "SHM" else code):
            if k in trigger_scores and trigger_scores[k] is not None:
                score = trigger_scores[k]
                break
        try:
            score = round(float(score))
        except (TypeError, ValueError):
            score = 0
        out.append({"name": label, "score": score})
    out.sort(key=lambda r: r["score"], reverse=True)
    return out


# ─── Main entry point ───

def get_report_data(
    primary_trigger: str,
    core_question: str,
    mechanism: str,
    breakdown: str,
    trigger_scores: dict,
    home_desc: str,
    name: str,
    pair_code: str,
    wrapup_answers: Optional[dict] = None,
) -> dict:
    """Assemble the full dictionary of template variables for the PDF + email."""

    trig_key = _norm_trigger_key(primary_trigger)
    cq_key = core_question.upper()
    mech_key = mechanism.upper()
    brk_key = _norm_breakdown_key(breakdown)

    trig = TRIGGERS.get(trig_key, {})
    cq = CORE_QUESTIONS.get(cq_key, {})
    mech = MECHANISMS.get(mech_key, {})
    brk = BREAKDOWNS.get(brk_key, {})

    mech_name = MECHANISM_NAMES.get(mech_key, mech.get("name", "").replace("The ", ""))
    brk_name = BREAKDOWN_NAMES.get(brk_key, brk.get("name", "").replace("The ", ""))

    # Articles ("a Architect" → "an Architect")
    mechanism_article = article_for(mech_name)
    breakdown_article = article_for(brk_name)

    # Home description default when the intake didn't provide one
    home_desc_text = (home_desc or "").strip() or "a home I'm still making sense of"

    return {
        # Identity / meta
        "name": name or "Friend",
        "pair_code": pair_code,
        "date": datetime.now().strftime("%B %d, %Y"),
        "year": datetime.now().year,
        "home_desc": home_desc_text,

        # Trigger (primary)
        "trigger_name": trig.get("name", ""),
        "trigger_short": trig.get("short", ""),
        "trigger_desc": trig.get("desc", ""),
        "trigger_examples": trig.get("examples", ""),
        "trigger_signature": trig.get("signature", ""),

        # Core question
        "core_question_name": cq.get("name", ""),
        "core_question_short": cq.get("short", ""),
        "core_question_desc": cq.get("desc", ""),
        "core_question_why": cq.get("why", ""),
        "core_question_markers": cq.get("markers", []) or [],

        # Mechanism
        "mechanism_key": mech_key,
        "mechanism_name": mech_name,
        "mechanism_article": mechanism_article,
        # mechanism_short from the library already contains the article (e.g. "an Architect").
        "mechanism_short": mech.get("short", ""),
        "mechanism_desc": mech.get("desc", ""),
        "mechanism_full": mech.get("full", ""),
        "mechanism_markers": mech.get("markers", []) or [],
        "mechanism_partner_view": mech.get("spouseSees", ""),
        "mechanism_gospel_need": mech.get("gospelNeed", ""),
        "mechanism_personalized": _render_personalized("mechanisms", mech_key, wrapup_answers),

        # Breakdown
        "breakdown_key": brk_key,
        "breakdown_name": brk_name,
        "breakdown_article": breakdown_article,
        "breakdown_short": brk.get("short", ""),
        "breakdown_desc": brk.get("desc", ""),
        "breakdown_full": brk.get("full", ""),
        "breakdown_markers": brk.get("markers", []) or [],
        "breakdown_partner_view": brk.get("spouseSees", ""),
        "breakdown_gospel_word": brk.get("gospelWord", ""),
        "breakdown_personalized": _render_personalized("breakdowns", brk_key, wrapup_answers),

        # Gospel section (driven by the core question)
        "gospel_bridge": cq.get("bridge", ""),
        "gospel_anchor": cq.get("gospelAnchor", ""),
        "gospel_scripture": cq.get("scripture", ""),

        # Origin stories (tied to mechanism)
        "origin_stories": ORIGIN_STORIES.get(mech_key, []) or [],

        # Reflection questions (tied to mechanism)
        "reflection_questions": REFLECTION_QUESTIONS.get(mech_key, []) or [],

        # Prayer (tied to mechanism) — as list of paragraphs
        "prayer_paragraphs": _prayer_paragraphs(mech_key),

        # Trigger score list for the bar chart
        "trigger_scores": _build_trigger_score_list(trigger_scores),
    }
