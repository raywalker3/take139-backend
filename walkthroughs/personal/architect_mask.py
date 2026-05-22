"""Personal Walkthrough — Architect + Mask.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Shame/Disrespect trigger, "Am I acceptable?" core question.
~25 pages, 9 sections.
"""
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Paragraph, Spacer, KeepTogether, HRFlowable, Table, TableStyle,
    PageBreak, NextPageTemplate,
)

from ..base import (
    make_doc, make_styles, finalize_buffer, ensure_fonts,
    section_header, journal_lines, divider,
    PAGE_W, MARGIN_L, MARGIN_R,
    PAPER, INK, ACCENT, MUTED, RULE, HIGHLIGHT_BG,
)


# ──────────── PROSE ────────────

OPENING_BODY = [
    "Before you read any further, I want to do something a good pastor does before a hard conversation. I want to lower the lights and slow the room down, because what we are about to look at is not a catalogue of weaknesses. It is a picture of the way your soul has learned to stay alive \u2014 competent, composed, and in charge \u2014 in a world that has, in specific and sometimes invisible ways, made it feel dangerous to be seen.",
    "We are going to walk through your trigger \u2014 the particular kind of wound that fires the alarm in you when no one else in the room has noticed anything is wrong. We are going to name the question underneath the wound, the one that has probably been present since you were young and that all your competence has never quite managed to silence. We will describe the way you have built a self that can carry enormous responsibility and still look entirely composed, and then we will name what happens to that composed self when the wound becomes too deep to manage. And then, only then, will we put some tools in your hands.",
    "If you were sitting across from me, I would say this plainly. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a God who has seen the wound under the composure and has not looked away; a Son who bore, in his own person, the specific horror of full exposure and public shame; and a Spirit who is this moment more interested in your interior life than you have allowed yourself to be.",
    "So read slowly. The Architect in you will want to read efficiently, to extract the useful parts and get back to work. Resist that. Argue with what does not fit. Linger with what does. Write in the margins. Pray when something catches in your throat, because that catch is not weakness \u2014 it is a door the Lord is opening. The goal is not insight collected and filed away. The goal is a life slightly less defended, lived before a God who has nothing to gain from your performance and everything to give you instead.",
    "Take your time. The people who gave you this document were not wrong about you. That is worth sitting with for a moment before you turn the page.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and the reason it keeps happening, in part, is that it looks from the outside like nothing at all. Someone comments on a decision you made, lightly, almost in passing, and a flash of something hot moves through your chest. A family member asks, with genuine curiosity, how you are really doing \u2014 and you feel a sudden desire to give them a perfectly calibrated answer, one honest enough to seem open but not so honest that you could not take it back.",
    "Your body has just registered a signal of exposure \u2014 the sense that someone is looking at you in a way that might see past what you have arranged for them to see. The trigger is <b>shame</b>, though that word is likely to feel too large for what you experience. Your version is quieter than the word suggests. Not the theatrical shame of public humiliation, though that would fire it too. It is the more ordinary, more relentless kind: the sense that if someone looked carefully enough, they would find the gap between who you appear to be and who you actually are.",
    "C. S. Lewis, writing about pride in <i>Mere Christianity</i>, observed that the proud person is not primarily concerned with having good things \u2014 they are concerned with having more than others. What you experience is the inverse. You are not anxious about being better than someone. You are anxious about being found to be less. Less capable than people believe. Less together than you present. That anxiety is not pride. It is something older and sadder.",
    "Here is what most people do not see when they look at you. They see someone who handles pressure with remarkable calm, who can absorb setbacks that would flatten others and still show up the next morning with a clear plan. What they do not see is the monitoring that makes all of that possible: the constant, quiet scan of every interaction for the moment that might reveal too much.",
    "There is almost certainly a history underneath this. Shame is never free-floating. It attaches itself to specific memories and voices, to moments when the gap between what you showed and what you felt was seen by someone with power over you, and the seeing went badly. A parent whose approval was contingent on performance. A classroom moment you have not allowed yourself to think about in years. A season of failure that no one knew the full extent of, and that you buried carefully and built over. Whatever its origin, the lesson it wrote in you was this: <i>The self people see is safer than the self I actually am. I will manage the difference.</i>",
    "That lesson was not irrational. In the circumstance that produced it, it may have been the only reasonable response available to a young person with limited options. But it does not age well. Managing the gap between the seen self and the felt self becomes, over time, an enormous and exhausting project, and the energy it consumes is energy quietly borrowed from everything else.",
    "Before we go further, I want you to answer two questions in writing \u2014 not in your head, where the Architect will draft the most presentable version, but on paper, where something more honest tends to emerge.",
]

