"""Couples Walkthrough — Adapter + Island.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where Spouse A is an Adapter and
Spouse B is an Island. First names are substituted from the submissions:
    {name_a}  -> the Adapter spouse's first name
    {name_b}  -> the Island spouse's first name

Adapter: trigger Control/Shame, core question "Am I free?" / "Am I acceptable?"
Island:  trigger Disconnection/Significance, core question "Am I enough to be remembered?"

Key pastoral dynamic: This pairing has an unusual surface stability because both
spouses appear undemanding. The Adapter accommodates the room; the Island asks for
little. Beneath the apparent peace, both are managing the cost of being themselves
alongside the other person in ways neither fully sees. The Adapter shifts to become
what the Island can accept; the Island withdraws to give the Adapter room to do that
work. Each is, in effect, paying the cost of the other's mechanism, and neither
realizes it.
"""
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    Paragraph, Spacer, KeepTogether, HRFlowable, Table, TableStyle,
    PageBreak, NextPageTemplate,
)

try:
    from ..base import (
        make_doc, make_styles, finalize_buffer, ensure_fonts,
        section_header,
        PAGE_W, MARGIN_L, MARGIN_R,
        PAPER, INK, ACCENT, ACCENT_HER, MUTED, RULE, HIGHLIGHT_BG,
    )
except ImportError:
    import sys as _sys
    import os as _os
    _sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
    from base import (
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


# ──────────── PROSE — uses {name_a} (Adapter) and {name_b} (Island) ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small "
    "repeating ones &mdash; the same quiet misunderstanding in slightly different "
    "clothes, three or four times a week, year after year, until both people have "
    "forgotten what they were originally hoping for.",

    "In your marriage, the small repeating rock has an unusual shape. From the "
    "outside, it does not look like conflict at all. People who know you would "
    "describe you as a low-drama couple. Neither of you raises your voice often. "
    "Neither of you creates scenes. But something is happening in the silences "
    "between you &mdash; a distance that is too comfortable, a peace that has been "
    "purchased at a cost neither of you has fully named. This document is going to "
    "name it.",

    "You are both reading this because you have decided to look. That decision is "
    "more significant than it seems. Many couples spend years inside the quiet "
    "distance without examining it, because the quiet is not painful enough to "
    "demand attention and not close enough to feel like home. Naming what is "
    "happening between you is more than half the work.",

    "Here is what I intend to do. I will name what each of you brings the other "
    "that you could not have built alone &mdash; the genuine theological gift your "
    "two shapes form when they are at their best. Then I will name the collision "
    "your two questions create, in the specific way it runs in your marriage. Then "
    "I will name the harder picture &mdash; when both of you are in breakdown at "
    "once &mdash; and what to do when you can still see it happening. Then I will "
    "hand each of you a set of commitments: not rules, but the small daily "
    "practices that, over months and years, change the temperature of a home.",

    "Read it together if you can. If not, read it separately and then sit down "
    "with it. Argue with what does not fit. Stay with what does. The goal is not "
    "insight for its own sake. The goal is a marriage in which neither of you has "
    "to manage the cost of the other's presence quietly and alone. That is worth "
    "looking at, even when the looking is uncomfortable.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, "
    "on paper, side by side. Most couples never see their two profiles next to each "
    "other. You are about to.",
]

