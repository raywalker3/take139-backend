"""Personal Walkthrough — Adapter + Quiet Exit (Verdict).

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Control trigger, "Am I free?" core question.
Breakdown: Quiet Exit (VERD) — quietly decides "I'm done"; stops investing;
           withdraws into a verdict, often invisible to the other person.

Breakdown code: VERD. Walkthrough #29 of 36.

Calibration note: This is the saddest Verdict breakdown because it involves
the death of a persona rather than the exit from a relationship. The Adapter
has decided which version of themselves cannot survive in this relationship
and has quietly retired that version, even while remaining physically present.
The spouse will say "you seem different" and the Adapter will say "I'm fine"
— and both will be telling the truth, because a specific version of the Adapter
has died but the body is still there.

KEY MOVES in Section Five:
- Distinguish the Adapter's legitimate self-editing (a form of love) from
  the Verdict's persona-retirement (a form of amputation).
- The temptation to retire a version is profound because the Adapter has
  multiple versions to spare. But every version retired is a part of self
  abandoned to silence — and what God created is the whole person.
- Romans 12:1-2: Paul does not say "present your most successful version"
  but "your bodies" — the whole self.
- Tozer, The Pursuit of God: "It is impossible to know God in part."
- Lloyd-Jones on dying to self (Christ's requirement) vs. slow death of
  personas (the world's substitute).

CRITICAL CODE-QUALITY RULES:
- Do NOT use Python adjacent-string-literal continuation inside triple-quoted
  strings. All long strings must be single unbroken string literals.
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
    "Before you read any further, I want to do what a good counselor does before he says anything difficult. I want to lower the lights, slow the pace, and ask you to stay with me for a few minutes in the particular sadness of the profile you are holding. Because the person this walkthrough describes is not a person who fails loudly. They are a person who disappears quietly — and there is a real pastoral difference between those two things, because the quiet disappearances are the ones that are hardest to interrupt, and hardest to name, and hardest to grieve, because from every external angle they look like nothing has changed.",
    "You are, in a real sense, an Adapter. Not because you are false or insincere — the Adapter is, if anything, one of the most genuinely present people in any room they enter. But because something early in your experience taught you that the surest path to belonging was not to bring a fixed self and wait to see if it would be received, but to read the room carefully and become what the room could hold. You learned to move between people the way a musician moves between keys — the same instrument, a different sound depending on what the piece required.",
    "We are going to walk through your trigger — the moment your nervous system registers something as wrong. We will listen to the question underneath that moment, one that has probably been with you since you were very small. We will name the strategy you built in response, and then the specific place that strategy collapses when it has been strained long enough. And only then will we put tools in your hands.",
    "If you were sitting across from me, I would say this plainly and mean it: <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who knew you before any version of you was assembled; a Son who walked into every room as himself and never adjusted who he was to keep people close; and a Spirit who is, at this very moment, attending to the whole person — not the version you have decided to present today, and not the versions you have quietly retired, but the entire self that God made and has never stopped calling by name.",
    "Read slowly. Argue with what does not fit. Stay with what does. Pray when something catches in your throat, because that catch is usually the Lord saying, <i>look here, with me.</i> The goal of this walkthrough is not self-knowledge for its own sake. The goal is a slightly freer life — one in which you do not have to keep choosing which version of yourself is safe enough to survive the next room. Take your time. The chapter you are about to read about yourself has been a long time in the writing.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it is difficult to describe to people who do not share your wiring, because from the outside it often looks like almost nothing. Someone tells you what to do in a tone that does not ask. A decision that affects you is made without consulting you. A spouse sets a condition — a small one, perhaps even a reasonable one — and something in you goes very still in a way that has nothing to do with whether you agree with the condition. Someone uses the word <i>should</i> in a particular way, directed at you, and you feel something tighten in the center of your chest.",
    "This is not the tightening of stubbornness, though it can look like that from the outside. It is not the tightening of pride, though pride will sometimes attach to it quickly. What fires inside you, in under three seconds, is a signal that is older and more primal than either of those. The signal is not <i>that is unfair.</i> The signal is closer to <i>something about who I am is being required to be otherwise, and I do not know if there is enough of me left to be required.</i>",
    "This is your trigger. The word we use for it is <b>control</b>, but the word is doing more work here than it appears to. For most people, a control trigger is about autonomy — the desire not to be told what to do. For you, it is something more subtle and more frightening. The question that rises underneath the trigger is not merely <i>will I be allowed to make my own choices?</i> It is: <i>Am I free? Is there a me here that is not simply a reflection of what you need from me? Will my individuality survive this relationship?</i>",
    "C. S. Lewis, in <i>The Weight of Glory</i>, observed that there is something in every human soul that longs to hear a word spoken by the highest authority: <i>well done</i> — not to a performance, but to a person. You have spent years performing, and you have been extraordinarily good at it, and the applause has been real. But the performance has left behind a question that the applause has never quite answered: <i>if I stopped performing — if there were no room to read and no version to become — would there be someone here? And would that person be loved?</i>",
    "<b>Your sensitivity to control is not random.</b> It is the residue of something learned early — in a household where having your own preferences, your own particular interior life, carried a cost. Perhaps love was conditional on conformity. Perhaps the emotional climate changed unpredictably and reading the room became survival before it became style. Perhaps there was enmeshment, a family system so tightly woven that having a self that differed from the family's preferred self felt threatening to the whole unit. Whatever the history, the lesson lodged clearly: <i>the safest thing is to be whatever the room can love.</i> And over time, the Adapter was born — not as a deceiver, but as a genuinely gifted reader of human beings who learned to give each person the version of you they most needed to receive.",
    "Before we go further, I want you to sit with two questions in writing. Not in your head — the Adapter's head will reframe the questions to fit whatever the moment seems to need. Your hand will be more honest.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week, that the control trigger fired. What happened, in two sentences? You are not looking for a dramatic event — often the trigger fires quietly, in a small moment of being told who you are supposed to be.",
    "What was the size of the actual event, and what was the size of the response inside you? If the response was significantly larger than the event — if something in you went still in a way that surprised you — you have just located your trigger. Write one sentence about what the gap tells you.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding. The Adapter has been guarding this one for a very long time, and so skillfully that you may not have let yourself put it into plain words.",
    "Yours is this: <b>Am I free?</b>",
    "It is not simply the question of whether you are allowed to make your own choices — though that concern is real, and we will stay with it. It is something more personal and more frightening than external permission. It is the question of a soul that has spent so much time reading rooms and becoming what rooms needed that it now wonders whether there is a self underneath the adaptations that would survive if the adaptations were removed. <i>Am I free to be myself? And if I were — truly, without adjustment, without the version-selection — is there a self to be?</i>",
    "Most adults would prefer not to ask this question. They have organized their lives so that it does not need to be asked directly. For the Adapter, the question comes in through the side door every time someone tries to set a condition on who you are allowed to be in their presence. The trigger is not the condition itself; the trigger is the implication behind it: <i>there is a version of you that is more convenient to me, and I would like that version rather than the one currently present.</i> And your soul, which has been selecting versions of itself for years, does not know whether to comply or revolt — because it is not entirely sure it has a version that is not already a selection.",
]

QUESTION_BODY_P2 = [
    "There is a reason the theologians of the Reformation — Luther, Calvin, and the entire tradition the Apostle Paul grounded — understood freedom not merely as a political or social category but as a theological one. The freedom that matters most is not the freedom to do whatever you wish. It is freedom from the tyranny of being anyone's source of meaning — the freedom of a soul that does not have to earn its standing in every room it enters. Paul names it in Romans 6:6-7: <i>We know that our old self was crucified with him in order that the body of sin might be brought to nothing, so that we would no longer be enslaved to sin. For one who has died has been set free from sin.</i>",
    "The Adapter's captivity is rarely to sin in the obvious sense. It is to something subtler: the captivity of a self that cannot be still, that must keep reading and adjusting and becoming, because the alternative — being simply who one is, without the adaptive fluency — feels exposed in a way that is intolerable. Paul names this too: <i>you did not receive the spirit of slavery to fall back into fear.</i> (Romans 8:15) The Adapter's adaptation is, at its root, a response to fear — the fear that a fixed, un-performed self will be found wanting.",
    "The Psalms name this longing honestly. Psalm 31:8: <i>you have not delivered me into the hand of the enemy; you have set my feet in a broad place.</i> The broad place David speaks of is not a wide field. It is the freedom of a soul whose standing does not depend on performing correctly, on reading the room, on becoming what the moment requires. And yet here is the honest rub: the gospel tells the Adapter that in Christ you are already free — that the question <i>am I free?</i> has been answered once and permanently. Your nervous system does not feel this yet. It has been reading rooms for so long that being told it does not have to feels less like freedom and more like a trap.",
]

QUESTION_BODY_P3 = [
    "The gospel anchor for the question you carry is this: you are a <i>New Creation</i> — the old identity in Adam, with all its captivity and its exhausting responsiveness to whoever was in the room, is dead. <i>Therefore, if anyone is in Christ, he is a new creation. The old has passed away; behold, the new has come.</i> (2 Corinthians 5:17) This is not a permission to stop caring about the people around you — the Adapter's attunement is a genuine gift, and the gospel does not retire gifts. It is the announcement that the attunement is now free to be what it was always designed to be: love that flows from abundance rather than adaptation that flows from need.",
    "The freedom the Adapter has been guarding so fiercely is already fully yours in Christ. You do not need to fight for it, perform for it, or flee from rooms that threaten it. John 8:36 says it plainly: <i>if the Son sets you free, you will be free indeed.</i> Not free pending compliance. Not free conditional on the right performance. Free indeed — which is to say, free even when the room is asking for something else.",
    "The work this section invites is not more self-examination — the Adapter has enough introspection. The work is the slow practice of receiving freedom as a gift already given, rather than fighting for it as territory that must be defended at great cost. Before we close this section, use the table below. You are not analyzing yourself; you are observing. Use recent events, not ancient ones.",
]

ADPT_BODY_P1 = [
    "You have built something. It did not announce itself as a strategy when it was forming. It formed the way a river forms — not by decision, but by the path of least resistance through a landscape that rewarded certain movements and punished others. And one day you looked up and the river was already there, running through every relationship you had, shaping the way you moved through every room. Throughout this walkthrough we are going to call it <b>the Adapter</b>, and the Adapter deserves to be introduced as a character before we say anything about what it costs.",
    "The Adapter is not the Ambassador. This distinction matters, and the two mechanisms look so similar from the outside that they are worth pausing over carefully. The Ambassador takes care of people by serving them — bringing warmth, managing emotional temperature, being the one who notices when someone is left out and goes to find them. The Ambassador is the same person across contexts, serving differently but remaining recognizably themselves. The Adapter does something different: the Adapter takes care of people by <i>becoming what they need to see.</i> Not performing a false self — the Adapter is genuinely present in every version. But the version itself shifts. You can be utterly authentic in five different ways with five different people in one day and feel no contradiction, because for the Adapter, authenticity has never been a fixed self presenting itself consistently; it has been the full entering-in to whatever the relationship most needs.",
    "There is a great deal in Scripture that commends relational intelligence of this kind. Proverbs 25:11 says: <i>A word fitly spoken is like apples of gold in a setting of silver.</i> Paul himself said: <i>I have become all things to all people, that by all means I might save some.</i> (1 Corinthians 9:22) The Adapter lives this verse before they have ever read it. It is a genuine fluency in relational languages, and the world is better when people like you are in it.",
]

ADPT_BODY_P2 = [
    "But there is a cost, and the cost is specific to this mechanism, and it deserves to be named honestly. The Adapter's most characteristic experience is this: you can be fully present in a conversation — genuinely moved, genuinely engaged, genuinely yourself — and walk away an hour later and not be entirely sure which of your preferences, which of your opinions, which of your actual interior responses were yours and which were calibrated to the person you were with. The calibration happens below the level of conscious decision. It is not dishonesty. But it produces, over years, a specific kind of interior ambiguity about what you actually want, what you actually believe, what you would actually choose if no one were in the room to calibrate to.",
    "The taxonomy we work from suggests several histories that tend to produce the Adapter, and you will likely recognize yourself in at least one. Perhaps you grew up in a household where the emotional climate changed frequently and reading the room was not a preference but a survival skill — the way to stay safe was to become what the safest version of the moment needed. Perhaps there was enmeshment, a family system where having a self that differed from the family's preferred self felt dangerous, and you learned to make your self available rather than insisting on it. Perhaps you discovered very early that being exactly what someone needed was the most intoxicating experience available — the look of recognition on a person's face when you gave them the version of you they did not know they were looking for. Perhaps a parent's love was conditional on conformity and you adapted into lovability and never quite found your way back to yourself.",
    "Whatever the specific history, the Adapter's deepest characteristic is not the adaptation itself. It is the difficulty of answering, in the quiet, the question asked with unusual directness: <i>Who are you when no one is watching?</i> For most people, this question has an answer ready. For the Adapter, the answer is slower in coming. <b>The Adapter is not your enemy.</b> He is a younger version of you who learned, in some real and specific circumstance, that the self which could flex was safer than the self which held its ground. He deserves your respect, not your contempt. He kept you connected. He gave you gifts — empathy, attunement, a rare fluency in the emotional languages of the people around you — that are genuinely valuable. But he has been working overtime on a project that was finished years ago. And the question he was built to prevent — <i>will you be acceptable if you are simply yourself?</i> — is one that he is not, and has never been, equipped to answer.",
]

ADPT_BODY_P3 = [
    "What does it look like to begin loosening the Adapter's grip? Not eliminating the gift — the attunement is real and should not be retired. But beginning, slowly, to distinguish between the attunement that flows from love and the adaptation that flows from fear. These two things feel almost identical from the inside. The difference is in the root: the attunement that flows from love can stop if the stopping is right; the adaptation that flows from fear cannot stop without triggering the alarm.",
    "It begins with sitting still long enough to notice what you actually want. Not what the room wants from you, not what would serve the other person best, not which version of your preference would land most smoothly. What do you want? The Adapter often discovers, when sitting with this question for the first time without the usual social context to calibrate against, that the answer is genuinely unclear. This is not a failure of self-knowledge. It is the honest recognition of a mechanism that has been so faithfully at work that the self underneath it has not had much occasion to speak.",
    "The letter below is written in the Adapter's voice — addressed directly to you. He is not a villain. He is genuinely confused, and genuinely faithful, and genuinely tired. He has something to say that he has never been asked to put into words. Give him that chance now.",
]

ADPT_LETTER_INSTRUCTION = [
    "The letter below is written from the Adapter, in his own voice, to you. He is not a villain; he is a craftsman who has mistaken his tool for his identity. Read it slowly. Then answer the three prompts that follow.",
    "Dear [your name],",
    "I want to tell you something I have never been asked to say, because I have never been still long enough to say it. And the truth is, the stillness is the problem. I do not do well with stillness. In stillness, there is no room to read. There is no feedback to borrow. There is no version of you to present. There is only — I am not sure what. And that not-knowing is the thing I have been moving away from, more or less continuously, for as long as I can remember.",
    "I learned early that I could be loved. Not by being fixed, not by holding my ground, not by saying <i>this is who I am and this is what I want</i>. That kind of love felt too uncertain — you put yourself out and waited and the waiting was unbearable. But I found something better, or what seemed like something better: I could read what someone needed, and become it, and the love came immediately. It did not require waiting. It required attention, and I had an inexhaustible supply of attention.",
    "I want you to know what I actually did for you. I kept you in every room you were ever in. I kept the relationships going. I kept people close. I made you easy to love, because I made sure that whoever you were with, you were giving them something they needed. That is not nothing. You have been loved. And I have worked very hard for that.",
    "What I did not know how to do — what I am only now beginning to see I could not do — is give you a self that was yours when no one was there. I kept you present in every room. I did not know how to keep you present in the room with no one in it. I do not think I knew there was supposed to be a you there too.",
    "I am telling you this because something has been happening that I should have named sooner. When the room has required too much — when the version it needed felt like the last version available, when I ran out of versions to produce — I did not announce it. I simply retired one. Quietly, without ceremony. Withdrew it from service. And I told you, and told myself, that this was wisdom. That we had simply learned which parts of us this relationship could hold and which parts it could not. I called it maturation. I am not certain it was.",
    "The Adapter",
]

ADPT_LETTER_PROMPTS = [
    "What part of the Adapter's letter surprised you — not the part you expected, but the part you were not quite ready to read?",
    "The Adapter says he retired versions quietly, calling it maturation. Name one version of yourself — one way of being, one set of opinions or desires or patterns of engagement — that has gone quiet in a specific relationship. When did it go quiet? Was it a conscious decision or something that simply happened?",
    "The Adapter says he kept you present in every room but could not keep you present in the room with no one in it. When was the last time you sat quietly, without calibrating to anyone, and felt at home in yourself? Describe that moment, or describe the absence of it.",
]

VERD_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Adapter, the breakdown is called <b>the Quiet Exit</b>, and the Adapter's version of it is, among all the profiles in this taxonomy, the one most likely to go unnamed for the longest time — by the Adapter, and by everyone around them. It does not look like withdrawal. It looks like maturation. It looks like a person who has wisely learned which version of themselves this relationship can hold. It is none of those things, though it has borrowed all of their vocabulary.",
    "Here is the setup. The Adapter has been doing what the Adapter does — reading every room, adjusting to every person, being whatever the relationship most needed. And over time something accumulates. A particular version — the one that wanted to disagree, or the one that had desires the relationship did not seem to welcome — keeps finding that the room cannot hold it. The control trigger fires quietly: <i>you are being required to be otherwise.</i> And the Adapter, who has more versions available than most people have moods, makes the only move the mechanism knows. It retires the troublesome version. Not dramatically, not with an announcement — with the quiet efficiency of a craftsman who has run a studio for years and knows which tools are no longer in use.",
    "And then the spouse says, after a while, <i>you seem different lately.</i> And the Adapter says, <i>I am fine.</i> Here is what makes this profile so pastorally important to see clearly: <b>both of them are telling the truth.</b> The Adapter is fine — the surviving roster is functioning well. The spouse is also right — a specific version of the Adapter has quietly died and the body is still there. The grief for that part has never been held, because the part was never announced, and the retirement was never mourned.",
]

VERD_BODY_P2 = [
    "Now I want to make a distinction this walkthrough must make carefully, because if it is not made, I will be heard as saying something I am not saying.",
    "There is a genuine and God-honoring capacity in the Adapter to edit — to recognize that not every version of the self belongs in every relationship, that maturity involves learning which parts of the self to offer and when. This is not the Quiet Exit. The theologian A. W. Tozer wrote, in <i>The Pursuit of God</i>, that <i>it is impossible to know God in part</i> — by which he meant that the soul cannot approach God holding certain rooms closed while presenting a selected interior. But Tozer was not saying the soul should say everything to everyone. He was naming the particular danger of a soul that has so subdivided its own interior that it no longer knows the whole of itself.",
    "The Quiet Exit is not the Adapter learning what to offer. The Quiet Exit is the Adapter permanently amputating a version of the self from the relational inventory — not because the relationship has genuinely been tested and found unable to hold that version, but because the mechanism has decided, on its own evidence, in its own private court, that testing would be too costly. <b>The pastoral distinction is this:</b> the Adapter who genuinely presents a difficult version of the self and discovers, over time, that the relationship cannot hold it, has earned a limit. The Adapter who retires a version before the test was honestly run has not discovered a limit. They have imposed one. That imposition — silent, efficient, and almost invisible — is the Quiet Exit.",
    "D. Martyn Lloyd-Jones, in his sermons on spiritual depression, wrote about the dangerous spiritual condition that has substituted a self-secured equilibrium for genuine communion. It feels like peace. It presents as composure. It has none of the visible distress that might cause someone to intervene. The pastoral work of this section is to ask, gently but directly: <i>Am I at rest in this relationship because God has given me that rest, or am I at rest because a version of me has stopped hoping and the body has become comfortable with the quietness that followed?</i> The difference between those two things is everything.",
]

VERD_BODY_P3 = [
    "The Apostle Paul, in Romans 12:1-2, writes one of the most searching sentences in the New Testament: <i>I appeal to you therefore, brothers, by the mercies of God, to present your bodies as a living sacrifice, holy and acceptable to God, which is your spiritual worship.</i> Notice what Paul says — and equally what he does not say. He does not say <i>present your most successful version</i>. He says <i>your bodies</i> — the whole self, including the versions that have been quietly retired because the room did not seem able to hold them. The living sacrifice is not a curated offering.",
    "The temptation to retire a version is profound precisely because the Adapter has multiple versions to spare. When a version is retired, the mechanism does not feel the loss immediately — other versions are available, the relational service continues, and the Adapter can operate for years with a significantly reduced self without the external signs that would normally prompt intervention. But every version retired is a part of self abandoned to silence. And what God created in the Adapter is the whole person, not the surviving roster.",
    "Lloyd-Jones drew a distinction that belongs directly here: the difference between dying to self — which Christ requires, which produces genuine freedom — and the slow death of personas, which is the world's substitute for crucifixion. The former involves surrender to God; the latter involves surrender to the room. The former produces life; the latter produces a carefully managed silence that both parties eventually learn to call maturity. The pastoral word to the Adapter is this: <i>stop burying versions of yourself that God made, and bring them — carefully, bravely — into the relationship that has not yet had the chance to receive them honestly.</i>",
]

VERD_PROMPTS = [
    "Name the version of yourself that has gone quiet in a specific relationship — not a version you consciously chose to retire, but one that simply stopped appearing. When did it begin to disappear? Was there a particular moment, or was it a slow withdrawal across many small moments?",
    "Ask yourself the honest question: <i>In this specific situation, have I presented this version of myself to this relationship honestly and found it genuinely unable to hold it — or have I made that decision on my own evidence, in my own private court, before the honest test occurred?</i> Write the most honest answer you can. Do not edit it for pastoral acceptability.",
]

TWO_TOG_BODY = [
    "Now we place them side by side, because the Adapter and the Quiet Exit are not two separate problems. They are the same interior life, moving in two different directions — and in the end, arriving at the same silence.",
    "<b>The Adapter is what your need does when it has room to maneuver.</b> The Quiet Exit is what your need does when it runs out of versions. The Adapter reads rooms and becomes what rooms need so the alarm will not have to ring. The Quiet Exit quietly retires the version that keeps triggering the alarm and continues operating with what remains. Together they form a loop, and the loop is powered by the same question: <i>Am I free to be myself, and if I were, would that self — the whole of it — be loved?</i>",
    "The pattern, in slow motion, looks like this. <b>(1)</b> The Adapter moves through the world reading rooms and becoming what the rooms need. <b>(2)</b> A moment arrives in which the control trigger fires: someone requires a particular version of you, or refuses a version you needed to offer. <b>(3)</b> The trigger fires. The body says, <i>something about who I am is being overridden.</i> <b>(4)</b> The core question wakes up: <i>Am I free?</i> <b>(5)</b> The Adapter tries to produce a version that will resolve the tension — honest enough to satisfy, adaptive enough not to cost anything. <b>(6)</b> It does not work. The version that needed to speak is still waiting. <b>(7)</b> Over time, quietly, that version is retired. The mechanism continues operating with the surviving roster. <b>(8)</b> The spouse says <i>you seem different</i>. The Adapter says <i>I am fine</i>. Both are telling the truth. The loop has reached its most dangerous point, because there is no obvious alarm left to interrupt.",
    "What breaks the loop is not a better version of the self, and it is not a braver performance. It is a different source for the self altogether — the reception of the whole self, not the curated self, from a Father who named every version before any of them were assembled, and who is not satisfied with the surviving roster. Below is your sequence. Fill in the blanks. When you are done, read it aloud. Both the Adapter and the Quiet Exit lose some of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as control \u2014 as "
    "being required to be a particular self that is not mine to choose \u2014 and the "
    "old question surfaces: <i>am I free?</i> My first move is to ____________________, "
    "because the Adapter in me believes that if I can ____________________, the "
    "tension will pass and the relationship will remain. When that does not work, "
    "I do not announce a verdict. I simply retire ____________________. Quietly, "
    "without ceremony. This feels like ____________________, but what it actually "
    "is, underneath, is ____________________. What God has said about the whole "
    "self \u2014 not the surviving roster, but the entire person he made \u2014 is "
    "____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of tools — each one concrete enough to carry, honest enough to use. None of them will dissolve the Adapter's pattern in a single application. All of them, practiced over months, will loosen the grip of the loop you have just named.",
    "I have divided them into two sets: tools for when the Adapter is overworking its calibration — when the room-reading has tipped from gift into compulsion — and tools for when the Quiet Exit has begun or is beginning, and you need to interrupt the retirement before it becomes the kind of permanent that cannot be undone. The Adapter's tools come first, because the Exit cannot be addressed usefully until the mechanism underneath it is understood.",
]

ADPT_TOOLS = [
    ("The preference question", "Once a day, before the first social interaction, ask yourself one question without reference to anyone else in the room: <i>What do I want today?</i> Not what would be best, not what would serve the relationship, not which version of me would be most useful. What do I want? The Adapter will find this question disorienting at first. That is the point. The disorientation is the honest recognition that the mechanism has been running. Do not push for a large answer. A small one will do."),
    ("The unedited opinion", "Once a week, in a low-stakes conversation, offer an opinion before you have checked it against what the other person appears to need. Not a combative opinion — simply an un-adjusted one. Notice what happens in your body when you do this. Notice whether the relationship survives. It almost certainly will, and the survival is data the Adapter needs to receive."),
    ("The handed-back calibration", "When you notice the Adapter running — when you catch yourself adjusting, selecting a version, softening a preference for the room — say quietly, before you adjust: <i>Lord, I am doing it again. The version I am about to present is not the whole of whom you named. Help me be present as the person you chose before any room required a version.</i> You do not have to stop the adaptation immediately. Simply naming it disrupts its automaticity."),
    ("The solitude practice", "Once a week, spend thirty minutes alone without input — no phone, no music, no reading. Sit with the question: <i>Who is here?</i> The Adapter, having nothing to calibrate to, will initially feel unmoored. That feeling is not emptiness. It is the legitimate discomfort of a self that has not often been allowed to be simply present without a room to serve. The practice, over months, begins to give the self below the versions a chance to speak."),
    ("The Psalm of identity", "When the Adapter's calibration tips into anxiety — when you feel the compulsive need to check, adjust, and become — open to Psalm 139 and read the first four verses aloud: <i>O Lord, you have searched me and known me. You know when I sit down and when I rise up.</i> God is not reading the version you selected this morning. He is reading you — the specific, irreducible, un-adapted you he knew before the foundation of the world."),
]

VERD_TOOLS = [
    ("The version inventory", "When you notice the Quiet Exit beginning — when you catch a version of yourself going quiet, showing up less, hoping less — write it down. Name the version: <i>the version of me that wanted to speak about ___; the version of me that cared about ___.</i> Then write: <i>Have I honestly tested whether this relationship can hold this version? Or have I made that judgment on my own evidence, before the test?</i> The inventory is not the cure. But it breaks the secrecy that allows the retirement to proceed uncontested."),
    ("The whole-self prayer", "When a version of yourself has been quietly retired and you can feel it, pray Romans 12:1-2 back to God: <i>Lord, Paul did not say 'present your most successful version.' He said 'your bodies' — the whole self. I offer you the version I have been hiding. I offer you the parts of me I have decided this relationship cannot hold. I trust you with the whole person, not the surviving roster.</i> Say it slowly. The Adapter's mechanism is strong; the prayer will not feel persuasive the first time. Say it anyway."),
    ("Tell one person a version is missing", "The Quiet Exit lives on secrecy. The retirement proceeds quietly precisely because no one knows it has been filed. Before the version goes silent permanently, tell one trusted person — a pastor, a counselor, a friend who has earned the right to your interior — that a part of you has been going quiet. Not to fix it in that conversation. Simply to break the secrecy. The Exit loses most of its power the moment it is no longer entirely interior."),
    ("The honest test", "The Adapter has usually decided that this relationship cannot hold the difficult version before the test was honestly run. The practice is this: choose one version of yourself that has gone quiet and bring it into the relationship as a gentle experiment — not a confrontation, but a simple honest presence. <i>I actually see that differently. I actually want something different here.</i> Wait for the response. The Adapter's premise deserves to be tested rather than assumed."),
    ("The elder brother question", "Sit with Luke 15:28-30. The elder son was at home and had already left. Ask quietly: <i>Am I present in this relationship and already gone in the only sense that matters? Am I running the surviving roster while the person I was meant to be has quietly gone missing?</i> The father's response to the elder son was not condemnation. It was an invitation. The question is not: <i>what have I lost?</i> The question is: <i>what is the Father still inviting me toward?</i>"),
    ("The confession that fits", "When you recognize the Quiet Exit in yourself — when you see that a version has been retired and the retirement is being called maturation — the pastoral response is not self-criticism. It is confession: <i>Lord, I have been amputating parts of the person you made rather than bringing them to you and to this relationship. I called it wisdom. I think some of it was fear. I hand the whole self back to you. I am willing to bring the version I have been protecting into the light, and to trust you with what happens next.</i>"),
]

PRAYER_BODY = [
    "Father,",
    "You see the Adapter in me, and you are not disoriented by him. You have seen every version, attended every room, watched every calibration. You know which ones were gifts and which ones were survival. Thank you that he kept me connected. Thank you that the attunement he gave me has been genuinely useful, in real relationships, to real people.",
    "But Father, something else has been happening that I have not named honestly. The versions have been going quiet. Not all at once. One at a time. And I have been calling the quietness growth, calling the retirement wisdom, telling myself and telling the people I love that I have simply learned what this relationship can hold. I am not certain that is the whole truth. I think some of it is that I ran out of courage to find out. Teach me that you made the whole person — not the surviving roster. Teach me that Romans 12 says <i>your bodies</i>, and that the offering you want is not the best version I have assembled but the whole self, including the parts I have been protecting from the test. Let that truth reach the place where the retirements are filed.",
    "Lord Jesus, you walked into every room as yourself. You read every person you encountered and loved them without adjusting who you were to keep them close. When the rooms could not hold you — when the mechanism of the world tried to require a different version than the one you brought — you did not retire the version. You brought the whole self all the way to the cross. I do not know what it would look like to do that in my marriage, in my friendships, in the ordinary rooms of my daily life. But I want to find out. Give me the courage to bring the version I have been hiding back into the room, and to trust you with the outcome.",
    "Holy Spirit, where I am calibrating, give me stillness. Where I am retiring versions, give me the courage to test them. Where the Quiet Exit has already proceeded further than I have admitted even to myself — where the surviving roster is running and I have told everyone I am fine — would you be the one who stands at the door before it seals, and calls the whole self back in.",
    "In the name of the One who said to the Father, <i>not my will but yours</i> — and who meant the whole self, every version, held nothing back — I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Adapter and the Quiet Exit have been with you for a long time, and one careful reading will not retire them — though it may be the first time they have heard themselves named. What follows is a short set of next steps, honest and unhurried, for the work that has just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different lines will land. The Adapter will prefer to file this once and consider the matter handled. Read it again anyway. The section that felt least relevant today may be the most necessary one in a month — particularly Section Five, which the mechanism will work hard to dismiss as an overstatement."),
    ("Take one tool, not six.", "Choose the single practice from Section 7 that is most directly relevant to where you are right now — not the most comfortable one, the most necessary one. Try it for two weeks before you add another. One posture, held long enough, begins to change the shape of the interior."),
    ("Tell one person what you found.", "Not the whole document. One sentence: <i>I learned that my mechanism is the Adapter, and my breakdown is the Quiet Exit, and I have been retiring versions of myself rather than testing whether this relationship could hold them.</i> The Adapter's pattern lives precisely in the space between the private verdict and the spoken word. Breaking that secrecy to one trusted witness is the first act of living outside the loop."),
    ("Sit with one Psalm of identity.", "Psalm 139 for a week, aloud, one section per day. Verse 1: <i>You have searched me and known me.</i> Verse 13: <i>For you formed my inward parts.</i> Verse 16: <i>In your book were written, every one of them, the days that were formed for me.</i> The Adapter needs, more than almost any other mechanism, the practice of being addressed by God as a singular, known, irreplaceable whole — not a successful version, the whole person. The Psalms do this. Let them."),
    ("Read further on the self you did not build.", "Tim Keller, <i>Counterfeit Gods: The Empty Promises of Money, Sex, and Power, and the Only Hope That Matters</i> — especially his treatment of identity as something received rather than constructed. C. S. Lewis, <i>The Weight of Glory</i> — read the title essay in full; his treatment of the longing to be known and addressed by name is the most precise pastoral address to what the Adapter most needs. A. W. Tozer, <i>The Pursuit of God</i> — particularly the chapter on the blessedness of possessing nothing; the soul that has been offering versions of itself has been, in Tozer's language, possessing itself rather than surrendering it."),
    ("If you are stuck, ask for help.", "There are seasons when the Adapter and the Quiet Exit are too entrenched to dislodge alone — particularly when the retirements have been proceeding for years and the surviving roster has become so practiced that neither partner can easily remember what is missing. A wise pastor, a Christian counselor, a trusted friend who has earned the right to your un-adapted self — these are not signs of failure. For the Adapter specifically, asking for help without managing the other person's experience of the asking is one of the most countercultural and most healing things on this list."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom by a Father "
    "who made the whole person \u2014 not the surviving roster, not the version that has been "
    "most reliably received, but every version, every desire, every disagreement, every part "
    "of you that has quietly gone missing from rooms where it was needed. "
    "The self underneath the retirements is not lost. It is known. It is kept. It is beloved. "
    "Go gently with yourself. The One who began the good work in you will be the one to finish it."
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
    """Generate the Adapter+Quiet Exit (Verdict) walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='ADPT', primary_breakdown='VERD',
    primary_trigger='CTRL', core_question='FREE'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="ADAPTER  \u00b7  QUIET EXIT",
        title="Take 139 Walkthrough \u2014 Adapter + Quiet Exit",
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
    story.append(Paragraph("The Adapter \u00a0\u00b7\u00a0 The Quiet Exit", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Control \u00a0\u00b7\u00a0 Core Question: Am I free?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cI appeal to you therefore, brothers, by the mercies of God,<br/>"
        "to present your bodies as a living sacrifice,<br/>"
        "holy and acceptable to God.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Romans 12:1",
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
                   "The chameleon, the social tuning fork. What you have built, and what it costs you.")
    for p in ADPT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ADPT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in ADPT_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Adapter.",
                   "Read the Adapter\u2019s own words. He has been faithful; let him speak.")

    letter_style = ParagraphStyle(
        "AdptVerdLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
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
                   "The Quiet Exit.",
                   "The retirement that looks like maturation. The amputation called wisdom.")
    for p in VERD_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "Editing versus amputating.",
                   "The pastoral distinction the Adapter most needs to hear.")
    story.append(Paragraph("<b>Editing as love; the Quiet Exit as amputation.</b>", S["H3"]))
    for p in VERD_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>The whole self, not the surviving roster.</b>", S["H3"]))
    for p in VERD_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions before you turn the page.",
                   "Write the honest answer, not the pastoral-sounding one.")
    for prompt in VERD_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=5)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same need, in two directions.",
                   "The Adapter and the Quiet Exit are not two problems. They are one loop.")
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
                   "When the Quiet Exit has begun.",
                   "Six practices for interrupting the retirement before it seals.")
    for name, desc in VERD_TOOLS:
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


# \u2500\u2500 STANDALONE TEST \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "ADPT"
        primary_breakdown = "VERD"
        primary_trigger = "CTRL"
        core_question = "FREE"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "adapter_verd_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages using /Type /Page[^s] pattern
    import re
    page_count = len(re.findall(b"/Type /Page[^s]", pdf_bytes))

    # Grab a snippet from the letter constant
    raw_letter = ADPT_LETTER_INSTRUCTION[2]
    clean_letter = re.sub(r"<[^>]+>", "", raw_letter)
    snippet = clean_letter[:120]

    print(f"DONE: adapter_verd.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB) — {out_path}")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet}")
