"""IMAGO Report Data Assembler.

Given a scored ImagoResult, assembles a single flat dict of every variable
the Jinja2 PDF template will need. Nothing here touches HTML rendering or PDF
generation — this is purely data assembly.

Public API
----------
    get_report_data(result, name, pair_code) -> dict

The returned dict is safe to pass directly to ``template.render(**data)`` or
to ``template.render(data)``. Every key is a plain Python string; values are
strings, lists of strings (paragraph lists), lists of dicts, or simple
scalars — whatever Jinja2 templates consume most naturally.
"""
from __future__ import annotations

import logging
from datetime import date
from typing import Dict, List, Optional

from imago_content_loader import (
    ARCHETYPES,
    ASPECTS,
    DOMAINS,
    REFLECTION_QUESTIONS,
    SOUL_SHAPES,
)
from imago_scoring import (
    ASPECTS as SCORING_ASPECTS,
    DOMAINS as SCORING_DOMAINS,
    ImagoResult,
)

log = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Domain / aspect ordering (matches IMAGO scoring engine order)
# ─────────────────────────────────────────────────────────────────────────────

_DOMAIN_ORDER = [code for code, _name in SCORING_DOMAINS]          # ["I","M","A","G","O"]
_ASPECT_ORDER = [code for code, _name, _domain in SCORING_ASPECTS]  # ["I1","I2",...]


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _resolve_pole(pole: str, percentile: float) -> str:
    """Resolve 'borderline' to 'high' or 'low' by which side the percentile is closer to.

    A borderline score is in the 55-65 range.  We break the tie at 60:
    >= 60 → 'high', < 60 → 'low'.
    """
    if pole in ("high", "low"):
        return pole
    # borderline
    return "high" if percentile >= 60.0 else "low"


# ── Conditional narrative builder ─────────────────────────────────────────────
# v3: every Soul Shape narrative is generic by design — written for the class.
# But the same Soul Shape can contain very different people. Two Anchors with
# the same Steadiness can be wildly different on the inside if one has high I
# (Imagination) and the other low. This function generates a short
# personalization paragraph that names what is distinctive about *this* person
# within their shape, so the report stops feeling generic at the top.

