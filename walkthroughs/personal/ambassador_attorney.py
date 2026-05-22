"""Personal Walkthrough — Ambassador + Attorney.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disconnection trigger, "Am I lovable?" core question.
~25 pages, 9 sections.

Calibration anchor: same Attorney breakdown as ARCH+ATTY and ISLE+ATTY,
now carried by the Ambassador mechanism — the most painful version of this
breakdown because it overturns a lifetime of visible self-presentation.
The Ambassador has spent years being the warm one, the giver, the one who
manages the emotional temperature. When wounded enough, the Ambassador
produces an evidence binder no one knew was being kept: "I did this for you,
and this, and this, and this, and you never noticed."

Spiritual problem named in Section Five: the ledger of love — the Ambassador
has been keeping a record of giving while believing they were keeping none,
and this is the seed of bitterness Hebrews 12:15 warns about.
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
    "Before you read any further, I want to do for you what a good counselor does in the first session — lower the lights and slow the pace — because what you are about to look at is not a catalogue of your gifts, though you have real ones, and it is not a rebuke of the way you have loved people, though there is something in it that must be named. It is a patient conversation about the way your soul has learned to keep itself safe in a world that has not always loved you in return.",
    "You have, in all likelihood, been the one who kept the peace in most of the rooms you have entered. You were the one who noticed when someone was left out and went to find them. You were the one who remembered birthdays, who asked the follow-up question, who tracked how everyone was doing and made the phone call before anyone else thought to. People have probably told you that they feel safe around you. That is not nothing. But this walkthrough is going to ask you to look at something underneath that warmth — something that has been moving quietly in the direction opposite to warmth for a long time.",
    "We are going to walk through your trigger — the specific moment your nervous system says something is wrong here. We will listen to the question underneath that moment, one that has probably been with you since you were very small. We will name the strategy you have built in response to that question, and the place that strategy collapses when it cannot hold any longer. And then, only then, will we put tools in your hands.",
    "If you were sitting across from me, I would say this plainly. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father whose love for you is not a function of your usefulness to him; a Son who, on the night he was betrayed, washed the feet of the man who was about to betray him and called him friend; and a Spirit who is, at this very moment, interceding for you with a love that does not require anything from you to sustain it.",
    "So read slowly. When something catches in your throat, do not manage it or redirect it or ask whether someone else in the room is all right. Stay with it. That catch is usually the Lord saying, <i>look here, with me.</i> The goal is a slightly freer life — one in which you give because you are loved, rather than giving in order to discover whether you are.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life have no idea it is occurring — not because they are careless, but because you have become very skilled at not showing it. Your spouse has been quiet all evening. Not cold, not hostile, just absent — far away, somewhere you are not. A friend replies to your message with two words after you wrote three paragraphs. The group moves through a gathering and the warmth you expected is somehow thinner than you needed it to be. Or you have given something — time, attention, an act of service that cost you real effort — and it was received without comment, the way furniture is received, as though it simply belonged in the room.",
    "On the surface, none of these register as catastrophes. You may not show it. Your face may be the same. You may even be the one who then asks how the other person is doing, smooths the moment over, generates warmth to fill the gap. You are good at that. But inside, something has registered. A quiet signal, specific and cold, has fired: <i>the connection is gone.</i>",
    "This is your trigger. The word for it is <b>disconnection</b> — and for you it is not merely the absence of contact but the withdrawal of warmth from someone whose warmth you rely on. For the Ambassador, disconnection does not feel like a neutral condition. It feels like a verdict. The question that rises underneath the trigger is not <i>why are they quiet tonight</i> but something much older: <i>did I do something? Is it me? Am I losing them?</i>",
    "C. S. Lewis, in <i>The Four Loves</i>, observed that there is a kind of love that can become its own vulnerability — that the more we love, the more we expose ourselves to being hurt by the withdrawal of what we love. This is particularly acute for the Ambassador, who has organized much of life around being close to people, being the source of warmth in relationships. When the warmth flows back, everything feels right. When it is absent, the Ambassador experiences it as loss — and what is being lost is not merely comfort but something close to confirmation.",
    "<b>Your sensitivity to disconnection is not an accident.</b> It is the residue of something specific that was learned, usually early, in a household or relationship in which love was inconsistent in its warmth or conditional in its expression. Perhaps closeness came when you were helpful and receded when you were not. Perhaps you learned very early that needs, if expressed too plainly, drove people away — and so you built a self that presented need as service, that turned your own longing into care for others, that kept the love coming by making yourself indispensable.",
    "That early schooling lodged a lesson deep in you: <i>love is something I participate in by giving, not simply by being.</i> Underneath the giving has been a question, quiet and patient and never quite answered, waiting each time to see whether the love you gave will be returned, whether your presence is wanted for its own sake or merely for its usefulness. Before we go further, sit with two questions in writing. Your head will manage this. Your hand will not.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week, that the disconnection signal fired. What happened, in two sentences? You are looking for the moment your internal temperature dropped — not necessarily a dramatic event, but the moment something inside you said <i>the warmth is gone.</i>",
    "How large was the event, and how large was the response inside you? If the response was larger than the event, you have just located your trigger.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding. The Ambassador has been guarding this one for a very long time, and has been guarding it so quietly that most people who know you have never heard it.",
    "Yours is this: <b>Am I lovable?</b>",
    "It is not the same as <i>Am I loved?</i> — you have received love, you know you have, and yet the question does not go away. The question is more specific and more frightening: <i>Am I the kind of person who is loved for what I am, rather than for what I do?</i> If I stopped serving, stopped warming, stopped being useful and available and attentive — would anyone stay?",
    "Most adults prefer to believe they settled this question long ago. They have not. They have only buried it under sufficient activity that it does not speak clearly during the daylight hours. For the Ambassador, the question speaks in the silences — in the spouse's quiet evening, in the friend's short reply, in the gathering that was warmer for others than it was for you. And the nervous system's verdict, in those silences, is not neutral: <i>see? Even after everything you have given, the connection can simply disappear. This is what you suspected all along.</i>",
    "For you, this question carries a particular urgency because you have organized your life around answering it through your behavior. You have been generous. You have been present. You have taken care of people in ways that have cost you real time and real energy. And the hope underneath all that giving — the hope you have perhaps never quite put into words — is that love given consistently enough, warmly enough, sacrificially enough, will eventually produce a love that is stable and sure and not contingent on anything you do next. You have been trying to answer the question <i>am I lovable?</i> by making yourself indispensable.",
]

QUESTION_BODY_P2 = [
    "There is a reason that theologians from Augustine to John Calvin have insisted that the human heart, at its deepest, is not looking for productivity or security or meaning in the ordinary sense — it is looking for a love that holds it permanently. Augustine's words at the opening of his <i>Confessions</i> — <i>our heart is restless until it rests in Thee</i> — are not merely a philosophical observation. They are a map of the soul's truest motion. The longing that drives the Ambassador is a version of this longing. You want to be held. You want to know that someone's love for you is not dependent on your next act of service.",
    "The Psalms understand this longing. Psalm 103, which David wrote out of a life that had tested the question thoroughly, begins with these words: <i>Bless the Lord, O my soul, and all that is within me, bless his holy name! Bless the Lord, O my soul, and forget not all his benefits — who forgives all your iniquity, who heals all your diseases, who redeems your life from the pit, who crowns you with steadfast love and mercy.</i> (Psalm 103:1–4) Notice the word that stands at the center of this passage: <i>steadfast</i>. The Hebrew word is hesed — the covenant love of God, the love that does not depend on the beloved's performance, the love that was decided before you did anything to earn it and that cannot be revoked by anything you fail to do. This is the love the Ambassador's soul is looking for in every room it enters.",
    "The gospel's answer to the question <i>am I lovable?</i> is specific and theologically precise. The answer is not <i>yes, because of who you are</i> — which would be flattery, and God does not traffic in flattery. The answer is not <i>yes, if you continue to serve faithfully</i> — which would be the very treadmill you are already on. The answer is: <i>you are loved not because you are lovable but because you are in Christ — and in him, the love the Father has for his Son flows over to you, without condition and without end.</i> This is what Paul means in Romans 8:15: <i>you did not receive the spirit of slavery to fall back into fear, but you have received the Spirit of adoption as sons, by whom we cry, 'Abba! Father!'</i>",
    "But here is where pastoral honesty demands something of you. The Ambassador hears this and nods. You may even feel it, briefly and warmly, and then set it aside to go check on how everyone else is doing. The gospel answer to <i>am I lovable?</i> is not something the Ambassador easily receives and rests in, because receiving requires stopping, and stopping requires trusting that the room will be all right without you managing it. The hardest thing about this answer, for you specifically, is not the theology. It is the sitting still long enough to let it land.",
]

QUESTION_BODY_P3 = [
    "Here is what the honest work looks like for you. The Ambassador has been trying to earn, through giving, the security that comes only from being given to. This is a loop that cannot be closed by any amount of service, because the question underneath it is not <i>have I given enough?</i> but <i>am I loved?</i> — and giving more is not the answer to the second one.",
    "The cross is. Not in the abstract — specifically and personally. Jesus Christ, who on the night of his betrayal did not withdraw his love from the man he knew was about to betray him, has absorbed the worst possible version of the thing you most fear: to give everything and be abandoned anyway. He went to that place, for you. And from the other side of the empty tomb he says: <i>the love that holds you is not contingent on anything you do next.</i> Galatians 4:7 says it plainly: <i>so you are no longer a slave, but a son, and if a son, then an heir through God.</i> An heir does not earn the inheritance. An heir receives it — simply by being in the family. This is what you are. Not an employee. An heir.",
    "Before we close this section, use the reflection table below. Not to analyze — to observe. Use recent events, not old ones. Your hand will be more honest than your memory.",
]

AMB_BODY_P1 = [
    "You have built something. You did not sit down one day and draw the blueprints. Most Ambassadors do not. It grew from you the way a habit grows — imperceptibly, out of necessity, from small decisions made in response to real situations that rewarded the behavior. But it is a structure now, and we are going to spend this section walking through it together, because the Ambassador is the first mechanism in this series and it deserves a careful introduction.",
    "The <b>Ambassador</b> is a soul who has learned — usually early, usually from a specific set of circumstances — that love is something that must be maintained through service. The Ambassador does not experience love as a stable ground beneath the feet but as something more like a temperature that must be managed. If the Ambassador is attentive enough, warm enough, giving enough, helpful enough, the temperature stays up. If the Ambassador stops giving — gets tired, goes quiet, has a need of their own — the temperature drops, and dropping feels dangerous.",
    "The Ambassador is not a manipulator. The Ambassador gives generously, and the generosity is real. The warmth is not performed — it is felt. The care for other people is genuine. When you ask the person you love how they are doing, you actually want to know. But underneath the genuine warmth is a strategy, put in place long before you had words for it: <i>if I am the most caring person in the room, I will not be left behind.</i>",
    "Where did this come from? For most Ambassadors, one of several specific histories. Perhaps love in your household was genuinely inconsistent — warm some days, withdrawn on others — and you discovered as a child that your behavior seemed to influence which version you got. If you were helpful, the warmth returned. If you were needy, it retreated. And so you became helpful, because helpful was safer than needy. Perhaps there was real pain in your home and you became, without anyone asking you to, the one who managed the emotional temperature — who knew how to read the room before anyone else did, and positioned themselves between the storm and the people who could not weather it.",
    "There is a Proverb that commends this kind of wisdom: <i>A soft answer turns away wrath, but a harsh word stirs up anger.</i> (Proverbs 15:1) The Ambassador has long known this. You learned it in your bones before you could read it off a page. And it is not wrong. The world needs people who can walk into a tense room and, without raising their voice, without shaming anyone, reduce the temperature to something livable. That is a real gift.",
]

AMB_BODY_P2 = [
    "But let me name what the gift has cost you. The Ambassador is a person who has, over years, developed an almost complete inability to distinguish between serving and surviving. You give to people you love, and you give to people you barely know, and you give when you are tired and hurting and when what you most need is for someone to notice that you are tired and hurting and give something to you. And you keep giving, because stopping feels dangerous, and because you learned a long time ago that the way to be loved is to be the one who loves.",
    "J. C. Ryle, writing on the dangers of self-deception in the Christian life, observed that the soul is capable of doing very righteous-looking things for very unrighteous reasons, and that the difficulty is not the behavior itself but the root from which it grows. The Ambassador's giving looks like love — and much of it is love — but at the root is a question that love alone cannot answer: <i>am I loved in return?</i> And the giving has become, partly, a way of trying to force a yes to that question without ever having to ask it out loud.",
    "The people who love you have probably felt something they cannot quite name. They know you are generous. But they may also have a sense — difficult to articulate, almost guilty to admit — that there is something in your giving that is not entirely free. A slight weight to it. A way in which, after you have given a great deal, there is an expectation in the air — not spoken, not demanded, just present — that something will come back. They cannot name this easily, because you have never said it. But the expectation is there, and they feel it, and when they fail to meet it — as they sometimes will, because they are human and tired, as we all are — something happens in you that they usually never see.",
    "<b>The Ambassador is not your enemy.</b> He is a younger version of you who learned, in some real circumstance, that warmth was the price of connection and that stopping the warmth meant risking the connection. He has been faithful. He has kept you in relationship, kept the rooms you inhabit at a temperature where human beings can live together. He deserves your gratitude, not your contempt. But he has been running the emotional budget of your life on an unsustainable model: giving out more than you are taking in, keeping the ledger off the books, hoping that no one will notice the deficit — including yourself.",
]

AMB_BODY_P3 = [
    "What does it look like to begin retiring him, in the dignified sense of the word? Not eliminating the warmth — the warmth is real and good and the world needs it. But beginning to disentangle the giving from the earning; beginning to serve from a place of security rather than from a place of need; beginning to allow yourself to be cared for with the same openness with which you care for others.",
    "It begins with naming the assumption the Ambassador has been operating under: <i>I am safest when I am giving. My worth in this relationship is proportional to my usefulness to it.</i> This assumption is not merely emotionally costly. It is, when examined in the light of the gospel, a quiet but real rejection of grace. It says: <i>I must earn my place.</i> But the gospel says your place was given to you, at great cost, before you did anything to merit it. The Ambassador believes this doctrinally. He has not yet believed it at the level where the giving happens.",
    "The exercise below is different from the one in the Architect and Island walkthroughs. I am not asking you to write to the Ambassador. I am asking you to let the Ambassador write to you — to hear, in the Ambassador's own voice, what he has been doing and why, and what he is afraid would happen if he stopped. The Ambassador has never had this conversation. He has been too busy taking care of everyone else to have it.",
]

AMB_LETTER_INSTRUCTION = [
    "The letter below is written in the Ambassador's voice — from him, to you. He is not villainous. He is exhausted, and he is frightened. Read it slowly. Then answer the three prompts that follow.",
    "Dear [your name],",
    "I want to tell you something I have never told anyone, because I have never let myself sit still long enough to say it. I have been keeping a record.",
    "Not deliberately. Not maliciously. I did not decide one morning to tally the giving. But somewhere in a part of me I did not fully know was operating, I have been keeping count. Of the meals I brought when no one brought any to me. Of the calls I made when no one checked in on how I was doing. Of the effort that went unacknowledged — not unrewarded, exactly, but unnoted, absorbed as though it were simply the ambient condition of my presence.",
    "I kept this record because I did not know how else to track whether my love was landing. Whether I was mattering. I kept it the way you keep a secret — not by locking it somewhere, but simply by never speaking of it. And I told myself it was not a ledger. I told myself I was simply a generous person, that I gave freely, that I kept no record. I have read 1 Corinthians 13. I believed I was living it. What I did not see is that I was keeping a record of my giving while telling myself the book was closed. I was giving on credit and waiting for the account to be settled — feeling the slow burning of an account that never quite closes.",
    "I do not know what it would feel like to give from a place where the account does not matter — where the giving is simply the overflow of a love already given to me without my earning it. I would like to learn. But I cannot learn it as long as I am the one managing everyone else's warmth. I am more tired than you know. And more frightened. And I want more than I have ever admitted to wanting.",
    "The Ambassador",
]

AMB_LETTER_PROMPTS = [
    "What part of the Ambassador's letter surprised you? Not the part you expected — the part you were not quite ready to hear.",
    "The Ambassador says he has been keeping a ledger while telling himself he was keeping none. Name one specific relationship or season of your life where this was true. What was on the ledger?",
    "What would the Ambassador need to believe — really believe, at the level where the giving happens — in order to give without keeping score? What would have to change in how he understands his own lovability?",
]

ATT_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Ambassador, the breaking has a shape that is, among the six breakdowns we track, the most painful and the most theologically instructive — because it overturns, in a moment, a lifetime of self-presentation. This breakdown is called <b>the Attorney</b>.",
    "The setup matters. The Ambassador has been giving — for months, for years, sometimes for decades. The giving has been real. The warmth has been real. The service has cost real time, real energy, real emotional reserves. And because the Ambassador has genuinely not been consciously tracking it, the Ambassador has maintained a sincere and entirely good-faith belief: <i>I give freely. I am not keeping score.</i>",
    "And then something happens. A wound. A moment of disconnection larger than the usual small ones. A partner who not only fails to notice but actually criticizes. A friend who, after years of receiving, simply disappears. A family member who says, in a moment of conflict, <i>you are the problem here.</i> The trigger fires. The question wakes up: <i>am I lovable?</i> The Ambassador tries to do what the Ambassador always does: warm up, smooth over, give more. And for the first time in a long time, it does not work. The wound stays open. And something the Ambassador genuinely did not know was there comes to the surface.",
    "The evidence binder opens. And what comes out is not a thin file. It is a brief that has been assembling, without the Ambassador's conscious knowledge, for a very long time.",
]

ATT_BODY_P2 = [
    "This is what the Ambassador's Attorney sounds like when it arrives. It does not arrive quietly, the way the Island's Attorney arrives. It does not arrive with cold precision, the way the Architect's Attorney arrives. It arrives with heat — the heat of a person who has been quietly absorbing, quietly serving, quietly containing the injury, and who suddenly cannot contain it anymore. The words carry a texture of grief and fury that surprises everyone in the room, including the Ambassador. <i>I did this for you, and this, and this, and this, and you never noticed. I have given and given, and you have no idea what it has cost me, and here you are telling me I am the problem.</i>",
    "What the other person is experiencing is a complete reversal of character. The person who was, an hour ago, asking how they were doing is now presenting, in specific and documented detail, a catalogue of accumulated grievances the other person never knew were being gathered. They had no idea the Ambassador was in pain. They had no idea there was a ledger. The Ambassador had been so consistently warm that there had been no signal that anything was wrong. And now there is a binder on the table, and the other person is utterly disoriented, and the Ambassador is saying things that are, in many cases, completely factually accurate — and still the conversation is not going the way the Ambassador hoped.",
    "Here is what the Attorney is actually after. Not a legal victory. An acknowledgment that makes the question go away: <i>yes, you are lovable. Yes, you have given enough. Yes, we see you.</i> The brief exists not to prosecute but to make them understand the depth of what the Ambassador has given, so that they will finally give back a proportionate love. It is not anger for its own sake. It is grief that has run out of room to be quiet.",
    "But I want to say something carefully, because this is the specific spiritual problem the Ambassador must eventually face. <b>The Ambassador has been keeping a record while believing they were keeping none.</b> This is a kind of self-deception Hebrews 12:15 names with striking precision: <i>See to it that no one fails to obtain the grace of God; that no root of bitterness springs up and causes trouble, and by it many become defiled.</i> The root of bitterness does not announce itself as bitterness. It announces itself as hurt, as exhaustion, as the entirely reasonable sense that you have given more than you have received. But underneath the hurt, the root has been growing — and the Attorney is what happens when it finally breaks the surface.",
]

ATT_BODY_P3 = [
    "Charles Spurgeon, preaching on the parable of the laborers in the vineyard, gave a warning I want to put before you directly: <i>the giver who keeps count is the most dangerous kind of bitter.</i> He is the most dangerous because he believes, sincerely, that he is not bitter at all — that he is simply presenting the evidence of what has been owed and not repaid. The Ambassador's Attorney is not presenting false exhibits. The Ambassador really did all those things. The accounting is accurate. What is wrong is not the facts; it is the assumption behind them — that giving creates an obligation, that love given consistently enough should produce a love that is finally certain and secure.",
    "Paul, in 1 Corinthians 13:5, says that love <i>keeps no record of wrongs</i>. The Ambassador has been keeping no record of wrongs. The record the Ambassador has been keeping is a record of <i>givings</i> — a ledger of generosities offered and not fully reciprocated. This is subtler than what Paul warns against, which is why the Ambassador often misses the warning. The ledger does not feel like bitterness. It feels like a perfectly reasonable accounting. It is only when the Attorney opens it and begins to read aloud that the bitterness in the ledger becomes visible — even to the Ambassador.",
    "The gospel's interruption is not <i>your ledger is wrong.</i> The specific acts of service are real. The specific needs that went unmet are real. The gospel's interruption is this: <b>you already have an Advocate, and he has already presented the only ledger that finally counts.</b> <i>If anyone does sin, we have an advocate with the Father, Jesus Christ the righteous.</i> (1 John 2:1) Christ does not merely plead your case. He closes the account entirely — and the same closing that freed you from condemnation also frees you from the obligation to collect from others. The ledger you have been keeping was never yours to carry. It was put down at the cross. The question, from here, is whether you will hand the brief to the only Advocate qualified to hold it.",
]

ATT_PROMPTS = [
    "Name the last time the Attorney appeared in you — not necessarily out loud, but in the internal brief. What had you been giving, for how long, and what was the wound that finally opened the binder?",
    "The Ambassador has been keeping a record of givings while believing the ledger was closed. What is on your current ledger? Write one or two specific entries — acts of service, sacrifices of time or attention, needs you carried alone — that have never been spoken aloud to the person who received them.",
    "What verdict were you hoping the Attorney's brief would produce? Write it in one sentence beginning: <i>If they could only understand how much I have given, they would finally ___.</i> What does Christ's advocacy make of that sentence?",
]

TWO_TOG_BODY = [
    "Now we place them next to each other, because the Ambassador and the Attorney are not two separate problems. They are the same wound, dressed in two different postures. One posture gives; the other presents the bill. But underneath both is the same person, asking the same question, and still not quite sure of the answer.",
    "<b>The Ambassador is what your need does when it has time.</b> The Attorney is what your need does when the patience runs out. The Ambassador gives generously, warmly, faithfully — managing the emotional temperature, preventing the disconnection from ever becoming large enough to be undeniable. The Attorney emerges when the disconnection becomes undeniable anyway, and the evidence that was never supposed to be gathered must be presented to someone who was supposed to have already seen it.",
    "The pattern, in slow motion, looks like this. <b>(1)</b> The Ambassador moves through the world giving — warmth, service, attention — because giving feels like love, and love feels like safety. <b>(2)</b> A disconnection occurs: someone fails to notice what was given. <b>(3)</b> The trigger fires: <i>the connection is gone.</i> <b>(4)</b> The core question wakes up: <i>am I lovable?</i> <b>(5)</b> The Ambassador responds by giving more, because this has worked before. <b>(6)</b> It does not work this time. The wound stays open. <b>(7)</b> The ledger opens, and the Attorney takes the floor with heat and grief and specific documentation. <b>(8)</b> The acknowledgment that comes, if it comes, feels coerced. The question is not answered. The Ambassador retreats, gives again, and the loop restarts.",
    "What breaks the loop is not more giving, and it is not a more persuasive brief. It is a different answer to the question. Until the Ambassador receives — really receives, not as doctrine but as lived reality — that the love they are looking for has already been given without condition and without ledger, the loop has nothing to run against. With that answer received and practiced, the Ambassador begins to give from a different place: not to earn, but to share what they themselves have been given. Both the Ambassador and the Attorney begin to work shorter hours.",
    "Fill in your sequence below. Read it aloud when you finish. Both the Ambassador and the Attorney lose a measure of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I experience ____________________, something in me reads it as disconnection "
    "and the old question wakes up: <i>am I lovable?</i> My first move is to "
    "____________________, because the Ambassador in me believes that if I can "
    "____________________, the warmth will return and the question will quiet. When that "
    "does not work, the Attorney opens the ledger and argues that ____________________. "
    "What I am actually after, underneath all of it, is the verdict "
    "____________________ \u2014 a verdict Christ has already spoken over me in "
    "____________________, and which I do not need to earn."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of tools, each simple enough to carry and honest enough to use. None of them will fix the Ambassador's pattern in a single application. All of them, practiced over months, will loosen the grip of the loop you just named.",
    "I have divided them into two sets: tools for when the Ambassador is overworking its giving (when service has tipped from love into survival), and tools for when the Attorney is assembling the brief (when the wound is fresh and the ledger has opened). The Ambassador's tools come first, because the Attorney cannot be addressed usefully until the mechanism underneath it is understood.",
]

AMB_TOOLS = [
    ("The honest inventory", "Once a week, ask one question: <i>in the past seven days, was there anything I gave in order to secure love rather than to express it?</i> Do not scold yourself for what you find. Simply name it. The Ambassador loses some of its automatic power when it is required, once a week, to account for its own motives."),
    ("The gift received", "Each day, practice receiving something from someone without immediately giving something back. A compliment. An offer of help. A text that says you are being thought of. Let it land without deflecting, qualifying, or turning the attention back to them. The Ambassador is practiced at giving and unpracticed at receiving. Receiving is where the healing begins."),
    ("The handed-back ledger", "Each evening, name one thing you gave today that you secretly hoped would be noticed. Then say, aloud or in writing: <i>Lord, I hand this entry back to you. The account is yours to keep. I am not the treasurer of this love.</i> The Ambassador has been keeping the ledger on God's behalf. This is the practice of returning it."),
    ("The unexpressed need", "Once a week, name one genuine emotional or relational need and express it to someone directly, without framing it as a concern for them. The question <i>am I lovable?</i> cannot be answered while you are managing the answer by making yourself useful. Asking a need is the first act of letting someone love you without earning it."),
    ("The Abba prayer", "Once a day, before you have done anything for anyone, sit for five minutes and say: <i>Father, I am your child. Not your employee. Your child. I am loved before I have given anything today.</i> The Ambassador serves from morning to night. This establishes the right order: loved first. Service after."),
]

ATT_TOOLS = [
    ("Name the ledger entry aloud", "Within twenty-four hours of the wound registering, tell one trusted person one sentence: <i>I gave something today and it went unnoticed, and I felt the old question wake up.</i> Not to build a case. Simply to break the secrecy before the evidence goes underground. The Ambassador's Attorney does its most damaging work in private. Spoken aloud to a safe witness, the brief loses momentum."),
    ("The thirty-second test", "When you feel the Attorney rising, pause thirty seconds and ask: <i>Am I bringing a wound or delivering a verdict?</i> Bringing a wound is appropriate and necessary. Delivering a verdict — a prosecuted case with documented exhibits — is the Attorney's territory. Know which one is happening before you open your mouth."),
    ("The ledger handed over", "If the brief will not leave you alone, write it out in full — every entry, every unreturned gift of time and attention. Then pray: <i>Lord, this account is yours. I was not designed to collect this debt. I hand these entries to you.</i> Then tear the pages. This is not suppression. It is transfer."),
    ("The one honest sentence", "When you must speak to the person who wounded you, discipline yourself to one sentence that names the specific wound: <i>When that happened, I felt invisible, and I need you to know that.</i> The relationship can sustain a wound expressed honestly. It is less clear it can sustain a full prosecution."),
    ("The advocate prayer", "When the Attorney is loudest, pray these words: <i>Lord Jesus, you are my Advocate. You have seen every entry on this ledger, and you have already settled the account that could not be settled. I do not need to collect this debt.</i> Say it slowly. The third time, the courtroom usually begins to quiet."),
    ("The proportionality audit", "Before delivering the brief to the other person, ask: <i>If this wound had happened last week, would I be bringing this much?</i> If the answer is no, you are not bringing a fresh wound. You are delivering an accumulated case. The other person may need to hear the wound. They do not need the full audit."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Ambassador in me, and you do not despise him. You know what he was built for. You know the specific households, the specific moments in which he learned that the surest path to love was to make himself impossible to leave behind. Thank you that he has kept me connected, kept me warm, kept the people I love in relationship with me. He has not been wrong about everything.",
    "But he is tired, and the ledger is heavier than I have admitted, and I have been keeping a record while telling myself the book was closed. Teach me to hand it back. Teach me what it feels like to give from a place that is not earning but overflowing — to serve because I am already secure rather than serving in order to become secure. When the disconnection fires and the old question wakes up — <i>am I lovable?</i> — would you let me hear your answer before I hear the Ambassador's? <i>You are my child. My love for you is not contingent on what you do next.</i> Let that land somewhere below the doctrine.",
    "Lord Jesus, when the Attorney rises — when the heat of the ledger breaks the surface and I want to read the account aloud to the person who did not notice — remind me that you have already settled the account that stood against me. The same grace that forgave my debt releases me from the obligation to collect from others. The ledger was never mine to keep. Help me to live from that freedom, one day at a time, until the Ambassador learns to give without counting.",
    "In the name of the One who, on the night of his betrayal, gave bread to the hands that were about to hand him over — who loved freely to the end, from a place so secure that nothing could make him keep score — I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Ambassador and the Attorney have been with you a long time, and one afternoon's reading will not retire them. What follows is a short list of next steps — some immediate, some long — for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different sections will land differently. The Ambassador will resist a second reading — he prefers to receive information once, file it, and then go check on someone else. Read it again anyway."),
    ("Take one tool, not six.", "Choose a single practice from Section 7 and try it for two weeks before adding another. The tools are postures, not a program. One posture, held for long enough, begins to change the shape of the soul."),
    ("Tell one person what you found.", "Not the whole document. One sentence: <i>I learned that my mechanism is the Ambassador, and my breakdown is the Attorney, and I have been keeping a ledger I did not know I was keeping.</i> The Ambassador's pattern lives in secrecy. Speaking it to a trusted witness is the first act of living outside the management."),
    ("Sit with 1 Corinthians 13 again, slowly.", "Read it once through and notice what it says about keeping records. Then read it again and ask: <i>where am I doing the opposite of what love here says?</i> Not to condemn yourself — Paul was writing to a church that was failing at all of it. But to let the text do what it was meant to do."),
    ("Read further on the love that frees.", "Tim Keller, <i>The Prodigal God</i> — his reading of the elder brother in Luke 15 will name the specific self-righteousness that attaches to the Ambassador's giving. C. S. Lewis, <i>The Four Loves</i> — especially his chapter on affection and the ways in which affectionate love, when it becomes need, begins to demand rather than give."),
    ("If you are stuck, ask for help.", "For the Ambassador specifically, asking for help is one of the most countercultural things this walkthrough can recommend. You are the one who helps others. Asking someone to help you is, for you, an act of faith."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom by a Father "
    "who has not, in all the years you have been giving, kept any record of what you owe him. "
    "His love for you is not a transaction. It is a gift, given before you could earn it, "
    "held open after everything you have done to deserve its withdrawal. "
    "Go gently with yourself. The One who began the good work in you will be the one who finishes it."
)


def _three_column_table(rows=7):
    """Three-column journal table for Section 3's reflection exercise."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE EVENT", header_style), Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WAS I LOVED HERE?", header_style), Paragraph("what your nervous system concluded", sub_style)],
        [Paragraph("WAS MY SOUL IN DANGER?", header_style), Paragraph("the deeper question", sub_style)],
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
    """Generate the Ambassador+Attorney walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='AMB', primary_breakdown='ATTY',
    primary_trigger='DISC', core_question='LOV'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor's Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR'S WALKTHROUGH",
        cover_right_label="AMBASSADOR  \u00b7  ATTORNEY",
        title="Take 139 Walkthrough \u2014 Ambassador + Attorney",
    )

    story = []

    # ── COVER ──
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor's<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the way<br/>you have learned to keep yourself safe.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph("The Ambassador &nbsp;\u00b7&nbsp; The Attorney", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disconnection &nbsp;\u00b7&nbsp; Core Question: Am I lovable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cWe are not the sum of our weaknesses and failures;&nbsp;\u2014&nbsp;<br/>"
        "we are the sum of the Father\u2019s love for us<br/>"
        "and our real capacity to become the image of his Son.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Tim Keller, <i>The Prodigal God</i>",
        ParagraphStyle("cqa", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: Opening ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read this slowly. The chapter that follows has been a long time in the writing.")
    for p in OPENING_BODY:
        story.append(Paragraph(p, S["BodyJ"]))

    # ── SECTION 2: Trigger ──
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
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 3: Core Question ──
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I lovable?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "The love that does not fluctuate.",
                   "What Scripture actually says, and the honest rub of receiving it.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "Where was I actually unloved? Where was my soul in danger?")
    story.append(Paragraph(
        "Use the table below. In the first column, name a recent event in which the "
        "disconnection signal fired. In the second, write what your nervous system concluded: "
        "<i>was I loved here?</i> In the third, answer the deeper question: "
        "<i>was the part of me that finally matters \u2014 my soul, my standing before "
        "God \u2014 at any point in danger?</i>",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table())
    story.append(PageBreak())

    # ── SECTION 4: Mechanism ──
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Ambassador.",
                   "The caretaker. The peace-maker. The one who manages the temperature of every room.")
    for p in AMB_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "What the giving has cost.",
                   "Serving and surviving, and the slow unsustainable model underneath them.")
    for p in AMB_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in AMB_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Ambassador.",
                   "Read the Ambassador's own words. He has been faithful; let him speak.")

    letter_style = ParagraphStyle(
        "AmbLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for line in AMB_LETTER_INSTRUCTION:
        story.append(Paragraph(line, letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in AMB_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Attorney.",
                   "The evidence binder no one knew was being kept.")
    for p in ATT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ATT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The ledger of love.",
                   "The root Hebrews 12 warns about, and the Advocate who closes the account.")
    for p in ATT_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Step out of the courtroom.",
                   "Three questions to sit with before you turn the page.")
    for prompt in ATT_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same wound, in two postures.",
                   "The Ambassador and the Attorney are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=6)
    story.append(PageBreak())

    # ── SECTION 7: Tools ──
    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "When the Ambassador is overworking its giving.",
                   "Six practices for the time before the Attorney is needed.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    for name, desc in AMB_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Attorney opens the ledger.",
                   "Six practices for the moment the heat rises and the brief begins to assemble.")
    for name, desc in ATT_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())

    # ── SECTION 8: Prayer ──
    section_header(story, S, "SECTION EIGHT  \u00b7  A PRAYER",
                   "Pray this slowly.",
                   "Out loud, if you can. Sit a moment after the Amen.")
    for line in PRAYER_BODY:
        story.append(Paragraph(line, S["BlockQuote"]))
    story.append(PageBreak())

    # ── SECTION 9: Going Further ──
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


# ── STANDALONE TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "AMB"
        primary_breakdown = "ATTY"
        primary_trigger = "DISC"
        core_question = "LOV"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "ambassador_attorney_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages using pypdf
    import io
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        # Get a snippet from the first letter/text page
        snippet = ""
        for page in reader.pages[1:3]:
            txt = page.extract_text() or ""
            if txt.strip():
                snippet = txt.strip()[:120]
                break
    except Exception:
        page_count = "unknown"
        snippet = ""

    print(f"DONE: ambassador_attorney.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
