"""Couples Walkthrough — Adapter + Vault.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where Spouse A is an Adapter and
Spouse B is a Vault. First names are substituted from the submissions:
    {name_a}  -> the Adapter spouse's first name
    {name_b}  -> the Vault spouse's first name

Adapter: trigger Control/Shame, core question "Am I free?" / "Am I acceptable?"
Vault:   trigger Shame, core question "Am I acceptable?"

Key pastoral dynamic: The Adapter calibrates outward — fluent, attuned,
mirror-like. The Vault holds inward — closed, curated, finished. From outside
this looks like a marriage where the warm, social spouse compensates for the
reserved one. From inside, neither spouse has quite landed in real intimacy.
The Adapter does not know which version the Vault is responding to; the Vault
has watched the Adapter cycle through versions and has learned not to trust
any single one — because if the Adapter can be many people, can the love also
be many things?

The unique pastoral move is naming the unspoken bargain: the Adapter does not
press the Vault into exposure (because the Adapter does not have a fixed enough
self to demand fixity from the spouse), and the Vault does not press the Adapter
into a single version (because the Vault appreciates the relief of not being
asked to perform the interior). The bargain works for years. It also means
neither spouse has been honestly known by the other.
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


# ──────────── PROSE — uses {name_a} (Adapter) and {name_b} (Vault) ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small "
    "repeating ones &mdash; the same wordless distance in slightly different clothes, "
    "week after week, until both people have stopped expecting anything different "
    "and have learned to call the distance peace.",

    "This document is about your particular kind of distance. It is not the "
    "distance of two people who have given up on each other. It is the distance "
    "of two people who have, without quite deciding to, built a quiet arrangement "
    "that keeps them comfortable and keeps them apart. From the outside, your "
    "marriage often looks like a natural pairing: one of you warm and socially "
    "gifted, the other steady and private. People who know you may have described "
    "it that way. There is truth in the description. What it does not capture is "
    "what happens behind it &mdash; the specific way that two people who are each, "
    "in their own fashion, very good at managing what they show have arrived at a "
    "marriage where neither of them is quite sure they have been known.",

    "You are both reading this because something has begun to feel insufficient "
    "about the arrangement. That feeling is more significant than it appears. "
    "Many couples never feel it at all &mdash; they are too comfortable, or too "
    "busy, or too practiced at the management. The fact that you are here, reading "
    "this together, means something in both of you suspects there is more available "
    "than what you have so far received from each other.",

    "Here is what I intend to do. I will name what each of you genuinely brings "
    "the other &mdash; the real gift, the theological one, the thing you could "
    "not have gotten from a different spouse. Then I will name the particular "
    "dynamic your two shapes create &mdash; the bargain you have made, mostly "
    "without words, and what it has cost you. Then I will name the harder picture, "
    "and then I will hand each of you something specific to do.",

    "Read it together if you can. If not, read it separately and then sit down "
    "with it. Argue with what does not fit. Stay with what does. The goal is not "
    "a better understanding of each other as personality types. The goal is a "
    "marriage in which two people who are each very good at being unknown finally "
    "begin to be known.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, "
    "on paper, side by side. Most couples never see their two profiles next to each "
    "other. You are about to.",
]

TWO_SHAPES_BODY = [
    "{name_a}, you are an <b>Adapter</b> whose body reads control and shame as "
    "alarm signals, and whose deepest question is whether you are free &mdash; "
    "free to be yourself, free to be acceptable exactly as you are. You move "
    "through the world the way a musician moves through different keys: the same "
    "instrument, a different sound depending on what the room requires. You are "
    "genuinely present in every version of yourself that you offer. But underneath "
    "the fluency lives a question that the fluency is very good at outrunning: "
    "<i>if I stopped reading the room and became simply, unalterably myself "
    "&mdash; would that self be loved? Would it be acceptable?</i> When the "
    "pressure becomes too great, a <b>Plea</b> can follow &mdash; the urgent, "
    "almost desperate attempt to restore the connection that felt threatened "
    "&mdash; or the mechanism can drift toward a <b>Quiet Exit</b>, receding "
    "from a room that began pressing you into a version you cannot hold.",

    "{name_b}, you are a <b>Vault</b> whose body also reads shame as its primary "
    "alarm signal, and whose deepest question is whether you are acceptable &mdash; "
    "acceptable as you actually are, with the unfinished and unglamorous interior "
    "that most people never see. You process carefully before speaking. You bring "
    "conclusions rather than processes. The messy middle &mdash; the doubt, the "
    "grief, the half-formed things &mdash; stays yours until it is organized enough "
    "to present. When the wound becomes large enough to force the vault open, "
    "what emerges is not the messy middle but a carefully assembled file: "
    "organized, dated, specific. An <b>Attorney</b> who has been keeping records "
    "longer than anyone knew.",

    "Notice the most striking thing these two profiles share: they are both asking "
    "the same core question. {name_a} and {name_b} are each, in their own idiom, "
    "asking <i>am I acceptable?</i> &mdash; asking it constantly, quietly, beneath "
    "every interaction. But they are asking it in such different directions that "
    "they have, until now, rarely noticed they were asking the same thing. {name_a} "
    "asks it outward, by reading rooms and offering the version most likely to be "
    "received. {name_b} asks it inward, by managing what is shown and presenting "
    "only what has been approved. Both strategies answer the same fear. Neither "
    "strategy, by itself, is capable of answering it permanently.",

    "What you share underneath is a common wound: both of you have come to believe, "
    "at some level beneath conscious thought, that exposure is dangerous. "
    "That being seen, fully and without preparation, is a risk that has to be "
    "managed. {name_a} manages it by offering a version so well-suited to the "
    "room that there is nothing to reject. {name_b} manages it by curating what "
    "the room receives so that the parts most likely to be found wanting stay "
    "private. These two strategies do not cancel each other out. They find "
    "each other with a kind of relief &mdash; and then build a very comfortable, "
    "very quiet distance.",

    "From the outside, your marriage has often looked like a balanced pairing. "
    "One of you socially fluent; the other privately solid. People have said so. "
    "What they cannot see from the outside is what this document is going to "
    "name &mdash; not to disturb the peace you have made, but to show you "
    "what a more honest peace might look like.",
]

GIFT_TO_A = [
    "{name_b} gives {name_a} something that almost no other person in the Adapter's "
    "world is positioned to give: <b>a room that does not ask for a performance.</b>",

    "Every other room the Adapter walks into makes a request. The workplace asks "
    "for competence. The social gathering asks for warmth and wit. The difficult "
    "relationship asks for the version of you that can hold the tension. Even "
    "the friendships that feel most relaxed are, at some level, asking {name_a} "
    "to be something &mdash; and the Adapter, whose genius is reading exactly "
    "what is being asked and delivering it, cannot easily stop reading even when "
    "no one is looking.",

    "{name_b}, by the nature of the Vault mechanism, does not make that request "
    "in the usual way. The Vault is not performing in the room. The Vault is not "
    "tracking whether {name_a} is bringing the right version. The Vault has its "
    "own interior preoccupations, its own carefully managed inner world, and it "
    "does not, in the moment-to-moment texture of ordinary life, require {name_a} "
    "to be reading the room on its behalf. For a person whose engine never quite "
    "turns off, this is remarkable. {name_a} can be near {name_b} and not "
    "feel the pull to calibrate. This is, without {name_a} usually naming it "
    "as such, one of the most restful experiences the Adapter knows.",

    "The theological word for what {name_b} gives {name_a} is close to what "
    "the Psalms call <i>a broad place</i> &mdash; a room in which the soul is "
    "not required to perform for its standing. Psalm 31:8: <i>you have set my "
    "feet in a broad place.</i> The Adapter's deepest fear is that freedom must "
    "be earned by reading and becoming. {name_b}'s presence, at its best, "
    "quietly refuses that premise. You do not have to become anything to be "
    "near the Vault. The Vault asks only that you be present. For {name_a}, "
    "this is an uncommon gift.",

    "{name_a} &mdash; if you want to thank {name_b} for something this week, "
    "thank them for the evenings when you were simply next to each other, "
    "without the social machinery running, and something in you could rest. "
    "{name_b} may not know they were giving that to you. Name it. Tell them "
    "that the particular quality of their presence &mdash; the willingness to "
    "simply be, without requiring you to perform being &mdash; is one of the "
    "specific gifts that makes this marriage yours and not someone else's.",

    "{name_b} &mdash; what {name_a} receives from you, in the moments when "
    "you are simply present without an agenda for who they should be, is "
    "the closest thing to freedom the Adapter gets in most weeks. The "
    "self-containment in you that others have sometimes experienced as "
    "withholding is, for {name_a}, a kind of permission.",
]

GIFT_TO_B = [
    "{name_a} gives {name_b} something the Vault rarely receives and "
    "almost never builds for itself: <b>the warmth of being genuinely "
    "reached for.</b>",

    "The Vault, by design, does not reveal enough of itself to make reaching "
    "for it easy. People who do not know {name_b} well tend to read the "
    "reserve as self-sufficiency and leave them alone. People who have been "
    "hurt by the Vault's careful management of the interior have learned not "
    "to reach. The result, for many Vaults, is that the inner world grows "
    "richer and more private simultaneously &mdash; a library with thicker "
    "and thicker walls, and fewer and fewer visitors.",

    "{name_a}, by the nature of the Adapter mechanism, does not read "
    "{name_b}'s reserve as a stop sign. The Adapter reads rooms. "
    "The Adapter reads people. And what {name_a} reads in {name_b} &mdash; "
    "even when {name_b} has presented only the curated surface &mdash; "
    "is that there is more. The Adapter does not always know what the more is. "
    "But the Adapter can sense the depth, and the Adapter's attunement "
    "reaches for it without requiring it to announce itself first. "
    "For the Vault, who has organized an entire internal system around "
    "the premise that genuine reaching is rare and dangerous, being "
    "genuinely reached for is quietly extraordinary.",

    "There is a theological image for what {name_a} gives {name_b}. "
    "Bonhoeffer wrote in <i>Life Together</i> that the Christian community "
    "is called to bear one another's burdens &mdash; not the burdens people "
    "present, but the ones they actually carry. The Adapter's attunement, "
    "which functions like a kind of emotional fluency, can detect the weight "
    "of what {name_b} is carrying even when {name_b} has not named it. "
    "This is a form of being witnessed that the Vault, in its ordinary "
    "social interactions, almost never experiences. {name_a} can be "
    "the witness the Vault has been waiting for, if the Vault will risk "
    "letting the witness see something real.",

    "{name_b} &mdash; if you want to thank {name_a} for something this week, "
    "thank them for the specific moments when they reached past the presented "
    "surface and asked for the person underneath it. Not because they had to. "
    "Not because you made it easy. Because something in them could sense that "
    "the surface was not the whole of what was there. That noticing is a gift. "
    "Tell them so.",

    "{name_a} &mdash; what {name_b} receives from you, in the moments when "
    "your attunement refuses to accept the curated conclusion and reaches "
    "for the person behind it, is the experience of being known despite "
    "themselves. For a Vault, that experience is among the rarest and most "
    "disorienting goods in a marriage. It is also, over years, among "
    "the most healing ones.",
]

COLLISION = [
    "Now we come to the small repeating rock. It is quieter than most "
    "marital collisions, which is part of why it has been so hard to name.",

    "The Adapter and the Vault share a trigger &mdash; shame &mdash; and "
    "they share a core question &mdash; <i>am I acceptable?</i> &mdash; "
    "but they have developed strategies so different in their expression "
    "that the two people living inside these strategies rarely recognize "
    "themselves as asking the same question. {name_a} manages the fear "
    "of being unacceptable by becoming whatever the room most needs. "
    "{name_b} manages the same fear by showing the room only what has "
    "been approved. Neither strategy requires the other to fail. "
    "In fact, each strategy quietly depends on the other not pressing too hard.",

    "This is the thing that must be named, because it is the most distinctive "
    "feature of your pairing: <b>you have made an unspoken bargain.</b> "
    "{name_a} does not press {name_b} into exposure &mdash; does not demand "
    "that the vault open, does not require the messy middle to be shown "
    "&mdash; because the Adapter does not have a fixed enough self to "
    "demand fixity from a spouse. The Adapter, who has been many versions "
    "of itself in this marriage, cannot exactly insist that the Vault "
    "show its single, settled interior. {name_b}, in turn, does not press "
    "{name_a} into a single, consistent version &mdash; does not ask "
    "<i>which of you is the real one?</i> &mdash; because the Vault "
    "has quietly appreciated the relief of a spouse who does not require "
    "the interior to perform. Neither of you has pressed the other. "
    "You have been very comfortable together. You have also been, "
    "in the deepest sense, largely unknown to each other.",

    "The Apostle Paul wrote to the Corinthians: <i>We have spoken freely "
    "to you, Corinthians; our heart is wide open.</i> (2 Corinthians 6:11) "
    "Paul is describing a pastoral relationship that has cost him something "
    "&mdash; the cost of an open heart, of speech that does not manage "
    "the recipient's response but simply speaks. This is what neither "
    "{name_a} nor {name_b} has yet fully offered the other. "
    "{name_a} has offered fluency &mdash; many versions, each genuine, "
    "none of them quite resting long enough to be held. "
    "{name_b} has offered conclusions &mdash; carefully considered, "
    "organizationally sound, never quite the messy middle from "
    "which the conclusions were drawn. The open heart that Paul is "
    "describing would require something from both of you that the "
    "bargain has made unnecessary. That is why the bargain has to be named.",

    "Here is what the dynamic looks like in the ordinary week. {name_a} "
    "comes home from an interaction &mdash; social, professional, relational "
    "&mdash; having been several versions of themselves in the span of a "
    "few hours. There is, underneath the fluency, a small exhaustion, "
    "and a question that the Adapter always carries but rarely names: "
    "<i>which version am I when I come back here?</i> The Adapter looks "
    "at {name_b} and tries to read which version of themselves will be "
    "received. {name_b}, meanwhile, has been processing something "
    "internally all day &mdash; a concern, a grief, a half-resolved "
    "question &mdash; and has arrived at a presentable conclusion. "
    "The conclusion gets offered. The Adapter, reading the room, "
    "receives it at face value. Neither of them has spoken. "
    "Both of them feel, at some level, that the conversation they "
    "just did not have was the one they needed.",

    "Paul writes in Ephesians 4:15 of <i>speaking the truth in love</i> "
    "&mdash; and notice that the instruction is not to possess the truth, "
    "not to think the truth, but to <i>speak</i> it, in love, to one another. "
    "This applies to both of you in specific ways. {name_a}, speaking the "
    "truth in love means risking a single, un-calibrated voice &mdash; "
    "not the version most likely to be received, but the actual voice of "
    "the person underneath the versions. {name_b}, speaking the truth in "
    "love means risking the unfinished interior &mdash; not the polished "
    "conclusion, but the actual process, with its doubts and half-formed "
    "things, brought to {name_a} before it has been organized into "
    "something safe to present. Both of these require breaking the "
    "bargain. Both of them are the way toward a marriage in which "
    "two people actually know each other.",

    "{name_a} &mdash; the most important question you can ask yourself "
    "when you come home is not <i>which version does this room need?</i> "
    "It is: <i>which version is actually here?</i> {name_b} cannot know "
    "you if you do not know which self you are presenting. And the "
    "Vault, for all its carefulness, is genuinely capable of knowing "
    "a fixed self that stays long enough to be known. What the Vault "
    "cannot do &mdash; what no one can do &mdash; is know someone "
    "who has not decided who they are.",

    "{name_b} &mdash; the most important thing you can do in the "
    "ordinary week is offer {name_a} one unfinished thing. Not the "
    "conclusion. Not the organized file. Something from the middle "
    "&mdash; a question you have not resolved, a feeling you have "
    "not named even to yourself, a grief you have been carrying "
    "without quite knowing why. The Adapter is, of all the mechanisms, "
    "the one most likely to receive an unfinished thing with "
    "genuine presence rather than judgment. That is the gift "
    "{name_a} is in a unique position to give you. But you have "
    "to open the vault slightly, before the Attorney has assembled "
    "the file, for that gift to be received.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be seasons &mdash; not most weeks, "
    "but they will come &mdash; when the bargain breaks down and both of "
    "you are in breakdown at the same time. The Plea is cycling. The "
    "Attorney is unsealing. The room is strange in a way that neither of "
    "you quite has words for, because this kind of breakdown does not "
    "look like most marital conflict from the outside. There is no "
    "shouting. There is no obvious confrontation. There is instead "
    "a peculiar dance in which neither of you can locate the other.",

    "Here is what is happening, named plainly.",

    "{name_a}, when the Plea is cycling in the Adapter, what you are "
    "doing &mdash; even when it does not look like pleading from the "
    "outside &mdash; is moving through versions, searching for the "
    "one that will reach {name_b}. The calm version. The vulnerable "
    "version. The withdrawn version that hopes the withdrawal will "
    "prompt pursuit. The version that apologizes for things you are "
    "not quite sure you did. Each version is a genuine attempt at "
    "connection. But to {name_b}, watching from inside the Vault, "
    "what registers is not <i>my spouse is reaching for me.</i> "
    "What registers is: <i>my spouse is cycling through versions, "
    "and I do not know which one to trust, and I am not sure "
    "the one who is reaching for me now will be the same one "
    "who is here tomorrow.</i>",

    "{name_b}, when the Attorney unseals in the Vault, what you "
    "are doing &mdash; even when it does not look like prosecution "
    "&mdash; is retreating into deeper management. The file you "
    "have been keeping is not brandished publicly. It is there, "
    "behind the eyes, organizing everything. The Vault under "
    "pressure does not open; it closes more completely. "
    "The Ghost emerges &mdash; the one who performs normalcy "
    "while something large moves behind the performance. "
    "To {name_a}, watching from outside, this is disorienting "
    "in a specific way. The Adapter, whose gift is reading rooms, "
    "can read that something is wrong. The Adapter cannot read "
    "<i>what</i> is wrong, because the Vault has locked the file. "
    "And the Adapter, who cannot reach what cannot be read, "
    "cycles through more versions, which confirms {name_b}'s "
    "sense that there is no stable self to trust.",

    "This is the strange dance. The Adapter cannot find which "
    "version will reach the Vault that has gone quiet. "
    "The Vault cannot find which version of the Adapter to trust "
    "with what is inside. Both of you, in this moment, are "
    "alone in your own mechanism. The Psalm names what is "
    "needed before either of you can help the other: "
    "<i>Search me, O God, and know my heart; try me and "
    "know my thoughts. And see if there be any grievous way "
    "in me, and lead me in the way everlasting.</i> "
    "(Psalm 139:23&ndash;24) This is not a verse about "
    "introspection. It is a verse about surrender. It is "
    "the prayer of a person who has stopped trying to manage "
    "their own interior and is asking God to take it up. "
    "Both of you need this prayer before the marriage can "
    "be the container that holds you.",

    "Augustine wrote, in a passage that describes both "
    "of your mechanisms from the inside, that the heart "
    "is <i>more known to God than to itself.</i> "
    "The Adapter does not fully know itself &mdash; "
    "the self has been so long assembled from feedback "
    "that the self below the versions is genuinely unfamiliar. "
    "The Vault does not fully know itself either &mdash; "
    "the interior has been so long managed that even the "
    "Vault's own access to its deepest things is mediated "
    "through the same curatorial instinct that keeps "
    "others at a distance. God knows what both of you "
    "do not. The prayer of Psalm 139 is the prayer of two "
    "people handing that problem to the One who does not "
    "need the interior to be organized before he enters it.",

    "When you are in the dance and you can still see it happening, "
    "do three things. <b>First, one of you names it.</b> Not with "
    "accusation. With the simplest possible honesty: "
    "<i>I think we are doing the thing. I am not sure which version "
    "of me is in the room right now, and I think you have gone "
    "somewhere I cannot reach. Can we stop for twenty minutes?</i> "
    "The Vault will often resist the naming. The Adapter will often "
    "continue cycling for a beat after the naming. That is expected. "
    "Name it anyway.",

    "<b>Second, in the pause, do not strategize. Pray the Psalm.</b> "
    "Each of you, separately, pray Psalm 139:23&ndash;24 by name. "
    "Not eloquently. Not with theological precision. "
    "<i>Search me. Know my heart. Not the version I have been presenting. "
    "The actual one. Lead me toward the person I was made to be "
    "in this marriage.</i> The Adapter needs this prayer because "
    "the version-cycling cannot stop by willpower. The Vault needs "
    "this prayer because the curating cannot stop by willpower either. "
    "Both of you are asking God to do something you cannot do alone.",

    "<b>Third, when you return to each other, each of you speaks "
    "one sentence that is not a management of the other person's "
    "response.</b> {name_a}, your sentence is not the version most "
    "likely to be received. It is the thing that is true right now, "
    "before you have calculated how to present it. "
    "{name_b}, your sentence is not the conclusion. It is something "
    "from the process &mdash; something unfinished, something you have "
    "not organized, something the Attorney has not yet catalogued. "
    "One sentence each. Then stop. Let what was said be enough "
    "for this moment.",
]

COMMITMENTS_INTRO = [
    "What follows are six commitments &mdash; three from {name_a}, three from "
    "{name_b}. They are not vows in the legal sense. They are the small daily "
    "practices that, offered to each other freely and kept with reasonable "
    "consistency, change the temperature of a home over months and years. "
    "Read each one slowly. If one of you cannot make a particular commitment "
    "in good faith yet, do not make it. The goal is not performance. "
    "It is honesty.",
]

A_COMMITMENTS = [
    (
        "I will let you see one consistent self this week.",
        "{name_b}, I commit to showing you, at least once this week, "
        "the version of me that is not calibrated to what I think the "
        "room needs. Not my best version. Not the version most likely "
        "to land well. The actual one &mdash; with whatever I am "
        "carrying that day, before I have decided how to present it. "
        "You deserve a spouse you can know. I am going to practice "
        "being knowable, even when the room seems to ask for something "
        "else.",
    ),
    (
        "I will name the question before I cycle through the versions.",
        "{name_b}, when I feel myself beginning to move through versions "
        "&mdash; searching for the one that will reach you, or the one "
        "that will protect me from being found unacceptable &mdash; "
        "I commit to naming what I am doing before I do it. "
        "One sentence: <i>I am not sure which version of me is in the "
        "room right now, and I am afraid of being found wanting.</i> "
        "I will give you the truth of the moment rather than the "
        "management of it.",
    ),
    (
        "I will receive what you give without instantly calibrating to it.",
        "{name_b}, when you offer me something from your interior "
        "&mdash; even a small thing, even something unfinished &mdash; "
        "I commit to receiving it without immediately reading what "
        "version of me you need in response. I will be still for "
        "a moment. I will let what you gave me be what it is before "
        "I decide what to do with it. You showed me something real. "
        "It deserves something real back, not something calibrated.",
    ),
]

B_COMMITMENTS = [
    (
        "I will trust you with one unfinished thing today.",
        "{name_a}, I commit to bringing you something from the interior "
        "before it has been resolved &mdash; a question I have not "
        "answered, a feeling I have not named, a weight I am still "
        "in the middle of. I cannot predict which version of you "
        "will receive it. I am choosing to bring it anyway, because "
        "the alternative &mdash; waiting until everything is organized "
        "and concluded &mdash; means you will only ever know the "
        "Vault's finished products, and I want you to know more "
        "than that. Even if the unfinished thing is small. Especially "
        "if it is.",
    ),
    (
        "I will let you see me in the middle of something.",
        "{name_a}, I commit to resisting the instinct to disappear "
        "into the interior when I am processing something difficult. "
        "I will not perform normalcy when something large is moving "
        "behind the performance. If I am not ready to name the thing "
        "in full, I will at least say: <i>something is going on in "
        "me and I will tell you when I have more of it.</i> That is "
        "not a finished product. But it is real, and it is more than "
        "the silence.",
    ),
    (
        "I will name what the file says before the Attorney assembles it.",
        "{name_a}, when I notice the Attorney beginning to organize "
        "the record &mdash; when I feel the careful accumulation of "
        "evidence that something between us has been wrong &mdash; "
        "I commit to naming one item from the file in the week it "
        "happened, rather than carrying it until the file is full "
        "enough to present as a case. <i>That thing that happened "
        "on Tuesday landed harder than I showed.</i> That is one "
        "sentence. I can give you one sentence in the week it happens. "
        "That is the commitment.",
    ),
]

PRAYER = [
    "Father,",

    "You set these two next to each other, and you knew exactly what "
    "you were doing. You knew the Adapter would need a spouse who "
    "did not ask for a performance. You knew the Vault would need "
    "a spouse who could sense the depth without requiring it to "
    "announce itself. You knew the bargain they would make &mdash; "
    "the quiet arrangement, the comfortable distance &mdash; and "
    "you knew it would not finally be enough. You knew all of this "
    "before either of them said yes.",

    "Teach them the grammar of each other. Teach {name_a} to be "
    "present as one person rather than as whoever the room requires "
    "&mdash; to offer {name_b} a self that stays long enough to be "
    "known, to speak the truth in love even when the truth has not "
    "been calibrated to the expected response. Teach {name_b} to "
    "trust {name_a} with the unfinished things &mdash; to open the "
    "vault before the conclusion is ready, to let the messy middle "
    "be witnessed rather than resolved before it can be shown.",

    "When the Plea cycles in {name_a} &mdash; when the versions multiply "
    "and the search for the one that will reach becomes desperate "
    "&mdash; remind {name_a} that there is a name spoken over them "
    "that is not assembled from the rooms they have read: chosen in "
    "Christ before the foundation of the world, named before any "
    "version was required. When the Vault closes in {name_b} &mdash; "
    "when the file thickens and the performance of normalcy begins "
    "&mdash; remind {name_b} that the One who sees what is inside "
    "has already spoken the verdict: covered, clean, beloved. "
    "There is no condemnation for those who are in Christ Jesus.",

    "Search them, O God, as the Psalm asks &mdash; each of them, "
    "in the privacy of their own souls, before they come back to "
    "each other. Know their hearts, not the versions they have "
    "been presenting, not the conclusions they have been curating, "
    "but the actual interior that is more known to you than it is "
    "to either of them. Lead them in the way everlasting, which "
    "runs through this marriage, through the small daily practice "
    "of speaking freely and hearing what is spoken, of open hearts "
    "and wide doors.",

    "Make their home a room in which {name_a} can rest from "
    "reading rooms, and {name_b} can rest from managing what "
    "is shown. Make their table a place where unfinished things "
    "are welcome and one consistent self shows up to receive them. "
    "Make their marriage, in time, the evidence that two people "
    "who share a question &mdash; <i>am I acceptable?</i> &mdash; "
    "found, in each other, a partial answer, and found in you "
    "the whole one.",

    "In the name of the One whose heart was wide open, and whose "
    "love did not wait for us to be organized before it came for us.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. "
    "The pages that follow are different. They are meant to be spoken "
    "<i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken "
    "slowly, somewhere quiet, with no children in the room and no "
    "phones on the table. There are six rounds, and they build on "
    "each other. Resist the temptation to skip ahead. Start at "
    "Round One even if it feels too light; the lightness is the point.",

    "Some of the questions are playful. Some are direct. A few are "
    "the kind that, when answered honestly, will sit with you for "
    "a week. None of them are trivia. All of them are an invitation.",

    "<b>How to use it.</b> One of you reads a question aloud. "
    "The one who did not read answers first, in full, without "
    "interruption. Then the reader answers the same question. "
    "Then you move on. You do not have to finish all six rounds "
    "in one night &mdash; two or three rounds, taken seriously, "
    "is often better than racing through all of them. "
    "Save the rest for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. "
    "You may not love everything you hear. Stay with it. "
    "The point of this is not to grade each other's answers. "
    "The point is to be known, and to do the slow work of knowing.",
]

ROUND_1 = [
    (
        "hypothetical",
        "If our marriage were a house, what kind of house would it be "
        "&mdash; what would it look like from the outside, and what would "
        "someone find if they were let into the room no one usually sees?",
        "Let the metaphor do the work plain language sometimes cannot. "
        "Answer with the first image that comes to mind.",
    ),
    (
        "observation",
        "What is something I did for you this week that you noticed "
        "and didn't mention?",
        "Not a complaint. A small noticing. The fact that you noticed "
        "at all is already something.",
    ),
    (
        "playful",
        "If you had to choose a single song that describes what our "
        "marriage feels like right now &mdash; not what you wish it were, "
        "but what it actually feels like &mdash; what would it be?",
        "Yes, really. First answer wins. Explain it briefly.",
    ),
]

ROUND_2 = [
    (
        "fill-in-blank",
        "I don't think I tell you this enough &mdash; I am amazed at the "
        "way God made you so _______. Your _______ is a gift to this "
        "marriage, and I want to get better at receiving it.",
        "Two blanks. Be specific. 'Patient' is too easy; "
        "'able to sense what I need before I have named it myself' is closer.",
    ),
    (
        "observation",
        "What is one thing you have watched me do this year that "
        "you wish more people could see?",
        "Most of us only see ourselves doing our most public things. "
        "Tell your spouse about the private ones.",
    ),
    (
        "one-word",
        "If you had to choose one word to describe what it feels like "
        "when you are completely certain that I am actually present with you "
        "&mdash; not performing, not managing, but actually here &mdash; "
        "what word would it be?",
        "One word, said out loud. Then explain it, briefly.",
    ),
]

ROUND_3 = [
    (
        "forward-looking",
        "Five years from now, when we look back on this season, "
        "what do you hope we will say we did well together?",
        "Not what you wish you had done. What you want, when you look back, "
        "to be able to say you actually did.",
    ),
    (
        "theological",
        "Where, in the last month, have you seen God specifically "
        "at work in me &mdash; not the version I present to the world, "
        "but something real that you caught a glimpse of?",
        "Not where you want him to work. Where you have already seen it. Name it.",
    ),
    (
        "shared-identity",
        "Finish this sentence three times: "
        "'We are the kind of couple who _______.' "
        "Give one playful answer, one true answer, and one aspirational answer.",
        "The 'we' is the point. Let all three answers be real.",
    ),
]

ROUND_4 = [
    (
        "strength",
        "What is something I bring to our shared life that you would "
        "have to learn to do for yourself if I were not here?",
        "Hard to ask. Important to hear. Stay with the answer.",
    ),
    (
        "fill-in-blank",
        "One of the gifts of being married to you is that I get to "
        "be _______ in ways I never would have been on my own.",
        "A version of yourself that only exists because this marriage exists. "
        "Name it as specifically as you can.",
    ),
    (
        "observation",
        "Name one moment in our story where you knew, without doubt, "
        "that we had built something together that neither of us "
        "could have built alone.",
        "Tell the story in full. The remembering is part of the strengthening.",
    ),
]

ROUND_5 = [
    (
        "hard",
        "{name_a}, when have you felt most genuinely known by {name_b} "
        "&mdash; not responded to, not accommodated, but actually known? "
        "What was different about that moment?",
        "Take your time. The answer matters more than the pace.",
    ),
    (
        "hard",
        "{name_b}, is there something you have been carrying in private "
        "that you have not yet brought to {name_a} &mdash; not the "
        "conclusion, but the actual thing still in the middle of being "
        "processed? Can you name it, even partially, right now?",
        "You do not have to have it organized. That is the point. "
        "Unfinished is allowed.",
    ),
    (
        "profile-aware",
        "The walkthrough describes an unspoken bargain between you: "
        "the Adapter doesn't press the Vault to open, and the Vault "
        "doesn't press the Adapter to be one consistent version. "
        "Has that description felt true? Where have you felt the cost "
        "of the bargain most clearly?",
        "One answer each. Heard without defending. This is not an accusation.",
    ),
    (
        "profile-aware",
        "When my Plea cycles or my versions multiply, what is one thing "
        "you wish I would say or do differently &mdash; not later, "
        "but in that moment? And when the vault closes and the performance "
        "begins, what is one thing that would help?",
        "You both know what these patterns are now. Ask each other for "
        "what would actually help.",
    ),
]

ROUND_6 = [
    (
        "blessing",
        "Place your hand on your spouse's hand. Say their name. "
        "Then say: 'You are not a problem to be solved. "
        "You are a gift I get to receive again tomorrow.' "
        "Say it slowly. Let them say it back.",
        "You may feel silly. That is part of why it works. Do it anyway.",
    ),
    (
        "prayer",
        "Pray for each other &mdash; not silently, not generally, "
        "but out loud and by name. One sentence is enough. "
        "Pray for the thing they told you in Round Five.",
        "The closing of the date. Do not skip.",
    ),
]


def _render(text, name_a, name_b):
    return text.format(name_a=name_a, name_b=name_b)


def build(sub_a, sub_b) -> bytes:
    """Generate the Adapter+Vault couples walkthrough PDF.

    sub_a: the submission of the Adapter spouse
    sub_b: the submission of the Vault spouse
    """
    ensure_fonts()
    S = make_styles()

    name_a = _first_name(sub_a, "Adapter")
    name_b = _first_name(sub_b, "Vault")

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
                "Adapter &middot; Plea / Quiet Exit<br/>"
                "<font size=9 color='#6b6862'>Control / Shame &middot; Am I free? / Am I acceptable?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_b.upper()}</b></font><br/>"
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
        "<i>\u201cWe have spoken freely to you, Corinthians;<br/>"
        "our heart is wide open.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "2 Corinthians 6:11",
        ParagraphStyle("cqa", fontName="Inter", fontSize=9, leading=14,
                       textColor=MUTED, alignment=TA_CENTER, spaceBefore=4)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1 ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "The quiet distance.",
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
            _profile_card(S, name_a, ACCENT,
                          "Control / Shame", "Am I free? / Am I acceptable?",
                          "The Adapter", "The Plea / Quiet Exit"),
            "",
            _profile_card(S, name_b, ACCENT_HER,
                          "Shame", "Am I acceptable?",
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

    # ── SECTION 3 ──
    section_header(story, S, "SECTION THREE  \u00b7  THE ADAPTER'S GIFT",
                   f"What {name_a} gives {name_b}.",
                   "The warmth of being genuinely reached for.")
    for p in GIFT_TO_A:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4 ──
    section_header(story, S, "SECTION FOUR  \u00b7  THE VAULT'S GIFT",
                   f"What {name_b} gives {name_a}.",
                   "A room that does not ask for a performance.")
    for p in GIFT_TO_B:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5 ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "The unspoken bargain.",
                   "The small repeating rock, named.")
    for p in COLLISION[:4]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "Speaking truth in love.",
                   "What breaking the bargain looks like, for each of you.")
    for p in COLLISION[4:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6 ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When the Plea cycles and the Vault closes.",
                   "The strange dance, named.")
    for p in BOTH_BREAK[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do while you can still see it.",
                   "Three practices for the dance, in order.")
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
    story.append(Paragraph(f"FROM {name_a.upper()}, TO {name_b.upper()}", S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for cname, cbody in A_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(cname, S["H3"]),
            Paragraph(R(cbody), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_b}, to {name_a}.",
                   "Three commitments, in their voice, for the other to receive.")
    story.append(Paragraph(f"FROM {name_b.upper()}, TO {name_a.upper()}", S["CommitLabelHer"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT_HER,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for cname, cbody in B_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(cname, S["H3Her"]),
            Paragraph(R(cbody), S["CommitBody"]),
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


# ── STANDALONE TEST ──────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    class FakeSub:
        def __init__(self, name, mech, breakdown, trigger, question):
            self.name = name
            self.primary_mechanism = mech
            self.primary_breakdown = breakdown
            self.primary_trigger = trigger
            self.core_question = question

    sub_a = FakeSub("Sophia", "ADPT", "PLEA", "CTRL", "FREE")
    sub_b = FakeSub("Daniel", "VAULT", "ATTY", "SHM", "ACC")

    pdf_bytes = build(sub_a, sub_b)
    out_path = os.path.join(os.path.dirname(__file__), "adapter_vault_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    import io
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        snippet = ""
        for page in reader.pages:
            txt = page.extract_text() or ""
            if "ADAPTER" in txt and "GIFT" in txt.upper():
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
        snippet = str(e)

    print(f"DONE: adapter_vault.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
