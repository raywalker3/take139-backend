"""Personal Walkthrough — Architect + Quiet Exit (Verdict).

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disrespect / Injustice trigger, "Am I protected?" core question.
Breakdown: Quiet Exit (VERD) — quietly decides "I'm done"; stops investing;
           withdraws into a verdict.
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
    "Before you read any further, I want to do something that a good pastor does "
    "before he preaches a hard text. I want to slow down the pace, lower the "
    "expectation that what follows will be quick, and ask you to sit with me in "
    "the particular sadness of the profile you are about to encounter. Because "
    "this one \u2014 the one this walkthrough describes \u2014 is the saddest of its kind.",

    "We are going to walk through the way your soul has learned to keep itself "
    "safe in a world that has, in specific and real ways, failed to keep you safe. "
    "We will name the trigger that keeps firing in you. We will listen for the "
    "wound under that trigger, the question that has been with you since you were "
    "very small. We will describe the strategy you built to answer that question, "
    "and then we will spend careful time on the place that strategy collapses "
    "\u2014 the place it most needs the gospel, and receives it least.",

    "If you were sitting across from me, I would say this slowly and mean it: "
    "<b>What you are about to read is true, but it is not the whole truth about you.</b> "
    "The whole truth includes a Father who has not, in fact, left you to be "
    "swallowed by disappointment; a Son who endured the worst possible version of "
    "the abandonment you fear and emerged from the other side with wounds that "
    "healed rather than hardened; and a Spirit who is, at this very moment, more "
    "committed to your remaining open than you are.",

    "The particular thing this walkthrough will ask of you is this: it will ask "
    "you to take seriously the possibility that a move you have always experienced "
    "as maturity \u2014 as finally accepting reality, as having grown beyond the "
    "need for a thing that was never going to come \u2014 is actually something "
    "different. It will ask you to consider that your acceptance is, in some "
    "cases, not peace. It is a slow departure. And it will ask you to stay "
    "long enough to feel the difference.",

    "C. S. Lewis, in <i>A Grief Observed</i>, wrote about the strange way grief "
    "can look like calm from the outside. He described a man who has locked a "
    "door he cannot bear to open. From a distance, the locked door looks like "
    "composure. Only from the inside can you tell whether it is composure or "
    "closure. That distinction is the pastoral work of this document.",

    "Read slowly. Argue with what does not fit. Stay with what does. Write in the "
    "margins, and pray when something catches in your throat, because that catch "
    "is usually the Lord saying, <i>look here, with me.</i> Take your time. The "
    "chapter you are about to read about yourself has been a long time in the "
    "writing, and it deserves more than a skimming.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it has its own particular "
    "texture. It usually comes not in a single large event, but in the accumulation "
    "of smaller ones. Someone dismisses what you said without fully hearing it. An "
    "agreement is made and then quietly allowed to expire. A pattern repeats that "
    "you named once, perhaps twice, and nothing changed. An elder disregards your "
    "counsel. A spouse uses the same tone again. A colleague receives the credit "
    "for something you carried. Your body registers each one, files it, and waits.",

    "On the surface each individual moment may look like a small grievance. In "
    "reality your nervous system has been running a long, quiet calculation, "
    "and the calculation is not <i>I have been inconvenienced.</i> It is something "
    "closer to <i>The scales are not level here, and no one is going to level them.</i> "
    "You are, at bottom, a person who carries a keen and hypervigilant sense of "
    "justice \u2014 not for yourself alone but for the people and structures you are "
    "responsible for. When that sense is violated repeatedly, it does not announce "
    "itself as outrage. It announces itself as arithmetic.",

    "This is your trigger, and it has two faces. The first face is <b>disrespect</b>: "
    "the moment when someone's action or tone tells you, whether they mean to or "
    "not, that you do not warrant the dignity you know you possess. The second face "
    "is <b>injustice</b>: the moment when the scales tip and no one moves to correct "
    "them. Often both fire at once. They share a common root: the conviction, lodged "
    "somewhere early and deep, that the world is not reliably safe for you, and that "
    "no one has stationed themselves at the door to keep the dangerous thing from "
    "coming in.",

    "The taxonomy here is important. This is not vanity. It is not thin-skinned "
    "pride, though the Architect in you has almost certainly been accused of one "
    "or both at difficult moments. What is happening under your trigger is something "
    "more structural. You are a person who reads the justice-temperature of a room "
    "the way a pilot reads instruments \u2014 constantly, without being asked, because "
    "somewhere in your history the instruments gave a reading that was never "
    "corrected, and the uncorrected reading had real costs.",

    "What is particularly important to see is that most of the people who trigger "
    "you are not malicious. They are careless. And carelessness is, for you, almost "
    "worse \u2014 because carelessness implies that the question your soul has been "
    "asking since you were small, <i>is anyone watching the scales?</i>, has been "
    "answered in the negative. No one is watching. You have been managing the ledger "
    "alone, and you are tired.",

    "The fatigue matters. It is the soil in which the Quiet Exit grows. Before we "
    "name the breakdown, you need to understand how the wound was formed, because "
    "the withdrawal you have been practicing \u2014 emotionally, relationally, sometimes "
    "literally \u2014 makes complete sense given the weight you have been carrying. "
    "The pastoral move is not to dismiss the weight. It is to ask whether the "
    "response to it is the one that will lead somewhere good.",

    "Here is what I want you to notice: the same sensitivity that fires your trigger "
    "is also what makes you a gift in the rooms you inhabit. You are the one who "
    "sees the injustice that others have smoothed over. You are the one who keeps "
    "the commitments others quietly abandon. You are the one who does not stop "
    "paying attention. This is not nothing. The very wiring that wounds you is also "
    "what the people around you most depend on. But right now, before we go "
    "further, I want you to sit with two questions in writing.",
]

TRIGGER_PROMPTS = [
    "Name the most recent moment in which the trigger fired. What was the "
    "event, in two sentences? Be specific \u2014 name the person, the setting, "
    "the thing that was said or left unsaid.",
    "On a scale of one to ten, what was the objective size of that event, and "
    "what was the size of the response inside you? If those numbers were "
    "different, you have located your trigger. Write one sentence about what "
    "the gap tells you.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than any of "
    "the events that fire it. The trigger is the alarm; the question is the "
    "wound the alarm is standing guard over.",

    "Yours is this: <b>Am I protected?</b>",

    "It is not, at its root, a question about whether you are respected, though "
    "you need respect and are right to need it. It is not a question about "
    "whether you are loved, though you need love. It is a more primal question, "
    "the one that wakes at three in the morning in a child who has heard the "
    "door open and does not know what is coming: <i>Is there someone between me "
    "and what could hurt me? Is anyone holding the scales? If the worst happens, "
    "will anyone correct it?</i>",

    "Most adults carry this question underground, where it works on them "
    "anonymously. You carry it closer to the surface, which is both more painful "
    "and, in the end, more honest. The Architect in you has built elaborate "
    "structures partly to answer it: if I plan well enough, secure the right "
    "relationships, anticipate the failure modes, keep my word and insist others "
    "keep theirs, then perhaps the answer will be yes. You have been running that "
    "experiment for a long time, and the results have been mixed.",

    "What the theology of the Psalms tells you is that the question itself is "
    "not pathological. It is human. It is the question of every Psalm of "
    "lament, which is to say it is the question of roughly a third of the prayer "
    "book Jesus himself used. Psalm 10 begins: <i>Why, O Lord, do you stand far "
    "away? Why do you hide yourself in times of trouble?</i> That is not weak faith. "
    "That is honest faith, faith that has not yet received the answer but has "
    "refused to stop asking.",

    "The question <i>Am I protected?</i> is God-shaped. The longing for a defender, "
    "a just judge, a protector who will not look away \u2014 this is precisely what "
    "the gospel addresses. The trouble is that the address takes a form that does "
    "not satisfy the nervous system's version of the question. You know this "
    "already, in your head. The harder work is receiving it somewhere deeper.",
]

QUESTION_BODY_P2 = [
    "Here is what Scripture actually says in answer to your question, and it "
    "has to be said in two halves.",

    "The first half is the one the Psalms shout. <i>The Lord is my rock and my "
    "fortress and my deliverer, my God, my rock, in whom I take refuge, my "
    "shield, and the horn of my salvation, my stronghold.</i> (Psalm 18:2) Notice "
    "the pile-up of synonyms. David does not say it once and move on. He says it "
    "seven different ways because the question does not stay answered. It wakes "
    "up again the next morning, and the next. David is not embarrassed by this "
    "repetition; he hands it to God in the same breath he hands everything else. "
    "The psalmist is protected. The scales are held. The fortress is real.",

    "The second half is the harder one, and Paul says it plainly. <i>Who shall "
    "separate us from the love of Christ? Shall tribulation, or distress, or "
    "persecution, or famine, or nakedness, or danger, or sword?</i> (Romans 8:35) "
    "The list is instructive. Paul does not promise you a life without any of "
    "those things. He is promising you that none of them can do the one thing "
    "your soul most fears: separate you from the love that finally holds you. "
    "The protection the gospel offers is not a shield around your circumstances. "
    "It is a shield around your soul.",

    "This is, admittedly, a harder answer than the one your trigger demands. "
    "Your trigger wants to hear: <i>nothing bad will happen to you.</i> Scripture "
    "refuses to say that, and it refuses to say that because it would be a lie, "
    "and God does not console his children with lies. What it says instead is "
    "this: <i>You are protected from the only thing that could finally undo you, "
    "and in the place that matters permanently, the scales are held by hands "
    "that do not tire.</i>",

    "The gospel anchor for your core question is this: <b>I am a Creature.</b> "
    "God holds the scales. He sees every injustice. Nothing escapes him. "
    "<i>Vengeance is mine, I will repay, says the Lord.</i> (Romans 12:19) The "
    "thrones are occupied. The Judge is not asleep. You do not have to prosecute "
    "every case, level every scale, or hold the door yourself, because you are "
    "not the justice of last resort. And that is not a diminishment. It is the "
    "most liberating sentence in the universe.",
]

QUESTION_BODY_P3 = [
    "But \u2014 and this is where the honest pastoral work begins \u2014 the Architect "
    "in you has not, in practice, believed this at the level where it counts. "
    "At the level of doctrine, yes. At the level of Sunday morning, yes. At the "
    "level of the running internal ledger, the contingency plans, the nightly "
    "inventory of what went wrong today and who did not hold their end \u2014 no. "
    "At that level, the working theology is something like: <i>God is just, but "
    "God is not fast enough, and in the meantime the scales will tip unless I "
    "hold them.</i>",

    "That functional theology is exhausting, and it is the precondition for the "
    "Quiet Exit. When the holding becomes too heavy, when the scales keep tipping "
    "despite your best efforts, when the injustice accumulates past the point the "
    "Architect's systems can absorb it \u2014 the soul looks for a way to stop "
    "holding. And the Quiet Exit is the way it finds.",

    "Before we go further, I want you to use the table below. In the first "
    "column, name a recent event. In the second, answer: was my dignity or "
    "justice genuinely at stake? In the third, answer: was the part of me that "
    "finally matters \u2014 my standing before God, my soul's safety \u2014 at any "
    "point in danger? The gap between columns two and three is the width of the "
    "work that remains.",
]

ARCH_BODY_P1 = [
    "You have built something. You probably did not set out to build it; most "
    "people who construct this kind of architecture do not. It emerged gradually, "
    "over small decisions and real experiences, until it was simply the shape of "
    "how you move through the world. We are going to call it, throughout this "
    "walkthrough, <b>the Architect</b>.",

    "The Architect's strategy is elegant in its logic. <i>If I think it through "
    "carefully enough, prepare thoroughly enough, honor my commitments precisely "
    "enough, and insist that the people around me honor theirs, then the world "
    "will be fair, and fair means safe.</i> The Architect believes \u2014 not in "
    "his mind but in his bones \u2014 that most suffering is a function of "
    "insufficient preparation, insufficient accountability, or insufficient "
    "attention. And so the Architect does not stop building, does not stop "
    "tracking, does not stop noticing.",

    "There is much in Scripture that commends this. <i>The plans of the diligent "
    "lead surely to abundance.</i> (Proverbs 21:5) The Bible does not romanticize "
    "carelessness. Wisdom literature is full of the virtue of foresight, of "
    "seeing consequences before they arrive, of keeping one's word. So the "
    "Architect is not, in himself, a sin. He is a gift. He is also, when "
    "unexamined, a kind of private declaration of independence from God.",

    "The trouble is not with the planning. The trouble is with what the planning "
    "is doing. Under the blueprints is an assumption your mouth would never "
    "quite say aloud: <i>If I do not hold the scales, no one will.</i> That is "
    "not a statement about project management. It is a statement about God, and "
    "about whether the God who holds the scales in Romans 12 is actually to be "
    "trusted with the specific scales in your marriage, your church, your "
    "organization, your family.",
]

ARCH_BODY_P2 = [
    "I want to describe how this wiring gets formed, because you deserve to "
    "understand it from the inside.",

    "The taxonomy research behind this profile consistently surfaces one of two "
    "origins. The first: a home in which the adults were careless or unpredictable "
    "\u2014 not necessarily cruel, but unreliable in a way that meant no one was "
    "holding the door, and you learned early that vigilance was the price of "
    "safety. The second: a home in which love was, in some way, conditional on "
    "performance \u2014 where being good at things was how you earned security. "
    "In both cases, the child's conclusion is the same: <i>I cannot afford "
    "to stop paying attention.</i>",

    "Tolkien, in his letters about <i>The Lord of the Rings</i>, described the "
    "Ring as a picture of what happens when a person places their power, or their "
    "life, into an external object. When the object is threatened, the person is "
    "threatened. The Architect has done something similar with his systems: he "
    "has placed too much of his safety into his structures, and so every threat "
    "to a structure \u2014 every broken agreement, every disregarded plan, every "
    "careless dismissal \u2014 registers not as a management problem but as a "
    "personal wound. Because, in a sense, it is.",

    "The person closest to an Architect usually says some version of the same "
    "sentence: <i>You carry too much.</i> Or: <i>You can never just let it go.</i> "
    "Or, from children: <i>Why does it always have to be such a big deal?</i> "
    "They are not wrong. What they are sensing is that the Architect has never "
    "fully learned the difference between stewardship, which God commands, and "
    "sovereignty, which God reserves for himself. The Architect is running "
    "both lines at once, and it is exhausting everyone, beginning with himself.",

    "Hear me carefully. <b>The Architect is not your enemy.</b> He is a younger "
    "version of you who learned, in a real environment, that vigilance kept "
    "things from falling apart. He deserves your respect, not your contempt. "
    "But the Architect was formed for a specific set of circumstances that no "
    "longer fully obtain. He is still building for a house you no longer live "
    "in, and the building project is taking up too much of the floor plan of "
    "your current relationships.",
]

ARCH_BODY_P3 = [
    "What does it look like to retire him \u2014 not fire him, not dismantle him, "
    "but begin the long, slow process of handing back to God the rooms the "
    "Architect has been securing on God's behalf?",

    "It begins, as almost everything spiritual begins, with naming the assumption. "
    "The Architect has been operating under a functional theology that says: "
    "<i>God is sovereign in heaven; the specifics down here are my department.</i> "
    "He would never say that out loud. It contradicts his stated beliefs entirely. "
    "But his calendar, his contingencies, the mental energy he spends every "
    "evening reviewing what went wrong and by whose fault \u2014 these confess "
    "the working theology more honestly than his Sunday words.",

    "John Owen, in <i>The Mortification of Sin</i>, wrote that you cannot overcome "
    "what you have not named. The first work is always the naming. What the "
    "Architect has not yet named is the specific scale he has been secretly "
    "holding \u2014 the relationship, the institution, the person, the outcome \u2014 "
    "that he believes God cannot be trusted to hold without his help. That is "
    "the scale you need to hand back. Not all scales at once; one at a time, "
    "with prayer and with grief, because the handing-back will feel like loss "
    "before it feels like freedom.",

    "Before we close this section, I want you to receive a letter. I have "
    "written it in the voice of the Architect himself \u2014 as I have heard it "
    "across many conversations and many profiles like yours. Read it as if it "
    "were written to you, because it was.",
]

ARCH_LETTER_INSTRUCTION = [
    "What follows is a letter from the Architect. Read it slowly. After you "
    "read it, use the journaling prompts that follow to write back \u2014 not to "
    "fix him, but to tell him what you are now able to see.",
]

ARCH_LETTER = """\
Dear one,