TRIGGER_PROMPTS = [
    "Name the last time you felt the exposure signal fire \u2014 the moment someone seemed to be looking past what you had arranged for them to see. What happened? What did you do in the next thirty seconds?",
    "What would it mean, practically and concretely, if the person who triggered you actually saw the full picture? What are you most afraid they would conclude?",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is what the alarm is standing guard over.",
    "Yours is this: <b>Am I acceptable?</b>",
    "It is not the same as <i>Am I loved?</i>, though it sometimes borrows that face. It is not <i>Am I competent?</i>, though competence is one of the primary ways you have tried to answer it. It is more specifically located than either. It is the question of whether you are acceptable as you actually are \u2014 not the performing version, not the planning version, not the version that shows up prepared and in command, but the version underneath all of that, the one that is tired and uncertain and aware of its own gaps. The question is: <i>If they saw that version, would they still keep me?</i>",
    "The taxonomy of fear has a name for this profile, and it is the right one. This is the shame question \u2014 not shame about a specific act, though that is part of it, but shame about a self. The haunting sense that there is something fundamentally not-right about you, something that your performance has been constructed, over years, to conceal. John Owen, in his great work on the mortification of sin, wrote that the indwelling sin we most need to address is not always the one that announces itself loudly but the one that has quietly organized the whole life around its own avoidance. The shame question is, for many people, exactly that kind of organizing principle. It runs the show from a room no one is allowed to enter.",
]

QUESTION_BODY_P2 = [
    "There is a reason the Psalms spend so much time in the territory of shame and concealment. The prayer book of Israel did not assume that God's people would have their interior lives sorted out. It assumed the opposite.",
    "<i>My wounds stink and fester because of my foolishness; I am utterly bowed down and prostrate; I go about mourning all day long . . . I am feeble and crushed; I groan because of the tumult of my heart.</i> (Psalm 38:5\u20136, 8)",
    "Notice that the psalmist does not present well. He names the festering, the feebleness, the groaning, with no concern for the impression he is making. This is not because he lacks dignity. It is because he has located the one Audience before whom the management project is both unnecessary and impossible. <i>O Lord, all my longing is before you; my sighing is not hidden from you.</i> (Psalm 38:9) You are already fully seen, and the seeing has not produced rejection.",
    "The gospel anchor for the shame question is this: <i>I am justified \u2014 just as if I had never sinned, and just as if I had always perfectly obeyed. And I am in Christ \u2014 covered, clean, belonging.</i> Paul says it with a directness that should stop us cold: <i>There is therefore now no condemnation for those who are in Christ Jesus.</i> (Romans 8:1) Not reduced condemnation. None. The verdict was not based on the version of you that performed well.",
    "<i>For our sake he made him to be sin who knew no sin, so that in him we might become the righteousness of God.</i> (2 Corinthians 5:21) Christ entered, in his crucifixion, the full horror of public exposure \u2014 seen, mocked, found contemptible by those who watched \u2014 not because he had earned it, but to absorb, once and finally, the shame you have been carrying and building over ever since.",
]

