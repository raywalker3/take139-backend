"""Couples Walkthrough — Island + Performance Campaign.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where one spouse is an Island and the
other is a Performance Campaign. First names are substituted from the submissions:
    {name_isle}  -> the Island spouse's first name
    {name_camp}  -> the Performance Campaign spouse's first name

Spouse A (Island): self-contained; trigger Disconnection or Significance;
    core question "Am I enough to be remembered?"
Spouse B (Performance Campaign): runner, achiever; trigger Significance;
    core question "Am I enough to be remembered?"

The key pastoral dynamic: both spouses carry the same core question but answer
it with opposite strategies. The Island answers by asking nothing of the world
(self-containment). The Performance answers by producing extravagantly (demonstration).
In marriage, this creates a particular kind of friction: the Island's quiet becomes
the Performance's worst fear, and the Performance's extravagance becomes the
Island's most exhausting experience.
"""
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    Paragraph, Spacer, KeepTogether, HRFlowable, Table, TableStyle,
    PageBreak, NextPageTemplate,
)

try:
    from ..base import (
        make_doc, make_styles, finalize_buffer, ensure_fonts,
        section_header,
        PAGE_W, MARGIN_L, MARGIN_R,
        PAPER, INK, ACCENT, ACCENT_HER, MUTED, RULE, HIGHLIGHT_BG,
    )
except ImportError:
    import sys as _sys
    import os as _os
    _sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
    from base import (
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


# ──────────── PROSE — uses {name_isle} and {name_camp} placeholders ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small repeating ones"
    " \u2014 the same disappointment in slightly different clothes, three or four times a"
    " week, year after year, until both people have forgotten what they were originally"
    " hoping for. What makes your marriage unusual is this: the small repeating rocks are"
    " not caused by two people who want different things. They are caused by two people who"
    " want exactly the same thing, and who have spent years answering that want with"
    " opposite strategies.",

    "Both of you are asking a version of the same question. You have been asking it since"
    " childhood, from inside very different kinds of lives, with very different habits and"
    " very different ways of protecting yourselves from the worst possible answer. The"
    " question is this: <i>Am I enough to be remembered?</i> {name_isle} has answered that"
    " question by building an Island \u2014 by needing very little from the outside world,"
    " so that the world\u2019s failure to give it cannot register as a verdict. {name_camp}"
    " has answered the same question by building a Campaign \u2014 by producing, achieving,"
    " demonstrating, until the visible record is large enough that it cannot be ignored.",

    "What follows is a counselor\u2019s read of what happens in your particular marriage"
    " when these two strategies meet each other every day across a kitchen table."
    " Not the dramatic failures. The small ones. The ones that happen on a Tuesday evening"
    " when {name_camp} arrives home from a long day of producing and needs to be received,"
    " and {name_isle} is simply present and quiet and, in the Island\u2019s own way,"
    " perfectly content. Neither of you is wrong in that moment. Both of you are, in the"
    " grammar of the other\u2019s mechanism, getting it exactly wrong.",

    "Here is what I want to do for you. I will name what each of you brings the other that"
    " you could not have built alone \u2014 the genuine, theological gift your two shapes"
    " form together. Then I will name the collision your two strategies create in the"
    " specific way it shows up in your marriage. Then I will name the worst case, and what"
    " to do then. Then I will hand each of you commitments \u2014 not rules, but the kind"
    " of small daily practices that, over years, change the temperature of a home.",

    "Read it together, if you can. If not, read it separately and then sit down with it."
    " Argue with what does not fit. Stay with what does. The goal is not insight; the goal"
    " is a marriage in which two people who carry the same question finally begin to offer"
    " each other \u2014 slowly, imperfectly, in the small grace of ordinary days \u2014"
    " a better answer than either of them has been able to build alone.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on paper,"
    " side by side. Most couples never see their two profiles next to each other at once."
    " You are about to \u2014 and what you will see is not two opposites, but two people"
    " carrying the same wound and protecting it with entirely different armor.",
]

