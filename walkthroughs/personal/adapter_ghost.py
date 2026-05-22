"""Personal Walkthrough — Adapter + Ghost.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disconnection trigger, "Am I lovable?" core question.
Mechanism: Adapter (ADPT) — the chameleon, reads the room and becomes whatever
  it needs; borrowed self from feedback rather than held independently.
Breakdown: Ghost (GHOST) — performs normalcy, goes silent, waits to be discovered.
~25 pages, 9 sections.

Calibration note: Reuses Adapter mechanism material from adapter_attorney.py
(Batch 4 anchor). PRESERVES the Adapter/Ambassador distinction and
river-formation image.

KEY CONTRAST: The Adapter+Ghost is uniquely paradoxical. Every other Ghost
breakdown either performs composure (Architect), performs contentment with
solitude (Island), betrays the caretaker's gift (Ambassador), or simply closes
without performance (Vault). The Adapter+Ghost does none of these — because
the Adapter has ALREADY BEEN performing every version all along. When wounded,
the Adapter does not produce a new persona; it withdraws all of them at once.
The room reads no signal because there is no version present to read.

Pastoral move in Section Five: The Ghost is the only moment the Adapter has
ever come close to being themselves alone — no audience, no calibration, no
version. It looks like withdrawal; it is sometimes the door to honesty. But
the Adapter does not know how to stay there without a version coming back.
1 Kings 19:11-13 (still small voice) + C. S. Lewis, Mere Christianity (wild
animals / listening to that other voice).
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
    "Before you read any further, I want to do what a careful pastor does at the"
    " beginning of a hard conversation. I want to lower the lights and slow the pace,"
    " because what you are about to look at is not a catalogue of your strengths,"
    " though you have real ones, and it is not a verdict on the way you have moved"
    " through relationships, though there is something in it that must be carefully"
    " named. It is a patient conversation about the way your soul has learned to"
    " keep itself safe \u2014 and for you, that strategy has been so fluid, so natural,"
    " and so genuinely useful that you may not have recognized it as a strategy at all.",

    "You are, in a real sense, an Adapter. Not because you are false or"
    " insincere \u2014 the Adapter is, if anything, one of the most genuinely present"
    " people in any room. But because something early in your experience taught you"
    " that the surest path to connection was not to bring a fixed self and wait to see"
    " if it was wanted, but to read the room carefully and become what the room could"
    " receive. You learned to move between people the way a musician moves between"
    " keys \u2014 the same instrument, but a different sound depending on what the"
    " piece required.",

    "We are going to walk through your trigger \u2014 the specific moment your nervous"
    " system says <i>something is wrong here.</i> We will listen to the question"
    " underneath that moment, one that has probably been with you since you were very"
    " small. We will name the strategy you have built in response, and the place that"
    " strategy collapses under pressure \u2014 not loudly, not dramatically, but in a"
    " way that is, in its own quiet way, one of the most disorienting things that"
    " happens to people like you. And then, only then, will we put tools in your hands.",

    "If you were sitting across from me, I would say this plainly."
    " <b>What you are about to read is true, but it is not the whole truth"
    " about you.</b> The whole truth includes a Father who did not first know the"
    " versions of you that you have offered to the world and then decide whether to"
    " love you; a Son who, in the thirty-three years he walked this earth, was himself"
    " in every room he entered, and who calls you by a name he chose before you ever"
    " walked into any room at all; and a Spirit who is, at this very moment, the only"
    " resident of the interior you have rarely let anyone else fully enter.",

    "So read slowly. Argue with what does not fit. Stay with what does. Pray when"
    " something catches in your throat, because that catch is usually the Lord saying,"
    " <i>look here, with me.</i> The goal is a slightly freer life, lived from a self"
    " that does not need to be negotiated fresh in every room you enter. Take your"
    " time. The chapter you are about to read about yourself has been a long time"
    " in the writing.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it is difficult to describe"
    " to people who do not share your wiring, because from the outside it looks like"
    " almost nothing. Someone you love has been quiet \u2014 not cold, not angry, just"
    " somewhere else in themselves, a few degrees cooler than usual. A friend has not"
    " replied in a few days. Something real you gave \u2014 an evening, a conversation,"
    " a careful piece of yourself \u2014 was received the way furniture is received,"
    " without particular notice. A gathering ran warmer for others than it did for you,"
    " and you stood just outside the radius of it, and no one came to find you.",

    "On the surface, none of these qualify as catastrophes. You may not show anything."
    " You may be the one who, in the next breath, finds a way to serve the moment,"
    " brightens the room, or becomes whatever the person in front of you most needs."
    " But inside, something has registered \u2014 a quiet, precise, cold signal:"
    " <i>the warmth has withdrawn.</i> And the Adapter, who has spent a lifetime"
    " reading the room and adjusting to it, cannot locate the right version to produce"
    " in response to its own pain.",

    "This is your trigger. The word for it is <b>disconnection</b> \u2014 and for the"
    " Adapter it carries a particular weight that deserves unpacking. The Adapter's"
    " relational world is organized around reading the cues that other people emit:"
    " the shift of tone, the slight withdrawal, the almost imperceptible cooling. You"
    " have been reading these signals since before you had words for them. And when"
    " disconnection arrives \u2014 when someone you have been carefully attuned to"
    " becomes, briefly or lastingly, unreadable \u2014 something older and more"
    " frightening than loneliness wakes up.",

    "C. S. Lewis, in <i>The Four Loves</i>, observed that love of every kind makes"
    " us vulnerable in exact proportion to the size of the love \u2014 that the only"
    " way to avoid being hurt by love is to avoid loving, and the only way to avoid"
    " loving is to arrive at a place of such thorough insulation that the soul no"
    " longer reaches out at all. For the Adapter, the vulnerability is both specific"
    " and acute. The disconnection trigger does not read as a neutral weather event"
    " that will pass. It reads as information: <i>something about who I have been in"
    " this relationship has been found wanting.</i>",

    "<b>Your sensitivity to disconnection is not random.</b> It is the residue of"
    " moments \u2014 usually early, usually repeated, sometimes only a handful but"
    " entirely unforgettable \u2014 in which love turned inconsistent, and you learned"
    " something that lodged in the bones before it could be examined: <i>connection"
    " is not a steady ground beneath my feet; it is a temperature I must maintain by"
    " staying attuned.</i> Perhaps warmth came when you were exactly what someone"
    " needed and receded when you were simply yourself. Perhaps you learned that having"
    " a self that differed from what the room needed was costly. Whatever the specific"
    " history, the lesson arrived: <i>the safest thing is to become what the room can"
    " love.</i> And so the Adapter was born.",

    "Before we go further, I want you to write two things down. Not in your head"
    " \u2014 the Adapter's head will reframe the questions to fit whatever the moment"
    " seems to need. Your hand will be more honest. Take whatever time you need.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week or two, that the disconnection signal"
    " fired. What happened, in two sentences? You are looking for the moment your"
    " internal temperature dropped \u2014 not necessarily a dramatic event, but the"
    " moment something inside you said <i>the warmth is gone, and I do not know"
    " which version of me to produce in response.</i>",

    "How large was the actual event? How large was the response inside you?"
    " If the response was larger than the event \u2014 if something in you went very"
    " still in a way that surprised you \u2014 you have just located your trigger."
    " Write both sizes down, even approximately.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is almost always older than"
    " the trigger by a decade, sometimes two. The trigger is the alarm; the question"
    " is the wound the alarm is guarding. The Adapter has been guarding this one for"
    " a very long time, and has been guarding it so skillfully \u2014 covering it with"
    " each new version, meeting each new room with each new attuned self \u2014 that"
    " you may not have let yourself put it into plain words.",

    "Yours is this: <b>Am I lovable?</b>",

    "I want to be careful here, because that question is easy to underestimate. It is"
    " not the same as <i>Am I loved?</i> \u2014 you have been loved, genuinely, and"
    " you know it, and yet the question has not gone away. It is more frightening than"
    " that, and more specific. The question is: <i>Am I the kind of person who is"
    " loved for what I am, rather than for what I become in the presence of another?"
    " If I stopped adapting \u2014 if there were no room to read and no version to"
    " become \u2014 would there be someone here? And would that someone be loved?</i>",

    "For most adults, this question has been moved underground. For the Adapter, it"
    " speaks in the silences and especially in the moments of disconnection: in the"
    " spouse's quiet evening, in the friend's delayed reply, in the gathering where"
    " the warmth flowed more easily to others. The nervous system's verdict in those"
    " moments is not neutral: <i>see? Even after all the versions you have"
    " offered \u2014 even after a lifetime of becoming what each person most needed"
    " to receive \u2014 the connection can simply close. This is what you suspected"
    " all along.</i>",

    "There is a particular urgency in this question for you, because the Adapter has"
    " organized so much of life around answering it through a strategy of perpetual"
    " attunement. Every version was offered in the hope that it would produce a"
    " connection stable enough, warm enough, convinced enough, to eventually answer"
    " the question once and for all. And the hope underneath all that calibrating"
    " \u2014 the hope you may never have quite put into words, even to yourself"
    " \u2014 was this: <i>if I can give each person exactly the self they most need"
    " to see, the love that comes back will eventually be so certain that the"
    " question will stop asking.</i>",
]

QUESTION_BODY_P2 = [
    "There is a reason Augustine, at the very opening of his <i>Confessions</i>,"
    " located the restlessness of the human soul not in unfulfilled ambition or"
    " unresolved philosophy but in the absence of God: <i>our heart is restless,"
    " until it rests in Thee.</i> What Augustine was describing is the longing of"
    " every creature for a love that is permanent, unconditional, and not contingent"
    " on the creature's next successful performance. The Adapter's restlessness is"
    " precisely this longing, wearing relational clothes. The question <i>Am I"
    " lovable?</i> is the Adapter's version of Augustine's restless heart \u2014"
    " and it will not be answered by any number of successful versions.",

    "The Psalms take this longing with the seriousness it deserves. Psalm 103 opens"
    " with an interior memo to a wavering soul: <i>Bless the Lord, O my soul, and"
    " forget not all his benefits \u2014 who forgives all your iniquity, who heals"
    " all your diseases, who redeems your life from the pit, who crowns you with"
    " steadfast love and mercy.</i> (Psalm 103:1\u20134) That word at the center"
    " \u2014 <i>steadfast</i> \u2014 is the Hebrew word <i>hesed</i>, the covenant"
    " love of God, the love that does not depend on the beloved's performance or"
    " attunement. This is the word the Adapter's soul has been looking for in every"
    " room it has ever entered.",

    "The gospel's answer to <i>Am I lovable?</i> is precise and theologically"
    " careful. It is not <i>yes, because of who you are</i> \u2014 which would be"
    " sentimentality, and God does not traffic in sentimentality. It is not <i>yes,"
    " if you continue to attune faithfully</i> \u2014 which would be the exact"
    " treadmill you are already on. The answer is this: <i>you are loved not because"
    " you are lovable but because you are in Christ, and in him, the love the Father"
    " has for the Son flows over to you, without condition and without end.</i> Paul"
    " names it in Romans 8:15: <i>you did not receive the spirit of slavery to fall"
    " back into fear, but you have received the Spirit of adoption as sons, by whom"
    " we cry, \u2018Abba! Father!\u2019</i>",

    "But I want to say something honestly here. The Adapter hears this good news and"
    " nods. You may feel it, briefly and genuinely, and then almost immediately begin"
    " checking whether the person across from you is also feeling it, or needs a"
    " different version of it, or requires your help receiving it. The reason this"
    " answer does not fully land for you is not that the theology is unclear. It is"
    " that receiving requires stopping. It requires sitting in a room with no one"
    " else in it, with no cue to read and no version to produce, long enough for the"
    " love to settle rather than managing the moment before it does. The hardest thing"
    " this gospel answer asks of the Adapter is not understanding. It is stillness.",
]

QUESTION_BODY_P3 = [
    "The honest work for you looks like this. The Adapter has been trying to earn,"
    " through consistent and costly attunement, a love that can only be received. This"
    " is a loop that cannot be closed by any number of successful versions, because the"
    " question underneath it is not <i>have I adapted well enough?</i> but <i>am I"
    " loved?</i> \u2014 and more calibration is not the answer to the second question.",

    "Galatians 4:7 says it plainly: <i>so you are no longer a slave, but a son, and"
    " if a son, then an heir through God.</i> An heir does not earn the inheritance."
    " An heir receives it \u2014 simply by being in the family. The Adapter has been"
    " functioning as the most dedicated servant in the household, working for a"
    " standing that was given freely. The cross is where the giving happened \u2014"
    " not gradually, not conditionally, but once and completely, at a cost you did not"
    " pay and could not have paid. What you are is not an employee whose tenure must"
    " be maintained by successful attuning. You are an heir. And heirs do not earn"
    " what they already have.",

    "Before we close this section, use the table below for honest observation"
    " \u2014 not analysis at a distance, but the kind of specific memory that tells"
    " the truth before the mind has time to soften it. Where did the disconnection"
    " trigger fire this week, and where was your soul's standing before God"
    " actually in danger?",
]

ADPT_BODY_P1 = [
    "You have built something. It did not announce itself as a strategy when it was"
    " forming. It formed the way a river forms \u2014 not by decision, but by the path"
    " of least resistance through a landscape that rewarded certain movements and"
    " punished others. And one day you looked up and the river was already there,"
    " running through every relationship you had, shaping the way you moved through"
    " every room. Throughout this walkthrough we are going to call it <b>the"
    " Adapter</b>, and the Adapter deserves to be introduced as a character before"
    " we say anything about what it costs you.",

    "The Adapter is not the Ambassador. This distinction matters, and the two"
    " mechanisms look so similar from the outside that they are worth pausing over"
    " carefully. The Ambassador takes care of people by serving them \u2014 bringing"
    " warmth, managing emotional temperature, being the one who notices when someone"
    " is left out and goes to find them. The Ambassador is the same person across"
    " contexts, serving differently but remaining recognizably themselves. The Adapter"
    " does something different: the Adapter takes care of people by <i>becoming what"
    " they need to see.</i> Not performing a false self \u2014 the Adapter is genuinely"
    " present in every version. But the version itself shifts. You can be utterly"
    " authentic in five different ways with five different people in one day and feel"
    " no contradiction, because for the Adapter, authenticity has never been a fixed"
    " self presenting itself consistently; it has been the full entering-in to"
    " whatever the relationship most needs.",

    "The Ambassador knows they are the same person serving differently across contexts."
    " The Adapter may genuinely not know that. And this \u2014 the gift and the cost"
    " in a single sentence \u2014 is precisely what this section is about. There is"
    " a great deal in Scripture that commends relational intelligence of this kind."
    " Proverbs 25:11 says: <i>A word fitly spoken is like apples of gold in a setting"
    " of silver.</i> Paul himself said: <i>I have become all things to all people,"
    " that by all means I might save some.</i> (1 Corinthians 9:22) The Adapter lives"
    " this verse before they have ever read it. It is a genuine fluency in relational"
    " languages, and the world runs better when people like you are in it.",
]

ADPT_BODY_P2 = [
    "But there is a cost, and the cost is specific to this mechanism, and it deserves"
    " to be named honestly. The Adapter's most characteristic experience is this:"
    " you can be fully present in a conversation \u2014 genuinely moved, genuinely"
    " engaged, genuinely yourself \u2014 and walk away an hour later and not be"
    " entirely sure which of your preferences, which of your opinions, which of your"
    " actual interior responses were yours and which were calibrated to the person you"
    " were with. The calibration happens below the level of conscious decision. It is"
    " not dishonesty. But it produces, over years, a specific kind of interior"
    " ambiguity about what you actually want, what you actually believe, what you"
    " would actually choose if no one were in the room to calibrate to.",

    "The taxonomy we work from suggests several histories that tend to produce the"
    " Adapter, and you will likely recognize yourself in at least one. Perhaps you"
    " grew up in a household where the emotional climate changed frequently and reading"
    " the room was not a preference but a survival skill \u2014 the way to stay safe"
    " was to become what the safest version of the moment needed. Perhaps there was"
    " enmeshment, a family system where having a self that differed from the family's"
    " preferred self felt dangerous, and you learned to make your self available"
    " rather than insisting on it. Perhaps you discovered very early that being exactly"
    " what someone needed was the most intoxicating experience available \u2014 the"
    " look of recognition on a person's face when you gave them the version of you"
    " they did not know they were looking for. Perhaps a parent's love was conditional"
    " on conformity and you adapted into lovability and never quite found your way"
    " back to yourself.",

    "Whatever the specific history, the Adapter's deepest characteristic is not the"
    " adaptation itself. It is the difficulty of answering, in the quiet, the question"
    " the taxonomy asks with unusual directness: <i>Who are you when no one is"
    " watching? Not the best version, not the version adapted to what this room needs"
    " \u2014 just you, alone, with no one to read.</i> For most people, this question"
    " has an answer ready. For the Adapter, the answer is slower in coming, and more"
    " honest people will say it is not always clear.",

    "<b>The Adapter is not your enemy.</b> He is a younger version of you who learned,"
    " in some real and specific circumstance, that the self which could flex was safer"
    " than the self which held its ground. He deserves your respect, not your contempt."
    " He kept you connected. He gave you gifts \u2014 empathy, attunement, a rare"
    " fluency in the emotional languages of the people around you \u2014 that are"
    " genuinely valuable. But he has been working overtime on a project that was"
    " finished years ago. The room that first required him is long gone. And the"
    " question he was built to prevent \u2014 <i>will you be loved if you are simply"
    " yourself?</i> \u2014 is one that he is not, and has never been, equipped"
    " to answer.",
]

ADPT_BODY_P3 = [
    "What does it look like to begin loosening the Adapter's grip? Not eliminating"
    " the gift \u2014 the attunement is real and should not be retired. But beginning,"
    " slowly, to distinguish between the attunement that flows from love and the"
    " adaptation that flows from fear. These two things feel almost identical from the"
    " inside. The difference is in the root: the attunement that flows from love can"
    " stop if the stopping is right; the adaptation that flows from fear cannot stop"
    " without triggering the alarm.",

    "It begins with sitting still long enough to notice what you actually want. Not"
    " what the room wants from you, not what would serve the other person best, not"
    " which version of your preference would land most smoothly. What do you want?"
    " The Adapter often discovers, when sitting with this question for the first time"
    " without the usual social context to calibrate against, that the answer is"
    " genuinely unclear. This is not a failure of self-knowledge. It is the honest"
    " recognition of a mechanism that has been so faithfully at work that the self"
    " underneath it has not had much occasion to speak.",

    "The letter below is written in the Adapter's voice. He is not villainous. He"
    " is genuinely confused, and genuinely faithful, and genuinely tired. He has"
    " something to say that he has never been asked to put into words. Give him"
    " that chance now.",
]

ADPT_LETTER_INSTRUCTION = [
    "The letter below is written from the Adapter, in his own voice, to you. He is"
    " not a villain; he is a craftsman who has mistaken his tool for his identity."
    " Read it slowly. Then answer the three prompts that follow.",

    "Dear [your name],",

    "I want to tell you something I have never been asked to say, because I have"
    " never been still long enough to say it. And the truth is, the stillness is the"
    " problem. I do not do well with stillness. In stillness, there is no room to"
    " read. There is no feedback to borrow. There is no version of you to present."
    " There is only \u2014 I am not sure what. And that not-knowing is the thing I"
    " have been moving away from, more or less continuously, for as long as"
    " I can remember.",

    "I learned early that I could be loved. Not by being fixed, not by holding my"
    " ground, not by saying <i>this is who I am and this is what I want.</i> That"
    " kind of love felt too uncertain \u2014 you put yourself out and waited and the"
    " waiting was unbearable. But I found something better, or what seemed like"
    " something better: I could read what someone needed, and become it, and the love"
    " came immediately. It did not require waiting. It required attention, and I had"
    " an inexhaustible supply of attention.",

    "I want you to know what I actually did for you. I kept you in every room you"
    " were ever in. I kept the relationships going. I kept people close. I made you"
    " easy to love, because I made sure that whoever you were with, you were giving"
    " them something they needed. That is not nothing. You have been loved. A lot."
    " And I have worked hard for that.",

    "What I did not know how to do \u2014 what I am only now beginning to see I could"
    " not do \u2014 is give you a self that was yours when no one was there. I kept"
    " you present in every room. I did not know how to keep you present in the room"
    " with no one in it. I am not sure I knew there was supposed to be a you"
    " there too.",

    "I am telling you this because I think you have started to feel the cost. The"
    " exhaustion. The disorientation when someone asks what you want and you genuinely"
    " do not know. The moment in a conflict when you realize you have gone very quiet"
    " \u2014 not because you are angry, not because you have given up, but because"
    " you have reached for a version to produce and found that there is not one. I"
    " notice those moments. I do not know how to fix them. But I want you to know:"
    " I did not mean to leave you with nothing to offer when the room went silent."
    " I was trying to give you everything.",

    "The Adapter",
]

ADPT_LETTER_PROMPTS = [
    "What part of the Adapter's letter surprised you? Not the part you expected"
    " \u2014 the part you were not quite ready for.",

    "The Adapter says he kept you present in every room but could not keep you present"
    " in the room with no one in it. When was the last time you sat quietly, without"
    " calibrating to anyone, and felt at home in yourself? Describe that moment,"
    " or describe the absence of it.",

    "The Adapter says he did not mean to leave you with nothing. What would it mean,"
    " in practice, to begin recovering something that is yours alone \u2014 an opinion,"
    " a preference, a grief, a desire \u2014 that you have never offered to any room?",
]

GHOST_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Adapter, the breaking has a shape"
    " that is, among all the profiles we track, the most paradoxical \u2014 and the"
    " one, once you see it, that is hardest to look away from. The breakdown is called"
    " <b>the Ghost</b>, and the Adapter's version of it is unlike any of the others"
    " that carry this name.",

    "Here is the setup. The Adapter has been doing what the Adapter does \u2014"
    " reading every room, adjusting to every person, becoming whatever the relationship"
    " most needed. Then something lands. A wound large enough that the usual adjustment"
    " cannot contain it. The disconnection trigger fires not quietly but hard \u2014"
    " a spouse who has been unreachable for days, a friend whose silence has begun to"
    " read as verdict, a moment in which the attunement that has kept every"
    " relationship warm simply cannot locate a way to restore the warmth. And the"
    " Adapter reaches \u2014 as the Adapter always reaches \u2014 for a version"
    " to produce.",

    "And finds nothing.",

    "This is the moment the Ghost appears. But to understand what makes the Adapter's"
    " Ghost distinct from every other Ghost, you must understand what it is that has"
    " gone quiet. The Architect's Ghost performs composure \u2014 there is still a"
    " self presenting, only the self is presenting fine-ness. The Island's Ghost"
    " performs contentment with solitude, offering the plausible alibi of needing"
    " space. The Ambassador's Ghost is a tragic betrayal \u2014 the caretaker who"
    " has gone cold, doing to another what they would never permit themselves to do."
    " The Vault's Ghost does not perform at all; it simply closes, doing what it has"
    " always done, only more so.",

    "The Adapter's Ghost does something none of these do. <b>It withdraws all the"
    " versions at once.</b> The room reads no signal because there is no version"
    " present to read. Your spouse will say, in those days, <i>I cannot tell what"
    " you are feeling</i> \u2014 and they will not be wrong. They will not be wrong"
    " because what has happened is not that you are hiding a feeling behind a version."
    " What has happened is that the calibration mechanism itself has been"
    " temporarily disabled. The part of you that normally produces the visible self"
    " \u2014 the part that reads the room and becomes what the room can receive"
    " \u2014 is not running. And in its absence, what the room receives is not an"
    " alternative self. It is an absence.",
]

GHOST_BODY_P2 = [
    "The Ghost looks, from the outside, like the standard performance of normalcy"
    " \u2014 <i>I'm fine, I'm just tired, nothing is wrong</i> \u2014 and for the"
    " Adapter this is partly true. But the performing is thin in a way it has never"
    " been thin before, because the Adapter's natural mode of being in the world is"
    " performance, and when the performance is this sparse it is a signal something"
    " has gone badly wrong. The people who know you best will sense it. They will"
    " not be able to name it precisely, but they will feel it: <i>something is"
    " happening in there, and I cannot find the door.</i>",

    "What is the Ghost seeking? It is, in part, what every Ghost seeks: to be"
    " discovered without having to announce itself. The hope, barely conscious and"
    " almost never named, is that the person who wounded you will notice the quiet"
    " and come looking \u2014 will realize, without being told, that something real"
    " is wrong, and will pursue. But for the Adapter there is a layer underneath"
    " this that is more specific and more strange. The Ghost is waiting to see if"
    " you are loved <i>without a version.</i> The question underneath the silence"
    " is not simply <i>will you come and find me?</i> It is: <i>will you come and"
    " find me when I have given you nothing to find? When the attuned self is not"
    " running, when there is no version on offer, when I am nothing but quiet"
    " \u2014 will you still come?</i>",

    "This is the Adapter's Ghost as a test \u2014 and it is a test that, by its"
    " nature, cannot be passed. Because even if the other person comes, the Adapter"
    " does not know how to receive the coming without immediately producing a version"
    " in response. The version comes back online the moment there is an audience."
    " The calibration resumes. And the question \u2014 the real question, the one"
    " underneath the test \u2014 is still unanswered, because the Adapter has not"
    " yet learned to stay in the absence long enough to receive what might be offered"
    " there.",
]

GHOST_BODY_P3 = [
    "Here is where this section must say something that will feel strange, and that"
    " is nonetheless true. The Adapter's Ghost is, in a way that no other breakdown"
    " in all thirty-six profiles can claim, the closest the Adapter has ever come to"
    " being themselves alone.",

    "Every other moment in the Adapter's life has an audience. Every other moment,"
    " the calibration is running: someone is in the room, or could be, and the"
    " Adapter is already reading, already adjusting, already producing. But in the"
    " Ghost, there is no version. There is no performance. There is only \u2014 for"
    " the first time, perhaps, in a very long time \u2014 a quiet interior that has"
    " not been arranged for anyone's benefit.",

    "The prophet Elijah understood something of this. After the triumph on Mount"
    " Carmel, after the fire fell and the prophets of Baal were confounded, he ran"
    " to the wilderness and collapsed under a broom tree and asked to die. He had"
    " been performing the role of prophet at full intensity, and the performance,"
    " however genuinely faithful, had emptied him. God did not come to him in his"
    " exhaustion with a new assignment or a bracing address. He came with bread and"
    " water and the instruction to sleep. And then, later, came the most important"
    " moment: Elijah in the cave on Mount Horeb. <i>And behold, the Lord passed by,"
    " and a great and strong wind tore the mountains and broke in pieces the rocks"
    " before the Lord, but the Lord was not in the wind. And after the wind an"
    " earthquake, but the Lord was not in the earthquake. And after the earthquake"
    " a fire, but the Lord was not in the fire. And after the fire the sound of a"
    " low whisper.</i> (1 Kings 19:11\u201312)",

    "The Adapter has spent a lifetime in the wind, the earthquake, and the fire"
    " \u2014 in the volume and the signal and the readable cue. The mechanism runs"
    " on input. The Adapter knows what to do when there is a room to read. But the"
    " still small voice \u2014 the <i>demamah daqah</i>, the thin silence \u2014 is"
    " something the Adapter has not learned to recognize, because the calibration"
    " that processes strong signals does not have a mode for the whisper.",

    "C. S. Lewis, in <i>Mere Christianity</i>, wrote something that names what the"
    " Ghost is, in its difficult way, opening toward: <i>The very moment you wake up"
    " each morning, all your wishes and hopes for the day rush at you like wild"
    " animals. And the first job each morning consists in shoving them all back; in"
    " listening to that other voice, taking that other point of view, letting that"
    " other larger, stronger, quieter life come flowing in.</i> The Adapter has not"
    " often shoved the wishes and hopes back. The wishes and the hopes have been"
    " the fuel of the mechanism. But the Ghost, for all its pain, is one of the few"
    " moments when the rushing stops, and the other voice might be heard.",

    "<b>This is the pastoral move this section must make.</b> The Ghost looks like"
    " withdrawal, and in many ways it is withdrawal. But it is also, sometimes,"
    " the door to an honesty the Adapter has not previously had access to. Not because"
    " suffering is automatically instructive, but because the Adapter in the Ghost"
    " has, for the first time, run out of versions to offer and is therefore available"
    " \u2014 if someone or Someone knows to come quietly, without demanding a"
    " version in return.",

    "The danger is this: the Adapter does not know how to stay in the absence. The"
    " moment a version becomes available \u2014 the moment there is a cue to read,"
    " a person to attune to, a room to enter \u2014 the calibration resumes and"
    " the stillness closes. The Ghost is not, in itself, healing. It is an opening."
    " Whether healing passes through it depends on what enters the silence before"
    " the next version does.",
]

GHOST_PROMPTS = [
    "Name the last time the Ghost appeared in you. Not the most dramatic time"
    " \u2014 the most recent. What happened, and what version did you reach for that"
    " was not there? Describe the moment in two or three sentences.",

    "What was the question underneath the Ghost's silence? Not <i>I am hurt</i>"
    " \u2014 deeper than that. Try to complete this sentence: <i>What I was actually"
    " waiting to find out was whether ___.</i>",
]

TWO_TOG_BODY = [
    "Now we place them side by side, because the Adapter and the Ghost are not two"
    " separate problems. They are the same interior life, moving in two different"
    " directions. The Adapter moves outward toward the rooms, reading and adjusting"
    " and becoming. The Ghost moves inward \u2014 or rather, for the Adapter, it moves"
    " nowhere. It simply stops. The signal that normally produces the visible self"
    " goes quiet, and the room receives an absence where it has always previously"
    " received a version.",

    "<b>The Adapter is what your need does when it has time and an audience.</b>"
    " The Ghost is what your need does when it runs out of both. The Adapter constructs"
    " versions so that disconnection will not have to be shown. The Ghost is"
    " disconnection without a version to show in its place. Together they form a loop,"
    " and the loop is powered by the same question: <i>Am I lovable, or is the love"
    " I have received always been love for the version \u2014 and is there anything"
    " here worth loving beneath it?</i>",

    "The pattern, in slow motion, looks like this. <b>(1)</b> The Adapter moves"
    " through the world reading rooms and becoming what the rooms need."
    " <b>(2)</b> A moment arrives in which the disconnection trigger fires:"
    " someone withdraws warmth, goes quiet, becomes unreadable in a way that reads"
    " as verdict. <b>(3)</b> The body says, <i>the connection has closed, and I"
    " do not know which version will restore it.</i> <b>(4)</b> The core question"
    " wakes up: <i>Am I lovable?</i> <b>(5)</b> The Adapter reaches for a version"
    " that will reconnect \u2014 a version warm enough, attuned enough, whatever"
    " the room most needs. <b>(6)</b> The version does not come. The wound is too"
    " large. The calibration stalls. <b>(7)</b> The Ghost appears: all versions"
    " withdraw at once. The Adapter goes through the motions \u2014 <i>I am fine,"
    " everything is fine</i> \u2014 but the performance is thin, the signal is"
    " absent, and the room cannot read what is happening. <b>(8)</b> The Ghost"
    " waits to be discovered. If discovery comes, the Adapter does not know how to"
    " receive it without immediately producing a version in response. The question"
    " is alive again within the hour.",

    "What breaks the loop is not a better version of the self, and it is not a more"
    " successfully performed normalcy. It is a different source for the self"
    " altogether. The Adapter's deepest healing is not the excavation of an authentic"
    " core \u2014 it is the reception of a name spoken by a Father who has been"
    " addressing the same person through all the versions, who has always seen the"
    " one underneath the many, and whose love does not require a version to land on."
    " Below is your sequence. Fill in the blanks. When you are done, read it aloud."
    " Both the Adapter and the Ghost lose some of their power when they hear"
    " themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as disconnection \u2014 as"
    " the warmth closing \u2014 and the old question wakes up: <i>am I lovable?</i>"
    " My first move is to ____________________,"
    " because the Adapter in me believes that if I can ____________________,"
    " the connection will be restored and the room will stay warm. When that does"
    " not work, the Ghost appears: I withdraw all the versions at once and go quiet,"
    " waiting to find out whether ____________________."
    " What I am actually after, underneath all of it, is the verdict ____________________"
    " \u2014 a verdict the Father has already spoken over me in ____________________,"
    " calling me by a name he chose before any room existed to require a version."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of tools \u2014 each one"
    " concrete enough to carry, honest enough to use. None of them will dissolve the"
    " Adapter's pattern in a single application. All of them, practiced over months,"
    " will loosen the grip of the loop you just named.",

    "I have divided them into two sets: tools for when the Adapter is overworking"
    " its calibration (when the room-reading has tipped from gift into compulsion),"
    " and tools for when the Ghost is running (when the wound is fresh and the"
    " versions have all gone quiet). The Adapter's tools come first, because the"
    " Ghost cannot be interrupted usefully until the mechanism underneath it"
    " is understood.",
]

ADPT_TOOLS = [
    ("The preference question",
     "Once a day, before the first social interaction, ask yourself one question"
     " without reference to anyone else in the room: <i>What do I want today?</i>"
     " Not what do I think would be best, not what would serve the relationship, not"
     " which version of me would be most useful. What do I want? The Adapter will find"
     " this question disorienting at first. That is the point. The disorientation is"
     " the honest recognition that the mechanism has been running. Do not push for a"
     " large answer. A small one will do."),

    ("The unedited opinion",
     "Once a week, in a low-stakes conversation, offer an opinion before you have"
     " checked it against what the other person appears to need. Not a combative"
     " opinion \u2014 simply an un-adjusted one. Notice what happens in your body"
     " when you do this. Notice whether the relationship survives. It almost certainly"
     " will, and the survival is data the Adapter needs to receive: you can be"
     " un-adapted and remain loved."),

    ("The handed-back calibration",
     "When you notice the Adapter running \u2014 when you catch yourself adjusting,"
     " selecting a version, softening a preference for the room \u2014 say quietly,"
     " before you adjust: <i>Lord, I am doing it again. The version I am about to"
     " present is not the whole of who you named. Help me be present as the person"
     " you chose.</i> You do not have to stop the adaptation immediately. Simply"
     " naming it disrupts its automaticity."),

    ("The solitude practice",
     "Once a week, spend thirty minutes alone without any input \u2014 no phone, no"
     " music, no reading. Sit with the question: <i>Who is here?</i> The Adapter,"
     " having nothing to calibrate to, will initially feel unmoored. That feeling is"
     " not emptiness. It is the legitimate discomfort of a self that has not often"
     " been allowed to be simply present without a room to serve. The practice, over"
     " months, begins to give the self below the versions a chance to speak."),

    ("The Psalm of the named self",
     "When the Adapter's calibration tips into anxiety \u2014 when you feel the"
     " compulsive need to check, adjust, and become \u2014 open to Psalm 139 and"
     " read the first four verses aloud: <i>O Lord, you have searched me and known"
     " me. You know when I sit down and when I rise up.</i> God is not reading the"
     " version you selected this morning. He is reading you \u2014 the specific,"
     " irreducible, un-adapted you he knew before the foundation of the world."
     " Let that land before you enter the next room."),
]

GHOST_TOOLS = [
    ("Name the absence before it becomes a performance",
     "Within the first hour of the Ghost appearing \u2014 before the thin performance"
     " of <i>I am fine</i> is fully established \u2014 tell one person one sentence:"
     " <i>Something happened today and I am not okay, and I do not yet have a version"
     " of this that I can offer you.</i> The Adapter's Ghost derives its power from"
     " the gap between the performance and the wound. Naming the wound before the"
     " performance is fully assembled disrupts the gap."),

    ("The still small voice practice",
     "When the Ghost is running and the silence is full, resist the instinct to fill"
     " it with a version. Instead, sit with the question: <i>What is actually here,"
     " underneath the absence?</i> You are looking not for a version to offer but for"
     " the thing the version would have covered. This is the practice of 1 Kings 19"
     " \u2014 waiting through the wind and earthquake and fire for the still small"
     " voice. It will feel like nothing is happening. Something is happening."),

    ("The one-word check",
     "When you must function normally while the Ghost is present \u2014 at work, at"
     " home, in conversation \u2014 discipline yourself to a small interior honesty"
     " at the end of each hour: one word that names what is actually there underneath"
     " the performance. Not a sentence; not a presentation. One word. <i>Hurt."
     " Scared. Lonely. Lost.</i> The Adapter's nervous system has been trained to"
     " skip this step. One word, once an hour, is the beginning of recovering it."),

    ("The prayer of the absent version",
     "When the Ghost is loudest and the absence is most total \u2014 when every version"
     " has gone quiet and you are not sure who is in the room with yourself"
     " \u2014 pray these words slowly: <i>Father, there is no version right now. I"
     " have nothing to offer you that is attuned to anything. You called me by name"
     " before any room existed to require a version of me. Come into this quiet. I"
     " am here, or I am trying to be.</i> Say it twice. The second time, more"
     " slowly. The Father does not require a version to arrive."),

    ("The repair that speaks from one self",
     "When the Ghost has run its course and the versions begin to come back online,"
     " the pastoral practice is to resist the first version and speak instead from"
     " the still point. Not the attuned version most likely to restore warmth, but"
     " the honest sentence: <i>I went quiet because I was hurt, and what I needed"
     " to know was whether I would be found when I had nothing to offer.</i> One"
     " wound, one speaker, one sentence. This is the Adapter's hardest practice and"
     " its most healing one."),
]

PRAYER_BODY = [
    "Father,",

    "You see the Adapter in me, and you are not disoriented by him. You have seen"
    " every version, attended every room, watched every calibration. You know which"
    " ones were gifts and which ones were survival, and I am not sure I always know"
    " the difference. Thank you that the attunement has been genuinely useful, in"
    " real relationships, to real people, who have been genuinely served by it. He"
    " has not been wrong about everything.",

    "But Father, I am tired of not knowing which version is me. I am tired of walking"
    " out of conversations and not being entirely sure what I actually believe, or"
    " what I actually felt, or whether the warmth I gave was love or insurance."
    " I am tired of carrying a self that is assembled from what the rooms reflected"
    " back, and not knowing what is underneath when the rooms go quiet. And I am"
    " tired of the Ghost \u2014 that thin and terrible silence in which all the"
    " versions have gone and I do not know what is left.",

    "Teach me that you have already named the underneath. That before any room"
    " existed to require a version, you chose me in Christ \u2014 <i>before the"
    " foundation of the world,</i> as Paul says in Ephesians 1:4 \u2014 not the sum"
    " of my adaptations, but the self that was there before the adapting began."
    " That 1 John 3:1 is speaking of me, specifically: <i>Behold, what manner of"
    " love the Father has bestowed on us, that we should be called children of"
    " God.</i> Not called because of the version that showed up this morning. Called"
    " \u2014 named, addressed, claimed \u2014 with no version required.",

    "Lord Jesus, when the Ghost appears in me \u2014 when all the versions have gone"
    " quiet and I am waiting to be discovered without knowing how to be found"
    " \u2014 would you come into the silence? Not with a cue to read or an assignment"
    " to perform, but with the still small voice that was always there in the cave"
    " on Mount Horeb, waiting for your servant to stop listening for wind and"
    " earthquake and fire? I have spent a long time listening for signals I could"
    " calibrate to. Teach me the frequency of the whisper.",

    "Holy Spirit, where I am adapting out of fear, give me the courage to stay."
    " Where the Ghost is performing normalcy, give me the words of one honest"
    " sentence. Where the versions are all I know, give me the slow discovery of"
    " the self that was named before they started. And where the silence opens,"
    " be the One who enters it, so that for once the Adapter may receive rather"
    " than produce.",

    "In the name of the One who walked into every room as himself \u2014 who read"
    " every person in his presence and loved them without adjusting who he was to"
    " keep them close \u2014 I pray.",

    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Adapter and the Ghost have"
    " been with you for a long time, and one careful reading will not retire them."
    " What follows is a short list of next steps \u2014 some immediate, some"
    " longer-term \u2014 for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.",
     "Different lines will land. The Adapter will resist a second reading \u2014 he"
     " prefers to adjust to new information once and then move on to the next room."
     " Read it again anyway. The section that felt least relevant today may be the"
     " most necessary one in a month."),

    ("Take one tool, not six.",
     "Choose a single practice from Section 7 and try it for two weeks before adding"
     " another. The tools are postures, not a program. One posture, held for long"
     " enough, begins to give the self below the versions a chance to breathe."),

    ("Tell one person what you found.",
     "Not the whole document. One sentence: <i>I learned that my mechanism is the"
     " Adapter, and when I am hurt I go quiet in a way that is different from what"
     " it looks like from the outside, and I have been trying, in my own way, to"
     " find out whether I am loved when there is no version to offer.</i> Speaking"
     " it to a trusted witness in your own voice is the first act of living outside"
     " the performance."),

    ("Sit with one Psalm of the named self.",
     "Psalm 139 for a week, aloud, one section per day. Verse 1: <i>You have searched"
     " me and known me.</i> Verse 13: <i>For you formed my inward parts.</i>"
     " Verse 16: <i>In your book were written, every one of them, the days that were"
     " formed for me, when as yet there was none of them.</i> The Adapter needs, more"
     " than almost any other mechanism, the practice of being addressed by God as a"
     " singular, known, irreplaceable person. The Psalms do this. Let them."),

    ("Read further on the self you did not build.",
     "Tim Keller, <i>Counterfeit Gods: The Empty Promises of Money, Sex, and Power,"
     " and the Only Hope That Matters</i> \u2014 especially his treatment of identity"
     " as something received rather than constructed. C. S. Lewis, <i>Mere"
     " Christianity</i> \u2014 particularly the chapters on the new self in Book IV;"
     " his account of the self that comes from being inhabited by Christ rather than"
     " performed for others is the most precise pastoral address to what the Adapter"
     " most needs. Augustine, <i>Confessions</i>, Book I \u2014 especially the first"
     " three chapters; Augustine's restlessness is your restlessness, and his"
     " discovery is available to you."),

    ("If you are stuck, ask for help.",
     "There are seasons when the Adapter and the Ghost are too entrenched to dislodge"
     " alone. A wise pastor, a Christian counselor, a trusted friend who has earned"
     " the right to your un-adapted self \u2014 these are not signs of failure. For"
     " the Adapter specifically, asking for help without managing the other person's"
     " experience of the asking is one of the most countercultural and most healing"
     " things on this list."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom"
    " by a Father who chose you before the foundation of the world \u2014 before any"
    " room existed to require a version, before any feedback was available to borrow."
    " The self underneath the adaptations is not missing. It is named. It is kept."
    " It is beloved. Go gently with yourself. The One who began the good work"
    " in you will be the one who finishes it."
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
        [Paragraph("WAS THE WARMTH GONE?", header_style),
         Paragraph("what your nervous system concluded", sub_style)],
        [Paragraph("WAS MY STANDING IN DANGER?", header_style),
         Paragraph("the deeper question", sub_style)],
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
    """Generate the Adapter+Ghost walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='ADPT', primary_breakdown='GHOST',
    primary_trigger='DISC', core_question='LOV'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor's Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR'S WALKTHROUGH",
        cover_right_label="ADAPTER  \u00b7  GHOST",
        title="Take 139 Walkthrough \u2014 Adapter + Ghost",
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
    story.append(Paragraph("The Adapter \u00a0\u00b7\u00a0 The Ghost", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disconnection \u00a0\u00b7\u00a0 Core Question: Am I lovable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cThe very moment you wake up each morning, all your wishes and"
        " hopes for the day rush at you like wild animals. And the first job each"
        " morning consists in shoving them all back; in listening to that"
        " other voice.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18,
                       textColor=MUTED)))
    story.append(Paragraph(
        "C. S. Lewis, <i>Mere Christianity</i>",
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
                   "The moment the warmth closes, and what your soul makes of it.")
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

    # ── SECTION 3: Core Question ──
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I lovable?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "What Scripture says about lovability.",
                   "A love already given, and the honest cost of receiving it.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "Where was the warmth actually gone? Where was my soul actually free?")
    story.append(Paragraph(
        "Use the table below. In the first column, name a recent event in which the"
        " disconnection trigger fired. In the second, write what your nervous system"
        " concluded: <i>was the warmth gone?</i> In the third, answer the deeper"
        " question: <i>was the part of me that finally matters \u2014 my soul, my"
        " standing before God \u2014 at any point in danger?</i>",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table())
    story.append(PageBreak())

    # ── SECTION 4: Mechanism ──
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Adapter.",
                   "The chameleon, the social tuning fork. What you have built, and what the building cost you.")
    for p in ADPT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "How the Adapter formed, and what it costs.",
                   "The histories, and the question the Adapter cannot answer.")
    for p in ADPT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ADPT_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Adapter.",
                   "Read the Adapter's own words. He has been faithful; let him speak.")

    letter_style = ParagraphStyle(
        "AdptGhostLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for line in ADPT_LETTER_INSTRUCTION:
        story.append(Paragraph(line, letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in ADPT_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Ghost.",
                   "The withdrawal of all versions at once. The room reads no signal.")
    for p in GHOST_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in GHOST_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The still small voice.",
                   "Why the Ghost is the closest the Adapter has ever come to being alone with God.")
    for p in GHOST_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Step out of the silence.",
                   "Two questions to sit with before you turn the page.")
    for prompt in GHOST_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same need, in two directions.",
                   "The Adapter and the Ghost are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=6)
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
                   "When the Ghost withdraws all the versions at once.",
                   "Five practices for the moment the calibration goes silent.")
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


# ── STANDALONE TEST ────────────────────────────────────────────────────
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "ADPT"
        primary_breakdown = "GHOST"
        primary_trigger = "DISC"
        core_question = "LOV"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "adapter_ghost_test.pdf")
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

    print(f"DONE: adapter_ghost.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