def _build_conditional_soul_shape_note(
    soul_shape: str,
    domain_by_code: dict,
    metatraits: list,
) -> str:
    """Generate a 2-4 sentence note that personalizes the Soul Shape based on
    the specific score profile within it. Returned as a single string (one
    paragraph). Empty string if no distinctive pattern is detected.

    domain_by_code: {code: DomainScore}  (with .percentile)
    metatraits: list of MetatraitScore (with .name and .percentile)
    """
    if not domain_by_code:
        return ""

    def pct(code):
        d = domain_by_code.get(code)
        return d.percentile if d is not None else 50.0

    I, M, A, G, O = pct("I"), pct("M"), pct("A"), pct("G"), pct("O"),
    meta_pct = {m.name: m.percentile for m in metatraits}
    steadiness = meta_pct.get("Steadiness", 50)
    reach = meta_pct.get("Reach", 50)

    notes = []

    # ── Anchor-specific personalization ──
    if soul_shape == "Anchor":
        if I >= 75:
            notes.append(
                "One thing worth naming about your Anchor profile: your inner imagination is unusually active. "
                "You are steady on the outside, but the inside is full of ideas. That combination — a settled person who still pursues new thought — is rare, and it is part of why people trust your conclusions. You did not arrive there carelessly."
            )
        if A >= 70 and G <= 35:
            notes.append(
                "Your Anchor pattern also carries a Reformer's edge. You are not the quiet, agreeable kind of steady. You are the kind who will speak — plainly, sometimes uncomfortably — because the truth matters more to you than the temperature of the room. This is a real gift, and it is also a place to watch your own heart."
            )
        elif G <= 25:
            notes.append(
                "Worth noting: your Anchor steadiness pairs with a directness that does not soften easily. You hold the line, and you say so. Read your domain sections carefully — your courtesy score asks for some honest reflection."
            )
        if M <= 35 and O >= 75:
            notes.append(
                "One more thing: your Anchor steadiness is emotional, not necessarily operational. The inside is calm. The desk may not be. That is a real version of this shape — just know which half of your steadiness is doing the heavy lifting."
            )
        if O >= 80 and steadiness < 70:
            notes.append(
                "Your emotional steadiness specifically is very high — higher than your overall Steadiness number suggests, because the metatrait blends in other factors. On the inside, you are not easily shaken."
            )

    # ── Psalmist-specific personalization ──
    elif soul_shape == "Psalmist":
        if O >= 70:
            notes.append(
                "Worth naming inside your Psalmist shape: your emotional life is actually more settled than this shape typically describes. You feel deeply, but you also recover. That mix — depth without volatility — is unusual and is part of what makes your voice trustworthy."
            )
        if I >= 80 and A >= 70:
            notes.append(
                "You are the kind of Psalmist whose feeling is fueled by both ideas and people. The artist and the host live in the same body. That is a high-output combination, and one to steward intentionally."
            )
        if M >= 70:
            notes.append(
                "And unusually for this shape, you are also disciplined. The feeling does not run away with you. You can finish what you start, even on a hard day. That makes your Psalmist gift productive, not just expressive."
            )

    # ── Host-specific personalization ──
    elif soul_shape == "Host":
        if G >= 75:
            notes.append(
                "Inside the Host shape, your grace-bearing domain is unusually strong. You are not just a steady, reaching person — you are a kind one. Watch for the temptation to absorb other people's weight as if it were your own."
            )
        if A >= 80:
            notes.append(
                "Your Host shape leans extraverted in a pronounced way. Your room-making is energetic, not contemplative. That is a real gift and a real cost — read your Animation section carefully."
            )
        if M <= 40:
            notes.append(
                "One Host-specific watch: your openness and steadiness are real, but your operational follow-through is lower. The room is warm. The promises kept may need shoring up."
            )

    # ── Watchman-specific personalization ──
    elif soul_shape == "Watchman":
        if I >= 75:
            notes.append(
                "Inside the Watchman shape, your imagination runs high. You are not a stoic guard — you are a thoughtful one. The things you see, you see in detail."
            )
        if G <= 30:
            notes.append(
                "Your Watchman calling carries a sharp edge. The line you hold, you do not soften. This is part of your strength and a place to watch — the message can be true and still be delivered in a way that closes the ear it most needed to reach."
            )
        if O >= 70:
            notes.append(
                "Worth naming: your inner weather is more settled than this shape usually implies. You watch without being shaken by what you see. That is rare and valuable."
            )

    return "\n\n".join(notes).strip()


def _format_date(d: date) -> str:
    """Format a date as 'Month Day, Year' (e.g., 'April 25, 2026')."""
    return d.strftime("%B %-d, %Y")


def _letter_type_display(letter_type: str, borderline: List[str]) -> List[dict]:
    """Return a list of per-letter display metadata.

    Each dict:
        {
            "letter": "I",            # uppercase letter
            "is_high": True,          # True if uppercase in letter_type
            "is_borderline": True,    # True if in borderline list
            "display_letter": "I",    # the letter as it appears in letter_type
        }
    """
    result = []
    for char in letter_type:
        letter_upper = char.upper()
        result.append({
            "letter": letter_upper,
            "is_high": char.isupper(),
            "is_borderline": letter_upper in borderline,
            "display_letter": char,
        })
    return result


def _get_soul_shape(soul_shape_name: str) -> dict:
    """Fetch soul shape content with graceful fallback."""
    data = SOUL_SHAPES.get(soul_shape_name)
    if data is None:
        log.warning(
            "Soul shape '%s' not found in SOUL_SHAPES. Available: %s",
            soul_shape_name,
            list(SOUL_SHAPES.keys()),
        )
        return {
            "name": soul_shape_name,
            "sidebar_meta": {},
            "tagline": "",
            "narrative_paragraphs": [f"[Content for soul shape '{soul_shape_name}' not found.]"],
        }
    return data


