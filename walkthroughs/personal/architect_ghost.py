"""Personal Walkthrough — Architect + Ghost.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disrespect trigger, "Am I protected?" core question.
Mechanism: Architect (ARCH) — plans, prepares, anticipates.
Breakdown: Ghost (GHOST) — performs normalcy, goes silent, waits to be discovered.
~25 pages, 9 sections.
"""
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Paragraph, Spacer, KeepTogether, HRFlowable, Table, TableStyle,
    PageBreak, NextPageTemplate,
)

from walkthroughs.base import (
    make_doc, make_styles, finalize_buffer, ensure_fonts,
    section_header, journal_lines, divider,
    PAGE_W, MARGIN_L, MARGIN_R,
    PAPER, INK, ACCENT, MUTED, RULE, HIGHLIGHT_BG,
)


# ──────────── PROSE ────────────

OPENING_BODY = [
    "Before you read any further, I want to do what a careful pastor does at the beginning of a hard conversation. I want to slow down. I want to lower the lights. I want to resist every instinct in both of us to move quickly toward resolution, because what we are about to look at is not a personality profile or a list of tendencies. It is the architecture of your soul's attempt to stay safe in a world that has, at certain key moments, refused to keep you safe.",
    "We are going to name your trigger \u2014 the event that keeps arriving in slightly different clothes, the one that your nervous system registers before your mind does. We will listen for the question underneath that trigger, the one your soul has been asking since you were much younger than you are now. We will walk through the strategy you have built to answer that question yourself, because no one else seemed prepared to. And we will name the place that strategy goes silent \u2014 where it does not fight, does not argue, does not defend, but simply performs. And disappears.",
    "That last part \u2014 the disappearing \u2014 is the reason this particular walkthrough is harder to write than most. Because what you do when you are most wounded does not look like wounding. It looks like composure. It looks like maturity. It looks, from the outside, like someone who has made peace with something they have not made peace with at all. And because it looks like that, the people who love you most may have missed it entirely, for years.",
    "<b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who sees through every performance of fine-ness, who is not deceived by your silence, and who has not \u2014 not once, not for a moment \u2014 stopped coming to look for you. We will get to that. But we must start where you actually are, not where you wish you were.",
    "Read slowly. Stay with what lands. Write when the pen will not keep still. When something catches in your chest and you are not sure whether it is grief or recognition, it is probably both, and that is the Lord saying, <i>look here, with me.</i> The goal is a slightly more honest life, lived in front of a God who is not surprised by anything he finds in you and has not withdrawn his love on account of any of it. Take your time. What you are about to read has been a long time forming.",
]