TWO_SHAPES_BODY = [
    "{name_isle}, you are an <b>Island</b> whose body reads disconnection and significance"
    " as an alarm and whose deepest question is whether you are enough to be remembered."
    " You have built an inner world of unusual depth and self-sufficiency, because you"
    " learned early that the distance between your interior and the outside world was"
    " safer to maintain than to close. When the containment breaks, a <b>Ghost</b>"
    " moves through the rooms of your marriage \u2014 present in body, unreachable in"
    " spirit, performing normalcy while something real goes unspoken underneath.",

    "{name_camp}, you are a <b>Performance Campaign</b> whose body reads significance as"
    " an alarm and whose deepest question is, identically, whether you are enough to be"
    " remembered. You have answered that question by building something visible and"
    " remarkable \u2014 by running hard enough that the record of what you have done"
    " cannot be overlooked. When the campaign cannot answer the question, a <b>Plea</b>"
    " takes over: the pursuit of the connection that has gone quiet, the attempt to close"
    " the gap with gifts and gestures and produced demonstrations of love, each one"
    " carefully offered, each one landing in the wrong register.",

    "Sit with this for a moment, because it is the strangest and most important thing"
    " about your pairing. You are not, as most couples are, two people asking different"
    " questions who have found each other across the difference. You are two people asking"
    " the <i>same</i> question who have developed strategies so opposed that you regularly"
    " make each other\u2019s question more acute rather than less. The Island\u2019s"
    " silence says, to the Performance\u2019s nervous system: <i>you are not enough to"
    " require my attention.</i> The Performance\u2019s extravagance says, to the Island\u2019s"
    " nervous system: <i>someone in this marriage is demanding more than I can give.</i>",

    "And yet you chose each other. Not by accident. Something in each of you recognized"
    " something in the other \u2014 a kind of weight, a kind of depth, a kind of seriousness"
    " about what it means to matter that neither of you wears casually. The Island recognized"
    " in the Campaign someone who takes significance seriously, who has put real effort into"
    " answering the question rather than pretending it does not exist. The Campaign recognized"
    " in the Island someone who carries an interior life that is genuinely worth pursuing"
    " \u2014 a depth that is not produced for an audience, but simply present. Both of you"
    " saw something real. What this document is going to ask is whether you have been able"
    " to give each other what you each most need from the other, or whether the strategies"
    " have been in each other\u2019s way.",
]

GIFT_TO_ISLE = [
    "{name_camp} gives {name_isle} something the Island rarely receives and is poorly"
    " equipped to ask for: <b>a witness who keeps showing up.</b>",

    "The Island\u2019s deepest wound is the suspicion that its interior life is not worth"
    " another person\u2019s sustained attention. The Island has learned, over years and"
    " through specific evidence, that needing to be remembered is a liability \u2014 that"
    " the safest response to the question <i>am I enough to be remembered?</i> is to need"
    " as little remembering as possible. So the Island has built a life that does not"
    " visibly depend on anyone else\u2019s memory. It processes alone. It carries its"
    " interior alone. It has, in the most practical sense, made itself harder to forget"
    " by making itself harder to know.",

    "{name_camp}, by the very nature of the Campaign, refuses this arrangement. The"
    " Performance is constitutionally incapable of treating the people it loves as"
    " background. The Campaign notices, remembers, marks occasions, pursues. It shows up"
    " \u2014 again, and again, and again \u2014 with evidence that it has been thinking"
    " about you. It arrives with something made or found or chosen specifically for the"
    " person it loves. It does not forget. For the Island, who has spent years managing"
    " the wound of being forgotten, this persistent, extravagant remembering is not a small"
    " thing. It is the specific answer to the specific wound \u2014 offered freely, without"
    " the Island having to ask for it, which is the only way the Island can receive it.",

    "The theological word that belongs here is <i>steadfast love</i> \u2014 what the"
    " Hebrew Bible calls <i>hesed</i>, the love that does not withdraw when the beloved"
    " goes quiet. Paul, in 1 Corinthians 13, says that love \u201cbears all things,\u201d"
    " and one of the things love must bear in this marriage is the Island\u2019s silence."
    " {name_camp} bears it. Not always easily. But the bearing is real, and what it gives"
    " {name_isle} is the rarest and most costly thing in the Island\u2019s economy: the"
    " experience of being pursued by someone who knows you are in there, and who keeps"
    " knocking anyway.",

    "{name_isle} \u2014 if you want to thank {name_camp} for something this week, thank"
    " them for this. They have not given up on the interior. They have kept arriving."
    " The Campaign\u2019s persistence, which can sometimes feel overwhelming, is at its"
    " root the specific gift the Island most needs: someone who keeps asking <i>are you"
    " in there?</i> Tell them it has landed. They need to hear it. The Island\u2019s"
    " silence, even when it means peace, is indistinguishable to the Performance from"
    " the silence that means <i>you are not enough.</i> Say it in words.",

    "{name_camp} \u2014 what {name_isle} receives from you, when you keep showing up"
    " and remembering and arriving with evidence of your attention, is the thing the"
    " Island\u2019s strategy was built to protect against needing. You have given it"
    " anyway, without requiring the Island to ask. That is, in the truest sense of the"
    " word, a grace.",
]