QUESTION_BODY_P3 = [
    "This is where you have to do some honest work, because the Architect in you has been trying to answer the shame question with architecture. You have been building a self so competent, so visibly capable, so reliably composed under pressure that the question <i>Am I acceptable?</i> never quite has to be asked out loud. The building project is very good. That is not an insult; it is an accurate description of something that has taken years and enormous effort. But a building, however good, cannot answer a question about a person. It can only defer it.",
    "The deferral has a cost. Every time you succeed at the project of appearing composed, you get a small hit of relief, and that relief feels like an answer. But it is not the answer. It is the absence of the question for a moment. And the question comes back, reliably, the next time someone looks at you a half-second too long, or asks something you did not expect, or reveals that they have seen a part of the interior you thought was sealed.",
    "The real answer to <i>Am I acceptable?</i> cannot be constructed. It can only be received. It comes not from the building you have made but from the verdict that was spoken over you at the cross, before you had done anything at all to merit it. That verdict is not waiting for your performance to justify it. It has already been justified \u2014 by his performance, on your behalf. The covering you have been trying to build for yourself was already provided. What you are doing, when you maintain the managed self, is refusing to step under the covering that is already there.",
    "This will not be resolved in a single reading. The reception of justification as a felt reality rather than a doctrinal affirmation is the work of years. But the work begins with naming, accurately and without flinching, what you have been doing and what you have been afraid of.",
]

ARCH_BODY_P1 = [
    "You have built something. The Architect is not a label your friends gave you; it is a way your soul has organized itself, quietly and over time, in response to something real. The Architect is the part of you that believes, in his bones if not in his words, that the best protection against the worst outcomes is thorough preparation, excellent systems, and a level of personal competence that leaves as little as possible to chance.",
    "The Architect is, in many respects, admirable. He is the reason people trust you with hard things, the reason the rooms he manages run well. Proverbs does not romanticize the disorganized life: <i>Know well the condition of your flocks, and give attention to your herds.</i> (Proverbs 27:23) The Bible commends the kind of careful, attentive stewardship the Architect provides. We are not here to fire him. We are here to understand what he is afraid of, because that is where the architecture gets complicated.",
    "The Architect was not born from nothing. He was built, usually early, in a household or a season in which things went wrong when no one was paying sufficient attention. He may have been built in a home where approval was tied to achievement \u2014 where competence was the price of belonging. He may have been built in a family that needed someone to hold it together, and that child was you. Whatever the origin, the lesson lodged: <i>If I do not keep this held together, no one will.</i>",
    "And it worked. Systems and competence produced real outcomes: respect, trust, opportunity. But over time the strategy stopped being a tool and started being an identity. The Architect stopped being something you did and became something you were.",
]

ARCH_BODY_P2 = [
    "This is where Tolkien, writing about a very different kind of architecture, names something important. In his letters about <i>The Lord of the Rings</i>, Tolkien wrote that the fundamental error of Sauron was the placing of so much of his own power and identity into an external object that its destruction became his destruction. The ring was not a tool. It was a repository of the self. When we pour enough of our identity into what we have built, we become unable to survive what we have built being threatened.",
    "The Architect has done this with his competence and composure. Any crack in the performance registers not as a setback but as an exposure of the self underneath. A project that fails is not just a failed project. It is evidence. A criticism is not just an uncomfortable observation. It is a near-miss of the thing he most fears: being seen as the person he is afraid he actually is.",
    "The people closest to an Architect often say some version of the same sentence: <i>I don't always know where you really are. You're always fine, but I can't tell if you actually mean it.</i> They are not wrong. The Architect has become so practiced at presenting competence that the presentation runs even when the person watching is the person who loves him most and who would not leave if they saw the rest.",
    "The Architect is not your enemy. He is a version of you that learned, under real conditions, that preparation and performance kept you safer than vulnerability did. He was probably right about that in the context that made him. But he is still running that analysis on conditions quite different from those that required it, and the cost of his maintenance is rising faster than the protection he provides.",
]