def _get_archetype(archetype_name: str) -> dict:
    """Fetch archetype content with graceful fallback."""
    data = ARCHETYPES.get(archetype_name)
    if data is None:
        log.warning(
            "Archetype '%s' not found in ARCHETYPES. Available: %s",
            archetype_name,
            list(ARCHETYPES.keys()),
        )
        return {
            "name": archetype_name,
            "sidebar_scores": {},
            "biblical_anchor": "",
            "opening": [f"[Content for archetype '{archetype_name}' not found.]"],
            "what_this_looks_like": [],
            "behavioral_markers": [],
            "what_you_bring": [],
            "scripture_figures": [],
            "shadow": [],
            "gospel_calling": [],
            "deepest_call": [],
            "prayer": [],
            "gift_to_body": [],
        }
    return data


def _get_domain_section(domain_code: str, resolved_pole: str) -> dict:
    """Fetch a domain pole's content with graceful fallback."""
    domain_data = DOMAINS.get(domain_code)
    if domain_data is None:
        log.warning("Domain code '%s' not found in DOMAINS.", domain_code)
        return _empty_domain_section(domain_code, resolved_pole)

    pole_data = domain_data.get(resolved_pole)
    if pole_data is None:
        log.warning(
            "Pole '%s' not found for domain '%s'. Available poles: %s",
            resolved_pole,
            domain_code,
            list(domain_data.keys()),
        )
        # Try the opposite pole as last-resort
        alt_pole = "low" if resolved_pole == "high" else "high"
        pole_data = domain_data.get(alt_pole, _empty_domain_section(domain_code, resolved_pole))

    return pole_data


def _empty_domain_section(domain_code: str, pole: str) -> dict:
    return {
        "sidebar": {},
        "opening_paragraphs": [f"[Domain {domain_code} {pole} content not found.]"],
        "what_this_looks_like": [],
        "imago_dei_connection": [],
        "calling": [],
        "shadow": [],
        "gospel_anchor": [],
        "partner_insight": [],
        "_sections": {},
    }


def _get_aspect_section(aspect_code: str) -> dict:
    """Fetch aspect content with graceful fallback."""
    data = ASPECTS.get(aspect_code)
    if data is None:
        log.warning("Aspect code '%s' not found in ASPECTS.", aspect_code)
        return {
            "code": aspect_code,
            "name": aspect_code,
            "sidebar": {},
            "opening_paragraphs": [f"[Aspect {aspect_code} content not found.]"],
            "high_paragraph": "",
            "low_paragraph": "",
            "pastoral_note": "",
        }
    return data


def _get_reflection_questions(archetype_name: str) -> List[dict]:
    """Fetch reflection questions with graceful fallback."""
    questions = REFLECTION_QUESTIONS.get(archetype_name)
    if not questions:
        log.warning(
            "Reflection questions for '%s' not found. Available: %s",
            archetype_name,
            list(REFLECTION_QUESTIONS.keys()),
        )
        return []
    return questions


# ─────────────────────────────────────────────────────────────────────────────
# Main assembler
# ─────────────────────────────────────────────────────────────────────────────