GIFT_TO_CAMP = [
    "{name_isle} gives {name_camp} something the Campaign almost never finds in the rooms"
    " it moves through: <b>a place where nothing has to be earned.</b>",

    "The Performance Campaign is, by nature, a person who works for standing. Everything"
    " the Campaign builds is, at some level, an argument \u2014 a demonstration that the"
    " person behind the output is worth noticing, worth keeping, worth the air they are"
    " breathing. This is exhausting in ways the Campaign rarely admits, because the"
    " Campaign has been running long enough that the exhaustion has become background noise."
    " What the Campaign rarely experiences is a room it did not have to earn its way into.",

    "{name_isle}, by virtue of being an Island, provides exactly this. The Island does not"
    " require demonstration. Its self-containment means it does not approach the world"
    " with a ledger of what has been produced and what is owed in return. When {name_camp}"
    " comes home \u2014 not the day\u2019s best self, not the campaign-facing self, but"
    " simply the person who has been running and is tired \u2014 the Island does not"
    " respond with a score. The Island is simply present, quietly, without requiring"
    " the Campaign to perform. For {name_camp}, who spends most of each day in rooms that"
    " are scoring, this is a relief that is difficult to name but easy to feel.",

    "Tim Keller, in <i>The Meaning of Marriage</i>, observed that the deepest gift one"
    " spouse can give the other is not a better version of what the world already provides,"
    " but something the world fundamentally cannot: the experience of being known and"
    " accepted as the person behind the presentation. The Island knows almost nothing"
    " about producing for an audience. Its very mechanism \u2014 self-containment,"
    " interior processing, the refusal to perform for approval \u2014 means that what it"
    " receives from {name_camp} is received as the person, not the portfolio. When the"
    " Island is simply present with {name_camp}, it is present with the person. That is,"
    " for the Campaign, the rarest kind of room there is.",

    "{name_camp} \u2014 if you want to thank {name_isle} for something this week, thank"
    " them for this: the room that does not require you to be impressive. The Island\u2019s"
    " quiet presence, which can sometimes feel like indifference, is at its root a form"
    " of acceptance that has nothing to do with your performance today. You do not have"
    " to earn the Island\u2019s presence. It is simply there. For the Campaign, which"
    " has been earning its place in every other room it inhabits, this is not nothing."
    " It is rest.",

    "{name_isle} \u2014 what {name_camp} receives from you, when you are simply present"
    " without requiring a demonstration, is the experience of being in a room that does"
    " not score them. You may not know you are giving this. You are giving it. The"
    " Campaign\u2019s most characteristic wound is the suspicion that it is only as"
    " valuable as its last visible achievement. Your presence \u2014 undemanding,"
    " unhurried, simply there \u2014 is one of the few things that interrupts that"
    " suspicion without requiring the Campaign to produce anything in response.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you, even"
    " if you have never put a name on what makes it so reliably painful.",

    "Both of you are asking <i>am I enough to be remembered?</i> The gospel answer to"
    " that question is the same for both of you: you are enough because you were chosen"
    " before the foundation of the world, not because of what you produced or how"
    " self-sufficiently you managed. Paul writes in Ephesians 1:4 that God \u201cchose us"
    " in him before the foundation of the world.\u201d Not chosen after the campaign"
    " produced something impressive. Not chosen after the Island demonstrated it could"
    " manage alone. Chosen \u2014 before, unconditionally, permanently. But in the daily"
    " mechanics of a marriage, both of you are still trying to answer the question with"
    " your own strategies. And your strategies, in each other\u2019s presence, make the"
    " question louder rather than quieter.",

    "Here is what {name_isle}\u2019s strategy produces for {name_camp}. The Island\u2019s"
    " mechanism whispers: <i>ask for nothing, and you cannot be denied.</i> So {name_isle}"
    " is self-sufficient, self-contained, quiet. The Island does not perform; it simply"
    " is. From {name_isle}\u2019s perspective, this is dignity. From {name_camp}\u2019s"
    " perspective, it is silence \u2014 and silence, for the Campaign, has always carried"
    " a specific message. The Campaign learned early that when the room goes quiet, it"
    " means you have not produced enough to hold the room\u2019s attention. So the"
    " Island\u2019s peaceful self-containment registers, in {name_camp}\u2019s nervous"
    " system, as <i>you have not done enough to be noticed here.</i> The significance"
    " trigger fires. The Campaign reaches for its only tool: produce more.",

    "Here is what {name_camp}\u2019s strategy produces for {name_isle}. The Campaign\u2019s"
    " mechanism whispers: <i>produce more, and you cannot be replaced.</i> So {name_camp}"
    " arrives with gifts, gestures, plans, surprises \u2014 all of them carefully"
    " constructed, all of them aimed at the Island. From {name_camp}\u2019s perspective,"
    " this is love. From {name_isle}\u2019s perspective, it is stimulus \u2014 and"
    " stimulus, for the Island, is not nourishment. It is demand. The Island did not ask"
    " for all of this. The Island cannot easily receive all of this. The very extravagance"
    " of the Campaign\u2019s love \u2014 its refusal to be quiet, its insistence on being"
    " seen and received \u2014 is experienced by the Island as pressure. So {name_isle}"
    " withdraws further. Which the Campaign reads as the audience going silent. Which"
    " triggers more producing. Which produces more withdrawal.",

    "The loop is not a moral failure on either side. It is the predictable arithmetic of"
    " two wound-protection strategies that were never designed to coexist in the same"
    " room. You are both, in your own grammar, trying to love each other. You are both,"
    " in the other\u2019s grammar, landing it wrong every time.",

    "The way out begins with naming what is actually happening, in real time, before the"
    " loop has run very far. This requires something from both of you that your mechanisms"
    " are designed to prevent. It requires {name_isle} to speak \u2014 to say, in words,"
    " what the Island almost never says in words: <i>I am here. I received what you"
    " brought. It landed.</i> The Island does not need to perform gratitude it does not"
    " feel. But it must find a way to close the circuit that the Campaign has opened,"
    " because the Campaign cannot read silence as anything other than insufficient.",

    "And it requires {name_camp} to stop producing for sixty seconds \u2014 to sit with"
    " {name_isle} in the Island\u2019s own register, which is quiet and unhurried and"
    " without agenda. Not to fill the silence. Not to check whether the silence is approval."
    " To simply be present, producing nothing, and allow that to be enough. Ecclesiastes"
    " 4:9\u201310 says that two are better than one not because of what they produce"
    " together but because \u201cif either of them falls, one can help the other up.\u201d"
    " The help this marriage most needs, in the small repeating moment, is not more output."
    " It is a hand extended quietly across the silence.",

    "{name_camp}, when {name_isle} goes quiet after you have given everything you have,"
    " the translation is almost never <i>you are not enough.</i> Nine times out of ten,"
    " the translation is: <i>the Island has received as much external input as it can"
    " process, and it needs a moment of internal quiet before it can come back to you.</i>"
    " The right move is not to produce more. It is to become still, and to wait. What the"
    " Island\u2019s return from stillness looks like will not be applause. It will be"
    " something small and quiet \u2014 a hand placed on your arm, a sentence said quietly,"
    " a presence that is simply there. Learn to receive that register as love.",

    "{name_isle}, when {name_camp} arrives with a gift at exactly the moment you needed"
    " silence, the translation is almost never <i>this person does not know me.</i>"
    " Nine times out of ten, the translation is: <i>the Campaign is asking me to confirm"
    " that I have not forgotten them, and this is the only language it knows for asking.</i>"
    " The right move is not to withdraw immediately. It is to say one true sentence:"
    " <i>I see you. I received this.</i> Then you can ask for the quiet you need."
    " But say the sentence first. The Campaign cannot hear the rest until it knows"
    " the audience has not left.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be moments \u2014 not often, but they will come"
    " \u2014 when both of you are in breakdown at the same time. The Ghost is walking"
    " through your marriage. The Plea is pursuing it. The room looks, from the outside,"
    " like one person trying very hard while the other is somewhere else entirely. From"
    " the inside, both of you are in pain, and neither of you has access to the more"
    " thoughtful person you were three hours ago.",

    "Here is what is happening when the Ghost and the Plea are in the room together.",

    "{name_isle}, when the Ghost is up, you are not, in that moment, choosing to hurt"
    " {name_camp}. You are doing the only thing the Island knows how to do when the"
    " wound has gone past the threshold: you are managing it in private, the way the"
    " Island has always managed things in private, because the alternative \u2014 bringing"
    " it out into the open, where it might be mishandled or minimized or added to the"
    " performance ledger \u2014 feels more dangerous than the silence. You are performing"
    " normalcy not to deceive but to protect. What {name_camp} experiences, however, is"
    " the specific thing the Campaign most fears: an audience that has stopped responding."
    " The Island\u2019s Ghost is, to the Campaign\u2019s nervous system, indistinguishable"
    " from the silence that means <i>you are not enough to be seen here.</i>",

    "{name_camp}, when the Plea is up, you are not, in that moment, being demanding or"
    " unreasonable. You are doing the only thing the Campaign knows how to do when the"
    " significance trigger fires and producing harder has not answered it: you are"
    " pursuing the connection directly, with everything you have. Gifts, plans, surprises,"
    " gestures, words \u2014 all of them targeted at the Island, all of them an attempt"
    " to close the gap that the Ghost has opened. But every escalation of the Plea is,"
    " to the Island, more stimulus than it can receive. The Ghost withdraws further."
    " The Plea pursues harder. The very thing {name_camp} is doing to be remembered is"
    " making {name_camp} harder to be present with.",

    "Spurgeon wrote that the love which flows from union with Christ gives freely, without"
    " calculation of return, while the love that flows from the fear of being unloved gives"
    " in order to receive, and grows more desperate the longer the return is withheld. In"
    " this marriage, both of you are, in breakdown, drawing on the second kind. But Jesus"
    " said to his disciples, who had been giving without ceasing, in Mark 6:31:"
    " <i>Come away by yourselves to a desolate place and rest a while.</i> In your"
    " marriage, when both of you are in breakdown, that command is spoken to both of you"
    " at once. {name_camp} needs to come away from the producing. {name_isle} needs to"
    " come away from the hiding. Both of you need to find, somewhere in the desolate"
    " quiet, the answer that neither your mechanism nor your breakdown has been able"
    " to provide.",

    "<b>One of you, not both, calls the pause.</b> Whichever one notices first says it"
    " out loud: <i>this is the loop. Twenty minutes.</i> No discussion about who started"
    " it. No final word from the Campaign. No further retreat from the Island. The"
    " twenty minutes belongs to neither of you. It belongs to the God who is, at this"
    " very moment, more present to each of you than you are to each other.",

    "<b>In the twenty minutes, do not strategize. Pray.</b> Not eloquently. {name_camp}:"
    " <i>Lord, my Plea is up. Quiet it. Help me stop producing for sixty seconds and"
    " simply receive that {name_isle} is here, even in the silence.</i> {name_isle}:"
    " <i>Lord, my Ghost is walking. Help me find one true sentence to say out loud"
    " rather than taking this underground where {name_camp} cannot find it.</i>",

    "<b>When you come back, each of you says one sentence, not a paragraph.</b>"
    " {name_camp}, your sentence is not the Plea. It is one true thing about what you"
    " are actually afraid of, beginning with <i>I.</i> {name_isle}, your sentence is"
    " not the silence. It is the one thing, the single weight, that the Ghost has been"
    " protecting. <i>I felt like I disappeared to you tonight</i> is one sentence."
    " <i>I received more than I could hold and I needed somewhere quiet</i> is one"
    " sentence. Both of you can say one sentence. Then stop.",

    "<b>Neither of you is the problem.</b> The Ghost and the Plea are old mechanisms"
    " that have been running for a long time, doing the only job they were ever taught"
    " to do. The truest thing about both of you is not that you are hard to love. It is"
    " that you are two people who took the same question seriously enough to build"
    " a life around it, who found each other across the difference in strategies, and"
    " who are, even in the hardest room, still here. That is what marriage actually is.",
]