ARCH_BODY_P3 = [
    "What does it look like to begin loosening his hold? Not dismantling him \u2014 you need an Architect; the question is whether he needs to run everything. It looks like allowing a small thing to be imperfect without correcting it. It looks like telling one person one true thing about your interior, and then waiting to see whether what happens next matches what the Architect has been predicting all these years.",
    "There is an assumption buried in the Architect's deepest systems worth naming plainly: <i>If people see me as I am, rather than as I appear, the outcome will be negative.</i> That assumption has never been tested in the presence of the gospel. It has been tested in the presence of the world, which has sometimes confirmed it. But the gospel has a different data set. It says that the one Person before whom you are fully seen \u2014 with no gap, no managed presentation, no facade between his sight and your actual self \u2014 has not rejected you. He has moved toward you, at great cost, to make you acceptable. The Architect has been running his risk model without including the most important variable.",
    "The exercise below is not comfortable for an Architect, and that is partly the point. Read the letter that follows \u2014 written from the Architect to you, in the voice he would use if he were honest about what he is afraid of. Then use the prompts to respond.",
]

ARCH_LETTER_INSTRUCTION = [
    "The letter below was written on your behalf, in the voice the Architect would use if he dropped his own management project for a moment. Read it as you would read a letter from someone who has been protecting you for a long time and is, for once, telling you the truth about why.",
]

ARCH_LETTER = """\
Dear friend,

I have been with you a long time. You probably do not think of me as a separate thing \u2014 you think of me as simply the way you are. But I want to tell you something honest.

I am afraid. That is what has been running the whole operation. Not ambition, not the desire to be excellent, though I have dressed myself in those clothes at various times. Underneath is a very old fear: that if the people who need you to be capable ever saw that you are not entirely capable, something irreversible would happen. They would place you in a different category \u2014 the category of people who need things rather than provide them \u2014 and you could not bear that.

I built the composure to prevent that. The planning, the competence, the seamless management of impression \u2014 all of it to keep the gap from showing. And it has worked, most of the time. Which is why you keep letting me run things.

But I need you to know something I have never told you. I cannot protect you from the thing I am most afraid of. The gap is there. Every person who has ever known you well has sensed it. The protection I provide is not protection from being seen \u2014 it is the exhausting maintenance of a delay.

I am not the answer. I am the question, asking itself in architectural form. Let someone else answer it.

The Architect
"""

ARCH_LETTER_PROMPTS = [
    "What is the one line in that letter that you most wanted to dismiss? What does your resistance to it tell you?",
    "Who in your life has sensed the gap the Architect describes \u2014 the distance between the composed self and the interior one? Have you let them name it? Why or why not?",
    "Write one sentence that names what the Architect has been building toward, and one sentence that names what he has been building away from.",
]

MASK_BODY_P1 = [
    "Every mechanism has a place where it breaks, and the way it breaks tells you something essential about what it has been doing all along. For you, the breakdown is called <b>the Mask</b>, and what makes it so difficult to address is that it does not look like a breakdown. It looks like composure. It looks like leadership. It looks fine, and it works, and no one knows anything is wrong.",
    "Here is how it happens. The Architect has been running the operation \u2014 maintaining the building, managing the presentation, ensuring the gap stays sealed. Then something exposes a crack: a criticism you did not see coming, a failure you cannot reframe quickly enough, or sometimes just a quiet moment when the silence asks a question you have been successfully avoiding for years.",
    "In that moment, the Architect does not collapse into argument or silent withdrawal. Instead, a different mechanism engages with extraordinary smoothness. You put on a self \u2014 not a fabricated self, but a functional, persuasive, entirely credible version of you that can handle this room, this conversation, this moment, without letting the wound show. The Mask slides on, and the person wearing it continues to lead, to serve, to counsel \u2014 all real, or close enough to real that no one, not even you much of the time, can tell exactly where the performance ends and the person begins.",
    "D. Martyn Lloyd-Jones, writing on spiritual depression, observed that many of the most apparently functional people he knew were the most spiritually lonely, because their competence had insulated them from the honest disclosure that fellowship requires. He was describing what happens when an Architect puts on a Mask. The result is a person who is admired, respected, sought out \u2014 and fundamentally alone.",
]

