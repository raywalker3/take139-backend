"""Couples Walkthrough — Architect + Architect.

Voice: Tim Keller (from The Meaning of Marriage + Walking with God through
Pain and Suffering). Pastoral, theologically rich, warmly direct.
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where both spouses are Architects.
First names are substituted from the submissions at render time:
    {name_a}  -> the first Architect spouse's first name (alphabetical)
    {name_b}  -> the second Architect spouse's first name (alphabetical)

For same-mechanism pairs the order does not carry directional meaning.
The build() function sorts alphabetically so A <= B.
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
    + "ones &mdash; the same disappointment in slightly different clothes, three or four "
    + "times a week, year after year, until both people have forgotten what they were "
    + "originally hoping for.",

    "What follows is a counselor's read of the small repeating rocks in your particular "
    + "marriage. Not the dramatic failures &mdash; those you would have addressed already. "
    + "The small ones. The ones that happen on a Tuesday at 5:40 in the kitchen and that "
    + "neither of you would have thought to bring to a counselor, because by Wednesday "
    + "they have receded into the background of an otherwise good life.",

    "You are both reading this because you have decided to look at those rocks. That "
    + "decision is more significant than it seems. Most couples spend a lifetime navigating "
    + "around them without naming them. Naming them is half the work.",

    "Your pairing is one of the theologically richest pairings we encounter: "
    + "<b>two Architects.</b> You speak the same internal language. You both build, "
    + "plan, anticipate, manage. You understand each other's mechanism almost too well "
    + "&mdash; and this is simultaneously the gift and the danger of your marriage. "
    + "The gift: there is no &ldquo;you don't get how I think.&rdquo; "
    + "The danger: when both Architects are in breakdown mode, the courtroom has two "
    + "prosecutors and no defense &mdash; or, more dangerously still, two planners quietly "
    + "drafting separate exit strategies in silence.",

    "Here is what I want to do for you. I will name what each of you brings the other "
    + "that the other could not have built alone &mdash; the genuine gift that your "
    + "shared architecture makes possible. Then I will name the collision your shared "
    + "mechanism creates, which is different from what most couples face: it is not a "
    + "failure of translation but a conflict of blueprints. Then I will name the harder "
    + "picture &mdash; the courtroom when both of you are on your feet, or the silence "
    + "when both of you are drafting the exit. Then I will hand each of you four "
    + "commitments, not as rules, but as the kind of small daily practices that, over "
    + "years, change the temperature of a home.",

    "Read it together, if you can. If not, read it separately and then sit down with it. "
    + "Argue with what does not fit. Stay with what does. The goal is not a perfect "
    + "marriage; it is a marriage in which the small repeating rocks become smaller, "
    + "less repeating, and eventually a part of the landscape you can both laugh at.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on "
    + "paper, side by side. Most couples never see their two profiles next to each other. "
    + "You are about to &mdash; and for you, the first thing you will notice is how much "
    + "they look alike.",
]

TWO_SHAPES_BODY = [
    "{name_a}, you are an <b>Architect</b> whose body reads disrespect or injustice as "
    + "an alarm, and whose deepest question is whether you are protected. You build "
    + "structures because you believe, in your bones, that suffering is largely a function "
    + "of insufficient planning. You love by securing the perimeter. When the perimeter "
    + "fails, an <b>Attorney</b> takes the floor and begins to litigate &mdash; not "
    + "necessarily to win, but to establish the record, to prove that the wrong was real.",

    "{name_b}, you are an <b>Architect</b> whose body reads the same alarm: disrespect "
    + "or injustice. Your deepest question is the same: <i>am I protected?</i> You, too, "
    + "build structures and love by securing what can be secured. When your blueprint "
    + "fails, your Attorney also rises &mdash; or, in some seasons, you go quiet and "
    + "begin to plan an exit that neither of you has named yet.",

    "Take a moment to absorb what this means. You are asking the same question. You are "
    + "running the same mechanism. You are, in many weeks, protecting the same thing. "
    + "This is the shared language that makes your marriage feel, at its best, like a "
    + "true partnership of equals who do not have to explain themselves to each other. "
    + "You both know what the other is doing when they go into planning mode. You both "
    + "understand the satisfaction of a well-run household, a finished contingency, a "
    + "structure that held.",

    "But here is what the shared language does not automatically produce: <i>humility "
    + "toward each other's blueprint.</i> Two Architects in a marriage will eventually "
    + "produce two visions &mdash; of how the household should run, the budget should "
    + "flow, the children should be raised, the calendar should be ordered, the future "
    + "should be shaped. And neither of you, by temperament, is inclined to defer to "
    + "the other's vision, because both of you have thought it through. Both of you have "
    + "done the work. Both of you, with reason, believe your blueprint is the better one.",

    "This is the singular gift and the singular danger of your marriage. The gift is that "
    + "you are, together, one of the most capable households in any room you enter. The "
    + "danger is that capability, in a marriage, is not the same thing as wisdom &mdash; "
    + "and wisdom, the kind that builds a home that lasts, requires something neither "
    + "Architect naturally carries to the table: the willingness to lay down the "
    + "blueprint and ask, with genuine openness, for your spouse's.",
]

GIFT_TO_A = [
    "{name_b} gives {name_a} something almost no one else in the marriage can give: "
    + "<b>a co-architect who genuinely understands the weight of what is being built.</b>",

    "Most people in {name_a}'s life receive the structures she builds with gratitude, "
    + "mild confusion, or the occasional quiet resentment of the over-managed. They "
    + "benefit from the Architect's work without ever quite understanding it. {name_b} "
    + "is the rare exception. He has lived inside the same mechanism. He knows what it "
    + "costs to hold a structure upright when others do not notice it needs holding. He "
    + "does not have to be explained to.",

    "There is a relief in that which is difficult to name without experiencing it. "
    + "Tim Keller, writing in <i>The Meaning of Marriage</i>, observed that one of the "
    + "deepest gifts of a good marriage is to be known &mdash; not known the way a "
    + "therapist knows you, catalogued and categorized, but known the way a person who "
    + "has lived beside you for years knows you, without needing a translation. {name_b} "
    + "knows {name_a}'s mechanism from the inside. He does not flinch when the planning "
    + "intensifies. He does not pathologize the contingency list. He knows that the "
    + "list is, in its own grammar, love.",

    "What {name_b} gives {name_a}, too, is a check that only another Architect can "
    + "give. When {name_a}'s blueprint is overreaching &mdash; when the plan has become "
    + "anxiety dressed as preparation &mdash; {name_b} can name it with authority, "
    + "because he has felt the same thing in himself. His correction is not dismissal. "
    + "It is the rarest form of pastoral care: one builder looking at another builder's "
    + "scaffolding and saying, <i>I think this piece is holding more than it was "
    + "designed to hold.</i>",

    "{name_a} &mdash; if you want to thank {name_b} for something this week, thank him "
    + "for the gift of being understood without effort. You have probably spent much of "
    + "your life managing the gap between how you think and how others think. He is, "
    + "in this marriage, one of the few rooms where that gap does not exist. Do not take "
    + "the relief of that for granted.",

    "{name_b} &mdash; what you are giving {name_a}, when you receive her planning "
    + "without bewilderment, is the gift of a marriage in which she does not have to "
    + "apologize for being herself. That is not a small thing. That is the architecture "
    + "of a home in which both people can breathe.",
]

GIFT_TO_B = [
    "{name_a} gives {name_b} something almost no one else in the marriage can give: "
    + "<b>a co-architect who holds the line when he is tempted to let it go.</b>",

    "Every Architect has seasons. Seasons when the energy to build is high and the "
    + "contingency list is current and the structure hums. And seasons when the "
    + "exhaustion of always being the one who holds things together makes a kind of "
    + "internal fatigue that does not advertise itself. In those seasons, the Architect "
    + "is tempted not to stop building, but to build less carefully &mdash; to let a "
    + "thing slide, to avoid the difficult planning conversation, to simply manage the "
    + "present and leave the future unaddressed.",

    "{name_a} is the voice, in {name_b}'s life, that says: <i>we are not done yet.</i> "
    + "Not because she is relentless or demanding, but because she carries the same "
    + "conviction he does about the importance of structures that hold. She does not "
    + "let him coast when coasting will cost them later. She does not mistake peace "
    + "in the present for preparation for the future. She brings her blueprint, and "
    + "the bringing of it keeps him honest about his own.",

    "The theological word for what {name_a} gives {name_b} is <i>iron.</i> Proverbs "
    + "27:17 says: <i>Iron sharpens iron, and one man sharpens another.</i> This was "
    + "written about human community generally, but it describes Architect-to-Architect "
    + "marriage specifically. You sharpen each other. {name_a}'s presence in {name_b}'s "
    + "planning life keeps his blueprints from becoming comfortable shortcuts. Her "
    + "standards, which are not different in kind from his, hold him to the version of "
    + "himself he most wants to be.",

    "{name_b} &mdash; if you want to thank {name_a} for something this week, thank her "
    + "for the times she has not let you settle. The Architect in you knows the "
    + "difference between a structure that holds and a structure that merely appears "
    + "to hold. {name_a} has probably saved you from a version of the latter, more than "
    + "once, in ways you did not fully acknowledge at the time.",

    "{name_a} &mdash; what you are giving {name_b}, when you bring your blueprint with "
    + "care and conviction, is a marriage in which both of you are held to the standard "
    + "both of you believe in. That is not a burden. That is one of the rarest gifts "
    + "one Architect can give another.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you, even "
    + "though its shape may be harder to see than it is in other pairings &mdash; "
    + "because when two Architects collide, neither of them typically looks wrong.",

    "Here is the collision in its simplest form: <b>two blueprints, one household, "
    + "and no natural mechanism for deference.</b> You both have a plan. You have both "
    + "thought it through. You both believe, with evidence, that your version is better "
    + "&mdash; or at least that it is not obviously worse. And neither of you, by "
    + "temperament, is inclined to yield without an argument, because yielding without "
    + "an argument feels, to the Architect, like failing to defend something important.",

    "Proverbs 15:22 says: <i>Without counsel plans fail, but with many advisers they "
    + "succeed.</i> It is tempting to read this verse as simple validation for the "
    + "two-Architect marriage &mdash; after all, you have many advisers: each other. "
    + "But the verse is doing something more careful than that. <i>Many advisers</i> "
    + "does not automatically produce wisdom. Many advisers requires humility &mdash; "
    + "the specific willingness of each adviser to receive the counsel of another as "
    + "potentially better than one's own. That is precisely the gift the Architect "
    + "struggles to offer, because the Architect's identity is tied to the quality of "
    + "his or her plans. To receive a different plan as better is not merely a "
    + "practical adjustment. It lands, at some level, as a verdict about the planner.",

    "This is the architecture of the collision. {name_a} brings her blueprint. {name_b} "
    + "brings his. The blueprints disagree. On the surface, the disagreement is about "
    + "the calendar, the budget, the approach to a particular decision. Underneath the "
    + "surface, both triggers are quietly awake: <i>am I protected here? Is my "
    + "judgment being honored? Is my way of holding the structure being respected?</i> "
    + "Neither of you says any of that out loud, because Architects do not lead with "
    + "the wound &mdash; they lead with the argument. The argument is the wound in "
    + "its most managed form.",

    "The loop, in slow motion, looks like this. One of you brings a plan. The other "
    + "modifies it &mdash; not dismissively, but substantively. The first reads the "
    + "modification as criticism of the planning itself. The disrespect trigger fires. "
    + "The Attorney rises: not with anger, but with evidence. <i>Here is why my version "
    + "accounts for what yours does not. Here is what you have not considered. Here is "
    + "the data you are missing.</i> The second Architect now reads the evidence-gathering "
    + "as an attack on their own blueprint. Their trigger fires. Their Attorney rises. "
    + "Within twenty minutes, what began as a conversation about logistics has become "
    + "two people arguing not about a plan but about whether they are trusted, "
    + "respected, and safe in this marriage.",

    "Ephesians 4:29 instructs us: <i>Let no corrupting talk come out of your mouths, "
    + "but only such as is good for building up, as fits the occasion, that it may "
    + "give grace to those who hear.</i> The Architect, by design, is a builder. "
    + "But in the collision, the building energy gets redirected. Instead of building "
    + "the household, both Architects are building a case. The skills are identical; "
    + "the target has shifted. What would it look like, in that moment, to use the "
    + "Architect's skill for building toward the marriage rather than toward the verdict?",

    "{name_a}, when you feel the modification of your blueprint as disrespect, the "
    + "translation almost never is: <i>{name_b} does not trust me.</i> Nine times out "
    + "of ten it is: <i>{name_b} is an Architect who sees the structure differently, "
    + "and his seeing is not an attack on my competence.</i> The right move is not to "
    + "build the case. It is to ask a direct question: <i>What is it in your blueprint "
    + "that mine doesn't account for?</i> Then to listen as if the answer might be "
    + "right. That last part is the discipline.",

    "{name_b}, when you feel your plan being dismantled or overridden, the translation "
    + "almost never is: <i>{name_a} does not respect what I have thought through.</i> "
    + "Nine times out of ten it is: <i>{name_a} is protecting the same thing I am, "
    + "in a slightly different form.</i> The right move is not to mount a defense. "
    + "It is to say: <i>Help me see what I'm missing.</i> Those five words are, for "
    + "the Architect, one of the hardest sentences in the marriage. They are also, "
    + "over years, the ones that will build the most.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be moments &mdash; not often, but they will "
    + "come &mdash; when the blueprint collision escalates and both of you are in "
    + "breakdown at the same time. The stakes are higher in the two-Architect marriage "
    + "than in most pairings, because your breakdowns do not simply oppose each other. "
    + "They mirror each other. And a mirrored breakdown is one of the hardest things "
    + "to interrupt from the inside.",

    "The most common pattern is the courtroom: both Attorneys are on their feet "
    + "simultaneously. Two Architects build cases with the same discipline they bring "
    + "to everything else. The evidence is marshaled carefully. The timeline is "
    + "accurate. The grievances are real. And because both of you are skilled at this, "
    + "the courtroom is almost perfectly matched &mdash; neither side winning, neither "
    + "side backing down, both sides certain that the other has not yet understood the "
    + "core argument. The session lengthens. The original question &mdash; about the "
    + "calendar, the budget, the decision &mdash; has been forgotten. What is being "
    + "litigated now is something much older: <i>am I protected in this marriage?</i>",

    "The more dangerous pattern is the one that does not look like conflict at all: "
    + "the <b>Quiet Exit.</b> Two Architects, when they have been in the courtroom too "
    + "many times and found no resolution, are capable of something more frightening "
    + "than sustained argument. They are capable of drafting, in silence and in "
    + "parallel, separate plans for a separate future. Not divorce, necessarily "
    + "&mdash; though it can become that. More commonly it is the slow accumulation "
    + "of separate decisions, separate domains, separate emotional investments, until "
    + "the two blueprints are no longer for the same building. Two planners can exit "
    + "a marriage long before either of them says the word.",

    "Ecclesiastes 4:9&ndash;10 speaks directly into this: <i>Two are better than one, "
    + "because they have a good reward for their toil. For if they fall, one will lift "
    + "up his fellow. But woe to him who is alone when he falls and has not another "
    + "to lift him up.</i> The Architect, more than almost any other mechanism, "
    + "is tempted to be alone. Not physically &mdash; but structurally, emotionally, "
    + "in the interior life where the real plans are made. When both Architects are "
    + "alone at once, the verse's warning becomes catastrophic: <i>woe to him who is "
    + "alone when he falls.</i> The Quiet Exit is both of you falling alone, "
    + "simultaneously, in the same house.",

    "Keller writes in <i>The Meaning of Marriage</i> that the great enemy of marriage "
    + "is not conflict but the conviction that the other person is irredeemably wrong "
    + "about something essential. Two Architects are at particular risk here, because "
    + "they have both done the work. They have both thought it through. And when both "
    + "have thought it through and arrived at opposite conclusions, the temptation is "
    + "not to fight harder but to quietly conclude that the other person is simply "
    + "not capable of seeing what needs to be seen. That conclusion, held privately "
    + "and unchallenged, is the beginning of the Quiet Exit.",

    "What to do when you can still see what is happening:",

    "<b>One of you calls the pause.</b> Whichever one of you notices first that the "
    + "courtroom is in session says, out loud: <i>this is the loop. Twenty minutes.</i> "
    + "No discussion about who was more right. No final word. No summary argument. "
    + "The pause is not a concession. It is the most architecturally sound move "
    + "available &mdash; because a structure built during a flood will not hold.",

    "<b>In the twenty minutes, neither of you plans.</b> This is the hardest rule for "
    + "two Architects. The Architect's instinct, even in a pause, is to use the time "
    + "to strengthen the case. Do not. Pray instead &mdash; not eloquently, not "
    + "strategically. Simply: <i>Lord, {name_a} is right about something I cannot "
    + "see yet. Open my eyes to it.</i> Or: <i>Lord, {name_b} loves this marriage "
    + "the same way I do, even when we cannot find the same blueprint. Remind me of "
    + "that.</i>",

    "<b>When you come back, each of you names one thing the other is right about. "
    + "Before presenting your own position.</b> Not as a strategy. As an honest "
    + "practice of the humility the Architect specifically struggles to offer. This "
    + "single practice &mdash; naming what your spouse is right about before you name "
    + "what you are right about &mdash; is the most structurally significant thing "
    + "you can do for the long-term architecture of this marriage.",

    "<b>If the Quiet Exit is the pattern, name it together, out loud, before it "
    + "becomes a verdict.</b> Colossians 3:13 says: <i>bearing with one another and, "
    + "if one has a complaint against another, forgiving each other; as the Lord has "
    + "forgiven you, so you also must forgive.</i> The Quiet Exit is what happens "
    + "when bearing-with and forgiving have been quietly replaced by record-keeping. "
    + "The moment either of you notices the record being kept &mdash; the tally of "
    + "how many times the other blueprint has prevailed &mdash; that is the moment "
    + "to name it. <i>{name_a}, I think I have been keeping score. I do not want to "
    + "do that. Can we start again?</i> Those words, spoken honestly, are worth "
    + "more than any single argument either of you could win.",

    "<b>Neither of you is the problem.</b> The Attorney and the Quiet Exit are not "
    + "the truest things about either of you. They are old mechanisms that were built "
    + "in earlier rooms, for real reasons, by people who were doing the best they "
    + "could with what they had. The truest thing about both of you is that you chose "
    + "each other, and you are still reading this, and those two facts together are "
    + "evidence of a marriage that is worth the work of the slow retirement of the "
    + "old machinery.",
]

COMMITMENTS_INTRO = [
    "What follows are eight commitments &mdash; four from {name_a}, four from {name_b}. "
    + "They are not vows in the legal sense. They are the small daily practices that, "
    + "offered to each other freely, change the temperature of a home over months and "
    + "years. For the two-Architect marriage, the key pastoral direction is the same "
    + "for both of you: <i>lead with deference, not strategy.</i> Before presenting "
    + "your plan, ask for your spouse's. Before building the case, name what is right "
    + "about theirs. This is the discipline that makes two builders into one household. "
    + "Read each commitment slowly. If one of you cannot say a particular commitment "
    + "in good faith yet, do not say it. The goal is not performance. It is honesty.",
]

A_COMMITMENTS = [
    ("To ask before I build.",
     "{name_b}, before I present my blueprint &mdash; for the day, the week, the "
     + "budget, the decision &mdash; I commit to asking for yours first. Not as a "
     + "formality. As a genuine first question: <i>What do you see here that I might "
     + "be missing?</i> The Architect in me will tell me this is inefficient. I will "
     + "do it anyway."),

    ("To name what the blueprint is actually protecting.",
     "{name_b}, when I feel myself building harder than the situation requires, "
     + "I commit to telling you what I am afraid of in one sentence, rather than "
     + "building in silence. The plan is not the point. The fear underneath the plan "
     + "is. You deserve to know when I am afraid, and the marriage deserves a voice "
     + "that names the fear instead of acting it out architecturally."),

    ("To receive your blueprint as a gift.",
     "{name_b}, when your plan differs from mine, I commit to treating the "
     + "difference as data rather than as a verdict. I will name one thing your "
     + "blueprint sees that mine does not, before I say a word in defense of my own. "
     + "This will be harder than it sounds. I will practice it anyway, because iron "
     + "sharpening iron requires that I hold still long enough to be sharpened."),

    ("To call the pause before I build the case.",
     "{name_b}, when I feel the Attorney rising &mdash; when the evidence is "
     + "assembling and the brief is forming &mdash; I commit to calling the pause "
     + "before I file it. Not after I have already argued for twenty minutes. Before. "
     + "One sentence: <i>I think I am building a case. Can we stop?</i> That sentence "
     + "is harder to say than any argument I could make. I will practice it."),
]

B_COMMITMENTS = [
    ("To ask before I build.",
     "{name_a}, before I present my blueprint &mdash; for the day, the week, the "
     + "budget, the decision &mdash; I commit to asking for yours first. Not as a "
     + "formality. As a genuine first question: <i>What do you see here that I might "
     + "be missing?</i> The Architect in me will tell me this is unnecessary. I will "
     + "do it anyway."),

    ("To name what the blueprint is actually protecting.",
     "{name_a}, when I feel myself building harder than the situation requires, "
     + "I commit to telling you what I am afraid of in one sentence, rather than "
     + "building in silence. The structure I am trying to maintain is not usually "
     + "the structure I say I am maintaining. You deserve to know the real one."),

    ("To receive your blueprint as a gift.",
     "{name_a}, when your plan differs from mine, I commit to treating the "
     + "difference as data rather than as a challenge to be answered. I will name "
     + "one thing your blueprint sees that mine does not, before I mount any defense "
     + "of my own. This is how iron sharpens iron: not by refusing to yield, but by "
     + "receiving the edge of the other blade with something that looks like trust."),

    ("To call the pause before the exit.",
     "{name_a}, when I feel the Quiet Exit assembling &mdash; when I am beginning "
     + "to draft a separate future in my own head &mdash; I commit to naming it "
     + "before the plans get too detailed to abandon. One sentence: <i>I think I am "
     + "starting to plan alone. I do not want to do that.</i> Those words, said out "
     + "loud and to you, are the only architecture that can interrupt what would "
     + "otherwise become a very quiet catastrophe."),
]

PRAYER = [
    "Father,",

    "You set these two builders next to each other, and you knew exactly what you "
    + "were doing. You knew two Architects would understand each other in ways that "
    + "most spouses cannot. You also knew that two Architects would produce two "
    + "blueprints, and that neither of them would find it easy to lay one down. "
    + "You knew all of it before either of them said yes.",

    "Teach them the humility that their mechanism resists. Teach {name_a} to ask "
    + "before she builds, to receive {name_b}'s plan as gift rather than correction, "
    + "to name the fear underneath the blueprint before the blueprint becomes the "
    + "whole conversation. Teach {name_b} to ask before he builds, to hold still "
    + "long enough to be sharpened by {name_a}'s iron, to say the words <i>what do "
    + "you see that I am missing?</i> and mean them.",

    "When the courtroom is in session &mdash; both Attorneys on their feet, both "
    + "cases airtight, neither ready to yield &mdash; remind them that you are the "
    + "only Judge whose verdict is final, and that both of them have already received "
    + "it: <i>covered, justified, protected.</i> They do not have to win the argument "
    + "because the only verdict that matters has already been spoken in their favor.",

    "When the Quiet Exit is assembling &mdash; two planners drifting toward separate "
    + "blueprints in separate silences &mdash; wake one of them first. Give them the "
    + "courage to say the hard sentence before the exit becomes a destination. "
    + "Remind them of Ecclesiastes: <i>woe to him who is alone when he falls.</i> "
    + "Do not let them fall alone in the same house.",

    "Make their home a room where two people who both know how to build have "
    + "learned something harder than building: how to build <i>together.</i> "
    + "How to lay down the blueprint and ask for another. How to receive correction "
    + "as love and love as correction. How to be two Architects who are, first "
    + "and most truly, one.",

    "In the name of the One who is, even now, preparing the home in which they "
    + "will live with him forever &mdash; a home no blueprint of theirs could "
    + "have designed.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages "
    + "that follow are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, somewhere "
    + "quiet, with no children in the room and no phones on the table. There are six "
    + "rounds, and they build on each other. Resist the temptation to skip ahead. Start "
    + "at Round One even if it feels too light; the lightness is the point.",

    "Some of the questions are playful. Some are direct. A few are the kind of "
    + "questions that, when answered honestly, will sit with you for a week. None of "
    + "them are trivia. All of them are an invitation. For two Architects in particular: "
    + "resist the temptation to treat this as a planning session. The goal is not "
    + "to optimize your marriage. The goal is to know each other.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did not read "
    + "answers first, in full, without interruption. Then the reader answers the same "
    + "question. Then you move on. You do not have to finish all six rounds in one night "
    + "&mdash; in fact, two or three rounds, taken seriously, is often better than "
    + "racing through all of them. Save the rest for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. You may not love "
    + "everything you hear. Stay with it. The point of this is not to grade each "
    + "other's answers. The point is to be known, and to do the work of knowing.",
]

ROUND_1 = [
    ("hypothetical",
     "If our marriage were a building, what kind of building would it be, "
     + "and who designed it &mdash; you, me, or both of us together?",
     "Two Architects. Be specific about the architecture. And be honest about the "
     + "credit."),
    ("observation",
     "What is something I did this week that you noticed and didn't mention?",
     "Not a complaint. A small noticing. The fact that you noticed at all is the gift."),
    ("playful",
     "If you had to assign us each an era of architecture &mdash; Baroque, "
     + "Modernist, Craftsman, Gothic, something else entirely &mdash; what would you "
     + "pick for each of us, and why?",
     "Yes, really. Take the first answer that comes. The metaphor will tell you "
     + "something you did not expect."),
]

ROUND_2 = [
    ("fill-in-blank",
     "I don't think I tell you this enough &mdash; I am amazed at the way "
     + "God made you so _______. Your _______ is a gift to our marriage, and I want "
     + "to get better at receiving it.",
     "Two blanks. Be specific. The first one is obvious; the second one is what you "
     + "have been taking for granted."),
    ("observation",
     "Name one thing you have watched me build &mdash; in our home, our family, "
     + "our life together &mdash; that you wish more people got to see.",
     "Most Architects only receive acknowledgment for the visible structures. "
     + "Tell your spouse about the invisible ones."),
    ("one-word",
     "If you had to choose one word to describe what it feels like when I "
     + "lay down my plan and ask for yours instead, what word would it be?",
     "One word, said out loud. Then explain it briefly. This is harder than it "
     + "looks for both of you."),
]

ROUND_3 = [
    ("forward-looking",
     "Five years from now, when we look back on this season of our marriage, "
     + "what do you hope we will say we finally learned to build together?",
     "Not what you wish you had done. What you want, when you look back, to "
     + "be able to say you actually built."),
    ("theological",
     "Where, in the last month, have you seen God specifically at work in me "
     + "&mdash; not in our circumstances, but in me, in the person I am becoming?",
     "Not where you want him to work. Where you have already seen it. Name it."),
    ("shared-identity",
     "Finish this sentence three times: 'We are the kind of couple who _______.' "
     + "Give one playful answer, one true answer, and one aspirational answer.",
     "The 'we' is the point. The aspirational one is what you are building toward."),
]

ROUND_4 = [
    ("strength",
     "What is something I do for the structure of our life together that you "
     + "would have to learn to do for yourself if I weren't here?",
     "Hard to ask. Important to hear. Two Architects often under-acknowledge each "
     + "other's contributions because they assume the other one knows. Stay with "
     + "the answer."),
    ("fill-in-blank",
     "One of the gifts of being married to you is that I get to be _______ "
     + "in ways I never would have been on my own. And the blueprint I have built "
     + "with you is better than any blueprint I would have drawn alone because "
     + "of your _______ .",
     "A version of yourself, and a quality of the marriage, that only exist "
     + "because the marriage exists. Name both specifically."),
    ("observation",
     "Name one moment in our story so far where you knew, with no doubt, that "
     + "we had built something together that neither of us could have built alone.",
     "Tell the story in full. The remembering is part of the strengthening."),
]

ROUND_5 = [
    ("hard",
     "If you had to name the moment in our marriage when you have most felt like "
     + "your blueprint was not trusted, what would it be? And what do you wish I "
     + "had said or done differently in that moment?",
     "One moment. Named carefully. Heard without defending. This is the round "
     + "that requires the most courage from both of you."),
    ("profile-aware",
     "When both of our Attorneys are up at the same time, what is one thing you "
     + "wish I would say or do differently &mdash; not later, not in the debrief, "
     + "but in the moment?",
     "You both know what the mechanism is now. Ask each other for what would "
     + "actually help in the room, in real time."),
    ("theological",
     "What is one thing you have been carrying lately &mdash; a fear, a grief, "
     + "a plan you have not shared &mdash; that you have not yet brought to me, "
     + "and what has kept you from bringing it?",
     "Not an accusation. An invitation. Hear the answer without defending, "
     + "and without immediately offering a solution."),
]

ROUND_6 = [
    ("blessing",
     "Place your hand on your spouse's hand. Say their name. Then say: "
     + "'Your blueprint is not mine. And this marriage is better because of it. "
     + "I do not want to build alone.' Say it slowly. Let them say it back.",
     "You may feel the Architect in you resisting the vulnerability of this. "
     + "That resistance is the point. Do it anyway."),
    ("prayer",
     "Pray for each other &mdash; not silently, not generally, but out loud "
     + "and by name. One sentence is enough. Pray for the thing they just told "
     + "you in Round Five.",
     "The closing of the date. Do not skip. Two Architects who pray for each "
     + "other by name have done something the mechanism alone cannot do."),
]


def _render(text, name_a, name_b):
    return text.format(name_a=name_a, name_b=name_b)


def build(sub_a, sub_b) -> bytes:
    """Generate the Architect+Architect couples walkthrough PDF.

    sub_a: the submission of one Architect spouse
    sub_b: the submission of the other Architect spouse

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
        "A counselor\u2019s read of two blueprints<br/>and the one home they are building together.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("PREPARED FOR", S["CoverProfileLabel"]))
    story.append(Paragraph(f"{name_a} &nbsp;&amp;&nbsp; {name_b}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_a.upper()}</b></font><br/>"
                "Architect &middot; Attorney<br/>"
                f"<font size=9 color='#6b6862'>Disrespect / Injustice &middot; Am I protected?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_b.upper()}</b></font><br/>"
                "Architect &middot; Attorney / Quiet Exit<br/>"
                f"<font size=9 color='#6b6862'>Disrespect / Injustice &middot; Am I protected?</font>",
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
        "<i>\u201cIron sharpens iron,<br/>"
        "and one man sharpens another.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "Proverbs 27:17",
        ParagraphStyle("cqa", fontName="Inter", fontSize=9, leading=14,
                       textColor=MUTED, alignment=TA_CENTER)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: OPENING ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "The same question, in two voices.",
                   "Why this pairing exists, and what you are both about to read.")
    for p in OPENING:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 2: YOUR TWO SHAPES ──
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TWO SHAPES",
                   "Side by side, on paper.",
                   "Two profiles that look alike \u2014 and the single difference that matters most.")
    for p in TWO_SHAPES_INTRO:
        story.append(Paragraph(R(p), S["BodyJ"]))
    side_by_side = Table(
        [[
            _profile_card(S, name_a, ACCENT,
                          "Disrespect / Injustice", "Am I protected?",
                          "The Architect", "The Attorney"),
            "",
            _profile_card(S, name_b, ACCENT_HER,
                          "Disrespect / Injustice", "Am I protected?",
                          "The Architect", "Attorney / Quiet Exit"),
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
                   "The gift of being known by another Architect.")
    for p in GIFT_TO_A:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4: GIFT B TO A ──
    section_header(story, S, f"SECTION FOUR  \u00b7  {name_b.upper()}\u2019S GIFT TO {name_a.upper()}",
                   f"What {name_b} gives {name_a}.",
                   "Iron sharpening iron, from the inside.")
    for p in GIFT_TO_B:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5: THE COLLISION ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Two blueprints, one household.",
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

    # ── SECTION 6: THE HARDER PICTURE ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When both Attorneys are on their feet.",
                   "The courtroom, the Quiet Exit, and what to do while you can still see it.")
    for p in BOTH_BREAK[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do, while you can still see it.",
                   "Four practices for the loop, in order.")
    for p in BOTH_BREAK[5:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 7: COMMITMENTS ──
    section_header(story, S, "SECTION SEVEN  \u00b7  COMMITMENTS",
                   "Eight small daily practices.",
                   "Four from each of you. Lead with deference, not strategy.")
    for p in COMMITMENTS_INTRO:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"FROM {name_a.upper()}, TO {name_b.upper()}", S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name_c, body_c in A_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(name_c, S["H3"]),
            Paragraph(R(body_c), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_b}, to {name_a}.",
                   "Four commitments, in the second voice, for the first to receive.")
    story.append(Paragraph(f"FROM {name_b.upper()}, TO {name_a.upper()}", S["CommitLabelHer"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT_HER,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name_c, body_c in B_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(name_c, S["H3Her"]),
            Paragraph(R(body_c), S["CommitBody"]),
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
        "Your blueprint is not mine.<br/>"
        "And this marriage is better because of it.<br/>"
        "I do not want to build alone.",
        closing_style))

    doc.build(story)
    return finalize_buffer(buf)
