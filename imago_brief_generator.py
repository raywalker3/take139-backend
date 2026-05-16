"""IMAGO Brief (one-page) generator.

Produces a single-page PDF that surfaces the headline shape + letter + archetype
plus 3-4 bullets per domain. The full report is the long-form companion.

Public API
----------
    generate_imago_brief_pdf(result, name, pair_code) -> bytes
    generate_imago_brief_html(result, name, pair_code) -> str  (for preview)
"""
from __future__ import annotations

import os
from datetime import date
from typing import Dict, List

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from imago_report_data import get_report_data
from imago_scoring import ImagoResult


_HERE = os.path.dirname(os.path.abspath(__file__))
_TEMPLATE_DIR = os.path.join(_HERE, "templates")


def _ordinal_suffix(n):
    n = int(n)
    if 10 <= (n % 100) <= 20:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def _ordinal(n):
    return f"{int(n)}{_ordinal_suffix(n)}"


_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), autoescape=False)
_env.filters["ordinal"] = _ordinal
_env.filters["ordinal_suffix"] = _ordinal_suffix
_template = _env.get_template("imago_brief.html")


# ─────────────────────────────────────────────────────────────────────────────
# Bullet generation per domain × pole.
# Each domain gets 3 short bullets. We pick the bullets from the existing
# v2 domain content if available, but provide solid defaults too.
# ─────────────────────────────────────────────────────────────────────────────

# Manually-curated, layperson, one-line domain bullets per pole.
# These are intentionally short and behavioral so the brief reads at a glance.
DOMAIN_BULLETS: Dict[str, Dict[str, List[str]]] = {
    "I": {
        "high": [
            "You think in pictures, possibilities, and what-ifs.",
            "Beauty and ideas register on you — they don't just decorate the day, they move it.",
            "You can hold complexity without rushing it to a tidy answer.",
        ],
        "low": [
            "You prefer the proven path over the speculative one.",
            "You don't need novelty to be engaged — the familiar is enough.",
            "Your strength is steadiness in what is, rather than reaching for what could be.",
        ],
    },
    "M": {
        "high": [
            "You finish what you start. Promises kept; details handled.",
            "You bring order to rooms, schedules, and projects without being asked.",
            "You can be counted on — the kind of person who actually does the thing.",
        ],
        "low": [
            "You move by inspiration more than by checklist.",
            "Routine and follow-through can feel like a tax; you may need scaffolding around them.",
            "Your gift is flexibility — the cost is the slipped detail.",
        ],
    },
    "A": {
        "high": [
            "You bring energy into a room; people feel the lift.",
            "You speak up, take the lead, and don't wait to be invited.",
            "You think out loud and find clarity in motion.",
        ],
        "low": [
            "You recharge in quiet; crowds drain rather than refill you.",
            "You hold back from leading until you're sure — sometimes too long.",
            "Your gift is depth over volume; you say less, but you mean it.",
        ],
    },
    "G": {
        "high": [
            "You feel what others feel — and you act on it.",
            "You instinctively soften, defer, and protect the dignity of the people in front of you.",
            "Your default is warmth; sharp words cost you something.",
        ],
        "low": [
            "You say the true thing even when it costs you the room.",
            "You don't soften easily — directness reads as honesty, not unkindness, to you.",
            "Watch the shadow: truth without warmth can wound the person it most needed to reach.",
        ],
    },
    "O": {
        "high": [
            "Your inner weather is settled — circumstances move, but you don't.",
            "You don't ruminate; setbacks land and pass.",
            "Others borrow your calm in crises.",
        ],
        "low": [
            "You feel deeply — the highs and the lows, with little buffer.",
            "Difficult conversations replay in your head; the body holds the day.",
            "Your sensitivity is a gift to those in pain — and a load you carry.",
        ],
    },
}

POLE_LABEL = {"high": "elevated", "low": "subdued", "borderline": "balanced"}


def _resolve_pole(pole: str, percentile: float) -> str:
    if pole in ("high", "low"):
        return pole
    return "high" if percentile >= 60.0 else "low"


def _build_brief_domains(data: dict) -> List[dict]:
    """Build the 5-cell domain grid data."""
    out = []
    for ds in data["domain_sections"]:
        code = ds["code"]
        pole = _resolve_pole(ds["pole"], ds["percentile"])
        bullets = DOMAIN_BULLETS.get(code, {}).get(pole, [])
        out.append({
            "code": code,
            "name": ds["name"],
            "percentile": ds["percentile"],
            "pole": ds["pole"],
            "pole_label": POLE_LABEL.get(ds["pole"], POLE_LABEL.get(pole, "")),
            "is_high": pole == "high",
            "bullets": bullets,
        })
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Shape-one-paragraph — a single tight paragraph version of each Soul Shape
# ─────────────────────────────────────────────────────────────────────────────

SHAPE_ONE_PARAGRAPH: Dict[str, str] = {
    "Host": (
        "You are steady on the inside and reaching on the outside at the same time — a rare combination. "
        "You can hold the room and make space in it. People show up at your door because, somehow, they sensed there would be room. "
        "Your gift to the body of Christ is integration: keeping a seat at the table for the introvert and the extrovert, "
        "the theological question and the immediate practical need."
    ),
    "Anchor": (
        "You are deeply settled on the inside, and you keep faith with the familiar. You hold the line — the prayer that keeps being prayed, "
        "the agreement that is honored, the friendship that lasts thirty years and shows it. Your presence is the long baseline others measure from. "
        "Your gift to the body of Christ is continuity: the institution runs because people like you keep showing up after the thrill is gone."
    ),
    "Psalmist": (
        "You experience life at full volume — grief and gratitude in the same hour — and you are drawn outward toward people, ideas, and beauty. "
        "Your range is not a deficit. It is a capacity. You can speak from inside the hard thing rather than just about it. "
        "Your gift to the body of Christ is voice: the church needs people who can name what others cannot name."
    ),
    "Watchman": (
        "You are not easily moved and not easily impressed. You hold what you hold, and you do not chase novelty. "
        "At the same time, you feel the weight of what is going wrong — and you say so, even when the room would prefer you didn't. "
        "Your gift to the body of Christ is discernment and faithfulness under pressure: you see what others miss, and you hold the line when others have left."
    ),
}