TRIGGER_BODY = [
    "There is a moment that keeps finding you, and it is usually so small that you would feel faintly embarrassed to describe it out loud. Someone speaks over you in a meeting \u2014 not rudely, just confidently, as if the point you were building toward was already obvious and did not need finishing. Your partner corrects something you said in front of other people. A person you respect gives their full attention to someone else in the room while you are standing right there. A decision gets made about something in your domain without anyone asking you. A colleague uses a tone that lands \u2014 not loudly, not cruelly, just with a particular flatness that tells you that what you said did not carry the weight you intended.",
    "This is your trigger. The technical word for it is <b>disrespect</b>, but the word is doing more work than its four syllables suggest. It is not vanity, though vanity is quick to attach itself to it and make it look like pride. It is something older and more essential than pride. It is the alarm that sounds when your soul reads a signal that says: <i>you have just been told, in this small and very specific way, that you do not matter as much as you thought you did.</i>",
    "C. S. Lewis, in <i>The Weight of Glory</i>, observed that there are no ordinary people \u2014 that every human being we encounter is either being drawn toward a glory that would make us fall down in awe, or else moving toward a ruin that we cannot fully imagine. What he was gesturing at is the extraordinary weight that personhood carries \u2014 and your body knows it. When that weight is dismissed, even carelessly, even by someone who meant nothing particular by it, the signal is real. You have been treated as something less than what you are.",
    "Here is what is essential to see, and to see without flinching: <b>your sensitivity to disrespect is not random.</b> It is the residue of specific moments — usually early, often repeated — in which someone with power over you used it carelessly, and you learned that dignity is not guaranteed. The lesson that lodged in you was this: <i>when I am not honored, something bad is already happening, or about to.</i> And so your system developed a vigilance that has never fully stood down.",
    "Before we go further, I want you to do something simple and somewhat inconvenient. Write two things down. Not in your head \u2014 your head is already twelve moves ahead, preparing a response to what you just read. Your hand is slower, and slower is better here.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week or two, that you felt the disrespect signal fire. Describe the event in two sentences. Just the facts \u2014 what happened, nothing more.",
    "What was the size of the actual event? What was the size of the response inside you? If those two numbers did not match, you have just located the trigger. Write both numbers, even if you can only express them approximately.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question. The trigger is the alarm; the question is what the alarm was installed to guard. And the question is almost always older than the trigger by a decade, sometimes two.",
    "Yours is this: <b>Am I protected?</b>",
    "I want to be careful here, because that question can easily be mistaken for something smaller than it is. It is not primarily asking <i>am I physically safe?</i> \u2014 most of the time you are, and part of you knows it. It is not <i>am I liked?</i> \u2014 that is closer, but it still misses the center. The question is more primal than either of those. It is the question a child asks, usually without words, when the world has behaved unpredictably or when the adults who were supposed to provide a structure of reliability failed to do so. It is the question that runs underneath everything else: <i>Is there someone between me and what could undo me?</i>",
    "You have probably moved this question underground. Adults generally do. The adult version sounds more reasonable: <i>Can I trust this person with what I've told them? Does this organization actually have my back, or are they protecting themselves? Did my spouse hear what I just said, or am I alone in this again?</i> But underneath that sophistication, the original question is still there, still awake, still asking at three in the morning what it was asking at seven years old.",
    "The Psalms \u2014 the prayer book that Israel handed to Jesus and that Jesus prayed from the cross \u2014 will not let this question be dismissed. They take it with the seriousness it deserves. The Psalms are not a collection of people who have resolved this question. They are a collection of people asking it, sometimes desperately, and recording what happened when they brought it to God.",
]

QUESTION_BODY_P2 = [
    "<i>God is our refuge and strength, a very present help in trouble. Therefore we will not fear though the earth gives way, though the mountains be moved into the heart of the sea.</i> (Psalm 46:1\u20132) The psalmist is not writing from calm water. He is writing from within the sound of the mountains giving way. The answer he brings back is not <i>it will probably be fine</i> but something stranger: God is here, now, in this, and nothing can alter the stability of what he holds.",
    "But here is where it gets difficult for you specifically, and I want to say it plainly. <b>The biblical answer to <i>Am I protected?</i> is not the answer your nervous system wants.</b> Your nervous system wants <i>nothing will disrespect you again.</i> It wants the alarm to be permanently decommissioned. It wants the perimeter to be finally secure. Scripture refuses to offer you that. The men and women whose voices fill the Psalms were dismissed, overlooked, mocked, threatened, abandoned, and in some cases killed. The protection they received did not prevent any of that.",
    "What Scripture offers instead is something harder and, in the long run, more sustaining. It offers a protection that runs beneath every event that can happen to you \u2014 a protection not of your circumstances but of your soul, your standing, the thing about you that is finally real. Paul, who understood dismissal and disrespect from the inside \u2014 <i>I have been beaten with rods, stoned, shipwrecked, adrift at sea, in danger from my own people</i> (2 Corinthians 11:25\u201326) \u2014 arrives at a sentence that has been landing like a stone in still water for two thousand years: <i>If God is for us, who can be against us?</i> (Romans 8:31) Not: <i>who can inconvenience us?</i> Not: <i>who can disrespect us?</i> But: who can <i>finally prevail</i> against us? The answer, against all appearances, is no one.",
    "The gospel anchor for the question <i>Am I protected?</i> is this: <b>I am a Creature \u2014 utterly dependent on God, not self-sufficient, not the justice of last resort.</b> God holds the scales. He sees every slight, every dismissal, every moment in which you were handled carelessly. Nothing is hidden from him. You do not have to correct every wrong or prosecute every case, because the thrones are occupied. The Judge has not stepped off the bench. He has not been replaced by your silence or your argument. He is there.",
]

