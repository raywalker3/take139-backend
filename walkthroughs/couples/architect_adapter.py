"""Couples Walkthrough — Architect + Adapter.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where Spouse A is an Architect and
Spouse B is an Adapter. First names are substituted from the submissions:
    {name_a}  -> the Architect spouse's first name
    {name_b}  -> the Adapter spouse's first name

Architect: trigger Disrespect/Injustice, core question "Am I protected?"
Adapter:   trigger Control/Shame, core question "Am I free?" / "Am I acceptable?"

Key pastoral dynamic: The Architect plans from fixed reference points.
The Adapter has fluid reference points. The Architect experiences the Adapter
as elusive; the Adapter experiences the Architect as inflexible. The marriage
looks like a smart partnership from outside, but beneath lies a collision
between knowability and fluency.
"""
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    Paragraph, Spacer, KeepTogether, HRFlowable, Table, TableStyle,
    PageBreak, NextPageTemplate,
)

from ..base import (
    make_doc, make_styles, finalize_buffer, ensure_fonts,
    section_header,
    PAGE_W, MARGIN_L, MARGIN_R,
    PAPER, INK, ACCENT, ACCENT_HER, MUTED, RULE, HIGHLIGHT_BG,
)


def _first_name(sub, default="Spouse"):
    full = (sub.name or "").strip()
    if not full:
        return default
    return full.split()[0]


def _profile_card(S, name, accent, trigger, question, mechanism, breakdown):
    body = [
        Paragraph(name, S["ProfileCardName"]),
        Paragraph("TRIGGER", S["ProfileCardLabel"]),
        Paragraph(trigger, S["ProfileCardVal"]),
        Paragraph("CORE QUESTION", S["ProfileCardLabel"]),
        Paragraph(question, S["ProfileCardVal"]),
        Paragraph("MECHANISM", S["ProfileCardLabel"]),
        Paragraph(mechanism, S["ProfileCardVal"]),
        Paragraph("BREAKDOWN", S["ProfileCardLabel"]),
        Paragraph(breakdown, S["ProfileCardVal"]),
    ]
    return Table(
        [[body]],
        colWidths=[(PAGE_W - MARGIN_L - MARGIN_R - 18) / 2.0],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HIGHLIGHT_BG),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 16),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
            ("LINEABOVE", (0, 0), (-1, 0), 2, accent),
        ]),
    )


QUESTION_TYPE_LABELS = {
    "hypothetical": "HYPOTHETICAL", "observation": "NOTICE", "playful": "PLAYFUL",
    "fill-in-blank": "FILL IN THE BLANK", "one-word": "ONE WORD",
    "forward-looking": "LOOK FORWARD", "theological": "GOD WITH US",
    "shared-identity": "WE ARE", "strength": "NAME THE GIFT",
    "hard": "THE HARDER ONE", "profile-aware": "FROM THE WALKTHROUGH",
    "blessing": "BLESSING", "prayer": "PRAYER",
}


def _question_card(kind, question_text, note_text, index_label):
    type_label = QUESTION_TYPE_LABELS.get(kind, kind.upper())
    chip = ParagraphStyle("Chip", fontName="Inter-SemiBold", fontSize=8, leading=11,
                         textColor=ACCENT, spaceAfter=2)
    q_style = ParagraphStyle("QText", fontName="Fraunces", fontSize=13, leading=20,
                             textColor=INK, spaceAfter=8)
    note_style = ParagraphStyle("QNote", fontName="Inter-Italic", fontSize=9.5, leading=14,
                                textColor=MUTED, spaceAfter=2)
    inner = [
        Paragraph(f"{index_label} &nbsp;&middot;&nbsp; {type_label}", chip),
        Paragraph(question_text, q_style),
        Paragraph(note_text, note_style),
    ]
    return Table(
        [[inner]],
        colWidths=[PAGE_W - MARGIN_L - MARGIN_R],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HIGHLIGHT_BG),
            ("LINEABOVE", (0, 0), (-1, 0), 1.5, ACCENT),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ]),
    )


def _round_header(story, S, round_num_roman, title, subtitle):
    rh_eyebrow = ParagraphStyle("RhEyebrow", fontName="Inter-Medium", fontSize=9, leading=14,
                                textColor=ACCENT, spaceAfter=4)
    rh_title = ParagraphStyle("RhTitle", fontName="Fraunces-SemiBold", fontSize=20, leading=26,
                              textColor=INK, spaceAfter=4)
    rh_sub = ParagraphStyle("RhSub", fontName="Fraunces-Italic", fontSize=12, leading=18,
                            textColor=INK, spaceAfter=12)
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"ROUND {round_num_roman}", rh_eyebrow))
    story.append(Paragraph(title, rh_title))
    story.append(Paragraph(subtitle, rh_sub))


def _render_round(story, round_num, round_data, title, subtitle):
    romans = {1: "ONE", 2: "TWO", 3: "THREE", 4: "FOUR", 5: "FIVE", 6: "SIX"}
    _round_header(story, None, romans[round_num], title, subtitle)
    for i, (kind, q, note) in enumerate(round_data, 1):
        idx = f"{round_num}.{i}"
        story.append(KeepTogether([_question_card(kind, q, note, idx)]))
        story.append(Spacer(1, 14))


