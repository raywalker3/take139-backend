"""Personal Walkthrough — Performance Campaign + Flood.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Significance trigger, "Am I enough to be remembered?" core question.
~25 pages, 9 sections.

Calibration anchor: Walkthrough 33 of 36 — Performance Campaign + Flood.
Preserves Ambassador/Adapter distinction and "let me show you one more thing"
and "two kinds of producing" from performance_attorney.py.

THE PERFORMANCE+FLOOD DISTINCTIVE:
The most public of all the Floods. The Performance has built its entire
visibility on being unflappable — polished, calibrated, composed. When the
Flood comes, it tends to happen in front of an audience: in a meeting, at a
pulpit, on stage, at the family table, or in the hallway when one person
finally asks "are you okay?" and the dam breaks. The breakdown is often
professionally consequential because composure was the brand.

Unique pastoral move in Section Five: the Flood is paradoxically a mercy to
the Performance — because the Performance can no longer hide behind the polished
output. The audience has now seen the runner exhausted. The Performance has
wanted to be seen for what it produced; now it has been seen for who it actually
is. This is sometimes the first moment grace can land.

Key Scripture: 2 Corinthians 12:9-10 (power made perfect in weakness).
Key voice: Charles Spurgeon (preached through depression).
Key reference: Keller, Walking with God through Pain and Suffering, on
suffering as the unmaking of false selves.
"""
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Paragraph, Spacer, KeepTogether, HRFlowable, Table, TableStyle,
    PageBreak, NextPageTemplate,
)

try:
    from ..base import (
        make_doc, make_styles, finalize_buffer, ensure_fonts,
        section_header, journal_lines, divider,
        PAGE_W, MARGIN_L, MARGIN_R,
        PAPER, INK, ACCENT, MUTED, RULE, HIGHLIGHT_BG,
    )
except ImportError:
    import sys as _sys
    import os as _os
    _sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
    from base import (
        make_doc, make_styles, finalize_buffer, ensure_fonts,
        section_header, journal_lines, divider,
        PAGE_W, MARGIN_L, MARGIN_R,
        PAPER, INK, ACCENT, MUTED, RULE, HIGHLIGHT_BG,
    )


# ──────────── PROSE ────────────

OPENING_BODY = [
    "Before you read any further, I want to do for you what a good counselor does at the start "
    "of a first session. I want to lower the lights and slow the pace, because what you are about "
    "to encounter is not a performance review. It is something considerably more uncomfortable "
    "than that. It is a patient conversation about the way your soul has learned to keep itself "
    "safe in a world that has, in specific and repeated ways, declined to see you as clearly as "
    "you needed to be seen. You are, in the deepest sense, a runner \u2014 a person who discovered, "
    "early in life, that moving forward at speed \u2014 building, achieving, demonstrating, producing "
    "\u2014 was the surest path to being noticed, valued, and kept. You learned that ordinary was "
    "forgettable. And forgettable, in the economy of your early world, was not safe.",

    "We are going to walk through your trigger \u2014 the specific moment your nervous system "
    "says <i>something is wrong here</i>. We will sit with the question underneath that moment, "
    "the one that has probably been with you since the first time you understood that some people "
    "are remembered and others are not. We will name the strategy you have constructed in "
    "response, and the place that strategy collapses when the weight of what you have built "
    "becomes, at last, too heavy to carry alone. And then, only then, will we put tools in "
    "your hands.",

    "If you were sitting across from me right now, I would say this carefully and mean every "
    "word of it. <b>What you are about to read is true, but it is not the whole truth about "
    "you.</b> The whole truth includes a Father who did not first require a curriculum vitae "
    "before deciding whether to love you; a Son whose entire life was spent in the company of "
    "people who produced nothing for him; and a Spirit who is, at this very moment, more "
    "interested in the person behind the portfolio than in anything the portfolio contains.",

    "So read slowly. Argue with what does not fit. Stay with what catches. Write in the margins. "
    "Pray when something lodges in your throat, because that lodging is usually the Lord saying, "
    "<i>look here, with me, at what is actually happening.</i> The goal of this walkthrough is "
    "not a better performance. It is a slightly freer life, lived from a self that does not need "
    "to earn its standing before every conversation begins. Take your time. The chapter you are "
    "about to read about yourself has been running for many years. It deserves a few hours "
    "of patient attention.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it is remarkably easy to miss because "
    "it hides so effectively inside experiences that look, from the outside, like perfectly "
    "reasonable frustration. Someone at work fails to credit you for an idea you clearly "
    "introduced. A friend tells the story of something you did together but edits you to the "
    "margins. Your spouse turns toward their phone at the exact moment you begin describing "
    "something that cost you real effort. A committee makes a decision in your area of expertise "
    "without consulting you. And something inside you, in under three seconds, goes from "
    "zero to a temperature that the event, on its face, does not seem to warrant.",

    "What fired in those three seconds was not, strictly speaking, irritation. It was not "
    "pride, though pride will arrive shortly. What fired was an alarm, and the alarm has a "
    "specific frequency: <i>I am being treated as though I am replaceable.</i> As though the "
    "work does not count. As though the years of investment, the sustained excellence, the "
    "accumulated evidence of what you can do and what you have done \u2014 none of it has "
    "actually registered. You are being looked through, as if you were any person off the "
    "street rather than the specific person who has built the specific thing now standing "
    "in front of them.",

    "This is your trigger. The technical word for it is <b>significance</b>, but the word needs "
    "careful unpacking, because it carries a freight it does not immediately appear to carry. "
    "This is not vanity, though vanity sometimes clings to it. This is not the simple desire "
    "for applause, though applause is welcome. It is something more fundamental: the longing "
    "to matter. To have one's presence register. To be known not merely as a face in the crowd "
    "but as a person who has shown up, done the work, and earned the right to be "
    "seen doing it.",

    "C. S. Lewis, in <i>The Weight of Glory</i>, named the longing more precisely than almost "
    "anyone else: <i>We do not want merely to see beauty, though, God knows, even that is "
    "bounty enough. We want something else which can hardly be put into words\u2014to be "
    "united with the beauty we see, to pass into it, to receive it into ourselves, to bathe "
    "in it, to become part of it.</i> He was speaking of beauty, but the grammar of the "
    "longing is the same as yours. You do not merely want to do excellent work. You want to "
    "pass into it, to have it received, to be united with the recognition it represents. "
    "When the recognition does not come \u2014 when the excellent work lands in silence \u2014 "
    "the pain is not proportionate to the circumstance. It is proportionate to the "
    "longing underneath.",

    "<b>Your sensitivity to significance is not random.</b> It is the residue of something "
    "learned in a specific season of your history, usually early, always formative. Perhaps "
    "you grew up in a household where love was notably warmer when you performed. Perhaps ordinary "
    "effort was unremarkable and extraordinary effort was, finally, noticed \u2014 which trained "
    "your system to the conclusion that the path to being seen ran through the extraordinary. "
    "Whatever its specific origin, the lesson arrived with the force of a conviction: "
    "<i>I will not be forgotten if I cannot be ignored.</i> And so you began to build \u2014 "
    "not the Architect's careful blueprints, that is a different mechanism, but to produce, "
    "to demonstrate, to show what you could do in the full light of day. You ran. And the "
    "running, over time, became not just a strategy but an identity. The Performance Campaign "
    "was born.",

    "Before we go further, I want you to sit with two questions in writing. Your head will "
    "reframe them in terms of the next campaign. Your hand will be more honest.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week, that the significance trigger fired. What "
    "happened? Who failed to see you, or what effort went unacknowledged? Write two sentences.",

    "What was the size of the actual event, and what was the size of the response inside "
    "you? If they did not match, you have just located the trigger \u2014 and underneath "
    "it, a question that is older than the event.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The "
    "trigger is the alarm; the question is the wound the alarm has spent years guarding.",

    "Yours is this: <b>Am I enough to be remembered?</b>",

    "It is not the same as <i>Am I competent?</i>, though you have built extraordinary "
    "competence in part as an attempt to answer it. It is not <i>Am I loved?</i>, though "
    "you have spent considerable energy in relationships that felt like they might finally "
    "answer it. It is something more primal than either: the question a child asks in the "
    "moment they realize that the world has a great many people in it, that most of those "
    "people will be forgotten, and that being forgotten is, somehow, the deepest kind of "
    "not-mattering. <i>Will I leave something behind that is still there when I am gone? "
    "Will anyone remember I was here?</i>",

    "You have almost certainly never put it in those words. The Performance never does. "
    "The Performance translates the question into action rather than sitting with it. "
    "But trace backward from the alarm that fired this week, and from the one that fired "
    "the week before, and from the campaign you have been running for the last decade, and "
    "you will find this question at the root of all of it. <i>Am I enough to be "
    "remembered?</i> And behind that question, barely below the surface, its "
    "companion: <i>Or am I, after everything, ordinary?</i>",

    "The fear of ordinariness is one of the most socially acceptable fears a person can "
    "carry in our present age, which makes it both easier and harder to see clearly. Easier, "
    "because the culture around you tends to validate the Campaign and reward the runner. "
    "Harder, because the validation makes it almost impossible to notice that what you "
    "are running from is not obscurity but the question of your worth, and that no "
    "quantity of achievement has ever, in your experience, fully silenced it.",
]

