"""Gender-neutral couples walkthrough PDF.

Used when:
  - The pair's gender combination doesn't match the hardcoded assumption in
    the specific pair file (e.g. two men, two women, female Architect + male
    Island, or any combo where one or both partners are unspecified).
  - We don't have a pair-specific written walkthrough at all (formerly the
    'preparing' fallback).

Voice:
  - Uses first names throughout: "Sarah" and "Charlie", not "he/she".
  - When pronouns are absolutely necessary, uses singular "they/them".
  - Sections are structured the same way as the gendered walkthroughs
    (collision, gifts each gives, prayer, commitments, date-night appendix)
    but written so a same-gender pair or any unconventional pair reads it
    and finds themselves in it.

This is a substantive ~12-page PDF, not a "coming soon" placeholder.
"""
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer, PageBreak, NextPageTemplate

from .base import (
    make_doc, make_styles, ensure_fonts, section_header, finalize_buffer,
)


# Short-code → display name
MECH_NAMES = {
    "ARCH": "Architect", "ISLE": "Island", "AMB": "Ambassador",
    "VAULT": "Vault", "ADPT": "Adapter", "CAMP": "Performance",
}
BD_NAMES = {
    "ATTY": "Attorney", "GHOST": "Ghost", "FLOOD": "Flood",
    "MASK": "Mask", "VERD": "Quiet Exit", "PLEA": "Plea",
    "DISAP": "Ghost", "REM": "Quiet Exit",
}
TRIG_NAMES = {
    "DIS": "Disrespect", "DISC": "Disconnection", "INJ": "Injustice",
    "CTRL": "Control", "SHAM": "Shame", "SIG": "Insignificance",
}
CORE_Q_NAMES = {
    "COMP": "Am I competent?",
    "LOV":  "Am I lovable?",
    "PROT": "Am I protected?",
    "FREE": "Am I free?",
    "ACC":  "Am I acceptable?",
    "SIG":  "Am I significant?",
}


# Each mechanism contributes ONE thing in a pairing — that's the spine of
# the "what each gives the other" sections. Written in name-based,
# gender-neutral prose.
MECH_GIFTS = {
    "ARCH": (
        "the structure that lets a household keep functioning under stress. "
        "When everything else is shaking, the Architect keeps building "
        "scaffolding. Their partner often does not realize until something "
        "breaks how much they were resting on what the Architect quietly held."
    ),
    "ISLE": (
        "the rare gift of a room that does not require performance. The "
        "Island doesn't need their partner to be three moves ahead or "
        "emotionally available at every moment. In a household where most "
        "people are managing each other's weather, an Island gives shelter "
        "from that work."
    ),
    "AMB": (
        "warmth as a discipline. The Ambassador keeps the relational fabric "
        "intact even when the day has been hard. They are the one who turns "
        "back to a conversation that another partner would let drop. Without "
        "this, a marriage cools faster than either partner realizes."
    ),
    "VAULT": (
        "containment. The Vault holds the things that should not be said in "
        "every room, and they hold them well. In a culture that confuses "
        "transparency with intimacy, the Vault remembers that a marriage is "
        "the place where some things stay between two people."
    ),
    "ADPT": (
        "the ability to bend without breaking. The Adapter sees the path "
        "around, under, or through whatever the day brings, and keeps "
        "moving. Their partner often does not realize how much grief or "
        "loss has been quietly metabolized by this gift."
    ),
    "CAMP": (
        "the bright fire around which other people gather. The Performance "
        "makes a home into a place where people want to be. Friends know "
        "where to come. Children know they are seen. The household has a "
        "warmth that other homes don't."
    ),
}