# ──────────── PROSE — uses {name_a} (Architect) and {name_b} (Adapter) ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small "
    "repeating ones &mdash; the same misunderstanding in slightly different clothes, "
    "three or four times a week, year after year, until both people have forgotten "
    "what they were originally hoping for.",

    "In your marriage, the small repeating rock has a particular shape. It arrives "
    "on an ordinary evening, usually around something logistical &mdash; a plan, "
    "a preference, a decision that one of you assumed was settled and the other "
    "assumed was still open. Nobody raises their voice. Nobody storms out. But "
    "something tightens in both of you, and by the next morning neither of you "
    "is quite sure what happened or who started it. You have been here before. "
    "You will be here again. And the question this document is asking is whether "
    "you would like to understand it.",

    "You are both reading this because you have decided to look. That decision "
    "is more significant than it appears. Most couples spend a decade navigating "
    "around the small repeating rock without naming it. Naming it is more than "
    "half the work.",

    "Here is what I intend to do. I will name what each of you brings the other "
    "that you could not have built alone &mdash; the genuine, theological gift "
    "your two shapes form when they are at their best. Then I will name the "
    "collision your two questions create, in the specific way it fires in your "
    "marriage. Then I will name the harder picture &mdash; when both of you are "
    "in breakdown at once &mdash; and what to do when you can still see it "
    "happening. Then I will hand each of you a set of commitments, not as rules "
    "but as the small daily practices that, over years, change the temperature "
    "of a home.",

    "Read it together if you can. If not, read it separately and then sit down "
    "with it. Argue with what does not fit. Stay with what does. The goal is not "
    "insight. The goal is a marriage in which the small repeating rocks become "
    "smaller, less repeating, and finally a part of the landscape you can both "
    "laugh at.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, "
    "on paper, side by side. Most couples never see their two profiles next to each "
    "other. You are about to.",
]

TWO_SHAPES_BODY = [
    "{name_a}, you are an <b>Architect</b> whose body reads disrespect and injustice "
    "as alarm signals, and whose deepest question is whether you are protected. "
    "You build structures &mdash; plans, systems, reliable expectations &mdash; "
    "because you believe, in your bones, that most suffering is a function of "
    "insufficient preparation. When someone violates the structure or disregards "
    "your design, an <b>Attorney</b> takes the floor. Not to win an argument, "
    "but to establish that the wrong was real, that the blueprints mattered, "
    "that the breach cannot simply be papered over.",

    "{name_b}, you are an <b>Adapter</b> whose body reads control and shame as "
    "alarm signals, and whose deepest question is whether you are free &mdash; "
    "free to be yourself, free from the pressure to be a particular version of "
    "yourself in this relationship. You move through the world the way a musician "
    "moves through different keys: the same instrument, a different sound depending "
    "on what the room requires. You are genuinely present in every version. "
    "But when someone tries to fix you in place &mdash; to name which version is "
    "the real one, or to prosecute a version you no longer quite recognize "
    "&mdash; a <b>Quiet Exit</b> or a <b>Plea</b> can follow, depending on whether "
    "the threat feels like a cage or like the loss of connection.",

    "Notice what these two profiles do <i>not</i> share, and then notice what they "
    "share underneath. You are not asking the same question. {name_a} is asking "
    "<i>am I protected?</i> &mdash; a question that wants stability, predictability, "
    "and a partner with knowable preferences. {name_b} is asking <i>am I free?</i> "
    "&mdash; a question that wants room to move, the latitude to change, and a "
    "partner who can hold a fluid self without pressing it into a fixed mold. "
    "Both are legitimate. Both are, in the architecture of a marriage, genuinely "
    "difficult to give each other.",

    "Beneath the two questions, however, there is the same root. You are both "
    "people who have built a strategy to prevent a particular kind of pain. "
    "{name_a}'s strategy is to know what is coming. {name_b}'s strategy is to "
    "become what the moment needs. Both strategies are forms of self-protection, "
    "and both have served each of you well in the world outside this marriage. "
    "Inside it, they pull in opposite directions &mdash; and that pull is what "
    "this document is about.",

    "From the outside, your pairing often looks like a natural division of labor: "
    "the Architect provides the structure, the Adapter provides the relational "
    "warmth. People who know you both may have said something like that. There "
    "is truth in it. But underneath the apparent efficiency is a deeper friction "
    "that neither of you may have found the words for yet. {name_a} cannot "
    "understand why {name_b} does not have stable preferences. {name_b} cannot "
    "understand why {name_a} treats every preference as fixed law. This document "
    "is going to name that friction by its right name, and then show you a way "
    "through it.",
]

GIFT_TO_A = [
    "{name_b} gives {name_a} something the Architect almost never builds for "
    "himself: <b>a room that does not require him to be certain.</b>",

    "The Architect's world is organized around the reduction of uncertainty. "
    "Plans exist to make the future manageable. Structures exist to prevent "
    "the collapse that insufficient preparation invites. In most of the rooms "
    "{name_a} walks through in a week &mdash; at work, in community, in the "
    "small negotiations of a shared life &mdash; the Architect's certainty is "
    "precisely what is wanted. People come to him with open questions; he leaves "
    "them with answers. This is a genuine gift. It is also exhausting, and "
    "{name_a} may not always know how exhausting it has been, because there has "
    "rarely been a room where the exhaustion was allowed to show.",

    "{name_b}, by the nature of the Adapter mechanism, is one of the few people "
    "in {name_a}'s world who does not require the Architect to have already "
    "figured everything out. The Adapter, skilled at reading what the room "
    "most needs, will often meet {name_a} in the register he is actually in "
    "rather than the register he is performing. When {name_a} is tired, {name_b} "
    "will frequently sense it before it is named. When {name_a} is carrying "
    "something he cannot quite articulate, {name_b} will often create the "
    "space in which the un-articulated thing has room to surface. This is not "
    "a minor gift. For a person whose vocation is to hold things together, "
    "being with someone who can meet you before you have organized yourself "
    "is rare and quietly irreplaceable.",

    "There is a theological word for what {name_b} gives {name_a}. It is "
    "<i>grace</i> &mdash; not in the formal doctrinal sense, but in the older "
    "meaning of unearned favor, presence that does not require performance as "
    "its entry fee. The Architect earns his place in most rooms. {name_b} is "
    "one of the rooms where he does not have to.",

    "{name_a} &mdash; if you want to thank {name_b} for something this week, "
    "thank her for the moments when she met you where you were rather than "
    "where the plan said you were supposed to be. She may not have known she "
    "was doing it. Adapters rarely know their attunement registers as a gift; "
    "they have been told often enough that their fluency is simply inconsistency. "
    "Tell her that the specific quality of her presence &mdash; the way she "
    "reads the room you are actually in rather than the room you have scheduled "
    "&mdash; is one of the kindest things in your week. She will not know what "
    "to do with the compliment. Say it anyway.",

    "{name_b} &mdash; what {name_a} receives from you, in the moments when "
    "you simply meet him without demanding that he be three steps ahead, is "
    "the closest thing to rest he gets in most weeks. The fluency in you that "
    "has sometimes been called inconsistency is, for him, a kind of mercy.",
]

