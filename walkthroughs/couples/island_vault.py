"""Couples Walkthrough — Island + Vault.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where one spouse is an Island and the
other is a Vault. First names are substituted from the submissions:
    {name_isle}  -> the Island spouse's first name
    {name_vault} -> the Vault spouse's first name

Pastoral key: The most invisible couple in the 21. Both mechanisms work
by holding interior life away from the marriage. The Island holds back
without realizing it — thin walls, temperamentally self-contained. The
Vault holds back deliberately, with strategy — thick walls with locks,
installed for a reason. Together they produce a marriage that looks peaceful
from the outside and from the inside has almost nothing actually said.
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


# ──────────── PROSE — uses {name_isle} and {name_vault} placeholders ────────────

OPENING = [
    "Most marriages do not end in a scene. They end in a silence that has been going on so long that neither person can remember exactly when the conversation stopped. There is no dramatic confrontation, no point of rupture that either spouse can identify with precision. There is only the accumulated weight of things that were never quite said, and the slow, mutual recognition that the interior lives of two people who chose each other have been running in parallel, without meeting, for years.",
    "What follows is a counselor's careful read of how this happens in your particular marriage. Not the dramatic failures &mdash; you have either addressed those or they are not what is quietly unmaking you. The quiet thing. The one that is most invisible because it does not look like a problem at all. From the outside, your marriage may look like one of the more peaceful ones in the room. From the inside, both of you know that something has been left mostly unsaid for a very long time, and neither of you is entirely sure when that started or how to change it.",
    "You are both reading this because you have decided to look at that thing. That decision is more significant than it feels right now, because the Island and the Vault both prefer not to look. Looking together &mdash; on paper, before a counselor's voice neither of you can dismiss easily &mdash; is more than half of the work.",
    "Here is what I want to do for you in these pages. I will name what each of you genuinely brings the other that you could not have built for yourselves &mdash; the real gift your two shapes form together. Then I will name the specific way your two mechanisms produce a collision that is slow and nearly invisible. Then I will name the harder picture &mdash; what happens when both of you have gone fully into breakdown at the same time &mdash; and what to do when you can still see it coming. Then I will hand each of you commitments: not resolutions, but the kind of small, concrete daily practices that, kept with patience, begin to change the temperature of a home across months and years.",
    "Read it together if you can. Sit in the same room for it. Argue with what does not fit; stay with what does. And before you begin, hear this clearly: the fact that both of you are reading the same pages, about the same marriage, at the same time, is itself a kind of speech. It says that {name_isle} and {name_vault} have not given up on being known. That is not a small thing. It is, in fact, the very thing this document is designed to move you toward.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on paper, side by side. Most couples never see their two profiles next to each other with this kind of deliberate clarity. You are about to.",
]

TWO_SHAPES_BODY = [
    "{name_isle}, you are an <b>Island</b> whose body reads disconnection and insignificance as an alarm and whose deepest question is <i>am I enough to be remembered?</i> You have learned, over a long time and perhaps without quite deciding to, to process your interior life alone. You are self-contained by temperament &mdash; not because you are afraid of exposure exactly, but because solitude is simply the environment in which you work best. Your walls are not thick, in the way that a fortified structure has thick walls; they are more like the natural distance of a landmass that simply does not have a bridge. When the Island reaches its limit and the contained weight finally breaks through, a <b>Ghost</b> takes the floor &mdash; a withdrawal that becomes nearly invisible, a performing-of-normalcy while the interior quietly empties.",
    "{name_vault}, you are a <b>Vault</b> whose body reads shame as an alarm and whose deepest question is <i>am I acceptable?</i> You keep the messy middle of your interior life private &mdash; not temperamentally but strategically. The Vault has thick walls with locks, and the locks were installed for a reason that was once good and real. You process internally and bring others the finished conclusion; the half-built house, the unresolved grief, the confusion you have not yet organized &mdash; these stay inside, because what has been shown in the past without preparation has sometimes been handled carelessly or used against you. When a wound lands large enough that the Vault cannot contain it, a <b>Ghost</b> takes the floor in you as well &mdash; a silent, composed withdrawal that is impossible to distinguish, from the outside, from simple steadiness.",
    "Notice what this pairing shares, and notice what it does not share. You share the same breakdown: the Ghost. You both, under pressure, go quiet and invisible. But the roads that lead to that common destination are very different. {name_isle} goes quiet because the Island's temperament moves toward solitude the way water moves toward low ground &mdash; without effort, without strategy, simply because that is the shape of the land. {name_vault} goes quiet because the Vault has made a decision, however unconscious, that quiet is safer than seen.",
    "That distinction &mdash; temperamental distance versus protective distance &mdash; is the pastoral key to everything that follows. The Island holds back without fully realizing that holding back is what is happening. The Vault holds back with awareness, with effort, with a specific fear driving the decision. These are not the same thing, and conflating them will make repair impossible. {name_isle}, you are not withholding strategically. {name_vault}, you are. Neither of these is a moral failure. Both of them, together, in the same marriage, produce a relationship in which almost nothing interior is ever actually exchanged.",
    "And yet you chose each other. The Island is drawn to the Vault's composure &mdash; a person who does not scatter their interior on every available surface, who processes before speaking, who does not need to be managed. The Vault is drawn to the Island's self-containment &mdash; a person who makes no demand on the Vault's interior, who does not press for access, who respects the distance instinctively. You recognized, before you had words for it, that this person would not require from you what has cost you in the past. What you did not quite anticipate is that two people who never require each other's interior can produce a marriage in which neither is ever fully given.",
]

GIFT_TO_VAULT = [
    "{name_isle} gives {name_vault} something most people who love the Vault will eventually stop giving: <b>a room with no inspection.</b>",
    "The Vault's deepest fear &mdash; the one underneath the question <i>am I acceptable?</i> &mdash; is a specific kind of scrutiny. Not criticism necessarily, but the gaze itself. The sense of being studied, assessed, found in an unfinished state. The Vault has learned that the safest response to this possibility is to curate what is shown: to bring people the finished product rather than the working draft, the resolved conclusion rather than the open question.",
    "{name_isle}, by virtue of being an Island, does not study {name_vault}. The Island is not, by temperament, a gazing person. The Island respects the interior because the Island has an interior of its own that it treats as sovereign. {name_vault} can be in the same room as {name_isle} without experiencing the surveillance that has historically preceded exposure. This is rarer than it sounds. Most people who love the Vault eventually, with great tenderness, begin pressing at the walls. The Island, almost uniquely, does not.",
    "There is a theological word for what {name_isle} gives {name_vault}, and it is something close to <i>sanctuary</i>. Not the false sanctuary of a relationship that does not care enough to look; the genuine sanctuary of a person who has a deep enough interior life of their own that the Vault's privacy does not read to them as a problem to be solved. The Vault can exist, in the Island's company, without being required to perform a finished self. That is, for the Vault, one of the rarest experiences in a life that has otherwise been organized around presentation.",
    "{name_vault} &mdash; if you want to thank {name_isle} for something this week, thank her for the room she does not enter. She may not know she is giving you this. Islands rarely know that their non-intrusion is a gift; they have simply been doing what comes naturally. Tell her that her restraint &mdash; the way she does not press, does not study, does not require access &mdash; has been one of the most consistent kindnesses of your life together. She will be surprised to hear it named. Say it anyway.",
    "{name_isle} &mdash; what {name_vault} receives from you when you simply allow her to be unfinished in your presence is a rest she finds nowhere else. The thing in you that has sometimes been misread as distance is, for her, a form of mercy. Receive that.",
]

GIFT_TO_ISLE = [
    "{name_vault} gives {name_isle} something Islands rarely receive and rarely know to ask for: <b>a witness who attends to the details.</b>",
    "The Island's deepest question is <i>am I enough to be remembered?</i> What this question most wants &mdash; what would answer it, if anything outside of God could &mdash; is a person who notices. Who carries forward what was said last week. Who remembers the small things. Who tracks the shape of the Island's life with the particular care that says: <i>you are not marginal to me. You are one of the things I keep track of.</i>",
    "{name_vault}, by virtue of being a Vault, is among the most precise record-keepers of all the mechanisms the taxonomy maps. The Vault files things. The Vault notes context, remembers the date, tracks what was said and what was not said. Most of this filing runs in a direction the Vault would not choose &mdash; toward wounds, toward the grievances kept private &mdash; but the same capacity for careful attention also means that {name_vault} notices {name_isle} in ways that most people do not. She remembers what you said about the thing at work. She brings it up three weeks later. She tracks the contours of your life with a precision that is, when it runs toward care rather than away from exposure, one of the most loving things a person can do.",
    "The theological word for this gift is something like <i>witness</i>. To be witnessed is to be seen in a way that is remembered, carried forward, not allowed to dissolve. The Island has always longed for precisely this &mdash; a person whose attention does not pass over the Island the way light passes over water. {name_vault}'s capacity for careful attention, which the Vault usually directs inward, is, when it is turned toward {name_isle}, one of the truest answers the Island's question has ever received from a human being.",
    "{name_isle} &mdash; if you want to thank {name_vault} for something this week, thank her for one specific time she remembered something you said. Name the instance. Tell her that being carried in another person's careful attention is one of the things you most needed and most rarely expected to find. The Vault will not be certain what to do with that gratitude. Say it anyway.",
    "{name_vault} &mdash; the noticing you do naturally, the careful tracking of what matters to {name_isle}, is one of the most profound answers to his deepest question. You may not have known you were answering anything. You were. This is worth knowing.",
]

COLLISION = [
    "Now we come to the specific way this marriage produces a collision. It is slower and quieter than most &mdash; which is precisely what makes it so difficult to see and so costly to ignore.",
    "Proverbs 18:1 names the problem with unusual directness: <i>Whoever isolates himself seeks his own desire; he breaks out against all sound judgment.</i> The writer of Proverbs is not addressing someone who has been cruel or angry or faithless. He is addressing someone who has simply &mdash; simply &mdash; organized their life around privacy. He calls it a fracture of sound judgment. He names isolation as a spiritual problem even when, and perhaps especially when, the isolation looks like maturity.",
    "{name_isle}'s isolation looks like maturity. He does not burden others. He is not emotionally volatile. He processes alone, arrives at conclusions, and functions with a quiet dignity that most people in his life read as strength. What it actually is &mdash; and the Island almost never knows this about himself &mdash; is a temperamental preference that has been left unexamined long enough to become a habit of withholding. The Island is not hiding. He simply does not think to show. The distance is not protective; it is structural. But from the outside, and from the inside of this marriage, structural distance and protective distance look identical.",
    "{name_vault}'s isolation also looks like maturity. The Vault is composed, thoughtful, careful. She does not scatter her interior on every available surface. She brings people the resolved version of herself, the organized conclusion rather than the chaotic working draft. What it actually is &mdash; and the Vault knows this, even when she does not say so &mdash; is deliberate. The distance is chosen. The privacy is maintained with effort and strategy, because the experience of exposure without preparation has cost her before, and the Vault has decided, at a level below articulation, that the cost is too high to risk again.",
    "The collision between these two mechanisms is not dramatic. There is no argument, no raised voice, no moment either of you can point to and say: that is where it broke. The collision is the slow accumulation of unspoken things. Each of you assumes the other is processing fine. Each of you is processing alone. Neither of you has ever brought the actual interior &mdash; the thing that is really happening inside, unfiltered and unfinished &mdash; into the marriage room. And because neither of you has, neither of you has ever been fully known by the other.",
    "James 5:16 says: <i>Confess your sins to one another, and pray for one another, that you may be healed.</i> The context James is addressing is physical illness, but the principle has wider reach. The healing he describes is not merely individual; it is relational. It requires that something real pass from one person to another &mdash; something that has been inside, brought into the air between two people. {name_isle} and {name_vault}, the healing James describes is the thing your two mechanisms have, together, been most effectively preventing.",
    "Hebrews 10:24-25 adds the same theme from a different angle: <i>And let us consider how to stir up one another to love and good works, not neglecting to meet together, as is the habit of some, but encouraging one another.</i> The gathering that Hebrews commends is not merely the Sunday assembly. It is the daily practice of mutual presence &mdash; the refusal to process the interior alone when someone has been placed next to you by God to share it with. You have both, in different ways, developed the habit of neglecting to meet. You are in the same house. You have not been in the same room, in the deepest sense, for a long time.",
    "Here is what the collision looks like when it is finally visible. It is a Sunday evening. Neither of you is in conflict. Both of you are, by every external measure, fine. {name_isle} has been processing something all weekend &mdash; a weight from work, a grief that has been sitting just below the surface &mdash; and has not mentioned it, not because he does not trust {name_vault}, but because processing alone is simply what the Island does, and it has not occurred to him that bringing it to her is an option. {name_vault} has been aware, in the Vault's precise way, that something has been slightly off &mdash; she has filed the observation, noted the quietness, and has not asked, because asking feels like pressing, and pressing might require her to offer something in return. By the time they go to bed, each of them has been alone, in the room they share, for the whole of a day. Neither of them has done anything wrong. Neither of them is fully present to the other. And neither of them quite knows how to change it without being asked to change something fundamental about who they are.",
    "{name_isle}, when you feel yourself beginning to process something alone &mdash; before the habit closes the interior door fully &mdash; practice asking one question: <i>Is this the kind of thing {name_vault} would want to know about while it is still forming?</i> Not after you have reached a conclusion. Before. The Island's instinct is to bring the conclusion; the marriage needs the process. She cannot carry you in her attention if you have only ever given her the finished version of yourself to carry.",
    "{name_vault}, when you sense that {name_isle} is processing something alone and you have chosen not to ask &mdash; notice the choice. You are not protecting him by not asking. You are protecting yourself from being required to offer something in return. Name that honestly, at least to yourself. And then consider whether one question &mdash; not an inspection, just a question &mdash; might be the most loving move available to you right now.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be moments, not dramatic but deeply consequential, when both of you have retreated fully into your separate interiors at the same time. The Ghost is up in {name_isle}. The Ghost is up in {name_vault}. Two Ghosts in the same marriage, performing normalcy in the same house, each waiting for the other to notice, and neither noticing because both have made themselves invisible.",
    "Jeremiah 17:9-10 names what is happening in this moment with uncomfortable precision: <i>The heart is deceitful above all things, and desperately sick; who can understand it? I the Lord search the heart and test the mind.</i> The heart that Jeremiah describes is not the heart of a villain. It is the ordinary human heart that has become expert at telling itself convincing stories about its own condition. The Island's heart says: <i>I am simply processing; this is how I work; I am fine.</i> The Vault's heart says: <i>I am composed; the interior is managed; everything is fine.</i> Both hearts are wrong, and neither can see it without help from outside the self.",
    "{name_isle}, when the Ghost is up in you, the story your heart tells is that you have withdrawn for good reason. Perhaps you are genuinely processing something. Perhaps the Island's normal mode of self-containment has simply deepened slightly. But the Ghost is not processing; it is disappearing. The Island can go weeks in Ghost mode and not recognize it as Ghost mode, because Ghost and Island look identical from the inside. What makes it Ghost is not the withdrawal but the performing &mdash; the active maintenance of a surface that says <i>I am here</i> while the interior has quietly left the room.",
    "{name_vault}, when the Ghost is up in you, the story your heart tells is that you are protecting the marriage from something that would be worse if said. This may even be partially true. But the Vault's Ghost is also a closing of the last door &mdash; a retreat to a place where even the composed, organized, curated version of the interior is no longer available. When the Vault Ghosts, there is nothing left to show anyone. The Vault has not merely closed the inner rooms; it has gone invisible in the hallway.",
    "Bonhoeffer, in <i>Life Together</i>, writes this: <i>The pious fellowship permits no one to be a sinner. So everybody must conceal his sin from himself and from the fellowship.</i> He means the Christian community, but the application to this marriage is exact. {name_isle} and {name_vault}, you have built &mdash; without intending to and without quite knowing it &mdash; a marriage that accidentally permits no one to be a sinner. There is no space in your life together in which the unresolved, the failing, the frightened, the half-built thing can be brought and received. The Island does not bring it because bringing is not the Island's instinct. The Vault does not bring it because bringing is not the Vault's strategy. The result is a marriage that looks, from the outside, like two very composed and capable people. From the inside, it is a marriage in which neither person has ever been fully loved, because neither person has ever been fully known.",
    "This is the pattern most likely to end the marriage quietly and without anyone quite realizing it has ended. The Island Ghost and the Vault Ghost, working together, produce what the taxonomy calls the Quiet Exit &mdash; not the dramatic departure, not the confrontation that ends things, but the slow, mutual, nearly imperceptible withdrawal from investment in the marriage itself. The exterior continues. The schedule holds. The meals are shared. But the interior of each person has been living somewhere else for a long time, and one day both of them discover, with something that is more exhaustion than grief, that they are strangers who share a house.",
    "What to do when you can still see what is happening:",
    "<b>Name it out loud, to each other.</b> One of you says &mdash; not in accusation, but in honesty &mdash; <i>I think we are both Ghosting right now. I think neither of us has actually been here for the past few days.</i> The naming is not the resolution; it is the precondition for the resolution. You cannot come back from a place you have not admitted you went to.",
    "<b>In the re-entry, the Island goes first.</b> {name_isle}, this is specific to you: the Island's Ghost is harder to name because it is harder to distinguish from the Island's ordinary mode. But because the Island holds back without realizing it, the discipline of going first is the Island's specific corrective. Say one thing that is actually happening inside you. Not a conclusion. The thing that is still in process. You do not have to have words for it yet. The attempt to find words, made in {name_vault}'s presence, is itself the act of presence the marriage needs from you.",
    "<b>The Vault receives it without filing it.</b> {name_vault}, when {name_isle} brings something interior and unfinished, your task is not to assess it, organize it, or file it. Resist the Vault's instinct to receive information as data to be managed. Receive it as a person who is being trusted with something that has been kept inside. Say one thing back that is also unfinished &mdash; not a response, not a conclusion, but something from the interior that has not been shown. This is the Vault's hardest discipline. It is also the most necessary.",
    "<b>Pray by name, out loud.</b> Not a general prayer. A specific one. <i>Lord, {name_isle} is here. I have not been fully here with him. Help me to come back.</i> Or: <i>Lord, {name_vault} has been keeping something I need to know about. Give her the courage to open one door. Give me the grace to receive what is behind it without turning it into something to plan around.</i> Neither the Island nor the Vault prays easily, and neither prays easily in front of another person. This is precisely why it is the practice that does the most work.",
]

COMMITMENTS_INTRO = [
    "What follows are six commitments &mdash; three from {name_isle}, three from {name_vault}. They are not vows in the legal sense. They are the small daily practices that, offered to each other freely and kept with patience, begin to change the temperature of a home across months and years. Read each one slowly. If you cannot say one of them in good faith yet, do not say it. Honesty about what you cannot yet offer is more useful to this marriage than performance of what you think you should.",
]

ISLE_COMMITMENTS = [
    (
        "I will tell you one thing today I would normally process alone.",
        "{name_vault}, I commit to the practice of bringing you something from my interior before I have finished processing it. Not the conclusion &mdash; the thing that is still forming. I know this will feel unnatural to the Island in me. I will do it anyway, in small measures, because I do not want this to be a marriage in which the only version of me you ever know is the one who has already sorted everything out. You deserve to know me while the sorting is still happening.",
    ),
    (
        "I will ask before I assume you are fine.",
        "{name_vault}, when something in you seems quiet or slightly off, I commit to asking rather than accepting the surface at face value. I know that asking may feel like pressing to you, and I will ask without requiring an immediate answer. But I will not allow the Island's respect for privacy to become an excuse for not noticing you. You are allowed to not be fine. I want to be the person who asks.",
    ),
    (
        "I will name when I have gone quiet.",
        "{name_vault}, when I realize that the Island has deepened into something closer to Ghost &mdash; when I am performing presence while the interior has gone somewhere else &mdash; I commit to naming it as soon as I notice it. Not explaining it, not having solved it first. Simply: <i>I have been away. I am trying to come back.</i> That sentence, offered while it is still true, is the beginning of the return. You deserve to know when I have left and when I am trying to come home.",
    ),
]

VAULT_COMMITMENTS = [
    (
        "I will let you see one unfinished thing today &mdash; not the conclusion, the middle.",
        "{name_isle}, I commit to the practice of showing you something from my interior before it is organized. I know how much the Vault resists this. I know the instinct to wait until the thing is resolved, presentable, safe. But I also know what keeping everything inside costs us, and I am no longer willing to pay that cost alone. I will bring you one thing, once a day, that is still in process. It may be small. The practice is the point.",
    ),
    (
        "I will tell you when the door is closed, instead of pretending there is no door.",
        "{name_isle}, when you ask about my interior at a moment when I am not ready to open it, I commit to naming the door rather than presenting a finished conclusion that is not quite the truth. <i>There is something here I am not ready to show yet.</i> One honest sentence. You deserve to know that the interior exists, even when I am not ready to show it &mdash; so that you are not living beside a person who appears to have no inner life while actually having one that is very full.",
    ),
    (
        "I will not wait for the wound to organize itself before I bring it.",
        "{name_isle}, I commit to naming things that hurt me while they are still fresh &mdash; within the same week, if possible &mdash; rather than carrying them alone until the file has grown too heavy to hold quietly. Not a deposition. One sentence, brought while the wound is still small enough to be repaired by a single conversation. I know the Vault's instinct is to manage pain privately and present the resolution. I am choosing, with God's help, to bring you the unresolved thing instead. Because you deserve a spouse who trusts you with what is actually inside.",
    ),
]

PRAYER = [
    "Father,",
    "You set these two next to each other, and you knew exactly what you were doing. You knew that the Island would process alone, not out of neglect but out of temperament &mdash; that bringing the interior to another person simply does not come naturally to {name_isle}, and that this would cost him in ways he has not fully seen. You knew that the Vault would keep the interior private, not out of coldness but out of fear &mdash; that {name_vault} has learned, in specific and real circumstances, that unfinished things shown to the wrong person at the wrong moment can be turned into something painful. You knew all of it before either of them said yes. You put them together anyway.",
    "Father, teach {name_isle} that bringing the interior to {name_vault} is not a violation of how he is made but a completion of it. The soul was not built for solitude alone; it was built for the one-flesh union that Genesis names as the first thing declared <i>not good</i> to be without. Remind him, when the Island's instinct is to process alone and present the conclusion, that the conclusion without the process is the finished product without the person &mdash; and {name_vault} is not asking for a finished product. She is asking for him.",
    "Teach {name_vault} that the God who has already seen everything she has ever kept inside has spoken the verdict not after inspection but before it, in Christ, at the cross, permanently. She does not need to curate what she shows {name_isle} the way she curates what she shows the world, because {name_isle} is not the world. He is the one who has been placed beside her by the same God who calls himself <i>husband</i> to his people. Give her the courage to open one door today that has been locked for a long time &mdash; not all the doors, just one &mdash; and to discover that the light that comes in is not dangerous.",
    "When the Ghost rises in {name_isle} &mdash; when the Island deepens into something that no longer even notices it is absent &mdash; bring him back to the surface. Let something in him remember that there is a person in the next room who is waiting to know him, not perfectly, but more than she does today. When the Ghost rises in {name_vault} &mdash; when even the composed, curated version goes invisible &mdash; remind her that the God who has engraved her name on his hands does not find the locked rooms inaccessible. He is already inside. Let her bring one thing out to {name_isle} from a room she has not opened before.",
    "Make this marriage a place where the unfinished thing is allowed to be brought. Make their home a room in which neither of them has to have everything sorted before they are allowed to be present to each other. Make their table the place where the actual interior &mdash; forming and unresolved and not quite ready &mdash; is what passes between them on ordinary evenings. And when they are old and the years of small, brave disclosures have accumulated into something neither of them expected, let them see that the quiet they once feared was slowly, by your grace, becoming the quiet of people who know each other and rest in that knowledge.",
    "In the name of the One who was himself disclosed fully &mdash; exposed, known, not hidden &mdash; so that we might be fully covered, and who calls us even now to bring what we are hiding into the light of his face.",
    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages that follow are different. They are meant to be spoken <i>between</i> you.",
    "What follows is a date-night conversation, designed to be taken slowly, somewhere quiet, with no children in the room and no phones on the table. There are six rounds, and they build on each other. The Island will be tempted to find the playful rounds unnecessary. The Vault will be tempted to want more time before answering the harder ones. Both temptations are part of why the structure matters. Trust it. Start at Round One even if it feels too easy; the ease at the beginning is the point.",
    "Some of the questions are light. Some are direct. A few are the kind that, when answered honestly, will sit with you for days. None of them are rhetorical. All of them are an invitation to be known a little more than you were when you sat down.",
    "<b>How to use it.</b> One of you reads a question aloud. The one who did not read answers first, in full, without interruption. Then the reader answers the same question. Then you move on. You do not have to finish all six rounds in one evening &mdash; two or three rounds, taken seriously and without rushing, is often better than racing through all of them. The Island and the Vault both prefer depth to speed. Let that preference work in your favor here.",
    "<b>One rule.</b> The other person's answer is never wrong. You may not love everything you hear. Stay with it. The goal is not to evaluate each other's answers. The goal is to be known, and to do the patient work of knowing.",
]

ROUND_1 = [
    (
        "hypothetical",
        "If our marriage were a landscape, what kind would it be &mdash; and what is the weather like there right now?",
        "Desert, coast, forest, plains. Let the metaphor do what plain language cannot. Be specific about the weather.",
    ),
    (
        "observation",
        "What is something I did this week that you noticed and didn't say anything about?",
        "Not a complaint and not necessarily a compliment. Just something you noticed. The noticing itself is worth naming.",
    ),
    (
        "playful",
        "If you had to describe the two of us as a pair of animals, what would we be &mdash; and what does that say about how we move through the world together?",
        "Yes, really. The first thing that comes to mind is usually the most honest.",
    ),
]

ROUND_2 = [
    (
        "fill-in-blank",
        "I don't think I tell you this enough &mdash; I am genuinely grateful that you are the kind of person who _______. That quality in you has made me _______ in ways I wouldn't have been otherwise.",
        "Two blanks. Be specific. 'Kind' is too easy. 'Patient with my silences even when you didn't understand them' is closer to what this question is asking for.",
    ),
    (
        "observation",
        "What is one thing you have watched me do in the past year that you wish you had told me you saw?",
        "Most of us only see ourselves in our public moments. Your spouse has seen the private ones. This is about those.",
    ),
    (
        "one-word",
        "If you had to choose one word for what it feels like to be truly known by me &mdash; on the rare occasions when that has happened &mdash; what would it be?",
        "One word. Said out loud. Then explain it, briefly, without editing yourself.",
    ),
]

ROUND_3 = [
    (
        "forward-looking",
        "Ten years from now, when we look back on this season of our marriage, what is the one thing you most hope we figured out together?",
        "Not what you wish had been different. What you want, ten years out, to be able to say you learned.",
    ),
    (
        "theological",
        "Where, in the last month, have you seen God specifically at work in me &mdash; not where you hope he will work, but where you have already seen it?",
        "Name it. Be specific. This is witness, not flattery.",
    ),
    (
        "shared-identity",
        "Finish this sentence three times: 'We are the kind of couple who _______.' Give one honest answer, one aspirational answer, and one that would make you both laugh.",
        "The 'we' is the point. Each answer tells you something about how you see the marriage as a unit.",
    ),
]

ROUND_4 = [
    (
        "strength",
        "What is something I carry for this marriage that you would have to learn to carry alone if I were not here?",
        "Hard to ask. Important to hear. Stay with the answer even if it surprises you.",
    ),
    (
        "fill-in-blank",
        "One of the gifts of being married to you is that I get to be _______ in ways I never would have been on my own.",
        "A version of yourself that only exists because the marriage exists. Name it.",
    ),
    (
        "observation",
        "Name one moment in our story where you knew, with no doubt, that we had built something together that neither of us could have built alone.",
        "Tell the whole story. The remembering is part of the strengthening.",
    ),
]

ROUND_5 = [
    (
        "hard",
        "{name_isle}, when you go quiet and process something alone &mdash; as you often do &mdash; what is actually happening inside you that you have never quite found words for?",
        "Not what you want {name_vault} to think is happening. What is actually there. Help her understand what the interior looks like from the inside.",
    ),
    (
        "hard",
        "{name_vault}, when you choose not to bring something interior to {name_isle} &mdash; when the door stays closed &mdash; what is it you are most afraid will happen if you open it?",
        "Not a generality. The specific fear. {name_isle} needs to hear this without defending against it.",
    ),
    (
        "profile-aware",
        "What is one thing you have been carrying this month that you have not brought to me &mdash; and what has kept you from bringing it?",
        "An invitation, not an accusation. The person asking commits to hearing the answer without immediately trying to fix it.",
    ),
]

ROUND_6 = [
    (
        "blessing",
        "Place your hand on your spouse's hand. Say their name. Then say: 'You are not too much to know. You are a person I want to keep learning.' Say it slowly. Let them say it back.",
        "You may feel awkward. Do it anyway. The awkwardness is part of why it works.",
    ),
    (
        "prayer",
        "Pray for each other &mdash; out loud, by name, in one or two sentences. Pray for the specific thing they told you in Round Five.",
        "This is the close of the date. The prayer is not a formality. It is the act of handing the evening, and each other, to the God who was present for all of it.",
    ),
]


def _render(text, name_isle, name_vault):
    return text.format(name_isle=name_isle, name_vault=name_vault)


def build(sub_a, sub_b) -> bytes:
    """Generate the Island+Vault couples walkthrough PDF.

    sub_a: the submission of the Island spouse
    sub_b: the submission of the Vault spouse
    """
    ensure_fonts()
    S = make_styles()

    name_isle = _first_name(sub_a, "Island")
    name_vault = _first_name(sub_b, "Vault")

    def R(text):
        return _render(text, name_isle, name_vault)

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Couples Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUPLES WALKTHROUGH",
        cover_right_label=f"{name_isle.upper()}  +  {name_vault.upper()}",
        title=f"Take 139 Couples Walkthrough \u2014 {name_isle} & {name_vault}",
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
    story.append(Paragraph(f"{name_isle} &nbsp;&amp;&nbsp; {name_vault}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_isle.upper()}</b></font><br/>"
                "Island &middot; Ghost<br/>"
                "<font size=9 color='#6b6862'>Disconnection &middot; Am I enough to be remembered?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_vault.upper()}</b></font><br/>"
                "Vault &middot; Ghost<br/>"
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
        "<i>\u201cWhoever isolates himself seeks his own desire;<br/>"
        "he breaks out against all sound judgment.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "Proverbs 18:1",
        ParagraphStyle("cqa", fontName="Inter", fontSize=9, leading=14,
                       textColor=MUTED, alignment=TA_CENTER, spaceAfter=4)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: OPENING ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "The silence, named.",
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
            _profile_card(S, name_isle, ACCENT, "Disconnection", "Am I enough to be remembered?",
                          "The Island", "The Ghost"),
            "",
            _profile_card(S, name_vault, ACCENT_HER, "Shame", "Am I acceptable?",
                          "The Vault", "The Ghost"),
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

    # ── SECTION 3: THE ISLAND'S GIFT ──
    section_header(story, S, "SECTION THREE  \u00b7  HER GIFT TO HIM",
                   f"What {name_isle} gives {name_vault}.",
                   "A room with no inspection.")
    for p in GIFT_TO_VAULT:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4: THE VAULT'S GIFT ──
    section_header(story, S, "SECTION FOUR  \u00b7  HER GIFT TO HIM",
                   f"What {name_vault} gives {name_isle}.",
                   "A witness who attends to the details.")
    for p in GIFT_TO_ISLE:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5: THE COLLISION ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Two silences that have never met.",
                   "The slow accumulation, and the Scripture that names it.")
    for p in COLLISION[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The Sunday evening, in slow motion.",
                   "What the collision looks like, and the way out for each of you.")
    for p in COLLISION[5:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6: THE HARDER PICTURE ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When both Ghosts are in the room.",
                   "The Quiet Exit as a shared lifestyle, and the gospel's interruption.")
    for p in BOTH_BREAK[:6]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do while you can still see it.",
                   "Four practices, in order.")
    for p in BOTH_BREAK[6:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 7: COMMITMENTS ──
    section_header(story, S, "SECTION SEVEN  \u00b7  COMMITMENTS",
                   "Six small daily practices.",
                   "Three from each of you. Read each one slowly.")
    for p in COMMITMENTS_INTRO:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"FROM {name_isle.upper()}, TO {name_vault.upper()}", S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                             hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for commit_name, body in ISLE_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(commit_name, S["H3"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_vault}, to {name_isle}.",
                   "Three commitments, in her voice, for him to receive.")
    story.append(Paragraph(f"FROM {name_vault.upper()}, TO {name_isle.upper()}",
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
        "You are not too much to know.<br/>"
        "You are a person I want to keep learning.",
        closing_style))

    doc.build(story)
    return finalize_buffer(buf)


# ── STANDALONE TEST ───────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    import sys
    import io

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
        name = "Jordan"
        primary_mechanism = "ISLE"
        primary_breakdown = "GHOST"
        primary_trigger = "DISC"
        core_question = "REM"

    class FakeSubB:
        name = "Morgan"
        primary_mechanism = "VAULT"
        primary_breakdown = "GHOST"
        primary_trigger = "SHM"
        core_question = "ACC"

    pdf_bytes = build(FakeSubA(), FakeSubB())
    out_path = os.path.join(_here, "island_vault_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        snippet = ""
        for page in reader.pages:
            txt = page.extract_text() or ""
            if "SECTION THREE" in txt and "GIFT" in txt:
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

    print(f"DONE: island_vault.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