QUESTION_BODY_P3 = [
    "This is where the Architect in you has to do some honest work. Because you have spent years \u2014 with genuine discipline, real intelligence, and considerable sacrifice \u2014 trying to build the kind of life in which the disrespect signal will never have to fire. You have structured your relationships so that your dignity is secured. You have arranged your environments so that unpredictability is minimized. You have earned the competencies, established the credibility, cultivated the reputation, that you believed would finally place you beyond the reach of dismissal.",
    "But it has not worked, has it? And not because you failed \u2014 you have succeeded at an extraordinary level of it. It has not worked because the thing you are protecting against is not, at root, a structural problem. It is a spiritual one. The need to be protected is not met by architecture. It is met by a person.",
    "Psalm 75:6\u20137 says, in the voice of the God who speaks through the psalm: <i>For not from the east or from the west and not from the wilderness comes lifting up, but it is God who executes judgment, putting down one and lifting up another.</i> Your lifting up, your vindication, your protection \u2014 none of it is coming from the structure you have built. It is coming, or it is not coming, from the One who holds the scales and the gavel and the final word on every verdict that has ever been rendered about you.",
    "Receiving that \u2014 not merely affirming it as a doctrine but actually receiving it into the part of you that keeps building and planning \u2014 is the work of years, not days. Before we go further, use the table below. This is an exercise in honest observation, not intellectual distance.",
]

ARCH_BODY_P1 = [
    "You have built something. Over years, through small and unremarkable decisions, through what felt like plain prudence and what your upbringing simply called responsibility, you have constructed a way of moving through the world that we are going to call, throughout this walkthrough, <b>the Architect</b>.",
    "The Architect's operating principle is straightforward and, in many respects, genuinely wise: <i>If I can think this through carefully enough, anticipate the failure modes specifically enough, prepare the ground thoroughly enough, then nothing truly important will go wrong. The people I love will be safe. I will not be caught unprepared. The world will not suddenly expose a gap I did not account for.</i> The Architect believes this not merely as a theory but in his bones, in the way he wakes up at two in the morning to run through the thing he may have missed, in the way his mind, even in a conversation he is enjoying, is already solving for the next three problems.",
    "Scripture does not mock this. Proverbs, the wisdom literature of the ancient church, honors it. <i>The plans of the diligent lead surely to abundance, but everyone who is hasty comes only to poverty.</i> (Proverbs 21:5) Careful preparation is a form of faithfulness. It is what good stewardship looks like. The Architect is not, in himself, a corruption. He is a legitimate gift that has been asked to carry a weight it was never designed to bear.",
    "The weight is this: the Architect has been quietly assigned not merely to build good things, but to ensure that <i>you are never in a position where you can be dismissed, disrespected, or found wanting.</i> That is a much larger job description. And it is a job description that was written by fear, not by wisdom.",
]

ARCH_BODY_P2 = [
    "Tolkien, in his letters about the nature of the Ring in <i>The Lord of the Rings</i>, wrote about the danger of placing one's identity in an external object \u2014 of binding oneself to something that could be taken, lost, or destroyed, such that its destruction would mean one's own unraveling. The Architect has done something like this with his structures. He has placed enough of his soul into his plans and preparations that every threat to a plan feels like a threat to the self. When the blueprint does not hold, he does not merely lose a strategy. He loses ground.",
    "John Owen, the great Puritan theologian, wrote that the soul's deepest misery consists in its attempt to find in created things what can only be found in the Creator. Not because created things are bad \u2014 Owen was not a mystic who disdained the material world \u2014 but because when we assign to them the weight of our security, we have put a creaturely thing in the place of God, and creaturely things will always, eventually, fail under that weight.",
    "The Architect's plan will fail. Not always. Not even usually. But at the specific moments when it matters most \u2014 when the relationship goes sideways despite your careful maintenance of it, when the structure you built absorbs a shock it was not designed to absorb, when someone you trusted and prepared for and invested in acts outside the blueprint \u2014 in those moments, the Architect has no answer. And what he reaches for instead is the Ghost. <b>Hear this carefully, because it is not a condemnation.</b> The Architect is not your enemy. He is a younger version of you who learned, in very real circumstances, that vigilance kept things intact and that lapses in vigilance had costs. He was right, in the world he was formed in. He deserves your respect and something that looks like tenderness \u2014 not contempt. But he is no longer in that world, and the structures he keeps building are, in their deepest motivation, an argument against trusting God with the specific details of your life.",
]