GIFT_TO_B = [
    "{name_a} gives {name_b} something Adapters rarely give themselves: "
    "<b>a fixed point.</b>",

    "The Adapter's world is organized around responsiveness. Every room has "
    "its own register, its own needs, its own version of {name_b} that the "
    "room has called forth. This fluency is a genuine gift &mdash; the Adapter "
    "is, in almost any company, one of the most genuinely present people there. "
    "But the cost, which accumulates slowly and is rarely named until it has "
    "become significant, is the absence of a stable center. When every room "
    "calls forth a version, the question <i>which version is me?</i> eventually "
    "becomes genuinely difficult to answer. The Adapter, who has never required "
    "a fixed center to function, may not notice the cost until the moment "
    "when someone asks &mdash; plainly, without any version to calibrate to "
    "&mdash; <i>what do you actually want?</i>",

    "{name_a}, by virtue of being an Architect, is one of the few people in "
    "{name_b}'s life who does not change the question depending on what answer "
    "would be most convenient. The Architect has preferences. He holds them. "
    "The plan he brings to a decision is not a suggestion. This can feel "
    "inflexible &mdash; and we will name the cost of it in due course &mdash; "
    "but it is also a form of constancy that the Adapter, who has rarely "
    "been allowed to rest against someone else's certainty, may have needed "
    "without knowing it. {name_b} can push against {name_a} and know "
    "something will push back. There is, in that resistance, a strange safety.",

    "The theological image for what {name_a} gives {name_b} is the one "
    "the Psalms return to most often: <i>the rock.</i> Not a rock that "
    "refuses to be climbed, but a rock that does not move when you lean "
    "against it. In a soul that has spent years reading which way the "
    "room is leaning, the experience of something that simply holds its "
    "ground &mdash; not cruelly, not rigidly, but because it is genuinely "
    "solid &mdash; is formative in a way that is difficult to overstate.",

    "{name_b} &mdash; if you want to thank {name_a} for something this week, "
    "thank him for holding a position even when you were not sure you agreed "
    "with it. The Architect's constancy, which can feel like inflexibility "
    "when the Adapter wants room to change, is also the thing that makes "
    "the marriage feel like it has a spine. You have sometimes been "
    "the one who provided the warmth. He has often been the one who "
    "provided the structure on which the warmth could hang. Both are "
    "necessary. Tell him you have noticed.",

    "{name_a} &mdash; what {name_b} receives from you, when you hold "
    "a position, keep a commitment, name a preference and mean it, is "
    "the experience of a relationship with a fixed point. The thing in "
    "you that has sometimes been called rigidity is, for her, a trellis "
    "against which a very fluid life can grow.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of "
    "you, even if you have not named it quite this way.",

    "{name_a}'s core question is <i>am I protected?</i> {name_b}'s is "
    "<i>am I free?</i> In the abstract, these two questions are not opposed. "
    "In the daily mechanics of a marriage &mdash; in the Tuesday evening "
    "conversation about the weekend, in the Sunday morning negotiation "
    "about the next three months &mdash; they ask for things that are "
    "genuinely difficult to give each other simultaneously.",

    "Protection wants knowability. The Architect builds his structures "
    "from fixed reference points, and his partner's preferences are "
    "among the most important of those points. When {name_a} says "
    "<i>what do you want to do for the holidays?</i> he is not making "
    "small talk. He is gathering data for a structure he is beginning "
    "to build. The answer he needs is not a gesture toward possibility "
    "but an actual coordinate &mdash; something he can mark on the "
    "map and plan from. When the answer shifts &mdash; when a preference "
    "that was stated last Tuesday is different from the preference being "
    "stated this Tuesday &mdash; the Architect does not receive this as "
    "ordinary human ambivalence. He receives it as a coordinate that "
    "has moved, and a structure that must now be redesigned. The "
    "question underneath the redesign is, quietly but urgently: "
    "<i>can I plan around this person? Can I protect this marriage "
    "if I cannot count on knowing where she is?</i>",

    "Freedom wants fluency. The Adapter's sense of self is not gathered "
    "from a fixed interior position but borrowed, over time, from the "
    "feedback of the rooms she has inhabited. This is not dishonesty. "
    "It is a different architecture of selfhood &mdash; one that is "
    "genuinely more responsive to context, and genuinely less stable "
    "across contexts, than the Architect's. When {name_b} changes her "
    "mind about the holidays, she is not revising a plan. She is simply "
    "present in a different moment, and the present moment has called "
    "forth a different version of what seems good. To her, this is "
    "ordinary. To {name_a}, it reads as a failure of knowability "
    "&mdash; and the Architect's response to a failure of knowability "
    "is to press for a fixed answer. Which is precisely what the "
    "Adapter's trigger hears as control.",

    "Here is the collision in slow motion. {name_a} asks a planning "
    "question. {name_b} gives a tentative answer. {name_a} treats the "
    "tentative answer as a coordinate and begins to build from it. "
    "Two days later, {name_b} has a different sense of things "
    "&mdash; the room has shifted, the moment is different, a new "
    "version of what seems right has emerged. She mentions the shift "
    "casually, the way the Adapter mentions such things, because to "
    "her it is not a big revision. {name_a} does not experience it "
    "as a small revision. He experiences it as the map being changed "
    "after he has already begun to build. His trigger fires: "
    "<i>disrespect &mdash; she did not take the plan seriously. "
    "Injustice &mdash; the ground shifted without warning.</i>",

    "He does not say all of this. He says something more compressed "
    "&mdash; something that, to {name_b}, sounds like a demand for a "
    "fixed answer, a pressure to commit to a version she is not sure "
    "she holds yet. Her trigger fires: <i>control &mdash; he is "
    "pressing me to be a particular person in a particular position "
    "and the pressing feels like a cage.</i> She goes quiet. The "
    "Adapter, when threatened with the loss of freedom, withdraws "
    "&mdash; not dramatically, but distinctly. And the Architect, "
    "who has learned to read silence as disregard, feels the "
    "withdrawal as confirmation of the original threat: "
    "<i>she is not taking this seriously. I cannot plan from this.</i>",

    "Neither of you is wrong. The Architect needs the Adapter to be "
    "more knowable &mdash; this is a legitimate need. The Adapter "
    "needs the Architect to grant the legitimate range of selves she "
    "actually has &mdash; this too is legitimate. The theologian Paul, "
    "writing to a church that was struggling with exactly this question "
    "of how different people with different wiring could hold together, "
    "said: <i>For as in one body we have many members, and the members "
    "do not all have the same function, so we, though many, are one "
    "body in Christ, and individually members one of another.</i> "
    "(Romans 12:4&ndash;5) He was addressing a church, but the "
    "principle reaches into every covenant between people whose "
    "shapes do not naturally mirror each other. The marriage itself "
    "can hold an Architect's stability and an Adapter's fluency "
    "the way the body holds both bone and muscle &mdash; the one "
    "provides the frame; the other provides the range of motion. "
    "Neither is dispensable. Neither should be flattened into "
    "the other.",

    "{name_a}, when {name_b} changes her mind, the translation is "
    "almost never <i>she does not respect the plan.</i> It is "
    "<i>she is in a different moment than she was, and her sense "
    "of things has shifted with it.</i> The right move is not to "
    "press for a locked answer but to ask what has changed, and "
    "to receive the answer as information rather than as a violation. "
    "You can build from approximate coordinates. You have done it "
    "before. What you cannot build from is a partner who has gone "
    "silent because the pressing felt like a cage.",

    "{name_b}, when {name_a} presses for a clear preference, the "
    "translation is almost never <i>he is trying to control who "
    "I am.</i> It is <i>he is trying to love us by securing the "
    "next three rooms, and he cannot do that without knowing "
    "where I am.</i> The right move is not to go quiet but to name "
    "the uncertainty directly &mdash; <i>I am not sure yet, "
    "and I will tell you by Thursday</i> &mdash; and then to "
    "actually tell him by Thursday. The Architect does not need "
    "certainty as much as he needs a coordinate he can trust. "
    "A provisional answer, honestly held and faithfully revised, "
    "is workable. Silence is not.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be moments &mdash; not most weeks, "
    "but they will come &mdash; when the small collision in the kitchen "
    "escalates and both of you are in breakdown at the same time. The "
    "Attorney is up. The Quiet Exit is pulling. The room is tense and "
    "quiet in the particular way that is harder than loud, because the "
    "silence is full of everything neither of you is saying. Neither of "
    "you, in that moment, has access to the more thoughtful person "
    "you were three hours ago.",

    "Here is what is happening, named plainly so you can both see it.",

    "{name_a}, when the Attorney is on his feet, he is not arguing with "
    "{name_b}. He is arguing with an old record in his head &mdash; "
    "an accumulated file of moments when the ground shifted without "
    "warning and he was left building on sand. The evidence he marshals "
    "against {name_b} in this moment is not fabricated. Each exhibit "
    "is real. The Tuesday she said one thing and did another. The "
    "holiday that was planned around a preference she later revised. "
    "The moment he worked to build something around her coordinate "
    "and the coordinate moved. He is presenting these, in his mind, "
    "as a brief. In hers, they are arriving as a prosecution.",

    "But here is the particular pastoral complexity with the "
    "Architect's Attorney in this marriage. The brief cites statements "
    "{name_b} made in one version of herself &mdash; the person she "
    "was on the Tuesday when the preference was stated, the mood "
    "she was in when the plan was agreed to. The Adapter may "
    "genuinely not know that she is the same person across contexts "
    "in the way the Attorney assumes. She cannot defend those "
    "statements, not because she is dishonest, but because they "
    "were made by a version of herself she may no longer fully "
    "recognize. The witness the Attorney is cross-examining is "
    "not the witness in the room. James writes, pastorally, of "
    "the person who is <i>double-minded, unstable in all his ways</i> "
    "(James 1:6&ndash;8) &mdash; and this is not an accusation "
    "against {name_b}'s character. It is a description of a soul "
    "that has not yet found its anchor in a self that is stable "
    "enough to be held to its word. The pastoral response is not "
    "judgment. It is the patient work of helping {name_b} find "
    "the center from which a reliable word can be offered. "
    "This is the Architect's opportunity in the marriage: "
    "not to prosecute the inconsistency but to be the "
    "stable presence that makes consistency possible over time.",

    "{name_b}, when the Quiet Exit begins in you, you are not "
    "coldly withdrawing from {name_a}. You are running a much "
    "older calculation &mdash; one that was written in a much "
    "earlier room &mdash; about whether the version of yourself "
    "that is present right now is the one he wants, and whether "
    "staying in the room means being pressed into a shape you "
    "cannot hold. The Attorney's brief lands on you not as "
    "a loving attempt at accountability but as evidence that "
    "you have failed to be the stable, knowable person the "
    "plan required. And the Adapter's response to that evidence "
    "is not to defend itself. The Adapter's response is to "
    "recede &mdash; to become less present, less committed, "
    "less available &mdash; because the version being "
    "prosecuted is one the Adapter cannot recognize or protect.",

    "This is one of the most painful kinds of marital conflict, "
    "because both of you feel you are speaking truth, and neither "
    "of you is wrong. The Attorney holds real evidence. The "
    "Adapter's receding is a real response to real pressure. "
    "The way forward is not to adjudicate the case. It is "
    "to interrupt it before it reaches the courtroom. "
    "Paul writes in Ephesians 4:25: <i>let each one of you "
    "speak the truth with his neighbor, for we are members "
    "one of another.</i> Notice the direction of the "
    "obligation: speaking truth <i>with</i> one another, "
    "not speaking truth <i>at</i> one another. The Architect's "
    "prosecution often demands a stability the Adapter "
    "has not yet been given. The Adapter's receding often "
    "withholds the honest word the Architect needs to stop "
    "building the case. Both failures are real. Both have a remedy.",

    "<b>One of you, not both, calls the pause.</b> Whoever "
    "notices first what is happening says, out loud: "
    "<i>this is the loop. Twenty minutes.</i> No final word. "
    "No last point on the record. Twenty minutes, non-negotiable, "
    "and the only rule of the pause is that no one drafts "
    "the next brief or rehearses the next version of herself "
    "while it is running.",

    "<b>In the twenty minutes, do not strategize. Pray.</b> "
    "Not eloquently. {name_a}: <i>Lord, my Attorney is up. "
    "Quiet the brief. Help me see her as a person and not "
    "a case I cannot win.</i> {name_b}: <i>Lord, the Exit "
    "is pulling. Help me stay. Help me speak one true "
    "sentence from the self underneath the versions.</i>",

    "<b>When you come back, each of you says one sentence.</b> "
    "{name_a}, your sentence is not the brief. It is one "
    "true thing you actually felt, beginning with the word "
    "<i>I.</i> {name_b}, your sentence is not the receding. "
    "It is one honest thing from the self below the versions "
    "&mdash; not the version that was most convenient, not "
    "the version most likely to close the gap, but the actual "
    "true thing. <i>I felt caged when the question kept "
    "coming.</i> That is one sentence. <i>I was afraid "
    "the ground was shifting again and I could not build.</i> "
    "That is one sentence. Both of you can give one sentence. "
    "Then stop.",

    "<b>Neither of you is the problem.</b> The Attorney and "
    "the Quiet Exit are old mechanisms doing the only job "
    "they were ever trained to do. The truest thing about "
    "both of you is not your breakdown pattern. It is that "
    "you are a man and a woman who chose each other, before "
    "God, and are committed to the slow work of learning "
    "each other's grammar. That is what covenant actually "
    "looks like from the inside. It is not a feeling. "
    "It is a decision renewed on the ordinary Tuesdays "
    "when the decision is least convenient.",
]