MASK_BODY_P2 = [
    "The Mask is not lying. That is what makes it so durable. Almost everything the Mask presents is true. You are competent. You do care about the people you serve. The Mask does not fabricate; it selects. It chooses, with remarkable precision, which parts of the true self to show, and it keeps the rest behind a very well-constructed door.",
    "The specific genius of the Architect-Mask combination is that the Mask is built from the same materials as the Architect: competence, composure, a presence under pressure that others find genuinely reassuring. When you are wounded \u2014 when the shame question fires \u2014 you do not retreat, do not argue, do not dissolve. You become more present, more in command. The wound goes underground and the leadership goes to the surface, and from the outside it looks like exactly what a great leader is supposed to look like.",
    "That is the theological problem with the Mask, and it is a serious one. <b>The gift and the hiding are using the same face.</b> The very quality that makes you genuinely valuable \u2014 your capacity to remain grounded under pressure \u2014 is, when the Mask is engaged, a sophisticated form of concealment. Not from God, who sees through it as effortlessly as he sees through everything. But from the people you are in relationship with, and more devastatingly, from yourself.",
    "Bonhoeffer, in <i>Life Together</i>, wrote a sentence worth holding: <i>He who is alone with his sin is utterly alone.</i> The Mask guarantees a particular kind of aloneness, because it prevents the confessional, fully honest speech that Bonhoeffer describes as the mechanism by which Christian community breaks the power of hiddenness. The Mask will give you a version of honesty that is credible enough to seem open but not costly enough to cost anything. And in that gap \u2014 between credible honesty and true confession \u2014 the wound continues its work underground.",
]

MASK_BODY_P3 = [
    "Here is the question the Mask has never been asked: <b>What would you lose if it came off?</b> Not who would leave. Not how people would respond. What in you would be at risk if the performance of fine-ness stopped?",
    "My guess is that the answer is something like this: you would lose the ability to tell yourself you are managing. And the managing has been, for a long time, the evidence that you are acceptable. If you stop managing, the question comes back in full size, unanswered. The Mask is not a lie about the outside world. It is the only kindness the shame-question has ever been offered, and the one you reach for every time. But it costs you everything it was meant to protect.",
    "The pastoral move here is not dramatic. It is the naming of what is happening, said clearly, so that the next time the Mask slides on, you can feel it go on \u2014 and choose, even once, to take it off instead. The courage required for that is not the same courage that makes you good at leading. It is a different and harder kind: the courage to be seen without the architecture in place, by at least one person, and to let the outcome be what it is.",
    "Peter, who was remarkably skilled at presenting bravely and retreating when it cost too much, was asked three times by the risen Christ: <i>Do you love me?</i> (John 21:15\u201317) The question was not asked because Christ did not know the answer. It was asked because Peter needed to say the true thing, out loud, with nothing between him and the words. The Mask does not survive that question \u2014 not because the love is not real, but because the question insists on the unmediated self, and the Mask can only offer the mediated one.",
]

MASK_PROMPTS = [
    "Name the last time you put the Mask on in response to a wound. What had just happened? What did you show? What did you actually feel?",
    "What is the one thing the Mask has never let you say out loud to another person? Name it here, even if only in writing, even if only to yourself.",
]

TWO_TOG_BODY = [
    "Now we put the two next to each other, because the Architect and the Mask are not separate problems. They are the same soul, organized around the same fear, moving through the same loop.",
    "<b>The Architect is what your soul does when it has time to prepare.</b> The Mask is what it does when something gets through the preparation. The Architect builds the perimeter. The Mask is what you reach for when the perimeter is breached. Together they form a closed system: the Architect ensures that exposure rarely happens, and the Mask ensures that when it does, no one \u2014 including you \u2014 has to know.",
    "The pattern looks like this. <b>(1)</b> You move through the world in the Architect's mode: planning, preparing, managing the gap. <b>(2)</b> Something lands that the architecture did not anticipate. <b>(3)</b> The trigger fires: <i>I have just been seen in a way I was not prepared for.</i> <b>(4)</b> The question wakes up: <i>Am I acceptable?</i> <b>(5)</b> The Architect tries a faster rebuild. <b>(6)</b> When that cannot happen quickly enough, the Mask engages: composed, present, fine. <b>(7)</b> The wound goes underground. The loop restarts.",
    "What breaks the loop is not a better Architect \u2014 a more sophisticated Architect only produces a better Mask. What breaks it is a different answer to the question: not the answer built from performance, but the one given at the cross. That answer, received rather than constructed, is the only thing the Mask does not know how to improve upon. Below, name your sequence in your own words. Both the Architect and the Mask lose ground when they are named in plain speech.",
]