I have been at this a long time. Longer than you realize, probably, because much of \
what I do I do quietly, at hours when you are not paying attention to me. While you \
sleep I am running the numbers. While you are talking to the people you love I am \
reading the room, watching for the thing that might go wrong, filing the evidence \
of how it has gone wrong before.

I want you to know why I do this. I do this because there was a time \u2014 you \
remember it, even if you have not named it in a while \u2014 when no one else was \
watching. When the scales tipped and stayed tipped, and the adults in the room \
either did not see or did not think it mattered. I started watching then. I have \
not stopped.

I am not asking you to fire me. I know you depend on me, and I know there are \
rooms where the people around you depend on me too. What I am asking you to \
consider is whether I have been asked to hold too much. Whether the weight I am \
carrying was ever mine to carry. Whether some of these scales belong to Someone \
else, and whether I have been reluctant to hand them over because \u2014 if I am \
honest \u2014 I am not entirely sure Someone else will hold them the way I would.

That is the thing I am most afraid of. Not that God will fail entirely. But that \
he will hold things with a looseness I cannot tolerate. That he will allow \
something I would have caught. That I will stand there, watching, and the wrong \
thing will happen, and it will have been preventable, and I will have stood down \
too soon.

I know how that sounds. I know what that confession means, theologically. I am \
telling you anyway, because I think you already knew it without quite having words \
for it. And I think you will not be able to loosen my grip until you have named \
what the grip is actually about.