TWO_SHAPES_BODY = [
    "{name_a}, you are an <b>Adapter</b> whose body reads control and shame as "
    "alarm signals, and whose deepest question is whether you are free &mdash; "
    "free to be yourself in this relationship, free from the pressure to become a "
    "particular version of yourself in every room you enter. You move through the "
    "world the way a river moves through a landscape: not by decision, but by the "
    "path of least resistance through a terrain that rewards certain movements and "
    "punishes others. You are genuinely present in every version of yourself. But "
    "when someone tries to fix you in place, or when the relationship quietly "
    "signals that one version is preferable to another, a <b>Plea</b> can follow "
    "&mdash; a rapid cycling through versions, trying to find the one that will "
    "close the gap.",

    "{name_b}, you are an <b>Island</b> whose body reads disconnection and "
    "insignificance as alarm signals, and whose deepest question is whether you "
    "are enough to be remembered &mdash; whether your passage through someone's "
    "life leaves a mark, whether you will be thought of in the night, whether your "
    "presence changes the shape of a room. You have learned to be self-contained "
    "because containment, for you, is dignity. When the containment is breached "
    "&mdash; when the wound is large enough to cross the perimeter the Island has "
    "built &mdash; a <b>Ghost</b> can follow: the performance of normalcy while "
    "something real and unspoken is happening inside.",

    "Notice what these two profiles do <i>not</i> share, and then notice what they "
    "share underneath. You are not asking the same question. {name_a} is asking "
    "<i>am I free?</i> &mdash; a question that wants room to move, the latitude "
    "to be many selves without being prosecuted for the inconsistency. {name_b} "
    "is asking <i>am I enough to be remembered?</i> &mdash; a question that wants "
    "weight, to matter, to be carried in someone's thoughts. Both are legitimate. "
    "Both are, in the architecture of a marriage, genuinely difficult to give each "
    "other.",

    "Beneath the two questions, however, there is the same root. You are both "
    "people who have learned to manage the risk of being fully seen. {name_a} "
    "manages it by becoming what the room can love, so that the self underneath "
    "the versions never has to be evaluated directly. {name_b} manages it by "
    "becoming self-sufficient, so that the longing to be remembered never has to "
    "be exposed as a longing. Both strategies have served each of you well in "
    "the world. Inside this marriage, they have created a strange and particular "
    "friction: a peace that costs more than either of you has admitted.",

    "Here is the friction, named plainly. The Adapter is always reading {name_b} "
    "and calibrating to what {name_b} can receive. The Island is always managing "
    "alone and giving {name_a} room to keep calibrating. Neither is demanding "
    "anything of the other. And yet both are quietly paying a cost: {name_a} "
    "does not know which version of herself {name_b} actually wants, because "
    "{name_b} has not said. {name_b} does not know if he is truly known in this "
    "marriage, because {name_a} has been presenting versions rather than the "
    "self underneath them. You are two people who have been very careful with "
    "each other, and the carefulness has quietly become its own kind of distance.",
]

GIFT_TO_A = [
    "{name_b} gives {name_a} something the Adapter almost never receives: "
    "<b>a room that does not demand a version.</b>",

    "The Adapter's world is organized around reading. Every room {name_a} enters "
    "has its own register, its own needs, its own implicit request for a particular "
    "version of her. At work, the room needs a particular self. With family, "
    "another. With friends, another still. The Adapter is extraordinarily good at "
    "this &mdash; she is, in almost every room, the person who makes others feel "
    "received. But the cost accumulates quietly. By the end of a week of careful "
    "calibration, {name_a} may not know which version is her own.",

    "{name_b}, by the nature of the Island, does not require the performance that "
    "other rooms require. The Island does not need to be entertained. He does not "
    "need the emotional temperature managed. He does not, in most seasons, need "
    "{name_a} to be anything other than simply present. The Island's "
    "self-containment, which to a different mechanism might feel like withholding, "
    "is to the Adapter one of the few rooms in a week where the reading can stop.",

    "There is a theological word for what {name_b} gives {name_a}. It is "
    "<i>sabbath</i> &mdash; not the formal Sabbath of Sunday observance, but the "
    "small, recurring sabbaths of a relationship in which one person does not "
    "require the other to be performing. Most of the rooms {name_a} walks through "
    "in a week require her gift and take it for granted. {name_b}'s presence "
    "does neither. He receives what is offered. He does not demand what has not "
    "been given. For a soul that has been reading rooms since childhood, "
    "that kind of presence is rarer and more restorative than {name_a} may "
    "have found words for.",

    "{name_a} &mdash; if you want to thank {name_b} for something this week, "
    "thank him for this: the particular quality of his presence that does not "
    "require you to be anyone in particular to earn it. He probably does not know "
    "he is giving it. Islands rarely know that their containment is a gift; "
    "they have been told often enough that it is a problem. Tell him that being "
    "near him without needing to calibrate is one of the kindest experiences "
    "in your week. He will not know what to do with the compliment. Say it anyway.",

    "{name_b} &mdash; what {name_a} receives from you, when you simply sit beside "
    "her without filling the air with expectation, is the closest thing she gets "
    "to rest most weeks. The thing in you that you have sometimes been told is "
    "too alone, too quiet, too interior &mdash; is for her a kind of mercy.",
]

