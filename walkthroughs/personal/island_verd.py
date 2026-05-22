"""Personal Walkthrough — Island + Quiet Exit (Verdict).

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disconnection / Significance trigger, "Am I enough to be remembered?"
Breakdown: Quiet Exit (VERD) — quietly decides "I'm done"; stops investing;
           withdraws into a verdict, often invisible to the other person.

Calibration note: This is one of the most dangerous profiles in the 36.
The Island already lives at distance; the Quiet Exit moves them from
"self-contained" to "permanently absent in place." The pastoral key:
Section Five distinguishes the Island's God-given temperamental preference
for solitude (a gift) from the Verdict's quiet abandonment (a kind of
unbelief — the Island has decided alone that this relationship cannot
hold who they actually are, before any honest test has occurred).
Scripture: Hosea 6:4 and the elder brother in Luke 15.
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
    "Before you read any further, I want to do what a good counselor does in the very first session. I want to lower the lights, slow the pace, and ask you to sit with me in the particular kind of quietness that defines the person you are about to meet in these pages. Because the profile this walkthrough describes is not a loud one. It does not announce itself. It does not storm out of rooms or fill silences with grievance. It simply, very quietly, over a long time, stops being present in the ways that matter most.",
    "This is the saddest of its kind, and I say that not to alarm you but to honor the weight of what we are about to look at together. The Island who carries the Quiet Exit is not a person who has given up obviously. They have given up invisibly — and there is a real pastoral difference between the two, because invisible departures are the ones that are hardest to interrupt, and hardest to grieve, and hardest to name as the crisis they actually are.",
    "We are going to walk through your trigger — the moment your nervous system registers something as wrong. We will listen to the question underneath that moment, the one that has probably been with you since you were very young. We will name the strategy you built in response to that question, and the specific way that strategy collapses when it has been strained long enough. And then, only then, we will put tools in your hands.",
    "If you were sitting across from me, I would say this plainly and mean it: <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who has not, in fact, left you to manage your significance alone in the silence; a Son who endured, in Gethsemane, the most complete abandonment in human history and emerged not into bitterness but into resurrection; and a Spirit who is, at this very moment, more committed to your remaining open than you are.",
    "Read slowly. Argue with what does not fit. Stay with what does. Pray when something catches in your throat, because that catch is usually the Lord saying, <i>look here, with me.</i> C. S. Lewis, in <i>The Four Loves</i>, observed that to love at all is to be vulnerable. What this walkthrough will ask you to consider is whether the Island's conclusion — <i>not worth the risk</i> — was reached honestly, or whether it was reached alone, in a private court, before the evidence was fully in. Take your time. The chapter you are about to read has been a long time in the writing.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it is easy to miss from the outside because it leaves no visible mark. You are in a conversation, or a gathering, or an ordinary evening at home, and someone does something small — or fails to do something small — and something in you registers it immediately and files it away. Not with drama. Not with visible reaction. With the quiet, precise efficiency of a person who has been collecting this particular kind of data for a very long time. Perhaps your partner began describing the weekend to a friend and edited you out of the story, not from malice but from absentmindedness. Perhaps you said something at dinner that mattered to you, and the conversation moved on without pausing. Perhaps you worked carefully on something — a gift, a plan, a gesture — and the person who received it said thank you and moved on, and three days later there was no evidence it had registered at all.",
    "On the surface, not one of these qualifies as an event. They are the ordinary friction of daily life, the small gaps between what we hope for and what we receive, the spaces where intention and attention do not quite meet. But for you, they do not stay small. They register as something more than inconvenience. They register as data — the kind that confirms a conclusion you arrived at a long time ago about your own weight in the lives of the people around you.",
    "This is your trigger. The word we use for it is <b>disconnection</b>, and in its deeper form, <b>significance</b>. The two are related in your particular case. Disconnection does not wound you merely because exclusion is unpleasant. It wounds you because exclusion carries a meaning your soul has been translating for years: <i>you were not necessary to this moment. You were here, and you did not leave a mark that needed accounting for.</i> And whether that translation is accurate — we will come to that — the translation itself is automatic, swift, and very old.",
    "Here is what I want you to see before we go further. The sensitivity you carry — to being overlooked, to being unmemorable, to occupying the periphery of someone's attention when you had hoped to occupy the center — is not vanity. It is not thin skin. It is the residue of real moments, usually early in your life, in which the evidence was gathered and a verdict was quietly reached: <i>the people in my world do not carry me the way I need to be carried.</i> And having reached that verdict, the Island made what seemed like the only reasonable decision: <i>I will stop needing them to.</i>",
    "But that decision — sensible as it was, honest as it was about the way things actually went — was not without cost. The Island became very good at not needing. And the question underneath the trigger — <i>Am I enough to be remembered?</i> — did not go away. It went underground, where it continued pressing and shaping behavior without the light of honest examination. It kept the tally. And now, when the trigger fires, the tally is still there, still running, still building a case that no one can see. Take a breath before we continue, and answer two questions in writing. Your hand will not spin the question the way your head will.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the disconnection or significance signal fired in you. What happened, in two sentences? You are not looking for a dramatic event — the nearly invisible ones are usually the most instructive.",
    "What was the objective size of that event, and what was the size of the response inside you? If they did not match — if a small oversight produced a large interior movement — you have just located the trigger. Write one sentence about what the gap tells you.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm has been standing guard over since you were young enough not to have words for it.",
    "Yours is this: <b>Am I enough to be remembered?</b>",
    "It is not the same as <i>Am I loved?</i>, though it sometimes borrows that face. It is not <i>Am I competent?</i>, though you have built real competence in part as a response to it. It is the question of a soul that wants to know whether its passage through the lives of others registers — whether something of it remains when it leaves the room, whether it is thought of in the ordinary middle of days when nothing is being asked of it, whether its name occurs to people not because they need something but simply because it is there, alive in someone's imagination.",
    "Most adults would prefer to believe they outgrew this question. They have not. They have only relocated it. The childhood version was blunt: <i>does anyone think about me when I am not there?</i> The adult version has more sophistication — <i>Does this work matter? Does this relationship account for me?</i> — but it is the same question, asking in the same dark, waiting to see if anyone answers. For you, this question is particularly alive because the Island has made it almost impossible to ask out loud. An Island does not petition. That kind of need would require an exposure the Island finds nearly intolerable — and so the question stays inside, forming and reforming, gaining evidence, losing none.",
]

QUESTION_BODY_P2 = [
    "There is a reason that the theologians from Augustine to Jonathan Edwards insisted that the deepest human longings, when followed honestly, do not finally terminate in a human answer. Augustine's famous confession — <i>our heart is restless until it rests in Thee</i> — was not poetry first. It was a map. And the longing to be remembered, to be inscribed, to be known in a way that nothing can erase, is a longing shaped specifically for God.",
    "The Scriptures are not embarrassed by this longing. Isaiah 49:15-16: <i>Can a woman forget her nursing child, that she should have no compassion on the son of her womb? Even these may forget, yet I will not forget you. Behold, I have engraved you on the palms of my hands.</i> The image is striking in its physicality. Not a note kept somewhere. Not a record filed for retrieval. Engraved — cut in, permanent, requiring deliberate and painful effort to remove. The God of Scripture does not carry you in a database. He carries you on his hands as a decision he has made and will not unmake.",
    "Paul, in Romans 8:38-39, works through everything that might conceivably separate a person from the love of God — death, life, angels, principalities, things present, things to come, height, depth, anything in all creation — and lands on the impossibility of any of them succeeding. This is not a general promise about the universe being benevolent. It is a specific promise about a Person who knows your name: <i>nothing shall be able to separate us from the love of God in Christ Jesus our Lord.</i>",
    "But here is where pastoral honesty must be maintained, and it is harder for you than for most. Your nervous system wants a particular person to demonstrate the answer — to remember consistently, to factor you in, to carry you in their thoughts without being asked. Scripture refuses to promise this. What it promises is larger and, in the moment the trigger fires, considerably more difficult to receive: you are already fully known and held permanently by the One whose memory is perfect and whose love does not depend on your being easy to remember.",
]

QUESTION_BODY_P3 = [
    "The gospel anchor for the question you carry is this: you are an <i>Adopted Son</i>, a <i>Saint</i> — set apart by God as his own possession, fully known, fully named, inscribed on the palms of his hands. Ephesians 1:4-5: God <i>chose us in him before the foundation of the world, that we should be holy and blameless before him. In love he predestined us for adoption as sons through Jesus Christ.</i> You were thought of before the world began. The question <i>Am I enough to be remembered?</i> was answered at the foundation of the cosmos, and the answer was not a conditional one.",
    "Here is the honest rub. Most Islands do not find it easy to receive this answer — not because they doubt it doctrinally but because receiving it requires a kind of openness that the Island has spent years resisting. To receive is a form of need. To say <i>I am fully known and it is enough</i> is to relinquish the tally, and the Island has been keeping the tally so long that the hand cramps at the thought of setting it down. David did this work not once but continuously. <i>How long, O Lord? Will you forget me forever?</i> (Psalm 13:1) He does not pretend the question is permanently settled. He brings it back. This is not weak faith. It is honest faith — exactly the faith the Island needs permission to practice.",
    "Before we close this section, use the table below. You are not analyzing yourself; you are observing. Use recent events, not ancient ones.",
]

ISLE_BODY_P1 = [
    "You have built something. You did not build it in a morning, and you probably did not build it consciously. Over years — and usually over a small handful of specific moments in which the world showed you, clearly and memorably, what it did and did not keep — you constructed a way of being in the world that we are going to call, throughout this walkthrough, <b>the Island</b>.",
    "The Island's strategy is this: <i>if I need very little from the outside world, the outside world cannot disappoint me with what it fails to give.</i> The Island is not antisocial, and is not incapable of genuine warmth. Islands often have real relationships, deep loyalties, people they love with a quiet consistency that does not announce itself. But the Island has learned — at some cost, and with real reason — that the most essential interior material is better handled alone. You process before you share. You reach conclusions before you open them for discussion. You have come to prefer the interior to the shared.",
    "There is much in Scripture that commends a certain self-possession. Proverbs 29:25: <i>Fear of man will prove to be a snare, but whoever trusts in the Lord is kept safe.</i> The ability to hold your own counsel, to process deeply before speaking — these are genuine gifts, and the Island has them in abundance. But the same self-containment that protects you from disappointment also prevents you from being genuinely known. And the question underneath your trigger — <i>Am I enough to be remembered?</i> — cannot be answered by a soul that has made itself systematically unreadable to the people whose memory it most wants. The moat that keeps people from disappointing you is the same moat that keeps them from knowing you.",
]

ISLE_BODY_P2 = [
    "The Island usually formed in one of several recognizable ways. Perhaps emotional expression was not welcomed in your household growing up — not punished, but simply not valued. Feelings were something you managed privately, the way you manage a headache: with minimal fuss, without drawing attention, until they passed. Perhaps you learned early that needing people set you up for disappointment, and self-sufficiency began to feel not merely safer but more honest. Perhaps you watched someone close to you need too much from other people — always in crisis, always dependent — and made a quiet, early decision that you would never become that.",
    "John Owen observed that the soul's desires do not die when they go unnamed. They go underground, where they continue to press and shape behavior without the light of honest examination. The Island's longing to matter — to be remembered, to be carried in someone's thoughts, to leave a mark — has gone underground. It has not gone away. It operates quietly, beneath the composed exterior, in the tally the Island keeps but never shows anyone. The people who love you have probably felt this without being able to name it. They know there is more inside than they are allowed to reach. They have learned, over time, not to push. This is not their failure. It is the Island's design working exactly as intended.",
    "<b>The Island is not your enemy.</b> He is a younger version of you who learned, in some specific and real circumstance, that managing alone was less painful than hoping for company that might not come. He deserves your respect, not your contempt. But he is working overtime on a project — keeping you safe from need — that has also become the primary obstacle to the thing you most need. The water around the Island is not only protection. It has become, over years, a kind of exile. The gospel's word to the Island is not <i>become a needier person</i> in the therapeutic sense, but: <i>receive the knowing of a Father who sees you in the interior, in the place you have kept from everyone else.</i>",
]

ISLE_BODY_P3 = [
    "What does it look like to begin loosening the Island's grip? Not demolishing it — it was built for real reasons, in real circumstances. But beginning, slowly, to lower the drawbridge. Not to everyone. To one person. And before that, to God — who has already crossed the water, who is already inside, who has seen everything you have processed alone and has never once turned away from it.",
    "It begins with naming what the Island is actually protecting. Not what it says it is protecting — not privacy, not efficiency, not simply a preference for solitude. What it is actually protecting: the wound of not being enough to be held in someone's memory, and the terror of testing that question and receiving the wrong answer. Until you name that, the Island will continue to insist that its distance is a temperamental preference, when it is in fact a strategy that predates any honest test.",
    "There is an exercise below that I want you to take seriously. A letter, written in the Island's own voice, addressed to you. Read it slowly. Then answer the three questions that follow. You are not being asked to dismantle him in an afternoon. You are being asked to give him, perhaps for the first time, an honest conversation.",
]

ISLE_LETTER_INSTRUCTION = [
    "The letter below is written in the Island's voice. He is not villainous. He is frightened, and faithful, and very tired. Read it slowly. Then answer the three prompts that follow.",
    "Dear [Your name],",
    "I have been keeping you safe. Not safe in the abstract but from a very specific danger: the danger of needing to be remembered by someone, and discovering that you were not. I have watched that happen enough times that I decided, at a point early enough that I no longer have full access to the memory, that the only honest response was to stop needing it. So I built the Island. I gave you solitude that looks like strength. I gave you the ability to process everything that matters on your own, so you would never be caught having needed someone who was not there.",
    "What I did not anticipate — what I genuinely did not know how to account for, when I was small enough to still be making these decisions — is that the same distance that keeps you from being forgotten also keeps you from being remembered. You cannot be carried in someone's thoughts if you have never let them carry you. I thought I was solving the problem. I was only relocating it to a place where it could not be touched.",
    "There is something else I should tell you. Over the years, when the wound has been touched despite my best efforts, I have done something I have not always named honestly. I have quietly begun to leave. Not all at once. Not loudly. I have simply reduced my investment, pulled back my hope, moved my care slightly further from the surface where it could be reached. I have called this protecting you. I think some of it has been. I think some of it has been something else. I am telling you this because the next step requires you to know that I know it too.",
    "The Island",
]

ISLE_LETTER_PROMPTS = [
    "What part of the Island's letter surprised you most — not the part you expected, but the part you were not quite ready to read?",
    "The Island says he built the distance to protect you from a specific wound: needing to be remembered and discovering you were not. Name that wound in your own words. When was the first time the evidence for it was gathered?",
    "The Island admits that over time, when the wound has been touched, he has quietly begun to leave — pulling back investment and hope without announcement. Can you name a specific relationship or situation where that has happened? What was the original wound that started the departure?",
]

VERD_BODY_P1 = [
    "Every mechanism has a place it breaks. The Island's breakdown is called <b>the Quiet Exit</b>, and it is the most dangerous profile in this taxonomy. I say that not to frighten you but to name the stakes clearly, because the Quiet Exit is the one breakdown most likely to be mistaken — by the person experiencing it, and by everyone around them — for something else entirely. It looks like peace. It looks like maturity. It looks like a person who has wisely stopped expecting more from a relationship than the relationship is capable of giving. It is none of those things, though it is dressed in all of their clothes.",
    "Here is what it looks like in the Island. The disconnection trigger fires — not once, not dramatically, but in the accumulation of small moments the Island has been noting for months or years. The tally reaches a number the Island has never announced. And then, very quietly, without a scene, without any of the visible signals that might allow someone on the other side to respond — something shifts. The Island stops investing. Not aggressively. Gradually. The texts become slightly shorter. The initiations become slightly less frequent. The hope that was once, even quietly, present — begins to be absent. What makes this so difficult to name is that the Island has been practicing a version of it all along. The Quiet Exit is not a new behavior. It is the same behavior at a different temperature. And because the temperature change is so gradual, neither the Island nor the people who love the Island often notice that something irreversible is beginning to happen.",
    "Hosea 6:4 names this with a directness that still carries its sting: <i>Your love is like a morning mist, like the early dew that disappears.</i> God is not describing a dramatic betrayal. He is describing a love that was real and has evaporated — quietly, without announcement, the way morning mist disappears not in a moment but in a slow dissolving you cannot pin to a particular instant. By the time you notice the dew is gone, it has been gone for some time. That is the Quiet Exit. That is what it feels like from the inside of the relationship being exited.",
]

VERD_BODY_P2 = [
    "Now I want to make a distinction that this walkthrough must make carefully, because if it is not made, I will be heard as saying something I am not saying.",
    "The Island, more than almost any other mechanism, has a God-given and legitimate preference for solitude. This is not a wound. This is a wiring — the way some souls are built, the way some people genuinely encounter God, genuinely recover, genuinely think best: in quiet, in interior space, with less external noise rather than more. Jonathan Edwards wrote his greatest theology in long, solitary walks. The contemplative tradition of the church — from Bernard of Clairvaux through the Desert Fathers — recognized that some souls are given a particular capacity for interiority, and that this capacity, rightly ordered, is a gift to the body of Christ rather than a pathology in need of correction.",
    "The Quiet Exit is not that. The Quiet Exit is not the Island retreating to solitude to encounter God and return. The Quiet Exit is the Island retreating to solitude to render a verdict — privately, without the other person's knowledge, without giving the relationship the chance to respond or repair. <b>The pastoral distinction is this:</b> solitude that brings you back is a gift. Solitude that replaces the relationship is a departure. The question is not whether you need time alone. The question is whether the alone-time is a refueling stop, or whether it has become the destination.",
    "And here is what makes the Island's Quiet Exit theologically serious in a way that must be named plainly: it is a kind of unbelief. Not the overt unbelief of the atheist. The subtle unbelief of a person who has decided, in their own private court, on their own evidence, that this relationship cannot hold who they actually are — before any honest test of that question has occurred. The Island has never said, out loud, in the hearing of the other person: <i>I need to know if this relationship can hold me. I need to show you what is inside, and find out if it is safe here.</i> The Island has not done that. And yet it has rendered a verdict on the basis of what it imagines the answer would be. That verdict — rendered in secret, without evidence, before the question was honestly asked — is, in its structure, the opposite of hope. And hope, Paul tells us in 1 Corinthians 13:7, is not optional for love. <i>Love hopes all things.</i>",
]

VERD_BODY_P3 = [
    "Jesus told a story about two sons. One of them took his inheritance and left visibly, loudly, scandalously. That son is easy to see. The other son stayed home, kept his obligations, maintained the appearance. And when his father ran to meet the returning brother, the elder son stood outside and refused to go in. He had been present all along, and he had already left in the only sense that matters. The Quiet Exit is the elder brother's departure — conducted invisibly, from inside the household, while everyone else assumed nothing had changed. It preemptively closes the account. It decides — on evidence that feels conclusive, in a private court where the defendant has no representation — that hope is no longer warranted. And then it continues to show up, physically, verbally, functionally, while the interior has quietly vacated. This is not peace. It is the most orderly kind of despair.",
    "D. Martyn Lloyd-Jones observed that the most dangerous spiritual condition is the one that has substituted a self-secured equilibrium for genuine communion with God. It feels like peace. It presents as composure. It has none of the visible distress that might cause someone to intervene. The pastoral work of this section is to test the peace — to ask, gently but directly: <i>Am I at peace because God has given it to me, or am I at peace because I have stopped hoping?</i> The difference between those two things is everything.",
]

VERD_PROMPTS = [
    "Name the relationship or situation where you most recognize the Quiet Exit. You do not have to have announced it — you may barely have admitted it to yourself. When did the investment begin to reduce? Was it a single moment, or was it a slow accumulation that you noticed only in retrospect?",
    "Ask yourself the honest question: <i>In this specific situation, am I drawing a God-given limit to protect myself from genuine harm — or am I pronouncing a verdict that belongs to God, before the question was honestly put to the relationship?</i> Write the most honest answer you can. Do not edit it for pastoral acceptability.",
]

TWO_TOG_BODY = [
    "Now we place them next to each other, because the Island and the Quiet Exit are not two separate problems. They are the same longing, managed by the same strategy. <b>The Island is what your longing does when it has enough hope to maintain the perimeter.</b> The Quiet Exit is what your longing does when the perimeter has been breached too many times and the Island has decided, quietly, that re-investment is no longer worth the cost.",
    "The pattern, in slow motion, looks like this. <b>(1)</b> The Island moves through the world self-sufficiently, keeping the tally privately. <b>(2)</b> Something lands that crosses the perimeter anyway — a disconnection, a forgetting, a failure of significance. <b>(3)</b> The trigger fires: <i>I was not enough to be remembered here.</i> <b>(4)</b> The core question surfaces: <i>Am I enough to be remembered?</i> <b>(5)</b> The Island retreats further, processes alone. <b>(6)</b> This happens again. And at some point — not in a single dramatic moment but in a quiet interior shift — the Island stops directing its care toward the relationship and begins managing the withdrawal. <b>(7)</b> The Quiet Exit has begun. Because it looks like the Island's normal composure, no one notices. <b>(8)</b> The verdict is rendered privately, in a court where no one else had standing. The story that God had not yet finished is quietly closed.",
    "What breaks this pattern is a different answer to the question. Until the Island receives — not merely affirms doctrinally, but genuinely receives into the interior it has been protecting — that it is already known, already inscribed, already carried by the One who does not forget, the loop has nothing to run against. With that answer received and practiced over time, the Island begins to find the perimeter less necessary. The Quiet Exit begins to reverse. Below is your sequence. Fill in the blanks, then read it aloud. The Island and the Quiet Exit lose some of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When ____________________, something in me reads it as disconnection — as not being "
    "enough to matter to this person — and the old question surfaces: <i>am I enough to be "
    "remembered?</i> My first move is to ____________________, because the Island in me "
    "believes that if I can ____________________, I will not need to expose the wound. When "
    "that does not work — when the wound stays open and the trigger fires again — I begin, "
    "quietly, to ____________________. The Exit feels like ____________________, but what "
    "it actually is, underneath, is ____________________. What I most need in that moment "
    "is not a better strategy but the truth that ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small collection of practices — each one simple enough to carry in a pocket, each one honest enough to be worth reaching for. None of them will resolve the Island's longing in a single application. All of them, practiced over months, will loosen the grip of the loop you have just named.",
    "I have divided them into two sets: tools for when the Island is overworking its defenses — when the solitude has tipped from gift into hiding — and tools for when the Quiet Exit has begun or is beginning, and you need to interrupt the departure before it becomes the kind of permanent that cannot be undone. The Island's tools come first, because the Island is the mechanism, and the Quiet Exit cannot be addressed usefully until the mechanism's habit patterns are understood.",
]

ISLE_TOOLS = [
    ("The one honest sentence", "Once a day — not more, because the Island cannot sustain more without feeling exposed — say one honest sentence to someone who is present to you. One sentence about something interior: what you are carrying, what is difficult, what you are glad about that you would not normally name aloud. The Island will classify this as unnecessary. Do it anyway. Over a month, the practice begins to widen the aperture between your interior world and the people who are trying to love you."),
    ("The audit of what you are protecting", "When you find yourself going quiet — processing alone, closing the interior door — ask one question before the door shuts: <i>Am I protecting a legitimate need for solitude, or am I protecting the wound from being touched?</i> You do not need to answer it out loud. But the asking disrupts the Island's automatic reflex. The Island loses some of its efficiency when it is required to explain itself, even privately."),
    ("The handed-back tally", "Each evening, name one moment where the significance tally was active — one moment where the question <i>am I being remembered?</i> was running quietly. Do not litigate it; simply notice it. Then say: <i>Lord, I hand this tally back to you. You keep the record that matters.</i> The Island has been keeping the tally on God's behalf for years. This is the practice of returning it."),
    ("The Psalm of disclosure", "When the Island's solitude tips toward hiding, open to Psalm 62 or Psalm 139 and pray one section aloud. Psalm 62: <i>Trust in him at all times, O people; pour out your heart before him; God is a refuge for us.</i> Psalm 139: <i>You have searched me and known me.</i> The Psalms model a disclosure to God that is too honest to be performance. The Island can pray Psalms without feeling exposed, which is exactly why they are the right discipline for this particular wound."),
    ("The ten-minute unlocked door", "Once a week, initiate a conversation with someone you trust about something interior — not a problem to solve, but something you are genuinely carrying. The Island will call this unnecessary. It is, from the Island's perspective, the most dangerous item on this list. It is also the most necessary, because the longing at the center of you cannot be answered by a soul that has made itself consistently unreadable."),
]

VERD_TOOLS = [
    ("The exit inventory", "When you notice the Quiet Exit beginning — when you catch yourself caring less, hoping less, initiating less — write down the name of the relationship or situation. Then write two sentences: (1) <i>The evidence I have been gathering.</i> (2) <i>The verdict I have quietly rendered.</i> Seeing the verdict written down is often the first time the Island recognizes it as a verdict rather than a settled conclusion. Verdicts require authority. Has God given you the authority to render this one?"),
    ("The hope question", "Ask yourself honestly: <i>When did I stop hoping in this specific situation? Was that a moment I received — a settled sense from God that this season was over — or was it a moment I chose, because hoping had become too costly?</i> Write the answer. The difference between those two origins is the difference between a God-given limit and the Quiet Exit. Name which one this is."),
    ("Tell one person the door is closing", "The Quiet Exit lives on secrecy. It is a private verdict rendered privately, and it becomes permanent because no one ever spoke into it before it sealed. Before the door closes, tell one trusted person — a pastor, a counselor, a friend who has earned the right to your interior — that you have been pulling back. Not to fix it in that conversation. Simply to break the secrecy. The Exit loses most of its power the moment it is no longer entirely interior."),
    ("The elder brother question", "Sit with Luke 15:28-30. The elder son was at home and had already left. Ask quietly: <i>Am I at home in this relationship, and already gone in the only sense that matters?</i> The father's response to the elder son was not condemnation. It was an invitation to come in. The Exit's power is partly that it presents itself as composure. What is the Father inviting you toward?"),
    ("The confession that fits", "When you recognize the Quiet Exit in yourself, the pastoral response is not self-criticism. It is confession — specific, honest, brief: <i>I have rendered a verdict that was not mine to render. I have allowed hope to leave this situation without asking you whether you were finished with it. I hand this back to you, Lord. I am willing to wait long enough to find out what you intend.</i> Then wait. The Island is not accustomed to waiting. This is the practice."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Island in me, and you do not despise it. You know what it was built to protect, and you know the specific moments — most of which I have never fully named, even to myself — in which the evidence for its construction was gathered. Thank you that it kept me alive. Thank you that you have been present in the interior even when I gave you no invitation and kept the door closed against everyone, including you.",
    "Father, the Island is tired, and the tally is heavier than I let on, and I have been keeping a record that was never mine to keep. Teach me to hand it back. Teach me that being fully known by you — not in the vague sense of the doctrine, but in the specific, particular sense of the moments I have never shown anyone — is the only answer that actually quiets the question underneath my trigger. When the disconnection fires, when the small moment registers that I was not remembered here, would you let me hear your answer before I hear the Island's? <i>I have engraved you on the palms of my hands. I will not forget you.</i> Let that truth land somewhere deeper than my theology.",
    "Lord Jesus, I confess that I have, in at least one relationship I could name right now, already begun to leave. Not with my body, and perhaps not yet with my words, but in the interior — in the place where the Island makes its decisions — the door has been closing. Quietly, without announcement, without giving the relationship the chance to respond. I have been more committed to protecting myself from further disappointment than to hoping in what you might yet do with a story I declared finished on my own evidence. Forgive me for pronouncing the verdict before you had given it. I hand the case back to you.",
    "Holy Spirit, where I am hiding, give me the courage to speak. Where I am exiting, give me the courage to stay. Where I have closed the account, give me the grace to leave the ledger on your desk and wait. And where the Quiet Exit has already gone further than I have admitted even to myself — would you be the one who stands at the door before it seals, and calls me back in.",
    "In the name of the One who, in the garden, stayed when every human instinct said flee — and who, from the cross, kept the door open for a thief who had done nothing to deserve it — I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not a conclusion. The Island and the Quiet Exit have been with you long enough to have deep roots, and one careful reading will not pull them up entirely. What follows is a short set of next steps — honest, concrete, unhurried — for the work that has just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different lines will land. The Island will prefer to file this once and consider the matter handled; that preference is itself part of the pattern. Come back in a month. What you could not quite receive this week may be receivable then."),
    ("Take one tool, not five.", "Choose the single practice from Section 7 that is most directly relevant to where you are right now — not the most comfortable one, the most necessary one. Try it for two weeks before you add another. One posture, held long enough, begins to change the shape of the body."),
    ("Tell one person what you found.", "Not the whole document. One sentence: <i>I learned that my mechanism is the Island, and my breakdown is the Quiet Exit.</i> Tell it to someone who has the right to your interior. Notice what happens when the Island's private conclusions are spoken to a safe witness. This is the first lowering of the drawbridge."),
    ("Read further on the longing underneath the wound.", "Tim Keller, <i>Counterfeit Gods: The Empty Promises of Money, Sex, and Power, and the Only Hope That Matters</i>. The Island tends to make self-sufficiency a counterfeit god — a way of answering the deepest questions without exposing them to another. Also: C. S. Lewis, <i>The Weight of Glory</i> — read the title essay slowly. His treatment of the human longing for significance and the only source that can finally bear its weight is the most honest thing in English on the subject."),
    ("Read the Psalms of lament aloud.", "Psalm 13, Psalm 22, Psalm 62, Psalm 139. Pray one aloud each morning for a week. The Psalms model what the Island most needs to practice: a soul that brings its interior to God without editing, without waiting until the processing is complete. Notice which lines stop you. Those are the lines for you."),
    ("If the door has already closed, ask for help.", "There are seasons when the Quiet Exit has gone too far to be interrupted alone. A wise pastor, a Christian counselor, a trusted elder who knows you well — these are not signs of failure. They are, for the Island in particular, the most courageous thing on this list. The Island was built to manage alone. Learning to receive help is not its abandonment. It is the beginning of its redemption."),
]

GOING_FURTHER_CLOSING = (
    "You are not a person who stopped hoping because you were weak. "
    "You are a person who carried the wound of not being remembered for a very long time, "
    "in a very private place, without letting anyone help you carry it. "
    "God does not despise that. He meets you there, in the interior, where you thought no one could reach. "
    "The One who began the good work in you will be the one to finish it, "
    "and he has not yet issued the final statement on the story you are in the middle of."
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
        [Paragraph("WAS I REMEMBERED HERE?", header_style), Paragraph("what your nervous system concluded", sub_style)],
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
    """Generate the Island+Quiet Exit (Verdict) walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='ISLE', primary_breakdown='VERD',
    primary_trigger='DISC', core_question='REM'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="ISLAND  \u00b7  QUIET EXIT",
        title="Take 139 Walkthrough \u2014 Island + Quiet Exit",
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
    story.append(Paragraph("The Island &nbsp;\u00b7&nbsp; The Quiet Exit", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disconnection &nbsp;\u00b7&nbsp; Core Question: Am I enough to be remembered?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cYour love is like a morning mist,<br/>"
        "like the early dew that disappears.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Hosea 6:4",
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
                   "The moment your nervous system says: I was not enough to be remembered here.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will process and refile; your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 3: Core Question ──
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I enough to be remembered?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "What Scripture says \u2014 and the honest rub.",
                   "Engraved on the palms of his hands, and what receiving that answer costs.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "Where was I actually forgotten? Where was my soul in danger?")
    story.append(Paragraph(
        "Use the table below. In the first column, name a recent event. "
        "In the second, write what your nervous system concluded: "
        "<i>was I remembered here?</i> In the third, answer the deeper question: "
        "<i>was the part of me that finally matters \u2014 my soul, my standing before "
        "God \u2014 at any point in danger?</i>",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table())
    story.append(PageBreak())

    # ── SECTION 4: Mechanism ──
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Island.",
                   "What you have built, and what the building has cost you.")
    for p in ISLE_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>How the Island formed.</b>", S["H3"]))
    for p in ISLE_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ISLE_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Island.",
                   "Read the Island\u2019s own words. Then answer the three questions below.")

    letter_style = ParagraphStyle(
        "IslandLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for line in ISLE_LETTER_INSTRUCTION:
        story.append(Paragraph(line, letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in ISLE_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Quiet Exit.",
                   "The departure that looks like peace. The verdict rendered in private.")
    for p in VERD_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>Solitude as gift; the Quiet Exit as departure.</b>", S["H3"]))
    for p in VERD_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>The elder brother\u2019s departure.</b>", S["H3"]))
    for p in VERD_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions before you turn the page.",
                   "Write the honest answer, not the pastoral-sounding one.")
    for prompt in VERD_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same longing, in two forms.",
                   "Island and Quiet Exit are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  YOUR SEQUENCE",
                   "Write it in your own words.",
                   "Fill the blanks below, then read the sequence aloud.")
    story.append(Spacer(1, 6))
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
                   "When the Island is overworking its defenses.",
                   "Five practices for before the alarm fires; six for when the Exit has begun.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    for name, desc in ISLE_TOOLS:
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
        primary_mechanism = "ISLE"
        primary_breakdown = "VERD"
        primary_trigger = "DISC"
        core_question = "REM"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "island_verd_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages using /Type /Page[^s] pattern (works with compressed PDFs)
    import re
    page_count = len(re.findall(b"/Type /Page[^s]", pdf_bytes))

    # Grab a snippet from the letter constant (not PDF bytes, which are compressed)
    import html
    raw_letter = ISLE_LETTER_INSTRUCTION[2]  # "I have been keeping you safe..."
    clean_letter = re.sub(r"<[^>]+>", "", raw_letter)
    snippet = clean_letter[:120]

    print(f"DONE: island_verd.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB) — {out_path}")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet}")
