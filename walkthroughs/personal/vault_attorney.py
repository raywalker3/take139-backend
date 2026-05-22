"""Personal Walkthrough — Vault + Attorney.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Shame trigger, "Am I acceptable?" core question.
~25 pages, 9 sections.

Calibration anchor: Batch 3 — FIRST VAULT walkthrough. Establishes the
Vault mechanism as a distinct character. The Vault knows what is going on
inside but keeps it close; selective about what they show and to whom;
processes internally and presents a finished conclusion; the messy middle
stays private.

The Vault's Attorney moment is an unsealing — not a tally of givings
(Ambassador) and not a private courtroom (Island), but a file. Organized,
dated, sourced. The Vault's spouse will say: "How long have you been
keeping that?" The answer is: years.

Key theological move in Section Five: the unsealing is paradoxically a
form of intimacy — finally letting the other person see what has been
hidden — but in the worst possible form, forced by wound rather than
chosen by trust. 1 Samuel 16:7, Bonhoeffer (Life Together), Spurgeon on
secret sin.
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
    "Before you read any further, I want to do for you what a good counselor does in the first session. I want to lower the lights and slow the pace, because what you are about to look at is not a personality profile or a spiritual assessment. It is a careful look at the way your soul has learned to survive a particular kind of fear — the fear of being seen, fully and without preparation, and found wanting.",
    "You are, in a real sense, a Vault. Not because you are empty inside — the Vault is, if anything, too full. Not because you are cold or incapable of intimacy — Vaults often have the richest inner lives of anyone in the room. But because something specific and early in your experience taught you that the interior world is best kept interior. That what you show must be chosen carefully. That the finished product is safer than the half-built one, and that the messy middle — the doubt, the grief, the confusion, the longing — belongs to you alone, to be managed privately and resolved before anyone else is invited in.",
    "We are going to walk through your trigger — the specific moment your nervous system says <i>something is wrong here.</i> We will listen to the question underneath that moment, one that has probably been with you since you were very small. We will name the strategy you have built to answer that question on your own, and the place that strategy collapses under pressure. And then, only then, will we put tools in your hands.",
    "If you were sitting across from me, I would say this. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who does not require you to curate your interior before he will receive it; a Son who was exposed, publicly and completely, so that your exposure might be permanently covered; and a Spirit who is, at this very moment, praying over the parts of you that you have never shown anyone, and is not surprised by a single one of them.",
    "So read slowly. Argue with what does not fit. Stay with what does. Pray when something catches in your throat, because that catch is usually the Lord saying, <i>look here, with me.</i> The goal of this walkthrough is not insight. The goal is a slightly freer life, lived before a God who has already seen everything you have locked away and has not once turned away from it.",
    "Take your time. The chapter you are about to read about yourself has been a long time in the writing. It deserves a few unhurried hours.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life do not notice it when it occurs. From the outside it can look like almost nothing. You are in a conversation, or a meeting, or an ordinary moment at the kitchen table, and something shifts. Someone asks a question that goes slightly deeper than you were prepared for. Someone draws a conclusion about you that is close enough to true that it feels like a violation. Someone catches a glimpse of something you had not chosen to show — a failure, a fear, an unresolved grief — and they comment on it, or mention it to someone else, or simply look at you with a specific expression, the one that says: <i>I see something you didn't mean to reveal.</i>",
    "On the surface this may look like ordinary social discomfort, the minor friction of being misread or overexposed. For you, it registers as something else entirely. What fires in your chest — fast, involuntary, almost physical — is not merely embarrassment. It is closer to alarm. The signal that goes through you is not <i>that was awkward.</i> It is: <i>I have been seen in a way I did not authorize. Something I was holding has been taken from my hands. I am less safe than I was ten seconds ago.</i>",
    "This is your trigger. The word for it is <b>shame</b> — and that word needs unpacking, because it is doing more work here than it usually appears to do. Shame is not guilt. Guilt says <i>I did something wrong.</i> Shame says <i>something about me, as I am, is wrong.</i> It is not about an action that can be corrected. It is about a self that might be, beneath its careful presentation, unacceptable. The trigger fires every time someone gets close enough to the interior that this possibility becomes relevant.",
    "C. S. Lewis, in <i>The Screwtape Letters</i>, observed through his demon's voice that one of the enemy's most effective tactics is to keep a person's attention perpetually fixed on themselves — on how they appear, on what others see, on the maintenance of a self that is adequate to any inspection. This is not precisely what happens inside a Vault, but it names something adjacent to it. The Vault does not think about itself constantly; the Vault has learned to think ahead. To manage exposure before exposure becomes a problem. To anticipate the gaze before it arrives and decide, in advance, exactly what it will find.",
    "<b>Your sensitivity to shame is not random, and it is not vanity.</b> It is the residue of something that happened — usually early, usually in a context where your vulnerability was met not with care but with judgment, with indifference, with mockery, or with the particular cruelty of people who meant well and handled badly what you gave them. Maybe you shared something tender and it was dismissed. Maybe you were honest about a struggle and it became a cautionary tale someone told to someone else. Maybe you simply lived in a household where the interior life was treated as a liability — where showing emotion was weakness, or where what you felt was declared incorrect by someone with authority over you.",
    "Whatever the specific history, the lesson was lodged clearly in you: <i>what is shown can be used against you, and what stays inside stays safe.</i> And so the Vault was built — not in a morning, not as a decision exactly, but as a slow accumulation of choices that all moved in the same direction. Toward selectivity. Toward presentation. Toward the careful management of what crosses the threshold between your interior and the world.",
    "There is a real gift here that should be named honestly. The Vault processes carefully before speaking. The Vault does not scatter its interior on every available surface. When the Vault does disclose, what comes out is considered, organized, and usually precise. These are genuine qualities. They serve you in many settings. But the same mechanism that makes you a thoughtful communicator also makes genuine intimacy difficult — and the question underneath your trigger is one that genuine intimacy is the only adequate answer to. Before we go further, take a breath and answer two questions in writing. Not in your head — the Vault will reorganize what happens in your head. Your hand will be more honest.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the shame trigger fired. It does not need to be a dramatic event — look for the moment when something inside you said <i>I have just been seen in a way I did not choose.</i> What happened, in two sentences?",
    "What was the size of the actual event, and what was the size of the response inside you? If the response was significantly larger than the event, you have just located your trigger. Where did the gap appear?",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding. The Vault has been guarding this question for a very long time, and has guarded it so skillfully that you may not yet have put it into plain language.",
    "Yours is this: <b>Am I acceptable?</b>",
    "It is not quite the same as <i>Am I competent?</i> — though you have built real competence in part as a way of answering it. It is not quite <i>Am I lovable?</i> — though the questions live near each other. It is more specific and more frightening than either. It is the question that a person asks when they have deep awareness of their own interior — of the failures, the fears, the confusion, the longing they have worked so carefully to contain — and that awareness produces in them not peace but a low-grade terror. <i>If someone saw all of this, exactly as it is, with no preparation and no curation — would they find me acceptable? Would they stay?</i>",
    "Most adults would prefer to believe they settled this question long ago. They have not. They have only relocated it — buried it beneath sufficient competence, or achievement, or careful self-presentation, that it does not speak loudly during the ordinary hours. For you, this question is especially alive because you know the interior better than most people know theirs. The Vault is not self-deceived. The Vault has done real work in the interior. The Vault knows exactly what is in there. And it is precisely because you know what is in there that the exposure of it feels so dangerous.",
    "There is a cruelty in this that deserves to be named. The very quality that makes you thoughtful and self-aware — the capacity to see your own interior honestly — is the same quality that makes the shame trigger so acute. You are not anxious about exposure because you are vain. You are anxious about exposure because you have accurate information about what is inside, and you are not sure it will be well received.",
]

QUESTION_BODY_P2 = [
    "There is a reason theologians from Augustine to the Reformers have insisted that the deepest hunger of the human soul is for justification — not merely forgiveness in the everyday sense, but the settled verdict that one is acceptable, right, clean, covered. This hunger is not neurosis. It is theology. It is the correct intuition of a creature that has sinned and knows it, that has a broken interior and suspects it, and that longs to hear from the only court that finally matters: <i>you are acceptable. Not acceptable despite what is inside you, but acceptable — covered, held, named, kept — because of what has been done for you.</i>",
    "The Psalms tell the truth about this longing. Psalm 139, which the Vault often finds either deeply comforting or quietly terrifying, does not allow for the possibility of a hidden interior: <i>O Lord, you have searched me and known me. You know when I sit down and when I rise up; you discern my thoughts from afar. You search out my path and my lying down and are acquainted with all my ways. Even before a word is on my tongue, behold, O Lord, you know it altogether.</i> (Psalm 139:1-4) David is not performing openness here. He is confessing the inevitable. He is saying: everything the Vault is trying to manage, God has already seen — and David does not end this Psalm in despair. He ends it in the language of being held. <i>Search me, O God, and know my heart. Try me and know my thoughts.</i> He is inviting what the Vault most fears, because he has discovered that the God who already sees does not turn away from what he finds.",
    "Paul, in 2 Corinthians 5:21, puts it with theological precision: <i>For our sake he made him to be sin who knew no sin, so that in him we might become the righteousness of God.</i> This is not merely a transaction on a ledger. This is the permanent answer to the question <i>Am I acceptable?</i> Christ took on himself, publicly and explicitly, the full weight of the shame that you are working to manage internally. He was exposed — stripped, mocked, displayed. And he absorbed that exposure so that the one who is united to him stands before God clothed, not naked. Covered, not exposed. The verdict over you is not <i>acceptable pending inspection.</i> It is <i>acceptable, finally and forever, because of what the Son has done.</i>",
    "But here is the honest rub, and it is specific to you. The Vault hears this and files it accurately. You may well have memorized the doctrine. You can likely state justification with precision. But the Vault has a particular difficulty with the gospel's answer to this question, and it is not an intellectual difficulty. The difficulty is this: <b>receiving the verdict requires letting it in.</b> Receiving requires a kind of interior permeability — an openness to being given something you did not produce, did not curate, did not present in its best light. And the Vault has spent years building the walls specifically to prevent that kind of permeability.",
]

QUESTION_BODY_P3 = [
    "Samuel 16:7 gives the oldest version of this problem in Scripture. The Lord says to Samuel, standing before Eliab who looks the part: <i>Do not look on his appearance or on the height of his stature, because I have rejected him. For the Lord sees not as man sees: man looks on the outward appearance, but the Lord looks on the heart.</i> The Vault has organized its entire strategy around the outward appearance — around presenting what has been curated and keeping the heart out of view. But the God of Scripture has already entered through the wall. He does not see the exterior presentation. He sees the heart, and he has been looking at it all along, and he has spoken his verdict not after inspection but before it, in Christ, on your behalf.",
    "This is the word the Vault most needs to receive: <b>God already sees what is inside, and the verdict is not condemnation. The verdict is covered.</b> Romans 8:1 — <i>There is therefore now no condemnation for those who are in Christ Jesus.</i> Not <i>no condemnation once you have organized yourself</i>. Not <i>no condemnation when you have resolved the messy middle.</i> Now. In Christ. The Vault has been working to make the interior acceptable before showing it to anyone. God has already seen it and called it covered.",
    "The work this section invites is not the work of further self-inventory — the Vault already has more than enough inventory. The work is the practice of receiving the verdict. Day by day. Not as a feeling, not as a rush of liberation, but as a quiet return to the news that the case has been decided in your favor, not by your performance but by your advocate. Before we close this section, use the table below — not to analyze more deeply, but simply to bring recent events into the light of the question and the answer together.",
]

VAULT_BODY_P1 = [
    "You have built something. It took years, and you probably did not decide to build it — it grew from the accumulation of small choices that all pointed the same direction, and one day you looked up and the structure was already there. Throughout this walkthrough we are going to call it <b>the Vault</b>, and the Vault deserves to be understood as a character before we say anything about what it costs you.",
    "The Vault is not the Island. This distinction matters, and it is worth pausing over before we continue. The Island processes alone because that is how the Island processes. The Island's distance from others is temperamental — it is not driven by fear of a specific kind of exposure. The Island has thin walls, in a sense; it is simply self-contained by nature. The Vault has thick walls with locks, and the locks were installed for a reason. The Island stays inside because inside is comfortable. The Vault stays inside because outside has been shown to be dangerous.",
    "The Vault's strategy, stated plainly, is this: <i>I will show you what I have chosen to show you, and what I have chosen to show you will be organized and finished and carefully considered, and what I have not chosen to show you will remain mine, and this arrangement will protect me from the specific danger that comes when unfinished things are seen and judged.</i> This is not dishonesty — the Vault does not perform a false self. The Vault shows real things. But real things that have been selected, arranged, and cleaned up before presentation.",
    "There is a great deal in Scripture that honors the person who holds their counsel carefully. Proverbs 17:27 says: <i>Whoever restrains his words has knowledge, and he who has a cool spirit is a man of understanding.</i> The Vault often quotes this internally, and the Vault is not wrong to do so. Self-command is a virtue. The capacity to hold one's interior and not scatter it indiscriminately is wisdom, not weakness. <b>The Vault is not, in itself, a sin.</b> It is a gift that has been overemployed until the gift has become a wall.",
]

VAULT_BODY_P2 = [
    "How did the Vault form? The taxonomy we work from suggests four histories that tend to produce it, and you will likely recognize yourself in at least one.",
    "The first is the history of <i>exposure that went badly.</i> You showed something interior and the person who received it handled it carelessly — critically, dismissively, or they used what you gave them in a way that cost you. You showed the half-built house and someone commented on the mess. The lesson lodged precisely: <i>what I show can be turned against me.</i>",
    "The second history is <i>shame about the interior itself.</i> Not simply fear of exposure, but a suspicion that what is inside — the particular textures of your doubt, your failure, your longing, your fear — is more disordered than what others carry, and that if it were seen clearly it would change how you are regarded. The Vault in this case is not merely cautious; it is protective of something it believes to be, at some level, genuinely problematic.",
    "The third history is <i>a preference for finished conclusions.</i> Some Vaults genuinely process well internally and believe, not without reason, that sharing the process in real time is unhelpful. <i>I will bring you the conclusion when it is ready.</i> This is not always avoidance. But when the conclusion is always ready and the process is never seen, intimacy becomes a function of what you present rather than what you are.",
    "The fourth history is <i>a home in which expression was discouraged.</i> Feelings were handled quietly, privately, as personal management — not punished, but not valued. Or perhaps expression was over-valued, everything a drama that had to be processed aloud, and you retreated into privacy as the only available peace. Either extreme teaches the same lesson: <i>what is inside is better managed alone.</i>",
    "Dietrich Bonhoeffer, in <i>Life Together</i>, observed that the Christian who keeps the struggle private and brings only the resolution to the community has severed themselves from one of the great mercies of the church — the mercy of being known in one's actual condition and received anyway. The Vault has usually never had this experience. It brings the finished version to God and to the community, holds the process alone. Bonhoeffer would call this a kind of spiritual solitude that is, in the end, lonely rather than holy.",
]

VAULT_BODY_P3 = [
    "What does the Vault cost you? Let me name three things honestly, because the Vault is skilled at acknowledging costs in the abstract without sitting with them in the particular.",
    "It costs you <i>the intimacy you most want.</i> The Vault genuinely longs to be known — to have someone who knows what is actually inside and remains. This is exactly what the question <i>Am I acceptable?</i> is asking. But the Vault's mechanism ensures that no one ever has access to the information that would allow them to answer the question. Their love — however real — can never fully satisfy, because it is love offered to the Vault's presentation rather than to the Vault's interior.",
    "It costs you <i>the speed of repair.</i> When you are wounded, the Vault takes it inside. What goes inside does not disappear; it is filed. The Vault is the most precise record-keeper of all the mechanisms we track, because precision is part of its gift. It notes the date, the context, the specific words. This is not malice. It is what happens when a careful, inward-processing person is hurt and has no mechanism for immediate disclosure. The file grows. The relationship continues on the surface. Something accumulates underground.",
    "It costs you <i>the ability to be prayed for in your actual condition.</i> The people in your life pray for the Vault's presentation — the resolved version, the organized version. They are not praying for the actual interior because they do not know it. There is a loneliness in this that the Vault rarely names but often feels: a sense of being held, superficially, by people who would hold you differently if they actually knew.",
    "<b>The Vault is not your enemy.</b> He is a younger version of you who learned, in some real circumstance, that the unlocked version was not safe. He has been faithful. But he is working on a project that has long since outgrown the original threat. The walls that once protected you are now preventing the one thing the question underneath your trigger most needs: to bring the actual interior into the actual light and discover that the light is not dangerous.",
    "Before we close this section, I want you to read a letter — not one you wrote to the Vault, but one from the Vault, in his own voice, to you. He has been faithful for a long time and has never been asked to account for himself honestly. Give him that chance now.",
]

VAULT_LETTER_INSTRUCTION = [
    "The letter below is written in the Vault's voice — from him, to you. He is not villainous. He is careful, and he is frightened, and he has been doing his best with a very difficult assignment. Read it slowly. Then answer the three prompts that follow.",
    "Dear [your name],",
    "I want to tell you something I have never been asked to explain, because no one has ever been able to see me clearly enough to ask. I want to tell you what I have been doing, and why, and what I am afraid will happen if I stop.",
    "I have been keeping a file.",
    "Not deliberately, not as a conscious project. But everything that has entered me — every wound, every fear, every moment of exposure that went badly, every doubt I resolved alone, every grief I processed before showing anyone the conclusion — has been organized. Filed by date. Cross-referenced. Labeled with context. I am, if nothing else, thorough.",
    "I built the walls because the alternative was worse. Because I showed something once — I'm not sure you remember all the times, but I remember every one — and what happened next taught me that showing without preparation is the same as handing someone a weapon and asking them to be careful with it. So I started preparing. I started choosing. I started bringing people the finished version, the version that had been worked over and organized and presented in its best light. And it worked. No one could use against you what you had not given them.",
    "What I did not calculate is the weight of it. Every file is still in here. Everything you have ever resolved alone, I have kept. And the longer you carry it, the more precisely I know what is inside, and the more certain I have become that if it were seen clearly — without the preparation, without the curation, without the finished conclusion — something would break. I am not sure what. Only that the break would be irreversible.",
    "But I want to tell you something that costs me a great deal to say. I think I have confused carrying with hiding. I think I have been so long at the project of keeping the interior safe that I have begun to believe the interior is the problem, when actually the interior is just you. All of it. Even the parts I have been most careful to keep filed away.",
    "I don't know what to do with that. I have been doing this too long to simply stop. But you should know why I am here. And what it is I am protecting you from. And whether the thing I am protecting you from is still as dangerous as I believe.",
    "The Vault",
]

VAULT_LETTER_PROMPTS = [
    "What part of the Vault's letter surprised you? Not the part you expected — the part you were not quite ready for.",
    "The Vault says he has been keeping a file. Name one specific entry in that file — one wound, one grief, one fear — that has been inside, organized and dated, that you have not disclosed to anyone. You do not need to disclose it here. Simply name that it exists.",
    "What would the Vault need to believe — really believe, at the level where the filing happens — in order to begin loosening its grip on the contents? What would have to be true about God, or about at least one other person, for the door to become slightly less locked?",
]

ATT_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Vault, the breaking has a shape that is unlike any other version of this breakdown, and the difference is important enough to name very carefully. The breakdown is called <b>the Attorney</b>, and you have almost certainly encountered it — but you may not have recognized it as the Attorney, because the Vault's version of this breakdown does not look like an argument. It looks like an unsealing.",
    "Here is the setup. The Vault has been managing the interior with characteristic precision — processing privately, presenting conclusions, keeping the file organized and secure. Then something lands. A wound large enough that the Vault's usual management cannot fully contain it. A spouse who says something that lands as a judgment about who you actually are, not merely about something you did. A friendship that ends in a way that confirms the oldest suspicion: <i>that if they really knew, they would leave.</i> A moment of public exposure, unplanned, that puts something interior in front of others before you had a chance to prepare it.",
    "The trigger fires. The question wakes up: <i>Am I acceptable?</i> The Vault does what the Vault always does — takes the wound inside and begins to manage it. But this wound is too large for management. And something that the Vault has been doing for a very long time without quite knowing it now becomes visible: <i>the file is enormous.</i>",
    "The Vault has been keeping records the whole time. Not a tally of givings, the way the Ambassador keeps records. Not a running brief assembled in real time, the way the Architect prosecutes. Not the silent case-building of the Island, who takes a wound and builds over months. The Vault's record-keeping is different from all of these: it is a <i>file</i>. An archive. Organized, labeled, dated, cross-referenced. Every wound the Vault has received that went unfiled is in there. Every piece of evidence the Vault has gathered about its own unacceptability is preserved with precision. Every exhibit in the case against the Vault's worth — <i>this is what happened, on this date, in this context, with these words</i> — has been kept.",
]

ATT_BODY_P2 = [
    "And then the vault opens.",
    "This is what the Vault's Attorney looks like, and your spouse or closest friend may recognize the description with a jolt. It does not look like an argument. It does not look like heat, the way the Ambassador's Attorney arrives. It does not look like the Island's cold closing statement. What it looks like is a drawer being opened, and inside the drawer are organized documents. With dates. From years ago.",
    "The other person in the room goes quiet. They are being shown that the Vault has been keeping records they did not know existed. Not records of what they gave; an archive of what was done to the Vault. Every exhibit is specific. Every date is accurate. The Vault does not exaggerate because the Vault does not need to; the precision of the file is devastating on its own.",
    "And the question the other person will almost certainly ask — the question that becomes the signature of the Vault's Attorney — is this: <b>How long have you been keeping that?</b> The answer is: years. And this is the pastoral problem that must be named directly. The Vault's file-keeping is not malicious. It is the natural consequence of a mechanism that takes wounds inside and does not have a reliable way to let them back out. Every wound filed is a wound that never found its way to disclosure, to repair. The file is the record of a thousand small moments of unexpressed injury, and the opening of the file is, paradoxically, the most intimate thing the Vault has ever done — the first time the other person is seeing what has actually been inside.",
    "But it is intimacy of the worst possible kind. Forced by wound rather than chosen by trust. Charles Spurgeon, preaching on the hidden life of the soul, warned his congregation that <i>there is no sin more dangerous than the sin that is kept secret in a secret heart</i>. He was speaking of unconfessed wrongdoing. But the principle extends: there is no wound more dangerous than the wound kept precisely filed in a precisely locked place, because the keeping of it alone, without the light of another's witness, allows it to grow in the dark into something larger than what first arrived.",
]

ATT_BODY_P3 = [
    "Here is the paradox that the Vault must eventually sit with, and it is a difficult one. <b>The Attorney moment is, in a broken form, exactly the intimacy the Vault has been longing for.</b> What the Vault has always wanted — underneath the question <i>Am I acceptable?</i> — is for someone to see what is actually inside and stay. The Attorney delivers the contents of the file and asks, implicitly: <i>Now that you know what has been in here, do you stay?</i> It is the Vault's first act of genuine disclosure. But it comes as a prosecution, and the person receiving it is not being given a gift of vulnerability; they are being presented with evidence in a case they did not know was running.",
    "The reason the Attorney's disclosure does not satisfy is that it is not free. Trust-based disclosure is given; the Attorney's disclosure is forced by wound. And the intimacy that the question <i>Am I acceptable?</i> needs is the intimacy of a free disclosure received with care — not the intimacy of a vault opened under duress. The acknowledgment that comes after the Attorney's presentation, even when it is heartfelt, will not answer the question, because the Vault knows that the other person is responding to prosecution rather than to offered vulnerability.",
    "Bonhoeffer, in <i>Life Together</i>, writes that the person who avoids the confession of sin — who refuses to bring the actual interior to a brother in the Lord — has thereby refused one of the great healing mercies of the Christian community. He is not speaking of formal sacramental confession. He is speaking of the act of bringing what is actually inside into the light of a trusted presence, and receiving the assurance of grace in a human voice. The Vault has been avoiding this mercy for years. Not because it is proud; because it is afraid. And the Attorney is what the unconfessed interior does when it cannot hold any longer.",
    "The gospel's interruption of the Vault's Attorney is not <i>your file is wrong.</i> The wounds in the file are real. The evidence is accurate. The gospel's interruption is this: <b>you already have an Advocate who has already presented the only file that finally counts.</b> <i>If anyone does sin, we have an advocate with the Father, Jesus Christ the righteous.</i> (1 John 2:1) Christ does not wait for the Vault to organize its case before he enters the plea. He has already seen the full interior — <i>man looks on the outward appearance, but the Lord looks on the heart</i> (1 Samuel 16:7) — and he has taken its shame into himself and left it at the cross. The file does not need to be delivered to earn a verdict. The verdict has been spoken. The only thing still required is the willingness to let the contents out of the vault — not as prosecution, but as confession.",
]

ATT_PROMPTS = [
    "Name the last time the Vault's Attorney opened the file. Not necessarily out loud — even internally, when you rehearsed what you would say to the person who had wounded you. What was in the file that you brought out? How long had those documents been in there?",
    "The Vault's Attorney makes its worst error by delivering disclosure as prosecution rather than as trust. Think of one wound you have been carrying internally — one item in the file — that has never been spoken to the person who contributed to it. What would it look like to bring that wound as a person asking for repair, rather than as an attorney presenting a case?",
    "What verdict were you hoping the Attorney's documents would produce? Write it in one sentence beginning: <i>If they could only understand what has been inside me, they would finally ___.</i> What has Christ's advocacy already said about that sentence?",
]

TWO_TOG_BODY = [
    "Now we place them side by side, because the Vault and the Attorney are not two separate problems. They are the same wound, organized in two different modes. The Vault organizes the interior for safety. The Attorney organizes the interior for prosecution. Both are working with the same long accumulation of what has been kept inside, and both are trying to answer the same question.",
    "<b>The Vault is what your fear does when it has time.</b> The Attorney is what your fear does when it has run out of time. The Vault files carefully so the wound will not have to be shown. The Attorney presents the file when the wound can no longer be contained. Together they form a closed system, and the system will run all your life if nothing interrupts it.",
    "The pattern, in slow motion: <b>(1)</b> The Vault manages exposure — presenting finished conclusions, filing what cannot be shown. <b>(2)</b> A wound lands large enough to threaten that management. <b>(3)</b> The trigger fires: <i>I have been seen in a way I did not authorize.</i> <b>(4)</b> The question wakes up: <i>Am I acceptable?</i> <b>(5)</b> The Vault takes the wound inside. <b>(6)</b> The wound joins the file. <b>(7)</b> A later wound — often smaller — finally opens the vault. The Attorney presents years of accumulated evidence that was never shown. The other person asks: <i>How long have you been keeping that?</i> The answer is: years. <b>(8)</b> The acknowledgment does not satisfy. The Vault closes again. The loop restarts.",
    "What breaks the loop is not better file management. It is a different answer to the question — received, not merely affirmed. Until the Vault receives, at the level where the filing happens, that the God who has already seen every document has spoken the verdict <i>acceptable, covered, in Christ</i>, the loop has nothing to push against. With that answer practiced over time, the Vault begins to find less need for the locks. The Attorney finds less need for the file. Neither retires fully in this life. But both begin to work shorter hours.",
    "Below is your sequence. Fill in the blanks. Read it aloud when you finish. The Vault and the Attorney both lose some of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as exposure — as "
    "being seen in a way I did not authorize — and the old question wakes up: "
    "<i>am I acceptable?</i> My first move is to ____________________, because "
    "the Vault in me believes that if I can ____________________, the danger will "
    "be contained. When that does not work — when the wound is too large for "
    "management — the Attorney opens the file and presents the evidence that "
    "____________________. What I am actually after, underneath all of it, is the "
    "verdict ____________________ \u2014 a verdict Christ has already spoken over me "
    "in ____________________, in a voice the Vault has not yet fully let in."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of tools, each one concrete enough to use and honest enough to matter. None of them will dissolve the Vault's pattern in a single application. All of them, practiced over months, will loosen the grip of the loop you just named.",
    "I have divided them into two sets: tools for when the Vault is overworking its defenses (when the management of exposure has tipped from wisdom into hiding), and tools for when the Attorney is opening the file (when the wound is fresh and the documents are being arranged). The Vault's tools come first, because the Attorney cannot be interrupted usefully until the mechanism underneath it is understood.",
]

VAULT_TOOLS = [
    ("The half-built house practice", "Once a week, share something with one trusted person before it is finished. Not a crisis — simply something you are in the middle of, a question you have not resolved, a feeling not yet organized into a conclusion. The Vault will insist this is unnecessary. Do it before you know what you think. Over a month, the practice begins to demonstrate that unfinished things, shared carefully, do not produce the catastrophe the Vault is guarding against."),
    ("The audit of what is being filed", "Once a week, ask: <i>what went inside this week that I have not disclosed to anyone?</i> You do not need to disclose it all at once. Simply name that it exists — to yourself, and if possible to God in prayer. The Vault's most dangerous work is invisible. Naming the contents, even privately, begins to interrupt the automatic filing."),
    ("The Psalm of the searched heart", "When the Vault is in full management mode, open to Psalm 139 and pray it aloud — the whole thing, not selected verses. It ends not in shame but in invitation: <i>Search me, O God, and know my heart. Try me and know my thoughts. And see if there be any grievous way in me.</i> The Vault needs practice asking to be known by God before it can practice asking to be known by people."),
    ("The one-degree opening", "Identify one person who has demonstrated, over time, that they can be trusted with your interior. Choose one item from the file — one old grief, one unresolved question — and disclose it. Not as a test. As a practice. The Vault was built to prevent precisely this, which is why it is the most important thing on this list."),
    ("Receive the verdict before you manage the wound", "When the shame trigger fires, before you file the wound, say aloud: <i>God has already seen this, and the verdict is covered. I am in Christ. I do not need to manage this alone.</i> The Vault's instinct is to receive the wound silently and begin organizing. This practice interrupts the organizing and replaces it with the gospel's answer to the question the wound re-opens."),
]

ATT_TOOLS = [
    ("The age test for the file", "When the Attorney begins to organize documents, ask: <i>how old is the oldest item in this file?</i> If the answer is more than two weeks, you are not processing a fresh wound; you are prosecuting accumulated grievance. Prosecution delivers the file. Processing brings a specific wound while it is still fresh enough to be repaired."),
    ("Name the document before it enters the file", "Within forty-eight hours of a wound registering, tell one trusted person one sentence: <i>something landed on me this week and I am naming it before it goes into the file.</i> Simply break the secrecy before the evidence is fully organized. The Vault's Attorney does its most dangerous work when nothing about it is visible. Spoken aloud to a safe witness, the brief loses momentum."),
    ("Bring the wound, not the brief", "When you must speak to the person who wounded you, bring one sentence: <i>When that happened, I felt exposed in a way I did not choose, and I need you to know that.</i> One wound, one sentence, one request for acknowledgment. Not the full file, the pattern, the precedent. The relationship can sustain a wound expressed honestly; it is much less clear it can sustain the full archive."),
    ("The advocate prayer", "When the Attorney is loudest, pray slowly: <i>Lord Jesus, you are my Advocate. You have already seen every document in this file. You took the exposure I fear into yourself at the cross and left it there. I do not need to deliver this brief. The verdict has been spoken. Help me to receive it.</i> Say it three times. The third time is usually when the file begins to feel less necessary."),
    ("Write it and confess it", "If the brief will not leave you alone, write it out in full — every item, every wound, every date. Then bring the paper into prayer: <i>Lord, this is what has been inside. You have known all of it. I hand it to you now, not as a brief to be prosecuted but as a burden I was not meant to carry alone.</i> Then tear the pages slowly. This is not suppression. It is transfer. It is the beginning of deaccessioning the file."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Vault in me, and you are not surprised by it. You know what was locked inside long before I began to lock it. You know the specific moments — the exposures that went badly, the interior I was ashamed of, the home that taught me that expression was a liability — and you have been present in the interior through all of it, every document I ever filed, every wound I ever chose not to show. Thank you that the Vault kept me alive. Thank you that he has been, in his way, faithful.",
    "But Father, the file is heavy, and I have been keeping it for a long time, and I have been confusing management with safety and privacy with peace. Teach me that you have already seen what is inside, and that your verdict is not what the Vault fears. The verdict is covered. In Christ. Now and forever. Teach me, when the shame trigger fires and the old question asks <i>Am I acceptable?</i>, to hear your answer before I hear the Vault's. <i>There is therefore now no condemnation for those who are in Christ Jesus.</i> Let that land somewhere below my theology.",
    "Lord Jesus, when the Attorney rises in me — when the file has grown too large to hold and the documents begin to organize themselves for presentation — remind me that you are my Advocate, that you have already entered the only plea that finally counts, that you presented at the cross the evidence of your own blood and not my file. I do not need to deliver the brief. The case is decided. Help me to live from the verdict rather than toward it.",
    "Holy Spirit, where I have been hiding, give me the courage to speak. Where I have been filing, give me the practice of confessing. Teach me the difference between managing my interior and offering it — first to God, then to the people who have earned the right to receive it. Teach me that the God who looks on the heart, and not the outward appearance, has looked and has not turned away.",
    "In the name of the One who was exposed, fully and publicly, so that my exposure might be permanently covered \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Vault and the Attorney have been with you for a long time, and one careful afternoon's reading will not retire them. What follows is a short list of next steps — some immediate, some longer — for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different sections will land differently. The Vault will resist a second reading — it prefers to receive information once, file it, and consider the matter resolved. Read it again anyway. The section that felt least relevant today may be the most necessary one in a month."),
    ("Take one tool, not six.", "Choose a single practice from Section 7 and try it for two weeks before you add another. The tools are postures, not a program. One posture, held for long enough, begins to change the shape of the interior."),
    ("Tell one person what you found.", "Not the whole document. One sentence: <i>I learned that my mechanism is the Vault, and my breakdown is the Attorney, and I have been keeping a file I did not fully know was there.</i> Notice what happens when the Vault speaks about itself to a trusted witness. The Vault loses some of its authority when it is required to describe its own operations aloud."),
    ("Pray Psalm 139 slowly, once a week, for a month.", "All of it. Not the parts that feel safe. Verse 23 especially: <i>Search me, O God, and know my heart. Try me and know my thoughts. And see if there be any grievous way in me.</i> This is the Vault's hardest prayer because it is the explicit invitation of the God who already sees. Practice the invitation."),
    ("Read further on the shame the gospel answers.", "Tim Keller, <i>Walking with God through Pain and Suffering</i> \u2014 especially his treatment of why suffering feels like exposure and how the gospel reframes it. C. S. Lewis, <i>The Weight of Glory</i> \u2014 his treatment of the longing to be known and named by the highest authority will name the Vault's deepest longing with unusual precision. Dietrich Bonhoeffer, <i>Life Together</i> \u2014 his chapters on confession and community are the most direct pastoral address to what the Vault most needs and most avoids."),
    ("If you are stuck, ask for help.", "There are seasons when the Vault and the Attorney are too entrenched to dislodge alone. A wise pastor, a Christian counselor, a trusted friend who has earned the right to the interior \u2014 these are not signs of failure. For the Vault specifically, asking for help is among the most countercultural practices on this list. The Vault was built to manage alone. Asking someone in is the beginning of its healing."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom by a Father "
    "who has already seen everything in the file and has spoken the verdict before you could "
    "organize a single document in your defense. Go gently with yourself. "
    "The One who began the good work in you will be the one who finishes it."
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
        [Paragraph("WAS I EXPOSED HERE?", header_style), Paragraph("what your nervous system concluded", sub_style)],
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
    """Generate the Vault+Attorney walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='VAULT', primary_breakdown='ATTY',
    primary_trigger='SHM', core_question='ACC'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor's Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR'S WALKTHROUGH",
        cover_right_label="VAULT  \u00b7  ATTORNEY",
        title="Take 139 Walkthrough \u2014 Vault + Attorney",
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
    story.append(Paragraph("The Vault &nbsp;\u00b7&nbsp; The Attorney", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Shame &nbsp;\u00b7&nbsp; Core Question: Am I acceptable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cThe Lord sees not as man sees: man looks on the outward appearance,<br/>"
        "but the Lord looks on the heart.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "1 Samuel 16:7",
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
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
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
                   "Where was I actually in danger? Where was my soul covered?")
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
        "VaultLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for line in VAULT_LETTER_INSTRUCTION:
        story.append(Paragraph(line, letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in VAULT_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Attorney.",
                   "The unsealing. The file no one knew was being kept.")
    for p in ATT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ATT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "Intimacy in the worst possible form.",
                   "What the unsealing was always longing to be, and what it became instead.")
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
                   "The same wound, in two modes.",
                   "The Vault and the Attorney are not two problems. They are one loop.")
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
                   "Six practices for the time before the Attorney is needed.")
    for name, desc in VAULT_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Attorney begins to open the file.",
                   "Six practices for the moment the documents are being arranged.")
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
        primary_mechanism = "VAULT"
        primary_breakdown = "ATTY"
        primary_trigger = "SHM"
        core_question = "ACC"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "vault_attorney_test.pdf")
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

    print(f"DONE: vault_attorney.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