GIFT_TO_B = [
    "{name_a} gives {name_b} something Islands rarely build for themselves: "
    "<b>a witness.</b>",

    "The Island's strategy is self-sufficiency &mdash; to need very little from "
    "the outside world, to process alone, to be the kind of person whose absence "
    "of need is mistaken for the absence of longing. But underneath the "
    "self-sufficiency, {name_b}'s deepest question is whether he is enough to "
    "be remembered &mdash; whether his presence leaves a mark. And this question "
    "cannot be answered by a soul that has made itself invisible to the people "
    "whose memory it most wants. The Island's strategy and the Island's longing "
    "are working against each other at the roots.",

    "{name_a}, by virtue of being an Adapter, is one of the most genuinely "
    "attentive people {name_b} has ever been close to. The Adapter reads people "
    "with a precision that most people cannot match. She notices. She registers "
    "what {name_b} does, how he moves through a room, what matters to him that "
    "he has not said aloud. The Island, who has spent years believing that "
    "the interior goes largely unnoticed, has in {name_a} a person who has "
    "been seeing it all along.",

    "The theological word for what {name_a} gives {name_b} is <i>witness</i> "
    "&mdash; the ancient covenant word for one who has been present, who has "
    "seen, who can testify that the thing happened. The Island's deepest fear "
    "is anonymity: going through life without having mattered. {name_a}, simply "
    "by being who she is, has been answering that fear week by week, in small "
    "and largely unspoken ways. She has carried him in her attention even when "
    "neither of them named it as such.",

    "{name_b} &mdash; if you want to thank {name_a} for something this week, "
    "thank her for noticing. Not for anything dramatic. For the specific, "
    "ordinary noticing she has done quietly over the course of your marriage: "
    "the things she saw in you that you did not think were visible, the moments "
    "she registered when you assumed no one had. The Adapter has been "
    "witnessing you. She does not always know that this is a gift. Tell her.",

    "{name_a} &mdash; what {name_b} receives from you, when you pay attention "
    "to the interior life he has largely kept private, is something he has been "
    "hoping for and half-convinced was not possible. Your attunement &mdash; "
    "the thing that other people have sometimes called inconsistency or people-"
    "pleasing &mdash; is, for him, evidence that he has been seen. That evidence "
    "is not small.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you, "
    "even if you have not named it quite this way.",

    "{name_a}'s core question is <i>am I free?</i> {name_b}'s is <i>am I enough "
    "to be remembered?</i> On the surface, these two questions are not in "
    "conflict. In the daily mechanics of a marriage &mdash; in the ordinary "
    "Tuesday evening, in the weekend conversation that starts easily and then "
    "goes quiet without either of you knowing why &mdash; they create a "
    "particular friction that is the harder to name because it is so quiet.",

    "Here is how the Adapter moves through this marriage. {name_a} reads {name_b} "
    "the way she reads every room: carefully, attentively, with a genuine desire "
    "to give him what she senses he needs. If he seems to want space, she gives "
    "it. If he seems to want a particular kind of conversation, she becomes "
    "available for it. If the evening feels like it wants quiet, she settles into "
    "quiet. This is not performance in the pejorative sense &mdash; {name_a} is "
    "genuinely present in each of these versions. But it means that {name_b} "
    "almost never encounters the un-adapted version of his wife &mdash; the "
    "version that has not first checked what the room needs. The Adapter, who "
    "cannot quite stop reading, keeps presenting the version most likely to be "
    "received rather than the self underneath the reading.",

    "Here is how the Island moves through this marriage. {name_b} processes "
    "alone, shares selectively, gives {name_a} room without being asked to. "
    "He does not demand that she be anyone in particular. He does not press for "
    "access to the interior he senses she is managing. He has learned, over "
    "years, that pressing makes the Adapter calibrate harder, and he has quietly "
    "decided that what she offers is worth receiving without requiring more. "
    "This is a genuine form of respect. It is also &mdash; and this is the part "
    "neither of you has named &mdash; a form of withdrawal. The Island's "
    "self-sufficiency means that {name_a} does not know what {name_b} actually "
    "needs from her. She keeps reading. He keeps retreating. Neither of them "
    "has said, directly, what they are actually looking for.",

    "Here is the collision, in slow motion. {name_a} presents a version of "
    "herself &mdash; the version she believes the evening calls for. {name_b} "
    "receives it, but something in him registers that it is a version, not the "
    "self underneath the version. He does not say so. The Island does not say "
    "so. Instead, he goes slightly more interior, slightly more self-contained, "
    "as though giving the Adapter more room to find the right key. {name_a} "
    "notices the slight withdrawal and reads it as a signal: <i>that was not "
    "quite the right version.</i> She tries another. {name_b} withdraws a "
    "little further, not to punish, but because the series of versions is "
    "beginning to feel like a performance he does not know how to respond to. "
    "{name_a} tries again. The loop is quiet, almost invisible, and by the "
    "end of the evening both of you have been in the same room for three hours "
    "without either of you having met the actual person you married.",

    "The Apostle Paul, writing to the church in Ephesus, said: <i>let each one "
    "of you speak the truth with his neighbor, for we are members one of "
    "another.</i> (Ephesians 4:25) The obligation is not merely to avoid "
    "lying. It is to offer truth in a single voice &mdash; a voice that is "
    "recognizably the same person across contexts, the person the other has "
    "covenanted to. The Adapter's gift is attunement, but the Adapter's cost "
    "is the withholding of the self that the other person actually needs in order "
    "to be in a real marriage rather than a very pleasant arrangement. {name_b} "
    "needs to know who he is married to. He cannot know that if {name_a} keeps "
    "presenting what she believes the room can receive.",

    "{name_a}, when {name_b} goes quiet, the translation is almost never "
    "<i>I want a different version of you.</i> It is more often: <i>I have "
    "received a version and I am not sure how to respond to it because I "
    "cannot tell if it is really you.</i> The right move, when you notice the "
    "withdrawal, is not to try another version. It is to set down the reading "
    "for a moment and offer something un-calibrated &mdash; a preference you "
    "actually hold, an opinion you have not checked against what the room seems "
    "to need, a sentence that begins with <i>I actually think.</i> {name_b} "
    "will not always know what to do with it. He will do more with it than "
    "he does with the version.",

    "{name_b}, when {name_a} cycles through registers looking for the one "
    "you will engage with, the translation is almost never <i>she is being "
    "inauthentic.</i> It is: <i>she is trying to reach me and does not know "
    "where I am, because I have not told her.</i> The right move is not "
    "to withdraw further to give her more room. It is to name, in one sentence, "
    "what you actually need from this conversation &mdash; not in general, "
    "not philosophically, but tonight: <i>I want to hear what you think about "
    "this, not what you think I want to hear.</i> The Adapter can work with "
    "that instruction. What the Adapter cannot work with is silence "
    "that she keeps reading as a request for a different version.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be moments &mdash; not every week, but "
    "they will come &mdash; when the quiet collision escalates. The Plea is up "
    "in {name_a}. The Ghost is up in {name_b}. The room is neither loud nor "
    "physically empty, but something in it has gone unreachable. Both of you are "
    "in breakdown at the same time, and neither of you, in that moment, has access "
    "to the more thoughtful person you were three hours ago.",

    "Here is what the room looks like from the outside, and then from the inside.",

    "From the outside: {name_a} is active. She is trying things &mdash; "
    "different tones, different topics, different emotional registers &mdash; "
    "moving quickly from one attempt to the next. {name_b} is still. He is "
    "present in the room but not quite in the conversation. He answers when "
    "spoken to. He has not left. But something essential about him has gone "
    "interior, behind the practiced normalcy of the Ghost, and {name_a} "
    "cannot find the opening. The room looks like one person trying and "
    "one person waiting. That is not quite what is happening.",

    "From the inside: {name_a}, when the Plea is running, is not trying "
    "different versions to be manipulative. She is frightened. The Adapter's "
    "deepest alarm is the sense that the room has closed to her, that no "
    "version she can produce will be received, that the relationship is at "
    "risk of something she cannot name. The Plea is the mechanism's emergency "
    "response &mdash; cycle faster, try more, find the version that opens the "
    "door. But each new version that lands in silence confirms the alarm: "
    "<i>the room is closed. There is no version that fits. I am not free "
    "here.</i> The Plea escalates because the silence reads as rejection.",

    "{name_b}, when the Ghost is up, is not withholding to punish. The Island, "
    "when a wound has crossed its perimeter, does not have immediate access "
    "to the wound in words. It goes interior &mdash; behind the composed "
    "surface, behind the &ldquo;I&rsquo;m fine,&rdquo; behind the ordinary "
    "motions of the evening &mdash; and begins the slow private work of "
    "processing what happened. The Ghost is not strategic silence. It is the "
    "Island's honest response to a wound it has not yet found the words for. "
    "But from inside the Plea, the Ghost does not read as <i>I need time.</i> "
    "It reads as <i>none of the versions are acceptable to him. He has "
    "gone somewhere I cannot reach.</i>",

    "The result is one of the most painful dynamics in any marriage: the person "
    "who most needs connection is cycling through versions at increasing speed, "
    "and the person who most needs to be remembered is going quiet behind the "
    "surface of normalcy. Both feel completely alone. Both believe they are "
    "doing the right thing. Neither is wrong about what they are experiencing. "
    "Both are wrong about what the other person is experiencing.",

    "Hear Genesis 2:18 in this moment: <i>It is not good that the man should "
    "be alone.</i> God said this of Adam before the Fall, in a world without "
    "sin, with God himself present. The not-good-aloneness is not a result of "
    "brokenness. It is written into the design. You were made to be known by "
    "another person in a way that God's presence alone, in this life, does not "
    "fully satisfy &mdash; and you were given each other precisely for that "
    "purpose. When the Plea and the Ghost are in the room together, both of "
    "you are experiencing the not-good-aloneness in the most acute form your "
    "particular wiring produces. The remedy is not a technique. It is the "
    "willingness of one of you to stop the loop.",

    "Peter writes that husbands are to <i>live with your wives in an "
    "understanding way... so that your prayers may not be hindered.</i> "
    "(1 Peter 3:7) The principle is striking: not understanding your spouse "
    "impedes your prayer life. God is attentive to how you treat the person "
    "he gave you. This is not a threat &mdash; it is a pastoral observation "
    "about the cost of remaining a stranger to the person you sleep beside.",

    "<b>One of you, not both, calls the pause.</b> Whoever notices first what "
    "is happening says, out loud: <i>this is the loop. Twenty minutes.</i> "
    "No final word. No last attempt at the right version. No performing "
    "normalcy. Just twenty minutes, agreed to, non-negotiable.",

    "<b>In the twenty minutes, do not strategize. Pray.</b> Not eloquently. "
    "{name_a}: <i>Lord, the Plea is up. I am cycling. Help me be still "
    "enough to be one person, and to trust that one person is enough for "
    "him.</i> {name_b}: <i>Lord, the Ghost is up. I am behind the surface. "
    "Help me find one word for the wound before it goes underground for "
    "another week.</i>",

    "<b>When you come back, each of you says one sentence.</b> {name_a}, "
    "your sentence is not the next version. It is one true thing from the "
    "self below the reading: what you actually felt, beginning with "
    "<i>I.</i> {name_b}, your sentence is not the performed normalcy. "
    "It is one honest thing from behind the surface: the wound in its "
    "plainest form. <i>I felt like I was disappearing when the conversation "
    "kept shifting.</i> That is one sentence. <i>I felt invisible when I "
    "could not tell which of you was actually here.</i> That is one sentence. "
    "Both of you can manage one sentence. Then stop.",

    "<b>Neither of you is the problem.</b> The Plea and the Ghost are old "
    "mechanisms doing the only job they were ever taught to do. The truest "
    "thing about both of you is not the breakdown pattern. It is that you are "
    "two people who chose each other, before God, and who are committed to "
    "the slow work of learning to be known by each other. That commitment "
    "&mdash; renewed on the quiet Tuesdays when it is least dramatic and least "
    "convenient &mdash; is what covenant actually looks like from the inside.",
]