COMMITMENTS_INTRO = [
    "What follows are commitments \u2014 three from {name_isle}, three from {name_camp}."
    " They are not vows in the legal sense. They are the small daily practices that,"
    " offered to each other freely, change the temperature of a home over months and"
    " years. Read each one slowly. If one of you cannot say a particular commitment in"
    " good faith yet, do not say it. The goal is not performance; the goal is honesty.",
]

ISLE_COMMITMENTS = [
    ("To tell you, in words, that it landed.",
     "{name_camp}, I commit to closing the circuit you open, in words, on the same day"
     " you open it. When you bring something \u2014 a gift, a gesture, a plan, a moment"
     " of attention \u2014 I commit to telling you, in one sentence, that I received it."
     " Not a performance. Not more than the Island can honestly give. One sentence:"
     " <i>I see what you brought. It landed.</i> The Island\u2019s silence has cost you"
     " more than I realized. I will try to break it with words, in the same week,"
     " on the same day, when I can."),

    ("To name the weight before it goes underground.",
     "{name_camp}, when something lands hard enough to send the Ghost walking, I commit"
     " to naming it to you in one sentence before it goes underground. Not the full case."
     " Not the week\u2019s accumulation. One sentence, on the day it happens: <i>that"
     " landed harder than I showed.</i> I will not always know how to open the door"
     " further. But I will tell you the door exists. You deserve to know when something"
     " is happening inside that I have not shown you."),

    ("To let you see the interior, a little at a time.",
     "{name_camp}, I commit to letting you in on what is actually happening in my"
     " interior life \u2014 not all of it, not immediately, not without processing first."
     " But I will try, with some regularity, to give you a sentence from inside:"
     " something I am carrying, something I noticed, something the Island has been"
     " working on alone for too long. The Island was built to manage alone. I am"
     " learning that the question underneath the Island \u2014 <i>am I enough to be"
     " remembered?</i> \u2014 cannot be answered by a soul that has made itself"
     " unreadable. I will try to be a little more readable to you."),
]

