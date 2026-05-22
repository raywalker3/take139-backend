"""Personal Walkthrough — Architect + Plea.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disrespect or Disconnection trigger, "Am I protected?" / "Am I lovable?" core question.
Unique profile: The Architect whose mechanism collapses not into litigation but into panic-pursuit.
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
    "Before you read any further, I want to do something for you that a good pastor does at the beginning of a hard conversation. I want to slow us down. What you are about to read is not a personality profile. It is not a list of tendencies or a chart of your temperament. It is a careful look at the way your soul has learned, over a long time, to keep itself from harm — and what happens when that strategy meets something it cannot handle.",
    "We are going to walk through your trigger — the specific kind of moment that makes something inside you tighten and then move very fast. We are going to listen to the question underneath that moment, the one that has probably been asking itself since you were young. We will name the strategy you constructed to answer that question, and the place that strategy breaks open under pressure. And only then will we hand you tools.",
    "I want to say something plainly, before we go further, because you deserve to hear it. <b>What follows is true, but it is not the whole truth about you.</b> The whole truth includes a Father who has not abandoned you to make your own peace; a Son who took upon himself the full weight of everything you are afraid of; and a Spirit who is, at this very moment, working more patiently and more thoroughly in you than you are working in yourself.",
    "So read slowly. Argue with what does not fit. Sit with what does. Write in the margins. If a sentence catches in your throat, stay there a moment — that catch is almost always the Lord putting his finger on something worth looking at together. The goal of what follows is not insight for its own sake. It is a slightly freer life, lived with a slightly looser grip, in front of a God who has nothing to gain from your anxiety and everything to give to your rest.",
    "This chapter about yourself has been a long time in the writing. It deserves a few hours of patient, unhurried attention.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you. It usually has very little warning. A tone shifts in a conversation. Someone you love answers a question with one word when they usually use twenty. A plan you put real care into is changed without asking you. And something inside you moves — quickly, and not always in the direction you would choose.",
    "On the surface, this may appear to be ordinary sensitivity. In reality, your body has just registered something your nervous system treats with extreme seriousness. The signal is not merely <i>I have been overlooked</i>. The signal lands deeper: <i>the connection is at risk, and if it breaks, I will not be safe.</i>",
    "This is your trigger. It may have the face of <b>disrespect</b> — someone failing to honor what you have built or offered. It may wear the face of <b>disconnection</b> — someone moving away from you in ways that register as a small emergency. Often, for you, the two are tangled: distance feels like dismissal. When someone pulls back, your body reads it as a verdict on your worth.",
    "C. S. Lewis, in <i>The Four Loves</i>, observed that every act of love makes the one who loves more vulnerable — that to love is to hand another person a capacity to wound you. This is true of all of us, but it is especially true of you. The same sensitivity that allows you to read a room and care well for the people in it is the same sensitivity that makes a shift in tone feel, to your body, like a storm warning.",
    "Here is something important to see without flinching. <b>Your sensitivity to disrespect and disconnection is not a weakness in your character.</b> It is the residue of something real. There were moments — likely early, sometimes few in number but impossible to forget — in which the people responsible for your safety either used their power carelessly over you or withdrew in ways that made you feel as though your standing in their world was conditional. You learned that closeness could be revoked, that approval had to be maintained, and that when someone moved away from you it was wise to move toward them, fast, before the gap became permanent.",
    "It may have been a parent whose warmth was intermittent — present when things went well, cooler when they did not. It may have been a household in which the emotional temperature was never quite predictable and you became very good, very early, at reading signs and adjusting accordingly.",
    "Whatever its origin, the lesson lodged in you was this: <i>when someone moves away from me, I need to close the gap, and I need to close it now.</i> And so your body learned a kind of relational vigilance — watching for the early signs of withdrawal, moving toward people before the separation can solidify. This is a remarkably intelligent adaptation to a world that required it of you. But you are no longer in that world, and the alarm that served you then is firing many times a day in circumstances that do not require it.",
    "Before we go further, take a breath. Answer two questions in writing. Not in your head — your head will manage and spin the question. Your hand will tell you what your head is trying not to say.",
]

TRIGGER_PROMPTS = [
    "Think of the last week. Name one moment when you felt the distance between yourself and another person, or when you felt dismissed or disregarded. What happened, in two sentences?",
    "What was the actual size of the event? What was the size of the movement inside you in response to it? If those two things did not match, you have just located your trigger.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question. The trigger is the alarm; the question is what the alarm is built to protect. The question is older than the trigger, and older than the relationships in which the trigger fires. It was there, in some form, before most of your memories.",
    "For you, the question has two faces, and they sometimes appear together. The first: <b>Am I protected?</b> The second, which you may recognize even more painfully: <b>Am I lovable?</b> Not <i>am I liked</i> — that is a shallower version. The deeper form is this: <i>If someone sees all of me — the real version, with the failures and the fears and the places I have not yet sorted out — will they still want to stay?</i>",
    "These two questions are cousins. The person who asks <i>Am I protected?</i> is wondering whether there is someone between them and what could hurt them. The person who asks <i>Am I lovable?</i> is wondering whether they are the kind of person who deserves that protection in the first place. You have probably lived with both, and they have probably reinforced each other: when you feel disrespected, you feel unloved; when you feel unloved, you feel unprotected; when you feel unprotected, you feel unsafe. The loop is swift and not always visible from the inside.",
    "Most adults would prefer to believe they have long since outgrown these questions. We have not. We have only become sophisticated at hiding them from ourselves. The adult versions sound more reasonable — <i>Can I trust this person? Will my spouse be there for me when it actually matters? Does this community have room for me if I am not at my best?</i> — but they are the same questions. And for you, they do not stay buried for long. Something happens, the distance opens, and the question is awake again, looking for an answer.",
]

QUESTION_BODY_P2 = [
    "The Psalms — the prayer book that Jesus himself used — are astonishing documents partly because they refuse to pretend these questions go away. They are full of people who are not sure whether God can be trusted with their safety, who feel abandoned, who cry out for reassurance and do not always hear an answer as quickly as they need one.",
    "<i>How long, O Lord? Will you forget me forever? How long will you hide your face from me?</i> (Psalm 13:1) And then, in the same short psalm, the turn: <i>But I have trusted in your steadfast love; my heart shall rejoice in your salvation.</i> (Psalm 13:5) David does not resolve the question by getting a better situation. He resolves it by returning to a conviction that precedes his circumstances. The steadfast love — the Hebrew <i>hesed</i>, covenantal faithfulness that cannot be undone — is the floor he falls back to when the question gets loudest.",
    "The gospel anchor for your particular question is this: <b>I am an Adopted Son — or Daughter.</b> The love the Father has for his own Son flows toward you because you are in Christ. Paul, in Romans 8, places this adoption alongside the very question of protection: <i>If God is for us, who can be against us? He who did not spare his own Son but gave him up for us all, how will he not also with him graciously give us all things?</i> (Romans 8:31–32) The argument is startling in its simplicity. The most costly thing God had to give, he gave. Everything lesser is already covered by that gift.",
    "But here is where you have to be honest with yourself. <b>The biblical answer to <i>Am I lovable?</i> is not the answer your nervous system wants.</b> Your nervous system wants to be convinced by what it can feel — by the warmth of the person in front of you, by reassurance through eye contact and tone. Scripture does not say that feeling is wrong. It says that feeling is not the foundation. The foundation is a covenant made before the world existed, sealed in blood, ratified in an empty tomb. Your lovability is not a question God is still deliberating. He deliberated it before you were born, in Christ, and the answer was yes.",
]

QUESTION_BODY_P3 = [
    "This is where the honest work must happen. Because the Architect in you has spent years trying to construct a relational environment so carefully ordered that the question of your lovability would never have to be asked. You have planned and managed and anticipated. You have done the right things. You have given well. And then, when the question wakes up anyway — when someone is distant, when the warmth you worked for does not appear — the gap between your effort and your result registers not as disappointment but as something closer to catastrophe.",
    "John Owen, the Puritan theologian, wrote with unusual precision about what he called the soul's tendency to seek its rest in what it can see and manage rather than in the invisible steadfastness of God. He said that the soul in its unrenewed state prefers a certainty it can hold in its hand over a certainty it can only receive by faith — and that this preference, unchallenged, is a form of practical atheism, however orthodox the theology that lives upstairs. The Architect's version of this is the belief that a good enough relational system will answer the question. It will not. It has not yet. It cannot.",
    "The peace the gospel offers you is not the peace of having secured the relational outcome you need. It is the peace of knowing that your standing — before the only One whose opinion of you is finally determinative — has been settled, not by your work, but by Christ's. This peace is strange and slow. It takes years to reach the level of the body. But it is the only peace that does not eventually demand a toll.",
    "Before we move forward, I want you to sit with one question in writing. It is the most important question in this section, and it deserves more than a quick answer.",
]

QUESTION_TABLE_INTRO = (
    "Use the table below. In the first column, name a recent moment when the question "
    "<i>Am I lovable?</i> or <i>Am I protected?</i> woke up. In the second, write what you "
    "did in response — what did the Architect do to try to close the gap or secure the answer? "
    "In the third, write the gospel word that speaks to what you actually needed: "
    "<i>the love of the Father, given in Christ, that no distance can remove.</i>"
)

ARCH_BODY_P1 = [
    "You have built something. Most people who build what you have built did not set out to build it. It came together slowly, one small response at a time, in the presence of circumstances that rewarded care and planning and penalized what felt like carelessness. Over years, you became very good at it. We are going to call it, throughout this walkthrough, <b>the Architect</b>.",
    "The Architect's governing conviction is this: <i>If I think carefully enough, prepare thoroughly enough, and attend to the right details, I can make the people I love feel safe — and I can keep the connection I need from being threatened.</i> The Architect applies his drafting energy not only to projects and plans but to relationships. He reads what is needed, plans his responses, manages the emotional climate around him. He is, in the best sense of the word, thoughtful. People around him tend to feel cared for, because he genuinely cares — and because he has studied how to show it.",
    "There is real virtue here. Proverbs commends this kind of attention. <i>The plans of the diligent lead surely to abundance, but everyone who is hasty comes only to poverty.</i> (Proverbs 21:5) The Architect is not a fool, and his carefulness is not a sin. The Scriptures honor the person who thinks before he speaks, who attends to what is required, who brings order where there was disorder. The Architect is, in many ways, a gift to the people around him.",
    "But underneath all the careful management is an assumption we need to name directly. The assumption is: <i>the connection I need is something I must maintain by my own effort, because if I let my vigilance drop, something will break and I will not be able to repair it.</i> Which is, when you say it plainly, a statement about the nature of love. It says: love is conditional enough that it requires constant maintenance. It says: the gap between me and the people I need is always potentially fatal, and I am the one responsible for keeping it closed.",
]

ARCH_BODY_P2 = [
    "The Architect's origin story is usually not dramatic. It rarely involves a single catastrophic rupture. More often it involves a pattern — a household in which relational warmth was available but not guaranteed, in which the child learned that certain behaviors produced closeness and others produced distance, in which the adults were doing their best but were limited enough that love felt, in some real sense, conditional on performance. The child did not consciously decide to become an Architect. He simply noticed what worked, and kept doing it.",
    "Tolkien, in his letters about <i>The Lord of the Rings</i>, wrote that the great temptation of the Ring was not power for its own sake but the desire to do good — to order and arrange things well — through one's own strength. He called it a kind of sub-creation gone wrong: the gift of making, bent toward self-reliance. The Architect understands this. The drive to plan and arrange is not simply self-protection. Part of it is genuine love. Part of it is the real and good desire to see things go well for the people you care about. But it has been bent, over time, into a system that must produce results — and when it does not, something breaks.",
    "The person closest to an Architect knows this before the Architect does. They experience it as a particular kind of pressure — not aggressive, not demanding, but present. The Architect's care has a certain weight to it. You can feel that someone is tracking you, monitoring the relational temperature, making adjustments. It is not always unwelcome. But there are seasons when the person you love most wants to say: <i>you do not have to manage this. I am not going anywhere. You do not have to keep building in order to keep me.</i>",
    "<b>Hear this carefully.</b> The Architect in you is not your enemy. He is a younger self who learned, in real circumstances, that vigilance was required and that lapses cost something. He has been faithful, in his way, for a long time. He deserves your respect. But he is carrying a burden that was never his to carry — the burden of securing, through his own effort, the love that was given to him as a gift in Christ before he ever built anything.",
]

ARCH_BODY_P3 = [
    "What does it look like to begin retiring him? Not dismissing him — he has done real work. <i>Retiring</i> him, in the honorable sense. Giving him fewer hours. Letting him still draft the occasional blueprint, still offer his careful attention, but releasing him from the weight of keeping the relationship alive by sheer management.",
    "It begins with naming the assumption he operates under. The assumption is: <i>God's love is real, but it is not concrete enough to count on in the moment when someone moves away from me.</i> The Architect would never say that in a theology classroom. He affirms divine love without hesitation. But his relational calendar — the constant checking, the managed conversations, the apologies offered before they are needed — confesses something different. It confesses that, at the level where it actually counts, he does not yet believe that the Father's steadfast love is sufficient for this moment.",
    "Letting go of that assumption is not a decision made once. It is a practice, returned to again and again, of trusting the love you have already been given rather than engineering the love you still fear you might lose. It will feel, at first, like negligence. Like letting go of the only rope you can see. It is not negligence. It is the slow discovery that you are not, in fact, holding yourself up. You were held before you started building, and you will be held when the building is finally set down.",
    "Before we close this section, I want you to hear a letter. Not from me. From the Architect himself. I have written it in his voice — the voice that has been running this project in you for a long time. Read it slowly, and then write back to him in the space provided.",
]

ARCH_LETTER_BODY = """\
<i>Dear one,