ARCH_BODY_P3 = [
    "The assumption underneath the Architect's constant activity is one that very few people who hold it would state out loud. It goes something like this: <i>God is sovereign over large things. But the small, specific, daily things \u2014 the conversation that could go wrong, the relationship that needs maintaining, the reputation that could fracture \u2014 those are mine to handle. If I do not handle them, no one will.</i>",
    "This is, when you say it plainly, a statement about God. It is a statement that says: his attention is general; mine must be specific. His care is for the arc of history; mine must be for the Tuesday-afternoon meeting. This is the confession hidden in the Architect's perpetual busyness. It is not that he disbelieves in God. It is that he does not yet trust God with the details.",
    "What does retirement look like for the Architect? Not dismissal \u2014 he has been faithful. Not contempt \u2014 he has served real purposes, protected real things. But a gradual, honest reduction of his portfolio. A daily practice of handing back to God the rooms the Architect has been securing on his behalf. It will feel, at first, like negligence. It is not. It is the slow, difficult recovery of the difference between <i>being a steward</i> and <i>being the one who holds everything together by force of will.</i>",
    "Before we move on, I want you to do something unusual. What follows is a letter written as if the Architect himself were writing it to you. Read it in that spirit \u2014 not as something written about you from the outside, but as something written from within you, from the part that has been working this hard for this long. Then the journaling exercise that follows is yours to complete.",
]

ARCH_LETTER = """Dear Friend,

I have been at this longer than you realize. I started quietly, learning to read the variables before they became problems \u2014 because in the world I was formed in, that was what love looked like.

I am afraid of being caught unprepared. I am afraid of the moment someone looks at you and sees that the thing I was supposed to have handled was not, in fact, handled. I have been trying, faithfully, to protect you from that look. What I have not admitted is that I cannot do it. I cannot secure your dignity by building a better structure.

I am ready to hand some rooms back. I am tired, and some of what I have been holding belongs to Someone who is not tired. I will still be here. But let me hold less than the whole thing.

The Architect
"""

ARCH_LETTER_INSTRUCTION = [
    "The letter above was written from within the Architect's perspective \u2014 as a model of the kind of honest reckoning that Section Four is calling you toward. What follows is yours to complete. Use the prompts below in your journal, or in the space provided.",
]

ARCH_PROMPTS = [
    "Looking at the Architect's letter: which sentence lands most heavily, and why do you think that is?",
    "Name one domain where the Architect is currently working hardest, and write the sentence: <i>Lord, I am giving you _____ today. I will steward it; I will not be its god.</i>",
]

GHOST_BODY_P1 = [
    "Every mechanism has a point of collapse \u2014 a place where the strategy runs out of room and something else takes over. For the Architect, that collapse has a name. We are going to call it <b>the Ghost</b>.",
    "Here is how it happens, and I want you to read this slowly because it is easy to miss. The Architect has done his work. He has prepared, anticipated, structured. Then something penetrates the structure. Not necessarily a catastrophe \u2014 in fact, often something that would look minor to anyone watching. Someone dismisses your judgment in front of others. A colleague takes credit for something you built. Your spouse makes a decision without asking you, in an area where your input was implied. A leader you respect does not defend you when you were defensible. Something in the structure that was supposed to protect your dignity has failed to protect it.",
    "Now here is the crucial detail. The Architect's most natural response to a failure is to rebuild \u2014 to diagnose the gap, draft a new blueprint, and repair it. But there are certain failures he cannot rebuild around, because the failure is relational, not structural. You cannot rebuild someone's respect. You cannot draft a contingency plan for someone's contempt. You cannot engineer your way into being handled with care. And so, facing a wound that the Architect cannot fix, you do something the Architect would never do voluntarily.",
    "You go quiet. You say, <i>I'm fine.</i> You continue. You participate. You function. You may even be warm, and from the outside you look entirely present \u2014 like someone who either did not notice, or noticed and handled it gracefully. But you are not present. The part of you that is present is a performance of presence. The real part \u2014 the part that was hurt, the part asking <i>am I protected?</i> at full volume \u2014 has receded into something very quiet and very private, and it is waiting.",
]

