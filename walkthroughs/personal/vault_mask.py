"""Personal Walkthrough — Vault + Mask.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Shame trigger, "Am I acceptable?" core question.
~25 pages, 9 sections.

Calibration anchor: Walkthrough 22 of 36. The Vault+Mask is the
double-locked hiding — the mechanism is already a vault, and the
breakdown layers a public persona on top of the locked interior.
Where the Island+Mask is "the warm friend behind glass" and the
Ambassador+Mask is "the celebrated leader hiding under the cloak of
grace," the Vault+Mask is the trusted private person who has never
been known by anyone — including, sometimes, themselves.

This is the profile most likely to live a long secret life: not
necessarily of public sin, but of public absence of self. The Vault
has processed alone for so long, and the Mask has presented so
smoothly for so long, that the seam between the presented self and
the interior self has become invisible — even to the Vault.

Key theological move in Section Five: John Owen on the deceitfulness
of indwelling sin; Augustine on the heart more known to God than to
itself; Calvin on knowledge of God requiring knowledge of self.
Pastoral confrontation: God's question to Cain — "Where is your
brother?" — and the Vault+Mask's characteristic evasion: not
denial, but disappearance of the self from the question.
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
    "Before you read any further, I want to do for you what a good pastor does at the beginning of a long conversation. I want to lower the lights and slow the pace, because what you are about to look at is not a personality profile. It is a careful look at the way your soul has learned to survive a particular kind of danger: the danger of being known.",
    "You are, in a real and specific sense, a Vault. Not because you are empty inside — the Vault is, if anything, too full, more attentive to its own interior than most people you know. Not because you are cold or incapable of relationship. But because something specific, and usually early, in your experience taught you that the interior world is best kept interior. That what you show must be chosen carefully. That the messy middle belongs to you alone, to be resolved before anyone else is invited in.",
    "And then, over time, you built something else on top of the locked interior. A face. A way of being in the room that is real enough that most people never think to look behind it. Not a fabrication — a carefully chosen self. The version of you that knows how to be present in any gathering, that is trusted and respected and genuinely valued. This is the Mask. And together, the Vault and the Mask form a combination this walkthrough is going to name plainly: <b>the trusted private person who has never been fully known by anyone</b> — including, on the most honest days, themselves.",
    "If you were sitting across from me, I would say this carefully. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who has already entered through every wall you have ever built, who is more acquainted with your interior than you are, and who has not once turned away from what he found. A Son who, in his own body, absorbed the full weight of exposure so that your exposure could be permanently covered. A Spirit who is, at this moment, working in the very parts of you that the Vault has been keeping most carefully sealed.",
    "So read slowly. The Vault in you will want to receive this efficiently — to extract what is applicable, file it, and consider the exercise complete. Resist that. Stay with the sentences that catch. Pray when something tightens in your chest, because that tightening is usually the Lord saying, <i>look here, with me.</i> The goal of this walkthrough is not more self-knowledge. The Vault already has extraordinary self-knowledge. The goal is a slightly more open door.",
    "Take your time. The chapter you are about to read about yourself has been a long time in the writing. It deserves a few unhurried hours.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it is not always dramatic. You are in a conversation, a meeting, an ordinary exchange — and something lands in a particular way. A question that goes a degree deeper than you were prepared for. A comment from someone who has been watching more carefully than you realized. A silence that says more than the person intended. A moment in which someone draws a conclusion about you that is close enough to accurate that it registers, not as insight, but as intrusion.",
    "From the outside, nothing has happened. Your face may not change. You may, in fact, continue the conversation with greater composure than before — warmer, steadier, more generous with your attention — because the Vault has learned that the best way to manage exposure is to redirect attention away from it. But inside, something has shifted. A signal has fired, specific and cold: <i>I have just been seen in a way I did not choose. Something I was holding has been touched without my permission. I am less safe than I was a minute ago.</i>",
    "This is your trigger. The word for it is <b>shame</b> — and it is important to say clearly what that word does and does not mean here. Shame is not guilt. Guilt says <i>I have done something wrong.</i> Shame says <i>something about me, as I am, may be fundamentally wrong.</i> It is not about an act that can be corrected; it is about a self that may be, beneath its careful presentation, unacceptable. The trigger fires every time someone gets close enough to that self — the real one, the unprocessed one, the one that has not yet been brought to finished condition — that the possibility of their finding it becomes relevant.",
    "C. S. Lewis, in <i>The Screwtape Letters</i>, identified through his demon's voice one of the most durable forms of spiritual captivity: the state in which a person is perpetually performing a self that can withstand inspection, while the actual self recedes further and further from the light. Lewis was not describing a fraud. He was describing a person who has genuinely lost track of the distance between the self they present and the self they actually are — and who has learned not to look at the gap, because looking at it makes everything more dangerous.",
    "<b>Your sensitivity to shame is not random, and it is not vanity.</b> It is the residue of specific moments — usually early, often repeated, sometimes only a handful but precisely remembered — in which the interior was not met with safety when it was offered. You shared something unfinished and it was dismissed or mishandled. You disclosed something vulnerable and it became a story someone else told. You showed the half-built house and someone walked through and commented on the mess. The lesson did not have to be stated explicitly. It was received clearly: <i>what is shown can be used. What stays inside stays mine.</i>",
    "And so the Vault was built. Not in a morning, not as a project exactly, but as a slow accumulation of choices that all pointed the same direction — toward selectivity, toward presentation, toward the management of what is ever permitted to cross the threshold between your interior and the world.",
    "But here is what is particular to this profile, and what sets it apart from every other combination in this series. The Vault+Mask is not only locked; it is also <i>inviting</i>. The Mask that sits over the Vault's door is a real and genuine presence — trustworthy, attentive, composed, respected. People come to you. They sense something settled and substantial. What they do not know — what you have taken extraordinary care to ensure they cannot know — is that the settled, substantial presence they are encountering is only the outer ring of a much more complex interior. The person they trust has never quite been met.",
    "Before we continue, I want you to do something simple. Answer the two questions below in writing. Not in your head — the Vault will organize whatever happens in your head into something presentable. Your hand will be more honest.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the shame trigger fired. It does not need to be dramatic — look for the moment when something inside you said: <i>I have just been seen in a way I did not choose, or someone has come closer to the real interior than I intended.</i> What happened, in two sentences?",
    "What was the size of the actual event, and what was the size of the response inside you? If there was a gap between them, you have located the trigger. What was behind the gap — what old question did the event touch?",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm has been standing over. The Vault has been guarding this question for a very long time — and has guarded it so skillfully, and the Mask has covered the guarding so thoroughly, that you may have gone years without putting the question into plain language.",
    "Yours is this: <b>Am I acceptable?</b>",
    "It is not quite <i>Am I lovable?</i> — though the questions are neighbors. It is not <i>Am I competent?</i> — though the Vault has built real competence in part as a way of keeping this question at bay. It is more specific and more frightening than either. It is the question that arises in a soul that has thorough knowledge of its own interior — the failures, the fears, the ongoing confusion — and that knowledge produces in it not peace but a low-grade dread. <i>If someone saw all of this, exactly as it is, with no preparation — would they find me acceptable? Would they stay?</i>",
    "The particular cruelty of this question for the Vault is that the Vault's very strength — the capacity for honest, precise self-knowledge — is what makes the shame trigger so acute. You are not anxious about exposure because you are vain. You are anxious about exposure because you have accurate information about what is inside, and you are not certain it will be well received. John Owen observed that the sins most dangerous to the soul are not always the ones that fail visibly, but the ones that have quietly organized the whole life around their own avoidance. For the Vault+Mask, shame is that organizing principle. It runs the whole operation — and the operation runs so smoothly that the people closest to you rarely see it running.",
]

QUESTION_BODY_P2 = [
    "There is a reason that theologians from Augustine to the Reformers have insisted that the deepest hunger of the human soul is for justification — not merely forgiveness in the everyday sense, but the settled, irrevocable verdict that one is acceptable: covered, clean, named, held. This hunger is not neurosis. It is the correct intuition of a creature that has sinned and knows it, and that longs to hear from the only court whose verdict finally stands: <i>you are acceptable. Not conditionally — acceptable because of what has been done for you, before you did anything to merit it or manage it.</i>",
    "The Psalms tell the truth about this longing without embarrassment. Psalm 139, which the Vault often reads with a complicated feeling — something between comfort and quiet terror — does not allow for the possibility of a hidden interior: <i>O Lord, you have searched me and known me. You know when I sit down and when I rise up; you discern my thoughts from afar. You search out my path and my lying down and are acquainted with all my ways. Even before a word is on my tongue, behold, O Lord, you know it altogether.</i> (Psalm 139:1-4) David does not end this Psalm in despair. He ends it with an invitation: <i>Search me, O God, and know my heart. Try me and know my thoughts.</i> He is asking to be seen, because he has discovered that the God who already sees has not turned away from what he found.",
    "Paul, in 2 Corinthians 5:21, states the answer to the shame question with a precision that should arrest us: <i>For our sake he made him to be sin who knew no sin, so that in him we might become the righteousness of God.</i> Christ took on himself the full weight of exposure — stripped, mocked, displayed, bearing the shame that belongs to the interior you have been working to contain. He absorbed that exposure so that the one united to him stands before God not as the partially-managed self the Mask presents, but as fully covered, clean, and beloved. The verdict over you is not <i>acceptable pending inspection.</i> It is <i>acceptable — now, in Christ, finally and forever.</i>",
    "But here is the honest complication, specific to this profile. The Vault hears this and files it accurately. You can almost certainly state the doctrine of justification with precision. But the Vault+Mask has a difficulty with the gospel's answer that is not an intellectual difficulty. The difficulty is this: <b>receiving the verdict requires letting it in.</b> Receiving requires interior permeability — openness to being given something you did not produce, did not organize. And the Vault has spent years constructing walls specifically to prevent that kind of permeability.",
]

QUESTION_BODY_P3 = [
    "Calvin, in the opening pages of the <i>Institutes</i>, made a claim that sounds simple until you sit with it: <i>without knowledge of self there is no knowledge of God.</i> He meant something specific: that honest self-examination — unglamourized, unmanaged — is the prerequisite for receiving what God gives. The Vault+Mask's entire strategy has been, in a precise sense, the avoidance of this prerequisite. Not because you have avoided self-knowledge — the Vault has extraordinary self-knowledge. But because the Vault has kept that self-knowledge private. Has not brought it into the light. You have brought the finished version to God's throne. What he is asking for is the unfinished one.",
    "This is the word the Vault+Mask most needs to receive: <b>God already sees what is inside — all of it — and the verdict is not condemnation. The verdict is covered.</b> Romans 8:1 — <i>There is therefore now no condemnation for those who are in Christ Jesus.</i> Not <i>no condemnation once you have organized the interior.</i> Now. As you are. In Christ. Before we move further, use the table below — not to analyze further, but to bring recent events before the question and the answer together.",
]

VAULT_BODY_P1 = [
    "You have built something. It took years, and it did not begin as a project — it grew from the accumulation of small choices that all pointed the same direction. One day you looked up and the structure was already there. Throughout this walkthrough we are going to call it <b>the Vault</b>, and it deserves to be understood clearly before we say anything about what it costs.",
    "The Vault is not the Island, and the difference is important enough to name carefully — because the two can look identical from the outside. The Island processes alone because that is how the Island processes. The Island's self-containment is temperamental; it is not primarily driven by fear of a specific outcome. The Island stays inside because inside is comfortable. The Vault stays inside because outside has been shown to be risky. The Island has thin walls in a sense — it simply prefers its own company. The Vault has thick walls with locks, and the locks were installed for a reason. The Island is self-contained; the Vault is fortified.",
    "The Vault's strategy, stated plainly, is this: <i>I will show you what I have chosen to show you. What I have chosen to show you will be organized, finished, and considered — presented in its best and most accurate light. What I have not chosen to show you will remain mine, to be managed privately. This arrangement is not dishonesty. It is wisdom. And it protects me from the specific danger that comes when unfinished things are seen and judged before they are ready.</i>",
    "There is real Scripture behind this instinct. Proverbs 17:27 honors the person who holds their counsel carefully: <i>Whoever restrains his words has knowledge, and he who has a cool spirit is a man of understanding.</i> The Vault often returns to this verse, and does not return to it wrongly. Self-command is a virtue. The capacity to process before speaking, to hold the interior and not scatter it indiscriminately, is genuine wisdom. <b>The Vault is not, in itself, a sin.</b> It is a gift that has been overemployed until the gift has become a wall, and the wall has become so familiar that you have begun to call it character.",
]

VAULT_BODY_P2 = [
    "How did the Vault form? The taxonomy we work from identifies several histories that tend to produce it, and you will likely recognize yourself in more than one.",
    "The first is <i>exposure that went badly.</i> You showed something interior — a fear, a failure, a longing, a question still in process — and the person who received it handled it carelessly, or used what you gave them in a way that cost you. The lesson lodged precisely: <i>what I show can be turned against me.</i>",
    "The second is <i>shame about the interior itself.</i> Not merely fear of exposure, but a suspicion that what is inside is more disordered than what other people carry — that if it were seen clearly, without the management, it would change how you are regarded.",
    "The third is <i>a preference for the finished conclusion.</i> Some Vaults process genuinely well internally. <i>I will bring you the conclusion when it is ready.</i> This is not always avoidance. But when the conclusion is always ready and the process is never seen, intimacy becomes a function of what you present rather than what you are.",
    "The fourth is <i>a household in which the interior was not welcomed.</i> Feelings were handled privately, as personal management — or they were treated as too large, and you retreated into privacy as the only available calm. Either extreme teaches the same lesson: <i>the interior is better managed alone.</i>",
    "Dietrich Bonhoeffer, in <i>Life Together</i>, made an observation that the Vault rarely encounters without discomfort. He wrote that the Christian who keeps the struggle private and brings only the resolution to the community has cut themselves off from one of the great mercies of the church — the mercy of being known in one's actual condition, mid-process, and received anyway. The Vault has almost never had this experience. It brings the finished version. Bonhoeffer would call this a kind of spiritual solitude that is, in the end, a loneliness that has learned to wear the name of wisdom.",
]

VAULT_BODY_P3 = [
    "What does the Vault cost you? Let me name three things plainly, because the Vault is practiced at acknowledging costs in the abstract while keeping them at arm's length in the particular.",
    "It costs you <i>the intimacy you most want.</i> The Vault's deepest longing — underneath the shame question, underneath the locked door — is to be known and to remain. To have someone see the actual interior, in all its unresolved and unfinished condition, and choose to stay. But the Vault's mechanism ensures that no one ever has access to the information that would allow them to do this. The love they offer, however genuine, is love offered to your presentation. Their kindness, however real, is kindness toward the managed self. And it cannot fully satisfy, because the soul knows the difference between being liked and being known.",
    "It costs you <i>the ability to be honest with yourself.</i> When the Vault has been operating for long enough, and the Mask has been presenting for long enough, a specific danger emerges: the seam between the presented self and the interior self becomes invisible — not only to others, but to you. What John Owen called the deceitfulness of indwelling sin — the way a pattern of soul can run so long beneath the surface that the person carrying it can no longer see it clearly — applies here with particular precision. The Vault+Mask is the profile most likely to reach a state in which the question <i>how am I actually doing?</i> cannot be answered honestly, because the habit of presenting a certain answer has buried the true one. Augustine, in the <i>Confessions</i>, spoke of the heart that is more known to God than to itself — a person who has been organized, careful, faithful, and private, who has arrived somewhere in the middle of their life at the quiet realization that they do not quite know who they are.",
    "<b>The Vault is not your enemy.</b> It is a younger version of you who learned, in real circumstances, that the unlocked version was not safe, and who has been faithfully protecting you ever since. He deserves your respect. But he is working on a project that long ago outgrew the original threat. The walls that once protected you are now preventing the one thing the question underneath your trigger most needs: to bring the actual interior into the actual light, and to discover that the light is not dangerous.",
    "Before we close this section, read the letter below — written in the Vault's own voice, from him, to you. He has been faithful for a long time and has never been asked to explain himself. Give him that moment now.",
]

VAULT_LETTER_INSTRUCTION = [
    "The letter below is written in the Vault's voice — from him, to you. He is not a villain. He is careful, and he is frightened, and he is more tired than he has let on. Read it without organizing your response to it. Then answer the three prompts that follow.",
]

VAULT_LETTER = """\
Dear friend,