COMMITMENTS_INTRO = [
    "What follows are six commitments &mdash; three from {name_a}, three from "
    "{name_b}. They are not vows in the legal sense. They are the small daily "
    "practices that, offered to each other freely and kept with reasonable "
    "consistency, change the temperature of a home over months and years. "
    "Read each one slowly. If one of you cannot make a particular commitment "
    "in good faith yet, do not make it. The goal is not performance. "
    "It is honesty.",
]

A_COMMITMENTS = [
    (
        "I will hold the marriage steady without holding you rigid.",
        "{name_b}, I commit to separating the stability of our marriage from "
        "the stability of your preferences. The plan can hold even when your "
        "coordinates shift, if I am willing to hold it loosely enough to "
        "accommodate a partner whose sense of things moves with the moment. "
        "I will ask once for a preference, and I will receive a provisional "
        "answer without treating it as a betrayal when it changes. I can "
        "build from approximate coordinates. I will practice doing so.",
    ),
    (
        "I will translate your silence before the Attorney rises.",
        "{name_b}, when you go quiet or begin to recede, I commit to "
        "translating it correctly before my mechanism takes over. "
        "Your silence is not disrespect. Most of the time, it means "
        "the pressing felt like a cage, and I pressed when I should have "
        "paused. I will name what I am noticing in one question rather "
        "than one accusation: <i>did I just make you feel like I needed "
        "you to be a particular person right now?</i> I will wait for "
        "the answer. I can work with what the answer gives me.",
    ),
    (
        "I will name what I am afraid of, not just what I need.",
        "{name_b}, when I feel the plan losing its anchor, I commit to "
        "telling you what I am actually afraid of in one sentence, "
        "rather than pressing for certainty as though certainty were "
        "the point. The point is almost never the plan. The point is "
        "that I am afraid the ground is shifting and I do not know "
        "how to protect us from it. You deserve to know that "
        "is what is happening. The marriage deserves a voice "
        "that names the fear rather than prosecuting the evidence.",
    ),
]