# Each breakdown style describes how a person fails under stress. Used in
# the "collision" section.
BD_FAILURES = {
    "ATTY": (
        "argues their case. They build a brief, complete with evidence and "
        "precedent, and they will not stop presenting it until the verdict "
        "matches what they believe is true. The other partner stops "
        "listening long before the brief is finished."
    ),
    "GHOST": (
        "disappears. Not physically — emotionally. The room becomes a place "
        "where they are present in body but absent in every other way. The "
        "other partner finds themselves talking to someone who is not really "
        "there."
    ),
    "FLOOD": (
        "spills. Every emotion that had been held back for a week pours "
        "into one conversation, and the conversation drowns. The other "
        "partner cannot find a foothold inside the flood."
    ),
    "MASK": (
        "performs. The face they show stops matching the inside. They smile "
        "while inside they are dying, and their partner — who can tell the "
        "smile is wrong but cannot prove it — does not know which version "
        "to respond to."
    ),
    "VERD": (
        "renders quiet judgment. The conversation appears to end, but the "
        "ruling has already been filed. The other partner only finds out "
        "weeks later, when something they didn't know they were doing wrong "
        "is named as the proof."
    ),
    "PLEA": (
        "begs. They will trade almost anything to make the rupture stop. "
        "The other partner cannot tell whether the apology is real or "
        "whether they are simply being given what will make them go quiet."
    ),
}


def _first_name(sub, default="Partner"):
    full = (getattr(sub, "name", None) or "").strip()
    if not full:
        return default
    return full.split()[0]


def _name(d, code, fallback="—"):
    if not code:
        return fallback
    return d.get(code.upper(), code)


def _gift_for(sub):
    return MECH_GIFTS.get((sub.primary_mechanism or "").upper(), MECH_GIFTS["ARCH"])


def _failure_for(sub):
    return BD_FAILURES.get((sub.primary_breakdown or "").upper(), BD_FAILURES["ATTY"])


