"""Couples Walkthrough — Ambassador + Vault.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where one spouse is an Ambassador and the
other is a Vault. First names are substituted from the submissions:
    {name_amb}   -> the Ambassador spouse's first name
    {name_vault} -> the Vault spouse's first name

Pastoral dynamic: The Ambassador brings warmth toward the other person's
interior; the Vault keeps the interior locked away from warmth. The Ambassador
reaches — asking, attending, drawing out — and the Vault experiences each
reach as a small invasion. The Ambassador experiences each gentle deflection
as evidence they are not being loved in return.
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


# ──────────── PROSE — uses {name_amb} and {name_vault} placeholders ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small "
    "repeating ones &mdash; the same disappointment in slightly different clothes, "
    "three or four times a week, year after year, until both people have forgotten "
    "what they were originally hoping for.",

    "What follows is a counselor's read of the small repeating rocks in your "
    "particular marriage. Not the dramatic failures, which you would have addressed "
    "already. The small ones. The ones that happen on an ordinary Wednesday evening "
    "when {name_amb} asks how {name_vault}'s day was, and something in the air "
    "changes, and neither of you quite understands why the question cost what it "
    "cost. The ones that accumulate in the margins of an otherwise good life.",

    "You are both reading this because you have decided to look at those rocks. "
    "That decision is more significant than it seems. Most couples spend a lifetime "
    "navigating around them without naming them. Naming them is half the work.",

    "Here is what this document is going to do. It will name what each of you "
    "brings the other that you could not have built alone &mdash; the genuine, "
    "theological gift of your two shapes placed next to each other. Then it will "
    "name the collision: the specific, predictable place where your two mechanisms "
    "produce the same recurring friction. Then it will name the worst case &mdash; "
    "the moment when {name_amb}'s Flood and {name_vault}'s Ghost or Mask are in "
    "the room at the same time &mdash; and what to do then. Then it will hand each "
    "of you a set of commitments, not as rules, but as the kind of small daily "
    "practices that, over years, change the temperature of a home.",

    "Read it together, if you can. If not, read it separately and then sit down "
    "with it. Argue with what does not fit. Stay with what does. The goal is not "
    "insight; it is a marriage in which the Ambassador's reach is received as the "
    "gift it is, and the Vault's interior is offered as the gift it is &mdash; and "
    "both of you find, over time, that being known is less dangerous than you feared.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, "
    "on paper, side by side. Most couples never see their two profiles next to each "
    "other. You are about to.",
]

TWO_SHAPES_BODY = [
    "{name_amb}, you are an <b>Ambassador</b> whose body reads disconnection as an "
    "alarm and whose deepest question is whether you are lovable. You have organized "
    "much of your life around being the warm one in the room &mdash; the one who "
    "notices when someone is left out, who asks the follow-up question, who manages "
    "the emotional temperature so that the people around you stay connected. When "
    "the connection fails anyway, an <b>Attorney</b> takes the floor with a ledger "
    "no one knew was being kept.",

    "{name_vault}, you are a <b>Vault</b> whose body reads shame as an alarm and "
    "whose deepest question is whether you are acceptable. You have organized much "
    "of your life around the careful management of what crosses the threshold between "
    "your interior and the world. The finished conclusion is safe to show; the messy "
    "middle stays inside. When the wound is too large to file, an <b>Attorney</b> "
    "opens the Vault &mdash; not with heat, but with organized, dated documents that "
    "your spouse did not know existed.",

    "Notice what these two profiles share and what they do not. You are not asking "
    "the same question. {name_amb} is asking <i>am I lovable?</i> &mdash; a question "
    "that runs outward, toward the other person, always checking whether the warmth "
    "is flowing back. {name_vault} is asking <i>am I acceptable?</i> &mdash; a "
    "question that runs inward, checking whether what is inside will survive "
    "inspection if it is ever brought out. Both questions are ancient. Both are "
    "answered, finally, only by the gospel. And in the daily mechanics of your "
    "marriage, they pull in almost exactly opposite directions.",

    "What they share underneath is more important. Both of you are people who have "
    "learned to live with a level of vigilance that most of the world does not "
    "require. {name_amb} is vigilant about whether the connection is intact. "
    "{name_vault} is vigilant about whether the interior is secure. You are asking "
    "different questions in different directions, but underneath both is the same "
    "ache: <i>am I safe to be fully known, as I actually am, by the person I chose?</i>",

    "This pairing is not uncommon, and there is a reason it forms. The Ambassador "
    "is drawn to the Vault's depth and composure &mdash; the sense that here is "
    "someone with a rich interior, someone who does not scatter themselves carelessly. "
    "The Vault is drawn to the Ambassador's warmth &mdash; the sense that here is "
    "someone who will receive whatever the interior eventually offers. The attraction "
    "is real, and the foundation is genuinely good. What neither quite saw at the "
    "beginning is that the Ambassador's reach and the Vault's lock were going to "
    "meet each other, repeatedly, in the kitchen.",
]

GIFT_TO_VAULT = [
    "{name_amb} gives {name_vault} something the Vault has been longing for without "
    "quite knowing it: <b>a persistent invitation to be known.</b>",

    "The Vault's question is <i>Am I acceptable?</i> &mdash; and the Vault has "
    "answered it alone, for years, by managing the interior carefully enough that "
    "exposure never quite becomes a risk. The tragedy of this strategy is that it "
    "prevents the only answer that could finally satisfy the question. The Vault "
    "cannot discover that its interior is acceptable until someone actually sees "
    "the interior. And the Vault cannot let anyone see the interior until it "
    "discovers that the interior is acceptable. The loop is closed from the inside.",

    "{name_amb}, by virtue of being an Ambassador, will not stop knocking. Not "
    "intrusively, not with impatience &mdash; but with the patient, warm, recurring "
    "invitation of a person who genuinely wants to know. You ask how {name_vault} "
    "is doing, not as a social formality, but because you actually want to know. "
    "You notice when something in the room changes. You create the conditions "
    "&mdash; a quieter evening, a moment with no agenda, a direct and unhurried "
    "question &mdash; in which the Vault could, if it chose, say something true "
    "about what is actually inside.",

    "The theological word for what {name_amb} gives {name_vault} is <i>pursuit.</i> "
    "It is the oldest biblical image of grace: the God who does not wait for the "
    "Vault to get its interior organized before he comes looking. The father in "
    "Luke 15 does not wait at the door with crossed arms. He runs down the road. "
    "The Ambassador, in loving the Vault, is participating &mdash; imperfectly, "
    "humanly, but really &mdash; in this motion. You run down the road toward an "
    "interior the Vault has been guarding, and you do not stop running because "
    "the door is often still closed when you arrive.",

    "{name_vault} &mdash; if you want to thank {name_amb} for something this week, "
    "thank them for this. The reaching that has sometimes felt like pressure is "
    "also, from another angle, the evidence that your interior is worth pursuing. "
    "Most people who encounter a locked door eventually stop knocking. {name_amb} "
    "has not stopped. That persistence is not a character flaw. It is a form of "
    "love that does not require a reward to continue.",

    "{name_amb} &mdash; what {name_vault} receives from you, when you ask again "
    "and attend again and create the quiet space again, is the slow, accumulating "
    "evidence that someone in the world believes what is inside the Vault is worth "
    "the effort of opening it. {name_vault} may not say this. The Vault rarely "
    "does. But the evidence is being filed. It is working.",
]

GIFT_TO_AMB = [
    "{name_vault} gives {name_amb} something the Ambassador has rarely received: "
    "<b>depth without performance.</b>",

    "The Ambassador has spent most of life being the one who provides warmth &mdash; "
    "the one who manages emotional temperature, who reads the room, who notices "
    "and attends and gives. Most of the people in the Ambassador's life have "
    "received this warmth without much question, because receiving warmth is "
    "easier than providing it. But the Ambassador is, underneath the giving, "
    "asking a question: <i>is anyone going to attend to me, the way I attend to "
    "everyone else?</i>",

    "The Vault, when it finally opens, gives {name_amb} something genuinely rare: "
    "access to a rich, carefully considered interior that has not been scattered "
    "casually across every available relationship. What the Vault offers, when it "
    "offers anything, is precise and real. It has been thought about. It is not "
    "performance; it is the actual thing, brought out deliberately. When {name_vault} "
    "tells {name_amb} something true about what is inside &mdash; a fear, a "
    "struggle, a moment of wonder &mdash; it is not casual disclosure. It is trust. "
    "It is the most specific kind of intimacy.",

    "There is a related gift that the Vault gives the Ambassador without either "
    "of them quite naming it. The Vault is not easily overwhelmed by the "
    "Ambassador's warmth. While others sometimes feel the weight of the "
    "Ambassador's giving &mdash; the slight pressure of a love that needs to be "
    "received &mdash; the Vault receives what is given and processes it quietly "
    "and does not make {name_amb} feel like too much. The Vault's composure is "
    "a kind of steadiness that the Ambassador does not always find elsewhere.",

    "The theological word for what {name_vault} gives {name_amb} is <i>substance.</i> "
    "J. I. Packer, writing on the nature of genuine friendship in the Christian "
    "life, observed that the rarest form of intimacy is not the kind that comes "
    "easily but the kind that is offered deliberately, from a person who has "
    "counted the cost of offering it. When the Vault opens the door, even a "
    "little, the Ambassador receives something that has been considered and chosen. "
    "That is not a small thing.",

    "{name_amb} &mdash; if you want to thank {name_vault} for something this week, "
    "thank them for one specific moment of disclosure, however small, in which "
    "you saw something real. Not the moment you wished had happened. The moment "
    "that did. {name_vault} brought that to you deliberately. It cost something. "
    "Name that you received it.",

    "{name_vault} &mdash; what {name_amb} is receiving from you, when you allow "
    "even a small degree of access to your interior, is more than you know. "
    "The Ambassador has been giving warmth to many rooms for a long time. What "
    "the Ambassador most needs, and finds most rarely, is not more warmth returned "
    "but genuine depth encountered. You are, when you open even slightly, "
    "providing exactly that.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you, "
    "even if you have not put words to it.",

    "{name_amb}'s primary mode of love is <i>bringing warmth toward the other "
    "person's interior</i>. To the Ambassador, love is relational and active and "
    "directed: it reaches, asks, attends, draws out, notices, provides. When "
    "{name_amb} loves {name_vault}, the love looks like questions &mdash; about "
    "the day, about the mood that seems to have changed, about the thing that "
    "went quiet. To {name_amb}, these questions are not interrogation. They are "
    "the form love takes. They are how the Ambassador says <i>you matter to me.</i>",

    "{name_vault}'s primary survival strategy is <i>keeping the interior locked "
    "away until the Vault has chosen to open it</i>. To the Vault, access to the "
    "interior is something that is given by choice, not drawn out by another "
    "person's asking. The Vault processes privately, arrives at a finished "
    "conclusion, and then &mdash; when trust has been established and the moment "
    "feels right &mdash; discloses what it has decided to disclose. To {name_vault}, "
    "this is not withholding. It is dignity. It is the way the Vault maintains "
    "the one thing that feels reliably safe: the managed interior.",

    "Here is what happens when these two modes meet. {name_amb} asks how {name_vault} "
    "is doing. {name_vault} gives a finished answer &mdash; brief, composed, "
    "adequate. {name_amb} senses that there is something behind the finished "
    "answer &mdash; the Ambassador is good at reading rooms &mdash; and asks a "
    "follow-up question. {name_vault} experiences the follow-up as pressure: "
    "<i>I already gave an answer. Why are you not accepting it?</i> The Vault "
    "gives a slightly shorter response. {name_amb} reads the shorter response as "
    "evidence that the connection is receding, and the disconnection trigger fires: "
    "<i>am I losing them? Is it me?</i> The Ambassador presses a little more. "
    "The Vault withdraws a little more. Within ten minutes, both of you are "
    "frustrated, neither of you fully understands what just happened, and the "
    "kitchen has gone cold.",

    "This is the collision, and it is worth naming carefully because both of you, "
    "in this sequence, are operating in good faith. {name_amb} is not trying to "
    "be intrusive; the reach is the form love takes. {name_vault} is not trying "
    "to be withholding; the managed disclosure is the form dignity takes. Neither "
    "of you is doing anything wrong in your own grammar. The tragedy is that your "
    "grammars are, at exactly this point, opposites.",

    "There is a pastoral word from Scripture that belongs here. Proverbs 25:11 "
    "says: <i>A word fitly spoken is like apples of gold in a setting of silver.</i> "
    "The image is not of more words or fewer words. It is of the right word at the "
    "right time &mdash; the word that neither demands more than the moment can hold "
    "nor retreats from the moment when the moment is asking for something real. "
    "The Ambassador must learn that not every act of love is reception; sometimes "
    "it is intrusion in the costume of care. The Vault must learn that not every "
    "reach is a demand for exposure; sometimes it is the cost of marriage, and "
    "must be answered, even when the answering costs something.",

    "The Apostle Paul, writing to the church in Ephesus, says: <i>speaking the "
    "truth in love, we are to grow up in every way into him who is the head, "
    "into Christ.</i> (Ephesians 4:15) The phrase has two movements that belong "
    "together: truth and love. Truth without love is prosecution. Love without "
    "truth is management. The Ambassador must learn to give the Vault the gift "
    "of a question that does not press for more than the Vault has chosen to give. "
    "The Vault must learn to give the Ambassador the gift of something more than "
    "the finished answer &mdash; one unresolved thing, offered while it is still "
    "unresolved, trusted to the person who will not mock the mess.",

    "Here is the way out, for each of you in your own grammar. {name_amb}, when "
    "{name_vault} gives you a composed, brief answer, the translation is almost "
    "never <i>I do not trust you.</i> It is more likely: <i>I have not yet "
    "finished processing this, and I do not yet know what to bring you.</i> The "
    "right move is not a third question. It is one sentence &mdash; <i>I am here "
    "when you are ready</i> &mdash; and then the willingness to wait. The Vault "
    "does not respond well to pressure, but it responds deeply to patience.",

    "{name_vault}, when {name_amb} asks a follow-up question after you have already "
    "answered, the translation is almost never <i>they do not trust my answer.</i> "
    "It is: <i>I love you and I can feel that something is happening and I do not "
    "want to be on the other side of a closed door from you.</i> The right move is "
    "not a shorter answer. It is one more thing &mdash; one sentence that is "
    "slightly more interior than the finished conclusion. <i>I am still thinking "
    "about something, but I am not ready to talk about it yet.</i> That one "
    "sentence costs the Vault very little and gives the Ambassador what it actually "
    "needs: not the full interior, but evidence that the interior exists and that "
    "you trust {name_amb} enough to say so.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be moments &mdash; not often, but they "
    "will come &mdash; when the small collision in the kitchen escalates and both "
    "of you are in the breakdown at the same time. For this particular pairing, "
    "the breakdown has a specific shape, and it is important to name it clearly "
    "so you can both see it from the outside before it is happening to you from "
    "the inside.",

    "Here is what is happening when the loop is fully running. {name_amb}'s "
    "disconnection trigger has been firing for some time &mdash; days, perhaps, "
    "or weeks &mdash; and the Ambassador has been doing what the Ambassador always "
    "does: giving more, asking more warmly, attending more carefully, trying to "
    "restore the connection by making it impossible to refuse. The ledger has been "
    "open, though neither of you knew it. The entries have been accumulating: "
    "<i>I asked how you were and you gave me two words. I made space for a real "
    "conversation and you changed the subject. I have been reaching for you and "
    "you have been locked.</i>",

    "And then something tips. The Flood arrives &mdash; not cold, but with heat, "
    "with the specific texture of a person who has been quiet about something "
    "real for too long. The ledger opens, and what comes out is not one grievance "
    "but the accumulated weight of many. James, in his epistle, asks: <i>What "
    "causes quarrels and what causes fights among you? Is it not this, that your "
    "passions are at war within you?</i> (James 4:1-3) The Ambassador's Flood is "
    "exactly this: a war that has been running inside, quietly, under the warmth, "
    "finally breaking the surface.",

    "{name_vault}, when the Flood is in the room, your instinct is not to match "
    "it. The Vault does not flood. The Vault does something more disorienting: it "
    "disappears. The Ghost retreats from the room, or the Mask appears &mdash; "
    "a composed, managed, unreachable version of {name_vault} that is present in "
    "body but absent in every other sense. You may go quiet. You may become "
    "formal. You may leave the room. You may stay and say nothing real. From "
    "inside the Vault, this is self-protection. From inside the Flood, it is "
    "abandonment.",

    "Bonhoeffer writes, in <i>Life Together</i>: <i>He who is alone with his "
    "sin is utterly alone.</i> The Vault has been alone with its interior &mdash; "
    "its accumulated wounds, its filed grievances, its organized list of the times "
    "the Ambassador's reach felt like too much &mdash; and the aloneness has made "
    "what is inside grow larger than it was when it first arrived. The Ghost and "
    "the Mask are not indifference. They are the Vault's version of the same "
    "aloneness &mdash; a retreat into the interior that feels like safety and "
    "functions like isolation.",

    "What happens next follows a predictable pattern. The Ambassador floods; the "
    "Vault retreats; the Ambassador floods harder because the retreat confirms the "
    "disconnection; the Vault retreats further because the flood confirms that "
    "opening is dangerous. Both of you are, in this loop, being proven right "
    "about your worst fears. {name_amb} is learning that giving is not enough "
    "to keep the connection. {name_vault} is learning that the interior, when "
    "under pressure, is not safe to show. The loop is not a moral failure on "
    "either side. It is the predictable arithmetic of two wounded people whose "
    "mechanisms were not built to find each other gracefully.",

    "What to do, when you can still see what is happening:",

    "<b>One of you, not both, calls the pause.</b> Whichever one notices first "
    "says, out loud: <i>this is the loop. Twenty minutes.</i> Not as a withdrawal "
    "of love. Not as a postponement of the real conversation. As a recognition "
    "that neither of you currently has access to the more thoughtful person you "
    "were this morning, and that the conversation you need requires that person "
    "to be available.",

    "<b>In the twenty minutes, do not draft the next statement. Pray.</b> "
    "{name_amb}: pray for {name_vault} by name. Not for them to open up. For them "
    "to feel safe. <i>Lord, the Vault is locked right now because it is afraid. "
    "Help {name_vault} to know that the interior is not dangerous with me.</i> "
    "{name_vault}: pray for {name_amb} by name. Not for them to stop pressing. "
    "For them to feel found. <i>Lord, the Ambassador is flooding right now because "
    "disconnection feels like abandonment. Help {name_amb} to know that I am "
    "still here, even when the door is closed.</i>",

    "<b>When you come back, each of you brings one sentence.</b> {name_amb}: not "
    "the ledger. One true sentence about the specific wound underneath the Flood. "
    "<i>I felt invisible when you did not answer me last Tuesday, and I have been "
    "carrying that.</i> {name_vault}: not the Ghost. One true sentence about "
    "something real. <i>I was overwhelmed and I went inside, and I know that cost "
    "you something.</i> One sentence each. Then stop. The marriage can sustain one "
    "true sentence from each of you. It is less certain it can sustain the full "
    "prosecution and the full retreat in the same room.",

    "<b>Neither of you is the problem.</b> The Flood and the Ghost are old "
    "mechanisms doing the only job they were ever taught to do. The truest thing "
    "about both of you is that you are a man and a woman who have chosen, in the "
    "small grace of an ordinary evening, to keep coming back to each other. That "
    "is what marriage is. The loop will run. It will run less, and shorter, as "
    "both of you practice the one-sentence return.",
]

COMMITMENTS_INTRO = [
    "What follows are commitments &mdash; four from {name_amb}, four from {name_vault}. "
    "They are not vows in the legal sense. They are the small daily practices that, "
    "offered to each other freely over months and years, change the temperature of "
    "a home. Read each one slowly. If one of you cannot say a particular commitment "
    "in good faith yet, do not say it. Say which one it is, and why, and that "
    "conversation will be worth more than a dozen commitments spoken without honesty.",
]

AMB_COMMITMENTS = [
    ("I will distinguish my reach from my need.",
     "{name_vault}, I commit to learning the difference between asking because I love "
     "you and asking because I am afraid you are gone. When I ask how you are and you "
     "give me a composed answer, I will practice receiving that answer as enough for "
     "this moment &mdash; not because I am giving up on knowing you, but because love "
     "that does not press is also love. I will not interpret a closed door as a verdict "
     "against my love."),

    ("I will wait without withdrawing.",
     "{name_vault}, when you tell me you are not ready to talk about something yet, "
     "I commit to saying one true sentence in return &mdash; <i>I am here when you "
     "are</i> &mdash; and then letting you come to me on your own time. I will not "
     "make my waiting into pressure. I know that you are not absent from me when the "
     "door is closed. I am learning to know it."),

    ("I will name the wound before it enters the ledger.",
     "{name_vault}, when the disconnection signal fires, I commit to naming it within "
     "the same day it happens &mdash; in one sentence, without the accumulated weight "
     "of the week. Not as a brief. As a wound. <i>I felt invisible in that moment, "
     "and I need you to know that.</i> The ledger that I did not know I was keeping "
     "is the thing I am most committed to closing, one entry at a time."),

    ("I will receive what you give without asking for more.",
     "{name_vault}, when you bring me something from your interior &mdash; a fear, "
     "a thought, an unfinished thing &mdash; I commit to receiving it as the gift "
     "it is, without immediately asking a follow-up question. What you offer is "
     "chosen. It cost something. I will let it land before I reach for more."),
]

VAULT_COMMITMENTS = [
    ("I will let you in one more inch today than I am comfortable with.",
     "{name_amb}, I commit to disclosing one thing each week that is not yet resolved "
     "&mdash; something I am still thinking about, something I have not yet organized "
     "into a finished conclusion. I will not wait until the interior is presentable "
     "before I bring you in. You married me, not my curated conclusions. I want you "
     "to know the one who does the curating."),

    ("I will answer the reach, even when it costs.",
     "{name_amb}, when you ask how I am, I commit to giving you something more than "
     "the managed answer, at least once each day. It may be small. <i>I am more "
     "tired than I expected.</i> <i>Something is sitting with me and I am not ready "
     "to name it yet, but I wanted you to know it is there.</i> You deserve to know "
     "the interior exists, even when the door is not fully open."),

    ("I will not file what can be spoken.",
     "{name_amb}, I commit to bringing wounds while they are still fresh enough to "
     "repair, rather than organizing them into the file. When something lands on "
     "me that involves you, I will try to say so within two days, before the "
     "document has been dated and cross-referenced. The file I did not know I was "
     "keeping is the thing I am most committed to deaccessioning, one entry at a time."),

    ("I will trust the pursuit as love.",
     "{name_amb}, I commit to retraining the part of me that reads your follow-up "
     "question as pressure. When you ask a second question after I have answered "
     "the first, I will try to remember, before I go shorter, that you are asking "
     "because you want to be near me. The reach is the love. I am learning to "
     "receive it as such."),
]

PRAYER = [
    "Father,",

    "You set us next to each other, and you knew exactly what you were doing. "
    "You knew the Ambassador would reach for the Vault. You knew the Vault would "
    "keep the door locked longer than the Ambassador could easily bear. You knew "
    "the Flood would come, and the Ghost would come, and the kitchen would go cold "
    "on ordinary evenings. You knew all of it before either of us said yes.",

    "Teach us the grammar of each other. Teach {name_amb} that not every act of "
    "love is reception &mdash; that sometimes the most loving thing is a patient "
    "question left unasked, a space held open without filling it, a willingness "
    "to wait at the door without pressing the handle. And teach {name_amb}, in "
    "that same patience, to know that {name_vault}'s locked door is not a verdict. "
    "It is a history. It is the residue of a real wound. It is not the last word "
    "about what is possible between them.",

    "Teach {name_vault} that the reach of the Ambassador is not a demand for "
    "exposure. It is pursuit. It is the human form of the love that ran down the "
    "road before the returning son had composed his speech. Teach {name_vault} "
    "to open the door one more inch today than feels comfortable &mdash; not "
    "because the interior has been sufficiently organized, but because the person "
    "on the other side of the door has earned the right to more than the finished "
    "version.",

    "When the Flood comes in {name_amb}, remind them that the ledger was never "
    "theirs to keep &mdash; that you are the Advocate who has already seen every "
    "entry and has spoken the only verdict that finally counts. When the Ghost "
    "or the Mask comes in {name_vault}, remind them that the interior they are "
    "protecting has already been fully seen by you, and you have not turned away. "
    "<i>There is therefore now no condemnation for those who are in Christ Jesus.</i> "
    "Let that answer both questions. Let it answer <i>am I lovable?</i> and "
    "<i>am I acceptable?</i> &mdash; not with flattery, but with the settled "
    "verdict of the One who gave everything to make it true.",

    "Make our home a room in which the Ambassador does not have to flood to be "
    "heard, and the Vault does not have to hide to be safe. Make our table a "
    "place where the unfinished thing is welcomed, and the one who reaches is "
    "received. And when we are old and the mechanisms have grown quieter, let "
    "us look back and see that the small repeating rocks became smaller, and "
    "less repeating, and finally a part of the landscape we can both laugh at "
    "together.",

    "In the name of the One who pursued us when we were locked, and who waits "
    "for us still, with the door already open.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages "
    "that follow are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, "
    "somewhere quiet, with no children in the room and no phones on the table. "
    "There are six rounds, and they build on each other. Resist the temptation "
    "to skip ahead. Start at Round One even if it feels too light; the lightness "
    "is the point. Round Five will be there when you arrive, and it will land "
    "differently because you came through the first four.",

    "Some of the questions are playful. Some are direct. A few are the kind of "
    "questions that, when answered honestly, will sit with you for a week. None "
    "of them are trivia. All of them are an invitation.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did "
    "not read answers first, in full, without interruption. Then the reader "
    "answers the same question. Then you move on. You do not have to finish all "
    "six rounds in one evening &mdash; two or three rounds, taken seriously, is "
    "often better than racing through all of them. Save the rest for the next "
    "date night.",

    "<b>One rule.</b> The other person's answer is never wrong. You may not love "
    "everything you hear. Stay with it. The point of this is not to grade each "
    "other's answers. The point is to be known, and to do the work of knowing.",
]

ROUND_1 = [
    ("hypothetical",
     "If our marriage were a piece of music, what genre would it be, and what "
     "would the title of the album be?",
     "Let the metaphor work. Answer with the first thing that comes to mind, then "
     "say one sentence about why."),
    ("observation",
     "What is something I did this week that you noticed and did not comment on?",
     "Not a complaint. A small noticing. The fact that you noticed at all is the gift."),
    ("playful",
     "If you had to describe our marriage in exactly three words &mdash; not the "
     "best three, just the most honest three &mdash; what would they be?",
     "All three words. Then explain the one you are least certain about."),
]

ROUND_2 = [
    ("fill-in-blank",
     "I don't think I tell you often enough &mdash; I am genuinely amazed at the "
     "way God made you so _______. Your _______ is something I would not want to "
     "build this life without.",
     "Two blanks. Be specific. 'Kind' is too easy. 'Patient with me when I reach "
     "and you are not ready' is closer."),
    ("observation",
     "What is one thing you have watched me do this year that you wish more people "
     "in our lives got to see?",
     "Not the public version of who I am. The private one. The one you see."),
    ("one-word",
     "If you had to choose one word to describe what it feels like when I reach "
     "for you &mdash; when I ask how you are and I actually want to know &mdash; "
     "what word would it be?",
     "One word, said out loud. Then say one sentence about when you feel that most."),
]

ROUND_3 = [
    ("forward-looking",
     "Five years from now, when we look back on this season of our marriage, what "
     "do you hope we will say we learned to do differently?",
     "Not what you wish you had done. What you want, when you look back, to have "
     "actually changed."),
    ("theological",
     "Where, in the last month, have you seen God specifically at work in me "
     "&mdash; not in who I want to be, but in who I actually was?",
     "Name it specifically. The work you have already witnessed. Not the work "
     "you are hoping for."),
    ("shared-identity",
     "Finish this sentence three times: 'We are the kind of couple who _______.' "
     "Give one playful answer, one true answer, and one aspirational answer.",
     "The 'we' is the point. All three must be honest."),
]

ROUND_4 = [
    ("strength",
     "What is one thing I do for you that you would have to learn to do for "
     "yourself, or go without, if I were not here?",
     "Hard to ask. Important to hear the answer. Stay with it without deflecting."),
    ("fill-in-blank",
     "One of the gifts of being married to you is that I get to be _______ in "
     "ways I would not have been on my own. You make that version of me possible.",
     "A version of yourself that only exists because this marriage exists. Name it "
     "specifically."),
    ("observation",
     "Name one moment in our story &mdash; one specific scene, not a category of "
     "moments &mdash; when you knew we had built something together that neither of "
     "us could have built alone.",
     "Tell the whole story. Take your time. The remembering is part of the "
     "strengthening."),
]

ROUND_5 = [
    ("hard",
     "When I reach for you and you feel the door close &mdash; or when you reach "
     "and I do not quite open &mdash; what is the one word for what happens inside "
     "you in that moment?",
     "One word. Said carefully. Then let it sit before you explain it."),
    ("profile-aware",
     "{name_amb}, what would help you most in the moment when you feel the "
     "disconnection signal fire &mdash; not tomorrow, but right then, in that "
     "moment? And {name_vault}, what would make it easier to open the door one "
     "more inch than feels comfortable?",
     "You both know the mechanisms now. Ask each other for what would actually help. "
     "Not the ideal. The doable."),
    ("theological",
     "What is one thing you have been carrying lately that you have not brought "
     "to me yet, and what has kept you from bringing it?",
     "Not an accusation. An invitation. The other person's answer is a gift. "
     "Receive it without defending."),
]

ROUND_6 = [
    ("blessing",
     "Place your hand on your spouse's hand. Look at them. Say their name. "
     "Then say: 'I do not need you to be open before I love you. I do not need "
     "you to stop reaching before I trust you. You are enough, as you are, right "
     "now.' Say it slowly. Let them say it back.",
     "You may feel uncertain about it. That is part of why it works. Do it anyway."),
    ("prayer",
     "Pray for each other &mdash; not silently, not generally, but out loud and "
     "by name. One sentence is enough. Pray for the thing they told you in "
     "Round Five that they have been carrying.",
     "The closing of the date. The most important round. Do not skip it."),
]


def _render(text, name_amb, name_vault):
    return text.format(name_amb=name_amb, name_vault=name_vault)


def build(sub_a, sub_b) -> bytes:
    """Generate the Ambassador+Vault couples walkthrough PDF.

    sub_a: the submission of the Ambassador spouse
    sub_b: the submission of the Vault spouse
    """
    ensure_fonts()
    S = make_styles()

    name_amb = _first_name(sub_a, "Ambassador")
    name_vault = _first_name(sub_b, "Vault")

    def R(text):
        return _render(text, name_amb, name_vault)

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Couples Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUPLES WALKTHROUGH",
        cover_right_label=f"{name_amb.upper()}  +  {name_vault.upper()}",
        title=f"Take 139 Couples Walkthrough \u2014 {name_amb} & {name_vault}",
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
    story.append(Paragraph(f"{name_amb} &nbsp;&amp;&nbsp; {name_vault}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_amb.upper()}</b></font><br/>"
                "Ambassador &middot; Attorney<br/>"
                "<font size=9 color='#6b6862'>Disconnection &middot; Am I lovable?</font>",
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
        "<i>\u201cA word fitly spoken is like apples of gold in a setting of silver.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "Proverbs 25:11",
        ParagraphStyle("cqa", fontName="Inter", fontSize=9, leading=14,
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
            _profile_card(S, name_amb, ACCENT,
                          "Disconnection", "Am I lovable?",
                          "The Ambassador", "The Attorney"),
            "",
            _profile_card(S, name_vault, ACCENT_HER,
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

    # ── SECTION 3: Ambassador's gift to Vault ──
    section_header(story, S, "SECTION THREE  \u00b7  THE AMBASSADOR'S GIFT",
                   f"What {name_amb} gives {name_vault}.",
                   "A persistent invitation to be known.")
    for p in GIFT_TO_VAULT:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4: Vault's gift to Ambassador ──
    section_header(story, S, "SECTION FOUR  \u00b7  THE VAULT'S GIFT",
                   f"What {name_vault} gives {name_amb}.",
                   "Depth without performance.")
    for p in GIFT_TO_AMB:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5: The Collision ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "The reach meets the lock.",
                   "Two spiritual disciplines running in opposite directions.")
    for p in COLLISION[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The word fitly spoken.",
                   "The way out, for each of you in your own grammar.")
    for p in COLLISION[5:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6: The Harder Picture ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When the Flood and the Ghost are in the room at once.",
                   "The specific loop, named plainly.")
    for p in BOTH_BREAK[:6]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do, while you can still see it.",
                   "Three practices for the loop, in order.")
    for p in BOTH_BREAK[6:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 7: Commitments ──
    section_header(story, S, "SECTION SEVEN  \u00b7  COMMITMENTS",
                   "Eight small daily practices.",
                   "Four from each of you. Read each one slowly.")
    for p in COMMITMENTS_INTRO:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"FROM {name_amb.upper()}, TO {name_vault.upper()}", S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name, body in AMB_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(name, S["H3"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_vault}, to {name_amb}.",
                   f"Four commitments, in their voice, for you to receive.")
    story.append(Paragraph(f"FROM {name_vault.upper()}, TO {name_amb.upper()}", S["CommitLabelHer"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT_HER,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for name, body in VAULT_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(name, S["H3Her"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())

    # ── SECTION 8: Prayer ──
    section_header(story, S, "SECTION EIGHT  \u00b7  A PRAYER",
                   "For the two of you.",
                   "Pray it together, if you can. Out loud, if you can.")
    for line in PRAYER:
        story.append(Paragraph(R(line), S["BlockQuote"]))
    story.append(PageBreak())

    # ── SECTION 9: Date Night ──
    section_header(story, S, "SECTION NINE  \u00b7  DATE NIGHT",
                   "Six rounds, taken slowly.",
                   "A conversation designed to be spoken between you, not read about.")
    for p in DATE_NIGHT_OPENING:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    rendered_round = lambda r: [(kind, R(q), note) for (kind, q, note) in r]

    _render_round(story, 1, rendered_round(ROUND_1),
                  "Warm up.",
                  "The lightness is the point. Start here even if you would rather skip ahead.")
    story.append(PageBreak())
    _render_round(story, 2, rendered_round(ROUND_2),
                  "Notice the good.",
                  "Specific praise. The kind that lands because it could only have been said by you.")
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
        "I do not need you to be open before I love you.<br/>"
        "I do not need you to stop reaching before I trust you.",
        closing_style))

    doc.build(story)
    return finalize_buffer(buf)


# ── STANDALONE TEST ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    class FakeSub:
        def __init__(self, mechanism, name):
            self.primary_mechanism = mechanism
            self.name = name

    sub_a = FakeSub("AMB", "Alexandra")
    sub_b = FakeSub("VAULT", "Victor")

    pdf_bytes = build(sub_a, sub_b)
    out_path = os.path.join(os.path.dirname(__file__), "ambassador_vault_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    import io
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        snippet = ""
        for page in reader.pages[2:5]:
            txt = page.extract_text() or ""
            if txt.strip():
                snippet = txt.strip()[:200]
                break
    except Exception:
        page_count = "unknown"
        snippet = ""

    print(f"DONE: ambassador_vault.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
