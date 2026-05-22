"""Personal Walkthrough — Performance Campaign + Mask.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Shame trigger, "Am I acceptable?" core question.
~25 pages, 9 sections.

Calibration anchor: Walkthrough #34 of 36. The most professionally rewarded
of all the Mask breakdowns. The Performance's natural persona — competent,
capable, in command — IS the mask. The audience does not see a mask; they see
excellence. The Performance themselves often does not see a mask; they see a
self that has worked.

The breakdown is the Performance who has so successfully built the persona of
"the one who has it together" that when they suffer, they cannot put the
suffering down. They give the talk anyway. They preach anyway. They ship the
deliverable anyway. They smile in the meeting anyway. And meanwhile the gap
between the seen self and the actual self grows wider until something gives.

KEY THEOLOGICAL MOVES:
- Galatians 6:2: the Performance+Mask has made themselves unbearable in the
  literal sense — no one is allowed to carry their weight.
- Jonathan Edwards: grace is a gift received by an open hand. The Performance
  has trained itself into a closed fist.
- C. S. Lewis, The Screwtape Letters: the "long, dull murmur of a soul's
  surrender to itself" — not sudden corruption, but slow domestication of
  grace by competence.
- Keller, The Reason for God: the impossibility of being saved by accumulating
  moral credit.

DISTINGUISHING FROM OTHER MASK BREAKDOWNS:
- Island+Mask: warm friend behind glass.
- Ambassador+Mask: celebrated leader hiding under cloak of grace.
- Vault+Mask: double-locked hiding.
- Adapter+Mask: the Adapter who has stopped translating.
- Performance+Mask: excellence IS the disguise. The persona never looked like
  a mask — it looked like character. This is why it is the last to be named.
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
    "Before you read any further, I want to do for you what a good counselor does in the first "
    "minutes of a genuinely difficult conversation. I want to lower the lights and slow the pace, "
    "because what you are about to encounter is not a personality assessment. It is not a "
    "celebration of your capabilities, though you have real ones. It is something more "
    "uncomfortable than either of those things: a patient, honest look at the way your soul has "
    "learned to survive by becoming someone it does not have to feel ashamed of.",

    "You are, in a deep and specific sense, a runner. Not necessarily a literal runner, though "
    "the metaphor fits: you move forward at speed, you build things, you demonstrate, you "
    "produce. You discovered, early in life, that the path from invisible to valued ran through "
    "achievement. And you ran. Over years, the running produced something extraordinary. You "
    "became the person who had it together. You became the one people leaned on, the one the "
    "room depended on to keep the standard high, the one who always delivered. And here is "
    "the thing that no one told you, and that this walkthrough is going to name plainly: "
    "<b>the person you became was, in part, a mask.</b> Not a deception. A performance of "
    "competence so sustained, so genuinely inhabited, that even you stopped being able to "
    "see the seam between the person and the persona.",

    "We are going to walk through your trigger \u2014 the specific moment your body "
    "registers that something has gone wrong with the question of your worth. We will sit "
    "with the question underneath that moment, the one that has been with you since the "
    "first time you understood that some people are accepted and some are found wanting. "
    "We will name the Performance Campaign you have built in response, and then we will "
    "look carefully at the Mask \u2014 the breakdown that is most particular to your "
    "profile, the one that does not look like a breakdown at all because it looks, "
    "from the outside, like professionalism.",

    "If you were sitting across from me, I would say this plainly and mean every word. "
    "<b>What you are about to read is true, but it is not the whole truth about you.</b> "
    "The whole truth includes a Father who has been watching the Campaign run for decades, "
    "who has not once been impressed by the output and not once reduced in his love by "
    "the failures, and who has been waiting, with great patience, for the day when you "
    "allow him to carry something for you. A Son who, in the hours before his own arrest, "
    "said: <i>my soul is very sorrowful, even to death</i> \u2014 who did not manage "
    "that admission, did not give the talk anyway, did not smile in the meeting anyway, "
    "but sat in a garden and told his closest companions that he needed them near. And a "
    "Spirit who is not interested in the polished version you bring to every room. He is "
    "interested in the one underneath it.",

    "So read slowly. The Performance in you will want to extract what is useful, apply it "
    "efficiently, and count this walkthrough as a completed project. Resist that. Argue "
    "with what does not fit. Stay with what catches in your throat. Pray when something "
    "lodges, because that lodging is usually the Lord saying: <i>look here, with me, at "
    "what you have been carrying alone.</i> The goal of this walkthrough is not "
    "better performance. It is a slightly freer life \u2014 one in which the gap between "
    "the seen self and the actual self begins, slowly, to close. Take your time. "
    "This chapter has been running a long time. It deserves a few hours of careful attention.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it is unusually hard to catch because "
    "it hides so effectively inside experiences that look, from the outside, like simple "
    "perfectionism. You present something you worked hard on, and someone offers a mild "
    "correction, and something inside you goes very cold, very fast. A colleague receives "
    "credit for work that was partly or largely yours. A superior passes over your judgment "
    "in favor of a less experienced opinion. Your spouse, in a quiet moment, mentions that "
    "you seem unreachable \u2014 that they are not sure they know what is happening inside "
    "you these days \u2014 and the comment lands not as a question but as a verdict.",

    "What fired in that moment was not irritation, though irritation will arrive shortly. "
    "What fired was an alarm with a very specific frequency: <i>something about me, as I "
    "actually am, has been found insufficient.</i> Not the output \u2014 the output may "
    "have been excellent. The self behind the output. The one who is tired, who has doubts, "
    "who has been giving talks and preaching sermons and arriving early and staying late "
    "and smiling in every meeting \u2014 that self. The one who is, today, not certain "
    "whether it is acceptable.",

    "This is your trigger. The technical word for it is <b>shame</b> \u2014 not the "
    "theatrical kind, the kind accompanied by public disgrace. The quieter, more durable "
    "kind: a self that suspects, at the level of bone rather than intellect, that if the "
    "whole thing were ever seen clearly \u2014 the weariness, the uncertainty, the gap "
    "between the public competence and the private confusion \u2014 the verdict would be: "
    "<i>not quite as advertised.</i> The alarm runs continuously in the background, and "
    "the Campaign has been answering it with output for years.",

    "C. S. Lewis, in <i>The Weight of Glory</i>, wrote with characteristic precision "
    "about the longing every human being carries to be known and affirmed by the only "
    "Audience whose verdict finally holds. <i>We do not want merely to see beauty \u2014 "
    "we want to be united with the beauty we see, to pass into it, to receive it into "
    "ourselves.</i> The grammar of your longing is the same. You do not merely want to "
    "be competent. You want the competence to be received \u2014 to settle into the part "
    "of you that is still not sure. When it is acknowledged and still does not settle it, "
    "the pain is proportionate not to the compliment that was missed but to the wound "
    "underneath.",

    "<b>Your sensitivity to this signal is not random, and it is not simply professional "
    "pride.</b> It is the residue of something specific, usually early, that taught you "
    "what it felt like to be found insufficient. Perhaps ordinary effort was unremarkable "
    "while extraordinary effort was noticed and warmed toward. Perhaps you grew up in a "
    "context where the right response to difficulty was to manage it and move forward \u2014 "
    "and you learned this so thoroughly that you eventually could not remember the "
    "difference between managing and being fine. The Performance Campaign was built "
    "from that lesson. You ran. And the running eventually became something more "
    "than a strategy. It became a self.",

    "Before we go further, I want you to sit with two questions in writing. Your head "
    "will want to frame the answers in terms of professional patterns. Ask your hand "
    "to be more honest.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week, that the shame signal fired \u2014 "
    "the moment something registered as <i>I have been found insufficient, or "
    "something about me as I actually am has been seen and found wanting.</i> "
    "It may have been a small moment. Write what happened, and what you did in "
    "the ten seconds after.",

    "What is the gap you have been most carefully managing \u2014 the distance "
    "between who you appear to be in your professional or public life and what "
    "is actually happening inside you right now? Not the gap as you would "
    "describe it to a colleague. The gap as you experience it alone. "
    "Write it plainly.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. "
    "The trigger is the alarm; the question is the wound the alarm has been standing "
    "guard over for a very long time. The Performance Campaign has been answering it "
    "for years with output, with visibility, with the sustained demonstration of what "
    "you can do. The campaign has not silenced it. It cannot. The question is not "
    "a professional problem.",

    "Yours is this: <b>Am I acceptable?</b>",

    "It is worth pausing on the precise shape of this question, because the "
    "Performance is likely to misread it. It is not <i>Am I competent?</i> \u2014 "
    "though you have built extraordinary competence, in part as a way of trying to "
    "answer it. It is not <i>Am I enough to be remembered?</i> \u2014 though you "
    "have spent real energy on the question of legacy. It is something more "
    "fundamental and more frightening than either: the question of a self that has "
    "done remarkable things and is still not certain that the self behind the things "
    "is, apart from them, actually worth keeping. <i>If the campaign stopped. If the "
    "output dried up. If everything I have built were suddenly beside the point "
    "\u2014 would I be acceptable then, as I actually am?</i>",

    "The taxonomy of fear has a name for this profile, and it is the right one. "
    "This is the shame question \u2014 not shame about a specific act, but shame "
    "about a self. And for the Performance, it wears a disguise more convincing "
    "than almost any other profile in the thirty-six. You present so well. People "
    "tend to assume you have it together in a way they themselves do not. The gap "
    "between your exterior and your interior is large, and the maintenance of "
    "that gap is exhausting in ways you rarely let anyone see. John Owen observed "
    "that the sins most dangerous to the soul are not always the ones that "
    "announce themselves in failure, but the ones that have quietly organized the "
    "whole life around their own avoidance. For the Performance, shame is that "
    "organizing principle. And the Campaign is what shame built to keep the "
    "question from ever having to be answered out loud.",
]

QUESTION_BODY_P2 = [
    "There is a reason that the Psalms \u2014 the prayer book that Jesus himself "
    "prayed, and that the people of God have been praying for three thousand years "
    "\u2014 spend so much time in the territory of shame and exposure. The prayer "
    "book did not assume that its users had their interior lives managed. "
    "It assumed the opposite.",

    "<i>My wounds stink and fester because of my foolishness; I am utterly bowed "
    "down and prostrate; I go mourning all the day long . . . I am feeble and "
    "crushed; I groan because of the tumult of my heart. O Lord, all my longing "
    "is before you; my sighing is not hidden from you.</i> (Psalm 38:5\u20136, 8\u20139)",

    "Notice what the psalmist does not do. He does not present well. He does not "
    "manage the impression. He names the festering, the feebleness, the groaning, "
    "without qualification \u2014 because he has located the one Audience before "
    "whom the management project is both unnecessary and impossible. "
    "<i>O Lord, all my longing is before you.</i> You are already fully seen. "
    "The seeing has not produced rejection. This is the foundation on which the "
    "whole walkthrough rests.",

    "The gospel anchor for the shame question is this: <i>There is therefore now "
    "no condemnation for those who are in Christ Jesus.</i> (Romans 8:1) "
    "Not reduced condemnation. None. The verdict was not based on the version of "
    "you that performed well. <i>For our sake he made him to be sin who knew no "
    "sin, so that in him we might become the righteousness of God.</i> "
    "(2 Corinthians 5:21) Christ entered, in his own person, the full horror of "
    "public exposure \u2014 seen, mocked, stripped, found contemptible by those "
    "watching \u2014 and he absorbed that exposure, all of it, so that the verdict "
    "spoken over you in him would not be the verdict your shame has been "
    "predicting all these years.",

    "But here is where the pastoral work gets specific to you. The Performance is "
    "uniquely positioned to hear the gospel correctly and receive it "
    "incompletely. You can state the doctrine of justification with precision. "
    "You have probably taught it. You may have preached it. The difficulty is not "
    "intellectual; the difficulty is interior. Tim Keller, in <i>The Reason for "
    "God</i>, names the core problem: we cannot be saved by accumulating moral "
    "credit, and yet the mechanism every human being defaults to is precisely the "
    "attempt to do so. The Performance's version of this mechanism is not crude "
    "\u2014 it does not claim that God owes you something. It is more subtle "
    "than that. It simply cannot stop running the Campaign, because stopping the "
    "Campaign would require receiving the coverage that has already been provided. "
    "And receiving requires an open hand. The Performance, over years of building, "
    "has trained itself into a closed fist.",
]

QUESTION_BODY_P3 = [
    "The honest work this section asks of you is not to stop producing. "
    "The Performance Campaign is not, in itself, a sin. It is a gift that has "
    "been pressed into the service of an answer it cannot provide. The gift of "
    "sustained excellence, of remarkable output, of capacity to build and lead "
    "and deliver \u2014 these are real, and they were given for genuine purposes. "
    "The question is what the gift is being used to do. There is producing that "
    "flows from a self that already knows it is acceptable \u2014 that creates "
    "from gratitude, from fullness, from the freedom of a person who has nothing "
    "to prove. And there is producing that flows from a self that is still "
    "uncertain \u2014 that creates from anxiety, that cannot stop, that treats "
    "rest as a kind of small death because in the silence the question comes "
    "back. From the outside, these two persons look almost identical. "
    "From the inside, one is free and the other is exhausted.",

    "The runner who already knows they are acceptable can stop. "
    "The runner who is running to become acceptable cannot stop, because stopping "
    "would mean sitting with the question: <i>and if I am not producing anything "
    "today, who am I, and is that person enough?</i> That is the question that "
    "needs to be asked, and answered not by tomorrow's deliverable but by the "
    "verdict already given. Before we move further, use the table below. "
    "Name it, column by column, without the Campaign's usual framing.",
]

CAMP_BODY_P1 = [
    "You have built something. It did not announce itself as a strategy; strategies "
    "are chosen, and this was not entirely chosen. It grew the way a campaign grows "
    "\u2014 from early wins, from the discovery that excellence reliably produced "
    "attention, from the slow accumulation of a track record that eventually "
    "became a persona. We are going to call it, throughout this walkthrough, "
    "<b>the Performance Campaign</b>. And before we say anything about what it "
    "costs you, it is worth saying clearly what it is and what it is not.",

    "It is important to be precise, because the Performance is sometimes confused "
    "with other mechanisms that superficially resemble it. The Performance Campaign "
    "is not the Ambassador. The Ambassador serves in order to be loved \u2014 "
    "pours out warmth and care and relational attentiveness and waits, sometimes "
    "invisibly, for the love to come back. The Ambassador's currency is relational "
    "service. The Performance's currency is visible output. The Ambassador is the "
    "one who stayed late to make sure everyone was all right; the Performance is "
    "the one who stayed late to finish something excellent and wants you to know "
    "about the excellent thing. Both are earning, in a sense. They are earning "
    "different things, and using different methods, and the Mask that results "
    "from each is correspondingly different.",

    "Nor is the Performance the Adapter. The Adapter reads the room and becomes "
    "what the room needs \u2014 translates its real self into whatever language "
    "the context is speaking, fluently and genuinely. The Performance does not "
    "translate to the room. The Performance demonstrates to the room. The Adapter "
    "is asking, at some level, <i>what do you need from me?</i> The Performance "
    "is asking, at some level, <i>do you see what I have built?</i> And there is "
    "a crucial difference between those questions, because the second one requires "
    "an audience, and requiring an audience is the beginning of the "
    "Performance's particular cost.",

    "The Performance Campaign is the runner. It is the builder of visible "
    "competence, the achiever, the person with a long record and, often, a "
    "thin sense of who they are off the field. Its default response to anxiety "
    "is not to plan carefully \u2014 that is the Architect \u2014 and not to "
    "withdraw into solitude \u2014 that is the Island \u2014 but to <i>produce.</i> "
    "When the question fires \u2014 <i>am I acceptable?</i> \u2014 the "
    "Performance's answer is always the same: <i>let me show you one more thing.</i>",
]

CAMP_BODY_P2 = [
    "There is much in Scripture that commends the kind of diligence the Performance "
    "embodies at its best. The Wisdom literature does not romanticize amateur effort. "
    "<i>Do you see a man skillful in his work? He will stand before kings; he will "
    "not stand before obscure men.</i> (Proverbs 22:29) And Paul's word in "
    "Colossians 3:23 is not a word against excellence: <i>Whatever you do, work "
    "heartily, as for the Lord and not for men.</i> The Performance Campaign is "
    "not, at its root, a sin. It is a gift. The runner was given legs and taught "
    "to run, and the running has produced real things of genuine value.",

    "But trouble, as always, is in the purpose the gift is pressed to serve. "
    "The taxonomy we use to understand these patterns names it directly: the "
    "Performance's drive to achieve, build, and demonstrate does something specific "
    "for it. It answers the question <i>am I acceptable?</i> through output. "
    "If I can point to something I built, I know I was here. If I can demonstrate "
    "what I am capable of, the question of what I am when I am not demonstrating "
    "anything recedes, at least temporarily. The producing is not merely "
    "vocation; it is an argument. <i>I was here. I did this. The evidence is "
    "on the table. Whatever you find inside me, the outside is not in question.</i>",

    "The specific history that produces the Performance Campaign takes several "
    "forms. Perhaps ordinary achievement was unremarkable in your household while "
    "extraordinary achievement was noticed and warmed toward. Perhaps you grew up "
    "feeling genuinely invisible \u2014 in a large family, a distracted or "
    "depressed household, a school where the quiet student disappeared \u2014 "
    "and excellence became the reliable antidote: <i>if I am extraordinary enough, "
    "I cannot be overlooked.</i> Perhaps there was loss in your family of origin "
    "and you became the one who would redeem the name. Perhaps the drive to leave "
    "something permanent is partly grief looking for somewhere to live. Whatever "
    "the specific origin, the lesson arrived with the force of a conviction, and "
    "the Campaign began.",
]

CAMP_BODY_P3 = [
    "Whatever its specific shape, the Campaign arrived with characteristic "
    "features. The pursuit is genuinely energizing: the building, the vision, "
    "the satisfaction of a thing done with real excellence. Rest, by contrast, "
    "does not fill you in the same way. Rest feels, if you are honest, like a "
    "kind of exposure \u2014 not physical fatigue, but the cessation of forward "
    "movement, the afternoon when there is nothing to demonstrate and nothing "
    "to produce, and the question that the producing has been holding at bay "
    "is allowed to surface again. Your spouse, or the person who has known you "
    "the longest, has probably said some version of the same sentence more than "
    "once: <i>I feel like I can't reach you when you're in this mode. I feel "
    "like an afterthought.</i> They are not wrong. The Campaign's visibility "
    "problem is precise: it sees the next deliverable with great clarity, and "
    "the people standing quietly in the room \u2014 wanting simply to be with "
    "you, not to evaluate your output \u2014 blur at the edges.",

    "Hear me carefully. <b>The Campaign is not your enemy.</b> It is a younger "
    "version of you who learned, in some real and specific circumstance, that "
    "excellence was the reliable path to being acceptable and that being "
    "acceptable was necessary for being safe. The Campaign has been faithful. "
    "It has produced genuinely remarkable things. It deserves your respect. "
    "But it is no longer young, and you are no longer in the household or the "
    "school or the early context that required it. It is running a race on a "
    "track that does not lead where it thinks it leads. The finish line it is "
    "pursuing \u2014 <i>finally acceptable, finally enough, finally safe from "
    "the question</i> \u2014 is not at the end of that track.",

    "What does it look like to begin giving the Campaign shorter hours and a "
    "different mandate? It begins with the question the Campaign almost never "
    "asks, because the asking requires stopping: <i>what do the people who love "
    "me want from me that my excellence cannot give them?</i> The letter below "
    "is the Campaign's attempt to answer that question in its own voice. "
    "Read it slowly. The Campaign is not accustomed to stopping. "
    "Give it a moment.",
]

CAMP_LETTER_INSTRUCTION = (
    "The letter below is written from the Performance Campaign, in his own voice, "
    "to you. He is not a villain. He is a builder who has confused his output "
    "for his worth, and who has been running long enough that he has forgotten "
    "what he was running from. Read it slowly. Then answer the three prompts "
    "that follow."
)

CAMP_LETTER = """\
Dear [your name],