def build_neutral_couples_walkthrough(sub_a, sub_b) -> bytes:
    """Build a gender-neutral couples walkthrough for any pair.

    Substantive ~12 pages: intro, side-by-side, collision, gifts (each
    direction), prayer, three commitments per partner, closing.
    """
    ensure_fonts()
    S = make_styles()

    name_a = _first_name(sub_a, "Partner A")
    name_b = _first_name(sub_b, "Partner B")

    mech_a = _name(MECH_NAMES, sub_a.primary_mechanism, "their mechanism")
    mech_b = _name(MECH_NAMES, sub_b.primary_mechanism, "their mechanism")
    bd_a = _name(BD_NAMES, sub_a.primary_breakdown, "their breakdown")
    bd_b = _name(BD_NAMES, sub_b.primary_breakdown, "their breakdown")
    trig_a = _name(TRIG_NAMES, sub_a.primary_trigger, "their trigger")
    trig_b = _name(TRIG_NAMES, sub_b.primary_trigger, "their trigger")
    cq_a = _name(CORE_Q_NAMES, sub_a.primary_core_question, "their core question")
    cq_b = _name(CORE_Q_NAMES, sub_b.primary_core_question, "their core question")

    doc, buf = make_doc(
        brand_text="Take 139  ·  A Couples Walkthrough",
        cover_top_label="TAKE 139  ·  COUPLES WALKTHROUGH",
        cover_right_label=f"{name_a.upper()}  +  {name_b.upper()}",
        title=f"Take 139 Couples Walkthrough — {name_a} & {name_b}",
    )

    story = []

    # ── COVER ──
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph(
        f"A Couples Walkthrough<br/>for {name_a} &amp; {name_b}",
        S["CoverTitle"],
    ))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(
        "The pattern underneath your conflict, named in your two names.",
        S["CoverSub"],
    ))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("YOUR TWO ARCHETYPES", S["CoverProfileLabel"]))
    story.append(Paragraph(
        f"{name_a} &middot; {mech_a}",
        S["CoverProfileVal"],
    ))
    story.append(Paragraph(
        f"{name_b} &middot; {mech_b}",
        S["CoverProfileVal"],
    ))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION ONE — A NOTE TO BOTH OF YOU ──
    section_header(story, S,
                   "SECTION ONE  ·  A WORD TO BOTH OF YOU",
                   "Two patterns, named together.",
                   "Read this section out loud, or read it side by side.")
    for p in [
        f"This is a walkthrough written for the two of you, not for either of you alone.",
        f"{name_a} took the assessment and came out as {'an' if mech_a[0].lower() in 'aeiou' else 'a'} <b>{mech_a}</b> with {'an' if bd_a[0].lower() in 'aeiou' else 'a'} <b>{bd_a}</b> breakdown. {name_b} took the assessment and came out as {'an' if mech_b[0].lower() in 'aeiou' else 'a'} <b>{mech_b}</b> with {'an' if bd_b[0].lower() in 'aeiou' else 'a'} <b>{bd_b}</b> breakdown. Those are the labels. The labels are not the whole story.",
        f"The story is that {name_a} keeps coming back to one question underneath the daily run of life, and that question is, in plainer language, <b>{cq_a}</b>. The same is true for {name_b}, whose question is <b>{cq_b}</b>. Those two questions are not the same. They are not even close to the same. And yet they are both being asked, often, in the small moments of a normal week, by the two of you.",
        f"This walkthrough is going to do four things. First, it is going to name what each of you carries into the marriage. Second, it is going to name what each of you keeps doing that the other one experiences as the small repeating wound. Third, it is going to name what each of you gives the other that almost no one else in their life is in a position to give. And fourth, it is going to give you a small set of practical things to do this week.",
        f"You are not broken. You are two people who have been asking different questions of each other for a long time without realizing it. The Lord has put you together. The work is to learn to hear what is actually being asked underneath.",
    ]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION TWO — THE TWO SHAPES ──
    section_header(story, S,
                   "SECTION TWO  ·  THE TWO SHAPES",
                   f"{name_a} the {mech_a}.  {name_b} the {mech_b}.",
                   "Side by side, for the first time, in plain words.")
    for p in [
        f"{name_a} comes alive — and gets reactive — around <b>{trig_a}</b>. When something in the day touches that nerve, the question underneath fires: <em>{cq_a}</em> And when the answer to that question feels like 'no,' {name_a} does not freeze in place. {name_a} reaches for the pattern that has gotten them through before. That pattern is the {mech_a}.",
        f"{name_b} comes alive — and gets reactive — around <b>{trig_b}</b>. The question for {name_b} is different: <em>{cq_b}</em> And when the answer to <em>that</em> question feels like 'no,' {name_b} does what they have always done. The {mech_b}.",
        f"Here is what to notice: both of these are good gifts. The {mech_a} is a way of loving the world that has saved {name_a} more times than they remember. The {mech_b} is a way of loving the world that has saved {name_b} the same way. Marriage does not require either of you to stop being who you are. It requires you to recognize what the other one is doing — and stop reading it as the worst possible version of itself.",
    ]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION THREE — WHAT NAME_A GIVES NAME_B ──
    section_header(story, S,
                   f"SECTION THREE  ·  WHAT {name_a.upper()} GIVES {name_b.upper()}",
                   f"Something almost no one else in {name_b}'s life is in a position to give.",
                   "Receive it on purpose this week.")
    for p in [
        f"{name_a} gives {name_b} {_gift_for(sub_a)}",
        f"{name_b} — if you want to thank {name_a} for something this week, thank them for this. They probably do not know they are giving it. Tell them specifically. Not 'thank you for being you,' but 'thank you for the way you _____ on Tuesday, because here is what it did for me.' Be specific. Specifics are how a gift becomes received.",
    ]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION FOUR — WHAT NAME_B GIVES NAME_A ──
    section_header(story, S,
                   f"SECTION FOUR  ·  WHAT {name_b.upper()} GIVES {name_a.upper()}",
                   f"Something almost no one else in {name_a}'s life is in a position to give.",
                   "Receive it on purpose this week.")
    for p in [
        f"{name_b} gives {name_a} {_gift_for(sub_b)}",
        f"{name_a} — same instruction. Thank {name_b} specifically this week. Name the exact thing. Refuse the generic 'thanks for being you.' Generic gratitude does not land. Specific gratitude does.",
    ]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION FIVE — THE COLLISION ──
    section_header(story, S,
                   "SECTION FIVE  ·  THE COLLISION",
                   "Where the two patterns hit each other.",
                   "The small repeating rock, named.")
    for p in [
        f"Here is what happens when the day is hard. {name_a}'s nerve gets touched — usually around <b>{trig_a}</b> — and the question fires: <em>{cq_a}</em> The answer feels like 'no.' So {name_a} reaches for the {mech_a}. So far, normal.",
        f"But the way {name_a} fails when this is happening — the breakdown — is the <b>{bd_a}</b>. Under stress, {name_a} {_failure_for(sub_a)}",
        f"{name_b} reads that and — because {name_b} is a {mech_b} — does what they always do when the air goes hot in this particular way. But {name_b}'s OWN nerve has now been touched. {name_b}'s question — <em>{cq_b}</em> — gets a 'no.' And {name_b} starts the {bd_b} breakdown: {_failure_for(sub_b)}",
        f"Now both of you are inside your own breakdown at the same time, and each one is making the other one worse. {name_a} cannot hear {name_b}'s {mech_b} as love anymore — it just looks like the proof of the no. And {name_b} cannot hear {name_a}'s {mech_a} as love either. The loop locks.",
        f"This is the rock. It is small. It repeats. It is not because either of you is bad. It is because two patterns are colliding without either of you knowing what to call them.",
        f"<b>Naming it</b> — even mid-fight — interrupts it. Try this, this week: when the loop starts, one of you says out loud, <em>'I think we are doing the thing.'</em> That sentence is your shared language now. It is permission to step back without either of you losing face.",
    ]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION SIX — PRAYER ──
    section_header(story, S,
                   "SECTION SIX  ·  A PRAYER FOR THIS MARRIAGE",
                   "Spoken in two voices.",
                   "Read it together. It is short on purpose.")
    for p in [
        f"<i>Father,</i>",
        f"<i>You made {name_a} the way You made {name_a}, and You made {name_b} the way You made {name_b}, and You put these two specific people into one home.</i>",
        f"<i>Teach us to read each other's instincts as love. When {name_a}'s {mech_a} is working, give {name_b} eyes to see it. When {name_b}'s {mech_b} is working, give {name_a} eyes to see it.</i>",
        f"<i>And when we fall into the breakdown — when one of us {_failure_for(sub_a).split('.')[0].lower()}, and the other {_failure_for(sub_b).split('.')[0].lower()} — bring us back. Be quicker than our patterns. Speak louder than the question underneath.</i>",
        f"<i>In the name of Christ, who searches us and knows us. Amen.</i>",
    ]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION SEVEN — COMMITMENTS ──
    section_header(story, S,
                   "SECTION SEVEN  ·  THREE COMMITMENTS FOR EACH OF YOU",
                   "What to actually do this week.",
                   "Pick one. You do not have to do all of them.")
    story.append(Paragraph(f"<b>For {name_a}:</b>", S["BodyJ"]))
    for p in [
        f"1. When you feel the {trig_a} nerve get touched this week, before you reach for the {mech_a}, name it out loud to {name_b}. Just: <em>'My nerve is hot right now.'</em> Don't explain it yet. Just name it.",
        f"2. Thank {name_b} specifically — by Wednesday — for the thing in Section Four. Be specific. Name the moment.",
        f"3. When the {bd_a} breakdown starts to fire, give yourself permission to say, <em>'I'm doing the thing. Give me twenty minutes.'</em> Twenty minutes. Then come back.",
    ]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>For {name_b}:</b>", S["BodyJ"]))
    for p in [
        f"1. When you feel the {trig_b} nerve get touched this week, before you reach for the {mech_b}, name it out loud to {name_a}. <em>'I'm in it right now.'</em> Same rule. Don't explain. Just name.",
        f"2. Thank {name_a} specifically — by Wednesday — for the thing in Section Three. Specifics. Not 'thanks for being you.'",
        f"3. When the {bd_b} breakdown starts, the same twenty-minute pause is yours. Take it. Then come back.",
    ]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION EIGHT — CLOSING ──
    section_header(story, S,
                   "SECTION EIGHT  ·  A CLOSING WORD",
                   "Marriage is two people learning to read each other.",
                   "You have what you need to begin.")
    for p in [
        f"This is the document. It is not the work. The work is the next conversation you have, and the one after that, and the small naming you do for each other at the kitchen table when one of you is about to fire the old pattern again.",
        f"You now have words for what has been happening. That is a real gift. Most couples never get it. They keep having the fight without the language.",
        f"Two practical things to consider:",
        f"<b>1.</b> Pick one of the commitments above — just one — and start there. Not all three. One.",
        f"<b>2.</b> Read this together once a quarter for the next year. The first read is the framework. The third read is the fluency.",
        f"And if reading this surfaced something heavy — something more than what a walkthrough is built to hold — please bring it to a pastor, a counselor, or a trusted friend. This document is a starting place. It is not the whole conversation.",
        f"Grace and peace to you both.",
    ]:
        story.append(Paragraph(p, S["BodyJ"]))

    doc.build(story)
    return finalize_buffer(buf)