TWO_TOG_TEMPLATE = (
    "When I encounter ____________________, my body reads it as exposure, and "
    "the old question wakes up \u2014 <i>am I acceptable?</i> My first move is to "
    "____________________, because the Architect in me believes that if I "
    "can ____________________, the exposure will pass unnoticed. When that does not "
    "work quickly enough, the Mask engages: I become ____________________ . "
    "What I am actually after, underneath all of it, is the verdict "
    "____________________ \u2014 a verdict Christ has already spoken over me in "
    "____________________ ."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a collection of small, portable practices, each of which is calibrated to a specific moment in the loop you just named. None of them will resolve in a week what years have put in place. All of them, practiced faithfully over months, will begin to loosen the grip.",
    "I have divided them into two sets: tools for the Architect in his overworking mode, when the preparation has tipped into anxious management of impression; and tools for the Mask, for the moment after the wound fires and before the Mask has fully engaged. That second window is narrow, but it is real, and it is where the most important work of this season will happen.",
]

ARCH_TOOLS = [
    ("The daily incompleteness inventory", "Each evening, name one thing you left unmanaged today \u2014 one gap in the presentation, one moment of imperfection you did not correct. Do not analyze it. Simply name it and let it sit. The Architect cannot retire until he is allowed to leave work at work."),
    ("Stewardship, not sovereignty", "Each morning, pray this sentence aloud before the first plan of the day: <i>Lord, I am your steward of this, not its sovereign.</i> List two or three specific situations. Say it about each one. You will not feel it for the first month. Something begins to give around the fortieth day."),
    ("The ten-minute sabbath of self", "Once each day, set aside ten minutes with no agenda, no device, no monitoring. Sit with whatever is actually true of you in that moment. The Architect will call this waste. It is not waste. It is the smallest rehearsal of the truth that you are not holding yourself together \u2014 you are being held."),
    ("The Psalms of exposure", "When the urge to prepare and present is running at full capacity, open to Psalm 38, Psalm 51, or Psalm 139 and pray one aloud. The psalmists said the true thing directly to God without editing it first, and they were not destroyed by the saying. Borrow their courage until you develop your own."),
    ("One true sentence per week", "Choose one trustworthy person. Once per week, say one true sentence about your interior to that person \u2014 not a performed honesty, but a sentence that says where you actually are. Do this for thirty days and note what happens to the Architect's maintenance costs."),
]

