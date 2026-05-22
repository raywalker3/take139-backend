"""Couples Walkthrough — Performance Campaign + Vault.

Voice: Tim Keller (slightly more concrete and practical than the personal walkthroughs).
~25 pages, 9 sections + 6-round Date Night appendix.

This builder serves any couple where one spouse is a Performance Campaign and the
other is a Vault. First names are substituted from the submissions:
    {name_camp}  -> the Performance Campaign spouse's first name
    {name_vault} -> the Vault spouse's first name

Spouse A (Performance Campaign): runner, achiever; trigger Significance;
    core question "Am I enough to be remembered?"
Spouse B (Vault): curates what is shown; trigger Shame;
    core question "Am I acceptable?"

KEY PASTORAL DYNAMIC:
This is one of the most outwardly successful marriages in the 21 — and one of
the loneliest. Both spouses curate what they show: the Performance shows the world
a polished, accomplished, visible self; the Vault shows a measured, reserved,
controlled self. Together they look formidable. Both keep their interior heavily
managed; neither shares the unfinished places easily. The marriage often functions
as a high-performing partnership with very little messy middle ever crossing
the threshold.
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


# ──────────── PROSE — uses {name_camp} and {name_vault} placeholders ────────────

OPENING = [
    "Most marriages do not break on the large rocks. They break on the small repeating ones"
    " \u2014 the same quiet misfire in slightly different clothes, week after week, year after"
    " year, until both people have forgotten what they were originally hoping for when they sat"
    " down together at the end of a long day. You are not the kind of couple that breaks"
    " obviously. You are, in fact, the kind of couple that rarely appears to break at all."
    " Both of you know how to present well. Both of you keep the difficult parts largely"
    " interior. The question this document is going to press on is not whether the life you"
    " have built looks good from the outside. It does. The question is whether either of you"
    " fully knows what is carrying the weight of it from the inside.",

    "What follows is a counselor\u2019s read of the specific, recurring misfire in your"
    " particular marriage. Not the dramatic failures, which you would have addressed by now."
    " The quiet ones. The ones that happen on an ordinary evening when the house is settled"
    " and one of you is running on something the other cannot quite name, and neither of you"
    " quite finds the other. The ones that, by morning, have receded into the background of"
    " an otherwise well-managed life.",

    "You are both reading this because you have decided to look at those things. That decision"
    " is more significant than it appears. Most couples with your particular wiring spend years"
    " navigating around the small misfires without ever naming them, because both of you have"
    " extraordinary capacity for managing what is uncomfortable without making it visible. You"
    " chose to name it. That is already unusual, and it is already the beginning of something.",

    "Here is what I want to do for you. I will name what each of you brings the other that"
    " you could not have built alone \u2014 the genuine, theological gift that your two very"
    " different shapes form together. Then I will name the collision your two core questions"
    " create in the specific way it shows up in your marriage. Then I will name the harder"
    " picture \u2014 when both of you are in breakdown at once \u2014 and what to do in that"
    " moment. Then I will hand each of you commitments: not rules, but the kind of small"
    " daily practices that, offered to each other freely and kept with patience, change the"
    " temperature of a home over years.",

    "Read it together if you can. If not, read it separately and then sit down with it. Argue"
    " with what does not fit. Stay with what does. The goal is not insight for its own sake."
    " The goal is a marriage in which {name_camp} and {name_vault} are more fully known to"
    " each other \u2014 not perfectly, but more than they are today.",
]

TWO_SHAPES_INTRO = [
    "Before we go anywhere else, take a long look at what each of you actually is, on paper,"
    " side by side. Most couples never see their two profiles next to each other with this kind"
    " of clarity. You are about to.",
]

TWO_SHAPES_BODY = [
    "{name_camp}, you are a <b>Performance Campaign</b> whose body reads invisibility as an"
    " alarm and whose deepest question is whether you are enough to be remembered. You have"
    " learned, early and with real conviction, that the path to being seen runs through the"
    " extraordinary \u2014 that if you can build something visible and impressive, you cannot"
    " be ignored, and if you cannot be ignored, you cannot be forgotten. When the campaign"
    " fails to produce the recognition it was built to earn, an <b>Attorney</b> takes the"
    " floor and presents the r\u00e9sum\u00e9 as evidence for the love that no r\u00e9sum\u00e9"
    " has ever been able to purchase.",

    "{name_vault}, you are a <b>Vault</b> whose body reads shame as an alarm and whose deepest"
    " question is whether you are acceptable. You have learned, carefully and over a long time,"
    " that the interior world is best kept interior \u2014 that what you show must be chosen,"
    " that the finished product is safer than the half-built one, and that the messy middle of"
    " your inner life belongs to you alone, to be managed privately and resolved before anyone"
    " else is invited in. When a wound lands large enough that the Vault cannot contain it, an"
    " <b>Attorney</b> takes the floor \u2014 not with heat, but with a file: organized, dated,"
    " precise, and years in the keeping.",

    "Notice what these two profiles share on the surface, and notice how different the wounds"
    " underneath them actually are. From the outside, this marriage often looks formidable."
    " Both of you are composed in public. Both of you know how to manage what is uncomfortable."
    " Both of you present well. The world sees two people who appear to have it together, and"
    " it is not wrong \u2014 you do, in significant ways. What the world cannot see is that"
    " {name_camp} is managing the interior by converting it into output, while {name_vault} is"
    " managing the interior by keeping it precisely filed. The strategies look similar from"
    " outside. They are driven by entirely different fears.",

    "{name_camp}\u2019s question is <i>am I enough to be remembered?</i> \u2014 which is"
    " answered, in the Campaign\u2019s grammar, by producing something that cannot be ignored."
    " {name_vault}\u2019s question is <i>am I acceptable?</i> \u2014 which is answered, in"
    " the Vault\u2019s grammar, by showing only what has been prepared and keeping the rest"
    " private. The Performance runs outward. The Vault holds inward. Both are, in their own"
    " way, managing the same fundamental terror: that if seen fully, without preparation or"
    " accomplishment, they might not be enough.",

    "This shared terror is part of what drew you to each other, even if you have never named"
    " it that way. {name_camp} is drawn to {name_vault}\u2019s composure \u2014 the sense"
    " that the Vault is not rattled, not scattered, not in need of managing, which offers the"
    " Campaign a rare experience of a room that is not demanding anything. {name_vault} is"
    " drawn to {name_camp}\u2019s visibility \u2014 the sense that the Campaign stands in the"
    " world with confidence and produces things of real worth, which offers the Vault something"
    " adjacent to the covering it most needs. You recognized something in each other before you"
    " had words for it. This document is part of finding the words.",
]

GIFT_TO_VAULT = [
    "{name_camp} gives {name_vault} something the Vault has always needed but would rarely"
    " build for itself: <b>a witness who stands in the room and is seen.</b>",

    "The Vault\u2019s deepest longing \u2014 underneath the question <i>am I acceptable?</i>"
    " \u2014 is to be known without being exposed. To have someone see what is actually inside"
    " and remain. But the Vault\u2019s mechanism ensures this is extraordinarily difficult"
    " to receive, because the Vault curates what is shown and therefore can never be quite sure"
    " whether what is loved is the real interior or only the presented version. What {name_camp}"
    " gives {name_vault}, in a way few other mechanisms can, is the experience of someone who"
    " does not hide. The Campaign is visible. It puts itself in the light and asks to be seen."
    " This is, for the Vault, an education in a kind of courage it has rarely practiced.",

    "There is more. {name_camp}\u2019s visibility \u2014 the willingness to be present, to be"
    " known publicly, to stand in rooms and be recognized \u2014 creates, around {name_vault},"
    " a kind of social covering. The Vault does not often seek the front of a room. The"
    " Campaign occupies it naturally. For {name_vault}, this is not a small thing. It is the"
    " experience of being in a marriage with someone who stands in the world with their name"
    " on their work, and who takes {name_vault} as a given, a permanent companion in that"
    " standing. The Vault is known, in part, by who it chose. The Campaign chosen by the Vault"
    " is someone who makes the Vault\u2019s world larger without requiring the Vault to expand"
    " its own exposure.",

    "The theological word for what {name_camp} brings {name_vault} is something close to"
    " <i>declaration</i>. Paul writes in Romans 10:10 that it is with the mouth one confesses"
    " and is saved \u2014 that faith, finally, must be spoken outward. {name_camp} is"
    " constitutionally outward in a way the Vault rarely is. The Campaign declares. It stands"
    " in the open and speaks. This is not merely a social virtue; it is, for the Vault who has"
    " spent years keeping things close, a living demonstration that being visible does not"
    " necessarily produce the catastrophe the Vault has been guarding against.",

    "{name_vault} \u2014 if you want to thank {name_camp} for something this week, thank them"
    " for this. Not for a specific accomplishment, but for the way their willingness to be seen"
    " has made a room in the world that you share without having to construct it entirely"
    " yourself. The Campaign\u2019s visibility is, in part, a gift to the Vault\u2019s privacy."
    " You have received it without perhaps naming it as a gift. Name it once. They will not"
    " know what to do with the compliment. Say it anyway.",

    "{name_camp} \u2014 what {name_vault} receives from you, when you stand in the world and"
    " are seen and bring {name_vault} into that standing as your person, is more than social"
    " capital. It is the experience of being known and accompanied by someone the world has"
    " already recognized. That means more to the Vault than the Vault will usually say.",
]

GIFT_TO_CAMP = [
    "{name_vault} gives {name_camp} something the Performance Campaign almost never builds"
    " for itself: <b>a room that does not require the campaign to run.</b>",

    "Most of the rooms {name_camp} walks into require performance. People depend on the"
    " Campaign\u2019s output. Recognition arrives when the campaign produces. Every"
    " relationship, every professional context, every social room carries an implicit"
    " expectation: show us what you can do, and we will confirm that you belong here. The"
    " Performance Campaign has spent years becoming extraordinarily good at meeting that"
    " expectation. The cost of this, which the Campaign rarely acknowledges even to itself,"
    " is that it has almost no experience of rooms that simply receive it as a person"
    " rather than as a producer.",

    "{name_vault}, by virtue of being a Vault, gives {name_camp} exactly that. The Vault does"
    " not require output in order to remain. The Vault\u2019s mechanism is built around careful"
    " reception, not around demand for demonstration. When {name_vault} is present, they are"
    " not checking whether the Campaign is impressive enough for the evening. They are simply"
    " there, contained and composed, not requiring anything particular of {name_camp} in order"
    " to stay in the room. For the Campaign, whose entire wiring is organized around earning"
    " its place in every room it enters, this is a genuinely unusual and quietly medicinal"
    " experience.",

    "The theological word for what {name_vault} gives {name_camp} is <i>sabbath</i>. Not the"
    " formal Sabbath of religious observance, but the small recurring sabbaths of a marriage"
    " in which one person does not require the other to be performing. The Preacher of"
    " Ecclesiastes wrote that the eye is never satisfied with seeing, nor the ear with hearing"
    " (Ecclesiastes 1:8) \u2014 that the campaign to be seen and remembered runs on an engine"
    " that cannot, by its nature, reach a resting state. {name_vault}\u2019s composure does"
    " not silence that engine. But it creates, in the marriage, a room where the engine is"
    " allowed to idle rather than run at full speed. That is no small thing for a person who"
    " has been running most of their life.",

    "{name_camp} \u2014 if you want to thank {name_vault} for something this week, thank them"
    " for the times they were simply present with you without needing you to be impressive."
    " The evenings they did not ask about the next project. The moments they received you"
    " as a person rather than as the sum of what you had recently produced. The Vault rarely"
    " knows this is a gift; they have often been told their reserve is the problem, not the"
    " contribution. Tell them otherwise.",

    "{name_vault} \u2014 what {name_camp} receives from you, when you simply remain without"
    " requiring them to perform, is the closest thing to genuine rest that the Campaign"
    " experiences in a typical week. The thing in you that you have sometimes been told is too"
    " quiet, too contained, too much alone \u2014 is for them a kind of mercy.",
]

COLLISION = [
    "Now we come to the small repeating rock. It will be familiar to both of you, even if"
    " you have never had quite these words for it.",

    "{name_camp}\u2019s core question is <i>am I enough to be remembered?</i> The way the"
    " Campaign answers this question is by producing \u2014 by building something visible and"
    " impressive that cannot be ignored. When the question fires, {name_camp}\u2019s first"
    " move is to demonstrate: to accomplish something, to name an achievement, to make sure"
    " the room has registered what has been done. The Campaign\u2019s love language, when it"
    " is anxious, is visibility. <i>See what I have built. See what I can do. See that I was"
    " here and that my presence mattered.</i>",

    "{name_vault}\u2019s core question is <i>am I acceptable?</i> The way the Vault answers"
    " this question is by curating \u2014 by ensuring that what is shown has been organized"
    " and considered, and that what has not been organized and considered stays private. When"
    " the question fires, {name_vault}\u2019s first move is not outward but inward: to manage"
    " the interior, to process privately, to present a composed exterior while the interior"
    " continues its careful work behind locked doors. The Vault\u2019s love language, when it"
    " is anxious, is measured composure. <i>I am fine. We are fine. Nothing to see here that"
    " has not already been prepared for viewing.</i>",

    "Here is what the Campaign unconsciously asks of the Vault: <i>be my audience.</i> Not"
    " deliberately, not cruelly \u2014 but the Performance\u2019s engine is built to run"
    " toward recognition, and the person standing closest in the marriage is the natural"
    " target. {name_camp} is, at some level, hoping that {name_vault} will be the one who"
    " finally sees the campaign clearly enough and responds to it warmly enough that the"
    " significance trigger quiets. And here is what the Vault unconsciously asks of the"
    " Campaign: <i>require nothing of the interior.</i> Not deliberately, not as a"
    " negotiation \u2014 but the Vault\u2019s equilibrium depends on not being pressed toward"
    " exposure, and the person standing closest in the marriage is the person most capable"
    " of pressing. {name_vault} is, at some level, hoping that {name_camp} will be too busy"
    " with the campaign to notice what is in the Vault, and to leave it undisturbed.",

    "Both requests are completely understandable. Both are also unsustainable. The Preacher"
    " of Ecclesiastes names the Campaign\u2019s treadmill with devastating precision: <i>The"
    " eye is not satisfied with seeing, nor the ear filled with hearing... There is no"
    " remembrance of former things; nor will there be any remembrance of things that are to"
    " come among those who come after.</i> (Ecclesiastes 1:8, 11) What the Preacher names is"
    " not that the campaign is wrong to want to be remembered, but that the campaign is"
    " running on an engine that has no off switch \u2014 that the recognition, when it comes,"
    " satisfies for a season and then hands the question back unsatisfied. {name_camp}, you"
    " have experienced this. The recognition comes. It quiets the question briefly. And then"
    " the question returns, and the campaign must run again.",

    "And the author of Hebrews names the Vault\u2019s situation with equal precision:"
    " <i>And no creature is hidden from his sight, but all are naked and exposed to the eyes"
    " of him to whom we must give account.</i> (Hebrews 4:13) {name_vault}, the interior you"
    " have been so carefully curating has already been fully seen by the only witness whose"
    " verdict finally matters. You have been hiding from a God who has already looked and has"
    " not turned away. The management project that has governed so much of your interior life"
    " is, before God, unnecessary \u2014 not because the interior does not need tending, but"
    " because the tending has already been done on your behalf, by One who entered the exposure"
    " you most fear and absorbed its consequence.",

    "The collision these two mechanisms produce in a marriage is this: the Campaign finds the"
    " Vault\u2019s measured response insufficient. {name_camp} brings something to the marriage"
    " \u2014 an accomplishment, an idea, a moment of genuine investment \u2014 and {name_vault}"
    " receives it with composure rather than with the warm, ringing recognition the Campaign"
    " was hoping for. The Vault is not withholding; the Vault is being the Vault \u2014 careful,"
    " considered, measured in its responses. But to the Campaign, whose alarm is tuned to the"
    " frequency of insufficient recognition, the Vault\u2019s composure reads as"
    " <i>invisible again.</i> The trigger fires. The Campaign runs harder: more output, more"
    " achievement, more demonstration. And the Vault, sensing that something is being"
    " demanded of it \u2014 some warmer, fuller response than it knows how to produce on"
    " request \u2014 retreats further into its interior. The walls go up. The Campaign finds"
    " the walls confirming the invisibility it feared. The loop is running.",

    "{name_camp}, when {name_vault} responds to something you have brought with composure"
    " rather than recognition, the translation is almost never <i>they do not care.</i> The"
    " Vault cares with extraordinary depth. The translation is: <i>the Vault processes"
    " internally, and what it brings you is the considered response rather than the immediate"
    " one, and the considered response does not always look like what the Campaign is"
    " calibrated to receive.</i> The right move, when you notice the Campaign wanting more, is"
    " to set down the accomplishment for a moment and ask {name_vault} one direct question"
    " that has nothing to do with what you have produced. The Vault will not always answer"
    " immediately. But it will register that you came as a person rather than as a campaign,"
    " and that registration matters.",

    "{name_vault}, when {name_camp} brings accomplishments into the marriage with an energy"
    " that can feel like it is asking something of you, the translation is almost never"
    " <i>they are demanding an audience.</i> The translation is: <i>the Campaign just"
    " experienced the significance trigger, and the only language it has in that moment is"
    " demonstration.</i> The right move is not to retreat further. It is to name what you"
    " actually see \u2014 not the accomplishment, but the person behind it. <i>I see you"
    " working hard on this.</i> <i>I notice what this has cost you.</i> The Campaign can"
    " receive that. It is not the recognition the campaign was chasing, but it is something"
    " rarer: being seen as a person rather than as a producer.",
]

BOTH_BREAK = [
    "Now the harder picture. There will be seasons \u2014 not often, but they will arrive"
    " \u2014 when the quiet misfire in the marriage escalates and both of you are in breakdown"
    " at the same time. The Quiet Exit is up in {name_camp}. The Ghost is up in {name_vault}."
    " And here is what makes this particular pairing so pastorally urgent: when both of you"
    " are in breakdown, the marriage often looks, from every external angle, completely fine.",

    "The Quiet Exit is the Campaign\u2019s version of the breakdown. {name_camp}, when the"
    " significance trigger has fired enough times without the answer the Campaign was running"
    " toward, the Campaign does not collapse visibly. It retires. Not in a scene, not in a"
    " confrontation, but in a quiet withdrawal of investment from the marriage. The campaign"
    " keeps running \u2014 the output is still real, the achievement is still genuine, the"
    " professional life is still productive. But the marriage itself becomes, gradually, one"
    " more room in which {name_camp} is performing rather than present. The runner is still"
    " running. But they have stopped running toward {name_vault}.",

    "The Ghost is the Vault\u2019s version of the same breakdown. {name_vault}, when the"
    " shame trigger has confirmed its suspicion \u2014 that showing the interior costs more"
    " than it gains \u2014 the Vault does not collapse visibly either. It simply becomes less"
    " permeable. The composure that was always a feature of the Vault now becomes its totality."
    " {name_vault} is still present, still functional, still managing the ordinary transactions"
    " of a shared life. But the interior \u2014 which was always carefully curated \u2014 is"
    " now entirely closed. The person is there. The person is not accessible.",

    "Psalm 51:6 speaks a word that lands on both mechanisms at once: <i>Behold, you delight"
    " in truth in the inward being, and you teach me wisdom in the secret heart.</i> God does"
    " not delight in the polished exterior. He does not delight in the accomplished"
    " presentation or the managed composition. He delights in truth in the inward being \u2014"
    " in the secret heart, the actual interior, the half-built and unresolved and fearful"
    " things that both of you have been keeping away from each other and sometimes from"
    " yourselves. {name_camp}, the part of you the Lord most delights in is not the campaign."
    " It is the person behind the campaign who gets tired and wonders if any of it matters."
    " {name_vault}, the part of you the Lord most delights in is not the curated conclusion."
    " It is the interior that you have been managing alone for a very long time. Both of you"
    " have been offering the world the product. God is asking for the process.",

    "Martyn Lloyd-Jones, writing on spiritual depression in his sermons on Psalm 88, observed"
    " that the achiever and the hidden person are often closer to grace than they believe"
    " \u2014 precisely because both have been driven to the outer limit of what self-management"
    " can provide, and the outer limit of self-management is exactly the place where the gospel"
    " becomes, at last, not a doctrine but a lifeline. {name_camp} and {name_vault}, you have"
    " both been managing extraordinarily well. And both of you are, in different ways, arriving"
    " at the place where management is not enough.",

    "What to do when you can both still see what is happening:",

    "<b>One of you calls the pause.</b> Whichever one notices first that the two of you are"
    " no longer actually present to each other \u2014 not arguing, perhaps, but absent"
    " \u2014 says it plainly: <i>I think we are not really here with each other right now."
    " I think we have both retreated. Can we come back?</i> No brief. No campaign entry. The"
    " pause is the acknowledgment that both withdrawals have been noticed, by at least one"
    " of you.",

    "<b>In the pause, pray by name.</b> {name_camp}: <i>Lord, the Campaign in me has retired"
    " from this marriage, and I know it. Bring me back. Help me show up as a person, not"
    " as a producer, and trust that {name_vault} will receive what they find.</i>"
    " {name_vault}: <i>Lord, the Ghost in me has closed everything, and I know it. Give me"
    " the courage to open one door. Help me show {name_camp} one true thing about what is"
    " inside, uncurated, before I have resolved it.</i>",

    "<b>When you come back, each of you says one true sentence.</b> {name_camp}, your"
    " sentence is not an accomplishment. It is one true thing about what you have been"
    " feeling, beginning with <i>I</i>: <i>I have been running and I have not been here."
    " I am sorry. I want to come back.</i> {name_vault}, your sentence is not a finished"
    " conclusion. It is one thing from the interior, still in process: <i>I have been"
    " keeping something in, and I want to try to show it to you.</i> One sentence each."
    " Then stop. The stop is as important as the sentence.",

    "<b>Neither of you is the problem.</b> The Quiet Exit and the Ghost are old mechanisms"
    " doing what old mechanisms do: protecting what they were built to protect, long past"
    " the season that required the protection. The marriage that can name them together,"
    " out loud, in one sentence each, is already doing something neither mechanism believes"
    " is possible. Do it anyway.",
]

COMMITMENTS_INTRO = [
    "What follows are six commitments \u2014 three from {name_camp}, three from {name_vault}."
    " They are not vows in the formal sense. They are the small daily practices that, offered"
    " to each other freely and kept with patience, change the temperature of a home across"
    " months and years. Read each one slowly. If one of you cannot say a particular commitment"
    " in good faith yet, do not say it. The goal is not performance; the goal is honesty.",
]

CAMP_COMMITMENTS = [
    (
        "I will spend an hour with you this week that produces nothing.",
        "{name_vault}, I commit to spending an hour with you \u2014 at least once this week,"
        " and with some regularity after that \u2014 in which I am not building anything,"
        " not demonstrating anything, not advancing any campaign. I will simply be present"
        " with you. When the anxiety rises that the hour is unproductive, I will name it"
        " to you rather than convert it into output. I want to learn what it feels like to"
        " let an hour be enough, rather than something to fill."
    ),
    (
        "I will name the wound before the attorney assembles the portfolio.",
        "{name_vault}, when the significance trigger fires \u2014 when I feel invisible,"
        " unseen, or like the campaign has been running without an adequate audience"
        " \u2014 I commit to telling you in one sentence what I actually need, before the"
        " Attorney builds the case from my accomplishments. Not <i>do you know what I have"
        " done?</i> but <i>I need to feel like I matter to you right now.</i> The wound"
        " is what I will try to bring. The brief stays in the folder."
    ),
    (
        "I will ask about what is inside you before I tell you what I have built.",
        "{name_vault}, I commit to beginning more of our conversations with a question about"
        " your interior rather than an account of my output. I know you do not always bring"
        " the interior forward readily. I will not press. I will ask one question, and I will"
        " wait, and I will receive whatever you give me as a gift rather than as data."
        " The campaign can wait. You cannot."
    ),
]

VAULT_COMMITMENTS = [
    (
        "I will let you see something I have not finished, and not curate it for you.",
        "{name_camp}, I commit to bringing you, at least once this week and with some"
        " regularity after that, one thing from the interior that is still in process \u2014"
        " a question I have not resolved, a feeling I have not organized, a grief I have not"
        " yet brought to a conclusion. I will not prepare it before I show you. I will let"
        " it be unfinished. I know the Vault will resist this. I am willing to resist the"
        " Vault, in small doses, for you."
    ),
    (
        "I will receive your accomplishments as an offering, not as a demand.",
        "{name_camp}, when you bring something you have built or achieved into the space"
        " between us, I commit to receiving it as an offering from a person I love rather"
        " than as a campaign requesting an audience. I will name what I actually see:"
        " not just the accomplishment, but the effort and care behind it. You have been"
        " running for a long time, and I want to be someone who notices the runner and"
        " not only the race."
    ),
    (
        "I will name a wound within the same week it happens.",
        "{name_camp}, I commit to naming things that hurt me within the same week they occur,"
        " rather than carrying them alone until the file grows too large to hold quietly."
        " Not the full archive. One wound, one sentence, brought while it is still small"
        " enough for a single conversation to repair. You deserve to know when something"
        " has landed on me, without having to wait for the Attorney to organize it into"
        " evidence. I will try to bring you the wound before I bring you the file."
    ),
]

PRAYER = [
    "Father,",

    "You set us next to each other, and you knew exactly what you were doing. You knew the"
    " Campaign would need a room that did not require the running. You knew the Vault would"
    " need someone willing to stand in the light, visible, without collapsing under the"
    " weight of it. You knew the Quiet Exit and the Ghost would, in certain seasons, arrive"
    " at the same time and that the marriage would look fine from every external angle while"
    " both of us were somewhere else entirely. You knew all of it before either of us"
    " said yes.",

    "Teach us the grammar of each other. Teach {name_camp} that the significance the Campaign"
    " has been running toward is not at the end of the next achievement but has already been"
    " engraved on the palms of your hands \u2014 permanent, present, spoken before a single"
    " campaign entry was ever made. Let that reach the place in {name_camp} that is still"
    " running. Teach {name_vault} that the interior you have been so carefully curating is"
    " already fully known to you, and that your verdict is not exposure but covering \u2014"
    " <i>there is therefore now no condemnation for those who are in Christ Jesus.</i>"
    " Let that reach the place in {name_vault} that is still filing.",

    "When the Campaign retires in {name_camp} and the Quiet Exit takes the floor, would you"
    " call {name_camp} back \u2014 back to this marriage, back to this person, back to the"
    " conviction that the hour spent producing nothing for anyone is not a wasted hour but a"
    " holy one. When the Ghost rises in {name_vault} and the interior closes further, would"
    " you give {name_vault} the courage to open one door \u2014 to show {name_camp} one"
    " unfinished thing, uncurated, trusting that what is found will be received.",

    "Make our home a room where {name_camp} does not have to run in order to belong, and"
    " where {name_vault} does not have to present a finished product in order to be loved."
    " Make our table a place where the inward being \u2014 the secret heart that you"
    " delight in \u2014 is what we actually bring to each other, rather than the polished"
    " version each of us has learned to show the world.",

    "And Father, when we are old and the campaigns have finally run their last race and the"
    " Vault has at last been opened fully \u2014 let us look back and see that the small"
    " repeating rocks became smaller, and that the home we built together was one in which"
    " both of us were more fully known than we have ever been known before.",

    "In the name of the One who was made visible, fully and at great cost, so that we might"
    " be covered \u2014 and who calls what is hidden in us his own.",

    "Amen.",
]

DATE_NIGHT_OPENING = [
    "Most of what you have read so far has been spoken <i>to</i> you. The pages that follow"
    " are different. They are meant to be spoken <i>between</i> you.",

    "What follows is a date-night conversation, designed to be taken slowly, somewhere quiet,"
    " with no children in the room and no phones on the table. There are six rounds, and they"
    " build on each other. Resist the temptation to skip ahead. Start at Round One even if it"
    " feels too light; the lightness is the point. The document earns the harder rounds by"
    " starting with the easier ones.",

    "Some of the questions are playful. Some are direct. A few are the kind that, when"
    " answered honestly, will sit with both of you for the rest of the week. None of them"
    " are trivia. All of them are an invitation.",

    "<b>How to use it.</b> One of you reads a question aloud. The one who did not read"
    " answers first, in full, without interruption. Then the reader answers the same question."
    " Then you move on. You do not have to finish all six rounds in one evening \u2014"
    " two or three rounds, taken seriously and without rushing, is often better than racing"
    " through all of them. Save the rest for the next date.",

    "<b>One rule.</b> The other person\u2019s answer is never wrong. You may not love"
    " everything you hear. Stay with it anyway. The goal is not to assess each other\u2019s"
    " answers. The goal is to be known, and to do the patient work of knowing.",
]

ROUND_1 = [
    (
        "hypothetical",
        "If our marriage were a room in a house, what kind of room would it be, and what"
        " would it look like on its best day?",
        "Let the metaphor do the work. The first answer that comes to mind is usually"
        " the most honest one."
    ),
    (
        "observation",
        "What is one thing I did this week that you noticed and did not mention?",
        "Not a complaint and not necessarily a compliment. A noticing."
        " The fact that you noticed at all is worth naming."
    ),
    (
        "playful",
        "If the two of us were characters in a novel, what kind of novel would it be,"
        " and what chapter are we in right now?",
        "Say the first thing that comes to mind. Then explain why you chose it."
    ),
]

ROUND_2 = [
    (
        "fill-in-blank",
        "I don\u2019t think I tell you this enough \u2014 I am genuinely amazed at the way"
        " God made you so _______. Your _______ is a gift to this marriage, and I want to get"
        " better at receiving it.",
        "Two blanks. Resist the general answer. \u2018Strong\u2019 is too easy;"
        " \u2018able to hold something difficult completely alone so that I never had to"
        " worry about it\u2019 is closer to what this question is asking for."
    ),
    (
        "observation",
        "What is one thing you have watched me do this year that you wish more people"
        " got to see?",
        "Most of us only ever see ourselves in our public moments."
        " Your spouse has seen the private ones. This question is about those."
    ),
    (
        "one-word",
        "If you had to choose one word to describe what it feels like when I walk into"
        " the room at the end of a long day, what word would it be?",
        "One word, said out loud. Then explain it briefly, without editing yourself."
    ),
]

ROUND_3 = [
    (
        "forward-looking",
        "Five years from now, when we look back on this season of our marriage, what do"
        " you hope we will say we finally learned to do together?",
        "Not what you wish you had done. What you want, when you look back from five"
        " years out, to be able to say you actually did."
    ),
    (
        "theological",
        "Where, in the past month, have you seen God specifically at work in me"
        " \u2014 not where you hope he will work, but where you have already seen it?",
        "Name it. Be specific. This is not flattery; it is bearing witness"
        " to what you have actually observed."
    ),
    (
        "shared-identity",
        "Finish this sentence three times: \u2018We are the kind of couple who _______.\u2019"
        " Give one playful answer, one true answer, and one aspirational answer.",
        "The \u2018we\u2019 is the point. Let the three answers be genuinely different"
        " from each other."
    ),
]

ROUND_4 = [
    (
        "strength",
        "What is something I carry for this marriage that you would have to learn to carry"
        " alone if I were not here?",
        "Hard to ask. Important to hear. Stay with the answer even if it surprises you."
    ),
    (
        "fill-in-blank",
        "One of the gifts of being married to you is that I get to be _______ in ways"
        " I never would have been on my own.",
        "A version of yourself that only exists because this marriage exists. Name it."
    ),
    (
        "observation",
        "Name one moment in our story where you knew, without any doubt, that we had"
        " built something together that neither of us could have built alone.",
        "Tell the whole story. The remembering is part of the strengthening."
    ),
]

ROUND_5 = [
    (
        "hard",
        "{name_camp}, when the Campaign in you is running hardest \u2014 when the output"
        " is up and the significance trigger has fired \u2014 what do you most wish"
        " {name_vault} knew about what that moment feels like from the inside?",
        "Not a critique of {name_vault}\u2019s response. An account of the experience"
        " of being in the mechanism. There is a difference, and it matters."
    ),
    (
        "hard",
        "{name_vault}, when the walls in you go up \u2014 when something has landed and"
        " the Vault closes and you find yourself presenting a composed exterior while"
        " something is happening inside \u2014 what do you most wish {name_camp} knew"
        " about what that moment feels like from the inside?",
        "Not a critique of {name_camp}\u2019s response. An honest account of what the"
        " interior closing feels like to the one inside it."
    ),
    (
        "profile-aware",
        "What is one thing you have been carrying this past month that you have not"
        " brought to the other person, and what has kept you from bringing it?",
        "Not an accusation. An invitation. The person asking commits to hearing the"
        " answer without immediately making it something to fix or manage."
    ),
]

ROUND_6 = [
    (
        "blessing",
        "Place your hand on your spouse\u2019s hand. Say their name. Then say:"
        " \u2018You do not have to perform for me. You do not have to be finished for me."
        " You are enough, exactly as you are, right now.\u2019 Say it slowly."
        " Let them say it back.",
        "You may feel self-conscious. That is part of why it works. Do it anyway."
    ),
    (
        "prayer",
        "Pray for each other \u2014 out loud, by name, in one or two sentences."
        " Pray specifically for the thing they told you in Round Five.",
        "This is the close of the date. The prayer is not a formality."
        " It is the act of handing the evening to the God who was present for all of it."
    ),
]


def _render(text, name_camp, name_vault):
    return text.format(name_camp=name_camp, name_vault=name_vault)


def build(sub_a, sub_b) -> bytes:
    """Generate the Performance Campaign + Vault couples walkthrough PDF.

    sub_a: the submission of the Performance Campaign spouse (CAMP)
    sub_b: the submission of the Vault spouse (VAULT)
    """
    ensure_fonts()
    S = make_styles()

    name_camp = _first_name(sub_a, "Performance")
    name_vault = _first_name(sub_b, "Vault")

    def R(text):
        return _render(text, name_camp, name_vault)

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Couples Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUPLES WALKTHROUGH",
        cover_right_label=f"{name_camp.upper()}  +  {name_vault.upper()}",
        title=f"Take 139 Couples Walkthrough \u2014 {name_camp} & {name_vault}",
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
    story.append(Paragraph(f"{name_camp} &nbsp;&amp;&nbsp; {name_vault}", S["CoverNames"]))

    cover_tbl = Table(
        [[
            Paragraph(
                f"<font color='#8a4a2c'><b>{name_camp.upper()}</b></font><br/>"
                "Performance Campaign &middot; Attorney<br/>"
                "<font size=9 color='#6b6862'>Significance &middot; Am I enough to be remembered?</font>",
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
        "<i>\u201cBehold, you delight in truth in the inward being,<br/>"
        "and you teach me wisdom in the secret heart.\u201d</i>",
        ParagraphStyle("cq", fontName="Fraunces-Italic", fontSize=11, leading=18,
                       textColor=MUTED, alignment=TA_CENTER)))
    story.append(Paragraph(
        "Psalm 51:6",
        ParagraphStyle("cqa", fontName="Inter", fontSize=9, leading=14,
                       textColor=MUTED, alignment=TA_CENTER, spaceBefore=4)))

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
            _profile_card(S, name_camp, ACCENT, "Significance",
                          "Am I enough to be remembered?",
                          "The Performance Campaign", "The Attorney"),
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

    # ── SECTION 3: THE PERFORMANCE'S GIFT TO THE VAULT ──
    section_header(story, S, "SECTION THREE  \u00b7  THE PERFORMANCE\u2019S GIFT TO THE VAULT",
                   f"What {name_camp} gives {name_vault}.",
                   "A witness who stands in the room and is seen \u2014 which the Vault needs but rarely builds.")
    for p in GIFT_TO_VAULT:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 4: THE VAULT'S GIFT TO THE PERFORMANCE ──
    section_header(story, S, "SECTION FOUR  \u00b7  THE VAULT\u2019S GIFT TO THE PERFORMANCE",
                   f"What {name_vault} gives {name_camp}.",
                   "A room that does not require the campaign to run \u2014 which the Campaign has never quite found.")
    for p in GIFT_TO_CAMP:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 5: THE COLLISION ──
    section_header(story, S, "SECTION FIVE  \u00b7  THE COLLISION",
                   "Significance meets the locked room.",
                   "Two mechanisms, each asking the other for the one thing it cannot readily give.")
    for p in COLLISION[:4]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The loop, in slow motion.",
                   "And the way out, in each spouse\u2019s own grammar.")
    for p in COLLISION[4:]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 6: THE HARDER PICTURE ──
    section_header(story, S, "SECTION SIX  \u00b7  THE HARDER PICTURE",
                   "When the Quiet Exit and the Ghost are in the room at once.",
                   "The marriage looks fine. Neither of you is present.")
    for p in BOTH_BREAK[:5]:
        story.append(Paragraph(R(p), S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  CONTINUED",
                   "What to do while you can still see it.",
                   "Three practices, in order, for the moment of recognition.")
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
    story.append(Paragraph(f"FROM {name_camp.upper()}, TO {name_vault.upper()}", S["CommitLabel"]))
    story.append(HRFlowable(width="30%", thickness=0.6, color=ACCENT,
                            hAlign="LEFT", spaceBefore=2, spaceAfter=10))
    for commit_name, body in CAMP_COMMITMENTS:
        story.append(KeepTogether([
            Paragraph(commit_name, S["H3"]),
            Paragraph(R(body), S["CommitBody"]),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   f"From {name_vault}, to {name_camp}.",
                   "Three commitments, in the Vault\u2019s voice, for the Campaign to receive.")
    story.append(Paragraph(f"FROM {name_vault.upper()}, TO {name_camp.upper()}", S["CommitLabelHer"]))
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
                  "The lightness is the point. Start here even if you\u2019d rather skip ahead.")
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
        "You do not have to perform for me.<br/>"
        "You do not have to be finished for me.<br/>"
        "You are enough, exactly as you are, right now.",
        closing_style))

    doc.build(story)
    return finalize_buffer(buf)


# ── STANDALONE TEST ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    import io

    class FakeSubA:
        primary_mechanism = "CAMP"
        primary_breakdown = "ATTY"
        primary_trigger = "SIG"
        core_question = "REM"
        name = "Jordan"

    class FakeSubB:
        primary_mechanism = "VAULT"
        primary_breakdown = "ATTY"
        primary_trigger = "SHM"
        core_question = "ACC"
        name = "Taylor"

    pdf_bytes = build(FakeSubA(), FakeSubB())
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "performance_vault_test.pdf")
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
            if "SECTION THREE" in txt and ("PERFORMANCE" in txt or "GIFT" in txt):
                snippet = txt.strip()[:200]
                break
        if not snippet:
            for page in reader.pages[4:8]:
                txt = page.extract_text() or ""
                if txt.strip():
                    snippet = txt.strip()[:200]
                    break
    except Exception as e:
        page_count = "unknown"
        snippet = f"(pypdf error: {e})"

    print(f"DONE: performance_vault.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Section Three snippet: {snippet!r}")
