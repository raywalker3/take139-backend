"""Personal Walkthrough — Vault + Ghost.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Shame trigger, "Am I acceptable?" core question.
Mechanism: Vault (VAULT) — keeps the messy middle private; curates what is shown;
  processes internally and presents finished conclusions.
Breakdown: Ghost (GHOST) — performs normalcy, goes silent, waits to be discovered.
~25 pages, 9 sections.

Calibration note: The Vault+Ghost is the EXPECTED breakdown for this mechanism —
the breakdown the Vault has been quietly preparing for all along. Unlike the
Architect+Ghost (which performs composure), the Island+Ghost (which performs
contentment with solitude), or the Ambassador+Ghost (which is a tragic betrayal
of the caretaker's gift) — the Vault+Ghost does not perform at all. It simply
closes. The doors that were already locked become unreachable. This is the hardest
Ghost to recover from because it requires no performance: the mechanism is simply
doing what it has always done, only more so.

Key theological move in Section Five: Psalm 32:3 ("when I kept silent, my bones
wasted away through my groaning all day long") and David Powlison's pastoral
observation that hidden sin and hidden sorrow operate by the same physics — both
grow in the dark.
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
    "Before you read any further, I want to do for you what a good counselor does in the"
    " first session. I want to lower the lights and slow the pace, because what you are"
    " about to look at is not a personality inventory or a catalog of your tendencies. It"
    " is a patient look at the way your soul has learned to survive a particular kind of"
    " fear \u2014 the fear that if someone saw what was actually inside you, without"
    " preparation, without curation, without the finished version that you have worked so"
    " carefully to present \u2014 they would find you wanting. And having found you wanting,"
    " they would leave.",

    "You are, in a real sense, a Vault. Not because you are cold or incapable of love"
    " \u2014 the Vault, if anything, has a richer interior than most people in the room. Not"
    " because you are dishonest \u2014 the Vault shows real things. But because something"
    " specific and early in your experience taught you that the interior life is best"
    " managed privately, that the messy middle \u2014 the doubt, the grief, the confusion,"
    " the longing, the failure not yet resolved into a tidy conclusion \u2014 belongs to you"
    " alone. That is the Vault's arrangement with the world.",

    "We are going to walk through your trigger, the question underneath it, the strategy"
    " you have built in response, and the place that strategy collapses under pressure."
    " And then, only then, will we put tools in your hands.",

    "<b>What you are about to read is true, but it is not the whole truth about you.</b>"
    " The whole truth includes a Father who does not require you to organize yourself"
    " before he will receive you; a Son who was stripped and exposed, publicly and"
    " completely, so that your exposure might be permanently covered; and a Spirit who is,"
    " at this very moment, interceding for the parts of you that you have locked away and"
    " have never shown anyone, and who is not surprised by a single syllable of what he"
    " finds in there. So read slowly. Argue with what does not fit. Stay with what does."
    " Pray when something catches in your throat, because that catch is usually the Lord"
    " saying, <i>look here, with me.</i> The goal is a slightly freer life, lived before a"
    " God who has already seen everything in the file and has not once turned away from"
    " what he found. Take your time. It deserves a few unhurried hours.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life"
    " have never seen it occur. From the outside it can look like almost nothing \u2014 a"
    " brief flicker, a small stillness, a barely perceptible shift in how present you are."
    " You are in a conversation, or a meeting, or a moment at the kitchen table, and"
    " something changes. Someone draws a conclusion about you that is close enough to"
    " accurate that it lands like a violation. Someone notices something you had not chosen"
    " to show \u2014 a failure, a fear, a grief that was not yet resolved into a conclusion"
    " \u2014 and they comment on it, or they mention it to someone else, or they simply look"
    " at you with the particular expression that says: <i>I see something you did not mean"
    " to reveal.</i>",

    "On the surface this looks like ordinary social discomfort. For you, it registers as"
    " something else entirely. What fires in your chest \u2014 fast, involuntary, almost"
    " physical \u2014 is not mere embarrassment. It is closer to alarm. The signal is not"
    " <i>that was awkward.</i> The signal is: <i>I have been seen in a way I did not"
    " authorize. Something I was holding has been taken from my hands. I am less safe than"
    " I was ten seconds ago.</i>",

    "This is your trigger. The word for it is <b>shame</b> \u2014 and that word needs careful"
    " handling, because it is doing more work here than it usually appears to do. Shame is"
    " not guilt. Guilt says, <i>I did something wrong.</i> Shame says, <i>something about"
    " me, as I am, is wrong.</i> It is not about a behavior that can be corrected. It is"
    " about a self that might be, beneath its carefully presented exterior,"
    " unacceptable \u2014 and the trigger fires every time someone gets close enough to the"
    " interior that this possibility becomes relevant.",

    "C. S. Lewis, in <i>The Screwtape Letters</i>, has his senior demon observe that one"
    " of the most effective strategies for tormenting a human soul is to keep its attention"
    " fixed perpetually on itself \u2014 on how it appears, on what others see, on the"
    " maintenance of a self that will be adequate to any inspection. The Vault does not"
    " do this exactly \u2014 the Vault is not a navel-gazer. The Vault does something more"
    " sophisticated: it thinks ahead. It anticipates the gaze before it arrives and"
    " decides, in advance, what the gaze will find. The Vault is not anxious about"
    " exposure in the moment. It manages exposure before the moment comes.",

    "<b>Your sensitivity to shame is not random, and it is not vanity.</b> It is the"
    " residue of something specific and early in your experience \u2014 moments in which your"
    " vulnerability was met not with care but with judgment, with carelessness, with"
    " mockery, or with the particular cruelty of people who meant well and handled badly"
    " what you gave them. Perhaps you shared something tender and it was dismissed. Perhaps"
    " you were honest about a failure and it became a cautionary tale someone told to"
    " someone else. Perhaps you simply lived in a household where the interior life was"
    " treated as a liability \u2014 where feeling things too visibly was weakness, where what"
    " you showed could be corrected or ignored or turned against you.",

    "Whatever the specific history, the lesson was lodged precisely in you: <i>what is"
    " shown can be used against you, and what stays inside stays safe.</i> And so the"
    " Vault was built \u2014 not in a morning, not by a single decision, but by a long"
    " accumulation of small choices that all moved in the same direction. Toward"
    " selectivity. Toward presentation. Toward the careful management of what crosses the"
    " threshold between your interior and the world.",

    "There is a real gift here that deserves to be acknowledged honestly. The Vault does"
    " not scatter its interior on every available surface. When the Vault does disclose,"
    " what comes out is considered, organized, and precise. These are genuine qualities."
    " But the same mechanism that makes you a thoughtful communicator also makes genuine"
    " intimacy difficult \u2014 and the question underneath your trigger is one that only"
    " genuine intimacy can begin to answer. Before we go any further, take a breath and"
    " write two things down. Not in your head \u2014 the Vault will reorganize whatever"
    " happens in your head. Your hand will be more honest.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the shame trigger fired. It does"
    " not need to be dramatic. Look for the moment when something inside you said:"
    " <i>I have just been seen in a way I did not choose.</i> What happened, in two"
    " sentences?",

    "What was the size of the actual event, and what was the size of the response inside"
    " you? If the response was significantly larger than the event, you have just located"
    " your trigger. Where was the gap?",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The"
    " trigger is the alarm; the question is the wound the alarm was installed to guard."
    " The Vault has been guarding this question for a very long time, and has guarded it"
    " so skillfully that you may not yet have put it into plain language.",

    "Yours is this: <b>Am I acceptable?</b>",

    "It is not quite the same as <i>Am I competent?</i> \u2014 though you have built real"
    " competence in part as a way of answering it. It is not quite <i>Am I lovable?</i>"
    " \u2014 though the questions live near each other. It is more specific and more"
    " frightening than either. It is the question a person asks when they have deep and"
    " accurate knowledge of their own interior \u2014 of the failures, the fears, the"
    " confusion, the longing they have worked so carefully to contain \u2014 and that"
    " knowledge produces in them not peace but a low-grade, persistent dread: <i>If"
    " someone saw all of this, exactly as it is, without preparation and without curation"
    " \u2014 would they find me acceptable? Would they stay?</i>",

    "There is a particular cruelty in this that deserves to be named. The very quality"
    " that makes you thoughtful and self-aware \u2014 the capacity to see your own interior"
    " honestly, to know what is actually in there \u2014 is the same quality that makes the"
    " shame trigger so acute. You are not anxious about exposure because you are vain. You"
    " are anxious about exposure because you have accurate information about what is inside,"
    " and you are not yet sure that it will be well received.",

    "Most adults would prefer to believe they settled this question long ago. They have"
    " not. They have only relocated it \u2014 buried it beneath sufficient achievement or"
    " sufficient presentation that it does not speak loudly during the ordinary hours. For"
    " you, it is especially alive precisely because the Vault does not deceive itself. The"
    " Vault has done real work in the interior. The Vault knows exactly what is in there."
    " And it is because you know what is in there that showing it feels like the most"
    " dangerous thing in the world.",
]

QUESTION_BODY_P2 = [
    "There is a reason that theologians from Augustine to the Reformers have insisted that"
    " the deepest hunger of the human soul is not for comfort or significance but for"
    " justification \u2014 not merely forgiveness in the everyday sense, but the settled"
    " verdict that one is acceptable, right, covered, clean. This hunger is not neurosis."
    " It is theology. It is the correct intuition of a creature that has sinned and knows"
    " it, has a broken interior and suspects it, and longs to hear from the only court"
    " that finally matters: <i>you are acceptable. Not acceptable despite what is inside,"
    " but acceptable \u2014 covered, held, named, kept \u2014 because of what has been done for"
    " you.</i>",

    "The Psalms tell the truth about this longing with unusual directness. Psalm 139,"
    " which the Vault often finds either quietly comforting or quietly terrifying, does"
    " not permit the possibility of a hidden interior: <i>O Lord, you have searched me"
    " and known me. You know when I sit down and when I rise up; you discern my thoughts"
    " from afar. You search out my path and my lying down and are acquainted with all my"
    " ways. Even before a word is on my tongue, behold, O Lord, you know it altogether.</i>"
    " (Psalm 139:1\u20134) David is not performing openness here. He is confessing the"
    " inevitable. He is saying: everything the Vault has been managing, God has already"
    " seen. And David does not end this Psalm in despair or in shame. He ends it in the"
    " language of being held, and then \u2014 astonishingly \u2014 in an invitation: <i>Search"
    " me, O God, and know my heart. Try me and know my thoughts.</i> He is asking for the"
    " very thing the Vault most fears, because he has discovered that the God who already"
    " sees does not turn away from what he finds.",

    "Paul puts the theological precision to it in 2 Corinthians 5:21: <i>For our sake he"
    " made him to be sin who knew no sin, so that in him we might become the righteousness"
    " of God.</i> This is the permanent answer to the question <i>Am I acceptable?</i>"
    " Christ took on himself, publicly and explicitly, the full weight of the shame you"
    " have been working to manage internally. He was exposed \u2014 stripped, mocked,"
    " displayed, hung before a crowd with nothing hidden. And he absorbed that exposure"
    " so that the one who is united to him stands before God clothed, not naked; covered,"
    " not exposed. The verdict over you is not <i>acceptable pending further review.</i>"
    " It is <i>acceptable, finally and forever, because of what the Son has done.</i>",

    "But here is the honest difficulty, specific to the Vault. The Vault hears this and"
    " files it accurately. You may have memorized the doctrine. You can likely state"
    " justification with precision. But receiving the verdict is different from knowing"
    " the doctrine. <b>Receiving requires a kind of interior permeability \u2014 an openness"
    " to being given something you did not produce, did not curate, did not present in"
    " its best light.</b> And the Vault has spent years building walls specifically to"
    " prevent that permeability. The gospel's answer to <i>Am I acceptable?</i> is not"
    " an intellectual problem for you. It is a structural one.",
]

QUESTION_BODY_P3 = [
    "First Samuel 16:7 gives us the oldest version of this problem in Scripture. The Lord"
    " says to Samuel, standing before Eliab who looks every inch the king: <i>Do not look"
    " on his appearance or on the height of his stature, because I have rejected him. For"
    " the Lord sees not as man sees: man looks on the outward appearance, but the Lord"
    " looks on the heart.</i> The Vault has organized its entire strategy around the"
    " outward appearance \u2014 around presenting what has been curated and keeping the heart"
    " out of view. But the God of Scripture has already entered through the wall. He does"
    " not see the exterior presentation. He sees the heart. He has been seeing it all"
    " along. And he has spoken his verdict not after inspection but before it, in Christ,"
    " on your behalf.",

    "This is the word the Vault most needs to receive: <b>God already sees what is inside,"
    " and the verdict is not condemnation. The verdict is covered.</b> Romans 8:1 \u2014"
    " <i>There is therefore now no condemnation for those who are in Christ Jesus.</i> Not"
    " <i>no condemnation once you have organized your interior.</i> Not <i>no condemnation"
    " when you have resolved the messy middle.</i> Now. In Christ. The Vault has been"
    " working to make the interior acceptable before showing it to anyone. God has already"
    " seen it and spoken the verdict: covered.",

    "The work this section is inviting is not the work of further self-inventory \u2014 the"
    " Vault already has more than enough of that. The work is the daily, repeated,"
    " quiet practice of receiving the verdict. Not as a feeling. Not as a rush of"
    " liberation. But as a steady return to the news that the case has been decided in"
    " your favor by your Advocate, not by your own careful self-presentation. Before we"
    " move on, use the table below \u2014 not to analyze further, but to bring recent events"
    " into the light of the question and the answer together.",
]

VAULT_BODY_P1 = [
    "You have built something. It took years, and you almost certainly did not decide to"
    " build it \u2014 it assembled itself from the accumulation of small choices that all"
    " pointed the same direction, and one day you looked up and the structure was already"
    " there. Throughout this walkthrough we are going to call it <b>the Vault</b>, and"
    " the Vault deserves to be understood as a character in its own right before we say"
    " anything about what it costs you.",

    "The Vault is not the Island. This distinction matters. The Island processes alone"
    " because that is simply how the Island processes \u2014 its distance is temperamental,"
    " not primarily driven by fear. The Island has thin walls; it is self-contained by"
    " nature. The Vault has thick walls with locks, and the locks were installed for a"
    " reason. The Island stays inside because inside is comfortable. The Vault stays"
    " inside because outside has been shown to be dangerous. The distance is not"
    " preference. It is protection.",

    "The Vault's strategy, stated plainly, is this: <i>I will show you what I have chosen"
    " to show you, and what I have chosen to show you will be organized and finished and"
    " carefully considered. What I have not chosen to show you will remain mine.</i> This"
    " is not dishonesty \u2014 the Vault shows real things. But real things that have been"
    " selected, arranged, and presented at their best before they cross the threshold.",

    "There is a great deal in Scripture that honors this kind of self-command. Proverbs"
    " 17:27 says, <i>Whoever restrains his words has knowledge, and he who has a cool"
    " spirit is a man of understanding.</i> The Vault often knows this verse, and the"
    " Vault is not wrong to claim it. The capacity to hold one's interior and not scatter"
    " it indiscriminately is wisdom, not weakness. <b>The Vault is not, in itself, a"
    " sin.</b> It is a genuine gift that has been overemployed until the gift has become"
    " a wall \u2014 and the wall has become a kind of lonely precision.",
]

VAULT_BODY_P2 = [
    "How did the Vault form? The pattern tends to emerge from one of several histories,"
    " and you will likely recognize yourself in at least one of them. The first is the"
    " history of <i>exposure that went badly.</i> You showed something interior and the"
    " person who received it handled it carelessly \u2014 critically, dismissively, or they"
    " used what you gave them in a way that cost you. You showed the half-built house and"
    " someone commented on the mess. The lesson lodged precisely: <i>what I show can be"
    " turned against me.</i>",

    "The second is <i>shame about the interior itself.</i> Not simply fear of exposure,"
    " but a suspicion that what is inside \u2014 the textures of your doubt, your failure,"
    " your longing \u2014 is more disordered than what others carry. The third is <i>a"
    " preference for finished conclusions.</i> Some Vaults process well internally and"
    " believe that sharing the process in real time is unhelpful. <i>I will bring you the"
    " conclusion when it is ready.</i> This is not always avoidance. But when the"
    " conclusion is always ready and the process is never seen, intimacy becomes a function"
    " of what you present rather than what you are. The fourth history is <i>a household"
    " in which expression was discouraged or destabilized</i> \u2014 where feelings were"
    " managed quietly, as private business, or where they were made into dramas that"
    " required public performance. Either extreme teaches the same lesson: <i>what is"
    " inside is better managed alone.</i>",

    "Dietrich Bonhoeffer, in <i>Life Together</i>, observed that the Christian who keeps"
    " the struggle private and brings only the resolution to the community has severed"
    " themselves from one of the great mercies of the church \u2014 the mercy of being known"
    " in one's actual condition and received anyway. The Vault has usually never had this"
    " experience. It brings the finished version to God and to the people around it, and"
    " holds the process alone. Bonhoeffer would call this a kind of spiritual solitude"
    " that is, in the end, less holy than it looks and lonelier than it feels.",
]

VAULT_BODY_P3 = [
    "What does the Vault cost you? Let me name three things honestly, because the Vault"
    " is skilled at acknowledging costs in the abstract without sitting with them in the"
    " particular.",

    "It costs you <i>the intimacy you most want.</i> The Vault genuinely longs to be"
    " known \u2014 to have someone who knows what is actually inside and remains. This is"
    " exactly what the question <i>Am I acceptable?</i> is asking. But the Vault's"
    " mechanism ensures that no one ever has access to the information that would allow"
    " them to answer the question. Their love, however genuine, can never fully land,"
    " because it is love offered to the Vault's presentation rather than to the Vault's"
    " actual interior.",

    "It costs you <i>the speed of repair.</i> When you are wounded, the Vault takes the"
    " wound inside. What goes inside does not disappear; it is filed. The Vault is"
    " meticulous. It notes the context, the words, the date. The relationship continues"
    " on the surface while something accumulates underground. The accumulation is not"
    " malice. It is what happens when a careful, inward-processing person has no reliable"
    " mechanism for letting wounds back out.",

    "It costs you <i>the ability to be prayed for in your actual condition.</i> The people"
    " in your life pray for the Vault's presentation \u2014 the organized version, the"
    " resolved version. They are not praying for the actual interior because they do not"
    " know it. There is a loneliness in this that the Vault rarely names but often feels:"
    " a sense of being held, superficially, by people who would hold you differently if"
    " they actually knew.",

    "<b>The Vault is not your enemy.</b> He is a younger version of you who learned, in"
    " some real circumstance, that the unlocked version was not safe. He has been"
    " faithful in his way. But he is working on a project that has long since outgrown"
    " the original threat. The walls that once protected you are now preventing the one"
    " thing the question underneath your trigger most needs: to bring the actual interior"
    " into the actual light and discover, slowly and against every expectation, that the"
    " light is not what the Vault has been afraid of.",

    "Before we close this section, I want you to read a letter \u2014 not one you wrote to"
    " the Vault, but one the Vault has written to you. He has been operating for a very"
    " long time without being asked to account for himself. Give him that chance now.",
]

VAULT_LETTER_INSTRUCTION = [
    "The letter below is written in the Vault's voice \u2014 from him, to you. He is not"
    " villainous. He is careful, and he is frightened, and he has been doing the best he"
    " knows how to do with a very difficult assignment. Read it slowly. Then answer the"
    " three prompts that follow.",
]

VAULT_LETTER = """\
Dear Friend,