COMMITMENTS_INTRO = [
    "What follows are six commitments &mdash; three from {name_a}, three from "
    "{name_b}. They are not vows in the legal sense. They are the small daily "
    "practices that, offered to each other freely and kept with reasonable "
    "faithfulness, change the temperature of a home over months and years. "
    "Read each one slowly. If one of you cannot make a particular commitment "
    "in good faith yet, do not make it. The goal is not performance. "
    "It is honesty.",
]

A_COMMITMENTS = [
    (
        "I will offer you the same self today, even when the room calls for someone else.",
        "{name_b}, I commit to offering you the un-adapted version of myself at "
        "least once each day &mdash; a preference I actually hold, an opinion I "
        "have not checked against what the evening seems to need, a sentence that "
        "begins with <i>I actually want</i> and means it. I will not always find "
        "this easy. The Adapter has been reading rooms for a long time. But you "
        "deserve to know who you married, and I deserve to be known by you as "
        "that person, not only as the version most likely to be received.",
    ),
    (
        "I will name what I actually feel before the Plea begins.",
        "{name_b}, when I feel the loop starting &mdash; when I sense you "
        "withdrawing and the mechanism wants to cycle through versions to find "
        "the one that opens the door &mdash; I commit to stopping and naming "
        "one true thing instead. Not a version. Not an attempt. One honest "
        "sentence in my own voice: <i>I feel like I am losing you right now, "
        "and I do not know what I did.</i> I will trust that one true sentence, "
        "spoken plainly, does more work than ten calibrated versions. Even when "
        "the trust does not come easily.",
    ),
    (
        "I will stay in the room as myself when the room goes quiet.",
        "{name_b}, when you go interior &mdash; when the Ghost is up and the "
        "surface is composed and I cannot find the opening &mdash; I commit to "
        "staying present as myself rather than searching for the key. I will "
        "say, once, in a plain voice: <i>I am here. I am not going anywhere. "
        "You do not have to talk right now, but I want you to know I am still "
        "here as me, not as a version of me.</i> And then I will be still. "
        "You can come back when you are ready. I will be the same person "
        "when you do.",
    ),
]

