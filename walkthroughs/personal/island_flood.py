"""Personal Walkthrough — Island + Flood.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disconnection trigger, "Am I enough to be remembered?" core question.
~25 pages, 9 sections.

Key insight: The Island has spent so long not feeling — or rather, not releasing —
that when the Flood comes it surprises everyone, including the Island. The spouse
thought you were unflappable. The Island thought the silence was working. Section 5
names the Flood not as a failure of composure but as the first signal that the silence
cost something — a long-delayed honesty, not a loss of control. Lamentations and
Psalm 88 frame the unique pastoral move: sometimes the only faithful thing left is to
refuse to compose yourself.
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
    "Before you read any further, I want to do for you what a good counselor does in the first session. I want to lower the lights, slow the pace, and make it safe to say the thing that has not yet been said. What you are about to look at is not a personality inventory or a catalog of your worst moments. It is a careful look at the way your soul has learned to manage a particular kind of pain, and why that management has shaped you into something we are going to call, throughout this walkthrough, the Island. Not because you are cold, or incapable of love. You are almost certainly neither. You are an Island because something early in your life taught you that the distance between your interior world and the world outside was not a gap to be closed but a perimeter to be maintained. You learned to process alone. You learned that needing people in the transparent and exposed way that needing requires set you up for a kind of disappointment that was not worth the cost.",
    "We are going to walk through your trigger \u2014 the moment your nervous system registers <i>something is wrong here.</i> We will listen to the question underneath that moment, the one that has probably been asking itself since you were young, in some version or another. We will name the strategy you have built in response, and then we will look at the place that strategy breaks under pressure. Only then will we put tools in your hands.",
    "If you were sitting across from me, I would say this before we went further. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who has not left you to manage your significance alone; a Son who endured, in Gethsemane, the most complete desolation in human history and who spoke from the cross the words of Psalm 22 \u2014 <i>My God, my God, why have you forsaken me?</i> \u2014 so that you would never have to speak them and mean them; and a Spirit who is, at this very moment, more present to you than you are to yourself.",
    "So read slowly. Argue with what does not fit. Stay with what does. Write in the margins if you have them. Pray when something catches in your throat, because that catch is usually the Lord saying, <i>look here, with me.</i> The goal of this walkthrough is not mere self-knowledge. The goal is a slightly freer life, lived in the company of a God who has never once, not for a single moment, lost track of your name. Take your time. The chapter you are about to read about yourself has been a long time in the writing.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life do not know it is occurring. It does not look dramatic from the outside. Sometimes it looks like nothing at all. You are in the middle of an ordinary evening, or a gathering, or a conversation, and something happens \u2014 or fails to happen \u2014 and something inside you registers it with a precision that surprises you when you stop to notice it.",
    "Perhaps your spouse began telling a story from the weekend and did not include you in the telling, as though you had been furniture rather than a participant. Perhaps a group of friends made a plan that everyone seemed to know about already, and you discovered it in passing, the way you learn about things that do not require your involvement. Perhaps you said something at a dinner table \u2014 something that mattered to you, something you had been thinking about \u2014 and the conversation moved on without acknowledgment, as if the words had dissolved in the air the moment you finished speaking. Perhaps you spent weeks on something, gave it carefully, and the person who received it said thank you and set it down and never mentioned it again.",
    "On the surface, none of these qualify as injuries. They are the ordinary traffic of relational life, the small gaps and oversights that accumulate in every friendship, every marriage, every community. But for you, they do not stay small. The moment registers as something more than inconvenience. It registers as a signal \u2014 quiet, specific, and unmistakable: <i>you were not necessary to this moment. You were not thought of. You were here, and you did not leave a mark.</i>",
    "This is your trigger. The technical name for it is <b>disconnection</b>, though in your case disconnection and significance travel together, because disconnection wounds you not merely as exclusion but as confirmation: <i>I did not matter enough to be included.</i> And mattering \u2014 being the kind of person whose absence is noticed, whose presence changes the shape of a room, whose words are carried forward rather than dissolving where they landed \u2014 is something your soul has been quietly tracking for a very long time.",
    "C. S. Lewis, in <i>The Weight of Glory</i>, wrote about the longing in every human being to be known and noticed by the universe \u2014 to have one's name spoken by the highest authority. He called it a desire for glory, and he was unwilling to be embarrassed by it, because he recognized it as a longing God himself had placed there. What he also observed was that when this desire goes to creatures rather than to the Creator, the creatures buckle under the weight. They were never designed to carry it, and neither was the Island, though the Island has been trying to answer the question on its own for a very long time.",
    "You have probably spent considerable effort not appearing to need this. The Island in you has learned that the most efficient strategy is to need as little as possible from the outside world, and so you have constructed a life that does not visibly depend on anyone's memory of you. You are capable. You are productive. You can go long stretches without showing anyone your interior. But underneath that capable exterior, the tally continues. And when the disconnection signal fires \u2014 when someone fails to notice, fails to remember, fails to carry you forward \u2014 the Island does not dissolve. It simply takes note. It files it. And it keeps moving, alone, in the direction it was already heading.",
    "Here is what I want you to see. The sensitivity you carry \u2014 to being overlooked, to the specific ache of not having left a mark \u2014 is not vanity. It is the residue of something real that happened, usually early, in which the evidence was gathered and a verdict was quietly reached: <i>the people in my world do not keep track of me the way I need them to.</i> And having reached that verdict, the Island made a practical decision: <i>I will not ask them to.</i> Take a breath, and answer the two questions below in writing. Not in your head \u2014 your head will process and refile; your hand will not.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the disconnection or significance signal fired in you. What happened, in two sentences? You are not looking for a dramatic event \u2014 the almost-invisible ordinary ones are usually the most instructive.",
    "What was the size of the actual event, and what was the size of the response inside you? If they did not match \u2014 if a small oversight produced a large internal movement \u2014 you have just located the trigger.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding. The Island has been guarding this one for a very long time, usually without anyone knowing it is there.",
    "Yours is this: <b>Am I enough to be remembered?</b>",
    "It is not the same as <i>Am I loved?</i>, though it sometimes wears that face. It is not <i>Am I competent?</i>, though you have built real competence in part as a way of trying to answer it. It is more specific than either. It is the question of a soul that wants to know whether its passage through the lives of others registers \u2014 whether it will be thought of in the night, whether something of it will remain when the moment is over, whether the world is, in some measurable way, different because you were in it. <i>Am I the kind of person who gets remembered?</i>",
    "Most adults prefer to believe they outgrew this question long ago. They have not. They have only relocated it. The childhood version was blunt: <i>does anyone think about me when I am not in the room?</i> The adult version has more syllables \u2014 <i>Does my work matter? Does this relationship account for me? Am I significant to the people whose significance I feel?</i> \u2014 but it is the same question, asking in the dark, waiting to see whether anything answers back.",
    "For you, this question is especially alive because the Island has made it nearly impossible to ask it out loud. An Island does not petition. An Island does not say, <i>I need to know that you think about me.</i> That kind of need would require an exposure the Island finds intolerable. So the question stays inside \u2014 forming and reforming, gathering evidence, losing none.",
]

QUESTION_BODY_P2 = [
    "There is a reason that theologians from Augustine through Jonathan Edwards have insisted that the deepest human longings, followed honestly to their source, point not to a human answer but to a divine one. Augustine's confession \u2014 <i>our heart is restless until it rests in thee</i> \u2014 was not merely poetry. It was a map. And the longing to be remembered, inscribed, known in a way that nothing can erase, is at its root a longing shaped for God.",
    "The Scriptures do not flinch from this. Isaiah 49:15\u201316: <i>Can a woman forget her nursing child? Even these may forget, yet I will not forget you. Behold, I have engraved you on the palms of my hands.</i> The image is startling in its specificity. Not a note kept somewhere. Engraved \u2014 cut in, deliberate, permanent. The God of Scripture carries you on his hands as a decision he has made and will not reverse.",
    "Paul, in Romans 8:38\u201339, works through everything that might conceivably separate a person from the love of God \u2014 death, life, angels, height, depth, anything in all creation \u2014 and lands on the impossibility of any of them succeeding: <i>nothing shall be able to separate us from the love of God in Christ Jesus our Lord.</i> The Island's deepest fear is that it is, at bottom, forgettable. Paul says: the One who cannot forget has claimed you.",
    "But here is where pastoral honesty must be maintained, and it is harder for you than for most. Your nervous system wants a particular person \u2014 a spouse, a friend, a parent \u2014 to demonstrate the answer. It wants to be factored in, remembered consistently, carried in someone's thoughts. Scripture refuses to promise this. What it promises is larger and, in the moment the trigger fires, considerably more difficult to receive: you are known fully and held permanently by the One whose memory is perfect and whose love does not depend on your being easy to remember.",
]

QUESTION_BODY_P3 = [
    "The gospel anchor for the question you carry is this: you are an <i>Adopted Son</i> \u2014 a <i>Saint</i>, set apart by God as his own possession, fully known, fully named, inscribed on the palms of his hands. This is not comfort in the conventional sense. It is a theological claim, and it asks something of you: that you allow the answer God has given to actually contest the answer the trigger supplies.",
    "Here is the honest difficulty. Most Islands do not find it easy to receive this answer, not because they doubt it doctrinally but because receiving it requires a kind of openness \u2014 to being given to, to being known, to allowing the interior world to be entered \u2014 that the Island has learned to resist. The Island is exquisitely defended against needing, and receiving \u2014 genuine, ungrasping, un-performing receiving \u2014 is a form of need. To say <i>I am fully known and it is enough</i> is to relinquish the tally, and the Island has been keeping the tally for so long that the hand cramps at the thought of setting it down.",
    "This is the real work. Not a single decision but a practice, returned to daily, of letting the God who has engraved you on his hands answer the question that the trigger keeps re-opening. David did this in the Psalms, returning to the question and returning to the answer and then returning to the question the next morning. <i>How long, O Lord? Will you forget me forever? How long will you hide your face from me?</i> (Psalm 13:1) He does not pretend the question is settled at dawn and therefore illegitimate by evening. He brings it back. This is not weak faith. It is honest faith, and it is the kind the Island most needs permission to practice. Before we close this section, use the table below — recent events, not ancient ones.",
]

ISLE_BODY_P1 = [
    "You have built something. You did not build it in a morning, and you almost certainly did not know you were building it with quite this much weight on it. But over years \u2014 over a specific handful of moments in which the world showed you what it did and did not keep \u2014 you constructed a way of being in the world that we are going to call, throughout this walkthrough, <b>the Island</b>.",
    "The Island's strategy is this: <i>if I need very little from the outside world, I cannot be devastated by what the outside world fails to give me.</i> The Island is not a hermit and is not antisocial. Islands often have deep relationships. But the Island has learned that the most essential interior material \u2014 the things that carry the most weight, that feel the most vulnerable \u2014 is better handled alone. You process before you share. You reach your own conclusions before you open them for discussion. Over the years, this has come to feel not merely manageable but preferable.",
    "There is something in Scripture that commends this kind of self-possession. Proverbs is direct about it: <i>Fear of man will prove to be a snare, but whoever trusts in the Lord is kept safe.</i> (Proverbs 29:25) The ability to hold your own counsel, to not be carried away by the opinion of the crowd, to process deeply before you speak \u2014 these are genuine gifts. The Island has these gifts in abundance. You are not, in your self-containment, simply wrong. You have been doing something real, and doing it faithfully, for a long time.",
    "But there is a cost the Island almost never names: the same self-containment that protects you from disappointment also prevents you from being genuinely known. The question underneath your trigger \u2014 <i>Am I enough to be remembered?</i> \u2014 cannot be answered by a soul that has made itself systematically invisible to the people whose memory it most wants. The Island's strategy and its longing are working against each other at the roots.",
]

ISLE_BODY_P2 = [
    "The Island usually formed in one of several ways. Perhaps emotional expression was not welcome in your household growing up \u2014 not punished exactly, but simply not valued. Feelings were things you handled privately, the way you handle a headache: alone, without fuss, until they passed. Perhaps you learned early that needing people set you up for disappointment, and self-sufficiency began to feel not merely safer but more honest. Perhaps you watched someone close to you need too much, and you decided quietly that you would never become that. Perhaps you were given more independence early than was healthy, and you grew comfortable with solitude before you understood what it was costing you.",
    "John Owen observed that the desires of the soul do not die simply because they go unnamed. They go underground, where they continue to press and shape behavior without the light of honest examination. The Island's longing to matter, to be remembered, to leave something behind \u2014 has gone underground. It has not gone away. It operates quietly, in the tally the Island keeps but rarely shows. The people who love you have probably felt this without being able to name it. They know there is more inside than they are permitted to reach, and they have learned not to push. And so the longing at the center of you \u2014 <i>I want to be known, I want to matter, I want someone to carry me in their thoughts when I am not present</i> \u2014 is being systematically blocked by the very mechanism that is supposedly answering it.",
    "<b>The Island is not your enemy.</b> He is a younger version of you who learned, in some real circumstance, that managing alone was safer than hoping for company. He deserves your respect. But he is working overtime on a project \u2014 keeping you safe from need \u2014 that has become, without his knowing it, the very thing that makes the longing impossible to answer. The gospel's call to the Island is not to become a different kind of person, but to receive the kind of knowing that requires no performance and no petition \u2014 the knowing of a Father who sees you in secret, in the interior, in the place you have allowed no one else to enter.",
]

ISLE_BODY_P3 = [
    "What does it look like to begin loosening the Island's grip? Not dismantling it \u2014 it was built for a reason, and the reason was real. But beginning, slowly, to lower the drawbridge. Not to everyone. To one person. And before that, to God \u2014 who has already crossed the water, who is already inside, who has known everything you have ever processed alone and has never recoiled from it.",
    "It begins with naming what the Island is protecting. Not what it says it is protecting \u2014 not merely privacy or efficiency or independence \u2014 but what it is actually protecting: the wound of not being enough to be held in someone's memory. Until you name that, the Island will continue to insist that its solitude is simply a preference, a temperament, a gift. It is those things too. But underneath them, it is a strategy. And a strategy can be examined.",
    "There is a letter exercise below, and I want you to take it seriously. It is written from the Island's own voice, to you. The Island has something to say that it has not been asked to say before. Give it the space.",
]

ISLE_LETTER_MODEL = [
    "The letter below is written in the Island\u2019s voice. He is frightened, and he has been faithful for a long time. Read it slowly. Then answer the three prompts that follow.",
    "Dear [Your name],",
    "I have been keeping you safe \u2014 not safe in the abstract, but from a specific wound: the wound of needing someone to remember you and discovering that you were not memorable enough. I watched that happen to you. Enough times that I decided the only reasonable response was to stop needing in ways that could produce that verdict. So I built the Island. I gave you solitude that looks like strength. I gave you a self that is, by design, not entirely visible \u2014 because what cannot be seen cannot be forgotten in the way that matters most. What I did not know is that the same distance that keeps you safe from being forgotten also keeps you from being remembered. I thought I was solving the problem. I was only moving it underground.",
    "Part of the reason I have held so tightly is that the silence felt like dignity. As long as I did not need, I could not be pitied. But I think you should know that the tally I have been keeping \u2014 the long, careful record of who has and has not remembered you \u2014 has always been too heavy for me to hold alone.",
    "The Island",
]

ISLE_LETTER_PROMPTS = [
    "What part of the Island's letter was not what you expected? Not the part you recognized \u2014 the part that surprised you.",
    "The Island says he built the distance to protect you from a specific wound. Name the wound in your own words. When was the first time the evidence for it was gathered?",
    "What would it cost the Island to let one person \u2014 just one \u2014 closer to the interior? Name the person. Name the cost. Be honest about both.",
]

FLOOD_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Island, the breaking takes a form that surprises nearly everyone who witnesses it \u2014 including, often, the Island itself.",
    "Here is what happens. The Island has been keeping its composure. It has been doing what it does well \u2014 processing alone, maintaining the exterior, filing everything in the interior rather than releasing it into the open air. Then something lands. Not always a single large event. More often it is an accumulation of small ones: a recurring disconnection that was never quite addressed, a pattern of not being thought of that the Island has been documenting in the interior for weeks or months, a private ache that had no occasion to surface, a grief that was held so long it began to feel like furniture. And then \u2014 usually at a moment that seems disproportionately small, a moment that no one watching would flag as significant \u2014 something gives.",
    "What comes next is not an argument, and it is not a cold withdrawal, and it is not the kind of measured statement the Island usually produces when it decides to speak. It is a Flood. We call it <b>the Flood</b> deliberately, because a flood does not build \u2014 it releases. It does not discriminate \u2014 it carries everything that was waiting behind the dam, sorted or unsorted, old and new, proportionate and disproportionate. Tears. Accumulated feeling. Intensity that the people watching cannot locate on the map of recent events, because the recent event was not the beginning of the story \u2014 it was only the final weight on a structure that had been absorbing weight for a very long time. The people who love you, watching this, often do not recognize you. <i>I thought you were fine.</i> You have heard some version of that sentence. Perhaps you have said it to yourself. The Island spent months appearing fine; the Flood arrives, and the Island is, suddenly, very much not fine.",
]

FLOOD_BODY_P2 = [
    "What is happening during a Flood is not, precisely, a breakdown. It is the consequence of a kind of holding that has been applied for too long and too broadly. The Island is exquisitely good at containing. What it has not been trained in is releasing a little at a time. And so the only release available to it, after the structure has absorbed enough, is total release. Not because you are unstable. Because the dam was full.",
    "David Powlison observed in <i>Good and Angry</i> that unexpressed emotion does not disappear \u2014 it compounds. What is not grieved becomes weight. What is not lamented accumulates until it finds its own exit through a crack you did not plan for. The Island's error is not that it has feelings. It is that it has been filing them rather than praying them, holding them in the interior rather than lifting them to the One who can actually receive them.",
    "Here is the thing that needs to be said plainly, and named in a way the Island has probably never heard: <b>for you, the Flood is often the first signal that the silence cost something.</b> The Architect+Flood is a planner whose dam bursts after months of impossible suppression; this has its own particular pain. But the Island+Flood carries an additional weight: the spouse, the friend, the colleague, thought the Island was <i>unflappable.</i> They genuinely believed nothing was gathering. And they were not wrong to believe it, because the Island spent considerable energy communicating exactly that. The Flood, when it comes, is not only a release \u2014 it is a revelation. It reveals, to everyone including the Island, that the silence had a cost that was never declared. And that revelation is one of the more disorienting experiences the Island will have.",
]

FLOOD_BODY_P3 = [
    "Scripture is unusually honest about this predicament. The book of Lamentations is written by a prophet who refused to compose himself. Jeremiah does not manage his devastation or sort it before presenting it. He speaks in the middle of it. <i>Is it nothing to you, all you who pass by? Look and see if there is any sorrow like my sorrow.</i> (Lamentations 1:12) This is not a failure of faith. This is what honest lament sounds like when it can no longer be contained. Consider also Psalm 88 \u2014 the only psalm in the entire psalter that ends without resolution. Every other lament finds its way, before the final verse, to some form of trust or anticipated deliverance. Psalm 88 ends in darkness: <i>darkness is my closest friend.</i> (Psalm 88:18) The Church has kept this psalm for three thousand years not because it is pessimistic but because there are seasons of the soul in which the darkness has not yet lifted, and the only faithful thing is to say so rather than to manufacture a resolution that has not arrived. John Calvin wrote that \"the heart's affections are an ocean\" \u2014 vast, not to be ashamed of, and not to be dammed up in the name of composure.",
    "<b>For the Island, the pastoral word in Section Five is this: the Flood is not a failure of composure. It is a long-delayed honesty.</b> The silence was not strength; it was a strategy that eventually reached its limit. The Flood is the interior life speaking, finally and at great cost, the truth about what it has been carrying. The work is not to prevent the Flood by holding tighter. The work is to learn the discipline of small, regular release \u2014 the lament offered to God before the accumulation becomes an avalanche. Psalm 13, Psalm 22, Psalm 42, Psalm 88 \u2014 these are not the prayers of people who lost faith. They are the prayers of people who kept it by refusing to pretend. Martyn Lloyd-Jones observed that the psalms of lament teach the Church something it tends to suppress: that it is more faithful to cry out honestly in the dark than to perform a composure you do not have. The Island has been performing composure. The Flood is the interior life protesting that performance. The invitation is not to silence the protest but to learn to make it earlier, smaller, and to God.",
]

FLOOD_PROMPTS = [
    "Think of the last time the Flood came \u2014 the last time everything arrived at once, in a way that surprised you or the people around you. What had been gathering, and for how long? Be as specific as you can.",
    "What would it have taken \u2014 what small, earlier act of honesty, offered to God or to one person \u2014 to prevent the flood from reaching that level? What would the Island have had to allow?",
]

TWO_TOG_BODY = [
    "Now we put them next to each other, because the Island and the Flood are not two separate problems. They are the same soul in two different seasons \u2014 one in which the holding is working, and one in which it has run out of room.",
    "<b>The Island is what your soul does when it has time.</b> The Flood is what your soul does when the time has run out and the silence has cost more than it could bear. The Island manages so the dam will never have to break. The Flood is what happens when the dam breaks anyway. Together they form a cycle \u2014 and the cycle will run for the rest of your life if nothing interrupts it.",
    "The pattern, in slow motion, looks like this. <b>(1)</b> The Island moves through the world self-contained, needing less than most, maintaining the interior perimeter. <b>(2)</b> Something lands that crosses the perimeter anyway \u2014 a disconnection, a forgetting, a failure of significance. <b>(3)</b> The trigger fires. The body says, <i>I was not enough to be remembered here.</i> <b>(4)</b> The core question wakes up: <i>Am I enough to be remembered?</i> <b>(5)</b> The Island does not react outwardly. It takes the wound inside and files it. <b>(6)</b> This happens again. And again. The file grows thicker. <b>(7)</b> At a moment no one predicted \u2014 often triggered by something small \u2014 the structure gives and the Flood comes: tears, accumulated feeling, intensity that startles everyone in the room. <b>(8)</b> Afterward, the Island is often ashamed of the Flood and resolves to hold more tightly next time. The cycle restarts.",
    "What breaks the cycle is not better self-containment and not stronger willpower. It is a different practice: the small, regular, honest offering of what you are actually carrying to a God who is listening. Until the Island learns to lament before the accumulation becomes an avalanche \u2014 to bring the complaint to God while it is still a handful rather than a flood \u2014 the pressure will keep building until the structure fails. With this practice in place, slowly, the Floods become less catastrophic, then less frequent, then, for some Islands, rare.",
    "Below is your sequence, written in your own words. Fill in the blanks. When you are done, read it aloud. The Island and the Flood both lose a measure of their power when they hear themselves named out loud, in your own voice.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as disconnection \u2014 "
    "as not being enough to matter to this person \u2014 and the old question wakes up: "
    "<i>am I enough to be remembered?</i> My first move is to ____________________, "
    "because the Island in me believes that if I can ____________________, I will not "
    "have to expose the wound. What I do not always see is that I have been carrying "
    "____________________ for ____________________, and the filing has been adding "
    "pressure rather than releasing it. When the structure finally gives, the Flood "
    "releases everything at once \u2014 the long-held ____________________ that needed "
    "to be named. What I actually needed, before the Flood, was to offer it earlier "
    "to ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small collection of practices \u2014 each one simple enough to carry, durable enough to make a real difference. None of them will resolve the Island's longing in a single application. All of them, practiced with any consistency over months, will loosen the grip of the cycle you just named.",
    "I have divided them into two sets: tools for when the Island is overworking its defenses (when the solitude has tipped from gift into hiding), and tools for when the Flood has arrived or is building pressure (when the structure is straining and you can feel it). The Island's tools come first, because the Island is the mechanism, and you cannot address the Flood usefully until you understand the Island's part in it.",
]

ISLE_TOOLS = [
    ("The one honest sentence", "Once a day \u2014 not more, because the Island cannot sustain more without feeling exposed and pulling back \u2014 say one honest sentence to someone who is present to you. Not a report. Not information. One sentence about something interior: what you are carrying today, what you are glad about, what is quietly difficult. The Island will resist this as unnecessary. Do it anyway. Over a month, the practice begins to widen the aperture between your interior world and the people who love you. The aperture is where the Flood eventually finds a smaller exit."),
    ("The audit of what you are protecting", "When you find yourself going quiet, closing the interior door \u2014 pause and ask: <i>am I protecting something healthy, or am I protecting the wound from being touched?</i> You do not need to answer it out loud. The asking alone disrupts the automatic quality of the Island's reflex."),
    ("The Psalm of disclosure", "When the Island's solitude tips toward hiding, open to Psalm 62 or Psalm 139 and pray one section aloud \u2014 out loud, not silently. Psalm 62: <i>Trust in him at all times, O people; pour out your heart before him.</i> Psalm 139: <i>You have searched me and known me.</i> The Psalms are the one place where the interior world is required to speak, where processing alone is explicitly not sufficient, where disclosure to God is the only adequate response. The Island can practice Psalms without feeling fully exposed, which is why it is the right discipline for this particular wound."),
    ("The ten-minute unlocked door", "Once a week, initiate a conversation about something interior with someone you trust \u2014 not a problem you need help solving, but something you are carrying. The Island will resist this. It is, from the Island's perspective, the most threatening practice on this list. It is also the most necessary: the longing at the center of you cannot receive its answer from a soul that has made itself systematically unreadable."),
]

FLOOD_TOOLS = [
    ("Name it before it is a flood", "When you feel the pressure building \u2014 when the interior file has been growing for more than a week with no release \u2014 say something to someone. Not the entire accumulation. One sentence: <i>I have been carrying something I have not named yet.</i> This single practice, done while the content is still manageable, prevents most Floods. The Flood happens because the naming was delayed past the point of manageability. Learn to speak before you are ready to speak perfectly."),
    ("The pre-flood prayer of lament", "When you sense that you have been holding something for too long \u2014 when the composure is beginning to feel effortful rather than natural \u2014 pray Psalm 13 or Psalm 88 aloud. Not as a devotional exercise. As an act of deliberate transfer: <i>I am carrying this, Lord, and I am releasing it to you before it becomes a flood.</i> The Psalms of lament were given to the Church precisely as the liturgy for this moment. The prophet Jeremiah, who wrote Lamentations without composing himself, is the patron saint of Islands who have held too long."),
    ("After the flood: the sorting conversation", "Once the waters have receded, sit with the person most affected and sort. Ask: <i>Of everything that came out, what was the one thing I most needed you to hear?</i> The Flood itself is often unsortable in the moment; the conversation afterward is the actual repair. Repair requires the Island to name specifically what was real, rather than leaving it buried under the volume."),
    ("The proportionality question", "Before you decide to stay silent about something that hurt, ask: <i>If I do not name this now, how much weight will it add to what I am already carrying?</i> The Island calculates the cost of speaking and concludes that silence is cheaper. This question forces it to calculate also the cost of not speaking \u2014 to see the dam, not only the water."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Island in me, and you do not despise it. You know what it was built to protect. You know the specific moments \u2014 the ones I have never fully named even to myself \u2014 in which the evidence for the Island's construction was gathered. Thank you that it kept me alive. Thank you that you have been present in the interior even when I gave you no invitation, even in the seasons when I processed everything alone and brought you none of it. You were there anyway. You always were.",
    "But Father, the Island is tired, and the tally is heavy, and the silence has been costing more than I have admitted. Teach me what the Psalmist knew \u2014 that honest complaint before you is not weakness but faithfulness, that the dark unresolved cry of Psalm 88 is as much your word as the triumphant close of Psalm 103. Teach me the discipline of small, honest release \u2014 the word of lament offered to you while it is still a handful, before it becomes a flood. Remind me that you have engraved me on the palms of your hands, and that no silence of mine has ever caused you to forget it.",
    "Lord Jesus, when the Flood comes \u2014 when everything I have held too long comes out in front of someone who thought I was unflappable \u2014 remind me that this is not the end of the story. You wept at Lazarus's grave. You prayed in Gethsemane in agony, in front of witnesses. You are not a God who handles only the composed version of my soul. Meet me in the ruins too.",
    "Holy Spirit, where I am hiding, give me the courage to speak \u2014 one sentence, to one person, before the pressure builds beyond managing. Where I have already flooded and am now rebuilding the walls higher out of shame, give me the grace to leave a door in the structure instead \u2014 a door that opens regularly, in prayer, in lament, in honest disclosure. In the name of the One who, on the cross, cried out the opening words of Psalm 88 and thereby sanctified every cry that does not yet have an answer \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not a conclusion. The Island has been with you for a long time, and the Flood has surprised you more than once, and neither of them will retire after a single afternoon of reading. What follows is a short list of next steps \u2014 some immediate, some long-term \u2014 for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different sentences will land. The Island prefers to file things once and consider them addressed. Read it again anyway."),
    ("Take one tool, not five.", "Choose a single practice from Section 7 and try it for two weeks before adding another. The Island's instinct is to assess all of them, implement none, and consider the matter covered. Resist this. One practice, held for long enough, changes the shape of the soul."),
    ("Read Lamentations once through.", "Read all five chapters in a single sitting, slowly. Notice where you feel Jeremiah is being too honest, too unguarded. That feeling is the Island's reaction. Notice where you feel relieved that someone said it. That is the place the Spirit is pointing."),
    ("Read further on the disciplines of honest lament.", "Tim Keller, <i>Walking with God through Pain and Suffering</i> \u2014 especially the chapters on lament, which address the Island's temptation to perform composure. C. S. Lewis, <i>A Grief Observed</i> \u2014 Lewis shows you what it looks like to be an intelligent, composed man who stopped pretending and started being honest with God. David Powlison, <i>Good and Angry</i> \u2014 on what unexpressed emotion does to the soul, and what it looks like to bring it to God rather than to file it."),
    ("Tell one person what you found.", "Not the whole document. One sentence: <i>I learned that my mechanism is the Island, and my breakdown is the Flood, and the Flood is apparently the first signal that my silence cost something.</i> Say it to your spouse, or to a pastor, or to a trusted friend who has earned access to your interior. Secrecy is the dam's primary building material. Spoken to a safe witness, the pressure begins to decrease."),
    ("If you are stuck, ask for help.", "There are seasons when the Island and the Flood are too entrenched to dislodge alone. A wise pastor, a Christian counselor, a friend who has earned the right to your interior \u2014 for the Island, this is the most courageous thing on this list."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom by a Father "
    "who has engraved your name on his hands and who has not, in all the years you have been "
    "keeping the tally alone, forgotten a single entry. The Flood was not the end of the story. "
    "It was, perhaps, the moment the story got honest. "
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
    """Generate the Island+Flood walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='ISLE', primary_breakdown='FLOOD',
    primary_trigger='DISC', core_question='REM'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="ISLAND  \u00b7  FLOOD",
        title="Take 139 Walkthrough \u2014 Island + Flood",
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
    story.append(Paragraph("The Island &nbsp;\u00b7&nbsp; The Flood", S["CoverProfileVal"]))
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
                   "Engraved on the palms of his hands, and what receiving that answer costs you.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
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
                   "How the Island formed.",
                   "The longing that went underground, and the people who felt the distance.")
    for p in ISLE_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ISLE_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Island.",
                   "Read it slowly. Then answer the three questions below.")
    letter_style = ParagraphStyle(
        "IslandLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for line in ISLE_LETTER_MODEL:
        story.append(Paragraph(line, letter_style))
    story.append(Spacer(1, 8))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in ISLE_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Flood.",
                   "What happens when the Island\u2019s silence has cost more than it can bear.")
    for p in FLOOD_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "What the Flood is looking for.",
                   "A long-delayed honesty. Not a failure of composure.")
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

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same soul in two different seasons.",
                   "Island and Flood are not two problems. They are one cycle.")
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
    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "What to do when you feel the cycle start.",
                   "Small enough to carry; useful enough to reach for.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Island is overworking its defenses.",
                   "Four practices for the time before the pressure becomes critical.")
    for name, desc in ISLE_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Flood has come or is coming.",
                   "Five practices for the overflow and its aftermath.")
    for name, desc in FLOOD_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<b>Integration:</b> The single discipline connecting both sides is this \u2014 "
        "the small, honest prayer of lament before the accumulation demands a flood. "
        "Before the silence tips into hiding, bring it to God. Before the interior file "
        "gets too heavy, bring it to God \u2014 not as a last resort but as a first practice. "
        "The Psalms of complaint were given to you for exactly this moment.",
        S["BodyJ"]))
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
        primary_breakdown = "FLOOD"
        primary_trigger = "DISC"
        core_question = "REM"
        name = "Test User"

    # Print letter snippet before building PDF
    print("=== ISLAND LETTER SNIPPET ===")
    print(ISLE_LETTER_MODEL[3][:300])
    print("...")
    print()

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "island_flood_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)

    # Count pages via simple heuristic (ReportLab doesn't expose page count directly)
    page_count = pdf_bytes.count(b"/Type /Page\n") or pdf_bytes.count(b"/Type/Page")
    size_kb = len(pdf_bytes) // 1024

    print(f"DONE: island_flood.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Output: {out_path}")
    print()
    print("=== LETTER SNIPPET (first 200 chars of model) ===")
    print(ISLE_LETTER_MODEL[3][:200])
