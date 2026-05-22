"""Couples Walkthrough — Performance Campaign + Performance Campaign.

Voice: Tim Keller (from The Meaning of Marriage + Counterfeit Gods).
Pastoral, theologically rich, warmly direct.
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where both spouses are Performance Campaigns.
First names are substituted from the submissions at render time:
    {name_a}  -> the first Performance spouse's first name (alphabetical)
    {name_b}  -> the second Performance spouse's first name (alphabetical)

For same-mechanism pairs the order does not carry directional meaning.
The build() function sorts alphabetically so name_a <= name_b.

Pastoral key: The most outwardly impressive same-mechanism pairing. Both
spouses are accomplished, productive, visibly contributing. The hidden
problem: both are running on visibility and producing for recognition,
and the marriage itself slowly becomes another arena where each performs.
Each spouse has cast the other as audience. Neither has the interior
reserves to stop running and simply receive the other.

THIS IS WALKTHROUGH 21 OF 21 — THE FINAL COUPLES WALKTHROUGH.
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


# ──────────── PROSE CONSTANTS — use {name_a} and {name_b} ────────────
# CRITICAL: No adjacent string literal continuation inside triple-quoted
# strings. All long strings use + concatenation or list items.

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small repeating "
    + "ones &mdash; the same disappointment in slightly different clothes, week after "
    + "week, until both people have forgotten what they were originally hoping for. But "
    + "for you, the small repeating rock has a particular shape, because you are one of "
    + "the most counterintuitive pairings we encounter: <b>two Performance Campaigns.</b>",

    "From the outside, yours is the marriage everyone points to. You appear in rooms "
    + "and the rooms take notice. Between the two of you, there are accomplishments, "
    + "credentials, visible contributions &mdash; ministry, business, academia, the arts, "
    + "medicine, leadership, something in which at least one of you has been publicly "
    + "recognized and likely both. You are that couple. People admire you. They admire "
    + "your productivity and your complementary ambitions and the way you seem to "
    + "handle everything. They are not entirely wrong.",

    "What they cannot see &mdash; and what you may have difficulty seeing yourselves "
    + "&mdash; is that both of you have been, for a long time, running. Not running "
    + "<i>together</i> exactly, though you often run side by side. Running, each of you, "
    + "for the visibility that the question underneath your mechanism has always required. "
    + "And the marriage, quietly, over time, has become one more arena. One more room "
    + "where the running must continue. One more audience. And the person sitting across "
    + "from you at dinner is not only your spouse &mdash; they are, without either of "
    + "you intending it, your most important audience member. The one whose notice "
    + "matters most. The one who, somehow, never quite notices enough.",

    "Here is what I want to do for you. I will name what each of you genuinely brings "
    + "the other that the marriage could not have built alone &mdash; because there is a "
    + "real gift in this pairing, and it deserves to be named before anything else is "
    + "said. Then I will name the collision your shared mechanism creates: not a fight, "
    + "typically, but something slower and more consequential &mdash; the quiet erosion "
    + "of all rest in the marriage. Then I will name the harder picture, the moment when "
    + "both campaigns have retired in spirit while the bodies keep running, and what "
    + "to do while you can still see it. Then I will hand each of you commitments: not "
    + "rules, but the specific small practices that, kept faithfully, begin to change "
    + "the temperature of a home.",

    "Read it together, if you can. If not, read it separately and then sit down with "
    + "it. Argue with what does not fit. Stay with what does. And before you begin, "
    + "hear this: the fact that {name_a} and {name_b} are reading the same pages, "
    + "about the same marriage, at the same time, is itself an act of stopping. Two "
    + "Performances who agree to stop and look together have already done something "
    + "the mechanism resists with everything it has. That is not nothing. It is, in "
    + "fact, the first rest either of you has taken in a long time.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on "
    + "paper, side by side. Most couples never see their two profiles next to each other "
    + "with this kind of deliberate clarity. You are about to &mdash; and for you, the "
    + "first thing you will notice is how completely the profiles mirror each other.",
]

TWO_SHAPES_BODY = [
    "{name_a}, you are a <b>Performance Campaign</b> whose body reads insignificance as "
    + "an alarm and whose deepest question is <i>Am I enough to be remembered?</i> You "
    + "are a runner. You discovered early in life that achievement was the surest path "
    + "to being seen &mdash; that ordinary was forgettable, and forgettable was not safe. "
    + "And so you began to build: to produce, to demonstrate, to show what you could do "
    + "in the full light of day. The Campaign was born. Over years and campaigns and the "
    + "accumulation of evidence, you have developed a way of moving through the world "
    + "that answers the question <i>do I matter?</i> through visible output. Rest, if "
    + "you are honest, does not feel like rest. It feels like a kind of risk.",

    "{name_b}, you are a <b>Performance Campaign</b> running the same mechanism: "
    + "significance is the alarm, <i>Am I enough to be remembered?</i> is the question. "
    + "You, too, are a runner. You, too, discovered that the path to being seen ran "
    + "through the extraordinary. You, too, have built an identity around demonstrated "
    + "worth rather than received worth &mdash; around what you have produced rather "
    + "than around who you are when you are producing nothing. The default response to "
    + "anxiety, in both of you, is not to withdraw and not to plan. It is to produce. "
    + "When the question fires, the answer is always the same: <i>let me show you "
    + "one more thing.</i>",

    "Take a moment to absorb what this means. You are asking the same question. You are "
    + "running the same Campaign. You are, at some level, protecting the same wound in "
    + "the same way. This shared grammar makes for a marriage of unusual energy and "
    + "mutual respect &mdash; two people who understand each other's drive, who never "
    + "have to explain why the project matters, who do not need to apologize for the "
    + "next campaign. Neither of you has ever had to justify the running to the "
    + "other. You simply run, side by side, and at its best this is a remarkable "
    + "thing to behold.",

    "But here is what the shared grammar does not automatically produce: <i>a place "
    + "to stop.</i> Two Performances in a marriage create a home with no natural resting "
    + "place. Both of you are managing your visibility. Both of you are producing. Both "
    + "of you are watching, in some peripheral register, for the recognition that the "
    + "mechanism always requires. And neither of you &mdash; this is the pastoral "
    + "key &mdash; has the interior surplus to be a genuine audience for the other. "
    + "Because you cannot fully receive someone else's running when you are also running.",

    "Tim Keller, writing in <i>The Meaning of Marriage</i>, observed that a good "
    + "marriage requires each spouse to become what the other cannot be for themselves. "
    + "This is the specific discipline a two-Performance marriage must learn: how to stop "
    + "running long enough to actually see the person beside you. Not their "
    + "accomplishments. Not their campaign. <i>Them.</i> That discipline is, for "
    + "both of you, among the hardest things this marriage will ever ask.",
]

GIFT_TO_A = [
    "{name_b} gives {name_a} something almost no one else in the marriage is in a "
    + "position to give: <b>a witness who already knows the cost of the running.</b>",

    "Most people in {name_a}'s world receive the Campaign's output &mdash; benefit from "
    + "the accomplishments, enjoy the results, admire the energy &mdash; without any "
    + "particular understanding of what it costs to produce. The Campaign is very good "
    + "at making the running look effortless. But it is not effortless. It is "
    + "sustained, deliberate, and costly &mdash; the particular exhaustion of a person "
    + "who cannot fully rest because rest, for the Campaign, is never quite safe. Most "
    + "of the world does not know this because the Campaign does not show it.",

    "{name_b} knows it. Not because of unusual perceptiveness, but because {name_b} "
    + "carries the same mechanism and therefore knows, from the inside, what it means "
    + "to sustain excellence past the point of genuine energy. {name_b} knows the "
    + "particular quiet of an evening when there is nothing left to produce and the "
    + "anxiety comes in anyway. {name_b} knows what it feels like when recognition "
    + "arrives and fails &mdash; again &mdash; to fully silence the question. {name_b} "
    + "has lived there. {name_b} knows.",

    "What this gives {name_a} is something rare: a marriage in which the most important "
    + "person in the room does not need the Campaign explained. {name_b} does not require "
    + "{name_a} to justify the drive, does not pathologize the ambition, does not "
    + "interpret the restlessness as a deficiency of character. {name_b} receives the "
    + "running as the thing it genuinely is &mdash; a gift pressed into service as a "
    + "survival strategy &mdash; with the particular grace of one who has run the same "
    + "race by the same logic.",

    "{name_a} &mdash; if you want to thank {name_b} for something this week, thank "
    + "{name_b} for the fact that {name_b} has never once made you feel that the "
    + "running was too much. You have probably spent much of your life being received "
    + "by people who either admired the output without seeing the cost, or who found "
    + "the ambition exhausting and said so. {name_b} has done neither. Tell {name_b} "
    + "that the being-known-from-inside matters more than the admiration ever has. "
    + "{name_b} may not know what to do with the gratitude. Say it anyway.",
]

GIFT_TO_B = [
    "{name_a} gives {name_b} something almost no one else in the marriage can give: "
    + "<b>a person who will not be diminished by the campaign.</b>",

    "The Performance Campaign carries a hidden fear that most of its relationships "
    + "confirm: that its drive, when fully visible, will crowd out the people beside it. "
    + "That the ambition will be too much. That the running will leave the other person "
    + "feeling small &mdash; either because the accomplishments are intimidating, or "
    + "because the Campaign's attention is so consistently focused on the next thing "
    + "that those beside it feel, over time, like the room the Campaign is always about "
    + "to leave. The Performance has often been told, in one form or another, "
    + "that it is a lot.",

    "{name_a}, by virtue of being a Performance Campaign, cannot be crowded out by "
    + "{name_b}'s running. {name_a} has a campaign of their own. {name_a}'s own "
    + "significance is not dependent on {name_b} running less. This gives {name_b} "
    + "something rare: a spouse who is genuinely not diminished by the ambition, who "
    + "does not need the Campaign to slow down in order to feel safe, who stands beside "
    + "the running without flinching because {name_a} understands the running "
    + "from the inside.",

    "The theological word for what {name_a} gives {name_b} in this is something close "
    + "to <i>solidarity</i> &mdash; the companionship of one who shares the burden "
    + "rather than standing outside it in judgment. Ecclesiastes 4:9&ndash;10 says: "
    + "<i>Two are better than one, because they have a good reward for their toil. For "
    + "if they fall, one will lift up his fellow.</i> The Preacher is not romanticizing "
    + "companionship &mdash; he is naming a fact: the toil is real, the falling is real, "
    + "and the one who can lift you when you fall is always someone who has been near "
    + "enough to see you fall. {name_a} is near enough. {name_a} has seen "
    + "the falling.",

    "{name_b} &mdash; if you want to thank {name_a} for something this week, thank "
    + "{name_a} for never once making you feel that your ambition was too much. In a "
    + "marriage of two campaigns, the gift of not-being-crowded-out goes unnoticed "
    + "precisely because it is always present. Name one specific moment &mdash; one "
    + "season, one campaign, one room &mdash; in which {name_a}'s steadiness beside "
    + "your running made the running possible. {name_a} will not know what to do "
    + "with the acknowledgment. Say it anyway.",
]

COLLISION = [
    "Now we come to the small repeating thing. It will be familiar to both of you, "
    + "even if you have never put it into language &mdash; because the two-Performance "
    + "collision is not a fight. Two Performances rarely have time for fights. The "
    + "collision is something slower, quieter, and more consequential. It is the "
    + "steady erosion of any rest in the marriage.",

    "Here is what is happening, stated plainly. Both of you have organized your "
    + "identity around demonstrated worth. Both of you are, in some register of the "
    + "self, always running &mdash; always producing, always visible, always counting "
    + "what the next week requires. And because both of you are running, neither of "
    + "you has the interior surplus to fully stop and simply <i>receive</i> the other. "
    + "The dinners become status updates: what was accomplished, what is next, what "
    + "recognition arrived or failed to arrive. The vacations become productive &mdash; "
    + "better workouts, sharper recovery, more reading, a faster version of the same "
    + "person returning to the same race. The Sundays do not become Sabbath, because "
    + "both of you are quietly counting what next week requires, and counting is "
    + "not resting.",

    "The Hebrews author names this dynamic with a precision that should be "
    + "uncomfortable for both of you. In Hebrews 4:9&ndash;11, he writes: "
    + "<i>So then, there remains a Sabbath rest for the people of God, for whoever "
    + "has entered God's rest has also rested from his works as God did from his. Let "
    + "us therefore strive to enter that rest.</i> Pause at the irony. The author calls "
    + "us to <i>strive</i> to enter <i>rest</i>. This is not a contradiction. It is "
    + "a diagnosis. The runner does not stop without effort. The Performance Campaign "
    + "cannot simply choose to rest the way a person with different wiring might simply "
    + "choose to rest. The stopping requires something that functions, for the runner, "
    + "almost like a discipline of resistance. Two runners in one marriage have built "
    + "a household in which no one is practicing the stopping.",

    "Jesus called his disciples from their fishing nets with an invitation recorded in "
    + "Mark 6:31: <i>Come away by yourselves to a desolate place and rest a while.</i> "
    + "The disciples were not, at this point, resting. They were so busy that they "
    + "had no time to eat. The Lord did not commend the busy-ness and ask them to "
    + "produce more efficiently. He called them away from the producing. The "
    + "two-Performance marriage has, with the best of intentions, arranged itself "
    + "so that no one ever calls either of you away from the producing. You are "
    + "both producing. You are both, in your own grammar, calling the other to "
    + "produce. The desolate place &mdash; the still, small room in which the "
    + "Campaign is not running &mdash; has gone uninhabited.",

    "Keller, in <i>Counterfeit Gods</i>, writes about workaholism as functional "
    + "idolatry &mdash; the arrangement of a life around the production of visible "
    + "results as a means of answering the deepest questions of worth and identity. "
    + "What he does not address directly, because it is rare enough to be almost "
    + "invisible, is what happens when <b>two workaholics build one household together.</b> "
    + "Two Performances in a marriage have not built a home with one altar to "
    + "achievement. They have built a home with two altars and no Sabbath. Both are "
    + "worshipping at the same shrine. Both are making the same offering. And the "
    + "question underneath both of their campaigns &mdash; <i>am I enough to be "
    + "remembered?</i> &mdash; is no closer to an answer than the day either "
    + "of them first started running.",

    "Here is the collision in slow motion. {name_a} has had a week in which something "
    + "significant was accomplished &mdash; something that cost real effort and produced "
    + "real results &mdash; and in the evening, over dinner, reaches for the one person "
    + "whose notice matters most. But {name_b} has had a week of their own. {name_b}'s "
    + "own campaign has been running, and {name_b}'s own significance trigger has been "
    + "firing, and {name_b} is, in that dinner, also reaching for the one person whose "
    + "notice matters most. Both of them are, at the same moment, casting the other as "
    + "audience. Neither of them is able to be the audience the other needs, because "
    + "both of them need an audience right now. The moment passes in warmth that is "
    + "slightly thinner than it looks, and neither of them names what just happened.",

    "{name_a} &mdash; the way out, in your grammar, begins with a single discipline: "
    + "to spend thirty seconds this week looking at {name_b} as a person rather than as "
    + "a fellow runner. Not at the campaign. Not at the accomplishments. At the person "
    + "who is, underneath the running, asking the same question you are asking. When you "
    + "notice the question in them &mdash; the particular flatness of a person whose "
    + "recognition has not yet arrived &mdash; do not try to fix it with encouragement "
    + "about the campaign. Be present to the question. That is a different thing, and "
    + "it is the thing {name_b} most needs from you.",

    "{name_b} &mdash; the same discipline applies, in the same grammar. When {name_a} "
    + "is running hard and reaching for your notice, the right move is not to "
    + "immediately shift to your own campaign. It is to stop, genuinely, for one minute, "
    + "and be the audience {name_a} needs. Not a cheerleader. Not a producer of "
    + "counter-evidence about your own week. A witness. Someone who can say: <i>I see "
    + "what you did. I see what it cost. I am not going anywhere.</i> One minute. "
    + "That is the length of a Sabbath this marriage can begin to practice.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be seasons &mdash; not often, but they will "
    + "come &mdash; when both campaigns have quietly retired. Not the campaigns visibly. "
    + "The campaigns keep running. The bodies keep producing. The calendars remain full "
    + "and the accomplishments keep accumulating and the recognition keeps arriving. But "
    + "something has changed. Neither of you feels anything when the recognition arrives. "
    + "The accomplishment lands and goes flat. The applause is real and the interior "
    + "is silent. This is the Quiet Exit &mdash; and in a two-Performance marriage, "
    + "it is the most dangerous pattern precisely because it looks, from every angle "
    + "including the inside, like business as usual.",

    "The church at Ephesus was, by all accounts, productive. They were doing "
    + "the right things. They were enduring, laboring, discerning. And yet the risen "
    + "Christ addresses them in Revelation 2:4&ndash;5 with words that should land "
    + "in this room: <i>But I have this against you, that you have abandoned the love "
    + "you had at first. Remember therefore from where you have fallen; repent, and "
    + "do the works you did at first.</i> The church at Ephesus had not stopped working. "
    + "They had stopped <i>loving.</i> They had maintained the form of the first works "
    + "while quietly losing the interior that had originally animated them. A two-"
    + "Performance marriage in Quiet Exit looks exactly like Ephesus: productive, "
    + "commendable, and quietly abandoned on the inside.",

    "When both of you are in Quiet Exit simultaneously &mdash; both still producing, "
    + "both still receiving recognition, both still going through the motions of "
    + "a marriage &mdash; the symptoms are specific. The dinner conversations become "
    + "efficient. You coordinate logistics with precision and connect about almost "
    + "nothing. The physical proximity is maintained. The household functions. Friends "
    + "looking in would see nothing wrong. But both of you know, somewhere below the "
    + "level of words, that the interior has vacated. That you are sharing a calendar "
    + "and a campaign schedule but no longer sharing the question underneath either. "
    + "The marriage is running. The runners are not, in any sense that matters, "
    + "still here.",

    "D. Martyn Lloyd-Jones, writing on spiritual depression, observed something "
    + "directly relevant here: the most dangerous form of flatness is not the kind "
    + "that announces itself. It is the kind the sufferer does not recognize as "
    + "flatness, because the machinery keeps moving, and the machinery moving has "
    + "always been the signal that things are well. The Performance cannot easily "
    + "see the Quiet Exit from the inside, because the running looks exactly like "
    + "health. What is missing is not visible on the calendar. What is missing is "
    + "the person. The {name_a} who exists when there is nothing to produce. The "
    + "{name_b} who is still asking, underneath the running, <i>am I enough to "
    + "be remembered &mdash; by you, specifically, apart from everything I have "
    + "done?</i> These are the people the marriage most needs back.",

    "What to do when you can still see what is happening:",

    "<b>One of you names the Quiet Exit out loud.</b> This is harder than it sounds, "
    + "because neither of you will want to name it as failure, and the Campaign's "
    + "instinct is to treat a problem as a campaign to be solved. This is not a campaign. "
    + "It is a confession. Whichever one of you notices first &mdash; whose love for "
    + "the marriage is, in that moment, larger than the Campaign's resistance &mdash; "
    + "says, without organizing it: <i>I think we have both been running, and I think "
    + "we may have lost each other somewhere on the track. I want to stop. I do not "
    + "know how to stop. But I want to try.</i> That sentence is not efficient. It is "
    + "not productive. It is not the kind of thing that goes on a resume. It is "
    + "also the most important sentence either of you has said in months.",

    "<b>Stop producing, together, for one hour.</b> Not the Sabbath hour that gets "
    + "populated with plans for next week. Not the vacation that becomes a better "
    + "version of the workday. One hour in which neither of you accomplishes anything, "
    + "and neither of you apologizes for accomplishing nothing. You may need to schedule "
    + "it, because the Campaign will not leave it open. Schedule it. Then sit in it "
    + "together. The goal is not a productive conversation. The goal is to be "
    + "present, unproductively, with the person you married.",

    "<b>Pray for each other, by name, for the thing underneath the running.</b> Not "
    + "for the campaign's success. For the question. <i>Lord, {name_b} is asking "
    + "whether they are enough to be remembered. Would you answer that question in "
    + "a way that I cannot &mdash; not through the next accomplishment, but through "
    + "the love that knew their name before any campaign began?</i> Or: <i>Lord, "
    + "{name_a} keeps running because stopping feels like risking the question. "
    + "Would you make the stopping safe? Would you be present in the quiet in a "
    + "way that makes the quiet bearable?</i>",

    "<b>Neither of you is the problem.</b> The Quiet Exit is not the truest thing "
    + "about either of you. It is an old mechanism doing what it was built to do "
    + "&mdash; protecting a significance that was always going to be given rather "
    + "than earned, in a world that trained both of you to earn it anyway. The "
    + "truest thing about both of you is that you chose each other, and you are "
    + "still here, and two runners who learn, slowly and with genuine effort, "
    + "to stop and look at each other rather than at the next horizon are building "
    + "something the campaign alone could never have produced: a home where "
    + "the interior is actually inhabited, and where both people inside it "
    + "are known.",
]

COMMITMENTS_INTRO = [
    "What follows are eight commitments &mdash; four from {name_a}, four from {name_b}. "
    + "They are not vows in the legal sense. They are the small daily practices that, "
    + "offered to each other freely and kept with patience, begin to change the "
    + "temperature of a home across months and years. For the two-Performance marriage, "
    + "the pastoral direction is the same for both of you, and it reverses the "
    + "mechanism's entire logic: <i>lead with stopping, not running.</i> The commitment "
    + "that matters most, for both of you, is this: two hours this week, with your "
    + "spouse, producing nothing, and letting that be enough. Read each commitment slowly. "
    + "If you cannot say one of them in good faith yet, do not say it. Honesty about "
    + "what you cannot yet offer is more useful to this marriage than performance "
    + "of what you think you should.",
]

A_COMMITMENTS = [
    ("To spend two hours with you producing nothing.",
     "{name_b}, I commit to spending two hours this week with you in which neither of "
     + "us is accomplishing anything, and I will not treat that time as a loss. I will "
     + "not fill it with plans. I will not mentally rehearse next week's campaign. I "
     + "will be present to you, unproductively, and I will practice letting that be "
     + "enough. The Campaign in me will resist this. I will do it anyway, because the "
     + "marriage I want to build with you is not only a chronicle of our accomplishments. "
     + "It is a room where we have learned to stop."),

    ("To see you apart from your campaign.",
     "{name_b}, I commit to looking at you, once this week, not as a fellow runner "
     + "but as a person. Not at what you have built or are building. At you. When I "
     + "notice the question in you &mdash; the significance trigger, the particular "
     + "quiet of a person whose recognition has not yet arrived &mdash; I will not "
     + "try to solve it by pointing to your accomplishments. I will be present to the "
     + "question. I will say: <i>I see you. Not the campaign. You.</i> That is a "
     + "different sentence. I will practice it."),

    ("To name what I am running from, not only what I am running toward.",
     "{name_b}, when I feel the Campaign accelerating &mdash; when the drive to "
     + "produce is running harder than the situation requires &mdash; I commit to "
     + "telling you, in one sentence, what question the running is answering. Not "
     + "the goals. The question. <i>I think I am running because the question "
     + "fired again.</i> That sentence is not efficient. It is not impressive. "
     + "It is true, and the truth is what this marriage needs from me more "
     + "than any campaign."),

    ("To call the Quiet Exit before the campaign hides it.",
     "{name_b}, when I notice that I am still producing but no longer present "
     + "&mdash; when the accomplishments are real and the interior has quietly gone "
     + "flat &mdash; I commit to naming it before the exit becomes a destination. "
     + "Not with the organized explanation. With the honest admission: <i>I think "
     + "I have been running, and I think I may have left you behind. I want to "
     + "come back. Can we stop together for a while?</i> Those words, said while "
     + "it is still true, are worth more than any result I could produce alone."),
]

B_COMMITMENTS = [
    ("To spend two hours with you producing nothing.",
     "{name_a}, I commit to spending two hours this week with you in which the "
     + "campaign is not running, and I will practice not apologizing for it. I "
     + "will not use the time to think about the next thing. I will be with you "
     + "&mdash; unproductively, unhurriedly, without an agenda &mdash; because I "
     + "believe that the best thing I can build with you is not a longer resume but "
     + "a marriage in which both of us have learned to inhabit the same room at "
     + "the same time without needing the room to produce something."),

    ("To be your audience, not your fellow runner, for one moment this week.",
     "{name_a}, I commit to stopping my own campaign, once this week, long enough "
     + "to be the witness you actually need. Not a co-achiever. A witness. Someone "
     + "who can say: <i>I see what you built. I see what it cost. I am not "
     + "measuring it against my own week.</i> The Campaign in me will want to "
     + "respond to your running with my own. I will resist that, because what "
     + "you need in those moments is not another campaign. You need one person "
     + "who has genuinely stopped."),

    ("To name what I am running from, not only what I am running toward.",
     "{name_a}, when the drive to produce is running harder than the situation "
     + "requires &mdash; when I feel the anxiety of a question I have not named "
     + "&mdash; I commit to telling you what is underneath the running. One "
     + "sentence, without dressing it up: <i>I think the question fired. I think "
     + "I am trying to answer it by producing more. I want to stop for a minute "
     + "and let you know what is actually happening.</i> You deserve to know what "
     + "is underneath the campaign. I will practice telling you."),

    ("To call the Quiet Exit before the campaign hides it.",
     "{name_a}, when I notice that the interior has gone flat &mdash; that "
     + "the running is still happening but the person behind it has quietly "
     + "vacated &mdash; I commit to naming it before the exit has a destination. "
     + "I will not wait until I have a tidy explanation. I will say: <i>I "
     + "think I have been going through the motions. I think we may have lost "
     + "each other somewhere on the track. I want to stop. Will you stop "
     + "with me?</i> That sentence is an act of faith in this marriage. "
     + "I will practice it."),
]

PRAYER = [
    "Father,",

    "You set these two runners next to each other, and you knew exactly what you were "
    + "doing. You knew that two Performance Campaigns would build something visible and "
    + "real &mdash; a marriage that accomplishes, that contributes, that makes rooms "
    + "take notice. You also knew that two people whose identity is organized around "
    + "demonstrated worth would, between them, build a home where both altars are "
    + "always lit and the Sabbath is always deferred. You knew all of it before "
    + "either of them said yes. You put them together anyway, and we trust "
    + "that you knew what you were doing.",

    "Teach them the stopping that the mechanism resists. Teach {name_a} to spend "
    + "one hour this week with {name_b} in which nothing is produced &mdash; in "
    + "which the Campaign is at rest, the question is allowed to be present without "
    + "being immediately answered by the next achievement, and the person behind "
    + "the portfolio is simply here. Remind {name_a} of what you said through Isaiah: "
    + "<i>I have engraved you on the palms of my hands.</i> Not engraved on a "
    + "credential. On the palms of his hands. {name_a} does not have to produce "
    + "anything to remain there. The engraving does not depend on the campaign.",

    "Teach {name_b} the same courage in the same grammar. One stopped hour, with "
    + "{name_a}, producing nothing. Let {name_b} discover that the question &mdash; "
    + "<i>am I enough to be remembered?</i> &mdash; does not grow louder in "
    + "the stopping. Let the stopping become, over time, the evidence that the "
    + "answer has already been given. Not by the accomplishments. By the cross, "
    + "where Christ stood before the Father and said: <i>This one. Known. Named. "
    + "Kept.</i> Before any campaign had a single entry.",

    "When the Quiet Exit is assembling &mdash; two campaigns still running, two "
    + "interiors quietly gone flat, two people sharing a calendar and no longer "
    + "sharing the question &mdash; wake one of them first. Give them the sentence "
    + "the Campaign cannot write for them: <i>I think I have lost you somewhere "
    + "on the track. I want to stop. Can we stop together?</i> Let the one who "
    + "goes first discover that the other one has also been waiting to stop. "
    + "Because they have. The Campaign always is, when someone else goes first, "
    + "because going first is the thing the Campaign has never been "
    + "willing to do alone.",

    "And where each of them asks &mdash; in the interior quiet of an afternoon "
    + "when there is nothing to produce &mdash; <i>am I enough to be remembered?</i> "
    + "Let them hear the answer that was spoken before the question was formed. "
    + "In Christ, at the cross, in the specific love of a God who chose them "
    + "before the foundation of the world and inscribed them on the palms "
    + "of his hands: <i>Yes. You are enough. You were always enough. "
    + "You were enough before the first campaign began.</i>",

    "Make their home a room where two runners have learned something harder "
    + "than running: how to stop. How to sit across from each other with nothing "
    + "to show, and let that be the best thing they built today. And when they "
    + "are old, and the campaigns have quieted, and the recognition has become "
    + "less important than it once was &mdash; let them look back and see that "
    + "the marriage they made between two runners became, in the end, a Sabbath. "
    + "A real one. Not a Sabbath worked toward as the next campaign. A Sabbath "
    + "received, together, as a gift.",

    "In the name of the One who said <i>come to me, all who labor and are "
    + "heavy laden, and I will give you rest</i> &mdash; and who has been "
    + "offering that rest, without condition, since before either of them "
    + "first learned to run.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages "
    + "that follow are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, somewhere "
    + "quiet, with no children in the room and no phones on the table. There are six "
    + "rounds, and they build on each other. Resist the temptation to skip ahead. "
    + "Start at Round One even if it feels too light &mdash; for a two-Performance "
    + "marriage, the lightness at the beginning is not an indulgence. It is the "
    + "point. You are practicing the stopping.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did not "
    + "read answers first, in full, without interruption. Then the reader answers "
    + "the same question. Then you move on. You do not have to finish all six rounds "
    + "in one evening &mdash; two or three rounds, taken seriously and without "
    + "rushing, is often better than completing all of them in one sitting. "
    + "Save the rest for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. You may not love "
    + "everything you hear. Stay with it. The point of this is not to evaluate "
    + "each other's performance &mdash; notice the word &mdash; but to be known "
    + "by the one person whose knowing matters most, and to do the patient "
    + "work of knowing them in return.",
]

ROUND_1 = [
    ("hypothetical",
     "If our marriage were a season of a race &mdash; training, mid-race, the final "
     + "stretch, the finish line, the day after &mdash; which season would it be right "
     + "now, and what would be true about both runners?",
     "Two Performances. Let the metaphor say what plain language resists. Be specific "
     + "about the season. The answer will tell you something about where you both are."),
    ("observation",
     "What is something I did or built this week that you noticed and did not "
     + "mention to me?",
     "Not a complaint. Not a compliment, necessarily. A small noticing. Two "
     + "Performances often see each other's work more clearly than they say. "
     + "This question gives the noticing a voice."),
    ("playful",
     "If you had to describe our marriage as a specific kind of campaign &mdash; "
     + "a marathon, a sprint, a relay, a long-distance expedition &mdash; what "
     + "would you pick, and who would be carrying the baton right now?",
     "Yes, really. Let the first answer surface. The metaphor will tell you "
     + "something neither of you expected."),
]

ROUND_2 = [
    ("fill-in-blank",
     "I don't think I tell you this enough &mdash; I am genuinely in awe of the way "
     + "God made you capable of _______. That capacity in you has made me _______ in "
     + "ways I would not have been if I were running this alone.",
     "Two blanks. The second one is the harder one. 'Stronger' is too easy. "
     + "The version of yourself that only exists because this marriage exists "
     + "&mdash; name that version."),
    ("observation",
     "Name one thing you have watched me carry this year &mdash; one campaign, one "
     + "cost, one effort &mdash; that I probably never mentioned to you, and that "
     + "you knew about anyway.",
     "Two Performances often see each other's hidden cost more clearly than they "
     + "acknowledge. This is the question that makes the invisible visible."),
    ("one-word",
     "If you had to choose one word to describe what it feels like when I stop "
     + "my campaign long enough to simply be with you &mdash; no agenda, no "
     + "phone, no next thing &mdash; what word would it be?",
     "One word, said out loud. Then explain it without editing yourself. The "
     + "Performance's answer to this question is almost never what the "
     + "Performance expects."),
]

ROUND_3 = [
    ("forward-looking",
     "Ten years from now, when we look back on this season of our marriage, what "
     + "is the one thing you most hope we will have figured out &mdash; not in "
     + "our careers, but in the room between us?",
     "Not what you wish had been different. What you want, ten years out, to "
     + "be able to say you actually built together. Name it specifically."),
    ("theological",
     "Where, in the last month, have you seen God specifically at work in me "
     + "&mdash; not in what I produced, but in who I am becoming?",
     "Name it with the specificity of a witness. 'More patient' is too general. "
     + "The particular moment, the specific thing &mdash; that is witness. "
     + "That is what the Performance most needs to hear."),
    ("shared-identity",
     "Finish this sentence three times: 'We are the kind of couple who _______.' "
     + "Give one playful answer, one honest answer, and one aspirational answer.",
     "The 'we' is the point. The aspirational one is what you are running toward "
     + "together, not apart. Notice what each of you says."),
]

ROUND_4 = [
    ("strength",
     "What is something I carry for this marriage that you would have to learn "
     + "to carry for yourself if I were not here?",
     "Two Performances often assume the other one already knows their contribution. "
     + "They rarely do, in the specific way. Stay with the answer. "
     + "Say it in full, without qualifying it."),
    ("fill-in-blank",
     "One of the gifts of being married to you is that I get to be _______ in ways "
     + "I never would have been on my own &mdash; and the version of myself that "
     + "exists because of this marriage is better than any version I would have "
     + "managed alone because of your _______.",
     "A version of yourself, and a quality of the marriage, that only exist because "
     + "the marriage exists. Name both specifically enough that they could not "
     + "apply to anyone else."),
    ("observation",
     "Name one moment in our story where you knew, with no doubt, that we had "
     + "built something together that neither of us could have built alone.",
     "Tell the whole story. Do not summarize. The remembering, done in detail "
     + "and out loud, is itself one of the best things two runners can do together."),
]

ROUND_5 = [
    ("hard",
     "When was the last time you felt like you were running and I was not watching "
     + "&mdash; not distracted, not unkind, just not watching &mdash; and what "
     + "would you have needed me to do differently?",
     "One moment. Named carefully. Heard without defending. This is the question "
     + "that goes to the center of what the two-Performance marriage most "
     + "needs to practice."),
    ("profile-aware",
     "When you sense that I have slipped into campaign mode and cast you as my "
     + "audience rather than my spouse &mdash; when you can feel the running more "
     + "than the person &mdash; what is one thing you wish you could say or do "
     + "in that moment that you haven't yet?",
     "You both know the mechanism now. This question names what the other person "
     + "wishes they could offer. Hear it without defending. It is a gift."),
    ("theological",
     "What is one thing you are carrying right now &mdash; a fear, a question, "
     + "something about us or about the running &mdash; that you have not yet "
     + "brought to me, and what has kept you from bringing it?",
     "Not an accusation. An invitation. Answer it unfinished. Hear the answer "
     + "without turning it into a campaign to be solved. Just receive it."),
]

ROUND_6 = [
    ("blessing",
     "Place your hand on your spouse's hand. Say their name. Then say: "
     + "'I am not here because of what you have built. I am here because of "
     + "who you are when you are building nothing. You are enough. You have "
     + "always been enough.' Say it slowly. Let them say it back.",
     "The Campaign in both of you will want to qualify this. Do not. Say it "
     + "as written, slowly, by name. The unedited version is the point. "
     + "This is the answer to the question underneath all the running."),
    ("prayer",
     "Pray for each other &mdash; not silently, not generally, but out loud "
     + "and by name. One sentence is enough. Pray for the thing they told you "
     + "in Round Five &mdash; not for the campaign's success, but for the "
     + "person underneath the campaign.",
     "The closing of the date. Do not skip. Two Performances who pray for "
     + "each other's question &mdash; not each other's output, but each "
     + "other's question &mdash; have done something the mechanism alone "
     + "cannot do. The prayer is itself the stopping."),
]


def _render(text, name_a, name_b):
    return text.format(name_a=name_a, name_b=name_b)


def build(sub_a, sub_b) -> bytes:
    """Generate the Performance+Performance couples walkthrough PDF.

    sub_a: the submission of one Performance Campaign spouse
    sub_b: the submission of the other Performance Campaign spouse

    Names are sorted alphabetically so name_a <= name_b.
    """
    ensure_fonts()
    S = make_styles()

    raw_a = _first_name(sub_a, "Partner A")
    raw_b = _first_name(sub_b, "Partner B")

    # Sort alphabetically so A <= B (same-mechanism pair: order is arbitrary)
    if raw_a.lower() <= raw_b.lower():
        name_a, name_b = raw_a, raw_b
    else:
        name_a, name_b = raw_b, raw_a

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
        "A counselor\u2019s read of two campaigns<br/>and the marriage between them.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("PREPARED FOR", S["CoverProfileLabel"]))
    story.append(Paragraph(f"{name_a} &nbsp;&amp;&nbsp; {name_b}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_a.upper()}</b></font><br/>"
                "Performance Campaign &middot; Quiet Exit<br/>"
                f"<font size=9 color='#6b6862'>Significance &middot; Am I enough to be remembered?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_b.upper()}</b></font><br/>"
                "Performance Campaign &middot; Quiet Exit<br/>"
                f"<font size=9 color='#6b6862'>Significance &middot; Am I enough to be remembered?</font>",
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
        "<i>\u201cLet us therefore strive to enter that rest.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "Hebrews 4:11",
        ParagraphStyle("cqa", fontName="Inter", fontSize=9, leading=14,
                       textColor=MUTED, alignment=TA_CENTER)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: OPENING ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "Two campaigns, one home.",
                   "Why this pairing exists, and what you are both about to read.")
    for p in OPENING:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 2: YOUR TWO SHAPES ──
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TWO SHAPES",
                   "Side by side, on paper.",
                   "Two profiles that look alike \u2014 and the single stopping that matters most.")
    for p in TWO_SHAPES_INTRO:
        story.append(Paragraph(R(p), S["BodyJ"]))
    side_by_side = Table(
        [[
            _profile_card(S, name_a, ACCENT,
                          "Significance", "Am I enough to be remembered?",
                          "Performance Campaign", "Quiet Exit"),
            "",
            _profile_card(S, name_b, ACCENT_HER,
                          "Significance", "Am I enough to be remembered?",
                          "Performance Campaign", "Quiet Exit"),
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

    # ── SECTION 3: GIFT A TO B ──
    section_header(story, S, f"SECTION THREE  \u00b7  {name_a.upper()}\u2019S GIFT TO {name_b.upper()}",
                   f"What {name_a} gives {name_b}.",
                   "A witness who already knows the cost of the running.")
    for p in GIFT_TO_A:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4: GIFT B TO A ──
    section_header(story, S, f"SECTION FOUR  \u00b7  {name_b.upper()}\u2019S GIFT TO {name_a.upper()}",
                   f"What {name_b} gives {name_a}.",
                   "A person who will not be diminished by the campaign.")
    for p in GIFT_TO_B:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5: THE COLLISION ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Two campaigns, no Sabbath.",
                   "The small repeating thing that makes no sound.")
    for p in COLLISION[:4]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The erosion, in slow motion.",
                   "And the way out, for each of you in your own grammar.")
    for p in COLLISION[4:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6: THE HARDER PICTURE ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When both campaigns retire in spirit.",
                   "The Quiet Exit, and what to do while you can still see it.")
    for p in BOTH_BREAK[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do, while you can still see it.",
                   "Four practices for the breakdown, in order.")
    for p in BOTH_BREAK[5:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 7: COMMITMENTS ──
    section_header(story, S, "SECTION SEVEN  \u00b7  COMMITMENTS",
                   "Eight small daily practices.",
                   "Four from each of you. Lead with stopping, not running.")
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
                   "Four commitments, in the second voice, for the first to receive.")
    story.append(Paragraph(f"FROM {name_b.upper()}, TO {name_a.upper()}", S["CommitLabelHer"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT_HER,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for commit_name, commit_body in B_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(commit_name, S["H3Her"]),
            Paragraph(R(commit_body), S["CommitBody"]),
        ]))
    story.append(PageBreak())

    # ── SECTION 8: PRAYER ──
    section_header(story, S, "SECTION EIGHT  \u00b7  A PRAYER",
                   "For the two of you.",
                   "Pray it together, if you can. Out loud, if you can.")
    for line in PRAYER:
        story.append(Paragraph(R(line), S["BlockQuote"]))
    story.append(PageBreak())

    # ── SECTION 9: DATE NIGHT ──
    section_header(story, S, "SECTION NINE  \u00b7  DATE NIGHT",
                   "Six rounds, taken slowly.",
                   "A conversation designed to be spoken between you, not run through.")
    for p in DATE_NIGHT_OPENING:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    rendered_round = lambda r: [(kind, R(q), note) for (kind, q, note) in r]

    _render_round(story, 1, rendered_round(ROUND_1),
                  "Warm up.",
                  "The stopping is the point. Start here even if you\u2019d rather skip ahead.")
    story.append(PageBreak())
    _render_round(story, 2, rendered_round(ROUND_2),
                  "Notice the good.",
                  "Specific witness. The kind that lands because it could not have been said by anyone else.")
    story.append(PageBreak())
    _render_round(story, 3, rendered_round(ROUND_3),
                  "Wonder together.",
                  "About us, about God, about the life we are making between the campaigns.")
    story.append(PageBreak())
    _render_round(story, 4, rendered_round(ROUND_4),
                  "Sit in the strength.",
                  "Let yourselves feel the actual weight of what you\u2019ve built together.")
    story.append(PageBreak())
    _render_round(story, 5, rendered_round(ROUND_5),
                  "Tell the truth.",
                  "The harder ones. Asked gently. Heard without turning them into a campaign.")
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
        "I am not here because of what you have built.<br/>"
        "I am here because of who you are when you are building nothing.<br/>"
        "You are enough. You have always been enough.",
        closing_style))

    doc.build(story)
    return finalize_buffer(buf)


# ── STANDALONE TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import io
    import os

    class FakeSub:
        primary_mechanism = "CAMP"
        primary_breakdown = "QE"
        primary_trigger = "SIG"
        core_question = "REM"
        name = "Andrew Performance"

    class FakeSubB:
        primary_mechanism = "CAMP"
        primary_breakdown = "QE"
        primary_trigger = "SIG"
        core_question = "REM"
        name = "Claire Performance"

    pdf_bytes = build(FakeSub(), FakeSubB())
    out_path = os.path.join(os.path.dirname(__file__), "performance_performance_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages via pypdf
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
    except Exception:
        page_count = pdf_bytes.count(b"%%Page:")

    # Section Three snippet
    snippet = GIFT_TO_A[0][:200]

    print(f"DONE: performance_performance.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Output:   {out_path}")
    print(f"Pages: {page_count}")
    print(f"Section Three snippet: {snippet}")