I want to tell you something I have never been asked to explain, because until now \
no one could see me clearly enough to ask. I want to tell you what I have been doing \
all these years, and why, and what I am afraid will happen if I stop.

I have been keeping a file. Not deliberately, not as a conscious plan. But everything \
that has come through me \u2014 every wound, every fear, every moment of exposure that \
went badly, every grief I processed before showing anyone the conclusion \u2014 has been \
organized. Filed by date. Cross-referenced. I am, if nothing else, thorough.

I built the walls because the alternative was worse. Because I showed something once \
\u2014 several times, and I remember every one, even if you have moved past them \u2014 and \
what happened next taught me that showing without preparation is the same as handing \
someone a weapon and trusting them to be careful. So I started preparing. I started \
choosing. I started bringing people the finished version, and it worked. Nothing I \
had not given could be used against you.

What I did not calculate is the weight of it. Everything you have ever resolved alone, \
I have kept. And the longer I carry it, the more certain I have become that if it were \
seen clearly \u2014 without the preparation, without the curation \u2014 something would break.

But I want to tell you something that costs me a great deal to say. I have begun to \
suspect that I have confused carrying with hiding. I have been so long at the project \
of keeping the interior safe that I have started to believe the interior is the problem, \
when actually the interior is just you. All of it. Even the parts I have been most \
careful to keep filed away. I am not sure what to do with that. But you should know \
why I am here. And whether the thing I am protecting you from is still as dangerous \
as I have believed.