QUESTION_BODY_P2 = [
    "There is a reason that the biblical tradition, from its earliest pages to its last, "
    "insists on the significance of those the world has forgotten. The Psalms were written "
    "by and for people who felt unseen and unnamed, and who brought that wound directly to "
    "God rather than sublimating it into a campaign.",

    "<i>Can a woman forget her nursing child, that she should have no compassion on the son "
    "of her womb? Even these may forget, yet I will not forget you. Behold, I have engraved "
    "you on the palms of my hands.</i> (Isaiah 49:15\u201316)",

    "The image is almost too intimate. Not engraved in a ledger, not recorded in a database, "
    "not awarded a certificate of achievement. Engraved on the palms of his hands \u2014 "
    "the part of the body that a person carries in front of their face every waking hour, "
    "the part that is always visible, always present. God is saying: when I look at my own "
    "hands, I see you. You are not forgettable. You are not ordinary. You are not anonymous. "
    "You are, in the most literal possible sense, impossible to forget.",

    "But \u2014 and this is where the honest pastoral work begins \u2014 the answer "
    "Scripture gives to your question is not the answer your nervous system has been "
    "trying to construct. Your nervous system has been trying to construct an answer made "
    "of accomplishments: <i>if I build enough, produce enough, achieve enough visible "
    "excellence, I cannot be ignored, and if I cannot be ignored, I cannot be forgotten, "
    "and if I cannot be forgotten, I am safe.</i> What Scripture says is something "
    "stranger and, in the long run, more solid: your significance is not produced. "
    "It is received. It is not earned by the campaign. It is given before "
    "the campaign begins.",

    "Paul puts it with his characteristic bluntness in Ephesians 1:4\u20135: "
    "<i>he chose us in him before the foundation of the world, that we should be holy "
    "and blameless before him. In love he predestined us for adoption to himself as sons "
    "through Jesus Christ.</i> Before anything you have ever built. Before any credential "
    "you have ever earned. Before the campaign had a single entry. Chosen. Named. "
    "Inscribed on the palms of his hands.",
]

QUESTION_BODY_P3 = [
    "The difficult honest work this section asks of you is not to stop achieving. The "
    "Performance Campaign is not, in itself, a sin. It is a gift that has been pressed "
    "into service as a salvation strategy, and it is wearing both itself and you down "
    "in the process.",

    "The honest work is to begin, slowly and with patience, distinguishing between two "
    "very different kinds of producing. There is producing that flows from gratitude \u2014 "
    "from a person who already knows they are seen and significant, who creates and builds "
    "from fullness rather than from need. And there is producing that flows from anxiety \u2014 "
    "from a person who is still trying to earn the significance that was given before "
    "they drew their first breath. From the outside, these two persons look almost "
    "identical. From the inside, one is free and the other is exhausted.",

    "The runner who knows they are already known can stop. The runner who is running "
    "to be known cannot \u2014 because stopping would mean risking the question: "
    "<i>and if I am not running, who am I?</i> That question is the one we need to "
    "stay with before we go any further.",

    "Before we close this section, use the table below. In the first column, name an "
    "event from the past week in which the significance trigger fired. In the second, "
    "answer your nervous system's question: <i>was I seen here?</i> In the third, "
    "answer the deeper question: <i>was the part of me that finally matters \u2014 "
    "my soul, my standing before God \u2014 at any point in danger?</i>",
]

