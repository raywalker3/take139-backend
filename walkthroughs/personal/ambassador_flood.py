"""Personal Walkthrough — Ambassador + Flood.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disconnection trigger, "Am I lovable?" core question.
~25 pages, 9 sections.

Key distinctives vs. other Flood profiles:
  - Architect+Flood: a planner's dam bursting after months of impossible suppression.
  - Island+Flood: the first signal that the silence had a cost.
  - Ambassador+Flood: the most theologically loaded — the flood is not merely
    unmanaged feeling but a lifetime of INVISIBLE GIVING finally inventoried aloud.
    "I did this for you. And this. And this. And no one ever noticed."
    The flood IS the Ambassador's ledger speaking.

Unique pastoral move in Section Five: name BOTH that the Ambassador's flood is
PARTLY RIGHTEOUS (the love really was given and really was overlooked — Galatians 6:9)
AND PARTLY IDOLATROUS (the keeping of the ledger was itself a form of self-justification —
Galatians 6:3). Hold both. Spurgeon on burnout in ministry. Keller on the love-idol
(Counterfeit Gods).
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
    "Before you read any further, I want to do for you what a good pastor does at the beginning of a long and honest conversation. I want to lower the lights, slow the pace, and make it safe to say the thing that has never quite been said. What you are about to read is not an assessment of how generously you have lived, though you have been genuinely generous. It is a patient look at the way your soul has learned to manage a particular kind of pain \u2014 and at the cost that management has accumulated, quietly and without announcement, over a long time.",
    "You have, in all probability, been the one who held things together. You were the one who noticed when someone was struggling before anyone else did. You were the one who showed up with food, with presence, with the exact right question at the exact right moment. People have told you the room is warmer for your being in it. That is true. But this walkthrough is going to ask you to look at something underneath that warmth \u2014 a river that has been running in a channel below the giving for longer than you know.",
    "We are going to walk through your trigger \u2014 the specific moment your nervous system says <i>something is wrong here.</i> We will listen to the question underneath that moment, the one that has probably been asking itself since you were young. We will name the strategy you have built in response, and then we will look at the place that strategy breaks under pressure. Only then will we put tools in your hands.",
    "If you were sitting across from me, I would say this plainly. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father whose love for you is not a function of what you have produced for him; a Son who, on the night he was betrayed, did not stop giving even to the one who was selling him \u2014 and who gave from a place so secure that no deficit could threaten it; and a Spirit who is, at this very moment, more committed to your freedom than you are.",
    "So read slowly. When something catches in your throat, stay with it. Do not immediately redirect the attention to whether anyone else in the room is all right. That impulse is the very thing we are here to examine. The catch in your throat is usually the Lord saying, <i>look here, with me.</i> The goal of this walkthrough is a life in which you give because you are loved, rather than giving in order to find out whether you are.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life have no idea it is occurring. Not because they are careless, but because you have become very skilled \u2014 practiced over years \u2014 at not showing it. Someone you have been serving faithfully receives your effort without comment, the way you receive furniture that simply belongs in a room. A family member is quiet for an evening \u2014 not cold, just absent \u2014 and something inside you drops a degree before you have finished noticing. You have given something that cost you more than anyone knew, and the person who received it says thank you and moves on.",
    "On the surface, none of these register as injuries. They are the ordinary weather of relational life. But for you, they do not stay ordinary. Something registers \u2014 a quiet signal, cold and specific \u2014 before you have consciously processed what happened: <i>the connection is gone.</i> And in the wake of that signal, a question rises that is older and more urgent than the evening's disappointment.",
    "This is your trigger. The word for it is <b>disconnection</b> \u2014 and for the Ambassador, disconnection is not merely the absence of warmth. It is the moment the relational temperature drops below what your giving was meant to maintain. And when the temperature drops anyway, the question your soul reaches for is not <i>why are they quiet tonight.</i> It is something older and more searching: <i>did I not give enough? Is it me? After everything I have given, am I still not enough?</i>",
    "C. S. Lewis, in <i>The Four Loves</i>, observed that affection \u2014 the love that gives warmth, that makes home, that smooths the rough edges of daily life \u2014 is among the most beautiful things in the world and among the most dangerous. Dangerous not because it is wrong but because it is peculiarly vulnerable to becoming need dressed in the clothing of generosity. The person whose affection has become their primary instrument for securing love does not usually know this is happening. They feel, genuinely, that they are giving. They are. But underneath the giving, a question is being asked that the giving was never fully able to answer.",
    "<b>Your sensitivity to disconnection is not an accident.</b> It is the residue of something learned, usually early, in a household in which love was inconsistent in its warmth. Perhaps closeness came when you were helpful and retreated when you were not. Perhaps you learned that the way to be held was to make yourself indispensable. Perhaps you became, in your family of origin, the one who managed the emotional temperature before anyone appointed you to the role. You were rewarded for it in the only currency that mattered: people stayed near.",
    "That early schooling wrote a lesson deep in you: <i>love is something I participate in by giving, not by being.</i> And underneath the giving has been a hope, quiet and patient and rarely spoken, that love given consistently enough will eventually produce a love that is stable and sure and not contingent on anything you do next. You have been trying to earn, by giving, a security that only grace can provide. Sit with two questions before we go further. Your head will manage these; your hand will not.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week, that the disconnection signal fired in you. What happened, in two sentences? You are looking for the moment the emotional temperature dropped \u2014 not necessarily a dramatic event, but the moment something inside you registered: <i>the warmth is gone, and I gave so much to maintain it.</i>",
    "How large was the actual event, and how large was the response inside you? If the response was larger than the event, you have just located the trigger. Write the gap in honest terms.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding. The Ambassador has been guarding this one so faithfully that most people who know you have never suspected the wound is there at all. The warmth you project has been, among other things, a very effective cover.",
    "Yours is this: <b>Am I lovable?</b>",
    "It is not the same as <i>Am I loved?</i> \u2014 though it sometimes wears that face. You have received love. You know you have. And still the question does not go away, because the question is more specific and more frightening: <i>Am I loved for what I am, rather than for what I do? If I stopped serving \u2014 stopped warming, stopped being the most attentive person in the room \u2014 would anyone stay?</i>",
    "Most adults would prefer to believe they settled this question long ago. They have not. They have only buried it under sufficient giving that it does not speak during the daylight hours. For the Ambassador, it speaks in the silences \u2014 in the evening that is cooler than expected, in the thank-you without eye contact. And the nervous system's verdict in those silences is not neutral: <i>see? Even after everything you have given, the connection can disappear. This is what you suspected all along.</i>",
    "For you, this question carries a particular weight because you have spent your life organizing around the answer. The hope underneath all your giving \u2014 the hope you may have never quite put into words \u2014 is that love given faithfully enough will eventually become a love stable and certain and not contingent on anything you do next. The Ambassador has been trying to purchase security with service. The terrible thing about this strategy is not that it fails completely \u2014 it is that it works just enough to keep the Ambassador trying.",
]

QUESTION_BODY_P2 = [
    "There is a reason theologians from Augustine to Calvin have insisted that the human heart, at its deepest, is not looking for productivity or comfort in the ordinary sense \u2014 it is looking for a love that holds it permanently. Augustine's confession at the opening of his <i>Confessions</i> \u2014 <i>our heart is restless until it rests in thee</i> \u2014 is a map of the soul's truest motion. The longing that drives the Ambassador is a version of this longing. You want to be held. Not earned. Not maintained. Held.",
    "The Psalms understand this longing. Psalm 103 begins with images of steadfast love that pile upon one another: <i>who forgives all your iniquity, who heals all your diseases, who redeems your life from the pit, who crowns you with steadfast love and mercy.</i> (Psalm 103:3\u20134) The word translated <i>steadfast love</i> is the Hebrew <i>hesed</i> \u2014 the covenant love of God, the love that was decided before you did anything to earn it and cannot be revoked by anything you fail to do. This is the love the Ambassador's soul has been searching for in every room it enters.",
    "The gospel's answer to <i>am I lovable?</i> is theologically precise. Not <i>yes, because of how lovable you are</i> \u2014 which would be flattery, and God does not traffic in flattery. Not <i>yes, if you continue to serve faithfully</i> \u2014 which is the treadmill you are already on. The answer is: <i>you are loved not because you are lovable but because you are in Christ \u2014 and in him, the love the Father has for the Son flows over to you, without condition and without end.</i> Paul names it in Romans 8:15: <i>you have received the Spirit of adoption as sons, by whom we cry, Abba! Father!</i>",
    "But here is where pastoral honesty requires something of you. The Ambassador hears this and nods. You may even feel it, briefly, as a warmth in the chest \u2014 and then set it aside to go check on how everyone else is doing. The gospel answer to <i>am I lovable?</i> is not something the Ambassador easily receives and rests in, because receiving requires stopping, and stopping requires trusting that the room will hold its temperature without your management. The hardest thing about this answer is not the theology. It is the sitting still long enough to let it land.",
]

QUESTION_BODY_P3 = [
    "Here is what the honest work looks like. The Ambassador has been trying to earn, through giving, the security that comes only from being given to. This is a loop that cannot be closed by any amount of service, because the question underneath it is not <i>have I given enough?</i> \u2014 it is <i>am I loved?</i> And giving more cannot answer the second question, because the second question is not about performance. It is about being.",
    "Galatians 4:7 says it plainly: <i>so you are no longer a slave, but a son, and if a son, then an heir through God.</i> An heir does not earn the inheritance. An heir receives it \u2014 simply by being in the family. This is what you are. Not a steward whose tenure depends on service rendered. An heir, whose place was secured at the cross, by a love that did not wait for you to deserve it.",
    "Before we close this section, take a few minutes with the table below. Use recent events \u2014 not ancient ones. Be honest about the size of the response. Your hand will tell you what your head has been managing.",
]

AMB_BODY_P1 = [
    "You have built something. You did not build it in a single decision; no Ambassador does. It grew from you the way a practiced skill grows \u2014 imperceptibly at first, from small responses to real circumstances that rewarded the behavior and penalized the alternative. Over years, it became not merely a strategy but an identity. We are going to call it, throughout this walkthrough, <b>the Ambassador</b>.",
    "The Ambassador's strategy is this: <i>if I am warm enough, attentive enough, generous enough, the connection will hold and the love will stay.</i> The Ambassador does not experience love as a stable ground beneath the feet. The Ambassador experiences love as a temperature that requires maintenance. When the giving flows outward, the temperature stays up and the question is quiet. When the giving stops \u2014 when there is nothing left to give \u2014 the temperature drops, and the question speaks.",
    "The Ambassador is not a manipulator. The warmth is real. The care is genuine. When you ask the person you love how they are doing, you actually want to know. But underneath the genuine warmth is a structure, built long before you had language for it: <i>if I am the most caring person in this relationship, I will not be left behind.</i> The warmth and the strategy have been traveling together for so long that you cannot always tell where one ends and the other begins.",
    "Where did this come from? Perhaps love in your household was inconsistent \u2014 warm on some days, withdrawn on others \u2014 and you discovered that your behavior seemed to influence which version you got. Being helpful brought the warmth back. Expressing need drove it away. Or perhaps there was pain in your home and you became, without anyone asking, the one who managed the emotional temperature before the storm arrived. You were good at it. The role fit you in ways that felt, at the time, like love.",
    "There is a Proverb that commends this kind of wisdom: <i>A soft answer turns away wrath, but a harsh word stirs up anger.</i> (Proverbs 15:1) The Ambassador learned this before being able to read it. And it is not wrong. The world needs people who can enter a tense room and, without raising their voice or shaming anyone, reduce the temperature to something livable. That is a genuine gift, and it has served the people you love in real and specific ways.",
]

AMB_BODY_P2 = [
    "But let me name what the gift has cost. The Ambassador has, over years, developed an almost complete inability to distinguish between serving and surviving. You give when you are tired and when you are hurting and when what you most need is for someone to notice that you are tired and hurting. And you keep giving, because stopping feels dangerous \u2014 because the lesson lodged early was that the way to be loved is to be the one who loves.",
    "J. C. Ryle, writing on self-deception in the Christian life, observed that the soul is fully capable of doing profoundly righteous-looking things for profoundly unrighteous reasons, and that the difficulty is always the root rather than the fruit. The Ambassador's giving looks like love \u2014 and much of it is love \u2014 but at the root is a question that generosity alone cannot answer: <i>am I loved in return?</i> The giving has become, partly, a way of trying to force a yes to that question without ever having to ask it out loud.",
    "The people who love you have probably sensed something they cannot quite articulate. They know you are generous. But some of them have, at moments, a slight sense that something in your giving is not entirely free. There is a weight to it. And when they fail to notice what was given \u2014 when they receive your service with the naturalness of someone receiving furniture \u2014 something happens in you that they never see. The ledger that you did not know you were keeping makes an entry.",
    "<b>The Ambassador is not your enemy.</b> He is a younger version of you who learned, in some real circumstance, that warmth was the price of connection and that stopping the warmth meant risking the connection entirely. He has been faithful. He has kept you in relationship. He deserves your respect, not your contempt. But he has been running the emotional budget of your life on a model that cannot be sustained: giving out more than he takes in, keeping the books off the ledger, hoping the deficit stays invisible.",
]

AMB_BODY_P3 = [
    "What does it look like to begin retiring him, in the dignified sense of that word? Not eliminating the warmth \u2014 the warmth is real and the world needs it. But beginning, slowly, to disentangle the giving from the earning. To serve from a place of security rather than need.",
    "It begins with naming the assumption the Ambassador has been operating under: <i>I am safest when I am giving. My worth in this relationship is proportional to my usefulness to it.</i> This assumption is not merely emotionally costly. When examined in the light of the gospel, it is a quiet but persistent rejection of grace. It says, in its bones: <i>I must earn my place.</i> But the gospel says your place was given to you, at the greatest possible cost, before you did anything to merit it. The Ambassador believes this doctrinally. He has not yet believed it at the level where the giving happens.",
    "The exercise below is written in the Ambassador's own voice \u2014 a letter from him, to you. He has never been asked to speak for himself. He has been too busy taking care of everyone else to have this particular conversation. Read it slowly. He is not villainous. He is exhausted. And he has been waiting a long time for permission to say so.",
]

AMB_LETTER_INSTRUCTION = [
    "The letter below is written in the Ambassador's voice \u2014 to you, the person who has been housing him. Read it without managing it. Then answer the three prompts that follow.",
    "Dear [your name],",
    "I want to tell you something I have never quite said, because I have never let myself be still long enough to say it. I have been giving \u2014 time, attention, warmth, effort, the particular effort of noticing people before they ask to be noticed \u2014 and I have believed, as I gave, that I was giving freely. That I kept no record.",
    "But I want to be honest. I have been keeping a record. Not deliberately. Not with malice. But in some part of me that operated below what I would call intentional, I have been tallying. The meal brought when no one brought one to me. The hour given to someone else's crisis when my own was sitting unremarked in the corner. The care that landed without acknowledgment, absorbed as though it were simply the ambient condition of my presence. I kept this tally the way you keep a secret \u2014 not by hiding it, but simply by never naming it, not even to myself.",
    "I told myself I was living 1 Corinthians 13. I believed I kept no record. What I did not see was that I was keeping a meticulous record of my <i>giving</i> while telling myself the book was closed. I was extending credit and waiting for the account to balance, with a patience I mistook for grace. It was not entirely grace. It was the patience of a person who has not yet admitted what they are waiting for.",
    "What I want, more than I have ever admitted wanting, is to give from a place where the account does not matter \u2014 where the service is the overflow of a love already given to me without my earning it. I am more tired than you know. And more frightened. And I have wants I have never named because naming them felt, for a very long time, like the most dangerous thing I could do.",
    "The Ambassador",
]

AMB_LETTER_PROMPTS = [
    "What part of the Ambassador's letter surprised you? Not the part you recognized immediately \u2014 the part you were not quite prepared to hear.",
    "The Ambassador says he has been keeping a record while telling himself the book was closed. Name one specific relationship or season of life where this was true. What were the entries on the ledger? Write two or three of them by name.",
    "What would the Ambassador need to believe \u2014 really believe, at the level where the giving happens \u2014 in order to give without keeping score? Not doctrinally. What would have to change in the part of him that keeps the tally?",
]

FLOOD_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Ambassador, the breaking has a specific shape that is \u2014 among the three Flood profiles we track in this series \u2014 the most theologically loaded, because it overturns, in a single moment, a lifetime of self-presentation. The Architect+Flood is a planner's dam bursting after months of suppressed competence. The Island+Flood is the first signal that the silence had a cost that was never declared. <b>The Ambassador+Flood is the Ambassador's ledger speaking out loud.</b>",
    "Here is how it happens. The Ambassador has been giving \u2014 not for weeks or months but, in many cases, for years. The care has cost real time, real energy, real emotional reserves drawn on when there was not much left to draw. And because the Ambassador has maintained, in good faith, the sincere belief that the ledger is closed \u2014 that this is love freely given, without account \u2014 the Ambassador has kept going. The belief is not false. The love is real. What the Ambassador has not seen is the other belief running quietly alongside it: <i>surely someone will notice. Surely the giving will eventually be seen and returned.</i>",
    "Then something happens. A wound arrives that cannot be smoothed over. A partner who not only fails to notice but actually criticizes. A friend who, after years of receiving, simply disappears. A family member who says, in a moment of conflict, <i>you are the problem here</i> \u2014 and the Ambassador, who has been managing this relationship's temperature for years, hears this verdict and something gives way. The strategy is tried one more time. It does not work. The wound stays open. And what rises, from wherever it has been gathering, is not what the Ambassador expected.",
    "The ledger opens. And what comes out is not a thin file. It is a record that has been assembling, without the Ambassador's conscious awareness, for a very long time. The voice that emerges is not the warm voice the room is used to. It is the voice of every unreturned gift, every unacknowledged sacrifice, every act of care received as furniture. <i>I did this for you. And this. And this. And you never noticed. I have given and given, and here you are, telling me I am the problem.</i>",
]

FLOOD_BODY_P2 = [
    "The person on the other side of this is disoriented in a way that is hard to describe. An hour ago the Ambassador was warm. Now there is a binder on the table, entries specific and documented and going back years, and the other person had no idea. They did not know the ledger existed. The Ambassador had been so consistently warm that there had been no signal, not once, that anything was accumulating. And the worst part is that the entries are largely accurate. The Ambassador really did all those things. The giving was real, and it was overlooked.",
    "Here is where pastoral care must be both honest and precise, because the Ambassador's Flood contains two truths that must be held simultaneously, and the failure to hold both will leave you in a worse position than when you started.",
    "The first truth: <b>the love the Ambassador gave was real, and much of it was genuinely overlooked.</b> Paul, in Galatians 6:9, says plainly: <i>Let us not grow weary in doing good, for in due season we will reap, if we do not give up.</i> Paul knew that genuine goodness is sometimes invisible to the people who receive it, that faithful service can go unremarked. He did not say this was fine. He told the Galatians not to give up \u2014 which acknowledges that giving up is a real temptation, produced by a real weariness with real cause. The Ambassador's Flood contains genuine grief. Real love was given. Real love was not returned. This part is not idolatry. It is hurt.",
    "The second truth is harder: <b>the keeping of the ledger was itself a form of self-justification.</b> Paul, three verses earlier in the same letter, says: <i>if anyone thinks he is something, when he is nothing, he deceives himself.</i> (Galatians 6:3) The Ambassador who has been giving and counting has been, in the counting, building a case for his own worth: <i>I am worthy of love because of what I have given.</i> The generosity was real. But it was also, in part, a project of self-authentication. The ledger is not merely a record of hurt. It is a record of the Ambassador's attempt to establish, through accumulation, that he deserves to be loved. Tim Keller names this pattern precisely in <i>Counterfeit Gods</i>: a good thing, made into the ultimate thing, becoming a destructive thing.",
]

FLOOD_BODY_P3 = [
    "Charles Spurgeon, preaching to a congregation of tired ministers and exhausted servants, put it plainly: the person who serves in order to be seen \u2014 even seen by himself, even in the privacy of his own internal accounting \u2014 has confused ministry with merit. The Ambassador in the midst of the Flood is presenting a case. The case is real. The exhibits are accurate. What is wrong is not the facts. It is the assumption behind them: that love given consistently enough creates an obligation, that faithfulness accumulates into a debt that can eventually be called in.",
    "It cannot. Love does not work that way. Which is why Paul, who knew something about giving and going unappreciated \u2014 who was treated, as he wrote to the Corinthians, as the scum of the earth by the very people he was pouring himself out for \u2014 refused to build a case. <i>It is the Lord who judges me,</i> he wrote. (1 Corinthians 4:4) He handed the ledger to God and got back to work. The Ambassador has not yet learned to do this. He keeps returning to the tally, hoping that one more presentation of the evidence will finally produce the acknowledgment that makes the question go away.",
    "The gospel's interruption of the Ambassador's Flood is not <i>you are wrong to be hurt.</i> It is not <i>you should not have given so much.</i> It is this: <b>the ledger you have been keeping was never yours to carry, and the love you have been trying to purchase was given to you at the cross before you had anything to show for it.</b> Keller writes in <i>Counterfeit Gods</i> that when a good thing is made into the thing you are living for, you know it has become an idol because its loss is unbearable. The Ambassador's Flood is the sound of that unbearability. Not because the love was not real. Because it was made into the thing the Ambassador was living for, and the accumulation of evidence that it was not being returned became, finally, impossible to contain.",
    "1 John 2:1 says: <i>If anyone does sin, we have an advocate with the Father, Jesus Christ the righteous.</i> The Ambassador has been presenting a ledger of givings to a jury of people never qualified to adjudicate it. Christ does not merely plead the Ambassador's case. He closes the account entirely. The love the Ambassador has been trying to earn by giving has already been given, without condition, at a cost no ledger could match. The question <i>am I lovable?</i> has been answered in the only forum where the answer is binding. The task now is not to collect from others. It is to receive from the One who has already paid.",
]

FLOOD_PROMPTS = [
    "Think of the last time the Flood came for you \u2014 the last time the ledger opened and the accumulated grievances arrived with heat and grief and a documentation the other person never knew existed. What had been gathering, and for how long? Be specific.",
    "As you look back: how much of what came out in that flood was real hurt (love genuinely given and overlooked) and how much was the ledger speaking (the accumulated case for your own worth)? You do not have to resolve the proportion. Simply name both parts honestly.",
]

TWO_TOG_BODY = [
    "Now we set them beside each other, because the Ambassador and the Flood are not two separate problems. They are the same soul in two different postures \u2014 one in which the giving is working to maintain the warmth, and one in which the giving has failed and the ledger must speak for itself.",
    "<b>The Ambassador is what your need does when it has time.</b> The Flood is what your need does when the time runs out and the patience of the ledger is exhausted. The Ambassador gives because giving feels like love, and love feels like safety, and safety is what the question <i>am I lovable?</i> has been asking for since before you had the question in words. The Flood arrives when the giving fails to produce the warmth it was meant to maintain, and everything the Ambassador could not say without threatening the connection is finally said.",
    "The pattern, in slow motion, looks like this. <b>(1)</b> The Ambassador moves through the world giving \u2014 warmth, service, attention \u2014 because giving is the Ambassador's strategy for maintaining love. <b>(2)</b> A disconnection occurs: someone fails to notice what was given. <b>(3)</b> The trigger fires: <i>the connection is gone.</i> <b>(4)</b> The question wakes up: <i>am I lovable?</i> <b>(5)</b> The Ambassador responds by giving more. <b>(6)</b> It does not work this time. The wound stays open. <b>(7)</b> The ledger opens. The Flood arrives \u2014 heat, grief, and the specific documentation of every unreturned gift. <b>(8)</b> Any acknowledgment comes under duress and feels coerced. The question is not answered. The Ambassador retreats, gives again, and the cycle restarts.",
    "What breaks the cycle is not more giving, and not a more persuasive presentation of the ledger. It is a different answer to the question \u2014 received not as doctrine but as lived reality: the love you are looking for has already been given to you, without condition, at a cost you could never match. With that answer received and practiced, the Ambassador begins to give from a different place \u2014 not from scarcity trying to become abundance, but from abundance that has nowhere to go but out.",
    "Fill in the sequence below. When you are done, read it aloud. Both the Ambassador and the Flood lose a measure of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I experience ____________________, something in me reads it as disconnection "
    "and the old question wakes up: <i>am I lovable?</i> My first move is to "
    "____________________, because the Ambassador in me believes that if I can "
    "____________________, the warmth will return and the question will quiet. When that "
    "does not work, the ledger opens and the Flood speaks what I have been carrying: "
    "____________________. What I am actually after, underneath all of it, is the verdict "
    "____________________ \u2014 a verdict Christ has already spoken over me, not because "
    "of what I have given but because of what has been given for me, in ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of practices, each one honest enough to help and simple enough to actually use. None of them will resolve the Ambassador's pattern in a single application. All of them, practiced with any consistency over months, will loosen the grip of the cycle you have just named.",
    "I have divided them into two sets: tools for when the Ambassador is overworking its giving (when service has tipped from love into survival, from gift into insurance), and tools for when the Flood has come or is building (when the ledger has opened and the heat is rising). Ambassador tools come first, because the Flood cannot be addressed usefully until you understand what the Ambassador has been doing and why.",
]

AMB_TOOLS = [
    ("The motive audit", "Once a week, ask one question: <i>in the past seven days, was there anything I gave in order to secure love rather than to express it?</i> Simply name it without scolding yourself. The Ambassador loses some of its automatic power when it is required, once a week, to account honestly for its own motives."),
    ("The gift received", "Each day, practice receiving something from someone without immediately giving something back. A compliment. An offer of help. Let it land without deflecting or turning the attention back to the other person. Receiving without converting it into an occasion to give more is, for you, the harder spiritual discipline."),
    ("The handed-back ledger", "Each evening, name one thing you gave today that you secretly hoped would be noticed. Then say aloud or in writing: <i>Lord, I hand this entry back to you. The account is yours to keep. I am not the treasurer of this love.</i> The Ambassador has been keeping the ledger on God's behalf. This is the practice of returning it."),
    ("The unexpressed need", "Once a week, identify one genuine relational or emotional need and express it directly, without framing it as concern for the other person. Not: <i>I know you are busy, but</i>. Simply: <i>I need ___.</i> Asking directly is the first act of letting someone love you without your having to earn it."),
    ("The Abba prayer", "Before you have done anything for anyone, sit for five minutes and say: <i>Father, I am your child. Not your steward. Your child. I am loved before I have given anything today.</i> The Ambassador serves from morning to night. This establishes the right order: loved first. Service after."),
]

FLOOD_TOOLS = [
    ("Name the entry before it becomes a flood", "When the ledger begins to fill \u2014 when you have been giving into a silence for more than a week without acknowledgment \u2014 say one sentence to a trusted person: <i>I have been giving something that has not been noticed, and I feel the old question asking.</i> Not to build a case. To break the secrecy before the evidence goes underground. Named early, while it is still a small entry, it remains manageable."),
    ("The righteous grief / idolatrous ledger distinction", "After a wound, and before you respond, sit with these two questions separately: <i>What is the genuine hurt here \u2014 love truly given and truly overlooked?</i> And: <i>What is the ledger speaking \u2014 the accumulated case for my own worth?</i> The first deserves to be named and mourned. The second deserves to be handed to God. Knowing the difference before you open your mouth will change both what you say and how you say it."),
    ("The thirty-second test", "When you feel the Flood rising, pause and ask: <i>Am I bringing a wound to be witnessed, or am I opening a ledger to be settled?</i> Bringing a wound is appropriate and necessary. Opening a ledger will not produce the verdict you are after, because the verdict you are after is not judicial. It is relational. And ledgers do not produce closeness."),
    ("The one honest sentence", "When you must speak to the person who wounded you, say one sentence that names the specific wound: <i>When that happened, I felt invisible, and I need you to know that.</i> Not the whole accumulation. One sentence. The relationship can sustain a wound named honestly. It is less certain it can sustain the full documentation of everything that has been missed for years."),
    ("The advocate prayer", "When the Flood has come or is building, pray slowly: <i>Lord Jesus, you are my Advocate. You have seen every entry on this ledger, and you have already settled the account that stood against me. The love I am looking for has already been given. I do not need to collect this debt.</i> The third time through, the heat usually begins to subside."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Ambassador in me, and you do not despise him. You know what he was built for \u2014 the specific households, the specific mornings in which he learned that the surest path to being held was to make himself the one who did the holding. Thank you that the warmth he has been carrying, though mixed with strategy, has been real warmth, and that real warmth fed real people.",
    "But Father, the ledger is heavier than I have admitted. I have been keeping a record while telling myself the book was closed. Teach me to give from a place that is not earning but overflowing. When the disconnection fires and the old question wakes up \u2014 <i>am I lovable?</i> \u2014 let me hear your answer before I reach for the ledger. <i>You are my child. My love for you is not contingent on what you do next.</i> Let that land in the place where the giving happens.",
    "Lord Jesus, when the Flood comes, remind me that I contain both a genuine grief and an idolatrous ledger, and that you have made provision for both. For the grief: let it be mourned honestly. For the ledger: remind me that the account has already been settled at a cost I could not have matched, and that releasing the debt is not defeat. It is the discovery of what grace actually costs.",
    "In the name of the One who, on the night he was betrayed, took bread in his hands and gave it to the very ones who were about to hand him over \u2014 who gave to the end, from a place so secure that no ledger could threaten it \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Ambassador and the Flood have been with you for a long time, and one afternoon's reading will not retire either of them. What follows is a short list of next steps \u2014 some immediate, some long-term \u2014 for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different sentences will land. The Ambassador will want to receive this document once, file it, and return to taking care of everyone else. Read it again anyway."),
    ("Take one tool, not six.", "Choose a single practice from Section 7 and try it for two weeks before adding another. One posture, held with any consistency, begins to reshape the soul from the inside."),
    ("Sit with Galatians 6:9 and 6:3 together.", "Read them in the same sitting: <i>Let us not grow weary in doing good, for in due season we will reap, if we do not give up</i> (v. 9) and <i>if anyone thinks he is something, when he is nothing, he deceives himself</i> (v. 3). Ask honestly which verse describes your giving in a particular relationship right now. Both may be true simultaneously. The Ambassador's particular spiritual danger is in conflating them."),
    ("Tell one person what you found.", "Not the whole document. One sentence: <i>I learned that my mechanism is the Ambassador and my breakdown is the Flood \u2014 and the Flood is my ledger speaking, and I have been keeping a ledger I did not fully know I was keeping.</i> The Ambassador's pattern feeds on secrecy. Named to a safe witness, the pressure begins to lose its structure."),
    ("Read further on the love that frees.", "Tim Keller, <i>Counterfeit Gods</i> \u2014 his chapter on the love-idol. C. S. Lewis, <i>The Four Loves</i> \u2014 especially on affection and the ways affectionate love, when it becomes possessive need, begins to demand rather than give. Tim Keller, <i>Walking with God through Pain and Suffering</i> \u2014 for the longer work of receiving the love you have been trying to manufacture."),
    ("If you are stuck, ask for help.", "For the Ambassador specifically, asking for help is the most countercultural thing this walkthrough can recommend. Asking someone to help you \u2014 not as a project of vulnerability but as a genuine, undisguised need \u2014 is, for you, an act of faith."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom by a Father "
    "who has not, in all the years you have been giving, kept any record of what you owe him. "
    "His love for you is not a transaction and it is not contingent on the warmth you generated "
    "this week. The love was given at the cross, before you had anything to show for it, "
    "to a version of you that had nothing to offer. That is the love the Ambassador has been "
    "looking for in every room he has ever entered. It was already there. "
    "Go gently with yourself. The One who began the good work in you will be the one who finishes it."
)


def _three_column_table(rows=7):
    """Three-column journal table for the core question reflection exercise."""
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
    """Generate the Ambassador+Flood walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='AMB', primary_breakdown='FLOOD',
    primary_trigger='DISC', core_question='LOV'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="AMBASSADOR  \u00b7  FLOOD",
        title="Take 139 Walkthrough \u2014 Ambassador + Flood",
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
    story.append(Paragraph("The Ambassador &nbsp;\u00b7&nbsp; The Flood", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disconnection &nbsp;\u00b7&nbsp; Core Question: Am I lovable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cLet us not grow weary in doing good,<br/>"
        "for in due season we will reap,<br/>"
        "if we do not give up.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Galatians 6:9",
        ParagraphStyle("cqa", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 1: Opening \u2500\u2500
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read this slowly. The chapter that follows has been a long time in the writing.")
    for p in OPENING_BODY:
        story.append(Paragraph(p, S["BodyJ"]))

    # \u2500\u2500 SECTION 2: Trigger \u2500\u2500
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TRIGGER",
                   "Disconnection.",
                   "The moment the warmth disappears, and what your soul makes of it.")
    for p in TRIGGER_BODY[:3]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  CONTINUED",
                   "Where the sensitivity came from.",
                   "The lesson that was lodged, and what it has been costing you.")
    for p in TRIGGER_BODY[3:]:
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

    # \u2500\u2500 SECTION 3: Core Question \u2500\u2500
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I lovable?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "The love that does not fluctuate.",
                   "What Scripture actually says, and the honest cost of receiving it.")
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

    # \u2500\u2500 SECTION 4: Mechanism \u2500\u2500
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Ambassador.",
                   "The caretaker. The warmth-keeper. The one who arrived before anyone asked.")
    for p in AMB_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "What the giving has cost.",
                   "Serving and surviving, and the ledger kept off the books.")
    for p in AMB_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in AMB_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Ambassador.",
                   "He has been faithful. Let him speak.")

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

    # \u2500\u2500 SECTION 5: Breakdown \u2500\u2500
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Flood.",
                   "The ledger speaking. Everything the Ambassador could not say until now.")
    for p in FLOOD_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "Righteous grief and idolatrous ledger.",
                   "Two truths the Ambassador's Flood contains, and why both must be named.")
    for p in FLOOD_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in FLOOD_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions about the last Flood.",
                   "Sit with these before you turn the page.")
    for prompt in FLOOD_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 12))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same need, in two postures.",
                   "Ambassador and Flood are not two problems. They are one cycle.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  YOUR SEQUENCE",
                   "Write it in your own words.",
                   "Fill the blanks. Read it aloud when you are done.")
    story.append(Spacer(1, 6))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=5)
    story.append(PageBreak())

    # \u2500\u2500 SECTION 7: Tools \u2500\u2500
    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "What to do when you feel the cycle begin.",
                   "Small enough to carry. Useful enough to reach for.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Ambassador is overworking its giving.",
                   "Five practices for the time before the ledger fills.")
    for name, desc in AMB_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Flood has come or is building.",
                   "Five practices for the overflow and its aftermath.")
    for name, desc in FLOOD_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<b>Integration:</b> The single discipline that connects both sides is this \u2014 "
        "the regular, small, honest practice of receiving love before you give it. "
        "Before the giving begins each morning, receive. Before the ledger fills, "
        "return an entry to God. Before the flood, name the entry to one person. "
        "The Ambassador was made to give from abundance. The abundance is already there. "
        "The practice is learning to stand in it before you start handing it out.",
        S["BodyJ"]))
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


# \u2500\u2500 STANDALONE TEST \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "AMB"
        primary_breakdown = "FLOOD"
        primary_trigger = "DISC"
        core_question = "LOV"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "ambassador_flood_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    import io
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        snippet = ""
        for page in reader.pages[1:4]:
            txt = page.extract_text() or ""
            if txt.strip():
                snippet = txt.strip()[:150]
                break
    except Exception:
        page_count = pdf_bytes.count(b"/Type /Page\n") or pdf_bytes.count(b"/Type/Page")
        snippet = ""

    print("DONE: ambassador_flood.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
