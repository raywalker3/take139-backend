"""Couples Walkthrough — Island + Island.

Voice: Tim Keller (from The Meaning of Marriage + Walking with God through
Pain and Suffering). Pastoral, theologically rich, warmly direct.
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where both spouses are Islands.
First names are substituted from the submissions at render time:
    {name_a}  -> the first Island spouse's first name (alphabetical)
    {name_b}  -> the second Island spouse's first name (alphabetical)

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
    + "ones &mdash; the same disappointment in slightly different clothes, week after "
    + "week, year after year, until both people have forgotten what they were originally "
    + "hoping for. But for you, the small repeating rock is different from almost any "
    + "other couple&rsquo;s. Yours is not a rock that makes noise.",

    "From the outside, you are one of the most peaceable marriages in any room. Neither "
    + "of you floods. Neither of you prosecutes publicly. Neither of you demands constant "
    + "presence from the other. People look at your marriage and see two self-possessed "
    + "people who have figured out how to give each other room. And they are not wrong "
    + "&mdash; you have. The question is whether <i>room</i> has, over time, quietly "
    + "become <i>distance</i>. The question is whether two people who grant each other "
    + "generous space have gradually stopped crossing it.",

    "What follows is a counselor&rsquo;s read of the small repeating rocks in your "
    + "particular marriage. Your pairing is <b>two Islands</b> &mdash; and the pastoral "
    + "challenge of two Islands in one marriage is unlike any other. Two Islands do not "
    + "collide dramatically. They drift. They process in parallel. They protect the same "
    + "thing in the same way, each from their own shore, and the water between them can "
    + "look remarkably calm on the surface while both of them are quietly wondering whether "
    + "the other one has been thinking of them.",

    "Here is what I want to do for you. I will name what each of you brings the other "
    + "that the other could not have built alone &mdash; because there is a genuine gift "
    + "in this pairing, and it deserves to be named before anything else. Then I will "
    + "name the collision your shared mechanism creates, which is less a collision than "
    + "a slow-motion divergence &mdash; the marriage that never fights because nothing "
    + "has ever been put on the table to fight about. Then I will name the harder picture "
    + "&mdash; what happens when two Islands break at the same time. Then I will hand "
    + "each of you commitments, not as rules, but as small daily practices that, over "
    + "years, close the water between two coves on the same coastline.",

    "Read it together, if you can. If not, read it separately and then sit down with "
    + "it. Argue with what does not fit. Stay with what does. The goal is not a marriage "
    + "that performs closeness. The goal is a marriage where the closeness is real &mdash; "
    + "where {name_a} and {name_b} are not two Islands who happen to share a home, "
    + "but one flesh who have learned, slowly, to let the water between them recede.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on "
    + "paper, side by side. Most couples never see their two profiles next to each other. "
    + "You are about to &mdash; and for you, the first thing you will notice is how "
    + "much they resemble each other.",
]

TWO_SHAPES_BODY = [
    "{name_a}, you are an <b>Island</b> whose body reads disconnection or insignificance "
    + "as an alarm, and whose deepest question is <i>Am I enough to be remembered?</i> "
    + "You have learned, over years, to process alone &mdash; to reach conclusions before "
    + "you open them for discussion, to carry the interior weight without showing it, to "
    + "need less than most people in ways that protect you from a very specific "
    + "disappointment: the disappointment of having needed someone who was not there.",

    "{name_b}, you are an <b>Island</b> whose body reads the same alarm: disconnection, "
    + "insignificance, the creeping question of whether your passage through someone&rsquo;s "
    + "life has left a mark. You, too, have built the Island&rsquo;s characteristic "
    + "self-sufficiency &mdash; the composed exterior, the interior life that runs deep "
    + "and largely unseen, the instinct to handle your deepest things alone rather than "
    + "risk them being mishandled.",

    "Take a moment to absorb what this means. You are asking the same question. You "
    + "are running the same mechanism. You are, in many seasons, protecting the same "
    + "wound. This is the shared grammar that makes your marriage feel, at its best, "
    + "unusually spacious &mdash; two people who understand each other&rsquo;s need for "
    + "solitude without explanation, who do not take each other&rsquo;s quiet personally, "
    + "who have built a home that breathes.",

    "But here is what the shared grammar does not automatically produce: <i>crossing "
    + "the water.</i> The Island&rsquo;s strategy &mdash; if I need very little from the "
    + "outside world, I cannot be disappointed by what it fails to give me &mdash; "
    + "was built for a world of one. It was not built for a marriage. In a marriage, "
    + "the strategy means that both of you are, in your own way, managing your deepest "
    + "material alone. Both of you are processing in private. Both of you have decided, "
    + "at some level below conscious thought, that the most important things stay inside "
    + "where they are safer. And the result is two people living near each other, peacefully, "
    + "in parallel &mdash; two coves on the same coastline that the water between them "
    + "never actually connects.",

    "This is the singular gift and the singular challenge of your marriage. The gift "
    + "is that you have built a home without the ordinary friction of incompatible "
    + "mechanisms &mdash; neither of you overwhelms the other, neither demands more "
    + "than the other can give. The challenge is that the Island&rsquo;s deepest longing "
    + "&mdash; to be known, to be remembered, to matter in a way that is specific and "
    + "permanent &mdash; requires exactly the kind of crossing that both of you have "
    + "learned, for very good reasons, not to do.",
]

GIFT_TO_A = [
    "{name_b} gives {name_a} something almost no one else in the marriage is in a "
    + "position to give: <b>a room that does not require explanation.</b>",

    "The Island has spent much of its life translating. Explaining why it needs to "
    + "think before it speaks, why it does not want to process out loud, why going "
    + "quiet is not an indictment of anyone, why solitude is not withdrawal but "
    + "something more like breathing. These translations take energy. They require "
    + "the Island to become legible to a world that runs on extroversion and processing-in-"
    + "community, and the legibility costs something.",

    "{name_b}, by virtue of being an Island, is the one room in {name_a}&rsquo;s "
    + "life that does not require this translation. He knows what the quiet is. He "
    + "does not read it as rejection. He does not read the interior life as withholding. "
    + "He understands, from the inside, what it means to need to process alone before "
    + "you can open something, and he does not pathologize it. For {name_a}, this is "
    + "one of the rarest gifts in any relationship: being with someone who does not "
    + "require you to explain yourself.",

    "Tim Keller, writing in <i>The Meaning of Marriage</i>, observed that one of "
    + "the deepest gifts of a good marriage is to be known &mdash; not catalogued, "
    + "but known the way a person who has lived beside you for years knows you, without "
    + "needing a translation. {name_b} knows {name_a}&rsquo;s mechanism from the inside. "
    + "He does not flinch at the composure. He does not push when the door is closed. "
    + "He is, in this particular way, the best reader {name_a} has.",

    "{name_a} &mdash; if you want to thank {name_b} for something this week, thank "
    + "him for this: for the gift of a marriage where you do not have to perform "
    + "extroversion to be loved. Most of the world requires this of you at some level. "
    + "He does not. That is not a small thing. It is one of the quiet graces you have "
    + "been given.",

    "{name_b} &mdash; what you are giving {name_a}, simply by being who you are, "
    + "is a marriage where the Island&rsquo;s natural rhythm is honored rather than "
    + "corrected. You have probably not thought of this as a gift. You were simply "
    + "being yourself. Name it as a gift anyway. It is.",
]

GIFT_TO_B = [
    "{name_a} gives {name_b} something almost no one else in the marriage is in a "
    + "position to give: <b>a witness who does not require performance.</b>",

    "Most of the people in {name_b}&rsquo;s life encounter the composed exterior and "
    + "respond accordingly. They take the quiet at face value. They respect the "
    + "self-sufficiency. They do not look for what is underneath, because the Island "
    + "is very good at making it unnecessary to look. {name_a} is different, not because "
    + "she pushes harder than others, but because she has the same mechanism and "
    + "therefore the same knowledge: she knows what the Island is protecting, because "
    + "she is protecting the same thing.",

    "This means that when {name_b} is carrying something &mdash; when the significance "
    + "tally is running, when the old question is awake, when something has registered "
    + "in the interior that he has not yet named &mdash; {name_a} is the one person "
    + "in his life most likely to notice without being told. Not to interrogate, not "
    + "to demand disclosure, but simply to notice. For the Island, being noticed "
    + "without having to announce itself is one of the most quietly profound "
    + "experiences available. It is, in miniature, the answer to the question "
    + "underneath the trigger: <i>Am I enough to be remembered?</i>",

    "The theological word for what {name_a} gives {name_b} is <i>witness.</i> "
    + "Not testimony in the legal sense, but the older, weightier sense: the "
    + "presence of a person who has seen you, who carries the seeing in her mind "
    + "between moments, who does not need you to perform significance in order to "
    + "grant it. Proverbs 17:17 says: <i>A friend loves at all times, and a brother "
    + "is born for a time of adversity.</i> {name_a}&rsquo;s Island mechanism makes "
    + "her, paradoxically, a better witness to {name_b}&rsquo;s interior than almost "
    + "anyone else &mdash; because she is not looking for what is easy to see.",

    "{name_b} &mdash; if you want to thank {name_a} for something this week, thank "
    + "her for the times she has noticed something in you without your having to announce "
    + "it. For the Island, this is one of the rarest forms of being loved. She has done "
    + "it more than you have probably acknowledged. Name one instance. Say it to her "
    + "specifically. She will not know what to do with the gratitude. That is fine. "
    + "Say it anyway.",

    "{name_a} &mdash; what you are giving {name_b}, when you notice his interior "
    + "without requiring a performance, is the closest thing to gospel-shaped love "
    + "that one Island can offer another. You are, in small and daily ways, giving "
    + "him the answer to the question his trigger keeps reopening. Do not underestimate "
    + "the weight of this.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you, "
    + "even if you have never named it &mdash; because it does not look like a "
    + "collision at all. That is what makes it the hardest collision in any pairing "
    + "to see.",

    "Most couples collide. Two incompatible mechanisms rub against each other and "
    + "produce heat. The Architect and the Ambassador argue about plans versus feelings. "
    + "The Vault and the Flood argue about disclosure. The friction is visible, and "
    + "while visible friction is painful, it is at least present. The two of you do "
    + "not collide this way. Your collision is the slow-motion absence of collision "
    + "&mdash; the marriage that does not fight because nothing has ever been fully "
    + "put on the table to fight about.",

    "Ecclesiastes 4:9&ndash;12 says: <i>Two are better than one, because they have "
    + "a good reward for their toil. For if they fall, one will lift up his fellow. "
    + "But woe to him who is alone when he falls and has not another to lift him up. "
    + "Again, if two lie together, they keep warm, but how can one keep warm alone? "
    + "And though a man might prevail against one who is alone, two will withstand "
    + "him &mdash; a threefold cord is not quickly broken.</i> This passage praises "
    + "two-ness. The Island couple has, paradoxically, arranged a marriage of two "
    + "people in which each remains, in the most essential sense, one &mdash; two "
    + "ones, each self-sufficient, each processing alone, each deciding not to ask. "
    + "The threefold cord is hard to braid when both hands are busy managing their "
    + "own end of the rope.",

    "Genesis 2:18 is the foundational marriage text: <i>It is not good that the man "
    + "should be alone.</i> God did not say this about Adam before Eve. He said it "
    + "after a full assessment of what Adam had &mdash; work, purpose, the presence "
    + "of God himself in the garden. And still: it is not good to be alone. The Island "
    + "couple has, with the best intentions and the most peaceful of motives, structured "
    + "a marriage in which each remains, in the interior, alone. Not estranged. Not "
    + "hostile. Simply alone. Processing alone. Asking alone. Keeping the tally alone. "
    + "And the God who said <i>it is not good</i> was speaking into exactly this.",

    "Here is the pattern, in slow motion. {name_a} is processing something difficult "
    + "&mdash; a weight, an unasked question, a longing she has not found language for. "
    + "The Island&rsquo;s instinct is to handle it privately, to wait until the "
    + "processing is complete before she opens it. {name_b} is processing something "
    + "of his own, in his own interior, on his own timeline. Neither of them is "
    + "withholding maliciously. Both of them are doing exactly what the Island was "
    + "designed to do. But the result is two people in the same home, in the same "
    + "evening, each carrying something the other could have helped with &mdash; "
    + "and neither of them will know it, because neither of them said anything.",

    "The day ends. The weight was managed. The tally was kept privately. No argument "
    + "occurred. From the outside, the marriage looks fine. From the inside, "
    + "{name_a} is not sure {name_b} thought of her today, and she will not ask. "
    + "{name_b} is not sure {name_a} needs him for anything, and he will not push. "
    + "Both of them, in their own way, are keeping a count they were not designed to "
    + "keep, asking a question they were not designed to answer alone: "
    + "<i>Am I enough to be remembered?</i>",

    "The way out is not for either of you to become a different mechanism. Islands "
    + "should not be turned into Ambassadors; the self-containment has genuine gifts, "
    + "and forcing it out produces only performance. The way out is something more "
    + "specific and considerably harder for both of you: <b>naming one thing, before "
    + "the processing is complete.</b> Not the finished conclusion &mdash; the Island "
    + "can live with handing over finished conclusions. The unfinished thing. The weight "
    + "that does not yet have language. The question that is still forming.",

    "{name_a}, when you are carrying something, the right move &mdash; not always, "
    + "but once &mdash; is to say one sentence to {name_b} before the processing is "
    + "done: <i>I am carrying something I don&rsquo;t have words for yet. I wanted "
    + "you to know it is there.</i> That sentence is not disclosure; it is an open "
    + "door. The Island can give one sentence without feeling exposed. And one "
    + "sentence, offered before the processing is complete, changes everything "
    + "that follows &mdash; because now {name_b} knows to come looking, and "
    + "the finding changes the answer to the question underneath the trigger.",

    "{name_b}, when {name_a} goes quiet, the translation is almost never "
    + "<i>she is fine.</i> Nine times out of ten, the translation is <i>she is "
    + "processing something she does not yet know how to say.</i> The right move "
    + "is not to push. It is to offer, gently, one specific gesture: "
    + "<i>I noticed something is there. You do not have to say it. But I am here "
    + "when you are ready.</i> For the Island, being noticed without having to "
    + "announce it is one of the deepest forms of being loved. That sentence is "
    + "the gesture that does the most.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be seasons &mdash; not often, but they "
    + "will come &mdash; when both of you are in breakdown at the same time. And "
    + "here is what makes the two-Island breakdown different from almost any other "
    + "couple&rsquo;s: it does not escalate loudly. It goes silent. Both of you, "
    + "separately, begin to assemble what the Island does when it is wounded.",

    "The most common pattern is what we call <b>parallel Quiet Exits.</b> "
    + "Two people drafting separate internal verdicts without ever putting them in "
    + "the room. Each Island, in breakdown mode, does what it was built to do: "
    + "it takes the wound inside, closes the door, and begins to process. The case "
    + "builds in private. The tally grows. Neither of them says so. Both of them, "
    + "at the same time, in the same home, are running a courtroom in which the "
    + "other person appears only as defendant &mdash; a courtroom in which the "
    + "defendant does not know the trial is happening.",

    "Hosea 6:4 speaks a word that fits this pattern with uncomfortable precision: "
    + "<i>Your love is like the morning mist &mdash; it disappears as quickly as "
    + "the dew.</i> The Island couple&rsquo;s danger is not hatred. It is evaporation. "
    + "The love was real; it does not end in a scene but in a slow thinning, a "
    + "gradual withdrawal of interior investment, until both people have arranged "
    + "a life together that runs quietly and asks nothing of either of them. They "
    + "are not separated. They have simply, quietly, stopped crossing the water. "
    + "And neither of them said so, because Islands do not say so.",

    "Paul writes in 1 Corinthians 13:7 that love <i>hopes all things</i>. The "
    + "parallel Quiet Exit is what happens when hope has quietly been replaced by "
    + "a private verdict &mdash; when each Island has concluded, inside, that the "
    + "other one will not cross, will not come looking, will not remember. The "
    + "verdict has not been delivered. It has not been contested. It has simply "
    + "been filed, in the interior, and the Island is living alongside it as "
    + "though it were settled fact.",

    "Dietrich Bonhoeffer wrote in <i>Life Together</i>: <i>Let him who cannot "
    + "be alone beware of community. Let him who is not in community beware of "
    + "being alone.</i> He meant these as warnings in opposite directions: the "
    + "person who cannot tolerate solitude will corrupt community by using it "
    + "as escape. The person who will not enter community will use solitude "
    + "as a way of avoiding what only community can give. The Island couple "
    + "has, in the breakdown, chosen the second warning. Both of them are "
    + "alone &mdash; not by circumstance but by the accumulated decisions of "
    + "two mechanisms that were never designed to operate without the "
    + "interruption of another person.",

    "What to do when you can still see what is happening:",

    "<b>One of you names it out loud.</b> This is the hardest thing in a "
    + "two-Island breakdown, because the Island does not name things until "
    + "the processing is complete. This is the one exception. One of you "
    + "&mdash; whichever one notices first &mdash; says: <i>I think we "
    + "have both been processing separately for a while. I don&rsquo;t "
    + "think either of us has put anything in the room. I want to put "
    + "one thing in the room.</i> Not the verdict. Not the assembled "
    + "case. One thing &mdash; the smallest, earliest, most specific "
    + "weight that started the drift. Name it in one sentence.",

    "<b>Do not wait for the other to go first.</b> The Island&rsquo;s "
    + "instinct, in a two-Island breakdown, is to wait. Each of you, "
    + "at some level, is running the Island&rsquo;s oldest test: "
    + "<i>if they care, they will come. If they come, I was worth "
    + "finding.</i> Both of you are running this test at the same time. "
    + "It will not produce a result. One of you must decide that the "
    + "love of Christ &mdash; who came seeking, who did not wait to be "
    + "petitioned &mdash; is a better model for this moment than the "
    + "Island&rsquo;s strategy. One of you goes first. The other receives. "
    + "Then the other goes.",

    "<b>When you come back to each other, lead with the specific, not "
    + "the accumulated.</b> The Island&rsquo;s breakdown tendency is "
    + "to carry weight in silence until the full brief is ready. By "
    + "the time two Islands speak, the case has been running for a "
    + "long time. The discipline is to skip the brief and speak only "
    + "the original wound &mdash; the one moment, the one sentence, "
    + "the earliest specific thing. <i>I felt unseen at dinner on "
    + "Tuesday.</i> Not the pattern. Not the accumulated evidence. "
    + "The one thing. Then stop. Let your spouse respond to the one "
    + "thing before adding the next.",

    "<b>Neither of you is the problem.</b> The Quiet Exit is not the "
    + "truest thing about either of you. It is an old mechanism doing "
    + "what it was built to do &mdash; protecting a wound that was real, "
    + "in a season that required protection. The truest thing about both "
    + "of you is that you chose each other, that you are still here, and "
    + "that two Islands who learn, slowly, to cross the water are building "
    + "something that the original Island strategy could never have built: "
    + "a home where the interior is shared, and the sharing does not "
    + "require performance.",
]

COMMITMENTS_INTRO = [
    "What follows are eight commitments &mdash; four from {name_a}, four from {name_b}. "
    + "They are not vows in the legal sense. They are the small daily practices that, "
    + "offered to each other freely, close the water between two coves over months and "
    + "years. For the two-Island marriage, the key pastoral direction is the same for "
    + "both of you: <i>lead with disclosure, not solitude.</i> Before you finish "
    + "processing, name one thing that is still forming. Before you carry the weight "
    + "all the way alone, give it a sentence. This is the discipline that makes two "
    + "Islands into one household. Read each commitment slowly. If one of you cannot "
    + "say a particular commitment in good faith yet, do not say it. The goal is not "
    + "performance. It is honesty.",
]

A_COMMITMENTS = [
    ("To tell you one thing before I finish processing.",
     "{name_b}, I commit to naming one thing I am carrying before the processing is "
     + "complete. Not the conclusion &mdash; the Island can live with handing over "
     + "conclusions. The unfinished weight. The question that does not yet have language. "
     + "I will say: <i>I am carrying something I don&rsquo;t have words for yet. I "
     + "wanted you to know it is there.</i> I will practice this once a week, and "
     + "I will not wait until it is safe to say."),

    ("To receive your noticing.",
     "{name_b}, when you notice something in me without my having to announce it, "
     + "I commit to receiving it rather than deflecting it. The Island&rsquo;s instinct "
     + "is to say <i>I&rsquo;m fine</i> &mdash; to close the door before it can be "
     + "opened further. I will try, when you come looking, to leave the door ajar "
     + "rather than pressing it shut. Your coming is the answer to the question I "
     + "carry. I will practice receiving it as such."),

    ("To say one thing I am grateful for, specifically.",
     "{name_b}, I commit to telling you one specific thing I noticed about you "
     + "this week that I did not mention. Islands are good at noticing and poor "
     + "at naming what they noticed. The noticing, unspoken, does not reach you. "
     + "I will name one thing &mdash; not a general gratitude, but a specific moment, "
     + "a specific act, the kind of thing only I would have seen. Once a week. "
     + "I will practice the naming."),

    ("To cross the water before it widens.",
     "{name_b}, when I feel the drift beginning &mdash; when I notice that we have "
     + "both been processing separately for longer than is good for us &mdash; I "
     + "commit to naming it before the silence becomes a verdict. I will say: "
     + "<i>I think we have both been on our own islands for a few days. I want "
     + "to cross. Can we put one thing each in the room?</i> That sentence is "
     + "harder than it sounds. I will practice it anyway."),
]

B_COMMITMENTS = [
    ("To tell you one thing before I finish processing.",
     "{name_a}, I commit to naming one thing I am carrying before the processing "
     + "is complete. The Island in me will resist this &mdash; it will tell me that "
     + "what I am holding is not ready, not finished, not legible enough to share. "
     + "I will share it anyway, in one sentence, before the door closes: "
     + "<i>something is there, and I want you to know it is there.</i> This is "
     + "the discipline that two Islands need from each other most."),

    ("To come looking.",
     "{name_a}, when I notice that you have gone quiet in a way that feels like "
     + "more than preference &mdash; when something in me says the Island has "
     + "closed rather than simply rested &mdash; I commit to coming. Not with "
     + "a demand. With one sentence: <i>I noticed something is there. You do not "
     + "have to say it yet. But I am here when you are ready.</i> For the Island, "
     + "being found without having to announce it is the nearest thing to the "
     + "answer to the question we both carry. I will practice coming."),

    ("To say one thing I am grateful for, specifically.",
     "{name_a}, I commit to telling you one specific thing I noticed about you "
     + "this week that I did not mention. You are probably carrying more than "
     + "you show. I notice more than I say. The gap between my noticing and my "
     + "naming is where your significance question lives. I will close that gap "
     + "once a week, with one specific thing, said out loud. You deserve to know "
     + "what I see."),

    ("To cross the water before it widens.",
     "{name_a}, when I feel the drift &mdash; when I notice that both of us have "
     + "been alone on our own islands longer than is good for us &mdash; I commit "
     + "to naming it before the silence becomes a verdict. One sentence: "
     + "<i>I think we have both been processing alone for too long. I want to "
     + "put something in the room. Can we?</i> The Island who goes first is "
     + "the Island who loves. I will practice going first."),
]

PRAYER = [
    "Father,",

    "You set these two Islands next to each other, and you knew exactly what you "
    + "were doing. You knew two people who process alone would understand each other "
    + "in ways that most spouses cannot. You also knew that two Islands in one "
    + "marriage produce two people who are quietly, separately, carrying things "
    + "the other could have helped with &mdash; and that neither of them will say so. "
    + "You knew all of it before either of them said yes.",

    "Teach them the crossing that their mechanism resists. Teach {name_a} to open "
    + "the door before the processing is complete &mdash; to give {name_b} the "
    + "unfinished weight, the sentence without a conclusion, the admission that "
    + "something is there before she knows what to do with it. Teach {name_b} "
    + "to come looking &mdash; to notice what {name_a} is carrying and to "
    + "come gently, without requiring an announcement, without making the "
    + "noticing cost her anything.",

    "When the Quiet Exit is assembling &mdash; two Islands drifting in parallel, "
    + "two separate verdicts forming in two separate silences &mdash; wake one of "
    + "them first. Give them the courage to say the hard sentence before the "
    + "verdict becomes a destination: <i>I think we have both been on our own "
    + "islands too long. I want to cross.</i> Remind them of Ecclesiastes: "
    + "<i>woe to him who is alone when he falls.</i> Do not let them fall "
    + "alone in the same home.",

    "And Father, where they ask <i>Am I enough to be remembered?</i> &mdash; "
    + "where the old question surfaces in the interior, as it will, as it always "
    + "has &mdash; remind them that the answer was given before the question was "
    + "formed. <i>Behold, I have engraved you on the palms of my hands.</i> "
    + "They are not forgotten. They are not unremarkable. They are inscribed, "
    + "carried, kept &mdash; by the One whose memory is perfect and whose love "
    + "does not depend on their being easy to remember. Let that truth be the "
    + "ground under the marriage, the thing that makes crossing possible "
    + "because neither of them has anything left to prove.",

    "Make their home a room where two people who both know how to be alone have "
    + "learned something harder: how to be together &mdash; not performing "
    + "closeness, but crossing the water, one sentence at a time, into the "
    + "genuine and unhurried presence of each other.",

    "In the name of the One who left the ninety-nine to come looking &mdash; "
    + "who did not wait to be petitioned, who crossed the distance first &mdash; "
    + "and who is, even now, preparing a home in which they will live with him "
    + "forever.",

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
    + "them are trivia. All of them are an invitation. For two Islands in particular: "
    + "resist the temptation to give the fully processed answer. The point of these "
    + "questions is not your conclusions. It is what you are still figuring out. "
    + "The unfinished answer is often the more honest one.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did not "
    + "read answers first, in full, without interruption. Then the reader answers the "
    + "same question. Then you move on. You do not have to finish all six rounds in "
    + "one night &mdash; in fact, two or three rounds, taken seriously, is often "
    + "better than racing through all of them. Save the rest for the next date.",

    "<b>One rule.</b> The other person&rsquo;s answer is never wrong. You may not "
    + "love everything you hear. Stay with it. The point of this is not to grade "
    + "each other&rsquo;s answers. The point is to be known, and to do the work "
    + "of knowing.",
]

ROUND_1 = [
    ("hypothetical",
     "If our marriage were a landscape, what kind of landscape would it be &mdash; "
     + "and what is the weather like today?",
     "Two Islands. Be specific. The weather in particular will tell you something "
     + "neither of you expected."),
    ("observation",
     "What is something I did this week that you noticed and did not mention?",
     "Not a complaint. A small noticing. The fact that you noticed at all is the gift. "
     + "The naming of it is the crossing."),
    ("playful",
     "If you had to describe each of us as a specific kind of island &mdash; a Pacific "
     + "atoll, a rocky Scottish isle, a Venetian lagoon island, something else entirely "
     + "&mdash; what would you pick, and why?",
     "Yes, really. Let the metaphor do something. The answer will be more accurate "
     + "than you expect."),
]

ROUND_2 = [
    ("fill-in-blank",
     "I don&rsquo;t think I tell you this enough &mdash; I am amazed at the way "
     + "God made you so _______. Your _______ is something I notice and rarely "
     + "name, and I want to get better at naming it.",
     "Two blanks. The second one is what you have been taking for granted. Be specific "
     + "enough that only you could have said it."),
    ("observation",
     "Name one thing you have watched me carry alone this year that I probably "
     + "did not tell you about &mdash; and that you knew was there anyway.",
     "Two Islands. You have both been noticing more than you say. This is the "
     + "question that gives the noticing a voice."),
    ("one-word",
     "If you had to choose one word to describe how it feels when I actually cross "
     + "the water &mdash; when I tell you something unfinished, something I do not "
     + "have language for yet &mdash; what word would it be?",
     "One word, said out loud. Then explain it. The Island&rsquo;s answer to this "
     + "question is usually not what the Island expects."),
]

ROUND_3 = [
    ("forward-looking",
     "Five years from now, when we look back on this season of our marriage, what "
     + "do you hope we will say we finally learned to give each other?",
     "Not what you wish you had done. What you want, when you look back, to be "
     + "able to say you actually practiced."),
    ("theological",
     "Where, in the last month, have you seen God specifically at work in me &mdash; "
     + "not in our circumstances, but in me, in the person I am becoming?",
     "Not where you want him to work. Where you have already seen it. Name it "
     + "with the specificity that only a witness carries."),
    ("shared-identity",
     "Finish this sentence three times: &ldquo;We are the kind of couple who _______." 
     + "&rdquo; Give one playful answer, one true answer, and one aspirational answer.",
     "The &ldquo;we&rdquo; is the point. The aspirational one is what you are "
     + "crossing the water toward."),
]

ROUND_4 = [
    ("strength",
     "What is something I carry for the two of us that you would have to learn to "
     + "carry for yourself if I were not here?",
     "Two Islands often under-acknowledge each other&rsquo;s contributions because "
     + "both assume the other one knows. Stay with the answer. Say it in full."),
    ("fill-in-blank",
     "One of the gifts of being married to you is that I get to be _______ in ways "
     + "I never would have been alone &mdash; and the interior life I have built "
     + "with you is deeper than any interior life I would have built without your "
     + "_______.",
     "A version of yourself, and a quality of the marriage, that only exist because "
     + "the marriage exists. Name both specifically."),
    ("observation",
     "Name one moment in our story so far where you knew, with no doubt, that we "
     + "had crossed the water &mdash; that we had built something together that "
     + "neither of us could have built on our own shore.",
     "Tell the story in full. The remembering is part of the strengthening."),
]

ROUND_5 = [
    ("hard",
     "When was the last time you felt like I was not thinking about you &mdash; "
     + "not in an argument, just in the ordinary days &mdash; and what would have "
     + "made it different?",
     "One moment. Named carefully. Heard without defending. This is the question "
     + "that goes to the center of what both Islands carry."),
    ("profile-aware",
     "When you go quiet and I do not come looking, what is it that you are hoping "
     + "I will do &mdash; and what has kept you from asking for it directly?",
     "You both know the mechanism now. This question names the gap between what "
     + "the Island hopes for and what it asks for. Both halves matter."),
    ("theological",
     "What is one thing you have been carrying lately &mdash; a fear, a longing, "
     + "a question about us &mdash; that you have not yet brought to me, and what "
     + "has kept you from bringing it?",
     "Not an accusation. An invitation. Hear the answer without defending, and "
     + "without immediately offering a solution."),
]

ROUND_6 = [
    ("blessing",
     "Place your hand on your spouse&rsquo;s hand. Say their name. Then say: "
     + "&lsquo;You are not someone I have figured out. You are someone I want "
     + "to keep crossing toward. I do not want to process this life alone.&rsquo; "
     + "Say it slowly. Let them say it back.",
     "You may feel the Island in you resist the directness of this. That resistance "
     + "is the point. Do it anyway. The crossing begins here."),
    ("prayer",
     "Pray for each other &mdash; not silently, not generally, but out loud and "
     + "by name. One sentence is enough. Pray for the thing they just told you "
     + "in Round Five.",
     "The closing of the date. Do not skip. Two Islands who pray for each other "
     + "by name have done something the mechanism alone cannot do: they have "
     + "crossed the water together, and the crossing is its own answer."),
]


def _render(text, name_a, name_b):
    return text.format(name_a=name_a, name_b=name_b)


def build(sub_a, sub_b) -> bytes:
    """Generate the Island+Island couples walkthrough PDF.

    sub_a: the submission of one Island spouse
    sub_b: the submission of the other Island spouse

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
        "A counselor\u2019s read of two islands<br/>and the water between them.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("PREPARED FOR", S["CoverProfileLabel"]))
    story.append(Paragraph(f"{name_a} &nbsp;&amp;&nbsp; {name_b}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_a.upper()}</b></font><br/>"
                "Island &middot; Quiet Exit<br/>"
                f"<font size=9 color='#6b6862'>Disconnection &middot; Am I enough to be remembered?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_b.upper()}</b></font><br/>"
                "Island &middot; Quiet Exit<br/>"
                f"<font size=9 color='#6b6862'>Disconnection &middot; Am I enough to be remembered?</font>",
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
        "<i>\u201cIt is not good that the man should be alone.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "Genesis 2:18",
        ParagraphStyle("cqa", fontName="Inter", fontSize=9, leading=14,
                       textColor=MUTED, alignment=TA_CENTER)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: OPENING ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "Two coves on the same coastline.",
                   "Why this pairing exists, and what you are both about to read.")
    for p in OPENING:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 2: YOUR TWO SHAPES ──
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TWO SHAPES",
                   "Side by side, on paper.",
                   "Two profiles that look alike \u2014 and the single crossing that matters most.")
    for p in TWO_SHAPES_INTRO:
        story.append(Paragraph(R(p), S["BodyJ"]))
    side_by_side = Table(
        [[
            _profile_card(S, name_a, ACCENT,
                          "Disconnection / Significance", "Am I enough to be remembered?",
                          "The Island", "The Quiet Exit"),
            "",
            _profile_card(S, name_b, ACCENT_HER,
                          "Disconnection / Significance", "Am I enough to be remembered?",
                          "The Island", "The Quiet Exit"),
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
                   "A room that does not require explanation.")
    for p in GIFT_TO_A:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4: GIFT B TO A ──
    section_header(story, S, f"SECTION FOUR  \u00b7  {name_b.upper()}\u2019S GIFT TO {name_a.upper()}",
                   f"What {name_b} gives {name_a}.",
                   "A witness who does not require performance.")
    for p in GIFT_TO_B:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5: THE COLLISION ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "The slow-motion absence of collision.",
                   "The small repeating rock that makes no sound.")
    for p in COLLISION[:4]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The drift, in slow motion.",
                   "And the way out, for each of you in your own grammar.")
    for p in COLLISION[4:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6: THE HARDER PICTURE ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When both Islands go silent at once.",
                   "The parallel Quiet Exit, and what to do while you can still see it.")
    for p in BOTH_BREAK[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do, while you can still see it.",
                   "Four practices for the drift, in order.")
    for p in BOTH_BREAK[5:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 7: COMMITMENTS ──
    section_header(story, S, "SECTION SEVEN  \u00b7  COMMITMENTS",
                   "Eight small daily practices.",
                   "Four from each of you. Lead with disclosure, not solitude.")
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
        "You are not someone I have figured out.<br/>"
        "You are someone I want to keep crossing toward.<br/>"
        "I do not want to process this life alone.",
        closing_style))

    doc.build(story)
    return finalize_buffer(buf)


# ── STANDALONE TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "ISLE"
        primary_breakdown = "GHOST"
        primary_trigger = "DISC"
        core_question = "REM"
        name = "Test User"

    class FakeSubB:
        primary_mechanism = "ISLE"
        primary_breakdown = "ATTY"
        primary_trigger = "SIG"
        core_question = "REM"
        name = "Another User"

    pdf_bytes = build(FakeSub(), FakeSubB())
    out_path = os.path.join(os.path.dirname(__file__), "island_island_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages
    page_count = pdf_bytes.count(b"%%Page:")

    # Section Three snippet
    snippet = GIFT_TO_A[0][:200]

    print(f"DONE: island_island.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Output:   {out_path}")
    print(f"Pages (approx): {page_count}")
    print(f"Section Three snippet: {snippet}")
