"""Couples Walkthrough — Architect + Vault.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where one spouse is an Architect and the
other is a Vault. First names are substituted from the submissions:
    {name_arch}  -> the Architect spouse's first name
    {name_vault} -> the Vault spouse's first name

Pastoral dynamic: The Architect wants to plan from full information;
the Vault provides curated finished conclusions. Each experiences the
other as withholding what they need most.
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


# ──────────── PROSE — uses {name_arch} and {name_vault} placeholders ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small repeating ones "
    "&mdash; the same misfire in slightly different clothes, four or five times a week, year "
    "after year, until both people have quietly forgotten what they were originally hoping for "
    "when they said yes to each other.",

    "What follows is a counselor's read of the specific, recurring misfire in your particular "
    "marriage. Not the dramatic failures, which you have either addressed or are managing. The "
    "quiet ones. The ones that happen on a Wednesday evening in the kitchen when nothing is "
    "technically wrong, and neither of you can quite explain, the next morning, why the night "
    "felt like it ended a degree colder than it started.",

    "You are both reading this because you have decided to look at those rocks. That decision "
    "is more significant than it may appear. Most couples spend years navigating around them "
    "without ever naming them. Naming them &mdash; together, on paper, before the same "
    "counselor's voice &mdash; is more than half the work.",

    "Here is what I want to do for you. I will name what each of you brings the other that "
    "you could not have built alone &mdash; the genuine theological gift that your two very "
    "different shapes form together. Then I will name the collision your two core questions "
    "create, in the specific way it shows up in your marriage. Then I will name the harder "
    "picture &mdash; what happens when both of you are in breakdown at the same time &mdash; "
    "and what to do in that moment. Then I will hand each of you commitments: not rules, but "
    "the kind of small daily practices that, offered to each other freely and faithfully, "
    "change the temperature of a home across years.",

    "Read it together if you can. If you cannot, read it separately and then sit down with "
    "it together. Argue with what does not fit. Stay with what does. The goal is not insight "
    "for its own sake. The goal is a marriage in which {name_arch} and {name_vault} can be "
    "more fully known to each other &mdash; not perfectly, but more than they are today.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on paper, "
    "side by side. Most couples never see their two profiles next to each other with this kind "
    "of clarity. You are about to.",
]

TWO_SHAPES_BODY = [
    "{name_arch}, you are an <b>Architect</b> whose body reads disrespect as a warning alarm "
    "and whose deepest question is <i>am I protected?</i> You build structures &mdash; plans, "
    "schedules, contingencies, the long view &mdash; because you believe, at a level below "
    "conscious reasoning, that most of the suffering in an ordinary life is a function of "
    "insufficient preparation. When the building feels threatened, an <b>Attorney</b> takes "
    "the floor and begins to litigate the case that the threat is real, and that someone is "
    "responsible for the insufficient protection.",

    "{name_vault}, you are a <b>Vault</b> whose body reads shame as an alarm and whose "
    "deepest question is <i>am I acceptable?</i> You have learned, over a long time and for "
    "reasons that were once good ones, to keep the messy middle of your interior life "
    "private. You process internally and bring others the finished conclusion. The half-built "
    "house, the unresolved grief, the question you have not yet answered &mdash; these stay "
    "inside, because what has been shown in the past without preparation has sometimes been "
    "handled carelessly. When a wound lands large enough that the Vault cannot contain it, "
    "an <b>Attorney</b> takes the floor &mdash; not with heat, but with a file: organized, "
    "dated, precise, and years in the keeping.",

    "Notice what these two profiles share, and notice what they do not. You are both "
    "protected by something. {name_arch} is protected by planning and structure. {name_vault} "
    "is protected by selectivity and curation. Both of you, in different costumes, have "
    "learned to keep something at bay. The Architect keeps chaos at bay by building ahead of "
    "it. The Vault keeps exposure at bay by choosing what to show and what to hold.",

    "But underneath the two strategies is a more interesting asymmetry. {name_arch}'s "
    "question &mdash; <i>am I protected?</i> &mdash; is forward-looking. The Architect is "
    "scanning the horizon for incoming. {name_vault}'s question &mdash; <i>am I "
    "acceptable?</i> &mdash; is inward-looking. The Vault is scanning the interior for "
    "anything that, if seen, might produce the verdict that the Vault dreads. These two "
    "orientations mean that, in any ordinary conflict, you are often facing different "
    "directions entirely. {name_arch} is watching the perimeter. {name_vault} is watching "
    "the interior. Neither of you, in those moments, is quite looking at each other.",

    "And yet you chose each other, and the choosing was not random. The Architect is drawn "
    "to the Vault's composure &mdash; the sense that {name_vault} has things sorted, "
    "processed, handled, which mirrors the Architect's own ambition toward order. The Vault "
    "is drawn to the Architect's competence &mdash; the sense that {name_arch} will hold "
    "what needs holding, which is precisely the kind of reliable covering that makes "
    "selective disclosure slightly less frightening. You recognized something in each other "
    "before you had words for it. This document is part of finding the words.",
]

GIFT_TO_ARCH = [
    "{name_vault} gives {name_arch} something most planners in his life will never provide: "
    "<b>a response that is not already organized around what he needs to do next.</b>",

    "The Architect's world is populated, largely, by people who are one more piece of "
    "incoming information. The neighbor mentions the weather; the Architect has already "
    "calculated its effect on Saturday's project. A colleague names a concern; the Architect "
    "is already building the response before the sentence ends. Most people, in {name_arch}'s "
    "life, are inputs that require outputs. The building never fully stops.",

    "{name_vault}, by virtue of being a Vault, gives {name_arch} something rarer than he "
    "may realize. When {name_vault} speaks, she speaks deliberately. She has already "
    "processed what she is about to say. She does not scatter her interior on the table and "
    "ask {name_arch} to help sort it. What she offers him &mdash; when she offers it &mdash; "
    "is considered. Organized. Selected. For the Architect, who is accustomed to managing "
    "everyone's loose ends, this is the gift of a person who does not add to the pile.",

    "There is more. {name_vault}'s composure gives {name_arch} permission to believe the "
    "perimeter is, at least partially, holding. The Vault's steadiness &mdash; her ability "
    "to manage her interior without broadcasting every fluctuation &mdash; reads to the "
    "Architect as <i>the home is not on fire.</i> For a person whose alarm system scans "
    "constantly for incoming threats, this steadiness is a genuine mercy.",

    "The theological word for what {name_vault} gives {name_arch} is something close to "
    "<i>peace</i> &mdash; not the false peace of pretended contentment, but the ordinary "
    "peace of a person who does not require her spouse to be vigilant on her behalf at every "
    "moment. Philippians 4:7 speaks of a peace that passes understanding. {name_vault} is "
    "not that peace &mdash; she is a person, not a promise &mdash; but her composure "
    "creates, in the home, something that functions like a quiet clearing in the Architect's "
    "otherwise very loud forest.",

    "{name_arch} &mdash; if you want to thank {name_vault} for something this week, thank "
    "her for the times she has handled her interior alone so that you could tend to what was "
    "in front of you. She may not know that her composure reads as a gift. Vaults are "
    "often told their privacy is the problem, not the contribution. Tell her otherwise. She "
    "will not know what to do with the compliment. Say it anyway.",
]

GIFT_TO_VAULT = [
    "{name_arch} gives {name_vault} something the Vault has always needed but would rarely "
    "build for herself: <b>a structure that does not require her to present a finished "
    "product before she is allowed to exist in it.</b>",

    "The Vault's relationship with structure is complicated. {name_vault}, you tend to "
    "under-build your external life, not because you are disorganized &mdash; you are "
    "not &mdash; but because committing to a structure in advance feels, at some level, "
    "like promising to show a finished product on a deadline. Calendars, plans, long-view "
    "decisions: these feel like exposure-by-anticipation. Better to leave them loose and "
    "move when necessary.",

    "The cost of this is rarely visible until something slips. An opportunity passes because "
    "no one had arranged to pursue it. A decision that needed to be made three months ago "
    "is being made today under pressure. The Vault's preference for the unscheduled life "
    "is partly a preference for the unexamined one &mdash; because a scheduled life "
    "requires showing where you are going, which requires showing where you have been.",

    "{name_arch}, by virtue of being an Architect, builds the structure around the marriage "
    "that {name_vault} would have been unlikely to build alone. The calendar holds. The "
    "long-view is tended. The contingencies are thought through. This is not administration; "
    "this is a form of love. The Architect builds covering so the people inside the structure "
    "can live without perpetually managing the structure itself.",

    "There is a biblical word for what {name_arch} gives {name_vault}, and it is "
    "<i>covering</i> &mdash; in the older, covenantal sense of one person standing in the "
    "weather so another can grow. Ephesians 5 speaks of a husband loving his wife as Christ "
    "loved the church &mdash; and the love of Christ for the church is, in large part, the "
    "love of one who came to do what we could not do for ourselves. {name_arch} loves "
    "{name_vault} by building what she could not, or would not, build alone. That is not "
    "a small thing.",

    "{name_vault} &mdash; if you want to thank {name_arch} for something this week, thank "
    "him for one specific piece of the structure that he built that you did not have to build. "
    "The plans he made so you did not have to. The calendar he holds so you can live inside "
    "it without managing it. He may not hear gratitude in this area often because the trellis "
    "that works is invisible. Make it visible once. He will not know what to do with it. "
    "Say it anyway.",
]

COLLISION = [
    "Now we come to the specific, recurring misfire &mdash; the small repeating rock. It "
    "will be familiar to both of you, even if you have not named it this precisely.",

    "{name_arch}'s core question is <i>am I protected?</i> The way the Architect answers "
    "this question is by securing information. In order to plan well, the Architect needs "
    "full information. He needs to know where things are, what the condition of the interior "
    "is, what challenges are on the horizon that have not yet been addressed. The Architect "
    "does not ask for your interior out of nosiness or control. He asks because, in his "
    "grammar, incomplete information is unsafe. He is, in his own mind, trying to love you "
    "by knowing enough to plan around you.",

    "{name_vault}'s core question is <i>am I acceptable?</i> The way the Vault answers "
    "this question is by controlling the exposure of her interior. What she shows is chosen. "
    "What she holds is organized and private. She does not withhold from {name_arch} out of "
    "mistrust or indifference. She withholds because the messy middle &mdash; the "
    "unresolved question, the not-yet-processed grief, the interior in its working "
    "state &mdash; has not felt safe to show. And she has a precise and accurate knowledge "
    "of what is inside, which makes the risk of exposure feel proportionally large.",

    "The collision is this: {name_arch} cannot plan around an interior that has been "
    "hidden. {name_vault} cannot show an interior to someone whose mode of love is to "
    "deploy that information in a plan. The Architect's love, expressed as inquiry, lands "
    "on the Vault as a demand for the kind of nakedness that has cost her before. The "
    "Vault's love, expressed as composure, lands on the Architect as a closed file he is "
    "being asked to work around blind.",

    "This is not a communication problem. This is an <i>exposure problem.</i> "
    "{name_arch} and {name_vault}, you do not need to get better at talking to each other "
    "before you can address this &mdash; you need to understand what the other person is "
    "actually doing when they do what they do. {name_arch} is not demanding access. He is "
    "asking for enough information to feel like he is not driving the family car with the "
    "windshield blacked out. {name_vault} is not stonewalling. She is protecting something "
    "that has been mishandled before &mdash; something that, if shown to a person whose "
    "next move is to plan around it, would feel less like intimacy and more like being "
    "studied.",

    "Scripture does not resolve this tension cheaply. Proverbs 17:27 says: <i>Whoever "
    "restrains his words has knowledge, and he who has a cool spirit is a man of "
    "understanding.</i> This is the Vault's verse, and the Vault is not wrong to hold it. "
    "Self-command is wisdom. The capacity to hold one's interior and not scatter it is a "
    "genuine virtue. And yet Ephesians 4:25 says: <i>Therefore, having put away falsehood, "
    "let each one of you speak the truth with his neighbor, for we are members one of "
    "another.</i> These verses are not contradictory. They address the same person in two "
    "different modes of failure. Proverbs is speaking to the person who talks without "
    "thinking. Ephesians is speaking to the person who thinks without talking &mdash; who "
    "manages the interior so successfully that the neighbor &mdash; the spouse &mdash; is "
    "excluded from it entirely. {name_vault} must learn to share in measured portions that "
    "{name_arch} can receive. {name_arch} must learn to receive disclosure as a gift rather "
    "than as data.",

    "Here is what the collision looks like in slow motion. It is a Thursday evening. "
    "{name_arch} asks a question about something that has seemed off &mdash; a quieter week, "
    "a decision that has not been made, a conversation that was started and not finished. He "
    "is asking because the Architect's alarm system has noted something and he needs to "
    "assess the situation. To him, this is care. To {name_vault}, the question lands as an "
    "inspection &mdash; someone asking for access to the half-built house before the "
    "construction crew has finished. Her first move is to present a finished conclusion: "
    "<i>I'm fine, we're fine, nothing to worry about.</i> {name_arch} receives this and his "
    "alarm does not quiet. The information is too neat. He asks again, with slightly more "
    "urgency. {name_vault} reads the escalation as pressure &mdash; a demand for the naked "
    "interior &mdash; and the walls go up. {name_arch} reads the walls as withholding, "
    "which fires the disrespect trigger. By the time they go to bed, both of them are "
    "quietly certain the other is the one who pulled away.",

    "{name_arch}, when {name_vault} presents you with a finished conclusion and the alarm "
    "says it is too neat, the right move is not to press harder for the interior. The right "
    "move is to name what you are actually feeling in one sentence &mdash; not an inquiry, "
    "but a disclosure: <i>I feel like I am being asked to plan around something I cannot "
    "see, and that makes me feel unsafe.</i> You are not filing a brief. You are opening a "
    "door. That is a different move, and {name_vault} will receive it differently.",

    "{name_vault}, when {name_arch} asks about your interior with the urgency that tends "
    "to close you down, the right move is not to present the finished version. The right "
    "move is to name the actual condition in one sentence, even if it is incomplete: <i>I "
    "am in the middle of something I have not finished processing, and I will bring you "
    "what I have when I have it.</i> This is not full exposure. It is a measured portion "
    "{name_arch} can receive. And the Architect, who respects directness, will receive it "
    "far better than the silence that currently reads to him as a closed file.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be moments &mdash; not often, God willing, but they "
    "will come &mdash; when the small collision in the kitchen escalates and both of you are "
    "in breakdown at the same time. The Attorney is up in {name_arch}. The Attorney is up "
    "in {name_vault}. Two very different versions of the same breakdown are in the same room. "
    "What happens in that room deserves to be named plainly.",

    "The Architect's Attorney argues in real time. It builds a case from the current "
    "evidence, presses for acknowledgment, and requires the other person to engage with "
    "the brief before the conversation can close. {name_arch}'s Attorney, when it is up, "
    "will cite what {name_vault} said three weeks ago, and what happened in August, and the "
    "pattern he has been noticing for two months. He is not, in his own mind, prosecuting "
    "his spouse. He is establishing the record so that the next plan can be built on "
    "accurate information. In {name_vault}'s ears, this sounds like an indictment.",

    "The Vault's Attorney is different, and the difference is important to name. {name_vault}'s "
    "Attorney does not argue in real time. The Vault has been keeping a file &mdash; "
    "organized, dated, cross-referenced &mdash; and when a wound lands large enough, the "
    "vault opens. What comes out is not heat. It is precision. Specific words from specific "
    "conversations, with context and consequence. {name_arch} will ask, when this happens: "
    "<i>How long have you been keeping that?</i> The answer is: years. And the Architect, "
    "who was pressing for more information, will find that he was not quite prepared for "
    "this much information, delivered this way.",

    "The loop these two Attorneys create together is one of the slower and more corrosive "
    "loops in the taxonomy. Neither Attorney is loud, necessarily. The Architect's is "
    "urgent and forward-pressing. The Vault's is quiet and backward-citing. Together they "
    "can occupy the same room for an hour without either person feeling heard, because the "
    "Architect is pressing for acknowledgment of the current situation and the Vault is "
    "delivering evidence about the history. They are, in a literal sense, looking at "
    "different time periods in the same argument.",

    "Hebrews 4:13 interrupts both Attorneys with the same word: <i>And no creature is "
    "hidden from his sight, but all are naked and exposed to the eyes of him to whom we "
    "must give account.</i> {name_vault}, hear this first, because it lands on you with "
    "particular force. The interior you have been so carefully managing &mdash; the file "
    "you have been keeping, the messy middle you have been curating for private "
    "processing &mdash; is not hidden from the only witness who finally matters. God "
    "has already seen everything in the Vault. He is not surprised by a single document. "
    "And the verdict he has spoken is not condemnation. It is <i>covered, clean, "
    "beloved</i> &mdash; in Christ, permanently. The Vault has been hiding from a "
    "witness who is far less generous than the Father; the Father has already seen, "
    "and has already spoken. {name_arch}, this verse lands on you as well. The Architect "
    "is not the keeper of the record. The one who holds all records has spoken his "
    "verdict, and that verdict does not require the Architect's litigation to stand.",

    "What to do when you can both still see what is happening:",

    "<b>One of you calls the pause.</b> Whichever one notices first that the two Attorneys "
    "are in the room says, out loud: <i>this is the loop. Twenty minutes.</i> No final "
    "word. No summary statement. The pause is non-negotiable, and the only rule of the "
    "pause is that neither of you is permitted to use it to add documents to the file or "
    "to draft the next brief.",

    "<b>In the twenty minutes, pray by name.</b> Not a strategy session with God. A "
    "prayer that names what has happened: <i>Lord, my Attorney is up, and {name_vault}'s "
    "file is open, and neither of us can see each other clearly right now. Quiet the "
    "prosecution in both of us. Help us come back to each other as people, not as "
    "cases.</i> If you cannot pray, read Psalm 46:10 slowly. Let it do the work your "
    "words cannot.",

    "<b>When you come back, each of you says one sentence.</b> {name_arch}, your "
    "sentence is not a brief. It is one true thing about what you actually felt, beginning "
    "with <i>I</i>: <i>I felt like I was being asked to plan around a closed room, and "
    "it scared me.</i> {name_vault}, your sentence is not the file. It is the one thing, "
    "the single wound, under all the documents: <i>I felt like what I showed you would "
    "become something to plan around, and not something to simply receive.</i> One "
    "sentence each. Then stop. The Architect who has said one true thing has given the "
    "Vault something to receive as gift, not as data. The Vault who has said one true "
    "thing has given the Architect something to work with that is not a closed door.",

    "<b>Neither of you is the problem.</b> The Attorney in {name_arch} and the Attorney "
    "in {name_vault} are old mechanisms working long shifts. They will retire slowly, and "
    "the marriage that knows this can be patient with the slow retirement. You have "
    "built something together that neither of you could have built alone, and the small "
    "collisions of a Tuesday evening have not undone it. They are, in their strange way, "
    "part of what you are building.",
]

COMMITMENTS_INTRO = [
    "What follows are six commitments &mdash; three from {name_arch}, three from "
    "{name_vault}. They are not vows in the formal sense. They are the small daily "
    "practices that, offered to each other freely and kept with patience, change the "
    "temperature of a home across months and years. Read each one slowly. If one of you "
    "cannot say a particular commitment in good faith yet, do not say it. The goal is "
    "honesty, not performance.",
]

ARCH_COMMITMENTS = [
    (
        "I will not treat your interior as material to be planned around.",
        "{name_vault}, I commit to receiving what you show me as a gift and not as "
        "data. When you give me access to something unfinished &mdash; a fear you have "
        "not resolved, a grief still in process, a question you have not yet answered "
        "&mdash; I will resist the Architect's reflex to immediately assess it and "
        "build around it. I will practice sitting with it. I will ask what you need "
        "from me before I offer a plan. The information you give me is not the "
        "blueprint. It is the person."
    ),
    (
        "I will name my own fear before I ask about yours.",
        "{name_vault}, when the alarm in me fires &mdash; when something feels "
        "incomplete and the Architect wants more information &mdash; I commit to "
        "disclosing what I am actually afraid of before I ask you any questions. "
        "Not <i>what is going on with you</i> but <i>I feel like I am planning "
        "blind and that frightens me.</i> The inquiry that comes after a disclosure "
        "lands differently than the inquiry that comes as an inspection. I want "
        "to give you the former."
    ),
    (
        "I will receive what is unfinished without finishing it for you.",
        "{name_vault}, I commit to not completing your sentences, resolving your "
        "ambivalence, or handing you back a tidy version of the messy thing you "
        "just showed me. The messy middle is part of what I am asking for. I will "
        "learn to hold the unfinished thing with you instead of immediately "
        "building around it. This will cost me something. I am willing to pay it."
    ),
]

VAULT_COMMITMENTS = [
    (
        "I will let you see what is unfinished, in measured portions you can receive.",
        "{name_arch}, I commit to not waiting until everything inside is organized "
        "before I give you access to it. I will practice naming one thing that is "
        "still in process &mdash; one question I have not answered, one grief I "
        "have not resolved &mdash; while it is still in process. Not everything. "
        "Not all at once. A measured portion, given while you can still receive "
        "it as a gift rather than as a file that has been kept from you."
    ),
    (
        "I will tell you when the door is temporarily closed.",
        "{name_arch}, when you ask about my interior at a moment when I am not "
        "ready to share it, I commit to naming that directly rather than presenting "
        "a finished conclusion that is not quite the truth. <i>I am in the middle "
        "of something and I will bring you what I have when I have it.</i> One "
        "sentence. An honest one. You deserve to know that the interior exists, "
        "even when I am not ready to show it &mdash; so that you are not planning "
        "around a closed room without knowing it is closed."
    ),
    (
        "I will bring you wounds while they are still fresh.",
        "{name_arch}, I commit to naming things that hurt me within the same week "
        "they happen, rather than carrying them alone until the file is too large "
        "to hold quietly. Not a deposition. One sentence, brought while the wound "
        "is still small enough to be repaired by a single conversation. I know "
        "what the file costs both of us. I am willing, with God's help, to bring "
        "things to you before they are fully organized &mdash; because you deserve "
        "a spouse who trusts you with what is actually inside."
    ),
]

PRAYER = [
    "Father,",

    "You put us next to each other, and you knew exactly what you were doing. You knew "
    "the Architect would ask for what the Vault has kept inside. You knew the Vault would "
    "protect what the Architect most needs to see. You knew the collision would come, on "
    "ordinary evenings, in the ordinary kitchen, and that neither of us would have the "
    "words for it. You knew all of it before we said yes to each other, and you said yes "
    "to us anyway.",

    "Teach {name_arch} to receive {name_vault}'s interior as a gift and not as a "
    "building material. Teach him that the messy middle she is holding is not a problem "
    "to be planned around but a person to be loved. Quiet the Attorney in him when "
    "{name_vault} finally opens a door &mdash; help him to stand still in the doorway "
    "rather than immediately measuring the room.",

    "Teach {name_vault} that what is inside her is already fully known to you, and that "
    "your verdict is not condemnation but covering. Remind her that the God who has "
    "already seen everything she has ever locked away has not once turned from it. Give "
    "her the courage, in small and measured ways, to show {name_arch} what she has "
    "shown you &mdash; the unfinished thing, the question still in process &mdash; "
    "trusting that he too can receive it without using it against her.",

    "When the Attorney rises in {name_arch}, remind him that you hold the record and "
    "that the verdict has already been spoken in Christ &mdash; he does not need to "
    "establish it through litigation. When the Attorney opens the file in {name_vault}, "
    "remind her that you are her Advocate, that you have already presented the only "
    "brief that finally counts, and that she does not need to carry the file alone.",

    "Make our home a room in which neither of us has to present a finished product "
    "before we are allowed to exist in it. Make our table a place where the unfinished "
    "thing can be named on the same day it happens. Make our marriage one in which the "
    "messy middle of each of us &mdash; unresolved, in process, still being built "
    "&mdash; is the very thing we hold for each other.",

    "In the name of the One who took on himself everything we have tried to keep hidden, "
    "and who calls us, even now, his own.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages that "
    "follow are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, somewhere "
    "quiet, with no children in the room and no phones on the table. There are six "
    "rounds, and they build on each other. Resist the temptation to skip ahead. Start "
    "at Round One even if it feels too light; the lightness is the point. The document "
    "earns the harder rounds by starting with the easier ones.",

    "Some of the questions are playful. Some are direct. A few are the kind that, when "
    "answered honestly, will sit with both of you for a week. None of them are trivia. "
    "All of them are an invitation &mdash; an invitation to be known a little more than "
    "you were before you sat down.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did not read "
    "answers first, in full, without interruption. Then the reader answers the same "
    "question. Then you move on. You do not have to finish all six rounds in one "
    "evening &mdash; two or three rounds, taken seriously and without rushing, is often "
    "better than racing through all of them. Save the rest for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. You may not love "
    "everything you hear. Stay with it anyway. The goal is not to grade each other's "
    "answers. The goal is to be known, and to do the patient work of knowing.",
]

ROUND_1 = [
    (
        "hypothetical",
        "If our marriage were a building, what kind of building would it be, "
        "and which room would you most want to spend the afternoon in?",
        "Let the metaphor work. Don't overthink the architecture."
    ),
    (
        "observation",
        "What is one thing I did this week that you noticed and didn't say anything about?",
        "Not a complaint and not a compliment necessarily. Just something you noticed. "
        "The noticing itself is worth naming."
    ),
    (
        "playful",
        "If you had to describe this marriage as a weather pattern, "
        "what would the forecast be for this season?",
        "Warm front moving in, scattered afternoon storms, chance of sunshine by the weekend. "
        "Be specific. Be honest. Be a little funny if you can."
    ),
]

ROUND_2 = [
    (
        "fill-in-blank",
        "I don't think I tell you this enough &mdash; I am amazed at the way God made you so "
        "_______. Your _______ is something I have come to rely on in ways I did not expect.",
        "Two blanks. Resist the general answer. "
        "'Patient' is too easy. 'Patient with me specifically when I have been immovable about "
        "something that didn't matter' is closer to what this question is asking for."
    ),
    (
        "observation",
        "What is one thing you have watched me do this year that you wish more people got to see?",
        "Most of us only see ourselves in our public moments. "
        "Your spouse has seen the private ones. This question is about those."
    ),
    (
        "one-word",
        "If you had to choose one word to describe what it feels like when I reach for your hand, "
        "what would that word be?",
        "One word, said out loud. Then explain it, briefly, without editing yourself."
    ),
]

ROUND_3 = [
    (
        "forward-looking",
        "Five years from now, when we look back on this season of our marriage, "
        "what do you hope we will say we finally figured out together?",
        "Not what you wish you had done. What you want, when you look back from five years out, "
        "to be able to say you learned."
    ),
    (
        "theological",
        "Where, in the past month, have you seen God specifically at work in me "
        "&mdash; not where you hope he will work, but where you have already seen it?",
        "Name it. Be specific. This is not flattery; it is witness."
    ),
    (
        "shared-identity",
        "Finish this sentence three times: 'We are the kind of couple who _______.' "
        "Give one playful answer, one true answer, and one aspirational one.",
        "The 'we' is the point. Each answer tells you something about how you see "
        "the marriage as a unit."
    ),
]

ROUND_4 = [
    (
        "strength",
        "What is something I carry for this marriage that you would have to learn "
        "to carry alone if I were not here?",
        "Hard to ask. Important to hear. Stay with the answer even if it surprises you."
    ),
    (
        "fill-in-blank",
        "One of the gifts of being married to you is that I get to be _______ "
        "in ways I never would have been on my own.",
        "A version of yourself that only exists because the marriage exists. Name it."
    ),
    (
        "observation",
        "Name one moment in our story where you knew, without any doubt, "
        "that we had built something together that neither of us could have built alone.",
        "Tell the whole story. The remembering is part of the strengthening."
    ),
]

ROUND_5 = [
    (
        "hard",
        "{name_vault}, when {name_arch} asks about your interior and you feel the walls go up "
        "&mdash; what do you wish he knew about what that moment feels like from the inside?",
        "Not a complaint about the asking. An explanation of the experience of being asked. "
        "There is a difference, and it matters."
    ),
    (
        "hard",
        "{name_arch}, when {name_vault} presents you with a finished conclusion and you can "
        "sense the door is closed &mdash; what do you wish she knew about what that feels "
        "like from the inside?",
        "Not a critique of the closing. An honest account of what it costs you. "
        "{name_vault} needs to hear this without defending against it."
    ),
    (
        "profile-aware",
        "What is one thing you have been carrying this past month that you have not brought "
        "to me, and what has kept you from bringing it?",
        "Not an accusation. An invitation. The person asking commits to hearing "
        "the answer without immediately making it something to fix."
    ),
]

ROUND_6 = [
    (
        "blessing",
        "Place your hand on your spouse's hand. Say their name. "
        "Then say: 'You are not a closed file. You are a person I get to keep knowing.' "
        "Say it slowly. Let them say it back.",
        "You may feel awkward. Do it anyway. The awkwardness is part of what makes it work."
    ),
    (
        "prayer",
        "Pray for each other &mdash; out loud, by name, in one or two sentences. "
        "Pray specifically for the thing they told you in Round Five.",
        "This is the close of the date. The prayer is not a formality. "
        "It is the act of handing the evening to the God who was present for all of it."
    ),
]


def _render(text, name_arch, name_vault):
    return text.format(name_arch=name_arch, name_vault=name_vault)


def build(sub_a, sub_b) -> bytes:
    """Generate the Architect+Vault couples walkthrough PDF.

    sub_a: the submission of the Architect spouse
    sub_b: the submission of the Vault spouse
    """
    ensure_fonts()
    S = make_styles()

    name_arch = _first_name(sub_a, "Architect")
    name_vault = _first_name(sub_b, "Vault")

    def R(text):
        return _render(text, name_arch, name_vault)

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Couples Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUPLES WALKTHROUGH",
        cover_right_label=f"{name_arch.upper()}  +  {name_vault.upper()}",
        title=f"Take 139 Couples Walkthrough \u2014 {name_arch} & {name_vault}",
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
    story.append(Paragraph(f"{name_arch} &nbsp;&amp;&nbsp; {name_vault}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_arch.upper()}</b></font><br/>"
                "Architect &middot; Attorney<br/>"
                "<font size=9 color='#6b6862'>Disrespect &middot; Am I protected?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_vault.upper()}</b></font><br/>"
                "Vault &middot; Attorney<br/>"
                "<font size=9 color='#6b6862'>Shame &middot; Am I acceptable?</font>",
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
        "<i>\u201cNo creature is hidden from his sight, but all are naked and exposed\u2014<br/>"
        "and he calls them, even so, his own.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: OPENING ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "The small repeating rocks.",
                   "Why this pairing exists, and why you are both reading it.")
    for p in OPENING:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 2: YOUR TWO SHAPES ──
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
            _profile_card(S, name_vault, ACCENT_HER, "Shame", "Am I acceptable?",
                          "The Vault", "The Attorney"),
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

    # ── SECTION 3: THE ARCHITECT'S GIFT ──
    section_header(story, S, "SECTION THREE  \u00b7  HIS GIFT TO HER",
                   f"What {name_arch} gives {name_vault}.",
                   "Something the Vault has needed but would rarely build for herself.")
    for p in GIFT_TO_VAULT:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4: THE VAULT'S GIFT ──
    section_header(story, S, "SECTION FOUR  \u00b7  HER GIFT TO HIM",
                   f"What {name_vault} gives {name_arch}.",
                   "Something most planners in his life will never provide.")
    for p in GIFT_TO_ARCH:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5: THE COLLISION ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Protection meets the locked room.",
                   "This is not a communication problem. It is an exposure problem.")
    for p in COLLISION[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The loop, in slow motion.",
                   "And the way out, in each spouse's own grammar.")
    for p in COLLISION[5:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6: THE HARDER PICTURE ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When both Attorneys are in the room at once.",
                   "Two very different files, opened at the same time.")
    for p in BOTH_BREAK[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do while you can still see it.",
                   "Three practices, in order.")
    for p in BOTH_BREAK[5:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 7: COMMITMENTS ──
    section_header(story, S, "SECTION SEVEN  \u00b7  COMMITMENTS",
                   "Six small daily practices.",
                   "Three from each of you. Read each one slowly.")
    for p in COMMITMENTS_INTRO:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"FROM {name_arch.upper()}, TO {name_vault.upper()}",
                            S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                             hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for commit_name, body in ARCH_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(commit_name, S["H3"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_vault}, to {name_arch}.",
                   "Three commitments, in her voice, for him to receive.")
    story.append(Paragraph(f"FROM {name_vault.upper()}, TO {name_arch.upper()}",
                            S["CommitLabelHer"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT_HER,
                             hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for commit_name, body in VAULT_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(commit_name, S["H3Her"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())

    # ── SECTION 8: A PRAYER ──
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
                  "Specific praise. The kind that lands because it could only come from you.")
    story.append(PageBreak())
    _render_round(story, 3, rendered_round(ROUND_3),
                  "Wonder together.",
                  "About us, about God, about the life we are making.")
    story.append(PageBreak())
    _render_round(story, 4, rendered_round(ROUND_4),
                  "Sit in the strength.",
                  "Let yourselves feel the actual weight of what you have built.")
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
        "You are not a closed file.<br/>"
        "You are a person I get to keep knowing.",
        closing_style))

    doc.build(story)
    return finalize_buffer(buf)


# ── STANDALONE TEST ───────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    import sys

    # Allow running from the couples-output directory directly
    _here = os.path.dirname(os.path.abspath(__file__))
    _parent = os.path.dirname(_here)
    if _parent not in sys.path:
        sys.path.insert(0, _parent)

    try:
        from walkthrough_writing.base import (
            make_doc, make_styles, finalize_buffer, ensure_fonts,
            section_header,
            PAGE_W, MARGIN_L, MARGIN_R,
            PAPER, INK, ACCENT, ACCENT_HER, MUTED, RULE, HIGHLIGHT_BG,
        )
    except ImportError:
        pass

    class FakeSubA:
        name = "Alex"
        primary_mechanism = "ARCH"
        primary_breakdown = "ATTY"
        primary_trigger = "DIS"
        core_question = "PROT"

    class FakeSubB:
        name = "Morgan"
        primary_mechanism = "VAULT"
        primary_breakdown = "ATTY"
        primary_trigger = "SHM"
        core_question = "ACC"

    pdf_bytes = build(FakeSubA(), FakeSubB())
    out_path = os.path.join(_here, "architect_vault_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    import io
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        snippet = ""
        # Find section three content
        for page in reader.pages:
            txt = page.extract_text() or ""
            if "SECTION THREE" in txt and "HIS GIFT" in txt:
                snippet = txt.strip()[:200]
                break
        if not snippet:
            for page in reader.pages[4:6]:
                txt = page.extract_text() or ""
                if txt.strip():
                    snippet = txt.strip()[:200]
                    break
    except Exception as e:
        page_count = "unknown"
        snippet = f"(pypdf error: {e})"

    print(f"DONE: architect_vault.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