CAMP_BODY_P1 = [
    "You have built something. It did not announce itself as a strategy; it announced "
    "itself as a life. But over years and campaigns and the accumulation of evidence, "
    "you have developed a particular way of moving through the world that we are going "
    "to call, throughout the remainder of this walkthrough, <b>the Performance Campaign</b>.",

    "It is important, before we go any further, to say what the Performance Campaign is "
    "not. It is not the Ambassador's mechanism. The Ambassador serves in order to be loved "
    "\u2014 brings warmth, manages emotional temperature, pours out care and waits, "
    "sometimes invisibly, for the love to come back. The Ambassador's currency is relational "
    "service. The Performance's currency is visible output. The Ambassador is the one who "
    "stayed late to make sure everyone was okay; the Performance is the one who stayed late "
    "to finish something extraordinary and wants you to know about the extraordinary thing. "
    "Both are earning, in a sense, but they are earning different things and using "
    "different methods.",

    "Nor is it the Adapter's mechanism. The Adapter reads the room and becomes what the "
    "room needs \u2014 calibrates its self to the audience, fluently and genuinely, as a "
    "way of purchasing connection. The Performance does not calibrate to the room. "
    "The Performance demonstrates to the room. The Adapter is asking, at some level, "
    "<i>what do you need from me?</i> The Performance is asking, at some level, "
    "<i>do you see what I have done?</i> The Adapter disappears into the audience; "
    "the Performance stands before it.",

    "The Performance Campaign is the runner. It is the achiever. It is the person who "
    "has a long r\u00e9sum\u00e9 and, often, a thin sense of who they are off the field. It is "
    "the person whose default response to anxiety is not to plan (that is the Architect) "
    "and not to withdraw (that is the Island), but to <i>produce</i>. When the question "
    "fires \u2014 <i>am I enough to be remembered?</i> \u2014 the Performance's answer "
    "is always the same: <i>let me show you one more thing.</i>",
]

CAMP_BODY_P2 = [
    "There is a great deal in Scripture that commends the kind of diligence the Performance "
    "embodies at its best. Proverbs 22:29 says: <i>Do you see a man skillful in his work? "
    "He will stand before kings; he will not stand before obscure men.</i> Excellence is "
    "genuinely valued in the biblical tradition. Work done with care and craft is, in "
    "Colossians 3:23, an act of worship: <i>Whatever you do, work heartily, as for the "
    "Lord and not for men.</i> The Performance Campaign is not, at its root, a sin. "
    "It is a gift. The runner was given legs and taught to run, and the running has "
    "been genuinely beautiful.",

    "But the trouble, as with all gifts, is in the purpose the gift has been pressed to "
    "serve. The Campaign's drive to achieve, build, and leave a mark does something specific "
    "for it. It answers the question <i>do I matter?</i> through achievement. If I can "
    "point to something I built, I know I existed. The producing is, underneath its genuine "
    "pleasure and craft, also an existential argument. <i>I was here. I did this. "
    "You cannot pretend I was not in this room.</i>",

    "And there is something in you, reading that sentence, that recognizes it. Perhaps "
    "with a flicker of relief. Perhaps with a flicker of resistance, because the naming "
    "makes it visible in a way that feels, however briefly, like exposure. Both "
    "reactions are honest. Let them be what they are. The specific history that tends "
    "to produce the Performance Campaign takes several forms: perhaps ordinary "
    "achievement was unremarkable in your family while extraordinary achievement was "
    "noticed and rewarded. Perhaps you grew up feeling genuinely invisible \u2014 in a "
    "large family, a distracted household, or a school where the quiet student "
    "disappeared \u2014 and achievement became the antidote: <i>if I am impressive "
    "enough, I cannot be ignored.</i> Perhaps there was significant loss in your "
    "family of origin and you became the one who would prove the name was worth "
    "something. Perhaps the drive to leave a mark is partly grief looking for "
    "somewhere to live.",
]

CAMP_BODY_P3 = [
    "Whatever the specific history, the Performance Campaign arrived with a characteristic "
    "shape. The Campaign is genuinely energizing: the pursuit \u2014 the building, the "
    "vision, the satisfaction of something done with real excellence \u2014 fills you in "
    "a way that few other experiences do. Rest, by contrast, does not fill you. Rest "
    "feels, if you are honest, like a kind of death \u2014 not physical rest necessarily, "
    "but the cessation of forward movement, the afternoon when there is nothing to "
    "produce and nothing to demonstrate. That produces, with disturbing regularity, "
    "an anxiety with no obvious cause. Because the cause is not in the afternoon. "
    "It is in the question the afternoon allows to surface: <i>and who are you, "
    "when you are not running?</i> Your spouse \u2014 or the person who has known "
    "you longest \u2014 has probably said some version of the same sentence more than "
    "once: <i>I feel like an afterthought.</i> They are not wrong. The Campaign has "
    "a visibility problem: it can see the next achievement with extraordinary clarity, "
    "and the people standing quietly in the room \u2014 wanting simply to be with you "
    "\u2014 blur at the edges.",

    "Hear me carefully. <b>The Performance Campaign is not your enemy.</b> It is "
    "a younger version of you who learned, in some real and specific circumstance, "
    "that achievement was the reliable path to being seen, and that being seen was "
    "necessary for being safe. He has been faithful. He has produced genuinely "
    "remarkable things. He deserves your respect. But he is not twelve any longer, "
    "and you are not in the household or the classroom or the early career context "
    "that required him. He is running a race on a track that no longer leads where "
    "he thinks it leads. The finish line he is running toward \u2014 <i>finally "
    "enough, finally seen, finally safe from being forgotten</i> \u2014 is not, "
    "and has never been, at the end of that particular track.",

    "What does it look like to begin slowing the Campaign, not retiring it, but "
    "giving it shorter hours and a different mandate? It begins with the question "
    "the Campaign almost never asks: <i>what do I actually want, from the people "
    "who love me, that my achievements cannot give me?</i> The letter below is the "
    "Campaign's attempt to answer that question in his own voice. Read it slowly.",
]

