"""Personal Walkthrough — Island + Plea.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disconnection trigger, "Am I enough to be remembered?" core question.
~25 pages, 9 sections.

Calibration note — THE MOST PARADOXICAL PROFILE:
The Island is the person who needs less. The Plea is the breakdown that needs more.
The Island+Plea reader has lived in self-containment for years and then, at the threshold
of feared loss, suddenly cannot stop pursuing. They are confused by their own behavior.
Their spouse is confused. The Island who always said "I don't need much" is now apologizing
nightly for things they did not do, asking again if everything is okay.

Section Five naming: the Plea is not betraying the Island's self-sufficiency — it is
revealing what the self-sufficiency was always covering. The Island never lived as truly
free of needing love; they lived as protected from feeling that need. The Plea is the first
time the unanswered question ("Am I enough to be remembered?") gets honest air.

Key texts: Luke 7 (the woman washing Jesus' feet — a Plea that was also faith);
1 John 4:18 ("perfect love casts out fear").
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
    "Before you read any further, I want to do what a good pastor does at the beginning of a hard conversation. I want to lower the lights and slow the pace. What you are about to look at is not a personality inventory. It is something more specific: a careful account of the way your soul has learned, over a long time, to keep itself from a particular kind of pain — and what happens when that strategy meets something it cannot hold.",
    "There is something I should name at the outset, because it is the thing most likely to make you read this with your arms crossed. You have probably spent a great deal of your life being the person who does not need much. You have processed things alone. You have managed your interior world with a composure that others have sometimes marveled at. You have learned that needing people in the exposed, transparent way that needing requires is something you can avoid — and that life is quieter and safer when you do.",
    "And yet something happened. At the moment you most feared losing something — a relationship, a connection, a person who carries real weight in your world — a different version of you appeared. A version that surprised you. One that pursued, that apologized for things it was not entirely sure it had done, that sent the message, made the call, asked one more time whether everything was still all right. You did not recognize this version. The people who love you may not have recognized it either.",
    "We are going to walk through your trigger — the moment in which your body registers something as wrong. We will listen to the question underneath that moment. We will name the strategy you built in response, and the place that strategy breaks. And then, only then, will we put tools in your hands.",
    "If you were sitting across from me, I would say this plainly. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who has not left you to manage your significance alone; a Son who bore, in Gethsemane, the most complete abandonment in human history so that <i>I am with you always</i> could be spoken without irony; and a Spirit who is at this very moment more present to your interior world than you are to yourself.",
    "So read slowly. Argue with what does not fit. Stay with what does. Pray when something catches in your throat. The goal is a slightly freer life, lived in front of a God who has nothing to gain from your self-sufficiency and everything to give to your honest need. The chapter you are about to read about yourself has been a long time in the writing.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life have no idea it is occurring. It does not look dramatic from the outside. It often looks like nothing at all. You are in the middle of an ordinary evening, or a conversation, or a gathering, and something happens — or fails to happen — and something inside you registers it immediately, with a precision that no one watching would guess you possessed.",
    "Perhaps your spouse's replies grow shorter than usual, and something in you marks the change before you could say how you know it. Perhaps you said something that mattered to you and the conversation moved on without acknowledgment, as though the words had simply dissolved in the air. Perhaps you are in a room full of people who care about you and you feel, without being able to explain it, like you are not quite there — present in body, absent in some way that no one is tracking. Perhaps someone made a plan that involves you without thinking to ask whether it suited you, and the small omission lands as something larger than an omission.",
    "On the surface, none of these look like injuries. They are the ordinary traffic of daily life — the gaps and oversights that accumulate in every relationship. But for you, they do not stay small. The moment registers as something more: a quiet, specific signal that says, <i>you were not necessary to this moment. You could have been somewhere else, and nothing would have changed.</i>",
    "This is your trigger. The word we use for it is <b>disconnection</b>. Not the dramatic disconnection of a visible argument or a declared rupture — but the quiet disconnection of not being factored in. Of being in the room but not in the room. Of being present but not counted. For you, disconnection registers not merely as an interpersonal inconvenience but as a signal with a heavier freight: <i>I did not matter enough here. I am not the kind of person whose absence would be noticed.</i>",
    "C. S. Lewis, in <i>The Weight of Glory</i>, wrote with great care about the longing in every human being to be known and named by something larger than themselves — a desire he traced not to vanity but to the God-given longing for significance, for the sense that one's existence has registered somewhere that counts. He saw that when this desire goes to creatures rather than the Creator, the creatures buckle under the weight. They were never designed to carry it. You have probably spent years trying not to put that weight on anyone. What you have felt, when it fires anyway, is precisely this: the weight of the unanswered question, and no one to bear it.",
    "Here is something worth seeing without looking away. <b>Your sensitivity to disconnection is not vanity, and it is not a character flaw.</b> It is the residue of something real — something that usually happened early, and that taught you a lesson worth examining. There were moments, likely before you had the words for them, in which the people responsible for your sense of mattering were unable, for their own reasons, to give you what you needed. Perhaps you were in a large family where it was easy to be overlooked. Perhaps a parent's emotional presence was limited by their own pain. Perhaps you grew up in a household where what you were inside — the specific texture of your thoughts and feelings — was not given much air. Whatever the form, the lesson lodged: <i>I cannot count on the outside world to remember that I am here. I will have to manage that on my own.</i>",
    "And so you became the Island. You learned to process alone. You learned to need less visibly than other people. You learned to move through the world in a way that did not publicly require acknowledgment — because requiring it was precisely what could not be trusted to produce it. Before we continue, I want you to stop and answer two questions in writing. Not in your head, where the Island will process and file and move on. On the page, where the hand tends to tell the truth the head is managing.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the disconnection signal fired. What happened, in two sentences? You are not looking for a dramatic event. The small, almost-invisible ones are usually the most instructive.",
    "What was the actual size of the event? What was the size of what moved inside you in response? If those two things did not match — if something minor produced a response you did not expect from yourself — you have just located the trigger.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding.",
    "Yours is this: <b>Am I enough to be remembered?</b>",
    "It is not the same as <i>Am I loved?</i>, though it sometimes wears that face. It is the question of a soul that wants to know whether its presence registers — whether it leaves something behind when it leaves the room, whether it occupies a real space in the thoughts of the people whose thoughts matter to it. <i>Am I the kind of person who is carried in someone's mind after the conversation ends?</i>",
    "Most people would prefer to believe they outgrew this question. They have not. They have only become adept at not asking it aloud. For you, the Island has learned to keep this question especially quiet. An Island does not petition. An Island does not say, <i>I need you to think of me.</i> That kind of need would require an exposure the Island finds intolerable. So the question stays inside — circling, gathering evidence, settling into a kind of careful certainty that the answer is probably no.",
    "There is a particular cruelty in this arrangement. The Island's self-containment is designed to protect against the wound of not mattering. But in protecting against the wound, it also prevents the experiences that might answer the question. A soul that has made itself unreadable cannot be carried in someone's thoughts, because there is nothing to carry. The Island's protection and the Island's longing are working against each other at the root, and the Island rarely knows it.",
]

QUESTION_BODY_P2 = [
    "The Psalms return to this longing with a regularity that should unsettle anyone who thinks the desire to matter is too small a thing to bring to God. <i>How long, O Lord? Will you forget me forever? How long will you hide your face from me?</i> (Psalm 13:1) The question is genuine. David does not know the answer when he asks it. What shifts by verse five is not his circumstances. What shifts is the floor he falls back to: the covenantal faithfulness of a God whose memory of him does not depend on how much he has needed or how well he has performed.",
    "The gospel anchor for the question you carry is this: <b>you are an Adopted Son — a Saint — set apart by God as his own possession, fully known, inscribed on the palms of his hands.</b> Isaiah 49:15–16: <i>Can a woman forget her nursing child? Even these may forget, yet I will not forget you. Behold, I have engraved you on the palms of my hands.</i> Engraved — cut in, permanent, requiring deliberate force to remove. God carries you on his hands as a decision already made, which no human forgetting can undo.",
    "Paul, in Romans 8:38–39, works his way through everything that might plausibly threaten this belonging — death, life, angels, principalities, height, depth, anything in all creation — and lands on the impossibility of any of them succeeding. This is a specific claim: the One whose memory of you is perfect cannot be separated from you.",
    "But here is where pastoral honesty is required, and it is harder for the Island than for most. Your nervous system does not want a theological claim. It wants a specific person to demonstrate the answer — to think of you between interactions, to carry you in their thoughts in a way you can feel. Scripture does not promise this. What it promises is larger and, in the moment the trigger fires, considerably more difficult to receive: you are already fully known and permanently held by the One whose memory is without error and whose love has never once depended on your being easy to reach.",
]

QUESTION_BODY_P3 = [
    "Here is the honest rub. Most Islands find it genuinely difficult to receive this answer — not because they doubt it as doctrine, but because receiving it requires an openness that the Island has spent years learning to close. To say <i>I am fully known by God and it is enough</i> is to relinquish the tally. And the Island has been keeping the tally so long that the hand cramps at the thought of setting it down.",
    "The work is not a single act of surrender. It is a practice, returned to daily, of allowing the God who has engraved you on his hands to answer the question the trigger keeps reopening. David modeled this in the Psalms — not once, but continuously. He brought the question, received the answer, and brought the question again the following morning. This is not weak faith. It is exactly the faith the Island most needs permission to practice.",
    "Before we move forward, use the table below. You are simply observing as a witness to your own interior. Use recent events, not ancient ones. The Island has a long memory; keep it to the last few weeks.",
]

ISLE_BODY_P1 = [
    "You have built something. Most people who build what you have built did not set out to do so. It assembled itself over years, one small response at a time, in the presence of circumstances that rewarded self-containment and revealed the cost of needing in the open. Over time you became very good at it, and it became hard to see it as a construction at all. It felt simply like who you are. We are going to call it, throughout this walkthrough, <b>the Island</b>.",
    "The Island's governing strategy is this: <i>if I need very little from the outside world, I cannot be devastated by what the outside world fails to give me.</i> The Island is not cold, not incapable of love. Islands often have deep and genuine relationships. But the Island has learned that the most essential interior material — the things that carry the most weight — is safest when handled alone. You process before you share. You arrive at conclusions before you open them. Over time, you have come to prefer it that way.",
    "There is real wisdom in this. Proverbs commends the person who holds their own counsel: <i>Fear of man will prove to be a snare, but whoever trusts in the Lord is kept safe.</i> (Proverbs 29:25) The ability to process deeply before speaking, to not be buffeted by every wind of opinion, to be genuinely self-possessed — these are gifts the Island carries in abundance.",
    "But the same self-containment that protects you from disappointment also prevents you from being genuinely known. You cannot be carried in someone's thoughts if you have never fully let them carry you. You cannot be remembered in the specific, personal way your soul most wants if you have made yourself, by habit and preference, into someone whose interior is largely inaccessible. The Island's strategy and the Island's longing are working against each other at the root — and the Island has been aware of this, on some level, longer than it would like to admit.",
]

ISLE_BODY_P2 = [
    "The Island usually formed in one of several specific ways. Perhaps emotional expression was simply not welcomed in your household — not punished, but not given air. Feelings were handled privately, the way one handles a headache: quietly, without requiring assistance. Perhaps you learned early that needing people set you up for a particular kind of disappointment, and self-sufficiency began to feel not just safer but more honest about the way things actually work. Perhaps you watched someone near you need too much — always in crisis, always dependent — and you made a quiet decision that you would never become that. Whatever the form, the result was the same: you learned to manage alone.",
    "John Owen, in his pastoral writings on the soul, observed that the desires of the soul do not die simply because they go unnamed. They go underground, where they continue to press and shape behavior without the light of honest examination. The Island's longing — to matter, to be remembered, to leave something behind — has not disappeared. It operates quietly, beneath the composed exterior, in the tally the Island keeps but rarely shows. It surfaces only in the small registrations: the disconnection signal that fires when the Island notes, without fanfare, that it was not thought of here.",
    "The people who love you have felt this without being able to name it. They know there is more interior than they are allowed to reach. They have learned not to push — pushing makes the Island close. And so the longing at the center of you — <i>I want to be known, I want to matter, I want someone to carry me in their thoughts</i> — is being blocked by the same mechanism that is supposed to be protecting you from the pain of not mattering.",
    "<b>The Island is not your enemy.</b> He is a younger version of you who learned, in real circumstances, that managing alone was safer than hoping for company. He deserves your respect, not your contempt. But he is working overtime on a project — keeping you safe from the exposure of needing — that is also keeping you from the thing you most need. The water surrounding the Island has become, over time, a very quiet kind of loneliness. The gospel's call is not to become publicly needier, but to receive the kind of knowing that does not require you to petition or perform: the knowing of a Father who sees you in secret, in the place you have let no one enter, and who has never once looked away.",
]

ISLE_BODY_P3 = [
    "What does it look like to begin loosening the Island's grip? Not demolishing it — the Island was built for a reason, and the reason was real. But beginning, slowly, to lower the drawbridge. Not to everyone. To someone. And before that, to God — who has already crossed the water, who is already present in the interior, who has known everything you have processed alone and has never once turned away.",
    "It begins with naming what the Island is actually protecting — not merely privacy or efficiency, but the wound of not being enough to be held in someone's mind. Until you name that, the Island will insist that self-containment is simply a personality feature, when it is, in fact, a strategy. And strategies built to prevent pain always, eventually, also prevent the alternative.",
    "The letter below is written in the Island's voice. He is not the villain of your story. He is frightened. Read what he has to say.",
]

ISLE_LETTER_INSTRUCTION = [
    "The letter below is written in the Island's voice. He is not villainous; he is honest in a way he has not been for a long time. Read it slowly. Then answer the three prompts that follow.",
    "Dear [Your name],",
    "I built this — the distance, the processing alone, the way I close before you can be reached — because I was trying to solve a specific problem. You needed to matter, and the world you grew up in was not consistently able to tell you that you did. Not cruelly, in most cases. Just inconsistently. And inconsistency, for a soul trying to answer <i>am I enough to be remembered?</i>, is worse than outright rejection. Rejection gives you something to push against. Inconsistency just leaves you checking. So I stopped letting you check.",
    "I gave you solitude that looks like strength. I gave you a self-sufficiency that others have admired. I made it possible for you to move through your days without visibly needing anyone's memory of you — because needing it, and then not receiving it, was the specific thing I could not allow to keep happening.",
    "What I did not anticipate is that the same distance that protected you from being forgotten also protected you from being remembered. You cannot be inscribed in someone's mind if you have never let your full self be seen by them. I thought I was answering the question. I was only sealing it away where it could never be answered.",
    "I am not going away. But I want you to hear what I am afraid of. Underneath all the self-sufficiency, it is very simple: that if I stop protecting you from needing, you will find out that the need is real — and that the need, when it is real, can be answered, or not answered. And not-answered, at that depth, is something I have been trying to spare you from your whole life.",
    "I think there is Someone who wants to answer it differently. I am not sure how to get out of the way. But I am ready to try.",
    "The Island",
]

ISLE_LETTER_PROMPTS = [
    "What part of the Island's letter surprised you? Not the part you expected — the part you were not ready for.",
    "The Island says he built the distance to protect you from a specific wound. Name the wound in your own words. When was the first time the evidence for that wound was gathered?",
    "What would it cost the Island to let one person — just one — closer to the interior? Name the person. Name the cost honestly. Do not soften either.",
]

PLEA_BODY_P1 = [
    "The Plea is a breakdown that does not fit the Island's character. The Island pulls inward; the Plea rushes outward. The Island needs less; the Plea wants more. The Island has spent years at the perimeter of its own need; the Plea suddenly, at the worst possible moment, lets all of it through.",
    "Every mechanism has a place it breaks. Yours is called <b>the Plea</b>. And before we describe it, I want to say something that I would only say to someone in your particular position: <b>the Plea is not a betrayal of the Island's self-sufficiency. It is the first time the Island's most honest question has gotten genuine air.</b> The need was always there. The composure was always a management of it, not an erasure. What the Plea reveals is not something new about you. It is something that has been working quietly underneath the Island's exterior, waiting for the threat to become large enough to break through.",
    "Here is what it looks like. The Island has moved through life with admirable equanimity. It has not required much. And then something happens — not necessarily dramatic, but significant. A relationship that carries real weight shows signs of strain. A person the Island actually needs seems to be moving away. The gap opens. And suddenly, something in the Island that has never run before runs. Toward. Fast.",
    "The Plea pursues. It sends the message before thinking. It apologizes — sometimes for things it did not do, or things it is not certain were wrong, because in the moment the content matters far less than closing the distance. It asks one more time whether everything is all right. It offers concessions on matters it had good reason to hold. It does all of this at a speed that does not feel like itself — because it is the self underneath the Island: the one that has been asking <i>am I enough to be remembered?</i> quietly for years, and is now asking it at volume.",
    "I want to name something here that is easy to miss. Luke 7 gives us a picture that speaks to what is happening inside you. A woman described by the text as a sinner — who knew her shame, who had no social standing — entered a Pharisee's dinner uninvited and washed Jesus' feet with her tears. The text calls it an act of love. It also reads like a Plea. It was uncontrolled, physically excessive. It was the kind of display the Island finds mortifying to imagine. And Jesus did not call it a breakdown. He called it faith. <i>Your faith has saved you; go in peace.</i> (Luke 7:50) The Plea, at its depth, is a cry that has finally broken through the Island's management. What the Plea does with that cry matters greatly. But the cry itself is not the enemy.",
]

PLEA_BODY_P2 = [
    "The specific way the Plea operates in the Island is worth naming carefully, because it differs from how this breakdown runs in other profiles.",
    "When the Plea takes the floor in an Architect, it tends to be organized — the Architect plans the apology before delivering it, manages the repair with his usual intentionality. In an Island, it looks different. The Island's Plea bypasses the Island's careful processing. It does not wait for the interior to reach a conclusion. It runs before the Island is ready — which is, for the Island, profoundly disorienting. The Island always processes before acting. And then, suddenly, in a conflict that threatens a relationship it cannot afford to lose, the Island is acting before it has processed anything. <b>The Plea is what happens when the Island's most protected need finally gets a real target to run toward.</b>",
    "This is why the Island+Plea person is confused by their own behavior. They know, intellectually, that they are apologizing for something they may not have done. They know that this version of themselves is not the one they have maintained for years. But the gap — the sense that the specific person they need might be in the process of deciding they are not worth the effort — bypasses the Island's usual deliberation entirely.",
    "The people on the receiving end are often themselves disoriented. They have known you as someone who does not need much. Someone composed. And now you are asking again if everything is okay. You apologized last night and again this morning. The intensity of the Plea is, beneath its surface, a declaration: <i>I need you more than I have been willing to say. I need you so much that the Island cannot hold it anymore.</i> That is a true thing. It deserves to be said. The question is whether the Plea is saying it in a form that can be received.",
]

PLEA_BODY_P3 = [
    "Here is the pastoral word this profile most needs to hear. <b>The Plea is not the opposite of the Island. It is the Island's question, finally given voice — but in a form that cannot receive the answer it is asking for.</b>",
    "Think about what the Plea actually wants. It wants to hear: <i>yes, you are enough, I am not going anywhere, you matter to me.</i> It wants the answer to the question that has been running underground since the Island was built. But here is the cruelty at the heart of the Plea's design: an apology given under fear of abandonment, a concession made to close a gap rather than because the concession was right — these do not produce the reassurance that answers the question. The word <i>we are okay</i>, said in response to a pursued apology, does not carry the weight the Plea was hoping it would. The Plea can feel, underneath the relief, that the reassurance was earned. And earned reassurance does not answer <i>am I enough to be remembered?</i> It only answers: <i>can I maintain this connection if I keep working for it?</i> Which is a different question — and one the Island has been living inside for years.",
    "John writes with precision about what the Plea is actually after: <i>There is no fear in love, but perfect love casts out fear.</i> (1 John 4:18) The Plea runs on fear. Fear that the gap will become permanent. Fear that the question is about to receive a final, devastating answer in the negative. And fear, John says, does not coexist with perfect love. Not because the fear is sinful, but because the love that the gospel offers is specifically designed to be the answer to it. <i>We love because he first loved us.</i> (1 John 4:19) The movement is from received love to given love — not from feared abandonment to desperate repair. <b>The Island has been earning its significance for a long time. The Plea is simply the Island trying to earn it faster, under more pressure, with a greater sense of emergency.</b> Neither will finally answer the question. The question is answered from outside the Island entirely — by a love that was not earned, is not contingent, and cannot be lost by any human distance.",
]

PLEA_PROMPTS = [
    "Think of the last time the Plea ran — the last time you pursued the reassurance, apologized for something you were not certain you had done, or asked one more time whether everything was still all right. Describe it in two sentences. Try not to edit for how it reflects on you.",
    "The Plea ran because something in the connection felt threatened. What specifically was the threat? Name it as precisely as you can, below the surface of the presenting conflict. What was the Island afraid was actually happening?",
]

TWO_TOG_BODY = [
    "Now we stand back and look at both of them together, because the Island and the Plea are not two separate problems. They are the same longing, housed in the same soul, expressing itself in two opposite directions — one toward safety, one toward connection — and never quite finding what it is looking for in either.",
    "<b>The Island is what your longing does when it has time.</b> It pulls inward, maintains the perimeter, manages the tally from a safe distance. <b>The Plea is what your longing does when the Island's defenses are overwhelmed.</b> When the gap opens and the threat is real enough, the longing breaks through the perimeter and runs outward — toward the person, toward the reassurance — fast, and usually faster than wisdom can keep up with.",
    "The sequence, in slow motion: <b>(1)</b> The Island moves through the world self-contained, needing less than most, keeping the interior question mostly quiet. <b>(2)</b> Something lands that the Island cannot manage — a disconnection, a signal that a specific person may be pulling away. <b>(3)</b> The trigger fires. <b>(4)</b> The core question wakes up: <i>Am I enough to be remembered?</i> <b>(5)</b> The Island's usual response is overwhelmed. The Plea takes the floor. <b>(6)</b> The Plea pursues: apologizes, asks again, offers concessions. <b>(7)</b> The reassurance arrives, or does not. Either way, the question is not answered at the level where it lives. The Island reassembles its perimeter, and the next trigger finds the same circuit intact.",
    "What breaks the loop is not better self-containment, and it is not faster pursuit. It is a different answer to the question — received not as a theological assertion but as a lived reality, practiced daily the way a person returns to water: <i>you are already known, already inscribed, already held in the memory of the One who does not forget, and no human distance changes that fact.</i> When this answer reaches deep enough — past the Island's management, past the Plea's panic — both begin, slowly, to work shorter hours.",
    "Below is your sequence in your own words. Write in the blanks. When you are done, read it aloud. The Island and the Plea both lose a measure of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as disconnection, "
    "as evidence that I am not enough to hold this person's attention, and the old "
    "question wakes up: <i>am I enough to be remembered?</i> My first move is usually "
    "to ____________________, because the Island in me believes that if I can "
    "____________________, the question will stay quiet. When that does not work "
    "— when the gap opens anyway and the threat feels real — the Plea takes over "
    "and I find myself ____________________. What I am actually after, underneath "
    "all of it, is the word ____________________. That word has already been spoken "
    "over me, not by ____________________, but by the One who has engraved me on "
    "____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. Each practice is small enough to carry in a pocket and useful enough to reach for when it matters. None of them will resolve the Island's longing or stop the Plea in a single application. All of them, practiced with patience over months, will loosen the grip of the loop you just named.",
    "I have divided them into two sets. The first is for the Island — for the ordinary days when the self-containment has tipped from healthy solitude into hiding. The second is for the Plea — for the urgent moments when the gap has opened and the panic is already moving. The Island's tools come first, because the Island is the mechanism. You cannot address the Plea usefully until you have a clearer picture of what the Island has been protecting.",
]

ISLE_TOOLS = [
    ("The one honest sentence", "Once a day — not more, because the Island cannot sustain more without feeling overexposed — say one honest sentence to someone present to you. Not information. Not a report. One sentence about something interior: what you are carrying, what you noticed about yourself this week. The Island will call this unnecessary. Do it anyway. Over thirty days, the practice creates a real aperture between your interior world and the people who care about you. Over sixty, the aperture begins to feel less like exposure and more like relief."),
    ("The audit of what you are protecting", "When you find yourself going quiet, closing the interior door, ask one question before the door shuts: <i>am I protecting something healthy, or am I protecting the wound from being touched?</i> You do not need to answer it aloud. But the asking disrupts the Island's automatic reflex. The Island was designed to operate without examination. When it is required to examine itself, it loses some of its efficiency over you."),
    ("The Psalm of disclosure", "When the Island's solitude tips into hiding, open to Psalm 62 or Psalm 139 and pray one passage aloud. <i>Trust in him at all times, O people; pour out your heart before him.</i> (Psalm 62:8) The Psalms model what the Island most needs to practice: a soul that brings its interior to God without first organizing it into something presentable. The movement from hiding to disclosure modeled in the Psalms is faith, not weakness."),
    ("The handed-back tally", "Each evening, name one moment where the question <i>am I being thought of?</i> was active. Do not litigate it. Simply name it. Then say: <i>Lord, I hand this tally back to you. You keep the record that matters.</i> The Island has been keeping the tally on God's behalf for years. This is the practice of returning it to its rightful keeper, one evening at a time."),
    ("The ten-minute opened door", "Once a week, initiate a conversation about something interior with one person you trust — not a problem to be solved, but something you are carrying. The Island will call this unnecessary. It is, from the Island's perspective, the most dangerous item on this list. It is also the most necessary, because the question at the center of the Island's longing cannot receive its truest answer from a soul that has made itself unreadable."),
]

PLEA_TOOLS = [
    ("The gap-naming pause", "When the Plea rises — when you feel the urgency to send the message, to ask again, to apologize before you have assessed whether the apology is warranted — give yourself one hour before you act. Not to refuse engagement, not to perform the Island's withdrawal, but to ask the question the Plea always bypasses: <i>Is this the repair of a genuine wrong, or is it reassurance that the connection is still intact?</i> Those are different requests. They deserve different responses. The pause does not eliminate the Plea. It gives you enough distance to know which one you are about to make."),
    ("Name the fear before you close the gap", "Practice saying to the person you are in conflict with: <i>I can feel the distance between us, and it is harder for me than I usually let on. I am not sure how much of what I am feeling is about this situation and how much is older. But I wanted you to know it is real.</i> This sentence does not pursue or apologize. It names the interior honestly without requiring the other person to immediately resolve it. This is one of the hardest things the Island will ever do. It is also one of the most genuinely connecting."),
    ("Ask before you apologize", "Before you apologize for something you are not certain you did wrong, ask: <i>Is this apology true, or is it a plea dressed in the language of repentance?</i> If the honest answer is the latter, do not apologize. Name the discomfort instead. Every false apology goes into a ledger the Island will quietly maintain. The ledger will eventually require payment with interest."),
    ("The received-love practice", "Each morning, before any relational concern begins, read one of the following slowly: Isaiah 49:15–16, Romans 8:38–39, 1 John 4:18, Ephesians 1:4–5. Read it as addressed to you by name by the only One whose memory of you is perfect. The Island will not feel it the first fifteen mornings. It is the daily reorientation toward a love already possessed, not needing to be pursued — the practice of receiving, before the day begins, what the Plea will spend the day trying to earn."),
    ("The fear question", "When the Plea has already run, resist the instinct to immediately analyze what you did wrong. Ask instead: <i>What was I actually afraid of?</i> Name it specifically. Not <i>I was afraid of the argument</i> but the one underneath: <i>I was afraid I had finally given them reason to stop wanting me.</i> That fear is the Island's question in emergency mode. It deserves to be named honestly, not processed away."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Island in me, and you do not despise it. You know what it was built to protect. You know the specific moments — the ones I have never fully named, even to myself — in which the evidence for its construction was gathered. Thank you that it kept me alive. Thank you that you have been present in the interior even when I gave you no invitation, even in the years I convinced myself I did not need one.",
    "But Father, the Island is tired, and the question it has been guarding is still awake, and I cannot answer it on my own. Teach me that being fully known by you is not a theological assertion to be filed — it is the answer I have been looking for since I was small enough to not yet know the question had a name. When the disconnection fires, when the trigger says <i>you were not enough to be remembered here</i>, would you let me hear your answer before I hear the Island's? <i>I have engraved you on the palms of my hands. I will not forget you.</i> Let that land not only in my mind but somewhere lower — in the place where the Plea lives.",
    "Lord Jesus, when the Plea rises in me — when I find myself pursuing and apologizing and asking one more time whether everything is still all right — would you remind me of the woman in Luke 7? She came in with her tears and her ointment and her hair, and she did not hold any of it back, and you did not call it weakness. You called it faith. Would you receive my Plea the way you received hers? Not as evidence that I am unraveling, but as the first honest thing my Island has said in a very long time. And then would you give me the peace you gave her — not the peace of having closed the gap, but the peace of having been seen and not turned away?",
    "Holy Spirit, where I am hiding, give me the courage to speak. Where I am pursuing in fear, give me the grace to pause and ask what I am actually asking for. Where I am keeping the tally, give me the open hand. Remind me that <i>perfect love casts out fear</i> — not by eliminating the fear through willpower, but by being large enough to hold it without being destroyed by it.",
    "In the name of the One who has engraved me, who holds me, who will not forget — I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not a conclusion. The Island and the Plea have been with you for a long time, and one reading will not retire them. What follows is a short list of next steps — some immediate, some long-term — for the work you have just begun. Do not try to do all of them at once. The Island will want to process the entire list efficiently and file it. Do not let it.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different lines will land. The Island prefers to file things once and move on. Read it again anyway. What could not be received this week may be receivable then."),
    ("Take one tool, not five.", "Choose a single practice from Section 7 and try it honestly for two weeks before adding another. The Island will want to implement the whole list efficiently. That is itself a version of the problem — management instead of formation."),
    ("Tell one person what you found.", "Not the whole document. One honest sentence: <i>I learned that my mechanism is the Island, and when I am threatened with losing someone, I become a Plea I do not recognize.</i> This is not a performance. It is the first lowering of the drawbridge."),
    ("Pray the Psalms of lament aloud.", "Psalm 13, Psalm 62, Psalm 139. Pray one aloud each morning for a week. The Psalms model what the Island most needs to practice: a soul that brings its interior to God without first organizing it, without waiting until the processing is complete. Notice which lines stop you."),
    ("Read further.", "Tim Keller, <i>Counterfeit Gods</i> — for the honest account of how self-sufficiency becomes a counterfeit god. C. S. Lewis, <i>The Weight of Glory</i> — his treatment of the human longing for significance remains among the most theologically honest essays in the English language. Tim Keller, <i>Walking with God through Pain and Suffering</i> — for the larger frame inside which the Island's particular pain finds its true address."),
    ("If you are stuck, ask for help.", "There are seasons when the Island is too entrenched and the Plea too urgent to dislodge alone. A wise pastor, a Christian counselor, a trusted friend who has earned the right to your interior — for the Island, asking for help is not the abandonment of the Island. It is the beginning of its redemption."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be managed. You are a soul being loved into freedom by a Father "
    "who has engraved your name on his hands and who has not, in all the years you have been "
    "keeping the tally, forgotten a single entry. The Island was built in real circumstances, "
    "for real reasons, and it has served you faithfully. But you were not made to live on it alone. "
    "Go gently with yourself. The One who began this work in you will be the one who finishes it. "
    "You do not have to manage that either."
)


def _three_column_table(rows=7):
    """Three-column journal table for Section 3's written reflection — Island+Plea version."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE EVENT", header_style), Paragraph("when the question woke up", sub_style)],
        [Paragraph("WAS I REMEMBERED HERE?", header_style), Paragraph("what the Island concluded", sub_style)],
        [Paragraph("WHAT GOD HAS SAID", header_style), Paragraph("the answer that precedes all others", sub_style)],
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
    """Generate the Island + Plea walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='ISLE', primary_breakdown='PLEA',
    primary_trigger='DISC', core_question='REM'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="ISLAND  \u00b7  PLEA",
        title="Take 139 Walkthrough \u2014 Island + Plea",
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
    story.append(Paragraph("The Island &nbsp;\u00b7&nbsp; The Plea", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disconnection &nbsp;\u00b7&nbsp; Core Question: Am I enough to be remembered?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cThere is no fear in love, but perfect love casts out fear.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "1 John 4:18",
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
                   "The moment your nervous system says: I was not enough to matter here.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will process and refile. Your hand will not.")
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
                   "Engraved on the palms of his hands, and what receiving that costs you.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "The event. What the Island concluded. What God has said.")
    story.append(Paragraph(
        "Use the table below. In the first column, name a recent event. "
        "In the second, write what the Island concluded: "
        "<i>was I remembered here?</i> In the third, write the gospel word "
        "that speaks to what you actually needed: "
        "<i>I have engraved you on the palms of my hands \u2014 I will not forget you.</i>",
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
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "How the Island formed, and what it has cost.",
                   "The longing that went underground, and the beginning of the way back.")
    for p in ISLE_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ISLE_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Island.",
                   "Read what he has to say. Then answer the three questions below.")
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
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Plea.",
                   "The place your mechanism breaks \u2014 and what it has been covering.")
    for p in PLEA_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "Perfect love casts out fear.",
                   "What the Island\u2019s Plea is actually after \u2014 and the only answer that satisfies it.")
    for p in PLEA_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in PLEA_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "The Plea, named plainly.",
                   "Two questions to sit with before you turn the page.")
    for prompt in PLEA_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same longing, in two opposite directions.",
                   "The Island and the Plea are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 10))
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
                   "Five practices for the ordinary days when solitude tips into hiding.")
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
                   "When the Plea is running.",
                   "Five practices for the urgent moments when the gap has opened.")
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


# ── STANDALONE TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "ISLE"
        primary_breakdown = "PLEA"
        primary_trigger = "DISC"
        core_question = "REM"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "island_plea_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages via simple marker
    page_count = pdf_bytes.count(b"/Type /Page\n") + pdf_bytes.count(b"/Type/Page\n")

    # Letter snippet (first line of Section 4 letter)
    snippet = "Dear [Your name], I want you to know something..."

    print(f"DONE: island_plea.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB) — {out_path}")
    print(f"Approximate page count: ~{page_count}")
    print(f"Letter snippet: \"{snippet}\"")