# Letter-type captions: e.g. "Imagination + Ortho-emotion dominant"
LETTER_CAPTIONS = {
    "I": "Imagination",
    "M": "Mastery",
    "A": "Animation",
    "G": "Grace-bearing",
    "O": "Ortho-emotion",
}


def _letter_type_caption(letter_type: str, borderline: list = None) -> str:
    """Build a caption like 'I + O dominant' (excluding borderline letters)."""
    borderline = set((borderline or []))
    # A letter is borderline if its uppercase form is in the borderline list
    high = [c for c in letter_type if c.isupper() and c not in borderline]
    if not high:
        return "All domains balanced"
    return f"{' + '.join(high)} dominant"


# Archetype one-liner captions
ARCHETYPE_CAPTIONS: Dict[str, str] = {
    "Shepherd":  "The one who tends and gathers",
    "Mason":     "The one who builds with care",
    "Reformer":  "The one who says the true thing",
    "Herald":    "The one whose voice carries",
    "Faithful":  "The one who keeps showing up",
    "Maker":     "The one who shapes beauty",
    "Attuned":   "The one who notices the quiet thing",
    "Initiator": "The one who starts things and finishes them",
    "Learner":   "The one who keeps asking why",
    "Servant":   "The one whose work is hidden",
}


# ─────────────────────────────────────────────────────────────────────────────
# Steadiness / Reach label helpers
# ─────────────────────────────────────────────────────────────────────────────

def _shape_pole_labels(soul_shape: str) -> tuple:
    """Return (steadiness_label, reach_label) for the shape."""
    mapping = {
        "Host":     ("High", "High"),
        "Anchor":   ("High", "Low"),
        "Psalmist": ("Low",  "High"),
        "Watchman": ("Low",  "Low"),
    }
    return mapping.get(soul_shape, ("—", "—"))


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def _build_brief_data(result: ImagoResult, name: str, pair_code: str) -> dict:
    full = get_report_data(result, name=name, pair_code=pair_code)

    steady_label, reach_label = _shape_pole_labels(result.soul_shape)

    data = {
        "name": name,
        "pair_code": pair_code,
        "assessment_date": full.get("date") or date.today().strftime("%B %-d, %Y"),

        "soul_shape_name": result.soul_shape,
        "soul_shape_tagline": full.get("soul_shape_tagline", ""),
        "soul_shape_steadiness_label": steady_label,
        "soul_shape_reach_label": reach_label,
        "shape_one_paragraph": SHAPE_ONE_PARAGRAPH.get(result.soul_shape, ""),

        "letter_type_display_str": result.letter_type,
        "letter_type_caption": _letter_type_caption(result.letter_type, result.letter_type_borderline),

        "archetype_name": result.archetype,
        "archetype_caption": ARCHETYPE_CAPTIONS.get(result.archetype, ""),

        "brief_domains": _build_brief_domains(full),
    }
    return data


def generate_imago_brief_pdf(result: ImagoResult, name: str, pair_code: str) -> bytes:
    """Generate the one-page IMAGO brief as PDF bytes."""
    data = _build_brief_data(result, name=name, pair_code=pair_code)
    html_str = _template.render(**data)
    return HTML(string=html_str).write_pdf()


def generate_imago_brief_html(result: ImagoResult, name: str, pair_code: str) -> str:
    data = _build_brief_data(result, name=name, pair_code=pair_code)
    return _template.render(**data)


if __name__ == "__main__":
    # End-to-end self-test using a Reformer-shaped profile
    from imago_items import ITEMS
    from imago_scoring import score_imago

    answers = {}
    for item in ITEMS:
        code = item["aspect_code"]
        direction = item["direction"]
        if code == "I1":
            answers[item["item_id"]] = 5 if direction == "FORWARD" else 1
        elif code == "I2":
            answers[item["item_id"]] = 5 if direction == "FORWARD" else 1
        elif code == "M1":
            answers[item["item_id"]] = 2 if direction == "FORWARD" else 4
        elif code == "M2":
            answers[item["item_id"]] = 2 if direction == "FORWARD" else 4
        elif code == "A1":
            answers[item["item_id"]] = 3 if direction == "FORWARD" else 3
        elif code == "A2":
            answers[item["item_id"]] = 4 if direction == "FORWARD" else 2
        elif code == "G1":
            answers[item["item_id"]] = 1 if direction == "FORWARD" else 5
        elif code == "G2":
            answers[item["item_id"]] = 1 if direction == "FORWARD" else 5
        elif code == "O1":
            answers[item["item_id"]] = 1 if direction == "FORWARD" else 5
        elif code == "O2":
            answers[item["item_id"]] = 1 if direction == "FORWARD" else 5

    result = score_imago(answers, ITEMS)
    pdf = generate_imago_brief_pdf(result, name="Test Friend", pair_code="GRACE-1234")
    out_path = "/tmp/imago_brief_test.pdf"
    with open(out_path, "wb") as f:
        f.write(pdf)
    print(f"Wrote {len(pdf)} bytes to {out_path}")
    print(f"Profile: {result.letter_type} · The {result.soul_shape} · The {result.archetype}")