CAMP_COMMITMENTS = [
    ("To spend an evening producing nothing for you, and see what that feels like.",
     "{name_isle}, I commit to spending at least one evening each week in which I"
     " produce nothing for you. No gift planned. No surprise arranged. No gesture"
     " prepared. I will simply be present with you, in the Island\u2019s register,"
     " which is quiet and unhurried and without agenda. I will not fill the silence."
     " I will not check whether the silence means approval. I will practice receiving"
     " your quiet presence as presence, not as an audience that has stopped clapping."
     " This will be difficult for the Campaign. I will try anyway."),

    ("To name the wound before the Plea answers it.",
     "{name_isle}, when the significance trigger fires \u2014 when your silence reads"
     " to me as <i>you have not done enough to be seen here</i> \u2014 I commit to"
     " naming what I actually feel in one sentence, before the Plea takes over and"
     " begins producing harder. One sentence: <i>I felt invisible just now and I"
     " need you to tell me you\u2019re here.</i> I will try to give you the wound"
     " rather than the campaign that the wound produces. The wound is something you"
     " can respond to. The campaign is something you can only endure."),

    ("To receive your quiet as its own kind of answer.",
     "{name_isle}, I commit to learning the Island\u2019s grammar of love. I know"
     " that for you, presence does not require production. I know that when you are"
     " simply near me, without filling the air, you are giving me something the"
     " Campaign has always been too busy to receive. I will try to let the quiet"
     " be enough. I will try to let your being here \u2014 not what you say or"
     " bring or produce, but simply your being here \u2014 answer the question the"
     " Campaign has been running to answer for years. You are enough. You being"
     " here is enough. I am learning to receive that."),
]

