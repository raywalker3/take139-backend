"""Couples Walkthrough — Vault + Vault.

Voice: Tim Keller (from The Meaning of Marriage + Walking with God through
Pain and Suffering). Pastoral, theologically rich, warmly direct.
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where both spouses are Vaults.
First names are substituted from the submissions at render time:
    {name_a}  -> the first Vault spouse's first name (alphabetical)
    {name_b}  -> the second Vault spouse's first name (alphabetical)

For same-mechanism pairs the order does not carry directional meaning.
The build() function sorts alphabetically so name_a <= name_b.

Pastoral key: The most guarded same-mechanism pairing. Both spouses have
organized their lives around the protection of interior life. Both
deliberately curate what is shown. The distance is not temperamental
(like Island+Island) but strategic — each respects the other's locks
because they understand the locks from inside. The unique pastoral
challenge: the unspoken contract of mutual non-intrusion makes the
marriage feel safe while slowly making it unreal.
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
    + "ones &mdash; the same distance in slightly different clothes, season after season, "
    + "year after year, until both people have quietly forgotten what it felt like to be "
    + "fully known. But your marriage has a particular shape to this problem, and it "
    + "deserves to be named precisely before anything else.",

    "From the outside, you look like one of the most composed couples in any room you "
    + "enter. Neither of you is volatile. Neither of you makes scenes. Both of you carry "
    + "yourselves with a kind of considered dignity that most people read as strength, "
    + "and they are not entirely wrong. The question is whether that composure, over years, "
    + "has become something more than strength &mdash; whether the same careful curation "
    + "that makes each of you impressive to the outside world has also, quietly, been "
    + "keeping you from each other.",

    "What follows is a counselor's careful read of the small repeating things in your "
    + "particular marriage. Your pairing is <b>two Vaults</b> &mdash; and the pastoral "
    + "challenge of two Vaults in one marriage is unlike anything else this taxonomy maps. "
    + "It is not that you fight without resolving. It is that you have, by mutual and "
    + "largely unspoken agreement, arranged a marriage in which neither of you is required "
    + "to show the unfinished thing. The locks are respected. The distance is maintained. "
    + "And the result, sometimes years in, is two people who chose each other and who "
    + "do not actually know each other in the places that matter most.",

    "Here is what I want to do for you. I will name what each of you genuinely brings "
    + "the other that you could not have built alone &mdash; because there is a real "
    + "gift in this pairing, and it deserves to be named before anything else is said. "
    + "Then I will name the specific collision your shared mechanism produces &mdash; "
    + "not a fight, but something slower and more consequential. Then I will name the "
    + "harder picture, the moment when two Vaults in breakdown can end a marriage "
    + "graciously and in silence, without either of them having said why. Then I will "
    + "hand each of you commitments: not rules, but the small concrete practices that, "
    + "kept faithfully, begin to change the temperature of a home.",

    "Read it together if you can. Sit with it in the same room. Argue with what does "
    + "not fit; stay with what does. And before you begin, hear this: the fact that "
    + "{name_a} and {name_b} are reading the same pages, about the same marriage, at "
    + "the same time, is itself a form of opening. Two Vaults who agree to look together "
    + "have already done something their mechanism resists. That is not nothing. It is, "
    + "in fact, the first act of the unlocking.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on "
    + "paper, side by side. Most couples never see their two profiles next to each other "
    + "with this kind of deliberate clarity. You are about to &mdash; and for you, the "
    + "first thing you will notice is how much they resemble each other.",
]

TWO_SHAPES_BODY = [
    "{name_a}, you are a <b>Vault</b> whose body reads shame or control as an alarm "
    + "and whose deepest question is <i>Am I acceptable?</i> You have built, over a "
    + "long time and with real effort, a carefully curated relationship between your "
    + "interior life and what you show to the world. The Vault knows what is going on "
    + "inside; it keeps it close. You process internally and bring others the finished "
    + "conclusion. The messy middle &mdash; the doubt, the grief, the half-built thing, "
    + "the longing you have not yet named &mdash; stays private, because something early "
    + "in your history taught you that the interior, shown without preparation, can be "
    + "used against you.",

    "{name_b}, you are a <b>Vault</b> whose body reads the same alarm: shame, the "
    + "threat of exposure, the sudden loss of control over what is seen. Your deepest "
    + "question is the same: <i>Am I acceptable?</i> You, too, have learned to curate. "
    + "To present the organized conclusion rather than the working draft. To give people "
    + "the version of yourself that has been thought through, because the unthought-through "
    + "version has sometimes been received badly, and the cost of that reception was too "
    + "high to risk repeating.",

    "Take a moment to absorb what this means. You are asking the same question. You are "
    + "running the same mechanism. You are, at some level, protecting the same wound in "
    + "the same way. This is the shared grammar that makes your marriage feel, at its "
    + "best, unusually safe &mdash; two people who understand each other's restraint, "
    + "who do not press for access, who respect the distance because they live the "
    + "distance themselves.",

    "But here is what the shared grammar does not automatically produce: <i>the "
    + "unsealing.</i> The Vault's strategy &mdash; if I curate what is shown, I cannot "
    + "be wounded by how it is received &mdash; was built for a world of one. It was not "
    + "built for a marriage. In a marriage, both of you running this strategy produces "
    + "something neither of you intended: two people who have never actually seen each "
    + "other in the unfinished places. Not because either of you has been dishonest, but "
    + "because both of you have been careful. And careful, in a marriage, is not always "
    + "the same thing as present.",

    "This is the singular gift and the singular danger of your marriage. The gift is "
    + "that you have built a home in which neither of you is overwhelmed or over-exposed "
    + "by the other &mdash; the Vault's deepest fear does not fire constantly in a "
    + "two-Vault marriage. The danger is that the same protection that prevents the "
    + "fear also prevents the fellowship. C. S. Lewis, in <i>The Four Loves</i>, writes "
    + "that to love at all is to be vulnerable. The Vault couple has built a marriage "
    + "that is structurally resistant to the vulnerability that Lewis describes &mdash; "
    + "and therefore, also, to the love he is pointing toward.",
]

GIFT_TO_A = [
    "{name_b} gives {name_a} something almost no one else in the marriage is in a "
    + "position to give: <b>a room in which the pressure to perform the interior is "
    + "completely absent.</b>",

    "The Vault has spent much of its life in rooms that study it. Not cruelly, "
    + "necessarily &mdash; most of the people who have loved the Vault have loved it "
    + "with genuine tenderness. But they have pressed. They have asked about feelings "
    + "before the feelings were ready. They have drawn conclusions from half-observed "
    + "expressions. They have noticed the Vault's composure and read it as either "
    + "strength or coldness, and either reading requires a response, and requiring a "
    + "response is its own form of exposure. The Vault has spent real energy managing "
    + "that pressure.",

    "{name_b}, by virtue of being a Vault, does not study {name_a} in this way. The "
    + "Vault does not press, because the Vault knows, from the inside, what pressing "
    + "costs. {name_b} has her own interior to manage; she does not have surplus "
    + "attention to turn into surveillance. For {name_a}, this is one of the rarest "
    + "experiences in an adult life: being in sustained close proximity to another "
    + "person without being required to perform the interior at the other person's "
    + "schedule. The relief this produces is real and deep, even when it goes unnamed.",

    "Tim Keller writes in <i>The Meaning of Marriage</i> that one of the deepest "
    + "gifts of a good marriage is to be known &mdash; not analyzed, but known the "
    + "way a person who has lived beside you for years knows you without needing a "
    + "translation. {name_b} knows {name_a}'s mechanism from the inside. She does not "
    + "flinch at the composure, because composure is her own native language. She does "
    + "not pathologize the silence, because she lives in her own silences and knows "
    + "they are not emptiness. For {name_a}, this is the gift of being received without "
    + "interpretation.",

    "{name_a} &mdash; if you want to thank {name_b} for something this week, thank her "
    + "for the room she has never entered without an invitation. She probably does not "
    + "think of this as a gift; the Vault almost never experiences its own restraint as "
    + "generosity. Tell her that her instinct not to press, not to study, not to require "
    + "the organized conclusion before it is ready &mdash; that instinct has been one "
    + "of the most consistent kindnesses of your life together. She will not know what "
    + "to do with the gratitude. Say it anyway.",

    "{name_b} &mdash; what {name_a} receives from you, when you simply allow him to "
    + "be in process without demanding the product, is a rest he finds in almost no "
    + "other relationship. The thing in you that has sometimes been called guarded or "
    + "withholding is, for him, a form of sanctuary. Receive that.",
]

GIFT_TO_B = [
    "{name_a} gives {name_b} something most of the people who love the Vault will "
    + "eventually stop giving: <b>a witness who does not require the finished version.</b>",

    "Most people who love the Vault, over time, stop asking. Not because they have "
    + "stopped caring, but because the Vault's presentation &mdash; composed, thoughtful, "
    + "resolved &mdash; is so convincing that there does not appear to be anything left "
    + "to ask about. The Vault has, in a sense, curated itself out of being known. The "
    + "world takes the curated self at face value, and the Vault is left with the "
    + "curious loneliness of having succeeded at what it built itself to do.",

    "{name_a}, by virtue of being a Vault himself, is not fooled by the curation. He "
    + "knows what the composure costs, because he pays the same price. He knows that "
    + "the organized conclusion has a messy middle behind it, because he has one of his "
    + "own. He does not read {name_b}'s careful presentation as the whole truth, because "
    + "he knows from the inside that the whole truth is never what the Vault shows first. "
    + "This gives him a peculiar kind of witness &mdash; one who receives the curated "
    + "self without quite believing it is the whole self, and who does not demand the "
    + "rest, but who also does not forget that the rest exists.",

    "The theological word for what {name_a} gives {name_b} is something close to "
    + "<i>faithfulness</i> in the old, weighty sense: a steadfastness that does not "
    + "require the beloved to perform a completed self in order to stay. Proverbs 17:17 "
    + "says: <i>A friend loves at all times, and a brother is born for a time of "
    + "adversity.</i> {name_a}'s love for {name_b} is not contingent on receiving "
    + "access to the interior. He is there before the door opens and he is there if "
    + "it doesn't. For {name_b}, who has learned to grant access only when safety is "
    + "established, this kind of unconditional presence is one of the few things that "
    + "makes unlocking feel conceivable.",

    "{name_b} &mdash; if you want to thank {name_a} for something this week, thank "
    + "him for staying in the waiting place &mdash; for not demanding access, for not "
    + "reading your composure as rejection, for remaining present to you even in the "
    + "seasons when the Vault has given him very little to work with. He has been more "
    + "patient with your locks than you may have acknowledged. Name one instance. He "
    + "will not know what to do with the acknowledgment. Say it anyway.",

    "{name_a} &mdash; what {name_b} receives from you, when you remain present without "
    + "requiring the organized conclusion, is the only soil in which the Vault's "
    + "unlocking ever actually becomes possible. Your faithfulness is the long "
    + "investment that pays out slowly. It is worth more than either of you knows.",
]

COLLISION = [
    "Now we come to the small repeating thing. It will be familiar to both of you, "
    + "even if you have never put it into language &mdash; because the two-Vault "
    + "collision is not a fight. It does not look like a collision at all. That is "
    + "what makes it the most consequential dynamic in your marriage.",

    "Here is what is happening, stated plainly. Two Vaults in a marriage tend to "
    + "develop, slowly and without any formal agreement, an unspoken contract: "
    + "<i>I will not press into your locked interior, and you will not press into "
    + "mine.</i> This contract is never articulated. It emerges organically from "
    + "the mutual recognition that both of you understand what pressing costs. Both "
    + "of you have been pressed before, in other relationships, and the experience "
    + "was unpleasant. So you give each other what you most wanted from others who "
    + "did not give it to you: space, privacy, the freedom to bring the finished "
    + "version of yourself without being pursued for what is behind it.",

    "The contract makes the marriage feel <i>safe.</i> It is one of the things you "
    + "may love most about each other &mdash; the absence of pressure, the sense that "
    + "neither of you has to perform vulnerability on demand. This is real and good. "
    + "But here is what the contract also produces, over time: a marriage in which "
    + "neither of you has ever been seen in the unfinished places. A marriage of "
    + "two finished conclusions living alongside each other. And a conclusion, however "
    + "well-organized, is not a person. You have been, without quite realizing it, "
    + "married to each other's presentations rather than to each other.",

    "Paul writes in 1 Corinthians 13:12: <i>For now we see in a mirror dimly, but "
    + "then face to face. Now I know in part; then I shall know fully, even as I have "
    + "been fully known.</i> Paul is speaking of the eschatological knowledge of God, "
    + "but the verse has an immediate pastoral weight: to be fully known is the "
    + "direction of love, the thing love is always moving toward even when it cannot "
    + "yet arrive. The two-Vault marriage has, with the best of intentions, built a "
    + "structure that points deliberately away from this &mdash; a structure optimized "
    + "for protection rather than for the kind of knowing Paul describes.",

    "The collision, when it finally becomes visible, is rarely a fight. More often "
    + "it is a moment &mdash; sometimes years into the marriage &mdash; when one or "
    + "both of you realizes that something essential is missing. That you can describe "
    + "your spouse's habits, preferences, and surface responses with great precision, "
    + "but that you cannot describe what your spouse is actually afraid of right now, "
    + "what they are grieving, what question is running underneath the competence. "
    + "The realization arrives quietly: <i>I have been married to a finished "
    + "conclusion. I have never actually met the person in process.</i>",

    "Ephesians 5:25&ndash;27 gives a striking picture of what Christ's love for the "
    + "Church looks like: <i>Husbands, love your wives, as Christ loved the church "
    + "and gave himself up for her, that he might sanctify her, having cleansed her "
    + "by the washing of water with the word, so that he might present the church to "
    + "himself in splendor, without spot or wrinkle or any such thing, that she might "
    + "be holy and without blemish.</i> Notice what Paul does not say. He does not "
    + "say the Bride hides her spots so that the presentation can be acceptable. He "
    + "says the Bride is <i>brought</i> to the spotless state by being washed "
    + "&mdash; by being known in her unfinished state and loved through it into "
    + "glory. The Vault couple has arranged a marriage in which no washing can "
    + "occur, because the spots are always managed out of sight before anyone "
    + "gets close enough to see them.",

    "{name_a}, here is the way out, in your grammar. The Vault's instinct is to "
    + "wait until something is organized before bringing it. The discipline you are "
    + "being asked to practice is the opposite: to bring one thing to {name_b} while "
    + "it is still in the middle. Not the darkest thing. Not the most frightening "
    + "thing. One small, real, unfinished thing. <i>I am working through something "
    + "I do not have words for yet. I wanted you to know it is there.</i> That "
    + "sentence is not a flood. It is a door, opened a crack. The Vault can do that.",

    "{name_b}, here is the way out, in the same grammar. When {name_a} offers "
    + "something unfinished &mdash; a worry half-named, a frustration not yet "
    + "organized &mdash; the Vault's instinct is to receive it, file it, and respond "
    + "with a polished conclusion. The discipline is to receive it and offer "
    + "something unfinished in return. Not a response. Something from your own "
    + "interior that is also still forming. <i>I have something like that too. I "
    + "haven't sorted it out yet either.</i> That sentence is, for a two-Vault "
    + "marriage, one of the most radical things either of you can say. It establishes "
    + "that the unfinished interior is allowed to exist between you, not only inside "
    + "each of you separately.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be seasons &mdash; not often, but they will "
    + "come &mdash; when both of you have retreated fully behind your locks at the "
    + "same time. And here is what makes the two-Vault breakdown different from almost "
    + "any other couple's: it does not escalate. It does not produce a scene. It "
    + "produces something quieter and more consequential.",

    "The most common pattern for the two-Vault breakdown is what we call <b>parallel "
    + "Quiet Exits.</b> Not the dramatic departure. The slow, mutual, nearly "
    + "imperceptible withdrawal from interior investment in the marriage. Each Vault, "
    + "wounded, does what the mechanism was built to do: it takes the wound inside, "
    + "closes the door, and begins to process privately. The case against the other "
    + "person builds inside, with the Vault's characteristic precision: dated, sourced, "
    + "organized. The other Vault is doing the same thing. Neither of them is saying "
    + "so. Both of them are being &mdash; from the outside, and even from the inside "
    + "&mdash; perfectly civil. The marriage is ending without a scene.",

    "The other pattern is the <b>parallel Ghost:</b> both Vaults retreating further "
    + "behind composure, performing normalcy while the interior has quietly vacated "
    + "the marriage. The Vault Ghost is the hardest of all the breakdowns to interrupt "
    + "from the inside, because it looks, from the inside, like steadiness. The Vault "
    + "in Ghost mode does not feel like it is in breakdown. It feels like it is being "
    + "appropriate. The discipline required of a watching eye. The management of "
    + "what is shown. The quiet professionalism of a person who has decided, at a "
    + "level below articulation, that the marriage is no longer worth the cost of "
    + "exposure &mdash; but who has not quite said that yet, even to themselves.",

    "Psalm 139:1&ndash;6 speaks into this moment with precision that should be "
    + "uncomfortable for both of you: <i>O Lord, you have searched me and known me! "
    + "You know when I sit down and when I rise up; you discern my thoughts from afar. "
    + "You search out my path and my lying down, and are acquainted with all my ways. "
    + "Even before a word is on my tongue, behold, O Lord, you know it altogether. "
    + "You hem me in, behind and before, and lay your hand upon me. Such knowledge is "
    + "too wonderful for me; it is high; I cannot attain it.</i> The psalmist is "
    + "naming the experience of being fully known &mdash; not curated, not presented, "
    + "not organized first &mdash; and finding that the knowledge does not destroy "
    + "but envelops. The two-Vault marriage has structured itself against this "
    + "experience with each other, which is precisely why it is the experience "
    + "both of you most need.",

    "1 John 1:7 adds the relational dimension: <i>if we walk in the light, as he "
    + "is in the light, we have fellowship with one another, and the blood of Jesus "
    + "his Son cleanses us from all sin.</i> Fellowship &mdash; the deep, mutual "
    + "presence John describes &mdash; is the product of walking in the light. Not "
    + "a performance of light; not a curated presentation of the acceptable parts "
    + "of oneself. The walking. The actual, in-process, unfinished walking. The two "
    + "Vaults in breakdown have, each of them, stopped walking in each other's "
    + "presence. The fellowship John describes has gone dark.",

    "What to do when you can still see what is happening:",

    "<b>One of you names it out loud.</b> This is the hardest thing in a two-Vault "
    + "breakdown, because neither of you is in the habit of naming the interior "
    + "without preparation. But this is the one moment where the preparation must "
    + "be skipped. Whichever one of you notices first &mdash; which will be the "
    + "one whose love for the marriage is, in that moment, stronger than the "
    + "Vault's instinct &mdash; says, without organizing it first: <i>I think "
    + "we are both behind our locks right now. I don't think either of us has "
    + "actually been here for a while. I want to put one thing in the room.</i> "
    + "Not the file. Not the organized case. One thing &mdash; the earliest, "
    + "smallest, most specific wound that started the withdrawal. Named in one "
    + "sentence.",

    "<b>Neither of you uses the pause to draft the file.</b> The Vault's instinct, "
    + "even in a moment of repair, is to use the time to organize the brief. The "
    + "discipline is to resist this with deliberate prayer. Bonhoeffer writes in "
    + "<i>Life Together</i>: <i>Confession in the presence of a brother is the "
    + "profoundest kind of humbling. It hurts, it cuts down, it is a dreadful "
    + "blow to pride.</i> The Vault couple has built a marriage that protects "
    + "them from this humbling, which also means it protects them from the "
    + "fellowship that the humbling alone can produce. In the moment of repair, "
    + "do not organize. Confess. One real thing, said without curation, to the "
    + "person who has been placed next to you by God to receive it.",

    "<b>When you come back to each other, lead with the unfinished, not the "
    + "conclusion.</b> The two-Vault repair fails when both spouses arrive at "
    + "the conversation with polished positions. It works when one of them "
    + "arrives with something that is still forming. <i>I do not fully "
    + "understand why this hurt me as much as it did. I am still sorting it "
    + "out. But I wanted to bring it to you while I was still in the middle "
    + "of it.</i> Those sentences are, for the Vault, an act of theological "
    + "courage. They are also the only sentences that can interrupt the parallel "
    + "Quiet Exit before it becomes a destination.",

    "<b>Neither of you is the problem.</b> The Quiet Exit and the Ghost are "
    + "not the truest things about either of you. They are old mechanisms doing "
    + "what they were built to do &mdash; protecting a wound that was real, in "
    + "a season that required protection. The truest thing about both of you is "
    + "that you chose each other, and you are still here, and two Vaults who "
    + "learn, slowly and with great difficulty, to bring the unfinished thing "
    + "to each other are building something the mechanism alone could never "
    + "have built: a home where the interior is actually shared, and where "
    + "the sharing has not destroyed either of them.",
]

COMMITMENTS_INTRO = [
    "What follows are eight commitments &mdash; four from {name_a}, four from {name_b}. "
    + "They are not vows in the legal sense. They are the small daily practices that, "
    + "offered to each other freely and kept with patience, begin to change the temperature "
    + "of a home across months and years. For the two-Vault marriage, the key pastoral "
    + "direction is the same for both of you: <i>lead with disclosure of the unfinished.</i> "
    + "Not the organized conclusion. The middle. The thing that is still forming. This is "
    + "the discipline that makes two Vaults into one household. Read each commitment "
    + "slowly. If you cannot say one of them in good faith yet, do not say it. Honesty "
    + "about what you cannot yet offer is more useful to this marriage than "
    + "performance of what you think you should.",
]

A_COMMITMENTS = [
    ("To tell you one unfinished thing today.",
     "{name_b}, I commit to naming one thing I am carrying before I have finished "
     + "processing it. Not the conclusion &mdash; the Vault can live with sharing "
     + "conclusions; it has always done that. The middle. The unresolved thing. I "
     + "will say it in one sentence, without organizing it first, once a day. The "
     + "Vault in me will tell me the thing is not ready. I will bring it anyway, "
     + "because a marriage in which you only ever know my finished conclusions is "
     + "a marriage in which you have never actually known me."),

    ("To receive your unfinished thing without filing it.",
     "{name_b}, when you bring me something that is still forming, I commit to "
     + "receiving it as a person, not as data. I will resist the Vault's instinct "
     + "to organize what you have given me into a file, a conclusion, a response "
     + "that is tidier than what you offered. I will hold the unfinished thing "
     + "gently and offer something unfinished in return. Because what you gave me "
     + "was a door opened, not a problem to be solved, and the only right answer "
     + "to an opened door is to step through it."),

    ("To name when the locks are closing.",
     "{name_b}, when I feel the Vault's interior strategy beginning &mdash; when "
     + "I am organizing a wound into a file rather than bringing it to you while "
     + "it is still small &mdash; I commit to naming it before the filing is "
     + "complete. One sentence: <i>Something happened and I am starting to carry "
     + "it alone. I want to tell you before it gets too organized to be honest.</i> "
     + "That sentence is harder to say than any conclusion. I will practice it."),

    ("To call the pause before the Quiet Exit assembles.",
     "{name_b}, when I notice that I have been withdrawing from interior investment "
     + "in this marriage &mdash; when the evidence is growing in the interior file "
     + "and the composure is performing while the person has left the room &mdash; "
     + "I commit to naming it before the exit becomes a destination. I will not "
     + "wait until I have a tidy explanation. <i>I think I have been going quiet "
     + "in a way that is not good. I do not want to do that. Can we stop?</i> "
     + "Those words, said while it is still true, are worth more than any "
     + "conclusion I could eventually arrive at alone."),
]

B_COMMITMENTS = [
    ("To tell you one unfinished thing today.",
     "{name_a}, I commit to naming one thing I am carrying before I have finished "
     + "processing it. The Vault in me has built a very strong habit of presenting "
     + "only what is ready. I am committing to breaking that habit, in small measures, "
     + "once a day, with you. Not the organized conclusion. The thing that is still in "
     + "the middle. Said without waiting until it is safe to say, because waiting "
     + "until it is safe is how two Vaults end up never saying anything that matters."),

    ("To receive your unfinished thing without filing it.",
     "{name_a}, when you bring me something still in process, I commit to receiving "
     + "it as a gift rather than as information to be assessed. I know the Vault's "
     + "instinct is to receive and organize. I will receive and be present instead. "
     + "I will ask one question that comes from curiosity rather than from the "
     + "desire to resolve the thing for you. I will offer something of my own that "
     + "is also unfinished. Because you trusted me with the middle, and the middle "
     + "deserves more than a conclusion."),

    ("To name when the locks are closing.",
     "{name_a}, when I feel the file beginning to build &mdash; when something you "
     + "said or did is being organized into a case rather than brought to you as a "
     + "wound &mdash; I commit to naming the wound before the case is ready. One "
     + "sentence, while the wound is still small: <i>something you did last night "
     + "is sitting with me and I have not said it yet.</i> Not the file. Not the "
     + "organized version. The one sentence. You deserve to know before the "
     + "Vault has processed you out of being able to help."),

    ("To call the pause before the Quiet Exit assembles.",
     "{name_a}, when I notice the interior withdrawing from this marriage &mdash; "
     + "when the composure is performing and the person has quietly made other "
     + "arrangements &mdash; I commit to naming it before the exit has a "
     + "destination. Not with the organized explanation. With the honest admission: "
     + "<i>I think I am starting to plan alone. I do not want to do that. I want "
     + "to be here, with you, even in the part that is not ready.</i> That sentence "
     + "is an act of faith in this marriage. I will practice it."),
]

PRAYER = [
    "Father,",

    "You set these two Vaults next to each other, and you knew exactly what you were "
    + "doing. You knew that two people who process in private and present only what is "
    + "ready would understand each other in ways that most spouses cannot. You also "
    + "knew that two Vaults in one marriage would, without intending to, build a home "
    + "in which the unfinished thing never crosses from one person to the other &mdash; "
    + "in which both of them are, in the most important sense, alone. You knew all of "
    + "it before either of them said yes. You put them together anyway, and we trust "
    + "that you knew what you were doing.",

    "Teach them the unsealing that their mechanism resists. Teach {name_a} to bring "
    + "{name_b} the thing that is still forming &mdash; not the conclusion he has "
    + "prepared, not the version that is ready for inspection, but the middle, the "
    + "unresolved, the half-built grief that is actually there. Remind him that "
    + "the God who has already searched him and known him &mdash; who knew every "
    + "locked room before the first door was installed &mdash; did not turn away. "
    + "Let that truth make the unlocking possible.",

    "Teach {name_b} the same courage in the same grammar. Let her bring {name_a} "
    + "one unfinished thing today, before it is organized, before it is safe, "
    + "before the Vault has processed it into something that no longer looks like "
    + "vulnerability. Remind her of what you wrote through John: <i>if we walk in "
    + "the light, as he is in the light, we have fellowship with one another.</i> "
    + "The fellowship she most wants from this marriage is available. It is on the "
    + "other side of the walking. Give her courage to walk.",

    "When the Quiet Exit is assembling &mdash; two organized interiors quietly "
    + "building two separate futures in two separate silences &mdash; wake one of "
    + "them first. Give them the nerve to say the hard sentence before the exit "
    + "becomes a verdict: <i>I think we are both behind our locks. I want to put "
    + "one thing in the room.</i> Let the one who goes first discover that the "
    + "other one is relieved. Because they are. The Vault always is, when someone "
    + "else goes first, because going first is the thing the Vault has never been "
    + "willing to do alone.",

    "And where each of them asks &mdash; in the interior, quietly, as they have "
    + "always asked &mdash; <i>Am I acceptable?</i> Let them hear the answer that "
    + "was given before the question was formed. In Christ, at the cross, fully "
    + "exposed and fully covered: <i>justified.</i> They do not have to curate "
    + "what they show you, because you have already seen everything and have "
    + "already spoken. Let that be the ground under this marriage &mdash; the "
    + "thing that makes unlocking possible, because neither of them has anything "
    + "left to protect.",

    "Make their home a room where two people who both know how to keep the "
    + "interior private have learned something harder than keeping: how to open "
    + "it, one small and imperfect and unready thing at a time, to each other. "
    + "And when they are old, and the years of small, brave unlockings have "
    + "accumulated into something neither of them expected &mdash; let them see "
    + "that the marriage they were afraid to be known inside of became the safest "
    + "room either of them ever lived in.",

    "In the name of the One who was himself fully disclosed &mdash; exposed, "
    + "known, nothing hidden &mdash; so that we might be fully covered; and who "
    + "calls us even now to bring what we have locked away into the light of "
    + "his face.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages "
    + "that follow are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, somewhere "
    + "quiet, with no children in the room and no phones on the table. There are six "
    + "rounds, and they build on each other. Resist the temptation to skip ahead. Start "
    + "at Round One even if it feels too easy; the ease at the beginning is the point.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did not read "
    + "answers first, in full, without interruption. Then the reader answers the same "
    + "question. Then you move on. You do not have to finish all six rounds in one "
    + "evening &mdash; two or three rounds, taken seriously and without rushing, is "
    + "often better than completing all of them in one sitting. Save the rest "
    + "for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. You may not love "
    + "everything you hear. Stay with it. The point of this is not to evaluate each "
    + "other's answers. The point is to be known &mdash; actually known, in the "
    + "middle, before the processing is complete &mdash; and to do the patient "
    + "work of knowing.",
]

ROUND_1 = [
    ("hypothetical",
     "If our marriage were a room, what kind of room would it be &mdash; and what "
     + "is in it that we have never talked about?",
     "Two Vaults. Let the metaphor do what plain language resists. Be specific "
     + "about what is in the room. The thing you've never mentioned is the point."),
    ("observation",
     "What is something I did or said this week that you noticed and didn't comment on?",
     "Not a complaint. Not necessarily a compliment. Just something you noticed. "
     + "The Vault notices more than it says. This question gives the noticing a voice."),
    ("playful",
     "If you had to describe our marriage as a specific kind of locked box &mdash; "
     + "a Victorian bureau, a bank vault, a jewelry chest, a time capsule &mdash; "
     + "what would you pick, and what is the combination?",
     "Yes, really. Let the first answer surface. The metaphor will tell you "
     + "something you did not expect about what each of you thinks is inside."),
]

ROUND_2 = [
    ("fill-in-blank",
     "I don't think I tell you this enough &mdash; I am genuinely grateful that you "
     + "are the kind of person who _______. That quality in you has made me _______ "
     + "in ways I would not have been on my own.",
     "Two blanks. The second one is what you have been receiving without naming. "
     + "Be specific enough that only you could have said it about only this person."),
    ("observation",
     "Name one thing you have watched me carry alone this year that I probably "
     + "did not tell you about &mdash; and that you somehow knew was there anyway.",
     "Two Vaults. You have both been noticing each other's interior through the "
     + "composure. This is the question that gives the noticing a voice."),
    ("one-word",
     "If you had to choose one word for what it feels like when I bring you something "
     + "unfinished &mdash; something I haven't organized yet &mdash; what would it be?",
     "One word, said out loud. Then explain it without editing yourself. The Vault's "
     + "answer to this question is usually not what the Vault expects."),
]

ROUND_3 = [
    ("forward-looking",
     "Ten years from now, when we look back on this season of our marriage, what is "
     + "the one thing you most hope we figured out how to do together?",
     "Not what you wish had been different. What you want, ten years out, to be "
     + "able to say you actually learned. Name it specifically."),
    ("theological",
     "Where, in the last month, have you seen God specifically at work in me &mdash; "
     + "not where you hope he will work, but where you have already seen it happening?",
     "Name it with the specificity of a witness. 'Generally more patient' is "
     + "too easy. The particular moment, the specific thing &mdash; that is witness."),
    ("shared-identity",
     "Finish this sentence three times: 'We are the kind of couple who _______.' "
     + "Give one playful answer, one honest answer, and one aspirational answer.",
     "The 'we' is the point. Each answer tells you something about how you see "
     + "the marriage as a unit rather than as two separate people."),
]

ROUND_4 = [
    ("strength",
     "What is something I carry for this marriage that you would have to learn to "
     + "carry for yourself if I were not here?",
     "Two Vaults often under-acknowledge each other because both assume the "
     + "other one already knows. This is the question that makes the invisible "
     + "contribution visible. Stay with the answer. Say it in full."),
    ("fill-in-blank",
     "One of the gifts of being married to you is that I get to be _______ in ways "
     + "I never would have been on my own &mdash; and the version of myself that "
     + "exists because of this marriage is better than any version I would have "
     + "managed alone because of your _______.",
     "A version of yourself, and a quality of the marriage, that only exist because "
     + "the marriage exists. Name both specifically enough that they could not "
     + "apply to anyone else."),
    ("observation",
     "Name one moment in our story where you knew, with no doubt, that we had built "
     + "something together that neither of us could have built alone.",
     "Tell the whole story. Do not summarize. The remembering, done in detail "
     + "and out loud, is part of what makes the marriage stronger."),
]

ROUND_5 = [
    ("hard",
     "When was the last time you felt like you were behind your locks and I did not "
     + "know it &mdash; and what would you have needed me to do differently?",
     "One moment. Named carefully. Heard without defending. This is the question "
     + "that goes to the center of what the two-Vault marriage most needs to practice."),
    ("profile-aware",
     "When you sense that I have organized a wound into a file rather than brought "
     + "it to you &mdash; when you can tell the Vault has been at work &mdash; what "
     + "is one thing you wish you could say or do in that moment that you haven't yet?",
     "You both know the mechanism now. This question names what the other person "
     + "wishes they could offer. Hear it without defending. It is a gift."),
    ("theological",
     "What is one thing you are carrying right now &mdash; a fear, a grief, a question "
     + "about us &mdash; that you have not yet brought to me, and what has kept you "
     + "from bringing it?",
     "Not an accusation. An invitation. Answer it unfinished. Hear the answer "
     + "without organizing it into a response. Just receive it."),
]

ROUND_6 = [
    ("blessing",
     "Place your hand on your spouse's hand. Say their name. Then say: 'I do not "
     + "need the organized version of you. I want the one that is still in the "
     + "middle. I am not going anywhere.' Say it slowly. Let them say it back.",
     "The Vault in both of you will want to edit this. Don't. Say it as written, "
     + "slowly, by name. The unedited version is the point."),
    ("prayer",
     "Pray for each other &mdash; not silently, not in general, but out loud and "
     + "by name. One sentence is enough. Pray for the specific thing they told you "
     + "in Round Five. Do not make the prayer about the conclusion. Pray into the middle.",
     "The closing of the date. Do not skip. Two Vaults who pray for each other "
     + "by name, about the unfinished thing, have done something the mechanism "
     + "alone cannot do. The prayer is itself the unlocking."),
]


def _render(text, name_a, name_b):
    return text.format(name_a=name_a, name_b=name_b)


def build(sub_a, sub_b) -> bytes:
    """Generate the Vault+Vault couples walkthrough PDF.

    sub_a: the submission of one Vault spouse
    sub_b: the submission of the other Vault spouse

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
        "A counselor\u2019s read of two locked interiors<br/>and the marriage between them.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("PREPARED FOR", S["CoverProfileLabel"]))
    story.append(Paragraph(f"{name_a} &nbsp;&amp;&nbsp; {name_b}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_a.upper()}</b></font><br/>"
                "Vault &middot; Quiet Exit / Ghost<br/>"
                f"<font size=9 color='#6b6862'>Shame &middot; Am I acceptable?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_b.upper()}</b></font><br/>"
                "Vault &middot; Quiet Exit / Ghost<br/>"
                f"<font size=9 color='#6b6862'>Shame &middot; Am I acceptable?</font>",
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
        "<i>\u201cFor now we see in a mirror dimly, but then face to face.<br/>"
        "Now I know in part; then I shall know fully,<br/>"
        "even as I have been fully known.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "1 Corinthians 13:12",
        ParagraphStyle("cqa", fontName="Inter", fontSize=9, leading=14,
                       textColor=MUTED, alignment=TA_CENTER)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: OPENING ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "Two locked rooms, one home.",
                   "Why this pairing exists, and what you are both about to read.")
    for p in OPENING:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 2: YOUR TWO SHAPES ──
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TWO SHAPES",
                   "Side by side, on paper.",
                   "Two profiles that look alike \u2014 and the single unlocking that matters most.")
    for p in TWO_SHAPES_INTRO:
        story.append(Paragraph(R(p), S["BodyJ"]))
    side_by_side = Table(
        [[
            _profile_card(S, name_a, ACCENT,
                          "Shame / Control", "Am I acceptable?",
                          "The Vault", "Quiet Exit / Ghost"),
            "",
            _profile_card(S, name_b, ACCENT_HER,
                          "Shame / Control", "Am I acceptable?",
                          "The Vault", "Quiet Exit / Ghost"),
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
                   "The gift of being received without interpretation.")
    for p in GIFT_TO_A:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4: GIFT B TO A ──
    section_header(story, S, f"SECTION FOUR  \u00b7  {name_b.upper()}\u2019S GIFT TO {name_a.upper()}",
                   f"What {name_b} gives {name_a}.",
                   "A witness who does not require the finished version.")
    for p in GIFT_TO_B:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5: THE COLLISION ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "The unspoken contract.",
                   "The small repeating thing that makes no sound.")
    for p in COLLISION[:4]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The collision made visible.",
                   "And the way out, for each of you in your own grammar.")
    for p in COLLISION[4:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6: THE HARDER PICTURE ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When both Vaults go silent at once.",
                   "The parallel Quiet Exit, and what to do while you can still see it.")
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
                   "Four from each of you. Lead with disclosure of the unfinished.")
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
                  "The harder ones. Asked gently. Heard without organizing.")
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
        "I do not need the organized version of you.<br/>"
        "I want the one that is still in the middle.<br/>"
        "I am not going anywhere.",
        closing_style))

    doc.build(story)
    return finalize_buffer(buf)


# ── STANDALONE TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "VAULT"
        primary_breakdown = "GHOST"
        primary_trigger = "SHM"
        core_question = "ACC"
        name = "Anna Vault"

    class FakeSubB:
        primary_mechanism = "VAULT"
        primary_breakdown = "QE"
        primary_trigger = "CTRL"
        core_question = "ACC"
        name = "Ben Vault"

    pdf_bytes = build(FakeSub(), FakeSubB())
    out_path = os.path.join(os.path.dirname(__file__), "vault_vault_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages via DSC markers
    page_count = pdf_bytes.count(b"%%Page:")

    # Section Three snippet
    snippet = GIFT_TO_A[0][:200]

    print(f"DONE: vault_vault.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Output:   {out_path}")
    print(f"Pages (approx): {page_count}")
    print(f"Section Three snippet: {snippet}")