B_COMMITMENTS = [
    (
        "I will offer you the same self across versions when it matters most.",
        "{name_a}, I commit to giving you a consistent word on the things "
        "that matter most to our shared life &mdash; not by suppressing "
        "my natural fluency, but by distinguishing between the preferences "
        "that are genuinely in motion and the commitments that are not. "
        "The question of what I want for dinner is legitimately open. "
        "The question of whether I am committed to this marriage is not. "
        "I will learn the difference, and I will give you coordinates "
        "you can build from in the places that require them.",
    ),
    (
        "I will name the cage before I exit the room.",
        "{name_a}, when I feel the pressing start &mdash; when the question "
        "keeps coming and the freedom I need is beginning to contract "
        "&mdash; I commit to naming it before I go quiet. "
        "One sentence: <i>I need room to not know yet.</i> "
        "Or: <i>I feel like I am being pressed into a version of "
        "myself I have not found yet.</i> I will not go silent "
        "and ask you to decode the silence. You cannot. "
        "I will give you one honest sentence and trust that "
        "you can receive it.",
    ),
    (
        "I will bring you the self below the versions.",
        "{name_a}, I commit to showing you, in small and regular ways, "
        "the person underneath the adaptation &mdash; not the version "
        "most likely to resolve the tension, not the version that "
        "reads what you need and becomes it, but the actual "
        "un-calibrated me. This will sometimes be less impressive "
        "than the adaptive version. It may be less smooth, less "
        "warm, less easy to be around. But it will be real, and "
        "you deserve real. Our marriage deserves a self it can "
        "know, not only a self it can enjoy.",
    ),
]