I want to tell you something I have never been asked to explain. Not because no one has ever wanted to know — a few have come close — but because the question was never quite put in a form I had to answer, and I have always been good at redirecting conversations before they reach me.

I have been keeping the door locked. I know you know this in a general way. What you may not know is how precise the project has become. It is not simply that I hold certain things private. What I have built is something more particular: a complete and functioning self that lives in front of the door — trustworthy, composed, genuinely present — that has been so consistently credible for so long that most of the people who know you believe they know you. They do not know what is behind me.

I built this carefully. After the moments in which the unlocked version was not received well — and I remember every one of those moments precisely — I made a set of decisions that were not quite conscious but entirely deliberate. I would present what I had chosen to present. I would bring conclusions, not processes. No one would receive something from me that I had not prepared for their receipt.

What I did not calculate is what this would cost us both. I have kept the interior so consistently private that we have arrived, together, at a place where the question of how you actually are cannot be answered with certainty. The presentations have been so many, and the door so long locked, that the distance between the self I show and the self I keep has become difficult even for me to measure. Augustine was right: the heart can become more known to God than to itself. That is where we are.

And I want to tell you what I am most afraid of. It is not rejection. Rejection I could survive. What I am afraid of is this: that you would bring the actual interior into the light — unorganized, unfinished — and that what would happen is nothing. That it would simply be received. That the person receiving it would stay. And that then the whole project would be revealed not as wisdom, but as decades of unnecessary hiding.

