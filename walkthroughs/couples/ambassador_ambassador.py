"""Couples Walkthrough — Ambassador + Ambassador.

Voice: Tim Keller (from The Meaning of Marriage + Walking with God through
Pain and Suffering). Pastoral, theologically rich, warmly direct.
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where both spouses are Ambassadors.
First names are substituted from the submissions at render time:
    {name_a}  -> the first Ambassador spouse's first name (alphabetical)
    {name_b}  -> the second Ambassador spouse's first name (alphabetical)

For same-mechanism pairs the order does not carry directional meaning.
The build() function sorts alphabetically so A <= B.

Pastoral frame: Two Ambassadors is the warmest-looking same-mechanism
pairing — and one of the most quietly dangerous. Both spouses give,
both serve, both care, both keep a ledger neither can name. The collision
is not a fight about who gives more; it is the slow accumulation of two
simultaneous ledgers. Key texts: 1 Cor 13:5, Romans 12:10, Galatians 6:9,
Galatians 6:3, Hebrews 12:15, Keller's Counterfeit Gods.
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
    + "for you, the small repeating rock has a particular texture, because you are one "
    + "of the most counterintuitive pairings we encounter: <b>two Ambassadors.</b>",

    "From the outside, yours is the marriage everyone points to. You are known for your "
    + "hospitality. You remember birthdays, yours and everyone else's. You are the couple "
    + "that shows up when something goes wrong in the neighborhood, the church, the family "
    + "network. Both of you are warm, attentive, considerate. People who know you well "
    + "probably use the word <i>kind</i> to describe your marriage before they use any "
    + "other word. They are not wrong. The warmth is real.",

    "What they cannot see &mdash; and what you may have difficulty seeing yourselves "
    + "&mdash; is that both of you have been, for a very long time, keeping a quiet "
    + "record. Not deliberately. Not maliciously. But the Ambassador, by the deep logic "
    + "of the mechanism, gives in order to know whether the giving will be returned, and "
    + "somewhere below the level of conscious thought, both of you have been tracking "
    + "whether it has been. You are both waiting for the account to be settled. The "
    + "account has not been settled, because it never is. And the warmth you are both "
    + "generating &mdash; genuine, costly, beautiful &mdash; has not yet answered the "
    + "question underneath it: <i>Am I lovable?</i>",

    "Here is what I want to do for you. I will name what each of you brings the other "
    + "that no one else in the marriage can give &mdash; the genuine gift that two "
    + "Ambassadors make possible together. Then I will name the collision your shared "
    + "mechanism creates: not a fight about who gives more, but the slow accumulation "
    + "of two simultaneous ledgers that neither of you will name. Then I will name the "
    + "harder picture &mdash; what happens when both of you are in breakdown at once "
    + "&mdash; and what to do then. Then I will give each of you commitments, not as "
    + "rules, but as small daily practices that change the temperature of a home over "
    + "months and years.",

    "Read it together, if you can. If not, read it separately and then sit down with "
    + "it. The goal is not a marriage in which both of you give more. You already give "
    + "more than most couples. The goal is a marriage in which both of you have finally "
    + "learned, in a room with each other, to <i>receive</i> &mdash; and to rest in the "
    + "love that was there before the giving began.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on "
    + "paper, side by side. Most couples never see their two profiles next to each other. "
    + "You are about to &mdash; and for you, the first thing you will notice is how "
    + "completely the profiles mirror each other.",
]

TWO_SHAPES_BODY = [
    "{name_a}, you are an <b>Ambassador</b> whose body reads disconnection as an alarm, "
    + "and whose deepest question is <i>Am I lovable?</i> You have learned, over years, "
    + "that the surest way to keep connection alive is to be the one who gives it. You "
    + "warm rooms. You take care of people. You notice when someone is left out and go "
    + "to find them. When the connection threatens to falter, you give more &mdash; "
    + "more warmth, more service, more attention &mdash; because giving is the only "
    + "strategy you have ever fully trusted to keep you close.",

    "{name_b}, you are an <b>Ambassador</b> running the same mechanism: disconnection "
    + "is the alarm, <i>Am I lovable?</i> is the question. You, too, have built a self "
    + "that presents need as service &mdash; that turns your own longing for closeness "
    + "into care for others, because this feels safer than asking directly for what you "
    + "need and having it withheld. You, too, keep the rooms around you warm. And you, "
    + "too, have been hoping that love given consistently enough will eventually produce "
    + "a love that is stable and sure and not contingent on anything you do next.",

    "Take a moment to absorb what this means. You are asking the same question. You are "
    + "running the same mechanism. You are, in many seasons, protecting the same wound. "
    + "The shared grammar of your marriage means there is a mutual understanding between "
    + "you that most couples do not have: neither of you has had to explain to the other "
    + "why you sent the thoughtful note, why you brought the meal, why you stayed late "
    + "at the gathering to make sure everyone felt included. You simply know. You have "
    + "lived inside this mechanism your whole lives.",

    "But here is what the shared grammar does not automatically produce: <i>rest.</i> "
    + "Two Ambassadors in a marriage create a home in which the giving never stops, "
    + "because neither person feels they have earned the right to stop giving. Both of "
    + "you are managing the temperature. Both of you are watching for the signal that "
    + "says the connection is cooling. Both of you have made yourselves indispensable "
    + "in ways that feel like love &mdash; and are love &mdash; but that have also "
    + "become a kind of endless labor that neither of you can lay down without fearing "
    + "what might happen if you do.",

    "This is the singular gift and the singular challenge of your marriage. The gift "
    + "is that you have built a home of uncommon warmth, one in which both people are "
    + "cared for with genuine attentiveness. The challenge is that underneath the warmth, "
    + "both of you are secretly exhausted, secretly waiting, and secretly keeping a "
    + "record neither of you has ever shown the other.",
]

GIFT_TO_A = [
    "{name_b} gives {name_a} something almost no one else in her life can give: "
    + "<b>a witness who already knows the cost of the giving.</b>",

    "Most people in {name_a}'s world receive her warmth gratefully, absorb it naturally, "
    + "and have no particular awareness of what it costs her. They benefit from the "
    + "Ambassador's care without understanding the labor behind it. This is not "
    + "carelessness on their part. The Ambassador is very good at making the giving "
    + "look effortless. But the cost is real, and most people never see it.",

    "{name_b} sees it. Not because he is unusually perceptive, but because he carries "
    + "the same mechanism and therefore knows, from the inside, what it means to give "
    + "past the point of your reserves and keep a composed face. He knows the particular "
    + "exhaustion of being the one who always notices. He knows what it costs to track "
    + "everyone's emotional temperature while quietly wondering whether anyone is "
    + "tracking yours. He has lived there. He knows.",

    "Tim Keller, writing in <i>The Meaning of Marriage</i>, observed that one of "
    + "the deepest gifts a good marriage can offer is to be known &mdash; not "
    + "catalogued and analyzed, but known the way a person who has lived beside you "
    + "for years knows you, without a translation. {name_b} knows {name_a}'s mechanism "
    + "from the inside. He does not need her to explain why the quiet evening from "
    + "someone she loves registers as a signal. He does not need her to explain the "
    + "math of the invisible ledger. He carries his own copy of the same ledger. For "
    + "{name_a}, being known this way &mdash; without effort, without explanation "
    + "&mdash; is one of the rarest gifts in any relationship.",

    "{name_a} &mdash; if you want to thank {name_b} for something this week, thank "
    + "him for the fact that he knows what the giving costs and stays anyway. You have "
    + "probably spent much of your life being thanked for what you do but rarely seen "
    + "for what it costs you. He sees it. Tell him that the seeing matters more than "
    + "almost anything else he has given you. He may not know how to receive the "
    + "gratitude &mdash; the Ambassador rarely does. Say it anyway.",

    "{name_b} &mdash; what you are giving {name_a}, simply by having lived inside the "
    + "same mechanism she lives in, is a marriage in which she does not have to perform "
    + "her care for an audience that cannot quite see it clearly. You are the one person "
    + "in the room who understands the grammar of what she is doing. That is not a small "
    + "thing. That is the architecture of a home in which the Ambassador can, perhaps "
    + "for the first time, be seen without having to explain herself.",
]

GIFT_TO_B = [
    "{name_a} gives {name_b} something almost no one else in his life can give: "
    + "<b>a person who will still come toward him when the giving has stopped.</b>",

    "Every Ambassador has seasons. Seasons when the giving is easy and the warmth is "
    + "genuine and the mechanism is running on something that feels close to joy. And "
    + "seasons when the reserves are low &mdash; when the Ambassador has been giving "
    + "past empty for so long that a cold and unfamiliar quiet begins to settle. In "
    + "those seasons, most of the Ambassador's world does not notice, because the "
    + "Ambassador does not show it. The composed exterior stays composed. The warmth "
    + "continues, if a little more effortful. The need stays hidden.",

    "{name_a} is the person in {name_b}'s life most likely to notice when the giving "
    + "has become labor rather than love &mdash; not because she is watching for it, "
    + "but because she knows the signs from the inside. She has felt the particular "
    + "flatness of a week in which she has given everything and received nothing she "
    + "can name. She does not need {name_b} to announce his depletion. She recognizes "
    + "it. And when she comes toward him in those moments &mdash; not with a question "
    + "he has to answer, but simply with presence, with the small specific attentiveness "
    + "that is her gift &mdash; she is doing something the mechanism alone cannot do "
    + "for him: she is giving without requiring the giving to be returned.",

    "The theological word for what {name_a} gives {name_b} in those moments is "
    + "<i>grace</i> &mdash; not in the theological shorthand of 'unmerited favor,' "
    + "but in its original texture: a love that comes toward you when you have nothing "
    + "left to offer in return. Galatians 6:9 says: <i>Let us not grow weary in doing "
    + "good, for in due season we will reap, if we do not give up.</i> {name_a} is, "
    + "for {name_b}, the living proof of that promise in miniature: the person who "
    + "does not stop coming simply because the season is hard.",

    "{name_b} &mdash; if you want to thank {name_a} for something this week, thank "
    + "her for the times she came toward you when you had nothing available to give "
    + "back. The Ambassador rarely believes he is worth being pursued when the giving "
    + "has stopped. She has proven, in small and repeated ways, that you are. Name "
    + "one of those moments specifically. She will not know what to do with the "
    + "gratitude. Say it anyway.",

    "{name_a} &mdash; what you are giving {name_b}, when you come toward him in "
    + "the flat seasons, is the closest thing to gospel-shaped love that one "
    + "Ambassador can offer another. You are giving him the answer to the question "
    + "the mechanism keeps reopening: <i>Am I lovable when I am not useful?</i> "
    + "Do not underestimate the weight of this. He may not be able to receive it "
    + "yet. Keep giving it anyway.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you, "
    + "though its shape is subtler than it is in most pairings &mdash; because when "
    + "two Ambassadors collide, the collision does not look like conflict. It looks "
    + "like two people who love each other very much and are both slightly, inexplicably "
    + "tired.",

    "Here is the collision in its simplest form: <b>two ledgers, kept simultaneously, "
    + "by two people who each sincerely believe they give more than the other and "
    + "receive less.</b> You are both right, in a narrow sense. You are both wrong, "
    + "in a more important one. Neither of you has stopped serving long enough to "
    + "receive what the other is actually offering. Both of you have been so busy "
    + "generating warmth that neither has slowed down enough to be warmed.",

    "The mechanism that runs in both of you was built for a world in which the "
    + "Ambassador gives and waits, gives and watches, gives and quietly tallies. It "
    + "was not built for a marriage of two Ambassadors, because in such a marriage "
    + "both people are giving and both are waiting and both are watching and both are "
    + "quietly, privately, feeling under-loved &mdash; not because the love is absent, "
    + "but because both are too busy giving it to stop and receive it. The meal is "
    + "being prepared by two people who are each convinced the other is not helping "
    + "enough, and neither of them has sat down to eat.",

    "Paul writes in 1 Corinthians 13:5 that love <i>keeps no record of wrongs.</i> "
    + "The Ambassador has, in good faith, read this verse and believed they were "
    + "living it. But Paul's instruction, for the two-Ambassador marriage, needs a "
    + "specific elaboration: <b>love keeps no record of givings.</b> The ledger the "
    + "Ambassador has been keeping is not a record of wrongs received but of goods "
    + "given &mdash; a tally of warmth offered and not matched, of service rendered "
    + "and not acknowledged, of attentiveness spent and not returned in kind. This "
    + "record feels nothing like bitterness. It feels like perfectly reasonable "
    + "accounting. And yet it is the root Hebrews 12:15 warns about: <i>See to it "
    + "that no one fails to obtain the grace of God; that no root of bitterness "
    + "springs up and causes trouble, and by it many become defiled.</i> The root "
    + "of bitterness does not announce itself as bitterness. It announces itself "
    + "as exhaustion. As the quiet conviction that you have given more than you "
    + "have received. Both of you are running it at once.",

    "Here is the slow-motion pattern. {name_a} has had a week in which she has "
    + "given considerably &mdash; to the children, to the household, to her own "
    + "network of people who needed her &mdash; and she has been quietly tracking "
    + "whether {name_b} has noticed. He has noticed, but he has not named it, "
    + "because he has been giving considerably himself and has been quietly "
    + "tracking whether she has noticed. She has noticed his giving too, but "
    + "she has not named it, because she is not quite sure whether naming it "
    + "would mean she is not also naming her own giving, and the whole accounting "
    + "has become too complicated to raise directly. Both of them are circling "
    + "the ledger without opening it. Both of them are waiting for the other "
    + "to go first. Neither will. The evening passes in warmth that is slightly "
    + "thinner than it looks.",

    "Romans 12:10 says: <i>Outdo one another in showing honor.</i> This verse "
    + "is frequently offered to Ambassador couples as an encouragement, and it "
    + "is one &mdash; but it carries a danger for two Ambassadors specifically. "
    + "Both of you are already trying to outdo each other in showing honor. "
    + "Both of you are already giving more than you are asked for. The verse's "
    + "instruction is sound; the Ambassador's execution of it has become, "
    + "quietly, a competition. Both of you are trying to win a race neither "
    + "of you has named, toward a finish line neither of you can see, and "
    + "the running is making both of you tired.",

    "Charles Spurgeon, preaching on the laborers in the vineyard, offered a "
    + "warning that applies here with unusual precision: <i>the giver who keeps "
    + "count is the most dangerous kind of bitter.</i> He is the most dangerous "
    + "because he sincerely believes he is not bitter at all &mdash; he is simply "
    + "presenting an accurate accounting of what has been given and not returned. "
    + "For two Ambassadors, Spurgeon's warning doubles: two givers keeping count "
    + "quietly is double the danger, double the ledger, and double the likelihood "
    + "that the bitterness will surface in a way that surprises both of them.",

    "The way out is not for either of you to give less. The warmth is real and "
    + "the world needs it. The way out is something considerably harder and more "
    + "specific: <b>to close the ledger, together, by naming it out loud.</b> "
    + "Not to prosecute. Not to demand a settlement. But to say, with as much "
    + "honesty as you can find: <i>I have been keeping a record. I did not mean "
    + "to. I want to put it down. Can we start again from something that is "
    + "not the ledger?</i>",

    "{name_a}, when you feel the tally running &mdash; when the sense of "
    + "giving more than you receive has been accumulating for several days "
    + "&mdash; the right move is not to give more in hopes the gap will close. "
    + "The gap does not close that way. The right move is to name one specific "
    + "thing you actually need from {name_b}, in one sentence, without "
    + "wrapping it in concern for him or qualifying it with <i>only if you can.</i> "
    + "The Ambassador's need, stated plainly and without apology, is one of the "
    + "hardest and most important sentences in this marriage.",

    "{name_b}, when you feel the tally running in you, the same discipline applies. "
    + "Name one specific thing you need. Not the whole ledger &mdash; the ledger "
    + "is too heavy to carry into a single conversation. The one thing, on this day, "
    + "that would answer the question underneath the accounting: <i>Am I loved "
    + "for what I am, and not only for what I give?</i> The Ambassador who can ask "
    + "for this directly is the Ambassador who has begun, quietly and significantly, "
    + "to believe the answer is yes.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be seasons &mdash; not often, but they will "
    + "come &mdash; when the ledger collision escalates and both of you are in "
    + "breakdown at the same time. The stakes are higher in the two-Ambassador "
    + "marriage than in most pairings, because your breakdowns do not simply oppose "
    + "each other. They mirror each other. And a mirrored breakdown, in the warmest "
    + "marriage in the room, is one of the most disorienting things either of you "
    + "will experience.",

    "The most common pattern is what we might call the <b>simultaneous Plea.</b> "
    + "Both Ambassadors, when their breakdown arrives, do what the Plea does: they "
    + "escalate the giving. They apologize more. They give more. They try harder to "
    + "close the gap with warmth. And because both of you are doing this at the same "
    + "time, the marriage becomes, in those seasons, a feast of unfelt love. So much "
    + "is being offered. So little is being received. You are both pouring into the "
    + "same vessel, neither of you pausing long enough to drink from it. The generosity "
    + "is extraordinary and the loneliness, underneath it, is acute.",

    "There is a second pattern, less common but more dangerous: the one in which "
    + "the Plea exhausts itself and tips over into <b>the Attorney.</b> The Ambassador "
    + "has been giving, and giving, and giving &mdash; and the tally, kept so quietly "
    + "for so long, finally becomes too heavy to carry without speaking. What comes "
    + "out then is not the Plea. It is the evidence binder: <i>I did this for you, "
    + "and this, and this, and this. I have given and given, and you have no idea "
    + "what it has cost me, and here you are telling me it is not enough.</i> The "
    + "other spouse, who has been doing the same giving and keeping the same ledger, "
    + "hears this and does not experience it as a disclosure. They experience it "
    + "as a prosecution. Their own Attorney rises. And suddenly two people who love "
    + "each other deeply are presenting competing evidence briefs, each accurate, "
    + "each genuinely aggrieved, neither of them finding the acknowledgment they "
    + "were actually looking for.",

    "Paul holds two verses together in Galatians 6 that speak directly into this "
    + "pattern, and the proximity of the two verses is not accidental. Verse 9: "
    + "<i>Let us not grow weary in doing good, for in due season we will reap, "
    + "if we do not give up.</i> Verse 3: <i>For if anyone thinks he is something, "
    + "when he is nothing, he deceives himself.</i> These two verses belong together "
    + "in the Ambassador's hearing. The first says: your giving is not wasted; do "
    + "not give up. The second says: but if the giving has become the ground of "
    + "your identity &mdash; if you have begun to think of yourself as something "
    + "because you give so much &mdash; you have entered the precise territory "
    + "where self-deception grows. The Ambassador does good. The Ambassador can "
    + "also, quietly, make the doing of good into the ground of the self. And "
    + "when that happens, and the doing of good is not reciprocated, the self "
    + "is threatened &mdash; and the Attorney rises to protect it.",

    "Keller, in <i>Counterfeit Gods</i>, names the specific spiritual danger that "
    + "the two-Ambassador marriage must eventually face together: <b>love itself "
    + "can become an idol.</b> Not love wrongly directed &mdash; love directed at "
    + "the right person, in a real marriage, for real reasons. But love organized "
    + "around a question &mdash; <i>am I lovable?</i> &mdash; becomes a kind of "
    + "temple, and the other spouse is placed at the altar. You are both, without "
    + "meaning to, asking the other to bear a weight only God can carry: the "
    + "weight of finally, definitively, certainly answering the question underneath "
    + "the trigger. When the other person inevitably fails to carry it &mdash; "
    + "because they are human and tired and carrying their own question &mdash; "
    + "the idol proves insufficient, and the breakdown follows.",

    "What to do when you can still see what is happening:",

    "<b>One of you names the Plea out loud.</b> Not to shame the other. Not to "
    + "score a point. But to interrupt the feedback loop of two people giving past "
    + "empty and neither receiving. One of you says: <i>I think we are both in "
    + "Plea. I think we are both trying very hard and neither of us is managing "
    + "to receive what the other is offering. I want to stop for a moment and "
    + "receive something before I offer anything else.</i> That sentence is harder "
    + "to say than it sounds. Say it anyway.",

    "<b>In the pause, each of you names one thing you are actually grateful for "
    + "in what the other has given this week &mdash; not generally, but specifically.</b> "
    + "Not <i>you are so caring.</i> That is too large and too easy for the "
    + "Ambassador to deflect. Something specific: a single act, a single moment, "
    + "the way they handled a particular Tuesday. Specific gratitude is the one "
    + "form of acknowledgment the Ambassador's ledger cannot argue with. When the "
    + "specific thing is named, something in the account closes &mdash; not the "
    + "whole ledger, but one line of it. One line at a time is how the Ambassador "
    + "learns to receive.",

    "<b>Pray for each other, by name, for the specific thing the other is "
    + "carrying.</b> Not eloquently. Not as a spiritual performance. Simply: "
    + "<i>Lord, {name_b} has been giving this week until he is tired. Would you "
    + "give him something that I cannot give him &mdash; the certainty that he "
    + "is loved before and apart from anything he does?</i> Or: <i>Lord, {name_a} "
    + "is asking the question she has always asked. Would you answer it &mdash; "
    + "not through me, because I will always be insufficient, but through the "
    + "love that was settled at the cross before either of us could give anything?</i>",

    "<b>Neither of you is the problem.</b> The Plea and the Attorney are not the "
    + "truest things about either of you. They are old mechanisms that were built "
    + "in seasons when giving was the only tool available and the question had no "
    + "other answer. The truest thing about both of you is that you chose each "
    + "other, and that the warmth you have built together, for all its hidden "
    + "ledgers, is real and good and worth the slow work of learning, at last, "
    + "to lay the accounting down and simply rest in what you have been given.",
]

COMMITMENTS_INTRO = [
    "What follows are eight commitments &mdash; four from {name_a}, four from {name_b}. "
    + "They are not vows in the legal sense. They are the small daily practices that, "
    + "offered to each other freely, change the temperature of a home over months and "
    + "years. For the two-Ambassador marriage, the pastoral direction is the same for "
    + "both of you, and it is a reversal of the mechanism's entire logic: "
    + "<i>lead with receiving, not giving.</i> Before you offer something to your "
    + "spouse today, accept something they have already offered you. Name it. Thank "
    + "them for it specifically. Let the acknowledgment come before the next act "
    + "of service. This is the discipline that makes two givers into one household "
    + "that knows how to rest. Read each commitment slowly. If one of you cannot "
    + "say a particular commitment in good faith yet, do not say it. The goal is "
    + "not performance. It is honesty.",
]

A_COMMITMENTS = [
    ("To accept what you have given me today.",
     "{name_b}, I commit to receiving one specific thing you have offered me "
     + "today &mdash; one act of care, one gesture of attention, one moment of "
     + "warmth &mdash; without immediately giving something back. I will name what "
     + "I received, in one sentence, before I offer anything in return. The "
     + "Ambassador in me will resist this. She will want to immediately match the "
     + "giving or exceed it. I will practice receiving first, on the conviction "
     + "that a marriage in which both of us can receive is a marriage in which "
     + "neither of us has to give past empty."),

    ("To name the ledger before I add to it.",
     "{name_b}, when I feel the tally running &mdash; when the sense that I am "
     + "giving more than I am receiving has been accumulating for several days "
     + "&mdash; I commit to naming it before the ledger grows too heavy to carry "
     + "into a conversation. I will say, in one sentence and without prosecuting: "
     + "<i>I have been tracking something this week. Can I name it?</i> I will "
     + "not wait until the Attorney has assembled the brief. I will name the first "
     + "line while the ledger is still small."),

    ("To ask for what I need, without qualifying it.",
     "{name_b}, I commit to naming one thing I actually need from you, in this "
     + "week, without wrapping it in concern for whether you can manage it. "
     + "No <i>only if it is not too much</i>. No <i>whenever you get a chance.</i> "
     + "The Ambassador's need, stated plainly, is not a burden. I am practicing "
     + "believing this by saying it plainly to you once a week, without apology."),

    ("To close the ledger with gratitude, not addition.",
     "{name_b}, when I notice that you have given me something specific this week, "
     + "I commit to saying so &mdash; specifically, with the actual thing named "
     + "&mdash; rather than responding to your giving with my own giving. "
     + "<i>Thank you for Tuesday</i> is not a ledger entry. It is the closing "
     + "of one. I will practice closing, not adding."),
]

B_COMMITMENTS = [
    ("To accept what you have given me today.",
     "{name_a}, I commit to receiving one specific thing you have offered me "
     + "today &mdash; one act of care, one gesture, one moment of attentiveness "
     + "&mdash; without immediately matching it or exceeding it. I will name what "
     + "I received, out loud, before I give anything back. I know this will feel "
     + "unnatural. The Ambassador in me will insist that receiving without "
     + "returning is some kind of failure. I will practice it anyway, because "
     + "a marriage where both of us can stop long enough to be cared for is "
     + "worth whatever awkwardness the stopping requires."),

    ("To name the ledger before I add to it.",
     "{name_a}, when I feel the tally running in me &mdash; when the quiet "
     + "sense of giving more than I am receiving has been building &mdash; "
     + "I commit to naming it before it grows into the brief. One sentence: "
     + "<i>I have been tracking something this week. Can I tell you what it is?</i> "
     + "Not the whole accumulation. The first line, named early, while there is "
     + "still room for the conversation to be something other than a prosecution."),

    ("To ask for what I need, without qualifying it.",
     "{name_a}, I commit to naming one thing I genuinely need from you, this "
     + "week, without apologizing for it in advance or framing it as fine if "
     + "you cannot. The Ambassador's need is not a burden. Stating it plainly "
     + "is the discipline I most need to practice, because it is the one that "
     + "runs most directly against the mechanism's grain. I will practice it "
     + "with you, once a week, in one clear sentence."),

    ("To close the ledger with gratitude, not addition.",
     "{name_a}, when I notice something specific you have given me this week, "
     + "I commit to naming it specifically &mdash; the act, the moment, the "
     + "particular Tuesday &mdash; and stopping there. Not matching. Not adding "
     + "my own contribution to the account. Simply: <i>I noticed that, and I am "
     + "grateful for it, and I want you to know that I received it.</i> This is "
     + "how the ledger closes. One specific acknowledgment at a time."),
]

PRAYER = [
    "Father,",

    "You set these two givers next to each other, and you knew exactly what you "
    + "were doing. You knew two Ambassadors would build one of the warmest homes in "
    + "any room they entered. You also knew that two people who give in order to "
    + "be loved would produce, between them, two ledgers kept so quietly that "
    + "neither of them would see the other's until the weight became unbearable. "
    + "You knew all of it before either of them said yes.",

    "Teach them the receiving that their mechanism resists. Teach {name_a} to "
    + "accept what {name_b} has already given her today, before she gives "
    + "anything back &mdash; to name it specifically, to let it land, to rest "
    + "in it for a moment rather than immediately adding to the account. "
    + "Teach {name_b} to accept what {name_a} has already given him &mdash; "
    + "to say <i>I received that</i> before he says <i>and here is what I "
    + "have for you.</i>",

    "Where the ledger is running &mdash; where the quiet tally of givings "
    + "has been accumulating in both of them at once, and neither of them "
    + "has named it &mdash; give one of them the courage to speak first. "
    + "Not with the full brief. With one line. <i>I have been tracking "
    + "something. Can I tell you what it is?</i> And let the other receive "
    + "that line without defending, without presenting their own tally, "
    + "without immediately giving something back to close the gap.",

    "Where the question is still running &mdash; <i>Am I lovable? Am I loved "
    + "for what I am, and not only for what I do?</i> &mdash; would you remind "
    + "them both that the answer was given before either of them could give "
    + "anything. <i>For God so loved the world</i> was not spoken to people "
    + "who had first demonstrated their generosity. It was spoken into a world "
    + "that had given nothing and owed everything &mdash; and it is, even now, "
    + "the only love that can finally answer what both of their mechanisms "
    + "have been asking. Let that love be the ground under this marriage. "
    + "Let it be what they both come home to when the giving has run out.",

    "Make their home a room in which two people who both know how to give have "
    + "learned something harder: how to receive &mdash; from each other, and "
    + "from you. How to sit at the table they have set for everyone else and "
    + "let someone bring them something. How to be loved not because they are "
    + "useful but because they are, in Christ, permanently and irrevocably held.",

    "In the name of the One who gave everything first, and who asks nothing "
    + "of us as the price of the giving.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages "
    + "that follow are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, somewhere "
    + "quiet, with no children in the room and no phones on the table. There are six "
    + "rounds, and they build on each other. Resist the temptation to skip ahead. Start "
    + "at Round One even if it feels too light; the lightness is the point.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did not "
    + "read answers first, in full, without interruption. Then the reader answers "
    + "the same question. Then you move on. You do not have to finish all six rounds "
    + "in one night &mdash; in fact, two or three rounds, taken seriously, is often "
    + "better than racing through all of them. Save the rest for the next date.",

    "<b>One rule.</b> The other person's answer is never wrong. You may not love "
    + "everything you hear. Stay with it. The point of this is not to care for each "
    + "other's answers. The point is to receive each other &mdash; and to do the "
    + "work of being received.",
]

ROUND_1 = [
    ("hypothetical",
     "If our marriage were a temperature, what would it be right now &mdash; "
     + "and who has been doing most of the heating?",
     "Two Ambassadors. Be honest. The question is not a complaint. It is a starting place."),
    ("observation",
     "What is something I did for you this week that you noticed and did not mention?",
     "Not a complaint. A small noticing. The fact that you noticed at all is the gift. "
     + "Naming it out loud is the receiving."),
    ("playful",
     "If you had to describe each of us as a kind of weather &mdash; a particular "
     + "season, a particular kind of day &mdash; what would you pick for each of us, and why?",
     "Yes, really. Let the metaphor do something. Two Ambassadors are often more "
     + "honest in metaphor than in plain statement."),
]

ROUND_2 = [
    ("fill-in-blank",
     "I don't think I tell you this enough &mdash; I am amazed at the way God made "
     + "you so _______. Your _______ is a gift to our marriage, and I have not been "
     + "receiving it as well as I should.",
     "Two blanks. The second one is the harder one. Be specific enough that only "
     + "you, in this marriage, could have said it."),
    ("observation",
     "Name one thing you have watched me carry for other people this year &mdash; "
     + "something I gave, or held, or managed for someone else &mdash; that you "
     + "wish you had acknowledged at the time.",
     "Two Ambassadors often see each other's giving more clearly than they say. "
     + "This is the question that gives the seeing a voice."),
    ("one-word",
     "If you had to choose one word to describe what it feels like when I actually "
     + "ask you for something &mdash; when I name a need directly, without qualifying "
     + "it &mdash; what word would it be?",
     "One word, said out loud. Then explain it. The Ambassador's answer to this "
     + "question is almost never what the Ambassador expects."),
]

ROUND_3 = [
    ("forward-looking",
     "Five years from now, when we look back on this season of our marriage, what "
     + "do you hope we will say we finally learned to receive from each other?",
     "Not what you hope to give. What you hope, by then, to be able to accept "
     + "without immediately giving something back."),
    ("theological",
     "Where, in the last month, have you seen God specifically at work in me &mdash; "
     + "not in what I have done for others, but in who I am becoming?",
     "Not where you want him to work. Where you have already seen it. Name it "
     + "with the specificity that only someone who lives beside you could carry."),
    ("shared-identity",
     "Finish this sentence three times: 'We are the kind of couple who _______.' "
     + "Give one playful answer, one true answer, and one aspirational answer.",
     "The 'we' is the point. The aspirational one is what you are working toward "
     + "together, not apart."),
]

ROUND_4 = [
    ("strength",
     "What is something I do for the warmth and care of this marriage that you "
     + "would have to learn to do for yourself if I were not here?",
     "Two Ambassadors often assume the other one knows. They rarely do, in the "
     + "specific way. Stay with the answer. Say it in full."),
    ("fill-in-blank",
     "One of the gifts of being married to you is that I get to be _______ in "
     + "ways I never would have been alone &mdash; and the warmth we have built "
     + "together is better than any warmth I would have built by myself because "
     + "of your _______.",
     "A version of yourself, and a quality of the marriage, that only exist because "
     + "the marriage exists. Name both specifically."),
    ("observation",
     "Name one moment in our story so far where you knew, with no doubt, that we "
     + "had built something together that neither of us could have built alone &mdash; "
     + "something warm, or good, or lasting, that required both of us.",
     "Tell the story in full. The remembering is part of the strengthening."),
]

ROUND_5 = [
    ("hard",
     "If you had to name the moment in our marriage when you have most felt like "
     + "your giving was invisible &mdash; not criticized, just not seen &mdash; "
     + "what would it be? And what would you have needed from me in that moment?",
     "One moment. Named carefully. Heard without defending. This is the question "
     + "that goes to the center of what both Ambassadors carry."),
    ("profile-aware",
     "When you are in Plea &mdash; when you are giving harder and faster to try "
     + "to close a gap you cannot name &mdash; what is one thing you wish I would "
     + "do or say that would actually help you stop?",
     "You both know the mechanism now. Ask each other for what would actually help "
     + "in the room, in real time, when the ledger is running."),
    ("theological",
     "What is one thing you have been carrying lately &mdash; a need, a longing, "
     + "something you have wanted from me &mdash; that you have not yet asked for "
     + "directly, and what has kept you from asking?",
     "Not an accusation. An invitation. Hear the answer without immediately "
     + "offering to meet the need. Receive the asking first."),
]

ROUND_6 = [
    ("blessing",
     "Place your hand on your spouse's hand. Say their name. Then say: "
     + "'You do not have to give me anything right now. I am glad you are here. "
     + "I receive you.' Say it slowly. Let them say it back.",
     "You may feel the Ambassador in you resist this &mdash; may want to add "
     + "something, to offer something, to make it more. Do not. Let the sentence "
     + "be enough. It is enough."),
    ("prayer",
     "Pray for each other &mdash; not silently, not generally, but out loud "
     + "and by name. One sentence is enough. Pray for the thing they just told "
     + "you in Round Five.",
     "The closing of the date. Do not skip. Two Ambassadors who pray for each "
     + "other's actual needs &mdash; not each other's giving, but each other's "
     + "longing &mdash; have done something the mechanism alone cannot do."),
]


def _render(text, name_a, name_b):
    return text.format(name_a=name_a, name_b=name_b)


def build(sub_a, sub_b) -> bytes:
    """Generate the Ambassador+Ambassador couples walkthrough PDF.

    sub_a: the submission of one Ambassador spouse
    sub_b: the submission of the other Ambassador spouse

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
        "A counselor\u2019s read of two ledgers<br/>and the love that was there before either was opened.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("PREPARED FOR", S["CoverProfileLabel"]))
    story.append(Paragraph(f"{name_a} &nbsp;&amp;&nbsp; {name_b}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_a.upper()}</b></font><br/>"
                "Ambassador &middot; Plea / Attorney<br/>"
                f"<font size=9 color='#6b6862'>Disconnection &middot; Am I lovable?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_b.upper()}</b></font><br/>"
                "Ambassador &middot; Plea / Attorney<br/>"
                f"<font size=9 color='#6b6862'>Disconnection &middot; Am I lovable?</font>",
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
        "<i>\u201cLove keeps no record of wrongs.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "1 Corinthians 13:5",
        ParagraphStyle("cqa", fontName="Inter", fontSize=9, leading=14,
                       textColor=MUTED, alignment=TA_CENTER)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: OPENING ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "The warmest-looking marriage in the room.",
                   "Why this pairing exists, and what you are both about to read.")
    for p in OPENING:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 2: YOUR TWO SHAPES ──
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TWO SHAPES",
                   "Side by side, on paper.",
                   "Two profiles that look alike \u2014 and the single question they share.")
    for p in TWO_SHAPES_INTRO:
        story.append(Paragraph(R(p), S["BodyJ"]))
    side_by_side = Table(
        [[
            _profile_card(S, name_a, ACCENT,
                          "Disconnection", "Am I lovable?",
                          "The Ambassador", "The Plea / Attorney"),
            "",
            _profile_card(S, name_b, ACCENT_HER,
                          "Disconnection", "Am I lovable?",
                          "The Ambassador", "The Plea / Attorney"),
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
                   "A witness who already knows the cost of the giving.")
    for p in GIFT_TO_A:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4: GIFT B TO A ──
    section_header(story, S, f"SECTION FOUR  \u00b7  {name_b.upper()}\u2019S GIFT TO {name_a.upper()}",
                   f"What {name_b} gives {name_a}.",
                   "A person who will still come toward you when the giving has stopped.")
    for p in GIFT_TO_B:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5: THE COLLISION ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Two ledgers, kept simultaneously.",
                   "The small repeating rock, named.")
    for p in COLLISION[:4]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The accounting, in slow motion.",
                   "And the way out, for each of you in your own grammar.")
    for p in COLLISION[4:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6: THE HARDER PICTURE ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When both Ambassadors are in Plea at once.",
                   "The feast of unfelt love, and what to do while you can still see it.")
    for p in BOTH_BREAK[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do, while you can still see it.",
                   "Three practices for the loop, in order.")
    for p in BOTH_BREAK[5:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 7: COMMITMENTS ──
    section_header(story, S, "SECTION SEVEN  \u00b7  COMMITMENTS",
                   "Eight small daily practices.",
                   "Four from each of you. Lead with receiving, not giving.")
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
        "You do not have to give me anything right now.<br/>"
        "I am glad you are here.<br/>"
        "I receive you.",
        closing_style))

    doc.build(story)
    return finalize_buffer(buf)


# ── STANDALONE TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "AMB"
        primary_breakdown = "PLEA"
        primary_trigger = "DISC"
        core_question = "LOV"
        name = "Eleanor"

    class FakeSubB:
        primary_mechanism = "AMB"
        primary_breakdown = "ATTY"
        primary_trigger = "DISC"
        core_question = "LOV"
        name = "Daniel"

    pdf_bytes = build(FakeSub(), FakeSubB())
    out_path = os.path.join(os.path.dirname(__file__), "ambassador_ambassador_test.pdf")
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

    print(f"DONE: ambassador_ambassador.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Output:   {out_path}")
    print(f"Pages: {page_count}")
    print(f"Section Three snippet: {snippet}")
