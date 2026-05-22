"""Personal Walkthrough — Vault + Plea.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Shame trigger, "Am I acceptable?" core question.
~25 pages, 9 sections.

Calibration note — THE PARADOXICAL PROFILE:
The Vault is the mechanism that withholds — that presents only finished,
curated versions of the self. The Plea is the breakdown that panic-pursues
when a gap appears. Together they produce a specific and recognizable person:
one who, when the connection threatens to break, does not suddenly become
transparent. Instead they become curated in a different genre. The handwritten
letter slid under the door at 2am. The multi-paragraph text apology with
enumerated points. The careful recitation of everything that went wrong and
everything they are willing to concede — organized, edited, sent.

The Vault+Plea has not opened. It has changed departments.

Key theological move in Section Five: the Plea has not broken the Vault
open — it has merely shifted the Vault's curation from "finished conclusion"
to "finished apology." The remedy is not a better apology. It is messy,
real presence. The Prodigal's father (Luke 15) — he ran while the son was
"still a long way off," before any speech was delivered. Spurgeon: "God runs
to meet the half-hearted prayer of the truly broken; he hears the polished
prayer of the still-hidden heart." 2 Corinthians 7:10 — godly grief produces
repentance without regret; worldly grief produces death.
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
    "Before you read any further, I want to do for you what a good counselor does at the opening of a difficult conversation. I want to lower the lights and slow the pace, because what you are about to look at is not a personality profile. It is something more specific and, I suspect, more unsettling: a careful account of the way your soul has learned to manage the fear of being seen without preparation, and what happens, at a precise pressure point, when that management is not enough.",
    "You are, in some deep sense, a Vault. Not because you are empty inside \u2014 the Vault is, if anything, richly furnished. Not because you are cold or uninterested in closeness \u2014 Vaults often long for intimacy more quietly and more consistently than almost anyone in the room. But because something specific and early in your experience taught you that the interior world is best presented in its finished form. That what is shown must be chosen and prepared. That the half-built house, the unresolved question, the grief still wet \u2014 these belong to you alone, until they are ready to be shared.",
    "There is a second thing I need to name, and it may be the reason this document landed in your hands. The strategy that keeps you private in the ordinary hours does not always hold. There are moments \u2014 usually when a relationship you cannot afford to lose seems to be in genuine danger \u2014 when something breaks through. Not in the way you would expect a breakthrough to look. Not with raw tears and unguarded words. But with something you have carefully written. A long message. A letter. A precise recounting of everything that has gone wrong and everything you are prepared to do. A curated apology, organized and delivered, in the unmistakable voice of someone who has been preparing it for longer than they are letting on.",
    "We are going to walk through your trigger, the question underneath it, the strategy you built, and the specific form that strategy takes when it breaks. And then, only then, will we put tools in your hands.",
    "If you were sitting across from me, I would say this. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who does not require you to curate your interior before he will receive it; a Son who was publicly and completely exposed so that your exposure might be permanently covered; and a Spirit who is, at this very moment, fully present to the parts of you that have never been shown to anyone \u2014 and is not waiting for a finished draft.",
    "So read slowly. Argue with what does not fit. Stay with what does. Pray when something catches in your throat, because that catch is usually the Lord saying, <i>look here, with me.</i> The goal is a slightly freer life \u2014 lived before a God who has already seen everything in the vault and has not once closed the door.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life never see it occur. It does not announce itself. You are in the middle of an ordinary conversation, or a meeting, or an evening at home, and something shifts \u2014 a question that goes one degree deeper than you had prepared for, an observation about you that is accurate enough to feel like a violation, a moment when someone glimpses something you had not selected for display. Maybe they comment on it. Maybe they mention it to someone else. Maybe they simply look at you with the particular expression that says: <i>I see something you didn\u2019t intend to show.</i>",
    "From the outside, this may look like a passing social discomfort. For you it registers as something else entirely. What moves through your chest in that moment \u2014 fast, involuntary, almost physical \u2014 is not merely embarrassment. It is closer to a quiet alarm. The signal is not <i>that was awkward.</i> It is something more specific: <i>I have just been seen in a way I did not authorize. Something I was holding has moved outside my control. The interior I was managing has been touched without my consent.</i>",
    "This is your trigger. The word for it is <b>shame</b>, and that word needs careful handling because it is doing more theological work here than it usually gets credit for. Shame is not guilt. Guilt says <i>I have done something wrong.</i> Shame says <i>something about me, as I am, is wrong.</i> Not a single action capable of correction. Something in the constitution of the self that might be, beneath its careful presentation, unacceptable. The Vault\u2019s trigger fires whenever someone gets close enough to the interior that this possibility becomes relevant.",
    "C. S. Lewis, in <i>The Problem of Pain</i>, observed that the human soul is peculiarly sensitive to what he called \u201cthe gaze\u201d \u2014 the experience of being seen and assessed by another. Most people can bear the ordinary gaze of ordinary life. But some souls, for reasons usually rooted in early and specific injury, have learned that the gaze is dangerous. Not that other people are malicious, necessarily. But that the gaze, when it arrives without invitation, arrives as a threat. You are one of those souls, and your strategy has been to manage the gaze before it arrives \u2014 to decide, in advance, exactly what it will find.",
    "<b>Your sensitivity to shame is not random, and it is not vanity.</b> It is the residue of something that happened. Usually early. Usually in a context where your interior was met not with care but with something that felt like judgment, or indifference, or the specific unkindness of a person who meant well and handled badly what you gave them. Perhaps you disclosed something tender and it was made a subject of conversation you did not authorize. Perhaps you showed a struggle and it became, in someone else\u2019s hands, a cautionary tale. Perhaps the household you grew up in simply did not give much air to the interior life \u2014 where what you felt was declared too much, or irrelevant, or not the thing you were supposed to be feeling.",
    "Whatever the specific form, the lesson was lodged in you with precision: <i>what is shown without preparation can be turned against you.</i> And so the Vault assembled itself, one choice at a time, all moving the same direction — toward selectivity, toward the finished version, toward the careful management of what crosses the threshold from interior to visible. There is a genuine gift here: when the Vault discloses, what comes out is considered and precise. But the same gift that makes you a thoughtful communicator also means that genuine intimacy — the kind that answers <i>am I acceptable?</i> — requires something the Vault has been specifically built to prevent. Before we go further, I want you to stop and answer two questions in writing. Not in your head — the Vault will organize what happens there. Your hand will be more honest.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the shame trigger fired. It does not need to be a dramatic event \u2014 look for the moment when something inside you said <i>I have just been seen in a way I did not choose.</i> What happened, in two sentences?",
    "What was the size of the actual event, and what was the size of the response inside you? If the response was significantly larger than the event, you have just located the gap where the trigger lives. Where did the gap appear?",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding. The Vault has been guarding this question for a long time, and has guarded it so effectively that you may not yet have put it into plain language.",
    "Yours is this: <b>Am I acceptable?</b>",
    "It is not quite the same as <i>Am I loved?</i> \u2014 though the questions live near each other. It is not <i>Am I competent?</i> \u2014 though real competence has certainly been built, in part, as a way of trying to answer it. The question is more specific and more frightening than either. It is the question of a person who knows their own interior well \u2014 who is familiar with the failures, the fears, the places of confusion and longing they have spent years carefully containing \u2014 and who is not certain that what is in there, if fully seen, would be received. <i>If someone saw all of this, exactly as it is, without preparation and without curation \u2014 would they find me acceptable? Would they stay?</i>",
    "Most adults prefer to believe they resolved this question long ago. They have not. They have only buried it below sufficient competence and self-presentation that it does not speak clearly in the daylight hours. For you, the question is especially alive because the Vault is honest. You know what is inside better than most people know their own interiors. The Vault is not self-deceived. It has done real work on the material. And it is precisely because you know what is in there that the exposure of it feels so dangerous. You are not anxious about being seen because you are vain. You are anxious because you have accurate information about what is inside, and you are not certain it will be well received.",
]

QUESTION_BODY_P2 = [
    "There is a reason theologians from Augustine to the Reformers have insisted that the deepest hunger of the human soul is for what Paul calls justification \u2014 not merely forgiveness in the everyday sense, but the settled verdict that one is acceptable, righteous, covered. The Psalms return to this hunger with a regularity that should reassure anyone who believes that the desire to be acceptable is too embarrassing to bring before God.",
    "Psalm 139 names the Vault\u2019s specific dilemma with unusual precision. David writes: <i>O Lord, you have searched me and known me. You know when I sit down and when I rise up; you discern my thoughts from afar. You search out my path and my lying down and are acquainted with all my ways. Even before a word is on my tongue, behold, O Lord, you know it altogether.</i> (Psalm 139:1\u20134) The Vault reads this and feels, depending on the day, either strange comfort or quiet dread \u2014 God sees what the Vault has been most carefully managing. But David does not end in despair. He ends in invitation: <i>Search me, O God, and know my heart.</i> He is inviting the one thing the Vault most fears, having discovered that the God who already sees does not turn away from what he finds.",
    "Paul gives the theological ground for this in 2 Corinthians 5:21: <i>For our sake he made him to be sin who knew no sin, so that in him we might become the righteousness of God.</i> Christ took on himself, publicly and without curation, the full weight of what shame is: exposure, stripping, public display. The crucifixion was not a private transaction on a ledger. It was an act of radical, unchosen, unrehearsed exposure \u2014 the only form of human experience the Vault most fears, borne by the Son of God on behalf of everyone who would ever try to manage their way to acceptability. And the one who is united to him stands before God clothed, not naked. Covered, not exposed. The verdict is not <i>acceptable pending further inspection.</i> It is <i>acceptable, finally and fully, because of what Christ has borne.</i>",
    "Here, though, is where the honest rub must be named, and it is specific to you. The Vault hears the doctrine and files it accurately. You may have memorized the precise formulation. But the Vault has a particular difficulty with the gospel that is not an intellectual one. <b>Receiving the verdict requires letting it land.</b> And letting it land requires a kind of interior permeability \u2014 an openness to being given something you did not produce, did not organize, did not present in its best light. The Vault was built specifically to prevent that kind of permeability. Every wall that protects you from exposure also keeps out the gift that exposure makes possible.",
]

QUESTION_BODY_P3 = [
    "Romans 8:1 states it flatly: <i>There is therefore now no condemnation for those who are in Christ Jesus.</i> Not <i>no condemnation once the interior is organized.</i> Not <i>no condemnation when the messy middle has been resolved.</i> Now. In Christ. The Vault has spent years making the interior acceptable before showing it to anyone. God has already seen it, and the verdict has already been spoken \u2014 not after inspection but before it, in Christ, on your behalf.",
    "The work this section is asking of you is not the work of additional self-inventory. The Vault already has more inventory than it can manage. The work is the practice of receiving. Day by day, not as a feeling, not as a sudden liberation, but as a quiet return to news that is already true: the case has been decided in your favor, not by your presentation but by your Advocate. Before we close this section, use the table below \u2014 not to generate more material for the file, but simply to bring recent events into the light of both the question and the answer, together.",
]

VAULT_BODY_P1 = [
    "You have built something. It did not come together in a morning. Most Vaults do not remember a single moment of construction \u2014 the structure assembled itself over years, from the accumulation of small choices that all pointed the same direction, until one day you looked up and it was simply there. Throughout this walkthrough we are going to call it <b>the Vault</b>, and before we say anything about what it costs, the Vault deserves to be understood accurately.",
    "The Vault is not the Island. This distinction is worth pausing over, because the two patterns can look similar from a distance. The Island stays inside because inside is where the Island lives comfortably. The Island\u2019s self-containment is temperamental \u2014 it is simply how the Island is wired, and there is nothing particularly strategic about it. The Vault is different. The Vault has locks, and the locks were installed for a reason. The Island is self-contained because outside is not needed. The Vault is self-contained because outside has been demonstrated, at specific moments, to be dangerous.",
    "The Vault\u2019s strategy, stated plainly, is this: <i>I will show you what I have chosen to show you. What I have chosen to show you will be organized, finished, and presented in its best form. What I have not chosen to show you will remain mine. This arrangement will protect me from the particular danger that comes when unfinished things are examined by people who have not been given the context to receive them well.</i> This is not dishonesty \u2014 the Vault shows real things. But real things that have passed through a selection process, a management process, a finishing process before presentation.",
    "There is genuine wisdom in this that Scripture itself commends. Proverbs 17:27 says: <i>Whoever restrains his words has knowledge, and he who has a cool spirit is a man of understanding.</i> The capacity to hold one\u2019s interior without scattering it indiscriminately is not weakness; it is a form of self-command. <b>The Vault is not, in itself, a sin.</b> It is a genuine gift that, over time, has been overextended \u2014 applied in places where what was built to protect has itself become a burden.",
]

VAULT_BODY_P2 = [
    "How did the Vault form? Most often from a specific kind of injury. You showed something interior \u2014 a fear, a doubt, a grief that was still wet \u2014 and the person who received it handled it carelessly: used what you gave them, shared it without permission, or held it so lightly that the wound of showing felt worse than the wound that prompted the showing. The lesson was lodged precisely: <i>what I give can be turned against me.</i>",
    "For others, the second origin was subtler: a suspicion that what is inside \u2014 the particular textures of your doubt, longing, failure, confusion \u2014 is more disordered than what other people carry. If it were seen clearly, it would change how you are regarded. A third origin is simpler still: a home in which feelings were handled quietly, privately, as personal management \u2014 not punished, but not given air. Whatever the form, the lesson was the same: <i>what is inside is best managed alone.</i>",
    "Dietrich Bonhoeffer, in <i>Life Together</i>, wrote with pastoral directness about the believer who brings only the resolved version of themselves to the community of faith \u2014 who processes the struggle alone and arrives at fellowship already finished. He called this a severing from one of the great mercies of the church: being known in one\u2019s actual condition and received anyway. What the Vault brings to God and the community has always already been prepared. Bonhoeffer would call this a spiritual solitude that is, in the end, lonelier than it is holy.",
]

VAULT_BODY_P3 = [
    "What does the Vault cost you? Let me name three things honestly. First, <i>the intimacy you most want.</i> The Vault\u2019s deepest longing is to be known fully and found acceptable — precisely what the question <i>am I acceptable?</i> is asking for. But the mechanism ensures that no one ever gains access to the information that would allow them to answer the question genuinely. Their acceptance, however real, can never fully satisfy, because it is acceptance of the Vault\u2019s presentation rather than of the Vault\u2019s interior.",
    "It costs you <i>the speed of repair.</i> When you are wounded, the wound goes inside. The Vault is meticulous \u2014 it notes the date, the context, the specific words. Not maliciously, but because precision is part of the gift. The file grows. The relationship continues on the surface. Something accumulates underneath, waiting for a moment large enough to break the management.",
    "It costs you <i>the freedom of real presence.</i> The people who love the Vault are, in a specific way, always in relationship with a performance \u2014 not a false performance, but a curated one. They do not know how to comfort you fully because you have not shown them the interior. They pray for the version of you that you have chosen to present, which is not quite you. There is a loneliness in being loved for the edited version of yourself that the Vault rarely names but almost always feels.",
    "<b>The Vault is not your enemy.</b> He is a younger version of you who learned, in real circumstances, that the unlocked interior was not safe. He has been faithful. He has kept you in relationships by keeping those relationships from the material most likely to fracture them. But the walls that once protected you are now preventing the one thing your question most needs: to bring the actual interior into actual presence and discover that it is received. Before we close this section, I want you to read a letter \u2014 not one you wrote to the Vault, but one from the Vault himself, in his own voice, to you. He has been faithful for a long time and deserves to be heard clearly.",
]

VAULT_LETTER_BODY = """\
<i>Dear [your name],

