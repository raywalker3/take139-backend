"""Personal Walkthrough — Adapter + Flood.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Control trigger, "Am I free?" core question.
~25 pages, 9 sections.

Walkthrough 27 of 36.

Calibration anchor: The Adapter+Flood is uniquely confusing because what floods
out is *multiple selves at once* — anger from one version, grief from another,
complaint from a third, all in a single conversation. The spouse says "I don't
know who is talking to me right now" and they are reporting accurately.

KEY CONTRAST WITH OTHER FLOOD PROFILES:
  - Architect+Flood: planner's dam bursting.
  - Island+Flood: first cost-signal of long silence.
  - Ambassador+Flood: the ledger speaking.
  - Vault+Flood: the file cabinet falling open in an earthquake.
  - Adapter+Flood: *involuntary integration* of selves kept artificially separate
    for years. Multiple personas arrive together with no clear conductor. Messy;
    also a kind of mercy. Psalm 42 frames the pastoral move (soul speaking to
    itself). Augustine's "vast palaces" of memory. Bonhoeffer on the first
    honest self-assessment outside the service of the room.

CRITICAL THEOLOGICAL MOVE (Section Five):
The Flood is not the Adapter's failure of self-control. It is the involuntary
integration of selves that have been kept artificially separated. It is messy;
it is also a kind of mercy, because what was hidden is being brought into one
room. The unique pastoral move: name that for the Adapter, the Flood is often
the first time they think honestly of themselves at all.
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
    "Before you read any further, I want to do something for you that a good counselor does in the opening minutes of a first session. I want to lower the lights and slow the pace, because what you are about to look at is not a list of your failures, not a verdict on the way you have moved through the people you love, and not a clinical inventory of a personality type. It is a patient conversation about the way your soul has learned to keep itself safe — and in your case, the learning was so natural and so effective, and so genuinely useful to the people around you, that you may never have recognized it as a strategy at all.",
    "You are an Adapter. Not because you are false or shallow — the Adapter is, in many ways, one of the most genuinely present people in any room. You are an Adapter because something early in your experience taught you that the surest path to belonging was not to arrive with a fixed self and wait to see if it was wanted, but to read the room carefully and become what the room could receive. You have spent years moving between people the way a skilled musician moves between keys — the same instrument, a different timbre depending on what the piece required. These are real gifts. But gifts can accumulate a cost when they are the only currency you have for belonging. And the particular cost the Adapter carries is this: when the pressure grows large enough, what floods out is not one person's pain but several versions of one person's pain — all at once, with no clear conductor. This is what this walkthrough is about, and we are going to name it carefully.",
    "We will walk through your trigger, the moment your nervous system says <i>something is wrong here</i>. We will listen to the question underneath that moment, the one that has probably been with you since you were very small. We will name the strategy you have built in response, and we will look at the place that strategy collapses. Only then will we put tools in your hands.",
    "If you were sitting across from me, I would say this before we went further. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who has seen every version of you — not the versions you have offered to each room, but the person underneath them — and who named that person beloved before any room existed to require a performance; a Son who walked into every room as himself, undivided, and who calls you by a name he did not derive from anyone's feedback; and a Spirit who is, at this very moment, more committed to your integration than you are.",
    "So read slowly. Argue with what does not fit. Stay with what does. When something catches in your throat, pray — because that catch is usually the Lord saying, <i>look here, with me.</i> The goal of this walkthrough is a slightly freer life, lived from a self that does not need to be reconstructed fresh in every room you enter. Take your time. The chapter you are about to read about yourself has been a long time in the writing.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it is genuinely difficult to describe to people who do not share your wiring, because from the outside it looks like almost nothing. Someone tells you what to do in a tone that does not ask. A decision that involves you is made without your input. A spouse sets a rule — a small one, possibly even a reasonable one — and something in you goes quiet in a way that has nothing to do with whether you agree with the rule. Someone uses the word <i>should</i> in a particular way, directed at you, and you feel something tighten before you have finished hearing the sentence.",
    "This is not stubbornness, though it can look like that from the outside. It is not willful pride, though pride may attach itself quickly. What fires inside you in those three seconds is something older and more frightening than either. The signal is not <i>that is unfair.</i> The signal is closer to <i>something about who I am is being overridden, and I am not certain there is enough of me left to be overridden without disappearing.</i>",
    "This is your trigger. The word we use for it is <b>control</b>, but the word is doing more work than it appears to do. For most people, a control trigger is primarily about autonomy — the desire not to be told what to do. For the Adapter, it is something more subtle and more threatening. The question that rises underneath the trigger is not merely <i>will I be allowed to make my own choices?</i> It is: <i>Am I free? Is there a me here that is not simply a mirror of what you need from me? Will my individuality survive this relationship?</i>",
    "C. S. Lewis, in <i>The Weight of Glory</i>, observed that there is something in every human soul that longs not for the applause of a crowd but to hear a word spoken by the highest authority — a word that addresses not a performance but a person. The Adapter has been performing, and the performances have been excellent, and the people who have received them have often been genuinely grateful. But underneath all of that gratitude, a question has gone unanswered: <i>if I stopped performing — if there were no room to read, no version to select — would there be someone here? And would that person be loved?</i>",
    "<b>Your sensitivity to control is not random.</b> It is the residue of something learned early, in a household where having your own preferences — your own particular interior life — was costly in some way. Perhaps love in your family was conditional on conformity: warmth came when you were what was needed, and retreated when you were not. Perhaps the emotional climate changed unpredictably and reading the room became survival before it became style. Perhaps there was enmeshment — a family system so tightly woven that having a self that differed from the family's preferred self felt threatening to the whole unit. Whatever the specific history, the lesson lodged clearly: <i>the safest thing is to be whatever the room can love.</i> And over time, the Adapter was born — not as a deceiver, but as a genuinely gifted reader of human beings who learned to give each person the version of you they most needed to receive.",
    "Before we go further, I want you to sit with two questions in writing. Not in your head — the Adapter's head will reframe the question to fit the moment. Your hand will be more honest.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week, that the control trigger fired. What happened, in two sentences? You are not looking for a dramatic event — often the trigger fires in a small moment of being told how things will be, or in the quiet sense that a version of you is being required that you did not choose.",
    "What was the size of the actual event, and what was the size of the response inside you? If something in you went still or quiet in a way that surprised you — if the internal reaction was larger than the occasion — you have just located the trigger. Write the gap honestly.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding. The Adapter has been guarding this one for a very long time, and has been guarding it so skillfully — by staying perpetually useful, perpetually present, perpetually the version each room needed — that you may never have allowed yourself to state it plainly.",
    "Yours is this: <b>Am I free?</b>",
    "It is not simply the question of whether you are permitted to make your own choices, though that concern is real. It is something more personal and more frightening than external permission. It is the question of a soul that has spent so much time reading rooms and becoming what those rooms needed that it now wonders whether there is a self underneath the adaptations — a self that would survive if the adaptations were removed. <i>Am I free to be myself? And if I were — truly, without adjustment, without the version-selection — is there a self to be free?</i>",
    "Most adults have arranged their lives so that this question does not need to be asked directly. For the Adapter, it comes in through the side door every time someone tries to define who you are supposed to be in their presence. The trigger is not the rule. The trigger is the implication behind the rule: <i>there is a version of you that is more convenient to me, and I would like that one.</i> And your soul, which has been selecting versions of itself for years, does not know whether to comply or revolt — because it is not entirely sure it has a version that is not already a selection.",
]

QUESTION_BODY_P2 = [
    "There is a reason theologians from the Reformation forward have insisted that freedom is not merely a political category but a theological one. The freedom that matters most is not the freedom to do whatever you wish. It is freedom from the tyranny of being anyone's source of meaning \u2014 the freedom of a soul that does not have to earn its standing in every room it enters. Paul names it in Romans 6:6\u20137: <i>We know that our old self was crucified with him in order that the body of sin might be brought to nothing, so that we would no longer be enslaved to sin. For one who has died has been set free from sin.</i> The Adapter's captivity is rarely to obvious sin. It is to the captivity of a self that cannot be still, that must keep reading and adjusting and becoming, because the alternative \u2014 being simply who one is \u2014 feels exposed in a way that is intolerable. Paul names this too: <i>you did not receive the spirit of slavery to fall back into fear.</i> (Romans 8:15)",
    "The gospel anchor for the question you carry is this: you are a <i>New Creation</i> \u2014 the old identity in Adam, with its captivity and its exhausting responsiveness to whoever was in the room, has been put to death. <i>Therefore, if anyone is in Christ, he is a new creation. The old has passed away; behold, the new has come.</i> (2 Corinthians 5:17) The attunement is a genuine gift, and the gospel does not retire gifts. It simply announces that the attunement is now free to be what it was always designed to be: love that flows from abundance rather than adaptation that flows from fear.",
]

QUESTION_BODY_P3 = [
    "But here is where pastoral honesty requires a careful word. The Psalms name this struggle in its full weight. Psalm 31:8: <i>you have not delivered me into the hand of the enemy; you have set my feet in a broad place.</i> The broad place David is describing is not a wide field. It is the freedom of a soul whose standing does not depend on performing correctly, on reading the room, on becoming what the moment requires. And yet here is the honest rub: being told that you are free, in Christ, often does not <i>feel</i> like freedom to the Adapter. It feels more like a truth the head holds and the nervous system does not yet inhabit.",
    "The freedom the Adapter has been protecting so fiercely is already fully yours in Christ. John 8:36: <i>if the Son sets you free, you will be free indeed.</i> Not free pending compliance. Not free conditional on the right performance in today's room. Free indeed — which is to say, free even when the room is asking for something else entirely.",
    "The work this section invites is not more self-examination — the Adapter has more introspection than almost any other mechanism. The work is the slow practice of receiving freedom as a gift already given, rather than fighting for it as a territory that must be defended with each new adaptation. Before we close this section, use the table below. Not to analyze, but to observe: where did the control trigger fire this week, and where was my soul's freedom actually in danger?",
]

ADPT_BODY_P1 = [
    "You have built something. It did not announce itself as a strategy when it was forming — it formed the way a river forms, not by decision but by the path of least resistance through a landscape that rewarded certain movements and discouraged others. One day you looked up and the river was already there, running through every relationship you had, shaping the way you moved through every room. Throughout this walkthrough we are going to call it <b>the Adapter</b>, and before we name what it costs you, the Adapter deserves to be properly introduced.",
    "The Adapter is not the Ambassador. This distinction matters, and the two mechanisms look so similar from the outside that they are worth pausing over carefully. The Ambassador takes care of people by serving them — bringing warmth, noticing who is struggling, being the one who manages the emotional temperature of the room. The Ambassador is the same person across all contexts, serving differently but remaining recognizably herself. The Adapter does something different: the Adapter takes care of people by <i>becoming what they need to see.</i> Not by performing a false self — the Adapter is genuinely present in every version. But the version itself shifts. You can be utterly authentic in five different ways with five different people in one day, and feel no contradiction in any of them, because for the Adapter, authenticity has never been a fixed self presenting itself consistently; it has been the full entering-in to whatever the relationship most needed.",
    "The Ambassador knows she is the same person serving differently across contexts. The Adapter may genuinely not know that. And this — the gift and the cost in a single sentence — is precisely what this section is about. There is a great deal in Scripture that commends this kind of relational attunement. Proverbs 25:11 says: <i>A word fitly spoken is like apples of gold in a setting of silver.</i> Paul himself wrote: <i>I have become all things to all people, that by all means I might save some.</i> (1 Corinthians 9:22) The Adapter lives this verse before having ever read it. It is a genuine fluency in the emotional languages of the people around you, and the world is genuinely better when people like you are in it.",
]

ADPT_BODY_P2 = [
    "But there is a cost, and the cost is specific to this mechanism. The Adapter's most characteristic experience is this: you can be fully present in a conversation — genuinely moved, genuinely engaged, genuinely yourself — and walk away an hour later unable to tell, with confidence, which of your preferences, which of your opinions, which of your actual interior responses were yours and which were calibrated to the person you were with. The calibration happens below the level of conscious decision. It is not dishonesty. But it produces, over years, a specific kind of interior ambiguity about what you actually want, what you actually believe, what you would actually choose if no one were in the room to read.",
    "The taxonomy of this kind of mechanism suggests several histories that tend to produce the Adapter, and you will likely recognize yourself in at least one. Perhaps you grew up in a household where the emotional climate changed frequently and reading the room was not a preference but a survival skill — the way to stay safe was to become what the safest version of the moment needed. Perhaps there was enmeshment, a family system where having a self that differed from the family's preferred self felt dangerous, and you learned to offer your self rather than insisting on it. Perhaps you discovered early that being exactly what someone needed was the most intoxicating experience available — the look of recognition on a person's face when you gave them the version of you they had not known they were looking for. Whatever the specific history, the deepest characteristic of the Adapter is not the adaptation itself. It is the genuine difficulty of answering, quietly, the question: <i>Who are you when no one is watching?</i>",
    "<b>The Adapter is not your enemy.</b> He is a younger version of you who learned, in some real and specific circumstance, that the self which could flex was safer than the self which held its ground. He deserves your respect, not your contempt. He kept you connected. He gave you gifts — empathy, attunement, a rare fluency in human emotional languages — that are genuinely valuable and that the people in your life have genuinely received. But he has been working overtime on a project that was finished years ago. The room that first required him is long gone. And the question he was built to prevent — <i>will you be acceptable if you are simply yourself?</i> — is one that he is not, and has never been, equipped to answer.",
]

ADPT_BODY_P3 = [
    "What does it look like to begin loosening the Adapter's grip? Not eliminating the gift — the attunement is real and should not be retired. But beginning, slowly, to distinguish between the attunement that flows from love and the adaptation that flows from fear. These two things feel almost identical from the inside. The difference is in the root: the attunement that flows from love can stop when stopping is right; the adaptation that flows from fear cannot stop without triggering the alarm.",
    "It begins with sitting still long enough to notice what you actually want. Not what the room wants from you, not what would serve the other person best, not which version of your preference would land most smoothly — but what do you actually want? The Adapter often discovers, when sitting with this question for the first time without a social context to calibrate against, that the answer is genuinely unclear. This is not a failure of self-knowledge. It is the honest recognition of a mechanism that has been so faithfully at work that the self underneath it has not had much occasion to speak.",
    "The letter below is written from the Adapter, in his own voice, to you. He is not a villain. He is a craftsman who has mistaken his tool for his identity. He is genuinely confused, and genuinely faithful, and genuinely tired. Read it slowly — because he has something to say that he has never been asked to put into words.",
]

ADPT_LETTER_INSTRUCTION = [
    "The letter below is written from the Adapter, in his own voice, directly to you. Read it slowly before you respond to the three prompts that follow.",
    "Dear [your name],",
    "I want to tell you something I have never been asked to say, because I have never been still long enough to say it. Stillness is the problem. I do not do well with stillness. In stillness there is no room to read, no feedback to receive, no version of you to present. There is only \u2014 I am not sure what. And that not-knowing is the thing I have been moving away from, more or less continuously, for as long as either of us can remember.",
    "I learned early that I could be loved \u2014 not by being fixed, not by holding my ground, but by reading what someone needed and becoming it. The love came immediately, without waiting. It required attention, and I had an inexhaustible supply. I kept you in every room you were ever in. I kept the relationships going. You have been loved. A great deal. And I worked hard for that.",
    "What I did not know how to do is give you a self that was yours when no one was there. I kept you present in every room. I did not know how to keep you present in the room with no one in it. I think I did not know there was supposed to be a you there too.",
    "I am telling you this because something is beginning to break. You have been containing things \u2014 the grief of the version who became your spouse's ideal, the frustration of the version who stayed calm through too many difficult seasons, the longing of the version who laughed when something was actually hurting her. I kept those things separate because I was afraid that bringing them into the same room would be the end of everything. I may have been wrong. And now they are all in the room together, and neither of us knows quite what to do with that.",
    "The Adapter",
]

ADPT_LETTER_PROMPTS = [
    "What part of the Adapter's letter surprised you? Not the part you expected — the part you were not quite ready for.",
    "The Adapter says he kept you present in every room but could not keep you present when no one was there. When was the last time you sat quietly, without calibrating to anyone, and felt genuinely at home in yourself? Describe that moment — or, with equal honesty, describe the absence of it.",
    "The Adapter says he kept things separate because he was afraid bringing them together would be the end of everything. What are the versions of you that have been kept apart? Name two or three by their characteristic role — and write one thing that each of them has been silently holding.",
]

FLOOD_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Adapter, the breaking has a shape that is, among all the versions of this breakdown, the most disorienting — both for the Adapter and for the person on the other side. The breakdown is called <b>the Flood</b>, and the Adapter's version of it is unlike any other version that carries this name.",
    "The Architect's Flood is the planner's dam bursting — months of rigidly maintained composure giving way at once, a single overpressured system. The Island's Flood is the first signal that the long silence had a cost — a small opening, unintended, honest. The Ambassador's Flood is the ledger finally speaking — a lifetime of invisible giving coming out in a single inventory. The Vault's Flood is the file cabinet falling open in an earthquake — documents the spouse never knew existed suddenly on the floor. The Adapter's Flood is something none of these, and it is worth naming with precision, because if you have experienced it, you already know how strange it was.",
    "What floods out, in the Adapter's Flood, is not one person's pain. It is several versions of one person's pain — all at once, in a single conversation, in a way that disorients both the Adapter and the listener. The anger belongs to one version of you. The grief belongs to another. The complaint — <i>you never once noticed what it cost me to stay calm through that season</i> — belongs to a third. The plea — <i>I just want you to see me, not the version I was giving you</i> — belongs to a fourth. And they arrive together, without a conductor, each speaking in its own register, each carrying its own history, each using language the listener did not know this relationship contained.",
    "The spouse will say afterward: <i>I did not know who was talking to me.</i> They will be reporting accurately. Not because you are unstable or deceptive — but because the Adapter has been storing unspoken feelings in the persona that was performing at the time, and now several of those personas are speaking at once with no clear integration. The listener is discovering, in one hour, that the person they thought they knew had been living several interior lives simultaneously.",
]

FLOOD_BODY_P2 = [
    "Here is what this looks like from the inside. You have been containing things — perhaps for months, perhaps for years. Each version of you that has been required in this relationship has been faithful to its role. The version that stayed calm when you needed to stay calm. The version that was funny when levity was needed. The version that adjusted its preferences so that the shared life could run smoothly. None of these versions was dishonest. Each one was real. But each one was also, in a very literal sense, a separate container — and each container has been quietly filling.",
    "Then something lands. A wound large enough that the usual adjustment cannot absorb it. A moment in which the control trigger fires so hard that the Adapter cannot find the right version to produce, and the mechanism stalls. And what emerges is not the clean, single-voiced grievance that a relationship can receive and respond to. What emerges is the accumulated contents of every container at once — tears from one version, accusations from another, grief from a third, a kind of wild insistence on being seen that does not fully know what it is insisting on.",
    "The psalmist David wrote something in Psalm 42 that names what is happening in the Adapter's Flood with a precision I find remarkable: <i>Why are you cast down, O my soul, and why are you in turmoil within me?</i> This is the psalmist speaking to his own soul as if it were another person. The psalmist who, in the same poem, both grieves and hopes, both despairs and remembers, both cries out in thirst and confesses that his hope is in God. He does not resolve the contradiction. He holds both in the same breath and speaks them to someone — even if that someone is himself. The Adapter's Flood is a version of this — a soul speaking to itself and to others in more than one register at once, and the registers are not tidy.",
    "<b>What the Adapter most needs to hear in this moment is not that the Flood was a failure of self-control.</b> It was not a failure. It was something closer to what Augustine described in the tenth book of his <i>Confessions</i> when he wrote of the \"vast palaces\" of memory — those cavernous interior rooms where different experiences, different images, different selves are stored, and which cannot always be kept in their separate apartments. Augustine was not dismayed by this multiplicity. He was astonished by it — and in that astonishment he found God. The Adapter's Flood is the first moment those apartments have emptied into the same room.",
]

FLOOD_BODY_P3 = [
    "The unique pastoral move for the Adapter is this: the Flood is not a loss of control. It is the <i>involuntary integration</i> of selves that have been kept artificially separated for years. And it is messy. And it is also — listen carefully — a kind of mercy. Because what was hidden in those separate apartments is being brought, for the first time, into one room. That is not destruction. That is the beginning of wholeness.",
    "Dietrich Bonhoeffer wrote in <i>Life Together</i>: <i>He who would learn to serve must first learn to think little of himself.</i> I want to use that sentence in an unusual direction. For most people, it is a call to humility about their importance. For the Adapter, the Flood is often the first time in years that they think about themselves at all — not in service of the room, not calibrated to what is needed, but honestly and urgently, with all the versions present. The Flood is, in this sense, the Adapter's first attempt at honest self-regard. It is clumsy. It is also necessary. The fact that it is messy does not mean it is wrong. It means it is real.",
    "What the Flood cannot do, on its own, is produce the integration it is reaching for. The versions arriving together are looking for someone to receive them — all of them, not the one the listener preferred. They want to be held as a whole. But flooding, by itself, does not accomplish this. It does the work of breaking the compartmentalization. The work of rebuilding, carefully, around one self rather than many — that is the work that follows. And it requires the gospel's answer: not <i>find your true self</i>, but <i>receive your true self from the One who named it before any version started</i>.",
]

FLOOD_PROMPTS = [
    "Name the last time the Flood came. You do not need to describe it in detail — describe the shape of it: how many different voices were in the room? Which version of you was most present? Which was the most unexpected? Which one had been silent the longest?",
    "After the Flood, what remained? What did you feel in the quiet that followed — relief, shame, disorientation, something else? Write it honestly. The Flood has already opened something; this question is asking you to stay with the open rather than closing it immediately.",
]

TWO_TOG_BODY = [
    "Now we place them side by side, because the Adapter and the Flood are not two separate events. They are the same interior life, moving in two directions. The Adapter moves outward toward the rooms, reading and adjusting and becoming what each room requires. The Flood moves inward — or rather, erupts outward after the inward pressure has reached the point where separation is no longer possible.",
    "<b>The Adapter is what your need does when it has time and space.</b> The Flood is what your need does when the time runs out and the containers can no longer be kept separate. The Adapter constructs versions so the wound can be managed; the Flood presents every version and every wound simultaneously when the construction collapses. Together they form a loop, and the loop is powered by the same question: <i>Am I free? Is there a me here that is not simply a mirror of what you need?</i>",
    "The pattern, in slow motion, looks like this. <b>(1)</b> The Adapter moves through the world reading rooms and becoming what the rooms need. <b>(2)</b> A moment arrives in which the control trigger fires: someone attempts to define who you are supposed to be, or fails to see what it has cost you to be who you have been. <b>(3)</b> The body says, <i>something about who I am is being overridden.</i> <b>(4)</b> The core question wakes up: <i>Am I free?</i> <b>(5)</b> The Adapter tries to produce a version that will resolve the tension. <b>(6)</b> It does not work. The wound stays open. The containers keep filling. <b>(7)</b> The containers can no longer be kept separate, and the Flood arrives — multiple versions, multiple wounds, multiple voices in a single conversation, with no clear conductor. <b>(8)</b> The listener says, <i>I don't know who I am talking to right now,</i> and they are telling the truth. <b>(9)</b> The question is alive again — but for the first time, it has been asked aloud. That is not nothing.",
    "What breaks the loop is not a more careful management of the versions, and it is not a more disciplined suppression of the Flood. It is a different source for the self altogether — a self that does not need to be assembled from the rooms' reflections, because it has already been named by the One who made it. Below is your sequence. Fill in the blanks. When you are done, read it aloud. Both the Adapter and the Flood lose some of their grip when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as control "
    "\u2014 as a requirement to be a particular version of myself I did not choose \u2014 "
    "and the old question wakes up: <i>am I free?</i> My first move is to "
    "____________________, because the Adapter in me believes that if I can "
    "____________________, the room will hold and the wound will not need to speak. "
    "When that does not work, the versions I have been keeping separate begin to arrive "
    "at once, and the Flood brings them all into the room together, each saying "
    "____________________. "
    "What I am actually after, underneath all of it, is the verdict "
    "____________________ \u2014 a verdict Christ has already spoken over "
    "the self he named before any version started, in ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of tools — each one concrete enough to carry, honest enough to use. None of them will dissolve the Adapter's pattern in a single application. All of them, practiced over months, will loosen the grip of the loop you just named.",
    "I have divided them into two sets: tools for when the Adapter is overworking its calibration — when the room-reading has tipped from gift into compulsion — and tools for when the Flood comes. The Adapter's tools come first, because the most important work is upstream: a self that has more occasions to speak, quietly, in the ordinary seasons, will have less need to speak in a torrent during the extraordinary ones.",
]

ADPT_TOOLS = [
    ("The preference question", "Once a day, before the first social interaction, ask yourself one question without reference to anyone else in the room: <i>What do I want today?</i> Not what would be best, not what version of me would be most useful — what do I actually want? The Adapter will find this disorienting at first. That disorientation is not a failure. It is the honest recognition that the mechanism has been running. A small answer is sufficient. The practice is not the answer; the practice is the asking."),
    ("The unedited opinion", "Once a week, in a low-stakes conversation, offer an opinion before you have checked it against what the other person seems to need. Not confrontational — simply an un-adjusted one. Notice what happens in your body when you do this. Notice whether the relationship survives it. It almost certainly will. The survival is data the Adapter needs: you can be un-adapted and remain loved."),
    ("Name the version", "When you catch the Adapter running — when you notice yourself adjusting, selecting, softening a preference for the room — say quietly: <i>Lord, I am doing it again. The version I am about to present is not the whole of who you named. Help me be present as the person you chose.</i> Simply naming it to God disrupts the automaticity. Over months, the naming creates a gap between stimulus and response that the Adapter has never had."),
    ("The solitude practice", "Once a week, spend thirty minutes alone without any input — no phone, no music, no reading. Sit with the question: <i>Who is here?</i> The Adapter, having nothing to calibrate to, will initially feel unmoored. That feeling is not emptiness. It is the legitimate discomfort of a self not often allowed to be simply present without a room to serve. Over months, this practice begins to give the self below the versions a chance to speak."),
    ("Psalm 139 as morning prayer", "When the Adapter's calibration tips into anxiety — when you feel the compulsive need to check, adjust, and become — open to Psalm 139 and read the first four verses aloud: <i>O Lord, you have searched me and known me. You know when I sit down and when I rise up.</i> God is not reading the version you selected this morning. He is reading the specific, irreducible, un-adapted you he knew before the foundation of the world. Let that land before you enter the next room."),
]

FLOOD_TOOLS = [
    ("Name the pressure before it breaks", "The Flood rarely arrives without warning; the Adapter simply does not have a practice of reading internal pressure until it is very high. Once a week, use this question: <i>What have I been holding this week that I have not said to anyone?</i> Write one sentence for each thing. The point is not to release everything immediately. It is to know what is in the containers before they overfill. This practice, done consistently, reduces the Flood's intensity without eliminating its honesty."),
    ("The one-voice rule", "When you must speak the wound, discipline yourself to one voice — not the colleague-voice or the calm-voice or the voice most likely to be received, but simply yours: <i>When that happened, something in me was hurt, and I need you to know that.</i> One wound. One sentence. One speaker. The Flood derives its power from the multiplication of voices. This rule asks the other voices to wait outside while one speaks. They will have their turn; they will be more likely to be received if they do not all arrive together."),
    ("Stay open after the Flood", "The Adapter's most powerful temptation in the aftermath of the Flood is to close immediately — to revert to a functional version, smooth over what came out, manage the other person's experience of the moment. Resist this. The Flood has opened something. Stay with the open for at least twenty-four hours before the Adapter begins its repair work. Ask: <i>What was the thing underneath all the voices? Name it in one sentence.</i>"),
    ("The psalm that speaks to itself", "Psalm 42 is the Adapter's psalm for the aftermath of the Flood. The psalmist speaks to his own soul: <i>Why are you cast down, O my soul, and why are you in turmoil within me? Hope in God; for I shall again praise him, my salvation and my God.</i> He does not resolve the turmoil before he speaks it. He speaks it, then speaks the hope, and both are true at once. Pray this psalm slowly after a Flood. Let the soul speak to itself as a whole, not as separate apartments."),
    ("The repair conversation", "The Flood is not the repair. It is the opening. Within twenty-four to forty-eight hours, when the intensity has settled, name one thing — not everything, one thing — that the Flood was reaching for: <i>What I most needed you to know is this.</i> One sentence. The repair conversation does not repeat the Flood. It names, quietly and in one voice, the thing underneath all the voices that the Flood was trying to say."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Adapter in me, and you are not confused by him. You have seen every version — the one who stayed calm when calm was needed, the one who became exactly what each room required, the one who read faces and adjusted and calibrated without pause. You know which of those versions were gifts, and which were survival. Thank you that he kept me connected. Thank you that the attunement he gave me has been genuinely useful, in real relationships, to real people who needed it. And thank you that you have always known the person underneath the versions — that you have seen every apartment in the vast palace of my interior, as Augustine said, and that none of what you found there changed the name you gave me.",
    "Lord Jesus, when the versions in me begin to speak at once — when the Flood gathers and the separate selves all try to get into the same room — remind me that you are my Advocate, and that you know every one of them. That you have seen every wound from every angle. That I do not need every voice to speak in order to be fully known, because the One who knows me fully has already received me wholly and called me his own. Give me one voice. Give me the courage to speak the wound in my own name, trusting that Ephesians 1:4 is speaking of me — chosen in Christ before the foundation of the world, before any room existed to require a version. And where the Flood has already come, give me the grace to stay open in the aftermath long enough to hear what it was actually saying.",
    "Holy Spirit, where I am calibrating, give me stillness. Where I am selecting a version, give me the courage to be simply present. Teach me, one room at a time, to give from love's abundance rather than from fear's adaptation.",
    "In the name of the One who walked into every room as himself, who read every person in his presence and loved them without adjusting who he was to keep them close \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Adapter and the Flood have been with you for a long time, and one careful reading will not retire them. What follows is a short list of next steps — some immediate, some longer-term — for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different lines will land. The Adapter will resist a second reading — he prefers to adjust to new information once and move on to the next room. Read it again anyway. The section that felt least relevant today is often the most necessary one in thirty days."),
    ("Take one tool, not five.", "Choose a single practice from Section 7 and try it for two weeks before adding another. The preference question or the solitude practice are the most foundational places to begin. One posture held consistently begins to give the self below the versions space to speak."),
    ("Tell one person what you found.", "Not the whole document. One sentence: <i>I learned that my mechanism is the Adapter, and my breakdown is the Flood, and I have been keeping the different versions of myself in separate apartments for years, and they finally got into the same room.</i> The Adapter's pattern lives in the social performance. Speaking it to a trusted witness in your own voice is the first act of living outside the performance."),
    ("Read further on the self you did not assemble.", "Tim Keller, <i>Counterfeit Gods</i> — especially his treatment of identity received rather than constructed. C. S. Lewis, <i>The Weight of Glory</i> — the title essay in full; his treatment of the longing to be known and addressed by name is the most precise pastoral address to what the Adapter most needs. Augustine, <i>Confessions</i>, Book 10 — his account of the vast palaces of memory and the selves stored within them is not a problem for him; it is the landscape in which he finds God. Bonhoeffer, <i>Life Together</i> — the community Bonhoeffer describes is one in which differentiated, un-adapted selves are not a threat to unity but the precondition of it."),
    ("If you are stuck, ask for help.", "There are seasons when the Adapter and the Flood are too entrenched to dislodge alone. A wise pastor, a Christian counselor, a trusted friend who has earned the right to your un-adapted self — these are not signs of failure. For the Adapter specifically, asking for help without managing the other person's experience of the asking is one of the most countercultural and most healing things on this list."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom by a Father "
    "who chose you before the foundation of the world \u2014 before any room existed to require "
    "a version, before any feedback was available to borrow. The self that came out in the "
    "Flood was not a failure. It was an arrival. The One who named you has been waiting for "
    "all of you to be in the same room. "
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
    """Generate the Adapter+Flood walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='ADPT', primary_breakdown='FLOOD',
    primary_trigger='CTRL', core_question='FREE'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor's Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR'S WALKTHROUGH",
        cover_right_label="ADAPTER  \u00b7  FLOOD",
        title="Take 139 Walkthrough \u2014 Adapter + Flood",
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
    story.append(Paragraph("The Adapter \u00a0\u00b7\u00a0 The Flood", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Control \u00a0\u00b7\u00a0 Core Question: Am I free?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cWhy are you cast down, O my soul,<br/>"
        "and why are you in turmoil within me?<br/>"
        "Hope in God; for I shall again praise him,<br/>"
        "my salvation and my God.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Psalm 42:5\u20136",
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
        story.append(Spacer(1, 8))
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
                   "The river that formed without a decision. What you built, and what the building cost you.")
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
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 5: Breakdown \u2500\u2500
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Flood.",
                   "Multiple selves at once, with no conductor. What floods out, and what it is reaching for.")
    for p in FLOOD_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "What the Flood contains.",
                   "The psalmist who speaks to his own soul. The vast palaces Augustine found.")
    for p in FLOOD_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in FLOOD_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Stay with the open.",
                   "Two questions to sit with before you turn the page.")
    for prompt in FLOOD_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same need, in two directions.",
                   "The Adapter and the Flood are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=3)
    story.append(PageBreak())

    # \u2500\u2500 SECTION 7: Tools \u2500\u2500
    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "When the Adapter is overworking.",
                   "Small enough to carry; honest enough to use.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    for name, desc in ADPT_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Flood comes.",
                   "Six practices for before, during, and after the containers break.")
    for name, desc in FLOOD_TOOLS:
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
        primary_breakdown = "FLOOD"
        primary_trigger = "CTRL"
        core_question = "FREE"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "adapter_flood_test.pdf")
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

    print(f"DONE: adapter_flood.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