def get_report_data(
    result: ImagoResult,
    name: str,
    pair_code: str,
) -> dict:
    """Assemble the complete Jinja2 template variables dict for the PDF report.

    Args:
        result:     A fully scored ImagoResult from imago_scoring.score_imago().
        name:       The respondent's name as it should appear in the report.
        pair_code:  The respondent's pair/couple code (for cross-referencing).

    Returns:
        A flat dict containing every variable the PDF template will need.
        Lists of paragraph strings are used for multi-paragraph body text so
        templates can iterate with ``{% for p in field %}``.

    Raises:
        TypeError:  If ``result`` is not an ImagoResult instance.
    """
    if not isinstance(result, ImagoResult):
        raise TypeError(f"Expected ImagoResult, got {type(result).__name__}")

    today = date.today()

    # ── Build domain lookup by code ────────────────────────────────────────
    domain_by_code = {d.code: d for d in result.domains}
    aspect_by_code = {
        a.code: a
        for d in result.domains
        for a in d.aspects
    }

    # ── Letter type display list ───────────────────────────────────────────
    letter_display = _letter_type_display(
        result.letter_type,
        result.letter_type_borderline,
    )

    # ── Soul Shape ─────────────────────────────────────────────────────────
    soul_shape_content = _get_soul_shape(result.soul_shape)
    soul_shape_conditional_note = _build_conditional_soul_shape_note(
        result.soul_shape,
        domain_by_code,
        result.metatraits,
    )

    # ── Archetype ──────────────────────────────────────────────────────────
    archetype_content = _get_archetype(result.archetype)

    # ── Domain sections (5) ────────────────────────────────────────────────
    domain_sections: List[dict] = []
    for code in _DOMAIN_ORDER:
        d = domain_by_code.get(code)
        if d is None:
            log.warning("Domain '%s' missing from ImagoResult.domains.", code)
            continue

        resolved_pole = _resolve_pole(d.pole, d.percentile)
        content = _get_domain_section(code, resolved_pole)

        domain_sections.append({
            # Score metadata
            "code": d.code,
            "name": d.name,
            "raw_mean": d.raw_mean,
            "percentile": d.percentile,
            "pole": d.pole,
            "resolved_pole": resolved_pole,
            "is_borderline": d.pole == "borderline",
            # Content from content loader
            "sidebar": content["sidebar"],
            "opening_paragraphs": content["opening_paragraphs"],
            "what_this_looks_like": content["what_this_looks_like"],
            "imago_dei_connection": content["imago_dei_connection"],
            "calling": content["calling"],
            "shadow": content["shadow"],
            "gospel_anchor": content["gospel_anchor"],
            "partner_insight": content["partner_insight"],
        })

    # ── Aspect sections (10) ───────────────────────────────────────────────
    aspect_sections: List[dict] = []
    for code in _ASPECT_ORDER:
        a = aspect_by_code.get(code)
        if a is None:
            log.warning("Aspect '%s' missing from ImagoResult aspect scores.", code)
            continue

        resolved_pole = _resolve_pole(
            "high" if a.percentile >= 60 else ("borderline" if 55 <= a.percentile <= 65 else "low"),
            a.percentile,
        )
        content = _get_aspect_section(code)

        # Pick the right pole paragraph
        pole_paragraph = (
            content["high_paragraph"]
            if resolved_pole == "high"
            else content["low_paragraph"]
        )

        aspect_sections.append({
            # Score metadata
            "code": a.code,
            "name": a.name,
            "domain_code": a.domain_code,
            "raw_mean": a.raw_mean,
            "percentile": a.percentile,
            "resolved_pole": resolved_pole,
            # Content
            "sidebar": content["sidebar"],
            "opening_paragraphs": content["opening_paragraphs"],
            "pole_paragraph": pole_paragraph,
            "high_paragraph": content["high_paragraph"],
            "low_paragraph": content["low_paragraph"],
            "pastoral_note": content["pastoral_note"],
        })

    # ── Reflection questions ───────────────────────────────────────────────
    reflection_questions = _get_reflection_questions(result.archetype)

    # ── Metatrait scores (for visualisation) ──────────────────────────────
    metatrait_scores = [
        {
            "name": m.name,
            "raw_mean": m.raw_mean,
            "percentile": m.percentile,
            "pole": m.pole,
        }
        for m in result.metatraits
    ]

    # ── Domain scores for visualisation ───────────────────────────────────
    domain_scores_viz = [
        {
            "code": d.code,
            "name": d.name,
            "raw_mean": d.raw_mean,
            "percentile": d.percentile,
            "pole": d.pole,
        }
        for d in result.domains
    ]

    # ── Aspect scores for visualisation ───────────────────────────────────
    aspect_scores_viz = [
        {
            "code": a.code,
            "name": a.name,
            "domain_code": a.domain_code,
            "raw_mean": a.raw_mean,
            "percentile": a.percentile,
        }
        for d in result.domains
        for a in d.aspects
    ]

    # ── Assemble final dict ────────────────────────────────────────────────
    return {
        # ── Identity ──────────────────────────────────────────────────────
        "name": name,
        "pair_code": pair_code,
        "date": _format_date(today),
        "year": today.year,

        # ── Letter type ───────────────────────────────────────────────────
        # Full string, e.g. "iMAGo"
        "letter_type": result.letter_type,
        # List of borderline letter codes, e.g. ["I", "O"]
        "letter_type_borderline": result.letter_type_borderline,
        # Structured per-letter display: list of
        # {letter, is_high, is_borderline, display_letter}
        "letter_type_display": letter_display,

        # ── Soul Shape ────────────────────────────────────────────────────
        "soul_shape_name": result.soul_shape,
        "soul_shape_tagline": soul_shape_content["tagline"],
        "soul_shape_sidebar": soul_shape_content["sidebar_meta"],
        # Steadiness / Reach from sidebar (with backward-compat for legacy keys)
        "soul_shape_steadiness": soul_shape_content["sidebar_meta"].get("steadiness", soul_shape_content["sidebar_meta"].get("stability", "")),
        "soul_shape_reach": soul_shape_content["sidebar_meta"].get("reach", soul_shape_content["sidebar_meta"].get("plasticity", "")),
        "soul_shape_biblical_anchor": soul_shape_content["sidebar_meta"].get("biblical_anchor", ""),
        # Narrative body as list of paragraph strings
        "soul_shape_narrative": soul_shape_content["narrative_paragraphs"],
        # v3: conditional note that personalizes the Soul Shape to *this* respondent's profile
        "soul_shape_conditional_note": soul_shape_conditional_note,

        # ── Archetype ─────────────────────────────────────────────────────
        "archetype_name": result.archetype,
        "archetype_match_score": result.archetype_match_score,
        "archetype_biblical_anchor": archetype_content["biblical_anchor"],
        "archetype_sidebar_scores": archetype_content["sidebar_scores"],
        "archetype_opening": archetype_content["opening"],
        "archetype_what_this_looks_like": archetype_content["what_this_looks_like"],
        "archetype_behavioral_markers": archetype_content["behavioral_markers"],
        "archetype_what_you_bring": archetype_content["what_you_bring"],
        "archetype_scripture_figures": archetype_content["scripture_figures"],
        "archetype_shadow": archetype_content["shadow"],
        "archetype_gospel_calling": archetype_content["gospel_calling"],
        "archetype_deepest_call": archetype_content["deepest_call"],
        "archetype_prayer": archetype_content["prayer"],
        "archetype_gift_to_body": archetype_content["gift_to_body"],

        # ── Domain sections (list, length 5) ──────────────────────────────
        # Each item: see domain_sections assembly above
        "domain_sections": domain_sections,

        # Also expose as a dict keyed by domain code for direct template access
        "domain_by_code": {s["code"]: s for s in domain_sections},

        # ── Aspect sections (list, length 10) ─────────────────────────────
        # Each item: see aspect_sections assembly above
        "aspect_sections": aspect_sections,

        # Dict keyed by aspect code for direct access
        "aspect_by_code": {s["code"]: s for s in aspect_sections},

        # ── Reflection questions ───────────────────────────────────────────
        # List of 5 dicts: {number, question_text, source_note}
        "reflection_questions": reflection_questions,

        # ── Score visualisation data ───────────────────────────────────────
        "domain_scores": domain_scores_viz,
        "aspect_scores": aspect_scores_viz,
        "metatrait_scores": metatrait_scores,

        # Full raw result dict for any template that needs it
        "raw_result": result.to_dict(),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Self-test
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s  %(name)s  %(message)s",
    )

    # ── Generate a test ImagoResult using the same fake-data approach as
    #    imago_scoring.py's self-test ─────────────────────────────────────
    from imago_scoring import ASPECTS as _SCORING_ASPECTS, score_imago

    fake_items = []
    for code, _, _ in _SCORING_ASPECTS:
        for i in range(10):
            direction = "FORWARD" if i < 6 else "REVERSE"
            fake_items.append({
                "item_id": f"FAKE-{code}-{i}",
                "aspect_code": code,
                "direction": direction,
            })
    answers = {
        item["item_id"]: (4 if item["direction"] == "FORWARD" else 2)
        for item in fake_items
    }

    test_result = score_imago(answers, fake_items)

    # ── Run get_report_data ───────────────────────────────────────────────
    data = get_report_data(
        result=test_result,
        name="Jane Testington",
        pair_code="XK-4492",
    )

    # ── Print summary ─────────────────────────────────────────────────────
    sep = "─" * 60

    print(sep)
    print("IMAGO Report Data Assembler — Self-Test")
    print(sep)
    print(f"\n  Name:           {data['name']}")
    print(f"  Pair code:      {data['pair_code']}")
    print(f"  Date:           {data['date']}")
    print(f"  Letter type:    {data['letter_type']}")
    print(f"  Borderline:     {data['letter_type_borderline']}")
    print(f"  Soul Shape:     {data['soul_shape_name']}")
    print(f"  Archetype:      {data['archetype_name']} (match: {data['archetype_match_score']:.3f})")

    print(f"\n{sep}")
    print("Letter type display")
    print(sep)
    for l in data["letter_type_display"]:
        flag = " (borderline)" if l["is_borderline"] else ""
        pole = "HIGH" if l["is_high"] else "low"
        print(f"  {l['display_letter']}  →  {pole}{flag}")

    print(f"\n{sep}")
    print("Soul Shape")
    print(sep)
    print(f"  Tagline:          {data['soul_shape_tagline']}")
    print(f"  Steadiness:       {data['soul_shape_steadiness']}")
    print(f"  Reach:            {data['soul_shape_reach']}")
    print(f"  Biblical anchor:  {data['soul_shape_biblical_anchor']}")
    print(f"  Narrative paras:  {len(data['soul_shape_narrative'])}")
    print(f"  First para:       {data['soul_shape_narrative'][0][:100]!r}...")

    print(f"\n{sep}")
    print("Archetype")
    print(sep)
    print(f"  Biblical anchor:  {data['archetype_biblical_anchor']}")
    print(f"  Opening paras:    {len(data['archetype_opening'])}")
    print(f"  Behavioral mkrs:  {len(data['archetype_behavioral_markers'])}")
    print(f"  Scripture figs:   {len(data['archetype_scripture_figures'])}")
    print(f"  Shadow paras:     {len(data['archetype_shadow'])}")
    print(f"  Gospel calling:   {len(data['archetype_gospel_calling'])}")
    print(f"  Prayer paras:     {len(data['archetype_prayer'])}")
    print(f"  Gift to body:     {len(data['archetype_gift_to_body'])}")

    print(f"\n{sep}")
    print("Domain sections")
    print(sep)
    for d in data["domain_sections"]:
        print(
            f"  {d['code']} {d['name']:<16} "
            f"pct={d['percentile']:5.1f}  pole={d['pole']:<12} "
            f"resolved={d['resolved_pole']:<5} "
            f"opening={len(d['opening_paragraphs'])} "
            f"what_looks={len(d['what_this_looks_like'])} "
            f"shadow={len(d['shadow'])} "
            f"calling={len(d['calling'])}"
        )

    print(f"\n{sep}")
    print("Aspect sections")
    print(sep)
    for a in data["aspect_sections"]:
        pole_snippet = a["pole_paragraph"][:60].replace("\n", " ")
        print(
            f"  {a['code']} {a['name']:<16} "
            f"pct={a['percentile']:5.1f}  pole={a['resolved_pole']:<5} "
            f"para='{pole_snippet}...'"
        )

    print(f"\n{sep}")
    print("Reflection questions")
    print(sep)
    for q in data["reflection_questions"]:
        print(f"  Q{q['number']}: {q['question_text'][:90]!r}...")
        print(f"       source: {q['source_note'][:70]!r}")

    print(f"\n{sep}")
    print("Score visualisation data")
    print(sep)
    print(f"  domain_scores keys:    {len(data['domain_scores'])} domains")
    print(f"  aspect_scores keys:    {len(data['aspect_scores'])} aspects")
    print(f"  metatrait_scores:      {len(data['metatrait_scores'])} metatraits")
    for m in data["metatrait_scores"]:
        print(f"    {m['name']:<12}: pct={m['percentile']:.1f}  pole={m['pole']}")

    print(f"\n{sep}")
    print("Total keys in report dict:", len(data))
    print(sep)

    # Verify JSON-serialisability of non-private values
    try:
        json.dumps({k: v for k, v in data.items() if not k.startswith("_")}, ensure_ascii=False)
        print("\nJSON serialisation check: PASS")
    except Exception as e:
        print(f"\nJSON serialisation check: FAIL — {e}")
        sys.exit(1)

    print("\nSelf-test complete.")