CAMP_LETTER_INSTRUCTION = [
    "The letter below is written from the Performance Campaign, in his own voice, "
    "to you. He is not a villain. He is a builder who confused his output for his "
    "worth. Read it slowly. Then answer the three prompts that follow.",

    "Dear [your name],",

    "I need to tell you something I have never said, because I have never stopped "
    "long enough to say it. The stopping is the problem. I do not do well with "
    "stopping. When there is nothing to build, nothing to demonstrate, nothing "
    "pointing toward the next achievement, I do not know what to do with the silence. "
    "The silence has always felt like danger.",

    "I learned early that excellence was noticed and ordinary was not. Someone whose "
    "opinion mattered enormously to you looked up when you achieved something and "
    "looked back down when you did not, and your system drew the conclusion before "
    "you were old enough to question it: <i>the path to being seen runs through "
    "the extraordinary.</i> And so I began. I built the campaign. I ran.",

    "I want you to know what I actually did for you. I kept you visible. I kept "
    "you in the conversation. I gave you something to point to when the question "
    "came \u2014 and the question always came: <i>what have you done? Why should "
    "you matter?</i> I made sure you always had an answer. What I could not do "
    "\u2014 what I am only now beginning to see I was never equipped to do "
    "\u2014 is give you a self that was secure when the campaign went quiet. "
    "I could make you visible. I could not give you the knowledge that you "
    "were enough even when invisible. That the people who love you are not "
    "keeping score. That you can stop, and still be held.",

    "And I need to tell you something about the Flood. When it came \u2014 "
    "when you lost composure in the meeting, or in the hallway after the event, "
    "or at the table in front of the people whose opinion matters most \u2014 "
    "I was ashamed. The whole campaign is built on composure. Built on the polished "
    "surface that says: I have this handled, I am someone who handles things. "
    "The Flood took that from us. And I spent the days afterward trying to "
    "rebuild the surface faster than it had fallen.",

    "But here is the thing I am learning to say: the Flood showed them something "
    "the campaign never did. It showed them you. Not the output. You. The person "
    "inside the achievement who has been carrying more than any single campaign "
    "was built to hold. I am not sure that is a failure. I am only sure "
    "that I was never the right one to carry it alone.",

    "The Performance Campaign",
]

CAMP_LETTER_PROMPTS = [
    "What part of the Campaign's letter surprised you? Not the part you expected "
    "\u2014 the part you were not quite ready to read.",

    "The Campaign says he could make you visible but could not give you the "
    "security of being enough when invisible. When was the last time you "
    "felt genuinely at rest \u2014 not productive rest, not earned vacation, "
    "but the rest of a person who has nothing to prove? Describe that moment, "
    "or describe the absence of it.",

    "The Campaign says the Flood showed them something the campaign never did. "
    "Name one person who witnessed your Flood \u2014 or who came closest to it. "
    "What do you imagine they saw? What do you wish they had understood?",
]

FLOOD_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Performance Campaign, the breaking "
    "takes a form that is, among all the versions of the Flood we have described in this "
    "series, the most publicly consequential. We call it <b>the Flood</b> deliberately, "
    "because a flood does not build argument and it does not compose itself. It releases. "
    "It does not discriminate \u2014 it carries everything that was waiting behind the dam: "
    "sorted and unsorted, old and new, proportionate and disproportionate. For the "
    "Performance, the particular terror of the Flood is not merely that it comes, "
    "but <i>where</i> it comes.",

    "The Architect's Flood is a planner whose dam finally bursts after months of "
    "impossible suppression. The Island's Flood is the first cost-signal of a long "
    "silence, arriving at a moment no one anticipated. The Ambassador's Flood is the "
    "invisible ledger speaking at last, all the givings inventoried aloud. The Vault's "
    "Flood is the file cabinet falling open. The Adapter's Flood is an involuntary "
    "integration of selves that have been kept apart. The Performance's Flood is different "
    "from all of these in one decisive respect: it tends to happen in public. The "
    "Performance has built its entire platform on being unflappable. Composure is not "
    "merely a personal preference \u2014 it is the brand. And so when the Flood comes, "
    "it comes at the worst possible time: in the meeting, on the stage, at the pulpit, "
    "in the hallway when one colleague stops and asks, \u2018are you all right?\u2019, "
    "and everything pours out at once.",

    "Here is how it happens. The Campaign has been running. For months, sometimes for years, "
    "it has been producing, building, demonstrating, achieving \u2014 and simultaneously "
    "absorbing things it has not released. The significance trigger has been firing, quietly "
    "and repeatedly, and the Campaign has been filing each instance rather than addressing it, "
    "because addressing it would require a kind of vulnerability the Campaign has not learned "
    "to perform. The Campaign can manage a press conference. It cannot manage a wound "
    "acknowledged in real time. So the wound goes underground, joins the other wounds, "
    "and the pressure grows.",
]

FLOOD_BODY_P2 = [
    "Then something small lands. Not necessarily a large thing \u2014 a flat response "
    "from someone whose opinion matters more than it should, a slight in the middle of "
    "a presentation, a criticism delivered in front of the wrong audience, a moment in "
    "which the excellence was not seen, and the runner has been running long enough that "
    "the particular smallness of the moment is the last weight the structure can absorb. "
    "And then \u2014 often, for the Performance, in a context that carries maximum "
    "professional cost \u2014 the Flood comes. Tears in the board meeting. Intensity "
    "that startles everyone in the room. The emotion that has been absent from ten "
    "years of brilliant composure, arriving all at once, at the least convenient moment "
    "the calendar could have provided.",

    "The people who witness this do not know what to do with it, because the Performance "
    "has trained them over years to expect the polished version. They have never been "
    "given reason to anticipate the exhausted version. <i>I thought you had this.</i> "
    "They say it with their faces if not with their words. And the Performance, in the "
    "hours and days after the Flood, does something characteristic and predictable: "
    "it rebuilds the wall faster than it fell. It works to reassure everyone that the "
    "Flood was an exception, an anomaly, a bad week. It performs recovery the way it "
    "performs everything else \u2014 visibly, convincingly, and at considerable cost to "
    "whatever was actually underneath the wall.",

    "<b>What the Campaign most fears about the Flood is what the Flood actually reveals.</b> "
    "Not weakness in the ordinary sense \u2014 the Performance has a perfectly adequate "
    "theology of weakness in the abstract. What the Flood reveals is that the campaign "
    "has not been working the way the Campaign has been insisting it works. That the "
    "composure was always, at least in part, a performance. That the runner is tired in "
    "a way that one more achievement will not fix. And that the people in the room, "
    "the audience the Campaign has been performing for all these years, have now seen "
    "something the Campaign never intended to show them: the person who is there when "
    "the performance stops.",
]

