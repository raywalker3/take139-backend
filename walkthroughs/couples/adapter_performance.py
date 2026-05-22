"""Couples Walkthrough — Adapter + Performance Campaign.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where Spouse A is an Adapter and
Spouse B is a Performance Campaign. First names are substituted from the submissions:
    {name_a}  -> the Adapter spouse's first name
    {name_b}  -> the Performance Campaign spouse's first name

Adapter:              trigger Control; core question "Am I free?"
Performance Campaign: trigger Significance; core question "Am I enough to be remembered?"

Key pastoral dynamic: This pairing is unusually high-functioning in the marketplace.
Both spouses are gifted at presenting calibrated public selves. The Adapter takes the
SHAPE of what the room needs; the Performance produces what the room CELEBRATES.
Together they are formidable — and together they are at risk of a closed loop in which
mutual production-and-reception never delivers either spouse's deepest need.
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


# ──────────── PROSE — uses {name_a} and {name_b} placeholders ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small repeating ones "
    "\u2014 the same moment in slightly different clothes, three or four times a week, "
    "year after year, until both people have slowly forgotten what they were originally "
    "hoping for when they chose each other.",

    "What follows is a counselor's read of the small repeating rocks in your particular "
    "marriage. You are, as a pair, unusually gifted at the social world. People who know "
    "you together probably describe you in words like <i>impressive</i> or <i>capable</i> "
    "or <i>they just seem to work.</i> And in many respects, they are right. You do work. "
    "You have built something real together, and the building has been more than performance.",

    "But something underneath the public fluency is not yet at rest, and this document is "
    "about that something. {name_a} has spent a lifetime reading rooms and becoming what "
    "they needed. {name_b} has spent a lifetime producing what rooms celebrate. Both of "
    "you, in different grammars, have learned that the way to stay safe in the world is "
    "to be responsive to what the world signals. The question this document asks is "
    "whether your home \u2014 the one room neither of you can leave \u2014 has become "
    "another room you are performing for, or whether it has become something rarer: "
    "the room where neither of you has to.",

    "Here is what I want to do for you. I will name what each of you brings the other "
    "that you could not have built alone \u2014 the genuine gift your two shapes form "
    "together. Then I will name the collision your two questions create, in the specific "
    "way it shows up in a marriage like yours. Then I will name the worst case \u2014 "
    "the moment when both of your breakdowns are running simultaneously \u2014 and what "
    "to do while you can still see it. Then I will hand each of you specific commitments, "
    "not as rules, but as the small daily practices that, offered to each other freely, "
    "change the temperature of a home.",

    "Read it together if you can. Argue with what does not fit. Stay with what does. "
    "The goal is not insight for its own sake. The goal is a marriage in which the "
    "performance slowly gives way to something more costly and more durable: "
    "the presence of two people who are genuinely known, and who have decided "
    "that being known is worth the exposure.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, "
    "on paper, side by side. Most couples never see their two profiles next to each "
    "other. You are about to.",
]

TWO_SHAPES_BODY = [
    "{name_a}, you are an <b>Adapter</b> whose body reads control as an alarm and whose "
    "deepest question is whether you are free. Not free in the political sense \u2014 free "
    "in a more frightening and personal sense: free to be a self that is not simply a "
    "reflection of what the room needs. You have moved through the world with extraordinary "
    "fluency, becoming what every room required, and underneath that fluency is a question "
    "that has been there since you were very young: <i>Is there a me here, underneath "
    "all the versions? And if I stopped becoming what people needed, would anyone stay?</i>",

    "{name_b}, you are a <b>Performance Campaign</b> whose body reads insignificance as "
    "an alarm and whose deepest question is whether you are enough to be remembered. "
    "You discovered early that ordinary was forgettable, and forgettable in the world "
    "you grew up in was not safe. So you ran. You built. You produced things with "
    "genuine excellence and genuine craft, and underneath each achievement, the question "
    "came back: <i>Is this enough? Will you remember me when the campaign goes quiet? "
    "Am I enough even when I am not producing?</i>",

    "Notice what these two profiles share at the surface, and notice what they "
    "do not share underneath. From the outside, you look like the same kind of person: "
    "high-functioning, socially capable, fluent in the registers the world rewards. "
    "But the question driving each of you is different. {name_a}'s question is about "
    "freedom \u2014 about the existence of a self that does not have to be earned "
    "in every room. {name_b}'s question is about significance \u2014 about whether "
    "the self that exists has done enough to merit being kept.",

    "Underneath both questions, though, is something they share. Both of you have "
    "built your sense of self on responsiveness to external signal \u2014 {name_a} "
    "responsive to relational cues, {name_b} responsive to achievement cues. Neither "
    "of you, in the honest interior, has a self that operates with full confidence "
    "outside of a feedback loop. This is the deep commonality, and it is the reason "
    "your marriage can feel both unusually productive and unusually hollow at the same time.",

    "You are not each other's problem. You are each other's mirror. And what you are "
    "about to read is an account of what happens when two people whose identities are "
    "built on responsiveness to the world try to give each other what they most need \u2014 "
    "and keep discovering, to their mutual bewilderment, that the mechanism they have "
    "relied on for everything else does not quite reach.",
]

GIFT_TO_A = [
    "{name_b} gives {name_a} something the Adapter rarely receives: <b>a room that "
    "notices when she walks into it.</b>",

    "The Adapter's deepest unspoken fear is invisibility \u2014 not the ordinary "
    "invisibility of being ignored, but the subtler invisibility of a self that has "
    "been so consistently adaptive that no one knows which version is the real one, "
    "or whether there is a real one. The rooms {name_a} walks through are full of "
    "people she has served by becoming what they needed. Very few of those people "
    "have turned around and said: <i>I see you. Not the version of you I needed. You.</i>",

    "{name_b}, by virtue of being a Performance Campaign, is one of the most intensely "
    "attentive people in any room. The Campaign does not miss much. It has spent years "
    "developing the skill of reading what the room will notice, and that skill, turned "
    "toward {name_a}, means that {name_b} often sees {name_a} more clearly than almost "
    "anyone else in her life. The Campaign's attentiveness is, at its best, a form of "
    "witness \u2014 someone who has watched you carefully and can tell you what "
    "they actually saw.",

    "There is a theological word for what {name_b} gives {name_a} at his best, and it "
    "is the word the Psalms use more than almost any other: <i>known.</i> Psalm 139 "
    "opens with it: <i>O Lord, you have searched me and known me. You know when I sit "
    "down and when I rise up.</i> The Adapter's deepest longing is to be known before "
    "she performs \u2014 to have someone see the person underneath the calibrations. "
    "{name_b}'s gift, when he is not running the Campaign on their behalf, is to be "
    "that witness. He has watched her long enough to see past the versions.",

    "{name_a} \u2014 if you want to thank {name_b} for something this week, thank him "
    "for the specific moments he has noticed you rather than your performance. The "
    "Campaign is hard to live with in many ways, but the Campaign is genuinely good "
    "at noticing what is real. Tell him what it has meant to be seen by someone "
    "who pays that kind of attention. He will be surprised; the Campaign rarely thinks "
    "of its attentiveness as a gift. Say it anyway.",

    "{name_b} \u2014 what you are giving {name_a} in those moments of clear-eyed "
    "witness is something she cannot give herself. The Adapter has a harder time "
    "seeing herself than almost anyone else she knows, because the version she is "
    "currently inhabiting is the one she assembled for the room she is in. You are "
    "one of the few people in her life who has stood in enough rooms with her to "
    "see the person who shows up in all of them. That is not a small thing. "
    "It is one of the great gifts a marriage can hold.",
]

GIFT_TO_B = [
    "{name_a} gives {name_b} something Performance Campaigns almost never receive "
    "without earning it: <b>unconditional reception.</b>",

    "The Campaign has spent years producing for rooms that respond when the output "
    "is excellent and go quiet when it is not. {name_b} has learned, through long "
    "experience, that presence in a room must be justified by what one contributes "
    "to it. Love, in the grammar the Campaign has been working with, is a response "
    "to demonstrated worth. Which means the Campaign has almost never simply rested "
    "in a room where it was loved regardless of what it was producing.",

    "{name_a}, by virtue of being an Adapter, has one of the rarest gifts in human "
    "relationships: the capacity to give a person the version of reception they most "
    "need. The Adapter reads what a room requires and provides it. When what the "
    "room requires is not applause but simple, unreserved warmth \u2014 when what "
    "{name_b} needs is not an audience but a witness who stays even when the campaign "
    "has nothing to show \u2014 {name_a}'s attunement is the thing that gives it. "
    "She can be present to {name_b} in a way that does not require him to be "
    "producing in order to justify her presence.",

    "The theological word for this is <i>grace</i>. Not grace in the watered-down "
    "contemporary sense of being easy to get along with, but grace in the Pauline "
    "sense: reception that precedes performance. <i>God shows his love for us in "
    "that while we were still sinners, Christ died for us.</i> (Romans 5:8) The "
    "Adapter's unconditional reception, at its best, is a small earthly echo of "
    "that grammar: you are received before you have produced anything, and you will "
    "continue to be received when the production stops.",

    "{name_b} \u2014 if you want to thank {name_a} for something this week, thank "
    "her for the times she has stayed with you when you were not running. The times "
    "she sat with you when you had nothing to show, when the campaign was quiet, when "
    "you felt the anxiety of an unproductive afternoon and she did not treat it as "
    "evidence of your diminishment. Tell her that her presence in those moments is "
    "worth more than most of the audience responses you have spent years pursuing. "
    "She may not know what to do with the compliment. Say it anyway.",

    "{name_a} \u2014 what {name_b} receives from you, in the moments when you are "
    "simply present without agenda, is a kind of rest the Campaign has rarely been "
    "permitted. The thing in you that reads what people need and gives it freely "
    "is, for him, something closer to home than almost anything else he has "
    "experienced in the social world. That is not nothing. It is one of the ways "
    "you love him that is genuinely irreplaceable.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you, "
    "even if you have not named it exactly.",

    "{name_a}'s core question is <i>Am I free?</i> {name_b}'s is "
    "<i>Am I enough to be remembered?</i> These two questions do not directly oppose "
    "each other. But in the daily mechanics of a marriage, they ask for different things "
    "from each other, and the asking misfires in a way that is specific to this pairing.",

    "Here is the mechanism of the collision. {name_b} produces something \u2014 an "
    "achievement, a project, a meal, an effort, something that cost him real work and "
    "deserves to be noticed. He brings it, consciously or unconsciously, into the "
    "marriage as a bid for the recognition the Campaign has always run on. He is not "
    "being calculating; this is simply the grammar his soul operates in. To {name_b}, "
    "bringing something excellent home is a love language. <i>I made this. Do you see "
    "what I have done? Am I enough?</i>",

    "{name_a} reads the room. She sees {name_b}'s bid, and she is genuinely good at "
    "recognizing what it needs. So she produces the appropriate reception: warmth, "
    "affirmation, the mirroring that the Campaign is looking for. And here is the "
    "tragedy: she does this so fluently, so naturally, so authentically in the moment, "
    "that {name_b} cannot tell whether the reception is real. He has watched enough "
    "audiences in his life to know what calibrated applause sounds like. And {name_a}'s "
    "reception, however genuine it may be in her own experience, arrives in a package "
    "that the Campaign has learned to read with suspicion: <i>are you saying this "
    "because you mean it, or because you sensed that I needed to hear it?</i>",

    "Meanwhile, {name_a} experiences the exchange differently. She gave what she read "
    "the room as needing. She was present and attentive and genuinely responsive. "
    "And {name_b} pulled back slightly \u2014 not dramatically, just the small withdrawal "
    "of a person who did not quite receive what they needed. To {name_a}, this withdrawal "
    "reads not as his disappointment but as correction: <i>I read the room wrong. "
    "I gave the wrong version. I need to try again.</i> And so she adjusts.",

    "The adjustment confirms what {name_b} suspected. If the reception needs adjusting, "
    "it was calibrated rather than spontaneous. He does not feel more seen; he feels "
    "more performed for. The significance trigger fires: <i>even the person closest "
    "to me is relating to the Campaign rather than to me.</i> He produces harder, "
    "or he withdraws into something that looks like work but is actually the "
    "Performance's version of licking its wounds.",

    "The Apostle Paul writes in Philippians 2:3\u20134: <i>Do nothing from selfish "
    "ambition or conceit, but in humility count others more significant than yourselves. "
    "Let each of you look not only to his own interests, but also to the interests "
    "of others.</i> The pastoral irony here is that both of you are, in a sense, "
    "already doing this \u2014 {name_a} is looking to {name_b}'s interests by "
    "providing what she reads him as needing; {name_b} is producing things he "
    "believes {name_a} will value. But Paul is describing something different from "
    "either mechanism. He is describing a looking-to-the-other that flows from "
    "being already loved \u2014 a freedom from self-protection that neither mechanism "
    "has yet found its way to.",

    "The collision in your marriage is not between selfishness and selflessness. "
    "It is between two people who are both trying, in their own grammar, to love "
    "each other \u2014 and who have each built a mechanism so responsive to external "
    "signal that the mechanisms interfere with each other in the place where they "
    "most need to be free of signal. You are not failing each other. You are "
    "performing for each other. And the tragedy is that neither of you actually "
    "wants a performance.",
]

COLLISION_2 = [
    "The way out of the collision is not for either of you to stop being who you are. "
    "{name_a} is not going to stop reading rooms; nor should she. {name_b} is not "
    "going to stop producing; nor should he. The Adapter's attunement is a genuine "
    "gift, and the Campaign's excellence is genuinely beautiful. What needs to change "
    "is not the capacity but the direction it is being aimed.",

    "{name_a}, the practice the collision most requires of you is the practice of "
    "unflattering honesty. Not cruelty \u2014 the Adapter does not need to become "
    "harsh. But there is a specific kind of honesty that is nearly impossible for "
    "the Adapter because it violates the mechanism's deepest rule: <i>give the room "
    "what it needs.</i> The honesty the collision requires is: <i>I am going to tell "
    "you what I actually thought about what you produced, even though I can see that "
    "you need to hear something else.</i> This honesty is a gift, not a wound. "
    "It is the one thing {name_b}'s Campaign cannot give itself, and it is the "
    "one thing you are uniquely positioned to give him.",

    "{name_b}, the practice the collision most requires of you is the practice of "
    "receiving {name_a}'s reception as real rather than as calibrated. Not naively "
    "\u2014 you have spent enough time with the Adapter to know that the calibration "
    "happens. But you have a choice, in the moment of receiving, between treating "
    "her reception as suspect and treating it as an act of love that is trying to "
    "reach you. The Campaign treats every reception as evidence to be evaluated. "
    "What the marriage requires is that you sometimes simply receive it, without "
    "running it through the evidence filter, as a person who is loved.",

    "Ecclesiastes 4:9\u201310 says: <i>Two are better than one, because they have "
    "a good reward for their toil. For if they fall, one will lift up his fellow. "
    "But woe to him who is alone when he falls and has not another to lift him up.</i> "
    "The preacher is not talking about productivity. He is talking about the human "
    "need to be lifted by someone who is close enough to know when you have fallen. "
    "You are that for each other. The question is whether you are close enough to "
    "let each other see the falling, rather than performing stability for each other's benefit.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be seasons \u2014 not often, but they will come "
    "\u2014 when both of your breakdowns are in the room at once. The Attorney is up "
    "in both of you, in its two very different forms. And the room gets fast and strange "
    "and exhausting in a way that neither of you will be able to explain clearly "
    "afterward, because what is happening is not a fight about a topic. It is two "
    "very old mechanisms running at full volume simultaneously.",

    "{name_a}'s breakdown is the <b>Attorney in its Adapter form</b>: the multi-witness "
    "courtroom. When {name_a} is finally wounded enough that the calibration cannot hold "
    "the wound, it does not come out as one person with one grievance. It comes out as "
    "every version of {name_a} who has adapted to {name_b}'s needs, speaking simultaneously "
    "\u2014 the version who stayed warm when she did not feel warm, the version who "
    "affirmed the campaign when she was not moved by it, the version who adjusted her "
    "honest reaction to protect the marriage. Each of them has been keeping a record. "
    "When they all speak at once, {name_b} does not experience it as a wound. "
    "He experiences it as discovering that the person he thought he knew "
    "had interior rooms he never knew existed.",

    "{name_b}'s breakdown is the <b>Attorney in its Performance form</b>: the "
    "r\u00e9sum\u00e9 as evidence. When the Campaign has been running and has not "
    "received the recognition it needed \u2014 when the significance trigger fires "
    "in a context that the portfolio cannot address \u2014 the evidence comes out. "
    "<i>Do you know what I have built for this marriage? Do you understand what I "
    "have given? Do you have any idea what I have produced in order to be the "
    "person I am in this family?</i> The accomplishments are real. The case is "
    "accurate. And {name_a}, who has heard every version of this brief, knows "
    "exactly which form of reception the Campaign is looking for \u2014 and is "
    "too wounded, in this moment, to produce it.",

    "Here is the particular exhaustion of this double breakdown. When both mechanisms "
    "are in Plea at once, the marriage runs at a frantic, high-output rate. {name_a} "
    "is cycling through versions trying to find the one that will stop the "
    "Campaign's brief. {name_b} is producing extravagantly \u2014 arguments, "
    "evidence, perhaps actual gestures of effort \u2014 trying to get {name_a} "
    "to see what he has done. Both spouses are giving their best moves. "
    "Neither is feeling met. The room is full of effort and entirely empty of rest.",

    "Paul writes in Galatians 5:1: <i>For freedom Christ has set us free; stand firm "
    "therefore, and do not submit again to a yoke of slavery.</i> Both mechanisms "
    "are, in their breakdown forms, yokes. {name_a}'s Adapter in Plea is the yoke "
    "of a self that cannot stop reading and adjusting even when the reading and "
    "adjusting is destroying her. {name_b}'s Campaign in Plea is the yoke of a "
    "person who cannot stop running even when the running has nothing left to prove. "
    "Both yokes look, from the outside, like freedom \u2014 the Adapter's flexibility, "
    "the Campaign's drive. They are not freedom. They are the oldest captivity "
    "either of you carries. Tim Keller, writing in <i>The Reason for God</i>, "
    "names the deepest form of self-salvation as the accumulation of moral credit "
    "\u2014 the attempt to earn one's standing through performance. Both of your "
    "mechanisms are, in breakdown, doing exactly this. The Adapter is earning "
    "safety through endless relational output. The Campaign is earning love through "
    "endless achievement. Neither will ever accumulate enough.",
]

BOTH_BREAK_2 = [
    "What to do when you can still see what is happening:",

    "<b>One of you, not both, names the loop.</b> Whichever of you first recognizes "
    "the pattern says quietly: <i>this is the loop. We are both performing. "
    "Twenty minutes.</i> No final word. No last adjustment. No final exhibit. "
    "The pause is not negotiable, and its only rule is that neither of you uses it "
    "to draft the next version or prepare the next brief.",

    "<b>In the twenty minutes, neither of you strategizes. Pray.</b> Pray for each "
    "other by name. Not eloquently. {name_a}: <i>Lord, my Adapter is cycling. "
    "Help me stop trying to produce the right version. Give me something true "
    "to say to {name_b}, even if it is not what the room needs.</i> {name_b}: "
    "<i>Lord, my Campaign is running. Help me put down the portfolio. "
    "Help me go back to {name_a} as a person who needs her, not as an attorney "
    "who needs an audience.</i>",

    "<b>When you come back, each of you speaks one sentence.</b> {name_a}'s sentence "
    "is not a calibrated version of what {name_b} needs to hear. It is one true "
    "thing about what she actually felt or needs. {name_b}'s sentence is not "
    "an exhibit from the brief. It is one honest thing about what he actually "
    "needed from {name_a} that he did not know how to ask for directly. "
    "One sentence each. Then stop.",

    "<b>If the loop runs anyway, name it the next day.</b> Not to relitigate. "
    "To name it together as a pattern that happened to both of you, that neither "
    "of you alone created, and that both of you are committed to outlasting. "
    "The Adapter's Attorney and the Campaign's Attorney have both been working "
    "very long shifts. They will retire slowly. The marriage that knows this can "
    "be patient with the slow retirement.",

    "And hear this clearly. <b>Neither of you is the problem.</b> The Adapter's "
    "mechanism and the Campaign's mechanism are not the truest things about either "
    "of you. They are old strategies doing the only job they were ever taught to do. "
    "The truest thing about both of you is that you are a man and a woman who, in "
    "the small grace of a Wednesday evening after a hard week, have decided to keep "
    "trying to reach each other through mechanisms that were built for everything "
    "except this. That choosing, repeated over years, is what a marriage actually is.",
]

COMMITMENTS_INTRO = [
    "What follows are six commitments \u2014 three from {name_a}, three from {name_b}. "
    "They are not vows in the legal sense. They are the small daily practices that, "
    "offered to each other freely and honestly, change the temperature of a home "
    "over months and years. Read each one slowly. If one of you cannot say a "
    "particular commitment in good faith yet, do not say it. The goal is not "
    "performance. It is honesty.",
]

A_COMMITMENTS = [
    ("To tell you what I actually thought.",
     "{name_b}, I commit to telling you when something you produced did not move me, "
     "even though I know how to make it look as if it did. This is the hardest "
     "commitment I can make, because the Adapter's deepest reflex is to give the room "
     "what it needs. What you need more than my calibrated reception is my actual one. "
     "I will practice giving it to you in small doses, in small moments, before the "
     "stakes are too high. An honest response from me, even an unflattering one, "
     "is a form of love I have withheld. I am going to try to stop withholding it."),

    ("To tell you when I am adapting.",
     "{name_b}, when I notice myself producing a version of myself for you rather than "
     "simply being present to you, I commit to naming it. Not as a confession that "
     "undoes everything, but as a small honest flag: <i>I just adjusted that, and "
     "I am not sure it was the real thing.</i> You deserve to know when the Adapter "
     "is running, so that you can ask for the person underneath it. I will try to "
     "tell you before you have to ask."),

    ("To receive your campaign as real.",
     "{name_b}, I commit to receiving what you produce for this marriage as a genuine "
     "act of love, even when I can see the mechanism running underneath it. "
     "You are trying to love me in the grammar you know. I will try to meet the "
     "love rather than diagnose the grammar. And when your production becomes "
     "something I cannot honestly affirm, I will tell you that too \u2014 "
     "not as rejection, but as the kind of honesty that only someone who is "
     "genuinely with you can give."),
]

B_COMMITMENTS = [
    ("To receive your honesty as a gift.",
     "{name_a}, I commit to receiving your unflattering honesty as a gift rather than "
     "as a failure of your output. When you tell me that something I produced did not "
     "move you, I will discipline myself against the Campaign's reflex, which is to "
     "produce something better until it does. Instead, I will stay with what you said. "
     "I will treat your honest response as the thing I have actually been running toward "
     "all along: a person close enough to tell me the truth. That is worth more "
     "than an audience that applauds on schedule."),

    ("To come to you without a portfolio.",
     "{name_a}, I commit to entering the room with you, at least once each day, without "
     "anything to show. No achievement to present, no evidence to offer, no "
     "demonstration of why I have earned your presence for the evening. I will simply "
     "be there. I know this feels counterintuitive to the Campaign. I will do it "
     "anyway, because the version of me who shows up with nothing to prove is the "
     "version I most want you to know \u2014 and the version the Campaign has spent "
     "years making unavailable."),

    ("To trust your reception even when it sounds calibrated.",
     "{name_a}, when you affirm something I have done, I commit to receiving it as "
     "love rather than as performance. I know the Adapter calibrates. I also know "
     "that you have been watching me long enough that your reception carries "
     "something real, even when the form of it is fluent. I will try to stop "
     "interrogating the delivery and receive the gift. And when I genuinely cannot "
     "tell, I will ask you directly: <i>was that real, or were you reading the room?</i> "
     "I trust that you will tell me."),
]

PRAYER = [
    "Father,",

    "You put these two next to each other, and you knew what you were doing. You knew "
    "that the Adapter would need someone who could see past the versions. You knew "
    "that the Campaign would need someone who could receive him when the running stopped. "
    "You knew the Adapter's Attorney and the Campaign's Attorney would, on hard days, "
    "find each other in the kitchen. You knew all of it, and you said yes anyway.",

    "Teach us the grammar of each other. Teach {name_a} to give {name_b} the honest "
    "reception that the Campaign has never been able to produce for itself \u2014 "
    "the word that is true even when it is not what the room needed. Teach {name_b} "
    "to receive {name_a}'s calibration not as performance but as the form love takes "
    "when it has spent years learning how to speak in your particular dialect.",

    "When the Adapter in {name_a} is cycling through versions trying to find the one "
    "that will finally be enough, would you remind her that she was named before "
    "any room existed to require a version of her \u2014 that Ephesians 1:4 is "
    "speaking of her specifically: chosen in Christ before the foundation of the "
    "world, before any calibration was needed. When the Campaign in {name_b} is "
    "assembling the portfolio and the brief is urgent and the recognition feels "
    "necessary, would you remind him that he is engraved on the palms of your "
    "hands \u2014 that Isaiah 49:16 is speaking of him by name, before the first "
    "campaign ran its first race.",

    "Make our home a room in which neither of us has to perform. Make our table a "
    "place where the honest response is safe to give and the honest wound is safe "
    "to name. Make our conversations a place where the Adapter can say what she "
    "actually thinks and the Campaign can arrive with nothing to show, and both "
    "of them find that the room did not empty when they stopped performing.",

    "In the name of the One who walked into every room as himself, who read every "
    "person with perfect attunement and loved them without calibrating who he was "
    "to keep them \u2014 and who produced, for us, the only achievement that finally "
    "answers both of our questions: I am free, and I am enough to be remembered, "
    "because he has made us his own.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages that "
    "follow are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, somewhere "
    "quiet, with no children in the room and no phones on the table. There are six "
    "rounds, and they build on each other. Resist the temptation to skip ahead. "
    "Start at Round One even if it feels too light; the lightness is the point.",

    "Some of the questions are playful. Some are direct. A few are the kind of "
    "questions that, when answered honestly, will sit with you for a week. None of "
    "them are trivia. All of them are an invitation.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did not "
    "read answers first, in full, without interruption. Then the reader answers the "
    "same question. Then you move on. You do not have to finish all six rounds in "
    "one night \u2014 in fact, two or three rounds, taken seriously, is often better "
    "than racing through all of them. Save the rest for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. You may not love "
    "everything you hear. Stay with it. The point is not to grade each other's "
    "answers. The point is to be known, and to do the work of knowing.",
]

ROUND_1 = [
    ("hypothetical",
     "If our marriage were a documentary film, what would the title be, "
     "and what would the opening scene look like?",
     "Not the highlight reel. The actual scene. Where are you, what time is it, what are you doing?"),
    ("observation",
     "What is something I did this week that you noticed and didn't mention?",
     "Not a complaint. A small noticing. The fact that you saw it at all is the gift."),
    ("playful",
     "If you had to describe the energy of our marriage as a weather pattern, "
     "what would it be this month?",
     "Yes, really. Be specific. 'Partly cloudy' is allowed."),
]

ROUND_2 = [
    ("fill-in-blank",
     "I don\u2019t think I tell you this enough \u2014 what I actually see when I "
     "watch you in a room full of people is _______. "
     "And I am still learning to receive that about you.",
     "Two parts: what you observe, and your own admission that it costs you something to receive it."),
    ("observation",
     "Name one moment this year when you felt, without any doubt, that I was actually "
     "with you \u2014 not performing, not managing the situation, just present.",
     "Tell the specific story. The moment matters more than the category."),
    ("one-word",
     "If you had to choose one word to describe what it feels like when I walk into "
     "the room and I am clearly not performing \u2014 when I am just myself \u2014 "
     "what word would it be?",
     "One word, said out loud. Then explain it."),
]

ROUND_3 = [
    ("forward-looking",
     "Five years from now, when we look back on this season, what do you hope we "
     "will say we did differently after reading this document?",
     "Not what you wish you had done. What you want, when you look back, to be able to say you did."),
    ("theological",
     "Where, in the last month, have you seen God working in me in a way that "
     "had nothing to do with my performance or my attunement to you?",
     "Not where you want him to work. Where you have already seen it. Name it specifically."),
    ("shared-identity",
     "Finish this sentence three times: \u2018We are the kind of couple who _______.\u2019 "
     "Give one playful answer, one true answer, and one aspirational answer.",
     "The \u2018we\u2019 is the point. Say all three out loud."),
]

ROUND_4 = [
    ("strength",
     "What is something I give you in this marriage that you would have to learn "
     "to give yourself if I were not here \u2014 and that you are not sure you could?",
     "Hard to ask. Important to hear. Stay with the answer."),
    ("fill-in-blank",
     "One of the gifts of being married to you is that I am allowed to be _______ "
     "in ways I never would have been on my own.",
     "A version of yourself that only exists because the marriage exists. Name it."),
    ("observation",
     "Tell me about a moment in our marriage when you saw me stop performing \u2014 "
     "when the mechanism went quiet and you saw the person underneath it. "
     "What did you see?",
     "This is a gift you are giving the other person: the account of what you saw when they were real."),
]

ROUND_5 = [
    ("hard",
     "When you sense that I am calibrating my response to what you need rather than "
     "giving you my actual response, what happens inside you? "
     "What do you want to say in that moment but usually do not?",
     "For {name_b}: the honest account of what the suspected calibration costs you. "
     "For {name_a}: the honest account of what it costs you to calibrate. Both answers matter."),
    ("profile-aware",
     "{name_a}, when have you given {name_b} a genuinely honest response that you "
     "knew he did not want to hear, and what happened? "
     "{name_b}, when have you come to {name_a} with nothing to show, no campaign running, "
     "and simply needed her \u2014 and what did that cost you?",
     "The Adapter's honesty and the Campaign's vulnerability are the two rarest things in this marriage. "
     "Name a moment when one of them happened."),
    ("theological",
     "What is one thing you have been carrying in this marriage that you have not "
     "yet brought to me, and what has kept you from bringing it?",
     "Not an accusation. An invitation. Hear the answer without defending or solving."),
]

ROUND_6 = [
    ("blessing",
     "Place your hand on your spouse's hand. Say their name. Then say: "
     "\u2018You are not a performance I am evaluating. You are a person I am receiving. "
     "I receive you today.\u2019 Say it slowly. Let them say it back.",
     "You may feel self-conscious. That is part of why it works. Do it anyway."),
    ("prayer",
     "Pray for each other \u2014 not silently, not generally, but out loud and by name. "
     "One sentence is enough. Pray for the thing they just told you in Round Five.",
     "The closing of the date. Do not skip this."),
]


def _render(text, name_a, name_b):
    return text.format(name_a=name_a, name_b=name_b)


def build(sub_a, sub_b) -> bytes:
    """Generate the Adapter + Performance Campaign couples walkthrough PDF.

    sub_a: the submission of the Adapter spouse (ADPT)
    sub_b: the submission of the Performance Campaign spouse (CAMP)
    """
    ensure_fonts()
    S = make_styles()

    name_a = _first_name(sub_a, "Adapter")
    name_b = _first_name(sub_b, "Performance")

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
                "Adapter &middot; Attorney<br/>"
                "<font size=9 color='#6b6862'>Control &middot; Am I free?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_b.upper()}</b></font><br/>"
                "Performance Campaign &middot; Attorney<br/>"
                "<font size=9 color='#6b6862'>Significance &middot; Am I enough to be remembered?</font>",
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
        "<i>\u201cFor freedom Christ has set us free;<br/>"
        "stand firm therefore, and do not submit again to a yoke of slavery.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "Galatians 5:1",
        ParagraphStyle("cqa", fontName="Inter", fontSize=9, leading=14,
                       textColor=MUTED, alignment=TA_CENTER)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1 ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "The room that does not require a performance.",
                   "Why this pairing exists, and what you are both reading it for.")
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
            _profile_card(S, name_a, ACCENT, "Control", "Am I free?",
                          "The Adapter", "The Attorney"),
            "",
            _profile_card(S, name_b, ACCENT_HER, "Significance",
                          "Am I enough to be remembered?",
                          "The Performance Campaign", "The Attorney"),
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
    section_header(story, S, "SECTION THREE  \u00b7  THE ADAPTER'S GIFT",
                   f"What {name_a} gives {name_b}.",
                   "Something Performance Campaigns almost never receive without earning it.")
    for p in GIFT_TO_A:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4 ──
    section_header(story, S, "SECTION FOUR  \u00b7  THE CAMPAIGN'S GIFT",
                   f"What {name_b} gives {name_a}.",
                   "Something the Adapter rarely receives: a room that notices when she walks into it.")
    for p in GIFT_TO_B:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5 ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "The closed loop.",
                   "What happens when the Adapter calibrates the reception the Campaign is producing for.")
    for p in COLLISION:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The way out, in each of your grammars.",
                   "Not stopping being who you are. Aiming the gift differently.")
    for p in COLLISION_2:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6 ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When both Attorneys are in the room at once.",
                   "What is happening, and what to do while you can still see it.")
    for p in BOTH_BREAK:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do, while you can still see it.",
                   "Four practices for the loop, in order.")
    for p in BOTH_BREAK_2:
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
                   f"Three commitments, in his voice, for her to receive.")
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

    rendered_round = lambda r: [(kind, R(q), R(note)) for (kind, q, note) in r]

    _render_round(story, 1, rendered_round(ROUND_1),
                  "Warm up.",
                  "The lightness is the point. Start here even if you would rather skip ahead.")
    story.append(PageBreak())
    _render_round(story, 2, rendered_round(ROUND_2),
                  "Notice the real.",
                  "Specific praise. The kind that lands because it could not have been said by anyone else.")
    story.append(PageBreak())
    _render_round(story, 3, rendered_round(ROUND_3),
                  "Wonder together.",
                  "About us, about God, about the life we are making.")
    story.append(PageBreak())
    _render_round(story, 4, rendered_round(ROUND_4),
                  "Sit in the strength.",
                  "Let yourselves feel the actual weight of what you have built together.")
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
        "You are not a performance I am evaluating.<br/>"
        "You are a person I am receiving. I receive you today.",
        closing_style))

    doc.build(story)
    return finalize_buffer(buf)


# ── STANDALONE TEST ────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    import io

    class FakeSub:
        def __init__(self, mech, name):
            self.primary_mechanism = mech
            self.name = name

    sub_a = FakeSub("ADPT", "Jordan")
    sub_b = FakeSub("CAMP", "Morgan")

    pdf_bytes = build(sub_a, sub_b)
    out_path = os.path.join(os.path.dirname(__file__), "adapter_performance_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        snippet = ""
        # Find Section Three snippet
        for page in reader.pages[4:8]:
            txt = page.extract_text() or ""
            if "ADAPTER" in txt.upper() and "GIFT" in txt.upper():
                snippet = txt.strip()[:200]
                break
        if not snippet:
            for page in reader.pages[3:6]:
                txt = page.extract_text() or ""
                if txt.strip():
                    snippet = txt.strip()[:200]
                    break
    except Exception as e:
        page_count = "unknown"
        snippet = str(e)

    print(f"DONE: adapter_performance.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
