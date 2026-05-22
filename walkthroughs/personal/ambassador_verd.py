"""Personal Walkthrough — Ambassador + Quiet Exit (Verdict).

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disconnection trigger, "Am I lovable?" core question.
Breakdown: Quiet Exit (VERD) — quietly decides "I'm done"; stops investing;
           withdraws into a verdict that is often invisible to the other person.

Breakdown code: VERD. Walkthrough #17 of 36.

Calibration note: This is the saddest of all the Verdict breakdowns because
the Ambassador — by definition — has spent years choosing love even when it
cost. The Ambassador has been warm, attentive, self-giving. When the Ambassador
finally renders the verdict, quietly and internally, with no announcement, what
they are saying is: I have given love long enough to know it is not coming back.

The breakdown presents as a softening: the Ambassador becomes gentler, less
demanding, more polite. This looks like maturity. It is an internal funeral.

Pastoral key in Section Five: distinguish (a) the Ambassador's God-honored
capacity to grieve genuine loss (good and biblical) from (b) the Verdict's
premature pronouncement of death over a relationship that may still be alive
(unbelief). Romans 12:18 ("if possible, so far as it depends on you, live
peaceably with all") names a real limit — but 1 Corinthians 13:7 ("love
hopes all things") names the corrective. The Ambassador's verdict often closes
the relational door before the gospel has had its full word in.
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
    "Before you read any further, I want to do what a good counselor does before he says anything hard. I want to lower the lights, slow the pace, and sit with you in the particular sadness of the profile you are holding in your hands. Because what follows is not primarily a description of your failures. It is a description of your faithfulness — and of the place where faithfulness, when it has been given long enough without return, can quietly become its own kind of loss.",

    "You are, in all likelihood, one of the warmer people in the rooms you inhabit. People know this about you. You were the one who noticed when someone was left out, who remembered the detail others forgot, who smoothed the rough edge of a thousand ordinary moments. You have given — generously, consistently, at real cost — over a very long time. This walkthrough is not going to ask you to question the giving. It is going to ask you to look at what the giving has been, quietly and without announcement, moving toward for a long time. And that is a harder thing to look at.",

    "We are going to walk through your trigger — the moment your nervous system says something is wrong here. We will listen to the question underneath that moment, the one that has probably been with you since you were very small. We will name the strategy you built to answer that question, and the place that strategy collapses when it has been strained long enough. And then, only then, will we put tools in your hands.",

    "If you were sitting across from me, I would say this plainly and mean it: <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father whose love for you is not a reward for your consistency; a Son who, on the night he was betrayed, did not exit the relationship with the man who was about to hand him over but washed his feet and called him friend; and a Spirit who is, at this very moment, interceding for you with a love that has never once factored in what you have managed to give this week.",

    "Read slowly. When something catches in your throat, stay with it — do not immediately check whether anyone else in the room is all right. That catch is usually the Lord saying, <i>look here, with me.</i> The goal is a slightly freer life: one in which you give because you are loved, not because giving has become the only language in which you know how to ask whether you are. Take your time. The chapter you are about to read has been a long time in the writing.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life would be startled to know it is occurring — not because they are careless, but because you have become very practiced at not letting it show. Your spouse has been quiet all evening. Not hostile, not cold — just absent, somewhere else, in a place you were not invited. A close friend replies to your careful three-paragraph message with two words and no follow-up question. A gathering you were anticipating is warm to everyone in the room and somehow slightly thinner than you needed it to be for you specifically. Or you gave something — real time, real emotional energy, an act of care that cost you — and it landed in the room the way a piece of furniture lands: received without comment, absorbed into the background as though it had always been there.",

    "On the surface, none of these are catastrophes. You may not show a thing. Your face may be exactly as warm as it always is. You may, in fact, be the one who turns to the person who just went quiet and gently asks how they are doing — who generates the warmth to fill the very gap their absence created. You are good at that. You have been good at that for a long time. But underneath the warmth, something specific and cold has registered: <i>the connection is gone.</i>",

    "This is your trigger. The word for it is <b>disconnection</b> — and for you it is not merely a temporary absence of contact but the withdrawal of warmth from someone whose warmth you depend on to feel safe. Disconnection does not present to you as a neutral weather condition. It presents as a signal, one that arrives immediately and with a precision your nervous system has spent years developing: <i>did I do something? Is it me? Am I losing them?</i>",

    "C. S. Lewis, in <i>The Four Loves</i>, observed that the more genuinely we love, the more we expose ourselves to being wounded by the withdrawal of what we love. This is particularly acute for the Ambassador, who has organized much of life around the maintenance of closeness — around being the source of warmth in relationships rather than its passive recipient. When the warmth flows back, everything feels ordered and right. When it goes absent, even briefly, the Ambassador experiences it not as inconvenience but as a kind of loss — and what is being lost is not merely comfort but something closer to confirmation.",

    "<b>Your sensitivity to disconnection is not a flaw in your character.</b> It is the residue of something specific, learned early, in a household or relationship in which love was inconsistent in its warmth or conditional in its expression. Perhaps closeness came when you were helpful and receded when you were not. Perhaps you learned early that expressing need plainly tended to make people go quiet or pull back, and so you became fluent in a different language — one in which your own longing was converted into care for others, your neediness translated into attentiveness, your desire to be held translated into an offering to hold. That early schooling deposited a lesson that still sits below ordinary reflection: <i>love is something I participate in by giving, not simply by being.</i> Underneath the generosity has been a question — quiet, patient, never quite answered — waiting to see whether the love you gave will come back. Before we go further, sit with two questions in writing. Your head will manage this question. Your hand will not.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week, that the disconnection signal fired in you. What happened, in two sentences? You are looking for the specific moment the internal temperature dropped — not necessarily a dramatic event, but the moment your soul said, <i>the warmth is gone.</i>",
    "How large was the event, and how large was the response inside you? If the response was disproportionate to the event, you have just located your trigger. Write one sentence about what the gap suggests.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm has been guarding for longer than you have had words for it. The Ambassador has been standing guard over this particular wound with unusual skill and consistency — so much skill, in fact, that most people who know you have never seen it.",

    "The question is this: <b>Am I lovable?</b>",

    "It is not the same as <i>Am I loved?</i> — you have received love, you know you have, and still the question does not go away. It is more precise and more frightening than that: <i>Am I the kind of person who is loved for what I am rather than for what I do?</i> If I stopped serving, stopped warming, stopped being useful and available and attentive — would anyone stay? This is not a theological abstraction for you. It is a question with teeth, and it bites hardest in the silences: in the spouse's quiet evening, in the friend's short reply, in the gathering that was somehow warmer for others than it was for you.",

    "For you this question carries a particular urgency because you have organized so much of your life around answering it through your behavior. You have been generous. You have been present. You have taken care of people in ways that cost real time and real energy and real emotional reserves. And the hope underneath all that giving — the hope you may never quite have put into words — is that love given consistently enough, warmly enough, sacrificially enough, will eventually produce a love that is stable and certain and not contingent on anything you do next. You have been trying to answer the question <i>am I lovable?</i> by making yourself indispensable. And this is, to put it plainly, a loop that cannot close.",
]

QUESTION_BODY_P2 = [
    "There is a reason that theologians from Augustine to John Calvin insisted that the human heart, at its deepest, is not looking for productivity or achievement or even ordinary security. It is looking for a love that holds it permanently. Augustine's words at the opening of his <i>Confessions</i> — <i>our heart is restless until it rests in Thee</i> — are not decoration. They are a map of the soul's truest motion. The longing that drives the Ambassador is a version of this longing. You want to be held. You want to know that someone's love for you is not the product of your last act of service but is, simply, for you.",

    "The Psalms understand this longing. Psalm 103, which David wrote from a life that had tested the question very thoroughly, begins: <i>Bless the Lord, O my soul, and all that is within me, bless his holy name! Bless the Lord, O my soul, and forget not all his benefits — who forgives all your iniquity, who heals all your diseases, who redeems your life from the pit, who crowns you with steadfast love and mercy.</i> (Psalm 103:1-4) The word at the center is <i>steadfast.</i> The Hebrew is hesed — the covenant love of God, the love decided before you were born and not dependent on anything you do to maintain it. This is the love the Ambassador's soul has been searching for in every room it enters. It is not a room-temperature love. It is a love that holds.",

    "The gospel's answer to the question <i>am I lovable?</i> is specific and theologically precise. It is not <i>yes, because of who you are</i> — that would be flattery, and God does not comfort his children with false things. It is not <i>yes, so long as you continue to serve faithfully</i> — that would be the very treadmill you are already on. It is: <i>you are loved not because you are lovable but because you are in Christ, and in him the love the Father has for the Son flows over you without condition and without end.</i> Paul says it in Romans 8:15: <i>you have received the Spirit of adoption as sons, by whom we cry, 'Abba! Father!'</i> An adopted son is not a probationary employee. He is an heir. Galatians 4:7: <i>so you are no longer a slave, but a son, and if a son, then an heir through God.</i>",

    "Here is where pastoral honesty demands something of you specifically. The Ambassador hears this and nods. You may feel it, warmly and briefly, and then set it aside to go check on how everyone else is doing. The gospel's answer to <i>am I lovable?</i> is not something the Ambassador easily receives and rests in, because receiving requires stopping, and stopping requires trusting that the room will be all right without you managing it. The hardest thing about this answer, for you, is not the theology. The theology is fine. It is the sitting still long enough to let it land below the theology.",
]

QUESTION_BODY_P3 = [
    "Here is what the honest work looks like for you. The Ambassador has been trying to earn, through giving, the security that comes only from being given to. Giving more is not the answer to the question <i>am I loved for who I am?</i> — it is a way of deferring the question, of substituting the one thing you can control (your own giving) for the one thing you cannot (whether someone loves you freely and permanently). The cross interrupts this substitution. Not in the abstract — specifically and personally. Jesus Christ absorbed the worst possible version of the thing you most fear: to give everything and be abandoned anyway. He went to that place, for you. And from the other side of the empty tomb he says: the love that holds you is not contingent on what you do next.",
]

AMB_BODY_P1 = [
    "You have built something. You did not sit down one morning and draw the blueprints. The Ambassador grew from you the way a habit grows — imperceptibly, out of necessity, from small decisions made in response to real situations that rewarded the behavior. It is a structure now, and it deserves a careful introduction, because it is both a genuine gift and a strategy that has been running on an unsustainable model for a very long time.",

    "The <b>Ambassador</b> is a soul who has learned — usually early, usually from a specific set of circumstances — that love is something that must be maintained through service. The Ambassador does not experience love as a stable floor beneath the feet but as something more like a temperature that must be managed. If the Ambassador is warm enough, attentive enough, giving enough, helpful enough, the temperature stays up. If the Ambassador stops giving — gets tired, goes quiet, has a need of their own — the temperature drops, and dropping feels dangerous. Not merely unpleasant. Dangerous.",

    "What matters here is this: the Ambassador is not a manipulator. The giving is real. The warmth is not performed — it is genuinely felt. The care is not theater. When you ask the person you love how they are doing, you actually want to know. But underneath the genuine warmth is a strategy, put in place long before you had words for it: <i>if I am the most caring person in the room, I will not be left behind.</i>",

    "Where does this come from? The taxonomy research behind this profile surfaces one of several recognizable histories. Perhaps love in your household was inconsistent — warm some days, withdrawn on others — and you discovered as a child that your behavior seemed to influence which version arrived. If you were helpful, the warmth returned. If you were needy, it retreated. And so you became helpful, because helpful was safer than needy. Perhaps there was real pain in your home and you became, without anyone asking you to, the one who managed the emotional temperature — who knew how to read a room before anyone else did, who positioned themselves between the disturbance and the people who could not weather it.",

    "There is a Proverb that commends this kind of wisdom: <i>A soft answer turns away wrath, but a harsh word stirs up anger.</i> (Proverbs 15:1) The Ambassador has known this in their bones long before reading it off a page. The ability to de-escalate, to bring warmth into tension, to hold a room together by sheer attentiveness — these are real gifts. The world needs people like you. The difficulty is not the gift. The difficulty is what the gift has been pressed into service for.",
]

AMB_BODY_P2 = [
    "Let me name what the gift has cost you. The Ambassador is a person who has, over years, developed an almost complete inability to distinguish between serving and surviving. You give to the people you love, and you give to people you barely know, and you give when you are tired and when what you most need is for someone to notice that you are tired and give something to you. And you keep giving, because stopping feels dangerous, and because you learned a long time ago that the way to be loved is to be the one who loves.",

    "Tim Keller, in <i>The Prodigal God</i>, observed that the elder brother in Luke 15 is the more dangerous of the two sons precisely because he cannot see his own condition: he has been serving faithfully, keeping every rule, giving everything required — and has still not understood that his father's love was not a wage to be earned. The Ambassador is, in many seasons, this elder brother. The giving is real and the faithfulness is real, but underneath both is the assumption that the love must be maintained by them — that it cannot simply be received. J. I. Packer, in <i>Knowing God</i>, put the theological point more precisely: the great mistake of the Christian life is to think of God's love as something we can secure through our faithfulness rather than something we are already held in. The Ambassador has made this mistake not only theologically but in every significant relationship, trying to secure love by faithfulness rather than resting in love as the prior condition.",

    "The people who love you have probably felt something they cannot quite articulate. They know you are generous. But they may have a sense — uncomfortable to admit, almost guilty — that there is something in your giving that is not entirely free. A slight weight to it. A way in which, after you have given a great deal, there is an expectation in the air — not spoken, not demanded, simply present — that something will come back. They cannot name this easily because you have never said it. But it is there. And when they fail to meet it — as they sometimes will, because they are human and tired, as we all are — something happens in you that they almost never see.",

    "<b>The Ambassador is not your enemy.</b> He is a younger version of you who learned, in some real circumstance, that warmth was the price of connection and that stopping the warmth meant risking the connection. He has been faithful. He has kept you in relationship, kept the rooms you inhabit at a temperature where human beings can live together. He deserves your gratitude, not your contempt. But he has been running the emotional budget of your life on an unsustainable model — giving out more than he takes in, keeping the books off the record, hoping that no one will notice the deficit. Including himself.",
]

AMB_BODY_P3 = [
    "What does it look like to begin retiring him, in the dignified sense of the word? Not eliminating the warmth — the warmth is real and the world needs it. But beginning to disentangle the giving from the earning; beginning to serve from a place of security rather than from a place of need; beginning, slowly, to allow yourself to be cared for with something like the openness you extend to everyone else.",

    "It begins with naming the assumption the Ambassador has been operating under: <i>I am safest when I am giving. My worth in this relationship is proportional to my usefulness to it.</i> When you examine that assumption in the light of the gospel, it is not merely emotionally costly. It is a quiet rejection of grace — a refusal, at the level where the behavior happens, of the word the gospel has already spoken: <i>you are loved not because you are useful but because you are his.</i> The Ambassador believes this doctrinally. He has not yet believed it at the level where the giving happens.",

    "The exercise below is different from the one in some of the other walkthroughs. I am not asking you to write to the Ambassador. I am asking you to read a letter from him — to hear, in his own voice, what he has been doing and why, and what he is afraid would happen if he stopped. The Ambassador has never had this conversation out loud. He has been too busy taking care of everyone else to have it.",
]

AMB_LETTER_INSTRUCTION = [
    "What follows is a letter written in the Ambassador's voice — from him, to you. He is not villainous. He is exhausted, and he is frightened. Read it slowly. Then answer the three prompts that follow.",
    "Dear [your name],",
    "I want to tell you something I have never told anyone, because I have never let myself sit still long enough to say it. I have been keeping a record.",
    "Not deliberately. Not maliciously. I did not decide one morning to keep a tally. But somewhere in a part of me I did not fully know was operating, I have been keeping count. Of the meals I brought when no one brought any to me. Of the calls I made when no one checked in on how I was doing. Of the effort that went unacknowledged — not unrewarded, exactly, but unnoted, absorbed as though it were simply the ambient condition of my presence.",
    "I kept this record because I did not know how else to track whether my love was landing. Whether I was mattering. Whether the giving was producing anything. I kept it the way you keep a secret — not by locking it somewhere but simply by never speaking of it. And I told myself, sincerely, that I was keeping no record at all. I have read 1 Corinthians 13. I believed I was living it. What I did not see — what I am only now beginning to name — is that I was keeping a record of my own giving while telling myself the book was closed.",
    "And something else I need to tell you. There is a verdict I have been writing in that record for a long time. Not a sentence, exactly. More like a direction. Each time the disconnection came — each time the warmth went absent, each time the giving landed without echo — another line was written. I have been telling myself it was simply honest accounting: here is what I gave; here is what came back. But accounting, held long enough, becomes a conclusion. And the conclusion I have been approaching, slowly and with no announcement, is: <i>this is not coming back. I have given enough to know.</i>",
    "I am more tired than you know. And I am more frightened. And what I want — what I have always wanted, underneath all the giving — is simpler than anything I have let myself say: to be loved freely. Without earning it. To give from abundance rather than from need. But I do not know how to get there from here, and the verdict has been growing in me quietly, and I am not sure you have even noticed it beginning.",
    "The Ambassador",
]

AMB_LETTER_PROMPTS = [
    "What part of the Ambassador's letter surprised you? Not the part you expected — the part you were not quite ready to hear.",
    "The Ambassador says he has been writing a verdict in the ledger — a slow conclusion that this is not coming back. Where in your current life is that verdict being written? Name the relationship or situation, and write one sentence about how far along the verdict has gone.",
    "What would the Ambassador need to believe — really believe, at the level where the giving happens — in order to give from abundance rather than need? What would have to change in how he understands his own lovability?",
]

VERD_BODY_P1 = [
    "Every mechanism has a place it breaks. The Ambassador's breakdown is called <b>the Quiet Exit</b>, and of all six breakdowns we track, this is the saddest — because the Ambassador, by definition, has not been protecting himself from connection. He has been running toward it, warmly and faithfully, at real cost, for a long time. When the Quiet Exit comes to an Ambassador, it is not the withdrawal of someone who never fully entered. It is the withdrawal of someone who gave everything they had to give and eventually, quietly, without announcement, concluded: <i>it is not coming back.</i>",

    "Here is how it forms. The Ambassador has been giving — perhaps for months, perhaps for years. The disconnection signals have been firing. The Ambassador's response has been, each time, to give more warmly, to smooth the rough edge, to bridge the gap. And for a long time that response has worked. The temperature has returned. But at some point, in some specific accumulation of moments, the response stops producing the return. The warmth is given. The gap stays. The question wakes again — <i>am I lovable?</i> — and this time the Ambassador does not have anything new to offer it.",

    "What happens then is not an explosion. It is something quieter and, in its way, sadder. Something in the Ambassador simply stops moving toward. The energy that has always flowed in the direction of the relationship begins, almost imperceptibly, to redirect. The Ambassador's emotional investment in the relationship begins to quietly retract — the way a tide goes out, steadily, without announcement, until the shore that was submerged is suddenly exposed.",

    "What makes this breakdown so difficult to name is that it presents, from the outside and often from the inside, as something healthy. The Ambassador becomes gentler in these seasons, not harsher. Less demanding. More polite. More apparently at peace. <i>I've come to terms with it. I've accepted that this person is who they are. I've stopped expecting things that were never going to come.</i> These sentences have the grammar of maturity. They feel like something a wise pastor might say. And that is precisely what makes them dangerous — because they can be those things, and they can also be something else entirely.",
]

VERD_BODY_P2 = [
    "What they can also be is unbelief wearing the costume of wisdom. Let me say that as directly as the Ambassador deserves, because the Ambassador respects directness even when — especially when — the directness is about himself.",

    "The Quiet Exit, at its deepest structural level, is a crisis of hope. And the particular Christian virtue of hope — not optimism, not positive thinking, not the refusal to see what is genuinely difficult — is precisely what Paul names in 1 Corinthians 13:7 as part of love's essential character: <i>love bears all things, believes all things, hopes all things, endures all things.</i> The Ambassador has spent years bearing. He has believed. He has endured. The Quiet Exit is the moment when hope quietly leaves the room — not in anger, not in protest, but with the composed and gentle certainty of someone who has done the math and reached a conclusion. And love, left behind, slowly loses its engine.",

    "Here is what the Ambassador must hear about hope, because the instinct will be to argue: Christian hope is not naivete. It is not the insistence that things will turn out the way you want them to. It is not the refusal to grieve genuinely what has been genuinely lost. Christian hope is the refusal to pronounce a final verdict on a story that God has not yet finished writing. It is the patient, sometimes aching, holding-open of a door that you, on your own evidence, would already have sealed. John Calvin, in his commentary on Romans 5, wrote that hope is <i>the patient expectation of those things which faith has believed to be truly promised by God.</i> Hope expects — not because the evidence is favorable but because the ground of its expectation is God's promise, and God has not yet issued the final statement on the relationship or situation the Ambassador is in the process of quietly exiting.",

    "I want to be pastorally honest about what makes this harder for the Ambassador than for anyone else. The Architect who renders a Quiet Exit has been building structures and controlling outcomes; self-sufficiency is familiar terrain. The Island who exits quietly has spent years practicing emotional distance. But the Ambassador who renders a Quiet Exit has been doing the opposite of self-protection for years. He has been present. He has given. When the verdict finally comes, it comes not from someone who refused to love but from someone who loved longer than almost anyone else would have. The pastoral word is not a rebuke. It is a lament. And after the lament — only after — a question.",
]

VERD_BODY_P3 = [
    "The question is this. There is a difference between the God-honored grief of genuine loss and the premature pronouncement of death over a relationship that may still be alive. Both can feel identical from the inside. Both involve sadness. Both involve the withdrawal of a certain kind of hope. But they are not the same thing, and the difference matters enormously for where you go next.",

    "Paul, writing in Romans 12:18, says: <i>if possible, so far as it depends on you, live peaceably with all.</i> Notice both qualifications. <i>If possible.</i> <i>So far as it depends on you.</i> Paul is not requiring the Ambassador to remain infinitely open to every person in every circumstance regardless of the cost. He knows that peaceable living is sometimes not possible — that some relationships, by the choices of the person on the other side, have genuinely ended, and that naming that is not unbelief but accuracy. There is a real and pastoral place for limits, for the acknowledgment that a particular door has, in fact, closed.",

    "But that same chapter opens with a verse that names what is required before any verdict is rendered: <i>Do not be conformed to this world, but be transformed by the renewal of your mind.</i> (Romans 12:2) The Ambassador's verdict is often rendered by the old mind — the mind formed by the early lesson that love has to be earned and that its withdrawal is probably your fault. The question is not whether limits ever belong. They do. The question is whether the verdict the Ambassador is currently writing has been formed by that renewed mind, or whether it has been formed by accumulated weariness and the old question — <i>am I lovable?</i> — answering itself in the silence.",

    "D. Martyn Lloyd-Jones, preaching on 1 Corinthians 13, said that the most reliable mark of love in the genuinely difficult seasons is not warmth — warmth comes easily when things are going well — but hope. The willingness to keep the door open when every feeling argues for closing it. To refuse the premature verdict. To say: <i>I do not know what God is still writing in this story.</i> That is not weakness. For the Ambassador, after years of faithful giving, it is among the most costly and most courageous acts of obedience available.",
]

VERD_PROMPTS = [
    "Name the relationship or situation in which the Quiet Exit has most recently begun. You do not have to have announced it. You may barely have admitted it to yourself. Describe what the exit has felt like from the inside: has it come as a single decision, or as a slow and quiet accumulation?",
    "Ask yourself the honest question: <i>Is the verdict I am writing in this relationship a grief that God has given me, or a conclusion I reached alone, in private, before the evidence was fully in?</i> Write the most honest answer you can. Do not edit it for pastoral acceptability.",
]

TWO_TOG_BODY = [
    "Now we place them next to each other, because the Ambassador and the Quiet Exit are not two separate problems. They are the same wound in two different phases of its long movement. In the first phase, the wound gives. In the second phase, the wound withdraws. But underneath both is the same person, asking the same question, and still — after all of it — not quite sure of the answer.",

    "<b>The Ambassador is what your need does when it still has hope.</b> The Quiet Exit is what your need does when the hope has run out. The Ambassador gives warmly, faithfully, generously — managing the emotional temperature, preventing the disconnection from ever becoming undeniable. The Quiet Exit comes when the disconnection becomes undeniable anyway, and the Ambassador, who has no evidence left to give in answer to the question, quietly stops asking.",

    "The sequence, in slow motion, looks like this. <b>(1)</b> The Ambassador moves through the world giving — warmth, service, attention — because giving feels like love, and love feels like the answer to the question <i>am I lovable?</i> <b>(2)</b> A disconnection occurs: someone is absent in a way that registers. <b>(3)</b> The trigger fires. <b>(4)</b> The core question wakes: <i>am I lovable?</i> <b>(5)</b> The Ambassador responds by giving more, because this has worked before. <b>(6)</b> It does not work this time. The warmth does not return. The question stays open. <b>(7)</b> At some point, without announcement, without drama, without anyone on the outside noticing, the giving quietly stops producing hope. The energy that moved toward the relationship begins to redirect. The Quiet Exit has begun. <b>(8)</b> Because it looks like peace — because the Ambassador is now gentler, not harsher — no one notices. And the departure continues.",

    "What breaks this sequence is not more giving and it is not better emotional management. It is a different answer to the question. Until the Ambassador receives — really receives, not as doctrine but as lived reality, at the level where the giving happens — that the love he is looking for has already been given without condition and without ledger, the loop has nothing to push against. With that answer received and practiced, slowly, the Ambassador begins to give from a different place. Not to earn. Not to keep the warmth up. To share what has already been given to him. And the Quiet Exit, which has been closing on a story God has not yet finished, begins, slowly, to open again.",

    "Fill in your sequence below. Read it aloud when you are done. Both the Ambassador and the Quiet Exit lose a measure of their power when they hear themselves named in your own voice.",
]

TWO_TOG_TEMPLATE = (
    "When I experience ____________________, something in me reads it as disconnection "
    "and the old question wakes up: <i>am I lovable?</i> My first move is to "
    "____________________, because the Ambassador in me believes that if I can "
    "____________________, the warmth will return and the question will quiet. When that "
    "does not work, and the giving produces nothing, I begin to ____________________. "
    "The Exit feels like ____________________, but what it actually is, underneath, is "
    "____________________. What I most need to receive, in that moment, is not more "
    "to give but the truth that ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of practices, each honest enough to use and simple enough to carry. None of them will fix the Ambassador's pattern in a single season. All of them, practiced over months, will loosen the grip of the loop you have just named.",

    "I have divided them into two sets: tools for when the Ambassador is overworking its giving (when service has tipped from love into survival), and tools for when the Quiet Exit has begun or is beginning (when hope has been quietly leaving and the door has begun to close). The Ambassador's tools come first, because the Exit cannot be addressed well until the mechanism underneath it is understood and, to some degree, interrupted.",
]

AMB_TOOLS = [
    ("The honest inventory",
     "Once a week, ask one question: <i>In the past seven days, was there anything I gave in order to secure love rather than to express it?</i> Do not scold yourself for what you find. Simply name it, plainly, in your journal. The Ambassador loses a measure of his automatic power when he is required, once a week, to account honestly for his own motives. The naming is not condemnation. It is the beginning of freedom."),

    ("The gift received",
     "Each day, practice receiving something from someone without immediately giving something back. A compliment. An offer of help. A text that says you are thought of. Let it land without deflecting, qualifying, or turning the attention back to them. The Ambassador is very practiced at giving and very unpracticed at receiving. The gospel's word to you is that receiving is not weakness. It is obedience — the obedience of a son who accepts what a Father has given."),

    ("The handed-back ledger",
     "Each evening, name one thing you gave today that you secretly hoped would be noticed or returned. Then say, aloud or in writing: <i>Lord, I hand this entry to you. The account is yours to keep. I am not the treasurer of this love.</i> The Ambassador has been keeping a ledger on God's behalf. This practice is the small, daily discipline of returning it."),

    ("The unexpressed need",
     "Once a week, identify one genuine emotional or relational need and express it directly to someone, without framing it as concern for them, without softening it into a question about their wellbeing. The question <i>am I lovable?</i> cannot be answered while you are managing the answer by making yourself useful. Asking a need is the first act of allowing someone to love you without your having earned it."),

    ("The Abba prayer",
     "Before you have done anything for anyone today, sit for five minutes and say: <i>Father, I am your child. Not your employee. Not your servant-for-hire. Your child. I am loved before I have given anything this morning.</i> The Ambassador serves from morning to night. This practice establishes the right order: loved first. Serving second — and from a different place."),
]

VERD_TOOLS = [
    ("The exit inventory",
     "When you notice the Quiet Exit beginning — when you catch yourself caring less, hoping less, investing less in a specific relationship — write down its name. Then write two sentences: (1) <i>The evidence I am holding.</i> (2) <i>The verdict I have been writing.</i> Seeing the verdict in writing is often the first time the Ambassador recognizes it as a verdict rather than a neutral conclusion. Verdicts require authority. Ask yourself honestly: whose authority is this?"),

    ("The hope question",
     "Ask yourself: <i>When did I stop hoping here? Was that a moment I received — in which God gave me settled peace that this season was over — or a moment I chose, because hoping had become too costly?</i> Write the answer. The difference between those two origins is the difference between a God-given limit and the Quiet Exit. Name it accurately, because each requires a different response."),

    ("Tell one person the door is closing",
     "The Quiet Exit lives on privacy. It is a verdict rendered alone that becomes permanent because no one ever spoke into it. Before the door closes, tell one trusted person — your spouse if possible, a pastor, a friend who knows you — that you have been pulling back. Not to fix it in that conversation. Simply to break the secrecy. The Exit loses power when it is exposed to light."),

    ("The 1 Corinthians 13 test",
     "Sit with this: <i>Love hopes all things.</i> (1 Corinthians 13:7) Ask: <i>Am I hoping here, or have I stopped?</i> If you have stopped, ask further: <i>What would it cost me to hold the door open for one week — not to expect a particular outcome, but simply to refuse the sealed verdict for seven days?</i> One week of deliberate hope is not naivete. It is obedience to the shape of love Paul describes."),

    ("The confession that fits",
     "When you recognize the Quiet Exit in yourself, the appropriate response is not self-condemnation but confession: <i>I have been writing a verdict that was not mine to write. I have allowed hope to leave without asking you whether you were finished. I hand this back to you.</i> Then wait. The Ambassador is not accustomed to waiting without doing something. Practice the waiting."),
]

PRAYER_BODY = [
    "Father,",

    "You see the Ambassador in me, and you do not despise him. You know what he was built for — you know which silences, which withdrawals of warmth, first taught him that giving was the only language in which he knew how to ask whether he was loved. Thank you that he has kept me in relationship across many years of faithful, costly service. He has not been nothing.",

    "But something in me has been writing a verdict for a long time — quietly, with no announcement, with no one knowing. The verdict says: <i>I have given enough to know it is not coming back.</i> I confess I rendered it alone, without asking you, in the privacy of a soul that learned to manage its own accounts. Forgive me. Teach me the difference between the grief you give and the verdict I write. Give me the courage to hold the door open a little longer than the evidence says I should, because you have not yet issued the final statement on this story.",

    "Lord Jesus, you are the one who, on the night of your betrayal, did not quietly withdraw from the men who were about to scatter. You broke bread with them. You called them friends. You gave from a place so secure that nothing could make you keep score. That is the love I need to be loved into. I cannot manufacture it. I can only receive it, and then begin to give from it.",

    "Holy Spirit, where the Exit has already begun — where the door is closing and I have been too composed to admit it — would you be the one who calls me back before it seals. Give me the particular courage of 1 Corinthians 13: to hope all things, not by my own resources, but by yours.",

    "In the name of the One who loved to the end — who did not exit, not even in the garden — I pray.",

    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Ambassador and the Quiet Exit have been with you a long time, and they have roots that run deeper than one afternoon's reading. What follows is a short list of next steps — some immediate, some longer-term — for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.",
     "Different sections will land differently. The Ambassador will resist a second reading — he prefers to receive information, file it, and then go check on someone else. The Quiet Exit will tell you there is nothing new to find. Both are wrong. Come back in a month."),

    ("Take one tool, not six.",
     "Choose a single practice from Section 7 — particularly from the tools for the Quiet Exit — and try it for two weeks before adding another. The Ambassador will want to apply all of them systematically and generously. That impulse is worth noticing."),

    ("Name the door that is closing.",
     "Tell one trusted person — your spouse, a pastor, a close friend who knows you — the name of the relationship in which the Exit has begun. Not to fix it in that conversation. Simply to break the secrecy. Say: <i>I have been pulling back from ___, and I wanted someone to know before the door closes all the way.</i>"),

    ("Sit with 1 Corinthians 13 again, slowly.",
     "Read it once through and stop at verse 7: <i>love hopes all things.</i> Sit with that phrase for ten minutes. Ask: where have I stopped hoping? Then ask the harder question: is this a hope God has set aside, or one I closed on my own?"),

    ("Read further on the love that frees.",
     "Tim Keller, <i>The Prodigal God</i> — his reading of the elder brother in Luke 15 will name the specific shape of the Ambassador's weariness with great precision and great pastoral care. C. S. Lewis, <i>The Four Loves</i> — especially his chapter on affection and the ways in which affectionate love, when it becomes need-love, begins to demand rather than give. Both are faithful companions for the particular work this walkthrough has begun."),

    ("If you are stuck, ask for help.",
     "For the Ambassador specifically, asking for help is one of the most countercultural things this walkthrough can recommend. You are the one who helps others. Asking someone — a wise pastor, a Christian counselor, a friend who knows you well — to help you is not weakness. For you, it is one of the most specific acts of faith available."),
]

GOING_FURTHER_CLOSING = (
    "You are not a person who ran out of love because you were selfish. You are a person who gave love "
    "faithfully, for a long time, from a well that was never meant to be your only source. "
    "God does not despise the exhaustion of the faithful. He meets you there. "
    "The One who began the good work in you will be the one to finish it, "
    "and he has not yet issued the final statement on the story you are in."
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
        [Paragraph("WAS MY SOUL IN DANGER?", header_style), Paragraph("the deeper, truer question", sub_style)],
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
    """Generate the Ambassador+Verdict (Quiet Exit) walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='AMB', primary_breakdown='VERD',
    primary_trigger='DISC', core_question='LOV'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="AMBASSADOR  \u00b7  QUIET EXIT",
        title="Take 139 Walkthrough \u2014 Ambassador + Quiet Exit",
    )

    story = []

    # ── COVER ──
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor\u2019s<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the way<br/>you have learned to keep yourself safe.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph("The Ambassador &nbsp;\u00b7&nbsp; The Quiet Exit", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disconnection &nbsp;\u00b7&nbsp; Core Question: Am I lovable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cLove bears all things, believes all things,<br/>"
        "hopes all things, endures all things.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "1 Corinthians 13:7",
        ParagraphStyle("cqa", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: Opening ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read this slowly. The chapter that follows has been a long time in the writing.")
    for p in OPENING_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 2: Trigger ──
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TRIGGER",
                   "Disconnection.",
                   "The moment the warmth disappears, and what your soul makes of it.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will manage the question. Your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 3: Core Question ──
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I lovable?",
                   "The wound the alarm has been guarding.")
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
                   "The caretaker. The peacemaker. The one who manages the temperature of every room.")
    for p in AMB_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in AMB_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in AMB_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Ambassador.",
                   "Read the Ambassador\u2019s own words. He has been faithful; let him speak.")

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
                   "The Quiet Exit.",
                   "The saddest of all the Verdict breakdowns \u2014 and the one most disguised as peace.")
    for p in VERD_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>Unbelief wearing the costume of wisdom.</b>", S["H3"]))
    for p in VERD_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The crucial distinction.",
                   "God-honored grief versus premature verdict \u2014 and how to tell them apart.")
    for p in VERD_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions before you turn the page.",
                   "Write the honest answer, not the pastoral one.")
    for prompt in VERD_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=5)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same wound, in two phases.",
                   "Ambassador and Exit are not two problems. They are one loop.")
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
                   "Five practices for the time before the Exit begins.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    for name, desc in AMB_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Quiet Exit has begun.",
                   "Six practices for interrupting the departure before it seals.")
    for name, desc in VERD_TOOLS:
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
        primary_breakdown = "VERD"
        primary_trigger = "DISC"
        core_question = "LOV"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "ambassador_verd_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages using pypdf
    import io
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(reader.pages)
        # Get a snippet from the letter/text page
        snippet = ""
        for page in reader.pages[1:3]:
            txt = page.extract_text() or ""
            if txt.strip():
                snippet = txt.strip()[:120]
                break
    except Exception:
        page_count = "unknown"
        snippet = ""

    print(f"DONE: ambassador_verd.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