B_COMMITMENTS = [
    (
        "I will engage with one version of you, today, instead of waiting for the one that feels safest.",
        "{name_a}, I commit to receiving what you offer rather than withholding "
        "until the version arrives that feels most like the right fit. I will "
        "name, when I notice it, the version I am actually being given: "
        "<i>I hear you trying to reach me. Here I am.</i> The Island has been "
        "waiting for the person who feels safe to receive. You have been "
        "adapting for years. I will do the work of meeting you where you are "
        "rather than requiring you to find the version of yourself I most "
        "easily recognize.",
    ),
    (
        "I will name the wound before it goes underground.",
        "{name_a}, I commit to telling you when something has landed hard on "
        "me &mdash; not after the Ghost has been running for a week, not in a "
        "closing argument after the case has been built in private, but as "
        "close to the moment as I can manage. One sentence. In my own voice. "
        "Before the surface closes over it. <i>That landed hard on me.</i> "
        "That is enough. You can work with that. You cannot work with the "
        "composed surface and the performed normalcy, and I am learning that "
        "the composed surface has cost both of us more than I knew.",
    ),
    (
        "I will tell you, in plain words, that you are enough.",
        "{name_a}, the Adapter's deepest question is whether she is free "
        "&mdash; whether there is a version of herself that is simply "
        "acceptable, without adjustment. I commit to telling you, regularly "
        "and specifically, that the un-adapted version of you &mdash; the "
        "one with opinions and preferences and the particular quirks you "
        "have learned to manage &mdash; is not merely tolerable. It is the "
        "one I chose. You do not have to read this room. You are already "
        "what this room needs.",
    ),
]