PRAYER = [
    "Father,",

    "You set these two next to each other, and you knew exactly what "
    "you were doing. You knew the Architect would need someone who "
    "could read him before he had organized himself. You knew the "
    "Adapter would need someone who would hold their ground when "
    "she had not yet found her own. You knew the Tuesday evenings "
    "that would feel like too much structure and the ones that would "
    "feel like too little. You knew all of it before either of them "
    "said yes.",

    "Teach them the grammar of each other. Teach {name_a} to hold "
    "the marriage steady without holding {name_b} rigid &mdash; "
    "to receive a fluid preference without treating it as a "
    "violation of the plan, to see in her movement a genuine "
    "responsiveness rather than a failure of knowability. "
    "Teach {name_b} to offer {name_a} the self below the versions "
    "&mdash; not the calibrated version, not the one most likely "
    "to keep the peace, but the actual un-adapted person "
    "you named before any room existed to call forth a version.",

    "When the Attorney rises in {name_a}, remind him that you "
    "are his advocate, and that the verdict has been spoken, "
    "and that no brief he builds in this marriage will ever "
    "establish his safety more surely than the one Christ "
    "has already argued on his behalf. When the Exit pulls "
    "in {name_b}, remind her that she is named &mdash; "
    "not by the room's reflection, not by the version "
    "most recently approved, but by a Father who chose "
    "her in Christ before the foundation of the world, "
    "before any room existed to require a version.",

    "Make their home a room in which {name_a} can set "
    "down the blueprints for five minutes without the "
    "world collapsing, and {name_b} can be simply present "
    "without calibrating to what the room seems to need. "
    "Make their table a place where one true sentence "
    "is offered and received without prosecution. "
    "Make their covenant the frame on which both of "
    "them can grow &mdash; the stability that the Adapter "
    "needs to find her center, and the warmth that the "
    "Architect needs to remember why the building is worth doing.",

    "And Father, when they are old and the small repeating rocks "
    "have finally become smaller and less repeating, let them look "
    "back and see that the two shapes &mdash; so different, so "
    "predictably in friction &mdash; made something together "
    "that neither of them could have made alone. Let them "
    "recognize, in that looking back, the signature of a "
    "Maker who knew what he was doing when he put them "
    "next to each other.",

    "In the name of the One who is himself the fixed point "
    "around whom all fluid things are free to move.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. "
    "The pages that follow are different. They are meant to be spoken "
    "<i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken "
    "slowly, somewhere quiet, with no children in the room and no "
    "phones on the table. There are six rounds, and they build on "
    "each other. Resist the temptation to skip ahead. Start at "
    "Round One even if it feels too light; the lightness is the point.",

    "Some of the questions are playful. Some are direct. A few are "
    "the kind that, when answered honestly, will sit with you for "
    "a week. None of them are trivia. All of them are an invitation.",

    "<b>How to use it.</b> One of you reads a question aloud. "
    "The one who did not read answers first, in full, without "
    "interruption. Then the reader answers the same question. "
    "Then you move on. You do not have to finish all six rounds "
    "in one night &mdash; two or three rounds, taken seriously, "
    "is often better than racing through all of them. "
    "Save the rest for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. "
    "You may not love everything you hear. Stay with it. "
    "The point of this is not to grade each other's answers. "
    "The point is to be known, and to do the slow work of knowing.",
]

ROUND_1 = [
    (
        "hypothetical",
        "If our marriage were a piece of architecture &mdash; a building "
        "of any kind, anywhere in the world &mdash; what would it be, "
        "and what would be your favorite room in it?",
        "Let the metaphor say what plain language sometimes cannot. "
        "Don't overthink it. Answer with the first image that comes.",
    ),
    (
        "observation",
        "What is something I did for you this week that you noticed "
        "and didn't mention?",
        "Not a complaint. A small noticing. The fact that you noticed "
        "at all is the gift.",
    ),
    (
        "playful",
        "If you had to describe our marriage as a weather pattern, "
        "what would the forecast say right now &mdash; and what would "
        "be your ideal forecast for the next six months?",
        "Yes, really. Answer with the first thing that comes to mind.",
    ),
]

ROUND_2 = [
    (
        "fill-in-blank",
        "I don't think I tell you this enough &mdash; I am amazed "
        "at the way God made you so _______. "
        "Your _______ is a gift to our marriage, and I want to "
        "get better at receiving it.",
        "Two blanks. Be specific. 'Thoughtful' is too easy; "
        "'able to sense what I need before I know it myself' is closer.",
    ),
    (
        "observation",
        "What is one thing you have watched me do this year "
        "that you wish more people could see?",
        "Most of us only ever see ourselves do our most public things. "
        "Tell your spouse about the private ones.",
    ),
    (
        "one-word",
        "If you had to choose one word to describe how it feels "
        "when we are completely in sync &mdash; when the Architect "
        "and the Adapter are working together rather than past each "
        "other &mdash; what word would it be?",
        "One word, said out loud. Then explain it, briefly.",
    ),
]

