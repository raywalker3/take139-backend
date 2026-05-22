"""Couples Walkthrough — Ambassador + Performance Campaign.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where one spouse is an Ambassador and the
other is a Performance Campaign. First names are substituted from the submissions:
    {name_amb}   -> the Ambassador spouse's first name
    {name_camp}  -> the Performance Campaign spouse's first name

Spouse A (Ambassador): caretaker, temperature manager; trigger Disconnection;
    core question "Am I lovable?"
Spouse B (Performance Campaign): runner, achiever; trigger Significance;
    core question "Am I enough to be remembered?"

One of the most common pairings in ministry and high-achievement households.
Both are giving — the Ambassador relationally, the Performance professionally.
Both are running on an earning model of love, just in different theaters.
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


# ──────────── PROSE — uses {name_amb} and {name_camp} placeholders ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small repeating ones "
    "&mdash; the same disappointment in slightly different clothes, three or four times a week, "
    "year after year, until both people have forgotten what they were originally hoping for.",

    "What follows is a counselor's read of the small repeating rocks in your particular marriage. "
    "Not the dramatic failures, which you would have addressed already. The small ones. The ones "
    "that happen on a Tuesday evening when {name_amb} has spent the day holding the household "
    "together and {name_camp} has spent it holding a campaign together, and neither of you can "
    "quite say why the two kinds of giving are not adding up to the closeness you both need.",

    "You are both reading this because you have decided to look at those rocks. That decision "
    "is more significant than it seems. Most couples spend a lifetime navigating around them "
    "without naming them. Naming them is half the work.",

    "Here is what I want to do for you. I will name what each of you brings the other that you "
    "could not have built alone &mdash; the genuine, theological gift that your two shapes form "
    "together. Then I will name the collision your two questions create, in the specific way it "
    "shows up in your marriage. Then I will name the worst case &mdash; the moment when "
    "{name_amb}'s Flood and {name_camp}'s Quiet Exit are in the room at the same time &mdash; "
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
    "{name_amb}, you are an <b>Ambassador</b> whose body reads disconnection as an alarm and "
    "whose deepest question is whether you are lovable. You have organized much of your life "
    "around maintaining warmth &mdash; in the home, in the family, in the small daily acts of "
    "service that nobody asked you to perform because you performed them before anyone could "
    "ask. When the warmth fails to return, or when the giving is met with absence rather than "
    "acknowledgment, a <b>Flood</b> takes the floor: years of quietly contained grief and "
    "uncredited service surfacing at once, louder and more complete than either of you expected.",

    "{name_camp}, you are a <b>Performance Campaign</b> whose body reads insignificance as an "
    "alarm and whose deepest question is whether you are enough to be remembered. You are a "
    "runner &mdash; not in the literal sense, necessarily, but in the interior sense: a person "
    "who learned early that achievement was the surest path to being seen, that ordinary was "
    "dangerous, that producing at a level others notice is how you hold your place in the "
    "world. When the campaign stalls or the recognition fails to come, a <b>Quiet Exit</b> "
    "begins: not a dramatic withdrawal but a slow retirement, a pulling-back from the field "
    "that can go undetected for months before anyone &mdash; including you &mdash; names it.",

    "Notice what these two profiles do <i>not</i> share, and notice what they actually share "
    "underneath. You are not asking the same question. {name_amb} is asking <i>am I lovable?</i> "
    "and {name_camp} is asking <i>am I enough to be remembered?</i> &mdash; two questions that, "
    "in a marriage, are easy to mistake for each other and surprisingly hard to answer for each "
    "other, because the currency each of you offers is not quite the currency the other needs.",

    "But underneath the two questions is the same root: both of you have learned to earn. "
    "{name_amb} earns through relational service &mdash; warmth, attentiveness, the endless "
    "small acts of care that hold a household together. {name_camp} earns through demonstrated "
    "achievement &mdash; results, visibility, the kind of output that registers in the broader "
    "world of work or ministry or community. The Ambassador's audience is the inner circle; "
    "the Performance's audience is the wider room. Both are earning mechanisms. Both are running "
    "on a model that will eventually, in the mercy of God, run out of fuel.",

    "This is one of the most common pairings in ministry households and high-achieving Christian "
    "marriages, and there is a reason. From the outside, you look like a powerful couple: one "
    "spouse holding the home together with remarkable warmth, the other building something "
    "significant in the world. People look at you and see competence and care working in concert. "
    "They are not wrong. What they cannot see is that both of you are quietly exhausted, each "
    "waiting for the other to notice what the earning has cost.",
]

GIFT_TO_CAMP = [
    "{name_amb} gives {name_camp} something almost no campaign can generate for itself: "
    "<b>a room that does not require the runner to keep running.</b>",

    "The Performance Campaign lives in a world that is largely constituted by achievement. "
    "Every room {name_camp} walks into outside this marriage has a way of measuring output "
    "&mdash; results, recognition, the accumulated evidence of what you have done and built "
    "and demonstrated. Even the good rooms, the rooms where people genuinely love {name_camp}, "
    "tend to love the Campaign version: the one who produces, who shows up ready, who runs "
    "the race well. These rooms are energizing. They are also exhausting, because the love "
    "in them is subtly, structurally tied to the running.",

    "{name_amb}, by virtue of being an Ambassador, makes warmth that is not a response to "
    "{name_camp}'s production. The Ambassador does not love the Campaign because the Campaign "
    "achieved something last week. {name_amb} notices when {name_camp} is tired before "
    "{name_camp} has admitted it. {name_amb} manages the relational temperature of the home "
    "so that {name_camp} comes back from the field to a room that is simply glad you are "
    "back &mdash; not because of what you accomplished out there, but because you are here. "
    "For a person who has spent the day being measured, this is rarer than it sounds.",

    "The theological word for what {name_amb} gives {name_camp} is <i>welcome</i>. Not the "
    "welcome of a crowd that is glad you came because you brought something impressive. The "
    "welcome of a home that is simply glad the door opened and you walked through it. Keller, "
    "writing in <i>The Meaning of Marriage</i>, observed that the one-flesh union of Genesis "
    "2:24 is not a partnership of outputs but a union of selves &mdash; a bond that holds "
    "not because of what each person produces but because of what each person <i>is</i>. "
    "{name_amb} embodies this for {name_camp} every time the home is warm before the "
    "campaign report has been delivered.",

    "{name_camp} &mdash; if you want to thank {name_amb} for something this week, thank her "
    "for this. She probably does not know she is giving it to you, because the Ambassador "
    "gives warmth so naturally that she may not have noticed it is a gift. Tell her that the "
    "home she has built feels different from every other room you walk into &mdash; that in "
    "this room, you do not have to earn being here. That sentence will mean more to her than "
    "you know. Say it anyway.",

    "{name_amb} &mdash; what {name_camp} is receiving from you, when you simply make the room "
    "warm before the report card arrives, is a small daily picture of the love that does not "
    "depend on output. The thing you do without thinking is, for the runner in {name_camp}, "
    "a place where the running can, at last, stop.",
]

GIFT_TO_AMB = [
    "{name_camp} gives {name_amb} something Ambassadors rarely build for themselves: "
    "<b>a witness to the world beyond the home.</b>",

    "The Ambassador is, by nature and by practice, oriented inward. Not selfishly &mdash; the "
    "opposite of selfishly. {name_amb}'s energy flows toward the people near at hand: the "
    "household, the family, the inner circle that constitutes the daily world of relationship. "
    "This is a genuine gift and a genuine calling. But it also means the Ambassador tends, over "
    "time, to lose sight of the wider horizon &mdash; to become so absorbed in the work of "
    "warmth within the home that the bigger story in which the home exists begins to recede.",

    "{name_camp}, by virtue of being a Performance Campaign, is constantly building something "
    "in that wider world. The work {name_camp} does &mdash; in ministry, in career, in "
    "community &mdash; is visible in ways the Ambassador's home-work rarely is. And what "
    "{name_camp} offers {name_amb}, at its best, is a window: a way of seeing that the life "
    "you are living together is part of something larger than the Tuesday-morning schedule. "
    "The Ambassador who is married to the Campaign does not live a small life, even when the "
    "days feel small. The Campaign's vision expands the horizon of the home.",

    "Paul, writing to the Colossians, offers a word that belongs to both of you: "
    "<i>Whatever you do, work heartily, as for the Lord and not for men, knowing that from "
    "the Lord you will receive the inheritance as your reward.</i> (Colossians 3:23&ndash;24) "
    "{name_camp} needs this verse for sanity &mdash; a reminder that the campaign is ultimately "
    "for an audience of One, not for the recognition of the wider room. But {name_amb} needs "
    "it too. The home service that no one in the wider world will ever notice is also done "
    "for the Lord &mdash; it is also a campaign, conducted in a different theater, and it is "
    "seen by the same eyes that see {name_camp}'s work.",

    "{name_amb} &mdash; if you want to thank {name_camp} for something this week, thank him "
    "for something specific he has built or pursued that has expanded what you understand to "
    "be possible. Campaigns often do not know their vision is received as a gift inside the "
    "home. Tell him, and he will know.",

    "{name_camp} &mdash; what {name_amb} is receiving from you, when you pursue something "
    "larger than the household, is a reminder that the family you are building together "
    "is not a refuge from the world but a launching point into it. The thing in you that "
    "drives toward the horizon is, for {name_amb}, a kind of courage she borrows.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you, even if "
    "you have not named it in quite these terms.",

    "{name_amb}'s core question is <i>am I lovable?</i> {name_camp}'s is <i>am I enough "
    "to be remembered?</i> These two questions are not opposed in theory. In the daily "
    "mechanics of a marriage, they ask for different things &mdash; and they tend to ask "
    "for them in different rooms, on different schedules, in dialects the other spouse has "
    "not been trained to hear.",

    "The Ambassador's giving is directed inward, toward the home and the inner circle. It "
    "is relational, warm, attentive to the small temperature-changes that most people miss. "
    "{name_amb} serves {name_camp} by making the home a place {name_camp} can actually "
    "come back to: meals prepared, children managed, emotional weather monitored. This is "
    "real love, offered in the grammar the Ambassador knows. To {name_amb}, this service "
    "is also a question: <i>do you see what I am doing for you? Am I lovable enough to "
    "be worth returning to?</i> The giving is genuine. The question underneath it is also "
    "genuine, and it is waiting for an answer.",

    "The Performance Campaign's giving is directed outward, toward the work and the wider "
    "world. {name_camp} is building something &mdash; a ministry, a career, a contribution "
    "that registers beyond the walls of the house. This is also real love, though it does "
    "not always look like it from inside the home. When {name_camp} works late to finish "
    "something that matters, there is a version of that which is love for the family "
    "&mdash; providing, building, securing. To {name_camp}, the campaign is also a "
    "question: <i>does what I am doing out there count for something? Is it enough to be "
    "remembered?</i> The running is genuine. The question underneath it is also genuine.",

    "Here is the problem: neither spouse can easily see the other's love-giving, because "
    "each spouse's attention is calibrated to a different theater. {name_camp}'s radar is "
    "scanning the wider room &mdash; the professional horizon, the community standing, the "
    "campaign's progress. In that scan, the home warmth {name_amb} has been quietly "
    "building simply does not register. It is not that {name_camp} is ungrateful. It is "
    "that the thing {name_amb} is offering is not on the channel {name_camp} is "
    "monitoring. The Ambassador's home-service is below the threshold of the Performance's "
    "significance radar.",

    "Meanwhile, {name_amb} is watching {name_camp} pour enormous energy into the campaign "
    "&mdash; work, community, ministry &mdash; and the internal question begins to form: "
    "<i>if he is giving that much out there, what does he have left for me here?</i> The "
    "Performance's outward investment reads, to the Ambassador's disconnection-sensitive "
    "system, not as love-giving but as love-absence. The very thing {name_camp} may be "
    "doing partly <i>for</i> the family looks, from inside the home, like evidence that "
    "the family does not come first.",

    "Paul, in Ephesians 5:21, writes: <i>submitting to one another out of reverence for "
    "Christ.</i> The word translated 'submitting' carries the sense of voluntary yielding "
    "&mdash; a willingness to receive what the other is offering, even when it is not "
    "offered in your preferred form. This is the precise posture both of you need. "
    "{name_amb} must learn to receive {name_camp}'s outward-facing work as a form of "
    "love, even when it does not feel like closeness. {name_camp} must learn to receive "
    "{name_amb}'s home-warmth as a real and visible contribution, even when it does not "
    "register on the significance radar. Both of you are, in fact, giving. Both of you are "
    "failing to receive what the other is offering. Mutual submission, here, means "
    "learning to receive love in a form you did not design.",

    "{name_camp}, when you walk into a room {name_amb} has made warm and do not name it, "
    "the translation inside {name_amb} is almost never <i>he is too busy to notice.</i> "
    "The translation is <i>I am invisible here, even here.</i> The right move, when you "
    "come home, is to set down the campaign for sixty seconds and look at what has been "
    "built in your absence. Name one specific thing you see. The Ambassador will not "
    "demand this. But she has been waiting for it longer than you know.",

    "{name_amb}, when {name_camp} goes back to the campaign after an evening together, "
    "the translation inside {name_camp} is almost never <i>the home does not matter.</i> "
    "The translation is usually <i>the campaign cannot afford to stop, and stopping feels "
    "like failing.</i> The right move, when you feel the disconnection rising, is not to "
    "give more in hopes that the giving will eventually pull {name_camp} back. It is to "
    "name, in one sentence, what you actually need: <i>I need ten minutes where you are "
    "here, not out there.</i> The runner can stop. But the runner needs to be told to stop "
    "before the stopping feels like permission rather than failure.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be seasons &mdash; not often, but they will come "
    "&mdash; when the small collision in the kitchen escalates, and both of you are in "
    "the breakdown at the same time. The Flood is up. The Quiet Exit has begun. The room "
    "is full of the accumulated weight of months, and neither of you, in that moment, has "
    "access to the more thoughtful person you were before it started.",

    "Here is what is happening, named plainly so you can both see it.",

    "{name_amb}, when the Flood is up, it is not simply a bad day arriving loudly. "
    "It is the ledger of invisible home-giving, quietly compiled over months or years, "
    "finally breaking the surface all at once. The meals that were received without "
    "comment. The emotional weather of the household managed in the background while "
    "the campaign ran in the foreground. The times {name_amb} needed to be seen and "
    "was not, because {name_camp}'s attention was on the wider room. None of these "
    "were disasters in themselves. Together, they became weight. And the Flood is what "
    "happens when the weight can no longer be quietly carried.",

    "{name_camp}, when the Quiet Exit begins, it is not a single decision. It is a "
    "sequence of small ones, each almost invisible: a campaign that is wound down "
    "internally before it is retired externally, a runner who is still on the field "
    "but is no longer really running. The Quiet Exit is not dramatic. It is the "
    "Performance's version of burnout &mdash; the campaign retired in spirit while "
    "the motions continue. And because the Quiet Exit is so quiet, {name_amb} often "
    "cannot see it coming until it has already arrived. By then, the Flood is building.",

    "The combination is a tragic mismatch. One spouse is pouring out the years of "
    "invisible service, finally, audibly &mdash; the Flood is saying <i>do you see "
    "what I have been carrying?</i> The other spouse is no longer running, but also "
    "no longer present &mdash; the Quiet Exit has already begun its slow withdrawal. "
    "Revelation 2:4&ndash;5 speaks to the church at Ephesus with words that carry "
    "unusual pastoral weight for this pairing: <i>I have this against you, that you "
    "have abandoned the love you had at first.</i> The word translated 'abandoned' "
    "does not mean betrayal. It means a gradual departure, a slow leaving of what was "
    "once the center. Both of you, in breakdown, are capable of this &mdash; the "
    "Ambassador abandoning the first love by replacing it with a ledger, the Performance "
    "abandoning it by retiring the campaign that love once fueled.",

    "Spurgeon, writing on ministry burnout, observed that the servant who gives without "
    "receiving is not practicing self-sacrifice but something closer to self-depletion "
    "&mdash; and that self-depleted servants eventually have nothing left to give anyone, "
    "including the people they love most. Both of you are, in your different theaters, "
    "at risk of this. The Ambassador depletes by giving relational reserves that are "
    "never replenished. The Performance depletes by running a campaign that is never "
    "allowed to rest. The marriage in which both spouses are depleted simultaneously "
    "is the marriage in which the Flood and the Quiet Exit find each other with "
    "nothing between them.",

    "What to do, when you can both still see what is happening:",

    "<b>One of you calls the pause.</b> Whichever one of you notices first what is "
    "happening says, out loud: <i>this is the loop. Twenty minutes.</i> No discussion "
    "about who is right. No final word. The pause is non-negotiable, and its only rule "
    "is that no one uses it to rehearse the next wave or to retreat further into the "
    "exit.",

    "<b>In the twenty minutes, do not manage the situation. Pray.</b> Pray for each "
    "other by name. Not eloquently. <i>Lord, my Flood is up. Show me the one thing "
    "under the years of weight. Help me come back to him as {name_amb}, not as the "
    "accumulated ledger.</i> Or: <i>Lord, my Exit has begun. Pull me back to the "
    "field. Help me see that presence here is not failure out there. Give me back "
    "the first love.</i>",

    "<b>When you come back, each of you says one sentence.</b> {name_amb}, your "
    "sentence is not the full ledger. It is the one entry, the single weight at the "
    "bottom of the pile, spoken as a need rather than a verdict. {name_camp}, your "
    "sentence is not a defense of the campaign. It is one true admission about where "
    "the Exit has been taking you, spoken before the Exit is complete. <i>I have "
    "been absent in ways I have not named.</i> Both of you can say one sentence. "
    "Then stop.",

    "<b>And hear this plainly.</b> Neither of you is the problem. The Flood and the "
    "Quiet Exit are old mechanisms doing the only job they were ever taught to do. "
    "The truest thing about both of you is that you chose each other, and you have "
    "been giving &mdash; both of you, in your different theaters &mdash; for a long "
    "time. The marriage that knows this can be patient with the slow retirement of "
    "the old machinery. The first love is not gone. It is waiting, just below the "
    "surface of the Flood, just before the Exit is complete.",
]

COMMITMENTS_INTRO = [
    "What follows are six commitments &mdash; three from {name_amb}, three from {name_camp}. "
    "They are not vows in the legal sense. They are the small daily practices that, offered "
    "to each other freely, change the temperature of a home over months and years. Read each "
    "one slowly. If one of you cannot say a particular commitment in good faith yet, do not "
    "say it. The goal is not performance; it is honesty.",
]

AMB_COMMITMENTS = [
    ("To measure love by the whole offering.",
     "{name_camp}, I commit to measuring your love not only by the warmth you bring to "
     "the home but by the whole of your offering &mdash; including what you do for the "
     "world outside our walls. When I see you working late on something that matters, I "
     "will practice receiving that as a form of love, even when it does not feel like "
     "closeness. I will not require that your love arrive only in the grammar I recognize."),

    ("To name the weight before it floods.",
     "{name_camp}, I commit to naming the small weights as they come, rather than carrying "
     "them in silence until the Flood does it for me. I will not always do this perfectly. "
     "But I will try, on the small things, to give them a sentence in the same week they "
     "happen &mdash; not as a verdict, but as a window into what I am actually carrying. "
     "You cannot see what I have not shown you. I will show you more."),

    ("To ask directly for what I need.",
     "{name_camp}, I commit to asking directly for presence rather than waiting for you "
     "to notice my absence. When I need ten minutes where you are here and not there, "
     "I will say so plainly. The Ambassador in me has been trained to express need only "
     "through giving. I will practice expressing it through asking. The question is not "
     "too much. Neither am I."),
]

CAMP_COMMITMENTS = [
    ("To see the home as a real and visible contribution.",
     "{name_amb}, I commit to receiving what you have built in the home as a real and "
     "visible contribution &mdash; not as the background to my work, not as the support "
     "structure the campaign runs on, but as a campaign in its own right, conducted in "
     "a theater I have not always had the eyes to see. I will name one specific thing "
     "you have built, each week, that I would not have named before reading this."),

    ("To come home, not just return.",
     "{name_amb}, when I walk through the door, I commit to actually arriving. Not to "
     "be managed into the next item on the household schedule &mdash; but to be present "
     "for sixty seconds before the evening begins, to look at what is here, and to let "
     "you know I am glad to be back. The campaign will still be there tomorrow. You "
     "are here now."),

    ("To name the Exit before it is complete.",
     "{name_amb}, I commit to telling you when the Quiet Exit has begun &mdash; when "
     "the campaign is winding down on the inside before it shows on the outside. I will "
     "not let you carry the marriage alone while I make my quiet withdrawal. If I am "
     "depleted, I will name it to you as a need before it becomes a disappearance. You "
     "deserve access to the person behind the campaign, not only the version that "
     "is still running."),
]

PRAYER = [
    "Father,",

    "You set us next to each other, and you knew exactly what you were doing. You knew "
    "the Ambassador would need a witness to the world beyond the home. You knew the "
    "Performance would need a room where the running could stop. You knew the Flood and "
    "the Quiet Exit would, on hard days, find each other in the kitchen. You knew all "
    "of it before either of us said yes.",

    "Teach {name_amb} what it feels like to be loved without having to earn it &mdash; "
    "to receive from {name_camp}'s outward giving the same warmth she has been building "
    "inward all these years. Quiet the question <i>am I lovable?</i> with the answer "
    "that was spoken over her before she gave a single thing: <i>you are my child; my "
    "love for you is not contingent on what you do next.</i>",

    "Teach {name_camp} what it feels like to be enough before the campaign delivers its "
    "results &mdash; to receive from {name_amb}'s home-warmth the very recognition the "
    "wider room has not always given. Quiet the question <i>am I enough to be "
    "remembered?</i> with the answer already inscribed in the palms of the hands that "
    "hold him: <i>I know you fully. I will not forget you. You are mine.</i>",

    "When the Flood rises in {name_amb}, remind her that the one entry she most needs "
    "to name is already known &mdash; that the years of unseen service were seen, and "
    "that the One who saw them is not keeping a ledger but a love. When the Quiet Exit "
    "begins in {name_camp}, pull him back to the field &mdash; remind him that the "
    "first love is not gone, only buried under the weight of too much producing and "
    "not enough receiving.",

    "Make our home a room where neither of us has to earn the right to be here. Make "
    "our table a place where the invisible work is named and the outward campaign is "
    "received as love in a different grammar. Make our bed a place where the day's "
    "loops are quieted before sleep, and our mornings a place where the two of us "
    "begin again, on grace and not on yesterday.",

    "And Father, when we are old and the children are grown and the campaign has run "
    "its course, let us look back and see that we saw each other &mdash; really saw "
    "each other &mdash; and that the seeing was enough.",

    "In the name of the One who took a bride for himself, who is preparing a home "
    "for her, and who will not rest until she is presented without spot or wrinkle "
    "before the Father.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages that follow "
    "are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, somewhere "
    "quiet, with no children in the room and no phones on the table. There are six rounds, "
    "and they build on each other. Resist the temptation to skip ahead. Start at Round One "
    "even if it feels too light; the lightness is the point.",

    "Some of the questions are playful. Some are direct. A few are the kind of questions "
    "that, when answered honestly, will sit with you for a week. None of them are trivia. "
    "All of them are an invitation.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did not read "
    "answers first, in full, without interruption. Then the reader answers the same question. "
    "Then you move on. You do not have to finish all six rounds in one night &mdash; in "
    "fact, two or three rounds, taken seriously, is often better than racing through all of "
    "them. Save the rest for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. You may not love everything "
    "you hear. Stay with it. The point of this is not to grade each other's answers. "
    "The point is to be known, and to do the work of knowing.",
]

ROUND_1 = [
    ("hypothetical",
     "If our marriage were a building, what kind would it be, and which room would be your favorite?",
     "Metaphor has a way of saying what plain language can't. Let the image surprise you."),
    ("observation",
     "What is something I did this week that you noticed and didn't say anything about?",
     "Not a complaint. A small noticing. The fact that you noticed at all is the gift."),
    ("playful",
     "If you had to describe our marriage as a season of the year, which season would it be right now, and why?",
     "Yes, really. Answer with the first thing that comes to mind."),
]

ROUND_2 = [
    ("fill-in-blank",
     "I don't think I tell you this enough &mdash; I am genuinely grateful for the way you _______. "
     "That particular gift of yours has held something in our marriage that I couldn't have held without you.",
     "Be specific. 'You're caring' is too easy. 'You noticed I was tired before I said anything, and "
     "made me sit down' is closer."),
    ("observation",
     "What is one thing you've watched me do this year that you wish I gave myself more credit for?",
     "Most of us undervalue the things we do most naturally. Tell your spouse which one you see."),
    ("one-word",
     "If you had to choose one word to describe what it feels like when I'm fully present with you &mdash; "
     "not half-distracted, not running &mdash; what word would it be?",
     "One word. Said out loud. Then explain it, briefly."),
]

ROUND_3 = [
    ("forward-looking",
     "Five years from now, when we look back on this season of our marriage, what do you hope we will "
     "say we did well together?",
     "Not what you wish you had done. What you want, when you look back, to be able to say you did."),
    ("theological",
     "Where, in the last month, have you seen God specifically at work in me &mdash; not in the campaign, "
     "not in the household, but in the person?",
     "Not where you want him to work. Where you've already seen it. Name it."),
    ("shared-identity",
     "Finish this sentence three times: 'We are the kind of couple who _______.'"
     " Give one playful answer, one true answer, and one aspirational answer.",
     "The 'we' is the point. Notice which sentences come easily and which ones take a moment."),
]

ROUND_4 = [
    ("strength",
     "What is something I do for this marriage that you would have to learn to do for yourself if I weren't here?",
     "Hard to ask. Important to hear the answer. Stay with it."),
    ("fill-in-blank",
     "One of the gifts of being married to you is that I get to be _______ in ways I never would have been on my own.",
     "A version of yourself that only exists because the marriage exists. Name it."),
    ("observation",
     "Name one moment in our story where you knew, with no doubt, that we had built something together "
     "that neither of us could have built alone.",
     "Tell the story in full. The remembering is part of the strengthening."),
]

ROUND_5 = [
    ("profile-aware",
     "{name_amb}: When you've been giving a lot and I haven't named what I see, "
     "what does that silence feel like? What is the question it wakes up in you?",
     "This is from the walkthrough. {name_camp}: listen to the answer without defending."),
    ("profile-aware",
     "{name_camp}: When the campaign is running well and the home feels like the background, "
     "what is actually happening inside you? Is it that the home matters less, or that "
     "the campaign feels like it can't afford to stop?",
     "This is from the walkthrough. {name_amb}: listen to the answer without fixing it."),
    ("hard",
     "What is one thing you have been carrying lately &mdash; about yourself, about us &mdash; "
     "that you have not yet brought to this marriage? What has kept you from bringing it?",
     "Not an accusation. An invitation. Hear the answer without defending."),
]

ROUND_6 = [
    ("blessing",
     "Place your hand on your spouse's hand. Say their name. Then say: "
     "'You are not a problem to be solved. You are a gift I get to receive again tomorrow.' "
     "Say it slowly. Let them say it back.",
     "You may feel silly. That is part of why it works. Do it anyway."),
    ("prayer",
     "Pray for each other &mdash; not silently, not generally, but out loud and by name. "
     "One sentence is enough. Pray for the thing they just told you in Round Five.",
     "The closing of the date. Do not skip."),
]


def _render(text, name_amb, name_camp):
    return text.format(name_amb=name_amb, name_camp=name_camp)


def build(sub_a, sub_b) -> bytes:
    """Generate the Ambassador + Performance Campaign couples walkthrough PDF.

    sub_a: the submission of the Ambassador spouse
    sub_b: the submission of the Performance Campaign spouse
    """
    ensure_fonts()
    S = make_styles()

    name_amb = _first_name(sub_a, "Ambassador")
    name_camp = _first_name(sub_b, "Performance")

    def R(text):
        return _render(text, name_amb, name_camp)

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Couples Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUPLES WALKTHROUGH",
        cover_right_label=f"{name_amb.upper()}  +  {name_camp.upper()}",
        title=f"Take 139 Couples Walkthrough \u2014 {name_amb} & {name_camp}",
    )

    story = []

    # ── COVER ──
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Couples<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph(
        "A counselor\u2019s read of the small repeating rocks<br/>in your particular marriage.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("PREPARED FOR", S["CoverProfileLabel"]))
    story.append(Paragraph(f"{name_amb} &nbsp;&amp;&nbsp; {name_camp}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_amb.upper()}</b></font><br/>"
                "Ambassador &middot; Flood<br/>"
                "<font size=9 color='#6b6862'>Disconnection &middot; Am I lovable?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_camp.upper()}</b></font><br/>"
                "Performance Campaign &middot; Quiet Exit<br/>"
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
        "<i>\u201cFrom the outside, they look like a powerful couple.<br/>"
        "One holds the home. The other runs the campaign.<br/>"
        "What neither one knows is that both are exhausted, and both are waiting to be seen.\u201d</i>",
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
                          "The Ambassador", "The Flood"),
            "",
            _profile_card(S, name_camp, ACCENT_HER, "Significance",
                          "Am I enough to be remembered?",
                          "The Performance Campaign", "The Quiet Exit"),
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
    section_header(story, S, "SECTION THREE  \u00b7  THE AMBASSADOR\u2019S GIFT TO THE PERFORMANCE",
                   f"What {name_amb} gives {name_camp}.",
                   "A room where the runner does not have to keep running.")
    for p in GIFT_TO_CAMP:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4 ──
    section_header(story, S, "SECTION FOUR  \u00b7  THE PERFORMANCE\u2019S GIFT TO THE AMBASSADOR",
                   f"What {name_camp} gives {name_amb}.",
                   "A window to the horizon the Ambassador rarely sees on her own.")
    for p in GIFT_TO_AMB:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5 ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Two giving mechanisms, two different theaters.",
                   "The small repeating rock, named.")
    for p in COLLISION[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The invisible giving, the missed reception.",
                   "And the way out, for each of you in your own grammar.")
    for p in COLLISION[5:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6 ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When the Flood and the Quiet Exit are in the room at once.",
                   "What is happening, and what to do while you can still see it.")
    for p in BOTH_BREAK[:6]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do, while you can still see it.",
                   "Three practices for the loop, in order.")
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
    story.append(Paragraph(f"FROM {name_amb.upper()}, TO {name_camp.upper()}", S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name, body in AMB_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(name, S["H3"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_camp}, to {name_amb}.",
                   "Three commitments, in the Campaign\u2019s voice, for the Ambassador to receive.")
    story.append(Paragraph(f"FROM {name_camp.upper()}, TO {name_amb.upper()}", S["CommitLabelHer"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT_HER,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name, body in CAMP_COMMITMENTS:
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
                  "The lightness is the point. Start here even if you\u2019d rather skip ahead.")
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
                  "Let yourselves feel the actual weight of what you\u2019ve built.")
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


# ── STANDALONE TEST ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    import io

    class FakeSubA:
        primary_mechanism = "AMB"
        primary_breakdown = "FLOOD"
        primary_trigger = "DISC"
        core_question = "LOV"
        name = "Sarah"

    class FakeSubB:
        primary_mechanism = "CAMP"
        primary_breakdown = "VERD"
        primary_trigger = "SIG"
        core_question = "REM"
        name = "Michael"

    pdf_bytes = build(FakeSubA(), FakeSubB())
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "ambassador_performance_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        snippet = ""
        for page in reader.pages[4:10]:
            txt = page.extract_text() or ""
            if "SECTION THREE" in txt or "room" in txt.lower() or "runner" in txt.lower():
                snippet = txt.strip()[:200]
                break
        if not snippet:
            for page in reader.pages[4:10]:
                txt = page.extract_text() or ""
                if txt.strip():
                    snippet = txt.strip()[:200]
                    break
    except Exception as e:
        page_count = "unknown"
        snippet = f"(pypdf error: {e})"

    print(f"DONE: ambassador_performance.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
