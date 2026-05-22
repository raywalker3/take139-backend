"""Couples Walkthrough — Architect + Ambassador.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where one spouse is an Architect and the
other is an Ambassador. First names are substituted from the submissions:
    {name_arch}  -> the Architect spouse's first name
    {name_amb}   -> the Ambassador spouse's first name

One of the most common pairings in evangelical marriages. The Architect builds
and protects; the Ambassador serves and warms. Until one of them feels
uncared-for, and then the prosecutor and the pleader meet in the kitchen.
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


# ──────────── PROSE — uses {name_arch} and {name_amb} placeholders ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small repeating ones "
    "&mdash; the same disappointment in slightly different clothes, three or four times a week, "
    "year after year, until both people have forgotten what they were originally hoping for.",

    "What follows is a counselor's read of the small repeating rocks in your particular marriage. "
    "Not the dramatic failures, which you would have addressed already. The small ones. The ones "
    "that happen on a Tuesday evening when {name_arch} is managing the calendar and {name_amb} "
    "is smoothing over something that should not require smoothing, and neither of you can "
    "quite say why the room feels slightly colder than it did an hour ago.",

    "You are both reading this because you have decided to look at those rocks. That decision "
    "is more significant than it seems. Most couples spend a lifetime navigating around them "
    "without naming them. Naming them is half the work.",

    "Here is what I want to do for you. I will name what each of you brings the other that you "
    "could not have built alone &mdash; the genuine, theological gift that your two shapes form "
    "together. Then I will name the collision your two questions create, in the specific way it "
    "shows up in your marriage. Then I will name the worst case &mdash; the moment when "
    "{name_arch}'s Attorney and {name_amb}'s Plea are in the room at the same time &mdash; "
    "and what to do then. Then I will hand each of you commitments, not as rules, but as the "
    "kind of small daily practices that, over years, change the temperature of a home.",

    "Read it together, if you can. If not, read it separately and then sit down with it. Argue "
    "with what does not fit. Stay with what does. The goal is not insight; the goal is a marriage "
    "in which the small repeating rocks become smaller, less repeating, and eventually a part of "
    "the landscape you can both laugh at.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on paper, "
    "side by side. Most couples never see their two profiles next to each other. You are about to.",
]

TWO_SHAPES_BODY = [
    "{name_arch}, you are an <b>Architect</b> whose body reads disrespect as an alarm and whose "
    "deepest question is whether you are protected. You build structures because you believe, in "
    "your bones, that suffering is largely a function of insufficient planning. When the plan is "
    "overridden or the boundary crossed, an <b>Attorney</b> takes the floor and begins to "
    "litigate &mdash; not to win an argument, but to prove the perimeter still holds.",

    "{name_amb}, you are an <b>Ambassador</b> whose body reads disconnection as an alarm and "
    "whose deepest question is whether you are lovable. You have learned to manage the emotional "
    "temperature of every room you enter, because warmth, for you, is not merely kindness &mdash; "
    "it is the evidence that the connection is still intact. When the warmth does not return, or "
    "when giving has not been received with gratitude, a <b>Plea</b> takes the floor: a bid for "
    "acknowledgment that has been waiting quietly in the wings for longer than either of you knew.",

    "Notice what these two profiles do <i>not</i> share, and notice what they actually share "
    "underneath. You are not asking the same question. {name_arch} is asking <i>am I protected?</i> "
    "and {name_amb} is asking <i>am I lovable?</i> &mdash; two questions that, in a marriage, "
    "are easy to mistake for each other and easy to fail to answer for each other.",

    "But underneath the two questions is the same root. Both of you have organized your lives "
    "around preventing a specific kind of pain: {name_arch} prevents loss through structure, "
    "and {name_amb} prevents loss through service. Both of you, in different costumes, are "
    "asking <i>is my place here secure?</i> Neither of you has quite believed, at the level "
    "where it counts, that the answer was spoken over you before you built anything or gave "
    "anything.",

    "This is, in fact, one of the most common pairings in evangelical marriages, and there is a "
    "reason. The Architect respects the Ambassador's warmth &mdash; it provides the relational "
    "climate in which the Architect's structures are gratefully received rather than merely "
    "tolerated. The Ambassador respects the Architect's coverage &mdash; it provides the external "
    "order that frees the Ambassador from having to manage everything at once. You have, without "
    "planning it, built something that works. The friction between you is real, but the foundation "
    "is unusually solid.",
]

GIFT_TO_ARCH = [
    "{name_amb} gives {name_arch} something almost no one else in his life is in a position to "
    "give: <b>a room that is warm before he has done anything to earn it.</b>",

    "Most of the rooms {name_arch} walks into require him to perform. Plans must be executed. "
    "Structures must be maintained. People depend on him, and the dependence is real. The "
    "Architect cannot rest in those rooms because the moment he does, something he has been "
    "holding will slip. The warmth in those rooms, when it comes, is in some sense a reward "
    "for the building.",

    "{name_amb}, by virtue of being an Ambassador, makes warmth. Not as a response to "
    "{name_arch}'s performance &mdash; warmth is simply what the Ambassador does. She asks "
    "how he is doing and actually wants to know. She notices when he is tired before he has "
    "named it. She manages the relational temperature of the home in ways that mean {name_arch} "
    "comes back at the end of the day to a room that does not require him to be three steps "
    "ahead. This is, for the Architect, rarer than {name_amb} may realize.",

    "The theological word for what {name_amb} gives {name_arch} is <i>welcome</i>. Not the "
    "welcome of a gathering that is glad you came because you brought something useful. The "
    "welcome of a home that is simply glad you are back. Keller, writing on Ephesians 5, "
    "observed that the mystery of Christ and the Church is partly the mystery of a love that "
    "does not require the beloved to have earned it before the door is opened. {name_amb}, "
    "in her best moments, embodies this for {name_arch} in the daily currency of a marriage.",

    "{name_arch} &mdash; if you want to thank {name_amb} for something this week, thank her "
    "for this. She probably does not know she is giving it to you, because the Ambassador "
    "gives warmth so naturally that she may not have noticed it is a gift. Tell her that the "
    "temperature of your home is, in no small part, something she builds every day, and that "
    "you do not take it for granted. She will receive the thanks quietly. Say it anyway.",

    "{name_amb} &mdash; what {name_arch} is receiving from you, when you simply make the room "
    "warm before he has done anything to justify it, is a small daily picture of the love he "
    "most needs to learn to receive: love that is not a function of his output. The thing you "
    "do without thinking is, for him, a kind of gospel.",
]

GIFT_TO_AMB = [
    "{name_arch} gives {name_amb} something Ambassadors rarely build for themselves: "
    "<b>a held perimeter.</b>",

    "The Ambassador manages the relational climate of every room she enters. What she rarely "
    "manages &mdash; not from laziness, but from the nature of the mechanism &mdash; is the "
    "external structure that holds the rooms in place. Calendars, contingencies, the long-range "
    "planning that means the family does not arrive at an important moment unprepared: these are "
    "the domains that the Ambassador, absorbed in the work of warmth and connection, tends to "
    "leave to the last possible moment, or to whoever will handle them.",

    "{name_arch}, by virtue of being an Architect, is constantly building that perimeter. "
    "The fact that the calendar functions, that the contingencies are thought through, that the "
    "family has a plan for the hard seasons before they arrive &mdash; this is {name_arch}'s "
    "love in its native grammar. He cannot always say <i>I love you</i> in the way {name_amb} "
    "says it. But he says it in the blueprint. He says it in the thing he prepared last Tuesday "
    "that no one will need until Thursday, and that, by Thursday, will simply be there.",

    "Paul, in Ephesians 5:25&ndash;33, uses the language of Christ's love for the Church to "
    "describe what a husband's love looks like in its fullest expression. He says Christ "
    "<i>gave himself up for her, that he might sanctify her, having cleansed her by the washing "
    "of water with the word, so that he might present her to himself in splendor, without spot "
    "or wrinkle or any such thing, that she might be holy and without blemish.</i> (Ephesians "
    "5:25&ndash;27) This is not the language of contract. It is the language of a builder who "
    "is constructing something beautiful, at cost to himself, for her. {name_arch} loves you "
    "this way, {name_amb}, when he builds in advance so that the life you share does not fall "
    "apart on the day it needs to hold.",

    "{name_amb} &mdash; if you want to thank {name_arch} for something this week, thank him "
    "for something specific he has built or planned that you did not have to build yourself. "
    "Name the exact thing. Architects do not always know their blueprints are received as love. "
    "Tell him, and he will know.",

    "{name_arch} &mdash; what {name_amb} is receiving from you, when you hold the structure "
    "and the long view, is the freedom to give warmth without paying the full external cost of "
    "running a life without backup. The thing in you that has sometimes been told it is too "
    "much planning, too much managing, is for her a kind of covering under which she can do "
    "what she does best.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you, even if "
    "you have not named it in quite these terms.",

    "{name_arch}'s core question is <i>am I protected?</i> {name_amb}'s is <i>am I lovable?</i> "
    "These two questions are not opposed in theory. In the daily mechanics of a marriage, they "
    "ask for different things, and the asking often misfires in ways that leave both of you "
    "quietly convinced you have been wronged.",

    "Protection wants order, reliability, predictability. When {name_arch} is trying to feel "
    "protected, he reaches for systems: the schedule, the plan, the expectation set in advance. "
    "The way the Architect loves {name_amb} is often through this grammar &mdash; by securing "
    "the next three rooms before either of you walks into them. To {name_arch}, this is love "
    "expressed in its most responsible form. He is, in his own language, covering the family.",

    "Lovability wants acknowledgment, warmth, the felt sense of being received as a person "
    "and not managed as a component. When {name_amb} is trying to feel lovable, she does not "
    "reach for systems. She reaches for the warmth she has been cultivating all day in the "
    "home &mdash; the dinner she made, the errand she ran, the quiet act of service that she "
    "did not mention because the Ambassador does not announce her giving. She is waiting, "
    "not consciously, but waiting, to see whether it was noticed. To {name_amb}, the felt "
    "sense of being administered &mdash; even kindly, even efficiently &mdash; is not "
    "protection. It is the absence of the very warmth she has been offering.",

    "Ecclesiastes 4:9&ndash;12 speaks of two people who are stronger together than apart, "
    "who warm each other, who help each other up when one falls. The writer is describing "
    "what a covenant partnership can be at its best. But underneath the warmth the preacher "
    "imagines is a shared understanding: each person knows what the other is giving and "
    "receives it gratefully. The Architect and the Ambassador have, in their best seasons, "
    "exactly this. The friction comes in the seasons when the giving is happening in two "
    "different dialects and neither person is certain the other is hearing it.",

    "Here is the collision in slow motion. {name_arch}, in trying to protect the home on "
    "a Tuesday evening, addresses {name_amb} as a node in the system he is maintaining "
    "&mdash; the appointment that needs confirming, the schedule item that requires her "
    "input, the logistical question that will not keep until morning. He is, in his mind, "
    "loving her by holding the structure. She experiences it as being addressed as a function "
    "rather than a person. Her trigger fires: <i>disconnection.</i> The old question wakes: "
    "<i>am I lovable, or am I useful?</i>",

    "She does not say so. Ambassadors rarely say so in the moment. Instead, she does what "
    "the Ambassador has always done: she continues giving. She answers the logistical question. "
    "She keeps the warmth available. But she gives now from a slightly different place &mdash; "
    "not from overflow, but from a quiet determination not to let the temperature drop, "
    "because dropping feels dangerous. The warmth is still present, but it has shifted from "
    "gift to maintenance.",

    "{name_arch} does not register the shift, because warmth is warmth to the Architect. "
    "What he registers, eventually, is that the evening feels slightly formal &mdash; that "
    "{name_amb} is pleasant but not quite present, that the room is warm but not quite "
    "connected. This reads to him not as <i>she is hurting</i> but as <i>she is withholding</i> "
    "&mdash; a subtle but real shade of disrespect, as though the Architect's careful management "
    "of the evening is being declined. His trigger fires: <i>disrespect.</i> He doubles down on "
    "the systems, because building is the only grammar he has. She gives more warmth from a "
    "more depleted place. Neither of you knows what the other is actually doing.",

    "The way out is not for either of you to stop being who you are. The Architect is not "
    "going to stop building, and he should not. The Ambassador is not going to stop warming, "
    "and she should not. The way out is for each of you to learn to translate what the other "
    "is actually saying, in real time, before the room gets too quiet.",

    "{name_arch}, when {name_amb} shifts from warm to merely pleasant, the translation is "
    "almost never <i>she is dismissing what I have built.</i> Nine times out of ten, the "
    "translation is <i>she just got administered when she needed to be seen.</i> The right "
    "move, when you notice the shift, is to set the calendar down for sixty seconds and ask "
    "her one question that has nothing to do with logistics. Not <i>are you okay?</i> as a "
    "scheduling check. A real question. <i>How are you actually doing tonight?</i> And then "
    "wait for the answer.",

    "{name_amb}, when {name_arch} goes into Architect mode and the questions feel like "
    "administration rather than love, the translation is almost never <i>he does not see me.</i> "
    "Nine times out of ten, the translation is <i>he is afraid the perimeter is failing and "
    "this is the only language he has for covering us.</i> The right move is to receive the "
    "logistical question first, and then name what you need in one sentence. Not a speech. "
    "One sentence: <i>I need a minute as a person, not as the next item.</i> He can hear that. "
    "What he cannot read is the warmth that has quietly gone from overflow to maintenance, "
    "because to him it still looks the same.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be seasons &mdash; not every week, but they will come "
    "&mdash; when the small collision in the kitchen escalates, or when a longer accumulation "
    "of smaller disappointments has built to a point where both of you are in the breakdown at "
    "the same time. The Attorney is on his feet. The Plea is in the room. And neither of you, "
    "in that moment, has access to the more generous person you were three hours ago.",

    "Here is what is happening, named plainly so you can both see it.",

    "{name_arch}, when the Attorney is on his feet, he is not arguing with {name_amb}. He is "
    "arguing with an old courtroom in his head &mdash; a room where being disregarded meant "
    "being unsafe, where the failure to honor the plan was evidence of a more fundamental "
    "disrespect. The brief he is building against {name_amb} is detailed and internally "
    "consistent. He believes, in that moment, that if he can simply lay out the evidence "
    "clearly enough, the verdict will correct the situation. To {name_amb}, however, "
    "who has given warmth all day and received what felt like administration in return, "
    "the Attorney's brief does not feel like a defense. It feels like a prosecution. "
    "She is being presented with exhibits by someone she has been trying to love.",

    "{name_amb}, when the Plea is rising, she is not, in that moment, making a calculated "
    "bid for sympathy. She is releasing the accumulated weight of an unknown ledger &mdash; "
    "the dinners made, the emotions smoothed, the needs set aside, the service given without "
    "acknowledgment &mdash; that she did not know she was keeping until this moment when it "
    "will no longer stay quiet. The Plea is not a manipulation. It is a grief that has run "
    "out of room. But to {name_arch}, who has been hearing what sounds like a counter-brief "
    "that he did not know was being assembled, the Plea reads as evidence that his Attorney "
    "must answer. So the Attorney rises higher. So the Plea rises higher. The loop is fast "
    "and almost never about what started it.",

    "Paul, in 1 Corinthians 13:4&ndash;7, writes what love actually looks like when it is "
    "working correctly: <i>Love is patient and kind; love does not envy or boast; it is not "
    "arrogant or rude. It does not insist on its own way; it is not irritable or resentful; "
    "it does not rejoice at wrongdoing, but rejoices with the truth. Love bears all things, "
    "believes all things, hopes all things, endures all things.</i> This is not a picture "
    "of either the Attorney or the Plea. The Attorney insists on its own way and keeps a "
    "record, even when the record is accurate. The Plea is patient until it is not, and "
    "then it speaks all the things it has been bearing at once. Both of you, in breakdown, "
    "are temporarily doing the opposite of what love requires. That is not a judgment on "
    "either of you. It is the honest diagnostic. Both of you, when you are most hurt, "
    "reach for the thing most opposite to the love Paul describes.",

    "What to do, when you can both still see what is happening:",

    "<b>One of you, not both, names the loop.</b> Whichever of you notices first what is "
    "happening says, out loud, without a verdict: <i>this is the loop. Twenty minutes.</i> "
    "No discussion of who is right. No final word before the pause. The pause is not a "
    "surrender; it is a suspension of proceedings that are no longer producing anything "
    "useful. The only rule of the pause is that neither of you uses it to draft the next "
    "sentence.",

    "<b>In the twenty minutes, do not strategize. Pray.</b> Pray for each other by name. "
    "Not eloquently &mdash; {name_arch}, pray for the Ambassador who is exhausted from "
    "giving and afraid that no one noticed. {name_amb}, pray for the Architect who is "
    "building hard because the perimeter feels like it is failing and he does not know "
    "another language for fear. You do not need to pray aloud, though you may. You need "
    "to pray specifically, by name, for the person who is also in the room.",

    "<b>When you come back, one sentence each.</b> {name_arch}, your sentence is not "
    "the brief. It is one true thing about what you felt, beginning with <i>I.</i> "
    "<i>I felt like the plan was being dismissed.</i> That is enough. {name_amb}, your "
    "sentence is not the ledger. It is the single weight under all the others. "
    "<i>I felt invisible tonight after I had tried all day.</i> That is enough. "
    "Both of you can say one sentence. Then stop.",

    "<b>If the loop runs anyway, name it together the next day.</b> Not to relitigate "
    "&mdash; to name it as a pattern that belongs to both of you, that neither of you alone "
    "caused, and that both of you are committed to outgrowing. The Attorney and the Plea "
    "have been working long shifts. They will not retire in a single conversation. "
    "The marriage that knows this can be patient with the slow retirement.",

    "Hear this clearly, both of you. <b>Neither of you is the problem.</b> The Attorney "
    "is not the truest thing about {name_arch}. The Plea is not the truest thing about "
    "{name_amb}. They are old mechanisms doing the only job they were ever taught to do. "
    "The truest thing about both of you is that you are a man and a woman who have chosen "
    "each other, and who are, in the ordinary Tuesday of a long marriage, learning to "
    "receive a kind of love from each other that neither of you fully learned to trust before.",
]

COMMITMENTS_INTRO = [
    "What follows are six commitments &mdash; three from {name_arch}, three from {name_amb}. "
    "They are not vows in the legal sense. They are the small daily practices that, offered "
    "to each other freely, change the temperature of a home over months and years. Read each "
    "one slowly. If one of you cannot say a particular commitment in good faith yet, do not "
    "say it. The goal is not performance; it is honesty.",
]

ARCH_COMMITMENTS = [
    (
        "To receive the warmth without auditing it.",
        "{name_amb}, I commit to receiving the care you bring to our home as a gift, not as "
        "a system I need to evaluate against the plan. When you make the room warm, I will "
        "receive that warmth as love &mdash; not as a variable to be optimized, not as a "
        "check I need to verify, but as the gift of the person I chose. I will thank you "
        "for one specific thing you gave this week, named out loud, before the week is done.",
    ),
    (
        "To set down the blueprint and look at you.",
        "{name_amb}, I commit to setting down the calendar at least once each evening we "
        "are in the same room. Not for an hour &mdash; for five minutes. In those five "
        "minutes I will look at you as a person, not as the next item in the structure I "
        "am maintaining. I will ask you a real question that has nothing to do with "
        "logistics. I will not always know what to ask. I will ask anyway.",
    ),
    (
        "To name the fear before the brief assembles.",
        "{name_amb}, when I feel myself building harder than the situation requires, I "
        "commit to naming what I am afraid of in one sentence rather than building in "
        "silence. The Attorney has been working overtime for a long time. You deserve to "
        "know when {name_arch} is afraid, not merely when the Architect is constructing "
        "a defense. The marriage deserves a voice that names the fear instead of acting "
        "it out.",
    ),
]

AMB_COMMITMENTS = [
    (
        "To name the cost before the ledger fills.",
        "{name_arch}, I commit to naming the small weights as they come, rather than "
        "carrying them in silence until the Plea does it for me. I will not always do "
        "this perfectly. But I will try, on the small things, to give them a sentence "
        "in the same week they happen. Not a brief &mdash; one sentence. Because the "
        "Plea becomes necessary only when the weight has nowhere else to go, and I "
        "want to give it somewhere else to go before it builds to that.",
    ),
    (
        "To receive the structure as love.",
        "{name_arch}, when you are in Architect mode and the questions feel like "
        "administration, I commit to remembering that the building is your way of "
        "saying <i>I am covering us.</i> I will receive the trellis as a gift, not "
        "a cage. When I need to be a person and not an item in the plan, I will say "
        "so in one sentence &mdash; and I will trust that you will course-correct, "
        "because you always have when I have said it plainly.",
    ),
    (
        "To let my need be visible.",
        "{name_arch}, I commit to letting you see what I actually need from this "
        "marriage, rather than serving in the direction of what I hope will be "
        "offered back. The Ambassador has been making herself useful for a long time "
        "as a way of answering the question <i>am I lovable?</i> I want to learn "
        "to ask the question directly instead &mdash; not constantly, not without "
        "consideration, but enough that you have the chance to answer it. Because "
        "I do not want you to find out what I needed only when the ledger opens.",
    ),
]

PRAYER = [
    "Father,",

    "You placed {name_arch} and {name_amb} next to each other, and you knew exactly what "
    "you were doing. You knew the Architect would need the Ambassador's warmth to teach him "
    "that love is not a reward for building. You knew the Ambassador would need the "
    "Architect's coverage to teach her that her place is secure even when she is not "
    "managing the temperature. You knew the Attorney and the Plea would find each other "
    "in the kitchen on hard evenings. You knew all of it before either of them said yes.",

    "Teach them the grammar of each other. Teach {name_arch} to read {name_amb}'s warmth "
    "not as a variable in the system but as the daily gift of a person who loves him before "
    "he has built anything today. Teach {name_amb} to read {name_arch}'s planning not as "
    "administration but as the language of a husband who is, in his own grammar, wrapping "
    "his arms around the family.",

    "You are, for {name_arch}, a Father &mdash; the one who holds the scales and from whom "
    "no perimeter is ever truly lost. You are, for {name_amb}, a Bridegroom &mdash; the one "
    "whose love is the only love in all the universe that requires nothing in return, that "
    "is not one degree warmer when she has given more. Teach them each to receive what the "
    "other cannot naturally give them, and to find in you the anchor for the question the "
    "other cannot fully answer.",

    "When the Attorney rises in {name_arch}, remind him that he already has an Advocate "
    "and the verdict has been spoken. When the Plea rises in {name_amb}, remind her that "
    "she is loved &mdash; not because of what she has given, but because of what you have "
    "given for her.",

    "Make their home a room in which neither of them has to perform. Make their table a "
    "place where the small weights are named on the day they happen. And when they are "
    "old and the children are grown and the calendar is finally quiet, let them look back "
    "and see that the small repeating rocks became smaller, and less repeating, and "
    "finally a part of the landscape they could both laugh at together.",

    "In the name of the One who loved his bride before she was lovely, and who is, even "
    "now, preparing the home in which they will live with him forever.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages that "
    "follow are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, somewhere "
    "quiet, with no children in the room and no phones on the table. There are six rounds, "
    "and they build on each other. Resist the temptation to skip ahead. Start at Round "
    "One even if it feels too light; the lightness is the point.",

    "Some of the questions are playful. Some are direct. A few are the kind of questions "
    "that, when answered honestly, will sit with you for a week. None of them are trivia. "
    "All of them are an invitation.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did not read "
    "answers first, in full, without interruption. Then the reader answers the same "
    "question. Then you move on. You do not have to finish all six rounds in one night "
    "&mdash; in fact, two or three rounds taken seriously is often better than racing "
    "through all of them. Save the rest for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. You may not love everything "
    "you hear. Stay with it. The point of this is not to grade each other's answers. "
    "The point is to be known, and to do the work of knowing.",
]

ROUND_1 = [
    (
        "hypothetical",
        "If our marriage were a building, what kind would it be &mdash; and which room "
        "would you say we spend the most time in together?",
        "Let {name_arch} answer as the Architect he is. Let {name_amb} answer as the person "
        "who knows which room is actually warmest.",
    ),
    (
        "observation",
        "What is something I did this week that you noticed and didn't mention?",
        "Not a complaint. A small noticing. The fact that you noticed at all is the gift.",
    ),
    (
        "playful",
        "If you had to give our marriage a theme song &mdash; right now, in this season "
        "&mdash; what would it be, and why?",
        "Yes, really. First thing that comes to mind. You can revise it after you explain it.",
    ),
]

ROUND_2 = [
    (
        "fill-in-blank",
        "I don't think I tell you this enough &mdash; I am amazed at the way God made "
        "you so _______. Your _______ is a gift to our marriage, and I want to get "
        "better at receiving it.",
        "Two blanks. Be specific. 'Kind' is too easy; 'still warm to me at the end of a "
        "day when I know you were exhausted' is closer.",
    ),
    (
        "observation",
        "What is one thing you've watched me do this year that you wish more people got to see?",
        "Most of us only see ourselves do our most public things. Tell your spouse about "
        "the private ones.",
    ),
    (
        "one-word",
        "If you had to choose one word to describe what it feels like when I walk through "
        "the door at the end of a long day, what word would it be?",
        "One word, said out loud. Then take one minute to explain it.",
    ),
]

ROUND_3 = [
    (
        "forward-looking",
        "Five years from now, when we look back on this season of our marriage, what do "
        "you hope we will say we did well together?",
        "Not what you wish you had done. What you want, when you look back, to be able "
        "to say you did.",
    ),
    (
        "theological",
        "Where, in the last month, have you seen God specifically at work in me?",
        "Not where you want him to work. Where you have already seen it. Name it.",
    ),
    (
        "shared-identity",
        "Finish this sentence three times: 'We are the kind of couple who _______.'"
        " Give one playful answer, one true answer, and one aspirational answer.",
        "The 'we' is the point. This is not about what each of you is separately.",
    ),
]

ROUND_4 = [
    (
        "strength",
        "What is something I do for you that you would have to learn to do for yourself "
        "if I weren't here?",
        "Hard to ask. Important to hear. Stay with the answer for a moment before you respond.",
    ),
    (
        "fill-in-blank",
        "One of the gifts of being married to you is that I get to be _______ in ways "
        "I never would have been on my own.",
        "A version of yourself that only exists because this marriage exists. Name it.",
    ),
    (
        "observation",
        "Name one moment in our story so far where you knew, with no doubt, that we had "
        "built something together that neither of us could have built alone.",
        "Tell the story in full. The remembering is part of the strengthening.",
    ),
]

ROUND_5 = [
    (
        "hard",
        "When you see me in breakdown &mdash; when the Attorney is up, or when the Plea "
        "is in the room &mdash; what is one thing you wish I would say or do differently, "
        "not later, but in the moment?",
        "You both know what these look like now. Ask each other for what would actually help.",
    ),
    (
        "profile-aware",
        "{name_arch}, what do you actually need from {name_amb} when the plan gets "
        "overridden &mdash; and {name_amb}, what do you actually need from {name_arch} "
        "when you have been giving all day and it has gone unnoticed?",
        "Name the real thing. Not the polite version. The real thing.",
    ),
    (
        "theological",
        "What is one thing you have been carrying lately that you have not yet brought "
        "to me, and what has kept you from bringing it?",
        "Not an accusation. An invitation. Hear the answer without defending.",
    ),
    (
        "fill-in-blank",
        "I think I present myself as very _______ in this marriage, but I am afraid I "
        "am actually a lot more _______ than I would like to admit.",
        "The first blank is what you perform. The second is what is underneath. "
        "Both halves matter; the gap between them is where the real work lives.",
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
        "Pray for each other &mdash; not silently, not generally, but out loud and by "
        "name. One sentence is enough. Pray for the thing they just told you in Round Five.",
        "The closing of the date. Do not skip.",
    ),
]


def _render(text, name_arch, name_amb):
    return text.format(name_arch=name_arch, name_amb=name_amb)


def build(sub_a, sub_b) -> bytes:
    """Generate the Architect+Ambassador couples walkthrough PDF.

    sub_a: the submission of the Architect spouse (primary_mechanism='ARCH')
    sub_b: the submission of the Ambassador spouse (primary_mechanism='AMB')
    """
    ensure_fonts()
    S = make_styles()

    name_arch = _first_name(sub_a, "Architect")
    name_amb = _first_name(sub_b, "Ambassador")

    def R(text):
        return _render(text, name_arch, name_amb)

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Couples Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUPLES WALKTHROUGH",
        cover_right_label=f"{name_arch.upper()}  +  {name_amb.upper()}",
        title=f"Take 139 Couples Walkthrough \u2014 {name_arch} & {name_amb}",
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
    story.append(Paragraph(f"{name_arch} &nbsp;&amp;&nbsp; {name_amb}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_arch.upper()}</b></font><br/>"
                "Architect &middot; Attorney<br/>"
                "<font size=9 color='#6b6862'>Disrespect &middot; Am I protected?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_amb.upper()}</b></font><br/>"
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
        "<i>\u201cLove does not insist on its own way;<br/>"
        "it is not irritable or resentful.\u201d</i><br/>"
        "<font size=9>1 Corinthians 13:5</font>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))

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
            _profile_card(S, name_arch, ACCENT, "Disrespect", "Am I protected?",
                          "The Architect", "The Attorney"),
            "",
            _profile_card(S, name_amb, ACCENT_HER, "Disconnection", "Am I lovable?",
                          "The Ambassador", "The Plea"),
        ]],
        colWidths=[
            (PAGE_W - MARGIN_L - MARGIN_R - 18) / 2.0,
            18,
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
    section_header(story, S, "SECTION THREE  \u00b7  THE AMBASSADOR'S GIFT",
                   f"What {name_amb} gives {name_arch}.",
                   "A room that is warm before he has done anything to earn it.")
    for p in GIFT_TO_ARCH:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4 ──
    section_header(story, S, "SECTION FOUR  \u00b7  THE ARCHITECT'S GIFT",
                   f"What {name_arch} gives {name_amb}.",
                   "A held perimeter. Something Ambassadors rarely build for themselves.")
    for p in GIFT_TO_AMB:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5 ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Protection meets lovability.",
                   "The small repeating rock, named.")
    for p in COLLISION[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The loop, in slow motion.",
                   "And the way out, for each of you in your own grammar.")
    for p in COLLISION[5:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6 ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When the Attorney and the Plea are in the room at once.",
                   "What is happening, and what to do while you can still see it.")
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
    story.append(Paragraph(f"FROM {name_arch.upper()}, TO {name_amb.upper()}",
                            S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name, body in ARCH_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(name, S["H3"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_amb}, to {name_arch}.",
                   f"Three commitments, in her voice, for him to receive.")
    story.append(Paragraph(f"FROM {name_amb.upper()}, TO {name_arch.upper()}",
                            S["CommitLabelHer"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT_HER,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name, body in AMB_COMMITMENTS:
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
                  "Specific praise. The kind that lands because it could not have been said "
                  "by anyone else.")
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
        def __init__(self, mech, name):
            self.primary_mechanism = mech
            self.name = name

    sub_a = FakeSub("ARCH", "Chris")
    sub_b = FakeSub("AMB", "Carolyn")

    pdf_bytes = build(sub_a, sub_b)
    out_path = os.path.join(
        os.path.dirname(__file__),
        "architect_ambassador_test.pdf"
    )
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    import io
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        snippet = ""
        for page in reader.pages[2:5]:
            txt = page.extract_text() or ""
            if txt.strip():
                snippet = txt.strip()[:160]
                break
    except Exception:
        page_count = "unknown"
        snippet = ""

    print(f"DONE: architect_ambassador.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
