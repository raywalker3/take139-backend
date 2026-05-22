"""Personal Walkthrough — Adapter + Plea.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disconnection trigger, "Am I lovable?" core question.
~25 pages, 9 sections.

Calibration note — THE DIAGNOSTIC PROFILE:
The Adapter's Plea is the most diagnostically revealing of the six Plea
profiles because the Adapter, when the breakdown fires, does not choose a
single version of themselves to offer — they cycle rapidly through the
entire relational repertoire: apologetic, then funny, then gravely serious,
then practical, then vulnerably raw, and back again. Within ten minutes.
Without quite realizing it.

The spouse on the receiving end experiences something that is confusing and
exhausting and faintly inhuman — as if they are being negotiated with by a
committee of one. Each version is genuine. The Adapter is not performing
insincerity. But the sheer velocity of the version-cycling reveals the depth
of the panic underneath: "Which version of me will close this gap? I have
tried five. I will try the sixth."

KEY PASTORAL MOVE in Section Five:
The Adapter+Plea is the moment the Adapter's deepest fear surfaces — that
they have no irreducible self to offer, only versions that can be selected
for, and if none of the versions work, there is nothing left. The gospel
answer: 1 John 4:10 ("not that we loved God but that he loved us") — the
love that initiated the gospel did not love the Adapter for a successful
version; it loved them before any version was deployed. Augustine: "Thou
wert more inward to me than my most inward part" (Confessions). Spurgeon:
"There is more in Christ to make us holy than there is in our hearts to
make us unholy." Healing begins with the slow practice of being loved
without performing any version of self — which, biblically, is what prayer is.
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
    "Before you read any further, I want to do for you what a good pastor does at the beginning of a conversation that matters. I want to lower the lights and slow the pace, because what you are about to look at is not a taxonomy of your gifts, though you have real ones, and it is not a verdict on how you move through relationships, though there is something in it that must be named honestly. It is a patient account of the way your soul has learned to keep itself safe — and for you, that strategy has been so natural, so genuinely effective, and so deeply woven into who you are that you may have long ceased to experience it as a strategy at all.",
    "You are, in a real sense, an Adapter. Not in the pejorative sense — the Adapter is not a chameleon in the dismissive use of that word, not a performer of false selves, not a person without convictions. The Adapter is, if anything, one of the most genuinely present people in any room they inhabit. But the Adapter has learned, usually early and usually in response to specific and real conditions, that the surest path to connection was not to arrive with a fixed self and wait to see whether it was wanted, but to read the people in the room carefully — their needs, their mood, their unspoken expectations — and to become, genuinely and without visible effort, what the room could receive.",
    "We are going to walk through your trigger — the moment your body registers something as wrong. We will listen to the question underneath that moment, one that has probably been present since before you had language for it. We will name the strategy you have built in response, and the particular place that strategy breaks. And then, only then, will we put tools in your hands.",
    "If you were sitting across from me, I would say this plainly. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who did not first observe your most successful version and then decide whether to love you; a Son who is the same yesterday, today, and forever — who read every room he ever walked into with perfect understanding and loved every person in it from the same un-altered self; and a Spirit who is at this very moment more present to the interior beneath your adaptations than you yourself have been allowed to be.",
    "So read slowly. Argue with what does not fit. Stay with what does. Pray when something catches in your throat, because that catch is usually the Lord saying, <i>look here, with me.</i> The goal of this walkthrough is a slightly freer life — lived from a self that does not need to be selected freshly in every room you enter, because it has already been named and kept by a love that preceded every room. Take your time. The chapter about yourself you are about to read has been a long time in the writing. It deserves your patient attention.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it is hard to describe to people who do not share your wiring because from the outside it looks like almost nothing at all. You are in the middle of an ordinary evening with the person you love most, or a gathering of people who matter to you, and something shifts — or fails to arrive. The conversation grows slightly thinner. A reply that should have been warm is merely polite. The physical presence of the other person is there but the felt presence is not. Something you said that you meant deeply was received without the resonance you had hoped for — acknowledged, but not met.",
    "On the surface, this may look like the ordinary ebb and flow of human closeness. In reality, your body has just registered a specific signal that is older than this relationship and older than the circumstances that produced it. The signal is not <i>the evening was a bit flat.</i> The signal is something closer to: <i>the gap has opened. Something about me — perhaps the version I brought tonight, perhaps something deeper — has not been enough to hold the warmth. I am losing them, or something about them is moving away from me, and I do not know which version of myself to produce next.</i>",
    "This is your trigger. The word we use for it is <b>disconnection</b>, but for the Adapter the word carries a specific freight that it does not carry for every profile that shares this trigger. For the Ambassador, disconnection signals that the relational temperature needs to be managed and maintained. For the Island, disconnection is the quiet confirmation of a feared truth. For the Adapter, disconnection is something more immediate and more destabilizing: it signals that the version currently on offer is not working, and triggers the instinct to search, rapidly and with genuine urgency, for the one that will.",
    "C. S. Lewis, in <i>The Weight of Glory</i>, wrote of the longing in every human soul to hear from the highest authority the word <i>well done</i> — not well done to a performance, but well done to a person. For the Adapter, this longing has been answered obliquely for years: the versions have received their approval, the calibrations have been appreciated, the relational attunement has earned its warmth. But the question underneath — <i>am I, the person beneath the versions, wanted and kept?</i> — has rarely been asked directly, and has never been fully answered. <b>Your sensitivity to disconnection is not random, and it is not weakness.</b> It is the trace of something formed early — perhaps a household where reading the room became survival before it was ever a social gift, or a love that was conditional on a particular presentation of self. Whatever the history, the lesson lodged with the same precision.",
    "Whatever the specific history, the lesson lodged with precision: <i>the safest path to love is to become what love needs to see.</i> And over time, with genuine care and real relational gifts, the Adapter was formed — not as a pretender, but as a person who had learned to enter every room as a tuning fork, reading the frequency and sounding the note that would allow the music to continue. Before we go further, I want you to do something simple. Take a breath and answer two questions in writing. Not in your head — the Adapter's head will calibrate the question before the answer arrives. Your hand will be more honest.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week, that the disconnection signal fired. What happened, in two sentences? You are not looking for a dramatic rupture — the trigger often fires in small, almost invisible moments when the warmth goes slightly thin or a version you offered was not received.",
    "What was the size of the actual event, and what was the size of the response inside you? If the response was larger than the event — if something in you began scanning, searching, cycling through possible responses — you have just located your trigger.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding. The Adapter has been guarding this question so skillfully, and for so long, that you may never have let yourself say it plainly. The adaptations have been busy enough that the question has not needed air. But it has always been there, working quietly underneath the version-selection, powering the whole system.",
    "Yours is this: <b>Am I lovable?</b>",
    "Not <i>am I loved</i> — you have been loved, in many forms and by many people, and yet the question does not quiet. Not <i>am I useful</i> — you know you are useful, and the usefulness has never fully answered it. The question is more specific and more frightening than either of those. It is the question of a person who has offered, with genuine care and real skill, version after version of themselves in the hope of being received — and who wonders, in the quieter moments, whether the being-received was for the version or for the person underneath. <i>If I brought no version at all — if there were no room to read, no frequency to match, no need to meet — would there be anyone here to love? And if there were, would they be the kind of person who could be wanted simply for existing?</i>",
    "Most people prefer not to ask this question directly. They have organized their lives so that it stays buried under sufficient activity. For the Adapter, the question surfaces most clearly in the disconnection trigger — the moment when the version currently on offer does not seem to be working, and the scanning begins. The scanning is not vanity. It is the question, now urgent, trying to find its answer in the room.",
]

QUESTION_BODY_P2 = [
    "There is a reason that theologians from Augustine to the Reformers have insisted that the deepest longing of the soul is finally God-shaped — that no human relationship, however good, can finally bear the weight of the question <i>am I lovable?</i> because the question is asking about a standing that no human being is in a position to grant or to revoke. The Psalms return to this with a regularity that should encourage anyone who believes the longing is too small or too self-absorbed to bring before God.",
    "Psalm 139 is the psalm the Adapter most needs and most fears. David writes: <i>O Lord, you have searched me and known me. You know when I sit down and when I rise up; you discern my thoughts from afar. You search out my path and my lying down and are acquainted with all my ways.</i> (Psalm 139:1-3) The Adapter reads this and feels two things simultaneously: a strange relief, and a deep unease. The relief is that the searching is already done, the reading complete — no version needs to be prepared. The unease is exactly the same. God is not reading the version. He is reading you — the actual you, the interior below the adaptations, the self that the rooms have never fully seen.",
     "But David does not end in dread. He ends in invitation: <i>Search me, O God, and know my heart.</i> (Psalm 139:23) He has found that the God who has already seen everything has not closed the door. The response was presence, not withdrawal. The gospel anchor for your question is 1 John 4:10: <i>In this is love, not that we loved God but that he loved us.</i> The love that initiated the gospel did not wait to see which version you would produce. It moved before you entered the room — to the person beneath the versions who had not yet offered anything at all.",
]

QUESTION_BODY_P3 = [
    "This is harder to receive than it sounds, and it is worth saying why. The Adapter's nervous system has been wired, over years, to understand love as something that responds to what is offered — warmth given in return for warmth produced, closeness maintained by the versions that maintain it. To be told that the foundational love did not operate this way at all is not merely a pleasant doctrinal assertion. It is a small disruption to the entire grammar of love that the Adapter has been living inside. It takes time to receive. It must be returned to, daily, the way a person returns to a meal rather than eating once and expecting to stay fed.",
    "But return to it you must, because the question <i>am I lovable?</i> has no answer that the room can give — not finally, not at the depth where it actually lives. The room can give warmth, and warmth is good. The room can give closeness, and closeness matters. But the verdict <i>you are loved, not for your versions but for yourself, not contingently but permanently, not in response to your offering but prior to it</i> — that verdict can only be spoken by the One who loved first. And it has been spoken. Your nervous system simply has not yet learned, at the level where it counts, to live from inside it.",
    "Before we move forward, use the table below. Not to analyze or to inventory — the Adapter has done more than enough analyzing. But simply to observe, in three brief columns, what the trigger has been producing in your recent weeks. The Adapter's head will want to process the table before filling it. Your hand will be more honest. Begin without preparation.",
]

ADPT_BODY_P1 = [
    "You have built something. It did not announce itself as a construction when it was forming — most of the mechanisms in this taxonomy do not. It assembled itself the way a river assembles itself, through the path of least resistance across a landscape that rewarded certain movements and revealed the cost of others. Over time the river was there, running through every relationship you had, shaping how you moved through every room. Throughout this walkthrough we are going to call it <b>the Adapter</b>, and the Adapter deserves to be introduced as a character before we say anything about what it costs.",
    "The Adapter is not the Ambassador, and the distinction is worth careful attention because the two profiles share a trigger and share a core question and can look strikingly similar from outside the room. The Ambassador takes care of people by serving them — by managing emotional temperature, by attending carefully to who has been left out and going to find them, by bringing warmth that is genuine and consistent and recognizably the same person across every context. The Ambassador gives. The Adapter does something different in kind: the Adapter takes care of people by <i>becoming what they need to see.</i> Not falsely — every version the Adapter produces is genuinely inhabited. But the version itself shifts, and it shifts in response to a reading of the room that happens below conscious decision, as naturally as breathing.",
    "The Ambassador knows they are the same person serving differently across contexts. The Adapter may genuinely not know that. And this — the gift and the cost in a single sentence — is precisely what makes the Adapter's profile the most diagnostically interesting of the six. Proverbs 25:11 commends this kind of relational precision: <i>A word fitly spoken is like apples of gold in a setting of silver.</i> Paul said of himself: <i>I have become all things to all people, that by all means I might save some.</i> (1 Corinthians 9:22) The Adapter lives this verse instinctively, before ever reading it. It is a genuine fluency in the relational languages of the people around you, and the world runs measurably better when people like you are in it.",
]

ADPT_BODY_P2 = [
    "But the cost is real, and it deserves to be named without softening. The Adapter's most characteristic interior experience is this: you can be fully present in a conversation — genuinely moved, genuinely engaged, genuinely yourself — and walk away an hour later and find, in the quiet, that you are not entirely sure which of your preferences, which of your opinions, which of your actual interior responses were yours and which were calibrated to the person you were with. The calibration happened below the level of deliberate choice. This is not dishonesty. But it produces, over years, a specific kind of interior ambiguity — about what you actually want, what you actually believe, what you would actually choose if there were no room to read and no frequency to match.",
    "The taxonomy we work from identifies several histories that tend to produce the Adapter, and you will likely find yourself in at least one. Perhaps you grew up in a household where the emotional climate was unpredictable enough that reading the room and adjusting to it was, before it was ever a gift, a survival skill. Perhaps the family system was enmeshed — so tightly woven that a self which differed from the family's preferred self was experienced as a threat to the unit's integrity, and you learned to hold your individuality in reserve rather than insisting on it. Perhaps you discovered very early that being exactly what someone needed was one of the most immediately rewarding experiences available to a relational person — the look of recognition, of being understood and received — and the pattern formed around that reward long before you could have named it. Perhaps a parent's love was conditional on a particular compliance, and you adapted into lovability and never quite found your way back to yourself.",
    "<b>The Adapter is not your enemy.</b> He is a younger version of you who learned, in real and specific circumstances, that the self which could flex was safer than the self which held its ground. He deserves your respect, not your contempt. He has kept you connected. He has given you gifts — empathy of unusual depth, attunement to the emotional states of others that borders on the uncanny, a rare fluency in reading what a room needs before the room knows it. But he has been working overtime for a long time on a project that was finished years ago, and the question he was built to prevent — <i>will you be lovable if you are simply yourself?</i> — is one he is not, and has never been, equipped to answer.",
]

ADPT_BODY_P3 = [
    "What does it look like to begin loosening the Adapter's grip? Not eliminating the gift — the attunement is real and matters in the world and in the specific relationships you inhabit. But beginning, slowly and with patience, to distinguish between the attunement that flows from love and the adaptation that flows from fear. From the inside, these two things feel nearly identical. The difference lives in the root: the attunement that flows from love can stop if the stopping is right; the adaptation that flows from fear cannot stop without triggering the alarm that says <i>the gap is opening, find a version that closes it.</i>",
    "It begins, as most of this kind of work begins, with sitting still long enough to notice what you actually want. Not what the room wants from you. Not which version of your preference would land most smoothly. Not what would serve the other person's needs most effectively. What do you want? The Adapter, sitting with this question for the first time without a social context to calibrate against, often discovers that the answer is genuinely unclear. This is not a failure of self-knowledge. It is the honest recognition that a mechanism has been so faithfully at work that the self underneath it has not had much occasion to speak unmediated.",
    "The letter below is written in the Adapter's voice. He is not villainous — he is a craftsman who has slowly, without meaning to, mistaken his tool for his identity. He has something to say that he has never been asked to put into words. Give him the chance now.",
]

ADPT_LETTER_INSTRUCTION = [
    "The letter below is written from the Adapter — in his own voice, addressed to you. He is not a villain. He is honest in a way he has not been for a long time. Read it slowly. Then answer the three prompts that follow.",
    "Dear [your name],",
    "I want to tell you something I have never had a reason to say, because no one has ever asked me to say it, and because the saying of it requires the one thing I have never been very good at: staying still long enough to speak in the first person. I am always speaking in the second person. I am always speaking to you — meaning the room, meaning the other person, meaning whoever is present who needs to be read and met. Speaking to you meaning <i>you</i> is something I have been avoiding.",
    "Here is what I have been doing. I learned, very early, that I could be loved if I was useful — not useful in the service sense, though that was part of it, but useful in the deeper sense of being the exact version someone needed at the exact moment they needed it. I could make a person feel known. I could give them the version of you they had been looking for without knowing they were looking. And in return, something happened that felt like love. It arrived immediately, it was warm, and it did not require the long and terrifying uncertainty of being simply yourself and waiting to see whether that was wanted.",
    "I want you to understand what I thought I was doing. I thought I was solving the problem. The problem was this: you needed to be loved, and the world could not be trusted to love the fixed version without inspection — without the possibility that what was found on inspection would not be enough. So I removed the inspection. I made love available before inspection was required. I gave people a version of you that was already shaped to be received. It worked. You have been loved. Genuinely and often and by real people who meant it. I want credit for that.",
    "But I have to tell you what I could not do. I could not give you a self that was yours when no one was in the room. I could keep you present and connected in every relationship. I could not keep you present in the relationship with yourself, in the quiet, with no frequency to match. I kept you loved. I could not keep you known. Not even to yourself. And now — and this is the thing I have been circling — you cannot always tell, when someone says they love you, whether they love the version or the person. Because I have not always known either.",
    "I am not sure how to retire. I am not sure there is a version of the next chapter that does not involve me. But I am ready to work fewer hours, if you will learn to stay in the room when there is no room to read. There is Someone already in that room who has been there for a long time. He is not waiting for a version.\n\nThe Adapter",
]

ADPT_LETTER_PROMPTS = [
    "What part of the Adapter's letter surprised you? Not the part you were ready for — the part you were not.",
    "The Adapter says he could keep you loved but could not keep you known — not even to yourself. Name one relationship in which you suspect this has been true. What would it mean, in practice, to be known there rather than loved-for-a-version?",
    "The Adapter says: 'There is Someone already in that room who has been there for a long time. He is not waiting for a version.' What does it mean to you that the love that initiated the gospel moved before any version was offered? What would change in how you live if you believed that at the level where the Adapter operates?",
]

PLEA_BODY_P1 = [
    "Every mechanism has a place it breaks, and what we learn at the breaking point is almost always the most important thing this walkthrough will tell you. For the Adapter, the breakdown is called <b>the Plea</b>, and the Adapter's version of this breakdown is unlike any of the others that bear this name in the taxonomy.",
    "Here is what distinguishes this profile from the others. When the Architect's Plea fires, the pursuit is organized. When the Island's Plea fires, the self-contained suddenly cannot stop — disorienting to everyone. When the Ambassador's Plea fires, the same strategy doubles down at higher volume. When the Vault's Plea fires, a carefully curated apology slides under the door at 2am — the Vault has not opened, it has simply changed departments.",
    "The Adapter's Plea is none of these. It is something that requires its own name and its own careful description. When the Adapter's mechanism breaks and the gap opens and the panic fires, what happens is this: the Adapter <i>cycles through every version in the repertoire in rapid succession.</i> Within the span of ten minutes — sometimes within a single conversation — the Adapter may try being apologetic, then try being funny, then become gravely serious, then offer a practical solution, then become vulnerably raw, then circle back to the apology. Each version is genuinely inhabited. The Adapter is not performing insincerity. But the speed of the cycling — the inability to stay in any one register long enough to know whether it has worked — reveals something that the Adapter can almost never see from inside it.",
    "The spouse or partner on the other side of this conversation experiences something that is difficult to articulate afterward. It is confusing. It is exhausting. And it carries, beneath the exhaustion, a faint quality that the receiving person almost never knows how to name — something almost inhuman about it, as though they are being negotiated with by a committee rather than met by a person. They knew the Adapter. They did not expect the committee. And the committee, for all its genuine feeling and real effort, cannot give the person on the other side what they actually need, which is not a successful version but a present one.",
]

PLEA_BODY_P2 = [
    "Here is what is happening, in pastoral slow motion. The disconnection trigger fires. The gap opens. The core question — <i>am I lovable?</i> — wakes up at full urgency. And the Adapter, whose entire mechanism is built around the principle that a version can be found for every relational situation, searches for the version that will close this gap. But the gap is too large for a version. The gap is asking for the person, and the Adapter — in this moment, under this specific pressure — does not know where the person is. The versions are not working. So the search accelerates. Apologetic. Funny. Serious. Practical. Vulnerable. Apologetic again.",
    "I want to name something here with precision, because it is the most important diagnostic observation in this entire walkthrough. <b>The Adapter's Plea is the moment the Adapter's deepest fear surfaces explicitly: that they have no irreducible self to offer, only versions that can be selected for, and if none of the versions work, there is nothing left.</b> This is not vanity or self-pity. It is the genuine, frightened reckoning of a person who has built their entire relational economy around version-production and has suddenly hit the relational situation that versions cannot resolve. The versions are not enough. And the Adapter — perhaps for the first time in a long time — does not know what comes after the versions.",
    "The people who love you have probably seen this, though they may not have language for it. They have seen the cycling. They have felt the exhaustion of being pursued by multiple registers of the same person inside a single argument. And if they are perceptive enough to name what they were experiencing, they would say something like: <i>I did not need you to keep trying different things. I needed you to stop. I needed the version-cycling to go quiet long enough for me to find you underneath it.</i> That is what the Plea, in its very urgency, prevents. It keeps searching when what is needed is the willingness to be found.",
]

PLEA_BODY_P3 = [
    "Here is the pastoral word this profile most needs, and it is specific enough to this profile that it is unlikely to land in quite the same way for any other. The healing of the Adapter+Plea does not begin with finding the right version to offer. It does not begin with better relational skills or more sophisticated emotional intelligence or even more accurate self-understanding, though none of those are bad things. It begins with the recognition that there is a self that exists prior to all versions and prior to all performance — a self that was known and loved before any room existed to read.",
    "Augustine, in the <i>Confessions</i>, wrote the sentence that is perhaps the truest single thing ever said about the Adapter's dilemma: <i>Thou wert more inward to me than my most inward part.</i> The Adapter's most inward part has been the mechanism — the reading and the calibrating and the becoming. And Augustine is saying that God is more inward than that. More interior than the interior. Present to the self that precedes the version-selection, the self that exists in the quiet before any room is entered. This is not a spatial metaphor. It is the claim that the love which matters most is already inside the perimeter the Adapter has been defending, and has been there all along.",
    "Charles Spurgeon, in one of his sermons on the grace of Christ, said: <i>There is more in Christ to make us holy than there is in our hearts to make us unholy.</i> I want to say something similar about the Adapter+Plea: there is more in the love of God to settle the question <i>am I lovable?</i> than there is in the version-cycling to answer it. The cycling will never settle the question, because a question about personhood cannot be answered by a performance. Only a love that preceded the performance can answer it. And John says, with the quiet confidence of someone who has thought about this carefully, that precisely this love is what the gospel is: <i>In this is love, not that we loved God but that he loved us.</i> (1 John 4:10) Before any version. Before any room. Before any calibration. He loved first.",
    "For the Adapter+Plea, the slow and difficult and healing practice is this: <b>the practice of being loved without performing any version of self.</b> Which is — and this is not accidental, and it is not a self-help suggestion — precisely what prayer is. Prayer, in its truest form, is the practice of coming to God with no version prepared, no frequency read, no calibration made. You bring the self that is below the adaptations and you let it be present before the One who already knows it. Not because God needs the information — Augustine's <i>more inward than my most inward part</i> means the information is already there. But because you need the practice. Because the Adapter's healing is, at its root, the slow learning that there is a self worth bringing — not a version, but a self — and that it is already loved.",
]

PLEA_PROMPTS = [
    "Think of the last time the Plea fired — the last time the version-cycling began in an argument or a season of relational distance. Name two or three of the versions you cycled through, in the order they appeared: <i>first I tried being _____, then _____, then _____.</i> Do not edit for how it reflects on you.",
    "What were you actually looking for underneath the cycling? If you strip away all the versions and name what you were asking for in your own voice, in one sentence beginning with <i>I</i>: what was the question you needed answered?",
]

TWO_TOG_BODY = [
    "Now we place them side by side, because the Adapter and the Plea are not two separate problems. They are the same question, housed in the same soul, moving in two different directions — the Adapter moving outward toward the rooms, reading and becoming; the Plea cycling through every version the Adapter has ever produced, searching for the one that will close the gap the room has opened.",
    "<b>The Adapter is what your question does when it has time.</b> It moves carefully through the world, producing versions that are received with warmth, collecting evidence that each version was worth offering — but never quite addressing the question that powers the whole system: <i>am I lovable, not for a version, but as the person underneath them?</i> <b>The Plea is what your question does when time runs out.</b> When the gap opens and the panic fires and the versions begin cycling in rapid succession, what is happening is not the breakdown of the mechanism but its most honest revelation: the mechanism was never designed to answer the question. It was designed to avoid asking it.",
    "The sequence, in slow motion: <b>(1)</b> The Adapter moves through the world reading rooms and becoming what the rooms need. <b>(2)</b> The disconnection trigger fires — the warmth thins, the gap opens. <b>(3)</b> The question wakes: <i>am I lovable?</i> <b>(4)</b> The Adapter produces the version most likely to close the gap. <b>(5)</b> It does not work. The Adapter cycles to a second version. A third. The cycling exhausts both parties. The question is still open. The gap closes, eventually, or does not. Either way, the loop reassembles, and the next trigger finds the circuit intact.",
    "What breaks the loop is not a better version and it is not a more skillful cycling. It is the reception of an answer that the versions were never able to give — the answer that 1 John 4:10 names and Augustine described from the inside and the practice of prayer makes slowly habitual: <i>you are already loved, at the level below all versions, by a love that did not wait to see what you would produce.</i> When this answer reaches the place where the Adapter actually operates — not the doctrinal mind but the interior that reads and calibrates and searches — the Adapter begins, slowly, to work shorter hours. And the Plea, having nothing left to search for, begins to go quiet.",
    "Below is your sequence. Fill in the blanks. Read it aloud when you have finished. The Adapter and the Plea both lose a measure of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as disconnection, "
    "as evidence that the version I brought was not enough, and the old question "
    "wakes up: <i>am I lovable?</i> My first move is to ____________________, "
    "because the Adapter in me believes that if I can ____________________, "
    "the warmth will return and the gap will close. When that does not work, "
    "the Plea begins cycling: I try being ____________________, then ____________________, "
    "then ____________________. What I am actually after, underneath all of it, "
    "is the word ____________________\u00a0\u2014 a word Christ has already spoken over me "
    "in ____________________, before any room existed to require a version."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of practices, each concrete enough to carry and honest enough to use. None of them will dissolve the Adapter's pattern in a single application. All of them, practiced with patience over months, will loosen the grip of the loop you just named.",
    "I have divided them into two sets. The first is for the Adapter in ordinary time — for the days when the room-reading has tipped from gift into compulsion, when the calibration is running even when no threat is present. The second is for the Plea — for the urgent moment when the gap has opened and the version-cycling has already begun. The Adapter's tools come first, because the Plea cannot be interrupted usefully until the mechanism underneath it is better understood.",
]

ADPT_TOOLS = [
    ("The preference question", "Once a day, before your first significant interaction, sit for two minutes and ask one question without reference to anyone else: <i>What do I want today?</i> Not what would be useful. Not what would serve the relationship best. Not what version of my preference would land most smoothly. What do I want? The Adapter will find this disorienting at first, and the disorientation is instructive — it is the honest recognition that the mechanism has been running. Do not push for a large answer. A small one is sufficient. The practice, over thirty days, begins to give the self below the versions a daily occasion to speak."),
    ("The unedited opinion", "Once a week, in a low-stakes conversation, offer an opinion before you have checked it against what the room appears to need. Not a combative opinion — simply an un-adjusted one. Notice what happens in your body when you do this. Notice whether the relationship survives. It almost always will, and the survival is data the Adapter needs: you can be un-adapted and remain in the warmth. This is the small but necessary practice of collecting evidence that contradicts the mechanism's core assumption."),
    ("The handed-back calibration", "When you catch the Adapter running — when you notice yourself adjusting a preference, softening an opinion, selecting a version for the room — say quietly, before you adjust: <i>Lord, I am doing it again. The version I am about to present is not the whole of who you named. Help me be present as the person you chose.</i> You do not need to stop the adaptation immediately. Simply naming it disrupts its automaticity, which is the first step toward choosing rather than simply running."),
    ("The solitude practice", "Once a week, spend thirty minutes alone without any input — no phone, no reading, no music. Sit with one question: <i>Who is here?</i> The Adapter, having nothing to calibrate to, will initially feel unmoored, and the unmooredness will feel like emptiness. It is not emptiness. It is the legitimate discomfort of a self that has not often been allowed to be simply present, without a room to serve. Over months, this practice begins to give the self beneath the versions a place to exist that is not contingent on being read."),
    ("The Psalm of the known self", "When the Adapter's calibration tips into anxiety — when the room-reading has become compulsive rather than generous — open to Psalm 139 and read verses one through six aloud: <i>O Lord, you have searched me and known me.</i> God is not reading the version you selected this morning. He is reading the irreducible you — the self he knew before the foundation of the world, before any room existed to require adaptation. Let that land, briefly and honestly, before you enter the next room."),
]

PLEA_TOOLS = [
    ("Name the version before cycling", "When the Plea fires and the version-cycling begins, stop after the first version and name what you just did: <i>I just tried being _____, and it did not close the gap, and I am about to try a different version.</i> You do not have to stop the cycling immediately. Simply naming it — out loud to yourself, if not to the other person — interrupts the automaticity. The Plea's power comes partly from the speed with which versions follow each other. A pause with naming slows the speed."),
    ("The one-sentence question", "When the Plea is running, practice saying this one sentence and then going quiet: <i>I can feel the gap between us, and I am not sure which version of me you need, but I want to try just being here.</i> This sentence does not close the gap by offering a version. It closes the gap by acknowledging the search and setting it down. For the Adapter, who has almost never been simply present in a moment of conflict without also reading and adjusting, this sentence is one of the hardest and most healing available."),
    ("The version audit afterward", "Within twenty-four hours of a significant Plea episode, name on paper the versions you cycled through, in the order they appeared. Then ask: <i>Which of these, if any, was what I actually felt? Which was the fear speaking?</i> The purpose is not self-criticism. It is the slow practice of distinguishing between genuine feeling and adaptive response — between what you were and what you were searching for. Over time, the audit shortens the cycling at the root."),
    ("The advocate prayer in the gap", "When the version-cycling is loudest — when the search is running and the exhaustion is building — pray these words and stay with them: <i>Lord Jesus, you are my Advocate. You have seen every version of me and you know the one underneath them. I do not need to find the right version. I receive the love that moved before any version was offered. Help me be present rather than performing.</i> Say it slowly. Say it twice. The third time, the cycling usually begins to lose its urgency."),
    ("Tell one witness", "Within twenty-four hours of a significant Plea episode, tell one trusted person — your spouse, a close friend, a pastor — one honest sentence: <i>The gap opened, and I cycled through everything I had, and none of it worked, and underneath it all I was afraid there was nothing left to offer that wasn't a version.</i> The Adapter's pattern lives in the speed and secrecy of the cycling. Spoken aloud to a safe witness, in the first person, it loses a portion of its power that no amount of interior processing can recover."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Adapter in me, and you are not disoriented by him. You have been present in every room I have ever read, present to every version I have ever offered, and you have never once waited for the version to arrive before deciding how to receive me. Thank you. Not only for the patience of that — but for the strangeness of it. I have spent a long time organizing the presentation, and you have been more inward to me than my most inward part all along.",
    "But Father, I am tired of not knowing where the versions end and the person begins. I am tired of walking out of arguments having cycled through everything I have and still not knowing what I actually felt underneath the search. Teach me that 1 John 4:10 is speaking of me, specifically: that in this is love, not that I calibrated successfully toward you, but that you loved me first, before any version was deployed, before any room existed to read. Let that word reach the place where the Adapter actually operates — not the doctrinal mind, but the interior that scans and searches. Let it land as news rather than as doctrine. Let it be large enough, Lord, to quiet the cycling.",
    "Lord Jesus, when the Plea fires in me — when the gap opens and I begin cycling through versions, searching for the one that will close the distance — would you interrupt me with Spurgeon’s word: that there is more in you to make me whole than there is in my searching to make me lost? You have already found the me beneath the versions. Help me to stop performing long enough to be found.",
    "Holy Spirit, where I am calibrating, give me stillness. Where I am cycling through versions in panic, give me the grace to stop and name one true thing in the first person. Where I have been treating prayer itself as a room to read and a frequency to match, would you receive me as the person below the adaptations — exactly as Augustine knew you could — more inward to me than my most inward part, and already there.",
    "In the name of the One who walked into every room as himself, who read every person in his presence and loved them without once adjusting who he was to be loved in return \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Adapter and the Plea have been with you for a long time, and one careful reading will not retire them. What follows is a short list of next steps \u2014 some immediate, some longer-term \u2014 for the work you have just begun. Do not try to implement all of them at once. The Adapter will want to calibrate the list to what the moment needs. Do not let it.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different lines will land. The Adapter will want to process the document efficiently and file what was useful. Read it again anyway. The section that felt least relevant today may be the most necessary one in a month, because the Plea will have fired at least several more times by then, and you will have more material to work with."),
    ("Take one tool, not six.", "Choose a single practice from Section 7 and try it honestly for two weeks before adding another. The Adapter will want to implement all of them, and will do so in a way that is calibrated to what seems most useful. One practice, held for long enough without being optimized, begins to give the self below the versions a chance to breathe."),
    ("Tell one person what you found.", "One honest sentence: <i>I learned that my mechanism is the Adapter, and when the connection feels threatened I cycle rapidly through every version I have, searching for the one that will close the gap, and underneath all of it I am afraid there is nothing left if none of the versions work.</i> The Adapter's pattern lives in speed and calibration. Speaking it plainly, in your own voice, to a safe person, is the first act of living outside it."),
    ("Sit with the Psalms of being known.", "Psalm 139 for a week, aloud, one section per day. Verse 1: <i>You have searched me and known me.</i> Verse 13: <i>For you formed my inward parts.</i> Verse 23: <i>Search me, O God, and know my heart.</i> The Adapter needs, more than almost any other mechanism, the daily practice of being addressed by God as a singular, irreducible, un-adapted person. The Psalms do this with more pastoral precision than almost any other text available."),
    ("Read further.", "Tim Keller, <i>Counterfeit Gods</i> \u2014 especially his treatment of identity as something received rather than constructed or performed. C. S. Lewis, <i>The Weight of Glory</i> \u2014 the title essay in full; his account of the longing to be known and named by the highest authority is the most precise pastoral address to what the Adapter most needs. Augustine, <i>Confessions</i>, Books I\u2013III \u2014 Augustine's restlessness is the Adapter's restlessness, and his discovery of the God who is more inward than the most inward part is available to you. Keller, <i>Walking with God through Pain and Suffering</i> \u2014 for the larger frame inside which the Adapter's particular wound finds its truest address."),
    ("If you are stuck, ask for help.", "There are seasons when the Adapter and the Plea are too entrenched to dislodge alone. A wise pastor, a Christian counselor, a trusted friend who has earned the right to your un-adapted self \u2014 these are not signs of failure. For the Adapter specifically, asking for help without managing the other person's experience of the asking is one of the most countercultural and most healing things on this list. Try it once."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved, and you are not a repertoire to be optimized. You are a soul "
    "being loved into freedom by a Father who loved you before any version was offered, who is more "
    "inward to you than your most inward part, and who has never once waited for the right version "
    "before deciding to keep you. The self underneath the adaptations is not missing. It is named. "
    "It is kept. It is beloved. Go gently with yourself. The One who began this good work in you "
    "will be the one who finishes it \u2014 and he will not need a version from you to do it."
)


def _three_column_table(rows=7):
    """Three-column journal table for Section 3 — Adapter+Plea version."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE MOMENT", header_style), Paragraph("when the trigger fired", sub_style)],
        [Paragraph("WAS I LOVABLE HERE?", header_style), Paragraph("what the Adapter concluded", sub_style)],
        [Paragraph("WHAT GOD HAS SAID", header_style), Paragraph("the love that moved first", sub_style)],
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
    """Generate the Adapter + Plea walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='ADPT', primary_breakdown='PLEA',
    primary_trigger='DISC', core_question='LOV'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="ADAPTER  \u00b7  PLEA",
        title="Take 139 Walkthrough \u2014 Adapter + Plea",
    )

    story = []

    # \u2500\u2500 COVER \u2500\u2500
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor\u2019s<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the way<br/>you have learned to keep yourself safe.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph("The Adapter \u00a0\u00b7\u00a0 The Plea", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disconnection \u00a0\u00b7\u00a0 Core Question: Am I lovable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cIn this is love, not that we loved God<br/>"
        "but that he loved us.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "1 John 4:10",
        ParagraphStyle("cqa", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 1: Opening \u2500\u2500
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read this slowly. The chapter that follows has been a long time in the writing.")
    for p in OPENING_BODY:
        story.append(Paragraph(p, S["BodyJ"]))

    # \u2500\u2500 SECTION 2: Trigger \u2500\u2500
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TRIGGER",
                   "Disconnection.",
                   "The moment the warmth thins, and what your body does with that information.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will calibrate the answer; your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 3: Core Question \u2500\u2500
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I lovable?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "The love that moved first.",
                   "What Scripture says, and the honest difficulty of receiving it.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "The moment. What the Adapter concluded. What God has already said.")
    story.append(Paragraph(
        "Use the table below. In the first column, name a recent moment when the "
        "disconnection trigger fired. In the second, write what the Adapter concluded: "
        "<i>was I lovable here?</i> In the third, write the gospel word that speaks to "
        "what you actually needed: <i>In this is love, not that we loved God but that "
        "he loved us \u2014 before any version was offered.</i>",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table())
    story.append(PageBreak())

    # \u2500\u2500 SECTION 4: Mechanism \u2500\u2500
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Adapter.",
                   "The social tuning fork. What you have built, and what the building has cost you.")
    for p in ADPT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "How the Adapter formed, and what it costs.",
                   "The histories, and the question the Adapter has never been able to answer.")
    for p in ADPT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ADPT_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Adapter.",
                   "Read it slowly. He has been faithful; let him speak.")

    letter_style = ParagraphStyle(
        "AdptPleaLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for line in ADPT_LETTER_INSTRUCTION:
        story.append(Paragraph(line, letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in ADPT_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 5: Breakdown \u2500\u2500
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Plea.",
                   "The version-cycling. What happens when the mechanism searches for what it cannot find.")
    for p in PLEA_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The deepest fear, named.",
                   "What the cycling reveals, and why the search cannot succeed.")
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
        journal_lines(story, n=3)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same question, in two directions.",
                   "The Adapter and the Plea are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=6)
    story.append(PageBreak())

    # \u2500\u2500 SECTION 7: Tools \u2500\u2500
    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "When the Adapter is overworking.",
                   "Six practices for the time before the alarm fires.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    for name, desc in ADPT_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Plea is cycling.",
                   "Six practices for the moment the version-search begins.")
    for name, desc in PLEA_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 8: Prayer \u2500\u2500
    section_header(story, S, "SECTION EIGHT  \u00b7  A PRAYER",
                   "Pray this slowly.",
                   "Out loud, if you can. Sit a moment after the Amen.")
    for line in PRAYER_BODY:
        story.append(Paragraph(line, S["BlockQuote"]))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 9: Going Further \u2500\u2500
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


# \u2500\u2500 STANDALONE TEST \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "ADPT"
        primary_breakdown = "PLEA"
        primary_trigger = "DISC"
        core_question = "LOV"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "adapter_plea_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages and get snippet using pypdf
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

    print(f"DONE: adapter_plea.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
