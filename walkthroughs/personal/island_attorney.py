"""Personal Walkthrough — Island + Attorney.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disconnection/Significance trigger, "Am I enough to be remembered?" core question.
~25 pages, 9 sections.

Calibration anchor: same Attorney breakdown as ARCH+ATTY, but carried by the Island
mechanism — self-contained, processes alone, builds the case silently and privately,
delivers a single devastating closing statement, then retreats.
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
    "Before you read any further, I want to do for you what a good counselor does in the first session — lower the lights and slow the pace — because what you are about to look at is not a list of tendencies or traits. It is a way of seeing how your soul has learned to manage a particular kind of ache, and how that management has become, over the years, a kind of island.",
    "You are, in a real sense, an Island. Not because you are cold or incapable of love — you are almost certainly neither — but because something early in your life taught you that the distance between your interior world and the world outside was not a gap to be closed but a perimeter to be maintained. You learned to process alone. You learned that your deepest thoughts were most reliable when they stayed inside, where they could not be mishandled. You learned that needing people, in the transparent and exposed way that needing requires, set you up for a kind of disappointment that was simply not worth the cost.",
    "We are going to walk through your trigger — the specific moment your nervous system says <i>something is wrong here.</i> We will listen to the question underneath that moment, the one that has probably been with you since childhood. We will name the strategy you have built in response, and the place that strategy breaks under pressure. And then, only then, will we put tools in your hands.",
    "If you were sitting across from me, I would say this plainly. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who has not left you to manage your significance alone; a Son who endured, in Gethsemane, the most complete abandonment in human history so that the words <i>I am with you always</i> could be spoken without irony; and a Spirit who is, at this very moment, more present to you than you are to yourself.",
    "So read slowly. Argue with what does not fit. Stay with what does. Pray when something catches in your throat, because that catch is usually the Lord saying, <i>look here, with me.</i> The goal is a slightly freer life, lived in the company of a God who has never once forgotten your name. Take your time. The chapter you are about to read about yourself has been a long time in the writing.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life have no idea it is occurring. It does not look dramatic from the outside. Sometimes it looks like nothing at all. You are in the middle of a conversation, or a gathering, or an ordinary evening, and someone says something — or fails to say something — and something inside you registers it immediately, like a stone dropped into still water.",
    "Perhaps your spouse started a story from the weekend without including you in the telling, as though you had not been there. Perhaps a friend mentioned a plan that everyone else seemed to know about, and you learned of it only by accident, in passing, the way you learn about things that don't require your involvement. Perhaps you said something at a table — something that mattered to you — and the conversation moved on without acknowledgment, as if the words had simply dissolved in the air. Perhaps you worked for weeks on something, and the person who received it said thank you and put it down and never picked it up again.",
    "On the surface, none of these look like injuries. They are the ordinary traffic of daily life, the small gaps and oversights that accumulate in every relationship. But for you, they do not stay small. The moment registers as something more than inconvenience. It registers as a signal — quiet, specific, and unmistakable — that says: <i>you were not necessary to this moment. You were not thought of. You were here, and you did not leave a mark.</i>",
    "This is your trigger. The word we use for it is <b>disconnection</b> — and in its deepest form, <b>significance</b>. The two belong together in your case. Disconnection wounds you not merely because you feel excluded but because exclusion means something to you: it means you did not matter enough to be included. And mattering — being the kind of person whose absence is noticed, whose words are carried forward, whose presence changes the shape of a room — is something your soul has been keeping a very careful tally about for a long time.",
    "C. S. Lewis, in <i>The Weight of Glory</i>, wrote with great care about the longing in every human being to be known and noticed by the universe — to have our names spoken by the highest authority. He called it a desire for glory, and he refused to be embarrassed by it, because he recognized it as a desire God himself had placed there. What he also saw was that when this desire goes to creatures rather than the Creator, the creatures buckle under the weight. They were never designed to carry it.",
    "You have probably spent a great deal of effort not appearing to need this. The Island in you has learned that the safest strategy is to need as little as possible from the outside world, and so you have constructed a life that does not visibly depend on anyone's memory of you. You are productive. You are capable. You can go long stretches without showing anyone your interior. But underneath that capable surface, the tally continues. And when the disconnection signal fires — when someone fails to notice, fails to remember, fails to carry you forward — the Island does not dissolve. It simply takes note. It files it away. And it keeps moving, alone, in the direction it was already heading.",
    "Here is what I want you to see. The sensitivity you carry — to being overlooked, to being forgotten, to occupying the margin rather than the center of someone's attention — is not vanity. It is the residue of something real that happened, usually early, in which the evidence was gathered and a verdict was reached: <i>the people in my world do not keep track of me the way I need them to.</i> And having reached that verdict, the Island made a practical decision: <i>I will not ask them to.</i> Take a breath before we continue, and answer the two questions below in writing. Not in your head — your head will process and refile; your hand will not.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the disconnection or significance signal fired. What happened, in two sentences? You are not looking for a dramatic event — the ordinary, almost-invisible ones are usually the most instructive.",
    "What was the size of the actual event, and what was the size of what moved inside you? If they did not match — if a small oversight produced a large internal response — you have just located the trigger.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding. The Island has been guarding this one for a very long time.",
    "Yours is this: <b>Am I enough to be remembered?</b>",
    "It is not the same as <i>Am I loved?</i>, though it sometimes wears that face. It is not <i>Am I competent?</i>, though you have built real competence in part as an answer to it. It is more specific than either. It is the question of a soul that wants to know whether it leaves a mark — whether its passage through the lives of others registers, whether it will be thought of in the night, whether something of it will remain when the moment is over. <i>Am I the kind of person who is remembered?</i>",
    "Most adults would prefer to believe they outgrew this question long ago. They have not. They have only relocated it. The childhood version was blunt: <i>does anyone think about me when I am not in the room?</i> The adult version has more syllables — <i>Does my work matter? Does this relationship account for me? Am I significant to the people whose significance I feel?</i> — but it is the same question, asking in the dark, waiting to see if anyone answers.",
    "For you, this question is especially alive because the Island has made it almost impossible to ask it out loud. An Island does not petition. An Island does not say, <i>I need to know that you think about me.</i> That kind of need would require an exposure that feels intolerable, and so the question stays inside — forming and reforming, gaining evidence, losing none.",
]

QUESTION_BODY_P2 = [
    "There is a reason that theologians from Augustine through Edwards have insisted that the deepest human longings point, when followed honestly, not to a human answer but to a divine one. Augustine's famous confession — <i>our heart is restless until it rests in Thee</i> — was not merely poetry. It was a map. And the longing to be remembered, inscribed, known in a way that nothing can erase, is at its root a longing shaped for God.",
    "The Scriptures are not embarrassed by this longing. Isaiah 49:15–16: <i>Can a woman forget her nursing child, that she should have no compassion on the son of her womb? Even these may forget, yet I will not forget you. Behold, I have engraved you on the palms of my hands.</i> The image is startling in its physicality. Not a note kept somewhere. Not a record filed. Engraved — cut in, permanent, requiring deliberate act to remove. The God of Scripture carries you on his hands as a decision he has made and will not unmake.",
    "Paul, in Romans 8:38–39, works his way through everything that might conceivably separate a person from the love of God — death, life, angels, principalities, things present, things to come, height, depth, anything in all creation — and lands on the impossibility of any of them succeeding. Not a general promise about the universe being benevolent. A specific promise about the One who knows your name: <i>nothing shall be able to separate us from the love of God in Christ Jesus our Lord.</i>",
    "But here is where pastoral honesty must be maintained, and it is harder for you than for most. Your nervous system wants a particular person to demonstrate the answer — to remember you consistently, to factor you in, to carry you in their thoughts. Scripture refuses to promise this. What it promises is larger and, in the moment the trigger fires, considerably more difficult to receive: you are known fully and held permanently by the One whose memory is perfect and whose love does not depend on your being easy to remember.",
]

QUESTION_BODY_P3 = [
    "The gospel anchor for the question you carry is this: you are an <i>Adopted Son</i>, a <i>Saint</i> — set apart by God as his own possession, fully known, fully named, inscribed on the palms of his hands. This is not comfort in the conventional sense. It is a theological claim, and it asks something of you: that you allow the answer God has given to actually contest the answer the trigger supplies.",
    "Here is the honest rub. Most Islands do not find it easy to receive this answer, not because they doubt it doctrinally but because receiving it requires a kind of openness — to being given to, to being known, to allowing the interior world to be entered — that the Island has learned to resist. The Island is exquisitely defended against needing, and receiving — genuine, ungrasping, un-performing receiving — is a form of need. To say <i>I am fully known and it is enough</i> is to relinquish the tally, and the Island has been keeping the tally so long that the hand cramps at the thought of setting it down.",
    "This is the work. Not a single decision — a practice, returned to daily, of letting the God who has engraved you on his hands answer the question that the trigger keeps re-opening. David did this in the Psalms, not once but continuously — returning to the question, returning to the answer, returning to the question again the next morning. <i>How long, O Lord? Will you forget me forever?</i> (Psalm 13:1). He does not pretend the question is settled in the morning and therefore illegitimate in the evening. He brings it back. This is not weak faith. It is honest faith — the kind the Island needs permission to practice.",
    "Before we close this section, I want you to use the table below. You are not analyzing yourself; you are simply observing. Use recent events, not ancient ones.",
]

ISLE_BODY_P1 = [
    "You have built something. You did not build it in a morning, and you probably did not know you were building it. But over years — and usually over a specific handful of moments in which the world showed you what it did and did not keep — you constructed a way of being in the world that we are going to call, throughout this walkthrough, <b>the Island</b>.",
    "The Island's strategy is this: <i>if I need very little from the outside world, I cannot be disappointed by what the outside world fails to give me.</i> The Island is not a hermit and is not antisocial. Islands often have deep and genuine relationships. But the Island has learned that the most essential interior material — the things that matter most, that carry the most weight, that feel the most vulnerable — is better handled alone. You process before you share. You reach conclusions before you open them for discussion. You do not need the other person's presence to work through what is happening inside you, and over time you have come to prefer it that way.",
    "There is something in Scripture that commends self-sufficiency of a kind. The book of Proverbs values the person who is not driven by the applause or contempt of the crowd: <i>Fear of man will prove to be a snare, but whoever trusts in the Lord is kept safe.</i> (Proverbs 29:25) The ability to hold your own counsel, to not be buffeted by every wind of opinion, to process deeply before speaking — these are genuine gifts. The Island has these gifts in abundance.",
    "But there is a cost that the Island rarely acknowledges, and it is this: the same self-containment that protects you from disappointment also prevents you from being genuinely known. And the question underneath your trigger — <i>Am I enough to be remembered?</i> — cannot be answered by a soul that has made itself invisible to the people whose memory it most wants. The Island's strategy and the Island's longing are working against each other at the roots.",
]

ISLE_BODY_P2 = [
    "The Island usually formed in one of several specific ways. Perhaps emotional expression was not welcome in your household growing up — not punished, exactly, but simply not valued. Feelings were something you handled on your own, the way you handle a headache: privately, without fuss, until it passed. Perhaps you learned early that needing people set you up for disappointment, and self-sufficiency began to feel not merely safer but more honest about the way things actually work. Perhaps you watched someone close to you need too much from other people, always in crisis, always dependent, and you decided quietly that you would never become that. Perhaps you were given more independence early than was healthy, and you grew comfortable with solitude before you understood what it cost you.",
    "John Owen, in his pastoral writings on mortification, observed that the desires of the soul do not die simply because they go unnamed. They go underground, where they continue to press and shape behavior without the light of honest examination. The Island's longing to matter — to be remembered, to leave a mark — has gone underground. It has not gone away. It operates quietly, beneath the composed exterior, in the tally the Island keeps but rarely shows.",
    "The people who love you have probably felt this at some level without being able to name it. They know there is more inside than they are allowed to reach. They have learned, over time, not to push — because pushing makes the Island close, and they have learned to take what they are given. This is not their failure. It is the Island's design working exactly as intended. And it means that the longing at the center of you — <i>I want to be known, I want to matter, I want someone to carry me in their thoughts</i> — is being systematically blocked by the same mechanism that is supposed to be answering it.",
    "<b>The Island is not your enemy.</b> He is a younger version of you who learned, in some specific and real circumstance, that managing alone was safer than hoping for company. He deserves your respect, not your contempt. But he is working overtime on a project — keeping you safe from need — that is also keeping you from the thing you most need. The water surrounding the Island is not protection. It has become, over time, a kind of prison. And the gospel's call to the Island is not to become a needier person in the therapeutic sense, but to receive the kind of knowing that does not require you to perform or petition — the knowing of a Father who sees you in secret, in the interior, in the place you have let no one enter.",
]

ISLE_BODY_P3 = [
    "What does it look like to begin loosening the Island's grip? Not demolishing it — it was built for a reason, and the reason was real. But beginning, slowly, to lower the drawbridge. Not to everyone. To someone. And before that, to God — who has already crossed the water, who is already inside, who has known everything you have processed alone and has never once turned away.",
    "It begins with naming what the Island is protecting. Not what it says it is protecting — not simply privacy or efficiency — but what it is actually protecting: the wound of not being enough to be held in someone's memory. Until you name that, the Island will continue to insist that solitude is simply a preference, when it is in fact a strategy.",
    "There is an exercise below that I want you to take seriously. I want you to write a letter from the Island — not a letter to him, but from him, in his voice, to you. The Island has something to say. He has been faithful; he has not had an honest conversation in a long time. Give him one now.",
]

ISLE_LETTER_INSTRUCTION = [
    "The letter below is written in the Island's voice. He is not villainous; he is frightened. Read it slowly. Then answer the three prompts that follow.",
    "Dear [Your name],",
    "I want to tell you what I have been doing, and why — before you decide I am the problem. Because I think you should hear what I have been trying to solve.",
    "I have been keeping you safe. Not safe in the abstract but from a specific danger: needing someone and discovering that you were not worth remembering. I have watched that happen. Enough times that I decided the only reasonable response was to stop needing in ways that could produce that verdict. So I built the Island. I gave you solitude that looks like strength. I gave you the ability to process everything alone, so you would never be caught having needed someone who was not there. I gave you a self that is, by design, not entirely visible — because what cannot be seen cannot be forgotten.",
    "What I did not anticipate — what I did not know how to account for, when I was small enough to still be making these decisions — is that the same distance that keeps you safe from forgetting also keeps you from being remembered. You cannot be carried in someone's thoughts if you have never let them carry you. I thought I was solving the problem. I was only moving it.",
    "I am not sure what to do with that. I have been at this too long to simply stop. But I think you should know why I am here, and what it is I am afraid of. Because it is not nothing. And you have known it was not nothing for a long time.",
    "The Island",
]

ISLE_LETTER_PROMPTS = [
    "What part of the Island's letter surprised you? Not the part you expected — the part you were not ready for.",
    "The Island says he built the distance to keep you safe from a specific wound. Name the wound in your own words. When was the first time the evidence for that wound was gathered?",
    "What would it cost the Island to let one person — just one — closer to the interior? Name the person. Name the cost honestly.",
]

ATT_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Island, the breaking has a particular shape — and it is called <b>the Attorney</b>.",
    "Here is what makes the Island's Attorney different from every other version of this breakdown, and different enough that it deserves careful naming: <i>you do not litigate in the open.</i> The Architect, when the Attorney takes the floor, tends to argue outwardly — to make the case visible, to prosecute in real time, to demand acknowledgment in the room where the wound happened. The Island does nothing of the kind. The Island takes the wound inside, closes the door, and begins building the case in private.",
    "This is what it looks like. Someone disconnects from you — fails to remember, fails to include, fails to honor what you brought. The wound registers. The Island, true to form, does not show it. The exterior remains composed. You may continue the conversation, finish the meal, complete the day. Nothing visible shifts. But inside, something has begun. The evidence has been accepted into evidence. The Island has started the brief.",
    "Over the following days — sometimes weeks, sometimes months — the case is assembled in private. Every exhibit is carefully filed. The original offense. The pattern of which it is a part. The specific instances that confirm the pattern. The things that were said and the things that were not said. The things you did that were not acknowledged. The investment you made that was not returned. The Island does not rush this process. It is patient, methodical, and thorough. The courtroom is entirely interior, and it runs without anyone else's knowledge.",
]

ATT_BODY_P2 = [
    "And then — usually at a moment that seems disproportionate to the occasion — the case is delivered. Not incrementally, the way a grievance might leak out over several conversations. All at once. A single, devastating closing argument, presenting the full brief, in a tone that the other person rarely saw coming, containing evidence they did not know had been gathered. The Island has been silent; what comes out is not silence. It is the summation of weeks of private prosecution, delivered without preamble, and then — the Island retreats.",
    "This is the specific danger of the Island's Attorney, and I want to name it plainly: <b>no one knew the courtroom was in session until the verdict was read.</b> The Architect's courtroom is loud and live; you can see it assembling, you can intervene before the closing argument. The Island's courtroom is private, and the verdict arrives as a complete surprise to everyone except the Island. This makes the Island's Attorney the most difficult version of this breakdown — not because it is the cruelest, but because by the time it is visible, the case has been running for a long time without the possibility of response or mercy.",
    "Scripture addresses this interior prosecution with unusual directness. Paul, writing to a church that had wounded him, said: <i>I do not even judge myself. For I am not aware of anything against myself, but I am not thereby acquitted. It is the Lord who judges me.</i> (1 Corinthians 4:3–4) What Paul refused was the assumption that his own private assessment — however carefully gathered — was the final word on the case. He had the right to his perceptions. He did not have the right to run the trial without the only Judge whose verdict counts.",
    "The Island's private prosecution is, in theological terms, an act of sovereignty — the assumption that the interior court is not only legitimate but sufficient. The God who says <i>I will not forget you</i> is also the God who says <i>vengeance is mine; I will repay</i> (Romans 12:19) — a promise that functions as a release from the obligation to prosecute.",
]

ATT_BODY_P3 = [
    "Here is the cruelty the Island must eventually face: the closing argument rarely produces what it was assembled to produce. The Island wants the wound acknowledged. The Attorney believes that a thorough enough case will finally compel this acknowledgment. It will not. Not because the other person is unmoved — they are often stunned — but because the verdict they give in the moment of confrontation has been preceded by weeks of private prosecution in which they had no voice. The acknowledgment, even when it comes, arrives inside a frame that makes it feel coerced rather than freely given. The Island does not feel better. It feels emptier, and retreats further.",
    "The Island's private case-building is, among other things, a way of staying connected to the wound. It is a form of relationship with the person who hurt you — a relationship conducted entirely in the interior, in which they appear only as defendant. Like all forms of distance-intimacy, it provides a substitute for the thing it prevents: real contact, real vulnerability, real repair. The Attorney keeps the Island occupied. But occupied is not the same as healed.",
    "The gospel's interruption of the Island's Attorney is not <i>your case is invalid.</i> It may be entirely valid. The gospel's interruption is this: <b>you already have an Advocate.</b> <i>If anyone does sin, we have an advocate with the Father, Jesus Christ the righteous.</i> (1 John 2:1) Christ is not a distant observer of your wound. He is your counsel. He has already entered the plea you have been trying to file, with the only evidence that finally settles the question — his own blood. You do not need to run the trial. The verdict over you is not <i>forgotten</i>. It is <i>known, carried, inscribed, kept.</i> You already have the Attorney you need. He is at the right hand of the Father.",
]

ATT_PROMPTS = [
    "Name the last time the Island's private courtroom was in session. Not the closing argument — the gathering of evidence. When did the case begin to be built? What was the original wound that opened it?",
    "What verdict were you hoping to compel? Write it in one sentence beginning: <i>If I could just make them understand that ___, I would finally feel ___.</i>",
    "What verdict has Christ already spoken over you — in this specific situation, about this specific wound — that makes the Island's case unnecessary?",
]

TWO_TOG_BODY = [
    "Now we place them next to each other, because the Island and the Attorney are not two separate problems. They are the same longing, shaped by the same wound, moving in the same direction — only one moves in sunlight and one moves underground.",
    "<b>The Island is what your longing does when it has time.</b> The Attorney is what your longing does when something has broken through the Island's defenses. The Island processes alone so that the alarm will not have to ring. The Attorney assembles privately when the alarm rings anyway. Together they form a sealed circuit, and the circuit will run all your life if nothing interrupts it.",
    "The pattern, in slow motion, looks like this. <b>(1)</b> The Island moves through the world self-sufficiently, needing less than most, maintaining the interior perimeter. <b>(2)</b> Something lands that crosses the perimeter anyway — a disconnection, a forgetting, a failure of significance. <b>(3)</b> The trigger fires. The body says, <i>I was not enough to be remembered here.</i> <b>(4)</b> The core question wakes up: <i>Am I enough to be remembered?</i> <b>(5)</b> The Island does not react outwardly. It takes the evidence inside and begins to file it. <b>(6)</b> Over days or weeks, the Attorney assembles the brief in private. <b>(7)</b> At an unannounced moment, the closing argument is delivered — then the Island retreats. <b>(8)</b> The verdict does not satisfy. The question is awake again within days. And the loop restarts.",
    "What breaks the loop is not better solitude, and it is not a better argument. It is a different answer to the question. Until the Island receives — really receives, not merely affirms as doctrine — that it is already known, already inscribed, already carried by the One who does not forget, the loop has nothing to run against. With that answer received and practiced over time, the Island begins, slowly, to find less need for the perimeter. The Attorney begins to file fewer cases. Neither retires fully in this life. But both begin to work shorter hours.",
    "Below is your sequence, written in your own words. Fill in the blanks. When you are done, read it aloud. The Island and the Attorney both lose a measure of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as disconnection — as not being "
    "enough to matter to this person — and the old question wakes up: <i>am I enough to be "
    "remembered?</i> My first move is to ____________________, because the Island in me believes "
    "that if I can ____________________, I will not need to expose the wound. When that does not "
    "work — when the wound stays open — the Attorney begins to build a case, privately, and the "
    "case says ____________________. What I am actually after, underneath all of it, is the "
    "verdict ____________________ \u2014 a verdict that Christ has already spoken over me, "
    "engraved not on paper but on ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small collection of tools — each one simple enough to carry, useful enough to reach for. None of them will resolve the Island's longing in a single application. All of them, practiced over months, will loosen the grip of the loop you just named.",
    "I have divided them into two sets: tools for when the Island is overworking its defenses (when the solitude has tipped into hiding), and tools for when the Attorney has begun assembling the brief (when the wound is fresh and the case is starting to build). The Island's tools come first, because the Island is the mechanism, and the Attorney cannot be addressed usefully until the mechanism is understood.",
]

ISLE_TOOLS = [
    ("The one honest sentence", "Once a day — not more, because the Island cannot sustain more without feeling exposed — say one honest sentence to someone who is present to you. Not a report. Not information. One sentence about something interior: what you are carrying, what you are glad about, what is difficult. The Island will resist this as unnecessary. Do it anyway. Over a month, the practice begins to widen the aperture between your interior world and the people who love you."),
    ("The audit of what you are protecting", "When you find yourself going quiet, processing alone, closing the interior door — ask one question before the door shuts: <i>am I protecting a healthy boundary, or am I protecting the wound from being touched?</i> You do not need to answer it out loud. But the asking disrupts the automatic nature of the Island's reflex. The Island loses some of its efficiency when it is required to explain itself."),
    ("The Psalm of disclosure", "When the Island's solitude tips into hiding, open to Psalm 62 or Psalm 139 and pray one section aloud. Psalm 62: <i>Trust in him at all times, O people; pour out your heart before him.</i> Psalm 139: <i>You have searched me and known me.</i> The Psalms are the one place where the interior world is required to speak, and they model a disclosure to God that is too honest to be performance. The Island can pray Psalms without feeling exposed, which is why it is the right discipline for this particular wound."),
    ("The handed-back tally", "Each evening, name one thing you noticed about your significance tally today — one moment where the question <i>am I being remembered?</i> was active. Do not litigate it; simply notice it. Then say: <i>Lord, I hand this tally back to you. You keep the record that matters.</i> The Island has been keeping the tally on God's behalf for years. This is the practice of returning it."),
    ("The ten-minute unlocked door", "Once a week, initiate a conversation about something interior with someone you trust — not a problem you need help solving, but something you are processing. The Island will call this unnecessary. It is, from the Island's perspective, the most dangerous thing on this list. It is also the most necessary, because the longing at the center of you cannot be answered by a soul that has made itself unreadable."),
]

ATT_TOOLS = [
    ("The case-age test", "When you notice that the Attorney is building a brief — when the same wound keeps presenting new evidence, keeps arranging and rearranging the facts — ask: <i>how long has this courtroom been in session?</i> If the answer is more than forty-eight hours, you are no longer processing; you are prosecuting. The distinction matters. Processing moves toward a response. Prosecution moves toward a verdict, and the Island's verdict is always delivered privately, always arrives as a surprise, and always costs more than the wound that opened the case."),
    ("Name the brief aloud", "Within twenty-four hours of the wound registering, tell one trusted person — not to rehearse the case but to break the secrecy: <i>the Attorney started up last night, and I need to name it before it goes underground.</i> The Island's Attorney does its most dangerous work in the dark. Spoken aloud to a safe witness, the brief loses its momentum. This is not the closing argument. It is the refusal to let the case run unseen."),
    ("Write it and hand it over", "If the brief will not leave you alone, write it out in full — every exhibit, every pattern, every instance. Then, slowly and deliberately, place the pages in a Bible, or tear them, or burn them — with the specific intention of handing the case to the only Judge who has the standing and the wisdom to run it. This is not suppression. It is transfer. You have given the evidence its hearing. You are declining to deliver the closing argument yourself."),
    ("The advocate prayer", "When the Attorney is loudest, pray these words: <i>Lord Jesus, you are my Advocate. You have seen the evidence. You know the wound. I do not need to run this trial. I receive the verdict you have already spoken over me.</i> Say it slowly, three times. The third time is usually when the courtroom begins to quiet."),
    ("The proportionality question", "Before delivering the closing argument — before bringing the assembled case to the other person — ask: <i>If this wound had happened last week, not four months ago, would I be saying this?</i> If the answer is no, you are not bringing a fresh wound; you are delivering a case that has been building in private for a long time. The closing argument, at that point, is not conversation. It is prosecution. Consider whether repair — not verdict — is what the situation actually requires."),
    ("The repair conversation", "The Island's Attorney tends to skip directly from wound to verdict, missing the middle step. The middle step is repair: a simple, direct naming of the original wound while it is still small, before the brief assembles. This requires the Island to speak before it has processed everything — to say <i>that landed hard on me</i> in the moment it lands, rather than weeks later when the full case is ready. This is the Island's hardest discipline, and also its most healing one."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Island in me, and you do not despise it. You know what it was built to protect. You know the specific moments — the ones I have never fully named, even to myself — in which the evidence for the Island's construction was gathered. Thank you that it kept me alive. Thank you that you have been present in the interior even when I gave you no invitation.",
    "But Father, the Island is tired, and the tally is heavy, and I have been keeping a record that was never mine to keep. Teach me to hand it back. Teach me that being fully known by you is the only answer that actually quiets the question underneath my trigger. When the disconnection fires — when the old wound says, <i>you are not enough to be remembered</i> — would you let me hear your answer before I hear the Island's? <i>I have engraved you on the palms of my hands. I will not forget you.</i> Let that land somewhere deeper than my doctrine.",
    "Lord Jesus, when the Attorney rises — when the wound goes underground and the brief begins to assemble in the dark — would you remind me that you are already my Advocate? That the case you have pleaded on my behalf was not assembled in secret but declared publicly, at Calvary, in front of the powers and authorities and every voice that has ever called me forgettable? I do not need to run the trial. The verdict has been spoken. Help me to receive it today, in this specific wound, as though it were the first time I heard it.",
    "Holy Spirit, where I am hiding, give me the courage to speak. Where I am prosecuting, give me the grace to repair. Where I am keeping the tally, give me the open hand. Remind me that the God who knows me fully has loved me fully — and that this is not a truth to file away. It is a truth to live inside.",
    "In the name of the One who, before the highest court in the universe, took the verdict I deserved so that I would never need to earn the one I long for \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not a conclusion. The Island and the Attorney have been with you a long time, and one reading will not retire them. What follows is a short list of next steps — some short, some long — for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different lines will land. The Island will resist a second reading — it prefers to file things once and move on. Read it again anyway. What you could not receive this week may be receivable then."),
    ("Take one tool, not six.", "Choose a single practice from Section 7 and try it for two weeks before adding another. The Island's tools are not programs; they are postures. One posture, held for long enough, begins to change the shape of the body."),
    ("Tell one person what you found.", "Not the whole document. One sentence: <i>I learned that my mechanism is the Island, and my breakdown is the Attorney.</i> Notice what happens when the Island's interior life is spoken to a trusted witness. This is not a performance. It is the first lowering of the drawbridge."),
    ("Read the Psalms of lament aloud.", "Psalm 13, Psalm 22, Psalm 62, Psalm 139, Psalm 88. Pray one aloud each morning for a week. The Psalms model what the Island most needs to practice: a soul that brings its interior to God without editing, without managing, without waiting until the processing is complete. Notice which lines stop you."),
    ("Read further on the longing underneath the wound.", "Tim Keller, <i>Counterfeit Gods: The Empty Promises of Money, Sex, and Power, and the Only Hope That Matters</i>. The Island tends to make self-sufficiency a counterfeit god — a way of answering the deepest questions without exposing them to another person. Keller names this pattern with precision and pastoral care. Also: C. S. Lewis, <i>The Weight of Glory</i> — his treatment of the human longing for significance is among the most honest and theologically careful in the English language. Read it slowly."),
    ("If you are stuck, ask for help.", "There are seasons when the Island and the Attorney are too entrenched to dislodge alone. A wise pastor, a Christian counselor, a trusted friend who has earned the right to your interior — these are not signs of failure. They are, for the Island, the most courageous thing on this list. The Island was built to manage alone. Learning to receive help is not the abandonment of the Island. It is the beginning of its redemption."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom by a Father who has engraved your name on his hands "
    "and who has not, in all the years you have been keeping the tally, forgotten a single entry. "
    "Go gently with yourself. The One who began the good work in you will be the one who finishes it."
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
    """Generate the Island+Attorney walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='ISLE', primary_breakdown='ATTY'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor's Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR'S WALKTHROUGH",
        cover_right_label="ISLAND  \u00b7  ATTORNEY",
        title="Take 139 Walkthrough \u2014 Island + Attorney",
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
    story.append(Paragraph("The Island &nbsp;\u00b7&nbsp; The Attorney", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disconnection &nbsp;\u00b7&nbsp; Core Question: Am I enough to be remembered?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cBehold, I have engraved you on the palms of my hands;&nbsp;\u2014&nbsp;<br/>"
        "your walls are continually before me.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Isaiah 49:16",
        ParagraphStyle("cqa", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: Opening ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read this slowly. The chapter that follows has been a long time in the writing.")
    for p in OPENING_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    # Section 1 flows to Section 2 on the same or next page without forcing a break

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
                   "What Scripture says — and the honest rub.",
                   "Engraved on the palms of his hands, and what receiving that answer costs you.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
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
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "How the Island formed, and what it has cost.",
                   "The longing that went underground, and the people who felt it.")
    for p in ISLE_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ISLE_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Island.",
                   "Read the Island's own words. Then answer the three questions below.")
    # Print the model letter
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
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Attorney.",
                   "The private courtroom. The silent case. The unannounced verdict.")
    for p in ATT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The courtroom no one knew was in session.",
                   "Why the Island's Attorney is the most dangerous version of this breakdown.")
    for p in ATT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
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
                   "The same longing, in two forms.",
                   "The Island and the Attorney are not two problems. They are one loop.")
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
                   "What to do when you feel the loop start.",
                   "Small enough to carry; useful enough to reach for.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 14))

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Island is overworking its defenses.",
                   "Five practices for the time before the alarm fires.")
    for name, desc in ISLE_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Attorney begins to assemble the brief.",
                   "Six practices for the moment the private courtroom opens.")
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
        primary_mechanism = "ISLE"
        primary_breakdown = "ATTY"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "island_attorney_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024
    print(f"DONE: island_attorney.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB) — {out_path}")
