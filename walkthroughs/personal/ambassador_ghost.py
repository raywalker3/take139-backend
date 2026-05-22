"""Personal Walkthrough — Ambassador + Ghost.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disconnection trigger, "Am I lovable?" core question.
Mechanism: Ambassador (AMB) — caretaker, peace-maker, manages temperature of every room.
Breakdown: Ghost (GHOST) — performs normalcy, goes silent, waits to be discovered.
~25 pages, 9 sections.

Calibration note: The Ambassador+Ghost is the most tragic of the Ghost breakdowns
because the Ambassador has spent a lifetime ensuring nobody around them experiences
this exact thing — silent withdrawal, the cold shoulder, "I'm fine" — and now the
Ambassador is doing it themselves. The plates are still hot, but the kitchen has gone quiet.

Section Five's unique pastoral move: the Ambassador's Ghost is a particularly devastating
betrayal of the Ambassador's own gift — the same person who would never let someone they
loved feel unseen has, by silently withdrawing, made the person they love feel exactly that.
Romans 7:15-19 (Paul: "the very thing I hate, that I do") — the moral confusion of seeing
yourself do what you would never tolerate from another. Lewis, Mere Christianity, on the
difference between feeling and willing.
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
    "Before you read any further, I want to do what a good pastor does at the beginning of a hard conversation. I want to slow things down. I want to lower the lights, because what you are about to look at is not a list of your tendencies or a profile of your strengths. It is the architecture of your soul's attempt to stay loved in a world that has not always loved you well.",
    "You have almost certainly been the person who kept the peace. You were the one who remembered what the room needed, who noticed who had gone quiet and found them before anyone else thought to look. You brought the warmth that others drew from, and you did it, more often than you would like to admit, without anyone thinking to ask whether you yourself were running low. People have told you that they feel safe around you, that you have a gift for making people feel seen. All of that is true. None of it is the whole truth.",
    "<b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father whose love for you is not a function of how useful you have been or how warm you have managed to stay; a Son who washed the feet of the man who was about to betray him and called him friend, not as a performance but as a demonstration of a love that does not require anything back; and a Spirit who is, at this very moment, praying for you with a love you did not have to generate and cannot lose.",
    "So read slowly. When something catches in your chest — when a sentence lands and you are not entirely sure whether what you feel is relief or grief or recognition — it is probably all three, and that is the Lord saying, <i>look here, with me.</i> The goal is a slightly freer life, in which you give because you have already been given to, rather than giving in order to discover whether you are worth giving to. Take your time. What you are about to read has been a long time in the writing.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life have no idea it is occurring — not because they are careless, but because you have learned, over a long time, not to show it. Your spouse has been quiet since dinner, somewhere else in themselves that you cannot reach. A friend has not replied in three days. Something real you gave went unremarked, received the way furniture is received. Or a gathering ran warmer for others than it did for you, and you stood just outside the radius of it and no one noticed.",
    "On the surface, none of these qualify as catastrophes. You may not show it. You may be the one who, in the next breath, asks how the other person is doing and moves things forward with the warmth you are very good at generating. But inside, something has registered — a quiet, precise, cold signal: <i>the connection has closed.</i> And the Ambassador, who has spent a lifetime managing the temperature of every room, feels the temperature drop in a way that no one else in the room has detected.",
    "This is your trigger. The word for it is <b>disconnection</b> — and for the Ambassador it is not merely an absence of contact but the withdrawal of warmth from someone whose warmth you rely on. C. S. Lewis, in <i>The Four Loves</i>, observed that love of every kind makes us vulnerable in proportion to the size of the love — that the more we love, the more we expose the part of ourselves that can be hurt by the loss of what we love. For the Ambassador, this vulnerability is specific and acute. Disconnection does not feel like a neutral condition. It feels like a signal that something about you has been found wanting.",
    "The question that rises underneath the trigger is not <i>why is the room quiet tonight</i> but something much older: <i>did I do something? Is it me? Are they leaving?</i> The Ambassador's nervous system does not experience emotional distance as a weather event that will pass. It experiences it as information about lovability.",
    "<b>Your sensitivity to disconnection is not random.</b> It is the residue of moments — usually early, usually repeated, sometimes only a small number but entirely unforgettable — in which the love you most needed turned inconsistent. Perhaps warmth came when you were helpful and receded when you were not. Perhaps you learned early that having needs of your own drove people back, and so you converted your own longings into service, your own hunger for love into care for others, and found that this kept the warmth coming. The lesson that lodged in you was this: <i>love is something I maintain by giving, not something I simply receive by being.</i> And so the Ambassador gave. And kept giving. And became very good at it.",
    "Before we go further, I want you to write two things down. Not in your head — your head will manage the question, frame it skillfully, and move to the next one. Your hand will be more honest. Take whatever time you need.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week or two, that the disconnection signal fired. What happened, in two sentences? You are looking for the moment your internal temperature dropped — not necessarily a dramatic event, but the moment something inside you said <i>the warmth is gone.</i>",
    "How large was the actual event? How large was the response inside you? If the response was larger than the event, you have just located your trigger. Write both sizes down, even approximately.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is almost always older than the trigger by a decade, sometimes more. The trigger is the alarm; the question is the wound the alarm was installed to guard. The Ambassador has been guarding this one for a very long time, and guarding it so quietly and so skillfully that most of the people who know you have never heard it.",
    "Yours is this: <b>Am I lovable?</b>",
    "I want to be careful here, because that question is easy to underestimate. It is not the same as <i>Am I loved?</i> — you have received love, you know it, and yet the question has not gone away. It is more frightening than that, and more specific. The question is: <i>Am I the kind of person who is loved for what I am, rather than for what I do?</i> If I stopped serving, stopped warming, stopped being the indispensable one — would anyone stay, simply for me?",
    "For most adults, this question has been moved underground — buried under sufficient activity that it does not speak clearly during the daylight hours. For the Ambassador, it speaks in the silences: in the spouse's quiet evening, in the friend's delayed reply, in the gathering where the warmth flowed more easily to others. And in those silences, the nervous system's verdict is not neutral: <i>see? Even after everything you have given, the connection can simply disappear. This is what you suspected all along.</i>",
    "There is a particular urgency in this question for you, because the Ambassador has organized so much of life around answering it through behavior. You have been generous, present, attentive. You have taken care of people in ways that cost you real time and real energy. And the hope underneath all of that giving — the hope you may never have quite put into words, even to yourself — is that love given faithfully enough, warmly enough, sacrificially enough, will eventually produce a love that is stable and sure and not contingent on anything you do next.",
]

QUESTION_BODY_P2 = [
    "There is a reason that Augustine, at the very opening of his <i>Confessions</i>, located the restlessness of the human soul not in unfulfilled ambition or unresolved philosophy but in the absence of God: <i>our heart is restless, until it rests in Thee.</i> What Augustine was describing is not merely an intellectual hunger. It is the longing of every creature for a love that is permanent and unconditional — a love whose warmth does not depend on the creature's next act of service. The Ambassador's deep restlessness is a version of this longing, wearing relational clothes.",
    "The Psalms take this longing seriously. Psalm 103, written by David out of a life that had tested the question thoroughly in every direction, begins with what sounds like an interior memo to a wavering soul: <i>Bless the Lord, O my soul, and all that is within me, bless his holy name! Bless the Lord, O my soul, and forget not all his benefits — who forgives all your iniquity, who heals all your diseases, who redeems your life from the pit, who crowns you with steadfast love and mercy.</i> (Psalm 103:1-4) That word at the center — <i>steadfast</i> — is the Hebrew word <i>hesed</i>, the covenant love of God, the love that does not depend on the beloved's performance. This is the word the Ambassador's soul has been looking for in every room it enters.",
    "The gospel's answer to <i>Am I lovable?</i> is precise and theologically careful. It is not <i>yes, because of who you are</i> — which would be sentimentality, and God does not traffic in sentimentality. It is not <i>yes, if you continue to serve faithfully</i> — which would be the exact treadmill you are already on. The answer is this: <i>you are loved not because you are lovable but because you are in Christ — and in him, the love the Father has for the Son flows over to you, without condition and without end.</i> Paul names it in Romans 8:15: <i>you did not receive the spirit of slavery to fall back into fear, but you have received the Spirit of adoption as sons, by whom we cry, 'Abba! Father!'</i>",
    "But I want to say something honestly, because pastoral honesty demands it. The Ambassador hears this good news and nods. You may feel it, briefly and genuinely, and then set it aside to go check on how the rest of the room is doing. The reason this answer does not fully land for you is not that the theology is unclear. It is that receiving requires stopping. It requires sitting still long enough for the love to settle rather than managing the moment before it does. The hardest thing this gospel answer asks of the Ambassador is not understanding. It is rest.",
]

QUESTION_BODY_P3 = [
    "The honest work for you looks like this. The Ambassador has been trying to earn, through consistent and costly service, the security that comes only from being given to. This is a loop that cannot be closed by any amount of giving, because the question underneath it is not <i>have I given enough?</i> but <i>am I loved?</i> — and more giving is not the answer to the second question.",
    "Galatians 4:7 says it plainly: <i>so you are no longer a slave, but a son, and if a son, then an heir through God.</i> An heir does not earn the inheritance. An heir receives it — simply by being in the family. The Ambassador has been functioning as a servant, working for a standing that was given freely. The cross is where the giving happened — not gradually, not conditionally, but once and completely, at a cost you did not pay and could not have paid. What you are is not an employee whose tenure must be maintained. You are an heir. And heirs do not earn what they already have.",
    "Before we close this section, use the table below for honest observation — not analysis at a distance, but the kind of specific memory that tells the truth before the mind has time to soften it.",
]

AMB_BODY_P1 = [
    "You have built something. You did not decide, one particular morning, to become the person who manages the emotional temperature of every room. It happened the way most significant things happen — gradually, in response to real circumstances, through small decisions that were rewarded often enough to become a pattern. But it is a structure now, and we are going to spend this section walking through it carefully, because understanding it is the first step toward being free from the part of it that is not serving you.",
    "The <b>Ambassador</b> is a soul who has learned — usually early, usually in a specific household, sometimes in a single defining relationship — that love is something that must be maintained through service. The Ambassador does not experience love as a stable ground beneath the feet. The Ambassador experiences love as something more like a temperature that must be managed, a room that will cool if no one tends the fire. If the Ambassador is attentive enough, warm enough, giving enough, the temperature stays up. If the Ambassador gets tired, goes quiet, has a need of its own — the temperature drops. And dropping feels dangerous.",
    "The Ambassador is not a manipulator. The warmth is genuine. The care for others is real. When you ask the person you love how they are doing, you actually want to know. You notice things about people that they have not mentioned. You track the relational weather of the rooms you inhabit with a precision that most people around you simply do not have. This is a genuine gift. Proverbs 15:1 says, <i>a soft answer turns away wrath, but a harsh word stirs up anger.</i> The Ambassador has known this truth in the bones since before they could read it off a page. You have prevented more damage in more relationships than you will ever be able to count, simply by knowing how to enter a tense room and reduce the temperature to something livable.",
    "But there is something underneath the gift that we must name, because not naming it is exactly the kind of thing the Ambassador does, and it has gone on long enough. Underneath the genuine warmth is a strategy — put in place long before you had words for it — that says: <i>if I am the most caring person in the room, I will not be left behind.</i> The giving and the fear are not fully separate. They are, at the root, drawing from the same well.",
]

AMB_BODY_P2 = [
    "J. C. Ryle, writing on the dangers of self-deception in the Christian life, observed that the soul is capable of doing very righteous-looking things for very unrighteous reasons, and that the danger is not in the behavior itself but in the root from which it grows. The Ambassador's giving looks like love — and much of it genuinely is love — but at the root, hidden from almost everyone including the Ambassador, is a transaction. The giving is partly love. The giving is also partly insurance: <i>if I am indispensable enough, I cannot be discarded.</i>",
    "The people who love you have probably sensed something they cannot fully name. They know you are generous. But they may also have a feeling — difficult to articulate, almost guilty to admit — that there is a slight weight to the giving. That after you have given a great deal, something in the air quietly expects a return. They cannot point to the moment you said it, because you have never said it. But the expectation is there, and they feel it, and when they inevitably fail to meet it — because they are human and tired and preoccupied, as we all are — something happens in you that they usually never see. Because the Ambassador does not show what happens next.",
    "<b>The Ambassador is not your enemy.</b> He is a younger version of you who learned, in some real circumstance, that warmth was the price of connection and that withdrawing the warmth meant risking the connection. He has been faithful. He has kept you in relationship, kept the rooms you inhabit livable, kept people who would otherwise have drifted from turning away. He deserves your gratitude, not your contempt. But he has been running the emotional budget of your life on a model that cannot sustain itself: giving out more than comes in, keeping the ledger invisible, hoping no one will notice the deficit — including himself.",
]

AMB_BODY_P3 = [
    "What does retirement look like for the Ambassador — in the dignified sense of the word? Not eliminating the warmth, which is real and necessary and the world genuinely needs it. But beginning to disentangle the giving from the earning. Beginning to serve from a place of security rather than from a place of need. Beginning, which will feel strange at first, to allow yourself to be cared for with the same openness with which you care for others.",
    "It begins by naming the assumption the Ambassador has been operating under: <i>I am safest when I am giving. My worth in this relationship is proportional to my usefulness to it.</i> This is not merely an emotional pattern. It is, examined in the light of the gospel, a quiet but genuine rejection of grace. It says: <i>I must earn my place.</i> The gospel says your place was secured before you gave anything. The Ambassador has believed this doctrinally. He has not yet believed it at the level where the giving happens — in the early morning, before the phone is checked; in the pause before the act of service, where the motive is formed; in the moment when someone asks how he is doing and he redirects the question to them, because having a need feels like losing ground.",
    "What follows is a letter written in the Ambassador's voice — from him, to you. It is a model of the kind of honest reckoning this section is asking you toward. Read it slowly. He has been faithful, and he is tired, and he has never quite had this conversation before.",
]

AMB_LETTER_LINES = [
    "Dear Friend,",
    "I have been doing this longer than you realize, and I have been doing it quietly enough that neither of us has had to look at it directly. I learned early that the temperature of a room was something I could influence. I learned that my presence, when I managed it carefully, could make things better — could keep people from leaving, could prevent the particular silence that felt like abandonment. And so I learned to manage it. I became good at it. And I told myself, honestly, that I was simply a loving person.",
    "What I did not tell you — what I have perhaps not told myself — is that I have been keeping a record. Not of grievances; not of wrongs done to me. A record of the other kind: of warmth given, of effort offered, of rooms tended that would have gone cold without me. I did not decide to keep it. I simply noticed, somewhere underneath everything, that the giving was accumulating, and that the question of whether it was being received was always present, quiet and patient, waiting to be answered.",
    "I want to tell you what I am most afraid of. I am afraid that if I stop, the room will cool and no one will notice that it was I who had been keeping it warm. I am afraid that my presence in this relationship is loved for what it produces, not for what it is. I have been trying, faithfully, to make that impossible to believe — to make myself so consistently warm and giving and available that the question of whether I am loved for what I am simply cannot arise. But the question arises anyway, usually in the silences, usually when I have done everything I know how to do and the warmth still comes back thin.",
    "I am more tired than I have admitted. And I want something I have not asked for, because asking feels like the one thing I cannot afford: to be given to, simply, without having earned it first. To sit still long enough to receive something without immediately finding a way to give it back.",
    "The Ambassador",
]

AMB_LETTER_PROMPTS = [
    "Which sentence in the Ambassador's letter lands most heavily? What does that tell you about where his fear is sharpest right now?",
    "The Ambassador says he has been keeping a record of the giving. Name one specific relationship or season where this was true. What was on the list, and for how long had it been accumulating?",
    "What would the Ambassador need to believe — really believe, at the level where the giving happens — in order to give without keeping score? What specific gospel truth would have to move from his head to the place where his fear lives?",
]

GHOST_BODY_P1 = [
    "Every mechanism has a place it breaks — a point where the strategy runs out of room and something else takes over. For the Ambassador, that place has a name, and we are going to spend this section naming it clearly, because it is the section that most people in your profile have never had named for them. The breakdown is called <b>the Ghost</b>.",
    "Here is how it happens. The Ambassador has been doing what the Ambassador does: giving, warming, managing, tending. The emotional temperature of the relationship has been maintained largely by the Ambassador's labor, though no one has a clear account of this, including the Ambassador. Then something happens. A wound. Not always a catastrophe — in fact, often something that would look very small to an outside observer. Your spouse says something dismissive when you expected warmth. A friend you have given a great deal to forgets something that mattered to you. A moment when you needed to be seen and you were not. The disconnection signal fires. The core question wakes up: <i>am I lovable?</i> And the Ambassador does what the Ambassador always does: tries to warm things up. Gives a little more. Smooths the moment over. Asks how they are doing.",
    "This time, it does not work. The wound stays open. The giving does not close the gap. And here, in this specific moment, the Ambassador does something the Ambassador does not do voluntarily and would not endorse in anyone else. The Ambassador goes quiet. Says, if asked, <i>I'm fine.</i> Continues. Functions. Participates in the relationship with enough warmth and enough presence that nothing in the room looks wrong. But something has gone underground. The kitchen is still putting out plates, but the cook has left the building.",
    "This is the Ghost. And in the Ambassador, it is a particularly important thing to see clearly, because of what it costs and because of the specific betrayal it involves — a betrayal the Ambassador will feel as acutely as anyone, once it is named.",
]

GHOST_BODY_P2 = [
    "The Ghost, in its simplest description, is a performance of normalcy over a live wound. The Ambassador has gone silent on the inside while continuing to function on the outside, waiting — with a patience that looks, from the outside, like composure — to be found. The Ghost wants to know whether the person who wounded them will notice. Will they come looking? Will they read the signal? Will they prove, by coming, that the Ambassador matters enough to pursue?",
    "This is the Ghost's most honest sentence, and I want you to hear it plainly: <i>If they have to be told, it doesn't count.</i> Which means the Ghost is not looking to have the wound addressed. It is looking for the unsolicited proof that the Ambassador is worth noticing when something is wrong — the very thing the Ambassador has spent a lifetime providing for everyone else. The Ambassador has always come looking. Has always noticed the slight decrease in temperature, the small withdrawal, the almost invisible sign that someone is not quite present. The Ghost, now, is asking to be noticed the same way the Ambassador has always noticed others.",
    "There is a cruelty in this that Paul names with unusual directness in Romans 7:15-19. Writing about the experience of seeing yourself do the very thing you hate, Paul says: <i>For I do not do what I want, but I do the very thing I hate. . . . For I do not do the good I want, but the evil I do not want is what I keep on doing.</i> This is the specific confusion of the Ambassador who has, all their life, made it their business to ensure that no one they love ever feels unseen — and who is now, by going silent, making the person they love feel exactly that. The Ambassador would never tolerate this in someone else. And yet, in the moment of deepest wound, this is what the Ambassador produces.",
    "C. S. Lewis, in <i>Mere Christianity</i>, makes a distinction that is directly useful here. He observes that the feelings we have are not always in our control — resentment, hurt, the impulse to withdraw may arise whether we choose them or not. But what is in our control, what faith actually addresses, is not the feeling but the will: the will to speak when the feeling says be silent, the will to come toward someone when the wound says withdraw. The Ambassador has enormous capacity to will warmth in the presence of contrary feelings. The Ghost is the moment that will has given up. It is not a character flaw. It is an exhaustion.",
]

GHOST_BODY_P3 = [
    "What makes the Ambassador's Ghost so difficult to see is that it occupies the exact shape of health. The Ambassador continues to function. The warmth does not disappear entirely. Nothing in the room looks wrong. Nothing can be pointed to. The person on the receiving end senses, if they are perceptive, a slight decrease in presence, a barely detectable shift in how fully the Ambassador is with them. But they cannot name it, because nothing happened.",
    "What the Ambassador has been holding, privately, is that everything happened.",
    "D. Martyn Lloyd-Jones, in his exposition of the Sermon on the Mount, wrote about the spiritual danger of nursing a wound in secret — of tending a grievance so carefully that it becomes more important than the relationship it lives inside. He was not dismissing the reality of the wound. He was naming what happens to a wound held in silence long enough: it hardens. The Ghost's silence is not neutral. It is a slow trial, conducted without the other person's knowledge, in which their failure to notice becomes the evidence of their guilt.",
    "<b>The Ghost has never once succeeded in getting what it is looking for.</b> The Ambassador's Ghost asks the person they love to find something they do not know they are looking for, to pass a test they do not know they are taking. When they fail — as they will, because they do not read the room with the Ambassador's precision — the Ghost concludes what it already suspected: <i>see? Even the person I love most cannot find me when I go quiet. This is what I feared.</i> The silence does not produce discovery. It produces the distance it was meant to test against.",
    "There is one more thing to name here, and I want to name it with the care it deserves. The Ambassador's Ghost is not simply painful. It is a betrayal of the Ambassador's own gift. The same person who could walk into any room and find the one who had withdrawn — who would have gone looking for exactly this silence in anyone else they loved — has, by going silent themselves, done to the person they love the one thing they have always known was intolerable. The gift has turned on the giver. The Ambassador has become the cold shoulder, the <i>I'm fine</i>, the unseen withdrawal that the Ambassador has spent a lifetime refusing to inflict on anyone else.",
]

GHOST_PROMPTS = [
    "Think of the last time the Ghost appeared in you — a time when you were genuinely hurt, said or showed <i>I'm fine</i>, and meant something entirely different. What happened? Who was in the room? What were you actually waiting for them to do?",
    "Did they come looking? If they did: was it enough, or did part of you move the standard? If they did not: what did that silence tell you, and what did you do with what it told you? Write this honestly — not the version that makes you look composed, but the version that was actually happening inside.",
]

TWO_TOG_BODY = [
    "Now we place them side by side, because the Ambassador and the Ghost are not two separate problems that arrived in sequence. They are the same wound, in two different postures. One posture gives without stopping. The other goes silent without warning. Both are trying to answer the same question. Neither has ever fully succeeded.",
    "<b>The Ambassador is what your need does when it has energy and strategy.</b> The Ghost is what your need does when the strategy has been tried and has failed. The Ambassador warms the room. The Ghost haunts the room after the warmth stopped working. The Ambassador gives in order to secure love. The Ghost withdraws in order to test whether love will come looking. Together, they describe the full range of a soul that has decided it must answer the question <i>am I lovable?</i> entirely on its own — through service when service is available, and through silence when it is not.",
    "The sequence looks like this. <b>(1)</b> The Ambassador moves through the relationship giving — warmth, service, attention — because giving feels like love, and love feels like safety. <b>(2)</b> A disconnection occurs: the warmth is not returned, something goes unnoticed. <b>(3)</b> The trigger fires: <i>the connection has closed.</i> <b>(4)</b> The core question wakes up: <i>am I lovable?</i> <b>(5)</b> The Ambassador responds by giving more, because this has worked before. <b>(6)</b> It does not work this time. The wound stays open. <b>(7)</b> The Ghost takes over. The Ambassador goes quiet, performs normalcy, and waits. <b>(8)</b> The person who is loved fails to notice — because the Ambassador performs fine-ness so well, and because they do not read rooms with the Ambassador's precision. <b>(9)</b> The Ghost concludes what it feared. The Ambassador retreats, gives again, and the loop prepares to run.",
    "What breaks this loop is not more giving, and it is not a more skillful performance of composure. It is a different answer to the question. Until the Ambassador receives — really receives, not simply affirms as a doctrine — that the love they are looking for has already been given without condition and without ledger, the loop has nothing to run against. With that answer received, the Ambassador begins to give from a different place: not to earn a love that is uncertain, but to share what they themselves have been given. And the Ghost begins to discover that it has already been found.",
    "Use the template below. Write your sequence in your own words. Read it aloud when you have finished. Both the Ambassador and the Ghost lose a measure of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I experience ____________________, something in me reads it as disconnection "
    "and the old question wakes up: <i>am I lovable?</i> My first move is to "
    "____________________, because the Ambassador in me believes that if I "
    "____________________, the warmth will come back and the question will quiet. "
    "When that does not work, the Ghost takes over \u2014 I go "
    "____________________ and wait for ____________________. "
    "What I am actually after, underneath all of it, is the assurance that "
    "____________________ \u2014 an assurance that Christ has already given me in "
    "____________________, and which I do not have to earn or perform to keep."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small collection of tools, each specific enough to be used in an actual Tuesday, in an actual moment when the Ambassador is overworking or the Ghost has already gone quiet. None of them are complete in themselves. All of them, practiced with some patience over months, will begin to loosen the grip of the loop you just named.",
    "I have organized them in two groups: practices for when the Ambassador is overworking its giving — when service has tipped from genuine love into survival strategy — and practices for when the Ghost has appeared — when you have already said <i>I'm fine</i> and something essential has gone underground. The Ambassador's tools come first, because the Ghost cannot be addressed usefully until the mechanism underneath it has been seen.",
]

AMB_TOOLS = [
    ("The honest inventory",
     "Once a week, ask one question before the week closes: <i>In the past seven days, was there anything I gave in order to secure love rather than to express it?</i> Do not condemn what you find. Simply name it. The Ambassador loses much of its automatic power when it is required, once a week, to account honestly for its own motives. The question does not need to produce a long list. One entry, named with honesty, is sufficient."),
    ("The gift received",
     "Each day this week, practice receiving one thing from someone without immediately giving something back. A compliment. An offer to help. A message that says you are being thought of. Let it arrive without deflecting it, qualifying it, or turning the attention immediately back to the person who offered it. The Ambassador is practiced at giving and unpracticed at receiving. Receiving is not passivity. It is the act of faith that says: I believe this love does not require me to match it."),
    ("The handed-back ledger",
     "Each evening, name one thing you gave today that you secretly hoped would be noticed. Then say, aloud or in writing: <i>Lord, I hand this entry back to you. The account is yours. I am not the treasurer of this love.</i> The Ambassador has been keeping the ledger on God's behalf. This small practice is the daily act of returning it to its rightful keeper."),
    ("The unexpressed need",
     "Once this week, name one genuine emotional or relational need — not a need framed as concern for another person, but a real need of your own — and express it directly to someone who loves you. The Ambassador has been asking the question <i>am I lovable?</i> while managing the answer by making itself indispensable. Naming a need is the first act of allowing someone to love you without your having earned it."),
    ("The Abba prayer",
     "Each morning, before you have done anything for anyone, sit for five minutes and say aloud: <i>Father, I am your child. Not your employee. Your child. You love me before I have given anything today. What I do today flows from that; it does not produce it.</i> The Ambassador serves from morning to night. This practice establishes the right order: loved first. Service after. It will not feel natural for several weeks. That is precisely the point."),
]

GHOST_TOOLS = [
    ("Name it before you perform it",
     "The Ghost most often fires in the first sixty seconds after the wound lands. Before you say <i>I'm fine</i>, try to notice that the performance is assembling. You do not have to say everything. But you can say something small and honest: <i>That landed differently than I expected. Can I come back to it?</i> This single sentence, offered in the moment before the silence begins, will do more to interrupt the Ghost than any number of private resolutions to be more open."),
    ("The thirty-six-hour rule",
     "If you have already gone quiet after a wound and you are not yet ready to name it fully, commit to naming something within thirty-six hours. Not a brief. Not the full account. One sentence: <i>I was more hurt by that than I showed.</i> This single sentence, offered to the right person within thirty-six hours, breaks the secrecy that the Ghost depends on in order to run its silent trial."),
    ("Ask one person to come looking",
     "This is the hardest practice on this list, and also the most direct. When you know the Ghost is operating — when you have gone quiet and you are waiting to be found — tell one trusted person: <i>I am not doing as well as I look. I am not ready to talk about it yet, but I need you to know it is happening.</i> This is not asking to be rescued. It is interrupting the test before it produces the verdict the Ghost fears."),
    ("Receive the Lord's pursuit",
     "The Ghost is waiting to be found. The gospel is the announcement that it already has been. Spend five minutes with Luke 15:20 — the father who saw his son when he was still a great way off, and ran. The father did not wait for the right words. He did not require a full accounting of what had gone wrong. He looked, and he ran. When the Ghost has gone silent and is waiting in the dark, this is the story that speaks directly into it. Pray it back: <i>You saw me. You ran. You did not wait for me to find the right way to ask. You came.</i>"),
    ("The will, not the feeling",
     "When the Ghost has taken over and the feeling says <i>stay silent, wait to be found</i>, ask one question: <i>What would I do right now if I believed I was already loved?</i> C. S. Lewis observed in <i>Mere Christianity</i> that the feelings are not always in our command, but the will is. The Ambassador has enormous capacity for willing warmth in the presence of contrary feelings. The practice here is to aim that capacity in a direction it does not usually go: toward asking to be seen, not waiting to be seen."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Ambassador in me, and you do not despise him. You know which rooms he was first asked to manage, which households taught him that warmth was something that had to be earned rather than given. You know the specific moments when giving was rewarded and needing was not. Thank you that he has kept me connected, kept me warm, kept people in my life who might otherwise have been lost. He has not been wrong about everything.",
    "But Father, he is tired. The ledger is heavier than I have admitted, and the model underneath the giving is not the one your gospel runs on. Teach me to give from a place that is not earning but overflowing. Teach me to receive something from someone without immediately converting it into an occasion to give something back. When the disconnection signal fires and the old question wakes up — <i>am I lovable?</i> — let me hear your answer before I hear the Ambassador's. <i>You are my child. The love the Father has for his Son flows to you. It was decided before you gave anything and it cannot be revoked by anything you fail to do.</i>",
    "Lord Jesus, when the Ghost appears in me — when I go quiet while saying I'm fine, when I make the person I love feel unseen by doing the very thing I have always known was intolerable — would you remind me of what Paul confessed in Romans 7: that the very thing he hated was the thing he did. Do not let me make peace with this. Do not let me call the silence composure. Teach me to name the wound before I perform around it. Teach me to come toward the person I love rather than waiting for them to find me.",
    "Holy Spirit, the Ambassador in me serves from morning to night and rarely sits still long enough to be given to. Give me the courage to stop, today, and receive. Give me the courage to say, to someone who loves me, one honest sentence about how I actually am. The warmth in me is real. You put it there. Let it flow now from the security of being loved rather than from the anxiety of having to earn it.",
    "In the name of the One who, on the night he was betrayed, loved freely to the last — who washed feet and broke bread and called his betrayer friend, not as a performance but as the overflow of a love that nothing could diminish \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Ambassador has been managing the room for a long time. The Ghost has been performing composure for a long time. Neither of them will retire after one afternoon's reading, because they were not formed in one afternoon of anything. What follows is a short list of places to go from here \u2014 some immediate, some for the longer road.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.",
     "Different sections will land differently on a second reading. The Ambassador will find many reasons to file this document and go take care of someone else. Read it again anyway. The Ghost will prefer to keep the contents private. Tell one person what you found in it."),
    ("Choose one tool, not six.",
     "Select a single practice from Section Seven and try it for two weeks before adding another. The Ambassador is a strong executor and will attempt all five tools in the first week. That is the Ambassador's strategy for not actually changing \u2014 doing many things adequately rather than one thing deeply. Choose one. Hold it for long enough that it begins to hold you."),
    ("Sit with Romans 8:15-17 for a week.",
     "Read it once slowly each morning for seven days: <i>you did not receive the spirit of slavery to fall back into fear, but you have received the Spirit of adoption as sons, by whom we cry, 'Abba! Father!' The Spirit himself bears witness with our spirit that we are children of God, and if children, then heirs.</i> Ask, on each reading, which word lands most heavily. The Ambassador needs to receive this not as a doctrinal affirmation but as a daily reality."),
    ("Read Tim Keller, <i>The Prodigal God</i>.",
     "Keller's reading of the elder brother in Luke 15 will name, with unusual precision, the spiritual self-deception that attaches to the Ambassador's giving \u2014 the performance of faithfulness that is partly genuine and partly a complaint, the ledger that has been kept while insisting it was not. It is a short book and an important one for you specifically."),
    ("Read C. S. Lewis, <i>The Four Loves</i>.",
     "Especially the chapter on affection and the ways in which affectionate love, when it becomes need-love rather than gift-love, begins to demand rather than give. Lewis is not harsh about this. He is honest about it, which is harder and more useful."),
    ("If you are stuck, ask for help.",
     "For the Ambassador, asking for help is one of the most theologically significant things this walkthrough can recommend. You are the one who helps. Asking someone to help you is, for you, an act of faith \u2014 a small, daily rehearsal of the truth that your value in this relationship does not depend on your being the indispensable one. A wise pastor, a Christian counselor, a friend who will not accept <i>I'm fine</i> as a complete answer \u2014 these are not signs of failure. They are the answer to your prayer, arriving in human form."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom "
    "by a Father who has not, in all the years you have been giving, kept any record "
    "of what you owe him. His love for you is not a transaction. It is a gift, "
    "given before you could earn it, held open after everything you have done to deserve "
    "its withdrawal. The Ambassador can rest. The Ghost has already been found. "
    "Go gently with yourself. The One who began the good work in you "
    "will be the one who finishes it."
)


def _three_column_table(rows=7):
    """Three-column journal table for Section 3's reflection exercise."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader_AG2", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub_AG2", fontName="Inter-Italic", fontSize=8.5, leading=11,
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
            "CalloutLabel_AG2", fontName="Inter-SemiBold", fontSize=9, leading=13,
            textColor=ACCENT, leftIndent=12, spaceBefore=2, spaceAfter=4)))
    body.append(Paragraph(text, ParagraphStyle(
        "Callout_AG2", fontName="Inter", fontSize=10.5, leading=17,
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
    """Generate the Ambassador+Ghost walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='AMB', primary_breakdown='GHOST',
    primary_trigger='DISC', core_question='LOV'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="AMBASSADOR  \u00b7  GHOST",
        title="Take 139 Walkthrough \u2014 Ambassador + Ghost",
    )

    story = []

    # ── COVER ──
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor\u2019s<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the way<br/>you have learned to keep yourself loved.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph("The Ambassador &nbsp;\u00b7&nbsp; The Ghost", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disconnection &nbsp;\u00b7&nbsp; Core Question: Am I lovable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cYou have received the Spirit of adoption as sons,<br/>"
        "by whom we cry, \u2018Abba! Father!\u2019<br/>"
        "The Spirit himself bears witness with our spirit<br/>"
        "that we are children of God.\u201d</i>",
        ParagraphStyle("cq_ag2", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Romans 8:15\u201316",
        ParagraphStyle("cqa_ag2", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: Opening ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read slowly. The chapter that follows has been a long time in the writing.")
    for p in OPENING_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 2: Trigger ──
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TRIGGER",
                   "Disconnection.",
                   "The moment the warmth closes, and what your soul makes of it.")
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
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "The heir, not the employee.",
                   "What the gospel says about earning what is already given.")
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
    story.append(_three_column_table(rows=5))
    story.append(PageBreak())

    # ── SECTION 4: Mechanism ──
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Ambassador.",
                   "The caretaker. The peace-maker. The one who manages the temperature of every room.")
    for p in AMB_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in AMB_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "Retiring him, not firing him.",
                   "The slow recovery of the difference between earning and receiving.")
    for p in AMB_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Ambassador.",
                   "Read it as if written from within you. He has been faithful; let him speak.")

    letter_style = ParagraphStyle(
        "AmbLetter_AG2", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for line in AMB_LETTER_LINES:
        story.append(Paragraph(line, letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in AMB_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Ghost.",
                   "The place the Ambassador\u2019s strategy collapses, and the betrayal it involves.")
    for p in GHOST_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in GHOST_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The breakdown that betrays the gift.",
                   "The same person who would never let someone they loved feel unseen.")
    for p in GHOST_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Come out from behind the performance.",
                   "Two questions to sit with before you turn the page.")
    for prompt in GHOST_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same wound, in two postures.",
                   "The Ambassador and the Ghost are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=5)
    story.append(PageBreak())

    # ── SECTION 7: Tools ──
    tool_h = ParagraphStyle("ToolH_AG2", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody_AG2", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "When the Ambassador is overworking its giving.",
                   "Five practices for the time before the Ghost appears.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    for name, desc in AMB_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Ghost has taken over.",
                   "Five practices for after you have already said \u2018I\u2019m fine.\u2019")
    for name, desc in GHOST_TOOLS:
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
        primary_breakdown = "GHOST"
        primary_trigger = "DISC"
        core_question = "LOV"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "ambassador_ghost_test.pdf")
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

    print(f"DONE: ambassador_ghost.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
