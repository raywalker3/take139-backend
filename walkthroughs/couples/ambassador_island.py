"""Couples Walkthrough — Ambassador + Island.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where one spouse is an Ambassador and the
other is an Island. First names are substituted from the submissions:
    {name_amb}  -> the Ambassador spouse's first name
    {name_isle} -> the Island spouse's first name

Pastoral dynamic: one of the more painful pairings because both spouses
are answering questions about whether they are loved/remembered, but with
opposite strategies. The Ambassador resolves the question by giving more;
the Island resolves the question by needing less. Each offers what the
other least needs: the Ambassador floods the Island with care the Island
did not ask for, and the Island withholds the visible appreciation the
Ambassador requires.
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


# ──────────── PROSE — uses {name_amb} and {name_isle} placeholders ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small repeating ones "
    "&mdash; the same disappointment in slightly different clothes, three or four times a week, "
    "year after year, until both people have forgotten what they were originally hoping for.",

    "What follows is a counselor's read of the small repeating rocks in your particular "
    "marriage. Not the dramatic failures, which you would have addressed already. The small "
    "ones. The ones that happen on a Tuesday evening when {name_amb} has quietly prepared "
    "something for {name_isle} and is watching, without knowing she is watching, to see "
    "whether it lands &mdash; and {name_isle} has already moved on, not ungratefully, but "
    "simply because that is how Islands move: forward, alone, efficiently.",

    "You are both reading this because you have decided to look at those rocks. That decision "
    "is more significant than it seems. Most couples spend a lifetime navigating around them "
    "without naming them. Naming them is half the work.",

    "Here is what I want to do for you. I will name what each of you brings the other that "
    "you could not have built alone &mdash; the genuine, theological gift that your two shapes "
    "form together. Then I will name the collision your two questions create, in the specific "
    "way it shows up in your marriage. Then I will name the worst case &mdash; the moment when "
    "{name_amb}'s Plea or Flood and {name_isle}'s Quiet Exit or Ghost are in the room at the "
    "same time &mdash; and what to do then. Then I will hand each of you commitments, not as "
    "rules, but as the kind of small daily practices that, over years, change the temperature "
    "of a home.",

    "Read it together, if you can. If not, read it separately and then sit down with it. "
    "Argue with what does not fit. Stay with what does. The goal is not insight; the goal is "
    "a marriage in which the small repeating rocks become smaller, less repeating, and "
    "eventually a part of the landscape you can both laugh at.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on paper, "
    "side by side. Most couples never see their two profiles next to each other. You are "
    "about to.",
]

TWO_SHAPES_BODY = [
    "{name_amb}, you are an <b>Ambassador</b> whose body reads disconnection as an alarm "
    "and whose deepest question is whether you are lovable. You have learned to manage the "
    "emotional temperature of every room you enter, because warmth, for you, is not merely "
    "kindness &mdash; it is the evidence that the connection is still intact. When the "
    "disconnection becomes undeniable and the giving has produced no visible return, a "
    "<b>Plea</b> or a <b>Flood</b> takes the floor: a bid for acknowledgment that has been "
    "waiting quietly in the wings for longer than either of you realized.",

    "{name_isle}, you are an <b>Island</b> whose body reads disconnection and insignificance "
    "as alarms and whose deepest question is whether you are enough to be remembered. You have "
    "learned to process alone, to need very little from the outside world, and to keep your "
    "interior life well-managed and private. When the wound becomes too large to process alone, "
    "a <b>Quiet Exit</b> or a <b>Ghost</b> takes over &mdash; not in anger but in the Island's "
    "most familiar move: withdrawal to a place where the question cannot be heard.",

    "Notice what these two profiles do <i>not</i> share, and notice what they actually share "
    "underneath. You are not asking the same question. {name_amb} is asking <i>am I "
    "lovable?</i> and {name_isle} is asking <i>am I enough to be remembered?</i> &mdash; "
    "two questions that, in a marriage, are easy to mistake for each other and almost "
    "impossible to answer for each other in the way each of you most needs.",

    "But underneath the two questions is the same root. Both of you have organized your "
    "interior lives around a particular ache: {name_amb} aches to know that love is not "
    "contingent on what she does next, and {name_isle} aches to know that his presence "
    "registers in the people who matter most to him. Both of you, in different costumes, "
    "are standing in the same doorway, asking a version of the same question: "
    "<i>Am I kept?</i>",

    "This is not a coincidence. The Ambassador and the Island are, in one sense, precisely "
    "mismatched &mdash; and in another sense, oddly suited. {name_amb} has warmth she does "
    "not know what to do with; {name_isle} has a soul that wants to be noticed but has never "
    "learned to ask for it. The friction between you is real, but the raw material is "
    "unusually rich. What you are reading is not a diagnosis of failure. It is a map of "
    "what it costs, and what it gives, to love across this particular distance.",
]

GIFT_TO_ISLE = [
    "{name_amb} gives {name_isle} something almost no Island ever receives cleanly: "
    "<b>evidence, without being asked, that he is thought of.</b>",

    "The Island's deepest longing &mdash; to be remembered, to leave a mark in someone's "
    "attention and carry a place in their concern &mdash; is by its nature a longing that "
    "cannot be satisfied by the Island's own efforts. The Island processes alone. The Island "
    "keeps its interior life private. The Island does not petition. And so the Island's "
    "question &mdash; <i>am I enough to be remembered?</i> &mdash; goes unanswered for "
    "years at a time, because the Island has constructed a life in which no one is close "
    "enough to answer it.",

    "{name_amb} breaks through this without quite knowing she is doing it. She notices. "
    "She remembers what {name_isle} mentioned in passing last Tuesday. She asks, in the "
    "middle of an ordinary afternoon, how the thing he said he was thinking about turned "
    "out. She tracks him &mdash; not in the way of a manager, not intrusively, but in "
    "the way of someone who finds another person genuinely interesting and cannot help "
    "demonstrating it. To most people in {name_isle}'s life, this kind of noticing is "
    "rare. To {name_amb}, it is simply how she moves through relationships.",

    "The theological word for what {name_amb} gives {name_isle} is <i>witness</i>. To "
    "be witnessed is to be seen by someone who was paying attention. Isaiah 49:15&ndash;16 "
    "carries God's promise in the same register: <i>I have engraved you on the palms of "
    "my hands.</i> The image is not of a God who is reminded to check on you. It is of a "
    "God who carries you permanently in the place most often visible to him. {name_amb}, "
    "in her native grammar, offers {name_isle} a small, human version of this &mdash; "
    "the knowledge that someone is keeping track of him not because she is obligated to, "
    "but because she wants to.",

    "{name_isle} &mdash; if you want to thank {name_amb} for something this week, thank "
    "her for the specific act of noticing. Name the moment. She may not have realized "
    "what it gave you. She will want to know. Receiving that gratitude is, for the "
    "Ambassador, one of the ways the question <i>am I lovable?</i> gets its best answer.",

    "{name_amb} &mdash; what {name_isle} is receiving from you, in the moments when "
    "you simply remember the detail and follow up, is the nearest thing his interior "
    "life gets to reassurance in the way he most needs it. The thing in you that "
    "naturally tracks people is, for him, a kind of grace.",
]

GIFT_TO_AMB = [
    "{name_isle} gives {name_amb} something Ambassadors rarely receive and rarely "
    "realize they need: <b>a room that does not demand she perform.</b>",

    "The Ambassador moves through most relationships with the same quiet burden: "
    "the need to keep the temperature up, to manage the emotional climate, to give "
    "enough that the connection remains warm and the question <i>am I lovable?</i> "
    "stays quiet. In most rooms, {name_amb} is the one doing this work. The warmth "
    "she extends is real, but it is rarely cost-free. She is, more often than she "
    "admits, watching to see whether the warmth is being returned &mdash; whether "
    "the giving is landing, whether the connection has been confirmed.",

    "{name_isle}, by virtue of being an Island, does not require {name_amb} to "
    "perform. The Island is self-contained. He does not need her to manage the "
    "room. He does not require constant warmth or reassurance. He can be near her "
    "in silence without reading the silence as a relational emergency. For an "
    "Ambassador who spends most of her relational energy in active maintenance, "
    "this is a gift whose value is almost impossible to name. She can, in the "
    "Island's presence, put down the temperature gauge for a little while. No one "
    "is monitoring her output. No one is waiting to feel managed.",

    "The theological word for what {name_isle} gives {name_amb} is <i>rest</i>. "
    "Not laziness &mdash; sabbath. Keller, in <i>The Meaning of Marriage</i>, "
    "notes that one of the things a good marriage offers is the relief of being "
    "fully known and not abandoned: the discovery that someone has seen the thing "
    "underneath the performance and stayed. {name_isle}'s self-containment, which "
    "in other contexts might feel like withholding, is for {name_amb} a kind of "
    "proof: he is not here for the performance. He is here for her.",

    "{name_amb} &mdash; if you want to thank {name_isle} for something this week, "
    "thank him for this. Name a specific moment when you felt the relief of not "
    "having to manage anything. He may not know he was giving it. Tell him. The "
    "Island rarely believes that his self-containment is a gift &mdash; he has "
    "more often been told it is a problem.",

    "{name_isle} &mdash; what {name_amb} is receiving from you, in the moments "
    "when you simply let her be without requiring anything of her, is the closest "
    "thing she gets to the restedness that the gospel promises. The thing in you "
    "that you have sometimes been told is too closed, too private, too self-sufficient, "
    "is for her a room she can exhale in.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you, "
    "even if you have not named it in quite these terms.",

    "{name_amb}'s core question is <i>am I lovable?</i> {name_isle}'s is <i>am I "
    "enough to be remembered?</i> These two questions, on paper, might seem to want "
    "the same thing: acknowledgment, warmth, the felt sense of being held in someone's "
    "regard. In the daily mechanics of a marriage, they ask for this through strategies "
    "that are almost exactly opposite each other &mdash; and the strategies, run in "
    "parallel, produce a pattern both of you have felt but neither of you has quite "
    "been able to name.",

    "{name_amb} resolves her question by giving more. When the warmth in the room "
    "drops, or when she cannot read whether the connection is still intact, she turns "
    "up the giving &mdash; the act of service, the follow-up question, the small "
    "gesture of care that is, in the Ambassador's grammar, the only proof of love "
    "she knows how to make. The giving is not calculated. It is almost reflexive. "
    "And underneath it is a watching: <i>did it land? Was it received? Does the "
    "temperature confirm that I am still wanted?</i>",

    "{name_isle} resolves his question by needing less. When the significance "
    "question surfaces &mdash; when he wonders whether he registers, whether his "
    "presence matters, whether he would be missed &mdash; he does not reach outward. "
    "He reaches inward. He contains. He processes. He becomes more self-sufficient, "
    "because self-sufficiency is the Island's dignity: the refusal to spill into "
    "rooms that have not explicitly asked for him. The Island's strategy and the "
    "Ambassador's strategy are moving in opposite directions at precisely the same "
    "moment.",

    "Paul, writing to the Romans, says: <i>Outdo one another in showing honor.</i> "
    "(Romans 12:10) This is often read as a competition of service, but notice what "
    "it actually describes: a marriage in which both partners are actively looking "
    "for ways to confer dignity on the other. It is not a competition of who gives "
    "more. It is a discipline of receiving what is given and noticing what is "
    "offered. The Ambassador and the Island are, in their best seasons, capable "
    "of this. The collision happens when neither of them is quite reaching the "
    "other's frequency.",

    "Here is the collision in slow motion. {name_amb}, in trying to confirm the "
    "connection on a Tuesday evening, gives. She makes the room warm. She asks "
    "the follow-up question. She brings something small and specific that she "
    "remembered because she has been paying attention. And then she watches. Not "
    "consciously, not with a ledger open, but the watching is there: "
    "<i>is this landing? Is he receiving it?</i> {name_isle}, who is genuinely "
    "moved by the gesture and who registers that he has been thought of, responds "
    "in the only way the Island knows how to respond: by moving forward. He says "
    "thank you. He continues with what he was doing. He does not understand that "
    "the thank you needed to linger.",

    "{name_amb} does not experience this as cruelty. She experiences it as "
    "invisibility. The giving went out and the response came back in the wrong "
    "currency &mdash; correct but brief, appreciated but not received in the way "
    "that would quiet the question. Her trigger fires: <i>disconnection.</i> The "
    "old question wakes: <i>am I lovable, or merely useful?</i> Her response is "
    "to give again, perhaps more, perhaps with a slightly different quality of "
    "attention that she hopes will produce a warmer acknowledgment.",

    "{name_isle}, for his part, does not experience the additional warmth as "
    "love. He experiences it as a pressure he has not asked for. The Island does "
    "not require constant tending. He was fine. He was, in his own way, feeling "
    "good about the evening. And now there is a quality of watchfulness in the "
    "room that he cannot name but that feels &mdash; to a soul that has spent a "
    "lifetime guarding its perimeter &mdash; faintly like surveillance. He "
    "withdraws. Not to punish. Simply because withdrawal is what the Island does "
    "when the air around him becomes too thick. His trigger fires: "
    "<i>significance.</i> The old question surfaces: <i>am I enough on my own, "
    "or do I have to perform warmth on demand to be acceptable here?</i>",

    "Paul's words to the Ephesians name what both of you are reaching for and "
    "failing to give each other: <i>submitting to one another out of reverence "
    "for Christ.</i> (Ephesians 5:21) Submission, here, is not a hierarchy. It "
    "is a posture: the willingness to let the other person's need shape your "
    "response before your own mechanism does. {name_amb}, the Island does not "
    "experience warmth the same way you generate it. The submission required "
    "of you is to receive less return than you would like, without reading it "
    "as rejection. {name_isle}, the Ambassador does not experience acknowledgment "
    "the same way you give it. The submission required of you is to linger, "
    "briefly and specifically, with what has been given &mdash; not because "
    "it feels necessary to you, but because it is the currency in which the "
    "person you love is listening.",

    "{name_amb}, when {name_isle} thanks you briefly and moves on, the translation "
    "is almost never <i>he does not care what I gave.</i> Nine times out of ten, "
    "the translation is <i>he received it in his own language and does not know "
    "yours requires a longer reception.</i> Tell him, once, in one sentence: "
    "<i>I need you to stay with that for a moment &mdash; tell me what it gave "
    "you.</i> He can do this. He does not know you need it unless you say so.",

    "{name_isle}, when {name_amb}'s warmth begins to feel like a quiet audit "
    "&mdash; when the giving seems to carry a weight of watching &mdash; the "
    "translation is almost never <i>she is smothering me.</i> Nine times out "
    "of ten, the translation is <i>she is trying to confirm that the love "
    "she is giving is landing, and she has no other way to check.</i> Give her "
    "the confirmation in words. Not because you owe it. Because it is the "
    "specific gift she is waiting for, and you are one of very few people in "
    "a position to give it.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be seasons &mdash; not every week, but they "
    "will come &mdash; when the small collision in the kitchen escalates, or when a "
    "longer accumulation of smaller disappointments has built to a point where both "
    "of you are in breakdown at the same time. And when that happens, this particular "
    "pairing develops a pattern that is among the most painful in the six mechanisms: "
    "one spouse pursuing harder while the other retreats further.",

    "Here is what is happening, named plainly so you can both see it.",

    "{name_amb}, when the Plea is rising &mdash; or when the Flood finally breaks "
    "what the Ambassador has been quietly containing &mdash; you are not, in that "
    "moment, making a calculated demand. You are releasing an accumulated weight that "
    "you did not know you were carrying. The giving has been real. The service has "
    "been real. The watching to see whether it landed has been continuous and mostly "
    "silent. And now, in a moment when the question cannot be held any longer, the "
    "evidence surfaces: <i>I have given this much, and I do not know whether any "
    "of it has mattered to you.</i> It is not a prosecution. It is grief that has "
    "run out of room. But to {name_isle}, who did not know the ledger existed, it "
    "lands as an accusation.",

    "{name_isle}, when the Quiet Exit is gathering &mdash; or when the Ghost has "
    "already pulled away &mdash; you are not, in that moment, trying to punish "
    "{name_amb}. You are doing the only thing the Island has ever known how to do "
    "with pain that has become too large: you are containing it, processing it "
    "alone, retreating to the interior where the question cannot be overheard. "
    "But to {name_amb}, whose trigger is disconnection, whose whole nervous system "
    "reads withdrawal as verdict, the retreat does not read as <i>he needs space.</i> "
    "It reads as <i>I have lost him.</i> The Plea rises. The Flood rises. The "
    "Ambassador pursues. And the harder {name_amb} pursues, the further {name_isle} "
    "retreats. The further {name_isle} retreats, the more desperate {name_amb} "
    "becomes. The loop is fast and almost never about what started it.",

    "Hosea 11:1&ndash;4 gives us a picture that belongs to this moment. God speaks "
    "of a child he taught to walk, a child he led with cords of kindness, a child "
    "he lifted to his cheek and fed. The child has wandered. God does not pursue "
    "with fury. He pursues with <i>tender love</i> &mdash; and in the tenderness "
    "is the acknowledgment that even the wandering is understood. Both of you, in "
    "breakdown, are versions of this child. {name_amb} is reaching for something "
    "she needs and cannot name cleanly. {name_isle} is retreating to the only "
    "place that has ever felt safe. Neither of them is the villain. The villain "
    "is the loop itself.",

    "John writes the sentence that names the only exit: <i>We love because he "
    "first loved us.</i> (1 John 4:19) The Ambassador cannot give freely as long "
    "as she is giving in order to discover whether she is lovable. The Island "
    "cannot receive freely as long as he believes that showing need will cost him "
    "something essential. Both of you need to receive before you can give well. "
    "Keller, in <i>The Meaning of Marriage</i>, names this plainly: the marriage "
    "cannot sustain itself on what two people generate from their own reserves. "
    "Each partner must learn to receive love &mdash; from God, and from the other "
    "&mdash; before the giving can come from a place that does not exhaust itself. "
    "The pursuit-retreat loop is what happens when both partners are trying to "
    "give from empty.",

    "What to do, when you can both still see what is happening:",

    "<b>One of you, not both, calls the halt.</b> Whichever of you notices first "
    "that the loop has started says, out loud: <i>this is the loop. Twenty "
    "minutes.</i> No discussion of who is right. No final word. The halt is not "
    "a surrender; it is the refusal to let the mechanism run the room. {name_isle}, "
    "the halt is your gift to give here &mdash; you can see the pattern faster "
    "than {name_amb} can when the Plea is rising. Name it. She will receive it, "
    "even if it takes a moment.",

    "<b>In the twenty minutes, do not rehearse. Pray.</b> {name_amb}, pray for "
    "{name_isle} by name &mdash; not for him to be different, but for him to "
    "know, in the retreat, that he is held by a God whose memory of him is "
    "perfect and permanent. {name_isle}, pray for {name_amb} by name &mdash; "
    "not for her to need less, but for her to receive the assurance she is "
    "reaching for from the One who can actually give it without running dry.",

    "<b>When you come back, one sentence each, spoken slowly.</b> {name_amb}, "
    "your sentence is not the ledger. It is the single weight under all the "
    "others: <i>I felt invisible when you moved on, and I needed you to know "
    "what that gave me.</i> {name_isle}, your sentence is not a defense. It is "
    "one honest thing: <i>I did not know you needed me to stay with it longer, "
    "and I am sorry I moved on before you were ready.</i> Both of you can say "
    "one sentence. Both of you stop after one sentence.",

    "<b>If the loop runs anyway, name it together the next day.</b> Not to "
    "relitigate &mdash; to name it as a pattern that belongs to both of you, "
    "that neither of you alone caused, and that both of you are committed to "
    "outgrowing. The Plea and the Quiet Exit have been working long shifts. "
    "They will retire slowly. The marriage that knows this can be patient "
    "with the slow retirement.",

    "And hear this clearly, both of you. <b>Neither of you is the problem.</b> "
    "The Plea is not the truest thing about {name_amb}. The Quiet Exit is not "
    "the truest thing about {name_isle}. They are old mechanisms doing the only "
    "job they were ever taught to do. The truest thing about both of you is "
    "that you chose each other &mdash; and that in the ordinary Tuesday of a "
    "long marriage, you are learning, slowly and not always gracefully, to "
    "receive a love from each other that neither of you fully knew how to "
    "trust before.",
]

COMMITMENTS_INTRO = [
    "What follows are six commitments &mdash; three from {name_amb}, three from "
    "{name_isle}. They are not vows in the legal sense. They are the small daily "
    "practices that, offered to each other freely, change the temperature of a home "
    "over months and years. Read each one slowly. If one of you cannot say a "
    "particular commitment in good faith yet, do not say it. The goal is not "
    "performance; it is honesty.",
]

AMB_COMMITMENTS = [
    (
        "To let you have the quiet.",
        "{name_isle}, I commit to letting you have a quiet day &mdash; or a quiet "
        "evening, or a quiet hour &mdash; without reading it as withdrawal from me. "
        "I know that your silence is not a verdict. I know it is the way you process "
        "and the way you rest. I will not always succeed at this. But I commit to "
        "pausing, in the moment when the silence triggers my question, and asking "
        "myself: <i>is he retreating, or is he simply being the Island he has "
        "always been?</i> More often than I expect, the answer will be the second "
        "one. And when I can receive the quiet without reading it as loss, I will "
        "have given you one of the most important gifts I know how to give.",
    ),
    (
        "To name the weight before it becomes a flood.",
        "{name_isle}, when something I give goes unacknowledged and the old question "
        "wakes up &mdash; <i>did it matter? Does he notice?</i> &mdash; I commit to "
        "naming it to you in one sentence on the same day it happens, rather than "
        "carrying it quietly until the weight becomes too heavy to hold. Not a brief. "
        "Not the full ledger. One sentence: <i>I gave you something today and I "
        "needed to know it landed.</i> You can answer that. I will give you the "
        "chance to answer it, rather than waiting for a moment when you have no "
        "idea anything was being kept.",
    ),
    (
        "To receive from you, not only give.",
        "{name_isle}, I commit to practicing the thing the Ambassador is worst at: "
        "receiving. When you give me something &mdash; a word, a piece of attention, "
        "a moment of noticing &mdash; I will stay with it. I will not deflect it back "
        "to you. I will not immediately ask how you are. I will let it land. And I "
        "will tell you, in words, what it gave me &mdash; because you receiving my "
        "giving with warmth teaches me that I do not have to earn my place here, "
        "and because you deserve to know that what you give, when you give it, "
        "actually reaches me.",
    ),
]

ISLE_COMMITMENTS = [
    (
        "To tell you what you have given me, in words.",
        "{name_amb}, I commit to telling you what you have given me &mdash; in words, "
        "said out loud, not assumed to be obvious. I know that I receive what you give. "
        "I know that it matters to me. What I have not always understood is that the "
        "receiving needs to be demonstrated, specifically and verbally, in the currency "
        "you are actually listening in. This week, and every week, I will tell you one "
        "specific thing you gave me and what it meant. Not because it is natural to me. "
        "Because you are waiting for it, and you have been waiting longer than I knew, "
        "and you deserve to hear it.",
    ),
    (
        "To show you that I have thought of you.",
        "{name_amb}, I commit to finding, at least once each week, a specific way to "
        "demonstrate that I have been thinking about you when you were not in the room. "
        "A detail I remembered. A question about something you mentioned. A small act "
        "that requires me to have paid attention. I know that this is what your question "
        "is listening for &mdash; not declarations, but evidence. I will give you the "
        "evidence. And in doing so I will be answering, in the language you can actually "
        "receive, the question you have been asking for a very long time.",
    ),
    (
        "To come back before the exit is complete.",
        "{name_amb}, when I feel the Island pulling me inward &mdash; when the room "
        "feels too thick and the withdrawal is beginning &mdash; I commit to telling "
        "you, in one sentence, what is happening before the exit is complete: <i>I "
        "need twenty minutes alone and then I will come back to you.</i> Not silence. "
        "Not disappearance. A sentence, and a promise, and a return. Because I know "
        "that my silence lands on you as disconnection, and I do not want to give "
        "you disconnection when what I actually need is only a brief pause. The Island "
        "can have his interior life. He can also learn to leave a note on the door.",
    ),
]

PRAYER = [
    "Father,",

    "You placed {name_amb} and {name_isle} next to each other, and you knew exactly "
    "what you were doing. You knew the Ambassador would carry the question <i>am I "
    "lovable?</i> into every room she entered, and that she would answer it by giving "
    "until the giving ran dry. You knew the Island would carry the question <i>am I "
    "enough to be remembered?</i> and that he would answer it by needing so little "
    "that no one would know how much he still needed. You knew all of it before "
    "either of them said yes.",

    "Teach them the grammar of each other. Teach {name_amb} to read {name_isle}'s "
    "quiet, not as a verdict on her lovability, but as a soul that is simply being "
    "the Island he has always been &mdash; present, internal, and in his own way, "
    "keeping track. Teach {name_isle} to read {name_amb}'s warmth, not as a demand "
    "to be performed, but as a soul that is asking, in the only language it knows, "
    "whether the connection is still intact. Teach each of them to linger, briefly "
    "and specifically, in the currency the other is listening in.",

    "You are, for {name_amb}, the Bridegroom whose love does not fluctuate with her "
    "output &mdash; the One who loved his bride before she was lovely, and who is "
    "not one degree warmer toward her because of what she gave this week. You are, "
    "for {name_isle}, the One who has engraved him on the palms of your hands "
    "&mdash; who does not need to be reminded of him, who carries him permanently "
    "in the place most often in your sight. Teach them each to receive the answer "
    "you have already spoken before they reach again for the question.",

    "When the Plea rises in {name_amb}, remind her that she is loved &mdash; not "
    "because she has given enough, but because you gave yourself for her, "
    "completely and without condition, before she gave anything at all. When "
    "the Quiet Exit gathers in {name_isle}, remind him that he is remembered "
    "&mdash; written, kept, thought of by the One whose thought of him does "
    "not lapse in the night.",

    "Make their home a room in which neither of them has to earn their place. "
    "Make their table a place where the small weights are named on the day they "
    "happen. Make their silences a place of rest, not retreat. And when they are "
    "old and the children are grown and the question has finally quieted, let "
    "them look back and see that what they built together &mdash; across the "
    "distance between giving and needing &mdash; was something neither of them "
    "could have built alone.",

    "In the name of the One who loved his bride before she was lovely, and who "
    "is, even now, preparing the home in which they will live with him forever.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages "
    "that follow are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, "
    "somewhere quiet, with no children in the room and no phones on the table. "
    "There are six rounds, and they build on each other. Resist the temptation "
    "to skip ahead. Start at Round One even if it feels too light; the lightness "
    "is the point.",

    "Some of the questions are playful. Some are direct. A few are the kind of "
    "questions that, when answered honestly, will sit with you for a week. "
    "None of them are trivia. All of them are an invitation.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did "
    "not read answers first, in full, without interruption. Then the reader "
    "answers the same question. Then you move on. You do not have to finish all "
    "six rounds in one night &mdash; in fact, two or three rounds taken seriously "
    "is often better than racing through all of them. Save the rest for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. You may not love "
    "everything you hear. Stay with it. The point of this is not to grade each "
    "other's answers. The point is to be known, and to do the work of knowing.",
]

ROUND_1 = [
    (
        "hypothetical",
        "If our marriage were a weather system, what would it be right now &mdash; "
        "and what kind of weather would you most want us to grow into?",
        "Let the metaphor do the work. Islands are often more comfortable with "
        "abstract images than direct declarations. Ambassadors often find that "
        "the image says what the sentence cannot.",
    ),
    (
        "observation",
        "What is something I did this week that you noticed and didn't mention?",
        "Not a complaint. A small noticing. The fact that you noticed at all is "
        "the gift &mdash; and for the Ambassador, being told she was noticed is "
        "one of the most important things this evening can offer.",
    ),
    (
        "playful",
        "If you had to describe this marriage as a book genre, what would it be "
        "&mdash; and what would the title be?",
        "Yes, really. First thing that comes to mind. You can revise it after "
        "you explain it.",
    ),
]

ROUND_2 = [
    (
        "fill-in-blank",
        "I don't think I tell you this enough &mdash; I am amazed at the way "
        "God made you so _______. Your _______ is a gift to our marriage, and "
        "I want to get better at receiving it.",
        "Two blanks. Be specific. 'Warm' is too easy; 'able to make a stranger "
        "feel found in the first five minutes of a conversation' is closer. "
        "'Thoughtful' is too easy; 'the way you work through something for three "
        "days in silence and then say the most precise thing' is closer.",
    ),
    (
        "observation",
        "What is one thing you've watched me do this year that you wish more "
        "people got to see?",
        "Most of us only see ourselves do our most public things. Tell your "
        "spouse about the private ones. The Ambassador often does her best "
        "work where no one is watching; the Island does his best thinking "
        "where no one can interrupt.",
    ),
    (
        "one-word",
        "If you had to choose one word to describe what it feels like when I "
        "walk into the room after a long day apart, what word would it be?",
        "One word, said out loud. Then take one minute to explain it. {name_isle}, "
        "this is one of the questions the Ambassador has been waiting to hear you "
        "answer. Say it slowly.",
    ),
]

ROUND_3 = [
    (
        "forward-looking",
        "Five years from now, when we look back on this season of our marriage, "
        "what do you hope we will say we did well together?",
        "Not what you wish you had done. What you want, when you look back, "
        "to be able to say you did.",
    ),
    (
        "theological",
        "Where, in the last month, have you seen God specifically at work in me?",
        "Not where you want him to work. Where you have already seen it. "
        "Name the specific moment. Both the Ambassador and the Island need "
        "to hear this answered by name.",
    ),
    (
        "shared-identity",
        "Finish this sentence three times: 'We are the kind of couple who _______.' "
        "Give one playful answer, one true answer, and one aspirational answer.",
        "The 'we' is the point. This is not about what each of you is separately. "
        "It is about what only exists because the two of you chose each other.",
    ),
]

ROUND_4 = [
    (
        "strength",
        "What is something I do for you that you would have to learn to do for "
        "yourself if I weren't here?",
        "Hard to ask. Important to hear. Stay with the answer for a moment before "
        "you respond. {name_amb}, this question was written partly for you to hear "
        "answered. {name_isle} may surprise you.",
    ),
    (
        "fill-in-blank",
        "One of the gifts of being married to you is that I get to be _______ "
        "in ways I never would have been on my own.",
        "A version of yourself that only exists because this marriage exists. "
        "Name it. Be specific enough that the other person could not have "
        "said it about someone else.",
    ),
    (
        "observation",
        "Name one moment in our story so far where you knew, with no doubt, that "
        "we had built something together that neither of us could have built alone.",
        "Tell the story in full. The remembering is part of the strengthening.",
    ),
]

ROUND_5 = [
    (
        "hard",
        "When you see me in breakdown &mdash; when the Plea is rising or the "
        "Flood is up, or when the Island is going quiet and the exit is "
        "gathering &mdash; what is one thing you wish I would say or do "
        "differently, not later, but in the moment?",
        "You both know what these look like now. Ask each other for what "
        "would actually help. Not the polished answer &mdash; the real one.",
    ),
    (
        "profile-aware",
        "{name_amb}, when you have given something and it has gone by too "
        "quickly, what do you most need from {name_isle} in that moment &mdash; "
        "and {name_isle}, when the room starts to feel too thick and the "
        "withdrawal begins, what is the one thing {name_amb} could say that "
        "would make it easier to stay?",
        "Name the real thing. The Ambassador often needs to hear her name "
        "and one specific word. The Island often needs one sentence of "
        "permission: <i>take the time you need. I will be here.</i>",
    ),
    (
        "theological",
        "What is one thing you have been carrying lately that you have not "
        "yet brought to me, and what has kept you from bringing it?",
        "Not an accusation. An invitation. Hear the answer without defending.",
    ),
]

ROUND_6 = [
    (
        "blessing",
        "Place your hand on your spouse's hand. Say their name. Then say: "
        "'You are not a problem to be solved. You are a gift I get to receive "
        "again tomorrow.' Say it slowly. Let them say it back.",
        "You may feel silly. That is part of why it works. {name_amb}: let "
        "yourself receive this without deflecting it. {name_isle}: say it "
        "slowly enough that it lands.",
    ),
    (
        "prayer",
        "Pray for each other &mdash; not silently, not generally, but out "
        "loud and by name. One sentence is enough. Pray for the thing they "
        "just told you in Round Five.",
        "The closing of the date. Do not skip.",
    ),
]


def _render(text, name_amb, name_isle):
    return text.format(name_amb=name_amb, name_isle=name_isle)


def build(sub_a, sub_b) -> bytes:
    """Generate the Ambassador+Island couples walkthrough PDF.

    sub_a: the submission of the Ambassador spouse (primary_mechanism='AMB')
    sub_b: the submission of the Island spouse (primary_mechanism='ISLE')
    """
    ensure_fonts()
    S = make_styles()

    name_amb = _first_name(sub_a, "Ambassador")
    name_isle = _first_name(sub_b, "Island")

    def R(text):
        return _render(text, name_amb, name_isle)

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Couples Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUPLES WALKTHROUGH",
        cover_right_label=f"{name_amb.upper()}  +  {name_isle.upper()}",
        title=f"Take 139 Couples Walkthrough \u2014 {name_amb} & {name_isle}",
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
    story.append(Paragraph(f"{name_amb} &nbsp;&amp;&nbsp; {name_isle}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_amb.upper()}</b></font><br/>"
                "Ambassador &middot; Plea / Flood<br/>"
                "<font size=9 color='#6b6862'>Disconnection &middot; Am I lovable?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#5e5c72'><b>{name_isle.upper()}</b></font><br/>"
                "Island &middot; Quiet Exit / Ghost<br/>"
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
        "<i>\u201cWe love because he first loved us.\u201d</i><br/>"
        "<font size=9>1 John 4:19</font>",
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
            _profile_card(S, name_amb, ACCENT, "Disconnection", "Am I lovable?",
                          "The Ambassador", "The Plea / Flood"),
            "",
            _profile_card(S, name_isle, ACCENT_HER,
                          "Disconnection / Significance",
                          "Am I enough to be remembered?",
                          "The Island", "The Quiet Exit / Ghost"),
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

    # ── SECTION 3 ── Ambassador's Gift to Island
    section_header(story, S, "SECTION THREE  \u00b7  THE AMBASSADOR'S GIFT",
                   f"What {name_amb} gives {name_isle}.",
                   "Evidence, without being asked, that he is thought of.")
    for p in GIFT_TO_ISLE:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4 ── Island's Gift to Ambassador
    section_header(story, S, "SECTION FOUR  \u00b7  THE ISLAND'S GIFT",
                   f"What {name_isle} gives {name_amb}.",
                   "A room that does not demand she perform.")
    for p in GIFT_TO_AMB:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5 ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Giving more meets needing less.",
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
                   "When the pursuit and the retreat are both running.",
                   "What is happening, and what to do while you can still see it.")
    for p in BOTH_BREAK[:6]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do, while you can still see it.",
                   "Four practices for the loop, in order.")
    for p in BOTH_BREAK[6:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 7 ──
    section_header(story, S, "SECTION SEVEN  \u00b7  COMMITMENTS",
                   "Six small daily practices.",
                   "Three from each of you. Read each one slowly.")
    for p in COMMITMENTS_INTRO:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"FROM {name_amb.upper()}, TO {name_isle.upper()}",
                            S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name, body in AMB_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(name, S["H3"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_isle}, to {name_amb}.",
                   "Three commitments, in his voice, for her to receive.")
    story.append(Paragraph(f"FROM {name_isle.upper()}, TO {name_amb.upper()}",
                            S["CommitLabelHer"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT_HER,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name, body in ISLE_COMMITMENTS:
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

    sub_a = FakeSub("AMB", "Sarah")
    sub_b = FakeSub("ISLE", "Daniel")

    pdf_bytes = build(sub_a, sub_b)
    out_path = os.path.join(
        os.path.dirname(__file__),
        "ambassador_island_test.pdf"
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
        for page in reader.pages[4:8]:
            txt = page.extract_text() or ""
            if txt.strip():
                snippet = txt.strip()[:200]
                break
    except Exception:
        page_count = "unknown"
        snippet = ""

    print(f"DONE: ambassador_island.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
