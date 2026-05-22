"""Personal Walkthrough — Performance Campaign + Attorney.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Significance trigger, "Am I enough to be remembered?" core question.
~25 pages, 9 sections.

Calibration anchor: Walkthrough 31 of 36 — FIRST PERFORMANCE CAMPAIGN walkthrough.
Establishes the Performance Campaign mechanism as a distinct character. After this
walkthrough, all six mechanisms (Architect, Island, Ambassador, Vault, Adapter,
Performance) will have been introduced.

THE PERFORMANCE CAMPAIGN CHARACTER:
The runner who learned early that achievement was the path to being seen. Carries
a long résumé and a thin sense of who they are off the field. Default response to
anxiety is to produce. Rest feels like death; visibility feels like oxygen. Identity
is tied to demonstrated worth, not received worth. Fears replaceability above all.

DISTINGUISHING MOVE: The Performance+Attorney is the resume-as-evidence breakdown.
A lifetime of building a portfolio of demonstrated worth, and when wounded enough,
that entire portfolio becomes the case. "Do you know what I have done? Do you
understand what I have accomplished? Do you have any idea what I have earned the
right to expect?" The evidence is accomplishments — credentials, results, public
recognition. The spouse experiences this as both true (the accomplishments are real)
and devastating (love must be calibrated to those accomplishments).

CRITICAL THEOLOGICAL MOVE (Section Five):
The Performance+Attorney's case is theologically identical to the elder brother's
case in Luke 15:29 ("these many years I have served you") — a valid accomplishment
ledger presented as grounds for the love that was never going to be earned by it.
Quote Keller from The Prodigal God. Bring in Galatians 2:21. Reference Lloyd-Jones
on the danger of "the moral man."

DISTINGUISHING FROM AMBASSADOR AND ADAPTER:
- Ambassador serves to be loved; Performance accomplishes to be seen
- Adapter calibrates to the room; Performance demonstrates to the room
- Performance specifically earns through visible output, not relational service
  or contextual fluency
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
    "you needed to be seen.",

    "You are, in the deepest sense, a runner. Not necessarily a runner in the literal sense, "
    "though you may well be that too. I mean something more interior: you are a person who "
    "discovered, early in life, that moving forward at speed \u2014 building, achieving, "
    "demonstrating, producing \u2014 was the surest path to being noticed, valued, and kept. You "
    "learned, in some context that mattered enormously to you, that ordinary was forgettable. "
    "And forgettable, in the economy of your early world, was not safe.",

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
    "you grew up in a household where love was not withheld but was notably warmer when you "
    "performed. Perhaps ordinary effort was unremarkable and extraordinary effort was, finally, "
    "noticed \u2014 which trained your system to the conclusion that the path to being seen "
    "ran through the extraordinary. Perhaps there was a parent whose attention was chronically "
    "elsewhere, and achievement became the reliable method of capturing it. Perhaps you were "
    "one child among many in a family system where visibility had to be earned rather than "
    "assumed, and you were an early learner of the relevant lesson.",

    "Whatever its specific origin, the lesson arrived with the force of a conviction: <i>I will "
    "not be forgotten if I cannot be ignored.</i> And so you began to build. Not the Architect's "
    "careful blueprints \u2014 that is a different mechanism, driven by a different fear. You "
    "began to produce, to demonstrate, to show what you could do in the full light of day. "
    "You ran. And the running, over time, became not just a strategy but an identity. The "
    "Performance Campaign was born.",

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
    "\u2014 brings warmth, managers emotional temperature, pours out care and waits, "
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
    "has a long résumé and, often, a thin sense of who they are off the field. It is "
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
    "serve. The taxonomy we use to understand these patterns names it directly: the "
    "Performance's drive to achieve, build, and leave a mark does something specific for "
    "it. It answers the question <i>do I matter?</i> through achievement. If I can point "
    "to something I built, I know I existed. The producing is, underneath its genuine "
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

    "I am telling you this because I think you are starting to feel the cost. "
    "The way the people closest to you have a particular tone when the campaign "
    "takes over again. The gap between your public self and the private self "
    "that sits alone some evenings wondering whether any of it matters. "
    "I built the right thing for the wrong reason, and I kept building it "
    "past the point where it could answer the question I was actually "
    "trying to answer.",

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

    "The Campaign says he built the right thing for the wrong reason. Name one "
    "specific thing you are currently building or pursuing. What is the "
    "right reason to do it? What might the wrong reason be? Can you tell "
    "the difference from the inside?",
]

ATT_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Performance Campaign, the breaking "
    "has a shape that is, among all the versions of this pattern we follow, the most "
    "theologically striking and the most pastorally urgent to name clearly. The breakdown "
    "is called <b>the Attorney</b>, and the Performance's version of it is unlike the "
    "ones we have encountered in other mechanisms.",

    "The Architect's Attorney argues live and loud when blueprints are violated. The "
    "Island's Attorney builds quietly in private and delivers a single devastating closing "
    "statement. The Ambassador's Attorney produces the invisible ledger of love \u2014 "
    "all the giving, finally presented as evidence. The Vault's Attorney unseals a "
    "curated file. The Adapter's Attorney is a multi-witness courtroom where every "
    "witness is the same person speaking from a different persona. The "
    "Performance's Attorney is different from all of these. It is the "
    "<b>r\u00e9sum\u00e9 as evidence</b>.",

    "Here is how it happens. The Campaign has been running. For months, perhaps years, "
    "it has been producing, building, demonstrating, achieving. And then something "
    "lands \u2014 a criticism from a spouse about the quality of presence in the marriage, "
    "an acknowledgment withheld at exactly the wrong moment, a dismissal of something "
    "the Campaign poured itself into, or simply the accumulated weight of feeling "
    "undervalued by someone whose valuation matters enormously. The Campaign cannot "
    "fix this from its usual position, because the fix would require a kind of "
    "standing that cannot be earned by producing more. And so a different part "
    "of you takes the floor.",

    "The Attorney does not solve the problem. The Attorney <i>presents the case.</i> "
    "And the Performance Attorney's case is built not from relational memories, not "
    "from the invisible givings of the Ambassador, not from the curated vulnerability "
    "of the Vault. It is built from <i>accomplishments</i>. The evidence is the "
    "portfolio. The witnesses are the achievements.",
]

ATT_BODY_P2 = [
    "Here is what this sounds like, not always out loud but sometimes: <i>Do you know "
    "what I have built? Do you understand what it cost to get here? Do you have any "
    "idea what I have given up, what I have sacrificed, what I have produced, in order "
    "to be the person I am in this room?</i> Sometimes it is less direct than that "
    "\u2014 sometimes it is a rapid inventory of credentials, a pointed reference to "
    "what others think of you, a careful enumeration of recent successes presented "
    "with a tone that says: <i>and yet you are treating me as if none of this "
    "counts.</i>",

    "The person on the other side of this \u2014 almost always the spouse or partner "
    "who knows the Campaign most intimately \u2014 experiences it in a particular way. "
    "They experience it as both <i>true and devastating</i>. True, because the "
    "accomplishments are real. The Campaign has, in fact, built remarkable things, "
    "and the spouse knows it. But devastating, because the logic underneath the "
    "argument is this: <i>given what I have achieved, your love should look "
    "different than it does.</i> Which is to say: love ought to be calibrated "
    "to accomplishment. Which is to say: if I had achieved less, you would be "
    "right to love me less.",

    "<b>That is not a logic the spouse can accept without destroying the thing "
    "they love most about the relationship.</b> And so the spouse finds themselves "
    "in an impossible position: to affirm the case is to agree that love is "
    "earned; to dispute the case is to seem to deny the accomplishments that "
    "are genuinely real. The Attorney has, without intending to, built a "
    "courtroom in which no verdict can produce what the Campaign is actually after.",

    "What the Campaign is actually after is not acknowledgment of the "
    "accomplishments. It has had that, many times, and it has never been "
    "enough. What the Campaign is after is the assurance that it is "
    "loved not because of what it has done, but in spite of the fact "
    "that it is not always the person the accomplishments seem to promise. "
    "The Attorney cannot get that verdict. The Attorney, by its nature, can only "
    "argue the case that love should respond to performance. And performance, "
    "as a ground for love, is precisely the thing that cannot hold.",
]

ATT_BODY_P3 = [
    "In Luke 15:29, Jesus gives us a man who has spent years building precisely the "
    "case the Performance Attorney builds. The elder brother, standing outside the "
    "father's feast, says: <i>Look, these many years I have served you, and I never "
    "disobeyed your command, yet you never gave me a young goat, that I might celebrate "
    "with my friends.</i> It is not an accusation of abuse. It is a performance review. "
    "A r\u00e9sum\u00e9 presented as grounds for love. Tim Keller, in <i>The Prodigal "
    "God</i>, names the elder brother's condition precisely: he had been serving the "
    "father not out of love but in order to build a claim. His obedience was, at its "
    "root, a transaction \u2014 and when the father refused to honor the transaction, "
    "the elder brother did not experience it as grace. He experienced it as betrayal.",

    "What the parable reveals is that an accurate accomplishment ledger, presented as "
    "grounds for the father's love, is <i>a misunderstanding of the father</i>. The "
    "father had been available all along: <i>Son, you are always with me, and "
    "everything I have is yours.</i> (Luke 15:31) The elder brother had been arguing "
    "for something he already possessed. Paul makes the same move in Galatians 2:21: "
    "<i>if righteousness were through the law, then Christ died for no purpose.</i> "
    "Apply it pastorally: <i>if love could be earned by accomplishment, the cross was "
    "unnecessary.</i> Martyn Lloyd-Jones warned against the danger of the moral man "
    "\u2014 the person whose goodness has become, without his knowing it, his god. "
    "Such a person is more lost than the prodigal, because the prodigal knows he "
    "needs the father's mercy while the elder brother believes he has already "
    "earned it. The case is real. The record is impressive. And neither fact brings "
    "the Campaign one step closer to the thing it most needs: to receive, not to earn.",
]

ATT_PROMPTS = [
    "Name the last time the Performance Attorney took the floor \u2014 out loud or "
    "in your own head. What was the case? What evidence did you present or want to "
    "present?",

    "The elder brother's case was accurate and it still missed the father's "
    "heart entirely. Write one sentence that names the accomplishment you most "
    "want your spouse or closest person to properly acknowledge. Then write "
    "one sentence that names what you actually want from them that the "
    "accomplishment cannot earn.",
]

TWO_TOG_BODY = [
    "Now we place them side by side, because the Performance Campaign and the "
    "Attorney are not two separate problems. They are the same longing, "
    "moving in two directions. The Campaign moves outward, building and demonstrating "
    "and running. The Attorney moves inward when the running has not produced the "
    "verdict, assembling the evidence and demanding that the record be consulted.",

    "<b>The Campaign is what your longing does when it has time.</b> The Attorney is "
    "what your longing does when the Campaign has not worked. The Campaign produces "
    "so the question will not have to be asked. The Attorney argues when the question "
    "is asked anyway. Together they form a closed loop, and the loop will run all "
    "your life if something does not interrupt it.",

    "The pattern, in slow motion, looks like this. <b>(1)</b> The Campaign runs. "
    "It produces, builds, achieves. It earns credentials and recognition and "
    "a visible record of demonstrated worth. <b>(2)</b> An event lands that the "
    "record cannot address. The significance trigger fires: someone fails to "
    "see you, or sees you and does not respond as your achievements seem to warrant. "
    "<b>(3)</b> The body says, <i>I am being treated as though I am replaceable.</i> "
    "<b>(4)</b> The core question surfaces: <i>Am I enough to be remembered?</i> "
    "<b>(5)</b> The Campaign tries to answer it by producing more. <b>(6)</b> "
    "When producing more cannot answer a relational question, the Attorney "
    "takes the floor and presents the existing portfolio as evidence for the "
    "love it cannot actually earn. <b>(7)</b> The verdict, even if it arrives, "
    "does not satisfy, because what was given was acknowledgment of the "
    "accomplishments, not the assurance that the person behind them is loved "
    "apart from them. The question wakes up again by morning.",

    "What interrupts the loop is not a larger portfolio. It is not a more "
    "complete case. It is the slow, daily, often unwilling reception of a "
    "verdict that has already been spoken \u2014 that you are engraved on "
    "the palms of his hands, chosen before the foundation of the world, "
    "significant not by achievement but by adoption. When that verdict is "
    "received \u2014 really received, in the place that has been running the "
    "campaign \u2014 the Campaign is free to run for different reasons, and "
    "the Attorney loses the one argument he has ever known how to make.",

    "Below is your sequence. Fill in the blanks. When you are done, read it "
    "aloud. The Campaign and the Attorney both lose some of their power when "
    "they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, my body reads it as being made invisible, "
    "and the old question surfaces \u2014 <i>am I enough to be remembered?</i> "
    "My first move is to ____________________, because the Campaign in me believes "
    "that if I can ____________________, the threat will pass. When that does not "
    "work, the Attorney takes the floor and presents the case that ____________________. "
    "What I am actually after, underneath all of it, is the verdict "
    "____________________ \u2014 a verdict Christ has already spoken over me in "
    "____________________, before any campaign had produced a single entry."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a set of tools, each small enough to carry "
    "and honest enough to use. None of them will dissolve the Campaign's pattern after "
    "a single application. All of them, used over months, will loosen the grip of "
    "the loop you just named.",

    "I have divided them into two sets: tools for when the Campaign is overrunning "
    "(when the producing has tipped from genuine vocation into existential argument), "
    "and tools for when the Attorney is on his feet (when the significance trigger "
    "has just fired and the portfolio is being assembled as evidence). The Campaign's "
    "tools come first, because the Attorney cannot be interrupted usefully until "
    "the mechanism underneath it is understood.",
]

CAMP_TOOLS = [
    ("The stopped-clock practice",
     "Once a week, spend thirty minutes doing something with no measurable output. "
     "Not productive rest. Not a walk to clear your head for the next campaign. "
     "Something genuinely unproductive: sit in a garden, read poetry, watch a bird. "
     "When the anxiety rises \u2014 and it will \u2014 name it: "
     "<i>this is the question coming up without the campaign to answer it.</i> "
     "Do not answer the question. Simply let it be present without immediately "
     "running from it. The Campaign cannot be healed without first allowing the "
     "question it is running from to be heard."),

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
     "Take it.</i> This will feel performatively humble the first several mornings. "
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
     "When the significance trigger fires and the Campaign reaches for the portfolio, "
     "pause and read Isaiah 49:15\u201316 aloud: <i>I have engraved you on the palms "
     "of my hands.</i> Not as a technique. As an act of receiving a verdict that was "
     "spoken before the Campaign ran its first race. The Campaign needs, more than "
     "almost anything else, to practice receiving significance from a source that "
     "does not require a demonstration."),

]

ATT_TOOLS = [
    ("Name the wound before the portfolio assembles",
     "Within twenty-four hours of the significance trigger firing, tell one "
     "trusted person one sentence: <i>I felt invisible today, and it hurt, "
     "and I am tempted to respond by making myself impossible to ignore.</i> "
     "The Attorney assembles the portfolio because the wound goes underground "
     "and is processed through the Campaign's framework rather than named as "
     "a wound. Speaking it directly \u2014 as hurt, not as argument \u2014 "
     "disrupts the assembly before it begins."),

    ("The elder brother question",
     "When the Attorney begins to rise, stop and ask: <i>Am I building a case "
     "right now, or am I naming a wound?</i> The elder brother's error was not "
     "that his accomplishments were false. His error was treating them as legal "
     "tender for the father's love. Ask yourself, honestly: "
     "<i>am I arguing for acknowledgment of the record, or am I asking to be "
     "loved?</i> If it is the latter, say that directly: "
     "<i>I need to feel like I matter to you right now,</i> not "
     "<i>do you know what I have done?</i>"),

    ("The single wound rule",
     "When you must speak, name one wound in one sentence, stripped of the "
     "portfolio: <i>When that happened, I felt unseen, and I need you to "
     "know that.</i> The Attorney derives its power from the scale of the "
     "evidence. Remove the evidence. Speak the wound. One sentence is "
     "almost always more powerful, and more repairable, than a closing brief."),

    ("The advocate prayer",
     "When the Attorney is loudest \u2014 when the portfolio is assembled "
     "and the case feels urgently necessary \u2014 pray these words slowly: "
     "<i>Lord Jesus, you are my advocate. You know everything I have done "
     "and everything that has been done to me. I do not need to present "
     "the case. I receive the verdict you have already spoken over me: "
     "engraved, adopted, chosen, known.</i> Say it three times. "
     "The third time, the courtroom usually begins to quiet."),

    ("Write the brief and receive the name",
     "If the closing argument will not leave you alone, write it out fully "
     "\u2014 every credential, every achievement, every entry in the "
     "portfolio. Then at the bottom of the last page, write: "
     "<i>If love could be earned by accomplishment, the cross was unnecessary. "
     "He was sent anyway. I was named before I built anything.</i> "
     "Tear the brief. Keep the sentence. This is the practice of "
     "receiving the significance the Campaign cannot produce."),

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
    "finish line keeps moving. Every credential I earn and every recognition I receive "
    "quiets the question for a season and then hands it back unsatisfied. Teach me "
    "to receive what Isaiah 49 says is already true: that I am engraved on the palms "
    "of your hands \u2014 not recorded in your ledger, not filed in your archive, "
    "but engraved, permanent, present to you every moment, before any campaign "
    "has produced a single entry. Let that reach the part of me that is still running.",

    "Lord Jesus, when the Attorney rises in me and the portfolio comes out as "
    "evidence for the love I have been unable to earn \u2014 remind me of the "
    "elder brother, standing outside the feast, making his case to a father who "
    "was already saying <i>son, you are always with me, and everything I have "
    "is yours.</i> Let me hear that sentence before I deliver the brief. "
    "Remind me that if love could be earned by accomplishment, you would not "
    "have been sent, and that the sending is the only evidence of significance "
    "I will ever actually need.",

    "Holy Spirit, where I am producing to be remembered, give me the freedom "
    "to produce for the Lord instead. Where the Attorney is assembling the "
    "portfolio, give me the courage to name the wound directly and trust the "
    "Advocate I already have. Where rest feels like death, give me the "
    "faith to know that I am held even when I am not running.",

    "In the name of the One who stood before Pilate with every credential of "
    "heaven available to him and opened not his mouth \u2014 because the verdict "
    "had already been spoken in the only court that counts \u2014 I pray.",

    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Performance Campaign and "
    "the Attorney have been running for a long time, and one careful reading will "
    "not retire them. What follows is a short list of next steps for the work "
    "you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.",
     "Different lines will land. The Campaign will want to treat this walkthrough "
     "as a completed project and move to the next item on the list. Read it "
     "again anyway. The section that felt least relevant today may be the "
     "most necessary one in a month."),

    ("Take one tool, not six.",
     "Choose a single practice from Section 7 and try it for two weeks before "
     "adding another. The tools are not a performance metric. They are postures. "
     "One posture, held for long enough, begins to give the self beneath the "
     "Campaign a chance to breathe."),

    ("Tell one person what you found.",
     "Not the whole document. One sentence: <i>I learned that my mechanism is "
     "the Performance Campaign, and my breakdown is the Attorney, and I have "
     "been building a case with my accomplishments for love that was never "
     "going to be purchased that way.</i> The Campaign lives in the public "
     "performance. Speaking it to a trusted witness is the first act "
     "of living outside the performance."),

    ("Sit with the Prodigal God.",
     "Tim Keller, <i>The Prodigal God.</i> Read it specifically for the elder "
     "brother sections. Keller's portrait of the elder brother is the most "
     "precise pastoral address to what the Performance Attorney is doing "
     "that exists in modern Christian writing. Read it slowly. "
     "The elder brother is you."),

    ("Read further on identity and counterfeit gods.",
     "Tim Keller, <i>Counterfeit Gods: The Empty Promises of Money, Sex, and "
     "Power, and the Only Hope That Matters</i> \u2014 especially his treatment "
     "of work and achievement as idols. C. S. Lewis, <i>The Weight of Glory</i> "
     "\u2014 read the opening essay in full; Lewis's treatment of the longing "
     "to be noticed and the direction that longing rightly points is precisely "
     "what the Campaign needs to hear. For Scripture reading, spend a week "
     "with Psalm 131 \u2014 three verses on the soul that has learned to be "
     "still rather than striving."),

    ("If you are stuck, ask for help.",
     "There are seasons when the Campaign and the Attorney are too entrenched "
     "to dislodge alone. A wise pastor, a Christian counselor, a trusted "
     "friend who knows you off the field \u2014 these are not signs of "
     "failure. For the Campaign specifically, asking for help without "
     "framing it as a project to be successfully completed is one of the "
     "most countercultural and most healing things on this list."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a son or daughter being loved into "
    "freedom by a Father who engraved your name on the palms of his hands before "
    "you ran a single race. The Campaign did not earn that love, and it cannot lose it. "
    "Go gently. The One who began the good work in you will be faithful to complete it "
    "\u2014 and he will not require a portfolio as evidence of your progress."
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
    """Generate the Performance Campaign+Attorney walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='CAMP', primary_breakdown='ATTY',
    primary_trigger='SIG', core_question='REM'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor's Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR'S WALKTHROUGH",
        cover_right_label="PERFORMANCE  \u00b7  ATTORNEY",
        title="Take 139 Walkthrough \u2014 Performance Campaign + Attorney",
    )

    story = []

    # \u2500\u2500 COVER \u2500\u2500
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor's<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the way<br/>you have learned to keep yourself safe.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph("The Performance Campaign \u00a0\u00b7\u00a0 The Attorney", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Significance \u00a0\u00b7\u00a0 Core Question: Am I enough to be remembered?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cThe man who has done great things and trusted in them"
        "<br/>is further from God than the man who knows he has done nothing.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Martyn Lloyd-Jones, <i>Studies in the Sermon on the Mount</i>",
        ParagraphStyle("cqa", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 1: Opening \u2500\u2500
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read this slowly. The chapter that follows has been a long time in the running.")
    for p in OPENING_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 2: Trigger \u2500\u2500
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TRIGGER",
                   "Significance.",
                   "The three-second moment when being made invisible fires an alarm.")
    for p in TRIGGER_BODY[:4]:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in TRIGGER_BODY[4:]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will frame the answer as a campaign. Your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
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
    story.append(_three_column_table(rows=4))
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
        "CampLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for line in CAMP_LETTER_INSTRUCTION:
        story.append(Paragraph(line, letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in CAMP_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 5: Breakdown \u2500\u2500
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Attorney.",
                   "The place your mechanism breaks, and the r\u00e9sum\u00e9 it builds.")
    for p in ATT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ATT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The elder brother's case.",
                   "An accurate ledger, and the father's answer it never expected.")
    for p in ATT_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Step out of the courtroom.",
                   "Two questions to sit with before you turn the page.")
    for prompt in ATT_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same longing, in two directions.",
                   "The Campaign and the Attorney are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 8))
    journal_lines(story, n=6)
    story.append(PageBreak())

    # \u2500\u2500 SECTION 7: Tools \u2500\u2500
    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "What to do when you feel the loop start.",
                   "Small enough to carry; honest enough to use.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 14))

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Campaign is overrunning.",
                   "Six practices for the time before the alarm fires.")
    for name, desc in CAMP_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Attorney is presenting the portfolio.",
                   "Six practices for the moment the courtroom assembles.")
    for name, desc in ATT_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 8: Prayer \u2500\u2500
    section_header(story, S, "SECTION EIGHT  \u00b7  A PRAYER",
                   "Pray this slowly.",
                   "Out loud, if you can. Sit a moment after the Amen.")
    for line in PRAYER_BODY:
        story.append(Paragraph(line, S["BlockQuote"]))
    story.append(PageBreak())

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
        primary_breakdown = "ATTY"
        primary_trigger = "SIG"
        core_question = "REM"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "performance_attorney_test.pdf")
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

    print(f"DONE: performance_attorney.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