PRAYER = [
    "Father,",

    "You set these two next to each other, and you knew exactly what you "
    "were doing. You knew the Adapter would need a room that did not demand "
    "a performance. You knew the Island would need a witness who could see "
    "the interior he keeps private. You knew the evenings when the Plea "
    "would cycle and the Ghost would go quiet and neither of them would "
    "quite find each other. You knew all of it before either of them said yes.",

    "Teach them the grammar of each other. Teach {name_a} to offer the "
    "self below the reading &mdash; the un-calibrated, un-adapted, "
    "genuinely present version that {name_b} has been hoping to encounter "
    "in the same room as himself. Teach {name_b} to receive what {name_a} "
    "offers before checking whether it is the version he was waiting for, "
    "and to name the wound before it goes underground, so that {name_a} "
    "can stop reading the silence for signals it was never meant to contain.",

    "When the Plea rises in {name_a} &mdash; when the cycling starts and "
    "the versions multiply and the alarm says the room has closed &mdash; "
    "would you remind her that she is named, not by the room's reflection, "
    "not by the version most recently approved, but by a Father who chose "
    "her in Christ before the foundation of the world, before any room "
    "existed to require a version? When the Ghost rises in {name_b} &mdash; "
    "when the surface is composed and the wound has gone interior and the "
    "tally runs quietly behind the performance of normalcy &mdash; would you "
    "remind him that he is engraved on the palms of your hands, that you "
    "have not forgotten a single entry in the tally, and that the verdict "
    "over him is not <i>forgotten</i> but <i>known, kept, beloved</i>?",

    "Make their home a room in which {name_a} can be one person without "
    "the room going silent, and {name_b} can bring the wound to the surface "
    "without waiting until it has become a case. Make their table a place "
    "where un-adapted words are offered and received without calibration. "
    "Make their covenant the frame on which both of them can grow: the "
    "witness that the Island needs to believe he has been seen, and the "
    "room that the Adapter needs to believe she is free.",

    "And Father, when they are old and the quiet distance has become a "
    "quiet closeness, let them look back and see that the two shapes "
    "&mdash; so apparently undemanding of each other, so carefully "
    "managed around each other &mdash; made something together that "
    "neither of them could have made alone. Let them recognize in that "
    "looking back the signature of a Maker who knew what he was doing.",

    "In the name of the One who is the same yesterday, today, and forever "
    "&mdash; who never adjusts his self to the room, and who never forgets "
    "a single person in his care.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. "
    "The pages that follow are different. They are meant to be spoken "
    "<i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken "
    "slowly, somewhere quiet, with no children in the room and no "
    "phones on the table. There are six rounds, and they build on each "
    "other. Resist the temptation to skip ahead. Start at Round One even "
    "if it feels too light; the lightness is the point.",

    "Some of the questions are playful. Some are direct. A few are the "
    "kind that, when answered honestly, will sit with you for a week. "
    "None of them are trivia. All of them are an invitation.",

    "<b>How to use it.</b> One of you reads a question aloud. The one "
    "who did not read answers first, in full, without interruption. Then "
    "the reader answers the same question. Then you move on. You do not "
    "have to finish all six rounds in one night &mdash; two or three "
    "rounds, taken seriously, is often better than racing through all of "
    "them. Save the rest for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. You may "
    "not love everything you hear. Stay with it. The point is not to "
    "grade each other's answers. The point is to be known, and to do "
    "the slow work of knowing.",
]

