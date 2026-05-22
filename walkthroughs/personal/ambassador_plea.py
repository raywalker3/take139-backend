"""Personal Walkthrough — Ambassador + Plea.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disconnection trigger, "Am I lovable?" core question.
~25 pages, 9 sections.

KEY PROFILE INSIGHT — THE DOUBLE-DOWN:
The Ambassador's ordinary mode IS already a chronic, low-grade Plea. The
Ambassador has organized their whole life around the principle: if I keep
serving, love stays. The Ambassador+Plea breakdown is not a departure from
this strategy. It is the same strategy at three times the volume — the same
person, the same impulse, but now panicked, now doubled, now audible to
everyone in the room. They apologize harder. They give more. They cancel their
own plans to attend to a gap that may not even be real. They check in again.
They ask once more whether everything is okay.

The unique pastoral move (Section Five): the Ambassador+Plea is functionally
trying to atone for their relationships through additional service. This is the
same theological error as trying to atone for sin through additional good works.
Gospel texts: Galatians 3:3; Luther, 95 Theses, Thesis 1.
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
    "Before you read any further, I want to do for you what a good pastor does at the beginning of a hard conversation \u2014 lower the lights and slow the pace. What we are about to look at is not a catalogue of your gifts, though you have real ones. It is a patient account of the way your soul has learned to keep itself safe, and what happens, at a very specific pressure point, when that strategy does not so much collapse as intensify.",
    "You have, in all likelihood, been the person who kept the rooms you inhabited at a livable temperature. You noticed when the warmth between two people was thinning and quietly moved to restore it. You remembered the details others forgot, made the call before it was asked for, gave time and care in a way that people around you have relied on for years. And if I asked the people who love you most to describe you, many of them would say some version of this: <i>they just always show up.</i>",
    "We are going to walk through your trigger \u2014 the specific moment your body says something is wrong. We will listen to the question underneath that moment, one that has almost certainly been with you since before you had language for it. We will name the strategy you built to answer that question on your own, and the particular shape of its breaking. And then, only then, will we put tools in your hands.",
    "If you were sitting across from me, I would say this plainly. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father whose love for you is not a function of your usefulness to him; a Son who, having loved his own who were in the world, loved them to the end \u2014 not to the degree to which they returned it; and a Spirit who is, at this very moment, interceding for you with groanings that words cannot express, not because you have earned that intercession but because you belong to him.",
    "So read slowly. Argue with what does not fit. Stay longer with what does. If a sentence catches in your throat, stay with it \u2014 that catch is usually the Lord putting his finger on something worth looking at together. The goal of this walkthrough is a slightly freer life: one in which you give because you are loved, rather than giving in order to keep testing whether you still are. This chapter about yourself has been a long time in the writing. It deserves your patient attention.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life have no idea it is occurring \u2014 not because they are careless, but because you have become very skilled at absorbing it without showing it. Your spouse has been quiet all evening. Not cold, not hostile, just somewhere else. A friend replies to your carefully composed message with three words after you wrote three paragraphs. The gathering you attended passed warmly for everyone in the room, but it was somehow thinner than you needed it to be. Or you gave something \u2014 time, care, real effort that cost you something \u2014 and it was received without comment, absorbed into the ambient condition of your presence as though it had simply always been there.",
    "On the surface, none of these events register as catastrophes. You may not show anything. You may be the one who then turns to ask how the other person is doing, who smooths the moment over, who generates warmth to fill the gap. You are practiced at that. But inside, something has registered. A quiet signal, specific and cold, has fired: <i>the connection is thin. Something is wrong. Did I do something? Is it me? Am I losing them?</i>",
    "This is your trigger. The word for it is <b>disconnection</b> \u2014 and for you it is not merely the neutral absence of contact. It is the withdrawal of warmth from a person whose warmth you rely on, and it does not feel like a neutral condition. It feels like a verdict, or the early sound of one. C. S. Lewis, in <i>The Four Loves</i>, observed that the more we love, the more we open ourselves to pain \u2014 that love by its very nature is a vulnerability, and that the only way to avoid that exposure is to stop loving, which is a kind of death. For most people, this is a general warning. For you, it is a map of something specific.",
    "<b>Your sensitivity to disconnection is not a random feature of your personality.</b> It grew in specific soil. Most Ambassadors carry a history in which closeness was real but not guaranteed \u2014 a household in which love was warm on some days and noticeably cooler on others, and the child in you discovered that the warmth seemed to track with your behavior. When you were helpful, the temperature went up. When you had needs of your own, the temperature dropped. And so you learned to become helpful \u2014 to become the person who was easiest to keep around, because easiness was the closest thing to safety you could construct.",
    "Perhaps there was genuine pain in your household \u2014 a parent struggling, a marriage under strain, a sibling whose needs consumed most of the available attention \u2014 and you became, without anyone asking you to, the one who managed the emotional temperature. Who could read the room before others did, and position themselves quietly between the storm and the people who could not weather it alone.",
    "Whatever the specific form, the lesson lodged in you was this: <i>love is something that must be maintained. It is a fire that requires fuel, and I am one of the primary sources of fuel. If I stop bringing what I bring, the fire goes out, and when the fire goes out, I am alone in the dark.</i> Before we go further, take a breath and answer two questions in writing. Not in your head \u2014 your head will manage and redirect. Your hand will tell you what your head is trying not to say.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week, that the disconnection signal fired. What happened, in two sentences? You are looking for the moment your internal temperature dropped \u2014 not necessarily a dramatic event, but the moment something in you said <i>the warmth is gone or going.</i>",
    "What was the size of the actual event, and what was the size of the response inside you? If those two things did not match \u2014 if a small withdrawal produced something larger than its cause would seem to warrant \u2014 you have just located your trigger.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding. For the Ambassador, this question has been present for so long, and has been managed so competently, that you may have genuinely forgotten it is still there. But it is still there. The warmth you give and the attention you maintain and the phone calls you make \u2014 all of it is, in part, a very long answer to a question you have never quite been able to close.",
    "Yours is this: <b>Am I lovable?</b>",
    "Not <i>am I loved?</i> \u2014 you have received love, you know you have, and yet the question does not quiet. The question is more frightening and more specific than that. It is the question of a person who has given a great deal and still wonders, in the small hours: <i>if I stopped giving, if I went quiet and still and stopped managing the warmth between us \u2014 would anyone stay? Am I wanted for what I am, or only for what I do?</i>",
    "Most adults prefer to believe they settled this question long ago. They have not settled it. They have only buried it under sufficient activity that it does not speak clearly in the daylight hours. For the Ambassador, it speaks in the silences \u2014 in the spouse's quiet evening, in the friend's short reply, in the gathering that was warmer for everyone else in the room. And in those silences, the nervous system's verdict is not gentle: <i>you see? Even after everything you have given, the warmth can simply disappear. This is what you have always suspected. You are not someone people stay for on their own.\u2013</i>",
]

QUESTION_BODY_P2 = [
    "There is a reason theologians from Augustine to Calvin have insisted that the soul's deepest hunger is finally God-shaped. Augustine's words have endured because they are so exactly true: <i>Thou madest us for Thyself, and our heart is restless, until it repose in Thee.</i> The longing that drives the Ambassador is this ancient longing \u2014 to be loved not for what you produce but for who you are. To be known, fully, and kept anyway. This longing is not pathological. It is the mark of the image of God in you, seeking the right thing in the wrong place.",
    "The Psalms understand this longing from the inside. Psalm 103 begins with a remarkable accumulation: <i>He forgives all your iniquity, he heals all your diseases, he redeems your life from the pit, he crowns you with steadfast love and mercy.</i> (Psalm 103:3\u20134) Notice the word at the center: <i>steadfast love.</i> The Hebrew is <i>hesed</i> \u2014 the covenant love of God, decided before you did anything to earn it, irrevocable by anything you fail to do. The Ambassador's soul is not looking for affection or approval, finally. It is looking for hesed. A love that holds without condition.",
    "The gospel answer to <i>am I lovable?</i> is not <i>yes, because of who you are</i> \u2014 that would be flattery \u2014 and it is not <i>yes, because of what you have given</i> \u2014 that would confirm the Ambassador's equation. The answer is: <i>you are loved not because you are lovable but because you are in Christ.</i> Paul names it in Romans 8:15: <i>you did not receive the spirit of slavery to fall back into fear, but you have received the Spirit of adoption as sons, by whom we cry, Abba! Father!</i> The word <i>Abba</i> \u2014 the intimate household word, the word a child used for the father who was always home \u2014 this is your word now, not because of your faithfulness but because of Christ's.",
    "Here pastoral honesty must say something difficult. The Ambassador hears this and assents. You may even feel it, briefly and warmly. And then, within the hour, you are back on your feet taking care of someone, because the only proof of love that fully registers in your body is relational warmth, not doctrinal statement. The hardest thing about this answer is not the theology. It is the receiving. Receiving requires stopping, and stopping requires trusting that the room will be all right without you managing it. The Ambassador has not yet learned, in the body, that it is safe to stop.",
]

QUESTION_BODY_P3 = [
    "Here is the honest work this section requires of you. The Ambassador has been trying to earn, through an endless offering of warmth and service, the security that comes only from being unconditionally given to. This is a loop the Ambassador cannot close by any amount of giving, because the question underneath it is not <i>have I given enough?</i> \u2014 it is <i>am I loved?</i> \u2014 and giving more is not the answer to the second question. It has never been the answer. It cannot be. No accumulated account of service, however long, can answer a question about inherent worth.",
    "The cross is the answer. Not in the abstract \u2014 specifically and personally. Jesus Christ, who on the night of his betrayal did not withdraw his love from the man he knew was about to betray him \u2014 who washed Judas's feet alongside the other disciples, who gave him bread, who called him friend in Gethsemane \u2014 went to the cross to absorb the worst possible version of the thing you most fear: to give everything and be abandoned anyway. He was abandoned. He bore the abandonment so that the words <i>I will never leave you nor forsake you</i> could be spoken to you without qualification. Galatians 4:7 is the answer to the Ambassador's question, stated with breathtaking economy: <i>so you are no longer a slave, but a son, and if a son, then an heir through God.</i> An heir does not earn the inheritance. An heir receives it, simply by virtue of being in the family. This is what you are.",
    "Before we move forward, use the table below. Not to analyze, not to assign blame, but simply to observe what your own recent experience has been. Use the last few weeks. The Ambassador has a long memory; keep it short and honest.",
]

QUESTION_TABLE_INTRO = (
    "Use the table below. In the first column, name a recent event in which the "
    "disconnection signal fired. In the second, write what you did in response \u2014 "
    "how did the Ambassador move to restore the warmth? In the third, write the "
    "gospel word that speaks to what you actually needed: <i>the hesed of the Father, "
    "given in Christ, held steady by a covenant you did not make and cannot break.</i>"
)

AMB_BODY_P1 = [
    "You have built something. You did not sit down one morning and draw the plans. Most Ambassadors never do. It assembled itself over years, one small decision at a time, in response to circumstances that rewarded warmth and revealed the cost of going cold. Over time you became very good at it, and it became so natural that it stopped feeling like a strategy at all \u2014 it simply felt like who you are. We are going to call it, throughout this walkthrough, <b>the Ambassador</b>.",
    "The Ambassador's governing conviction is one that sounds, at first, like virtue: <i>if I am warm enough, present enough, giving enough, the people I love will stay.</i> The Ambassador does not experience love as a stable floor beneath the feet but as something closer to a temperature that must be actively maintained. If the Ambassador is attentive and generous, the temperature stays up. If the Ambassador stops giving \u2014 gets tired, goes quiet, has a need of his own that requires the attention he usually gives away \u2014 the temperature threatens to drop. And dropping feels dangerous in a way that is difficult to fully explain to people who are wired differently.",
    "The Ambassador is not a manipulator. The warmth is real; the generosity is genuine. Scripture commends this kind of attending care: <i>a soft answer turns away wrath, but a harsh word stirs up anger</i> (Proverbs 15:1), and you have known this in your bones long before you found it on a page. But underneath the genuine warmth is a strategy put in place long before you had words for it: <i>if I am the most caring person in the room, I will not be left behind.</i> For most Ambassadors, one of several recognizable histories: love in your household was real but not guaranteed \u2014 warm when things went well, cooler when they did not \u2014 and you discovered as a child that your behavior seemed to influence which version you received. If you were helpful, the warmth returned. If you were needy, it receded. Whatever the form, the lesson lodged: <i>love must be maintained through service. Being the most loving person in the relationship is not just generosity. It is safety.</i>",
]

AMB_BODY_P2 = [
    "Let me name what that lesson has cost you. The Ambassador, over years, has developed an almost complete inability to distinguish between serving and surviving. You give to people you love, and you give when you are tired and when what you most need is for someone to notice that you are tired and bring something to <i>you</i>. You keep giving because stopping feels dangerous, because the equation learned in childhood has never quite been revised: the way to be loved is to be the one who loves. J. C. Ryle, writing on self-deception in the Christian life, observed that the soul is capable of performing entirely righteous-looking acts from deeply self-protective motives \u2014 that the difficulty is not with the behavior itself but with the root from which it grows. The Ambassador's giving looks like love \u2014 and much of it is love \u2014 but woven into the root is a question that love alone cannot answer: <i>will it be returned? And if I stop giving, will anything be left?</i>",
    "<b>The Ambassador is not your enemy.</b> He is a younger version of you who learned, in real circumstances, that warmth was the price of connection and that withdrawing the warmth meant risking the connection. He has been faithful, in his way, for a very long time. He has kept you in relationship. He has kept the rooms you inhabit at a temperature where human beings can live together. He deserves your gratitude and your compassion. But he has been running the emotional economy of your life on a model that cannot finally balance: giving out more than is coming in, keeping the shortfall off the books, trusting that generosity alone will eventually answer the question that generosity cannot answer.",
]

AMB_BODY_P3 = [
    "What does it look like to begin retiring him \u2014 not eliminating the warmth, which is real and good and wanted in the world, but beginning to disentangle the giving from the earning; beginning to serve from a place of security rather than from a place of need? The work begins with naming the assumption the Ambassador has been operating under: <i>my worth in this relationship is proportional to my usefulness to it. I am safest when I am giving. If I stop giving, the love stops coming.</i>",
    "This assumption is not merely emotionally expensive. When you look at it in the light of the gospel, it is a quiet and practical rejection of grace. It says: <i>I must earn my place.</i> But the gospel says your place was given to you, at incalculable cost, before you did anything to merit it. The Ambassador has believed this with his mind for a long time. He has not yet believed it at the level where the giving happens. That is the work of this walkthrough.",
    "The exercise below is different from the one in some other walkthroughs. I am not asking you to write to the Ambassador. I am asking you to let the Ambassador write to you \u2014 to hear, in the Ambassador's own voice, what he has been doing and why, and what he is afraid would happen if he stopped. He has never had this conversation. He has been too busy caring for everyone else to have it.",
]

AMB_LETTER_INSTRUCTION = (
    "The letter below is written in the Ambassador's voice \u2014 from him, to you. Read it slowly. "
    "He is not villainous. He is exhausted, and he is frightened, and he has something to tell you "
    "that he has never told anyone. Read it twice. Then answer the three prompts that follow."
)

AMB_LETTER_BODY = """
<i>Dear [your name],