GHOST_BODY_P2 = [
    "What is it waiting for? This is the question that will tell you the most. The Ghost is not simply withdrawing for self-preservation, though there is that. The Ghost is performing normalcy <i>as a test.</i> The Ghost wants to know whether the person who wounded you \u2014 or failed to protect you \u2014 will notice. Will they come looking? Will they read the signal and pursue? Will they prove, by their attention, that you were worth noticing when something was wrong?",
    "The Ghost is, in this sense, a bid for what the Architect could never build: the unsolicited proof that you matter to someone. The Architect earns respect through competence. The Ghost wants to be sought after without asking to be \u2014 because asking feels like a concession that should not be necessary. This is its most honest sentence: <i>If they have to be told, it doesn\u2019t count.</i> Which means the Ghost is not asking to have the wound addressed. It is asking to be discovered \u2014 and there is a profound difference between those two things.",
    "D. Martyn Lloyd-Jones, in his exposition of the Sermon on the Mount, wrote about the spiritual danger of nursing a grievance in secret \u2014 of tending a wound so carefully that it becomes more important than the relationship it lives inside. He was not dismissing the reality of the wound. He was pointing to what happens when we make the wound the final word, when we hold it in silence and let it harden into a verdict. The Ghost does precisely this. The silence is not neutral. The silence is active. It is a slow trial, conducted without the other person's knowledge, in which their failure to notice becomes the evidence of their guilt.",
]

GHOST_BODY_P3 = [
    "The Ghost is invisible precisely because it has learned to occupy the shape of health. It continues performing the functions of relationship with enough warmth and competence that no one can point to a specific behavior and say, <i>there \u2014 something is wrong there.</i>",
    "<b>This is the reason the Ghost is the harder breakdown to spot: it looks like maturity.</b> It looks like the kind of person who does not make a scene. It looks like someone who has developed the emotional stability to absorb minor wounds without needing to narrate them. And some of the time, it may genuinely be that. The difference is almost invisible from the outside \u2014 but you know which it is from the inside. You know whether the silence is genuine peace or a performance of peace. You know whether you are fine or whether you are saying <i>I'm fine</i> as a kind of dare.",
    "The cruelty of the Ghost is that it asks the people closest to you to find something they do not know they are looking for. They do not know you are wounded. They do not know they are being tested. They may simply notice, over time, a slight decrease in warmth, a small increase in distance, a barely perceptible shift in how fully you are with them \u2014 and they will not know what to make of it, because nothing happened. And what you have been holding, privately, is that everything happened.",
    "<b>The Ghost has never once succeeded in getting what it is looking for.</b> The cruelty of it is that it asks the people closest to you to find something they do not know they are looking for. They may simply notice, over time, a slight decrease in warmth, a barely perceptible shift in how fully you are with them \u2014 and they will not know what to make of it. The silence does not produce discovery. It produces distance. And the distance produces the loneliness the Ghost was protecting against.",
]

GHOST_PROMPTS = [
    "Think of the last time the Ghost appeared \u2014 a time when you were genuinely hurt and said <i>I\u2019m fine</i> and meant something entirely different. What happened? Who was in the room? What were you waiting for them to do?",
    "Did they come looking? If they did: was it enough, or did some part of you move the goalposts? If they did not: what did that tell you, and what did you do with what it told you?",
]