I know you may not have thought of me as a letter-writer. I am usually more comfortable with plans than with words. But I want to say something true to you, which I have not been able to say inside all the noise of the managing.

I built this to keep you safe. I know you know that. But what I am not sure you know is how frightened I was — and still am — underneath all the organizing. Every blueprint I draw is, at some level, an argument against the possibility that the people you need might leave. Every careful conversation, every preemptive apology, every managed emotional temperature is me saying: <i>please, not again, please stay.</i>

I learned this in a world where the connection was not guaranteed. I am not wrong that it was a real world. I am not wrong that the gap, when it opened, hurt. But I have been doing this work in circumstances that are different from the ones that trained me, and I think I have been getting in the way of something that was trying to reach you.

What I am most afraid of is this: that if I stop building, you will find out how little you have in you apart from the building. That the love you need will not hold if you are not maintaining it. That you are only worth keeping when you are useful.

I am telling you this because I think that fear is a lie — but I have not been able to stop believing it on my own. I need you to show me something I cannot show myself. I need you to hand this to Someone larger than both of us, and then stay close enough to see what happens.

I am not going away. But I am ready to work fewer hours. Are you ready to let me?

— The Architect</i>"""

ARCH_LETTER_INSTRUCTION = [
    "Read that letter twice. The second time, notice the sentence that lands heaviest. Then use the lines below to write back. What do you want to say to the part of you that has been managing all of this? Be honest with him — he will know if you are not.",
]

PLEA_BODY_P1 = [
    "Every mechanism has a place it breaks. Yours is called <b>the Plea</b>. And if you have not already recognized it, you will by the end of this section.",
    "Here is how it happens. The Architect has done his work — has planned, prepared, managed, tended the relational temperature with real care. And then something happens that the managing cannot hold. A conversation goes unexpectedly cold. A person you love does not respond the way you needed them to respond. The distance opens — even slightly, even in a way that most people would not clock — and something in you moves. Not slowly. Fast.",
    "The Plea does not prosecute. It does not go silent. It does not build a case or retire to the island of its own interior world. It pursues. It moves toward the gap at a speed that bypasses the part of you that knows, intellectually, that the gap may not require emergency action. You apologize — sometimes for things you did not do, or for things that were not actually wrong, because in the moment the specific content of the apology matters less than the closing of the distance. You offer concessions. You soften positions you were right to hold. You volunteer to carry more than your share. You do all of this not out of genuine conviction but out of the need to hear someone say: <i>we are still okay.</i>",
    "I want to describe this with care, because the Plea can look like humility and it can feel like love, and it is important to be honest about what it actually is. It is love's panic-stricken cousin. Real humility is slow and clear-eyed; it acknowledges wrong because it has actually recognized wrong. The Plea is fast and frightened; it acknowledges whatever is necessary to close the gap, whether or not the acknowledgment is true. Real love gives freely; the Plea gives at a rate that the giver will, quietly and resentfully, require to be repaid.",
]

PLEA_BODY_P2 = [
    "Here is the particular shape that the Plea takes in an Architect, which is worth naming precisely because it differs from how the Plea works in other wiring profiles. An Architect does not lose his ability to think clearly under pressure. He redirects it. Instead of drawing blueprints for the project he is stewarding, he draws blueprints for the repair. He plans the apology before he delivers it. He rehearses the concessions. He maps the conversation he needs to have and tries to control its outcome. The energy he usually puts into construction now goes entirely into the emergency repair of the connection he feels slipping.",
    "What this means is that the people on the receiving end of the Plea often cannot tell whether they are being truly apologized to or cleverly managed. Because both look careful. Both look thought through. The Architect's Plea is not impulsive in the way that some breakdowns are impulsive — it arrives with preparation and sincerity of tone. But the sincerity is in the service of connection-recovery, not in the service of truth. And the people who know you best begin, over time, to feel the difference.",
    "There is a further cost that takes longer to appear. The Architect who pleads too readily — who apologizes for things he did not do, who yields on matters of genuine conviction in order to close the gap — does not discharge the debt. He files it. He is not aware of filing it, but the ledger is open. Some months or years later, when the resentment surfaces, he will be confused by its size, because he forgot that every false apology was a deposit. <b>This is one of the most important things to understand about the Plea: what it costs you is not the apology itself. What it costs you is the self that knows the difference between true contrition and relational management, and learns, slowly, not to trust that self.</b>",
    "Martin Luther, who knew something about the difference between false peace and genuine reconciliation, put it this way in the opening theses of the Reformation: <i>when our Lord and Master Jesus Christ said 'Repent,' he willed the entire life of believers to be one of repentance.</i> Repentance, in Luther's understanding, was not a quick ceremony for closing the gap between people. It was a whole-life orientation toward truth — including the truth about what one had actually done wrong and what one had not. The Plea skips this discernment step. It offers repentance wholesale, regardless of whether it has first counted the actual cost of the wrong. And this wholesale repentance is, in Luther's terms, not repentance at all. It is the performance of repentance in the service of self-protection.",
]

PLEA_BODY_P3 = [
    "This is the pastoral word this section must say directly, because it is the word this profile most needs to hear and most seldom gets: <b>there is a difference between peacekeeping and peacemaking, and the Plea has confused them.</b>",
    "Dietrich Bonhoeffer, in <i>The Cost of Discipleship</i>, wrote about what he called cheap grace — the grace that excuses without transforming, that forgives without requiring genuine confrontation with what is wrong. There is a relational equivalent he might have named had he written more about marriage and conflict: cheap reconciliation. Cheap reconciliation is the restoration of surface warmth without the truth-telling that genuine restoration requires. It closes the gap, yes. But it closes it over something unresolved, and the unresolved thing does not disappear. It waits.",
    "Jesus, in Matthew 5:9, calls the peacemakers blessed — not the peacekeepers. The distinction is not small. A peacekeeper avoids conflict in order to preserve a relational surface. A peacemaker enters conflict in order to produce genuine resolution. The peacekeeper's goal is the absence of friction. The peacemaker's goal is the presence of truth and love together, even when that requires a season of discomfort. The Plea, at its core, is a peacekeeping instrument dressed in the language of repentance. It produces the appearance of resolution without the substance of it.",
    "What you need — and what the people you love need from you — is not faster repair. It is slower, more honest repair. The repair that says: <i>I am not sure I was wrong here. Can we look at it together?</i> Or: <i>I know I hurt you, and I want to understand exactly how before I apologize, because I want the apology to be true.</i> This kind of repair is slower. It allows the gap to stay open longer. It requires you to sit in the discomfort that the Plea exists to eliminate. But it produces something the Plea cannot: a connection built on the actual ground of what is true, rather than on the soft agreement not to examine it.",
]

PLEA_PROMPTS = [
    "Think of the last time the Plea ran. Did you apologize for something you were not actually convinced was wrong, in order to close the distance? Name it.",
    "What did you file in the ledger? What did you give that you later — quietly, privately — required to be repaid? Be honest here. No one will read this but you and the Lord.",
]

TWO_TOG_BODY = [
    "Now we stand back and look at both of them together, because the Architect and the Plea are not two different problems. They are the same fear, expressed through two different registers.",
    "<b>The Architect is what your fear does when it has time.</b> It plans, arranges, manages the relational temperature, attempts to construct an environment in which the question — <i>Am I loved? Am I protected?</i> — never has to be asked. <b>The Plea is what your fear does when the Architect's system fails.</b> When the gap opens anyway, the Plea takes the floor and runs: pursues, apologizes, concedes, and pays whatever price is asked before the distance can become final.",
    "Together they form a closed loop. <b>(1)</b> You plan and manage with genuine care, because you love well and because the Architect believes good management keeps the connection safe. <b>(2)</b> Something happens that management cannot prevent — a disconnection, a dismissal, an unexpected coldness. <b>(3)</b> The trigger fires. <b>(4)</b> The question wakes up: <i>Am I lovable? Am I protected?</i> <b>(5)</b> The Architect tries to answer it by engineering the repair. <b>(6)</b> When the engineering does not produce warmth quickly enough, the Plea overrides it and gives things away — apologies, concessions, false agreements — to close the gap at any cost. <b>(7)</b> The gap closes, the question quiets, but the ledger is not empty, and the next trigger arrives a little faster.",
    "What breaks this loop is not better planning and not faster repair. It is a different answer to the question, received deeply enough to reach the level of the body. The peace the gospel offers you is not the peace of having a close connection at all times. It is the peace of knowing that the connection that finally counts — your standing before the Father in Christ — cannot be disrupted by any human distance, and therefore does not require emergency management.",
    "Below is your sequence, in a brief template. Fill in the blanks. Then read it aloud. The Architect and the Plea both lose some of their urgency when the loop is named clearly.",
]

TWO_TOG_TEMPLATE = (
    "When I feel ____________________, my body reads it as disconnection or disrespect, "
    "and the old question surfaces — <i>am I lovable? am I protected?</i> My first move is "
    "to ____________________, because the Architect in me believes that if I can just "
    "____________________, the gap will close. When that does not work, the Plea takes "
    "over and I find myself ____________________. What I am actually offering is "
    "____________________ — but what I am actually after is the word "
    "____________________. That word has already been spoken over me, in Christ, in "
    "____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. Each practice is small enough to carry with you, and useful enough to make a difference when the loop begins to run. None of them will rewire you in a week. All of them, used patiently over months, will loosen the grip of the pattern you just named.",
    "I have divided them into two sets. The first is for the Architect — for the seasons when you are managing and planning and over-engineering the relational environment. The second is for the Plea — for the moments when the gap has just opened and the panic is already moving. Both sets are needed, because both parts of the loop need to be interrupted.",
]

ARCH_TOOLS = [
    ("The stewardship question", "When you catch yourself planning a repair before a rupture has actually occurred — rehearsing an apology for a conversation that has not yet happened, managing an outcome that does not yet need managing — stop and ask one question aloud or in writing: <i>Am I stewarding this relationship, or am I trying to be sovereign over it?</i> Stewardship is what God has asked of you. Sovereignty is what he has reserved for himself. The Architect almost always answers that question truthfully when he is required to say it in plain language."),
    ("The handed-back prayer", "Each morning, name one person or relationship that the Architect is currently managing, and say — aloud, if you can — the following: <i>This belongs to you today, Lord. I will be faithful. I will not be God.</i> You will not feel the truth of it the first twenty mornings. By the fortieth, something begins to give way."),
    ("Notice the cost before you pay it", "Once a week, ask your spouse or a trusted friend: <i>Have I seemed managing to you this week? Have you felt the weight of my care more than the freedom of it?</i> This question, asked genuinely and received without defense, is one of the most powerful tools available to an Architect. The answer will tell you things the Architect's internal monitoring cannot."),
    ("Rest as resistance", "Set down, once a day, every project of relational management — every plan, every contingency, every monitoring of the emotional temperature — for fifteen minutes. Sit in the discomfort of not managing. The Architect will tell you this is irresponsible. It is not. It is the smallest possible rehearsal of the truth that the relationships you love are held by Someone who does not need your oversight to keep them from falling."),
]

PLEA_TOOLS = [
    ("The twenty-four-hour rule", "When the trigger fires and the Plea rises — when you feel the urgent need to apologize, to concede, to close the gap at any price — give it twenty-four hours before you act. Not to be cold. Not to refuse engagement. But to give yourself enough time to ask the question the Plea always bypasses: <i>What am I actually sorry for, and what am I not? What is true, and what am I willing away because the distance is painful?</i> An apology delivered after honest discernment is worth ten apologies delivered in the panic."),
    ("Name the gap without closing it", "Practice saying, to the person you are in conflict with, these words or something like them: <i>I can feel the distance between us right now, and it is uncomfortable for me. I want to work through this together. But I need a little time to understand what I actually need to say.</i> This sentence names the gap without immediately trying to eliminate it. It is honest about what you are feeling without sacrificing the truth to the urgency."),
    ("Ask before you apologize", "Before you apologize, ask one question: <i>Am I apologizing because I was genuinely wrong, or because the gap is painful?</i> If the honest answer is the latter, do not apologize. Name the discomfort instead. The discipline of not apologizing for things you did not do is, for this profile, one of the most countercultural and most liberating practices available."),
    ("The received-love practice", "Each morning, before any relational work begins, read one of the following passages slowly: Romans 8:15–17, Galatians 4:7, 1 John 3:1. Read it as though it is addressed to you specifically, by name. This is not a feeling exercise. It is the daily reorientation of the soul toward a love it already possesses and does not need to earn. The Plea has less to do when the person it is running inside begins, slowly, to believe this."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Architect in me, and you do not despise him. You know why he was built. You know the early rooms in my history where he first learned that vigilance was required and carelessness had a cost. Thank you that he has, in his way, done faithful work for a long time.",
    "But Father, the work has cost more than it was worth, and I am tired of managing what you have already secured. Teach me to receive the love you have given in Christ rather than to engineer the love I am still afraid of losing. Teach me to sit with the gap — to let the distance exist without immediately reaching to close it — long enough to ask what is actually true. Teach me the difference between peacekeeping and peacemaking. Teach me that a connection built on cheap reconciliation is not the connection I was made for.",
    "Lord Jesus, when the Plea rises in me and I find myself apologizing for things I did not do, yielding on things I should have held, paying prices I will silently resent — would you interrupt me? Not with judgment, but with the reminder that you are the one who has already closed the only gap that finally mattered. You pursued me when I was not pursuing you. You paid the price I could never have afforded. I do not need to pay it again. I do not need to panic. The reconciliation has been accomplished.",
    "Holy Spirit, where I am managing, give me rest. Where I am pleading, give me the courage to speak the truth in love and wait. Where I am keeping the peace at the cost of making it, convict me gently — and then show me what genuine peacemaking looks like in this marriage, in this friendship, in this church.",
    "In the name of the One who is our peace — not merely the bringer of peace, but peace itself — I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not a conclusion. The Architect and the Plea have been with you for a long time, and a single reading will not retire them. What follows is a short set of next steps — some immediate, some longer-term — for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different lines will land. The Plea will resist a second reading more than most, because it would rather manage the future than sit with the past. Read it anyway."),
    ("Take one tool, not five.", "Choose a single practice from Section 7 and try it for two weeks before adding another. The Architect will want to implement the whole system at once. That is itself a form of the problem."),
    ("Tell one person what you read.", "Not the whole document. One honest sentence: <i>I learned that when conflict threatens a connection, I panic and apologize for things I did not do, in order to close the gap.</i> Naming it to a witness breaks its power more than anything else in this list."),
    ("Spend a week in the protection psalms.", "Psalm 23, 27, 46, 91, 121. Pray one aloud each morning. Notice which lines you cannot get through without stopping. Those are the places the Architect and the Plea are still doing their most urgent work."),
    ("Read further.", "Tim Keller, <i>The Meaning of Marriage</i> — for the honest theology of covenant love that outlasts emotional temperature. C. S. Lewis, <i>The Four Loves</i> — for the distinction between need-love and gift-love, which speaks directly to the Plea's deepest confusion. Dietrich Bonhoeffer, <i>Life Together</i> — for the difference between cheap and costly reconciliation in Christian community. And Tim Keller, <i>Walking with God through Pain and Suffering</i> — for the larger frame in which all of this sits."),
    ("If you are stuck, ask for help.", "There are seasons when the Plea is too entrenched, the Architect too exhausted, to move alone. A wise pastor, a Christian counselor, a trusted friend who will tell you the truth — these are not signs of failure. They are part of the answer to the prayer you just prayed."),
]

GOING_FURTHER_CLOSING = (
    "You are not a project to be optimized. You are a child being loved into freedom by a Father "
    "whose patience is without limit and whose love requires nothing from you that you have not "
    "already been given in Christ. Go gently. The One who began this work in you will be the one "
    "to finish it. You do not have to manage that either."
)


def _three_column_table(rows=7):
    """Three-column journal table for Section 3 — Plea profile version."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE MOMENT", header_style), Paragraph("when the question woke up", sub_style)],
        [Paragraph("WHAT THE ARCHITECT DID", header_style), Paragraph("how I tried to close the gap", sub_style)],
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
    """Generate the Architect + Plea walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="ARCHITECT  \u00b7  PLEA",
        title="Take 139 Walkthrough \u2014 Architect + Plea",
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
    story.append(Paragraph("The Architect &nbsp;\u00b7&nbsp; The Plea", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disrespect / Disconnection &nbsp;\u00b7&nbsp; Core Question: Am I lovable? Am I protected?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cGod loves us not because we are lovable, but because he is love.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "C. S. Lewis, <i>The Four Loves</i>",
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
                   "Disrespect. Disconnection.",
                   "The moment your body says: the gap has opened.")
    for p in TRIGGER_BODY[:4]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  CONTINUED",
                   "Where the vigilance came from.",
                   "What was lodged in you, and what your body learned.")
    for p in TRIGGER_BODY[4:]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will spin the question; your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=5)
        story.append(Spacer(1, 14))
    story.append(PageBreak())

    # ── SECTION 3: Core Question ──
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I lovable? Am I protected?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "What Scripture actually says.",
                   "A love that precedes your effort and survives your failure.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "The love you are still trying to engineer.",
                   "What the Architect builds in order not to have to ask.")
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

    # ── SECTION 4: Mechanism ──
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Architect.",
                   "What you have built, and what it was built for.")
    for p in ARCH_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "What Tolkien saw.",
                   "The gift of making, bent toward self-reliance.")
    for p in ARCH_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "Retiring him, not firing him.",
                   "The slow recovery of a love you did not build.")
    for p in ARCH_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Architect.",
                   "Read it twice. Then write back.")
    story.append(Paragraph(ARCH_LETTER_BODY, S["BlockQuote"]))
    story.append(Spacer(1, 10))
    for p in ARCH_LETTER_INSTRUCTION:
        story.append(Paragraph(p, S["BodyJ"]))
    journal_lines(story, n=14)
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Plea.",
                   "The place your mechanism breaks, and the pursuit it launches.")
    for p in PLEA_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The Architect\u2019s Plea.",
                   "Panic dressed in preparation. Management in the service of fear.")
    for p in PLEA_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "Peacekeeping and peacemaking.",
                   "The distinction Bonhoeffer saw, and Matthew 5 requires.")
    for p in PLEA_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "The ledger.",
                   "Two questions to sit with before you turn the page.")
    for prompt in PLEA_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=5)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same fear, in two speeds.",
                   "Architect and Plea are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  YOUR SEQUENCE",
                   "Write it in your own words.",
                   "Fill the blanks. Read it aloud when you are done.")
    story.append(Spacer(1, 6))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=8)
    story.append(PageBreak())

    # ── SECTION 7: Tools ──
    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "What to do when you feel the loop start.",
                   "Small enough to carry; useful enough to reach for.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Architect is over-managing.",
                   "Four practices for the time before the alarm fires.")
    for name, desc in ARCH_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Plea is running.",
                   "Four practices for the moment the panic starts.")
    for name, desc in PLEA_TOOLS:
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