PRAYER = [
    "Father,",

    "You set us next to each other, and you knew exactly what you were doing. You knew"
    " they were both asking the same question. You knew one of them would answer it by"
    " going quiet and the other would answer it by filling the quiet with everything"
    " they had. You knew the Ghost and the Plea would, on hard evenings, find each"
    " other in the same room and make the question louder rather than quieter. You knew"
    " all of it before either of us said yes.",

    "Remind us both of what Ephesians 1:4 says is already true: that we were chosen in"
    " you before the foundation of the world. Not chosen because {name_isle} managed"
    " alone well enough. Not chosen because {name_camp} produced impressively enough."
    " Chosen \u2014 before, permanently, unconditionally. Let that answer reach the"
    " place in each of us where the question is still running. The Island\u2019s"
    " mechanism whispers: <i>ask for nothing and you cannot be denied.</i> The"
    " Campaign\u2019s mechanism whispers: <i>produce more and you cannot be replaced.</i>"
    " Both whispers are wrong. Let them hear your voice instead.",

    "Teach {name_isle} that receiving is not exposure. That letting {name_camp} in on"
    " the interior is not the same as needing in a way that sets up disappointment."
    " That the question \u2014 <i>am I enough to be remembered?</i> \u2014 can be"
    " answered by a soul that allows itself to be known. Teach {name_camp} that"
    " producing nothing is not the same as being forgotten. That being quietly present,"
    " in the Island\u2019s register, is its own kind of love \u2014 the kind that does"
    " not require an audience to be real.",

    "And Father, remind them both \u2014 in the hard room, when the Ghost is walking"
    " and the Plea is pursuing \u2014 of what Psalm 139:13\u201316 says: that you"
    " formed them, each of them, in secret, and that your eyes saw their unformed"
    " substance. They were not afterthoughts in the cosmos. They were not ordinary."
    " They were made, and named, and inscribed on the palms of your hands, before"
    " either of them drew a breath or built a strategy. Let that be the answer both"
    " of them have been looking for. Let this marriage be the room where each of"
    " them finally begins to receive it.",

    "In the name of the One who took a bride for himself, and who is, even now,"
    " building the home in which we will live with him forever.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages that"
    " follow are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, somewhere"
    " quiet, with no children in the room and no phones on the table. There are six"
    " rounds, and they build on each other. Resist the temptation to skip ahead. Start"
    " at Round One even if it feels too light; the lightness is the point.",

    "Some of the questions are playful. Some are direct. A few are the kind of questions"
    " that, when answered honestly, will sit with you for the rest of the week. None of"
    " them are trivia. All of them are an invitation.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did not read"
    " answers first, in full, without interruption. Then the reader answers the same"
    " question. Then you move on. You do not have to finish all six rounds in one night"
    " \u2014 in fact, two or three rounds taken seriously is often better than racing"
    " through all of them. Save the rest for the next date.",

    "<b>One rule.</b> The other person\u2019s answer is never wrong. You may not love"
    " everything you hear. Stay with it. The point of this is not to assess each other\u2019s"
    " answers. The point is to be known, and to do the work of knowing.",
]

