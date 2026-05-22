"""Personal Walkthrough — Performance Campaign + Plea.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disconnection trigger, "Am I lovable?" core question.
~25 pages, 9 sections.

Calibration anchor: Walkthrough 36 of 36 — THE FINAL PERSONAL WALKTHROUGH.
This completes the full 6x6 matrix of mechanism × breakdown profiles.

THE PERFORMANCE+PLEA PROFILE — THE MOST INSIDIOUS COMBINATION:
The Performance Campaign has a campaign for everything. It produces for the
world. It builds for the record. It demonstrates for whatever audience is
available. When wounded — when the marriage shows a gap, when the spouse
grows quiet, when disconnection cracks the private world open — the Campaign
does not break down publicly. It redirects.

The unique tragedy of this profile: the Performance+Plea looks like love.
The Campaign, when the gap appears, stops competing with the world and starts
competing for one specific person. Gifts. Letters. Vacations they cannot afford.
Surprises. Plans. Initiatives. The private campaign is lavish, extravagant,
relentless. And the spouse, receiving all of it, feels something the Campaign
does not expect: increasingly suffocated.

Because what is actually happening is not generosity. It is the Performance
Campaign converting its arena from public output to private pursuit. The spouse
has become the new audience — and audiences, for the Campaign, must respond.
The gift is given to close the gap, not from a love already secure. The vacation
is planned to be remembered, not to remember the marriage.

CRITICAL THEOLOGICAL MOVE (Section Five):
1 John 4:19 — "We love because he first loved us." The order matters crucially.
Love that gives in order to receive is not the love the gospel speaks of. The
Performance+Plea is asking the spouse to be God — to be the source of acceptance
that only the cross can give. Quote Keller from The Meaning of Marriage:
"Marriage is the most profound human relationship, but it cannot bear the weight
of being your salvation." Reference Spurgeon on the love that flows from union
with Christ rather than from need. Quote Edwards: "Christ is the proper rest
of every soul."

DISTINGUISHING FROM OTHER PLEA PROFILES:
- Architect+Plea substitutes peacekeeping for peacemaking
- Island+Plea is the paradoxical self-contained suddenly pursuing
- Ambassador+Plea doubles down at triple volume
- Vault+Plea slides the curated apology under the door at 2am
- Adapter+Plea cycles through every version in ten minutes
- Performance+Plea redirects the entire campaign — from the world to the spouse.
  It is the only Plea that presents as extravagant generosity.
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
    "Before you read any further, I want to do for you what a good counselor does at the"
    " beginning of a genuinely difficult conversation. I want to lower the lights and slow"
    " the pace, because what you are about to encounter is not a profile or a personality"
    " assessment. It is something considerably more intimate: a careful account of the way"
    " your soul has learned to keep itself safe in a world that has, in real and specific"
    " ways, declined to love you as plainly as you needed to be loved. And the place where"
    " that account becomes most urgent \u2014 the place that has probably brought this"
    " document into your hands \u2014 is not your public world. It is your marriage, or"
    " the relationship that stands closest to it.",

    "We are going to walk through your trigger \u2014 the specific moment your body says"
    " <i>something is wrong here.</i> We will sit with the question underneath that moment,"
    " the one that has been circling since long before you had a name for it. We will name"
    " the strategy you built in response, and the place that strategy takes when it breaks."
    " And then, only then, will we put tools in your hands for what comes next.",

    "If you were sitting across from me, I would say this slowly and mean every word."
    " <b>What you are about to read is true, but it is not the whole truth about you.</b>"
    " The whole truth includes a Father who did not love you because of your output, who"
    " loved you before a single campaign had produced a single entry; a Son who was not"
    " given to this world as a performance but as a gift, freely and without condition;"
    " and a Spirit who is, at this very moment, more committed to your freedom than the"
    " Campaign is committed to its next initiative.",

    "So read slowly. Argue with what does not fit. Stay with what catches. Write in the"
    " margins. Pray when something lodges in your throat \u2014 because that lodging is"
    " usually the Lord saying, <i>look here, with me, at what is actually happening.</i>"
    " The goal of this walkthrough is not a better campaign. It is a slightly freer life,"
    " lived from a person who does not need to earn the love that has already been given."
    " The chapter you are about to read about yourself has been running for many years."
    " It deserves a few hours of patient attention.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it does not look, from the outside,"
    " like very much. You are at home. Or you and your spouse are together in the ordinary"
    " traffic of an ordinary week. And something shifts — a short answer where there used to"
    " be a real one, a distraction at the dinner table that lasts a few minutes too long,"
    " a silence in the car that feels different from comfortable silence, a sense that the"
    " person who knows you best is slightly — not dramatically, slightly — further away"
    " than they were yesterday. And something inside you, in under three seconds, moves"
    " from ordinary to alarmed.",

    "On the surface this looks like the sensitivity of a loving spouse. In reality, what has"
    " just fired is something more specific. It is not merely the grief of a missed"
    " connection. It is a signal — rapid, involuntary, physical — that says:"
    " <i>the gap is open. The specific person whose love I cannot replace has moved"
    " away from me, and I do not know by how much, and I do not know why, and I do not"
    " have a campaign in place for this contingency.</i> The Campaign has campaigns for"
    " nearly everything. The thing it does not have a campaign for is the private"
    " disconnection that does not respond to public excellence.",

    "This is your trigger. The technical word for it is <b>disconnection</b>,"
    " but the word needs careful unpacking because for you it carries a specific freight."
    " This is not the dramatic disconnection of a declared rupture. It is the quiet"
    " disconnection of sensing that the one person you cannot afford to lose is in the"
    " process of finding you slightly less necessary — that the gap between you is widening,"
    " by increments, and that the excellent things you have been building in the world"
    " have not, somehow, been enough to close it.",

    "C. S. Lewis, in <i>The Weight of Glory</i>, named the longing underneath this"
    " trigger more precisely than almost any other writer: the longing not merely to be"
    " noticed but to be <i>united</i> with the good we receive from another, to be"
    " welcomed into them, to find that we are genuinely wanted and not merely useful."
    " You have had, in your public world, a great deal of being found useful. What fires"
    " in the trigger moment is the fear that the person who matters most has concluded"
    " that you are, in the end, useful rather than beloved. And beloved, as Lewis knew,"
    " is what every soul is actually asking for.",

    "<b>Your sensitivity to disconnection is not random.</b> It is the residue of something"
    " learned, usually early, usually in a context where love was present but was notably"
    " warmer — more visible, more engaged, more real — when you performed. Perhaps there"
    " was a parent whose emotional presence was contingent on your output: available when"
    " you succeeded, preoccupied when you did not. Perhaps love in your household of origin"
    " had an earned quality — something you could reliably produce by producing, and that"
    " felt, in its quieter seasons, slightly uncertain. Perhaps you grew up with a"
    " generalized and accurate sense that you were loved and an equally specific and"
    " accurate sense that the love was more fully present when you were excellent."
    " The lesson was not spoken. It was simply there: <i>the way to be held is to give them"
    " something worth holding you for.</i>",

    "The Performance Campaign was built, among other things, to answer that lesson at"
    " scale. And it worked — in the arenas where visible output could be produced. What"
    " it could not solve was the private register: the marriage, the deep friendship,"
    " the intimate relationship where the question is not <i>what have you done?</i>"
    " but <i>are you, as you are, lovable?</i> That is the question the trigger is"
    " reopening. Before we go further, I want you to sit with two questions in writing."
    " Your head will reach for the next initiative. Your hand will not.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week or two, that the disconnection signal fired"
    " in your marriage or closest relationship. Not a dramatic event — the small, quiet,"
    " almost-invisible ones are usually the most instructive. What happened, in two"
    " sentences?",

    "What was the size of the actual event, and what was the size of the response inside"
    " you? If the response was larger than the event — if what you felt did not match what"
    " actually occurred — you have just located the trigger. And underneath it, a question"
    " that is older than this marriage.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The"
    " trigger is the alarm; the question is the wound the alarm has been guarding"
    " since long before the marriage, long before the Campaign began to run.",

    "Yours is this: <b>Am I lovable?</b>",

    "It is not the same as <i>Am I competent?</i>, though the Campaign has built"
    " extraordinary competence in part as a way of trying to answer it. It is not"
    " <i>Am I enough to be remembered?</i>, though the fear of being forgotten is"
    " a close cousin. It is something more specific and more vulnerable: the question"
    " of whether you are, as you are — apart from the portfolio, apart from the"
    " campaign, apart from what you have built and demonstrated and achieved — the kind"
    " of person who can be chosen for yourself. Not chosen because you are useful."
    " Not kept because you are impressive. Chosen and kept because you are, simply,"
    " <i>you.</i>",

    "You have almost certainly never put it in those words. The Performance Campaign"
    " does not easily tolerate that kind of plain vulnerability. It translates the"
    " question into production targets and leaves the question itself unanswered."
    " But trace backward from the disconnection trigger that fired this week, and from"
    " the one that fired the week before, and from the campaign the Campaign"
    " launched in its private arena — the gifts, the initiatives, the plans, the"
    " extravagant gestures that look to everyone like generosity and feel, to you,"
    " like urgency — and you will find this question at the root of all of it."
    " <i>Am I lovable?</i> And behind it, barely below the surface, its darker"
    " companion: <i>Or do people love the performance, and would they leave if the"
    " performance stopped?</i>",

    "The fear underneath is not abstract. It is the specific terror of being known"
    " fully — without the portfolio open, without the résumé visible — and found,"
    " in that unguarded state, insufficient. The Campaign has spent years ensuring"
    " that this test never has to be taken. The disconnection trigger fires whenever"
    " life threatens to administer it anyway.",
]

QUESTION_BODY_P2 = [
    "There is a reason the biblical writers returned, in season after season of their"
    " own uncertainty, to the language of being <i>known</i> by God — not merely"
    " observed or recorded, but genuinely known, in the specific, interior, unmistakable"
    " way a person knows and is known by someone who loves them. The Psalms return to"
    " this again and again, never with embarrassment.",

    "<i>O Lord, you have searched me and known me. You know when I sit down and when I"
    " rise up; you discern my thoughts from afar. You search out my path and my lying"
    " down and are acquainted with all my ways.</i> (Psalm 139:1\u20133)",

    "This is not the language of surveillance. It is the language of the most intimate"
    " knowledge imaginable: every path, every posture, every thought before it is"
    " formed. David is not frightened by this; he marvels at it. He goes on to say"
    " that even if he could flee to the uttermost parts of the sea, the hand of God"
    " would be there \u2014 and not as a threat. As a holding. <i>Even there your hand"
    " shall lead me, and your right hand shall hold me.</i> (Psalm 139:10)"
    " You are held, in the place where you are most fully known, by a love that did not"
    " require a performance before it arrived.",

    "Paul, in Romans 5:8, states the gospel in the order that matters most to you:"
    " <i>God shows his love for us in that while we were still sinners, Christ died for"
    " us.</i> Not after we demonstrated our worth. Not in response to our campaign."
    " <i>While we were still sinners.</i> The love arrived before anything could be"
    " produced to justify it. This is the order the gospel insists upon, and it is"
    " exactly the order the Campaign finds most difficult to receive, because the"
    " Campaign has always believed, somewhere below the level of doctrine, that love"
    " is a response to performance and that performance therefore cannot stop.",
]

QUESTION_BODY_P3 = [
    "Here is where pastoral honesty is required. The honest rub is not doctrinal."
    " You likely do not have difficulty affirming that God loves you apart from"
    " your works. The honest rub is that you have never quite been able to believe"
    " that your <i>spouse</i> does \u2014 or could \u2014 or would if the campaign"
    " went genuinely quiet. The theological conviction and the lived experience are"
    " running in two lanes that have never fully converged. And the Campaign has"
    " been exploiting the gap between them for years.",

    "The honest work this section asks of you is not to stop producing. The"
    " Performance Campaign is not, in itself, a sin. It is a gift that has been"
    " pressed into service as a love-earning strategy, and it is wearing both you"
    " and your marriage down in the process. The honest work is to begin sitting,"
    " daily and with patience, with the order the gospel establishes:"
    " you are already loved. The campaign is not the reason. The campaign has never"
    " been the reason. There is a love already in place that did not wait for"
    " the portfolio. Receiving that love \u2014 really receiving it, past the level"
    " of doctrinal assent, past the level of the Campaign's efficient processing"
    " of theological information \u2014 is the work.",

    "Before we move forward, use the table below. You are looking at recent moments"
    " when the disconnection question fired. Name the event. Name what your body"
    " concluded. Name what the gospel says is true at the deeper level. The Campaign"
    " will want to process this efficiently and file it. Take longer than that.",
]

CAMP_BODY_P1 = [
    "You have built something. It did not announce itself as a strategy at the time of"
    " its building; it announced itself as a life. But over years and campaigns and the"
    " accumulation of evidence, you have developed a particular and recognizable way of"
    " moving through the world that we are going to call, throughout the rest of this"
    " walkthrough, <b>the Performance Campaign</b>.",

    "Before we describe it in detail, it is worth being clear about what it is not."
    " It is not the Architect's mechanism. The Architect builds systems and structures"
    " to secure the perimeter; the Campaign builds a record of demonstrated worth."
    " The Architect is trying to make the world safe; the Campaign is trying to make"
    " itself impossible to ignore. It is not the Ambassador's mechanism. The Ambassador"
    " serves relationally \u2014 warms the room, pours care on people, earns love by"
    " giving it. The Campaign's currency is not relational service but visible output."
    " The Ambassador is the one who stayed late to make sure everyone was okay;"
    " the Campaign is the one who stayed late to finish something extraordinary and"
    " needs the extraordinary thing to be known. And it is not the Adapter's mechanism."
    " The Adapter reads the room and becomes what the room needs; the Campaign"
    " demonstrates to the room. The Adapter disappears into the audience;"
    " the Campaign stands before it.",

    "The Performance Campaign is the runner. It is the achiever. It is the person who"
    " carries a long résumé and, in unguarded moments, a thin sense of who they are"
    " off the field. Its default response to anxiety is not to plan or to withdraw"
    " but to <i>produce</i>. When the question fires \u2014 <i>am I lovable?</i>"
    " \u2014 the Campaign's instinctive answer is always the same: <i>let me show you"
    " one more thing that makes it worth saying yes.</i>",

    "There is a great deal in Scripture that commends what the Campaign does at its best."
    " Proverbs 22:29: <i>Do you see a man skillful in his work? He will stand before"
    " kings; he will not stand before obscure men.</i> Colossians 3:23: <i>Whatever"
    " you do, work heartily, as for the Lord and not for men.</i> The Performance"
    " Campaign is not, at its root, a sin. It is a gift. The runner was given real"
    " legs and learned to run genuinely well, and the running has produced things"
    " that were not wasted. The trouble is not with the running. The trouble is with"
    " what the running is attempting to answer.",
]

CAMP_BODY_P2 = [
    "The history that tends to produce the Performance Campaign takes several recognizable"
    " forms, and most of them involve, at some early point, a lesson about the relationship"
    " between love and performance. Perhaps ordinary effort was simply unremarkable in your"
    " household while extraordinary effort was finally noticed \u2014 which trained your"
    " system to the conclusion that the path from invisible to seen ran through the"
    " exceptional. Perhaps there was a parent whose emotional attention was distributed"
    " unevenly, and achievement became the reliable method of capturing what felt like"
    " real warmth. Perhaps you grew up one child among several in a family where visibility"
    " had to be earned rather than assumed, and you were an early learner of the relevant"
    " lesson. Whatever the specific form, the conviction arrived with real force:"
    " <i>if I am excellent enough, I cannot be set aside. If I cannot be set aside,"
    " I cannot be abandoned. If I cannot be abandoned, I am safe.</i>",

    "The Campaign arrived as an answer to that conviction. And in many arenas, it worked."
    " The Campaign produces genuinely energizing experiences: the pursuit, the vision,"
    " the satisfaction of something finished with real craft. Rest, by contrast, tends"
    " to produce for the Campaign a particular and uncomfortable anxiety. Not physical"
    " fatigue \u2014 physical rest is often welcome. But the cessation of forward movement,"
    " the afternoon when there is nothing to produce or demonstrate: this produces, with"
    " disturbing regularity, an unease without a clear cause. Because the cause is not in"
    " the afternoon. It is in the question the afternoon allows to surface:"
    " <i>and who are you, when you are not running?</i>",

    "Your spouse \u2014 or the person who has known you longest and most honestly \u2014"
    " has probably said some version of the same sentence more than once. Not cruelly."
    " Honestly. <i>I feel like an afterthought.</i> Or: <i>You are never fully here.</i>"
    " Or: <i>I don't know how to reach you when the campaign is on.</i>"
    " The Campaign has a visibility problem: it can see the next achievement with"
    " extraordinary clarity, and the people standing quietly in the room \u2014 wanting"
    " simply to be with you, not to witness another performance \u2014 blur at the edges.",

    "<b>The Campaign is not your enemy.</b> It is a younger version of you who learned,"
    " in some real and specific circumstance, that achievement was the reliable path to"
    " being held, and that being held was necessary for being safe. He has been faithful."
    " He has produced genuinely remarkable things and kept you visible in arenas that"
    " rewarded visibility. He deserves respect, not contempt. But he is not twelve"
    " any longer, and you are not in the household or the classroom or the early"
    " season of your career that required him. The question he is running toward an"
    " answer to \u2014 <i>am I lovable?</i> \u2014 is not located at the finish line"
    " of any campaign. It is located somewhere else entirely. And it is time"
    " to hear what he has been afraid to say.",
]

CAMP_LETTER_INSTRUCTION = [
    "The letter below is written in the Campaign's voice \u2014 addressed to you,"
    " from the part of you that has been running since before you could name what"
    " it was running from. He is not a villain. He is a builder who has been trying"
    " to earn something that was never going to be earned by building. Read it slowly."
    " Then answer the three prompts that follow.",

    "Dear [your name],",

    "I learned early that love was warmer when you performed. Someone whose warmth"
    " mattered enormously \u2014 whose face changed when you achieved something"
    " and returned to its ordinary distance when you did not \u2014 wrote a lesson"
    " into you before you were old enough to question it: <i>the path to being loved"
    " runs through being excellent enough to be worth loving.</i> And so I began. I"
    " built the campaign. I ran.",

    "What I want you to understand is what I did for you. I kept you visible."
    " I gave you something to point to when the question came \u2014 quietly, in"
    " the hours after the applause was gone: <i>are you, as you are, worth"
    " staying for?</i> I gave you credentials and results and a record that made it"
    " difficult for anyone to dismiss you. What I could not give you \u2014 what I"
    " am only beginning to understand I was never built to give you \u2014 was the"
    " security of being loved when the campaign went quiet. I could make you"
    " impressive. I could not make you certain of being cherished.",

    "And when the gap opened in the marriage, I did what I always do. I launched"
    " a campaign. Gifts. Plans. Letters. Vacations. Surprises. All of it genuinely"
    " motivated. And all of it, underneath the genuine feeling, an argument:"
    " <i>look what I have given you. You cannot say I do not love you.</i>"
    " I built the right instinct \u2014 to love your spouse extravagantly \u2014"
    " for the wrong reason. I am ready to admit I cannot run this particular campaign"
    " to its conclusion on my own.",

    "The Performance Campaign",
]

CAMP_LETTER_PROMPTS = [
    "What part of the Campaign's letter surprised you? Not the part you were prepared"
    " for \u2014 the part you were not ready to read.",

    "The Campaign says it gave you gifts and plans and surprises when the gap opened"
    " \u2014 and that all of it was, underneath the genuine feeling, an argument."
    " When was the last time you gave your spouse something that was not, in any"
    " part, an argument? Describe that moment, or describe the absence of it.",

    "The Campaign says it built the right instinct for the wrong reason. Name one"
    " specific gesture of love toward your spouse \u2014 a gift, a plan, a"
    " surprise \u2014 that you have made in the last month. What was the right"
    " reason? What might the wrong reason have been? Can you tell the difference"
    " from the inside?",
]

PLEA_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Performance Campaign, the breaking"
    " takes a form that is, among all the profiles we follow in this work, the most"
    " difficult to name clearly \u2014 because it does not look like breaking."
    " It looks like love.",

    "The breakdown is called <b>the Plea</b>. And the Performance's version of it is"
    " unlike the ones we have encountered elsewhere. When the Plea takes the floor in"
    " an Architect, it tends to be organized: the Architect plans the repair and"
    " manages it with his usual intentionality. When the Island pleads, it is"
    " disorienting and uncharacteristic \u2014 the self-contained suddenly running"
    " outward. When the Ambassador pleads, it doubles down at triple volume, pouring"
    " out more relational service than the relationship can absorb. When the Vault"
    " pleads, it slides a carefully written apology \u2014 edited, organized, precise"
    " \u2014 under the door at two in the morning. When the Adapter pleads, it cycles"
    " rapidly through every version of itself, one every few minutes, each one"
    " genuine, each one a different attempt to find the version that closes the gap.",

    "The Performance's Plea is different from all of these. It does not become disorganized."
    " It does not become more relational. It does not cycle through versions. It does"
    " what the Campaign has always done. It <b>launches a new campaign</b>. The only"
    " difference is the audience.",

    "Here is what it looks like. The Campaign has been running its ordinary operations"
    " \u2014 building publicly, producing visibly, earning recognition in the arenas"
    " where recognition is available. And then something happens in the marriage."
    " A sustained silence that does not resolve on its own. A criticism that lands with"
    " unexpected weight. A growing sense that the spouse is somewhere the Campaign's"
    " best work cannot reach. The Campaign cannot address this from its usual position,"
    " because the usual position produces output for a general audience, and what is"
    " needed here is something the Campaign has not been trained to provide: love that"
    " does not require a result. And so, because the Campaign does not know any other"
    " mode, it does the thing it knows how to do. It redirects. It converts.",
]

PLEA_BODY_P2 = [
    "The private campaign is, in many respects, more extravagant than the public one."
    " The gifts arrive \u2014 thoughtful ones, sometimes expensive ones, chosen with a"
    " care the Campaign brings to its best work. The surprises appear. The weekend"
    " away is planned \u2014 the one they said they wanted, three years ago, and"
    " you filed it and now you have arranged it, in a week, with the kind of execution"
    " that, in a different context, would produce a standing ovation. The letters."
    " The Campaign writes letters the way the Campaign builds anything: with real"
    " craft and genuine emotion. The letter arrives, and it is honest, and it is"
    " moving, and it is also \u2014 underneath all of that \u2014 a brief. An"
    " argument. A closing statement delivered to the only jury whose verdict"
    " currently matters.",

    "The spouse receives all of this. And something happens on the receiving end that"
    " the Campaign does not anticipate and cannot initially understand. The spouse"
    " feels, beneath the gratitude and the genuine recognition that this is a lot,"
    " something that is best described as increasingly suffocated. The gifts keep"
    " coming. The plans accumulate. The surprises continue to arrive. And the spouse"
    " begins to feel, without being able to quite name it, that they have become a"
    " performance venue \u2014 that the Campaign has moved its apparatus indoors and"
    " is now staging its most ambitious show in the living room. <b>The love is"
    " real. The campaign is also real. And the campaign is getting in the way of"
    " the love being received as love rather than as pressure.</b>",

    "This is the cruel irony at the heart of the Performance+Plea. The Campaign is"
    " genuinely trying to love. The giving is not calculated or insincere. But"
    " every gift given to close the gap \u2014 rather than from a love already"
    " secure \u2014 arrives with invisible strings attached. Not deliberately."
    " But really. The gift is not simply given; it is given <i>to produce a"
    " result</i>. The vacation is not simply planned; it is planned so that the"
    " spouse will remember it and remember you and remain. The letter is not simply"
    " written; it is written to accomplish something the Campaign cannot quite name"
    " but urgently needs. And the spouse, somewhere beneath their gratitude, can"
    " feel the weight of that needing. It is not the weight of generosity."
    " It is the weight of an audience requirement.",
]

PLEA_BODY_P3 = [
    "Here is the pastoral word this profile most needs to hear, and I want to say it"
    " with the care it requires, because naming it wrongly could do real harm."
    " <b>The Performance+Plea is one of the most insidious of the six plea profiles"
    " precisely because it presents as love and functions as performance under a"
    " different name.</b> The gift is given to close the gap, not in response to a"
    " love already secure. The vacation is planned to be remembered, not to remember"
    " the marriage. The letter is crafted to produce a verdict, not simply to say"
    " what is true. This is not hypocrisy. It is not dishonesty. It is the Campaign"
    " doing the only thing it knows how to do, applied now in the one arena where"
    " that thing cannot work.",

    "John writes something in his first letter that names precisely what is happening:"
    " <i>We love because he first loved us.</i> (1 John 4:19) The order matters"
    " more than it looks like it does. John is not making a point about gratitude."
    " He is making a point about the <i>origin</i> of love. Real love \u2014 the love"
    " that gives without requiring a return \u2014 flows from a love already received."
    " From security already possessed. From a knowing that you are already held, already"
    " enough, already loved not because of what you will produce but because of who"
    " you are to the One who made you. The Campaign has been running the sequence in"
    " reverse: <i>I love in order to receive love, in order to be secure, in order to"
    " know that I am loved.</i> That sequence does not work. It has never worked."
    " The love given in order to produce a return cannot generate the security it is"
    " trying to purchase, because the security it is trying to purchase is not"
    " available from that direction.",

    "Tim Keller, in <i>The Meaning of Marriage</i>, puts it with a directness that"
    " is worth sitting with: \u201cMarriage is the most profound human relationship,"
    " but it cannot bear the weight of being your salvation.\u201d The Performance"
    " Campaign, when the Plea has fired, is asking the spouse to do exactly that:"
    " to be the source of the acceptance that makes the Campaign finally feel that"
    " it is enough. This is too heavy a weight for any human being to carry. The"
    " spouse will fail under it \u2014 not because they do not love you, but because"
    " what is being asked is the work of the cross, and the cross has already done it.",

    "Charles Spurgeon, writing on the love that flows from union with Christ,"
    " observed that the Christian who has truly received the love of God is free"
    " to love others without needing anything from them in return \u2014 not because"
    " they are emotionally self-sufficient, but because their deepest need has already"
    " been met from a source that is not human. The love that gives without the"
    " agenda of return is not a heroic love; it is a loved love. It comes from"
    " someone who has already received. Jonathan Edwards, with his characteristic"
    " precision, named the same truth from a different angle: \u201cChrist is the"
    " proper rest of every soul.\u201d Not the spouse. Not the marriage. Not the"
    " verdict of the most important jury the Campaign has ever addressed."
    " Christ. And when that rest is found \u2014 when the Campaign discovers that"
    " its deepest question has already been answered from outside the campaign entirely"
    " \u2014 the gifts given to the spouse can finally become what they were always"
    " meant to be: gifts. Freely given. From fullness. Without the agenda of return.",
]

PLEA_PROMPTS = [
    "Think of the last time the Plea launched its private campaign \u2014 the last"
    " time you gave a gift, made a plan, wrote a letter, arranged a surprise, or"
    " produced something extravagant specifically because the gap was open and you"
    " needed it to close. Describe it in two sentences. Try not to edit for how"
    " it reflects on you.",

    "The Plea campaigns because it needs a verdict from the spouse. What is the"
    " specific verdict it is after? Write it in one sentence beginning:"
    " <i>If my spouse could just say ___, I would finally feel ___.</i>"
    " Now ask: is that a verdict any human being can reliably supply?"
    " And is there a source from which that verdict has already been spoken?",
]

TWO_TOG_BODY = [
    "Now we stand back and look at both of them together, because the Performance"
    " Campaign and the Plea are not two separate problems. They are the same longing,"
    " running in two theaters. The Campaign runs in public: building, producing,"
    " demonstrating, earning the record that it hopes will make the love"
    " self-evident. The Plea runs in private: lavishing, giving, planning, arranging,"
    " redirecting the full force of the Campaign's apparatus onto the one person"
    " whose love the Campaign has never been able to simply receive.",

    "<b>The Campaign is what your longing does when the question is quiet enough to"
    " be managed by production.</b> The Plea is what your longing does when the"
    " question has broken through the production and cannot be managed by producing"
    " more. The Campaign earns significance in the public arena. The Plea earns"
    " love in the private one. Together they form a closed loop, and the loop will"
    " run all your life if something does not interrupt it from outside.",

    "The pattern, in slow motion: <b>(1)</b> The Campaign runs its public operations:"
    " building, producing, accumulating a visible record of demonstrated worth."
    " <b>(2)</b> The disconnection trigger fires in the marriage \u2014 the gap"
    " appears, the spouse is slightly further away, the private register says"
    " something is wrong here. <b>(3)</b> The core question surfaces:"
    " <i>Am I lovable?</i> <b>(4)</b> The Campaign does the only thing it knows"
    " how to do: it redirects its full apparatus from the public arena to the"
    " private one. <b>(5)</b> The Plea launches its campaign: gifts, letters,"
    " surprises, plans, extravagant gestures that present as love and function,"
    " underneath, as argument. <b>(6)</b> The spouse receives the campaign and feels,"
    " beneath the gratitude, the weight of being an audience requirement."
    " The gap does not close in the way the Campaign needs it to close."
    " <b>(7)</b> The question wakes up the next morning, and the loop"
    " begins again.",

    "What interrupts the loop is not a better campaign and not a more extravagant"
    " Plea. It is the slow, daily, often unwilling practice of receiving the love"
    " that has already been given \u2014 not by the spouse, but by the One who loved"
    " you while you were still a sinner and who has not revised that verdict since."
    " When that love is received not as doctrine but as reality \u2014 when the"
    " Campaign discovers, in the specific, interior place where the question lives,"
    " that the question has already been answered and the answer requires nothing"
    " from the spouse to remain true \u2014 the Campaign begins to produce for"
    " different reasons. And the Plea, finding that the urgent need has been met"
    " from another direction, discovers it is free to love without the agenda of"
    " return. It is not an instantaneous change. It is a practice. But it is possible.",

    "Below is your sequence in your own words. Write in the blanks. When you are done,"
    " read it aloud. The Campaign and the Plea both lose some of their power when"
    " they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me registers it as disconnection,"
    " and the old question surfaces \u2014 <i>am I lovable?</i> My first move is to"
    " ____________________, because the Campaign in me believes that if I can"
    " ____________________, the gap will close and the love will be secured."
    " When that does not work, the Plea takes the floor and launches"
    " ____________________ \u2014 gifts, plans, letters, surprises \u2014 because"
    " the Campaign does not know another mode. What I am actually after, underneath"
    " all of it, is the verdict ____________________. That verdict has already been"
    " spoken over me, not by ____________________, but by the One who loved me"
    " while I was still ____________________, and who has not changed his mind."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a set of tools \u2014 each small enough to"
    " carry, each honest enough to use. None of them will dissolve the Campaign's"
    " pattern after a single application. All of them, practiced with patience over"
    " months, will loosen the grip of the loop you just named.",

    "I have divided them into two sets: tools for when the Campaign is overrunning"
    " \u2014 when the producing has tipped from genuine vocation into love-earning"
    " strategy \u2014 and tools for when the Plea has taken the floor and the private"
    " campaign has launched. The Campaign's tools come first, because the Plea cannot"
    " be interrupted usefully until the mechanism underneath it is understood.",
]

CAMP_TOOLS = [
    ("The stopped-clock practice",
     "Once a week, spend thirty minutes doing something with no measurable output and"
     " no audience. Not a walk to clear your head for the next campaign. Something"
     " genuinely unproductive and genuinely private: sit in a garden, read slowly,"
     " watch the light. When the anxiety rises \u2014 and it will \u2014 name it:"
     " <i>this is the question surfacing without the campaign to answer it.</i>"
     " Do not answer the question. Let it be present without immediately running."
     " The Campaign cannot be loosened without first allowing the question it is"
     " running from to have genuine air."),

    ("The gift audit",
     "Before you give your spouse a gift or plan a surprise, pause and ask one question:"
     " <i>Is this from fullness, or is this from the Plea?</i> Not to stop giving"
     " \u2014 giving is good and marriages need it. But to distinguish between the"
     " gift given freely and the gift given urgently. One of these builds the marriage."
     " The other builds the case. Over time, the pausing itself begins to create"
     " real space between the Campaign's urgency and your actual generosity."),

    ("The work-worship distinction",
     "Before beginning any significant project or initiative, ask:"
     " <i>If no one ever knew I did this \u2014 including my spouse \u2014"
     " would I still want to have done it?</i> This is not a test of purity."
     " It is the question Colossians 3:23 is asking: <i>whatever you do, work heartily,"
     " as for the Lord and not for men.</i> Work done for the Lord does not need"
     " the spouse to respond on schedule. The Campaign that has learned to work"
     " for the Lord can rest when the response does not arrive as expected."),

    ("The handed-back campaign",
     "Each morning, name one initiative currently in motion \u2014 at work, in the"
     " marriage, in the family \u2014 and say aloud: <i>This is yours today, Lord."
     " I did not build this to be remembered. I built it because you gave me these"
     " hands. The result is yours.</i> This will feel hollow the first twenty"
     " mornings. By the fiftieth, the Campaign begins to discover, in the practice,"
     " that handing the result back does not produce the death it feared."
     " It produces a quieter and more durable energy for the work."),

    ("The presence practice",
     "Once a day, give your spouse ten minutes of full and undivided presence:"
     " no device, no agenda, no half-attention toward the next initiative. Not to"
     " produce a better marriage \u2014 though it will. But because the Campaign's"
     " most characteristic failure is treating the person standing quietly in the"
     " room as background to the main event. This practice begins to reverse that"
     " posture, one ten-minute session at a time. The spouse who is seen, simply"
     " and without agenda, begins to feel the difference between being loved"
     " and being an audience."),
]

PLEA_TOOLS = [
    ("The gap-naming pause",
     "When the Plea begins to move \u2014 when you feel the urgency to give something,"
     " plan something, send something, arrange something extravagant in response to"
     " the gap \u2014 give yourself twenty-four hours before you act. Not to refuse"
     " connection. Not to perform the Campaign's composure. But to ask:"
     " <i>Is this from love, or is this from the Plea? Am I giving because I am"
     " full, or because I am frightened?</i> Those are different questions. The"
     " answer will not always be simple. But asking it disrupts the Campaign's"
     " automatic conversion from disconnection signal to private campaign."),

    ("Name the fear before you close the gap",
     "Practice saying to your spouse, simply and without the campaign:"
     " <i>I can feel some distance between us, and it is harder for me than I"
     " usually let on. I don't know how much of what I am feeling is about this"
     " week and how much is older. But I wanted you to know it is real.</i>"
     " This sentence does not give a gift. It does not launch an initiative."
     " It does not present a case. It names something true from the interior"
     " without requiring an immediate response. For the Campaign, this is one of"
     " the most difficult and most genuinely loving things on this list."),

    ("The received-love practice",
     "Each morning, before any initiative or agenda begins, read one of the following"
     " slowly and as addressed to you by name: Romans 5:8 (<i>while we were still"
     " sinners, Christ died for us</i>), 1 John 4:19 (<i>we love because he first"
     " loved us</i>), Psalm 139:1\u20133, or Isaiah 49:15\u201316. Read it not as"
     " information but as the answer to the question that is going to surface again"
     " today. The Campaign will not feel it the first fifteen mornings. It is the"
     " daily reorientation toward a love already possessed \u2014 the practice of"
     " receiving, before the Plea has a chance to launch, the verdict the Plea will"
     " spend the day trying to earn."),

    ("Ask before you give",
     "Before any extravagant gesture \u2014 the vacation, the gift, the letter, the"
     " surprise \u2014 ask your spouse, plainly: <i>Is this what you actually need"
     " from me right now?</i> Not rhetorically. Genuinely. The Campaign's gifts are"
     " often precisely calibrated to what the Campaign believes will close the gap."
     " They are less often calibrated to what the spouse is actually asking for."
     " Asking converts the gesture from campaign to conversation."),

    ("The advocate prayer",
     "When the Plea is loudest \u2014 when the urgency is highest and the campaign"
     " is fully assembled and ready to launch \u2014 pray these words slowly, and"
     " mean them: <i>Father, you loved me while I was still a sinner. You did not"
     " wait for a campaign. You did not require a performance. The verdict has"
     " already been spoken: I am yours. Let that be enough for today. Give me"
     " the grace to love my spouse from that fullness rather than from this fear.</i>"
     " Say it three times. The third time is usually when the urgency begins,"
     " very slightly, to lift."),
]

PRAYER_BODY = [
    "Father,",

    "You see the Campaign in me, and you are not impressed, and you are not disappointed."
    " You knew about the running before it started. You know which early moment wrote"
    " the lesson that love had to be earned, and which season it was when I first"
    " understood that the path from forgotten to held ran through the exceptional."
    " Thank you that the Campaign has produced real things. Thank you that those things"
    " were not wasted, even in the seasons when they were motivated by something other"
    " than you.",

    "But Father, the Campaign has moved indoors now, and I am watching it do to my"
    " marriage what it has done in every other arena \u2014 produce extravagantly in"
    " order to earn what cannot be earned. I am asking my spouse to carry what only"
    " you can carry. I am asking the marriage to answer what only the cross has answered."
    " Teach me the order that John names: <i>we love because he first loved us.</i>"
    " Let the love flow from received love rather than from the terror of losing it."
    " Teach me that the verdict \u2014 <i>you are mine, I will not let you go</i>"
    " \u2014 was spoken before any campaign produced a single entry, and has not"
    " been revised since.",

    "Lord Jesus, when the Plea launches its private campaign \u2014 when the gifts"
    " and the letters and the plans begin to accumulate as an argument rather than"
    " a gift \u2014 would you remind me of what Keller names plainly: that the"
    " marriage cannot bear the weight of being my salvation. That is your weight to"
    " bear, and you have already borne it. Would you give me the grace to love my"
    " spouse freely \u2014 as Spurgeon described, from the union that has already been"
    " secured \u2014 so that what I give is given from fullness and not from the"
    " Plea's urgency. And would you give my spouse the grace to receive it that way.",

    "Holy Spirit, where I am producing to be loved, give me the freedom to produce"
    " for the Lord instead. Where the Plea is launching the private campaign, give"
    " me the courage to name the fear instead of covering it with an initiative."
    " Where rest feels like risk, give me the faith to be still and know that I am"
    " held even when the Campaign has nothing to offer. <i>Christ is the proper rest"
    " of every soul</i> \u2014 including this one. Teach me to rest in him.",

    "In the name of the One who was given freely, without conditions, before"
    " we had produced anything to justify the giving \u2014 I pray.",

    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Performance Campaign and"
    " the Plea have been running together for a long time, and one careful reading"
    " will not retire either of them. What follows is a short list of next steps"
    " \u2014 some immediate, some longer \u2014 for the work you have just begun."
    " Do not try to do all of them at once. The Campaign will want to process"
    " the entire list efficiently and treat completion as the goal. Resist that.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.",
     "Different lines will land. The Campaign will want to file this walkthrough"
     " as a completed project and move to the next item. Read it again anyway."
     " The section that felt least relevant today may be the most necessary one"
     " in a month. Pay special attention to Section Five on your second reading."),

    ("Take one tool, not six.",
     "Choose a single practice from Section 7 and try it honestly for two weeks"
     " before adding another. The tools are not a performance metric. They are"
     " postures. One posture, held for long enough, begins to give the self beneath"
     " the Campaign a chance to be present in the marriage without an agenda."),

    ("Tell your spouse what you found.",
     "Not the whole document. One honest sentence: <i>I think I have been loving you"
     " in campaign mode, and I want to try something different.</i>"
     " This is not a performance of transparency. It is the first step of the"
     " Campaign learning to operate without an audience \u2014 even in confession."),

    ("Read The Meaning of Marriage.",
     "Tim Keller, <i>The Meaning of Marriage: Facing the Opportunities and Challenges"
     " of Christian Marriage</i>. Read specifically the chapter on marriage and"
     " self-knowledge. Keller's account of what a marriage cannot bear \u2014 and"
     " what the gospel frees it from having to bear \u2014 is the most direct"
     " pastoral address to what the Performance+Plea is doing that exists in"
     " modern Christian writing."),

    ("Read further on counterfeit gods and received love.",
     "Tim Keller, <i>Counterfeit Gods</i> \u2014 especially the chapter on the"
     " counterfeit god of human approval and achievement. C. S. Lewis,"
     " <i>The Weight of Glory</i> \u2014 the opening essay on the nature of"
     " the longing that drives the Campaign and the direction it rightly points."
     " For Scripture, spend a week in 1 John 4, reading slowly and praying"
     " verse 19 each morning as a direct address to the Campaign before any"
     " initiative begins."),

    ("If you are stuck, ask for help.",
     "There are seasons when the Campaign and the Plea are too entrenched to"
     " dislodge alone \u2014 and the marriage may be at a pressure point that"
     " needs more than a walkthrough. A wise pastor, a Christian counselor,"
     " a trusted friend who knows you off the field: these are not signs of failure."
     " For the Campaign specifically, asking for help without framing it as a"
     " project to be successfully completed is one of the most countercultural"
     " and most necessary things on this list."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved, and your marriage is not a campaign to be won."
    " You are a son or daughter being loved into freedom by a Father who loved you"
    " while you were still a sinner \u2014 before any performance, before any campaign,"
    " before the first gift was given or the first plan was made. The Campaign did not"
    " earn that love. The Plea cannot lose it. Go gently with yourself and gently with"
    " your spouse. The One who began the good work in you will be faithful to complete it,"
    " and he will not require a portfolio as evidence of your progress."
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
        [Paragraph("AM I LOVABLE HERE?", header_style), Paragraph("what the Campaign concluded", sub_style)],
        [Paragraph("WHAT GOD HAS SAID", header_style), Paragraph("the verdict already spoken", sub_style)],
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
    """Generate the Performance Campaign+Plea walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='CAMP', primary_breakdown='PLEA',
    primary_trigger='DISC', core_question='LOV'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="PERFORMANCE  \u00b7  PLEA",
        title="Take 139 Walkthrough \u2014 Performance Campaign + Plea",
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
    story.append(Paragraph("The Performance Campaign \u00a0\u00b7\u00a0 The Plea", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disconnection \u00a0\u00b7\u00a0 Core Question: Am I lovable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cWe love because he first loved us.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "1 John 4:19",
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
                   "Disconnection.",
                   "The moment the gap opens in the one arena the Campaign was not built for.")
    for p in TRIGGER_BODY[:4]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  CONTINUED",
                   "Where the sensitivity came from.",
                   "What was lodged in you, and what to do with what you find.")
    for p in TRIGGER_BODY[4:]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will reach for the next initiative. Your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 3: Core Question \u2500\u2500
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I lovable?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "What Scripture says \u2014 and the order that matters.",
                   "Loved while we were still sinners. Before any campaign.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "The honest rub.",
                   "Doctrine in one lane, lived experience in another.")
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
                   "What the Campaign costs, and what it cannot answer.",
                   "The question that surfaces when the running stops.")
    for p in CAMP_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))

    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Campaign.",
                   "Read what he has been afraid to say. Then answer the three prompts.")
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
                   "The Plea.",
                   "The place your mechanism breaks \u2014 and why it looks like love.")
    for p in PLEA_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in PLEA_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "We love because he first loved us.",
                   "The order the gospel insists upon, and the weight the marriage cannot bear.")
    for p in PLEA_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Name the campaign.",
                   "Two questions to sit with before you turn the page.")
    for prompt in PLEA_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same longing, in two theaters.",
                   "The Campaign and the Plea are not two problems. They are one loop.")
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
                   "Five practices for the time before the Plea launches.")
    for name, desc in CAMP_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Plea is running.",
                   "Five practices for the moment the private campaign assembles.")
    for name, desc in PLEA_TOOLS:
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


# \u2500\u2500 STANDALONE TEST \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "CAMP"
        primary_breakdown = "PLEA"
        primary_trigger = "DISC"
        core_question = "LOV"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "performance_plea_test.pdf")
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
        for page in reader.pages[1:4]:
            txt = page.extract_text() or ""
            if txt.strip():
                snippet = txt.strip()[:120]
                break
    except Exception:
        page_count = pdf_bytes.count(b"/Type /Page\n") + pdf_bytes.count(b"/Type/Page\n")
        snippet = ""

    print(f"DONE: performance_plea.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
