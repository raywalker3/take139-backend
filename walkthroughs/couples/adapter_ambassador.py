"""Couples Walkthrough — Adapter + Ambassador.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where Spouse A is an Adapter and
Spouse B is an Ambassador. First names are substituted from the submissions:
    {name_a}  -> the Adapter spouse's first name
    {name_b}  -> the Ambassador spouse's first name

Adapter:     trigger Control/Shame, core question "Am I free?" / "Am I acceptable?"
Ambassador:  trigger Disconnection, core question "Am I lovable?"

Key pastoral dynamic: This pairing is unusually warm AND unusually subtle.
Both spouses are gift-givers — the Adapter calibrates to the other person;
the Ambassador serves the other person. From outside this looks like a uniquely
attentive marriage. But underneath, the two mechanisms tangle: the Ambassador
gives because they need to know they are loved; the Adapter receives in whatever
form the room offers because they have no stable preference of their own.
The result is a marriage of mutual attunement where neither spouse is sure
who they actually are with the other.
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


# ──────────── PROSE — uses {name_a} (Adapter) and {name_b} (Ambassador) ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small "
    "repeating ones &mdash; the same quiet misunderstanding in slightly different "
    "clothes, week after week, until both people have forgotten what they were "
    "originally hoping for. What makes your particular marriage unusual is that "
    "the small repeating rock is nearly invisible from the outside. You are a warm "
    "couple. You are an attentive couple. The people who know you have probably "
    "said so. And they are not wrong. But warmth and attentiveness, it turns out, "
    "can be the wrapping on two very different kinds of need &mdash; and when those "
    "needs begin to pull against each other beneath the surface of an otherwise "
    "kind marriage, neither of you can quite explain what is going wrong.",

    "Here is what is going wrong, named plainly so you can both see it. "
    "{name_a}, you are extraordinarily good at reading the room and becoming "
    "what the room most needs. {name_b}, you are extraordinarily good at giving "
    "to the people you love and managing the emotional temperature of the "
    "relationships you care about. From the outside, these two gifts look "
    "perfectly matched. From the inside, they have been quietly tangling "
    "for years &mdash; because the Adapter's calibration and the Ambassador's "
    "service are not, at their roots, the same thing, and they are not "
    "meeting each other's deepest need.",

    "You are both reading this because you have decided to look at the tangle. "
    "That decision is more significant than it appears. Most couples in warm "
    "marriages spend years being kind to each other in ways that do not quite "
    "land, because neither of them has been able to name precisely what is "
    "missing. This document is going to name it.",

    "Here is what I intend to do. I will name what each of you brings the other "
    "that you could not have built alone &mdash; the genuine gift your two shapes "
    "form when they are at their best. Then I will name the collision your two "
    "questions create, in the specific way it shows up in your marriage. Then I "
    "will name the harder picture &mdash; when both of you are in breakdown at "
    "once &mdash; and what to do while you can still see it. Then I will hand "
    "each of you a set of commitments, not as rules but as the small daily "
    "practices that, over years, change the temperature of a home.",

    "Read this together if you can. If not, read it separately and sit down "
    "with it. Argue with what does not fit. Stay with what does. The goal is "
    "not a warmer marriage &mdash; you already have that. The goal is a more "
    "honest one. Honesty, in the long run, produces a warmth that does not "
    "require either of you to perform.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually "
    "is, on paper, side by side. Most couples never see their two profiles next "
    "to each other. You are about to.",
]

TWO_SHAPES_BODY = [
    "{name_a}, you are an <b>Adapter</b> whose body reads control and shame as "
    "alarm signals, and whose deepest question is whether you are free &mdash; "
    "free to be yourself, free from the pressure to be a particular version of "
    "yourself in this relationship. You move through the world the way a river "
    "moves through a landscape: not by decision, but by finding the path of "
    "least resistance through whatever the terrain requires. You can be utterly "
    "authentic in five different registers with five different people in a single "
    "day and feel no contradiction, because for you, authenticity has never been "
    "a fixed self presenting itself consistently. It has been the full "
    "entering-in to whatever the relationship most needs. When the pressure to "
    "be a fixed, named version of yourself becomes intolerable, a "
    "<b>Plea</b> or a <b>Quiet Exit</b> follows &mdash; depending on "
    "whether the threat feels like abandonment or like a cage.",

    "{name_b}, you are an <b>Ambassador</b> whose body reads disconnection as "
    "an alarm signal, and whose deepest question is whether you are lovable. "
    "You are the one who notices when the emotional temperature drops and goes "
    "to work raising it. You are the one who remembered the small thing "
    "{name_a} mentioned last month, who tracks how the people you love are "
    "doing, who gives consistently and generously because giving is how you "
    "know you are needed &mdash; and being needed has, for a long time, felt "
    "very close to being loved. When the giving does not produce the warmth "
    "you were hoping for, a <b>Plea</b> follows &mdash; giving harder, "
    "more urgently, more apologetically, trying to close a gap that the "
    "giving itself cannot close.",

    "Notice carefully what these two profiles share and what they do not. "
    "Both of you are oriented toward the other person. Both of you are, "
    "in some genuine sense, gift-givers. But the gifts are not the same, "
    "and the needs beneath them are not the same. {name_a} calibrates "
    "<i>to</i> you &mdash; reading what you need and becoming it. "
    "{name_b} serves <i>for</i> you &mdash; giving what you need in order "
    "to be received in return. The Adapter has a fluid self that takes the "
    "shape of each relationship. The Ambassador has a constant self that "
    "gives differently across relationships. This distinction is not subtle "
    "&mdash; it goes to the root of how each of you understands love and "
    "how each of you keeps yourself safe.",

    "The questions beneath the two mechanisms are also different, and this "
    "matters. {name_a} is asking <i>am I free?</i> &mdash; free to be "
    "un-pressed, un-fixed, un-named in a way that feels like a cage. "
    "{name_b} is asking <i>am I lovable?</i> &mdash; loved for who I am, "
    "not merely for what I give. In theory these two questions have nothing "
    "to do with each other. In the mechanics of a marriage between an Adapter "
    "and an Ambassador, they become entangled in a way that is genuinely "
    "difficult to unravel without help.",

    "From outside, your pairing looks like one of the most naturally harmonious "
    "in the taxonomy. Both of you attend to the other person. Both of you are "
    "skilled at warmth. Conflict in your home rarely looks like conflict "
    "&mdash; it looks like two very considerate people quietly not quite "
    "meeting each other. That is the small repeating rock in your marriage. "
    "It is worth naming.",
]

GIFT_TO_A = [
    "{name_b} gives {name_a} something the Adapter almost never receives from "
    "anyone: <b>love that comes toward you, unsolicited, without waiting for "
    "you to become something first.</b>",

    "The Adapter's world runs on a particular logic: the way to be loved is "
    "to read what the room needs and become it. Connection is something the "
    "Adapter earns by attuning, by adjusting, by giving the other person the "
    "version of you they most need to receive. This logic has served {name_a} "
    "well in many rooms. But it has a cost that accumulates slowly and is "
    "rarely named: when love is always something you calibrate toward, "
    "you never quite know whether you are being loved or whether your "
    "calibration is working. The two can feel identical from the inside.",

    "{name_b}, by the nature of the Ambassador mechanism, does not wait for "
    "{name_a} to produce the right version before giving. The Ambassador "
    "gives first. The warmth comes before it is asked for. The attention "
    "arrives before it is earned. For a person who has spent years producing "
    "the version most likely to be received, being with someone who gives "
    "regardless of the version &mdash; who notices and shows up and brings "
    "warmth without first requiring a particular self to be present &mdash; "
    "is genuinely disorienting in the best possible way.",

    "The theological word for what {name_b} gives {name_a} is "
    "<i>grace</i> &mdash; not the formal doctrinal category, but the older "
    "meaning: unearned favor, love given before it is merited. The Adapter "
    "has been working, in some sense, to earn every room he has ever walked "
    "into. {name_b} is one of the rooms where the earning is not required. "
    "The Ambassador loves without waiting for the calibration to produce the "
    "right output. This is, for {name_a}, a picture of something the gospel "
    "announces: that the Father loved the Son, and loved us in the Son, before "
    "we had produced anything at all. The Ambassador's giving, at its best, "
    "enacts this picture in the ordinary rhythm of a Tuesday evening.",

    "{name_a} &mdash; if you want to thank {name_b} for something this week, "
    "thank her for the times she showed up for you before you had figured out "
    "what version of yourself to bring. She probably does not know this is "
    "what she is giving you. Ambassadors give naturally, without always "
    "knowing the specific weight of what they offer. Tell her. She will not "
    "know what to do with the gratitude. Say it anyway.",

    "{name_b} &mdash; what {name_a} receives from you, in those moments of "
    "unsolicited warmth and quiet attentiveness, is something closer to rest "
    "than he usually gets. The giving in you that has sometimes been called "
    "too much, or exhausting, or difficult to receive &mdash; it is, for "
    "him, a form of grace he did not know he needed until you gave it.",
]

GIFT_TO_B = [
    "{name_a} gives {name_b} something Ambassadors rarely receive: "
    "<b>a mirror that moves.</b>",

    "The Ambassador's deepest fear is that the giving will stop mattering "
    "&mdash; that love given consistently enough will still not be "
    "sufficient to produce the warmth the Ambassador is looking for. This "
    "fear produces a pattern: give more, give better, give in the specific "
    "way that will finally be received. But the Ambassador can only give "
    "what the Ambassador knows how to give. And the Ambassador's giving, "
    "however warm and real, tends to come in recognizable shapes: the same "
    "acts of service, the same check-ins, the same temperature-management "
    "that has always been the Ambassador's language.",

    "{name_a}, by the nature of the Adapter mechanism, does not receive "
    "in a fixed register. The Adapter receives in whatever form the room "
    "offers, and mirrors the room back to you in a way that confirms the "
    "giving landed. When {name_b} brings care, {name_a} receives it in "
    "the key in which it was offered &mdash; not performing reception, "
    "but genuinely entering into the register of the moment. For an "
    "Ambassador whose deepest fear is that the giving goes unnoticed, "
    "being with someone who genuinely receives &mdash; who adjusts to "
    "the shape of what you are offering rather than requiring you to "
    "change the shape &mdash; is a form of confirmation that most "
    "Ambassadors have never experienced so consistently.",

    "There is a theological word for what {name_a} gives {name_b} too. "
    "It is <i>witness</i> &mdash; in the older sense of someone who sees "
    "and can testify to what they have seen. The Ambassador has been "
    "giving for years, often into rooms that received without noticing. "
    "{name_a}, by virtue of the Adapter's attunement, notices. The giving "
    "lands. It is witnessed. And for the Ambassador whose core question "
    "is <i>am I lovable?</i>, being received by someone who is genuinely "
    "present to what you are offering is, in its own way, an answer to "
    "the question.",

    "{name_b} &mdash; if you want to thank {name_a} for something this "
    "week, thank him for the times he received what you gave without "
    "making you feel that the giving was too much. He may not have been "
    "conscious of what he was giving you by receiving well. Adapters "
    "rarely know that their capacity to enter the room you are in is a "
    "gift; they have been told often enough that their fluency is simply "
    "inconsistency. Tell her that her attentiveness to what you are "
    "offering is one of the kindest things in your week.",

    "{name_a} &mdash; what {name_b} receives from you, in the moments "
    "when you genuinely take in what she gives rather than deflecting or "
    "redirecting the warmth back to her, is the experience of a giving "
    "that mattered. The thing in you that has sometimes seemed like an "
    "absence of stable preference is, for her, a presence that receives "
    "fully. She has needed that for a long time.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of "
    "you, even if you have not been able to name it quite this way.",

    "The collision in this marriage does not look like conflict. It looks like "
    "warmth that has begun, very slowly, to feel thin. {name_b} gives. "
    "{name_a} receives. The reception is real &mdash; the Adapter genuinely "
    "enters the room the Ambassador has created. But {name_b} cannot quite "
    "tell whether what is being received is the gift itself or a calibrated "
    "response to what the gift seemed to need. And {name_a} cannot quite "
    "tell whether what {name_b} is giving is love freely offered or love "
    "offered in expectation of a particular return. The warmth is real "
    "on both sides. The uncertainty is also real on both sides.",

    "Here is what is happening, named in slow motion. {name_b}'s core "
    "question is <i>am I lovable?</i> The Ambassador tries to answer this "
    "question by giving &mdash; by being so consistently warm, so "
    "attentive, so useful, that the love that comes back will eventually "
    "feel certain and permanent. The Ambassador needs the giving to land. "
    "She needs to see, in {name_a}'s response, that it has landed. "
    "She is watching for confirmation.",

    "{name_a}'s core question is <i>am I free?</i> or, in the version "
    "that runs most often in this pairing, <i>am I acceptable as I am?</i> "
    "The Adapter tries to answer this question by calibrating &mdash; by "
    "reading what the room most needs and becoming it, so that the love "
    "that comes back will feel earned and safe. When {name_b} gives, "
    "{name_a} reads what the giving seems to need in return and provides "
    "it. The reception is genuine. But it is also, in part, produced "
    "by the room rather than given freely from a stable interior.",

    "Here is the slow motion collision. {name_b} gives something &mdash; "
    "an act of service, a word of care, a piece of attention that cost "
    "real effort. {name_a} receives it and responds in the register "
    "the giving seemed to need: warm, engaged, grateful. {name_b} "
    "notices the warmth and begins to feel that the giving has landed. "
    "But then, in a later moment, {name_b} realizes that {name_a}'s "
    "response was so perfectly calibrated to what the giving seemed to "
    "need that she cannot be entirely sure whether she received love "
    "or produced it. The question wakes up again: <i>am I lovable, "
    "or did I simply calibrate the right response out of him?</i> "
    "She gives again, slightly differently, watching for a response "
    "that feels less calibrated. And {name_a}, reading the slight "
    "difference in the giving, adjusts the response accordingly.",

    "Neither of you is trying to deceive the other. {name_b} is "
    "genuinely giving. {name_a} is genuinely receiving. But the "
    "Ambassador's giving has begun to be shaped by the question "
    "<i>will this produce the confirmation I need?</i> and the "
    "Adapter's receiving has begun to be shaped by the question "
    "<i>what does this giving need from me?</i> The result is "
    "a marriage in which the warmth is real but the grounding "
    "underneath it has shifted. Both spouses are attending "
    "to each other with great care. Neither is sure who they "
    "are actually meeting.",

    "The pastoral insight that Scripture offers to this specific "
    "collision is Ephesians 4:25: <i>Therefore, having put away "
    "falsehood, let each one of you speak the truth with his "
    "neighbor, for we are members one of another.</i> Paul is "
    "speaking of the body of Christ, but the principle reaches "
    "into the one-flesh union of marriage with particular force. "
    "Speaking truth with one another &mdash; not performing "
    "warmth, not calibrating response, not giving in order to "
    "produce a particular outcome &mdash; is the act that makes "
    "a marriage a covenant rather than a negotiation. For both "
    "of you, in your own way, this is the hardest practice. "
    "The Adapter must speak truth in a single voice, even when "
    "the room is calling for a different version. The Ambassador "
    "must name what she actually wants, rather than giving in "
    "hopes that the wanting will be intuited and returned.",

    "{name_a} &mdash; here is what {name_b} actually needs from you. "
    "Not the version of you most likely to confirm that her giving "
    "landed. Not the reception that mirrors back what the giving "
    "seemed to require. She needs the response that would have come "
    "even if the giving had been different &mdash; the self that "
    "exists independently of what she just offered you. This is "
    "the hardest thing the Adapter is ever asked to do: to be "
    "present as a fixed self rather than a calibrated response. "
    "But it is the only thing that answers {name_b}'s actual "
    "question. You cannot love her into certainty by receiving "
    "her gifts well. You can only love her into certainty by "
    "being consistently, recognizably yourself.",

    "{name_b} &mdash; here is what {name_a} actually needs from you. "
    "Not the giving shaped by what you hope to receive. Not the "
    "warmth offered in expectation of confirmation. He needs to "
    "know that the giving is free &mdash; that if he failed to "
    "receive it perfectly, the warmth would still be there. The "
    "Ambassador's giving, when it is shaped by the question "
    "<i>will this be enough?</i>, has a weight to it that the "
    "Adapter feels before the words arrive. And the Adapter, "
    "feeling the weight, calibrates to it. You cannot receive "
    "a freer response from him by giving more carefully. You "
    "can only receive it by naming what you actually want, "
    "in your own voice, without managing his response to the naming.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be moments &mdash; not most weeks, "
    "but they will come &mdash; when the slow drift beneath the warmth "
    "breaks the surface and both of you are in breakdown at the same time. "
    "The Plea is up in both of you simultaneously. The room is not loud "
    "&mdash; this pairing rarely produces loud conflict &mdash; but it is "
    "fast and circular and exhausting, and neither of you, in that moment, "
    "has access to the more thoughtful person you were three hours ago. "
    "Here is what is happening in that moment, named plainly.",

    "{name_b}, when the Plea rises in you, you are not simply asking for "
    "reassurance. You are doing something more specific: you are giving "
    "harder, more urgently, more apologetically &mdash; offering more "
    "warmth, more care, more service &mdash; because giving is the only "
    "tool the Ambassador has ever had for closing the gap. The Plea "
    "does not look like desperation from the outside. It looks like "
    "more of what you have always been. But the urgency underneath it "
    "is real, and {name_a} feels it. The giving has changed temperature. "
    "It is now asking for something back in a way it was not before.",

    "{name_a}, when your Plea rises in response, you are also not simply "
    "asking for reassurance. You are cycling through versions &mdash; "
    "trying different registers, different levels of warmth, different "
    "responses to the giving &mdash; because the Adapter's answer to "
    "a gap is always to produce a better calibration. You sense that "
    "what you are currently offering is not landing, and so you adjust. "
    "But the adjustment itself is visible to {name_b}, who is watching "
    "precisely for a response that is not adjusted. The more you calibrate, "
    "the less certain she is of what she is actually receiving. "
    "The more uncertain she becomes, the harder she gives. "
    "The harder she gives, the more the calibration runs.",

    "Both of you are running toward each other. Neither of you is being "
    "met. The loop is fast and nearly invisible, because it is happening "
    "entirely inside the register of warmth and care. There is no anger "
    "in the room. There is only two people trying very hard to give "
    "each other something that neither of them can produce from within "
    "the mechanism they are running.",

    "The Apostle John names the root of this loop with unusual precision: "
    "<i>There is no fear in love, but perfect love casts out fear. "
    "For fear has to do with punishment, and whoever fears has not been "
    "perfected in love. We love because he first loved us.</i> "
    "(1 John 4:18&ndash;19) Read this slowly, both of you. Love that "
    "flows from fear cannot rest. {name_b}'s giving, when it is "
    "shaped by the fear that the connection will dissolve if she "
    "stops giving, is love mixed with fear &mdash; and love mixed "
    "with fear cannot produce the certainty she is looking for. "
    "{name_a}'s calibration, when it is shaped by the fear that the "
    "un-adapted self will not be acceptable, is receiving mixed with "
    "fear &mdash; and receiving mixed with fear cannot produce the "
    "freedom he is looking for. Both of you are, in this moment, "
    "doing something that looks like love and is partly something else.",

    "<b>One of you, not both, calls the pause.</b> Whichever one "
    "notices first what is happening says out loud: <i>this is the "
    "loop. Twenty minutes.</i> No final word. No last gesture of "
    "warmth. No one adjusts the room before they leave it. "
    "Twenty minutes, non-negotiable, and the only rule of the "
    "pause is that no one rehearses the next giving or produces "
    "the next calibration while it runs.",

    "<b>In the twenty minutes, do not strategize. Pray.</b> "
    "Not eloquently. {name_b}: <i>Lord, my Plea is up. "
    "I am giving from fear again. Help me stop giving for "
    "twenty minutes and receive what you have already given me. "
    "I am lovable because I am in Christ, and no amount of "
    "giving will make me more so.</i> {name_a}: <i>Lord, "
    "my calibration is running. I am producing versions "
    "again instead of being present. Help me come back to "
    "{name_b} as myself &mdash; the self you named before "
    "any room existed to require a version.</i>",

    "<b>When you come back, each of you says one sentence.</b> "
    "{name_b}, your sentence is not the giving. It is one "
    "true thing you actually want &mdash; not offered, not "
    "wrapped in care for him &mdash; just named plainly: "
    "<i>I need you to tell me something true about yourself "
    "that has nothing to do with what I just gave you.</i> "
    "{name_a}, your sentence is not the calibrated response. "
    "It is one true thing from the self below the versions: "
    "<i>I am glad you are here.</i> Or: <i>I love you and "
    "I have been working too hard to show it the right way.</i> "
    "One sentence. Then stop. Then sit in it.",

    "<b>Neither of you is the problem.</b> The Plea and the "
    "calibration-loop are old mechanisms doing the only job "
    "they were ever trained to do. They were built in rooms "
    "that no longer exist, for emergencies that have long since "
    "passed. The truest thing about both of you is not the "
    "mechanism. It is that you chose each other before God "
    "and have been, in your own imperfect and fear-adjacent "
    "ways, trying to love each other well. That is worth "
    "something. The covenant you made is not undone by the "
    "loop. It is the frame that holds you both while the "
    "loop slowly runs down.",
]

COMMITMENTS_INTRO = [
    "What follows are six commitments &mdash; three from {name_a}, three from "
    "{name_b}. They are not vows in the legal sense. They are the small daily "
    "practices that, offered to each other freely and kept with reasonable "
    "consistency, change the temperature of a home over months and years. "
    "Read each one slowly. If one of you cannot make a particular commitment "
    "in good faith yet, do not make it. The goal is not performance. "
    "The goal is honesty.",
]

A_COMMITMENTS = [
    (
        "I will offer you the same self this week even when the room calls for someone else.",
        "{name_b}, I commit to bringing you a consistent self in the moments that matter "
        "most to our shared life. Not by suppressing the attunement that is genuinely a "
        "gift, but by distinguishing between the calibration that flows from love and the "
        "calibration that flows from fear. When I feel myself adjusting to what your "
        "giving seems to need from me, I will pause and ask: <i>what would I actually "
        "say if I were not reading the room?</i> And then I will say that. You deserve "
        "to receive the un-calibrated version of me, even when it is less smooth and "
        "less warm than the version you sometimes produce in me.",
    ),
    (
        "I will name what I actually want before I read what you seem to need.",
        "{name_b}, I commit to speaking my own preference before I have checked "
        "it against what you appear to need from me. Once a day, in a low-stakes "
        "moment, I will offer an un-adjusted opinion &mdash; what I actually "
        "want for dinner, what I actually think about the decision, what I "
        "actually feel about the week &mdash; before I have calibrated it to "
        "what the room seems to require. The Adapter has been running your "
        "marriage on borrowed preferences for too long. I will practice giving "
        "you mine.",
    ),
    (
        "I will stay in the room as one person when the loop begins to run.",
        "{name_b}, when I feel myself cycling through versions in response to "
        "your giving &mdash; when the calibration is running and I cannot quite "
        "find the right register &mdash; I commit to stopping and naming it in "
        "one sentence rather than producing another version. <i>I am trying too "
        "hard to receive this correctly.</i> That is enough. You do not need the "
        "right version. You need me. I will practice being that.",
    ),
]

B_COMMITMENTS = [
    (
        "I will let you not match my emotional weather today, and not read that as withdrawal.",
        "{name_a}, I commit to separating your emotional register from my sense of "
        "the connection. When you are quieter than I expected, or less warm than the "
        "room I have prepared, I will not immediately read it as the beginning of "
        "disconnection. I will remind myself that your weather today is your weather "
        "&mdash; not a verdict on the giving. I will practice sitting with the "
        "difference for twenty minutes before I do anything about it.",
    ),
    (
        "I will name what I actually want, not what I hope you will spontaneously offer.",
        "{name_a}, I commit to asking for what I need directly, without first "
        "wrapping it in concern for you or framing it as fine-if-you-cannot. "
        "Once a week, I will name one genuine need without managing your response "
        "to the naming. Not <i>I was wondering if maybe, when you have time</i> "
        "&mdash; but <i>I need this from you.</i> The Ambassador has been "
        "waiting for you to intuit the asking. You cannot intuit it if I "
        "do not say it. I will say it.",
    ),
    (
        "I will give you something this week from fullness rather than from need.",
        "{name_a}, I commit to finding, at least once this week, a moment when "
        "I give to you not because the connection feels thin and I need to restore "
        "it, but because I am genuinely glad you are here and want to show you. "
        "The difference between those two givings is not always visible from the "
        "outside. I will know the difference. I commit to practicing the second "
        "one &mdash; to giving from what the gospel says I already have, rather "
        "than giving in order to earn what I am afraid I do not.",
    ),
]

PRAYER = [
    "Father,",

    "You set these two next to each other, and you knew exactly what you "
    "were doing. You knew the Adapter would need someone whose love comes "
    "first, before the calibration has produced anything. You knew the "
    "Ambassador would need someone whose attunement would make the giving "
    "feel received. You knew the Tuesday evenings when the warmth would "
    "be real and the grounding underneath it uncertain. You knew all of "
    "it before either of them said yes.",

    "Teach them the grammar of each other. Teach {name_a} to come to "
    "{name_b} as one person &mdash; not the version most likely to confirm "
    "that her giving landed, not the calibration that reads what the room "
    "needs and produces it, but the actual un-adapted self you named before "
    "any room existed to call forth a version. Teach {name_b} to give to "
    "{name_a} from what she already has in you &mdash; not in order to earn "
    "a love that is already hers, not in order to produce a confirmation "
    "that the giving mattered, but freely, from the overflow of a love she "
    "did not have to earn and cannot lose.",

    "When the calibration runs in {name_a} &mdash; when the versions are "
    "cycling and the self below them cannot quite find its way into the "
    "room &mdash; remind him that he is named, in Christ, before any "
    "room existed to require a version; that the Father who chose him "
    "before the foundation of the world is not waiting for the right "
    "performance before the love arrives. When the Plea rises in {name_b} "
    "&mdash; when the giving is hard and urgent and fear-shaped &mdash; "
    "remind her that she is already loved with a love that does not "
    "depend on what she gives next; that the account is settled; that "
    "she can set down the giving for five minutes and simply be held.",

    "Make their home a room in which {name_a} can be simply present "
    "without calibrating to what the room seems to need, and {name_b} "
    "can receive without watching to see whether the receiving is real. "
    "Make their table a place where one true sentence &mdash; unmanaged, "
    "un-calibrated, offered without a hand on the thermostat &mdash; is "
    "given and received and sufficient. Make their covenant the frame "
    "that holds them while the old mechanisms slowly work shorter hours.",

    "And Father, when they are old and the small repeating rocks have "
    "finally become smaller and less repeating, let them look back and "
    "see that the warmth they always had became, over the years, "
    "something more honest &mdash; a warmth that did not require either "
    "of them to perform, that came not from calibration or from earning "
    "but from two people who learned, slowly and imperfectly, to love "
    "each other from what you had already given them. Let them see, "
    "in that looking back, the signature of a Maker who knew what he "
    "was doing when he put them next to each other.",

    "In the name of the One who loved us while we were still calibrating "
    "ourselves against our own sin, and who gave himself freely, with "
    "no ledger in his hand.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. "
    "The pages that follow are different. They are meant to be spoken "
    "<i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken "
    "slowly, somewhere quiet, with no children in the room and no phones "
    "on the table. There are six rounds, and they build on each other. "
    "Resist the temptation to skip ahead. Start at Round One even if it "
    "feels too light; the lightness is the point.",

    "Some of the questions are playful. Some are direct. A few are the "
    "kind that, when answered honestly, will sit with you for a week. "
    "None of them are trivia. All of them are an invitation.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who "
    "did not read answers first, in full, without interruption. Then the "
    "reader answers the same question. Then you move on. You do not have "
    "to finish all six rounds in one night &mdash; two or three rounds, "
    "taken seriously, is often better than racing through all of them. "
    "Save the rest for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. You may "
    "not love everything you hear. Stay with it. The point of this is not "
    "to grade each other's answers. The point is to be known, and to do "
    "the slow work of knowing.",
]

ROUND_1 = [
    (
        "hypothetical",
        "If our marriage were a piece of music &mdash; any genre, any era &mdash; "
        "what would it be, and what part would each of us play?",
        "Let the metaphor say what plain language sometimes cannot. "
        "Don't overthink it. Answer with the first image that comes.",
    ),
    (
        "observation",
        "What is something I did for you this week that you noticed and didn't mention?",
        "Not a complaint. A small noticing. The fact that you noticed at all is the gift.",
    ),
    (
        "playful",
        "If you had to describe the emotional climate of our home right now as a season "
        "of the year, what season would it be &mdash; and what season do you want it to be "
        "in six months?",
        "Yes, really. Answer with the first thing that comes to mind. The difference "
        "between the two answers is often worth a whole conversation.",
    ),
]

ROUND_2 = [
    (
        "fill-in-blank",
        "I don't think I tell you this enough &mdash; I am amazed at the way God made "
        "you so _______. Your _______ is a gift to our marriage, and I want to get "
        "better at receiving it.",
        "Two blanks. Be specific. 'Caring' is too easy; 'the way you notice when I am "
        "carrying something before I have named it' is closer.",
    ),
    (
        "observation",
        "What is one thing you have watched me do this year that you wish more people "
        "could see?",
        "Most of us only ever see ourselves do our most public things. "
        "Tell your spouse about the private ones.",
    ),
    (
        "one-word",
        "If you had to choose one word to describe what it feels like when we are "
        "genuinely in sync &mdash; when the Adapter and the Ambassador are working "
        "together rather than around each other &mdash; what word would it be?",
        "One word, said out loud. Then explain it, briefly.",
    ),
]

ROUND_3 = [
    (
        "forward-looking",
        "Five years from now, when we look back on this season of our marriage, "
        "what do you hope we will say we did well together?",
        "Not what you wish you had done. What you want, when you look back, "
        "to be able to say you actually did.",
    ),
    (
        "theological",
        "Where, in the last month, have you seen God specifically at work in me "
        "&mdash; not the version I perform, but the actual person underneath?",
        "Not where you want him to work. Where you have already seen it. Name it.",
    ),
    (
        "shared-identity",
        "Finish this sentence three times: 'We are the kind of couple who _______.' "
        "Give one playful answer, one true answer, and one aspirational answer.",
        "The 'we' is the point. Let all three answers be real.",
    ),
]

ROUND_4 = [
    (
        "strength",
        "What is something I do for our shared life that you would have to learn to "
        "do for yourself if I were not here?",
        "Hard to ask. Important to hear. Stay with the answer.",
    ),
    (
        "fill-in-blank",
        "One of the gifts of being married to you is that I get to be _______ in ways "
        "I never would have been on my own.",
        "A version of yourself that only exists because this marriage exists. "
        "Name it as specifically as you can.",
    ),
    (
        "observation",
        "Name one moment in our story where you knew, without doubt, that we had "
        "built something together that neither of us could have built alone.",
        "Tell the story in full. The remembering is part of the strengthening.",
    ),
]

ROUND_5 = [
    (
        "hard",
        "{name_a}, when has {name_b}'s giving felt like a gift rather than a weight? "
        "And {name_b}, when has {name_a}'s attunement felt like presence rather than "
        "a mirror? Each of you name one specific moment.",
        "The answer is always somewhere in your history. Find it.",
    ),
    (
        "profile-aware",
        "When you are in the loop &mdash; when the giving is urgent and the calibration "
        "is running &mdash; what is the one thing you most wish the other person would "
        "say or do differently, not later, but in that moment?",
        "You both know what these patterns are now. Ask each other for what would "
        "actually help. Be specific.",
    ),
    (
        "hard",
        "What is one thing you have been carrying lately that you have not yet brought "
        "to me, and what has kept you from bringing it?",
        "Not an accusation. An invitation. Hear the answer without defending.",
    ),
]

ROUND_6 = [
    (
        "blessing",
        "Place your hand on your spouse's hand. Say their name. Then say: "
        "'You are not a problem to be solved. You are a gift I get to receive again "
        "tomorrow.' Say it slowly. Let them say it back.",
        "You may feel silly. That is part of why it works. Do it anyway.",
    ),
    (
        "prayer",
        "Pray for each other &mdash; not silently, not generally, but out loud and "
        "by name. One sentence is enough. Pray for the thing they just told you in "
        "Round Five.",
        "The closing of the date. Do not skip.",
    ),
]


def _render(text, name_a, name_b):
    return text.format(name_a=name_a, name_b=name_b)


def build(sub_a, sub_b) -> bytes:
    """Generate the Adapter+Ambassador couples walkthrough PDF.

    sub_a: the submission of the Adapter spouse
    sub_b: the submission of the Ambassador spouse
    """
    ensure_fonts()
    S = make_styles()

    name_a = _first_name(sub_a, "Adapter")
    name_b = _first_name(sub_b, "Ambassador")

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
                "Adapter &middot; Plea / Quiet Exit<br/>"
                "<font size=9 color='#6b6862'>Control &middot; Am I free?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_b.upper()}</b></font><br/>"
                "Ambassador &middot; Plea<br/>"
                "<font size=9 color='#6b6862'>Disconnection &middot; Am I lovable?</font>",
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
        "<i>\u201cThere is no fear in love, but perfect love casts out fear\u2026<br/>"
        "We love because he first loved us.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "1 John 4:18\u201319",
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
                          "Control / Shame", "Am I free?",
                          "The Adapter", "The Plea / Quiet Exit"),
            "",
            _profile_card(S, name_b, ACCENT_HER,
                          "Disconnection", "Am I lovable?",
                          "The Ambassador", "The Plea"),
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
                   "Love that comes toward you before the calibration has produced anything.")
    for p in GIFT_TO_A:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4 ──
    section_header(story, S, "SECTION FOUR  \u00b7  HIS GIFT TO HER",
                   f"What {name_a} gives {name_b}.",
                   "A mirror that moves. Something Ambassadors rarely receive.")
    for p in GIFT_TO_B:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5 ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Calibration meets service.",
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
                   "When both Pleas are in the room at once.",
                   "What is happening, and what to do while you can still see it.")
    for p in BOTH_BREAK[:4]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do, while you can still see it.",
                   "Four practices for the loop, in order.")
    for p in BOTH_BREAK[4:]:
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
    for commit_name, commit_body in A_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(commit_name, S["H3"]),
            Paragraph(R(commit_body), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_b}, to {name_a}.",
                   "Three commitments, in her voice, for him to receive.")
    story.append(Paragraph(f"FROM {name_b.upper()}, TO {name_a.upper()}", S["CommitLabelHer"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT_HER,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for commit_name, commit_body in B_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(commit_name, S["H3Her"]),
            Paragraph(R(commit_body), S["CommitBody"]),
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

    sub_a = FakeSub("Jordan", "ADPT", "PLEA", "CTRL", "FREE")
    sub_b = FakeSub("Rachel", "AMB", "PLEA", "DISC", "LOV")

    pdf_bytes = build(sub_a, sub_b)
    out_path = os.path.join(os.path.dirname(__file__), "adapter_ambassador_test.pdf")
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
            if "SECTION THREE" in txt:
                snippet = txt.strip()[:200]
                break
    except Exception as e:
        page_count = "unknown"
        snippet = str(e)

    print(f"DONE: adapter_ambassador.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