ROUND_1 = [
    ("hypothetical",
     "If our marriage were a landscape, what kind of landscape would it be, and what"
     " would the weather be doing right now?",
     "Not the landscape you want. The one that is actually true today. Describe it in"
     " one or two sentences."),

    ("observation",
     "What is something I did this week that you noticed and didn\u2019t mention?",
     "Not a complaint. A small noticing. The fact that you noticed at all is the gift."),

    ("playful",
     "If you had to give our marriage a soundtrack \u2014 three songs that capture"
     " what it actually feels like to be in it \u2014 what would the three songs be?",
     "One for the good stretches. One for the hard ones. One for the ordinary Tuesday."),
]

ROUND_2 = [
    ("fill-in-blank",
     "I don\u2019t think I tell you this enough \u2014 I am genuinely amazed at the"
     " way God made you so _______. Your _______ is a gift to this marriage, and I"
     " want to get better at receiving it.",
     "Two blanks. Be specific. \u2018Patient\u2019 is too easy; \u2018able to hold your"
     " interior together when the whole room is pulling at you\u2019 is closer."),

    ("observation",
     "What is one thing you\u2019ve watched me do this year that you wish more people"
     " got to see?",
     "Most of us only ever see ourselves at our most public. Tell your spouse about"
     " the private ones."),

    ("one-word",
     "If you had to choose one word to describe what it feels like to be in the same"
     " room with me at the end of a long day \u2014 not what you say, just what it"
     " feels like in your body \u2014 what word would it be?",
     "One word, said out loud. Then explain it, briefly."),
]

ROUND_3 = [
    ("forward-looking",
     "Five years from now, when we look back on this season of our marriage, what do"
     " you hope we will say we did well together?",
     "Not what you wish you had done. What you want, when you look back, to be able"
     " to say you actually did."),

    ("theological",
     "Where, in the last month, have you seen God specifically at work in me?"
     " Not where you want him to work \u2014 where you\u2019ve already seen it.",
     "Name it specifically. The noticing is its own act of love."),

    ("shared-identity",
     "Finish this sentence three times: \u2018We are the kind of couple who _______.\u2019"
     " Give one playful answer, one true answer, and one aspirational answer.",
     "The \u2018we\u2019 is the point. Let the three answers be genuinely different"
     " from each other."),
]

ROUND_4 = [
    ("strength",
     "What is something I do for you \u2014 or something I simply <i>am</i> for you"
     " \u2014 that you would have to build from scratch if I weren\u2019t here?",
     "Hard to ask. Important to hear. Stay with the answer for a moment before moving on."),

    ("fill-in-blank",
     "One of the gifts of being married to you is that I get to be _______ in ways"
     " I never would have been on my own.",
     "A version of yourself that only exists because this marriage exists. Name it."),

    ("observation",
     "Name one moment in our story where you knew, without any doubt, that we had"
     " built something together that neither of us could have built alone.",
     "Tell the whole story. The remembering is part of the strengthening."),
]

ROUND_5 = [
    ("hard",
     "When my Ghost is up \u2014 when I\u2019m present but somewhere else entirely"
     " \u2014 what is one thing you wish I would do or say differently, not later,"
     " but in that exact moment?",
     "The Island spouse answers first. Then the Performance spouse. Hear the answer without defending."),

    ("profile-aware",
     "When {name_camp}\u2019s Plea is running \u2014 when the producing and the"
     " gifts and the gestures are all aimed at me and I can feel the urgency under"
     " them \u2014 what is the one thing I most need from you that the Plea is not"
     " giving me?",
     "The Island spouse answers this one. Performance spouse: receive the answer as information,"
     " not as accusation."),

    ("theological",
     "What is one thing you have been carrying lately that you have not yet brought"
     " to me, and what has kept you from bringing it?",
     "Not an accusation. An invitation. The answer you give is a gift."),
]

ROUND_6 = [
    ("blessing",
     "Place your hand on your spouse\u2019s hand. Say their name. Then say:"
     " \u2018You are not a problem to be solved. You are a gift I get to receive"
     " again tomorrow.\u2019 Say it slowly. Let them say it back.",
     "You may feel self-conscious. That is part of why it works. Do it anyway."),

    ("prayer",
     "Pray for each other \u2014 not silently, not generally, but out loud and by name."
     " One sentence is enough. Pray for the thing they just told you in Round Five.",
     "The closing of the date. Do not skip. The prayer is the point of all of it."),
]


def _render(text, name_isle, name_camp):
    return text.format(name_isle=name_isle, name_camp=name_camp)