MASK_TOOLS = [
    ("Name the moment before it seals", "The Mask has a seam \u2014 a moment between the wound and the slide, before the composed self has fully engaged. Your only task is to notice that moment. Simply feel the Mask going on and know what is happening. Noticing is the beginning of choice."),
    ("The three-word honesty prayer", "In the moment after the wound, before the Mask seals, say these three words silently: <i>I am hurting.</i> Not as a petition \u2014 as a statement. Say it to God before the presentation begins. He already knows. The saying is for you."),
    ("The deferred confession", "You will not always be able to take the Mask off in the moment. But within twenty-four hours, find the person you trust most and say: <i>I put the Mask on yesterday when ___. What was actually happening was ___.</i> Do it once, with one person, within one day. The Mask's power is its secrecy. One honest sentence breaks that power."),
    ("The advocate prayer", "When the Mask is on and you can feel it: <i>Lord Jesus, you were exposed for me. I do not have to manage the exposure. The verdict is already spoken. Help me receive it.</i> Say it anyway, even before you feel it. The Architect trusts structures he does not feel. Give this prayer the same trust."),
    ("The letter to the wound", "At the end of a week when the Mask was particularly active, write one paragraph addressed to the wound itself. Name what happened, what the wound was asking for, and what you did instead. Writing the truth, even to no one, is a form of the exposure the Mask is designed to prevent. Do it anyway."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Architect in me, and you see the Mask he reaches for, and you are not surprised by either of them. You know why I built both. You were there for the moments that made them feel necessary. Thank you that you did not look away from those moments, and that you are not looking away now.",
    "Father, I am tired of the maintenance. I am tired of the monitoring, of the managing of distance, of the way I can walk through a hard day and come out the other side looking fine and feel, in the quiet afterward, that no one was actually there. I do not know how to stop on my own. I have tried to stop on my own, and what I built was a better Mask. So I am asking you to do what I cannot: teach me, slowly, what it means to be seen and not destroyed. Teach me to let the people who love me see further in than I have let them go. Teach me to say the true thing before the presentation has fully assembled.",
    "Lord Jesus, you know what it is to be fully exposed and fully wrongly judged \u2014 naked before the crowd, silent before Pilate, bearing the full weight of a verdict you did not deserve. You entered the experience of exposure I am most afraid of, and you did not manage it. You absorbed it. And in the absorbing, you reversed its verdict over me. Help me to receive that reversal not as doctrine but as the felt covering of a soul that has been hiding a long time.",
    "Holy Spirit, where the Mask goes on today, give me the courage to notice it. Where I am managing distance, give me the grace to close it \u2014 if only by one sentence, with one person, before the day ends. Where the question <i>am I acceptable?</i> wakes up in me, remind me of the answer you have already spoken, and keep speaking until I can hear it in the part of myself I have worked hardest to conceal.",
    "In the name of the One who said, to the woman who had managed her own exposure for years: <i>your faith has made you well; go in peace</i> \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Architect and the Mask have been with you a long time, and they will not retire after one reading. What follows is a short list of next steps \u2014 some for the next week, some for the longer work ahead.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different lines will land the second time. The Mask will try to let you read it efficiently the first time, to extract the useful parts without being changed by them. Read it again slowly. The Architect will resist; do it anyway."),
    ("Take one tool from Section Seven, not all of them.", "Choose the one that felt most uncomfortable \u2014 not the one that felt most manageable. Tools that cost nothing protect nothing. Try it for two weeks before evaluating."),
    ("Tell one person what you found here.", "Not the whole document. One sentence: <i>I learned that my pattern is the Architect, and that what I do when I\u2019m wounded is put on a Mask. I\u2019m working on letting the Mask come off.</i> The secrecy of the Mask is part of its power. Breaking the secrecy once, with one trusted person, changes the architecture."),
    ("Read Tim Keller\u2019s Counterfeit Gods.", "This is the book that most directly addresses what happens when we build our identity in something that cannot hold it. The Architect who builds his acceptability in his own competence and composure will find himself, somewhere in these pages, with precision."),
    ("Read C. S. Lewis\u2019s The Four Loves.", "Lewis\u2019s chapter on friendship, and his observations on the difference between intimacy and affection, will give you language for what the Mask has been preventing. He writes with the kind of honesty about the interior life that the Mask makes very difficult. Let him model it."),
    ("If you are stuck, ask for help.", "There are seasons when the Architect and the Mask have been in place so long that they cannot be dislodged without a trusted witness. A wise pastor, a Christian counselor, a friend who knows you well enough to say the hard thing gently \u2014 these are not signs of failure. They are the kind of help the Mask is specifically designed to prevent you from asking for. Ask anyway."),
]

GOING_FURTHER_CLOSING = (
    "You are not a project to be completed. You are a son or daughter being loved into freedom by a Father "
    "who has already seen everything the Mask was built to hide, and who has not changed his mind about you. "
    "Go gently. The One who began this work in you will be the one to finish it."
)