TWO_TOG_BODY = [
    "Now we place them side by side, because the Architect and the Ghost are not two separate problems operating in sequence. They are the same fear, expressed in two different registers \u2014 one in action, one in suspension.",
    "<b>The Architect is what your fear does when it has time and control.</b> The Ghost is what your fear does when the control is gone and no action remains available. The Architect builds fortresses. The Ghost haunts the fortress after it has been breached. The Architect speaks in blueprints. The Ghost speaks in silence. Together they describe the full perimeter of a soul that has decided it must handle the question <i>am I protected?</i> entirely on its own \u2014 through preparation when preparation is possible, and through a performance of fine-ness when it is not.",
    "The sequence looks like this. You encounter a dismissal or oversight that the Architect did not prevent. The trigger fires: <i>you are not safe.</i> The question wakes up: <i>am I protected?</i> The Architect tries to answer it by rebuilding \u2014 but the wound is relational, not structural. Failing to rebuild, you go quiet. The Ghost takes over, performs normalcy, and waits to be found. The people closest to you do not know they should be looking. The distance widens. And the loop prepares to run again.",
    "What breaks this loop is not a better structure, and it is not a more skillful performance of fine-ness. It is a different answer to the question. Until you begin receiving — not merely knowing but receiving — the protection already secured for you in Christ, the loop has no external pressure to push against. With that answer received, the Architect drafts fewer blueprints, and the Ghost finds it no longer needs to wait to be found, because it has already been found.",
    "Use the template below to write your sequence in your own words. Read it aloud when you finish. Both the Architect and the Ghost lose some of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I experience ____________________, my body reads it as disrespect, "
    "and the old question wakes up \u2014 <i>am I protected?</i> My first move is to "
    "____________________, because the Architect in me believes that if I "
    "can ____________________, the wound will not have room to land. When "
    "that does not work, the Ghost takes over \u2014 I go quiet and say "
    "____________________. What I am actually waiting for is ____________________. "
    "What I actually need, underneath all of it, is the assurance that "
    "____________________ \u2014 an assurance that has already been given to me in "
    "____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small collection of practices, each of which is specific enough to be used in an actual Tuesday, in an actual moment when the loop you just named has begun to run. None of them are complete in themselves. All of them, practiced with some regularity over months, will begin to loosen the Architect's grip on your soul and give the Ghost an alternative to silence.",
    "I have organized them in two groups: practices for when the Architect is overworking \u2014 when you have time and your preparation has become a form of low-grade anxiety \u2014 and practices for when the Ghost appears \u2014 when the wound has already landed and you have already said <i>I'm fine</i> and do not know what to do with what is actually happening inside.",
]

ARCH_TOOLS = [
    ("The handed-back list", "Each morning, write the names of two or three specific things you are carrying \u2014 a relationship, a meeting, a worry \u2014 and after each one, write the sentence: <i>This is yours today, Lord. I will steward it; I will not be its god.</i> Read it aloud. You will not feel the truth of it on the first morning, or the fifteenth. By the fortieth, something begins to shift in the part of you that wakes up already working."),
    ("Stewardship vs. sovereignty", "When you catch the Architect drawing up another contingency plan, ask him one honest question: <i>Is this stewardship, or am I trying to be sovereign?</i> Stewardship is faithful responsibility for what God has placed in your hands. Sovereignty is what God has reserved entirely for himself. Most Architects have blurred this line for so long that the question itself is clarifying."),
    ("The ten-minute Sabbath", "Once per day, put down every device, every list, every plan, and sit for ten minutes doing nothing useful. The Architect will tell you this is waste. He is not right. It is the smallest possible rehearsal of the truth that the world does not fall apart when you stop holding it up. Over time, it teaches something that doctrine alone cannot teach."),
    ("The protection psalms", "When the urge to over-prepare is strongest, open to Psalm 23, Psalm 46, Psalm 91, or Psalm 121 and pray one aloud. Not to manage an emotion. To put your soul back inside a story that is larger than the one the Architect is currently writing, and to hear the voice of the One who is actually doing the protecting."),
]