I want to say something I have never quite said before, because I have never stopped moving long enough to say it. I have been doing all of this for love. I need you to know that. The warmth I give is real warmth, not theater. The care is genuine.

But I have also been frightened. For as long as I can remember, I have operated under a quiet conviction that the love I am given is, in some essential way, a function of what I contribute to the relationship. Not because anyone told me this explicitly. But I learned it from the way warmth returned when I was helpful and receded when I was not. And so I kept giving. Generously, genuinely, persistently. And part of me \u2014 the part I have never quite admitted \u2014 kept watching to see whether the giving was working. Whether the love was holding. Whether I was still safe.

What I am frightened of, if I am honest, is this: that if I stop giving, I will find out what I have always feared. That the love was for the warmth I produced, not for me. That without the service, without the attentiveness, the room would eventually empty.

I am telling you this because I think it is a lie. But I have not been able to stop believing it on my own. I need you to receive a love that was decided for you before you ever gave anything \u2014 and then give from inside that love, rather than in pursuit of it. I am more tired than you know. And more lonely. I have been giving to people who are too close to the fire to notice that I have been cold.

I am ready to work fewer hours. Are you ready to let me?

\u2014 The Ambassador</i>"""

AMB_LETTER_PROMPTS = [
    "What part of the Ambassador's letter surprised you? Not the part you expected \u2014 the part you were not quite ready to hear.",
    "The Ambassador says he has been watching to see whether the giving is working. In one specific relationship or season of your life, what were you watching for? What would have told you that the love was holding?",
    "What would the Ambassador need to believe \u2014 not just affirm, but actually believe, at the level where the giving happens \u2014 in order to give without watching? What would have to shift in how he understands his own lovability?",
]

PLEA_BODY_P1 = [
    "Every mechanism has a place it breaks \u2014 a pressure point at which the strategy stops working and something else takes over. For most of the six profiles, the breakdown represents a departure from the mechanism: the Architect, whose method is careful planning, shifts into the Attorney's courtroom; the Island, whose method is self-containment, suddenly floods or pursues. The breakdown is recognizable as a change of gear.",
    "For the Ambassador, the breakdown is different in kind from the others. It is not a change of gear. <b>It is an acceleration in the same gear.</b> The Ambassador's breakdown is called <b>the Plea</b>, and you may have already recognized it, because the Plea looks, from the outside, like the Ambassador simply trying harder. The same strategies, at a higher register. The same warmth, now edged with desperation. The same giving, now faster, more, again.",
    "Here is how it unfolds. The Ambassador has been serving and attending and managing the warmth with real care. And then something happens that the management cannot hold. A gap opens that is larger than the usual small ones. A spouse does not merely go quiet for an evening but seems, over several days, genuinely distant. A friendship goes cool in a way that feels less like weather and more like a decision. A family member says something, in a moment of conflict, that lands not as a misunderstanding but as a verdict: <i>you are the problem here.</i> The Ambassador tries what the Ambassador always tries: warm up, give more, smooth it over, close the gap. And for the first time in a long time, it does not work. So the Ambassador does more \u2014 apologizes, asks again whether everything is okay, cancels plans to be available, checks in again in the morning. Because the question underneath all of this \u2014 <i>am I lovable?</i> \u2014 has become audible, and the only answer the Ambassador has ever known is the same answer he has always sought: more service, more warmth, more giving. The volume is up. The strategy is unchanged.",
]

PLEA_BODY_P2 = [
    "I want to describe what this looks like from the inside, because from the inside it does not feel like breakdown. It feels like faithfulness. It feels like love taking its responsibilities seriously. The Ambassador in Plea mode is not aware of having crossed a line; he is aware of trying very hard to repair something important. The apologies feel genuine. The extra effort feels like care. It is only from a slight distance \u2014 and only in retrospect \u2014 that the frantic quality becomes visible.",
    "From the outside, the people who love you experience something more complicated. They feel the weight of your pursuit. Even when they receive the care with gratitude, there is a pressure in it during these seasons that is different from the ordinary warmth of your presence. The difference is not the content of what you offer. It is the urgency beneath it. When the Ambassador is in Plea mode, every act of service carries a silent question: <i>is this enough? Are we okay now?</i> And the person on the receiving end feels that question even if they cannot name it. It is exhausting to be the answer to someone's question about their own lovability.",
    "There is a further cost that takes longer to appear. The Ambassador who doubles down \u2014 who apologizes for things he did not do, yields on matters he was right about, cancels his own plans to close the gap \u2014 does not discharge those false concessions. He files them. Not consciously, not maliciously, but the ledger opens, and every false apology is a deposit. Some months later, when the resentment surfaces, the Ambassador will be confused by its size, because he forgot that every false giving was a cost never honestly acknowledged. <b>The Plea costs you not only the peace you sacrificed to close the gap. It costs you the self that knows the difference between genuine love and relational survival \u2014 and learns, slowly, not to trust that self.</b>",
    "The theological problem the Plea presents is specifically evangelical, in the original sense of that word. Paul, writing to the churches in Galatia that had begun adding works to the gospel, asked with surgical precision: <i>Having begun by the Spirit, are you now being perfected by the flesh?</i> (Galatians 3:3) The argument he was addressing was not abandonment of Christ but supplement to Christ \u2014 adding human effort to what grace had already accomplished, as though grace were insufficient. The Ambassador+Plea is doing the same thing in the grammar of relationship. Having received the love of God as grace, understanding doctrinally that this love is unconditional, the Ambassador turns around and tries to maintain the love of the people closest to them through additional service. Having begun by the Spirit, trying now to be perfected by the flesh. The same error. The same exhaustion.",
]

PLEA_BODY_P3 = [
    "Martin Luther, in the first of the ninety-five theses, wrote: <i>When our Lord and Master Jesus Christ said 'Repent,' he willed that the entire life of believers be one of repentance.</i> Luther was not calling for endless remorse but for the orientation of a whole life toward truth — a daily, honest reckoning that does not perform contrition but practices it. The Plea offers repentance cheaply — not because the Ambassador has reckoned with what was actually wrong, but because the gap is painful and the apology closes it fastest. This is a performance of repentance in the service of self-protection, not repentance at all.",
    "Bonhoeffer's cheap grace — the grace that excuses without confronting, that says <i>peace, peace</i> where there is no peace — has a relational equivalent: cheap reconciliation. The Plea produces cheap reconciliation: surface warmth restored without the truth-telling that genuine restoration requires. It closes the gap, yes. But over something unresolved. And the unresolved thing waits.",
    "Jesus, in Matthew 5:9, calls the peacemakers blessed — not the peacekeepers. A peacekeeper avoids conflict to preserve a surface. A peacemaker enters conflict to produce something genuine. The peacekeeper's goal is the absence of friction. The peacemaker's goal is truth and love together, even when that requires a season of discomfort the Plea cannot tolerate. What you need — and what the people you love need from you — is not faster repair. It is slower, more honest repair. The repair that says: <i>I need to understand what actually happened before I apologize, because I want the apology to be true.</i>",
    "<b>This is the unique pastoral word this profile most needs and least often receives.</b> The Ambassador+Plea is, functionally, trying to atone for their relationships through additional service. More giving, more apology, more presence, more sacrifice — offered to close the gap between themselves and the people they love. But atonement by works is precisely what the gospel does not allow. The cross is not a down payment on a transaction the believer must complete. It is the transaction, completed, full, requiring nothing to be added. The freedom the gospel offers you is not freedom from giving — giving is your particular grace. It is freedom from <i>earning</i>. You do not need to atone for your relationships. Christ has already made that peace. Your job is to receive it and live from inside it.",
]

PLEA_PROMPTS = [
    "Name the last time the Plea ran. Not necessarily out loud \u2014 perhaps only in the messages you sent, or the plans you cancelled, or the apologies you offered before you had determined whether they were warranted. What had the gap been, and how did you respond to it?",
    "The Plea apologizes for things not yet clearly identified as wrong, gives more than was asked for, checks in more than necessary. In a specific recent season, what did you offer that you were not entirely sure was yours to offer? What did you yield that, in a quieter moment, you knew you should have held?",
]

TWO_TOG_BODY = [
    "Now we stand back and look at both of them together, because the Ambassador and the Plea are not two separate problems. For most profiles, the mechanism and the breakdown stand in contrast \u2014 the strategy and the collapse of the strategy. For this profile, they stand in continuity. <b>The Plea is the Ambassador at full volume.</b> The mechanism is what your love does when the temperature is manageable. The Plea is what your love does when the temperature becomes threatening. The tools are the same. The urgency is different. The fear underneath them is identical.",
    "The pattern, laid out slowly, looks like this. <b>(1)</b> The Ambassador moves through ordinary life giving warmth and service \u2014 genuine character, and the only strategy the Ambassador has ever known for keeping love safe. <b>(2)</b> A disconnection occurs \u2014 a withdrawal the management did not prevent. <b>(3)</b> The trigger fires. <b>(4)</b> The core question wakes up: <i>am I lovable? Did I do something? Am I losing them?</i> <b>(5)</b> The Ambassador responds by giving more. This has worked before. <b>(6)</b> It does not work this time. The gap stays open. <b>(7)</b> The Ambassador doubles down \u2014 apologizes, checks in again, cancels plans, offers concessions, tries to close the gap at any cost. <b>(8)</b> The gap closes. The question quiets. But the ledger is not empty, and the next trigger arrives a little faster, because the Ambassador has learned, one more time, that doubling down is what closing gaps requires.",
    "What breaks this loop is not a more sophisticated version of the same strategy. What breaks it is a different answer to the question, received at the level of the body and not only affirmed at the level of the mind. Until the Ambassador genuinely receives \u2014 in the <i>hesed</i>-sense, the covenant-sense, the <i>nothing can separate me from this love</i> sense \u2014 that he is already loved without condition, the loop has nothing to run against. With that answer received and practiced, the Ambassador begins to give from a different place: not to earn, but to share what he himself has been given. The Plea begins, slowly, to lose its urgency. Not because connections matter less, but because they no longer carry the weight of proving that love is possible.",
    "Below is your sequence. Fill in the blanks. Then read it aloud. Both the Ambassador and the Plea lose some of their power when the loop is named clearly.",
]

TWO_TOG_TEMPLATE = (
    "When I experience ____________________, something in me reads it as disconnection, "
    "and the old question wakes up: <i>am I lovable? did I do something wrong?</i> My first move is "
    "to ____________________, because the Ambassador in me believes that if I can "
    "____________________, the warmth will return and I will be safe. When that does not "
    "work quickly enough, the Plea takes over and I find myself ____________________. "
    "What I am actually after, underneath all of it, is the word ____________________\u00a0\u2014 "
    "the word that Christ has already spoken over me in ____________________, "
    "and which I do not need to earn by any additional service."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of practices, each simple enough to carry and honest enough to use. None of them will rewire the pattern in a single application. All of them, practiced with patience over months, will loosen the grip of the loop you just named.",
    "I have divided them into two sets. The first is for the Ambassador when the mechanism is overworking \u2014 when service has tipped from love into survival, when the giving is more about managing the connection than about genuinely caring for the person. The second is for the Plea \u2014 for the moment when the gap has opened and the urgency is already running. Both sets are needed, because the Plea cannot be addressed usefully until the mechanism beneath it is understood.",
]

AMB_TOOLS = [
    ("The honest inventory", "Once a week, ask one question honestly: <i>in the past seven days, was there anything I gave primarily in order to keep love coming, rather than simply because I loved?</i> Do not scold yourself for what you find. Simply name it. The Ambassador loses some of its automatic power when it is required, once a week, to account for its own motives out loud."),
    ("The gift received", "Each day, practice receiving something from someone without immediately returning it. A compliment. An offer of help. A text that says you are being thought of. Let it land, without deflecting, without qualifying, without turning the attention back to them. The Ambassador is practiced at giving and genuinely unpracticed at receiving. Receiving is not passivity. For the Ambassador, it is the discipline most directly opposed to the wound."),
    ("The handed-back prayer", "Each evening, name one thing you gave today that you secretly watched to see whether it was noticed. Then say, aloud or in writing: <i>Lord, I hand this entry back to you. The account is yours to keep. I am not the treasurer of this relationship.</i> The Ambassador has been keeping the books on God's behalf for a very long time. This is the daily practice of returning them."),
    ("The Abba practice", "Once a day, before you have done anything for anyone, sit for five minutes and say: <i>Father, I am your child. Not your employee. Not your contractor. Your child. I am loved before I have given anything today.</i> The Ambassador begins his day in service. This establishes the right order: loved first. Service from that place, not toward it."),
    ("Ask one real need", "Once a week, name one genuine relational need and express it to someone directly, without framing it as concern for them, without qualifying it as fine if they cannot meet it. The question <i>am I lovable?</i> cannot be answered while the Ambassador is managing the answer by making himself indispensable. Asking a need, plainly, is the first act of letting someone love you without earning it."),
]

PLEA_TOOLS = [
    ("The twenty-four-hour rule", "When the gap opens and the Plea rises \u2014 when you feel the urgent need to apologize, to check in again, to close the distance at any price \u2014 give it twenty-four hours before you act on the urgency. Not to be cold. Not to deny that the gap is real. But to give yourself enough time to ask the question the Plea always bypasses: <i>what am I actually sorry for, and what am I offering wholesale because the gap is painful?</i> An apology delivered after honest discernment is worth twenty delivered in the panic."),
    ("Ask before you apologize", "Before apologizing, ask one question silently: <i>am I apologizing because I was genuinely wrong, or because the distance is unbearable?</i> If the honest answer is the latter, do not apologize. Name the discomfort instead: <i>I am feeling the gap between us, and it is hard for me. I want to work through this. But I need to understand it before I respond to it.</i> For this profile, the discipline of not apologizing for things you did not do is among the most countercultural and most freeing practices available."),
    ("Name the gap without closing it", "Practice saying to the person across from you: <i>I can feel the distance between us right now, and that is uncomfortable. But I want what comes next to be real. Can we take a little time?</i> This sentence acknowledges the gap without immediately filling it with service. It is honest about your experience without sacrificing your truthfulness to the urgency of closing the space."),
    ("The Galatians 3 question", "When the Plea is loudest \u2014 when the instinct is to give more, apologize more, pursue more \u2014 ask yourself: <i>Having begun by the Spirit, am I now trying to be perfected by the flesh?</i> (Galatians 3:3) The love you are trying to secure through additional service was given to you before you gave anything. The Plea is trying to earn what grace has already settled. Naming this, in Scriptural language, in the moment it is happening, is not theological head work. It is the interruption of a loop that has run for years."),
    ("Tell one witness", "Within twenty-four hours of a significant Plea episode, tell one trusted person \u2014 your spouse, a close friend, an elder \u2014 one sentence: <i>I felt the gap, and I started running, and I gave more than I should have without stopping to ask whether it was true.</i> The Ambassador's pattern lives in the secrecy of a warmth that never admits its own cost. Spoken aloud to a safe witness, the loop loses its grip more quickly than any other intervention."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Ambassador in me, and you do not despise him. You know why he was built, and what it cost him to keep me in relationship for this long. Thank you for your patience with him.",
    "But Father, he is tired. Underneath the giving has always been a question I was trying to answer by my own effort: <i>am I lovable? Will anyone stay?</i> I have been trying to earn through service the security you have already given me in Christ. Having begun by the Spirit, I keep returning to the flesh. Teach me to receive. When the disconnection fires, let me hear your answer first: <i>You are my child. My love does not depend on what you do next.</i>",
    "Lord Jesus, when the Plea rises \u2014 when I find myself apologizing for things I did not do, checking in again, doubling down \u2014 interrupt me with Galatians 3:3: <i>Having begun by the Spirit, are you now being perfected by the flesh?</i> You have already made the peace I keep trying to make. You absorbed the abandonment I fear. Help me to live from that finished place.",
    "In the name of the One who, having loved his own, loved them to the end \u2014 completely, finally, needing nothing in return \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning. The Ambassador and the Plea have been with you for a long time, and a single reading will not retire them. What follows is a short list of next steps for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different sections will land differently. The Ambassador will want to process it once efficiently and move on. Read it again anyway \u2014 the Plea will have fired at least three more times, and you will have more material to work with."),
    ("Take one tool, not six.", "Choose a single practice from Section 7 and use it for two weeks before adding another. The Ambassador will want to implement everything at once because efficiency in self-improvement is itself a form of the mechanism. One practice, held honestly for long enough, begins to change the shape of the soul."),
    ("Tell one person what you found.", "One honest sentence: <i>My pattern is the Ambassador, and when the connection feels threatened I double down \u2014 I apologize for things I did not do, I give more than was asked, I try to earn with service what I already have in grace.</i> Speaking it aloud to a trusted witness is the first act of living outside it."),
    ("Read further on the love that frees.", "Tim Keller, <i>The Prodigal God</i> \u2014 his reading of the elder brother in Luke 15 names the self-righteousness that quietly attaches to faithful service. C. S. Lewis, <i>The Four Loves</i> \u2014 especially his chapter on need-love and gift-love. And Keller, <i>Walking with God through Pain and Suffering</i> \u2014 the larger frame, and the God who is large enough to hold it."),
    ("If you are stuck, ask for help.", "You are the person who helps. Asking someone to do that for you is not weakness \u2014 for this profile, it is an act of faith. A small rehearsal of the truth that you are allowed to need, and that the need will not cost you the love you are afraid of losing."),
]

GOING_FURTHER_CLOSING = (
    "You are not an employee whose value is determined by your last shift. You are a son or daughter "
    "being loved into freedom by a Father whose love was settled before you gave anything, who keeps "
    "no record of what you owe, and who is more interested in your rest than your productivity. "
    "Go gently with yourself. The One who began this good work in you will be the one to finish it. "
    "You do not have to earn that either."
)


def _three_column_table(rows=7):
    """Three-column journal table for Section 3 \u2014 Ambassador+Plea version."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE MOMENT", header_style), Paragraph("when the signal fired", sub_style)],
        [Paragraph("WHAT THE AMBASSADOR DID", header_style), Paragraph("how I moved to restore warmth", sub_style)],
        [Paragraph("THE GOSPEL WORD", header_style), Paragraph("the love I already have", sub_style)],
    ]
    data = [header_row] + [["", "", ""] for _ in range(rows)]
    tbl = Table(data, colWidths=[col_w]*3, rowHeights=[0.55*inch] + [0.5*inch]*rows)
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
    """Generate the Ambassador + Plea walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='AMB', primary_breakdown='PLEA',
    primary_trigger='DISC', core_question='LOV'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="AMBASSADOR  \u00b7  PLEA",
        title="Take 139 Walkthrough \u2014 Ambassador + Plea",
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
    story.append(Paragraph("The Ambassador \u00a0\u00b7\u00a0 The Plea", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disconnection \u00a0\u00b7\u00a0 Core Question: Am I lovable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cHaving begun by the Spirit, are you now being perfected by the flesh?\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Galatians 3:3",
        ParagraphStyle("cqa", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 1: Opening \u2500\u2500
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read this slowly. The chapter that follows has been a long time in the writing.")
    for p in OPENING_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 2: Trigger \u2500\u2500
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TRIGGER",
                   "Disconnection.",
                   "The moment the warmth disappears, and what your soul makes of it.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will manage the question; your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 14))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 3: Core Question \u2500\u2500
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I lovable?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "The love that does not fluctuate.",
                   "What the hesed of God actually says, and the honest rub of receiving it.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "The moment. The management. The gospel word.")
    story.append(Paragraph(QUESTION_TABLE_INTRO, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table())
    story.append(PageBreak())

    # \u2500\u2500 SECTION 4: Mechanism \u2500\u2500
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Ambassador.",
                   "The caretaker. The peacemaker. The one who manages the temperature of every room.")
    for p in AMB_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "What the giving has cost.",
                   "Serving and surviving, and the slow economy that cannot balance.")
    for p in AMB_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in AMB_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Ambassador.",
                   "Read it twice. He has been faithful; let him speak.")

    letter_style = ParagraphStyle(
        "AmbLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    story.append(Paragraph(AMB_LETTER_INSTRUCTION, S["BodyJ"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(AMB_LETTER_BODY, letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in AMB_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 5: Breakdown \u2500\u2500
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Plea.",
                   "The same strategy, at full volume. The double-down that looks like love.")
    for p in PLEA_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "Having begun by the Spirit.",
                   "What the Plea looks like from the inside, and what it costs.")
    for p in PLEA_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in PLEA_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "The double-down.",
                   "Two questions to sit with before you turn the page.")
    for prompt in PLEA_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same fear, at two volumes.",
                   "The Ambassador and the Plea are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 6))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=6)
    story.append(PageBreak())

    # \u2500\u2500 SECTION 7: Tools \u2500\u2500
    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "When the Ambassador is overworking.",
                   "Five practices for the time before the alarm fires.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    for name, desc in AMB_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Plea is running.",
                   "Six practices for the moment the urgency rises and the doubling-down begins.")
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

    # \u2500\u2500 SECTION 9: Going Further \u2500\u2500
    section_header(story, S, "SECTION NINE  \u00b7  GOING FURTHER",
                   "Where to go from here.",
                   "This walkthrough is a beginning, not an ending.")
    for name, desc in GOING_FURTHER_ITEMS:
        story.append(KeepTogether([
            Paragraph(name, S["H3"]),
            Paragraph(desc, S["BodyJ"]),
        ]))
    divider(story)
    story.append(KeepTogether([Paragraph(GOING_FURTHER_CLOSING, S["BlockQuote"])]))

    doc.build(story)
    return finalize_buffer(buf)


# \u2500\u2500 STANDALONE TEST \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "AMB"
        primary_breakdown = "PLEA"
        primary_trigger = "DISC"
        core_question = "LOV"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "ambassador_plea_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages using pypdf
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

    print(f"DONE: ambassador_plea.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
