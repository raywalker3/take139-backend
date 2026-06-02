"""Couples Walkthrough — Architect + Island.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 8 sections + 6-round Date Night appendix.

This builder serves any couple where one spouse is an Architect and the
other is an Island. First names are substituted from the submissions:
    {name_arch}  -> the Architect spouse's first name
    {name_isle}  -> the Island spouse's first name

The first builder was written for Chris (Architect) + Carolyn (Island).
For other couples, the names are swapped automatically.
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


def _pronouns(sub, prefix: str) -> dict:
    """Build a dict of pronoun substitutions for a given submission, keyed
    under the writer's positional prefix (e.g. 'arch' or 'isle').

    Returns keys: {prefix}_he, {prefix}_him, {prefix}_his, {prefix}_himself,
    {prefix}_Pronoun (subject, capitalized), {prefix}_Possessive (capitalized).

    Defaults to MALE forms when gender is missing/unknown — this is the
    safest fallback because every existing walkthrough in this file was
    originally written assuming the Architect is male. For non-male
    Architects the gender field MUST be set; otherwise pronouns are wrong.
    """
    g = (getattr(sub, "gender", None) or "M").upper()
    if g == "F":
        return {
            f"{prefix}_he": "she",
            f"{prefix}_He": "She",
            f"{prefix}_him": "her",
            f"{prefix}_Him": "Her",
            f"{prefix}_his": "her",
            f"{prefix}_His": "Her",
            f"{prefix}_himself": "herself",
            f"{prefix}_Himself": "Herself",
            f"{prefix}_man": "woman",
            f"{prefix}_husband": "wife",
            f"{prefix}_Husband": "Wife",
        }
    # default & 'M'
    return {
        f"{prefix}_he": "he",
        f"{prefix}_He": "He",
        f"{prefix}_him": "him",
        f"{prefix}_Him": "Him",
        f"{prefix}_his": "his",
        f"{prefix}_His": "His",
        f"{prefix}_himself": "himself",
        f"{prefix}_Himself": "Himself",
        f"{prefix}_man": "man",
        f"{prefix}_husband": "husband",
        f"{prefix}_Husband": "Husband",
    }


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


# ──────────── PROSE — uses {name_arch} and {name_isle} placeholders ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small repeating ones &mdash; the same disappointment in slightly different clothes, three or four times a week, year after year, until both people have forgotten what they were originally hoping for.",
    "What follows is a counselor's read of the small repeating rocks in your particular marriage. Not the dramatic failures, which you would have addressed already. The small ones. The ones that happen on a Tuesday at 5:40 in the kitchen and that neither of you would have thought to bring to a counselor because, by Wednesday, they have receded into the background of an otherwise good life.",
    "You are both reading this because you have decided to look at those rocks. That decision is more significant than it seems. Most couples spend a lifetime navigating around them without naming them. Naming them is half the work.",
    "Here is what I want to do for you. I will name what each of you brings the other that you could not have built alone &mdash; the genuine, theological gift that your two shapes form together. Then I will name the collision your two questions create, in the specific way it shows up in your marriage. Then I will name the worst case &mdash; the moment when your Attorney and {isle_his} Flood are in the room at the same time &mdash; and what to do then. Then I will hand each of you three commitments, not as rules, but as the kind of small daily practices that, over years, change the temperature of a home.",
    "Read it together, if you can. If not, read it separately and then sit down with it. Argue with what does not fit. Stay with what does. The goal is not insight; the goal is a marriage in which the small repeating rocks become smaller, less repeating, and eventually a part of the landscape you can both laugh at.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on paper, side by side. Most couples never see their two profiles next to each other. You are about to.",
]

TWO_SHAPES_BODY = [
    "{name_arch}, you are an <b>Architect</b> whose body reads disrespect as an alarm and whose deepest question is whether you are protected. You build structures because you believe, in your bones, that suffering is largely a function of insufficient planning. When the building fails, an <b>Attorney</b> takes the floor and begins to litigate &mdash; not to win an argument, but to prove {arch_he} is safe.",
    "{name_isle}, you are an <b>Island</b> whose body reads insignificance as an alarm and whose deepest question is whether you are significant. You have learned to be self-contained because containment, for you, is dignity &mdash; a refusal to spill yourself into rooms that have not asked for you. When the containment breaks, a <b>Flood</b> takes the floor and a week of unspoken weight comes out at once.",
    "Notice what these two profiles do <i>not</i> share, and notice what they actually share underneath. You are not asking the same question. One of you is asking <i>am I protected?</i> and the other is asking <i>am I significant?</i> &mdash; two questions that, in a marriage, are easy to mistake for each other and easy to fail to give each other.",
    "But underneath the two questions is the same root. You are both people who have learned to live with a level of vigilance most of the world does not require. {name_arch} is vigilant about the perimeter; {name_isle} is vigilant about whether {isle_his} presence in the room is actually wanted. Both of you, in different costumes, are asking <i>am I safe to be here, fully, as myself?</i>",
    "This is not a coincidence. The Architect and the Island are, in fact, one of the more common pairings in marriages that last, and there is a reason. Each of you intuitively respects something in the other that most spouses would not understand. The Architect respects the right to an interior life. The Island respects the right to plan and prepare without being mocked for it. The friction between you is real, but the foundation is unusually good.",
]

GIFT_TO_ARCH = [
    "{name_isle} gives {name_arch} something almost no one else in {arch_his} life is in a position to give: <b>a room that does not demand {arch_he} be three meetings ahead.</b>",
    "Most of the rooms {name_arch} walks into require the Architect to be working. People depend on {arch_him}. Plans depend on {arch_him}. The structures {arch_he} has built keep functioning because {arch_he} keeps building them. The Architect cannot rest in those rooms because the moment {arch_he} does, something {arch_he} has been holding will drop.",
    "{name_isle}, by virtue of being an Island, is the rare room that does not require this of {arch_him}. {isle_He} does not need {arch_him} to entertain {isle_him}. {isle_He} does not need {arch_him} to manage {isle_his} emotional weather. {isle_He} does not, in most seasons, need {arch_him} to anticipate {isle_his} three moves ahead. The Island's self-containment, which to a different mechanism would feel like withholding, is to the Architect one of the few oases in {arch_his} week.",
    "The theological word for what {name_isle} gives {name_arch} is <i>sabbath.</i> Not the formal Sabbath of Sunday observance, but the small, recurring sabbaths of a marriage in which one person does not require the other to be performing. The Architect does not know how to rest because {arch_his} job in every other room is to keep building. {name_isle}, simply by being who {isle_he} is, gives {arch_him} a room in which the building is allowed to stop.",
    "{name_arch} &mdash; if you want to thank {name_isle} for something this week, thank {isle_him} for this. {isle_He} probably does not know {isle_he} is giving it to you. Islands rarely know that their containment is a gift; they have been told often enough that it is a problem. Tell {isle_him} that {isle_his} ability to be near you without needing you to perform is one of the kindest things in your life. {isle_He} will not know what to do with the compliment. Say it anyway.",
    "{name_isle} &mdash; what {name_arch} is receiving from you, when you simply sit beside {arch_him} without filling the air, is the closest thing {arch_he} gets to rest most weeks. The thing in you that you have sometimes been told is too much alone, too quiet, too contained, is for {arch_him} a kind of medicine.",
]

GIFT_TO_ISLE = [
    "{name_arch} gives {name_isle} something Islands rarely build for themselves: <b>a trellis.</b>",
    "Islands under-build their structures. Not because they are lazy or undisciplined &mdash; you, {name_isle}, are neither &mdash; but because the structures themselves can feel like a violation of the self-containment the Island has worked to protect. Calendars, plans, contingencies, the small architectural choices that hold a life upright &mdash; the Island tends to leave these to the last possible moment, because committing to them in advance feels like giving up some piece of one's own autonomy.",
    "The cost of this is rarely visible to the Island, and it is almost never named by anyone else. But the cost is real. Without a trellis, even the most beautiful vine begins, over years, to lie on the ground. The Island can live a remarkable interior life and still end up with an exterior life that does not match it &mdash; appointments missed, opportunities allowed to drift past, gifts that never quite found a way to be given.",
    "{name_arch}, by virtue of being an Architect, is constantly building the trellis you would have been unlikely to build for yourself. The fact that the schedule holds, that the calendar functions, that the structures are in place, that the contingencies are accounted for &mdash; this is not a small thing. It is the trellis on which your life can grow without you having to admit that you needed one.",
    "There is a theological word for what {name_arch} gives {name_isle}, too. It is <i>covering.</i> Not the patriarchal covering that has been used badly in many marriages, but the older biblical sense of one person standing in front of the weather so the other can grow. Paul writes that husbands are to love their wives as Christ loved the church &mdash; and the love of Christ for his church is often, in Scripture, the love of a builder for what he is building. {name_arch} loves you by building.",
    "{name_isle} &mdash; if you want to thank {name_arch} for something this week, thank {arch_him} for this. Most weeks you will not feel the trellis, because trellises that work are invisible. Thank {arch_him} for one specific thing {arch_he} built that you did not have to build yourself. {arch_He} will not know what to do with the compliment. Say it anyway.",
    "{name_arch} &mdash; what {name_isle} is receiving from you, when you simply hold the calendar and the contingencies and the long view, is the freedom to live an interior life without paying the full external cost of doing so. The thing in you that has sometimes been told it is too much planning, too much vigilance, is for {isle_him} a kind of covering.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you, even if you have not named it.",
    "{name_arch}'s core question is <i>am I protected?</i> {name_isle}'s is <i>am I significant?</i> These two questions are not opposed in theory. In the daily mechanics of a marriage, they ask for different things, and the asking often misfires.",
    "Protection wants reliability, structure, predictability. When {name_arch} is trying to feel protected, {arch_he} reaches for systems: the schedule, the plan, the list, the contingency. The way the Architect loves you, {name_isle}, is by securing the next three rooms before either of you walks into them. To {name_arch}, this is love. {arch_He} is, in {arch_his} own grammar, putting {arch_his} arms around the family.",
    "Significance wants attention, weight, the felt sense of being seen as a singular person rather than as a function. When {name_isle} is trying to feel significant, {isle_he} does not reach for systems &mdash; {isle_he} reaches for a moment in which {isle_he} is unmistakably the subject of someone's attention, not the object of someone's management. To {name_isle}, the felt sense of being administered &mdash; even kindly, even efficiently &mdash; is not protection. It is a kind of erasure.",
    "Here is the collision in slow motion. {name_arch}, in trying to protect the family on a Tuesday evening, treats {name_isle} as a piece of the system {arch_he} is securing &mdash; the dinner that needs to be timed, the kid that needs to be picked up, the calendar item that needs to be confirmed. {arch_He} is, in {arch_his} mind, loving {isle_him} by holding the perimeter. {isle_He} experiences it as being addressed as a function rather than as a person. {isle_His} trigger fires: <i>insignificance.</i>",
    "{isle_He} does not say so. Islands do not say so. Instead, {isle_he} withdraws into the Island's self-containment &mdash; {isle_he} goes quiet, becomes briefer in {isle_his} responses, retreats into {isle_his} interior life. To {name_arch}, this withdrawal does not read as <i>{isle_he} is hurt.</i> It reads as <i>{isle_he} is disregarding me.</i> {arch_His} trigger fires: <i>disrespect.</i> The Architect doubles down on the systems, because more building is the only answer the Architect knows. The Island withdraws further, because more containment is the only answer the Island knows. Within twenty minutes, neither of you can remember what started it. Both of you are quietly convinced you are the one who has been wronged.",
    "This is not a moral failure on either side. It is the predictable arithmetic of two profiles whose alarms misread each other's love language. You are both, in your own grammar, trying to love. You are both, in the other's grammar, getting it slightly wrong.",
    "The way out is not for either of you to stop being who you are. The Architect is not going to stop building, and shouldn't. The Island is not going to stop containing, and shouldn't. The way out is for each of you to learn the other's grammar well enough to translate, in real time, what is actually happening.",
    "{name_arch}, when {name_isle} goes quiet, the translation is almost never <i>{isle_he} is disregarding me.</i> Nine times out of ten, the translation is <i>{isle_he} just got administered when {isle_he} needed to be seen.</i> The right move, when you notice the quiet, is not to litigate. It is to set down the calendar for sixty seconds and look at {isle_him} as a person rather than a node in your system. Ask {isle_him} one direct question that has nothing to do with logistics. The Island will not always answer immediately &mdash; {isle_he} may need a beat &mdash; but {isle_he} will register the gesture, and the trigger will start to recede.",
    "{name_isle}, when {name_arch} goes into Architect mode at the end of a long day, the translation is almost never <i>{arch_he} does not care about me.</i> Nine times out of ten, the translation is <i>{arch_he} is afraid the perimeter will fail and is loving us the only way {arch_he} knows how.</i> The right move, when you feel administered, is not to withdraw immediately. It is to name what just happened in one sentence &mdash; <i>I need a minute as a person, not as the next item</i> &mdash; and then to let {arch_him} course-correct. {arch_He} will. The Architect respects directness; what {arch_he} cannot read is silence.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be moments &mdash; not often, but they will come &mdash; when the small collision in the kitchen escalates and both of you are in the breakdown at the same time. The Attorney is up. The Flood is up. The room is fast and loud and exhausting, and neither of you, in that moment, has access to the more thoughtful person you were three hours ago.",
    "Here is what is happening, named plainly so you can both see it.",
    "{name_arch}, when the Attorney is on his feet, he is not arguing with {name_isle}. He is arguing with an old courtroom in his head &mdash; an earlier room where being misunderstood meant being unsafe. The current evidence he is marshaling against {name_isle} is, in his mind, a brief. In hers, it is a closing argument from a prosecutor. He thinks he is defending himself; she experiences it as being prosecuted.",
    "{name_isle}, when the Flood is up, she is not, in that moment, naming three separate grievances. She is releasing a week or a month of unsaid weight that she has been quietly carrying. The sequence does not feel sequential to her; it feels like one continuous truth. To {name_arch}, however, who has been hearing what sounds like a multi-count indictment, the Flood reads as the closing argument he must respond to. So the Attorney rises higher. So the Flood rises higher. The loop is fast and almost never about what started it.",
    "What to do, when you can both still see what is happening:",
    "<b>One of you, not both, calls the pause.</b> Whichever one of you notices first what is happening says, out loud: <i>this is the loop. Twenty minutes.</i> No discussion about who is right. No final word. The pause is non-negotiable, and the only rule of the pause is that no one is allowed to use it to draft the next brief or rehearse the next sentence.",
    "<b>In the twenty minutes, do not strategize. Pray.</b> Pray for each other by name. Not eloquently. <i>Lord, my Attorney is up. Quiet him. Help me see her as a person and not a case.</i> Or: <i>Lord, my Flood is up. Help me name the one thing under the week of weight. Help me come back to him as {name_isle}, not as the accumulation.</i>",
    "<b>When you come back, each of you says one sentence, not a paragraph.</b> {name_arch}, your sentence is not the brief. It is one true sentence about what you actually felt, beginning with <i>I.</i> {name_isle}, your sentence is not the week's accumulation. It is the one thing, the single weight, under all the others. <i>I felt unseen at dinner</i> is one sentence. <i>I was scared the perimeter was failing</i> is one sentence. Both of you can speak one sentence. Then you stop.",
    "<b>If, even with these tools, the loop runs anyway, name it the next day.</b> Not to relitigate. To name it together as a pattern that happened to both of you, neither of you alone caused, and both of you are committed to growing past. The Attorney and the Flood are old friends who have been working long shifts. They will retire slowly. The marriage that knows this can be patient with the slow retirement.",
    "And hear this clearly. <b>Neither of you is the problem.</b> The Attorney and the Flood are not the truest things about either of you. They are old mechanisms doing the only job they were ever taught to do. The truest thing about both of you is that you are a man and a woman who have chosen, in the small grace of an ordinary Tuesday, to keep loving each other through the slow retirement of the old machinery. That is what marriage actually is.",
]

COMMITMENTS_INTRO = [
    "What follows are six commitments &mdash; three from {name_arch}, three from {name_isle}. They are not vows in the legal sense. They are the small daily practices that, offered to each other freely, change the temperature of a home over months and years. Read each one slowly. If one of you cannot say a particular commitment in good faith yet, do not say it. The goal is not performance; it is honesty.",
]

ARCH_COMMITMENTS = [
    ("To set down the calendar.",
     "{name_isle}, I commit to setting down the calendar at least once each evening when you and I are in the same room. Not for an hour. For five minutes. In those five minutes I will look at you as a person and not as the next item I am securing. I will not always know what to ask. I will ask anyway."),
    ("To translate the quiet.",
     "{name_isle}, when you go quiet, I commit to translating it correctly. Nine times out of ten, your quiet does not mean you are disregarding me. It means I just administered you when you needed to be seen. I will pause before the Attorney rises and ask you what you actually need from me, with no calendar in my hand."),
    ("To name what I am afraid of.",
     "{name_isle}, when I feel myself building harder than the situation requires, I commit to telling you what I am afraid of in one sentence rather than building in silence. The Architect has been working overtime for a long time. You deserve to know when he is afraid, and the marriage deserves a voice that names the fear instead of acting it out."),
]

ISLE_COMMITMENTS = [
    ("To name the weight before it floods.",
     "{name_arch}, I commit to naming the small weights as they come, rather than carrying them in silence until the Flood does it for me. I will not always do this perfectly. I will sometimes still flood. But I will try, on the small things, to give them a sentence in the same week they happen, so the brief never has to be a closing argument."),
    ("To trust the trellis.",
     "{name_arch}, when you are in Architect mode, I commit to remembering that the building is your love language. I will receive the trellis as a gift, not a cage. When I need to be a person and not an item, I will say so directly in one sentence, and I will trust that you will course-correct because you always have."),
    ("To let myself be seen.",
     "{name_arch}, I commit to letting you see me, even when the Island would prefer to remain contained. I will not always know how to spill. But I will try, in small ways, to let you in on what is actually happening in my interior life, because I do not want our marriage to be one in which the most important things are the ones I never quite got around to saying."),
]

PRAYER = [
    "Father,",
    "You set us next to each other, and you knew exactly what you were doing. You knew the Architect would need an Island. You knew the Island would need a trellis. You knew the Attorney and the Flood would, on hard days, find each other in the kitchen. You knew all of it before either of us said yes.",
    "Teach us the grammar of each other. Teach {name_arch} to read {name_isle}'s quiet, not as disregard, but as a soul that needs to be seen. Teach {name_isle} to read {name_arch}'s building, not as administration, but as a husband loving the only way he knows how.",
    "When the Attorney rises in {name_arch}, would you remind him that you are his advocate, and that the verdict has been spoken. When the Flood rises in {name_isle}, would you remind her that she is significant &mdash; not because of what she has done, but because of what you have done in her.",
    "Make our home a room in which neither of us has to perform. Make our table a place where the small weights get named on the same day they happen. Make our bed a place where the day's loops are quieted before sleep, and our mornings a place where the two of us begin again, on grace and not on yesterday.",
    "And Father, when we are old and the children are grown and the calendar is finally quiet, let us look back and see that the small repeating rocks became smaller, and less repeating, and finally a part of the landscape we could both laugh at together.",
    "In the name of the One who took a bride for himself, and who is, even now, building the home in which we will live with him forever.",
    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages that follow are different. They are meant to be spoken <i>between</i> you.",
    "What follows is a date-night conversation, designed to be taken slowly, somewhere quiet, with no children in the room and no phones on the table. There are six rounds, and they build on each other. Resist the temptation to skip ahead. Start at Round One even if it feels too light; the lightness is the point.",
    "Some of the questions are playful. Some are direct. A few are the kind of questions that, when answered honestly, will sit with you for a week. None of them are trivia. All of them are an invitation.",
    "<b>How to use it.</b> One of you reads a question aloud. The one who did not read answers first, in full, without interruption. Then the reader answers the same question. Then you move on. You do not have to finish all six rounds in one night &mdash; in fact, two or three rounds, taken seriously, is often better than racing through all of them. Save the rest for the next date.",
    "<b>One rule.</b> The other person's answer is never wrong. You may not love everything you hear. Stay with it. The point of this is not to grade each other's answers. The point is to be known, and to do the work of knowing.",
]

ROUND_1 = [
    ("hypothetical", "If our marriage were a city, which one would it be, and which neighborhood would we live in?", "Borrow Esther Perel's habit of letting metaphor say the things plain language can't."),
    ("observation", "What is something I did this week that you noticed and didn't mention?", "Not a complaint. A small noticing. The fact that you noticed at all is the gift."),
    ("playful", "If you had to give us a band name, what would it be, and what genre would we play?", "Yes, really. Answer with the first thing that comes to mind."),
]

ROUND_2 = [
    ("fill-in-blank", "I don't think I tell you this enough &mdash; I am amazed at the way God made you so _______. Your _______ is a gift to our marriage, and I want to get better at receiving it.", "Two blanks. Be specific. 'Kind' is too easy; 'patient with the kids in the moments when I have already lost mine' is closer."),
    ("observation", "What is one thing you've watched me do this year that you wish more people got to see?", "Most of us only ever see ourselves do our most public things. Tell your spouse about the private ones."),
    ("one-word", "If you had to choose one word to describe what it feels like when I walk into the room after a long day apart, what word would it be?", "One word, said out loud. Then explain it, briefly."),
]

ROUND_3 = [
    ("forward-looking", "Five years from now, when we look back on this season of our marriage, what do you hope we will say we did well together?", "Not what you wish you had done. What you want, when you look back, to be able to say you did."),
    ("theological", "Where, in the last month, have you seen God specifically at work in me?", "Not where you want him to work. Where you've already seen it. Name it."),
    ("shared-identity", "Finish this sentence three times: 'We are the kind of couple who _______.' Give one playful answer, one true answer, and one aspirational answer.", "From Aron's 36 Questions, slightly retooled. The 'we' is the point."),
]

ROUND_4 = [
    ("strength", "What is something I do for you that you would have to learn to do for yourself if I weren't here?", "Hard to ask. Important to hear the answer. Stay with it."),
    ("fill-in-blank", "One of the gifts of being married to you is that I get to be _______ in ways I never would have been on my own.", "A version of yourself that only exists because the marriage exists. Name it."),
    ("observation", "Name one moment in our story so far where you knew, with no doubt, that we had built something together that neither of us could have built alone.", "Tell the story in full. The remembering is part of the strengthening."),
]

ROUND_5 = [
    ("hard", "If you had to choose one word to describe how you feel when you see me hurting during one of our arguments, what would it be?", "One word. Said carefully. Then let it sit before you explain."),
    ("fill-in-blank", "{name_isle} (or {name_arch}), I think I like to demonstrate to you that I am very _______, but I am afraid I am actually a lot more _______ than I would like to admit.", "The first blank is what you perform. The second is what is underneath. Both halves matter; the gap between them is where the real work lives."),
    ("theological", "What is one thing you have been carrying lately that you have not yet brought to me, and what has kept you from bringing it?", "Not an accusation. An invitation. Hear the answer without defending."),
    ("profile-aware", "When my Attorney is on his feet, or when my Flood is up, what is one thing you wish I would say or do differently &mdash; not later, but in the moment?", "You both know what these mechanisms are now. Ask each other for what would actually help."),
]

ROUND_6 = [
    ("blessing", "Place your hand on your spouse's hand. Say their name. Then say: 'You are not a problem to be solved. You are a gift I get to receive again tomorrow.' Say it slowly. Let them say it back.", "You may feel silly. That is part of why it works. Do it anyway."),
    ("prayer", "Pray for each other &mdash; not silently, not generally, but out loud and by name. One sentence is enough. Pray for the thing they just told you in Round Five.", "The closing of the date. Do not skip."),
]


def _render(text, **subs):
    return text.format(**subs)


def build(sub_arch, sub_isle) -> bytes:
    """Generate the Architect+Island couples walkthrough PDF.

    sub_arch: the submission of the Architect spouse
    sub_isle: the submission of the Island spouse
    """
    ensure_fonts()
    S = make_styles()

    name_arch = _first_name(sub_arch, "Architect")
    name_isle = _first_name(sub_isle, "Island")

    # Build the full substitution dict: names + pronouns for each spouse.
    subs = {"name_arch": name_arch, "name_isle": name_isle}
    subs.update(_pronouns(sub_arch, "arch"))
    subs.update(_pronouns(sub_isle, "isle"))

    # Section three / four headings depend on the Island spouse's gender:
    # "HER gift to HIM" when Island=F, "HIS gift to HIM" when Island=M.
    # Spelled out by combining each side's possessive + object pronouns.
    isle_poss_upper = subs["isle_His"].upper()   # 'HER' or 'HIS'
    arch_obj_upper  = subs["arch_him"].upper()   # 'HIM' or 'HER'
    arch_poss_upper = subs["arch_His"].upper()
    isle_obj_upper  = subs["isle_him"].upper()

    # Per-spouse "in {his/her} life" possessive (used in subheadings)
    arch_life_poss = subs["arch_his"]   # 'his' or 'her'
    isle_life_poss = subs["isle_his"]

    def R(text):
        return _render(text, **subs)

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Couples Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUPLES WALKTHROUGH",
        cover_right_label=f"{name_arch.upper()}  +  {name_isle.upper()}",
        title=f"Take 139 Couples Walkthrough \u2014 {name_arch} & {name_isle}",
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
    story.append(Paragraph(f"{name_arch} &nbsp;&amp;&nbsp; {name_isle}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_arch.upper()}</b></font><br/>"
                "Architect &middot; Attorney<br/>"
                "<font size=9 color='#6b6862'>Disrespect &middot; Am I protected?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_isle.upper()}</b></font><br/>"
                "Island &middot; Flood<br/>"
                "<font size=9 color='#6b6862'>Insignificance &middot; Am I significant?</font>",
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
        "<i>\u201cMost marriages do not break on the large rocks.<br/>"
        "They break on the small repeating ones.\u201d</i>",
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
            _profile_card(S, name_arch, ACCENT, "Disrespect", "Am I protected?", "The Architect", "The Attorney"),
            "",
            _profile_card(S, name_isle, ACCENT_HER, "Insignificance", "Am I significant?", "The Island", "The Flood"),
        ]],
        colWidths=[
            (PAGE_W - MARGIN_L - MARGIN_R - 18) / 2.0, 18, (PAGE_W - MARGIN_L - MARGIN_R - 18) / 2.0,
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
    section_header(story, S, f"SECTION THREE  \u00b7  {isle_poss_upper} GIFT TO {arch_obj_upper}",
                   f"What {name_isle} gives {name_arch}.",
                   f"Something almost no one else in {arch_life_poss} life is in a position to give.")
    for p in GIFT_TO_ARCH:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4 ──
    section_header(story, S, f"SECTION FOUR  \u00b7  {arch_poss_upper} GIFT TO {isle_obj_upper}",
                   f"What {name_arch} gives {name_isle}.",
                   "Something Islands rarely build for themselves.")
    for p in GIFT_TO_ISLE:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5 ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Protection meets significance.",
                   "The small repeating rock, named.")
    for p in COLLISION[:4]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The loop, in slow motion.",
                   "And the way out, for each of you in your own grammar.")
    for p in COLLISION[4:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6 ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When the Attorney and the Flood are in the room at once.",
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
    story.append(Paragraph(f"FROM {name_arch.upper()}, TO {name_isle.upper()}", S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name, body in ARCH_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(name, S["H3"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_isle}, to {name_arch}.",
                   f"Three commitments, in {subs['isle_his']} voice, for {arch_obj_upper.lower()} to receive.")
    story.append(Paragraph(f"FROM {name_isle.upper()}, TO {name_arch.upper()}", S["CommitLabelHer"]))
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
