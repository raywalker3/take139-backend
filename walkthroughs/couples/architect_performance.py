"""Couples Walkthrough — Architect + Performance Campaign.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where one spouse is an Architect and the
other is a Performance Campaign. First names are substituted from the submissions:
    {name_arch}  -> the Architect spouse's first name
    {name_camp}  -> the Performance Campaign spouse's first name

Spouse A (Architect): planner; trigger Disrespect; core question "Am I protected?"
Spouse B (Performance Campaign): runner, achiever; trigger Significance;
    core question "Am I enough to be remembered?"

The classic high-achieving couple — formidable from outside, each driven by a
different wound underneath: the Architect by fear of disorder, the Performance
by fear of being unseen.
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


# ──────────── PROSE — uses {name_arch} and {name_camp} placeholders ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small repeating ones"
    " \u2014 the same disappointment wearing slightly different clothes, three or four times"
    " a week, year after year, until both people have quietly forgotten what they were"
    " originally hoping for. You are not the kind of couple that breaks obviously. You are"
    " the kind that can appear, from every external angle, like one of the most formidable"
    " marriages in your circle. Both of you produce. Both of you plan. Both of you know"
    " how to lead a room. The question this document is going to press on is not whether"
    " the output is real. It is.",

    "The question is what is driving the output. And whether, in this marriage, each of you"
    " knows what the other is actually running on.",

    "What follows is a counselor\u2019s read of the small repeating rocks in your particular"
    " marriage. Not the dramatic failures, which you would have addressed by now. The small"
    " ones. The ones that happen on a Thursday evening when the calendar is full and one of"
    " you needs to be seen and the other needs the plan to hold, and neither of you quite"
    " gets what you came for. The ones neither of you would think to bring to a counselor,"
    " because by Friday the week has moved on.",

    "Here is what I want to do for you. I will name what each of you brings the other that"
    " you could not have built alone \u2014 the genuine, theological gift your two shapes form"
    " together. Then I will name the collision your two questions create in the specific way"
    " it shows up in your marriage. Then I will name the worst case \u2014 when the Attorney"
    " and the runner are both in the room at the same time \u2014 and what to do then. Then"
    " I will hand each of you three commitments, not as rules but as the kind of small daily"
    " practices that, over years, change the temperature of a home.",

    "Read it together if you can. If not, read it separately and then sit down with it."
    " Argue with what does not fit. Stay with what does. The goal is not insight; the goal"
    " is a marriage in which the small repeating rocks become smaller, and less repeating,"
    " and eventually a part of the landscape you can both look at honestly together.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on paper,"
    " side by side. Most couples never see their two profiles next to each other at once."
    " You are about to.",
]

TWO_SHAPES_BODY = [
    "{name_arch}, you are an <b>Architect</b> whose body reads disrespect as an alarm and"
    " whose deepest question is whether you are protected. You build structures because you"
    " believe, in your bones, that suffering is largely a function of insufficient planning."
    " When the building fails, an <b>Attorney</b> takes the floor and begins to litigate"
    " \u2014 not to win an argument for its own sake, but to prove that the perimeter is"
    " still sound, that the person in charge of the blueprint has not been dismissed.",

    "{name_camp}, you are a <b>Performance Campaign</b> whose body reads invisibility as an"
    " alarm and whose deepest question is whether you are enough to be remembered. You have"
    " learned that achievement is the most reliable path to being noticed \u2014 that if you"
    " can build something extraordinary and visible, you cannot be ignored, and if you cannot"
    " be ignored, you cannot be forgotten. When the campaign fails to produce the verdict,"
    " an <b>Attorney</b> takes the floor in you as well, presenting the r\u00e9sum\u00e9 as"
    " evidence for the love it was never going to be able to purchase.",

    "Notice what these two profiles share on the surface, and notice what they do not share"
    " underneath. You both produce. You both plan. You both have a long record of things"
    " built and achieved. From the outside, this marriage looks like two people running in"
    " the same direction. From the inside, {name_arch} is building because the fear is"
    " disorder, and {name_camp} is building because the fear is being unseen. Both fears"
    " produce output. They do not produce the same hunger.",

    "{name_arch}\u2019s question is <i>am I protected?</i> \u2014 meaning, will the things"
    " I have planned hold? The Architect can be at peace if the plan holds even when no one"
    " notices. {name_camp}\u2019s question is <i>am I enough to be remembered?</i> \u2014"
    " meaning, will the things I have produced be enough? The Performance cannot be at peace"
    " if the producing happens unnoticed. These look like the same drive from a distance."
    " They are not the same wound.",

    "What this pairing shares underneath the two questions is an unusual vocabulary of goals,"
    " structure, and output. The Architect respects the runner\u2019s ability to produce."
    " The runner respects the Architect\u2019s ability to build something that holds. There"
    " is genuine admiration here, often quietly operative and rarely named. The friction"
    " between you is real, but the foundation of mutual respect is genuinely good. What this"
    " document is going to ask is whether that mutual respect has been doing the work that"
    " only intimacy can do.",
]

GIFT_TO_ARCH = [
    "{name_camp} gives {name_arch} something the Architect\u2019s own mechanism almost"
    " never produces for itself: <b>a witness to the work.</b>",

    "The Architect builds because building is the vocabulary of love and safety. But the"
    " Architect\u2019s mechanism is characteristically inward \u2014 the satisfaction is in"
    " the structure holding, not in being seen holding it. What this means, in practice, is"
    " that {name_arch} often works without acknowledgment and has learned not to require it."
    " The plan functions; that is its own reward. But there is a cost to this. A person who"
    " is never seen doing the work eventually stops knowing whether the work matters to"
    " anyone but himself.",

    "{name_camp}, by virtue of being a Performance Campaign, pays attention to what is being"
    " built. The Campaign\u2019s sensitivity to visibility \u2014 to what is achieved, what"
    " is demonstrated, what leaves a mark \u2014 makes {name_camp} one of the few people"
    " in {name_arch}\u2019s life who actually notices the architecture. Who sees the"
    " contingency plan that saved the month. Who registers that the problem was solved before"
    " it became a crisis. Who says, in some form, <i>I saw what you did there, and it was"
    " remarkable.</i> To a different mechanism, this quality in {name_camp} would feel like"
    " an appetite for recognition. To the Architect, it is something genuinely different:"
    " a mirror held up to work that deserved to be seen.",

    "The theological word that belongs here is <i>honor.</i> Paul writes in Romans 13:7 that"
    " we are to give honor to whom honor is owed. {name_camp} is constitutionally inclined"
    " to honor what has been built \u2014 to name it, to notice it, to call it what it is."
    " For {name_arch}, who has often labored without acknowledgment and told himself it does"
    " not matter, this is an unusual and nourishing thing. The Architect built to protect."
    " The Performance sees what protecting costs. In a marriage where both of you speak"
    " primarily in the language of output, {name_camp} is the one who occasionally stops"
    " the campaign long enough to look at what {name_arch} has constructed and say:"
    " <i>this is good work.</i>",

    "{name_arch} \u2014 if you want to thank {name_camp} for something this week, thank"
    " them for this. Name one specific thing they have noticed and named in you that you"
    " would not have named yourself. The Performance\u2019s gift is visibility \u2014 and"
    " while the Campaign sometimes turns that gift inward, toward its own need to be seen,"
    " it is also genuinely capable of turning it outward, toward you. Receive it.",

    "{name_camp} \u2014 what {name_arch} receives from you, when you stop the campaign long"
    " enough to name what he has built, is more than acknowledgment. It is the experience"
    " of being seen doing the thing that, for him, constitutes love. You may not have known"
    " you were giving that. You were.",
]

GIFT_TO_CAMP = [
    "{name_arch} gives {name_camp} something the Performance Campaign almost never builds"
    " for itself: <b>a structure that does not require the Campaign to earn its place.</b>",

    "The Performance Campaign is, by nature, a person who works for standing. Everything the"
    " Campaign builds is, at some level, an argument \u2014 a demonstration that the person"
    " doing the building is worth noticing, worth keeping, worth the room they are"
    " occupying. This is exhausting in ways the Campaign rarely admits, because the Campaign"
    " has been running long enough that the exhaustion has become background noise. What the"
    " Campaign rarely experiences is a structure it did not have to earn its way into.",

    "{name_arch}, by virtue of being an Architect, builds structures that do not require"
    " constant demonstration. The plan holds whether or not {name_camp} performed today."
    " The calendar functions whether or not the campaign produced something visible this"
    " week. The contingencies are in place regardless of whether the runner was impressive"
    " at the last meeting. For {name_camp}, who has spent years living in structures that"
    " required ongoing demonstration to remain in, the Architect\u2019s unconditional"
    " structuring is \u2014 when it is received for what it actually is \u2014 a form of"
    " rest the Campaign has rarely known.",

    "The theological word for what {name_arch} gives {name_camp} is <i>grace.</i> Not grace"
    " as sentiment, but grace in its precise meaning: an unearned gift, given to the"
    " recipient not because of their performance but because of the giver\u2019s choice."
    " The Architect does not plan because the Campaign earned it. The Architect plans"
    " because planning is how the Architect loves. When {name_camp} receives the plan as"
    " grace rather than as pressure, the Campaign gets the thing it has been running toward"
    " without having to run: a place in the structure that was prepared before the"
    " performance began.",

    "{name_camp} \u2014 if you want to thank {name_arch} for something this week, thank"
    " them for this. Name one specific thing {name_arch} built, planned, or held in place"
    " that you did not have to manage because they managed it. The thing you walked into"
    " rather than constructed. The Architect\u2019s love language is the trellis. You have"
    " been growing on it. Name it.",

    "{name_arch} \u2014 what {name_camp} receives from you, when the structure simply holds,"
    " is the experience of being in a room that does not require them to earn their place."
    " The Campaign rarely gets to inhabit rooms like that. Yours is one of them. That is"
    " a gift of considerable weight, even when it is not named.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you,"
    " even if you have never put a name on it.",

    "{name_arch}\u2019s core question is <i>am I protected?</i> {name_camp}\u2019s"
    " is <i>am I enough to be remembered?</i> These are not opposed in theory. In the"
    " daily mechanics of a marriage, they ask for different things from the same person,"
    " and the asking regularly misfires.",

    "Protection wants reliability, structure, the sense that the plan is holding. When"
    " {name_arch} is anxious, he reaches for systems: the schedule, the contingency, the"
    " list, the blueprint for the next season. He is, in his own grammar, putting his arms"
    " around the family. What he requires of {name_camp} in those moments is"
    " cooperation with the structure \u2014 not necessarily enthusiasm, but adherence."
    " The plan is the love. The plan holding is the proof that the people in the plan"
    " are safe.",

    "Significance wants attention, the felt sense of being seen as a singular person, not"
    " as a function within someone else\u2019s system. When {name_camp} is anxious, they"
    " do not reach for structure \u2014 they reach for a moment in which they are"
    " unmistakably the subject of someone\u2019s full attention. To {name_camp}, the"
    " experience of being administered \u2014 of being a node in {name_arch}\u2019s"
    " well-constructed network \u2014 is not safety. It is precisely the thing the"
    " Campaign is running from: being one among many, replaceable, unnoticed.",

    "Here is the collision in slow motion. {name_arch}, trying to secure the family on a"
    " weeknight, addresses {name_camp} as a piece of the system: the dinner timing, the"
    " calendar item, the follow-up that needs to happen. He is, in his mind, loving by"
    " holding the perimeter. {name_camp} experiences it as being addressed as a function"
    " rather than as a person. The significance trigger fires: <i>I am being treated as"
    " though I am replaceable.</i>",

    "{name_camp} does not say so immediately. The Campaign\u2019s first move is not to"
    " name the wound \u2014 it is to produce harder. To accomplish something visible. To"
    " demonstrate worth that cannot be dismissed. So {name_camp} goes into campaign mode:"
    " takes on another project, stays later, produces something impressive. To {name_arch},"
    " who was hoping for cooperation with the current plan, this does not read as"
    " <i>they are hurting.</i> It reads as <i>they are expanding beyond the blueprint.</i>"
    " His trigger fires: <i>disrespect. The plan is not being honored.</i> The Attorney"
    " takes the floor.",

    "Now both of you are in your mechanisms. {name_arch} is litigating the violation of the"
    " structure. {name_camp} is producing harder and presenting the résumé as evidence"
    " that they deserve to be seen rather than administered. The conversation that follows"
    " does not address the actual wound in either of you, because both of you are speaking"
    " a language the other\u2019s mechanism cannot hear. The Architect hears the Campaign"
    " as self-promotion. The Campaign hears the Attorney as control. Both accusations miss"
    " the actual wound.",

    "Paul writes in 1 Corinthians 12:14\u201326 that the body of Christ is ordered such that"
    " each part is essential and each part requires honor it cannot give itself. He is"
    " speaking of the church, but the grammar holds in a marriage: <i>the eye cannot say"
    " to the hand, I have no need of you.</i> In this marriage, each of you is asking for"
    " something only the other can deliberately give. {name_arch} can choose to"
    " <i>notice</i> {name_camp}\u2019s output without immediately auditing it for whether"
    " it fits the plan. {name_camp} can choose to <i>trust</i> {name_arch}\u2019s plan"
    " without needing every element of it to also be a visible accomplishment. Neither of"
    " these moves comes naturally. Both are acts of deliberate love.",

    "{name_arch}, when {name_camp} goes into campaign mode at the wrong time, the"
    " translation is almost never <i>they are disregarding me.</i> Nine times out of ten,"
    " the translation is: <i>they just got administered when they needed to be seen, and"
    " producing harder is the only move they know in that moment.</i> The right response"
    " is not to litigate the deviation from the plan. It is to set the blueprint down for"
    " sixty seconds and address {name_camp} as a person: name one thing you have noticed"
    " them do that had nothing to do with the calendar. Watch what happens.",

    "{name_camp}, when {name_arch} goes into blueprint mode in the middle of an evening,"
    " the translation is almost never <i>they do not care about me.</i> Nine times out of"
    " ten, the translation is: <i>they are afraid the perimeter is failing and this is the"
    " only love language they know when the fear is up.</i> The right response is not to"
    " produce harder in a different direction. It is to name what just happened in one"
    " sentence \u2014 <i>I need a minute as a person, not as the next item on the list</i>"
    " \u2014 and then to trust that {name_arch} will course-correct. He will. The Architect"
    " respects directness. What he cannot read is the campaign running sideways.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be moments \u2014 not often, but they will come"
    " \u2014 when the small collision in the kitchen escalates and both of you are in"
    " breakdown at the same time. The Attorney is up in {name_arch}. {name_camp} is running"
    " harder: more output, more accomplishment, more visible productivity, more giving."
    " The room is frantic. There is no slow conversation. Both of you are, without knowing"
    " it, converting anxiety into output, and the marriage looks, from the inside, like a"
    " very efficient machine in which no one is actually home.",

    "Jesus said, in Mark 6:31, to his disciples who had been producing without ceasing:"
    " <i>Come away by yourselves to a desolate place and rest a while.</i> He said this not"
    " to people who were lazy or undisciplined \u2014 he said it to people who had been"
    " doing genuinely important work at a genuinely relentless pace. The command was not a"
    " rebuke. It was a diagnosis: you have confused the output with the life underneath it,"
    " and the life underneath it needs a room with no agenda. In your marriage, when both"
    " of you are in breakdown, that command is spoken to both of you at once.",

    "{name_arch}, when the Attorney is on his feet, he is not arguing with {name_camp}."
    " He is arguing with an older courtroom in his head \u2014 an earlier room where the"
    " plan not being honored meant someone was unsafe, where disrespect was a genuine threat"
    " to the structure that protected the people he loved. The current brief he is building"
    " against {name_camp} is, in his mind, a case for the perimeter. In {name_camp}\u2019s"
    " experience, it is a closing argument from a prosecutor who does not seem to see them"
    " as a person at all \u2014 only as a variable that is not behaving according to plan.",

    "{name_camp}, when the campaign runs into overdrive, it is not, in that moment, seeking"
    " recognition for its own sake. It is doing the only thing it knows how to do when the"
    " significance trigger fires and nothing is answering it: produce something that cannot"
    " be ignored. But what the campaign\u2019s overproduction looks like to {name_arch}, who"
    " is already worried about things expanding beyond the blueprint, is precisely the"
    " disorder the Architect most fears. So the Attorney rises higher to contain it. So the"
    " Campaign runs harder to escape the containment. The loop is fast, and by the time it"
    " breaks, neither of you can remember what started it, and both of you are exhausted in"
    " a way that a good night\u2019s sleep does not reach.",

    "What to do, when you can both still see what is happening:",

    "<b>One of you, not both, calls the pause.</b> Whichever one notices first what is"
    " happening says it plainly: <i>this is the loop. Twenty minutes.</i> No discussion"
    " about who is right. No final word. No campaign entry drafted in the interval. No"
    " brief assembled. The pause is non-negotiable, and its only rule is that neither"
    " of you uses it to prepare for the next round.",

    "<b>In the twenty minutes, do not strategize. Pray.</b> Pray for each other by name."
    " Not eloquently. {name_arch}: <i>Lord, my Attorney is up. Quiet him. Help me see"
    " {name_camp} as a person and not a variable in the plan.</i> {name_camp}: <i>Lord,"
    " my Campaign is running from something. Help me name what I actually need, in one"
    " sentence, instead of producing it into the room.</i>",

    "<b>When you come back, each of you says one sentence.</b> {name_arch}, your sentence"
    " is not the brief. It is one true thing about what you were afraid of, beginning with"
    " <i>I.</i> {name_camp}, your sentence is not the résumé. It is the one wound, the"
    " single moment of invisibility, under all the producing. <i>I was afraid the plan"
    " was failing</i> is one sentence. <i>I felt like an afterthought tonight</i> is one"
    " sentence. Both of you can say one sentence. Then stop.",

    "<b>If the loop runs anyway, name it the next day.</b> Not to relitigate. To name it"
    " together as a pattern that happened to both of you, that neither of you alone caused,"
    " and that both of you are committed to growing past. The Attorney and the Campaign"
    " in overdrive are both old mechanisms doing the only job they were ever taught to do."
    " The marriage that knows this can be patient with the slow retirement.",

    "And hear this clearly. <b>Neither of you is the problem.</b> The Attorney and the"
    " Campaign running at full speed are not the truest things about either of you."
    " They are old protections, wearing down in the service of a marriage that has"
    " room for something quieter and more permanent. The truest thing about both of you"
    " is that you are a man and a woman who chose each other, who are choosing each other"
    " still, in the small grace of an ordinary evening, even when the loop is running."
    " That is what marriage actually is.",
]

COMMITMENTS_INTRO = [
    "What follows are six commitments \u2014 three from {name_arch}, three from {name_camp}."
    " They are not vows in the legal sense. They are the small daily practices that, offered"
    " to each other freely, change the temperature of a home over months and years. Read"
    " each one slowly. If one of you cannot say a particular commitment in good faith yet,"
    " do not say it. The goal is not performance; the goal is honesty.",
]

ARCH_COMMITMENTS = [
    ("To see what you have done without auditing it for the plan.",
     "{name_camp}, I commit to noticing what you have built, achieved, or given \u2014"
     " not in order to assess how it fits the current blueprint, but simply to see it as"
     " a person who was watching. I know you need to be seen. I know the Campaign in you"
     " has been running for a long time without enough of that. I will try, at least once"
     " each week, to name one thing you have done that I witnessed and that I want you to"
     " know I witnessed. Not as an item in the report. As a person who is glad you are"
     " in this marriage with me."),

    ("To put the calendar down.",
     "{name_camp}, I commit to putting the calendar down at least once each evening"
     " when we are in the same room \u2014 not for an hour, but for five or ten minutes"
     " in which I address you as a person and not as the next thing to be coordinated."
     " When I feel the Attorney rising because the plan feels threatened, I will try to"
     " pause long enough to ask what you actually need from me in this moment, before"
     " I reach for the blueprint."),

    ("To name what I am afraid of, not just what is out of order.",
     "{name_camp}, when I feel myself building harder than the situation requires, I"
     " commit to telling you what I am afraid of in one sentence, rather than litigating"
     " the disorder in silence. The Architect\u2019s fear is not control for its own sake"
     " \u2014 it is the fear that something I love will break if I am not watching it."
     " You deserve to know when that fear is up. The marriage deserves a voice that names"
     " the fear instead of acting it out in case law."),
]

CAMP_COMMITMENTS = [
    ("To let you plan some things without needing them to also be visible accomplishments.",
     "{name_arch}, I commit to receiving the plan as a gift rather than as a constraint."
     " I know I have sometimes converted your structure into a stage \u2014 finding ways"
     " to make the planned thing also a demonstrable thing. I will try to trust the plan"
     " on its own terms, without needing every element of it to produce something I can"
     " point to. You plan because you love. I will try to let the plan be loved in return."),

    ("To name the wound before the campaign answers it.",
     "{name_arch}, I commit to naming the small wounds as they come \u2014 the moments"
     " of invisibility, the times I felt administered rather than seen \u2014 in one"
     " sentence, on the same day they happen, rather than letting the Campaign answer them"
     " by producing harder in a different direction. I will not always do this perfectly."
     " But I will try, before I run, to say one true thing about what I actually needed."),

    ("To let you see me when I am not running.",
     "{name_arch}, I commit to letting you see the person behind the campaign \u2014 not"
     " just the output, not just the accomplishment I want you to notice, but the person"
     " who sometimes, when the campaign goes quiet, does not know who they are without it."
     " That person is the one you married. I will try, in small ways and with some"
     " regularity, to let them be in the room with you, rather than always sending the"
     " campaign in their place."),
]

PRAYER = [
    "Father,",

    "You set us next to each other, and you knew exactly what you were doing. You knew the"
    " Architect would need someone who could see the work. You knew the Performance would"
    " need a structure that did not require constant demonstration to stay inside. You knew"
    " the Attorney and the running Campaign would, on hard evenings, find each other in the"
    " kitchen and convert their anxieties into output until the room was too full for either"
    " of them to breathe. You knew all of it before either of us said yes.",

    "Teach us the grammar of each other. Teach {name_arch} to read {name_camp}\u2019s"
    " campaign, not as deviation from the plan, but as a soul asking to be seen, using the"
    " only language it has ever known. Teach {name_camp} to read {name_arch}\u2019s"
    " building, not as administration, but as a spouse loving the only way the Architect"
    " knows how \u2014 by securing, in advance, the room where both of them can rest.",

    "When the Attorney rises in {name_arch}, would you remind him that you are his advocate,"
    " and that the verdict on his worth has already been spoken in a court that carries more"
    " weight than anything he will litigate tonight. When the Campaign runs harder in"
    " {name_camp}, would you remind them of what Isaiah 49 says is already true: that they"
    " are engraved on the palms of your hands \u2014 not recorded in a ledger of"
    " accomplishments, but inscribed, permanent, present to you before a single campaign"
    " entry was ever made.",

    "Make our home a room where neither of us has to earn our place. Make our table a place"
    " where the day\u2019s fears get named in one sentence instead of litigated or produced"
    " away. Make our evenings slow enough, at least sometimes, that the person behind the"
    " mechanism gets to sit with the person behind the other mechanism, without either of"
    " them performing.",

    "And Father, when we are old and the calendars are finally quiet and the last campaign"
    " has run its last race, let us look back and see that the small repeating rocks became"
    " smaller, and that the home we built together \u2014 imperfect and sometimes frantic"
    " and deeply loved \u2014 was one in which both of us were seen.",

    "In the name of the One who took a bride for himself, who is building the home in which"
    " we will live with him forever, and who does not require a résumé at the door.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages that follow"
    " are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, somewhere quiet,"
    " with no children in the room and no phones on the table. There are six rounds, and"
    " they build on each other. Resist the temptation to skip ahead. Start at Round One"
    " even if it feels too light; the lightness is the point.",

    "Some of the questions are playful. Some are direct. A few are the kind of questions"
    " that, when answered honestly, will sit with you for the rest of the week. None of"
    " them are trivia. All of them are an invitation.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did not read"
    " answers first, in full, without interruption. Then the reader answers the same"
    " question. Then you move on. You do not have to finish all six rounds in one night"
    " \u2014 in fact, two or three rounds taken seriously is often better than racing"
    " through all of them. Save the rest for the next date.",

    "<b>One rule.</b> The other person\u2019s answer is never wrong. You may not love"
    " everything you hear. Stay with it. The point of this is not to assess each other\u2019s"
    " answers. The point is to be known, and to do the work of knowing.",
]

ROUND_1 = [
    ("hypothetical",
     "If our marriage were a building, what kind of building would it be, and what would"
     " the most interesting room inside it look like?",
     "No wrong answers. The first thing that comes to mind is usually the most honest."),

    ("observation",
     "What is something I did this week that you noticed and didn\u2019t mention?",
     "Not a complaint. A small noticing. The fact that you noticed at all is the gift."),

    ("playful",
     "If the two of us were a two-person team in a competition \u2014 any competition,"
     " real or invented \u2014 what would we be competing in, and would we win?",
     "Say the first thing that comes to mind. Then explain why you chose it."),
]

ROUND_2 = [
    ("fill-in-blank",
     "I don\u2019t think I tell you this enough \u2014 I am genuinely amazed at the way"
     " God made you so _______. Your _______ is a gift to this marriage, and I want to"
     " get better at receiving it.",
     "Two blanks. Be specific. \u2018Hardworking\u2019 is too easy; \u2018able to hold the"
     " whole picture in your head at once, even when I\u2019ve completely lost it\u2019"
     " is closer."),

    ("observation",
     "What is one thing you\u2019ve watched me do this year that you wish more people"
     " got to see?",
     "Most of us only ever see ourselves do our most public things. Tell your spouse"
     " about the private ones."),

    ("one-word",
     "If you had to choose one word to describe what it feels like when I walk into"
     " the room after we\u2019ve been apart all day, what word would it be?",
     "One word, said out loud. Then explain it, briefly. Don\u2019t skip the explanation."),
]

ROUND_3 = [
    ("forward-looking",
     "Five years from now, when we look back on this season of our marriage, what do"
     " you hope we will say we did well together?",
     "Not what you wish you had done. What you want, when you look back, to be able"
     " to say you actually did."),

    ("theological",
     "Where, in the last month, have you seen God specifically at work in me?"
     " Not where you want him to work \u2014 where you\u2019ve already seen it.",
     "Name it specifically. The noticing is its own act of love."),

    ("shared-identity",
     "Finish this sentence three times: \u2018We are the kind of couple who _______.'"
     " Give one playful answer, one true answer, and one aspirational answer.",
     "The \u2018we\u2019 is the point. Let the three answers be genuinely different"
     " from each other."),
]

ROUND_4 = [
    ("strength",
     "What is something I do for you that you would have to learn to do for yourself"
     " if I weren\u2019t here?",
     "Hard to ask. Important to hear. Stay with the answer for a moment"
     " before moving on."),

    ("fill-in-blank",
     "One of the gifts of being married to you is that I get to be _______ in ways"
     " I never would have been on my own.",
     "A version of yourself that only exists because this marriage exists. Name it."),

    ("observation",
     "Name one moment in our story where you knew, without any doubt, that we had"
     " built something together that neither of us could have built alone.",
     "Tell the whole story. The remembering is part of the strengthening."),
]

ROUND_5 = [
    ("hard",
     "If you had to choose one word to describe how you feel when you see me hurting"
     " during one of our arguments \u2014 not the argument itself, but watching me"
     " hurt \u2014 what would it be?",
     "One word. Said carefully. Then let it sit before you explain it."),

    ("profile-aware",
     "{name_arch}, when your Attorney is on his feet \u2014 or {name_camp}, when the"
     " campaign is running at full speed to answer something \u2014 what is one thing"
     " you wish the other person would say or do differently, not later, but in that"
     " exact moment?",
     "You both know what these mechanisms are now. Ask each other for what would"
     " actually help. Hear the answer without defending."),

    ("theological",
     "What is one thing you have been carrying lately that you have not yet brought"
     " to me, and what has kept you from bringing it?",
     "Not an accusation. An invitation. The answer you give is a gift."
     " Receive each other\u2019s answers the same way."),
]

ROUND_6 = [
    ("blessing",
     "Place your hand on your spouse\u2019s hand. Say their name. Then say: \u2018You"
     " are not a problem to be solved. You are a gift I get to receive again tomorrow.\u2019"
     " Say it slowly. Let them say it back.",
     "You may feel self-conscious. That is part of why it works. Do it anyway."),

    ("prayer",
     "Pray for each other \u2014 not silently, not generally, but out loud and by name."
     " One sentence is enough. Pray for the thing they just told you in Round Five.",
     "The closing of the date. Do not skip. The prayer is the point of all of it."),
]


def _render(text, name_arch, name_camp):
    return text.format(name_arch=name_arch, name_camp=name_camp)


def build(sub_a, sub_b) -> bytes:
    """Generate the Architect + Performance Campaign couples walkthrough PDF.

    sub_a: the submission of the Architect spouse
    sub_b: the submission of the Performance Campaign spouse
    """
    ensure_fonts()
    S = make_styles()

    name_arch = _first_name(sub_a, "Architect")
    name_camp = _first_name(sub_b, "Performance")

    def R(text):
        return _render(text, name_arch, name_camp)

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Couples Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUPLES WALKTHROUGH",
        cover_right_label=f"{name_arch.upper()}  +  {name_camp.upper()}",
        title=f"Take 139 Couples Walkthrough \u2014 {name_arch} & {name_camp}",
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
    story.append(Paragraph(f"{name_arch} &nbsp;&amp;&nbsp; {name_camp}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_arch.upper()}</b></font><br/>"
                "Architect &middot; Attorney<br/>"
                "<font size=9 color='#6b6862'>Disrespect &middot; Am I protected?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_camp.upper()}</b></font><br/>"
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
        "<i>\u201cFrom the outside they look formidable.<br/>"
        "The Architect builds; the Performance runs.<br/>"
        "What they are each asking for is different from what the other thinks they are asking for.\u201d</i>",
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
            _profile_card(S, name_camp, ACCENT_HER, "Significance",
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
    section_header(story, S, "SECTION THREE  \u00b7  THE PERFORMANCE\u2019S GIFT TO THE ARCHITECT",
                   f"What {name_camp} gives {name_arch}.",
                   "A witness to the work \u2014 something the Architect\u2019s own mechanism rarely produces.")
    for p in GIFT_TO_ARCH:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4 ──
    section_header(story, S, "SECTION FOUR  \u00b7  THE ARCHITECT\u2019S GIFT TO THE PERFORMANCE",
                   f"What {name_arch} gives {name_camp}.",
                   "A structure that does not require the Campaign to earn its place.")
    for p in GIFT_TO_CAMP:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5 ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Protection meets significance.",
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
                   "When the Attorney and the Campaign are both running.",
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
    story.append(Paragraph(f"FROM {name_arch.upper()}, TO {name_camp.upper()}", S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name, body in ARCH_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(name, S["H3"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_camp}, to {name_arch}.",
                   "Three commitments, in the Campaign\u2019s voice, for the Architect to receive.")
    story.append(Paragraph(f"FROM {name_camp.upper()}, TO {name_arch.upper()}", S["CommitLabelHer"]))
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
        primary_mechanism = "ARCH"
        primary_breakdown = "ATTY"
        primary_trigger = "DISRESP"
        core_question = "PROT"
        name = "Jordan"

    class FakeSubB:
        primary_mechanism = "CAMP"
        primary_breakdown = "ATTY"
        primary_trigger = "SIG"
        core_question = "REM"
        name = "Taylor"

    pdf_bytes = build(FakeSubA(), FakeSubB())
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "architect_performance_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        snippet = ""
        for page in reader.pages[4:9]:
            txt = page.extract_text() or ""
            if "SECTION THREE" in txt or "witness" in txt.lower() or "gift" in txt.lower():
                snippet = txt.strip()[:200]
                break
        if not snippet:
            for page in reader.pages[4:9]:
                txt = page.extract_text() or ""
                if txt.strip():
                    snippet = txt.strip()[:200]
                    break
    except Exception as e:
        page_count = "unknown"
        snippet = f"(pypdf error: {e})"

    print(f"DONE: architect_performance.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
