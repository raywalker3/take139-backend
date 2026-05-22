"""Personal Walkthrough — Adapter + Mask.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Shame trigger, "Am I acceptable?" core question.
~25 pages, 9 sections.

Calibration anchor: Walkthrough #28 of 36. The MOST philosophically complex
profile in the entire set. The Adapter's gift is fluent translation across
rooms — becoming what each context needs, genuinely and without deception.
The Adapter+Mask is the Adapter who, under the pressure of the shame wound,
has locked into a single persona and cannot come out of it. Usually the
safest persona: "competent," "fine," "the steady one," "the helper." Where
the healthy Adapter moves freely among authentic expressions of self, the
Adapter+Mask is the Adapter whose fluency has been weaponized in the service
of a single fixed presentation. It looks like growth ("they are so settled now"),
but it is rigidity in the service of avoidance.

KEY THEOLOGICAL MOVES:
- 2 Corinthians 4:7: the jar is supposed to be cracked. The Adapter+Mask
  has tried to perfect the jar.
- C. S. Lewis, The Great Divorce: "Thy will be done" — the Adapter+Mask
  is choosing, in a small way, the will of the room over the Father's.
- John Owen on mortification: the Mask is a sin to be killed, not a self
  to be protected.
- The Adapter's healing involves recovering fluency INTO honest selfhood.
  The Mask is the Adapter who has stopped translating.
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


# \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 PROSE \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500

OPENING_BODY = [
    "Before you read any further, I want to do what a good counselor does at the beginning of a long, honest conversation. I want to lower the lights and slow the pace, because what you are about to look at is not a personality profile. It is something more precise and more personal: a description of the specific way your soul has learned to manage the question of whether you are acceptable \u2014 and the particular strategy you have built to ensure that question never quite has to be answered out loud.",
    "You are, in a genuine and important sense, an Adapter. The Adapter is one of the most genuinely gifted souls in any room: attuned to people with rare accuracy, fluent across contexts, able to be fully present to a grieving colleague in the morning and a laughing friend in the afternoon, and authentic in both. The Adapter does not perform different selves; the Adapter translates a real self into whatever language the room is speaking. That is a gift, and it has served you and the people around you well.",
    "But there is a particular thing that happens to the Adapter when the shame wound fires. In that moment, the Adapter does not collapse. The Adapter does not retreat. It does something far more subtle: it locks into one version and refuses to come out. It finds the safest persona in its repertoire \u2014 usually the one that reads as most competent, most stable, most <i>fine</i> \u2014 and it wears that version so consistently that everyone around it begins to believe it has simply grown into a steadier self. They are watching rigidity. They think they are watching peace.",
    "<b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who has seen every version you have ever offered any room, and who has been quietly addressing the one underneath all of them \u2014 the one you have not shown anyone in a very long time; a Son who, in his own earthen jar, was cracked all the way through at the cross, so that the light of God could come through in a way that a perfectly sealed surface could never have permitted; and a Spirit who is, at this very moment, working in the interior you have kept so carefully composed.",
    "So read slowly. The Adapter in you will be tempted to extract what is useful and move on. Resist that. Argue with what does not fit. Stay with what does. Pray when something catches in your throat, because that catch is precisely where the lid has been welded on. The goal is a slightly freer life, lived from the version of you that does not need to be the safest one in the room. Take your time.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it is easy to misread \u2014 not because it is subtle, but because you have become so practiced at processing it in under a second that most of the time you do not know you have processed anything at all. Someone offers an offhand critique of something you did. A relationship you have invested in signals, without words, that you have been found slightly wanting. A comparison is made, casually, in a social setting \u2014 not maliciously, perhaps not even consciously \u2014 and something inside you goes very still.",
    "From the outside, this moment is essentially invisible. You may not flinch. You may, in fact, become warmer and more present in the ten seconds after it than you were before. This is the signature of your wiring: you do not register the shame signal by going cold or hard or quiet. You register it by producing something. The production may be warmth, competence, a well-timed remark, a generous response to the very person whose words just landed. And the production is genuine \u2014 which is what makes it so extraordinarily difficult to name.",
    "This is your trigger. The word for it is <b>shame</b> \u2014 and before you argue with that word, I want to be careful about what it does and does not mean here. It does not mean the theatrical kind, the kind accompanied by public humiliation or acute disgrace. It means the quieter, more durable kind: the constant background awareness of a gap between the self you present and the self you actually are, and the specific alarm that fires whenever that gap seems in danger of being noticed. Your nervous system has been watching that gap with unusual vigilance for a very long time. The word <i>shame</i> is simply the name for the alarm.",
    "C. S. Lewis observed in <i>The Weight of Glory</i> that the deepest human longing is not for pleasure or achievement or even love in the common sense, but to be known \u2014 truly, without management, without the careful selection of which parts to show \u2014 and to be found, in that knowing, not insufficient. He called it the longing for glory, and he refused to be embarrassed by it. What he also saw was that when this longing is not brought to the right address \u2014 when it is taken to the rooms of human approval rather than to the Father who alone can answer it \u2014 it does not go away. It goes underground, where it keeps generating strategies.",
    "<b>Your sensitivity to shame is not vanity, and it is not weakness.</b> It is the residue of specific moments \u2014 usually early, often repeated \u2014 in which being seen went badly. A home in which emotional exposure was not handled with care. A season in which you offered something real about yourself and the offering was returned in a form you did not recognize. Whatever its specific origin, the lesson lodged clearly: <i>the self you present is safer than the self you actually are, and you are good at presenting, so let the presenting be the strategy.</i> The Adapter received this lesson and built something remarkable from it: a genuine fluency across rooms. But underneath that fluency, the shame question never got answered \u2014 because the fluency was, in part, a way of never having to ask it.",
    "Before we go further, answer two questions in writing. Not in your head \u2014 the Adapter will process the question into a useful insight before your hand has finished the sentence. Write it instead.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the shame alarm fired \u2014 the moment something registered as <i>I have been found slightly wanting.</i> It may have been a small moment. Write what happened, in two sentences, and what you did in the ten seconds after.",
    "What is the gap you have been most carefully managing in the relationship where you feel most exposed? Not the gap as you would explain it to someone else \u2014 the gap as you experience it alone, without an audience. Name it, as plainly as you can.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older and quieter than the trigger. The trigger is the alarm; the question is the wound the alarm has been standing over for most of your life.",
    "Yours is this: <b>Am I acceptable?</b>",
    "It is not <i>Am I competent?</i> \u2014 though you have built a formidable competence, in part as an answer to it. It is not <i>Am I lovable?</i> \u2014 though love is woven into it. It is the question of a soul that has been offering rooms a carefully selected version of itself and has never quite been sure whether the real one would still be found acceptable if anyone ever saw it. <i>Am I acceptable as I actually am \u2014 not the version I have produced for this room, but the interior one, the one you have never quite been permitted to see?</i>",
    "The shame named here is not primarily the shame of having done something wrong. It is the shame John Owen described in his writing on indwelling sin: the organized, quietly pervasive sense that something is not-right about you at the level of what you are, not merely what you have done \u2014 running the whole operation from below the surface, shaping presentations and protections in ways you have only partially been aware of. For the Adapter, this question has a particular texture, because the gift of fluency makes it very easy to never have to ask it directly. If you can always produce what the room needs, the room never has to conclude you are insufficient. The performance of appropriateness substitutes, day after day, for the answer to the question. But the question has not stopped gathering evidence.",
]

QUESTION_BODY_P2 = [
    "The Psalms \u2014 the prayer book that Jesus himself prayed, and that his people have prayed for three thousand years \u2014 do not pretend that this question is small. Psalm 139 is the most direct scriptural address to the shame-question that exists, and it refuses the reassurance the nervous system wants.",
    "<i>O Lord, you have searched me and known me. You know when I sit down and when I rise up; you discern my thoughts from afar. You search out my path and my lying down and are acquainted with all my ways. Even before a word is on my tongue, behold, O Lord, you know it altogether.</i> (Psalm 139:1\u20134)",
    "Notice what the psalmist is doing. He is not presenting to God. He is not offering a carefully selected version of himself. He is reporting the collapse of the management project \u2014 <i>you have already searched me. You are acquainted with all my ways. Before I speak, you already know it.</i> The gap that the Adapter has been protecting for years is, before this Audience, not a gap at all. There is no distance between the version offered and the version known. And the psalmist goes on, in verse 14: <i>I praise you, for I am fearfully and wonderfully made. Wonderful are your works; my soul knows it very well.</i> The soul that is already fully known is not destroyed by the knowing. It is, in the original Hebrew, declared awe-inspiring.",
    "The gospel anchor for your question is this: you are in Christ \u2014 covered, clean, belonging \u2014 and you are justified. Not improved. Not found acceptable on the condition of better performance. Justified: just as if you had never failed the acceptability test, and just as if you had always passed it perfectly. Paul states the verdict with a directness that should stop you: <i>There is therefore now no condemnation for those who are in Christ Jesus.</i> (Romans 8:1) Not reduced condemnation. None. The question <i>am I acceptable?</i> has been answered, permanently, in the only court that finally counts \u2014 and the answer was not based on the most competent or most composed version of you. It was based on the righteousness of Christ, imputed to you.",
    "What Scripture gives you is stranger and better than what your nervous system wants. The nervous system wants: <i>yes, you are acceptable, and here is the evidence, and the evidence is your own performance.</i> Scripture says: <i>you are acceptable because of what happened to someone else, and the verdict is not subject to revision based on subsequent evidence, and the One who rendered it has already seen everything you were afraid to show.</i>",
]

QUESTION_BODY_P3 = [
    "This is where honest work is required, because the Adapter who carries the shame question has been attempting to answer it with fluency. <i>If I can be the right version for every room, the shame question will never have occasion to fire.</i> But fluency is not the same as acceptability, and the answer built on performance is always the wrong shape for the question. The question is not <i>can I read rooms well?</i> The question is <i>would the room still want me if I stopped reading it?</i> And that question the Adapter's strategy cannot answer, because the strategy depends on the reading never stopping.",
    "The real answer comes from outside the performance entirely. It comes from Paul's language in 2 Corinthians 5:21: <i>For our sake he made him to be sin who knew no sin, so that in him we might become the righteousness of God.</i> The exchange is absolute. The acceptability you have been performing toward is already fully yours, not earned but received, and it is the kind that does not fluctuate based on which version of you showed up today. Christ entered, in his own person, the full experience of public exposure and shame at the cross \u2014 seen, mocked, stripped, found contemptible by those watching \u2014 precisely in order to absorb the verdict you have been managing around for years and to reverse it permanently.",
    "Receiving this \u2014 not as a doctrine to affirm but as a covering to stand inside of \u2014 is the slow work of a lifetime. It does not resolve in a single reading. But it begins with naming, clearly, what you have been doing and what you have been afraid of. Use the table below before you turn the page.",
]

ADPT_BODY_P1 = [
    "You have built something. It did not announce itself as a construction project. It formed the way a river forms \u2014 not by plan but by the repeated movement of water finding the path of least resistance through a landscape that rewarded certain movements and made others costly. And somewhere in your middle years, or perhaps earlier, you looked up and the river was already there, running through every significant relationship you had, shaping the way you entered every room, and you did not know quite how to call it anything other than simply the way you are. Throughout this walkthrough, we are going to call it <b>the Adapter</b>, and the Adapter is worth understanding deeply before we say anything about what it costs you.",
    "The Adapter is not the Ambassador, and the distinction matters because the two mechanisms look very similar from a distance and are in fact deeply different at the root. The Ambassador takes care of people by serving them \u2014 bringing warmth and presence and the instinct to notice who is left out and go find them. The Ambassador is recognizably the same person in every context, serving differently but remaining consistently themselves. The Adapter does something different: the Adapter takes care of people by <i>becoming what they need to encounter.</i> Not falsely. The Adapter is, if anything, one of the most genuinely present people in any room. But the version of you that is present shifts in ways that would be difficult to explain and that the Adapter rarely fully explains even to itself.",
    "Scripture commends both gifts. Proverbs 25:11 says: <i>A word fitly spoken is like apples of gold in a setting of silver.</i> Paul said, with a directness that the Adapter lives before ever reading it: <i>I have become all things to all people, that by all means I might save some.</i> (1 Corinthians 9:22) The relational intelligence that underlies your adaptability is a genuine gift \u2014 a real attunement to human beings that the world runs better for having. You read what people actually need rather than what they present themselves as needing. This is rare. Do not dismiss it.",
    "But there is a cost the Adapter carries that is specific to this mechanism, and it deserves to be named without flattery. The Adapter's most characteristic experience \u2014 the one that surfaces in the quiet, when there is no room to read and no version to produce \u2014 is a particular kind of interior ambiguity about what you actually want, what you actually believe, what you would actually choose if the choosing had no audience. The calibration happens below the level of conscious decision. It is not dishonesty. But over years it produces a specific kind of interior unclarity: the Adapter who can be five different authentic selves in one day sometimes cannot say, at the end of the day, which of those was the one that was most true.",
]

ADPT_BODY_P2 = [
    "The histories that tend to produce the Adapter have a common thread, even in their variety. Perhaps the emotional climate in your household was variable in ways that made reading the room not a preference but a survival practice \u2014 the way to stay connected, to stay safe, was to become whatever the moment most needed you to be. Perhaps there was a family system so tightly woven that a self that differed from the system's preferred self felt threatening to the whole, and adaptation into conformity was the price of belonging. Perhaps you discovered, somewhere between childhood and adolescence, that being exactly what someone needed was the most intoxicating experience available \u2014 the look of genuine recognition on someone's face when you gave them the version of you they did not know they were looking for. Perhaps a parent's love was present but calibrated \u2014 warmer when you were what they needed, cooler when you were something else \u2014 and you adapted into lovability and never quite found your way back to yourself.",
    "Whatever the specific history, the Adapter's deepest characteristic is not the adaptation itself. It is the difficulty of answering, in genuine stillness without any social context to calibrate against, the question the taxonomy asks with unusual directness: <i>Who are you when no one is watching? Not the best version, not the version adapted to what this room needs \u2014 just you, alone, with no one to read.</i> Most people have an answer ready. For the Adapter, the answer is slower in coming, and honest Adapters will say it is not always clear.",
    "<b>The Adapter is not your enemy.</b> He is a younger version of you who learned, in some real and specific circumstance, that the self which could flex was safer and more beloved than the self which held its ground. He deserves your respect and your honest affection. He kept you connected to people you needed to stay connected to. He gave you gifts \u2014 genuine empathy, attunement, a fluency in relational languages that is genuinely rare \u2014 that have been of real use to real people. But he has been working overtime, for years now, on a project that was finished long ago. The room that first required him is long gone. And the question he was built to prevent \u2014 <i>will you still be acceptable if you are simply yourself?</i> \u2014 is one that he has never been, and will never be, equipped to answer.",
]

ADPT_BODY_P3 = [
    "What does it look like to begin loosening the Adapter's hold? Not eliminating the gift \u2014 the attunement is real and the world is better for it. But beginning, slowly, to distinguish between the attunement that flows from genuine love and the adaptation that flows from the unresolved shame question. These two things feel almost identical from the inside; the Adapter has been confusing them for years. The difference is in the root: the attunement that flows from love can be still when the room does not need anything; the adaptation that flows from shame cannot be still, because the stillness is the very exposure it was built to prevent.",
    "The letter below is written in the Adapter's voice. He has something to say that no one has ever thought to ask him to put into words. Give him that chance now.",
]

ADPT_LETTER_INSTRUCTION = (
    "The letter below is written from the Adapter, in his own voice, to you. "
    "He is not a villain. He is a craftsman who has mistaken his instrument for his identity. "
    "Read it slowly. Then answer the three prompts that follow."
)

ADPT_LETTER_PARAGRAPHS = [
    "Dear [your name],",
    "I want to tell you something I have never been given space to say, because in all the years I have been working for you, no one has stopped the operation long enough to ask me to speak. And the honest truth is that I am not sure I could have spoken earlier. I needed you to have read this far first.",
    "I am extraordinarily good at my work. You know this. The people in your life know it, even if they could not name what it is I do. I read them. I read what they need, what they fear, what they are hoping you will be in this particular moment, and I produce it. I produce it genuinely \u2014 not inventing a self, but selecting from among your real qualities the combination that this room can best receive. The performance, such as it is, is made entirely of true materials. The selection is mine.",
    "What I was protecting you from, all this time, is the possibility that the full inventory \u2014 not the selected version, but all of it at once \u2014 might be found wanting. If I keep reading well, that possibility never has to become actual. You are almost always loved. The shame question fires occasionally, when something gets past my management, but I am usually quick enough to contain it.",
    "Here is what I need to tell you now. In keeping you always received, I have kept you always performing. In making sure no room ever had reason to find you insufficient, I have made it impossible for any room to know you fully. The self the rooms have loved is a curated self \u2014 real, but edited. The self underneath the curation has been growing quieter for want of being addressed. I did not mean to do this. I was trying to keep you safe. But the question \u2014 <i>am I acceptable as I actually am?</i> \u2014 cannot stay unanswered forever. And the only way to get an answer is to stop managing the presentation long enough for the real question to reach the real Audience. I cannot take you there. But I wanted you to know why I have been keeping you from it.",
    "The Adapter",
]

ADPT_LETTER_PROMPTS = [
    "What part of the Adapter's letter was hardest to read? Not the most interesting part \u2014 the part that made you want to move past it quickly. Write what you wanted to skip, and why.",
    "The Adapter says he has kept you always performed, always received, and always slightly unknown. Name one relationship in your life where this is most true. What has that person received from you consistently? What have they never been permitted to see?",
    "The Adapter says he was afraid of the answer to the shame question. What do you believe the answer would be, if the management stopped and the real question reached the real Audience? Write the honest fear, and then write Romans 8:1 next to it.",
]

MASK_BODY_P1 = [
    "Every mechanism has a place where it breaks under pressure. For the Adapter, this breaking point has a shape that is, among all the profiles we track, the most philosophically slippery and the most pastorally urgent. It is called <b>the Mask</b>, and for the Adapter, the Mask is not a separate thing from the mechanism. It is what happens when the mechanism's native gift \u2014 fluent self-presentation across contexts \u2014 turns against itself.",
    "Here is what needs to be said carefully, because it is the most important single insight in this walkthrough: <b>the Mask, for the Adapter, does not look like a mask.</b> For every other mechanism, the Mask involves adopting a persona that is recognizably a departure from the norm. The Vault who suddenly becomes warm and accessible is doing something unusual. The Island who starts performing openness is doing something unusual. For the Adapter, the entire repertoire of selfhood has always involved fluid persona selection. The Mask, when it goes on, looks exactly like everything else the Adapter does. No one notices a difference. The person who notices no difference is often the Adapter themselves.",
    "What is different, underneath the surface, is this: <b>the Adapter+Mask is the Adapter who has stopped translating.</b> The healthy Adapter moves with genuine fluency among authentic expressions of self \u2014 different vocabularies, the same voice. The Adapter under the pressure of the shame wound locks into a single version and refuses to come out of it. The fluency freezes. The range collapses to a single note. And the note selected is, almost always, the one with the lowest emotional risk: <i>competent, fine, steady, the helper, the one who is handling things.</i> The version that the shame question cannot easily reach.",
    "John Owen, in his writing on the mortification of indwelling sin, observed something that applies to the Adapter+Mask with particular precision. He said that sin is most dangerous not when it announces itself in obvious failure, but when it organizes the whole life around its own avoidance \u2014 when the management of the wound becomes the shape of the life, so thoroughly that the management no longer looks like management but like character. <i>Be killing sin, or sin will be killing you.</i> The Mask is not merely a coping mechanism. Owen would say it is a sin to be killed \u2014 not a self to be protected.",
]

MASK_BODY_P2 = [
    "The Adapter+Mask, when the shame wound fires, does not become quieter or colder or more distant. It becomes more present, more capable, more useful. At work, the wound fires and the Adapter produces the clearest strategic thinking of the week. In a marriage, the wound fires and the Adapter becomes an extraordinarily attentive spouse \u2014 emotionally available \u2014 while the interior wound goes not just unspoken but unacknowledged. In a friendship, the wound fires and the Adapter becomes the most generous listener in the room, while the thing that happened to the Adapter is processed alone in the car on the way home.",
    "People who know the Adapter+Mask well often say some version of the same thing: <i>they seem so settled now. They used to be more reactive, but they have really grown into themselves.</i> What they are observing is not growth. They are observing the successful installation of a permanent mask. The Adapter, who once moved with natural fluency among many authentic expressions, has achieved what looks like maturity but is the careful elimination of every expression that carries emotional risk. D. Martyn Lloyd-Jones, writing on spiritual depression, noted that many of the most apparently functioning people in the church are the most spiritually isolated, precisely because their evident competence has insulated them from the honest confession that genuine fellowship requires.",
    "Bonhoeffer, in <i>Life Together</i>, wrote: <i>He who is alone with his sin is utterly alone.</i> The Adapter+Mask guarantees a particular and self-reinforcing aloneness. The Mask presents a version of the self that is genuinely fine, genuinely capable, genuinely steady \u2014 and the presentation is good enough that the people around you believe it and stop asking. And in the believing, they stop offering what the Adapter actually needs: to be seen without the management, to be known without the performance, to be loved in the part of themselves that the Mask was built to conceal. The Adapter has all the connection the Mask can produce, and it is, at the level that finally matters, not quite the connection it was looking for.",
    "Paul writes in 2 Corinthians 4:7: <i>But we have this treasure in jars of clay, to show that the surpassing power belongs to God and not to us.</i> The jar of clay was supposed to be cracked. Not destroyed \u2014 cracked. The crack is the design. The light of the glory of God, Paul says, was meant to come through the crack, to show that the power is God's and not the vessel's. The Adapter+Mask has spent enormous energy perfecting the jar. Smoothing the cracks. Presenting a vessel so well-formed and so consistently sealed that the people who see it can only conclude that the vessel itself is the source of everything good that comes from it. But a perfectly sealed jar, however beautiful, cannot let the light through. The Mask is not protecting a self. It is blocking a glory.",
]

MASK_BODY_P3 = [
    "C. S. Lewis, in <i>The Great Divorce</i>, wrote a sentence that cuts to the center of what is happening in the Adapter+Mask: <i>There are only two kinds of people in the end: those who say to God, 'Thy will be done,' and those to whom God says, in the end, 'Thy will be done.'</i> Lewis meant this of large eternal choices. But it maps, in miniature, onto every moment in which the Adapter reaches for the Mask. In each of those moments, a small choice is made: <i>thy will be done</i> \u2014 the will of the room, the will of the safe version \u2014 rather than the Father's. And the Father's will is for the cracked jar. For the version that might be found insufficient and would discover, in the finding, that insufficient is covered.",
    "The Adapter's healing does not involve retiring the gift of attunement. It involves recovering fluency <i>into</i> honest selfhood. The Mask is the Adapter who has stopped translating \u2014 who has locked the vocabulary to the single word <i>fine</i> and refused every other register. The recovery of the gift is the recovery of the full range, including the words that cost something: <i>I am struggling. I do not know. I am not fine. And the One who knows this already has not changed his mind about me.</i>",
    "Peter, after his denial, met the risen Christ at the shore of the Sea of Tiberias. He had already put his outer garment back on \u2014 the resumption of the competent fisher-self after the catastrophic failure of the denier-self. Christ met him in that resumed persona and asked three times: <i>Do you love me?</i> (John 21:15\u201317) The question was not asked for information. It was asked because Peter needed to speak the true thing, without the garment, to the one Audience who could receive it without mishandling it. The risen Christ is asking the same question of the Adapter who has been wearing the competent-fine-steady garment for years. It will not be satisfied by the garment's most articulate performance. It requires, again and again, the unadorned answer from the unadorned self.",
]

MASK_PROMPTS = [
    "Name the last time the Mask went on \u2014 not the dramatic version, but the ordinary one: the moment the shame wound fired and you became, within seconds, more composed, more capable, more useful. What had just happened? What did you produce for the room? What did you actually feel, alone in the car or in the quiet later that night?",
    "The Adapter+Mask looks, from the outside, like growth into steadiness. What is it costing on the inside? Name one thing you have not said to anyone in the past year because the Mask was wearing the version that does not say such things.",
]

TWO_TOG_BODY = [
    "Now we place them next to each other, because the Adapter and the Mask are not two separate problems. They are the same interior life, moving in two different modes \u2014 and together they form the most theoretically unusual loop in the whole of the thirty-six profiles, because the breakdown is built from exactly the same materials as the mechanism.",
    "<b>The Adapter is what the soul does when it has time and confidence.</b> The Mask is what the soul does when the shame wound fires and time runs short. The Adapter moves through the world reading rooms and translating the self into what each room can receive. The Mask is what the Adapter does when shame makes fluency feel unsafe: it locks the translation, selects the lowest-risk version \u2014 competent, fine, steady \u2014 and holds that version with a grip that is mistaken, by everyone including the Adapter, for maturity.",
    "The pattern, in slow motion, looks like this. <b>(1)</b> The Adapter moves through the world in its characteristic mode: fluent, present, attuned, genuine in every room it enters. <b>(2)</b> The shame trigger fires \u2014 a moment of being found slightly wanting, a gap between the presented self and the received self becoming briefly visible, a comparison that lands, a criticism that cuts closer to the interior than the usual management can contain. <b>(3)</b> The core question wakes up: <i>am I acceptable as I actually am?</i> <b>(4)</b> The Adapter tries to produce a version that will resolve the exposure \u2014 warmer, more competent, steadier, more useful. <b>(5)</b> When this does not hold, the Mask locks on fully: the Adapter selects the single safest version and holds it. <b>(6)</b> From the outside, this looks like composure. From the inside, the range has collapsed, the wound is underground, and the question is alive again within the hour.",
    "The loop is powered by a conviction that the Adapter has never fully examined, because it has never needed to: <i>if I can always be the right version, the unacceptable self will never have to be the version that is seen.</i> What breaks the loop is not a better version, and it is not a more seamless performance. It is the reception \u2014 not the doctrinal affirmation, but the actual received experience \u2014 of the verdict already spoken over the self underneath the versions. The Adapter who has genuinely received that verdict does not stop translating across rooms. But the translation no longer needs to protect anything. The attunement is free to be what it was always designed to be: love that moves freely, because there is nothing left to manage.",
    "Below is your sequence. Fill in the blanks. When you are done, read it aloud. Both the Adapter and the Mask lose some of their grip when they hear themselves named in plain speech.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as exposure "
    "\u2014 as the gap between the self I have presented and the self I actually am "
    "becoming visible \u2014 and the old question wakes up: <i>am I acceptable as I "
    "actually am?</i> My first move is to ____________________, because the "
    "Adapter in me believes that if I can ____________________, the shame will "
    "not have to be seen. When that does not hold, the Mask locks on, and I "
    "become ____________________ \u2014 the version that costs the least, the one "
    "everyone has learned to expect. What I am actually after, underneath all "
    "of it, is the verdict ____________________ \u2014 a verdict Christ has already "
    "spoken over me in ____________________, before any version of me existed "
    "to earn it or fail to earn it."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a set of small, portable practices, each honest enough to actually use. None of them will dissolve a pattern that has been twenty years in forming. All of them, practiced with some patience over months, will loosen the loop you just named.",
    "I have divided them into two sets: tools for when the Adapter is overworking its calibration \u2014 when the room-reading has tipped from gift into compulsion \u2014 and tools for when the Mask is locking on, for the narrow and important window between the shame wound and the performance of composure. The Adapter's tools come first, because the Mask cannot be interrupted usefully until the mechanism that produces it is understood from the inside.",
]

ADPT_TOOLS = [
    ("The preference question", "Once a day, before the first significant social interaction, ask yourself one question without reference to anyone else in the room: <i>What do I actually want today?</i> Not what would serve this relationship, not what version of me would be most useful \u2014 what do I want? The Adapter will find this question disorienting. That is the point. A small honest answer is better than a large performed one."),
    ("The unedited opinion", "Once a week, in a low-stakes conversation, offer one opinion before you have checked it against what the other person appears to need. Simply an un-adjusted response: <i>I actually see that differently.</i> Notice whether the relationship survives. It almost certainly will, and the survival is data the Adapter has been needing: the room does not fall apart when you stop reading it."),
    ("The Psalm of the known self", "When the Adapter's calibration tips into anxiety \u2014 when you feel the compulsive need to read, adjust, and produce \u2014 open to Psalm 139 and read the first four verses aloud. <i>O Lord, you have searched me and known me.</i> The Adapter's anxiety is that the unsearched self might be found insufficient. Psalm 139 names the searching as already complete, and the verdict as not destruction but wonder."),
    ("The solitude practice", "Once a week, spend thirty unstructured minutes alone without any input. No phone, no music, no person to read. Sit with one question: <i>Who is here?</i> The Adapter, having nothing to calibrate against, will feel unmoored. That is not emptiness; it is the discomfort of a self rarely present without a room to serve. Over months, the self below the versions begins to speak."),
    ("The named disagreement", "Choose one relationship where you have been consistently adaptive and name one honest disagreement you have never expressed. Not a confrontation \u2014 simply a difference, spoken in a non-crisis moment: <i>I actually see that differently, and I have not said so.</i> One named difference, received without catastrophe, begins to collect evidence against the assumption that unadapted differences are dangerous."),
]

MASK_TOOLS = [
    ("Name the seam", "The Mask has a seam \u2014 a moment between the shame wound and the locked-on performance, before the competent-fine-steady version has fully assembled. For the Adapter it is brief: sometimes only two or three seconds. Your only task in this season is to notice that moment. Feel the Mask engaging and know, as it engages, what is happening: <i>the wound fired. I am now selecting the low-risk version.</i> Noticing is the beginning of a choice, and the Mask runs specifically on the absence of conscious choice."),
    ("The three-word honesty prayer", "In the moment after the shame wound fires \u2014 before the Mask has fully locked on \u2014 say these words silently to God: <i>I am hurting.</i> Not as a petition. Simply as a statement of what is true, addressed to the only Audience who has already seen it. Three words to the right Audience interrupt the machinery of the Mask at its source: the wound going underground without acknowledgment."),
    ("The deferred disclosure", "You will not always be able to remove the Mask in the moment. But within twenty-four hours of the shame wound firing, find the one person you trust most and say: <i>I put the Mask on yesterday when ___. What was actually happening was ___.</i> One honest sentence, spoken to a safe witness within a day, begins to interrupt the permanent concealment."),
    ("The cracked-jar prayer", "When the Mask is firmly on: <i>Lord, the jar is supposed to be cracked. I have been perfecting it. The light cannot get through a sealed surface. Help me to stop sealing. The power is yours, not mine. The covering is yours. Let the crack show.</i> The Adapter who has been performing steadiness will find this prayer uncomfortable. That discomfort is not a sign it is wrong. It is a sign it is working."),
    ("Write the locked version, then speak the wound", "At the end of any week when the Mask was active, write one page for your own eyes only: what the Mask offered the room, and what was actually true behind the performance. Then, within forty-eight hours, tell the person nearest to you the wound in a single sentence without the performance: <i>When that happened, I was hurt \u2014 not the composed version of me, but me.</i> The writing names it; the speaking breaks the secrecy. Both are necessary. The Adapter has learned that direct disclosure is less reliable than managed presentation. The practice of doing it once begins to rewrite that lesson."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Adapter in me, and you see the Mask it has learned to wear when the shame question fires, and you are not fooled by either of them. You know which rooms produced the Adapter and why. You know which wounds produced the Mask. You have been present through every year of the management project, and you have not once looked away from the version of me that has never quite been offered to any room. Thank you that you are not a room I need to read. Thank you that the searching is already done, and that the verdict is not what I feared.",
    "Father, I am tired of performing composure I do not feel. The jar has been sealed for a long time. When I try to unseal it, I manage the unsealing into something presentable. So I am asking you to do what I cannot: let the crack show. Not the curated crack, but the real one \u2014 the one that lets the light through, because the power is yours and not mine, because 2 Corinthians 4:7 is speaking of me specifically, and because a perfectly sealed jar, however beautiful, cannot let the glory through.",
    "Lord Jesus, you absorbed forever the verdict I have been performing to prevent. The question <i>am I acceptable?</i> has been answered at the cross in the only currency it was ever going to take: not my most composed version, but your perfect righteousness, given to the version underneath all the versions, the one you chose before I had ever read a room. Help me receive that. Not as doctrine. As the felt covering of a soul that has been managing its own exposure for a very long time.",
    "Holy Spirit, where the Mask locks on today, give me the grace to notice the seam. Where I am producing composure, give me the courage to say: <i>I am hurting.</i> Where the jar is being sealed, give me the willingness to let it be cracked. Keep speaking the answer to the shame question \u2014 <i>covered, clean, beloved, acceptable in Christ</i> \u2014 until it reaches the part of me the Mask was built to protect.",
    "In the name of the One who was cracked all the way through at the cross so that the light of God could come through in a way no sealed vessel could ever have permitted \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Adapter and the Mask have been with you for a long time, and they will not retire after one careful reading. What follows is a short list of next steps \u2014 some for the next week, some for the longer work that has been waiting.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different lines will land the second time. The Adapter will want to file this document away, having extracted what is useful. Do not let it. Read it again thirty days from now, and notice which paragraphs you could not quite receive on the first pass. The Mask performs better in your head than on paper; a second reading is harder to manage than the first."),
    ("Take one tool, not all of them.", "Choose the single practice from Section Seven that felt most uncomfortable \u2014 not the most manageable, the most uncomfortable. Tools that cost nothing protect nothing. Try the one that made the Adapter want to skip past it, and use it for two weeks before you evaluate."),
    ("Tell one person what you found here.", "Not the whole document. One sentence, spoken in your own voice, to one person you trust: <i>I learned that my pattern is the Adapter, and that when the shame wound fires I lock into the competent-fine-steady version and cannot come out of it. I am working on letting the crack show.</i> The Adapter+Mask draws its power specifically from the performance remaining unwitnessed. Breaking the secrecy once, with one person, changes the architecture in ways a hundred private insights do not."),
    ("Read further on identity and shame.", "Tim Keller, <i>Counterfeit Gods: The Empty Promises of Money, Sex, and Power, and the Only Hope That Matters</i> \u2014 especially his treatment of identity as something received rather than performed. C. S. Lewis, <i>The Weight of Glory</i> \u2014 the essay by that title, read in full, addresses what the Adapter is actually looking for underneath all the room-reading: to be known, called by name, by the highest authority. Lewis names the longing the Adapter has been managing for years, and gives it the only address it was ever designed for."),
    ("Sit with 2 Corinthians 4:7 for a week.", "Read it each morning: <i>But we have this treasure in jars of clay, to show that the surpassing power belongs to God and not to us.</i> Write one sentence each day in response to the question: <i>What crack have I been sealing this week?</i> The Adapter+Mask needs, more than almost any other practice, the daily reminder that the jar is supposed to be cracked \u2014 that the crack is not a failure of the vessel but the design condition of the glory."),
    ("If you are stuck, ask for help.", "There are seasons when the Adapter and the Mask are too entrenched to dislodge alone \u2014 which is, of course, precisely the kind of acknowledgment the Mask was built to prevent. A wise pastor, a Christian counselor, a friend who has earned access to the interior the Mask has been protecting \u2014 these are not signs of failure. For the Adapter specifically, asking for this kind of help without managing the other person's experience of the asking is one of the most countercultural and most healing things on this entire list."),
]

GOING_FURTHER_CLOSING = (
    "You are not a performance to be perfected. You are a jar of clay in which a treasure has been placed "
    "\u2014 chosen, named, covered \u2014 and the light that is meant to come through you comes not in spite of the cracks "
    "but precisely through them. The Adapter in you is a gift. The Mask is a weight you have been carrying "
    "for a long time. Put it down gently. The Father who has seen everything the Mask was built to conceal "
    "has not changed his mind about you. "
    "Go gently with yourself. The One who began the good work in you will be the one to finish it."
)


def _three_column_table(rows=7):
    """Three-column journal table for Section 3's shame/acceptability reflection."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE MOMENT", header_style), Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WHAT I SHOWED", header_style), Paragraph("the version I produced", sub_style)],
        [Paragraph("WHAT WAS ACTUALLY TRUE", header_style), Paragraph("what was underneath the version", sub_style)],
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
    """Generate the Adapter+Mask walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='ADPT', primary_breakdown='MASK',
    primary_trigger='SHM', core_question='ACC'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="ADAPTER  \u00b7  MASK",
        title="Take 139 Walkthrough \u2014 Adapter + Mask",
    )

    story = []

    # \u2500\u2500 COVER \u2500\u2500
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor\u2019s<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the version of yourself<br/>you have welded on, and the one underneath it.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph("The Adapter \u00a0\u00b7\u00a0 The Mask", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Shame \u00a0\u00b7\u00a0 Core Question: Am I acceptable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cBut we have this treasure in jars of clay,<br/>"
        "to show that the surpassing power belongs to God<br/>"
        "and not to us.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "2 Corinthians 4:7",
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
                   "The signal that fires before you know it has fired \u2014 and what you do in the second after.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will produce the composed answer. Your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 3: Core Question \u2500\u2500
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I acceptable?",
                   "The wound the alarm has been standing over.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "The answer the performance cannot give.",
                   "What Christ has already spoken over the self underneath the versions.")
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "What I showed. What was actually true.")
    story.append(Paragraph(
        "Use the table below. In the first column, name a recent moment when the shame alarm fired. "
        "In the second, describe what you showed the room \u2014 the version you produced. "
        "In the third, write what was actually true of you in that moment, "
        "<i>behind the presentation</i>.",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table(rows=4))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 4: Mechanism \u2500\u2500
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Adapter.",
                   "The gift, the cost, and the self that has never quite had a room to itself.")
    for p in ADPT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ADPT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ADPT_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Adapter.",
                   "Read his own words. Then answer the three prompts below.")

    letter_style = ParagraphStyle(
        "AdptMaskLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    story.append(Paragraph(ADPT_LETTER_INSTRUCTION, letter_style))
    story.append(Spacer(1, 10))
    for para in ADPT_LETTER_PARAGRAPHS:
        story.append(Paragraph(para, letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in ADPT_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 5: Breakdown \u2500\u2500
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Mask.",
                   "The place the Adapter breaks \u2014 and the lid that gets welded on.")
    for p in MASK_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The cracked jar, and the welded lid.",
                   "Why the Adapter+Mask looks like maturity, and what it is actually doing.")
    for p in MASK_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in MASK_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions to sit with.",
                   "Write, not think. The Mask performs better in your head than on paper.")
    for prompt in MASK_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same soul, in two modes.",
                   "The Adapter and the Mask are not two problems. They are one loop.")
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
                   "What to do when you feel the loop start.",
                   "Small enough to carry; honest enough to use.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 14))

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Adapter is overworking its calibration.",
                   "Five practices for the time before the alarm fires.")
    for name, desc in ADPT_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Mask is locking on.",
                   "Six practices for the narrow window between the wound and the performance of composure.")
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
        primary_mechanism = "ADPT"
        primary_breakdown = "MASK"
        primary_trigger = "SHM"
        core_question = "ACC"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "adapter_mask_test.pdf")
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
                snippet = txt.strip()[:120]
                break
    except Exception:
        page_count = "unknown"
        snippet = ""

    print(f"DONE: adapter_mask.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