def build(sub_a, sub_b) -> bytes:
    """Generate the Island + Performance Campaign couples walkthrough PDF.

    sub_a: the submission of the Island spouse
    sub_b: the submission of the Performance Campaign spouse
    """
    ensure_fonts()
    S = make_styles()

    name_isle = _first_name(sub_a, "Island")
    name_camp = _first_name(sub_b, "Performance")

    def R(text):
        return _render(text, name_isle, name_camp)

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Couples Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUPLES WALKTHROUGH",
        cover_right_label=f"{name_isle.upper()}  +  {name_camp.upper()}",
        title=f"Take 139 Couples Walkthrough \u2014 {name_isle} & {name_camp}",
    )

    story = []

    # ── COVER ──
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Couples<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph(
        "A counselor\u2019s read of the small repeating rocks<br/>in your particular marriage.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("PREPARED FOR", S["CoverProfileLabel"]))
    story.append(Paragraph(f"{name_isle} &nbsp;&amp;&nbsp; {name_camp}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#4f6b5e'><b>{name_isle.upper()}</b></font><br/>"
                "Island &middot; Ghost<br/>"
                "<font size=9 color='#6b6862'>Disconnection &middot; Am I enough to be remembered?</font>",
                ParagraphStyle("c1", fontName="Inter", fontSize=10.5, leading=15,
                               textColor=INK, alignment=TA_CENTER)),
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_camp.upper()}</b></font><br/>"
                "Performance Campaign &middot; Plea<br/>"
                "<font size=9 color='#6b6862'>Significance &middot; Am I enough to be remembered?</font>",
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
        "<i>\u201cBoth of them are asking the same question.<br/>"
        "They have simply chosen opposite strategies for answering it.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1 ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "The same question, two strategies.",
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
            _profile_card(S, name_isle, ACCENT, "Disconnection / Significance",
                          "Am I enough to be remembered?",
                          "The Island", "The Ghost"),
            "",
            _profile_card(S, name_camp, ACCENT_HER, "Significance",
                          "Am I enough to be remembered?",
                          "The Performance Campaign", "The Plea"),
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
    section_header(story, S, "SECTION THREE  \u00b7  THE PERFORMANCE\u2019S GIFT TO THE ISLAND",
                   f"What {name_camp} gives {name_isle}.",
                   "A witness who keeps showing up \u2014 and what that gives the Island.")
    for p in GIFT_TO_ISLE:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4 ──
    section_header(story, S, "SECTION FOUR  \u00b7  THE ISLAND\u2019S GIFT TO THE PERFORMANCE",
                   f"What {name_isle} gives {name_camp}.",
                   "A place where nothing has to be earned.")
    for p in GIFT_TO_CAMP:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5 ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "The same question, making each other\u2019s louder.",
                   "How two identical wounds and opposite strategies create one very specific loop.")
    for p in COLLISION[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The way out, in each other\u2019s grammar.",
                   "What each of you must do \u2014 in the moment \u2014 to break the loop.")
    for p in COLLISION[5:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6 ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When the Ghost and the Plea are in the room at once.",
                   "What is happening, named plainly, so both of you can see it.")
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
    story.append(Paragraph(f"FROM {name_isle.upper()}, TO {name_camp.upper()}", S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for commit_name, body in ISLE_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(commit_name, S["H3"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_camp}, to {name_isle}.",
                   "Three commitments, in the Campaign\u2019s voice, for the Island to receive.")
    story.append(Paragraph(f"FROM {name_camp.upper()}, TO {name_isle.upper()}", S["CommitLabelHer"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT_HER,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for commit_name, body in CAMP_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(commit_name, S["H3Her"]),
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
        "You are not a problem to be solved.<br/>"
        "You are a gift I get to receive again tomorrow.",
        closing_style))

    doc.build(story)
    return finalize_buffer(buf)


# ── STANDALONE TEST ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    import io

    class FakeSubA:
        primary_mechanism = "ISLE"
        primary_breakdown = "GHOST"
        primary_trigger = "DISC"
        core_question = "REM"
        name = "Jordan"

    class FakeSubB:
        primary_mechanism = "CAMP"
        primary_breakdown = "PLEA"
        primary_trigger = "SIG"
        core_question = "REM"
        name = "Taylor"

    pdf_bytes = build(FakeSubA(), FakeSubB())
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "island_performance_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        snippet = ""
        for page in reader.pages[4:10]:
            txt = page.extract_text() or ""
            if "SECTION THREE" in txt or "witness" in txt.lower() or "gift" in txt.lower():
                snippet = txt.strip()[:200]
                break
        if not snippet:
            for page in reader.pages[4:10]:
                txt = page.extract_text() or ""
                if txt.strip():
                    snippet = txt.strip()[:200]
                    break
    except Exception as e:
        page_count = "unknown"
        snippet = f"(pypdf error: {e})"

    print(f"DONE: island_performance.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