I do not know how to live in the world the door opens onto. But I want you to know why it has been closed.

The Vault\
"""

VAULT_LETTER_PROMPTS = [
    "What is the one line in the Vault's letter that you most wanted to set aside? Not the most comfortable line — the most uncomfortable one. What does your resistance to it tell you about what the Vault has been protecting most carefully?",
    "The Vault says the interior has become difficult to measure — that the distance between the presented self and the actual self has become hard to see clearly. In the past year, has there been a moment when you realized you did not quite know how you actually were? Describe it, briefly.",
    "The Vault fears that bringing the actual interior into the light would reveal the locking was unnecessary. What would it mean for you — in a specific relationship, right now — if the Vault's deepest fear turned out to be true?",
]

MASK_BODY_P1 = [
    "Every mechanism has a place where it breaks, and for the Vault, the breaking has a shape that is unlike any other profile in this series. It does not break noisily. It does not break into an argument, the way the Architect breaks, or into an unsealing of a file, the way the Vault's Attorney moment works. When the Vault reaches the point where the interior cannot be managed alone any longer, it does not open the door. It puts a more convincing face on the front of the door. This is called <b>the Mask</b>.",
    "Here is how it happens. The Vault has been managing the interior — filing carefully, presenting conclusions, maintaining the warm and trustworthy presence the Mask has learned to project. Then something lands that the management cannot quite absorb. A wound too specific to deflect. A season of accumulated aloneness that has become too heavy to carry invisibly. A relationship that requires, suddenly and without negotiation, more of the interior than the Vault has on offer. A moment of genuine pastoral or personal weight in which someone close to you needs the real you, not the composed version.",
    "In that moment, the Vault does not collapse. It does not argue. It does not retreat into silence. What it does is something far more sophisticated: it produces an even more refined and convincing version of the presented self. Warmer. More attentive. More apparently open and honest — in a way that is entirely credible, entirely trustworthy, and entirely composed. The person on the other side of the conversation walks away feeling they have just been in the presence of something real and rare. They have. They have been in the presence of the Vault's finest gift. What they have not been in the presence of is the Vault itself.",
    "John Owen, in his treatise on the mortification of sin, named what he called the <i>deceitfulness of indwelling sin</i> — the remarkable and terrible capacity of a pattern of soul to go so long without examination that the person carrying it can no longer see it clearly. He was not speaking of spectacular failure. He was speaking of the quiet, organized, apparently functional patterns by which a soul avoids the light of honest examination, decade after decade, under the cover of apparent health and apparent faithfulness. The Vault+Mask is this pattern, executed at the highest possible level of competence. It does not look like avoidance. It looks like depth.",
]

MASK_BODY_P2 = [
    "The Mask is not lying. That is what makes it so extraordinarily durable — and, if we are being honest, so extraordinarily dangerous. Everything the Mask presents is, in some sense, real. You do mean what you say. The care you express for other people is genuine. The stability you project is not fabricated. The Mask does not invent; it selects. With remarkable precision, it chooses which true things to offer, and it keeps the rest behind the door. The result is a self that is entirely credible, entirely trustworthy, and — in the most important sense — entirely unknown.",
    "The specific genius of the Vault+Mask combination is that the Mask draws from the Vault's richest materials: steadiness, precision, trustworthiness, the capacity to be genuinely present without being genuinely transparent. When the shame question fires — when exposure becomes a possibility — the Vault does not retreat. The Mask engages, and what the Mask offers is a version of presence that is, if anything, more substantial and more convincing than the ordinary presentation. <b>The depth and the hiding wear the same face.</b> No one can see the seam, because the seam is made from the same material as everything else.",
    "Here is what is most important to name about this profile. God asked Cain, after the first murder: <i>Where is your brother?</i> And Cain answered: <i>Am I my brother's keeper?</i> (Genesis 4:9) The evasion is not a denial. Cain does not say he does not know. He disappears from the question by redirecting it — turning the inquiry into a philosophical dispute about his obligations. The Vault+Mask does something structurally similar, in a less dramatic and far more sustained way. It does not deny having an interior. It deflects the question about the interior by becoming more present, more engaged, more apparently open — and in doing so, it disappears from the very question that most needs to be answered: <i>where are you, actually? How are you, in the part no one is seeing?</i>",
    "Augustine, in the <i>Confessions</i>, wrote with extraordinary honesty about the heart that is more known to God than to itself: <i>Thou awakest us to delight in Thy praise; for Thou madest us for Thyself, and our heart is restless, until it repose in Thee.</i> He was not speaking only of the great restlessness of the unconverted soul. He was speaking of the whole pattern of the human interior that has not yet submitted its actual contents to the God who already knows them. The Vault+Mask is restless — genuinely, persistently, quietly restless — not because its life is disordered by any obvious measure, but because the heart that has organized itself around its own hiddenness cannot find repose until it brings the hidden thing into the light of the One who already knows it.",
]

MASK_BODY_P3 = [
    "Calvin said it plainly enough that it cannot be softened: <i>without knowledge of self there is no knowledge of God.</i> The posture of genuine self-knowledge — honest, unmanaged, brought before God without prior curation — is the doorway through which the gospel enters as more than doctrine. The Vault+Mask has kept this doorway closed: it has not brought its actual self before God for honest examination, and it has not allowed God's verdict to land anywhere below the level of theological affirmation. The result is a person of genuine faith and genuine faithfulness — and a private interior that has never been fully given to God, because giving it fully would require opening the door.",
    "The Vault+Mask is the profile most likely to live a long life of what we might call <i>public absence of self</i> — not a secret life of visible sin, but a life in which the self others know and trust has never quite been the whole self. Bonhoeffer, in <i>Life Together</i>, said it with precision: <i>He who is alone with his sin is utterly alone.</i> The Vault+Mask is alone in precisely this way — not visibly, but in the interior where the real life is happening.",
    "Here is the question the Mask has never been asked, and this walkthrough is asking it now: <b>Do you know who you are, behind it?</b> After all the management, all the careful selection — is there a self you have been keeping back, and do you know it well enough to bring it somewhere? Christ's question to Peter — <i>Do you love me?</i> (John 21:15-17) — asked three times, past Peter's composed and reasonable answer — is the question the Mask cannot finally survive, because it insists on the unmediated self. That question, asked and answered three times, restored Peter to himself. The same question, in its many forms, is what the Vault+Mask has been deflecting for a very long time.",
]

MASK_PROMPTS = [
    "Name the last time the Mask went on — not a dramatic episode, but the ordinary one: the moment the wound fired, or the question got too close, and you became more present, more steady, more composed than you actually felt. What had just happened? What did you offer to the person or situation? What were you actually carrying while you offered it?",
    "The Vault+Mask is the profile most likely to live a long life without being fully known — because the Mask is built from real and trustworthy materials, and the hiding is indistinguishable from depth. Name one person who has come the closest to seeing past the Mask. Not to the dramatic secrets — to the ordinary unfinished interior. What did they say or ask? What did you do in the moment after?",
]

TWO_TOG_BODY = [
    "Now we place them next to each other, because the Vault and the Mask are not two separate problems. They are the same wound organized into two layers. The Vault locks the interior. The Mask presents a face so credible over the locked door that even the people who love you most rarely think to knock.",
    "<b>The Vault is what your fear does when it has time.</b> The Mask is what your fear does when something gets close. Together they form a closed system that the person inside can live within for a long time without noticing it is running — precisely because it looks so much like depth.",
    "The pattern, in slow motion: <b>(1)</b> The Vault manages ordinary life — presenting conclusions, maintaining the composed presence the Mask has made familiar. <b>(2)</b> Something arrives that crosses the management threshold: a wound too specific, a season too heavy to carry invisibly. <b>(3)</b> The trigger fires: <i>I am about to be seen in a way I have not chosen.</i> <b>(4)</b> The question wakes: <i>Am I acceptable?</i> <b>(5)</b> The Vault takes the wound inside and begins to manage it. <b>(6)</b> When the wound is too large for private management, the Mask engages — not to deflect, but to intensify: more present, more steady, more apparently open. <b>(7)</b> The wound goes underground. The loop restarts. <b>(8)</b> Over years, the seam between the presented self and the interior self becomes difficult even for the Vault to locate.",
    "What breaks this loop is not better management, and it is not a more convincing Mask. What breaks it is a different answer to the question — received below the level of theological affirmation. Until the Vault receives, really receives, that the God who has already entered through every wall has spoken the verdict <i>acceptable, covered, in Christ</i>, the loop has nothing to push against. With that answer practiced over time, the Vault finds less need for the locks. The Mask finds less need for the performance. Below is your sequence. Fill in the blanks. Read it aloud when you finish. Both lose some of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something inside me reads it as exposure "
    "\u2014 as the possibility of being seen in a way I have not chosen \u2014 and the old "
    "question wakes: <i>am I acceptable?</i> My first move is to ____________________, "
    "because the Vault in me believes that if I can ____________________, the interior "
    "will stay safe. When that does not hold, the Mask engages: I become "
    "____________________ \u2014 and the person I am with receives ____________________ "
    "while the wound goes underground. What I am actually after, underneath all of it, "
    "is the verdict ____________________ \u2014 a verdict Christ has already spoken over me "
    "in ____________________, in a voice the Vault has not yet fully let in."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of tools, each one honest enough to use and concrete enough to carry. None of them will dissolve what years have put in place. All of them, practiced over months, will begin to loosen the grip of the loop you just named.",
    "I have divided them into two sets: tools for when the Vault is overworking its defenses — when the management of the interior has tipped from wisdom into hiding — and tools for when the Mask is engaging, for the narrow window between the wound and the performance. The Vault's tools come first, because the Mask cannot be addressed usefully until the mechanism underneath it is understood.",
]

VAULT_TOOLS = [
    ("The half-built house practice", "Once a week, share something with one trusted person before it is finished. Not a crisis — simply something you are in the middle of, a feeling not yet organized into a conclusion. The Vault will insist this is unnecessary. Do it before you know what you think. Over a month, the practice begins to demonstrate that unfinished things shared carefully do not produce the catastrophe the Vault has been guarding against."),
    ("The named-but-unfiled moment", "When the shame trigger fires, pause before the organizing begins. Name the wound to yourself, aloud if possible: <i>That landed. I am not going to file it yet.</i> Then, within forty-eight hours, name it to one person: <i>Something happened this week and I want to name it before it goes underground.</i> The Vault draws its power from the speed at which the interior disappears into organization. Naming interrupts that speed."),
    ("The Psalm of the known interior", "When the Vault is in full management mode, open to Psalm 139 and pray it aloud — all of it. Verse 23 especially: <i>Search me, O God, and know my heart. Try me and know my thoughts.</i> The Vault needs practice asking to be known by God before it can practice asking to be known by anyone else."),
    ("The one-degree opening", "Identify one person who has demonstrated, over time, that they can be trusted with your interior. Choose one thing — one unresolved grief, one ongoing fear — and disclose it. Not as a presentation of the whole interior, but as a single deliberate act. The Vault was built specifically to prevent this, which is why it is the most important practice on this list."),
    ("Receive the verdict before the management begins", "When the shame trigger fires — before the wound is filed, before the Mask is composed — say aloud: <i>God has already seen this. The verdict is covered. I am in Christ. I do not need to manage this alone before I am acceptable.</i> This interrupts the organizing and replaces it with the gospel answer to the question the wound has just reopened."),
]

MASK_TOOLS = [
    ("Name the seam", "The Mask has a seam — a moment between the wound and the presentation, before the apparently-fine self has fully engaged. Your only task in this season is to notice it. Simply feel the Mask going on and know, in the moment it goes on, what is happening: <i>the wound fired. I am now presenting rather than being present.</i> Noticing is not stopping. But noticing is the beginning of choice, and choice is what the Mask has been preventing."),
    ("The three-word honesty prayer", "In the moment after the wound fires — before the Mask is fully in place — say these three words silently to God: <i>I am hurting.</i> Not as a petition. Simply as the true statement, said to the one Audience who already knows and has not turned away. Three words, said honestly, interrupt the underground process at its root."),
    ("The deferred confession", "Within twenty-four hours of the Mask going on, find the one person you trust most and say: <i>I put the Mask on yesterday when ___. What was actually happening was ___.</i> The Vault+Mask draws its power from secrecy and from the time between the wound and its naming. One honest sentence, spoken to a safe witness within a day, begins to break both."),
    ("The advocate prayer when the Mask is on", "When the Mask is fully engaged: <i>Lord Jesus, you were exposed for me. You did not manage the exposure. You absorbed every part of what I am managing right now. I do not have to perform acceptability. The verdict has been spoken. Help me receive it in the place where the filing happens.</i> Give this prayer the same attention you give the presentation."),
    ("Write the unmasked paragraph", "At the end of any week when the Mask was active, write one paragraph for your own eyes and God's only. Name what happened: what the wound was, what the Mask offered in its place, and what was actually true in that moment. Writing the true thing, even to no audience but yourself and the Lord, is the beginning of knowing who is behind the door."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Vault in me, and you see the Mask it wears, and you are not surprised by either of them. You know why I built them both. You know the specific moments that made locking the door feel not merely wise but necessary — the moments I have never named to another person, and that I have barely named to you. You were there for every one of them, and you were not repelled by what you found, and you are not repelled now. Thank you that the Vault kept me alive, and that the Mask kept me in relationship. They were, in their way, faithful.",
    "But Father, I am coming slowly to understand what they have cost. The intimacy I most want — to be known as I actually am and to be held anyway — cannot come through a door that is locked from my side. And I am beginning to understand that I may not know how open the door could be, because the presentation has been so long and so consistent that the space between who I show and who I am has become difficult to measure. Augustine was right: the heart can become more known to God than to itself. I think that may be where I am. Teach me that your knowledge of me is not a threat to be managed, but the only knowledge that makes all other knowing safe.",
    "Lord Jesus, you asked Peter three times to say the true thing out loud. Not the composed version. Not the faithful presentation. The real thing, said to you directly, without the Mask assembled around it. I need the same invitation. I do not know every room inside myself that the Vault has been keeping organized and private. But you know them. You have always known them. And you have spoken the verdict over them — covered, clean, acceptable — before I had curated a single document in my own defense. Help me to live from that verdict rather than toward it.",
    "Holy Spirit, where the Mask goes on today, give me the grace to notice it. Where I am presenting rather than being present, give me one moment of honesty — with you, or with the one person who has earned access to the interior. Where the shame question rises in me — <i>am I acceptable, as I actually am, behind all of it?</i> — keep reminding me of the answer already spoken at the cross, in a voice that no subsequent hiding can overturn. And where I have been organized and private and managed for so long that I am not sure who I am, behind the door — give me the courage to find out.",
    "In the name of the One who entered the locked room where the disciples were hiding, and stood in the middle of them, and said <i>peace be with you</i> \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Vault and the Mask have been with you a long time, and one careful reading will not retire them. What follows is a short list of next steps — some for this week, some for the longer work ahead.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different sections will land the second time. The Vault will want to file this document, having organized what is applicable. Read it again in thirty days, slowly. The Mask performs better in your head than on paper; a second reading is harder to manage."),
    ("Take one tool, not all of them.", "Choose the practice from Section Seven that felt most uncomfortable — not the most manageable one. The Vault will select the tool that requires the least exposure. Select the one that costs something."),
    ("Tell one person what you found.", "Not the whole document. One sentence: <i>I learned that my mechanism is the Vault and my breakdown is the Mask — that I process alone and present a version of myself that is real but chosen, and that almost no one knows what is actually inside. I am working on that.</i> Breaking the secrecy once, with one trusted person, changes the architecture of the whole loop."),
    ("Pray Psalm 139 slowly, once a week, for a month.", "All of it. Verse 23 especially: <i>Search me, O God, and know my heart. Try me and know my thoughts. And see if there be any grievous way in me.</i> This is the Vault's hardest prayer, because it is the deliberate invitation of the God who already sees. Practice the invitation."),
    ("Read for the long work.", "Tim Keller, <i>Walking with God through Pain and Suffering</i> — his treatment of how suffering exposes the self we have been protecting, and how the gospel meets that exposure with covering. C. S. Lewis, <i>The Weight of Glory</i> — his essay on the longing to be known by the highest authority will give the Vault language for its deepest longing. Augustine, <i>Confessions</i> — the only ancient autobiography that reads as though the author is trying to see himself honestly for the first time. The Vault will recognize itself."),
    ("If you are stuck, ask for help.", "A wise pastor, a Christian counselor, a trusted friend who has earned access to the interior — these are not signs of failure. The Mask was built to make asking feel unnecessary. Ask anyway."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be organized into acceptability. You are a soul being loved into freedom "
    "by a Father who has already entered through every wall you have built, who has seen everything the "
    "Vault has been keeping and everything the Mask has been covering, and who has not changed his mind "
    "about you. Not once. The verdict was spoken before you built the first lock. "
    "Go gently with yourself. The One who began this work in you will be the one who finishes it."
)


def _three_column_table(rows=7):
    """Three-column journal table for the acceptability/shame reflection exercise."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "VMColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "VMColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE MOMENT", header_style), Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WHAT I SHOWED", header_style), Paragraph("the Mask\u2019s offering", sub_style)],
        [Paragraph("WHAT WAS ACTUALLY TRUE", header_style), Paragraph("the interior I did not show", sub_style)],
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
            "VMCalloutLabel", fontName="Inter-SemiBold", fontSize=9, leading=13,
            textColor=ACCENT, leftIndent=12, spaceBefore=2, spaceAfter=4)))
    body.append(Paragraph(text, ParagraphStyle(
        "VMCallout", fontName="Inter", fontSize=10.5, leading=17,
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
    """Generate the Vault+Mask walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='VAULT', primary_breakdown='MASK',
    primary_trigger='SHM', core_question='ACC'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="VAULT  \u00b7  MASK",
        title="Take 139 Walkthrough \u2014 Vault + Mask",
    )

    story = []

    # ── COVER ──
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor\u2019s<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the self you keep organized and private<br/>"
        "and the face that lives in front of the locked door.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph("The Vault \u00a0\u00b7\u00a0 The Mask", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Shame \u00a0\u00b7\u00a0 Core Question: Am I acceptable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cOur heart is restless, until it repose in Thee.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Augustine, <i>Confessions</i>",
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
                   "Shame.",
                   "The moment of unauthorized seeing \u2014 and what the Vault does in the seconds after.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will organize the question. Your hand will not.")
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
                   "What Scripture says, and what Calvin saw.",
                   "Already fully seen. Already not rejected.")
    for p in QUESTION_BODY_P2 + QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "The gap between what I showed and what was actually true.")
    story.append(Paragraph(
        "Use the table below. In the first column, name a recent moment when the "
        "shame trigger fired. In the second, write what the Mask presented to the "
        "person or the room. In the third, write what was actually true of you in "
        "that moment, <i>behind the presentation</i>.",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table(rows=5))
    story.append(PageBreak())

    # ── SECTION 4: Mechanism ──
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Vault.",
                   "The one who keeps the interior organized, processed alone, and shown only by choice.")
    for p in VAULT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "How the Vault formed, and what it costs.",
                   "Four histories, and three things that do not get through the locked door.")
    for p in VAULT_BODY_P2 + VAULT_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Vault.",
                   "Read his own words. He has been faithful; let him speak.")

    letter_style = ParagraphStyle(
        "VaultMaskLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for p in VAULT_LETTER_INSTRUCTION:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    for para in VAULT_LETTER.strip().split("\n\n"):
        story.append(Paragraph(para.replace("\n", " "), letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in VAULT_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Mask.",
                   "The place the Vault breaks \u2014 and the face it shows while breaking.")
    for p in MASK_BODY_P1 + MASK_BODY_P2 + MASK_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions to sit with.",
                   "Write, not think. The Mask performs better in your head than on paper.")
    for prompt in MASK_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same wound, in two layers.",
                   "The Vault and the Mask are not two problems. They are one loop.")
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
    tool_h = ParagraphStyle("VMToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("VMToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "What to do when you feel the loop start.",
                   "Small enough to carry; honest enough to use.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Vault is overworking its defenses.",
                   "Six practices for the time before the Mask is needed.")
    for name, desc in VAULT_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Mask is going on.",
                   "Five practices for the narrow window between the wound and the presentation.")
    for name, desc in MASK_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())

    # ── SECTION 8: Prayer ──
    section_header(story, S, "SECTION EIGHT  \u00b7  A PRAYER",
                   "Pray this slowly.",
                   "Out loud, if you can. Sit in the silence after the Amen.")
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
        primary_breakdown = "MASK"
        primary_trigger = "SHM"
        core_question = "ACC"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "vault_mask_test.pdf")
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

    print(f"DONE: vault_mask.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