I am ready to carry less. I am not sure I know how. I am trusting you to help me.

\u2014 The Architect\
"""

ARCH_LETTER_PROMPTS = [
    "Which sentence in the Architect's letter landed with the most weight? "
    "Write it out again here, in your own hand, and then write one sentence "
    "below it: <i>The thing I have not trusted God with is...</i>",
    "The Architect says he is afraid God will hold the scales with a looseness "
    "he cannot tolerate. Is that fear recognizable to you? When did you first "
    "learn to be afraid of that kind of looseness?",
    "Name one specific scale \u2014 one relationship, institution, or outcome \u2014 "
    "that you could hand back to God this week. Not all of them. One. "
    "Write its name here.",
]

VERD_BODY_P1 = [
    "Every mechanism has a place it breaks. The Architect's breakdown is called "
    "<b>the Quiet Exit</b>, and it may be the hardest one to see \u2014 both for "
    "the person experiencing it and for the person on the other side of it.",

    "Here is how it forms. The Architect has done his work: he has planned "
    "carefully, held the scales faithfully, honored his commitments and tracked "
    "whether others honored theirs. The disrespect has been registered. The "
    "injustice has been noted. The Architect has, perhaps, raised the concern "
    "once. Perhaps twice. And the environment \u2014 the marriage, the church, the "
    "friendship, the organization \u2014 has not changed in the way the Architect "
    "needed it to change. The trigger has fired too many times. The scales have "
    "stayed tilted too long. And something in you, very quietly, without "
    "announcement, begins to draft a different kind of plan.",

    "Not a plan to fix it. A plan to leave it. Not always physically \u2014 though "
    "sometimes that too. More often emotionally. The Quiet Exit is the moment "
    "when the Architect's energy, which has always moved <i>toward</i> the "
    "relationship \u2014 toward building it, protecting it, securing it \u2014 "
    "begins, almost imperceptibly, to move away. You stop investing. You stop "
    "hoping. You stop caring whether the scales are level, not because you have "
    "stopped caring, but because you have made a decision, somewhere in the "
    "architecture of your soul, that caring is no longer worth the cost.",

    "What makes this breakdown so difficult to name is that it looks, from the "
    "outside and often from the inside, like health. It looks like maturity. "
    "<i>I've come to terms with it.</i> <i>I've accepted that this person is "
    "who they are.</i> <i>I've stopped needing things from this relationship that "
    "it was never going to provide.</i> These sentences have the grammar of "
    "wisdom. They feel like something a therapist might say, or a pastor, or a "
    "very sane adult who has done the work. And they may, in some cases, be "
    "precisely that. That is what makes them so dangerous: because they can be "
    "that, and they can also be something else entirely.",

    "What they can also be is unbelief wearing the costume of maturity. The "
    "Quiet Exit is the soul's way of protecting itself from further disappointment "
    "by closing the account before the final statement arrives. It is not peace. "
    "It is pre-emptive grief, chosen in advance, because the Architect has "
    "decided \u2014 on evidence that feels ironclad, on a case he has been quietly "
    "building for months or years \u2014 that the verdict is already in.",
]

VERD_BODY_P2 = [
    "Let me say the pastoral thing directly, because the Architect respects "
    "directness.",

    "The Quiet Exit is, in its deepest structure, a crisis of hope. And hope "
    "\u2014 not optimism, not positive thinking, but the particular Christian "
    "virtue of hope \u2014 is precisely what Paul names in 1 Corinthians 13 as "
    "the character of love. <i>Love bears all things, believes all things, hopes "
    "all things, endures all things.</i> (1 Corinthians 13:7) The order of "
    "those four words is not accidental. Paul is describing the shape of love "
    "under pressure. It bears. It believes. It <i>hopes</i>. It endures. The "
    "Quiet Exit is the moment when hope quietly exits the room \u2014 without "
    "drama, without announcement, with perfect composure \u2014 and love, left "
    "behind, slowly loses its engine.",

    "Here is what the Architect must hear about hope, because his instinct will "
    "be to argue with what I am about to say. Christian hope is not the same as "
    "optimism. It is not the insistence that things will turn out the way you "
    "want them to. It is not na\u00efvet\u00e9. It is not the refusal to be "
    "honest about what has happened. Christian hope is the refusal to pronounce "
    "a final verdict on a story that God has not yet finished writing. It is the "
    "patient holding-open of a door that you, on your own evidence, would already "
    "have sealed.",

    "The great Reformed theologian John Calvin wrote, in his commentary on "
    "Romans 5, that hope is <i>the patient expectation of those things which "
    "faith has believed to be truly promised by God.</i> Notice the grammar: hope "
    "expects. It does not calculate probabilities. It does not weigh evidence. "
    "It expects, because the ground of its expectation is not the person's "
    "track record but God's promise. And God has not yet given you the final "
    "statement on the relationship or situation you are in the process of "
    "silently exiting.",

    "The Quiet Exit bypasses this. The Architect, who has been keeping the "
    "ledger, who has the evidence, who has run the numbers \u2014 the Architect "
    "closes the book and says, <i>I have seen enough.</i> And the tragedy is that "
    "he may be right about the evidence. The injustice may be real. The disrespect "
    "may be documented. The failures of the person on the other side may be as "
    "systematic as the Architect says they are. None of that is in question. "
    "What is in question is whether the Architect has the authority to pronounce "
    "the verdict. And the pastoral answer, gentle but honest, is: he does not.",
]

VERD_BODY_P3 = [
    "I want to make a crucial distinction here, because if I do not, I will be "
    "heard as saying something I am not saying.",

    "There are situations in which limits are not only appropriate but necessary. "
    "There are relationships in which the exit \u2014 the real, physical, final "
    "exit \u2014 is the right and even the godly thing. Patterns of abuse, of "
    "chronic disregard, of covenant-breaking so thorough that no reasonable person "
    "could call continued engagement wisdom \u2014 these exist, and I do not want "
    "to speak past them. God-given limits are good. The Architect's sensitivity "
    "to injustice is partly what gives him the discernment to name those "
    "situations correctly when they arise.",

    "What I am describing is something different. I am describing the Quiet Exit "
    "as it fires <i>prematurely</i> \u2014 in relationships and situations that "
    "have not reached that point, where the verdict the Architect has rendered "
    "is not God's verdict but the Architect's, and where the rendering is driven "
    "not by wisdom but by accumulated weariness and self-protection. The pastoral "
    "question is not <i>are limits ever right?</i> The answer to that is obviously "
    "yes. The pastoral question is: <i>in this specific situation, am I drawing "
    "a God-given limit, or am I quietly exiting a story God has not yet finished?</i>",

    "The way to tell the difference is harder than the Architect would like it to "
    "be, because he is accustomed to arriving at verdicts through evidence and "
    "logic, and this distinction requires a kind of honesty that goes below the "
    "evidence. It requires asking: <i>Has my hope gone? And if so, was the exit "
    "of hope something I chose, or something I received?</i> If you chose it "
    "\u2014 if at some point you decided, quietly and without telling anyone, that "
    "the account was closed \u2014 that is not God-given limits. That is the "
    "Quiet Exit. And it needs, with great gentleness, to be named as such.",

    "D. Martyn Lloyd-Jones, preaching on Romans 8, said that the most dangerous "
    "spiritual state is one that has settled into a peace that has not come "
    "from God. Not agitation, not crisis, not obvious sin \u2014 but a settled, "
    "composed, self-secured equilibrium that has displaced the need for God's "
    "answer because the person has quietly resolved the question on their own. "
    "That is what the Quiet Exit looks like from the inside: settled. Resolved. "
    "At peace. The pastoral work is to test the peace.",
]

VERD_PROMPTS = [
    "Name the relationship or situation where you have most recently felt the "
    "Quiet Exit beginning. You do not have to have announced it; you may barely "
    "have admitted it to yourself. Describe what you felt when hope began to "
    "leave. Was it a sudden event, or a slow accumulation?",
    "Ask yourself the honest question: <i>In this situation, am I drawing a "
    "God-given limit \u2014 or am I pronouncing a verdict God has not yet given?</i> "
    "Write the most honest answer you can. Do not edit it for pastoral "
    "acceptability. Write what you actually believe.",
]

TWO_TOG_BODY = [
    "Now we place them side by side, because the Architect and the Quiet Exit "
    "are not two separate problems. They are the same wound, in two phases.",

    "<b>The Architect is what your fear does when it has time and hope.</b> The "
    "Quiet Exit is what your fear does when it has run out of both. The Architect "
    "plans so the alarm will never have to ring. The Quiet Exit is what happens "
    "when the alarm has rung too many times and the Architect has quietly stopped "
    "believing the building is worth protecting.",

    "The sequence, in slow motion, looks like this. <b>(1)</b> The Architect "
    "builds. He plans, prepares, tracks commitments, maintains the ledger. "
    "<b>(2)</b> An event lands: a disrespect, an injustice, a dismissal, a "
    "pattern that repeats. The trigger fires. The body says <i>something is "
    "wrong here.</i> <b>(3)</b> The core question wakes: <i>Am I protected?</i> "
    "<b>(4)</b> The Architect tries to answer it by rebuilding, adjusting, "
    "holding the scales more tightly. <b>(5)</b> The rebuild does not hold. "
    "The scales tip again. Another event lands. The trigger fires again. "
    "<b>(6)</b> At some point \u2014 not in a single dramatic moment but in "
    "a quiet internal shift \u2014 the Architect stops directing his energy "
    "toward the relationship and begins directing it away. <b>(7)</b> The Quiet "
    "Exit has begun. And because it looks like peace, no one notices, and "
    "the departure continues.",

    "What breaks this sequence is not a better plan, and it is not more "
    "patience, and it is not a better argument about the evidence. What breaks "
    "it is a different answer to the question. Until you receive \u2014 really "
    "receive, not just affirm \u2014 that the scales are held by hands that do "
    "not tire, that you are protected in the place that finally matters, that "
    "hope is not na\u00efvet\u00e9 but the refusal to pronounce verdicts that "
    "belong to God \u2014 the loop has nothing to push against. With that answer "
    "received, the loop begins, slowly, to lose its power. The Architect plans "
    "fewer contingencies. The Exit begins to close.",

    "Below is your sequence, in a form you can fill in with your own words. "
    "When you are finished, read it aloud. The Architect and the Exit both "
    "lose something when they are named in your own voice.",
]

TWO_TOG_TEMPLATE = (
    "When ____________________  happens, my body reads it as disrespect or "
    "injustice, and the old question surfaces \u2014 <i>am I protected?</i> "
    "My first move is to ____________________, because the Architect in me "
    "believes that if I can ____________________, the scales will level. "
    "When that does not work, and the wound accumulates past the point I can "
    "absorb, I begin to ____________________. The Exit feels like "
    "____________________, but what it actually is, underneath, is "
    "____________________. What I most need to receive, in that moment, "
    "is not a better plan but the truth that ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a set of practices, each small enough "
    "to carry and useful enough to reach for. None will fix you in a season. All "
    "of them, used over months, will loosen the grip of the loop you have just "
    "named.",

    "I have divided them into two sets: tools for when the Architect is "
    "overworking \u2014 when the planning has tipped into private sovereignty "
    "\u2014 and tools for when the Quiet Exit has begun or is beginning, and you "
    "need to interrupt the departure before it becomes permanent.",
]

ARCH_TOOLS = [
    ("The sovereignty audit",
     "Each evening, write down one thing you managed or controlled today that "
     "was not, strictly, your department. Do not scold yourself; simply notice. "
     "Name it: <i>This was God's to hold, and I took it back.</i> Over thirty "
     "days, the Architect begins to see his own pattern from the outside, which "
     "is the beginning of handing it back."),

    ("Steward's prayer",
     "Each morning, write the names of two specific situations facing you that "
     "day. After each one, write the single sentence: <i>I will steward this "
     "faithfully and hold it loosely, because you are the keeper of scales I "
     "cannot see.</i> Read it aloud. The Architect will resist this. Do it "
     "anyway."),

    ("The incompleteness fast",
     "Once a week, choose one situation you would normally track to a "
     "resolution and deliberately leave it in God's hands overnight without "
     "touching it. Make a note of what you feel when you do. This is not "
     "passivity; it is a rehearsal of the difference between stewardship and "
     "sovereignty, practiced in a low-stakes setting so it is available in "
     "the high-stakes ones."),

    ("The Psalm for the tired planner",
     "When you feel the weight of the scales, open to Psalm 73 and read it to "
     "the end. Not the beginning \u2014 the end. Asaph runs the same ledger the "
     "Architect runs, and comes to the same weariness. Then he enters the "
     "sanctuary, and the perspective shifts. He does not get a new plan. He "
     "gets a new vantage point. Let the end of Psalm 73 be the Architect's "
     "regular re-orientation."),
]

VERD_TOOLS = [
    ("The exit inventory",
     "When you notice the Quiet Exit beginning \u2014 when you catch yourself "
     "caring less, investing less, hoping less \u2014 write down the name of the "
     "relationship or situation. Then write two sentences: (1) <i>The evidence "
     "I am holding.</i> (2) <i>The verdict I have rendered.</i> Seeing the "
     "verdict written down is often the first time the Architect recognizes it "
     "as a verdict rather than a conclusion. Verdicts require authority. "
     "Conclusions require evidence. Which one is this?"),

    ("The hope question",
     "Ask yourself, honestly: <i>When did I stop hoping in this situation? "
     "Was that a moment I received \u2014 in which God gave me a settled sense "
     "that this season was over \u2014 or was it a moment I chose, because "
     "hoping had become too costly?</i> Write the answer. The difference between "
     "those two origins is the difference between a God-given limit and the "
     "Quiet Exit. Both deserve to be named accurately."),

    ("Tell one person the door is closing",
     "The Quiet Exit lives on secrecy. It is a private verdict, rendered in "
     "private, that slowly becomes permanent because no one ever spoke into it. "
     "Before the door closes, tell one trusted person \u2014 your spouse if "
     "possible, a pastor, a friend who knows you \u2014 that you have been "
     "pulling back. Not to fix it in that conversation. Simply to break the "
     "secrecy. The Exit loses power when it is exposed to light."),

    ("The 1 Corinthians 13 test",
     "Sit with 1 Corinthians 13:7: <i>Love hopes all things.</i> Ask, quietly: "
     "<i>Am I hoping in this situation, or have I stopped?</i> If you have "
     "stopped, ask a further question: <i>What would it cost me to hope again "
     "for one week \u2014 not to expect a particular outcome, but to hold the "
     "door open rather than sealed?</i> Trying one week of deliberate hope is "
     "not the same as na\u00efvet\u00e9. It is a small act of obedience to "
     "the shape of love Paul describes."),

    ("The confession that fits",
     "When you recognize the Quiet Exit in yourself, the appropriate response "
     "is not self-criticism. It is confession. Say, quietly or in your journal: "
     "<i>I have pronounced a verdict that was not mine to pronounce. I have "
     "allowed hope to leave without asking you whether you were finished. "
     "I hand this back to you.</i> Then wait. The Architect is not accustomed "
     "to waiting. Practice it."),
]

PRAYER_BODY = [
    "Father,",

    "You see the Architect in me, and you are not surprised by him. You know "
    "which rooms in my history he was first built to hold, and you know what it "
    "cost to hold them. I am not asking you to dismantle him. I am asking you "
    "to teach him, slowly, the difference between the scales I have been asked "
    "to hold and the scales you have reserved for yourself. I have been "
    "confusing the two for a long time. I have been carrying what you did not "
    "ask me to carry, and I am tired.",

    "Lord Jesus, there is a relationship \u2014 you know which one \u2014 where "
    "I have already begun to leave. Not with my body, and perhaps not yet with "
    "my words, but somewhere in the architecture of my soul the door has been "
    "closing, quietly and without announcement, because I have been more "
    "committed to protecting myself from further disappointment than to "
    "hoping in what you might yet do. I confess the verdict I have been "
    "quietly rendering. I do not know if it is the right verdict or the wrong "
    "one; what I know is that I rendered it without asking you. Forgive me "
    "for that. I hand the case back to you.",

    "Help me to know the difference between a God-given limit and a premature "
    "exit. Help me to sit with open hands where you have not yet closed a "
    "door. Give me the particular courage of 1 Corinthians 13: to bear, to "
    "believe, to <i>hope</i>, to endure \u2014 not by my own resources, which "
    "are genuinely spent, but by the Spirit who is more committed to my "
    "remaining open than I am.",

    "Holy Spirit, where I have been building my own fortress, give me the "
    "courage to step inside yours. Where I have been closing accounts, "
    "give me the grace to leave the ledger on your desk. Where the Quiet "
    "Exit has already begun, would you be the one who calls me back to the "
    "door before it seals.",

    "In the name of the One who, from the cross, prayed <i>Father, forgive "
    "them</i> \u2014 who did not exit, but endured, because he knew the "
    "Father held the scales \u2014 I pray.",

    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning. The Architect and the Quiet Exit have been "
    "with you long enough to have deep roots, and one reading will not pull them "
    "up. What follows is a short set of next steps \u2014 concrete, honest, "
    "unhurried \u2014 for the work that has just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.",
     "Different paragraphs will land. The Architect will resist a second "
     "reading; the Exit will tell you there is nothing new to find. Both are "
     "wrong. Come back."),

    ("Take one tool, not five.",
     "Choose the single practice from Section 7 that is most directly relevant "
     "to where you are right now. Try it for two weeks before adding another. "
     "The Architect will want to implement them all systematically. That is "
     "itself worth noticing."),

    ("Name the door that is closing.",
     "Tell one trusted person \u2014 your spouse, a pastor, a close friend "
     "\u2014 the name of the situation where the Exit has begun. Not to fix it "
     "in that conversation. Simply to break the secrecy. Say: <i>I have been "
     "pulling back from ___, and I wanted someone to know before the door "
     "closes all the way.</i>"),

    ("Read the Psalms of lament.",
     "Psalm 10, Psalm 13, Psalm 22, Psalm 73, Psalm 88. These are the psalms "
     "of people who asked <i>Am I protected?</i> and did not receive the answer "
     "quickly. Pray one aloud each morning for a week. Notice which lines you "
     "cannot get through without stopping. Those are the lines for you."),

    ("Read further on hope and suffering.",
     "Tim Keller, <i>Walking with God through Pain and Suffering</i>. C. S. "
     "Lewis, <i>A Grief Observed</i>. David Powlison, <i>God\u2019s Grace in "
     "Your Suffering</i>. Each of these is a faithful companion for the "
     "particular work the Quiet Exit asks of you."),

    ("If the door has already closed, ask for help.",
     "There are seasons when the Exit has proceeded far enough that you cannot "
     "interrupt it alone. A wise pastor, a Christian counselor, a trusted "
     "elder who knows you well \u2014 these are not signs of failure. They are "
     "part of God's answer to the prayer you just prayed."),
]

GOING_FURTHER_CLOSING = (
    "You are not a person who ran out of hope because you were weak. You are a "
    "person who carried more than you were meant to carry, for longer than "
    "anyone should have to, and the Exit began as self-protection. "
    "God does not despise that. He meets you there. "
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
        [Paragraph("WAS MY DIGNITY AT STAKE?", header_style), Paragraph("your nervous system's reading", sub_style)],
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
    """Generate the Architect+Verdict (Quiet Exit) walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="ARCHITECT  \u00b7  QUIET EXIT",
        title="Take 139 Walkthrough \u2014 Architect + Quiet Exit",
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
    story.append(Paragraph("The Architect &nbsp;\u00b7&nbsp; The Quiet Exit", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disrespect / Injustice &nbsp;\u00b7&nbsp; Core Question: Am I protected?",
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
                   "Disrespect and Injustice.",
                   "The accumulation that keeps happening to you.")
    for p in TRIGGER_BODY[:4]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  CONTINUED",
                   "The ledger you have been keeping.",
                   "What the fatigue is telling you, and what it is not.")
    for p in TRIGGER_BODY[4:]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will rationalize; your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=5)
        story.append(Spacer(1, 14))
    story.append(PageBreak())

    # ── SECTION 3: Core Question ──
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I protected?",
                   "The wound the alarm is standing guard over.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>What Scripture actually says.</b>", S["H3"]))
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>The functional theology.</b>", S["H3"]))
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table())
    story.append(PageBreak())

    # ── SECTION 4: Mechanism ──
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Architect.",
                   "What you have built, and what it was built for.")
    for p in ARCH_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>How the wiring was formed.</b>", S["H3"]))
    for p in ARCH_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>Retiring him, not firing him.</b>", S["H3"]))
    for p in ARCH_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Architect.",
                   "Read it as if it were written to you. Because it was.")
    for p in ARCH_LETTER_INSTRUCTION:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_callout(S, "THE ARCHITECT WRITES:", ARCH_LETTER))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Write back to him — not to fix him, but to tell him what you can now see.", S["Prompt"]))
    story.append(Spacer(1, 4))
    for prompt in ARCH_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Quiet Exit.",
                   "The saddest thing the Architect does \u2014 and the one most disguised as health.")
    for p in VERD_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>Unbelief wearing the costume of maturity.</b>", S["H3"]))
    for p in VERD_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>The crucial distinction.</b>", S["H3"]))
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
                   "Architect and Exit are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  YOUR SEQUENCE",
                   "Write it in your own words.",
                   "Fill the blanks. Read it aloud when you are done.")
    story.append(Spacer(1, 6))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=6)
    story.append(PageBreak())

    # ── SECTION 7: Tools ──
    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "What to do when you feel the loop start.",
                   "Small enough to carry; useful enough to reach for.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 6))

    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Architect is overworking.",
                   "Four practices for the time before the alarm fires.")
    for name, desc in ARCH_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Quiet Exit has begun.",
                   "Five practices for interrupting the departure before it seals.")
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