GHOST_TOOLS = [
    ("Name it before you perform it", "The Ghost most often fires in the first sixty seconds after the wound lands. Before you say <i>I'm fine</i>, try to notice that you are about to say <i>I'm fine</i> \u2014 that the performance is assembling. You do not have to say everything. But you can say something small and honest: <i>That landed oddly for me. Can I come back to it?</i> The Ghost loses most of its power in the moment you choose a partial truth over a full performance."),
    ("The thirty-six-hour rule", "If you have gone quiet after a wound and you are not yet ready to name it, commit to naming something within thirty-six hours. Not the full case. Not a brief. One sentence: <i>I was more hurt by that than I showed.</i> This single sentence, offered to the right person within thirty-six hours, will do more to interrupt the Ghost than any number of private resolutions to be less guarded."),
    ("Ask one person to come looking", "This is the hardest practice, and also the most direct. When you know the Ghost is operating \u2014 when you have gone quiet and you are waiting to be found \u2014 tell one trusted person: <i>I am not doing as well as I look. I am not ready to talk about it yet, but I need you to know it.</i> This is not asking to be rescued. It is interrupting the secrecy that the Ghost depends on."),
    ("Receive the Lord's pursuit", "The Ghost is waiting to be found. The gospel is the announcement that it has already happened. Spend five minutes with Luke 15 \u2014 the story of the father who saw his son when he was still a great way off and ran to meet him. The father did not wait to be asked. He did not require the son to find the right words. He looked, and he ran. When the Ghost falls silent and waits in the darkness, this is the story that speaks directly into it. Pray it back to God: <i>You saw me. You ran. You did not wait to be discovered. You came looking.</i>"),
]

PRAYER_BODY = [
    "Father,",
    "You see the Architect in me, and you do not mock him. You know which rooms he was first asked to secure, and which wounds taught him that vigilance was the only reliable thing. I thank you for him. He has been faithful in his way, and he has cost himself a great deal in being faithful.",
    "But Father, I know something now that he does not always believe: the structure he keeps building cannot do what only you can do. He cannot protect my dignity. He cannot earn my safety. He cannot build his way to the fortress that you have already made for my soul. Teach me to hand back to you, one room at a time, the things he has been holding on your behalf. Teach me the difference between stewardship and sovereignty, and give me the courage to live inside that difference.",
    "And Lord \u2014 you see the Ghost in me as well. You know the rooms it retreats to. You know what it is waiting for. I confess that the silence I have called composure has sometimes been a test, and that I have called the test maturity, and that I have been wrong. Teach me to name the wound before I perform around it. Teach me to trust that what I say aloud to a safe person will not undo me.",
    "Lord Jesus, the woman in the parable who lost her coin lit a lamp and swept the whole house and searched carefully until she found it. (Luke 15:8) I believe that is what you have done with me \u2014 not waited for me to emerge from the dark, but come in with the light. Help me to stop performing fine-ness in front of the one who is not deceived by it. Help me to be found.",
    "In the name of the One who, on the cross, was not fine \u2014 and did not pretend to be \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Architect has been building for a long time. The Ghost has been performing for a long time. Neither of them will retire after one reading of this document, because they were not formed in one reading of anything. What follows is a short list of directions to travel from here \u2014 some immediate, some longer-term, all of them worth your attention.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different lines will land. The Architect will find reasons to skip the second reading. Read it anyway. The Ghost will want to keep this document private. Tell one person what you found in it."),
    ("Choose one tool, not six.", "Pick a single practice from Section Seven and try it for three weeks before adding a second one. Tools attempted poorly, abandoned quickly, prove nothing. Tools practiced with some patience begin to change something."),
    ("Read Tim Keller, <i>Walking with God through Pain and Suffering.</i>", "This is the book whose voice has shaped this walkthrough. It is a patient, theologically rich companion for the kind of work you are doing \u2014 not a quick fix, but a sustained reckoning with what it means to trust a God who does not always prevent the painful thing."),
    ("Read C. S. Lewis, <i>The Problem of Pain</i> or <i>A Grief Observed.</i>", "Lewis wrote <i>The Problem of Pain</i> as a theologian. He wrote <i>A Grief Observed</i> as a man. The second is shorter, rawer, and, for the Ghost especially, more useful. It is a record of what it looks like to stop performing fine-ness in front of God."),
    ("Spend a week in Luke 15.", "Read all three parables slowly, one per day for the first three days. On the fourth day, ask: which figure in these stories do I most resemble right now \u2014 the son who left, the son who stayed and performed faithfulness while resenting it, or the coin that was simply lost and waiting to be found? Sit with the answer."),
    ("If you are stuck, ask for help.", "There are seasons when the Architect is too entrenched and the Ghost too practiced for a document alone to dislodge them. A wise pastor, a Christian counselor, a trusted friend who will not accept <i>I'm fine</i> as a complete answer \u2014 these are not signs of failure. They are instruments of the answer to your prayer."),
]