I want to explain myself, since no one has ever asked me to and I have never offered. I want to tell you what I have been doing, and why, and what I am most afraid of losing if I stop.

I have been protecting you from the injury of being seen in the middle of something \u2014 in the unresolved, unorganized, half-assembled middle \u2014 and having what is seen used as evidence against you.

I built the locks because the evidence was compelling. You showed something once. More than once. And what happened next taught me that showing without preparation is the same as handing someone a weapon and asking them to be careful. So I started choosing. I started finishing. I started bringing people only what had been thought through, organized, set in its best light. And it worked. What you did not give them, they could not misuse.

What I did not calculate is the weight of what stays inside. Every wound that went in and did not come back out is still in here. And the longer I keep it, the more certain I have become that the interior, if fully seen, would change what people think of you. I am no longer sure whether I arrived at that conclusion from evidence, or whether keeping the locks has simply become the evidence.

There is one thing I need to tell you, and it costs me a great deal to say it. I think I have confused protecting you with hiding you. Not your failures. Not your worst moments. You. The person underneath the finished version.

I do not know how to change this on my own. I have been doing it too long. But I want you to know what I am protecting you from, and whether what I am protecting you from is still as dangerous as it was when I first began.</i>

\u2014 The Vault"""

VAULT_LETTER_PROMPTS = [
    "What part of the Vault\u2019s letter surprised you? Not the part you already knew \u2014 the part you were not quite ready to hear.",
    "The Vault says he has confused protecting you with hiding you. Name one specific thing about your interior \u2014 a fear, a wound, a longing \u2014 that has been inside, organized but undisclosed, for a significant period of time. You do not need to disclose it here. Simply name that it exists.",
    "What would the Vault need to believe \u2014 really believe, at the level where the management happens \u2014 for the locks to begin to loosen? What would have to be true about God, or about one other person, for the interior to become slightly safer to show?",
]

PLEA_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Vault, the breaking has a shape unlike any of the other profiles, and naming that shape precisely is the most important pastoral work in this document. The breakdown is called <b>the Plea</b>. And before you read further, I want to tell you what it is not.",
    "It is not a sudden transparency. It is not the Vault finally opening and letting someone see the real interior. It is not the walls coming down. <b>The Vault\u2019s Plea is a change in the genre of what is curated.</b> For months or years, the Vault has been presenting finished conclusions. When the Plea fires, the Vault begins presenting finished apologies. The form has changed. The control is identical.",
    "Here is the specific image that will likely land with recognition. There is a conflict \u2014 a gap has opened, a relationship feels genuinely threatened, the person on the other side has gone quiet or cold in a way that the Vault\u2019s ordinary management cannot bridge. The Vault does not simply walk into the next room and say, with unguarded eyes, <i>I am frightened and I do not want to lose this.</i> That is not what happens. What happens is that the door stays closed, and sometime later \u2014 perhaps 2am, perhaps the following morning \u2014 something slides under the door. A letter. A long, carefully written letter. Or a message with numbered points. Or a text that has been drafted and revised and sent in the small hours, organized around the things that went wrong, the things that were felt, the things the Vault is now prepared to concede \u2014 all of it thought through, all of it considered, none of it messy, none of it truly present.",
    "The Vault+Plea is the person who processes the apology before delivering it. Who prepares the vulnerability before showing it. Who arrives at the door of reconciliation with a brief, having spent the night organizing the evidence of their own remorse into something coherent. From the outside, this can look like effort, which it is. It can look like care, which it is also. But here is the pastoral word that this profile most needs and is least likely to have heard: <b>the Plea has not opened the Vault. It has simply given the Vault a new project to curate.</b>",
]

PLEA_BODY_P2 = [
    "I want to describe what this looks like from the inside, because from the inside it does not feel like control. It feels like repentance. It feels like the Vault finally doing the thing it has spent years avoiding: producing something interior and offering it. The letter was hard to write. The message cost something. The organized recounting of what went wrong, delivered in the small hours, feels like exposure \u2014 and in a technical sense it is. The Vault is showing more than usual.",
    "What it is showing, however, is organized. Prepared. Curated. The messy middle \u2014 the actual experience of being frightened, of not knowing what happened, of genuinely not understanding whether the relationship is in danger \u2014 that part stayed inside. What was sent is the finished version of the remorse. Which is to say: what was sent is still the Vault.",
    "The person on the receiving end will feel this, even if they cannot name it. They will receive the letter and feel, alongside genuine appreciation for its effort, something they struggle to articulate: <i>I have been given a document. I have not been given the person.</i> The gap that opened between you has not, in fact, been crossed. A well-crafted bridge has been built across it, and the builder stands on their side, waiting to see whether you will walk across. The Vault\u2019s Plea is not presence. It is a very beautiful invitation to presence, extended from behind a door that has not quite opened.",
    "J. C. Ryle observed that the soul is capable of performing entirely correct-looking acts from deeply self-protective motives \u2014 that the problem lies not with the behavior but with the root. The Vault\u2019s Plea performs all the external behaviors of genuine repair: it acknowledges, it concedes, it apologizes. And underneath every one of those right behaviors is the Vault\u2019s oldest instinct: <i>let me produce something finished that demonstrates my remorse, because finishing is safer than being present in the middle of it.</i>",
]

PLEA_BODY_P3 = [
    "The gospel has a specific word for this. In Luke 15, the prodigal son rehearsed his speech before attempting his return: <i>Father, I have sinned against heaven and before you. I am no longer worthy to be called your son.</i> (Luke 15:18) He had organized his remorse into a proposal. He had, in other words, done what the Vault does: prepared the presentation before attempting the return.",
    "And then the father saw him coming while he was still a long way off. <b>And the father ran.</b> He did not wait for the speech. He ran toward the half-ready, still-unfinished version of his son and kissed him before a word of the prepared apology was delivered. The son got through the first line — and the father interrupted. Not with a response to the speech. With a robe, a ring, a celebration. The father did not need the finished version. He wanted the person.",
    "Spurgeon preached that <i>God runs to meet the half-hearted prayer of the truly broken; he hears the polished prayer of the still-hidden heart.</i> Paul names what is finally at stake in 2 Corinthians 7:10: <i>Godly grief produces a repentance that leads to salvation without regret, whereas worldly grief produces death.</i> When the letter was written at 2am — was that godly grief, the truly broken heart arriving unpolished? Or worldly grief, producing a presentation? Both feel identical from the inside. The difference is whether the actual person is being brought into the light, or whether the performance of remorse is being curated so the light will not have to land on the actual interior.",
    "<b>The remedy is not a better apology. The remedy is messy, real presence.</b> It is the walk from the next room to the room where the other person is sitting \u2014 without a draft, without numbered points, without a speech rehearsed on the way down the hall. It is the willingness to arrive unfinished and trust that the God who ran toward the unfinished son runs toward you too. That is not the Vault\u2019s natural motion. It will feel, the first time you attempt it, like incompetence. The Vault will call it irresponsibility. It is, in fact, the beginning of the intimacy the question has been asking for from the start.",
]

PLEA_PROMPTS = [
    "Think of the last time the Plea ran \u2014 the last apology that was prepared before delivery, the last message that was drafted and revised before sending, the last time you processed your remorse into a finished form before offering it to the person you had hurt or feared losing. Describe it in two sentences. Notice the specific genre: was it a letter? A text? A speech you ran through internally before speaking?",
    "The Vault\u2019s Plea is still curating. What, specifically, did you keep inside during that episode \u2014 what was still unfinished, unresolved, genuinely unsure \u2014 that did not make it into the prepared apology? What stayed in the vault while the presentation went out?",
]

TWO_TOG_BODY = [
    "Now we stand back and look at both of them together, because the Vault and the Plea are not two separate problems. They are the same fear, working in two modes that look entirely different from the outside but are identical at the root.",
    "<b>The Vault is what your fear does when it has time.</b> It processes, selects, finishes, presents. It keeps the interior close and releases only what has been prepared. <b>The Plea is what your fear does when it has run out of time.</b> When the relationship is in genuine danger and the usual management cannot hold, the Plea fires \u2014 but the Vault does not simply break. It shifts projects. It moves from curating conclusions to curating apologies. The medium changes. The control does not.",
    "The sequence, slowly: the Vault manages exposure, presenting finished conclusions, keeping the process private. A wound lands. The trigger fires. The question wakes up: <i>am I acceptable, even now?</i> The Vault takes the wound inside. What comes out is not the wound in its raw form but the finished version of the remorse — the letter, the organized message, the prepared speech. The gap may close. But the question is not answered, because no one has yet received the interior. The Vault closes again. The loop restarts.",
    "What breaks the loop is not a better apology. It is a different answer to the question — received below the management level. It is the practice of bringing the actual, unfinished, unprepared interior into the presence of God and of at least one other person, and discovering that what is found there is received. It is the slow learning that the father ran while the son was still a long way off. Still unprepared. Still unready. And still, in that state, received.",
    "Below is your sequence. Fill in the blanks. When you are finished, read it aloud. The Vault and the Plea both lose some of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as exposure \u2014 as "
    "being seen in a way I did not authorize, and as evidence that I may be losing "
    "something I cannot afford to lose \u2014 and the old question wakes up: "
    "<i>am I acceptable?</i> My first move is to ____________________, because "
    "the Vault in me believes that if I can ____________________, the danger can "
    "be managed. When that does not work \u2014 when the gap opens anyway and the "
    "threat is real \u2014 the Plea takes over, and I find myself ____________________. "
    "What comes out is still curated, still organized, still ____________________. "
    "What I am actually after, underneath all of it, is the word "
    "____________________\u00a0\u2014 a verdict Christ has already spoken over me in "
    "____________________, before I prepared a single word in my own defense."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of practices, each concrete enough to use and honest enough to matter. None of them will dissolve the Vault\u2019s pattern overnight. All of them, practiced with patience over months, will loosen the grip of the loop you just named.",
    "I have divided them into two sets: tools for when the Vault is overworking (when the management of exposure has tipped from wisdom into hiding), and tools for when the Plea is running (when the gap has opened and the curated apology is being prepared). The Vault\u2019s tools come first, because the Plea cannot be interrupted usefully until the mechanism beneath it is understood. You cannot stop curating apologies until you understand why you curate conclusions.",
]

VAULT_TOOLS = [
    ("The half-built offering", "Once a week, share something with one trusted person before it is finished. Not a crisis \u2014 simply something you are in the middle of, a question you have not resolved, a feeling not yet organized into a conclusion. The Vault will resist this as irresponsible. Do it before you know what you think. Over a month, the practice demonstrates that unfinished things, shared carefully, do not produce the catastrophe the Vault has been managing against."),
    ("The audit of what is being processed alone", "Once a week, ask: <i>what went inside this week that I have not disclosed to anyone?</i> You do not need to disclose it all. Simply name that it exists \u2014 to yourself, and if possible to God in prayer. The Vault\u2019s most dangerous work is invisible. Naming the contents, even privately, begins to interrupt the automatic management."),
    ("Pray Psalm 139, the whole thing", "When the Vault is in full management mode, open to Psalm 139 and pray it aloud \u2014 the whole psalm, not selected verses. It ends not in shame but in invitation: <i>Search me, O God, and know my heart. Try me and know my thoughts.</i> The Vault needs practice asking to be known by God before it can practice asking to be known by people. This psalm is that practice."),
    ("Receive the verdict before you organize the wound", "When the shame trigger fires \u2014 when the interior has just been touched without your consent \u2014 say aloud before you begin to manage it: <i>God has already seen this, and the verdict is covered. I am in Christ. I do not need to resolve this before I am acceptable.</i> The Vault\u2019s instinct is to receive the wound silently and begin the process. This practice interrupts the process before it starts and replaces it with the gospel\u2019s direct answer."),
]

PLEA_TOOLS = [
    ("Walk across before you write", "When the gap opens and the Plea rises \u2014 when you feel the impulse to draft the message, to organize the apology, to prepare the presentation \u2014 ask one question first: <i>can I simply go to where the person is, without a draft?</i> Not with a speech. Not with numbered points. Simply present, simply unfinished, simply there. The Vault will call this insufficient. It is the only form of presence that can answer the question underneath the Plea."),
    ("Name the drafting before you send", "If you cannot resist drafting, name it to the person when you send: <i>I wrote this out because I process better that way, but what I actually want is to be present with you, not just to give you a document.</i> This sentence does not stop the Vault from curating. But it makes the curating visible, which is the first step toward not needing it."),
    ("Ask before you apologize", "Before apologizing for something you are not entirely certain you did wrong, ask: <i>is this apology true, or is it the Plea dressed in the language of repentance?</i> If the honest answer is the latter, do not apologize. Be present instead. Sit down. Ask one question. Let the other person be the one to speak first. The false apology closes the gap temporarily. It does not open the interior."),
    ("The Spurgeon prayer", "When the Plea is running and the draft is being organized, pray this before sending anything: <i>Lord, I am bringing you the polished prayer. I know you hear the half-hearted prayer of the truly broken. Help me to be more broken than polished. Help me to walk in, not write in.</i> Say it slowly. The Vault loses some of its authority over the keyboard when it has been required to say what it is doing out loud."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Vault in me, and you are not surprised by it. You know when it was built — the specific moments when vulnerability went badly, when the lesson was lodged that the interior is best managed alone. Thank you that the Vault kept me in relationship. But Father, the finished version is not me. The concluded conclusion, the organized grief, the prepared apology — these are not me. They are me with the door still closed. You are not asking for the finished version. You searched me and knew me before I had anything prepared. Your verdict was spoken not because I presented well but because your Son bore what I most feared showing: the exposure, the stripping, the complete visibility. And the verdict he brought back was covered. Clean. Acceptable. Now, in Christ, before I organized a single word in my own defense.",
    "Lord Jesus, when the Plea rises in me and I find myself drafting the apology before I can bear to walk across the room \u2014 remind me of the father who ran while his son was still a long way off. Still unready. Still unrehearsed. Still carrying the smell of where he had been. The father did not wait for the speech. He ran. Teach me to walk toward the people I have wounded the way your father ran toward his son: before the presentation, before the polished language, before I know what I am going to say.",
    "Holy Spirit, where I am managing, give me the courage to simply be present. Where I am curating the apology, give me the grace to walk in with empty hands. Where I am polishing the prayer, make me more broken than polished. Teach me that the God who already sees the interior is running toward it \u2014 that I do not have to prepare it before he arrives, because he is already there, and the verdict is already spoken, and it is good.",
    "In the name of the One who was exposed, fully and finally, so that I might be covered \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Vault and the Plea have been with you for a long time, and one reading will not retire them. What follows is a short list of next steps \u2014 some immediate, some longer-term \u2014 for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different sections will land differently. The Vault will want to process this document once, file it accurately, and consider the matter handled. Read it again anyway. The section that felt least relevant today may be the most necessary one in a month."),
    ("Take one tool, not six.", "Choose a single practice from Section 7 and try it honestly for two weeks before adding another. The tools are postures, not a program. One posture, held long enough, begins to change the shape of the interior. The Vault will want to implement all of them efficiently. That is itself the mechanism at work."),
    ("Tell one person what you found.", "Not the whole document. One honest sentence: <i>My mechanism is the Vault, and when the connection feels threatened, my breakdown is a curated apology rather than real presence \u2014 and I am learning the difference.</i> Notice what happens when the Vault is required to describe its own operations to a trusted witness. The Vault loses authority when it is forced to speak about itself aloud."),
    ("Pray Psalm 139 slowly, once a week, for a month.", "All of it. The verses you find comforting and the ones you find quietly frightening. Verse 23 especially: <i>Search me, O God, and know my heart. Try me and know my thoughts.</i> This is the Vault\u2019s hardest prayer because it is the explicit invitation of the God who already sees. Practice the invitation."),
    ("Read further on the shame the gospel covers.", "Tim Keller, <i>Walking with God through Pain and Suffering</i> \u2014 especially his treatment of why suffering feels like exposure, and how the gospel\u2019s answer is not immunity from exposure but the covering of a son or daughter clothed in Christ\u2019s righteousness. C. S. Lewis, <i>The Weight of Glory</i> \u2014 his account of the longing to be known and named by the highest authority will name the Vault\u2019s deepest longing with unusual precision. Dietrich Bonhoeffer, <i>Life Together</i> \u2014 his chapters on confession and community are the most direct pastoral address to what the Vault most needs and most avoids."),
]

GOING_FURTHER_CLOSING = (
    "You are not a presentation to be evaluated. You are a soul being loved into freedom by a Father "
    "who ran toward you before you had finished your speech \u2014 who saw you from a long way off, "
    "still unready, still unpolished, and still ran. The Vault was built in real circumstances, for real "
    "reasons, and it has served you faithfully. But you were not made to live behind it. "
    "Go gently with yourself. The One who began this good work in you will be the one to finish it. "
    "You do not have to curate that either."
)


def _three_column_table(rows=7):
    """Three-column journal table for Section 3 \u2014 Vault+Plea version."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE EVENT", header_style), Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WAS I EXPOSED HERE?", header_style), Paragraph("what the Vault concluded", sub_style)],
        [Paragraph("WAS MY SOUL IN DANGER?", header_style), Paragraph("the deeper question, and God\u2019s answer", sub_style)],
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
    """Generate the Vault + Plea walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='VAULT', primary_breakdown='PLEA',
    primary_trigger='SHM', core_question='ACC'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="VAULT  \u00b7  PLEA",
        title="Take 139 Walkthrough \u2014 Vault + Plea",
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
    story.append(Paragraph("The Vault \u00a0\u00b7\u00a0 The Plea", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Shame \u00a0\u00b7\u00a0 Core Question: Am I acceptable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cGod runs to meet the half-hearted prayer of the truly broken;<br/>"
        "he hears the polished prayer of the still-hidden heart.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Charles Spurgeon",
        ParagraphStyle("cqa", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 1: Opening \u2500\u2500
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read this slowly. The chapter that follows has been a long time in the writing.")
    for p in OPENING_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 2: Trigger \u2500\u2500
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TRIGGER",
                   "Shame.",
                   "The moment of unauthorized exposure, and what your soul makes of it.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will organize the question; your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 3: Core Question \u2500\u2500
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I acceptable?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "What Scripture says, and what receiving it costs you.",
                   "The God who already sees, and the verdict he has already spoken.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "Where was I actually exposed? Where was my soul covered?")
    story.append(Paragraph(
        "Use the table below. In the first column, name a recent event in which "
        "the shame trigger fired. In the second, write what the Vault concluded: "
        "<i>was I exposed here?</i> In the third, answer the deeper question: "
        "<i>was the part of me that finally matters \u2014 my soul, my standing before "
        "God \u2014 at any point in danger?</i>",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table())
    story.append(PageBreak())

    # \u2500\u2500 SECTION 4: Mechanism \u2500\u2500
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Vault.",
                   "The one who keeps the interior close, and presents only what has been chosen.")
    for p in VAULT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "How the Vault formed, and what it costs.",
                   "Four origins, and three things that do not get through the locked door.")
    for p in VAULT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in VAULT_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Vault.",
                   "Read his own words. He has been faithful; let him speak.")

    letter_style = ParagraphStyle(
        "VaultPleaLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    story.append(Paragraph(
        "The letter below is written in the Vault\u2019s voice \u2014 from him, to you. "
        "He is not villainous. He is careful, and he is frightened, and he has something "
        "to tell you that he has never been asked to say. Read it slowly. "
        "Then answer the three prompts that follow.",
        S["BodyJ"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(VAULT_LETTER_BODY, letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in VAULT_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=2)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 5: Breakdown \u2500\u2500
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Plea.",
                   "The curated apology. The letter under the door. The Vault, still managing.")
    for p in PLEA_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in PLEA_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The father who ran before the speech was ready.",
                   "The remedy is not a better apology. It is messy, real presence.")
    for p in PLEA_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "The curated apology, named plainly.",
                   "Two questions to sit with before you turn the page.")
    for prompt in PLEA_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same fear, in two curation projects.",
                   "The Vault and the Plea are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 6))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=5)
    story.append(PageBreak())

    # \u2500\u2500 SECTION 7: Tools \u2500\u2500
    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "What to do when you feel the loop start.",
                   "Small enough to carry; honest enough to use.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Vault is overworking its defenses.",
                   "Four practices for the time before the alarm fires.")
    for name, desc in VAULT_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Plea begins to draft.",
                   "Five practices for the moment the curated apology starts to assemble.")
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


# \u2500\u2500 STANDALONE TEST \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "VAULT"
        primary_breakdown = "PLEA"
        primary_trigger = "SHM"
        core_question = "ACC"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "vault_plea_test.pdf")
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

    print(f"DONE: vault_plea.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