I have been with you for a long time. Longer than you realize, probably, because I do not announce myself. I simply run. I have always simply run. You may have thought that was simply who you are — the one who keeps going, who delivers, who does not let people down, who has never in a professional setting given anything less than everything. That is me. That has been me for as long as you can remember.

I want to tell you something I have never paused long enough to say. I am afraid. Not of failure exactly, though failure is what I am always trying to stay ahead of. I am afraid of the question that lives inside the silence: Is the person behind the output acceptable? Not the competent one. The real one — tired, uncertain, aware of its own gaps in a way the output never shows. I was built specifically to keep that question at bay. As long as I am running, the question does not get a hearing. As long as the deliverable is excellent, the discussion stays on the deliverable and off the deliverer. This has been the whole plan.

Here is what I gave you. I gave you a self you did not have to be ashamed of. A public self so reliably excellent that the private self could stay private indefinitely. I gave you language — the language of leaders, of people who have things in hand. I gave you a room that always takes you seriously. I did not give you rest. I do not know how. I gave you results, and I have always believed that results would eventually answer the question. They have not. You and I both know they have not. The question is not a results-shaped question.

What I have never been able to give you — and what I am only beginning to understand I was never equipped to give — is the safety of being known when the campaign is quiet. I can make you impressive. I cannot make you held. I can produce something that forces acknowledgment. I cannot produce the thing that comes to you when the output stops: the steady assurance that the person behind it is already covered, already named, already acceptable in the only court whose verdict holds. I kept you running precisely to avoid having to find out whether that was true. I am telling you now that I think you are ready to find out.

