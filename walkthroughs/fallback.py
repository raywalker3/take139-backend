"""Fallback walkthrough PDF — shown for profiles we haven't yet written.

The reader gets a one-page-or-so kind document acknowledging their profile,
explaining that the full walkthrough is being prepared, and giving them
something honest to sit with in the meantime.

When all 36 personal walkthroughs and 15 couples walkthroughs are written,
the fallbacks are never served. Until then, they're how we keep the launch
clean while content fills in over weeks.
"""
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer, NextPageTemplate, PageBreak

from .base import (
    make_doc, make_styles, ensure_fonts, section_header, finalize_buffer,
    PAGE_W, MARGIN_L, MARGIN_R,
)


# Short-code → display name (so we can write "the Architect" not "ARCH")
MECH_NAMES = {
    "ARCH": "Architect", "ISLE": "Island", "AMB": "Ambassador",
    "VAULT": "Vault", "ADPT": "Adapter", "CAMP": "Performance",
}
BD_NAMES = {
    "ATTY": "Attorney", "GHOST": "Ghost", "FLOOD": "Flood",
    "MASK": "Mask", "VERD": "Quiet Exit", "PLEA": "Plea",
    "DISAP": "Ghost",  # legacy code, maps to current name
    "REM": "Quiet Exit",  # legacy code
}
TRIG_NAMES = {
    "DIS": "Disrespect", "DISC": "Disconnection", "INJ": "Injustice",
    "CTRL": "Control", "SHAM": "Shame", "SIG": "Insignificance",
}
CORE_Q_NAMES = {
    "COMP": "Am I competent?",
    "LOV": "Am I lovable?",
    "PROT": "Am I protected?",
    "FREE": "Am I free?",
    "ACC": "Am I acceptable?",
    "SIG": "Am I significant?",
}


def _name_or_code(d, code, default="—"):
    if not code:
        return default
    return d.get(code.upper(), code)


