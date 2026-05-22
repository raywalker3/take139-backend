"""Personal Walkthrough — Adapter + Attorney.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Control trigger, "Am I free?" core question.
~25 pages, 9 sections.

Calibration anchor: Batch 4 — FIRST ADAPTER walkthrough. Establishes the
Adapter mechanism as a distinct character. The Adapter reads the room and
becomes whatever the room needs; their inner sense of self is borrowed from
feedback rather than held independently; can be utterly authentic in five
different ways with five different people in one day.

DISTINGUISHING MOVE: The Adapter's Attorney is a multi-witness courtroom
where every witness is the same person speaking from a different persona.
The closing argument cites evidence from multiple identities the spouse
may not have known existed in the same person.

Key theological move in Section Five: the Adapter has spent so long
borrowing self from feedback that even the wound is borrowed. The
pastoral resolution is not "find your true self" but "receive your true
self from the One who named you before you named yourself." 1 John 3:1,
Ephesians 1:4, C. S. Lewis (The Weight of Glory), Augustine (Confessions).
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
    "Before you read any further, I want to do for you what a good counselor does in the first session. I want to lower the lights and slow the pace, because what you are about to look at is not a catalogue of your strengths, though you have real ones, and it is not a verdict on the way you have moved through relationships, though there is something in it that must be carefully named. It is a patient conversation about the way your soul has learned to keep itself safe \u2014 and for you, that strategy has been so fluid, so natural, and so genuinely useful that you may not have recognized it as a strategy at all.",
    "You are, in a real sense, an Adapter. Not because you are false or insincere \u2014 the Adapter is, if anything, one of the most genuinely present people in any room. But because something early in your experience taught you that the surest path to connection was not to bring a fixed self and wait to see if it was wanted, but to read the room carefully and become what the room could receive. You learned to move between people the way a musician moves between keys \u2014 the same instrument, but a different sound depending on what the piece required.",
    "We are going to walk through your trigger \u2014 the specific moment your nervous system says something is wrong here. We will listen to the question underneath that moment, one that has probably been with you since you were very small. We will name the strategy you have built in response, and the place that strategy collapses under pressure. And then, only then, will we put tools in your hands.",
    "If you were sitting across from me, I would say this plainly. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who did not first know the versions of you that you have offered to the world and then decide whether to love you; a Son who, in the thirty-three years he walked this earth, was himself in every room he entered, and who calls you by a name he chose before you ever walked into any room at all; and a Spirit who is, at this very moment, the only resident of the interior you have rarely let anyone else fully enter.",
    "So read slowly. Argue with what does not fit. Stay with what does. Pray when something catches in your throat, because that catch is usually the Lord saying, <i>look here, with me.</i> The goal is a slightly freer life, lived from a self that does not need to be negotiated fresh in every room you enter. Take your time. The chapter you are about to read about yourself has been a long time in the writing.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it is difficult to describe to people who do not share your wiring, because from the outside it looks like almost nothing. Someone tells you what to do in a tone that does not ask. A decision that affects you is made without consulting you. A spouse sets a rule \u2014 a small one, perhaps even a reasonable one \u2014 and something in you goes quiet and still in a way that has nothing to do with whether you agree with the rule. Someone uses the word <i>should</i> in a particular way, directed at you, and you feel something tighten.",
    "This is not the tightening of stubbornness, though it can look like that from the outside. It is not the tightening of pride, though pride will sometimes attach to it quickly. What fires inside you, under three seconds, is a signal that is older and more primal than either of those. The signal is not <i>that is unfair.</i> The signal is closer to <i>something about who I am is being overridden, and I do not know if there is enough of me left to be overridden.</i>",
    "This is your trigger. The word we use for it is <b>control</b>, but the word needs unpacking, because it is doing more work here than it appears to do. For most people, a control trigger is about autonomy \u2014 the desire not to be told what to do. For you, it is something more subtle and more frightening. The question that rises underneath the trigger is not merely <i>will I be allowed to make my own choices?</i> It is: <i>Am I free? Is there a me here that is not simply a reflection of what you need from me? Will my individuality survive this relationship?</i>",
    "C. S. Lewis, in <i>The Weight of Glory</i>, observed that there is something in every human soul that longs to hear a word spoken by the highest authority: <i>well done</i> \u2014 not to a performance, but to a person. You have spent years performing, and you have been extraordinarily good at it, and the applause has been real. But the performance has left behind a question that the applause has never quite answered: <i>if I stopped performing \u2014 if there were no room to read and no version to become \u2014 would there be someone here? And would that person be loved?</i>",
    "<b>Your sensitivity to control is not random.</b> It is the residue of something learned early in a household where having your own preferences, your own particular interior life, was costly. Perhaps love in your family was conditional on conformity. Perhaps the emotional climate changed unpredictably and reading the room became survival before it became style. Perhaps there was enmeshment, a family system so tightly woven that having a self that differed from the family's preferred self felt threatening to the whole unit. Whatever the history, the lesson lodged clearly: <i>the safest thing is to be whatever the room can love.</i> And over time, the Adapter was born \u2014 not as a deceiver, but as a genuinely gifted reader of human beings who learned to give each person the version of you they most needed to receive.",
    "Before we go further, I want you to sit with two questions in writing. Not in your head \u2014 the Adapter's head will reframe the questions to fit whatever the moment seems to need. Your hand will be more honest.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week, that the control trigger fired. What happened, in two sentences? You are not looking for a dramatic event \u2014 often the trigger fires quietly, in a small moment of being told how things will be.",
    "What was the size of the actual event, and what was the size of the response inside you? If the response was significantly larger than the event \u2014 if something in you went quiet or still in a way that surprised you \u2014 you have just located your trigger.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding. The Adapter has been guarding this one for a very long time, and has been guarding it so skillfully that you may not have let yourself put it into plain words.",
    "Yours is this: <b>Am I free?</b>",
    "It is not simply the question of whether you are allowed to make your own choices \u2014 though that concern is real, and we will stay with it. It is something more personal and more frightening than external permission. It is the question of a soul that has spent so much time reading rooms and becoming what rooms needed that it now wonders whether there is a self underneath the adaptations that would survive if the adaptations were removed. <i>Am I free to be myself? And if I were \u2014 truly, without adjustment, without the version-selection \u2014 is there a self to be?</i>",
    "Most adults would prefer not to ask this question. They have organized their lives so that it does not need to be asked directly. For the Adapter, the question comes in through the side door every time someone tries to set a boundary on who you are allowed to be in their presence. The trigger is not the rule; the trigger is the implication behind the rule: <i>there is a you that is more convenient to me, and I would like that version rather than the one currently present.</i> And your soul, which has been selecting versions of itself for years, does not know whether to comply or revolt, because it is not entirely sure it has a version that is not already a selection.",
]

QUESTION_BODY_P2 = [
    "There is a reason that the theologians of the Reformation \u2014 Luther, Calvin, the entire tradition the Apostle Paul grounded \u2014 saw freedom as not merely a political or social category but a theological one. The freedom that matters most is not the freedom to do whatever you wish. It is freedom from the tyranny of being anyone's source of meaning \u2014 the freedom of a soul that does not have to earn its standing in every room it enters. This is what Paul names in Romans 6:6\u20137: <i>We know that our old self was crucified with him in order that the body of sin might be brought to nothing, so that we would no longer be enslaved to sin. For one who has died has been set free from sin.</i>",
    "The Adapter's captivity is rarely to sin in the obvious sense. It is to something subtler: the captivity of a self that cannot be still, that must keep reading and adjusting and becoming, because the alternative \u2014 being simply who one is, without the adaptive fluency \u2014 feels exposed in a way that is intolerable. Paul names this too: <i>you did not receive the spirit of slavery to fall back into fear.</i> (Romans 8:15) The Adapter's adaptation is, at its root, a response to fear \u2014 the fear that a fixed, un-performed self will be found wanting.",
    "The Psalms name this longing honestly. Psalm 31:8: <i>you have not delivered me into the hand of the enemy; you have set my feet in a broad place.</i> The broad place David is speaking of is not a wide field. It is the freedom of a soul whose standing does not depend on performing correctly, on reading the room, on becoming what the moment requires. And yet here is the honest rub: the gospel tells the Adapter that in Christ you are already free \u2014 that the question <i>am I free?</i> has been answered once and permanently. Your nervous system does not feel this yet. It has been reading rooms for so long that being told it does not have to feels less like freedom and more like a trick.",
]

QUESTION_BODY_P3 = [
    "The gospel anchor for the question you carry is this: you are a <i>New Creation</i> \u2014 the old identity in Adam, with all its captivity and its exhausting responsiveness to whoever was in the room, is dead. <i>Therefore, if anyone is in Christ, he is a new creation. The old has passed away; behold, the new has come.</i> (2 Corinthians 5:17) This is not a permission to stop caring about the people around you \u2014 the Adapter's attunement is a genuine gift, and the gospel does not retire gifts. It is the announcement that the attunement is now free to be what it was always designed to be: love that flows from abundance rather than adaptation that flows from need.",
    "The freedom the Adapter has been guarding so fiercely is already fully yours in Christ. You do not need to fight for it, perform for it, or flee from rooms that threaten it. John 8:36 says it plainly: <i>if the Son sets you free, you will be free indeed.</i> Not free pending compliance. Not free conditional on the right performance. Free indeed \u2014 which is to say, free even when the room is asking for something else.",
    "The work this section invites is not more self-examination \u2014 the Adapter has enough introspection. The work is the slow practice of receiving freedom as a gift already given, rather than fighting for it as a territory that must be defended. Before we close this section, use the table below. Not to analyze, but to observe: where did the control trigger fire this week, and where was my soul's freedom actually in danger?",
]

ADPT_BODY_P1 = [
    "You have built something. It did not announce itself as a strategy when it was forming. It formed the way a river forms \u2014 not by decision, but by the path of least resistance through a landscape that rewarded certain movements and punished others. And one day you looked up and the river was already there, running through every relationship you had, shaping the way you moved through every room. Throughout this walkthrough we are going to call it <b>the Adapter</b>, and the Adapter deserves to be introduced as a character before we say anything about what it costs you.",
    "The Adapter is not the Ambassador. This distinction matters, and the two mechanisms look so similar from the outside that they are worth pausing over carefully. The Ambassador takes care of people by serving them \u2014 bringing warmth, managing emotional temperature, being the one who notices when someone is left out and goes to find them. The Ambassador is the same person across contexts, serving differently but remaining recognizably themselves. The Adapter does something different: the Adapter takes care of people by <i>becoming what they need to see.</i> Not performing a false self \u2014 the Adapter is genuinely present in every version. But the version itself shifts. You can be utterly authentic in five different ways with five different people in one day and feel no contradiction, because for the Adapter, authenticity has never been a fixed self presenting itself consistently; it has been the full entering-in to whatever the relationship most needs.",
    "The Ambassador knows they are the same person serving differently across contexts. The Adapter may genuinely not know that. And this \u2014 the gift and the cost in a single sentence \u2014 is precisely what this section is about. There is a great deal in Scripture that commends relational intelligence of this kind. Proverbs 25:11 says: <i>A word fitly spoken is like apples of gold in a setting of silver.</i> Paul himself said: <i>I have become all things to all people, that by all means I might save some.</i> (1 Corinthians 9:22) The Adapter lives this verse before they have ever read it. It is a genuine fluency in relational languages, and the world runs better when people like you are in it.",
]

ADPT_BODY_P2 = [
    "But there is a cost, and the cost is specific to this mechanism, and it deserves to be named honestly. The Adapter's most characteristic experience is this: you can be fully present in a conversation \u2014 genuinely moved, genuinely engaged, genuinely yourself \u2014 and walk away an hour later and not be entirely sure which of your preferences, which of your opinions, which of your actual interior responses were yours and which were calibrated to the person you were with. The calibration happens below the level of conscious decision. It is not dishonesty. But it produces, over years, a specific kind of interior ambiguity about what you actually want, what you actually believe, what you would actually choose if no one were in the room to calibrate to.",
    "The taxonomy we work from suggests several histories that tend to produce the Adapter, and you will likely recognize yourself in at least one. Perhaps you grew up in a household where the emotional climate changed frequently and reading the room was not a preference but a survival skill \u2014 the way to stay safe was to become what the safest version of the moment needed. Perhaps there was enmeshment, a family system where having a self that differed from the family's preferred self felt dangerous, and you learned to make your self available rather than insisting on it. Perhaps you discovered very early that being exactly what someone needed was the most intoxicating experience available \u2014 the look of recognition on a person's face when you gave them the version of you they did not know they were looking for. Perhaps a parent's love was conditional on conformity and you adapted into lovability and never quite found your way back to yourself.",
    "Whatever the specific history, the Adapter's deepest characteristic is not the adaptation itself. It is the difficulty of answering, in the quiet, the question the taxonomy asks with unusual directness: <i>Who are you when no one is watching? Not the best version, not the version adapted to what this room needs \u2014 just you, alone, with no one to read.</i> For most people, this question has an answer ready. For the Adapter, the answer is slower in coming, and more honest people will say it is not always clear.",
    "<b>The Adapter is not your enemy.</b> He is a younger version of you who learned, in some real and specific circumstance, that the self which could flex was safer than the self which held its ground. He deserves your respect, not your contempt. He kept you connected. He gave you gifts \u2014 empathy, attunement, a rare fluency in the emotional languages of the people around you \u2014 that are genuinely valuable. But he has been working overtime on a project that was finished years ago. The room that first required him is long gone. And the question he was built to prevent \u2014 <i>will you be acceptable if you are simply yourself?</i> \u2014 is one that he is not, and has never been, equipped to answer.",
]

ADPT_BODY_P3 = [
    "What does it look like to begin loosening the Adapter's grip? Not eliminating the gift \u2014 the attunement is real and should not be retired. But beginning, slowly, to distinguish between the attunement that flows from love and the adaptation that flows from fear. These two things feel almost identical from the inside. The difference is in the root: the attunement that flows from love can stop if the stopping is right; the adaptation that flows from fear cannot stop without triggering the alarm.",
    "It begins with sitting still long enough to notice what you actually want. Not what the room wants from you, not what would serve the other person best, not which version of your preference would land most smoothly. What do you want? The Adapter often discovers, when sitting with this question for the first time without the usual social context to calibrate against, that the answer is genuinely unclear. This is not a failure of self-knowledge. It is the honest recognition of a mechanism that has been so faithfully at work that the self underneath it has not had much occasion to speak.",
    "The letter below is written in the Adapter's voice. He is not villainous. He is genuinely confused, and genuinely faithful, and genuinely tired. He has something to say that he has never been asked to put into words. Give him that chance now.",
]

ADPT_LETTER_INSTRUCTION = [
    "The letter below is written from the Adapter, in his own voice, to you. He is not a villain; he is a craftsman who has mistaken his tool for his identity. Read it slowly. Then answer the three prompts that follow.",
    "Dear [your name],",
    "I want to tell you something I have never been asked to say, because I have never been still long enough to say it. And the truth is, the stillness is the problem. I do not do well with stillness. In stillness, there is no room to read. There is no feedback to borrow. There is no version of you to present. There is only \u2014 I am not sure what. And that not-knowing is the thing I have been moving away from, more or less continuously, for as long as I can remember.",
    "I learned early that I could be loved. Not by being fixed, not by holding my ground, not by saying <i>this is who I am and this is what I want</i>. That kind of love felt too uncertain \u2014 you put yourself out and waited and the waiting was unbearable. But I found something better, or what seemed like something better: I could read what someone needed, and become it, and the love came immediately. It did not require waiting. It required attention, and I had an inexhaustible supply of attention.",
    "I want you to know what I actually did for you. I kept you in every room you were ever in. I kept the relationships going. I kept people close. I made you easy to love, because I made sure that whoever you were with, you were giving them something they needed. That is not nothing. You have been loved. A lot. And I have worked hard for that.",
    "What I did not know how to do \u2014 what I am only now beginning to see I could not do \u2014 is give you a self that was yours when no one was there. I kept you present in every room. I did not know how to keep you present in the room with no one in it. I do not think I knew there was supposed to be a you there too.",
    "I am telling you this because I think you have started to feel the cost. The exhaustion. The disorientation when someone asks what you want and you genuinely do not know. The moment in an argument when you realize you have been presenting the version most likely to resolve the conflict, and you cannot remember which version is the one you actually believe. I notice those moments. I do not know how to fix them. But I want you to know: I did not mean to steal the self. I was trying to save it.",
    "The Adapter",
]

ADPT_LETTER_PROMPTS = [
    "What part of the Adapter's letter surprised you? Not the part you expected \u2014 the part you were not quite ready for.",
    "The Adapter says he kept you in every room but could not keep you present when no one was there. When was the last time you sat quietly, without calibrating to anyone, and felt at home in yourself? Describe that moment, or describe the absence of it.",
    "The Adapter says he did not mean to steal the self. What would it mean, in practice, to begin recovering it? Name one relationship, one context, one ordinary situation where you might let the un-adapted version of yourself be present \u2014 even slightly.",
]

ATT_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Adapter, the breaking has a shape that is, among all the versions of this breakdown we track, the most theologically strange and the most pastorally interesting. The breakdown is called <b>the Attorney</b>, and the Adapter's version of it is unlike any of the others that carry this name.",
    "Here is the setup. The Adapter has been doing what the Adapter does \u2014 reading every room, adjusting to every person, being whatever the relationship most needed. Then something lands. A wound large enough that the usual adjustment cannot contain it. A spouse who criticizes not a behavior but a person. A friend who reveals, in a moment of carelessness, that the version of you they have been receiving is not one they particularly valued. A moment in which the control trigger fires so hard that the Adapter cannot find the right version to produce, and the mechanism stalls.",
    "And then something happens that the Adapter almost never sees coming, because the Adapter has almost never been still enough to notice it was there. The courtroom opens. And what steps to the floor is not one attorney. It is many. Because the Adapter has not been living one life in one relationship. The Adapter has been performing, genuinely and faithfully, multiple selves across multiple contexts \u2014 and each of those selves has been keeping its own private record of the wound.",
    "The Architect's Attorney argues live and loud: <i>the blueprints were violated.</i> The Island's Attorney builds quietly in private and delivers a single devastating closing statement. The Ambassador's Attorney produces the ledger of love. The Vault's Attorney unseals the file. The Adapter's Attorney is something none of these. It is a multi-witness courtroom, and every witness is the same person testifying from a different persona.",
]

ATT_BODY_P2 = [
    "Here is what this looks like. The wound has been received. The Adapter, for once, cannot adjust around it. And the closing argument that emerges does not come from a single self presenting a unified grievance. It comes in layers, in voices, in the different registers the Adapter inhabits \u2014 and the effect, on the person receiving it, is disorienting in a way that no other version of this breakdown produces.",
    "<i>When I was being the colleague-version of me, I noticed that you never once acknowledged my competence in front of others. When I was being the calm-version of me, I stayed quiet through things that hurt me because I thought that was what this relationship needed. When I was being the funny-version of me, I was actually covering grief. When I was being your wife, I became whatever you needed me to be in every season \u2014 and the version you are now criticizing is not a failure of character. It is the version you asked for.</i>",
    "The person on the other side of this conversation is experiencing something they will not easily be able to describe afterward. They are discovering, for the first time, that the person they thought they knew had multiple interior rooms they never knew existed \u2014 and that each of those rooms has been injured, and that each injury is now being presented, simultaneously, in the same closing argument. They knew the Adapter. They did not know the Adapter's Adapter. And now they are meeting all of them at once, in a courtroom they did not know was in session.",
    "<b>The Adapter's Attorney does not merely cite evidence from one person. It cites evidence from multiple identities the spouse may not have known existed in the same person.</b> This is not deception. Each version was real and did the work it was asked to do. But presenting them all at once, in a moment of wound, has an effect that is almost impossible to repair \u2014 because the other person, having heard it, now has to decide whether the person they loved was one person or several. And the Adapter, in this moment, is not sure of the answer either.",
]

ATT_BODY_P3 = [
    "Here is the pastoral problem at the heart of this breakdown. The Adapter has spent so long borrowing self from feedback that even the wound is borrowed. The grief is the accumulated grief of several versions of one person, each of whom experienced the wound differently. The Adapter, who has never had a stable enough center to know which version is the real one, is not entirely sure whose grief this is.",
    "C. S. Lewis wrote in <i>The Weight of Glory</i>: <i>There are no ordinary people. You have never talked to a mere mortal.</i> He was speaking of others; I want to turn it toward you. There is no ordinary you. Underneath the versions there is a person \u2014 singular, irreducible, known to God before any version started \u2014 not a composite of the rooms' reflections but a self chosen and named before a single room existed. The secular answer is: <i>find your true self.</i> Not wrong, but insufficient \u2014 it leaves the Adapter in charge of a discovery process that the mechanism has already shaped. The gospel's answer is more radical and more kind: <b>you do not need to find your true self. You need to receive your true self from the One who named you before you named yourself.</b>",
    "The Apostle John wrote: <i>Behold, what manner of love the Father has bestowed on us, that we should be called children of God.</i> (1 John 3:1) Notice the word <i>called</i>. Not assembled. Not negotiated. Called \u2014 spoken into being, addressed by name, claimed. Paul goes back even further: <i>he chose us in him before the foundation of the world.</i> (Ephesians 1:4) Before any room existed to be read. Before any feedback could be given or received. The self that is named is not the sum of your adaptations. It is the self that was chosen before the adaptations began.",
    "Augustine wrote the most honest thing anyone has ever written about the restless soul: <i>Thou hast made us for thyself, and our heart is restless until it rests in thee.</i> The Adapter's restlessness is the restlessness Augustine is describing \u2014 moving from room to room, version to version, because the self has not yet found the place where it does not have to perform to stay. That place is not another room to read. It is a Father who already knows the self underneath the adaptations and has declared it beloved.",
]

ATT_PROMPTS = [
    "Name the last time the Adapter's Attorney appeared \u2014 not necessarily out loud, but in the internal closing argument. Which versions of you showed up to testify? Name two or three by their characteristic role: <i>the version who stayed calm for years; the version who laughed it off; the version who became your ideal partner.</i>",
    "Underneath the multi-witness brief, there is one wound in one person. Name it in a single sentence, stripped of the different voices: <i>What I actually needed from you, in my own name, was ___.</i>",
    "The secular answer is: find your true self. The gospel answer is: receive your true self from the One who named you before you named yourself. In 1 John 3:1, you are called a child of God \u2014 not because of any version you produced, but because of what the Father has bestowed. What would it mean, in practice, to live from that identity rather than from the room's reflection?",
]

TWO_TOG_BODY = [
    "Now we place them side by side, because the Adapter and the Attorney are not two separate problems. They are the same interior life, moving in two different directions. The Adapter moves outward toward the rooms, reading and adjusting and becoming. The Attorney moves inward, assembling evidence from every version of the self that was hurt, and eventually delivers it all at once.",
    "<b>The Adapter is what your need does when it has time.</b> The Attorney is what your need does when the time runs out. The Adapter constructs versions so the wound will not have to be shown. The Attorney presents every version and every wound simultaneously when the construction can no longer hold. Together they form a loop, and the loop is powered by the same question: <i>Am I free to be myself, and if I were, would that self be loved?</i>",
    "The pattern, in slow motion, looks like this. <b>(1)</b> The Adapter moves through the world reading rooms and becoming what the rooms need. <b>(2)</b> A moment arrives in which the control trigger fires: someone attempts to define who you are supposed to be, or fails to acknowledge the cost of who you have been. <b>(3)</b> The trigger fires. The body says, <i>something about who I am is being overridden.</i> <b>(4)</b> The core question wakes up: <i>Am I free?</i> <b>(5)</b> The Adapter tries to produce a version that will resolve the tension \u2014 a version that is honest enough to satisfy, but adaptive enough not to cost anything. <b>(6)</b> It does not work. The wound stays open. <b>(7)</b> The Attorney assembles the multi-witness brief, presenting evidence from every version of the self that the relationship has ever asked for. <b>(8)</b> The verdict does not satisfy, because the self that was hurt was never clearly one self, and the acknowledgment that arrives cannot find its target. The question is alive again within the hour.",
    "What breaks the loop is not a better version of the self, and it is not a more articulate closing argument. It is a different source for the self altogether. The Adapter's deepest healing is not a therapeutic excavation for an authentic core \u2014 it is the reception of a name spoken by a Father who has been addressing the same person through all the versions, who has always seen the one underneath the many, and whose love is not calibrated to which version showed up today. Below is your sequence. Fill in the blanks. When you are done, read it aloud. Both the Adapter and the Attorney lose some of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as control \u2014 as "
    "being required to be a particular self that is not mine to choose \u2014 and the "
    "old question wakes up: <i>am I free?</i> My first move is to ____________________, "
    "because the Adapter in me believes that if I can ____________________, the threat "
    "will pass and the room will remain. When that does not work, the Attorney assembles "
    "the brief, and every version of me who was hurt shows up to testify that ____________________. "
    "What I am actually after, underneath all of it, is the verdict ____________________ "
    "\u2014 a verdict Christ has already spoken over me in ____________________, calling me "
    "by a name he chose before any room existed to reflect it."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of tools \u2014 each one concrete enough to carry, honest enough to use. None of them will dissolve the Adapter's pattern in a single application. All of them, practiced over months, will loosen the grip of the loop you just named.",
    "I have divided them into two sets: tools for when the Adapter is overworking its calibration (when the room-reading has tipped from gift into compulsion), and tools for when the Attorney is assembling the multi-witness brief (when the wound is fresh and the versions are beginning to line up). The Adapter's tools come first, because the Attorney cannot be interrupted usefully until the mechanism underneath it is understood.",
]

ADPT_TOOLS = [
    ("The preference question", "Once a day, before the first social interaction, ask yourself one question without reference to anyone else in the room: <i>What do I want today?</i> Not what do I think would be best, not what would serve the relationship, not what version of me would be most useful. What do I want? The Adapter will find this question disorienting at first. That is the point. The disorientation is the honest recognition that the mechanism has been running. Do not push for a large answer. A small one will do."),
    ("The unedited opinion", "Once a week, in a low-stakes conversation, offer an opinion before you have checked it against what the other person appears to need. Not a combative opinion \u2014 simply an un-adjusted one. Notice what happens in your body when you do this. Notice whether the relationship survives. It almost certainly will, and the survival is data the Adapter needs to receive: you can be un-adapted and remain loved."),
    ("The handed-back calibration", "When you notice the Adapter running \u2014 when you catch yourself adjusting, selecting a version, softening a preference for the room \u2014 say quietly, before you adjust: <i>Lord, I am doing it again. The version I am about to present is not the whole of who you named. Help me be present as the person you chose.</i> You do not have to stop the adaptation immediately. Simply naming it disrupts its automaticity."),
    ("The solitude practice", "Once a week, spend thirty minutes alone without any input \u2014 no phone, no music, no reading. Sit with the question: <i>Who is here?</i> The Adapter, having nothing to calibrate to, will initially feel unmoored. That feeling is not emptiness. It is the legitimate discomfort of a self that has not often been allowed to be simply present without a room to serve. The practice, over months, begins to give the self below the versions a chance to speak."),
    ("The Psalm of identity", "When the Adapter's calibration tips into anxiety \u2014 when you feel the compulsive need to check, adjust, and become \u2014 open to Psalm 139 and read the first four verses aloud: <i>O Lord, you have searched me and known me. You know when I sit down and when I rise up.</i> God is not reading the version you selected this morning. He is reading you \u2014 the specific, irreducible, un-adapted you he knew before the foundation of the world. Let that land before you enter the next room."),
    ("The named disagreement", "Choose one relationship in which you have been consistently adaptive and identify one honest disagreement you have never expressed. Not a confrontation \u2014 simply a difference, spoken in a non-crisis moment: <i>I actually see that differently than you do.</i> The Adapter was built on the assumption that differences are dangerous. The practice of naming one, gently and specifically, begins to collect evidence that the assumption was wrong."),
]

ATT_TOOLS = [
    ("Name the wound before the versions assemble", "Within twenty-four hours of the control trigger firing, tell one trusted person one sentence: <i>Something happened today and I was hurt \u2014 not one of my versions, but me.</i> The Adapter's Attorney assembles a multi-witness brief because the wound goes underground and each version processes it alone. Speaking in the first person, before the versions have time to organize, disrupts the assembly."),
    ("The one-voice rule", "When you must speak to the person who wounded you, discipline yourself to one voice \u2014 not the colleague-voice, the calm-voice, or the voice most likely to be received, but simply yours: <i>When that happened, I felt dismissed, and I need you to know that.</i> One wound. One sentence. One speaker. The Adapter's Attorney derives its power from multiplying voices; this rule begins to interrupt that multiplication."),
    ("The self-check before the brief", "When you feel the Attorney beginning to assemble, stop and ask: <i>How many versions of me are about to speak?</i> If the answer is more than one, you are not bringing a wound. You are conducting a prosecution. The prosecution may contain accurate evidence. It will not produce what you are actually after. The wound, expressed by one person in one voice, has a chance at repair. The brief, delivered by multiple witnesses, has almost none."),
    ("The advocate prayer", "When the Attorney is loudest \u2014 when the versions are lining up and the brief is feeling urgently necessary \u2014 pray these words slowly: <i>Lord Jesus, you are my Advocate. You know every version of me. You saw every wound from every angle. I do not need to call every witness. I receive the verdict you have already spoken over the me you named before the world began.</i> Say it three times. The third time, the courtroom usually begins to quiet."),
    ("Write the brief and receive the name", "If the multi-witness brief will not leave you alone, write it out \u2014 every version, every voice, every exhibit. Then, at the bottom of the last page, write: <i>Beneath all of these versions, there is one person, chosen in Christ before the foundation of the world. The One who chose that person has already spoken the verdict.</i> Tear the brief; keep the sentence. This is the practice of locating the self below the versions."),
    ("The repair conversation", "The Adapter's Attorney tends to skip the step between wound and verdict. That step is repair: a simple, immediate naming of the wound by one person to one other person, without assembled versions. It requires saying <i>that hurt</i> in the moment it hurts, before the mechanism selects the most appropriate response. This is the Adapter's hardest practice and its most healing one."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Adapter in me, and you are not disoriented by him. You have seen every version, attended every room, watched every calibration. You know which ones were gifts and which ones were survival. Thank you that he kept me connected. Thank you that the attunement he gave me has been genuinely useful, in real relationships, to real people. He has not been wrong about everything.",
    "But Father, I am tired of not knowing which version is me. I am tired of walking out of conversations and not being entirely sure what I actually believe. I am tired of carrying a self that is assembled from what the rooms reflected back, and not knowing what is underneath when the rooms go quiet. Teach me that you have already named the underneath. That Ephesians 1:4 is speaking of me, specifically: chosen in Christ before the foundation of the world, before any room existed to require a version. That 1 John 3:1 is speaking of me, not contingently but absolutely: called a child of God by the Father who bestowed that calling before I could earn it or lose it. Let those words reach the place where the calibration runs.",
    "Lord Jesus, when the Attorney assembles in me \u2014 when every version of me that has been hurt lines up to testify and the closing argument threatens to undo years of relationship in a single hour \u2014 would you remind me that you are my Advocate, and that you have already presented the only brief that finally counts? That you know every version of me and have loved the one underneath them all? That I do not need the court to vindicate the right version, because you have already spoken the verdict over the self that was real before the versions started?",
    "Holy Spirit, where I am calibrating, give me stillness. Where I am performing a version, give me the courage to be simply present. Where the Attorney is rising with many voices, give me one voice, speaking one wound, trusting one Advocate. Teach me the difference between the gift of attunement and the compulsion of adaptation \u2014 and help me, one room at a time, to give from the former rather than fleeing through the latter.",
    "In the name of the One who walked into every room as himself, who read every person in his presence and loved them without adjusting who he was to keep them close \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Adapter and the Attorney have been with you for a long time, and one careful reading will not retire them. What follows is a short list of next steps \u2014 some immediate, some longer-term \u2014 for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different lines will land. The Adapter will resist a second reading \u2014 he prefers to adjust to new information once and then move on to the next room. Read it again anyway. The section that felt least relevant today may be the most necessary one in a month."),
    ("Take one tool, not six.", "Choose a single practice from Section 7 and try it for two weeks before adding another. The tools are postures, not a program. One posture, held for long enough, begins to give the self below the versions a chance to breathe."),
    ("Tell one person what you found.", "Not the whole document. One sentence: <i>I learned that my mechanism is the Adapter, and my breakdown is the Attorney, and I have been borrowing my sense of self from every room I have ever entered.</i> The Adapter's pattern lives in the social performance. Speaking it to a trusted witness in your own voice is the first act of living outside the performance."),
    ("Sit with one Psalm of identity.", "Psalm 139 for a week, aloud, one section per day. Verse 1: <i>You have searched me and known me.</i> Verse 13: <i>For you formed my inward parts.</i> Verse 16: <i>In your book were written, every one of them, the days that were formed for me, when as yet there was none of them.</i> The Adapter needs, more than almost any other mechanism, the practice of being addressed by God as a singular, known, irreplaceable person. The Psalms do this. Let them."),
    ("Read further on the self you did not build.", "Tim Keller, <i>Counterfeit Gods: The Empty Promises of Money, Sex, and Power, and the Only Hope That Matters</i> \u2014 especially his treatment of identity as something received rather than constructed. C. S. Lewis, <i>The Weight of Glory</i> \u2014 read the essay by that title in full; his treatment of the longing to be known and addressed by name is the most precise pastoral address to what the Adapter most needs. Augustine, <i>Confessions</i>, Book I \u2014 especially the first three chapters; Augustine's restlessness is your restlessness, and his discovery is available to you."),
    ("If you are stuck, ask for help.", "There are seasons when the Adapter and the Attorney are too entrenched to dislodge alone. A wise pastor, a Christian counselor, a trusted friend who has earned the right to your un-adapted self \u2014 these are not signs of failure. For the Adapter specifically, asking for help without managing the other person's experience of the asking is one of the most countercultural and most healing things on this list."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom by a Father "
    "who chose you before the foundation of the world \u2014 before any room existed to require a version, "
    "before any feedback was available to borrow. The self underneath the adaptations is not missing. "
    "It is named. It is kept. It is beloved. "
    "Go gently with yourself. The One who began the good work in you will be the one who finishes it."
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
        [Paragraph("WAS I FREE HERE?", header_style), Paragraph("what your nervous system concluded", sub_style)],
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
    """Generate the Adapter+Attorney walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='ADPT', primary_breakdown='ATTY',
    primary_trigger='CTRL', core_question='FREE'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor's Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR'S WALKTHROUGH",
        cover_right_label="ADAPTER  \u00b7  ATTORNEY",
        title="Take 139 Walkthrough \u2014 Adapter + Attorney",
    )

    story = []

    # \u2500\u2500 COVER \u2500\u2500
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor's<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the way<br/>you have learned to keep yourself safe.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph("The Adapter \u00a0\u00b7\u00a0 The Attorney", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Control \u00a0\u00b7\u00a0 Core Question: Am I free?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cThou hast made us for thyself, and our heart is restless<br/>"
        "until it rests in thee.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Augustine, <i>Confessions</i>",
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
                   "Control.",
                   "The moment your individuality is overridden, and what your soul makes of it.")
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
                   "Am I free?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "What Scripture says about freedom.",
                   "A freedom already given, and the honest cost of receiving it.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "Where was I actually constrained? Where was my soul free?")
    story.append(Paragraph(
        "Use the table below. In the first column, name a recent event in which the "
        "control trigger fired. In the second, write what your nervous system concluded: "
        "<i>was I free here?</i> In the third, answer the deeper question: "
        "<i>was the part of me that finally matters \u2014 my soul, my standing before "
        "God \u2014 at any point in danger?</i>",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table())
    story.append(PageBreak())

    # \u2500\u2500 SECTION 4: Mechanism \u2500\u2500
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
        "AdptLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
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

    # \u2500\u2500 SECTION 5: Breakdown \u2500\u2500
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Attorney.",
                   "The multi-witness courtroom. Every version of you, testifying at once.")
    for p in ATT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ATT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The self beneath the versions.",
                   "Named before any room existed. The gospel's answer to the borrowed self.")
    for p in ATT_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Step out of the courtroom.",
                   "Three questions to sit with before you turn the page.")
    for prompt in ATT_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same need, in two directions.",
                   "The Adapter and the Attorney are not two problems. They are one loop.")
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
                   "Six practices for the time before the alarm fires.")
    for name, desc in ADPT_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Attorney assembles the multi-witness brief.",
                   "Six practices for the moment the versions begin to line up.")
    for name, desc in ATT_TOOLS:
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


# \u2500\u2500 STANDALONE TEST \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "ADPT"
        primary_breakdown = "ATTY"
        primary_trigger = "CTRL"
        core_question = "FREE"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "adapter_attorney_test.pdf")
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

    print(f"DONE: adapter_attorney.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