FLOOD_BODY_P3 = [
    "Here is where the pastoral move in this section must be made with both hands, because "
    "it runs against everything the Campaign's instincts will tell it. The pastoral move "
    "is this: <b>the Flood is, paradoxically, a mercy to the Performance. It is not the "
    "moment the Campaign failed. It is, sometimes, the first moment grace can land.</b>",

    "Paul, in 2 Corinthians 12:9\u201310, describes receiving from Christ a word that the "
    "Campaign will find almost impossible to receive without resistance: <i>My grace is "
    "sufficient for you, for my power is made perfect in weakness. Therefore I will boast "
    "all the more gladly of my weaknesses, so that the power of Christ may rest upon me. "
    "For when I am weak, then I am strong.</i> The apostle who wrote this was not "
    "romanticizing incompetence or advocating an end to effort. He was saying something "
    "much more dangerous to the Campaign: that the power of Christ has a specific address, "
    "and that address is weakness, not strength. That the composure the Campaign has "
    "constructed is precisely the thing that makes the resting place of Christ's power "
    "inaccessible. That the Flood, as unwelcome as it is, may be the first time the "
    "address was available.",

    "Charles Spurgeon preached through decades of public ministry while carrying a "
    "depression severe enough that he sometimes could not rise from his bed the week "
    "before he was scheduled to preach to thousands. He was perhaps the most visible "
    "minister in the English-speaking world, and he was undone regularly in private by "
    "the very weight the Campaign most fears. He did not hide it entirely. And in one "
    "of his most searching observations, he wrote: <i>I have learned to kiss the wave "
    "that throws me against the Rock of Ages.</i> This is not a sentence a person "
    "writes from the position of composure. It is a sentence written from the position "
    "of having been thrown, publicly, repeatedly, and having found that what one lands "
    "against when the wave has done its worst is solid.",

    "Tim Keller, in <i>Walking with God through Pain and Suffering</i>, observes that "
    "suffering has a particular ministry to the person who has built a false self \u2014 "
    "and that the achiever's false self is among the most elaborately constructed. "
    "The suffering \u2014 including the particular suffering of public exposure, the "
    "Flood witnessed by the wrong people at the wrong time \u2014 does something "
    "to the false self that no amount of achievement can do. It unmakes it. Strips it "
    "of its pretension to be the whole story. And in that unmaking, a different self "
    "becomes visible: one that is smaller, less polished, and considerably more real. "
    "The Performance has wanted to be seen for what it produced. The Flood has been seen "
    "for who it actually is. The audience in that meeting, that hallway, that family table "
    "\u2014 they did not see the portfolio. They saw the runner, exhausted. "
    "For the Gospel to be anything more than a doctrine the Campaign recites, it has to "
    "be able to land on the person who has been seen exhausted, and say: "
    "<i>this is the one I came for. Not the polished version. This one.</i>",
]

FLOOD_PROMPTS = [
    "Think of the last time the Flood came \u2014 the last time everything arrived at once "
    "in a way that was visible to others, or came dangerously close to it. Where were you? "
    "Who was there? What had been gathering underneath the surface, and for how long?",

    "The Campaign's instinct after the Flood is to rebuild the wall as fast as possible. "
    "What would it mean \u2014 what would it cost \u2014 to leave a door in the wall "
    "instead? Who is one person you could allow to stay close to the place where the "
    "Flood came from?",
]

TWO_TOG_BODY = [
    "Now we place them side by side, because the Performance Campaign and the Flood are "
    "not two separate problems. They are the same longing, moving in two directions at "
    "different speeds. The Campaign moves outward at high velocity, building and demonstrating "
    "and running. The Flood moves outward all at once when the velocity has been maintained "
    "past the point of sustainability.",

    "<b>The Campaign is what your longing does when it has time and momentum.</b> The Flood "
    "is what your longing does when the time has run out and the momentum has collapsed. "
    "The Campaign produces so the question will never have to be asked aloud. The Flood "
    "is what happens when the question cannot be silenced any longer and the answer the "
    "Campaign has been trying to produce has not arrived. Together they form a cycle, and "
    "the cycle will run for the rest of your life if nothing interrupts it.",

    "The pattern, in slow motion, looks like this. <b>(1)</b> The Campaign runs. It "
    "produces, builds, achieves. It earns credentials and recognition and a visible record "
    "of demonstrated worth. <b>(2)</b> An event lands that the record cannot address. "
    "The significance trigger fires: someone fails to see you, or sees you and does not "
    "respond as your achievements seem to warrant. <b>(3)</b> The body says, <i>I am being "
    "treated as though I am replaceable.</i> <b>(4)</b> The core question surfaces: <i>Am "
    "I enough to be remembered?</i> <b>(5)</b> The Campaign cannot afford to sit with "
    "the question, so it files it and produces more. <b>(6)</b> This happens again, and "
    "again. The pressure builds without visible release. <b>(7)</b> At a moment no one "
    "predicted \u2014 often in the middle of a public setting where composure is most "
    "required \u2014 the structure gives and the Flood comes. <b>(8)</b> The Campaign "
    "survives the embarrassment by rebuilding the wall immediately and performing recovery. "
    "The question goes underground again. The cycle restarts.",

    "What interrupts the cycle is not a larger portfolio and not a more controlled "
    "performance. It is the slow, daily, often unwilling practice of releasing pressure "
    "before it builds past the point of management \u2014 bringing the wound to God and "
    "to one trusted person while it is still a handful, before it becomes a flood. And "
    "underneath that practice, it is the gradual reception of a verdict that has already "
    "been spoken: that you are engraved on the palms of his hands, chosen before the "
    "foundation of the world, significant not by achievement but by adoption. When that "
    "verdict is received in the place where the Campaign runs \u2014 not merely affirmed "
    "doctrinally but felt in the body that has been running \u2014 the Campaign begins, "
    "slowly, to produce for different reasons. And the Flood, when it comes, is less "
    "catastrophic, because less has been held.",

    "Below is your sequence. Fill in the blanks. When you are done, read it aloud. The "
    "Campaign and the Flood both lose some of their power when they hear themselves named "
    "in your own voice.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, my body reads it as being made invisible, "
    "and the old question surfaces \u2014 <i>am I enough to be remembered?</i> "
    "My first move is to ____________________, because the Campaign in me believes "
    "that if I can ____________________, the threat will pass. What I have not "
    "been releasing is ____________________. When the structure finally gives, the "
    "Flood arrives in front of ____________________. What I actually needed, before "
    "the Flood, was to bring the wound to ____________________ while it was still "
    "small enough to carry in my hands."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a set of tools, each small enough to carry "
    "and honest enough to use. None of them will dissolve the Campaign's pattern after "
    "a single application. All of them, used over months, will loosen the grip of "
    "the cycle you just named.",

    "I have divided them into two sets: tools for when the Campaign is overrunning "
    "(when the producing has tipped from genuine vocation into existential argument), "
    "and tools for when the Flood has come or is building pressure (when the structure "
    "is straining and you can feel it). The Campaign's tools come first, because the "
    "Flood cannot be interrupted usefully until the mechanism underneath it is understood.",
]