The Performance Campaign
"""

CAMP_LETTER_PROMPTS = [
    "What is the one line in the Campaign's letter you most wanted to dismiss "
    "or argue with? Write it here, and then write one sentence about what your "
    "resistance to it tells you.",

    "The Campaign says he gave you a self you did not have to be ashamed of, but "
    "could not give you the safety of being known when the campaign is quiet. "
    "Name one person in your life who has ever seen the self behind the output "
    "\u2014 the tired, uncertain, privately struggling one. What was it like to "
    "be seen that way? If no one has ever seen it, name what you think has "
    "prevented it.",

    "The Campaign says the question is not a results-shaped question. Write, "
    "in one sentence, what you think the actual shape of the question is. "
    "Then write, in one sentence, the answer Scripture gives to it.",
]

MASK_BODY_P1 = [
    "Every mechanism has a place where it breaks. For the Performance Campaign, "
    "the breaking has a shape that is, among all the Mask breakdowns in this "
    "series, the most professionally rewarded, the most theologically complex, "
    "and the most difficult to name. It is called <b>the Mask</b>, and the "
    "Performance's version of it is unique among the thirty-six profiles because "
    "the Mask does not look like a mask. It looks like character. It looks like "
    "professionalism. It looks, from the outside, like the kind of steady, "
    "composed, capable presence everyone in the room is grateful for. The "
    "audience does not see a persona being maintained under pressure. They see "
    "excellence. And the Performance themselves, on most days, does not see "
    "a mask. They see a self that has worked.",

    "Here is how it happens. The Campaign has been running \u2014 producing, "
    "building, demonstrating, delivering. And then something arrives that the "
    "Campaign cannot answer with output. A season of genuine grief. A marriage "
    "that has been carrying a wound for longer than either partner has "
    "acknowledged. A failure of consequence that the Campaign cannot quickly "
    "redeem with a better subsequent result. A depression that does not respond "
    "to a change of projects. A spiritual dryness that persists behind the "
    "prepared talks and the careful sermons and the leadership meeting that ran "
    "exactly as planned. The campaign cannot fix this. And in that moment, "
    "instead of putting down the weight, the Performance does something "
    "remarkable: it picks up the weight and keeps going anyway.",

    "The sermon gets preached. The deliverable gets shipped. The talk gets given. "
    "The meeting gets run. The email gets sent. And the person running the "
    "meeting and giving the talk and shipping the deliverable is, in fact, "
    "suffering. But the suffering is not visible, because visibility would "
    "require the Campaign to stop long enough to show it, and stopping feels "
    "more dangerous than continuing. C. S. Lewis, in <i>The Screwtape Letters</i>, "
    "named something that is precise about this pattern. He described the devil's "
    "most effective strategy not as dramatic corruption but as what he called "
    "the long, dull murmur of a soul's surrender to itself \u2014 the gradual "
    "replacement of the real interior with a performance of the interior so "
    "habitual that the person carrying it eventually cannot hear the difference. "
    "The Performance+Mask is not a sudden corruption. It is a slow domestication "
    "of grace by competence. The Performance has trained itself, over years, to "
    "be the one who does not need help. And eventually the training takes, and "
    "the training is indistinguishable from character.",
]

MASK_BODY_P2 = [
    "This is what makes the Performance+Mask different from every other Mask "
    "breakdown in this series. The Island's Mask is the warm friend behind "
    "glass \u2014 it gives attention while keeping the interior perimeter. "
    "The Ambassador's Mask is the celebrated servant who has built a ministry "
    "out of the need to remain loved. The Vault's Mask is the trusted private "
    "person who has built a presentable exterior over a carefully locked "
    "interior. The Adapter's Mask is the translator who has locked into a "
    "single safe persona and stopped translating. All of these Masks adopt "
    "a persona. The Performance's Mask is different in kind: it does not adopt "
    "a persona. It <i>inhabits</i> a self that it has, over years, genuinely "
    "become. The competence is real. The leadership is real. The reliability "
    "is real. <b>The mask is the self, and the self has become the mask,</b> "
    "and the seam between them has been invisible for so long that even the "
    "person wearing it has lost track of where it is.",

    "The pastoral problem with this is precise and serious. It means that the "
    "usual indicators of breakdown are absent. The Performance does not become "
    "warm-friend-behind-glass \u2014 they remain fully present and apparently "
    "engaged. They do not retreat into the Vault \u2014 they continue to show "
    "up and perform. They do not freeze into a single safe persona the way the "
    "Adapter does \u2014 the Campaign is already versatile enough to look "
    "appropriate in every room. What happens instead is a slow widening of "
    "the gap between the seen self and the actual self, with no external "
    "indicator that the gap exists. The gap registers only on the inside, "
    "and the Performance has been treating the inside as proprietary "
    "information for a very long time.",

    "Paul, in Galatians 6:2, gives a command that the Performance+Mask has "
    "quietly made impossible: <i>Bear one another's burdens, and so fulfill "
    "the law of Christ.</i> Notice that the Performance+Mask does not merely "
    "fail to have its burdens borne. It has made itself unbearable in the "
    "literal sense of the word: no one is permitted to carry its weight. "
    "The command to bear burdens requires two participants: the one who carries "
    "and the one who is carried. The Performance+Mask has permanently assumed "
    "the first role and permanently foreclosed the second. In doing so, it has "
    "made the fulfillment of Christ's law structurally impossible in its "
    "closest relationships. Not because it does not love. Because being "
    "carried is incompatible with the public identity the Campaign has built.",

    "Jonathan Edwards, in his sermon on the nature of grace, wrote something "
    "that applies here with unusual force: <i>The grace of God is not a reward, "
    "but a gift, and the gift cannot be received by a closed hand.</i> The "
    "Performance has been running with both hands full for so long that grace "
    "has had nowhere to land. The Campaign fills the hands. The Campaign is "
    "what the hands are for. And a gift \u2014 the grace of being held, "
    "the grace of being carried, the grace of a community that can see you "
    "suffer and not run from what they see \u2014 cannot be received by a "
    "person who has organized their entire identity around the project of "
    "not needing it.",
]

MASK_BODY_P3 = [
    "Bonhoeffer, in <i>Life Together</i>, wrote: <i>He who is alone with his "
    "sin is utterly alone.</i> The Performance+Mask produces a specific and "
    "devastating form of this aloneness, because the Mask prevents the honest "
    "speech by which Christian community breaks the power of hiddenness. "
    "Confessional fellowship requires a self willing to be seen in its "
    "unfinished condition. The Performance has never shown the unfinished "
    "condition to anyone, because the Campaign's entire architecture depends "
    "on the condition appearing finished. And so the wound continues its work "
    "underground \u2014 not loudly, not dramatically, but in the slow widening "
    "of the gap, in the growing distance between the public self and the "
    "actual self, in the exhaustion that the next excellent performance does "
    "not resolve.",

    "Here is the question the Mask has never been asked: <b>What would happen "
    "if you let the sermon go ungiven, the deliverable go unshipped, the "
    "meeting go unled, and simply said to someone you trust: I am not fine?</b> "
    "Not as a project. Not as a growth initiative. Just as a true thing, said "
    "plainly, to a safe witness. My guess is that the Campaign finds this "
    "question more frightening than any professional failure you have ever "
    "faced, because at least professional failure happens in a domain where "
    "you know what to do next. Vulnerability, for the Performance, happens "
    "in a domain where there is no campaign. There is only a person, standing "
    "in front of another person, carrying something they did not finish.",

    "Jesus, in the Garden of Gethsemane the night before his crucifixion, did "
    "something the Performance+Mask finds deeply uncomfortable to read. "
    "He did not give the talk anyway. He did not manage the meeting. He took "
    "the disciples deeper into the garden and said: <i>My soul is very "
    "sorrowful, even to death; remain here, and watch with me.</i> "
    "(Matthew 26:38) He named the weight, plainly, and asked for company. "
    "He, who held all things together, asked to be accompanied. The Performance "
    "reads this and admires it at a safe doctrinal distance. The Mask does not "
    "let it in, because letting it in would mean that the pattern Jesus modeled "
    "in the garden \u2014 the pattern of naming the suffering and asking for "
    "presence \u2014 is available to you too. And available means required. "
    "And required means the next time the suffering is real, the Campaign "
    "is not sufficient.",
]

MASK_PROMPTS = [
    "Name the last time the Mask went on in its full Performance version "
    "\u2014 not the Island's warmth behind glass, but the Campaign's "
    "continued output under conditions that were, privately, not fine. "
    "What were you actually carrying? What did you produce or deliver "
    "or present instead of naming it?",

    "The Campaign has made you unbearable in the literal sense of "
    "Galatians 6:2 \u2014 no one is allowed to carry your weight. "
    "Name one specific weight you are carrying right now. Who in your life "
    "has the proximity and the safety to help carry it? What would you "
    "have to say, in one sentence, to let them in?",
]

TWO_TOG_BODY = [
    "Now we set them side by side, because the Performance Campaign and "
    "the Mask are not two separate problems. They are the same wound, "
    "moving in two directions \u2014 and together they produce the most "
    "professionally rewarded and the most personally costly "
    "pattern in the thirty-six profiles.",

    "<b>The Campaign is what the wound does when it has energy.</b> "
    "The Mask is what the Campaign does when the energy is gone and the "
    "wound is still present but must not show. The Campaign produces "
    "so the shame question will not have to be asked. The Mask performs "
    "competence when the shame question is being asked anyway, by the "
    "suffering itself, from the inside. Together they form a closed loop "
    "in which the real interior never has to appear, because when the "
    "Campaign is running it is behind the output, and when the Campaign "
    "falters it is behind the Mask.",

    "The pattern, in slow motion, looks like this. <b>(1)</b> The Campaign "
    "runs. It produces, builds, achieves, delivers. It earns a reputation "
    "for reliability and excellence. <b>(2)</b> Something arrives that the "
    "Campaign cannot answer with output: a grief, a failure, a relational "
    "wound, a season of interior darkness that persists behind the polished "
    "exterior. <b>(3)</b> The trigger fires: <i>I have been found insufficient, "
    "or something about me as I actually am has been exposed.</i> "
    "<b>(4)</b> The core question surfaces: <i>Am I acceptable?</i> "
    "<b>(5)</b> The Campaign tries to answer it by producing more. "
    "<b>(6)</b> When producing more cannot address an interior wound, the "
    "Mask engages: the suffering goes underground and the Campaign continues "
    "its visible performance, perhaps more intensely than before. "
    "<b>(7)</b> The gap between the seen self and the actual self widens. "
    "The wound continues its work. The question does not go away. "
    "And the loop restarts with the next deliverable.",

    "What interrupts the loop is not a better campaign and not a more "
    "convincing mask. It is a different answer to the question. Jonathan "
    "Edwards was right: the gift cannot be received by a closed hand. "
    "The gift that is being held out \u2014 the verdict spoken at the "
    "cross, the covering already provided, the grace that does not require "
    "a completed deliverable as its precondition \u2014 arrives only when "
    "the Campaign's hands open. That opening is the work of years and not "
    "of a single reading. But it begins here, with naming the loop plainly. "
    "Below, write your sequence in your own words. The Campaign and the "
    "Mask both lose some of their grip when they hear themselves named out loud.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, the shame trigger fires and the old "
    "question surfaces \u2014 <i>am I acceptable as I actually am?</i> "
    "My first move is to ____________________, because the Campaign in me "
    "believes that if I can ____________________, the question will recede. "
    "When the Campaign cannot hold the weight alone, the Mask engages: "
    "I ____________________, and the room sees ____________________ "
    "while the wound continues its work underground. What I am actually "
    "after, underneath all of it, is the verdict ____________________ "
    "\u2014 a verdict Christ has already spoken over me, not earned but "
    "received, in ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a set of small, honest practices, "
    "each calibrated to a specific moment in the loop you just named. "
    "None of them will dissolve in a week what the Campaign has been building "
    "for decades. All of them, practiced faithfully over months, will begin "
    "to loosen the grip of the loop and open the hand that has been closed "
    "around the Campaign's mandate.",

    "I have divided them into two sets: tools for when the Campaign is "
    "overrunning \u2014 when the producing has tipped from genuine vocation "
    "into existential argument \u2014 and tools for when the Mask is on, for "
    "the narrow and often nearly invisible window between the wound and the "
    "continued performance. The Campaign's tools come first, because the Mask "
    "cannot be addressed usefully until the mechanism underneath it is "
    "understood and beginning to loosen.",
]

CAMP_TOOLS = [
    ("The stopped-clock practice",
     "Once a week, spend thirty minutes doing something with no measurable output. "
     "Not productive rest. Not a walk to generate ideas for the next project. "
     "Something genuinely unproductive: sit with a cup of tea, read something for "
     "pleasure with no application in mind, watch a bird. When the anxiety rises "
     "\u2014 and it will, reliably, within ten minutes \u2014 name it: "
     "<i>this is the shame question coming up without the campaign to answer it.</i> "
     "Do not immediately answer the question. Let it be present. The Campaign "
     "cannot be healed without first allowing the question it has been running "
     "from to be heard."),

    ("The two-kinds-of-producing question",
     "Before beginning any significant project, ask yourself one question: "
     "<i>If this produced nothing visible \u2014 no recognition, no result anyone "
     "would see \u2014 would I still want to have done it?</i> This is not a "
     "test of purity. It is a test of source. Work from gratitude can answer "
     "yes and mean it; work from anxiety cannot easily answer yes and mean it. "
     "Colossians 3:23 is the frame: <i>Whatever you do, work heartily, as for "
     "the Lord and not for men.</i> Work done for the Lord does not require the "
     "audience to arrive on schedule."),

    ("The handed-back morning",
     "Each morning, name one thing you are building or carrying or producing "
     "in this season, and say aloud: <i>This is yours today, Lord. I did not "
     "build this to become acceptable. I built this because you gave me these "
     "hands. I hand it back to you now.</i> You will not feel it the first "
     "twenty mornings. By the fiftieth, something in the Campaign begins to "
     "distinguish between building for God and building for the verdict."),

    ("The Isaiah audit",
     "Once a week, read Isaiah 49:15\u201316 aloud: <i>I have engraved you on the "
     "palms of my hands.</i> Not as a technique. As an act of receiving a verdict "
     "that was spoken before the Campaign ran its first race. Then ask: "
     "<i>Is there a person I have been treating this week as background to the "
     "main event?</i> The Campaign's most consistent failure is not professional. "
     "It is relational. This practice names both the failure and its remedy "
     "in the same moment."),

    ("Full presence once a day",
     "Once each day, give the person closest to you ten full minutes of "
     "undivided presence \u2014 no device, no half-attention toward the next "
     "deliverable, no eyes that are planning the evening's work. Not to produce "
     "a better relationship, though it will do that. But because the Campaign's "
     "most characteristic sin is treating the people who love it most as the "
     "audience for a performance rather than as companions in a life. "
     "Ten minutes of genuine presence is the smallest possible rehearsal "
     "of a different relationship to the room."),
]

MASK_TOOLS = [
    ("Name the seam before the performance begins",
     "The Mask has a seam \u2014 a moment, sometimes only three or four seconds "
     "long, between the wound and the continued performance. Your only task in "
     "this season is to locate that moment. Feel the Mask going on and know, "
     "as it goes on, what is happening: <i>the suffering is present, and I am "
     "now performing over it.</i> Noticing is not the same as stopping. "
     "But noticing is the beginning of choice, and choice is what the Mask "
     "has been specifically designed to eliminate."),

    ("The garden prayer",
     "In the moment after the wound fires \u2014 before the Campaign has "
     "fully re-engaged and the Mask is back in place \u2014 say these words "
     "to God, as simply as Jesus said them in the garden: "
     "<i>My soul is very sorrowful. I need you near.</i> Not as a technique. "
     "As a true thing said to the right Audience. The Campaign's Mask depends "
     "on the wound going immediately underground, without acknowledgment even "
     "by the person carrying it. Three honest words, said to God, interrupt "
     "that process at its source."),

    ("The twenty-four-hour rule",
     "You will not always be able to take the Mask off in the moment \u2014 "
     "and in some moments it would not be wise or safe to do so. But within "
     "twenty-four hours of a significant wound or a significant episode of "
     "Mask-wearing, find the one person you trust most and say: "
     "<i>I gave the talk anyway yesterday. I was not actually fine. "
     "What was happening was ___.</i> One sentence. The Mask draws its power "
     "from the time that passes between the wound and its naming. "
     "One honest sentence, spoken to a safe witness within a day, breaks "
     "both the secrecy and the timeline."),

    ("The burden-bearing question",
     "Once a week, ask yourself: <i>What am I carrying right now that "
     "someone else is capable of helping carry, and that I have not allowed "
     "them to carry?</i> Galatians 6:2 is not a command for others to perform "
     "on your behalf. It is a command that requires your willingness to be "
     "carried. Name the weight. Name the person. Name what you would have "
     "to say to let them in. You do not have to say it yet. You have to "
     "name it, clearly, before the Campaign answers the question with "
     "another deliverable."),

    ("Write what the performance covered",
     "At the end of any week in which the Mask was particularly active, "
     "write one paragraph for your own eyes only. Name what happened: "
     "what the wound was, what the Campaign produced in its place, and "
     "what you did not say that needed to be said. Writing the true thing, "
     "even to no audience but yourself and God, is a form of the exposure "
     "the Mask is specifically designed to prevent. The Campaign will say "
     "this is unnecessary. The Campaign is wrong. The writing is not the "
     "final step. It is the first step toward speaking."),
]

PRAYER_BODY = [
    "Father,",

    "You see the Campaign in me, and you are not impressed and you are not "
    "disappointed. You knew about the running before it started. You know "
    "which early moments wrote the lesson that ordinary was insufficient, "
    "and which season it was when I concluded that I would never, if I "
    "could prevent it, be found wanting. Thank you that the running has "
    "produced real things, and that those things were not wasted even when "
    "they were motivated by something other than you.",

    "But Father, I am carrying something I have not been able to put down, "
    "and the Campaign does not know how to put it down, and the Mask keeps "
    "the room from seeing that I am carrying it. I am asking you to do what "
    "Paul said the law of Christ requires \u2014 what Jonathan Edwards said "
    "grace makes possible: help me open the hand that has been closed around "
    "the mandate to never need help. Teach me the difference between stewardship "
    "of the gifts you gave me and the attempt to become acceptable through them. "
    "Teach me that the verdict spoken over me at the cross was not a reward for "
    "the campaign. It was a gift to the person behind it.",

    "Lord Jesus, when I give the talk anyway, when I ship the deliverable anyway, "
    "when I smile in the meeting anyway and the gap between the seen self and the "
    "actual self grows wider for another week \u2014 remind me of the garden. "
    "Remind me that you said <i>my soul is very sorrowful</i> before you said "
    "<i>nevertheless.</i> That the sorrow came first, and was spoken aloud, "
    "and was not managed. Help me follow that order. Help me name the weight "
    "before I keep carrying it. Help me, by your grace, to become the kind of "
    "person who can be carried, which is the only kind of person who can "
    "truly carry others.",

    "Holy Spirit, where the Campaign overruns, give me the courage to stop. "
    "Where the Mask goes on and the suffering goes underground, give me the "
    "grace to find one person and say the true thing before another week has "
    "passed. Where the shame question rises in me \u2014 <i>am I acceptable "
    "as I actually am?</i> \u2014 remind me of the answer engraved on the "
    "palms of his hands, before any campaign produced a single entry. "
    "Keep speaking it until it reaches the part of me that has been "
    "running longest.",

    "In the name of the One who, in the garden, did not perform his way "
    "through the night, but sat in the darkness and said: <i>not my will "
    "but yours be done</i> \u2014 I pray.",

    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Campaign and the Mask "
    "have been running a long time, and one careful reading will not retire them. "
    "What follows is a short list of next steps \u2014 some for the next week, "
    "some for the longer work ahead.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.",
     "Different lines will land the second time. The Campaign will want to treat "
     "this walkthrough as a completed project. Read it again anyway, thirty days "
     "from now, and notice which sections you filed away on the first pass without "
     "quite receiving them. The Mask performs better in your head than on paper; "
     "a second reading is harder to manage."),

    ("Take one tool, not all of them.",
     "Choose the practice from Section Seven that felt most uncomfortable \u2014 "
     "not the most efficient one. Tools that cost the Campaign nothing protect "
     "nothing. The practice that made you want to move on quickly is almost "
     "certainly the one that is most necessary. Try it for two weeks before "
     "adding another."),

    ("Tell one person what you found here.",
     "Not the whole document. One sentence: <i>I learned that my pattern is the "
     "Performance Campaign, and that what I do when I am suffering is keep "
     "performing. I am working on learning to put the performance down.</i> "
     "The Campaign and the Mask both live in the gap between your public self "
     "and your private self. Speaking the true thing to one trusted witness "
     "is the first act of closing the gap. It is also the hardest one."),

    ("Sit with The Screwtape Letters.",
     "C. S. Lewis, <i>The Screwtape Letters</i>. Read it specifically for "
     "Screwtape's account of the slow, dull, domestic corruption of a soul "
     "\u2014 the way great dramatic failures are less effective than the "
     "gradual replacement of the real interior with a performance of the "
     "interior. The Performance+Mask is Screwtape's ideal patient: not "
     "dramatically fallen, not obviously corrupt, simply domesticated by its "
     "own competence into something that looks like virtue but has stopped "
     "receiving grace."),

    ("Read further on grace and the self.",
     "Tim Keller, <i>The Prodigal God</i> \u2014 specifically the chapters on "
     "the elder brother, whose record was impeccable and whose hand was closed "
     "to the very feast the father had prepared. Tim Keller, <i>Counterfeit "
     "Gods</i> \u2014 especially his treatment of achievement as an idol. "
     "For Scripture, spend a week with Psalm 131 \u2014 three verses on the "
     "soul that has learned to be still rather than striving. Read it aloud "
     "each morning. Notice which mornings the Campaign makes the three verses "
     "feel like wasted time."),

    ("If you are stuck, ask for help.",
     "There are seasons when the Campaign and the Mask are too entrenched to "
     "dislodge alone. A wise pastor, a Christian counselor, a friend who knows "
     "you when the campaign is quiet \u2014 these are not signs of failure. "
     "For the Performance specifically, asking for this kind of help without "
     "framing it as a project to be successfully completed is one of the "
     "most countercultural and most healing things on this list. "
     "The asking is itself the practice."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a son or daughter being loved into "
    "freedom by a Father who has engraved your name on the palms of his hands before "
    "you ran a single race and before you gave a single talk. The Campaign did not "
    "earn that love, and it cannot lose it. Go gently. The One who began the good "
    "work in you will be faithful to complete it \u2014 and he will not require "
    "a portfolio as evidence of your progress, or a performance as proof that "
    "the work is going well."
)


def _three_column_table(rows=7):
    """Three-column journal table for the shame/acceptability reflection."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE MOMENT", header_style),
         Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WHAT THE CAMPAIGN PRODUCED", header_style),
         Paragraph("the output offered in place of the wound", sub_style)],
        [Paragraph("WHAT WAS ACTUALLY TRUE", header_style),
         Paragraph("the interior the Mask did not show", sub_style)],
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
    """Generate the Performance Campaign+Mask walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='CAMP', primary_breakdown='MASK',
    primary_trigger='SHM', core_question='ACC'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="PERFORMANCE  \u00b7  MASK",
        title="Take 139 Walkthrough \u2014 Performance Campaign + Mask",
    )

    story = []

    # \u2500\u2500 COVER \u2500\u2500
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor\u2019s<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the self you have performed<br/>"
        "so well you have almost forgotten it is a performance.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph(
        "The Performance Campaign \u00a0\u00b7\u00a0 The Mask",
        S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Shame \u00a0\u00b7\u00a0 Core Question: Am I acceptable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cBear one another\u2019s burdens,<br/>"
        "and so fulfill the law of Christ.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18,
                       textColor=MUTED)))
    story.append(Paragraph(
        "Galatians 6:2",
        ParagraphStyle("cqa", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 1: Opening \u2500\u2500
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read this slowly. The chapter that follows has been "
                   "a long time in the running.")
    for p in OPENING_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 2: Trigger \u2500\u2500
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TRIGGER",
                   "Shame.",
                   "The alarm that fires when something about you as you "
                   "actually are has been found insufficient.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will frame the answer as a professional "
                   "pattern. Your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 3: Core Question \u2500\u2500
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I acceptable?",
                   "The wound the alarm has been standing guard over.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "Two kinds of producing.",
                   "From gratitude, or from anxiety. "
                   "Only one of them can stop.")
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table(rows=4))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 4: Mechanism \u2500\u2500
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Performance Campaign.",
                   "The runner. The builder of visible competence. "
                   "The one who always delivers.")
    for p in CAMP_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in CAMP_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "Giving it shorter hours.",
                   "The campaign is not your enemy. "
                   "It is a younger self that deserves the truth.")
    for p in CAMP_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Campaign.",
                   "Read the Campaign\u2019s own words. "
                   "He has been faithful. Let him speak.")
    letter_style = ParagraphStyle(
        "CampMaskLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    story.append(Paragraph(CAMP_LETTER_INSTRUCTION, S["BodyJ"]))
    story.append(Spacer(1, 8))
    for para in CAMP_LETTER.strip().split("\n\n"):
        story.append(Paragraph(para.replace("\n", " "), letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in CAMP_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=2)
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 5: Breakdown \u2500\u2500
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Mask.",
                   "The place the Campaign breaks \u2014 "
                   "and the face it shows while breaking.")
    for p in MASK_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in MASK_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in MASK_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions to sit with.",
                   "Write, not think. The Mask performs "
                   "better in your head than on paper.")
    for prompt in MASK_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same wound, in two modes.",
                   "The Campaign and the Mask are not two problems. "
                   "They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 8))
    journal_lines(story, n=4)
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
    story.append(Spacer(1, 14))

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Campaign is overrunning.",
                   "Five practices for the time before the wound fires.")
    for name, desc in CAMP_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Mask is going on.",
                   "Five practices for the narrow window between "
                   "the wound and the continued performance.")
    for name, desc in MASK_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 8: Prayer \u2500\u2500
    section_header(story, S, "SECTION EIGHT  \u00b7  A PRAYER",
                   "Pray this slowly.",
                   "Out loud, if you can. Sit in the silence after the Amen.")
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


# \u2500\u2500 STANDALONE TEST \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "CAMP"
        primary_breakdown = "MASK"
        primary_trigger = "SHM"
        core_question = "ACC"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "performance_mask_test.pdf")
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

    print(f"DONE: performance_mask.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
