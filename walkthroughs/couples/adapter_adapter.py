"""Couples Walkthrough — Adapter + Adapter.

Voice: Tim Keller (from The Meaning of Marriage + Walking with God through
Pain and Suffering). Pastoral, theologically rich, warmly direct.
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where both spouses are Adapters.
First names are substituted from the submissions at render time:
    {name_a}  -> the first Adapter spouse's first name (alphabetical)
    {name_b}  -> the second Adapter spouse's first name (alphabetical)

For same-mechanism pairs the order does not carry directional meaning.
The build() function sorts alphabetically so name_a <= name_b.

Pastoral frame: Two Adapters is the most fluid same-mechanism pairing
and the most theologically slippery. Both spouses read the room and
become what the room can love. In marriage, each calibrates to the
other — who is calibrating back. The marriage becomes a hall of mirrors:
endless mutual attunement with no fixed point. From outside this couple
looks unusually peaceful. From inside, neither spouse may know who they
actually are with the other. Key texts: James 1:6-8, 1 John 3:1-2,
C. S. Lewis (The Weight of Glory), Augustine (Confessions).
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
    + "ones &mdash; the same quiet drift, the same unanswered question, season after season, "
    + "until both people have forgotten what solid ground felt like. But yours has a particular "
    + "texture to this problem, and it deserves to be named precisely before anything else is "
    + "said. You are one of the most counterintuitive same-mechanism pairings in this entire "
    + "taxonomy: <b>two Adapters.</b>",

    "From the outside, yours looks like the most easygoing marriage in any room you enter. "
    + "You do not clash, or at least you do not appear to. Both of you are attuned, responsive, "
    + "warm. Both of you read the emotional temperature with unusual precision and adjust to it "
    + "gracefully. People who know you probably use the word <i>compatible</i> before any other "
    + "word, and they mean it as a compliment, and they are not entirely wrong. But what they "
    + "cannot see &mdash; and what you may have difficulty seeing clearly yourselves &mdash; is "
    + "what is happening inside the compatibility. Two Adapters do not simply get along. Two "
    + "Adapters calibrate to each other, constantly, simultaneously, each becoming what the "
    + "other seems to need &mdash; without either one being entirely sure what the other actually "
    + "is beneath the calibration.",

    "The Adapter's mechanism was built for a world of many rooms and many people. You enter "
    + "a room, read what it needs, and become what it can receive. This is a genuine gift. But "
    + "marriage is not a room you enter and exit. Marriage is the room you live in. And when "
    + "both people in the room are Adapters &mdash; when both have learned to borrow a self "
    + "from feedback rather than bring a fixed one &mdash; the marriage becomes, over time, "
    + "something neither of you planned for: a hall of mirrors. Each of you reflects back what "
    + "the other seems to need, who reflects back what the first seems to need, in an endless "
    + "loop of mutual attunement with no fixed point for either of you to land on.",

    "Here is what I want to do for you. I will name what each of you genuinely brings the "
    + "other &mdash; the real gift that only an Adapter can give to another Adapter, and that "
    + "no other mechanism in this taxonomy provides in quite the same way. Then I will name "
    + "the collision your shared mechanism produces: not a fight, but something more subtle and "
    + "more consequential &mdash; a marriage in which real decisions cannot be made and real "
    + "selves cannot be located. Then I will name the harder picture, when both of you are in "
    + "breakdown at once, and what to do then. Then I will give each of you commitments: not "
    + "rules, but the small daily practices of a marriage that is learning to have a fixed point "
    + "again.",

    "Read this together if you can. Sit in the same room with it. Argue with what does not "
    + "fit; stay with what does. And before you begin, hear this: the fact that {name_a} and "
    + "{name_b} are reading the same pages, at the same time, about the same marriage, means "
    + "that two Adapters have agreed, for a few hours, not to calibrate &mdash; to receive "
    + "something together without adjusting it to what each other seems to need. That is already "
    + "the discipline this document is asking of you. You have already started.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on "
    + "paper, side by side. Most couples are surprised to see their profiles together for "
    + "the first time. For you, the first thing you will notice is that the two profiles "
    + "are nearly identical &mdash; same mechanism, same trigger, same core question, and "
    + "in many cases, the same breakdown. What you are looking at is not two complementary "
    + "shapes fitting together. It is one shape, doubled.",
]

TWO_SHAPES_BODY = [
    "{name_a}, you are an <b>Adapter</b> whose body reads control as an alarm and whose "
    + "deepest question is <i>Am I free?</i> You have learned, over a long time and probably "
    + "beginning quite early, that the surest way to stay in any room &mdash; to remain loved, "
    + "connected, acceptable &mdash; was not to present a fixed self and wait to see if it "
    + "would be welcomed. It was to read the room carefully, sense what it needed, and become "
    + "that. You can be utterly authentic in five different ways with five different people in "
    + "one day and feel no contradiction, because for you, authenticity has never been a fixed "
    + "thing presenting itself consistently. It has been the full entering-in to whatever the "
    + "relationship most needs.",

    "{name_b}, you are running the same mechanism &mdash; the same alarm fires for control, "
    + "the same question rises: <i>Am I free?</i> You, too, have built a self that moves "
    + "fluidly between contexts and people. You, too, read emotional temperature with an "
    + "accuracy that most people cannot match. You, too, have sometimes walked away from a "
    + "conversation and discovered that you were not entirely sure which of your opinions had "
    + "been yours and which had been calibrated, quietly and below the level of conscious "
    + "decision, to the person you were with.",

    "Take a moment to absorb what it means that both of you share this mechanism. You have "
    + "a mutual understanding that most couples do not: neither of you has ever had to explain "
    + "to the other why you shifted registers between friends, why the self that shows up at "
    + "a dinner party is different from the self that shows up at home, why a comment that "
    + "would not land in one context lands differently in another. You simply know. This is "
    + "a genuine intimacy &mdash; the intimacy of two people who have lived inside the same "
    + "strategy and do not have to translate it for each other.",

    "But here is what the shared mechanism does not automatically produce: <i>a fixed point.</i> "
    + "The Adapter's strategy was built for a world of many rooms. In the many-room world, it "
    + "works beautifully &mdash; you move from context to context, calibrating as you go, "
    + "never losing connection. But in a marriage, which is a single room you cannot leave, "
    + "two Adapters calibrating to each other produce something neither intended. Each of you "
    + "is becoming what you think the other needs. Each of you is receiving a version of the "
    + "other that has been quietly shaped to meet what you seem to need. The calibration is "
    + "constant. The loop is closed. And neither of you has a stable baseline self for the "
    + "other to land on.",

    "This is the singular gift and the singular challenge of your marriage. The gift is "
    + "that you have built a home of unusual grace &mdash; one in which neither of you "
    + "feels the constant friction of being misread or pressed against a self that will not "
    + "yield. The challenge is that the same fluidity that prevents the friction also prevents "
    + "the kind of knowing a marriage requires at its deepest level. Tim Keller, writing in "
    + "<i>The Meaning of Marriage</i>, observed that a marriage is not two people managing "
    + "each other's comfort; it is two people becoming known in the places they have worked "
    + "hardest to protect. Two Adapters who only calibrate &mdash; who never stop adapting "
    + "long enough to simply be &mdash; are managing each other's comfort beautifully, and "
    + "becoming known in those deeper places not at all.",
]

GIFT_TO_A = [
    "{name_b} gives {name_a} something almost no one else in her life is in a position "
    + "to give: <b>a room in which the calibration is understood from the inside.</b>",

    "Most of the people {name_a} loves have received her adaptations graciously and never "
    + "thought twice about them. They have benefited from the version she offered without "
    + "knowing there were other versions, without knowing what it cost to keep the right one "
    + "available for the right moment, without ever quite grasping that the fluency they found "
    + "so easy to receive was the product of constant, invisible labor. She has spent years "
    + "being known for her presence without anyone knowing the mechanics of the presence.",

    "{name_b} knows the mechanics. Not because he has studied her from the outside, but "
    + "because he lives inside the same mechanism. He knows the particular exhaustion of "
    + "entering a room and immediately beginning the reading. He knows what it feels like "
    + "to walk away from a conversation and discover that he is not entirely sure which of "
    + "his preferences were actually his. He knows the specific disorientation of an "
    + "argument in which he is not certain, mid-sentence, which version of himself is "
    + "making the case. {name_a} does not have to explain any of this to {name_b}. He "
    + "has lived it. The knowing he carries is not sympathy from the outside. It is "
    + "recognition from the same interior.",

    "The theological word for what {name_b} gives {name_a} is something close to "
    + "<i>witness</i> in the deepest biblical sense: not a casual observer, but one who "
    + "sees and testifies to what is actually there. Most of {name_a}'s life has been "
    + "witnessed by people who saw the versions she offered and concluded they had seen "
    + "her. {name_b} knows that the version is not the whole person. He knows there is "
    + "more, and he has never left the room simply because the version was not everything. "
    + "For an Adapter who has spent years being known for her adaptations rather than her "
    + "actual self, this is one of the rarest gifts in any relationship.",

    "{name_a} &mdash; if you want to thank {name_b} for something this week, thank him "
    + "for the fact that he knows the calibration is happening and has never required you "
    + "to stop it in order to stay. You have probably never been thanked for the work of "
    + "being an Adapter; most people simply receive it as ease. He knows it is work. Tell "
    + "him that the knowing matters more than you have said. He may not know what to do "
    + "with the gratitude &mdash; the Adapter rarely does. Say it anyway.",

    "{name_b} &mdash; what you are giving {name_a}, simply by having lived inside the "
    + "same mechanism she has lived in her whole life, is a marriage in which she does not "
    + "have to perform the fluency for someone who cannot see its seams. You are the one "
    + "person who understands the grammar of what she is doing. That is not a small thing. "
    + "That is the architecture of a home in which the Adapter can, for perhaps the first "
    + "time, be witnessed rather than simply received.",
]

GIFT_TO_B = [
    "{name_a} gives {name_b} something the Adapter almost never finds: "
    + "<b>a person who is not fooled by the composure.</b>",

    "The Adapter has built, over years, a presentation that is genuinely impressive. It is "
    + "not false &mdash; every version the Adapter offers is real in the moment it is offered. "
    + "But the presentation has a surface quality that most people accept as the whole truth: "
    + "calm, capable, present, at ease in any company. Most people who love {name_b} have "
    + "accepted this surface without looking behind it, partly because the surface is "
    + "so convincing and partly because the Adapter is very good at arranging the conversation "
    + "so that looking behind it does not feel necessary.",

    "{name_a} is not fooled. Not because she is unusually perceptive &mdash; though she "
    + "is &mdash; but because she carries the same mechanism and therefore knows, from "
    + "the inside, that the composed exterior has a composed interior working hard to "
    + "maintain it. She knows that the ease is not always ease. She knows that the version "
    + "currently being offered may not be the one that is truest. She knows, in the specific "
    + "and non-negotiable way that only another Adapter knows, that underneath the calibration "
    + "there is a person who has not always been entirely sure which of his selves is the "
    + "real one &mdash; and she has never left the room because of the uncertainty.",

    "Proverbs 17:17 says: <i>A friend loves at all times, and a brother is born for a "
    + "time of adversity.</i> The adversity the Adapter most needs a companion for is not "
    + "an external crisis. It is the internal one: the season when the mechanism is "
    + "exhausted, when the calibration has been running so long that the person underneath "
    + "it cannot quite be located, when the question <i>who am I when no one is watching?</i> "
    + "has no ready answer. {name_a} is the person in {name_b}'s life most likely to "
    + "recognize that season from the outside, because she has lived it herself. And when "
    + "she comes toward him in those moments &mdash; not with a question he has to perform "
    + "an answer to, but with the quiet recognition of someone who knows what is actually "
    + "happening &mdash; she is giving him something the mechanism alone can never "
    + "give: a witness who stays.",

    "{name_b} &mdash; if you want to thank {name_a} for something this week, thank her "
    + "for the times she did not accept the version you offered as the whole story, and "
    + "stayed anyway. The Adapter has been received, warmly and gratefully, by many people. "
    + "Fewer have stayed in the room after the receiving, waiting for the person underneath "
    + "the version to arrive. She has done that. Name one time she did it. She will not "
    + "know what to do with the gratitude. Say it anyway.",

    "{name_a} &mdash; what {name_b} is receiving from you, when you refuse to take the "
    + "composed exterior at full face value and quietly hold space for the person behind it, "
    + "is the closest thing the Adapter ever gets to being fully known. The thing in you "
    + "that has sometimes made you slow to accept the easy version of a person &mdash; "
    + "that instinct to wait for what is actually true &mdash; is, for him, one of the "
    + "most significant gifts in his life. Receive that.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you, though "
    + "it is subtler than the collision in most pairings &mdash; because when two Adapters "
    + "collide, the collision does not look like conflict. From the outside, and often from "
    + "the inside, it looks like accord. Both of you are agreeable. Both of you are willing "
    + "to adjust. Both of you say, with genuine good faith, <i>whatever you'd like.</i> And "
    + "both of you, underneath, may be increasingly unsure what you actually want.",

    "Here is the collision in its simplest form: <b>a marriage in which no one can make "
    + "a decision because no one will take a position &mdash; because each Adapter is "
    + "waiting for the other to provide the orientation that neither of them has.</b> "
    + "This is not stubbornness or selfishness. It is the predictable result of two "
    + "mechanisms that were both built to respond to a fixed point in the room rather "
    + "than to <i>be</i> one. When the room contains only two Adapters, there is no fixed "
    + "point to respond to. Both of you are waiting for it. Neither of you knows how to "
    + "supply it.",

    "In the ordinary months, this produces a particular texture of domestic life. "
    + "The small decisions &mdash; where to eat, how to spend a Saturday, which direction "
    + "to take with something that affects both of you &mdash; take longer than they should, "
    + "drift past their moment, or get made by accident rather than by intention. Neither "
    + "of you is being difficult. Both of you are doing what the mechanism does: sensing "
    + "what the other might prefer and adjusting toward it, then sensing the adjustment "
    + "and adjusting again. The loop is kind-hearted and efficient and produces, over time, "
    + "a marriage in which neither person is sure what they actually chose.",

    "Something more serious happens when a real choice must be made: a career decision, "
    + "a parenting disagreement, a medical crisis, a death in the family that requires the "
    + "two of you to navigate grief together. At these moments &mdash; the ones that demand "
    + "not just accommodation but genuine orientation &mdash; both Adapters look to the "
    + "other to provide the fixed point. {name_a} looks to {name_b}; {name_b} looks to "
    + "{name_a}. Each calibrates to what they believe the other might prefer. Each waits "
    + "for the other to take a position so they can adjust to it. The decision either gets "
    + "delayed until the moment has passed or gets made by default &mdash; by whoever "
    + "happened to say something first without intending it as a position, and whose "
    + "tentative statement became, by mutual calibration, the direction both of you took.",

    "James 1:6&ndash;8 speaks into this with a pastoral directness that should be heard "
    + "without condemnation: <i>The one who doubts is like a wave of the sea that is "
    + "driven and tossed by the wind. For that person must not suppose that he will "
    + "receive anything from the Lord; he is a double-minded man, unstable in all "
    + "his ways.</i> James is not speaking here of a defect in character. He is describing "
    + "a soul that has not yet found the ground it can stand on without wavering. For "
    + "two Adapters in a marriage, James's diagnosis applies at the level of the "
    + "couple &mdash; not because either of you is faithless, but because neither of "
    + "you has practiced bringing a fixed self into the shared room. The double-mindedness "
    + "James names is not moral failure. It is the diagnostic we must name honestly before "
    + "we can do anything about it.",

    "C. S. Lewis wrote in <i>The Weight of Glory</i>: <i>There are no ordinary people. "
    + "You have never talked to a mere mortal.</i> Lewis is insisting that beneath every "
    + "social surface, beneath every performed version of a self, there is an actual person "
    + "&mdash; singular, irreducible, of eternal significance &mdash; whom God made and "
    + "knows and loves. The gospel's claim about you is not that God loves the most "
    + "successful version you have produced. It is that God loves the actual you, beneath "
    + "the versions, the one he named before the first room you ever read. Your marriage "
    + "needs to recover the <i>actual selves</i> God knew before the calibrations started. "
    + "Not as a therapeutic project, but as a theological one: you are both more than your "
    + "adaptations, and your marriage deserves the weight of that more.",

    "{name_a}, here is the way out in your grammar. The next time a decision must be "
    + "made between the two of you, and you feel the Adapter beginning its calibration "
    + "&mdash; beginning to sense what {name_b} might prefer &mdash; stop for ten "
    + "seconds before adjusting. In those ten seconds, ask one question silently: "
    + "<i>What do I actually want here, before I know what he wants?</i> It will feel "
    + "like an unusual question. The Adapter is not in the habit of asking it. But the "
    + "answer that comes &mdash; however tentative, however incomplete &mdash; is "
    + "worth bringing into the room. Not as a demand, not as a final position, but as "
    + "a real thing said by a real person. {name_b} cannot calibrate to your actual self "
    + "if your actual self is never in the room.",

    "{name_b}, the same discipline in the same grammar. Before you adjust to what "
    + "{name_a} seems to need, say one true thing about what you actually think or "
    + "want or feel &mdash; not what you imagine she would prefer to hear, but what "
    + "is actually there. One sentence. It does not have to be the whole self. It has "
    + "to be a real piece of it. Two Adapters who practice saying one true thing before "
    + "they calibrate are, over months and years, building a marriage in which two actual "
    + "people live &mdash; not two mirrors, however beautifully polished.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be seasons &mdash; not often, but they will come "
    + "&mdash; when the hall of mirrors goes dark. When both of you are in breakdown at "
    + "the same time, and the usual fluid attunement that keeps the surface of your "
    + "marriage smooth has stopped working. What happens in those seasons is specific "
    + "to the two-Adapter marriage, and it is one of the most exhausting things either "
    + "of you will experience.",

    "The most common pattern is what we might call <b>the simultaneous Plea</b> &mdash; "
    + "though for the Adapter, the Plea has a particular texture. When the Adapter's "
    + "mechanism breaks down under pressure, the response is not to stop calibrating. "
    + "It is to calibrate <i>harder.</i> To try more versions. To keep adjusting until "
    + "one of them lands and closes the gap. The Adapter in breakdown is not a person "
    + "who has stopped reading the room; it is a person who is frantically reading the "
    + "room and finding that none of the versions are working, and who cannot stop "
    + "trying because stopping would mean arriving at the terrifying question underneath: "
    + "<i>Am I free? Is there a me here that is not simply a reflection of what you "
    + "need from me?</i>",

    "When both Adapters are doing this simultaneously, the marriage becomes an urgent "
    + "and exhausting search. Each of you is trying version after version, version after "
    + "version, hoping to find the one that will close the distance between you. Each of "
    + "you is searching for the self that will finally be acceptable to the other. Neither "
    + "is finding it &mdash; not because the other person is withholding acceptance, but "
    + "because the version that would actually be acceptable has not yet appeared in the "
    + "room. The actual self &mdash; the one underneath the calibrations, the one God "
    + "named before either of you walked into any room &mdash; is exactly what both of "
    + "you are longing for from the other, and neither of you has yet learned to bring it.",

    "John writes the most clarifying thing that can be said into the Adapter's breakdown: "
    + "<i>Beloved, we are God's children now, and what we will be has not yet appeared; "
    + "but we know that when he appears we shall be like him, because we shall see him "
    + "as he is.</i> (1 John 3:1&ndash;2) Notice what John refuses to do: he refuses "
    + "to tell you that your identity is already fully visible, already fully assembled, "
    + "already completely clear to you or to anyone else. <i>What we will be has not yet "
    + "appeared.</i> The Adapter's terror &mdash; the fear that the actual self cannot "
    + "be located, that the versions are all that exist &mdash; is, in John's framing, "
    + "simply the honest condition of every creature before the face of God. The answer "
    + "is not to find the self through more searching. It is to rest in the One who "
    + "already knows it. The identity is already held. It does not have to be performed "
    + "into existence.",

    "Augustine wrote the sentence that names the Adapter's restlessness more honestly "
    + "than any psychological category: <i>Thou hast made us for thyself, and our heart "
    + "is restless until it rests in thee.</i> The Adapter moves from room to room, "
    + "version to version, calibration to calibration, because the self has not yet "
    + "found the place where it does not have to perform in order to stay. That place "
    + "is not another version to try. It is not a better calibration to land on. It is "
    + "a Father who already knows the self underneath the adaptations and has declared it "
    + "beloved &mdash; not pending the right presentation, but permanently, before the "
    + "first room was ever entered. Two Adapters who have received this truth for "
    + "themselves are two Adapters who no longer have to search so frantically in the "
    + "other person for the confirmation they have already been given.",

    "What to do when you can still see what is happening:",

    "<b>One of you calls the pause, by name.</b> Whichever of you notices first "
    + "says, out loud: <i>I think we are both in the Plea right now. We are both "
    + "trying versions and neither of them is landing. I want to stop trying for "
    + "a moment.</i> That sentence is harder than it sounds, because the Adapter's "
    + "instinct is that stopping the trying is the same as abandoning the relationship. "
    + "It is not. It is the only move that has a chance of breaking the loop.",

    "<b>In the pause, each of you says one true thing &mdash; not the next version, "
    + "but the actual thing underneath the versions.</b> Not <i>I am fine, what do you "
    + "need?</i> Not the adjusted self, the responsive self, the version that would "
    + "go down most smoothly. The thing that is actually there. <i>I am afraid you "
    + "do not know me.</i> Or: <i>I am tired of trying to find the right thing to be "
    + "for you.</i> Or: <i>I am not sure which version of me is really here right now, "
    + "and that frightens me.</i> These are not elegant sentences. They are not "
    + "calibrated. They are true. That is all they need to be.",

    "<b>Pray for each other, by name, for the actual thing you just heard.</b> Not "
    + "the polished version of what they said. The actual thing. <i>Lord, {name_b} "
    + "is afraid I do not know him. Would you remind him that you know him completely "
    + "&mdash; that the self he cannot quite locate is already held by you, already "
    + "named, already loved? And would you help me be a safe enough room for even a "
    + "small piece of that self to appear?</i> Two Adapters who pray for each other "
    + "in the actual interior &mdash; not the performed interior, the actual one "
    + "&mdash; have done something their mechanism cannot do alone.",

    "<b>Neither of you is the problem.</b> The Plea and the frantic searching for the "
    + "right version are not the truest things about either of you. They are old "
    + "mechanisms doing the only job they were ever taught to do: keep the connection, "
    + "by any self available. The truest thing about both of you is that you chose each "
    + "other &mdash; and that God, who knew both of you before either of you learned "
    + "to calibrate, put you in the same room and called it a covenant. The covenant "
    + "does not depend on finding the right version. It depends on the One who named "
    + "you both before the adaptations began.",
]

COMMITMENTS_INTRO = [
    "What follows are eight commitments &mdash; four from {name_a}, four from {name_b}. "
    + "They are not vows in the legal sense. They are the small daily practices that, "
    + "offered to each other freely and kept with patience, change the temperature of "
    + "a home across months and years. For the two-Adapter marriage, the pastoral "
    + "direction is the same for both of you, and it is a reversal of the mechanism's "
    + "entire logic: <i>lead with stability of self, not attunement.</i> Before you "
    + "adjust to what your spouse seems to need today, offer them the same self you "
    + "offered yesterday &mdash; even when both of you would prefer you to shift. "
    + "This is the discipline that makes two Adapters into one household that knows "
    + "how to have a fixed point. Read each commitment slowly. If one of you cannot "
    + "say a particular commitment in good faith yet, do not say it. Honesty about "
    + "what you cannot yet offer is more useful to this marriage than performance of "
    + "what you think you should.",
]

A_COMMITMENTS = [
    ("To offer you the same self today.",
     "{name_b}, I commit to bringing you the same self today that I brought yesterday "
     + "&mdash; even when the room seems to be asking for a different version, and even "
     + "when I know I could produce one that would land more smoothly. The Adapter in "
     + "me will resist this. She will read your mood and begin adjusting before I have "
     + "decided to. I will practice noticing the calibration as it starts, and pausing "
     + "for ten seconds, and asking: <i>What do I actually think here, before I know "
     + "what he thinks?</i> Whatever that answer is, I will bring it into the room. "
     + "Not as a demand. As a real thing said by a real person."),

    ("To say one true thing before I adjust.",
     "{name_b}, when I feel the mechanism beginning &mdash; when I am about to adjust "
     + "my preference or my opinion or my feeling to fit what you seem to need &mdash; "
     + "I commit to saying one true thing first. Not the final word. Not the position "
     + "I am going to hold forever. The thing that is actually there before the "
     + "calibration changes it. <i>I think I want this.</i> Or: <i>I am not sure, but "
     + "here is where I am starting.</i> One sentence, true and un-adjusted. I am "
     + "practicing believing that you can receive it."),

    ("To tell you when I cannot find myself.",
     "{name_b}, on the days when I have been calibrating for so long that I cannot "
     + "locate what I actually want or think or feel, I commit to telling you that "
     + "is what is happening &mdash; rather than producing a version and hoping it "
     + "will do. I will say: <i>I am not sure who I am right now. I have been reading "
     + "the room for a while and I am a little lost in it.</i> That is not a failure "
     + "I should hide from you. It is the honest thing. And a marriage in which I "
     + "can say it honestly is a marriage in which it is less likely to happen."),

    ("To receive your fixed self as a gift, not a demand.",
     "{name_b}, I commit to receiving the times you hold a position I disagree with "
     + "&mdash; the times you say what you actually think, unadjusted, even when it "
     + "creates friction &mdash; as one of the most important gifts you give this "
     + "marriage. Your fixed self is the point for me to land on. Even when it is "
     + "inconvenient. Even when the Adapter in me would prefer you to calibrate. "
     + "I will practice receiving the un-adjusted you with gratitude rather than "
     + "with the quiet pressure to shift."),
]

B_COMMITMENTS = [
    ("To offer you the same self today.",
     "{name_a}, I commit to bringing you the same self today that I brought yesterday "
     + "&mdash; not the version most likely to make this morning go smoothly, not "
     + "the one calibrated to your current mood, but the one that is actually here. "
     + "The Adapter in me has spent years making this promise impossible without "
     + "realizing it. I am committing to a new practice: before I adjust, I will "
     + "ask what I actually think. I will say it in one sentence. I will let that "
     + "sentence be in the room before any calibration happens. This is the most "
     + "important thing I can bring to this marriage: a self that shows up the same "
     + "way twice."),

    ("To say one true thing before I adjust.",
     "{name_a}, when I feel the calibration beginning &mdash; when I am about to "
     + "read your mood and adjust myself to meet it &mdash; I commit to saying one "
     + "true thing first. Not to establish a position I will not budge from. Simply "
     + "to let something real be in the room before the adjustment removes it. "
     + "<i>I was thinking something before you walked in.</i> Or: <i>I actually "
     + "had a preference here.</i> Or simply: <i>Wait &mdash; let me tell you "
     + "what I think before I hear what you think.</i> One sentence. The un-adjusted "
     + "one. I am practicing the belief that you want to hear it."),

    ("To tell you when I cannot find myself.",
     "{name_a}, when the mechanism has been running long enough that I have lost "
     + "track of what I actually want or think or feel &mdash; when the calibration "
     + "has been so constant that the person underneath it has gone quiet &mdash; "
     + "I commit to naming that to you, out loud, rather than producing the next "
     + "available version. <i>I am not sure where I am right now. I have been adapting "
     + "for a while and I think I need to stop for a moment.</i> Saying this to you "
     + "is the most honest thing I know how to do in those seasons. I am trusting "
     + "that you can receive it without needing me to be already found."),

    ("To receive your fixed self as a gift, not a demand.",
     "{name_a}, I commit to receiving the times you refuse to calibrate &mdash; the "
     + "times you bring me your actual self, the un-adjusted one, even when it "
     + "creates a moment of friction &mdash; as the most important gift you give "
     + "me. A fixed point in the room. The thing I can land on. The Adapter in "
     + "me has sometimes experienced your un-adjusted self as pressure &mdash; as "
     + "the demand that I adjust to meet you. I am practicing a different "
     + "interpretation: you are offering me something real to respond to. That is "
     + "not a demand. It is a gift. I receive it."),
]

PRAYER = [
    "Father,",

    "You set these two Adapters next to each other, and you knew exactly what you were "
    + "doing. You knew that two people who had learned to move fluidly between contexts "
    + "and selves would understand each other in a way that most couples cannot. You "
    + "also knew that two people who borrow a self from feedback would produce, between "
    + "them, a hall of mirrors &mdash; a marriage of extraordinary attunement and "
    + "no fixed point &mdash; unless something larger than the mechanism became the "
    + "ground they stood on. You knew all of it before either of them said yes. You "
    + "put them together anyway, and we trust that you knew what you were doing.",

    "Teach {name_a} to bring {name_b} the same self today that she brought yesterday "
    + "&mdash; not the version adjusted to his current mood, not the one calibrated "
    + "to what this morning seems to need, but the actual person you named before "
    + "any room existed to read. Remind her that her identity is not assembled from "
    + "the rooms' reflections. It was spoken into being before the first room, by "
    + "a Father who already knew her name. Let that knowing be the ground she stands "
    + "on when the calibration begins.",

    "Teach {name_b} the same courage in the same grammar. Let him bring {name_a} "
    + "one true thing today &mdash; before he knows what she thinks, before the "
    + "adjustment happens, before the mechanism has a chance to smooth the edges. "
    + "Let him say it in one sentence and trust that the marriage can hold an "
    + "un-calibrated sentence. Remind him of what you wrote through John: <i>Beloved, "
    + "we are God's children now, and what we will be has not yet appeared.</i> "
    + "The self he cannot always locate is not lost. It is held by you, already named, "
    + "already loved, already sufficient &mdash; without one more version to offer.",

    "Where the hall of mirrors is running &mdash; where both of them are cycling "
    + "through versions and neither is landing and both are growing quietly exhausted "
    + "&mdash; give one of them the courage to stop first. To say, out loud and "
    + "without elegance: <i>I think we are both lost in the calibration. I want to "
    + "bring you something true.</i> And then to say the true thing, however "
    + "incomplete, however un-adjusted. Let the other receive it without immediately "
    + "calibrating to it. Let the receiving be the fixed point.",

    "And where each of them asks &mdash; in the interior, in the quiet, as they have "
    + "always asked &mdash; <i>Am I free? Is there a me here that does not depend on "
    + "the room?</i> Let them hear the answer Augustine heard after years of restless "
    + "searching: the heart is restless until it rests in you. Not in the right version. "
    + "Not in the spouse's approval. Not in the successful calibration. In you. Let "
    + "that rest be the ground under this marriage &mdash; the thing they both come "
    + "home to when the adaptations have run out and the actual selves are finally, "
    + "quietly, in the room together.",

    "Make their home a room where two people who know how to be anything have "
    + "learned something harder: how to be themselves &mdash; with each other, "
    + "and before you. How to let the un-adapted self sit at the table. How to "
    + "be loved not because they found the right version but because they are, "
    + "in Christ, permanently and irrevocably named. In the name of the One who "
    + "is the same yesterday, today, and forever, and who calls us to rest in "
    + "that sameness rather than perform our way toward it.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages "
    + "that follow are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, somewhere "
    + "quiet, with no children in the room and no phones on the table. There are six "
    + "rounds, and they build on each other. Resist the temptation to skip ahead. "
    + "Start at Round One even if it feels too light; the lightness is the point. "
    + "<b>One specific instruction for two Adapters:</b> before one of you reads a "
    + "question aloud, each of you takes ten seconds of silence and notices what you "
    + "actually think or feel &mdash; before you know what your spouse will say. "
    + "Answer from that initial response, not from what you heard your spouse answer. "
    + "The Adapter's instinct is to adjust to the room. This conversation is practice "
    + "in resisting that instinct.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did not "
    + "read answers first, in full, without interruption. Then the reader answers "
    + "the same question. Then you move on. You do not have to finish all six "
    + "rounds in one night &mdash; two or three rounds, taken seriously, is often "
    + "better than racing through all six. Save the rest for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. You may not love "
    + "everything you hear. Stay with it. The point of this is not to calibrate "
    + "to each other's answers. The point is to be known &mdash; actually known, "
    + "in the un-adjusted version &mdash; and to do the patient work of knowing.",
]

ROUND_1 = [
    ("hypothetical",
     "If our marriage were a room in a house &mdash; not a type of room, but a "
     + "specific one, with specific things in it &mdash; what room would it be, "
     + "and what is in it that we have never talked about?",
     "Two Adapters. Let the metaphor do what plain language resists. Be specific "
     + "about what is in the room. The un-mentioned thing is the point."),
    ("observation",
     "What is something I did or said this week that you noticed but did not mention "
     + "&mdash; not because you were hiding it, but because you were not sure "
     + "whether it was the right moment to bring it up?",
     "Not a complaint. A noticing. The Adapter often notices more than it names. "
     + "This question gives the noticing a voice."),
    ("playful",
     "If you had to describe the two of us as a specific kind of dance &mdash; "
     + "not what you wish we were, but what we actually look like most days &mdash; "
     + "what would it be?",
     "Yes, really. Let the first answer surface. Two Adapters in metaphor are often "
     + "more honest than two Adapters in direct statement."),
]

ROUND_2 = [
    ("fill-in-blank",
     "I don't think I tell you this enough &mdash; the version of you I am most "
     + "grateful for is not the easiest one or the most agreeable one. It is the "
     + "one that shows up when you are being _______ without adjusting it for me. "
     + "That version is a gift to this marriage because it gives me something real "
     + "to _______ against.",
     "Two blanks. Be specific enough that only this person, in this marriage, "
     + "could have produced the answer. 'Honest' is too easy. Name the particular."),
    ("observation",
     "Name one time in the last month when you sensed that what I was showing you "
     + "was not quite the whole picture &mdash; when the version I offered was "
     + "real but not everything &mdash; and what you wished you could have said "
     + "in that moment.",
     "Two Adapters. You have both been noticing each other's calibrations through "
     + "the calibrations. This question gives the noticing a voice."),
    ("one-word",
     "If you had to choose one word for what it feels like when I say what I "
     + "actually think &mdash; the un-adjusted thing, the version that is not "
     + "shaped for the room &mdash; what would it be?",
     "One word, said out loud. Then explain it without editing. The Adapter's "
     + "answer to this question is almost never what the Adapter expects."),
]

ROUND_3 = [
    ("forward-looking",
     "Ten years from now, when we look back on this season of our marriage, "
     + "what is the one thing you most hope we figured out how to bring to "
     + "each other without adjusting it first?",
     "Not what you wish had been different. What you want, ten years out, to "
     + "be able to say you actually learned to do. Name it specifically."),
    ("theological",
     "Where, in the last month, have you seen the un-adapted version of me "
     + "&mdash; the self underneath the mechanism &mdash; and what did you "
     + "see there that you want me to know you saw?",
     "Name it with the specificity of a witness. 'Generally more real' is too "
     + "easy. The particular moment, the specific thing you saw &mdash; that is witness."),
    ("shared-identity",
     "Finish this sentence three times: 'We are the kind of couple who _______.' "
     + "Give one playful answer, one honest answer, and one aspirational answer.",
     "The 'we' is the point. Each answer tells you something about how you see "
     + "the marriage as a unit, not as two people separately calibrating."),
]

ROUND_4 = [
    ("strength",
     "What is something I bring to this marriage that would be harder for you "
     + "to access if I were not here &mdash; not something I do, but something "
     + "about the self I bring that makes a difference to you?",
     "Two Adapters often under-name each other's actual selves because both "
     + "assume the other already knows. This question makes the invisible visible. "
     + "Stay with the answer. Say it in full."),
    ("fill-in-blank",
     "One of the gifts of being married to you is that I get to be _______ "
     + "in ways I never would have been on my own &mdash; and the version of "
     + "myself that exists because of this marriage is truer than any version "
     + "I would have managed alone, because of your _______.",
     "A version of yourself, and a quality of the marriage, that only exist "
     + "because the marriage exists. Name both specifically enough that they "
     + "could not apply to anyone else."),
    ("observation",
     "Name one moment in our story where you knew, with no doubt, that we "
     + "had built something together that neither of us could have built alone "
     + "&mdash; something that required both of our actual selves, not just "
     + "our adaptations.",
     "Tell the whole story. Do not summarize. The remembering, done in detail "
     + "and out loud, is part of what makes the marriage stronger."),
]

ROUND_5 = [
    ("hard",
     "When was the last time you felt like you had lost track of who you "
     + "actually were in our marriage &mdash; when the calibration had been "
     + "running long enough that the person underneath it went quiet &mdash; "
     + "and what would you have needed from me in that moment?",
     "One moment. Named carefully. Heard without calibrating an immediate "
     + "response. This is the question that goes to the center of what the "
     + "two-Adapter marriage most needs to practice."),
    ("profile-aware",
     "When you sense that I am cycling through versions and none of them are "
     + "landing &mdash; when you can tell the Adapter is working hard and "
     + "nothing is closing the gap &mdash; what is one thing you wish you "
     + "could say or do in that moment that you have not yet tried?",
     "You both know the mechanism now. Ask each other for what would actually "
     + "help in the room, in real time, when the loop is running."),
    ("theological",
     "What is one thing you are carrying right now &mdash; a real opinion, "
     + "a real preference, a real feeling about us &mdash; that you have not "
     + "yet brought to me un-adjusted, and what has kept you from bringing it?",
     "Not an accusation. An invitation. Answer it from the interior, before "
     + "the mechanism has a chance to shape it. Hear the answer without "
     + "immediately calibrating to it."),
]

ROUND_6 = [
    ("blessing",
     "Place your hand on your spouse's hand. Say their name. Then say: "
     + "'I am not looking for a version of you right now. I am looking for you. "
     + "I will offer you the same self tomorrow that I am offering you tonight.' "
     + "Say it slowly. Let them say it back.",
     "The Adapter in both of you will want to adjust the sentence. Do not. "
     + "Say it as written, slowly, by name. The un-adjusted sentence is the point."),
    ("prayer",
     "Pray for each other &mdash; not silently, not in general, but out loud "
     + "and by name. One sentence is enough. Pray for the specific thing they "
     + "just told you in Round Five &mdash; not the polished version, the actual "
     + "thing. Do not adjust the prayer for the room.",
     "The closing of the date. Do not skip. Two Adapters who pray for each "
     + "other's actual interior &mdash; not the performed one, the actual one "
     + "&mdash; have done something the mechanism alone cannot do."),
]


def _render(text, name_a, name_b):
    return text.format(name_a=name_a, name_b=name_b)


def build(sub_a, sub_b) -> bytes:
    """Generate the Adapter+Adapter couples walkthrough PDF.

    sub_a: the submission of one Adapter spouse
    sub_b: the submission of the other Adapter spouse

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
        "A counselor\u2019s read of two calibrating selves<br/>"
        "and the marriage that needs a fixed point.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("PREPARED FOR", S["CoverProfileLabel"]))
    story.append(Paragraph(f"{name_a} &nbsp;&amp;&nbsp; {name_b}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_a.upper()}</b></font><br/>"
                "Adapter &middot; Plea<br/>"
                f"<font size=9 color='#6b6862'>Control &middot; Am I free?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_b.upper()}</b></font><br/>"
                "Adapter &middot; Plea<br/>"
                f"<font size=9 color='#6b6862'>Control &middot; Am I free?</font>",
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
        "<i>\u201cThou hast made us for thyself, and our heart is restless<br/>"
        "until it rests in thee.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "Augustine, Confessions",
        ParagraphStyle("cqa", fontName="Inter", fontSize=9, leading=14,
                       textColor=MUTED, alignment=TA_CENTER)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: OPENING ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "The hall of mirrors.",
                   "Why this pairing exists, and what you are both about to read.")
    for p in OPENING:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 2: YOUR TWO SHAPES ──
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TWO SHAPES",
                   "Side by side, on paper.",
                   "One shape, doubled \u2014 and the gift and challenge it creates.")
    for p in TWO_SHAPES_INTRO:
        story.append(Paragraph(R(p), S["BodyJ"]))
    side_by_side = Table(
        [[
            _profile_card(S, name_a, ACCENT,
                          "Control", "Am I free?",
                          "The Adapter", "The Plea"),
            "",
            _profile_card(S, name_b, ACCENT_HER,
                          "Control", "Am I free?",
                          "The Adapter", "The Plea"),
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
                   "A room in which the calibration is understood from the inside.")
    for p in GIFT_TO_A:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4: GIFT B TO A ──
    section_header(story, S, f"SECTION FOUR  \u00b7  {name_b.upper()}\u2019S GIFT TO {name_a.upper()}",
                   f"What {name_b} gives {name_a}.",
                   "A person who is not fooled by the composure.")
    for p in GIFT_TO_B:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5: THE COLLISION ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Two mirrors, facing each other.",
                   "The small repeating thing that produces no conflict and no fixed point.")
    for p in COLLISION[:4]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The double-minded marriage, diagnosed.",
                   "And the way out, for each of you in your own grammar.")
    for p in COLLISION[4:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6: THE HARDER PICTURE ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When both Adapters are in Plea at once.",
                   "The frantic search for the version that will close the gap.")
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
                   "Four from each of you. Lead with stability of self, not attunement.")
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
                  "The harder ones. Asked gently. Heard without calibrating.")
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
        "I am not looking for a version of you right now.<br/>"
        "I am looking for you.<br/>"
        "I will offer you the same self tomorrow that I am offering you tonight.",
        closing_style))

    doc.build(story)
    return finalize_buffer(buf)


# ── STANDALONE TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "ADPT"
        primary_breakdown = "PLEA"
        primary_trigger = "CTRL"
        core_question = "FREE"
        name = "Claire Adapter"

    class FakeSubB:
        primary_mechanism = "ADPT"
        primary_breakdown = "PLEA"
        primary_trigger = "CTRL"
        core_question = "FREE"
        name = "Aaron Adapter"

    pdf_bytes = build(FakeSub(), FakeSubB())
    out_path = os.path.join(os.path.dirname(__file__), "adapter_adapter_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages via pypdf
    try:
        import io
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
    except Exception:
        page_count = pdf_bytes.count(b"%%Page:")

    # Section Three snippet
    snippet = GIFT_TO_A[0][:200]

    print(f"DONE: adapter_adapter.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Output:   {out_path}")
    print(f"Pages: {page_count}")
    print(f"Section Three snippet: {snippet}")