CAMP_TOOLS = [
    ("The stopped-clock practice",
     "Once a week, spend thirty minutes doing something with no measurable output. "
     "Not productive rest. Not a walk to clear your head for the next campaign. "
     "Something genuinely unproductive: sit in a garden, read a poem, watch a bird. "
     "When the anxiety rises \u2014 and it will \u2014 name it: "
     "<i>this is the question coming up without the campaign to answer it.</i> "
     "Do not immediately answer it. Simply let it be present. "
     "The Campaign cannot be healed without first allowing the question "
     "it is running from to be heard."),

    ("The work-worship distinction",
     "Before beginning any significant project, ask one question: "
     "<i>If no one ever knew I did this, and it produced no visible recognition, "
     "would I still want to have done it?</i> This is not a test of purity \u2014 "
     "recognition is a legitimate good. It is a test of whether the work can be "
     "offered as worship rather than argument. Colossians 3:23 is the frame: "
     "<i>whatever you do, work heartily, as for the Lord and not for men.</i> "
     "Work done for the Lord does not need the audience to arrive on schedule."),

    ("The handed-back achievement",
     "Each morning, name one thing you have built or produced in the past year "
     "that you are proud of. Then say, aloud: <i>This is yours, Lord. I did not "
     "build this to be remembered. I built this because you gave me these hands. "
     "Take it.</i> This will feel hollow the first several mornings. "
     "By the thirtieth morning, something in the Campaign begins to distinguish "
     "between building for God and building for the verdict."),

    ("The presence practice",
     "Once a day, give the person closest to you ten minutes of full, undivided "
     "presence \u2014 no device, no agenda, no half-attention toward the next campaign. "
     "Not because it produces a better relationship (though it will), but because "
     "the Campaign's most characteristic failure is treating the people who love it "
     "as background to the main event. This practice begins to reverse that posture, "
     "one ten-minute session at a time."),

    ("The Psalm of inscription",
     "When the significance trigger fires and the Campaign reaches for the next "
     "achievement to answer it, pause and read Isaiah 49:15\u201316 aloud: "
     "<i>I have engraved you on the palms of my hands.</i> Not as a technique. "
     "As an act of receiving a verdict that was spoken before the Campaign ran "
     "its first race. The Campaign needs, more than almost anything else, "
     "to practice receiving significance from a source that "
     "does not require a demonstration."),
]

FLOOD_TOOLS = [
    ("Name the wound before the pressure builds",
     "Within twenty-four hours of the significance trigger firing, tell one "
     "trusted person one sentence: <i>I felt invisible today, and it is gathering "
     "pressure I have not released.</i> The Flood happens because the wound goes "
     "underground and accumulates past the point of management. Speaking it "
     "directly \u2014 as hurt, not as performance \u2014 "
     "disrupts the accumulation before it becomes a flood. The Performance "
     "will resist this because it feels like admission. It is. That is also "
     "why it works."),

    ("The pressure-gauge question",
     "Once a week, ask yourself honestly: <i>What am I holding right now that "
     "I have not released?</i> Not what the campaign is building \u2014 what the "
     "person inside the campaign is carrying. The gauge question interrupts "
     "the Campaign's tendency to file pressure rather than release it. If the "
     "answer is longer than one sentence, the filing has gone on long enough "
     "and the naming is already overdue."),

    ("The composure confession",
     "This is the hardest practice on the list for the Performance, which is "
     "why it is the most necessary. Once a month, tell one trusted person "
     "\u2014 a spouse, a pastor, an elder \u2014 one honest sentence about "
     "the cost of maintaining the composure: <i>I am more tired than I am "
     "showing, and I am not sure how long the structure holds.</i> "
     "Spurgeon told his congregation about his depression not because he had "
     "resolved it but because the hiding was adding to the weight. The "
     "composure confession is the practice of leaving a door in the wall "
     "before the wall falls."),

    ("After the flood: the repair conversation",
     "Once the Flood has come and the waters have receded, resist the instinct "
     "to rebuild the wall immediately. Instead, find the person who was nearest "
     "and say: <i>You saw me in a way I was not prepared to be seen. I want you "
     "to know what was underneath it.</i> Then name one true thing. Not the "
     "whole inventory \u2014 one true thing. The repair conversation is the "
     "beginning of allowing the Flood to have done something productive rather "
     "than merely something embarrassing."),

    ("The weakness prayer",
     "When the Flood has come, or when you feel it gathering, pray Paul's "
     "words from 2 Corinthians 12 back to God: "
     "<i>Lord, your power is made perfect in weakness. I am weak right now. "
     "I do not know how to boast in this. But I receive what you have said: "
     "when I am weak, then I am strong in you. Let that be true today, in "
     "the place where I am most aware that the campaign is not holding.</i> "
     "Say it slowly. The Campaign will resist it. Say it anyway. "
     "Spurgeon kissed the wave that threw him. You do not have to enjoy it. "
     "You only have to trust what it is throwing you against."),
]

