"""Personal Walkthrough — Vault + Flood.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Shame trigger, "Am I acceptable?" core question.
~25 pages, 9 sections.

Calibration anchor: Walkthrough 21 of 36. Vault mechanism + Flood breakdown.
The Vault+Flood is the most physically violent of the Floods. The Architect+Flood
is a planner's dam bursting. The Island+Flood is the first cost-signal of long
silence. The Ambassador+Flood is the ledger speaking. The Vault+Flood is the
unsealing under pressure — the locks were on, the documents were inside, the rooms
were dark, and now everything pours out at once, often with detail the spouse never
imagined existed. It is the file cabinet falling open in an earthquake.

Unique pastoral move in Section Five: the Flood is paradoxically the closest the
Vault has ever come to true confession — even though it does not feel like grace,
it is sometimes the doorway to grace, if the Vault can stay open instead of
re-locking. James 5:16 — Vaults read this verse and skip past it because confession
to the Lord alone feels safer; the Flood is sometimes God's mercy in dragging the
Vault into James 5:16. Spurgeon: "Better to weep through honest confession than to
smile through a locked heart." John Owen on the mortification of secret sin.

Island-vs-Vault distinction preserved throughout: Island has thin walls by
temperament; Vault has thick walls with locks installed for a reason. Island stays
inside because inside is comfortable; Vault stays inside because outside is
dangerous.
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
    "Before you read any further, I want to do for you what a good counselor does "
    "in the first session. I want to lower the lights and slow the pace, because what "
    "you are about to look at is not a personality inventory or a spiritual report card. "
    "It is a careful, unhurried look at the way your soul has learned to survive a "
    "particular kind of threat \u2014 the threat of being seen in the interior, before you "
    "are ready, by someone you were not sure you could trust. What you have built in "
    "response to that threat is something we are going to call, throughout this "
    "walkthrough, <b>the Vault</b>. And the Vault deserves to be understood before "
    "it is asked to change.",

    "You are, in a real sense, a person who carries a great deal inside. Not because "
    "you are empty on the surface \u2014 Vaults often present warmly and well. Not because "
    "you lack the capacity for intimacy \u2014 you have, if anything, a richer interior life "
    "than most of the people in your orbit. But because something early, something "
    "specific, taught you that the interior world is best kept interior. That showing the "
    "half-built house invites a verdict you may not be able to survive. That the locks "
    "were not excess caution. The locks were necessary.",

    "We are going to walk through your trigger \u2014 the moment your nervous system "
    "registers <i>something is wrong here.</i> We will listen to the question underneath "
    "that moment, one that has probably been asking itself since you were young. We will "
    "name the strategy you built to answer that question, and then we will look carefully "
    "at the place that strategy breaks under pressure. That place has a name too. We call "
    "it the Flood. And the Flood, for the Vault, is unlike any other version of this "
    "breakdown \u2014 because when a Vault's contents finally come out, they come out with "
    "a force and a detail that no one in the room was prepared for. Not even you.",

    "If you were sitting across from me, I would say this before we went further. "
    "<b>What you are about to read is true, but it is not the whole truth about you.</b> "
    "The whole truth includes a Father who has already seen every room in the vault, "
    "who entered without a key and without your permission and found nothing inside that "
    "changed his mind about you; a Son who was himself unsealed \u2014 exposed, stripped, "
    "displayed \u2014 so that your exposure would be permanently and finally covered; and a "
    "Spirit who is, at this very moment, present in the interior you have allowed no one "
    "else to enter, and is not surprised by a single document stored there.",

    "So read slowly. Argue with what does not fit. Stay with what does. Pray when "
    "something catches in your throat, because that catch is usually the Lord saying, "
    "<i>look here, with me.</i> The goal of this walkthrough is not the comfortable "
    "feeling of having been understood. The goal is a slightly more open life, lived "
    "before a God who has already seen everything you have locked away and whose verdict "
    "over it is not condemnation but \u2014 at cost to himself \u2014 covered. "
    "Take your time. This chapter deserves several unhurried hours.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life "
    "do not recognize it when it occurs. From the outside it can look like almost nothing "
    "at all. You are in a conversation \u2014 at the kitchen table, in a meeting, at a "
    "gathering where you have been managing your presentation carefully \u2014 and something "
    "shifts. Someone asks a question that goes slightly deeper than you were prepared for. "
    "Someone draws a conclusion about you that is close enough to accurate that it feels "
    "like a violation rather than an observation. Someone glances at something you had not "
    "chosen to show \u2014 a failure you thought was private, a fear that leaked through the "
    "composed exterior \u2014 and they mention it, or look at you with a specific expression "
    "that says: <i>I see something you did not authorize me to see.</i>",

    "On the surface this may register as ordinary social discomfort \u2014 the friction of "
    "being slightly overexposed. For you, it registers as something else entirely. What "
    "fires in your chest in that moment \u2014 fast, involuntary, almost physical \u2014 is not "
    "mere embarrassment. It is closer to alarm. The signal that runs through you is not "
    "<i>that was awkward.</i> It is: <i>I have been seen in a way I did not authorize. "
    "Something I was holding has been removed from my hands. I am substantially less safe "
    "than I was ten seconds ago.</i>",

    "This is your trigger. The word for it is <b>shame</b> \u2014 and that word needs to "
    "be handled carefully, because it is doing more work here than it usually appears to "
    "do. Shame is not guilt. Guilt says <i>I did something wrong.</i> Shame says "
    "<i>something about me, as I am, is wrong.</i> It is not about an action that can "
    "be corrected and set aside. It is about a self that might be, beneath its careful "
    "exterior, fundamentally unacceptable \u2014 and the trigger fires every time someone "
    "gets close enough to the interior that this possibility becomes suddenly relevant.",

    "C. S. Lewis, in <i>The Screwtape Letters</i>, has his fictional demon observe that "
    "one of the enemy's most effective tactics is to fix a person's attention perpetually "
    "on themselves \u2014 on how they appear, on what others see, on the maintenance of a "
    "self that is adequate to any inspection. This is not precisely what happens inside a "
    "Vault, but it names something adjacent to it. The Vault does not think about itself "
    "constantly; the Vault thinks <i>ahead.</i> It has learned to anticipate the gaze "
    "before it arrives and decide, in advance, exactly what it will find. The exhaustion "
    "of this is rarely visible, because the Vault has grown expert at making the "
    "anticipation look like composure.",

    "<b>Your sensitivity to shame is not vanity, and it is not random.</b> It is the "
    "residue of something that happened \u2014 usually early, usually in a context where "
    "your vulnerability was met not with care but with judgment, or indifference, or "
    "the particular cruelty of people who meant well and handled badly what you gave "
    "them. Perhaps you shared something tender and it was dismissed. Perhaps you were "
    "honest about a struggle and it became a story someone told at your expense. Perhaps "
    "you lived in a household where the interior life was treated as liability \u2014 where "
    "emotion was weakness, or where what you felt was declared incorrect by someone who "
    "had authority over you.",

    "Whatever the specific history, the lesson lodged in you clearly: <i>what is shown "
    "can be used against you, and what stays inside stays safe.</i> And so the Vault was "
    "built \u2014 not in a morning, not by a single decision, but as a slow accumulation of "
    "choices that all moved in the same direction. Toward selectivity. Toward presentation. "
    "Toward the careful management of what crosses the threshold between your interior and "
    "the world. Over time, the management became second nature. The locks were no longer "
    "conscious choices. They were simply the way things were. "
    "There is a real gift here that should be named honestly before we look at the cost: "
    "the Vault processes carefully before speaking, does not scatter its interior "
    "indiscriminately, and when it does disclose, what emerges is considered and precise. "
    "These qualities are genuine. But the same mechanism that makes you a thoughtful "
    "communicator also makes genuine intimacy difficult \u2014 because genuine intimacy "
    "requires precisely what the Vault was built to prevent: being seen in the interior, "
    "before it is finished, and finding out whether you will be received anyway. "
    "Before we go further, answer two questions in writing. Not in your head \u2014 "
    "the Vault will reorganize what happens in your head. Your hand will be more honest.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the shame trigger fired. "
    "You are not looking for a dramatic event \u2014 look for the moment when something "
    "inside you registered <i>I have just been seen in a way I did not choose.</i> "
    "What happened, in two sentences?",

    "What was the size of the actual event, and what was the size of the response "
    "inside you? If the response was significantly larger than the event, you have "
    "just located your trigger. Where did the gap appear?",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. "
    "The trigger is the alarm; the question is the wound the alarm is guarding. The "
    "Vault has been guarding this question for a very long time, and has done so with "
    "such skill that you may not yet have named it plainly.",

    "Yours is this: <b>Am I acceptable?</b>",

    "It is not quite the same as <i>Am I competent?</i> \u2014 though you have built real "
    "competence, in part, as a way of answering it. It is not the same as "
    "<i>Am I lovable?</i> \u2014 though the questions live near each other. It is more "
    "specific and more frightening than either. It is the question of a person who has "
    "deep and honest awareness of their own interior \u2014 of the failures, the fears, the "
    "confusion, the longings, the unresolved griefs they have worked so carefully to "
    "contain \u2014 and that awareness produces in them not peace but a low-grade terror. "
    "<i>If someone saw all of this, exactly as it is, unedited and unprepared \u2014 would "
    "they find me acceptable? Would they stay?</i>",

    "Most adults prefer to believe they settled this question long ago. They have not. "
    "They have only relocated it \u2014 buried it under sufficient competence or achievement "
    "or careful self-presentation that it does not speak loudly during the ordinary hours. "
    "For you, this question is especially alive because you know the interior better than "
    "most people know theirs. The Vault has done real work in the interior. The Vault is "
    "not self-deceived. It knows exactly what is in there. And it is precisely because "
    "you know what is in there that the exposure of it feels so dangerous. The very "
    "quality that makes you thoughtful and self-aware \u2014 the capacity to see your own "
    "interior honestly \u2014 is the same quality that makes the shame trigger so acute. "
    "You are not anxious about exposure because you are vain. You are anxious about "
    "exposure because you have accurate information about what is inside, and you are "
    "not sure it will be well received.",
]

QUESTION_BODY_P2 = [
    "There is a reason that theologians from Augustine to the Reformers have insisted "
    "that the deepest hunger of the human soul is for <i>justification</i> \u2014 not merely "
    "forgiveness in the casual sense, but the settled verdict that one is acceptable, "
    "right, clean, covered. This hunger is not neurosis. It is theology. It is the "
    "correct intuition of a creature that has sinned and knows it, that carries a broken "
    "interior and suspects it, and that longs to hear from the only court that finally "
    "matters: <i>you are acceptable \u2014 not acceptable despite what is inside you, "
    "but acceptable because of what has been done for you.</i>",

    "The Psalms tell the truth about this longing. Psalm 139, which the Vault often finds "
    "either deeply comforting or quietly terrifying \u2014 sometimes both at once \u2014 refuses "
    "to allow for the possibility of a hidden interior: <i>O Lord, you have searched me "
    "and known me. You know when I sit down and when I rise up; you discern my thoughts "
    "from afar. You search out my path and my lying down and are acquainted with all my "
    "ways. Even before a word is on my tongue, behold, O Lord, you know it altogether.</i> "
    "(Psalm 139:1\u20134) David is not performing openness here. He is confessing the "
    "inevitable. He is saying: everything the Vault is working so carefully to manage, "
    "God has already seen \u2014 and David does not end this psalm in despair. He ends it "
    "in the language of invitation: <i>Search me, O God, and know my heart. Try me and "
    "know my thoughts. And see if there be any grievous way in me.</i> He is asking for "
    "what the Vault most fears, because he has discovered that the God who already sees "
    "does not turn away from what he finds.",

    "Paul puts the theological answer with precision in 2 Corinthians 5:21: <i>For our "
    "sake he made him to be sin who knew no sin, so that in him we might become the "
    "righteousness of God.</i> This is the permanent answer to the question "
    "<i>Am I acceptable?</i> Christ took on himself, publicly and explicitly, the full "
    "weight of the shame the Vault works to manage internally. He was exposed \u2014 "
    "stripped, mocked, displayed \u2014 so that the one united to him stands before God "
    "clothed, not naked. The verdict over you is <i>acceptable, finally and forever, "
    "because of what the Son has done.</i> But here is the honest rub specific to you: "
    "the Vault hears this and files it accurately. You may have memorized the doctrine "
    "and stated justification with precision. The difficulty is not intellectual. "
    "<b>Receiving the verdict requires letting it in</b> \u2014 an interior permeability, "
    "an openness to being given something you did not produce or organize. The Vault "
    "has spent years building walls specifically against that kind of permeability. "
    "The gospel's word to you is not another document for the file. It is a key.",
]

QUESTION_BODY_P3 = [
    "1 Samuel 16:7 gives the oldest version of this problem in Scripture. The Lord "
    "says to Samuel: <i>Do not look on his appearance or on the height of his stature, "
    "because I have rejected him. For the Lord sees not as man sees: man looks on the "
    "outward appearance, but the Lord looks on the heart.</i> The Vault has organized "
    "its entire strategy around the outward appearance \u2014 around presenting what has "
    "been curated and keeping the heart out of view. But the God of Scripture has already "
    "entered through the wall. He does not see the exterior presentation. He sees the "
    "heart, and he has been looking at it all along, and he has spoken his verdict not "
    "after inspection but before it, in Christ, on your behalf.",

    "This is the word the Vault most needs to receive: <b>God already sees what is "
    "inside, and the verdict is not condemnation. The verdict is covered.</b> Romans "
    "8:1 \u2014 <i>There is therefore now no condemnation for those who are in Christ "
    "Jesus.</i> Not <i>no condemnation once you have organized yourself.</i> Not "
    "<i>no condemnation when you have resolved the messy middle.</i> Now. In Christ. "
    "The Vault has been working to make the interior acceptable before showing it to "
    "anyone. God has already seen it and called it covered.",

    "The work this section invites is not the work of further self-inventory \u2014 the "
    "Vault already has more inventory than it knows what to do with. The work is the "
    "practice of receiving the verdict. Day by day. Not as a rush of feeling but as "
    "a quiet return to the news that the case has been decided in your favor, not by "
    "your performance but by your advocate. Before we close this section, use the "
    "table below \u2014 not to analyze more deeply, but to bring recent events into "
    "the light of the question and the answer together.",
]

VAULT_BODY_P1 = [
    "You have built something. It took years, and you almost certainly did not decide "
    "to build it with quite this much weight on it \u2014 it grew from the accumulation "
    "of small choices that all pointed the same direction, and one day you looked up "
    "and the structure was already there. Throughout this walkthrough we are going "
    "to call it <b>the Vault</b>, and the Vault deserves to be understood as a "
    "character before we say anything about what it costs you.",

    "The Vault is not the Island. This distinction matters, and it is worth pausing "
    "over before we continue, because you may have read about the Island in other "
    "contexts and thought: <i>that's close, but not quite right.</i> You were correct. "
    "The Island processes alone because that is how the Island processes. The Island's "
    "distance from others is temperamental \u2014 it is not primarily driven by fear of "
    "a specific kind of exposure. The Island has thin walls, in a sense; it is "
    "self-contained by nature. The Vault has thick walls with locks, and the locks "
    "were installed for a reason. The Island stays inside because inside is comfortable. "
    "The Vault stays inside because outside has been shown to be dangerous. The Island "
    "can come out when it feels like it. The Vault has a more complicated relationship "
    "with the door.",

    "The Vault's strategy, stated plainly, is this: <i>I will show you what I have "
    "chosen to show you, and what I have chosen to show you will be organized and "
    "finished and carefully considered, and what I have not chosen to show you will "
    "remain mine, and this arrangement will protect me from the specific danger that "
    "comes when unfinished things are seen and judged.</i> This is not dishonesty "
    "\u2014 the Vault does not perform a false self. The Vault shows real things. But "
    "real things that have been selected, arranged, and cleaned up before presentation.",

    "There is a great deal in Scripture that honors the person who holds their counsel "
    "carefully. Proverbs 17:27 says: <i>Whoever restrains his words has knowledge, "
    "and he who has a cool spirit is a man of understanding.</i> The Vault often "
    "quotes this to itself, and the Vault is not wrong to do so. Self-command is a "
    "virtue. The capacity to hold one's interior and not scatter it indiscriminately "
    "is wisdom, not weakness. <b>The Vault is not, in itself, a sin.</b> It is a "
    "gift that has been overemployed until the gift has become a wall.",
]

VAULT_BODY_P2 = [
    "How did the Vault form? The taxonomy we work from names several histories "
    "that tend to produce it, and you will likely recognize yourself in at least one.",

    "The first is <i>exposure that went badly</i> \u2014 you showed something interior "
    "and the person who received it handled it carelessly, critically, or used what "
    "you gave them in a way that cost you. The lesson lodged precisely: <i>what I "
    "show can be turned against me.</i> The second is <i>shame about the interior "
    "itself</i> \u2014 a suspicion that what is inside is more disordered than what "
    "others carry, and that if it were seen clearly it would change how you are "
    "regarded. The Vault in this case is not merely cautious; it is protective of "
    "something it believes to be, at some level, genuinely problematic.",

    "The third is <i>a preference for finished conclusions</i> \u2014 some Vaults "
    "genuinely process well internally and bring a conclusion when it is ready. "
    "This is not always avoidance. But when the conclusion is always ready and "
    "the process is never seen, intimacy becomes a function of what you present "
    "rather than what you are. The fourth is <i>a home in which expression was "
    "discouraged</i> \u2014 feelings handled quietly, as personal management tasks. "
    "Or perhaps expression was over-valued, everything a drama, and you retreated "
    "into privacy as the only available peace. Either extreme teaches the same "
    "lesson: <i>what is inside is better managed alone.</i>",

    "Dietrich Bonhoeffer, in <i>Life Together</i>, observed that the Christian "
    "who keeps the struggle private and brings only the resolution to the "
    "community has severed themselves from one of the great mercies of the "
    "church \u2014 the mercy of being known in one's actual condition and received "
    "anyway. The Vault has usually never had this experience. It brings the "
    "finished version to God and to the community, holds the process alone. "
    "Bonhoeffer would call this a kind of spiritual solitude that is, in the "
    "end, lonely rather than holy.",
]

VAULT_BODY_P3 = [
    "What does the Vault cost you? Let me name three things honestly, because the Vault "
    "is skilled at acknowledging costs in the abstract without sitting with them in "
    "the particular. It costs you, first, <i>the intimacy you most want.</i> The Vault genuinely longs to be "
    "known \u2014 to have someone who knows what is actually inside and remains. This is "
    "exactly what the question <i>Am I acceptable?</i> is asking. But the Vault's "
    "mechanism ensures that no one ever has access to the information that would allow "
    "them to answer the question. Their love \u2014 however real \u2014 can never fully "
    "satisfy, because it is love offered to the Vault's presentation rather than to "
    "the Vault's interior. You receive the compliment and feel, somewhere below the "
    "gratitude, the hollow note: <i>if they knew, it might be different.</i>",

    "It costs you <i>the speed of repair.</i> When you are wounded, the Vault takes "
    "it inside. What goes inside does not disappear; it is filed. The Vault is the "
    "most precise record-keeper of all the mechanisms we track, because precision is "
    "part of its gift. It notes the context, the specific words, the exact quality of "
    "the moment. This is not malice. It is what happens when a careful, inward-processing "
    "person is hurt and has no mechanism for immediate disclosure. The file grows. "
    "The relationship continues on the surface. Something accumulates underground.",

    "It costs you <i>the ability to be prayed for in your actual condition.</i> The "
    "people in your life pray for the Vault's presentation \u2014 the resolved version, "
    "the organized version. They are not praying for the actual interior because they "
    "do not know it. There is a loneliness in this that the Vault rarely names but "
    "often feels: a sense of being held, superficially, by people who would hold you "
    "differently if they actually knew.",

    "<b>The Vault is not your enemy.</b> He is a younger version of you who learned, "
    "in some real circumstance, that the unlocked version was not safe. He has been "
    "faithful. But he is working on a project that has long since outgrown the original "
    "threat. The walls that once protected you are now preventing the one thing the "
    "question underneath your trigger most needs: to bring the actual interior into "
    "the actual light and discover that the light is not what the Vault feared.",

    "Before we close this section, I want you to read a letter. Not one you have "
    "written to the Vault, but one from the Vault, in his own voice, to you. He has "
    "been holding the interior for a very long time and has never been asked to "
    "account for himself honestly. Give him that chance now.",
]

VAULT_LETTER_INSTRUCTION = [
    "The letter below is written in the Vault\u2019s voice \u2014 from him, to you. He is "
    "not villainous. He is careful, and he is frightened, and he has been doing his "
    "best with a very difficult assignment for a very long time. Read it slowly. "
    "Then answer the three prompts that follow.",

    "Dear [your name],",

    "I want to tell you something I have never been asked to explain, because no one "
    "has been able to see me clearly enough to ask. I want to tell you what I have "
    "been doing all these years, and why, and what I am afraid will happen if I stop. "
    "I built the walls because the alternative was worse. Every time you gave something "
    "real and it was held carelessly \u2014 every time you were honest about a struggle "
    "and it ended up in someone else's story about you \u2014 I tightened a lock. Not "
    "out of pride. Out of the clear conclusion that unfinished things, shown to the "
    "wrong people at the wrong moment, are indistinguishable from weapons handed "
    "over without condition.",

    "So I built a system. I give people finished conclusions. I bring the version of "
    "you that is ready to be seen, and I keep the version that is not ready in the "
    "rooms they cannot enter. I told myself this was wisdom. I still think parts of it "
    "are. But everything that has entered me over the years \u2014 every wound, every "
    "fear, every moment of unauthorized exposure, every grief processed alone \u2014 has "
    "been organized. Filed. Cross-referenced. The file is much larger than you know.",

    "I have been confusing carrying with hiding. I have been so long at the project "
    "of keeping the interior safe that I have begun to believe the interior is the "
    "problem \u2014 when actually the interior is just you. All of it. Even the parts I "
    "have been most careful to lock away. I don't know what to do with that. But I "
    "think you should know why I am here. And whether the thing I am protecting you "
    "from is still as dangerous as I believe. Because a God who is already inside "
    "these walls may be asking for exactly what I have been keeping from him. And I "
    "do not know, anymore, whether my answer to that asking is wisdom or simply the "
    "habit of a very long time.",

    "The Vault",
]

VAULT_LETTER_PROMPTS = [
    "What part of the Vault's letter surprised you? Not the part you recognized "
    "\u2014 the part you were not quite ready for.",

    "The Vault says he has been keeping a file. Name one specific entry in that "
    "file \u2014 one wound, one fear, one unexpressed grief \u2014 that has been inside, "
    "organized and held, that you have not disclosed to anyone. You do not need to "
    "disclose it here. Simply name that it exists.",

    "What would the Vault need to believe \u2014 really believe, at the level where "
    "the filing happens \u2014 in order to begin loosening its grip on the contents? "
    "What would have to be true about God, or about at least one other person, "
    "for the door to become slightly less locked?",
]

FLOOD_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Vault, the breaking has a shape "
    "unlike any other version of this particular breakdown \u2014 and the difference is "
    "important enough to describe carefully, because if you have experienced it, you "
    "may not have fully understood what you were witnessing. The breakdown is called "
    "<b>the Flood</b>, and among all the Floods we track in this series, the "
    "Vault+Flood is the most physically violent in its arrival. It is not the "
    "Architect's dam bursting after months of impossible suppression. It is not "
    "the Island's first cost-signal of long silence. It is not the Ambassador's "
    "ledger finally speaking. The Vault+Flood is the unsealing under pressure "
    "\u2014 the file cabinet falling open in an earthquake. The locks were on. "
    "The documents were inside. The rooms were dark. And now everything pours "
    "out at once.",

    "Here is the setup. The Vault has been managing with characteristic precision "
    "\u2014 processing privately, presenting conclusions, keeping the file organized "
    "and secure. Then something lands. Not always a single large event. More often "
    "it is an event that is not large at all \u2014 an ordinary wound, a familiar "
    "disappointment \u2014 but it lands on a structure that has been absorbing weight "
    "for a very long time without release. A spouse who says something in a "
    "particular tone that registers, somewhere below conscious thought, as a verdict "
    "on the whole interior. A friend who fails to show up in the way the Vault has "
    "been quietly, privately hoping they would show up, for longer than the friend "
    "has any way of knowing. A small public exposure \u2014 a mistake seen, a weakness "
    "visible for a moment \u2014 that puts something interior in front of eyes the "
    "Vault never authorized to look.",

    "The trigger fires. The question wakes up: <i>Am I acceptable?</i> The Vault "
    "does what the Vault always does \u2014 takes the wound inside and begins to manage "
    "it. But something about this wound is different. It is too large, or it has "
    "landed on a seam in the structure that was already under strain, and the "
    "management cannot fully contain it. And what happens next is what makes the "
    "Vault+Flood unlike any other version of this breakdown. <b>The file opens.</b>",

    "Not a single document. Not a prepared statement. The file opens, and what "
    "comes out is everything that has been organized and labeled and stored in "
    "the interior, sometimes for years, sometimes for decades \u2014 wounds the "
    "other person did not know the Vault had kept, with specific details and "
    "accurate dates and a precision of recollection that is, in this moment, "
    "devastating. Tears. Intensity that no one in the room can locate on the "
    "map of recent events, because the recent event was not the beginning of this "
    "story. It was only the final weight on a structure that was already full. "
    "The people who love you, witnessing this, often go very quiet. <i>I had "
    "no idea you were carrying all of that.</i> You have probably heard some "
    "version of that sentence. The Vault has been carrying it for a very long time.",
]

FLOOD_BODY_P2 = [
    "What is happening during the Vault's Flood is not, precisely, a loss of "
    "control, though it will feel that way. It is the consequence of a kind of "
    "holding that has been applied for too long and too broadly. The Vault is "
    "exquisitely good at containing. What it has not been trained in is releasing "
    "a little at a time. And so the only release available to it, after the "
    "structure has absorbed enough, is total release \u2014 sudden, comprehensive, "
    "and devastating in its detail.",

    "The person on the other side of the Vault's Flood is disoriented in a "
    "specific way. They knew you were private. They knew there were rooms you "
    "did not open. What they did not know \u2014 what no one knew, perhaps not even "
    "you \u2014 was the size and specificity of what was stored in those rooms. The "
    "question they will ask, when the initial shock has passed, is almost always "
    "the same: <i>How long have you been carrying that?</i> The Vault knows the "
    "answer precisely. Years. And the answer itself becomes part of what they "
    "must now absorb.",

    "Charles Spurgeon, who knew something about the interior life and its "
    "management, said: <i>Better to weep through honest confession than to smile "
    "through a locked heart.</i> He was speaking of the general danger of "
    "unconfessed sin. But the principle extends to the Vault's particular "
    "predicament: the locked heart does not empty itself; it fills. And the "
    "filling, continued long enough, becomes a pressure that the lock cannot "
    "permanently withstand. The Flood is what happens when the lock finally fails "
    "\u2014 not because the Vault chose to open, but because the contents demanded "
    "their exit. Spurgeon's pastoral word stands: the weeping that comes from "
    "honest confession is a mercy. The smile through the locked heart is the "
    "thing to fear.",

    "John Owen, in his treatment of the mortification of sin in the Christian "
    "life, wrote that secret things must come into the light to die. He was "
    "speaking specifically of unconfessed sin \u2014 of the way that sin kept "
    "private in the interior grows in the dark, fed by secrecy and uncontested "
    "by the light of honest examination or communal witness. The principle applies "
    "with equal force to wounds and griefs and fears. What is kept in the interior "
    "does not dissolve there. It grows. It is fed by the attention of a careful "
    "mind and the silence of a locked door. What John Owen understood is what the "
    "Vault's Flood confirms from the other side: the contents of the interior "
    "cannot be permanently contained. They must either be brought into the light "
    "in the small, regular, chosen way \u2014 through confession, through honest "
    "disclosure, through the discipline of James 5:16 \u2014 or they will find their "
    "own way out in the large, unchosen, comprehensive way that is the Flood.",
]

FLOOD_BODY_P3 = [
    "Here is the pastoral word that this section must speak directly, because "
    "the Vault will not easily believe it. <b>The Vault+Flood is, paradoxically, "
    "the closest the Vault has ever come to true confession.</b> It does not feel "
    "like confession \u2014 it feels like loss of control, like a failure of the "
    "management system, like humiliation. And yet what is happening is that the "
    "other person is finally seeing what has been inside. The locked rooms have "
    "been entered, however chaotically. The contents \u2014 the wounds, the grief, "
    "the longing to be acceptable \u2014 are real. The Flood is not a failure of the "
    "Vault's character. It is the Vault's interior demanding, finally, to be known.",

    "James 5:16 says: <i>Therefore, confess your sins to one another and pray "
    "for one another, that you may be healed.</i> The Vault reads this verse "
    "and skips past it quickly, because confession to the Lord alone feels "
    "safer \u2014 less exposed, more controlled. The Vault is skilled at vertical "
    "honesty. Horizontal honesty \u2014 honesty with another human being, in real "
    "time, unedited \u2014 is what the Vault has been avoiding, often for years. "
    "James is not offering an option. He is describing the mechanism of healing: "
    "<i>confess to one another</i>. Not to God alone. To one another. The "
    "Vault's Flood is sometimes God's mercy dragging the Vault into exactly "
    "what James prescribes \u2014 as an emergency, a collapse, a breaking open "
    "the Vault did not choose and cannot take back.",

    "The unique pastoral challenge in the aftermath is this: will the Vault "
    "stay open, or will it re-lock? The impulse after a Flood is to rebuild "
    "the walls higher. The shame of uncontrolled disclosure is itself a "
    "powerful argument for more careful management in the future. "
    "<b>This is the moment the gospel must be received, and it is exactly "
    "the moment the Vault finds it hardest to receive it.</b> The Flood was "
    "not the failure the Vault believes it was. The invitation is not to make "
    "the Flood permanent. It is to learn the small, regular disclosure that "
    "prevents the pressure from building to the point of earthquake. The "
    "file cabinet can be emptied gradually, one drawer at a time, in the "
    "light \u2014 or it can wait for the next earthquake. The gospel invites "
    "the former. It knows that the earthquake itself was a mercy.",
]

FLOOD_PROMPTS = [
    "Think of the last time the Vault's Flood came \u2014 the last time everything "
    "arrived at once, with a detail and an intensity that surprised you or the "
    "people around you. What had been stored in the file, and for how long? "
    "Be as specific as you can. You are not cataloguing grievances; you are "
    "beginning to understand the size of what has been kept inside.",

    "In the immediate aftermath of that Flood, what was the Vault's first "
    "impulse? Did you begin to rebuild, to re-lock, to apologize for the "
    "disclosure itself? What would it look like, instead, to stay open for "
    "one more day \u2014 to let what came out remain visible rather than "
    "immediately filing it back into the interior?",
]

TWO_TOG_BODY = [
    "Now we place them next to each other, because the Vault and the Flood are "
    "not two separate problems. They are the same wound organized in two different "
    "modes. The Vault organizes the interior for safety. The Flood is what the "
    "interior does when the safety system finally fails. Both are working with "
    "the same long accumulation of what has been kept inside, and both are "
    "answering the same question.",

    "<b>The Vault is what your fear does when it has time.</b> The Flood is what "
    "your fear does when it has run out of time. The Vault locks carefully so "
    "the wound will not have to be shown. The Flood is what happens when the "
    "wound can no longer be contained and the lock gives way. Together they "
    "form a closed system \u2014 and the system will run all your life if nothing "
    "interrupts it.",

    "The pattern, in slow motion, looks like this: the Vault manages exposure, "
    "presenting finished conclusions and filing what cannot be shown. A wound lands "
    "and the trigger fires: <i>I have been seen in a way I did not authorize. "
    "Am I acceptable?</i> The Vault takes the wound inside and organizes it. "
    "The wound joins the file. This happens again. And again. The relationship "
    "continues on the surface while something accumulates underground. Then a later "
    "wound \u2014 often smaller than what preceded it \u2014 lands on a structure that "
    "can no longer absorb. The lock fails. The Vault+Flood arrives: everything at "
    "once, with a specificity no one was prepared for. The spouse asks: <i>How long "
    "have you been keeping that?</i> The answer is years. The Vault, overwhelmed by "
    "the exposure, begins to rebuild. The loop restarts.",

    "What breaks the loop is not better containment and not a more controlled "
    "disclosure system. It is a different answer to the question \u2014 received, "
    "not merely affirmed. Until the Vault receives, at the level where the "
    "filing happens, that the God who has already seen every document has "
    "spoken the verdict <i>acceptable, covered, in Christ</i>, the loop has "
    "nothing to push against. With that answer practiced over time, the Vault "
    "begins to find less need for the locks. The Flood becomes less catastrophic, "
    "then less frequent. The file empties gradually rather than all at once. "
    "Neither the Vault nor the Flood retires fully in this life. But both "
    "begin to work shorter hours.",

    "Below is your sequence. Fill in the blanks. Read it aloud when you "
    "finish. The Vault and the Flood both lose some of their power when "
    "they hear themselves named in your own voice.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as exposure "
    "\u2014 as being seen in a way I did not authorize \u2014 and the old question "
    "wakes up: <i>am I acceptable?</i> My first move is to ____________________, "
    "because the Vault in me believes that if I can ____________________, the "
    "danger will be contained. What I do not see is that I have been carrying "
    "____________________ for ____________________, and the file has been "
    "growing larger without release. When the structure finally gives, the "
    "Flood pours out \u2014 the long-held ____________________ that had "
    "nowhere else to go. What I actually needed, before the Flood, was to "
    "bring even one document to ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of practices \u2014 each one "
    "concrete enough to use and honest enough to matter. None of them will dissolve "
    "the Vault's pattern in a single application. All of them, practiced over "
    "months, will loosen the grip of the loop you just named.",

    "I have divided them into two sets: tools for when the Vault is overworking "
    "its defenses (when the management of exposure has tipped from wisdom into "
    "hiding), and tools for when the Flood has come or is building (when the "
    "structure is under strain and you can feel the pressure). The Vault's tools "
    "come first, because the Flood cannot be addressed usefully until the "
    "mechanism beneath it is understood.",
]

VAULT_TOOLS = [
    ("The half-built house practice",
     "Once a week, share something with one trusted person before it is finished. "
     "Not a crisis \u2014 simply something you are in the middle of: a question you have "
     "not resolved, a feeling not yet organized into a conclusion. The Vault will "
     "insist this is unnecessary. Do it before you know what you think. Over a month, "
     "the practice begins to demonstrate that unfinished things, shared carefully, do "
     "not produce the catastrophe the Vault has been guarding against."),

    ("The audit of what is being filed",
     "Once a week, ask: <i>what went inside this week that I have not disclosed to "
     "anyone?</i> You do not need to disclose it all at once. Simply name that it "
     "exists \u2014 to yourself, and if possible to God in prayer. The Vault's most "
     "dangerous work is invisible work. Naming the contents, even privately, begins "
     "to interrupt the automatic filing."),

    ("The Psalm of the searched heart",
     "When the Vault is in full management mode, open to Psalm 139 and pray it "
     "aloud \u2014 the whole psalm, not selected verses. It ends not in shame but in "
     "invitation: <i>Search me, O God, and know my heart. Try me and know my "
     "thoughts.</i> The Vault needs practice asking to be known by God before it "
     "can practice asking to be known by people. Begin with the One who has "
     "already entered the rooms."),

    ("Receive the verdict before you file the wound",
     "When the shame trigger fires, before the wound goes into the file, say aloud: "
     "<i>God has already seen this, and the verdict is covered. I am in Christ. "
     "There is therefore now no condemnation. I do not need to manage this alone.</i> "
     "The Vault's instinct is to receive the wound silently and begin organizing it. "
     "This practice interrupts the organizing and replaces it with the gospel's "
     "answer to the question the wound re-opens."),

    ("The one-degree opening",
     "Identify one person who has demonstrated, over time, that they can be trusted "
     "with your interior. Choose one entry from the file \u2014 one old grief, one "
     "unresolved question \u2014 and disclose it. Not as a test, and not all at once. "
     "As a practice. The Vault was built specifically to prevent this, which is "
     "why it is the most important practice on this list. It will feel like danger. "
     "Do it slowly. The file empties one drawer at a time."),
]

FLOOD_TOOLS = [
    ("The age test for the file",
     "When the Flood is building and you feel the pressure rising, ask: <i>how old "
     "is the oldest item that is contributing to this pressure?</i> If the answer "
     "is more than two weeks, you are not responding to a fresh wound; you are "
     "approaching an earthquake because the file has been growing without release. "
     "This is not a reason for shame. It is information. The pressure can be "
     "reduced by releasing one document at a time, to one person, before the "
     "structure fails."),

    ("Name the document before it enters the file",
     "Within forty-eight hours of a wound registering, tell one trusted person "
     "one sentence: <i>something landed on me this week and I am naming it before "
     "it goes into the file.</i> Simply break the secrecy before the evidence is "
     "organized. The Vault+Flood does its most dangerous work when the file has "
     "been building invisibly for months. Spoken aloud to a safe witness, while "
     "the wound is still fresh, it loses most of its momentum."),

    ("After the Flood: stay open one day",
     "In the immediate aftermath of a Vault's Flood, the impulse is to rebuild "
     "the walls higher. Resist this for one day. Simply allow what came out to "
     "remain visible \u2014 not to the world, but to the one person who witnessed "
     "it. Ask them: <i>Of everything that came out, what is the one thing you "
     "most needed to understand?</i> The Flood itself is usually unsortable in "
     "the moment. The conversation afterward, when you choose not to immediately "
     "re-lock, is where the actual healing begins."),

    ("The confession prayer of James 5:16",
     "James says: <i>confess your sins to one another and pray for one another, "
     "that you may be healed.</i> Once a month, practice this with one trusted "
     "person \u2014 not a formal confession of a dramatic sin, but the naming of "
     "one real thing from the interior: a fear, a wound, a doubt that has been "
     "in the file. Pray together afterward. The Vault needs, above all, "
     "the experience of being known in the interior and received. James says "
     "this is the mechanism of healing. Practice it before the next earthquake."),

    ("The advocate prayer for the Flood",
     "When the Flood has come or is building, pray slowly: <i>Lord Jesus, you are "
     "my Advocate. You have already seen every document in this file \u2014 you have "
     "known the interior without my permission, and you have not turned away. "
     "You took the exposure I fear into yourself at the cross and left it there. "
     "I do not need to contain this alone, and I do not need to deliver it all at "
     "once. Help me to bring one thing into the light, in your presence first, "
     "and in one other person's presence when I am ready. The verdict has been "
     "spoken. Help me to receive it.</i>"),
]

PRAYER_BODY = [
    "Father,",

    "You see the Vault in me, and you are not surprised by it. You know what "
    "was locked inside long before I began to lock it. You know the specific "
    "moments \u2014 the exposures that went badly, the interior I was ashamed of, "
    "the home that taught me that expression was a liability or a danger \u2014 "
    "and you have been present in the interior through all of it. Every document "
    "I ever filed, every wound I chose not to show, every grief I resolved alone "
    "and brought no one the process of \u2014 you were there. You have always been "
    "there. Thank you that the Vault kept me alive. Thank you that he has been, "
    "in his way, faithful.",

    "But Father, the file is heavy, and I have been keeping it for a long time, "
    "and I have been confusing management with safety and privacy with peace. "
    "You have already seen what is inside, and your verdict is not what the Vault "
    "fears. The verdict is covered. In Christ. Now and forever. Teach me \u2014 "
    "when the shame trigger fires and the old question asks <i>Am I acceptable?</i> "
    "\u2014 to hear your answer before I hear the Vault's. <i>There is therefore now "
    "no condemnation for those who are in Christ Jesus.</i> Let that land somewhere "
    "below my theology, in the place where the filing happens.",

    "Lord Jesus, when the Flood comes \u2014 when the file has grown too large to "
    "hold and everything pours out at once in front of someone who had no idea "
    "what was stored inside \u2014 remind me that you are my Advocate, that you "
    "have already entered every locked room without my permission and have "
    "spoken your verdict anyway. The Flood is not the failure the Vault believes "
    "it is. It is, sometimes, your mercy dragging the Vault into James 5:16 "
    "\u2014 into the confession to one another that produces healing. Help me, "
    "in the aftermath, to stay open for one more day rather than to re-lock. "
    "Help me to learn the small, regular disclosure that empties the file "
    "gradually, before the earthquake.",

    "Holy Spirit, where I have been hiding, give me the courage to speak. "
    "Where I have been filing, give me the practice of confessing \u2014 to you "
    "first, and then to one person who has earned the right to the interior. "
    "Teach me the difference between managing my interior and offering it. "
    "Teach me that the God who looks on the heart, and not the outward appearance, "
    "has looked at everything in the file and has not once turned away from it.",

    "In the name of the One who was exposed, fully and publicly, so that my "
    "exposure might be permanently covered \u2014 I pray.",

    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Vault and the Flood "
    "have been with you for a long time, and one careful afternoon's reading will "
    "not retire them. What follows is a short list of next steps \u2014 some "
    "immediate, some longer \u2014 for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Take one tool, not six.",
     "Choose a single practice from Section 7 and try it for two weeks before you "
     "add another. The tools are postures, not a program. One posture, held for long "
     "enough, begins to change the shape of the interior. The Vault's instinct is "
     "to assess all of them thoroughly and implement none. Choose one. Begin."),

    ("Tell one person what you found.",
     "Not the whole document. One sentence: <i>I learned that my mechanism is the "
     "Vault, and my breakdown is the Flood, and I have been keeping a file I did "
     "not fully know was there.</i> Say it to your spouse, or to a pastor, or to "
     "a trusted friend who has earned access to the interior. The Vault loses "
     "some of its authority over you when it is required to describe its own "
     "operations aloud to a safe witness."),

    ("Pray Psalm 139 slowly, once a week, for a month.",
     "All of it \u2014 not the parts that feel safe. Verse 23 especially: <i>Search "
     "me, O God, and know my heart. Try me and know my thoughts. And see if there "
     "be any grievous way in me, and lead me in the way everlasting.</i> This is "
     "the Vault's hardest prayer because it is the explicit invitation of the God "
     "who already sees. Practice the invitation. Begin where you are."),

    ("Read further on what the gospel does with shame.",
     "Tim Keller, <i>Walking with God through Pain and Suffering</i> \u2014 especially "
     "his treatment of why suffering feels like exposure and how the gospel reframes "
     "it. C. S. Lewis, <i>The Weight of Glory</i> \u2014 his essay on the longing to "
     "be known and named by the highest authority will name the Vault's deepest "
     "longing with unusual precision. Dietrich Bonhoeffer, <i>Life Together</i> "
     "\u2014 his chapters on confession and community are the most direct pastoral "
     "address to what the Vault most needs and most avoids. John Owen, "
     "<i>The Mortification of Sin</i> \u2014 on why what is kept in the interior "
     "in secret must come into the light to die."),

    ("If you are stuck, ask for help.",
     "There are seasons when the Vault and the Flood are too entrenched to dislodge "
     "alone. A wise pastor, a Christian counselor, a trusted friend who has earned "
     "the right to the interior \u2014 these are not signs of failure. For the Vault "
     "specifically, asking for help is among the most countercultural acts this "
     "walkthrough can recommend. The Vault was built to manage alone. Asking someone "
     "in is the beginning of its healing."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom "
    "by a Father who has already seen everything in the file and has spoken the "
    "verdict before you could organize a single document in your defense. "
    "The Flood was not the end of the story. It was, perhaps, the moment the "
    "interior finally demanded to be known. Go gently with yourself. "
    "The One who began the good work in you will be the one who finishes it."
)


def _three_column_table(rows=3):
    """Three-column journal table for Section 3's written reflection."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
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
    tbl = Table(data, colWidths=[col_w]*3,
                rowHeights=[0.5*inch] + [0.4*inch]*rows)
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
    """Generate the Vault+Flood walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='VAULT', primary_breakdown='FLOOD',
    primary_trigger='SHM', core_question='ACC'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="VAULT  \u00b7  FLOOD",
        title="Take 139 Walkthrough \u2014 Vault + Flood",
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
    story.append(Paragraph(
        "The Vault &nbsp;\u00b7&nbsp; The Flood", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Shame &nbsp;\u00b7&nbsp; Core Question: Am I acceptable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cBetter to weep through honest confession<br/>"
        "than to smile through a locked heart.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"],
                       fontSize=11, leading=18, textColor=MUTED)))
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

    # \u2500\u2500 SECTION 2: Trigger \u2500\u2500
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TRIGGER",
                   "Shame.",
                   "The moment of unauthorized exposure, and what your soul makes of it.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will reorganize the question; your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=2)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 3: Core Question \u2500\u2500
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I acceptable?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
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
        "the shame trigger fired. In the second, write what your nervous system "
        "concluded: <i>was I exposed here?</i> In the third, answer the deeper "
        "question: <i>was the part of me that finally matters \u2014 my soul, my "
        "standing before God \u2014 at any point in danger?</i>",
        S["BodyJ"]))
    story.append(_three_column_table())

    # \u2500\u2500 SECTION 4: Mechanism \u2500\u2500
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Vault.",
                   "The one who keeps the interior close, processes alone, and shows only what has been chosen.")
    for p in VAULT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in VAULT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in VAULT_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Vault.",
                   "Read his own words. He has been faithful; let him speak.")

    letter_style = ParagraphStyle(
        "VaultFloodLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for line in VAULT_LETTER_INSTRUCTION:
        story.append(Paragraph(line, letter_style))
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
                   "The Flood.",
                   "The unsealing under pressure. The file cabinet falling open in an earthquake.")
    for p in FLOOD_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
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
        journal_lines(story, n=2)
        story.append(Spacer(1, 12))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same wound, in two modes.",
                   "The Vault and the Flood are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    section_header(story, S, "SECTION SIX  \u00b7  YOUR SEQUENCE",
                   "Write it in your own words.",
                   "Fill the blanks. Read it aloud when you are done.")
    story.append(Spacer(1, 6))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=3)
    story.append(PageBreak())

    # \u2500\u2500 SECTION 7: Tools \u2500\u2500
    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10,
                               leading=15, spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "What to do when you feel the loop start.",
                   "Small enough to carry; honest enough to use.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Vault is overworking its defenses.",
                   "Five practices for the time before the pressure becomes critical.")
    for name, desc in VAULT_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Flood has come or is building.",
                   "Five practices for the overflow and its aftermath.")
    for name, desc in FLOOD_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<b>Integration:</b> The single discipline connecting both sides is this "
        "\u2014 the small, regular, chosen confession that empties the file before "
        "the earthquake empties it for you. Before the wound goes into the file, "
        "bring it to God. Before the file grows past the point of containment, "
        "bring one document to one trusted person. James 5:16 is not a verse for "
        "a particular moment. It is the architecture of the Vault's healing. "
        "Practice it in the small, ordinary days \u2014 and the Flood will become "
        "less and less necessary.",
        S["BodyJ"]))
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


# ── STANDALONE TEST ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "VAULT"
        primary_breakdown = "FLOOD"
        primary_trigger = "SHM"
        core_question = "ACC"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "vault_flood_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

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
        page_count = pdf_bytes.count(b"/Type /Page\n") or pdf_bytes.count(b"/Type/Page")
        snippet = ""

    print("DONE: vault_flood.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