def build_personal_fallback(submission) -> bytes:
    """A polite, real-feeling 'your walkthrough is being prepared' PDF."""
    ensure_fonts()
    S = make_styles()

    mech_name = _name_or_code(MECH_NAMES, submission.primary_mechanism, "your mechanism")
    bd_name = _name_or_code(BD_NAMES, submission.primary_breakdown, "your breakdown")
    trig_name = _name_or_code(TRIG_NAMES, submission.primary_trigger, "your trigger")
    # Submission stores the core question as `primary_core_question`. Older
    # docstrings called this `core_question`; both names are accepted here
    # so we never crash on a missing attribute.
    _cq_key = getattr(submission, "primary_core_question", None) or getattr(submission, "core_question", None)
    cq_name = _name_or_code(CORE_Q_NAMES, _cq_key, "your core question")

    doc, buf = make_doc(
        brand_text="Take 139  ·  Walkthrough in Preparation",
        cover_top_label="TAKE 139  ·  WALKTHROUGH",
        cover_right_label=f"{mech_name.upper()}  ·  {bd_name.upper()}",
        title=f"Take 139 — Walkthrough for {mech_name} + {bd_name}",
    )

    story = []

    # ── COVER ──
    story.append(Spacer(1, 1.4 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph(f"Your Walkthrough<br/>is Being Prepared", S["CoverTitle"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(
        "A counselor's full walk through your profile<br/>is being written for you.",
        S["CoverSub"],
    ))
    story.append(Spacer(1, 0.8 * inch))
    story.append(Paragraph("YOUR PROFILE", S["CoverProfileLabel"]))
    story.append(Paragraph(f"{mech_name} &nbsp;&middot;&nbsp; {bd_name}", S["CoverProfileVal"]))
    story.append(Paragraph(
        f"Trigger: {trig_name} &nbsp;&middot;&nbsp; Core Question: {cq_name}",
        S["CoverProfileSub"],
    ))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── BODY ──
    section_header(story, S,
                   "A WORD WHILE YOU WAIT",
                   "We are writing this one carefully.",
                   "Your full walkthrough is in progress.")

    for para in [
        f"Thank you for taking Take 139. Your assessment has been received, "
        f"your profile saved, and the result you saw on screen is yours to keep.",

        f"What you saw \u2014 the <b>{mech_name}</b> mechanism, the <b>{bd_name}</b> "
        f"breakdown, the trigger of <b>{trig_name}</b>, and the question your "
        f"soul keeps asking, <i>{cq_name}</i> \u2014 these are the four anchors "
        f"that the full Walkthrough takes apart, page by page.",

        f"The Walkthrough itself is a ~20-page PDF written in the voice of a "
        f"pastoral counselor (specifically, with Tim Keller's tone as the "
        f"reference point). It walks through your trigger, the question "
        f"underneath it, the mechanism you've built, the breakdown that "
        f"happens when the mechanism gives way, and concrete tools \u2014 plus "
        f"a prayer, and a clear path forward.",

        f"Honest disclosure: not every one of the 36 possible profile "
        f"combinations is written yet. Yours is being prepared. We are "
        f"working through the profiles in order of need and would rather "
        f"send you something true to your wiring than something rushed.",

        f"<b>When your walkthrough is ready</b>, we'll email you the PDF. "
        f"In most cases this is within a few days; we'll send a quick note "
        f"either way so you're not left wondering.",

        f"In the meantime, the result page you saw on take139.com is yours "
        f"to come back to anytime. Your pair code (<b>{submission.pair_code}</b>) "
        f"is permanent \u2014 if you ever want to connect with your spouse, "
        f"that's the code you'd share with them.",

        f"Grace and peace.",
    ]:
        story.append(Paragraph(para, S["BodyJ"]))

    doc.build(story)
    return finalize_buffer(buf)


def build_couples_fallback(sub_a, sub_b) -> bytes:
    """A polite couples-walkthrough fallback for mechanism-pairs we haven't written yet."""
    ensure_fonts()
    S = make_styles()

    mech_a = _name_or_code(MECH_NAMES, sub_a.primary_mechanism, "one mechanism")
    mech_b = _name_or_code(MECH_NAMES, sub_b.primary_mechanism, "the other")
    name_a = (sub_a.name or "Partner A").split()[0]
    name_b = (sub_b.name or "Partner B").split()[0]

    doc, buf = make_doc(
        brand_text="Take 139  ·  Couples Walkthrough in Preparation",
        cover_top_label="TAKE 139  ·  COUPLES WALKTHROUGH",
        cover_right_label=f"{name_a.upper()}  +  {name_b.upper()}",
        title=f"Take 139 — Couples Walkthrough ({mech_a} + {mech_b})",
    )

    story = []

    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("Your Couples Walkthrough<br/>is Being Prepared", S["CoverTitle"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(
        "A counselor's read of your pairing is being written for you.",
        S["CoverSub"],
    ))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("YOUR PAIRING", S["CoverProfileLabel"]))
    story.append(Paragraph(f"{name_a} &nbsp;&amp;&nbsp; {name_b}", S["CoverNames"]))
    story.append(Paragraph(
        f"{mech_a} &nbsp;&middot;&nbsp; {mech_b}",
        S["CoverProfileVal"],
    ))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    section_header(story, S,
                   "A WORD WHILE YOU WAIT",
                   "We are writing yours carefully.",
                   "Your couples walkthrough is in progress.")

    for para in [
        f"Thank you for connecting your profiles. The bond between "
        f"{name_a} and {name_b} is now recorded in our system, and the "
        f"synthesis page you saw together is yours to revisit anytime.",

        f"What you saw \u2014 the {mech_a} and the {mech_b}, side by side \u2014 "
        f"is the foundation. The full Couples Walkthrough is a ~25-page PDF "
        f"that includes your specific pairing's collision points, what each "
        f"of you gives the other that you could not build alone, six "
        f"commitments (three from each), a prayer for the marriage, and a "
        f"six-round date-night conversation designed to be spoken across "
        f"a table.",

        f"We're writing the 15 mechanism-pair Walkthroughs in order of "
        f"need. Yours \u2014 {mech_a} + {mech_b} \u2014 is being prepared.",

        f"<b>When your walkthrough is ready</b>, we'll email both of you "
        f"the PDF. In most cases this is within a few days; we'll send "
        f"a quick note either way so you're not left wondering.",

        f"In the meantime, your bond is locked in. You don't need to "
        f"re-pair or re-purchase anything. When the document is ready, "
        f"you'll receive it.",

        f"Grace and peace.",
    ]:
        story.append(Paragraph(para, S["BodyJ"]))

    doc.build(story)
    return finalize_buffer(buf)