The Vault\
"""

VAULT_LETTER_PROMPTS = [
    "What part of the Vault's letter surprised you? Not the part you expected \u2014 the"
    " part you were not quite ready for.",

    "The Vault says he has been keeping a file. Name one specific entry in that file"
    " \u2014 one wound, one grief, one fear \u2014 that has been inside, organized and dated,"
    " that you have not disclosed to anyone. You do not need to disclose it here. Simply"
    " name that it exists, and notice what it costs you even to name it.",

    "What would the Vault need to believe \u2014 really believe, at the level where the"
    " filing happens \u2014 in order to begin loosening its grip? What would have to be true"
    " about God, or about at least one other person, for the door to become slightly less"
    " locked?",
]

GHOST_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Vault, the breaking has a shape that"
    " is entirely its own \u2014 different from every other Ghost you have read about, if you"
    " have read them, and different in a way that is essential to name before anything else."
    " The breakdown is called <b>the Ghost</b>, and the first thing that must be said is"
    " this: <b>the Vault's Ghost is not a performance. It is the mechanism doing exactly"
    " what it has always done, only more so.</b>",

    "Think about this carefully. The Architect's Ghost performs composure \u2014 the planner"
    " pretending the plan is still working, maintaining the appearance of order while the"
    " order has collapsed. The Island's Ghost performs contentment with solitude \u2014"
    " <i>I just need a little space; I am fine alone</i> \u2014 a breakdown that looks"
    " indistinguishable from the mechanism's normal operating mode. The Ambassador's Ghost"
    " is a tragic reversal \u2014 the person who has spent a lifetime noticing when others"
    " have gone quiet now going quiet themselves, doing to the people they love the very"
    " thing they would never have tolerated being done to them.",

    "The Vault's Ghost is something else again. The Vault does not need to perform"
    " normalcy when it breaks, because the Vault has been performing normalcy \u2014 showing"
    " only what has been curated, holding the rest inside \u2014 all along. When the Vault"
    " breaks, it does not change its behavior. It deepens it. The doors that were already"
    " locked become unreachable. The silence that was already present becomes total. The"
    " interior, which was already being managed privately, simply closes. What was"
    " selective becomes sealed.",

    "Here is the setup. Something has wounded you \u2014 not a minor friction, but a wound"
    " large enough to shake the Vault's usual management. A spouse who says something that"
    " lands as a judgment on who you actually are, beneath the presentation. A friendship"
    " that ends in a way that confirms the oldest suspicion. A moment of public exposure,"
    " unplanned, that puts something interior in front of others before you had time to"
    " prepare it. The trigger fires. The question wakes up: <i>Am I acceptable?</i>"
    " And the Vault does what the Vault has always done: it takes the wound inside. It"
    " begins to manage.",
]

GHOST_BODY_P2 = [
    "But this wound is too large for management. And because the Vault's only strategy is"
    " management \u2014 because it has never developed the alternative of bringing the wound"
    " out while it is fresh and handing it to a safe person \u2014 the management simply"
    " intensifies. The door closes harder. The walls thicken. The presentations continue."
    " From the outside, nothing has changed except a nearly imperceptible cooling, a"
    " barely detectable reduction in availability \u2014 not a dramatic withdrawal, not a"
    " door slammed, not even a <i>I'm fine</i> delivered with audible frost. Simply: less."
    " Slightly less warmth. Slightly less access. Slightly more distance in the eyes.",

    "This is why the Vault's Ghost is the hardest of all Ghosts to recover from \u2014 and"
    " I want to say this plainly, because pastoral honesty demands it. The other Ghosts"
    " require a performance. The Architect has to maintain the pretense of composure."
    " The Ambassador has to keep the social machinery running while something has died"
    " inside. These performances are exhausting, and their exhaustion often becomes the"
    " signal that something is wrong. The Vault's Ghost requires no performance at all."
    " It requires only continuation. The Vault is simply doing what it has always done."
    " The people closest to you may not notice for weeks. They may not notice for months."
    " They may only slowly register, without being able to name it, that something is"
    " slightly further away than it used to be.",

    "David Powlison, in his pastoral work on the mechanics of the hidden interior, observed"
    " that hidden sin and hidden sorrow operate by the same physics: both grow in the"
    " dark. What is brought into the light can be addressed; what stays sealed can only"
    " accumulate. The Vault has created an almost perfect condition for that accumulation"
    " \u2014 not because it is self-destructive, but because it was built to manage alone,"
    " and a wound too large to manage alone will simply grow in the dark of a very well"
    " organized interior.",

    "The Psalms know this experience. Psalm 32:3, written by David about a season of"
    " concealment, names it with an honesty that still lands across three thousand years:"
    " <i>When I kept silent, my bones wasted away through my groaning all day long.</i>"
    " David was writing about unconfessed sin. But the physiology is the same. The person"
    " who keeps the wound sealed \u2014 who groans, as the Psalm says, <i>all day long</i>"
    " but shows nothing on the surface \u2014 does not thereby escape the weight of it. The"
    " weight does not dissipate in the filing. It builds. The silence is not neutral. The"
    " silence is active. It is its own kind of groaning, conducted without witnesses.",
]

GHOST_BODY_P3 = [
    "Here is what the Vault's Ghost is waiting for, and it is essential to understand"
    " this precisely because it differs slightly from the other Ghosts. The Architect's"
    " Ghost wants to be discovered and pursued \u2014 wants someone to notice that the"
    " composure is a performance and come looking. The Vault's Ghost wants something"
    " harder to name and, in many cases, harder to provide: it wants to be known without"
    " having to show anything. It wants the person who wounded it to somehow understand"
    " what has happened in the interior without the Vault having to open the door."
    " <i>If I have to tell you, it doesn't count the same way.</i>",

    "This is, if you will allow me to say it plainly, an impossible ask. The people in"
    " your life are not mind-readers. They cannot see through walls of even the finest"
    " construction. They will notice the distance but they will not know what it means,"
    " and what they do not understand they will often interpret in the direction that"
    " makes sense to them rather than the direction that is true. They will conclude that"
    " you are busy, or tired, or simply private by nature. They will not conclude that"
    " you have been wounded and have closed because of it \u2014 not because they do not care,"
    " but because the Vault has made it impossible for them to know.",

    "<b>The cruelty of the Vault's Ghost is not the silence itself. It is the distance"
    " it produces by a mechanism so quiet, so consistent with the Vault's normal"
    " operations, that the people who love you cannot distinguish it from who you have"
    " always been.</b> And in that indistinction lies the loneliness that the Vault was"
    " built to prevent: the sense of being not quite known, not quite reached, held at"
    " a level that is real but not quite real enough. The Ghost has never once succeeded"
    " in answering the question it is asking. The silence does not produce discovery."
    " It produces, slowly and with terrible efficiency, the very isolation it was"
    " supposed to protect against.",

    "Before we go further, let me ask you to do something honest. The two questions"
    " below are not designed to be comfortable. They are designed to be accurate."
    " Write your answers by hand.",
]

GHOST_PROMPTS = [
    "Think of the last time the Vault sealed in response to a wound. Not a dramatic"
    " moment necessarily \u2014 look for the moment you took something inside and did not"
    " let it back out. What happened? What did the other person see from the outside?"
    " What were you actually carrying on the inside?",

    "How long has the door been closed? In the relationship, season, or circumstance"
    " that came to mind \u2014 how long ago did the Vault close, and has the other person"
    " known? What would it look like to name one thing aloud before you finish this"
    " document?",
]

TWO_TOG_BODY = [
    "Now we place them beside each other, because the Vault and the Ghost are not two"
    " separate problems. They are the same soul, in two modes of the same strategy."
    " The Vault manages exposure when it has time. The Ghost is what the Vault does when"
    " a wound is too large for management: it simply continues managing, only more so."
    " There is no gear shift. There is only depth.",

    "<b>The Vault is what your fear does when it has time and preparation.</b> The Ghost"
    " is what your fear does when preparation has failed and the wound is inside. The Vault"
    " closes to protect. The Ghost closes to cope. Together they form a closed loop that"
    " runs with near-perfect efficiency, because the mechanism and the breakdown are"
    " nearly identical in form, and the observer \u2014 and sometimes even you \u2014 cannot"
    " tell the difference between the two.",

    "The pattern, in slow motion: <b>(1)</b> The Vault manages exposure. <b>(2)</b> A"
    " wound lands too large for management. <b>(3)</b> The trigger fires: <i>I have been"
    " seen in a way I did not authorize.</i> <b>(4)</b> The question wakes up: <i>Am I"
    " acceptable?</i> <b>(5)</b> The Vault takes the wound inside. The management simply"
    " intensifies. <b>(6)</b> From outside: slightly cooler, slightly further away."
    " Nothing looks different \u2014 only less. <b>(7)</b> The wound grows in the dark."
    " The loop restarts from a position slightly more fortified than before.",

    "What breaks this loop is not better management. What breaks it is a different answer"
    " to the question \u2014 received, not merely filed. Until the Vault receives, at the"
    " level where the managing happens, that the God who has already seen every document"
    " in the file has spoken the verdict <i>acceptable, covered, in Christ</i>, the loop"
    " has nothing to push against. With that answer practiced over time, the Vault finds"
    " less reason to seal every wound that comes through the door. The Ghost finds less"
    " reason to wait in silence. Neither retires fully in this life. But both begin to"
    " work shorter hours.",

    "Below is your sequence. Fill in the blanks. Read it aloud when you finish."
    " The Vault and the Ghost both lose some of their power when they hear themselves"
    " named together in the same sentence.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as exposure \u2014 as "
    "being seen in a way I did not authorize \u2014 and the old question wakes up: "
    "<i>am I acceptable?</i> My first move is to ____________________, because "
    "the Vault in me believes that if I can ____________________, the interior "
    "will stay safe. When the wound is too large for that, the Ghost takes over "
    "\u2014 not by going through the motions of fine-ness, but by simply "
    "____________________. What I am actually waiting for, underneath all of it, "
    "is ____________________. What I actually need is the verdict "
    "____________________ \u2014 a verdict Christ has already spoken over me in "
    "____________________, in a voice the Vault has not yet fully let in."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of practices, each concrete enough"
    " to use on an actual Tuesday, in an actual moment when the loop you just named has"
    " begun to run. None of them will dissolve the pattern in a single application."
    " All of them, practiced with some regularity over months, will begin to loosen the"
    " grip of what you have just described.",

    "I have divided them into two sets: practices for when the Vault is overworking its"
    " defenses \u2014 when the management of exposure has tipped from wisdom into hiding"
    " \u2014 and practices for when the Ghost has closed in \u2014 when the wound is inside and"
    " the door has sealed. The Vault's tools come first, because the Ghost cannot be"
    " meaningfully interrupted until the mechanism that produces it is understood from"
    " the inside.",
]

VAULT_TOOLS = [
    (
        "The half-built house practice",
        "Once a week, share something with one trusted person before it is finished."
        " Not a crisis \u2014 simply something you are in the middle of: a question not yet"
        " resolved, a feeling not yet organized into a conclusion. The Vault will insist"
        " this is premature and probably unnecessary. Do it before you know what you"
        " think. Over a month, this practice begins to demonstrate that unfinished things,"
        " shared carefully with a safe person, do not produce the catastrophe the Vault"
        " has been guarding against.",
    ),
    (
        "The audit of what is being filed",
        "Once a week, ask yourself: <i>what went inside this week that I have not"
        " disclosed to anyone?</i> You are not required to disclose it all at once."
        " Simply name that it exists \u2014 to yourself, and if possible to God in prayer."
        " The Vault's most dangerous work is invisible. Naming the contents, even"
        " privately, begins to interrupt the automatic filing.",
    ),
    (
        "Psalm 139 prayed aloud",
        "When the Vault is in full management mode, open to Psalm 139 and pray it aloud"
        " \u2014 the whole of it, not selected verses. It ends not in shame but in invitation:"
        " <i>Search me, O God, and know my heart. Try me and know my thoughts. And see if"
        " there be any grievous way in me.</i> This is the Vault's hardest prayer because"
        " it is the explicit invitation of the God who already sees. The practice of asking"
        " to be known by God is the precondition for the practice of asking to be known by"
        " people.",
    ),
    (
        "The one-degree opening",
        "Identify one person who has demonstrated, over time, that they can be trusted"
        " with your interior \u2014 not every person, not everyone at once, but one. Choose"
        " one item from the file \u2014 one old grief, one unresolved question, one fear you"
        " have been carrying alone \u2014 and disclose it. Not as a test. As a practice."
        " The Vault was built to prevent precisely this, which is exactly why it is the"
        " most necessary item on this list.",
    ),
    (
        "Receive the verdict before you manage the wound",
        "When the shame trigger fires, before you take the wound inside, say aloud:"
        " <i>God has already seen this. The verdict is covered. I am in Christ. I do not"
        " have to manage this alone.</i> The Vault's instinct is to receive the wound"
        " silently and begin organizing. This practice interrupts the organizing and"
        " replaces it with the answer to the question the wound re-opens.",
    ),
]

GHOST_TOOLS = [
    (
        "Name it before the door closes",
        "The Vault's Ghost is fastest in the first few hours after the wound lands,"
        " before the filing is complete and the door has sealed. In that window, try to"
        " say one sentence to one safe person: <i>Something landed on me, and I am not"
        " ready to talk about it yet, but I want you to know it happened.</i> You do not"
        " have to open the whole file. You have to keep the door from sealing entirely."
        " One sentence, one person, before the process finishes.",
    ),
    (
        "The forty-eight-hour disclosure",
        "If the door has already sealed, commit to naming something within forty-eight"
        " hours of the wound. Not the full interior \u2014 one item. One sentence: <i>I was"
        " more hurt by that than I showed.</i> This single sentence, spoken to the right"
        " person within two days, will do more to interrupt the Ghost than any amount of"
        " private resolution. The Ghost's power depends entirely on the wound remaining"
        " unwitnessed. Witnessed, even partially, it begins to lose its grip.",
    ),
    (
        "Ask one person to notice",
        "This is the hardest practice on this list, and also the most direct. When you"
        " know the Ghost has closed \u2014 when you are carrying something and have gone quiet"
        " with it \u2014 tell one trusted person: <i>I am not doing as well as I look, and I"
        " am not ready to say more than that yet, but I need you to know that something"
        " is there.</i> This is not asking to be rescued. It is interrupting the secrecy"
        " on which the Ghost depends.",
    ),
    (
        "Psalm 32 and the physics of silence",
        "When the Ghost is sealed, open to Psalm 32 and read verses 3 through 5 aloud:"
        " <i>When I kept silent, my bones wasted away through my groaning all day long."
        " For day and night your hand was heavy upon me. I acknowledged my sin to you,"
        " and you forgave the iniquity of my sin.</i> David is naming the physics of"
        " concealment: the kept wound does not dissipate by being organized. It"
        " dissipates by being brought into the light.",
    ),
    (
        "The advocate prayer for the sealed room",
        "When the Ghost is loudest, pray slowly: <i>Lord Jesus, you are my Advocate."
        " You have already seen what is in this room. You went publicly exposed so that"
        " my exposure might be covered. I do not have to manage this alone. Help me to"
        " hand one thing back to you, and one thing to a person who has earned the right"
        " to receive it.</i> The third time you pray this is usually when something in"
        " the room begins to loosen.",
    ),
]

PRAYER_BODY = [
    "Father,",
    "You see the Vault in me, and you are not surprised by it. You know what was locked"
    " inside long before I began to lock it. You know the specific moments \u2014 the"
    " exposures that went badly, the interior I was ashamed of, the home that taught me"
    " that expression was a liability \u2014 and you have been present through all of it,"
    " in every room I have ever organized and kept private. Thank you that the Vault kept"
    " me alive. Thank you that he has been, in his way, faithful.",
    "But Father, the file is heavy, and I have been keeping it for a very long time, and"
    " I have been confusing management with safety and privacy with peace. Teach me that"
    " you have already seen what is inside, and that your verdict is not what the Vault"
    " fears. The verdict is covered. In Christ. Now and forever. Teach me, when the shame"
    " trigger fires and the old question asks <i>Am I acceptable?</i>, to hear your answer"
    " before I hear the Vault's. <i>There is therefore now no condemnation for those who"
    " are in Christ Jesus.</i> Let that sentence land somewhere below my theology.",
    "Lord Jesus, you see the Ghost in me as well \u2014 the way I close, not dramatically,"
    " not with a performance of fine-ness, but simply by continuing to do what I have"
    " always done, only more so. You see the sealed room and the weight that is"
    " accumulating in the dark. You know the sentence in Psalm 32: <i>when I kept silent,"
    " my bones wasted away.</i> You know that I have been carrying things alone that were"
    " never meant to be carried alone. Teach me to open one door at a time. Teach me that"
    " the light on the other side of the door is not what I have feared.",
    "Holy Spirit, where I have been filing, give me the courage to confess. Where I have"
    " been managing, give me the grace to bring. Teach me the difference between the"
    " privacy that is wisdom and the privacy that is hiding. Teach me to bring the actual"
    " interior \u2014 first to the God who has already seen it, then to the people who have"
    " earned the right to receive it. Teach me that the God who looks on the heart, and"
    " not the outward appearance, has looked, has seen everything, and has not turned away.",
    "In the name of the One who was exposed, fully and publicly, so that my exposure might"
    " be permanently covered \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Vault and the Ghost have been"
    " with you for a long time, and one careful reading of this document will not retire"
    " them \u2014 because they were not formed in one reading of anything. What follows is a"
    " short list of directions to move from here: some immediate, some longer-term, all"
    " of them worth your attention.",
]

GOING_FURTHER_ITEMS = [
    (
        "Read this again in thirty days.",
        "Different sections will land differently. The Vault will want to file this"
        " document, mark it complete, and move on. Do not let it. Read it again. The"
        " section that felt least relevant today may be the most necessary one in a month."
        " What you found on the first reading was what the Vault was prepared to find."
        " What you find on the second will be closer to the truth.",
    ),
    (
        "Take one tool, not six.",
        "Choose a single practice from Section Seven and try it for two weeks before"
        " adding a second one. The tools are postures, not a program. One posture,"
        " held with some patience, begins to change the shape of the interior. The Vault"
        " will prefer to analyze all five tools intellectually and implement none of them."
        " Choose one. Do it before you know whether it will work.",
    ),
    (
        "Tell one person what you found.",
        "Not the whole document. One sentence: <i>I learned that my mechanism is the"
        " Vault and my breakdown is the Ghost, and I have been carrying things alone that"
        " I did not realize I was carrying.</i> Notice what it costs you to say that"
        " sentence aloud. Notice what it costs the Vault. That cost is the measure of"
        " how much the Vault has needed to hear it.",
    ),
    (
        "Pray Psalm 139 and Psalm 32 slowly, for a week.",
        "Psalm 139 for the God who already sees. Psalm 32 for the weight of what has"
        " been kept silent. Pray them aloud. The verses you cannot get through without"
        " stopping are the ones that are speaking most directly to the place the Vault"
        " has most carefully locked.",
    ),
    (
        "Read further on the shame the gospel answers.",
        "Tim Keller, <i>Walking with God through Pain and Suffering</i> \u2014 especially his"
        " treatment of why suffering feels like exposure and how the gospel reframes it."
        " C. S. Lewis, <i>The Weight of Glory</i> \u2014 his treatment of the longing to be"
        " known and named by the highest authority will put language to the Vault's"
        " deepest longing with unusual precision. Dietrich Bonhoeffer, <i>Life Together</i>"
        " \u2014 his chapters on confession and community are the most direct pastoral address"
        " to what the Vault most needs and most avoids.",
    ),
    (
        "If you are stuck, ask for help.",
        "There are seasons when the Vault and the Ghost are too entrenched to dislodge"
        " alone. A wise pastor, a Christian counselor, a trusted friend who has earned the"
        " right to the interior \u2014 these are not signs of failure. For the Vault"
        " specifically, asking for help is among the most countercultural acts on this"
        " list. The Vault was built to manage alone. Asking someone in is the beginning"
        " of its healing.",
    ),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom by a"
    " Father who has already seen everything in the file and spoken the verdict before"
    " you could organize a single document in your defense. Go gently with yourself."
    " The One who began the good work in you will be the one who finishes it \u2014 and he"
    " is neither surprised by the Vault nor impatient with the Ghost. He simply keeps"
    " coming to find what has been locked away."
)


def _three_column_table(rows=7):
    """Three-column journal table for Section 3 written reflection."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader_VG", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub_VG", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE EVENT", header_style),
         Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WAS I EXPOSED HERE?", header_style),
         Paragraph("what your nervous system concluded", sub_style)],
        [Paragraph("WAS MY SOUL IN DANGER?", header_style),
         Paragraph("the deeper question", sub_style)],
    ]
    data = [header_row] + [["", "", ""] for _ in range(rows)]
    tbl = Table(data, colWidths=[col_w] * 3,
                rowHeights=[0.55 * inch] + [0.5 * inch] * rows)
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
            "CalloutLabel_VG", fontName="Inter-SemiBold", fontSize=9, leading=13,
            textColor=ACCENT, leftIndent=12, spaceBefore=2, spaceAfter=4)))
    body.append(Paragraph(text, ParagraphStyle(
        "Callout_VG", fontName="Inter", fontSize=10.5, leading=17,
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
    """Generate the Vault+Ghost walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='VAULT', primary_breakdown='GHOST',
    primary_trigger='SHM', core_question='ACC'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="VAULT  \u00b7  GHOST",
        title="Take 139 Walkthrough \u2014 Vault + Ghost",
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
    story.append(Paragraph("The Vault \u00b7 The Ghost", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Shame \u00b7 Core Question: Am I acceptable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cWhen I kept silent, my bones wasted away<br/>"
        "through my groaning all day long.\u201d</i>",
        ParagraphStyle("cq_vg", parent=S["CoverSub"], fontSize=11,
                       leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Psalm 32:3",
        ParagraphStyle("cqa_vg", parent=S["CoverProfileSub"], fontSize=9)))

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
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ── SECTION 3: Core Question ──
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
        "Use the table below. In the first column, name a recent event in which the "
        "shame trigger fired. In the second, write what your nervous system concluded: "
        "<i>was I exposed here?</i> In the third, answer the deeper question: "
        "<i>was the part of me that finally matters \u2014 my soul, my standing before "
        "God \u2014 at any point in danger?</i>",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table())
    story.append(PageBreak())

    # ── SECTION 4: Mechanism ──
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Vault.",
                   "The one who keeps the interior close, processes alone, and shows only what has been chosen.")
    for p in VAULT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "How the Vault formed, and what it costs.",
                   "Four histories, and three things that do not get through the locked door.")
    for p in VAULT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in VAULT_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Vault.",
                   "Read his own words. He has been faithful; let him speak.")

    letter_style = ParagraphStyle(
        "VaultLetterVG", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    story.append(Paragraph(VAULT_LETTER_INSTRUCTION[0], S["BodyJ"]))
    story.append(Spacer(1, 8))
    divider(story)
    story.append(Spacer(1, 6))
    for para in VAULT_LETTER.strip().split("\n\n"):
        story.append(Paragraph(para.replace("\n", " "), letter_style))
    story.append(Spacer(1, 6))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in VAULT_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Ghost.",
                   "Not a performance of fine-ness. Simply the Vault, doing what it has always done.")
    for p in GHOST_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "Why this is the hardest Ghost to recover from.",
                   "The breakdown that needs no performance, and the distance it produces.")
    for p in GHOST_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in GHOST_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Come out from behind the door.",
                   "Two questions to sit with before you turn the page.")
    for prompt in GHOST_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same soul, in two modes of the same strategy.",
                   "The Vault and the Ghost are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=6)
    story.append(PageBreak())

    # ── SECTION 7: Tools ──
    tool_h = ParagraphStyle("ToolH_VG", parent=S["H3"], fontSize=10.5, leading=14,
                             spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody_VG", parent=S["BodyJ"], fontSize=10, leading=15,
                                spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "What to do when you feel the loop start.",
                   "Small enough to carry; honest enough to use.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Vault is overworking its defenses.",
                   "Five practices for the time before the Ghost is needed.")
    for name, desc in VAULT_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Ghost has closed in.",
                   "Five practices for after the wound is inside and the door has sealed.")
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


# ── STANDALONE TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "VAULT"
        primary_breakdown = "GHOST"
        primary_trigger = "SHM"
        core_question = "ACC"
        name = "Test User"

    # Print letter text first to verify no stray quote artifacts
    print("=== VAULT LETTER PREVIEW ===")
    print(VAULT_LETTER)
    print()
    print("=== BUILDING PDF ===")

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "vault_ghost_test.pdf")
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
        for page in reader.pages[1:4]:
            txt = page.extract_text() or ""
            if txt.strip():
                snippet = txt.strip()[:150]
                break
    except Exception:
        page_count = "unknown"
        snippet = ""

    print(f"DONE: vault_ghost.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