PRAYER_BODY = [
    "Father,",

    "You see the Campaign in me, and you are not impressed and you are not disappointed. "
    "You knew about the running before it started. You know which early moment wrote "
    "the lesson that ordinary was forgettable, and which season it was when I decided "
    "that I would never, if I could help it, be ordinary. Thank you that the "
    "running has produced real things, and that those things were not wasted "
    "even when they were motivated by something other than you.",

    "But Father, I am tired in a way that more achievement does not fix. The "
    "composure has been costing more than I have admitted. And the Flood, when it "
    "came \u2014 in the meeting, in the hallway, in front of the people I was least "
    "prepared to be seen by \u2014 I am only beginning to understand that you were "
    "not absent from it. That your power is, as Paul says, made perfect in weakness. "
    "Teach me to receive what Isaiah 49 says is already true: that I am engraved on "
    "the palms of your hands \u2014 not recorded in your ledger, not filed in your "
    "archive, but engraved, permanent, present to you every moment, before any campaign "
    "has produced a single entry. Let that reach the part of me that is still running.",

    "Lord Jesus, when the Flood came and the composure fell and the people in the room "
    "saw the runner exhausted \u2014 you were the one who saw what they saw, and more. "
    "You saw the question underneath the exhaustion: <i>am I enough to be remembered?</i> "
    "And you answered it before I could ask it, in a body broken and blood poured out, "
    "engraving the answer on your palms in a way no campaign could have produced and "
    "no Flood can wash away. Remind me, in the days when I am rebuilding the wall, "
    "that the Flood was not only an ending. It may have been the first moment grace "
    "had enough room to land.",

    "Holy Spirit, where I am producing to be remembered, give me the freedom "
    "to produce for the Lord instead. Where the Flood is gathering pressure I have "
    "not named, give me the courage to speak one true thing to one safe person "
    "before the structure fails. Where I am ashamed of having been seen undone, "
    "give me the faith of Spurgeon, who learned to kiss the wave that threw him "
    "against the Rock of Ages. In the name of the One who, before Pilate, had "
    "every credential of heaven available to him and opened not his mouth \u2014 "
    "because the verdict had already been spoken in the only court that counts "
    "\u2014 I pray.",

    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Performance Campaign and "
    "the Flood have been running for a long time, and one careful reading will "
    "not retire them. What follows is a short list of next steps for the work "
    "you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.",
     "Different lines will land. The Campaign will want to treat this walkthrough "
     "as a completed project and move to the next item on the list. Read it "
     "again anyway. The section that felt least relevant today is often the "
     "most necessary one in a month. Pay particular attention to whatever "
     "you skimmed."),

    ("Take one tool, not six.",
     "Choose a single practice from Section 7 and try it for two weeks before "
     "adding another. The Campaign's instinct will be to assess all of them "
     "efficiently and consider the matter addressed. Resist this. One posture, "
     "held for long enough, begins to give the self beneath the "
     "Campaign a chance to breathe."),

    ("Tell one person what you found.",
     "Not the whole document. One sentence: <i>I learned that my mechanism is "
     "the Performance Campaign, and my breakdown is the Flood, and the Flood "
     "has been happening in public in part because I have not been releasing "
     "pressure in private.</i> The Campaign lives in the public performance. "
     "Speaking it to a trusted witness is the first act "
     "of living outside the performance."),

    ("Read Walking with God through Pain and Suffering.",
     "Tim Keller, <i>Walking with God through Pain and Suffering.</i> Read it "
     "specifically for the chapters on the ministry of suffering to the "
     "false self. Keller names, with characteristic precision, what the "
     "achiever's constructed identity costs and what the Gospel offers in "
     "its place. For the Performance, this book does what the Flood does "
     "\u2014 but gently, over time, in the privacy of a chair."),

    ("Read further on identity and weakness.",
     "Tim Keller, <i>Counterfeit Gods</i> \u2014 especially his treatment of "
     "work and achievement as idols that promise significance and deliver "
     "exhaustion. C. S. Lewis, <i>The Weight of Glory</i> \u2014 read the "
     "opening essay in full; Lewis's treatment of the longing to be noticed "
     "and the direction that longing rightly points is precisely what the "
     "Campaign needs to hear. For Scripture reading, spend a week with Psalm "
     "131 \u2014 three verses on the soul that has learned to be "
     "still rather than striving \u2014 and with 2 Corinthians 12 on the "
     "strange address where Christ's power rests."),

    ("If you are stuck, ask for help.",
     "There are seasons when the Campaign and the Flood are too entrenched "
     "to dislodge alone. A wise pastor, a Christian counselor, a trusted "
     "friend who knows you off the field \u2014 these are not signs of "
     "failure. For the Campaign specifically, asking for help without "
     "framing it as a project to be successfully completed is one of the "
     "most countercultural and most healing things on this list. The Flood "
     "already showed you that the wall is not permanent. You do not have "
     "to rebuild it alone."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a son or daughter being loved into "
    "freedom by a Father who engraved your name on the palms of his hands before "
    "you ran a single race. The Campaign did not earn that love, and the Flood did not "
    "lose it. The runner who was seen exhausted in that room is the same one who is "
    "engraved, chosen, named, held. Go gently. The One who began the good work in you "
    "will be faithful to complete it \u2014 and he will not require a portfolio as "
    "evidence of your progress."
)