ROUND_3 = [
    (
        "forward-looking",
        "Five years from now, when we look back on this season, "
        "what do you hope we will say we did well together?",
        "Not what you wish you had done. What you want, when you look back, "
        "to be able to say you actually did.",
    ),
    (
        "theological",
        "Where, in the last month, have you seen God specifically "
        "at work in me &mdash; not the version I perform, "
        "but the real one underneath?",
        "Not where you want him to work. Where you have already seen it. Name it.",
    ),
    (
        "shared-identity",
        "Finish this sentence three times: "
        "'We are the kind of couple who _______.' "
        "Give one playful answer, one true answer, and one aspirational answer.",
        "The 'we' is the point. Let all three answers be real.",
    ),
]

ROUND_4 = [
    (
        "strength",
        "What is something I do for our shared life that you would have "
        "to learn to do for yourself if I were not here?",
        "Hard to ask. Important to hear. Stay with the answer.",
    ),
    (
        "fill-in-blank",
        "One of the gifts of being married to you is that I get to "
        "be _______ in ways I never would have been on my own.",
        "A version of yourself that only exists because this marriage exists. "
        "Name it as specifically as you can.",
    ),
    (
        "observation",
        "Name one moment in our story where you knew, without doubt, "
        "that the Architect and the Adapter had built something "
        "together that neither of us could have built alone.",
        "Tell the story in full. The remembering is part of the strengthening.",
    ),
]

ROUND_5 = [
    (
        "hard",
        "When our patterns collide &mdash; when the plan needs a fixed "
        "answer and the Adapter does not have one yet, or when the "
        "pressing feels like a cage &mdash; what do you most wish "
        "the other person understood about what that moment feels like "
        "from the inside?",
        "One answer each. Said carefully. Heard without defending.",
    ),
    (
        "profile-aware",
        "{name_a}, when has {name_b}'s fluency felt like a gift rather "
        "than a problem? And {name_b}, when has {name_a}'s constancy "
        "felt like safety rather than pressure? "
        "Each of you name one specific moment.",
        "The answer is always somewhere in your history. Find it.",
    ),
    (
        "hard",
        "What is one thing you have been carrying lately that you "
        "have not yet brought to me, and what has kept you from bringing it?",
        "Not an accusation. An invitation. Hear the answer without defending.",
    ),
    (
        "profile-aware",
        "When my Attorney is beginning to build, or when my Exit "
        "is beginning to pull &mdash; what is one thing you wish "
        "I would say or do differently, not later, but in that moment?",
        "You both know what these patterns are now. Ask each other "
        "for what would actually help.",
    ),
]

ROUND_6 = [
    (
        "blessing",
        "Place your hand on your spouse's hand. Say their name. "
        "Then say: 'You are not a problem to be solved. "
        "You are a gift I get to receive again tomorrow.' "
        "Say it slowly. Let them say it back.",
        "You may feel silly. That is part of why it works. Do it anyway.",
    ),
    (
        "prayer",
        "Pray for each other &mdash; not silently, not generally, "
        "but out loud and by name. One sentence is enough. "
        "Pray for the thing they told you in Round Five.",
        "The closing of the date. Do not skip.",
    ),
]


def _render(text, name_a, name_b):
    return text.format(name_a=name_a, name_b=name_b)