def _three_column_table(rows=7):
    """Three-column journal table for the acceptability reflection exercise."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE MOMENT", header_style), Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WHAT I SHOWED", header_style), Paragraph("the Mask\u2019s presentation", sub_style)],
        [Paragraph("WHAT WAS ACTUALLY TRUE", header_style), Paragraph("the interior I did not show", sub_style)],
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
    """Generate the Architect+Mask walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="ARCHITECT  \u00b7  MASK",
        title="Take 139 Walkthrough \u2014 Architect + Mask",
    )

    story = []

    # ── COVER ──
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor\u2019s<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the self<br/>you have learned to show, and the one you haven\u2019t.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph("The Architect &nbsp;\u00b7&nbsp; The Mask", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Shame &nbsp;\u00b7&nbsp; Core Question: Am I acceptable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cYou are not the kind of person God\u2019s love is comfortable with<br/>"
        "until it has made you the kind of person it is comfortable with.\u201d</i>",
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
    story.append(PageBreak())

    # ── SECTION 2: Trigger ──
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TRIGGER",
                   "Shame.",
                   "The moment no one else notices \u2014 and everything you do in the next five seconds.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will present the answer; your hand will tell the truth.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 3: Core Question ──
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I acceptable?",
                   "The wound the alarm is standing guard over.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "What the psalmist knew \u2014 and what the cross answers.",
                   "Already fully seen. Already not rejected.")
    for p in QUESTION_BODY_P2 + QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "The gap between what I showed and what was actually true.")
    story.append(Paragraph(
        "Use the table below. In the first column, name a recent moment when the exposure alarm fired. "
        "In the second, describe what you showed \u2014 what the Mask presented. "
        "In the third, write what was actually true of you in that moment, "
        "<i>behind the presentation</i>.",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table(rows=5))
    story.append(PageBreak())

    # ── SECTION 4: Mechanism ──
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Architect.",
                   "What you have built, and the fear that has been running the construction.")
    for p in ARCH_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "What Tolkien saw \u2014 and the assumption buried in the systems.",
                   "When you pour your identity into your structures, their threat becomes your threat.")
    for p in ARCH_BODY_P2 + ARCH_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Architect.",
                   "Read this as a letter from someone who has been protecting you for a long time.")
    for p in ARCH_LETTER_INSTRUCTION:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))

    # render the letter as a block-quote callout
    letter_style = ParagraphStyle(
        "ArchLetter", fontName="Fraunces-Italic", fontSize=11, leading=18,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8)
    for line in ARCH_LETTER.strip().split("\n\n"):
        story.append(Paragraph(line.replace("\n", " "), letter_style))

    story.append(Spacer(1, 12))

    tool_h = ParagraphStyle("ToolH2", parent=S["H3"], fontSize=10.5, leading=14,
                             spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody2", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    story.append(Paragraph("Now respond to the letter. Use the prompts below.", S["BodyJ"]))
    for prompt in ARCH_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Mask.",
                   "The place your mechanism collapses \u2014 and the face it shows while collapsing.")
    for p in MASK_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The gift and the hiding wear the same face.",
                   "Why the Architect\u2019s Mask is the hardest profile to break through to.")
    for p in MASK_BODY_P2 + MASK_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions to sit with.",
                   "Write, not think. The Mask performs better in your head than on paper.")
    for prompt in MASK_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same fear, in two modes.",
                   "The Architect and the Mask are not two problems. They are one loop.")
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
                   "When the Architect is overworking.",
                   "Small enough to carry; concrete enough to use.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    for name, desc in ARCH_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Mask is going on.",
                   "Five practices for the narrow window between the wound and the concealment.")
    for name, desc in MASK_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())

    # ── SECTION 8: Prayer ──
    section_header(story, S, "SECTION EIGHT  \u00b7  A PRAYER",
                   "Pray this slowly.",
                   "Out loud if you can. Sit in the silence after the Amen.")
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
