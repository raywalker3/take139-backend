"""Personal Walkthrough — Island + Ghost.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disconnection/Significance trigger, "Am I enough to be remembered?" core question.
~25 pages, 9 sections.

Key contrast: Island+Ghost is the most invisible profile in all 36.
The Island already lives at distance — and when wounded, that distance becomes
total silence performed as fine-ness. The Ghost performs contentment with solitude
itself ("I just need space; I'm fine alone"). This breakdown looks most like a
personality preference and is hardest to confront because it has the best alibi.
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
    "Before you read any further, I want to do for you what a good counselor does in "
    "the first session — lower the lights and slow the pace — because what you are about "
    "to look at is not a personality profile or a list of traits. It is a way of seeing "
    "how your soul has learned to manage a particular kind of ache, and how that "
    "management has become so practiced, so quiet, and so convincing that most of the "
    "people in your life have no idea it is happening. Including, some days, you.",

    "You are, in a real and specific sense, an Island. Not because you are cold or "
    "incapable of love — you are almost certainly neither — but because something "
    "early in your life taught you that the distance between your interior world and "
    "the world outside was not a gap to be closed but a perimeter to be maintained. "
    "You learned to process alone. You learned that your deepest thoughts were most "
    "reliable when they stayed inside, where they could not be mishandled. You learned "
    "that needing people, in the transparent and exposed way that needing requires, set "
    "you up for a kind of disappointment that was simply not worth the cost.",

    "And when you are wounded — when the ache registers, when the disconnection signal "
    "fires, when someone fails to notice or include or remember — you do not argue. You "
    "do not flood. You do not pursue. You go quiet. And here is the part that makes this "
    "profile the most difficult of all thirty-six to confront: the quiet looks fine. It "
    "looks like health. It looks like maturity. The Island in pain is so accomplished at "
    "performing contentment with solitude that the Ghost — the breakdown underneath — "
    "has the best alibi in the building. <i>I just need a little space. I am okay. I "
    "prefer quiet. This is simply how I am wired.</i> Every one of those sentences may "
    "be partly true. None of them are the whole truth.",

    "We are going to walk through your trigger — the specific moment your nervous system "
    "says <i>something is wrong here.</i> We will listen to the question underneath that "
    "moment, the one that has probably been with you since childhood. We will name the "
    "strategy you have built in response — the Island — and the place that strategy "
    "breaks under pressure — the Ghost. And then, only then, will we put tools in your "
    "hands.",

    "If you were sitting across from me, I would say this plainly. <b>What you are "
    "about to read is true, but it is not the whole truth about you.</b> The whole truth "
    "includes a Father who has not left you to manage your significance alone; a Son "
    "who endured, in Gethsemane, the most complete abandonment in human history so that "
    "the words <i>I am with you always</i> could be spoken without irony; and a Spirit "
    "who is, at this very moment, more present to you than you are to yourself.",

    "So read slowly. Argue with what does not fit. Stay with what does. Pray when "
    "something catches in your throat, because that catch is usually the Lord saying, "
    "<i>look here, with me.</i> The goal is not a personality makeover. It is a slightly "
    "freer life, lived in the company of a God who has never once forgotten your name. "
    "Take your time. The chapter you are about to read about yourself has been a long "
    "time in the writing.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life "
    "have no idea it is occurring. It does not look dramatic from the outside. Sometimes "
    "it looks like nothing at all. You are in the middle of a conversation, or a "
    "gathering, or an ordinary evening at home, and someone says something — or fails "
    "to say something — and something inside you registers it immediately, like a stone "
    "dropped into still water.",

    "Perhaps your spouse started a story about the weekend without including you in the "
    "telling, as though you had not been there — or as though your being there required "
    "no particular acknowledgment. Perhaps a friend mentioned a plan that everyone else "
    "seemed to know about, and you learned of it only by accident, in passing, the way "
    "you learn about things that do not require your involvement. Perhaps you said "
    "something at a dinner table — something that mattered to you — and the conversation "
    "moved on without acknowledgment, as if the words had dissolved in the air. Perhaps "
    "you worked for weeks on something, and the person who received it said thank you "
    "and set it aside and never picked it up again.",

    "On the surface, none of these look like injuries. They are the ordinary traffic "
    "of daily life, the small gaps and oversights that accumulate in every relationship. "
    "But for you, they do not stay small. The moment registers as something more than "
    "inconvenience. It registers as a signal — quiet, specific, and unmistakable — "
    "that says: <i>you were not necessary to this moment. You were not thought of. "
    "You were here, and you did not leave a mark.</i>",

    "This is your trigger. The word we use for it is <b>disconnection</b> — and beneath "
    "disconnection, in your particular case, is <b>significance</b>. The two belong "
    "together. Disconnection wounds you not merely because you feel excluded, but "
    "because exclusion means something to you: it means you did not matter enough to "
    "be included. And mattering — being the kind of person whose absence is noticed, "
    "whose words are carried forward, whose presence changes the shape of a room — "
    "is something your soul has been keeping a very careful, very private tally about "
    "for a very long time.",

    "C. S. Lewis, in <i>The Weight of Glory</i>, wrote with great care about the longing "
    "in every human being to be known and noticed by the universe — to have our names "
    "spoken by the highest authority. He called it a desire for glory, and he refused "
    "to be embarrassed by it, because he recognized it as a desire God himself had "
    "planted there. What he also saw was that when this desire is laid at the feet of "
    "creatures rather than the Creator, the creatures buckle under the weight. They "
    "were never designed to carry it.",

    "You have probably spent a great deal of effort not appearing to need this. The "
    "Island in you has learned that the safest strategy is to need as little as possible "
    "from the outside world, and so you have constructed a life that does not visibly "
    "depend on anyone's memory of you. You are productive. You are capable. You can go "
    "long stretches without showing anyone your interior. But underneath that capable "
    "surface, the tally continues. And when the disconnection signal fires — when "
    "someone fails to notice, fails to remember, fails to carry you forward — the "
    "Island does not dissolve. It simply takes note. Files it away. And keeps moving, "
    "alone, in the direction it was already heading.",

    "Here is what I want you to see before we continue. The sensitivity you carry — "
    "to being overlooked, to being forgotten, to occupying the margin rather than the "
    "center of someone's attention — is not vanity. It is the residue of something "
    "real that happened, usually early, in which the evidence was gathered and a "
    "verdict was quietly reached: <i>the people in my world do not keep track of me "
    "the way I need them to.</i> And having reached that verdict, the Island made a "
    "practical decision: <i>I will not ask them to.</i> Take a breath before we "
    "continue, and answer the two questions below in writing. Not in your head — "
    "your head will process and refile; your hand will not.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the disconnection or "
    "significance signal fired. What happened, in two sentences? You are not looking "
    "for a dramatic event — the ordinary, almost-invisible ones are usually the "
    "most instructive.",

    "What was the size of the actual event, and what was the size of what moved "
    "inside you? If they did not match — if a small oversight produced a large "
    "internal response — you have just located the trigger.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. "
    "The trigger is the alarm; the question is the wound the alarm is guarding. "
    "The Island has been guarding this one for a very long time.",

    "Yours is this: <b>Am I enough to be remembered?</b>",

    "It is not the same as <i>Am I loved?</i>, though it sometimes wears that face. "
    "It is not <i>Am I competent?</i>, though you have built real competence in part "
    "as an answer to it. It is more specific than either. It is the question of a "
    "soul that wants to know whether it leaves a mark — whether its passage through "
    "the lives of others registers, whether it will be thought of in the night, "
    "whether something of it will remain when the moment is over. "
    "<i>Am I the kind of person who is remembered?</i>",

    "Most adults would prefer to believe they outgrew this question long ago. They "
    "have not. They have only relocated it. The childhood version was blunt: "
    "<i>does anyone think about me when I am not in the room?</i> The adult version "
    "has more syllables — <i>Does my work matter? Does this relationship account for "
    "me? Am I significant to the people whose significance I feel?</i> — but it is "
    "the same question, asking in the dark, waiting to see if anyone answers.",

    "For you, this question is especially alive because the Island has made it almost "
    "impossible to ask it out loud. An Island does not petition. An Island does not "
    "say, <i>I need to know that you think about me.</i> That kind of need would "
    "require an exposure that feels intolerable, and so the question stays inside — "
    "forming and reforming, gathering evidence, losing none.",
]

QUESTION_BODY_P2 = [
    "There is a reason that theologians from Augustine through Edwards have insisted "
    "that the deepest human longings point, when followed honestly, not to a human "
    "answer but to a divine one. Augustine's confession — <i>our heart is restless "
    "until it rests in Thee</i> — was not merely poetry. It was a map. And the "
    "longing to be remembered, inscribed, known in a way that nothing can erase, "
    "is at its root a longing shaped for God.",

    "The Scriptures are not embarrassed by this longing. Isaiah 49:15\u201316: "
    "<i>Can a woman forget her nursing child, that she should have no compassion "
    "on the son of her womb? Even these may forget, yet I will not forget you. "
    "Behold, I have engraved you on the palms of my hands.</i> The image is "
    "startling in its physicality. Not a note kept somewhere. Not a record filed. "
    "Engraved — cut in, permanent, requiring deliberate act to remove. The God of "
    "Scripture carries you on his hands as a decision he has made and will not unmake.",

    "Paul, in Romans 8:38\u201339, works his way through everything that might "
    "conceivably separate a person from the love of God — death, life, angels, "
    "principalities, things present, things to come, height, depth, anything in "
    "all creation — and lands on the impossibility of any of them succeeding. Not a "
    "general promise about the universe being benevolent. A specific promise about "
    "the One who knows your name: <i>nothing shall be able to separate us from the "
    "love of God in Christ Jesus our Lord.</i>",

    "But here is where pastoral honesty must be maintained, and it is harder for you "
    "than for most. Your nervous system wants a particular person to demonstrate the "
    "answer — to remember you consistently, to factor you in, to carry you in their "
    "thoughts between interactions. Scripture refuses to promise that. What it "
    "promises is larger and, in the moment the trigger fires, considerably more "
    "difficult to receive: you are known fully and held permanently by the One whose "
    "memory is perfect and whose love does not depend on your being easy to remember.",
]

QUESTION_BODY_P3 = [
    "The gospel anchor for the question you carry is this: you are an <i>Adopted Son</i>, "
    "a <i>Saint</i> — set apart by God as his own possession, fully known, fully named, "
    "inscribed on the palms of his hands. Ephesians 1:4\u20135 says God chose you "
    "<i>before the foundation of the world</i> — not because you earned visibility, but "
    "because he decided, before time began, that you would be his. This is not comfort "
    "in the conventional sense. It is a theological claim, and it asks something of you: "
    "that you allow the answer God has given to actually contest the answer the trigger "
    "supplies.",

    "Here is the honest rub. Most Islands do not find it easy to receive this answer, "
    "not because they doubt it doctrinally but because receiving it requires a kind of "
    "openness — to being given to, to being known, to allowing the interior world to be "
    "entered — that the Island has learned to resist. The Island is exquisitely "
    "defended against needing, and genuine receiving is a form of need. To say "
    "<i>I am fully known and it is enough</i> is to relinquish the tally, and the "
    "Island has been keeping the tally so long that the hand cramps at the thought "
    "of setting it down.",

    "This is the work. Not a single decision — a practice, returned to daily, of "
    "letting the God who has engraved you on his hands answer the question that the "
    "trigger keeps re-opening. David did this in the Psalms, not once but continuously "
    "— returning to the question, returning to the answer, returning to the question "
    "again the next morning. <i>How long, O Lord? Will you forget me forever?</i> "
    "(Psalm 13:1). He does not pretend the question is settled in the morning and "
    "therefore illegitimate in the evening. He brings it back. This is not weak faith. "
    "It is honest faith — the kind the Island needs permission to practice.",

    "Before we close this section, I want you to use the table below. You are not "
    "analyzing yourself; you are simply observing. Use recent events, not ancient ones.",
]

ISLE_BODY_P1 = [
    "You have built something. You did not build it in a morning, and you probably "
    "did not know you were building it. But over years — and usually over a specific "
    "handful of moments in which the world showed you what it did and did not keep — "
    "you constructed a way of being in the world that we are going to call, throughout "
    "this walkthrough, <b>the Island</b>.",

    "The Island's strategy is this: <i>if I need very little from the outside world, "
    "I cannot be disappointed by what the outside world fails to give me.</i> The "
    "Island is not a hermit and is not antisocial. Islands often have deep and genuine "
    "relationships. But the Island has learned that the most essential interior "
    "material — the things that matter most, that carry the most weight, that feel "
    "the most vulnerable — is better handled alone. You process before you share. "
    "You reach conclusions before you open them for discussion. You do not need "
    "the other person's presence to work through what is happening inside you, "
    "and over time you have come to prefer it that way.",

    "There is something in Scripture that commends this kind of self-containment. "
    "Proverbs values the person who is not swept along by every wind of opinion: "
    "<i>Fear of man will prove to be a snare, but whoever trusts in the Lord is "
    "kept safe.</i> (Proverbs 29:25) The ability to hold your own counsel, to not "
    "be buffeted by crowd approval or crowd contempt, to process deeply before "
    "speaking — these are genuine gifts. The Island has them in abundance. They "
    "are not the problem.",

    "But there is a cost the Island rarely acknowledges, and it is this: the same "
    "self-containment that protects you from disappointment also prevents you from "
    "being genuinely known. And the question underneath your trigger — "
    "<i>Am I enough to be remembered?</i> — cannot be answered by a soul that has "
    "made itself invisible to the people whose memory it most wants. The Island's "
    "strategy and the Island's longing are working against each other at the roots.",
]

ISLE_BODY_P2 = [
    "The Island usually formed in one of several specific ways. Perhaps emotional "
    "expression was not welcome in your household growing up — not punished, exactly, "
    "but simply not valued. Feelings were something you handled privately, the way "
    "you handle a headache, until it passed. Perhaps you learned early that needing "
    "people set you up for disappointment, and self-sufficiency began to feel not "
    "merely safer but more honest about the way things actually work. Perhaps you "
    "watched someone close to you need too much from other people, always in crisis, "
    "always dependent, and you decided quietly that you would never become that. "
    "Perhaps you were given more independence early than was healthy, and you grew "
    "comfortable with solitude before you understood what it cost you.",

    "The people who love you have probably felt this at some level without being "
    "able to name it. They know there is more inside than they are allowed to reach. "
    "They have learned, over time, not to push — because pushing makes the Island "
    "close, and they have learned to take what they are given. This is not their "
    "failure. It is the Island's design working exactly as intended. And it means "
    "that the longing at the center of you — <i>I want to be known, I want to "
    "matter, I want someone to carry me in their thoughts</i> — is being "
    "systematically blocked by the very mechanism that is supposed to be answering it.",

    "<b>The Island is not your enemy.</b> He is a younger version of you who "
    "learned, in some specific and real circumstance, that managing alone was safer "
    "than hoping for company. He deserves your respect, not your contempt. But he "
    "is working overtime on a project — keeping you safe from need — that is also "
    "keeping you from the thing you most need. The water surrounding the Island is "
    "not protection. It has become, over time, a kind of prison. And the gospel's "
    "call to the Island is not to become a needier person in the therapeutic sense, "
    "but to receive the kind of knowing that does not require you to perform or "
    "petition — the knowing of a Father who sees you in secret, in the interior, "
    "in the place you have let no one enter.",
]

ISLE_BODY_P3 = [
    "What does it look like to begin loosening the Island's grip? Not demolishing "
    "it — it was built for a reason, and the reason was real. But beginning, slowly, "
    "to lower the drawbridge. Not to everyone. To someone. And before that, to God "
    "— who has already crossed the water, who is already inside, who has known "
    "everything you have processed alone and has never once turned away.",

    "It begins with naming what the Island is protecting. Not what it says it is "
    "protecting — not simply privacy or a preference for quiet — but what it is "
    "<i>actually</i> protecting: the wound of not being enough to be held in "
    "someone's memory. Until you name that, the Island will continue to insist "
    "that solitude is simply a preference, when it is in fact a strategy.",

    "Below is a letter written in the Island's voice — not a letter to him, "
    "but from him, in his own words, addressed to you. He is not villainous; "
    "he is frightened. He has been faithful; he has not had an honest conversation "
    "in a long time. Give him one now.",
]

ISLE_LETTER_INSTRUCTION = (
    "The letter below is written in the Island's voice. Read it slowly before "
    "you answer the questions that follow."
)

ISLE_LETTER = (
    "Dear [Your name],\n\n"
    "I want to tell you what I have been doing, and why\u2014before you decide "
    "I am the problem. I think you should hear what I have been trying to solve.\n\n"
    "I have been keeping you safe. Not safe in the abstract, but from a specific "
    "danger: needing someone and discovering that you were not worth remembering. "
    "I watched that happen. Enough times that I decided the only reasonable "
    "response was to stop needing in ways that could produce that verdict. So I "
    "built the Island. I gave you solitude that looks like strength. I gave you "
    "the ability to process everything alone, so you would never be caught having "
    "needed someone who was not there. I gave you a self that is, by design, not "
    "entirely visible\u2014because what cannot be seen cannot be forgotten.\n\n"
    "What I did not anticipate\u2014what I did not know how to account for, when "
    "I was small enough to still be making these decisions\u2014is that the same "
    "distance that keeps you safe from forgetting also keeps you from being "
    "remembered. You cannot be carried in someone's thoughts if you have never "
    "let them carry you. I thought I was solving the problem. I was only moving it.\n\n"
    "I am not sure what to do with that. I have been at this too long to simply "
    "stop. But I think you should know why I am here, and what it is I am afraid "
    "of. Because it is not nothing. And you have known it was not nothing for a "
    "very long time.\n\n"
    "The Island"
)

ISLE_LETTER_PROMPTS = [
    "What part of the Island's letter surprised you? Not the part you expected "
    "\u2014 the part you were not ready for.",

    "The Island says he built the distance to keep you safe from a specific wound. "
    "Name the wound in your own words. When was the first time the evidence for "
    "that wound was gathered?",

    "What would it cost the Island to let one person \u2014 just one \u2014 closer "
    "to the interior? Name the person. Name the cost honestly.",
]

GHOST_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Island, the breaking has a "
    "particular shape, and it is one of the most difficult shapes in all thirty-six "
    "profiles to name, because it is designed to be invisible. It is called "
    "<b>the Ghost</b>.",

    "Here is what the Ghost does: when the Island is wounded, it does not argue. "
    "It does not flood. It does not build a private brief and deliver a closing "
    "statement weeks later, the way the Attorney does. It goes quiet. It performs "
    "normalcy. It says <i>I'm fine</i> in a tone calibrated to be just believable "
    "enough that the other person might \u2014 if they were paying close attention, "
    "if they cared enough to look \u2014 notice that something is wrong. And then "
    "it waits. It waits to be discovered.",

    "This is the crucial distinction, and I want you to sit with it: the Ghost is "
    "not simply an introvert recharging. The Ghost is not an Island enjoying its "
    "natural preference for quiet. The Ghost is a wounded Island performing "
    "contentment with solitude so convincingly that the performance itself becomes "
    "an accusation: <i>if you loved me well enough, you would know I am not fine. "
    "The fact that you do not know tells me everything I needed to know.</i>",

    "The Architect\u2019s Ghost performs composure \u2014 the planner who pretends "
    "his planning is working while his system quietly collapses. But the Island's "
    "Ghost performs something subtler and considerably harder to confront: it "
    "performs <i>contentment with solitude itself.</i> This is why the Island+Ghost "
    "is the most invisible profile in all thirty-six. The alibi is perfect. "
    "<i>I just need a little space. I prefer quiet. I process alone. This is "
    "simply how I am wired.</i> The Island has been saying those sentences for "
    "years, and they are true often enough that no one \u2014 not even the person "
    "who loves you most \u2014 knows when the preference has curdled into a wound.",
]

GHOST_BODY_P2 = [
    "Dietrich Bonhoeffer, in <i>Life Together</i>, wrote a sentence that has stayed "
    "with pastors for decades: <i>Let him who cannot be alone beware of community. "
    "Let him who is not in community beware of being alone.</i> What Bonhoeffer "
    "saw was that solitude and community are not opposites. They are disciplines "
    "that must be held together, because each, pursued without the other, "
    "becomes something pathological. Solitude without community becomes hiding. "
    "Community without solitude becomes noise.",

    "The Island, in its healthy form, knows how to be alone. More than that: the "
    "Island <i>needs</i> to be alone, in the way Jesus needed to be alone. Mark "
    "1:35 records that Jesus, in the very early morning \u2014 before the crowds, "
    "before the demands, before the day had a shape \u2014 rose and went to a "
    "desolate place to pray. This was not withdrawal from people. It was the "
    "condition of genuine presence to people. The solitude replenished something "
    "that the crowds could not. This is holy. This is what the Island, at its best, "
    "is practicing.",

    "But there is another picture in Scripture. Adam, having sinned, hid himself "
    "among the trees of the garden. And when God came walking, asking the question "
    "that God did not need the information for \u2014 <i>Where are you?</i> (Genesis "
    "3:9) \u2014 Adam did not come out and say: <i>I am wounded and ashamed and "
    "afraid of what you will say.</i> He stayed hidden. He gave a reason for "
    "the hiding that was partly true and covered the real one. The fig leaves "
    "were the performance of normalcy. The trees were the alibi.",

    "The Island's Ghost is the spiritual descendant of Adam in the garden. Not "
    "the Jesus in the desolate place \u2014 praying, present, gathering strength "
    "for re-entry. But Adam among the trees: hidden, performing a kind of "
    "composure, waiting for someone to come looking and simultaneously afraid of "
    "what discovery will cost. The pastoral question that must be asked \u2014 "
    "gently, but honestly \u2014 is this: <b>When you go quiet, which kind of "
    "alone is it? The Mark 1:35 kind, or the Genesis 3:8 kind?</b>",
]

GHOST_BODY_P3 = [
    "What the Ghost is seeking, underneath the performance of fine-ness, is what "
    "the Island has always wanted but could never ask for directly: to be "
    "<i>found.</i> Not to be pursued desperately, not to be needed in an "
    "embarrassing way, but to have someone care enough about your interior life "
    "to notice when it has gone dark \u2014 and to come looking, gently, without "
    "making a scene. The Ghost has concluded, underneath everything, that the "
    "only way to know whether someone truly sees you is to go silent and observe "
    "whether they come. If they come, you were worth finding. If they do not "
    "come, the Island was right all along.",

    "This is the cruelty the Ghost eventually has to face: the test almost "
    "never produces the result it is designed to produce. The other person often "
    "does not know a test is being administered. They see what the Ghost is "
    "performing \u2014 fine-ness, quiet, a preference for space \u2014 and they "
    "respect it, because respecting your partner's solitude is what thoughtful "
    "people do. They are not failing you. They are reading the signals you are "
    "sending. And the Ghost watches them not come looking, and files it as "
    "evidence \u2014 more evidence for the tally, more evidence that you were "
    "not worth the search \u2014 and retreats further.",

    "The gospel speaks directly into the Ghost's wound. You do not have to be "
    "discovered. You have been found. <i>For the Son of Man came to seek and "
    "to save the lost.</i> (Luke 19:10) He did not wait for the lost sheep to "
    "come home and perform its return convincingly. He left the ninety-nine and "
    "went looking. The Ghost's entire strategy \u2014 perform fine-ness, wait "
    "to be found, interpret the search as evidence of worth \u2014 is made "
    "unnecessary by a Shepherd who has already gone out, who already knows where "
    "you are hiding, and who is not fooled by the performance.",
]

GHOST_PROMPTS = [
    "Name the last time the Ghost took over \u2014 the last time you said "
    "\u201cI'm fine\u201d or \u201cI just need space\u201d when the honest "
    "sentence would have been something else entirely. What was the honest sentence?",

    "When the Ghost goes quiet, what is it waiting for? Try to name it specifically: "
    "not \u201cto feel better\u201d but what would actually need to happen for "
    "the Ghost to come out of hiding. What would \u201cbeing found\u201d look like?",
]

TWO_TOG_BODY = [
    "Now we place them next to each other, because the Island and the Ghost are "
    "not two separate problems. They are the same longing, shaped by the same "
    "wound, moving in the same direction \u2014 only one has a schedule and one "
    "runs on silence.",

    "<b>The Island is what your longing does when it has time.</b> The Ghost is "
    "what your longing does when it has been hurt and has nowhere to put the pain. "
    "The Island processes alone so that the alarm will not have to ring. The Ghost "
    "goes silent when the alarm rings anyway \u2014 and performs fine-ness as a "
    "cover story for the wound. Together they form a sealed circuit, and the "
    "circuit has one tragic feature: it cannot be interrupted from the outside, "
    "because the Ghost is performing the very thing that would make an outside "
    "interruption seem unnecessary.",

    "The pattern, in slow motion, looks like this. <b>(1)</b> The Island moves "
    "through the world self-sufficiently, needing less than most, maintaining "
    "the interior perimeter. <b>(2)</b> Something lands that crosses the "
    "perimeter anyway \u2014 a disconnection, a forgetting, a failure of "
    "significance. <b>(3)</b> The trigger fires. The body says, <i>I was not "
    "enough to be remembered here.</i> <b>(4)</b> The core question wakes up: "
    "<i>Am I enough to be remembered?</i> <b>(5)</b> The Island does not react "
    "outwardly. It absorbs the wound and closes further. <b>(6)</b> The Ghost "
    "takes over: it performs fine-ness, says the right things, moves through the "
    "ordinary motions of the relationship, and goes still. <b>(7)</b> It waits "
    "to be found. <b>(8)</b> The other person, reading the signals being sent "
    "\u2014 space, quiet, fine-ness \u2014 respects them. The Ghost interprets "
    "this as abandonment and retreats further. <b>(9)</b> The wound deepens "
    "without ever being spoken, and the loop restarts.",

    "What breaks the loop is not better solitude, and it is not a better "
    "performance of fine-ness. It is a different answer to the question. Until "
    "the Island receives \u2014 really receives, not merely affirms as doctrine "
    "\u2014 that it is already found, already known, already held by the One who "
    "is not fooled by the Ghost's performance, the loop has nothing to push "
    "against. With that answer received and practiced over time, the Island "
    "begins, slowly, to need the Ghost less. The performance of fine-ness "
    "begins to have real competition from the practice of honest disclosure. "
    "Neither happens overnight. But both become possible.",

    "Below is your sequence, written in your own words. Fill in the blanks. "
    "When you are done, read it aloud. The Island and the Ghost both lose a "
    "measure of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as disconnection "
    "\u2014 as not being enough to matter to this person \u2014 and the old "
    "question wakes up: <i>am I enough to be remembered?</i> My first move is "
    "to ____________________, because the Island in me believes that if I can "
    "____________________, I will not need to expose the wound. When that does "
    "not work \u2014 when the wound stays open \u2014 the Ghost takes over, and "
    "I begin to ____________________. What I am actually waiting for is "
    "____________________. What Christ has already spoken over me, in place of "
    "that waiting, is ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small collection of tools \u2014 "
    "each one simple enough to carry, useful enough to reach for. None of them "
    "will resolve the Island's longing in a single application. All of them, "
    "practiced over months, will loosen the grip of the loop you just named.",

    "I have divided them into two sets: tools for when the Island is "
    "overworking its defenses (when the solitude has tipped into hiding), "
    "and tools for when the Ghost has taken over (when the wound is live and "
    "the silence is performing something). The Island's tools come first, "
    "because the Island is the mechanism, and the Ghost cannot be addressed "
    "usefully until the mechanism is understood.",
]

ISLE_TOOLS = [
    ("The one honest sentence",
     "Once a day \u2014 not more, because the Island cannot sustain more without "
     "feeling exposed \u2014 say one honest sentence to someone who is present to "
     "you. Not a report. Not information. One sentence about something interior: "
     "what you are carrying, what you are glad about, what is difficult. The Island "
     "will resist this as unnecessary. Do it anyway. Over a month, the practice "
     "begins to widen the aperture between your interior world and the people who "
     "love you."),

    ("The audit of what you are protecting",
     "When you find yourself going quiet, processing alone, closing the interior "
     "door \u2014 ask one question before the door shuts: <i>am I protecting a "
     "healthy boundary, or am I protecting the wound from being touched?</i> You "
     "do not need to answer it out loud. But the asking disrupts the automatic "
     "nature of the Island's reflex. The Island loses some of its efficiency when "
     "it is required to explain itself."),

    ("The Psalm of disclosure",
     "When the Island's solitude tips into hiding, open to Psalm 62 or Psalm 139 "
     "and pray one section aloud. Psalm 62: <i>Trust in him at all times, O people; "
     "pour out your heart before him.</i> Psalm 139: <i>You have searched me and "
     "known me.</i> The Psalms are the one place in Scripture where the interior "
     "world is required to speak without editing, and they model a disclosure to "
     "God that is too honest to be performance. The Island can pray Psalms without "
     "feeling exposed, which is precisely why this is the right discipline for "
     "this particular wound."),

    ("The handed-back tally",
     "Each evening, name one thing you noticed about your significance tally "
     "today \u2014 one moment where the question <i>am I being remembered?</i> "
     "was active. Do not litigate it; simply notice it. Then say: <i>Lord, I "
     "hand this tally back to you. You keep the record that matters.</i> The "
     "Island has been keeping the tally on God's behalf for years. This is the "
     "practice of returning it."),

]

GHOST_TOOLS = [
    ("Name it before it performs",
     "The Ghost is most easily interrupted in the first sixty seconds after the "
     "wound registers \u2014 before it has had time to dress itself in fine-ness. "
     "In that window, practice one sentence: <i>Something landed hard on me just "
     "now. I am not sure I can say it all yet, but I want you to know something "
     "is there.</i> This is not the full disclosure. It is the refusal to let the "
     "Ghost take the floor unopposed. One sentence, before the performance begins, "
     "changes everything that follows."),

    ("The discovered-already prayer",
     "When the Ghost is in full silence and the waiting has begun, pray these "
     "words: <i>Lord, you have already come looking. You found me before I knew "
     "I was lost. I do not have to perform fine-ness before you. I am not fine. "
     "I am here.</i> The Ghost cannot sustain its performance before the One who "
     "sees through it. This prayer, said honestly, begins to dismantle the alibi."),

    ("Ask instead of wait",
     "The Ghost waits to be found. The discipline that most directly counters "
     "this is asking for what you need before the waiting begins. This does not "
     "require dramatic vulnerability — only one sentence: <i>I need you to "
     "check in with me later.</i> Or: <i>I am having a harder week than I have "
     "let on.</i> The Ghost will call this weakness. It is not. It is the most "
     "courageous thing the Island+Ghost combination can do."),

    ("Tell one person what the Ghost does",
     "Choose one person who loves you \u2014 your spouse, a close friend, a "
     "pastor \u2014 and tell them what the Ghost does: <i>When I am hurt, I go "
     "quiet and perform fine-ness. It is not a preference for space. It is a "
     "test. I want you to know that, so the next time it happens you have "
     "permission to come looking.</i> This single conversation collapses the "
     "alibi, because the Ghost's power depends on the other person not knowing "
     "the test is being administered."),

    ("The Bonhoeffer question",
     "Bonhoeffer wrote: <i>Let him who cannot be alone beware of community. "
     "Let him who is not in community beware of being alone.</i> When the Ghost "
     "has been silent for more than twenty-four hours, ask honestly: which kind "
     "of alone is this? The Mark 1:35 kind \u2014 chosen, purposeful, a return "
     "to God before re-entry \u2014 or the Genesis 3:8 kind: hiding among the "
     "trees, waiting to see if anyone comes? The question itself is the "
     "interruption. The Ghost cannot survive honest self-examination."),
]

PRAYER_BODY = [
    "Father,",

    "You see the Island in me, and you do not despise it. You know what it was "
    "built to protect. You know the specific moments \u2014 the ones I have never "
    "fully named, even to myself \u2014 in which the evidence for the Island's "
    "construction was gathered. Thank you that it kept me alive. Thank you that "
    "you have been present in the interior even when I gave you no invitation.",

    "But Father, the Island is tired, and the tally is heavy, and I have been "
    "keeping a record that was never mine to keep. Teach me to hand it back. "
    "Teach me that being fully known by you \u2014 seen in the desolate place, "
    "in the early morning, before the day has a shape \u2014 is the only answer "
    "that actually quiets the question underneath my trigger. When the "
    "disconnection fires \u2014 when the old wound says, <i>you are not enough "
    "to be remembered</i> \u2014 would you let me hear your answer before I "
    "hear the Ghost's? <i>I have engraved you on the palms of my hands. "
    "I will not forget you.</i> Let that land somewhere deeper than my doctrine.",

    "Lord Jesus, when the Ghost rises \u2014 when the wound goes silent and the "
    "performance begins and I am waiting to be found \u2014 would you remind me "
    "that you have already come looking? That you left the ninety-nine and came "
    "into the far country and came into the garden and called my name and found "
    "me before I knew I needed finding? I do not have to perform fine-ness before "
    "you. You are not fooled by the fig leaves. Come, Lord Jesus. Come into "
    "the place I have made unreachable, and find me there.",

    "Holy Spirit, where I am hiding, give me the courage to speak. Where I am "
    "performing contentment, give me the grace to confess the wound. Where I am "
    "waiting to be found, give me the willingness to ask. And remind me, day "
    "after day, that I am not forgotten \u2014 that my name is engraved, my "
    "standing is settled, and the silence I have been performing can finally, "
    "in you, become rest.",

    "In the name of the One who rose before dawn to be alone with the Father "
    "\u2014 and who, from that solitude, went out to find the lost \u2014 I pray.",

    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not a conclusion. The Island and the Ghost "
    "have been with you a long time, and one reading will not retire them. What "
    "follows is a short list of next steps \u2014 some short, some longer-term "
    "\u2014 for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.",
     "Different lines will land. The Island will resist a second reading \u2014 "
     "it prefers to file things once and move on. Read it again anyway. What you "
     "could not receive this week may be receivable then. The Ghost may have "
     "less to perform the second time through."),

    ("Take one tool, not six.",
     "Choose a single practice from Section 7 and try it for two weeks before "
     "adding another. The Island's tools are not programs; they are postures. "
     "One posture, held for long enough, begins to change the shape of the body. "
     "If you are uncertain which tool to start with, begin with the one that "
     "made you most uncomfortable to read."),

    ("Tell one person what you found.",
     "Not the whole document. One sentence: <i>I learned that my mechanism is "
     "the Island, and when I am wounded, the Ghost takes over \u2014 I perform "
     "fine-ness and wait to be found.</i> Notice what happens when the Island's "
     "interior life is spoken to a trusted witness. This is not a performance. "
     "It is the first lowering of the drawbridge."),

    ("Read the Psalms of lament aloud.",
     "Psalm 13, Psalm 22, Psalm 62, Psalm 139, Psalm 88. Pray one aloud each "
     "morning for a week. The Psalms model what the Island+Ghost most needs to "
     "practice: a soul that brings its interior to God without editing, without "
     "managing, without waiting until the processing is complete. Notice which "
     "lines stop you. Those are the ones to stay with."),

    ("Read further on the longing underneath the wound.",
     "Tim Keller, <i>Counterfeit Gods: The Empty Promises of Money, Sex, and "
     "Power, and the Only Hope That Matters</i> \u2014 the Island tends to make "
     "self-sufficiency a counterfeit god, a way of answering the deepest "
     "questions without exposing them. Keller names this pattern with precision "
     "and pastoral care. Also: C. S. Lewis, <i>The Weight of Glory</i> \u2014 "
     "his treatment of the human longing for significance is among the most "
     "honest and theologically careful in the English language. Read it slowly. "
     "Also: Dietrich Bonhoeffer, <i>Life Together</i> \u2014 especially the "
     "chapters on solitude and community, which are the most useful theological "
     "map for the Island+Ghost combination that has been written."),

    ("If you are stuck, ask for help.",
     "There are seasons when the Island and the Ghost are too entrenched to "
     "dislodge alone. A wise pastor, a Christian counselor, a trusted friend "
     "who has earned the right to your interior \u2014 these are not signs of "
     "failure. They are, for the Island, the most courageous thing on this "
     "list. The Island was built to manage alone. Learning to receive help is "
     "not the abandonment of the Island. It is the beginning of its redemption."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom "
    "by a Father who has engraved your name on his hands and who has not, in all "
    "the years you have been performing fine-ness, been fooled for a single moment. "
    "He has seen you in the garden. He has been asking the question. "
    "Go gently with yourself. The One who began the good work in you "
    "will be the one who finishes it."
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
        [Paragraph("THE EVENT", header_style),
         Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WAS I REMEMBERED HERE?", header_style),
         Paragraph("what your nervous system concluded", sub_style)],
        [Paragraph("WAS MY SOUL IN DANGER?", header_style),
         Paragraph("the deeper question", sub_style)],
    ]
    data = [header_row] + [["", "", ""] for _ in range(rows)]
    tbl = Table(data, colWidths=[col_w]*3,
                rowHeights=[0.55*inch] + [0.5*inch]*rows)
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
    """Generate the Island+Ghost walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='ISLE', primary_breakdown='GHOST'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor's Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR'S WALKTHROUGH",
        cover_right_label="ISLAND  \u00b7  GHOST",
        title="Take 139 Walkthrough \u2014 Island + Ghost",
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
    story.append(Paragraph(
        "The Island &nbsp;\u00b7&nbsp; The Ghost", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disconnection &nbsp;\u00b7&nbsp; Core Question: Am I enough to be remembered?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cBehold, I have engraved you on the palms of my hands;&nbsp;\u2014&nbsp;<br/>"
        "your walls are continually before me.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"],
                       fontSize=11, leading=18, textColor=MUTED)))
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
    for p in TRIGGER_BODY[:4]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  CONTINUED",
                   "Where your sensitivity came from.",
                   "What was lodged in you, and what to do with what you find.")
    for p in TRIGGER_BODY[4:]:
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

    # Letter section
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Island.",
                   "Read the Island's own words. Then answer the three questions below.")
    letter_style = ParagraphStyle(
        "IslandLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    story.append(Paragraph(ISLE_LETTER_INSTRUCTION, letter_style))
    story.append(Spacer(1, 8))

    # Render the letter with paragraph breaks
    letter_paragraphs = ISLE_LETTER.split("\n\n")
    for lp in letter_paragraphs:
        clean = lp.replace("\n", " ").strip()
        if clean:
            story.append(Paragraph(clean, letter_style))

    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in ISLE_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Ghost.",
                   "The performance of fine-ness. The silence that waits to be found.")
    for p in GHOST_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "Holy solitude and wounded silence.",
                   "Mark 1:35 and Genesis 3:8 \u2014 the two kinds of alone.")
    for p in GHOST_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in GHOST_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Step out of the silence.",
                   "Two questions to sit with before you turn the page.")
    for prompt in GHOST_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same longing, in two forms.",
                   "The Island and the Ghost are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  YOUR SEQUENCE",
                   "Write it in your own words.",
                   "Fill the blanks below, then read the sequence aloud.")
    story.append(Spacer(1, 6))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=4)
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

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Island is overworking its defenses.",
                   "Four practices for the time before the wound registers.")
    for name, desc in ISLE_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Ghost has taken over.",
                   "Six practices for the moment the silence begins to perform.")
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
        primary_mechanism = "ISLE"
        primary_breakdown = "GHOST"
        primary_trigger = "DISC"
        core_question = "REM"
        name = "Test User"

    # Print a snippet of the mechanism letter first to verify no artifacts
    print("=== MECHANISM LETTER SNIPPET ===")
    print(ISLE_LETTER[:400])
    print("================================\n")

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "island_ghost_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages by counting %%Page markers in the PDF bytes
    page_count = pdf_bytes.count(b"%%Page:")

    print(f"DONE: island_ghost.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Output:   {out_path}")
    print(f"Pages (approx): {page_count}")