def build(sub_a, sub_b) -> bytes:
    """Generate the Architect+Adapter couples walkthrough PDF.

    sub_a: the submission of the Architect spouse
    sub_b: the submission of the Adapter spouse
    """
    ensure_fonts()
    S = make_styles()

    name_a = _first_name(sub_a, "Architect")
    name_b = _first_name(sub_b, "Adapter")

    def R(text):
        return _render(text, name_a, name_b)

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Couples Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUPLES WALKTHROUGH",
        cover_right_label=f"{name_a.upper()}  +  {name_b.upper()}",
        title=f"Take 139 Couples Walkthrough \u2014 {name_a} & {name_b}",
    )

    story = []

    # ── COVER ──
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Couples<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph(
        "A counselor's read of the small repeating rocks<br/>in your particular marriage.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("PREPARED FOR", S["CoverProfileLabel"]))
    story.append(Paragraph(f"{name_a} &nbsp;&amp;&nbsp; {name_b}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_a.upper()}</b></font><br/>"
                "Architect &middot; Attorney<br/>"
                "<font size=9 color='#6b6862'>Disrespect &middot; Am I protected?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_b.upper()}</b></font><br/>"
                "Adapter &middot; Quiet Exit<br/>"
                "<font size=9 color='#6b6862'>Control &middot; Am I free?</font>",
                ParagraphStyle("c2", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
        ]],
        colWidths=[(PAGE_W - MARGIN_L - MARGIN_R) / 2.0] * 2,
        style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LINEBETWEEN", (0, 0), (-1, -1), 0.5, RULE),
        ]),
    )
    story.append(cover_tbl)
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cFor as in one body we have many members,<br/>"
        "and the members do not all have the same function,<br/>"
        "so we, though many, are one body in Christ.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "Romans 12:4\u20135",
        ParagraphStyle("cqa", fontName="Inter", fontSize=9, leading=14,
                       textColor=MUTED, alignment=TA_CENTER, spaceBefore=4)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1 ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "The small repeating rocks.",
                   "Why this pairing exists, and why you are both reading it.")
    for p in OPENING:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 2 ──
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TWO SHAPES",
                   "Side by side, on paper.",
                   "Two profiles next to each other for the first time.")
    for p in TWO_SHAPES_INTRO:
        story.append(Paragraph(R(p), S["BodyJ"]))
    side_by_side = Table(
        [[
            _profile_card(S, name_a, ACCENT,
                          "Disrespect / Injustice", "Am I protected?",
                          "The Architect", "The Attorney"),
            "",
            _profile_card(S, name_b, ACCENT_HER,
                          "Control / Shame", "Am I free?",
                          "The Adapter", "The Quiet Exit"),
        ]],
        colWidths=[
            (PAGE_W - MARGIN_L - MARGIN_R - 18) / 2.0, 18,
            (PAGE_W - MARGIN_L - MARGIN_R - 18) / 2.0,
        ],
        style=TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]),
    )
    story.append(side_by_side)
    story.append(Spacer(1, 16))
    for p in TWO_SHAPES_BODY:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 3 ──
    section_header(story, S, "SECTION THREE  \u00b7  HER GIFT TO HIM",
                   f"What {name_b} gives {name_a}.",
                   "A room that does not require him to be certain.")
    for p in GIFT_TO_A:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4 ──
    section_header(story, S, "SECTION FOUR  \u00b7  HIS GIFT TO HER",
                   f"What {name_a} gives {name_b}.",
                   "A fixed point. Something Adapters rarely build for themselves.")
    for p in GIFT_TO_B:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5 ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Fixed points meet fluid ones.",
                   "The small repeating rock, named.")
    for p in COLLISION[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The loop, in slow motion.",
                   "And the way through it, for each of you in your own grammar.")
    for p in COLLISION[5:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6 ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When the Attorney and the Exit are in the room at once.",
                   "What is happening, and what to do while you can still see it.")
    for p in BOTH_BREAK[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do, while you can still see it.",
                   "Three practices for the loop, in order.")
    for p in BOTH_BREAK[5:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 7 ──
    section_header(story, S, "SECTION SEVEN  \u00b7  COMMITMENTS",
                   "Six small daily practices.",
                   "Three from each of you. Read each one slowly.")
    for p in COMMITMENTS_INTRO:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"FROM {name_a.upper()}, TO {name_b.upper()}", S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name, body in A_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(name, S["H3"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_b}, to {name_a}.",
                   f"Three commitments, in her voice, for him to receive.")
    story.append(Paragraph(f"FROM {name_b.upper()}, TO {name_a.upper()}", S["CommitLabelHer"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT_HER,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name, body in B_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(name, S["H3Her"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())

    # ── SECTION 8 ──
    section_header(story, S, "SECTION EIGHT  \u00b7  A PRAYER",
                   "For the two of you.",
                   "Pray it together, if you can. Out loud, if you can.")
    for line in PRAYER:
        story.append(Paragraph(R(line), S["BlockQuote"]))
    story.append(PageBreak())

    # ── SECTION 9: DATE NIGHT ──
    section_header(story, S, "SECTION NINE  \u00b7  DATE NIGHT",
                   "Six rounds, taken slowly.",
                   "A conversation designed to be spoken between you, not read about.")
    for p in DATE_NIGHT_OPENING:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    rendered_round = lambda r: [(kind, R(q), note) for (kind, q, note) in r]

    _render_round(story, 1, rendered_round(ROUND_1),
                  "Warm up.",
                  "The lightness is the point. Start here even if you'd rather skip ahead.")
    story.append(PageBreak())
    _render_round(story, 2, rendered_round(ROUND_2),
                  "Notice the good.",
                  "Specific praise. The kind that lands because it could not have been said by anyone else.")
    story.append(PageBreak())
    _render_round(story, 3, rendered_round(ROUND_3),
                  "Wonder together.",
                  "About us, about God, about the life we are making.")
    story.append(PageBreak())
    _render_round(story, 4, rendered_round(ROUND_4),
                  "Sit in the strength.",
                  "Let yourselves feel the actual weight of what you've built.")
    story.append(PageBreak())
    _render_round(story, 5, rendered_round(ROUND_5),
                  "Tell the truth.",
                  "The harder ones. Asked gently. Heard without defending.")
    story.append(PageBreak())
    _render_round(story, 6, rendered_round(ROUND_6),
                  "Bless each other.",
                  "Close the date with a benediction spoken aloud. Do not skip.")
    story.append(Spacer(1, 18))
    closing_style = ParagraphStyle(
        "DnClose", fontName="Fraunces-Italic", fontSize=12, leading=20,
        textColor=INK, alignment=TA_CENTER, leftIndent=36, rightIndent=36,
        spaceBefore=10, spaceAfter=10)
    story.append(HRFlowable(width="40%", thickness=0.6, color=ACCENT,
                            hAlign="CENTER", spaceBefore=8, spaceAfter=14))
    story.append(Paragraph(
        "You are not a problem to be solved.<br/>"
        "You are a gift I get to receive again tomorrow.",
        closing_style))

    doc.build(story)
    return finalize_buffer(buf)


# ── STANDALONE TEST ──────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    class FakeSub:
        def __init__(self, name, mech, breakdown, trigger, question):
            self.name = name
            self.primary_mechanism = mech
            self.primary_breakdown = breakdown
            self.primary_trigger = trigger
            self.core_question = question

    sub_a = FakeSub("Christopher", "ARCH", "ATTY", "DIS", "PROT")
    sub_b = FakeSub("Elena", "ADPT", "VERD", "CTRL", "FREE")

    pdf_bytes = build(sub_a, sub_b)
    out_path = os.path.join(os.path.dirname(__file__), "architect_adapter_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    import io
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        snippet = ""
        for page in reader.pages:
            txt = page.extract_text() or ""
            if "GIFT" in txt or "gift" in txt.lower():
                snippet = txt.strip()[:200]
                break
    except Exception as e:
        page_count = "unknown"
        snippet = str(e)

    print(f"DONE: architect_adapter.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
