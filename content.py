"""Content library loader — reads content_library.json extracted from the frontend.

Single source of truth for all trigger/question/mechanism/breakdown descriptions,
wrap-up questions, personalized templates, origin stories, reflections, prayers.

Category codes match the frontend exactly:
  Triggers:    DIS, DISC, INJ, CTRL, SHM, SIG
  Questions:   COMP, LOV, PROT, FREE, ACC, REM
  Mechanisms:  ARCH, ISLE, AMB, VAULT, ADPT, CAMP
  Breakdowns:  COURT, DISAP, FLOOD, GHOST, VERD, PLEA
"""
import json
import os

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_CONTENT_PATH = os.path.join(_THIS_DIR, "content_library.json")

with open(_CONTENT_PATH, "r", encoding="utf-8") as _f:
    _DATA = json.load(_f)

TRIGGERS = _DATA["TRIGGERS"]
CORE_QUESTIONS = _DATA["CORE_QUESTIONS"]
MECHANISMS = _DATA["MECHANISMS"]
BREAKDOWNS = _DATA["BREAKDOWNS"]
WRAPUP_QUESTIONS = _DATA["WRAPUP_QUESTIONS"]
PERSONALIZED_TEMPLATES = _DATA["PERSONALIZED_TEMPLATES"]
ORIGIN_STORIES = _DATA["ORIGIN_STORIES"]
REFLECTION_QUESTIONS = _DATA["REFLECTION_QUESTIONS"]
PRAYERS = _DATA["PRAYERS"]

# Friendly labels for the radar chart / score display
TRIGGER_LABELS = {
    "DIS": "Disrespect",
    "DISC": "Disconnection",
    "INJ": "Injustice",
    "CTRL": "Control",
    "SHM": "Shame",
    "SIG": "Significance",
}

MECHANISM_NAMES = {
    "ARCH": "Architect",
    "ISLE": "Island",
    "AMB": "Ambassador",
    "VAULT": "Vault",
    "ADPT": "Adapter",
    "CAMP": "Campaign",
}

BREAKDOWN_NAMES = {
    "COURT": "Attorney",  # Renamed from Courtroom per Chris's request
    "DISAP": "Disappearance",
    "FLOOD": "Flood",
    "GHOST": "Ghost",
    "VERD": "Verdict",
    "PLEA": "Plea",
}


def article_for(noun: str) -> str:
    """Return 'a' or 'an' for English articles."""
    if not noun:
        return "a"
    return "an" if noun[0].lower() in "aeiou" else "a"


def lookup_wrapup_text(category: str, kind: str, q_key: str, answer_value):
    """Given a mechanism/breakdown wrap-up answer, return the human-readable text.

    Args:
        category: one of 'mechanisms' or 'breakdowns'
        kind: the profile key (e.g. 'ARCH', 'COURT')
        q_key: 'mc' or 'rank'
        answer_value: for mc -> option value string ('a', 'b', ...); for rank -> list of indexes

    Returns:
        For mc: the label string of the selected option
        For rank: list of item strings in rank order
    """
    try:
        q = WRAPUP_QUESTIONS[category][kind][q_key]
    except KeyError:
        return None

    if q_key == "mc":
        # options is a list of {label, value}
        for opt in q.get("options", []):
            if opt.get("value") == answer_value:
                return opt.get("label", "")
        return None

    if q_key == "rank":
        items = q.get("items", [])
        if not isinstance(answer_value, list):
            return items
        # Rank order: the answer is indexes in rank order OR a list with rank-index values
        # Frontend stores rank as {itemIndex: rankNumber}; we may receive either
        # If it's a list of indexes in order, use directly
        if all(isinstance(x, int) for x in answer_value):
            # If max(answer_value) < len(items), treat as index-order
            try:
                return [items[i] for i in answer_value if 0 <= i < len(items)]
            except Exception:
                return items
        return items
    return None


def lowerstart(s: str) -> str:
    """Lowercase the first letter, preserving 'I' as pronoun."""
    if not s:
        return s
    if s.startswith("I "):
        return s  # keep "I ..." intact
    return s[0].lower() + s[1:]