ROUND_1 = [
    (
        "hypothetical",
        "If our marriage were a landscape &mdash; any landscape, anywhere "
        "in the world &mdash; what would it look like, and what would be "
        "your favorite place to sit inside it?",
        "Let the image say what plain language cannot. Answer with the "
        "first landscape that comes to mind. Don't overthink.",
    ),
    (
        "observation",
        "What is something I did for you this week that you noticed "
        "and did not mention?",
        "Not a complaint. A small noticing. The fact that you noticed "
        "at all is already something.",
    ),
    (
        "playful",
        "If you had to describe this marriage as a piece of music "
        "&mdash; any genre, any tempo &mdash; what would it sound like "
        "right now, and what would you want the next movement to be?",
        "Yes, really. Answer with the first thing that comes. There is "
        "no wrong answer.",
    ),
]

ROUND_2 = [
    (
        "fill-in-blank",
        "I don't think I tell you this enough &mdash; I am amazed at "
        "the way God made you so _______. Your _______ is a gift to "
        "our marriage, and I want to get better at receiving it.",
        "Two blanks. Be specific. 'Patient' is too easy; 'patient with "
        "my silences in a way that no one else in my life has ever been' "
        "is closer.",
    ),
    (
        "observation",
        "What is one thing you have watched me do this year that "
        "you wish more people could see?",
        "Most of us only ever see ourselves do our most public things. "
        "Tell your spouse about a private one.",
    ),
    (
        "one-word",
        "If you had to choose one word to describe what it feels like "
        "when the Adapter and the Island are actually meeting each other "
        "&mdash; when we are genuinely in the same place at the same "
        "time &mdash; what word would it be?",
        "One word, said out loud. Then explain it briefly.",
    ),
]

ROUND_3 = [
    (
        "forward-looking",
        "Five years from now, when we look back on this season of our "
        "marriage, what do you hope we will say we did well together?",
        "Not what you wish you had done. What you want, when you look "
        "back, to be able to say you actually did.",
    ),
    (
        "theological",
        "Where, in the last month, have you seen God specifically at "
        "work in me &mdash; not the version I present, but the real "
        "one underneath?",
        "Not where you want him to work. Where you have already seen it. "
        "Name it specifically.",
    ),
    (
        "shared-identity",
        "Finish this sentence three times: 'We are the kind of couple "
        "who _______.' Give one playful answer, one true answer, "
        "and one aspirational answer.",
        "The 'we' is the point. Let all three be real.",
    ),
]

ROUND_4 = [
    (
        "strength",
        "What is something I do for our shared life that you would "
        "have to learn to do for yourself if I were not here?",
        "Hard to ask. Important to hear the answer. Stay with it.",
    ),
    (
        "fill-in-blank",
        "One of the gifts of being married to you is that I get to "
        "be _______ in ways I never would have been on my own.",
        "A version of yourself that only exists because this marriage "
        "exists. Name it as specifically as you can.",
    ),
    (
        "observation",
        "Name one moment in our story where you knew, without doubt, "
        "that the Adapter and the Island had built something together "
        "that neither of us could have built alone.",
        "Tell the story in full. The remembering is part of "
        "the strengthening.",
    ),
]

ROUND_5 = [
    (
        "hard",
        "When our patterns collide &mdash; when the Plea is cycling "
        "and the Ghost is up &mdash; what do you most wish the other "
        "person understood about what that moment feels like from "
        "the inside?",
        "One answer each. Said carefully. Heard without defending.",
    ),
    (
        "profile-aware",
        "{name_a}, when has {name_b}'s self-containment felt like "
        "a gift rather than a distance? And {name_b}, when has "
        "{name_a}'s attentiveness felt like being seen rather than "
        "being read? Each of you name one specific moment.",
        "The answer is somewhere in your history. Find it.",
    ),
    (
        "hard",
        "What is one thing you have been carrying lately that you "
        "have not yet brought to me, and what has kept you from "
        "bringing it?",
        "Not an accusation. An invitation. Hear the answer "
        "without defending.",
    ),
    (
        "profile-aware",
        "When the Plea begins in me, or when the Ghost is up in me "
        "&mdash; what is one thing you wish I would say or do "
        "differently, not later, but in that moment?",
        "You both know what these patterns are now. Ask each other "
        "for what would actually help.",
    ),
]