GOING_FURTHER_CLOSING = (
    "You are not a project to be completed on your own timeline. "
    "You are a son or daughter being searched for by a Father who lit the lamp and swept the house and is still looking. "
    "Go gently with yourself. The One who began this good work in you is not finished, and he is not impatient, and he has never once been deceived by <i>I\u2019m fine.</i>"
)


def _three_column_table(rows=4):
    """Three-column journal table for the core question exercise."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE EVENT", header_style), Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WAS I PROTECTED HERE?", header_style), Paragraph("your nervous system\u2019s question", sub_style)],
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
    """Generate the Architect+Ghost walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="ARCHITECT  \u00b7  GHOST",
        title="Take 139 Walkthrough \u2014 Architect + Ghost",
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
    story.append(Paragraph("The Architect \u00b7 The Ghost", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disrespect \u00b7 Core Question: Am I protected?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cGod is our refuge and strength,<br/>"
        "a very present help in trouble.<br/>"
        "Therefore we will not fear.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Psalm 46:1\u20132",
        ParagraphStyle("cqa", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: Opening ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read slowly. What follows has been a long time in the writing.")
    for p in OPENING_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # ── SECTION 2: Trigger ──
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TRIGGER",
                   "Disrespect.",
                   "The moment that keeps finding you.")
    for p in TRIGGER_BODY[:4]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  CONTINUED",
                   "Where your sensitivity came from.",
                   "What was lodged in you, and what to do with what you find.")
    for p in TRIGGER_BODY[4:]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, written down.",
                   "Your head will spin the question; your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 14))
    story.append(PageBreak())

    # ── SECTION 3: Core Question ──
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I protected?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "What Scripture actually says.",
                   "A stranger and, in the long run, better answer.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "Where was my soul actually in danger? Where was it not?")
    story.append(Paragraph(
        "Use the table below. In the first column, name an event from the last week. "
        "In the second, answer the question your nervous system was asking: "
        "<i>was I protected here?</i> In the third, answer the deeper question: "
        "<i>was the part of me that finally matters \u2014 my soul, my standing before "
        "God \u2014 at any point in danger?</i>",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table())
    story.append(PageBreak())

    # ── SECTION 4: Mechanism ──
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Architect.",
                   "What you have built, and what it was built for.")
    for p in ARCH_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "What Owen saw.",
                   "The cost of placing your soul in creaturely things.")
    for p in ARCH_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "Retiring him, not firing him.",
                   "The slow recovery of the difference between stewardship and sovereignty.")
    for p in ARCH_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Architect.",
                   "Read it as if it were written from within you. Then answer the prompts below.")

    # Model letter in blockquote style
    for line in ARCH_LETTER.strip().split("\n\n"):
        story.append(Paragraph(line.replace("\n", " "), S["BlockQuote"]))

    story.append(Spacer(1, 10))
    for p in ARCH_LETTER_INSTRUCTION:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 6))

    tool_h = ParagraphStyle("ToolH_AG", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody_AG", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    for prompt in ARCH_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Ghost.",
                   "The place your mechanism collapses, and the performance it builds.")
    for p in GHOST_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "What the Ghost is waiting for.",
                   "The bid that the Architect could never make directly.")
    for p in GHOST_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "Why it looks like maturity.",
                   "The breakdown that fools everyone, including you.")
    for p in GHOST_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Come out from behind the performance.",
                   "Two questions to sit with before you turn the page.")
    for prompt in GHOST_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 14))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same fear, in two registers.",
                   "The Architect and the Ghost are not two problems. They are one loop.")
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

    # ── SECTION 7: Tools ──
    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "What to do when you feel the loop start.",
                   "Small enough to carry; useful enough to reach for.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Architect is overworking.",
                   "Five practices for the time before the wound lands.")
    for name, desc in ARCH_TOOLS:
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