def _three_column_table(rows=7):
    """Three-column journal table for Section 3's written reflection."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE EVENT", header_style), Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WAS I SEEN HERE?", header_style), Paragraph("your nervous system's verdict", sub_style)],
        [Paragraph("WAS MY SOUL IN DANGER?", header_style), Paragraph("the deeper question", sub_style)],
    ]
    data = [header_row] + [["", "", ""] for _ in range(rows)]
    tbl = Table(data, colWidths=[col_w]*3, rowHeights=[0.48*inch] + [0.42*inch]*rows)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HIGHLIGHT_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("LINEBEFORE", (1, 0), (1, -1), 0.5, RULE),
        ("LINEBEFORE", (2, 0), (2, -1), 0.5, RULE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, ACCENT),
    ]
    for i in range(1, len(data)):
        style.append(("LINEBELOW", (0, i), (-1, i), 0.4, RULE))
    tbl.setStyle(TableStyle(style))
    return tbl


def _callout(S, label, text):
    body = []
    if label:
        body.append(Paragraph(label, ParagraphStyle(
            "CalloutLabel", fontName="Inter-SemiBold", fontSize=9, leading=13,
            textColor=ACCENT, leftIndent=12, spaceBefore=2, spaceAfter=4)))
    body.append(Paragraph(text, ParagraphStyle(
        "Callout", fontName="Inter", fontSize=10.5, leading=17,
        textColor=INK, leftIndent=12, rightIndent=12, spaceAfter=8)))
    t = Table([[body]], colWidths=[PAGE_W - MARGIN_L - MARGIN_R],
              style=TableStyle([
                  ("BACKGROUND", (0, 0), (-1, -1), HIGHLIGHT_BG),
                  ("LEFTPADDING", (0, 0), (-1, -1), 6),
                  ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                  ("TOPPADDING", (0, 0), (-1, -1), 12),
                  ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
              ]))
    return t


def build(submission) -> bytes:
    """Generate the Performance Campaign+Flood walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='CAMP', primary_breakdown='FLOOD',
    primary_trigger='SIG', core_question='REM'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="PERFORMANCE  \u00b7  FLOOD",
        title="Take 139 Walkthrough \u2014 Performance Campaign + Flood",
    )

    story = []

    # \u2500\u2500 COVER \u2500\u2500
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor\u2019s<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the way<br/>you have learned to keep yourself safe.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph(
        "The Performance Campaign \u00a0\u00b7\u00a0 The Flood", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Significance \u00a0\u00b7\u00a0 Core Question: Am I enough to be remembered?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cMy grace is sufficient for you, for my power is made perfect in weakness."
        "<br/>For when I am weak, then I am strong.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "2 Corinthians 12:9\u201310",
        ParagraphStyle("cqa", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 1: Opening \u2500\u2500
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read this slowly. The chapter that follows has been a long time in the running.")
    for p in OPENING_BODY:
        story.append(Paragraph(p, S["BodyJ"]))

    # \u2500\u2500 SECTION 2: Trigger \u2500\u2500
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TRIGGER",
                   "Significance.",
                   "The three-second moment when being made invisible fires an alarm.")
    for p in TRIGGER_BODY[:3]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  CONTINUED",
                   "Where the lesson was written.",
                   "The conviction that arrived before you were old enough to question it.")
    for p in TRIGGER_BODY[3:]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will frame the answer as a campaign. Your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=6)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 3: Core Question \u2500\u2500
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I enough to be remembered?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "Two kinds of producing.",
                   "From fullness, or from need. Only one of them can stop.")
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table(rows=3))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 4: Mechanism \u2500\u2500
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Performance Campaign.",
                   "The runner. The achiever. The builder of visible competence.")
    for p in CAMP_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "What the Campaign produces, and what it costs.",
                   "The gift, the history, and the question it cannot answer.")
    for p in CAMP_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in CAMP_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Campaign.",
                   "Read the Campaign's own words. He has been faithful; let him speak.")
    letter_style = ParagraphStyle(
        "CampLetterFlood", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for line in CAMP_LETTER_INSTRUCTION:
        story.append(Paragraph(line, letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in CAMP_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=2)
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 5: Breakdown \u2500\u2500
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Flood.",
                   "What happens when the Campaign\u2019s composure can no longer hold.")
    for p in FLOOD_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in FLOOD_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The paradoxical mercy.",
                   "Power made perfect in weakness. The address where grace lands.")
    for p in FLOOD_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions about the last Flood.",
                   "Sit with these before you turn the page.")
    for prompt in FLOOD_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 12))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same longing, at two different speeds.",
                   "The Campaign and the Flood are not two problems. They are one cycle.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 8))
    journal_lines(story, n=4)
    story.append(PageBreak())

    # \u2500\u2500 SECTION 7: Tools \u2500\u2500
    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "What to do when you feel the cycle start.",
                   "Small enough to carry; honest enough to use.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 14))

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Campaign is overrunning.",
                   "Five practices for the time before the pressure becomes critical.")
    for name, desc in CAMP_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Flood has come or is coming.",
                   "Five practices for the overflow and its aftermath.")
    for name, desc in FLOOD_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<b>Integration:</b> The single discipline connecting both sides is this \u2014 "
        "the small, honest naming of what you are carrying, offered to God and to one "
        "trusted person, before the accumulation reaches the level of a public Flood. "
        "The Campaign was built to be seen for what it produces. Learning to be seen "
        "for what it carries, before the Flood forces the disclosure, is the most "
        "countercultural and most healing practice on this list. Spurgeon did not "
        "choose the wave. But he learned to trust what it was throwing him toward.",
        S["BodyJ"]))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 8: Prayer \u2500\u2500
    section_header(story, S, "SECTION EIGHT  \u00b7  A PRAYER",
                   "Pray this slowly.",
                   "Out loud, if you can. Sit a moment after the Amen.")
    for line in PRAYER_BODY:
        story.append(Paragraph(line, S["BlockQuote"]))

    # \u2500\u2500 SECTION 9: Going Further \u2500\u2500
    section_header(story, S, "SECTION NINE  \u00b7  GOING FURTHER",
                   "Where to go from here.",
                   "This walkthrough is a beginning, not an ending.")
    for p in GOING_FURTHER_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    for name, desc in GOING_FURTHER_ITEMS:
        story.append(KeepTogether([
            Paragraph(name, S["H3"]),
            Paragraph(desc, S["BodyJ"]),
        ]))
    divider(story)
    story.append(KeepTogether([Paragraph(GOING_FURTHER_CLOSING, S["BlockQuote"])]))

    doc.build(story)
    return finalize_buffer(buf)


# \u2500\u2500 STANDALONE TEST \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "CAMP"
        primary_breakdown = "FLOOD"
        primary_trigger = "SIG"
        core_question = "REM"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "performance_flood_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages and get snippet using pypdf
    import io
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        snippet = ""
        for page in reader.pages[1:3]:
            txt = page.extract_text() or ""
            if txt.strip():
                snippet = txt.strip()[:120]
                break
    except Exception:
        page_count = "unknown"
        snippet = ""

    print(f"DONE: performance_flood.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