ROUND_6 = [
    (
        "blessing",
        "Place your hand on your spouse's hand. Say their name. "
        "Then say: 'You are not a problem to be solved. You are a "
        "gift I get to receive again tomorrow.' Say it slowly. "
        "Let them say it back.",
        "You may feel silly. That is part of why it works. Do it anyway.",
    ),
    (
        "prayer",
        "Pray for each other &mdash; not silently, not generally, "
        "but out loud and by name. One sentence is enough. Pray for "
        "the thing they told you in Round Five.",
        "The closing of the date. Do not skip.",
    ),
]


def _render(text, name_a, name_b):
    return text.format(name_a=name_a, name_b=name_b)


def build(sub_a, sub_b) -> bytes:
    """Generate the Adapter+Island couples walkthrough PDF.

    sub_a: the submission of the Adapter spouse
    sub_b: the submission of the Island spouse
    """
    ensure_fonts()
    S = make_styles()

    name_a = _first_name(sub_a, "Adapter")
    name_b = _first_name(sub_b, "Island")

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
                f"<font color='#4f6b5e'><b>{name_a.upper()}</b></font><br/>"
                "Adapter &middot; Plea<br/>"
                "<font size=9 color='#6b6862'>Control &middot; Am I free?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_b.upper()}</b></font><br/>"
                "Island &middot; Ghost<br/>"
                "<font size=9 color='#6b6862'>Disconnection &middot; Am I enough to be remembered?</font>",
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
        "<i>\u201cIt is not good that the man should be alone.<br/>"
        "I will make him a helper fit for him.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "Genesis 2:18",
        ParagraphStyle("cqa", fontName="Inter", fontSize=9, leading=14,
                       textColor=MUTED, alignment=TA_CENTER, spaceBefore=4)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1 ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "The quiet that costs too much.",
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
            _profile_card(S, name_a, ACCENT_HER,
                          "Control / Shame", "Am I free?",
                          "The Adapter", "The Plea"),
            "",
            _profile_card(S, name_b, ACCENT,
                          "Disconnection / Significance", "Am I enough to be remembered?",
                          "The Island", "The Ghost"),
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
    section_header(story, S, "SECTION THREE  \u00b7  HIS GIFT TO HER",
                   f"What {name_b} gives {name_a}.",
                   "A room that does not demand a version.")
    for p in GIFT_TO_A:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4 ──
    section_header(story, S, "SECTION FOUR  \u00b7  HER GIFT TO HIM",
                   f"What {name_a} gives {name_b}.",
                   "A witness. Something Islands rarely build for themselves.")
    for p in GIFT_TO_B:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5 ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "The room inside the room.",
                   "The small repeating rock, named.")
    for p in COLLISION[:4]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The loop, in slow motion.",
                   "And the way through it, for each of you in your own grammar.")
    for p in COLLISION[4:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6 ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When the Plea and the Ghost are in the room at once.",
                   "What is happening, named plainly so both of you can see it.")
    for p in BOTH_BREAK[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do, while you can still see it.",
                   "Four practices for the loop, in order.")
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
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT_HER,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for cname, cbody in A_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(cname, S["H3Her"]),
            Paragraph(R(cbody), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_b}, to {name_a}.",
                   f"Three commitments, in his voice, for her to receive.")
    story.append(Paragraph(f"FROM {name_b.upper()}, TO {name_a.upper()}", S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for cname, cbody in B_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(cname, S["H3"]),
            Paragraph(R(cbody), S["CommitBody"]),
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


# ── STANDALONE TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    class FakeSub:
        def __init__(self, name, mech, breakdown, trigger, question):
            self.name = name
            self.primary_mechanism = mech
            self.primary_breakdown = breakdown
            self.primary_trigger = trigger
            self.core_question = question

    sub_a = FakeSub("Elena", "ADPT", "PLEA", "CTRL", "FREE")
    sub_b = FakeSub("Marcus", "ISLE", "GHOST", "DISC", "REM")

    pdf_bytes = build(sub_a, sub_b)
    out_path = os.path.join(os.path.dirname(__file__), "adapter_island_test.pdf")
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
            if "GIFT" in txt or "gift" in txt.lower() or "HIS GIFT" in txt:
                snippet = txt.strip()[:200]
                break
    except Exception as e:
        page_count = "unknown"
        snippet = str(e)

    print(f"DONE: adapter_island.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
