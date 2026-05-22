"""Personal Walkthrough — Performance Campaign + Quiet Exit (Verdict).

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Significance trigger, "Am I enough to be remembered?" core question.
Breakdown: Quiet Exit / Verdict (VERD) — the retirement of the campaign itself.

Walkthrough #35 of 36. Breakdown code: VERD.

THE PERFORMANCE+VERDICT CHARACTER:
This is the most catastrophically quiet of all the Verdict breakdowns, because
the Quiet Exit here is not an exit from a relationship. It is the retirement
of the campaign itself — the moment the Performance has decided, in private,
that the running is no longer worth what it costs, but has no category for
stopping, because stopping was always professional death. So the Performance
continues in body and exits in spirit. The public output continues. The heart
has left it. The achievements come and the Performance does not feel them.

This is the condition of the pastor who quietly stopped praying about his
sermons, the leader who wins the quarter and feels nothing, the executive
who closes the deal and sits alone in the parking lot unable to remember
why any of it began.

CRITICAL THEOLOGICAL MOVE (Section Five):
Revelation 2:1-7 (the church at Ephesus): "you have abandoned the love you
had at first... remember therefore from where you have fallen." The Performance
has not stopped doing the works; they have stopped doing them from love.
Mark 6:31: "Come away by yourselves to a desolate place and rest a while."
Keller, Walking with God: "The dark night of the soul is when God removes
the felt-sense of his presence so that we will love him rather than the
experience of him."

KEY DISTINCTIONS FROM OTHER VERDICT BREAKDOWNS:
- Architect's Verdict: a planner's drafted exit
- Island's Verdict: the elder brother who never left home
- Ambassador's Verdict: internal funeral disguised as gentleness
- Vault's Verdict: signed-and-sealed legal finality
- Adapter's Verdict: death of a persona while the body remains
- Performance's Verdict: retirement of the campaign itself — continues in
  body, exits in spirit; the unique spiritual condition of Revelation 2:4-5

PRESERVING FROM performance_attorney.py:
- Ambassador/Adapter distinction ("let me show you one more thing")
- "two kinds of producing"
- Campaign as "runner" character

CRITICAL CODE-QUALITY RULES:
- Do NOT use Python adjacent-string-literal continuation inside triple-quoted
  strings. All long strings must be single unbroken string literals.
- Avoid layout bugs: do NOT call _three_column_table(rows=5) followed
  immediately by PageBreak() near a page boundary. Use rows=3 or rows=4.
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
    "Before you read any further, I want to do for you what a good counselor does at the very beginning of a hard conversation. I want to lower the lights, slow the pace, and ask you to stay with me for a moment in the specific kind of exhaustion that has brought you to this page. Because the profile this walkthrough describes is not a person who has failed loudly. It is a person who has succeeded, and succeeded, and succeeded again — and arrived, somewhere in the middle of all that success, at a place where the winning no longer produces what it once promised, and the running no longer feels like it is going anywhere, and the question underneath everything is not yet ready to be spoken to anyone.",

    "You are, in a real sense, a runner. Not necessarily in the literal sense, though you may be that too. I mean something interior: you are a person who discovered, early in life, that forward movement — building, achieving, demonstrating, producing — was the surest path to being seen, valued, and kept. You learned that ordinary was forgettable, and forgettable was not safe. And so you ran. And the running worked, in the sense that running tends to work: it produced visibility, recognition, a record of demonstrated worth. What it did not produce, and has never produced, is the answer to the question underneath the running. That question is still there. It is why you are reading this.",

    "We are going to walk through your trigger — the specific moment your nervous system says something is wrong here. We will sit with the question underneath that moment, the one that has been with you since the first time you understood that some people are remembered and others are not. We will name the strategy you have constructed in response, and then we will look carefully at the specific way that strategy collapses — not loudly, not visibly, but in the interior, where no one can see it happening. And then, only then, will we put tools in your hands.",

    "If you were sitting across from me right now, I would say this carefully and mean every word of it. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who did not first require a portfolio of demonstrated worth before deciding to love you; a Son who spent his ministry in the company of tired, depleted, over-functioning people and whose most common word to them was not <i>produce more</i> but <i>come to me and rest</i>; and a Spirit who is, at this very moment, less interested in the next achievement than in the person behind it — the person who has been running so long that they have forgotten what they were running toward.",

    "So read slowly. Argue with what does not fit. Stay with what catches. Write in the margins. Pray when something lodges in your throat, because that catch is usually the Lord saying, <i>look here, with me, at what is actually happening.</i> The goal of this walkthrough is not a better performance. It is the beginning of a different kind of life — one lived from a self that already has what the running was trying to earn. Take your time. The chapter you are about to read about yourself has been running for many years. It deserves a few hours of patient attention.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it has become increasingly difficult to locate precisely because you have become very practiced at moving past it without examination. Someone at work fails to credit you for an idea you clearly introduced. A friend recounts a shared accomplishment and edits you toward the margin. Your spouse turns toward their phone at the exact moment you begin describing something that cost you real effort. A committee makes a decision in your area of expertise without consulting you. And something inside you, in under three seconds, goes from zero to a temperature that the event, on its face, does not seem to warrant.",

    "What fired in those three seconds was not, strictly speaking, irritation. It was not pride, though pride will arrive shortly. What fired was an alarm, and the alarm has a specific frequency: <i>I am being treated as though I am replaceable.</i> As though the work does not count. As though the years of investment, the sustained excellence, the accumulated evidence of what you can do and what you have done — none of it has actually registered. You are being looked through, as if you were any person off the street rather than the specific person who has built the specific thing now standing in front of them.",

    "This is your trigger. The technical word for it is <b>significance</b>, but the word needs careful unpacking, because it carries a freight it does not immediately appear to carry. This is not vanity, though vanity sometimes clings to it. This is not the simple desire for applause, though applause is welcome. It is something more fundamental: the longing to matter. To have one's presence register. To be known not merely as a face in the crowd but as a person who has shown up, done the work, and earned the right to be seen doing it.",

    "C. S. Lewis, in <i>The Weight of Glory</i>, named the longing more precisely than almost anyone else has: we do not want merely to see beauty, though that is bounty enough; we want something else which can hardly be put into words — to be united with what we see, to pass into it, to receive it into ourselves. He was speaking of beauty, but the grammar of the longing is the same as yours. You do not merely want to do excellent work. You want to pass into the recognition it represents, to have the excellent thing and the person who built it finally become inseparable in someone's memory. When the recognition does not come — when the excellent work lands in silence, when the campaign produces and no one notices — the pain is not proportionate to the circumstance. It is proportionate to the longing underneath.",

    "<b>Your sensitivity to significance is not random.</b> It is the residue of something learned in a specific season of your history, usually early, always formative. Perhaps you grew up in a household where love was not withheld but was notably warmer when you performed. Perhaps ordinary effort was unremarkable and extraordinary effort was, finally, noticed — which trained your system to the conclusion that the path to being seen ran through the extraordinary. Perhaps there was a parent whose attention was chronically elsewhere, and achievement became the reliable method of capturing it. Perhaps you were one child among many in a family system where visibility had to be earned rather than assumed, and you were an early learner of the relevant lesson.",

    "Whatever its specific origin, the lesson arrived with the force of a conviction: <i>I will not be forgotten if I cannot be ignored.</i> And so you began to build. Not the Architect's careful blueprints — that is a different mechanism, driven by a different fear. You began to produce, to demonstrate, to show what you could do in the full light of day. You ran. And the running, over time, became not just a strategy but an identity. The Performance Campaign was born.",

    "Before we go further, I want you to sit with two questions in writing. Your head will reframe them in terms of the next campaign. Your hand will be more honest.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week, that the significance trigger fired. What happened? Who failed to see you, or what effort went unacknowledged? Write two sentences.",

    "What was the size of the actual event, and what was the size of the response inside you? If they did not match, you have just located the trigger — and underneath it, a question that is older than the event.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm has spent years guarding.",

    "Yours is this: <b>Am I enough to be remembered?</b>",

    "It is not the same as <i>Am I competent?</i>, though you have built extraordinary competence in part as an attempt to answer it. It is not <i>Am I loved?</i>, though you have spent considerable energy in relationships that felt like they might finally answer it. It is something more primal than either: the question a soul asks in the moment it realizes that the world has a great many people in it, that most of those people will be forgotten, and that being forgotten is, somehow, the deepest kind of not-mattering. <i>Will I leave something behind that is still there when I am gone? Will anyone remember I was here?</i>",

    "You have almost certainly never put it in those words. The Performance never does. The Performance translates the question into action rather than sitting with it. But trace backward from the alarm that fired this week, and from the one that fired the week before, and from the campaign you have been running for the last decade, and you will find this question at the root of all of it. <i>Am I enough to be remembered?</i> And behind that question, barely below the surface, its companion: <i>Or am I, after everything, ordinary?</i>",

    "The fear of ordinariness is one of the most socially acceptable fears a person can carry in our present age, which makes it both easier and harder to see clearly. Easier, because the culture around you tends to validate the Campaign and reward the runner. Harder, because the validation makes it almost impossible to notice that what you are running from is not obscurity but the question of your worth, and that no quantity of achievement has ever, in your experience, fully silenced it.",
]

QUESTION_BODY_P2 = [
    "There is a reason that the biblical tradition, from its earliest pages to its last, insists on the significance of those the world has forgotten. The Psalms were written by and for people who felt unseen and unnamed, and who brought that wound directly to God rather than sublimating it into a campaign.",

    "<i>Can a woman forget her nursing child, that she should have no compassion on the son of her womb? Even these may forget, yet I will not forget you. Behold, I have engraved you on the palms of my hands.</i> (Isaiah 49:15\u201316)",

    "The image is almost too intimate. Not engraved in a ledger, not recorded in a database, not awarded a certificate of achievement. Engraved on the palms of his hands — the part of the body that a person carries in front of their face every waking hour, always visible, always present. God is saying: when I look at my own hands, I see you. You are not forgettable. You are not ordinary. You are not anonymous. You are, in the most literal possible sense, impossible for the One who holds everything to forget.",

    "But — and this is where the honest pastoral work begins — the answer Scripture gives to your question is not the answer your nervous system has been trying to construct. Your nervous system has been trying to construct an answer made of accomplishments: <i>if I build enough, produce enough, achieve enough visible excellence, I cannot be ignored, and if I cannot be ignored, I cannot be forgotten, and if I cannot be forgotten, I am safe.</i> What Scripture says is something stranger and, in the long run, more solid: your significance is not produced. It is received. It is not earned by the campaign. It is given before the campaign begins.",

    "Paul puts it with his characteristic directness in Ephesians 1:4\u20135: <i>he chose us in him before the foundation of the world, that we should be holy and blameless before him. In love he predestined us for adoption to himself as sons through Jesus Christ.</i> Before anything you have ever built. Before any credential you have ever earned. Before the campaign had a single entry. Chosen. Named. Inscribed on the palms of his hands.",
]

QUESTION_BODY_P3 = [
    "The difficult honest work this section asks of you is not to stop achieving. The Performance Campaign is not, in itself, a sin. It is a gift that has been pressed into service as a salvation strategy, and it is wearing both itself and you down in the process.",

    "The honest work is to begin, slowly and with patience, distinguishing between two very different kinds of producing. There is producing that flows from gratitude — from a person who already knows they are seen and significant, who creates and builds from fullness rather than from need. And there is producing that flows from anxiety — from a person who is still trying to earn the significance that was given before they drew their first breath. From the outside, these two persons look almost identical. From the inside, one is free and the other is exhausted.",

    "The runner who knows they are already known can stop. The runner who is running to be known cannot — because stopping would mean risking the question: <i>and if I am not running, who am I?</i> That question is the one we need to stay with before we go any further. Before we close this section, use the table below. In the first column, name a recent event in which the significance trigger fired. In the second, answer your nervous system's question: <i>was I seen here?</i> In the third, answer the deeper question: <i>was the part of me that finally matters — my soul, my standing before God — at any point in danger?</i>",
]

CAMP_BODY_P1 = [
    "You have built something. It did not announce itself as a strategy; it announced itself as a life. But over years and campaigns and the accumulation of evidence, you have developed a particular way of moving through the world that we are going to call, throughout the remainder of this walkthrough, <b>the Performance Campaign</b>.",

    "It is important, before we go any further, to say what the Performance Campaign is not. It is not the Ambassador's mechanism. The Ambassador serves in order to be loved — brings warmth, manages emotional temperature, pours out care and waits, sometimes invisibly, for the love to come back. The Ambassador's currency is relational service. The Performance's currency is visible output. The Ambassador is the one who stayed late to make sure everyone was okay; the Performance is the one who stayed late to finish something extraordinary and wants you to know about the extraordinary thing. Both are earning, in a sense, but they are earning different things and using different methods.",

    "Nor is it the Adapter's mechanism. The Adapter reads the room and becomes what the room needs — calibrates its self to the audience, fluently and genuinely, as a way of purchasing connection. The Performance does not calibrate to the room. The Performance demonstrates to the room. The Adapter is asking, at some level, <i>what do you need from me?</i> The Performance is asking, at some level, <i>do you see what I have done?</i> The Adapter disappears into the audience; the Performance stands before it.",

    "The Performance Campaign is the runner. It is the achiever. It is the person who has a long r\u00e9sum\u00e9 and, often, a thin sense of who they are off the field. It is the person whose default response to anxiety is not to plan (that is the Architect) and not to withdraw (that is the Island), but to <i>produce</i>. When the question fires — <i>am I enough to be remembered?</i> — the Performance's answer is always the same: <i>let me show you one more thing.</i>",
]

CAMP_BODY_P2 = [
    "There is a great deal in Scripture that commends the kind of diligence the Performance embodies at its best. Proverbs 22:29 says: <i>Do you see a man skillful in his work? He will stand before kings; he will not stand before obscure men.</i> Excellence is genuinely valued in the biblical tradition. Work done with care and craft is, in Colossians 3:23, an act of worship: <i>Whatever you do, work heartily, as for the Lord and not for men.</i> The Performance Campaign is not, at its root, a sin. It is a gift. The runner was given legs and taught to run, and the running has been genuinely beautiful.",

    "But the trouble, as with all gifts, is in the purpose the gift has been pressed to serve. The taxonomy we use to understand these patterns names it directly: the Performance's drive to achieve, build, and leave a mark does something specific for it. It answers the question <i>do I matter?</i> through achievement. If I can point to something I built, I know I existed. The producing is, underneath its genuine pleasure and craft, also an existential argument. <i>I was here. I did this. You cannot pretend I was not in this room.</i>",

    "And there is something in you, reading that sentence, that recognizes it. Perhaps with a flicker of relief that someone has finally said it plainly. Perhaps with a flicker of resistance, because the naming makes it visible in a way that feels, briefly, like exposure. Both reactions are honest. The specific history that tends to produce the Performance Campaign takes several forms: perhaps ordinary achievement was unremarkable in your family while extraordinary achievement was noticed and rewarded. Perhaps you grew up feeling genuinely invisible — in a large family, a distracted household, or a school where the quiet student disappeared — and achievement became the antidote: <i>if I am impressive enough, I cannot be ignored.</i> Perhaps there was significant loss in your family of origin and you became the one who would prove the name was worth something. Perhaps the drive to leave a mark is partly grief looking for somewhere to live.",
]

CAMP_BODY_P3 = [
    "Whatever the specific history, the Performance Campaign arrived with a characteristic shape. The Campaign is genuinely energizing: the pursuit — the building, the vision, the satisfaction of something done with real excellence — fills you in a way that few other experiences do. Rest, by contrast, does not fill you. Rest feels, if you are honest, like a kind of death — not physical rest necessarily, but the cessation of forward movement, the afternoon when there is nothing to produce and nothing to demonstrate. That produces, with disturbing regularity, an anxiety with no obvious cause. Because the cause is not in the afternoon. It is in the question the afternoon allows to surface: <i>and who are you, when you are not running?</i>",

    "Your spouse — or the person who has known you longest — has probably said some version of the same sentence more than once: <i>I feel like an afterthought.</i> They are not wrong. The Campaign has a visibility problem: it can see the next achievement with extraordinary clarity, and the people standing quietly in the room — wanting simply to be with you — blur at the edges. Not because you do not love them. Because the Campaign's urgency crowds them out the way a bright light makes it difficult to see what is in the dimmer room just beyond it.",

    "<b>The Performance Campaign is not your enemy.</b> It is a younger version of you who learned, in some real and specific circumstance, that achievement was the reliable path to being seen, and that being seen was necessary for being safe. He has been faithful. He has produced genuinely remarkable things. He deserves your respect. But he is not twelve any longer, and you are not in the household or the classroom or the early career context that required him. He is running a race on a track that no longer leads where he thinks it leads. The finish line he is running toward — <i>finally enough, finally seen, finally safe from being forgotten</i> — is not, and has never been, at the end of that particular track.",

    "What does it look like to begin slowing the Campaign, not retiring it, but giving it shorter hours and a different mandate? It begins with the question the Campaign almost never asks: <i>what do I actually want, from the people who love me, that my achievements cannot give me?</i> The letter below is the Campaign's attempt to answer that question in his own voice. Read it slowly.",
]

CAMP_LETTER_INSTRUCTION = [
    "The letter below is written from the Performance Campaign, in his own voice, to you. He is not a villain. He is a builder who, for a very long time, confused his output for his worth and his production for his proof of existence. Read it slowly. Then answer the three prompts that follow.",

    "Dear [your name],",

    "I need to tell you something I have never said, because I have never stopped long enough to say it. The stopping is the problem. I do not do well with stopping. When there is nothing to build, nothing to demonstrate, nothing pointing toward the next achievement, I do not know what to do with the silence. The silence has always felt like danger. Not the danger of death — the danger of being ordinary. The danger of sitting in a room with nothing to point to and hearing the question come up without a ready answer: <i>and who are you, exactly?</i>",

    "I learned early that excellence was noticed and ordinary was not. Someone whose opinion mattered enormously to you looked up when you achieved something and looked back down when you did not, and your system drew the conclusion before you were old enough to question it: <i>the path to being seen runs through the extraordinary.</i> And so I began. I built the campaign. I ran. And the running was real — genuinely energizing, genuinely productive, genuinely beautiful in some of its seasons.",

    "What I want to tell you is what I have been unable to see clearly until recently. I have been watching you for some time now, and something is changing. The achievements are still coming. The visible record is still growing. But somewhere in the middle of the last several years, something in you stopped arriving at the finish line with me. You cross it. You receive the acknowledgment. You say the right things in the room. And then you sit in the car on the way home and feel almost nothing. Not grief. Not satisfaction. A strange and very particular nothing, like a flavor you expected and the tongue did not find.",

    "I built the right thing for the wrong reason, and I kept building it past the point where it could answer the question I was actually trying to answer. The question was never really about the work. It was about whether you mattered. And mattering — really mattering, in the place where it counts — is not something I know how to give you. I can make you visible. I cannot give you the knowledge that you are enough even when invisible. I am telling you this because I think you already know it, and I think the quiet you have been carrying is the cost of knowing it without yet having anywhere honest to put it.",

    "The Performance Campaign",
]

CAMP_LETTER_PROMPTS = [
    "What part of the Campaign's letter surprised you — not the part you expected, but the part you were not quite ready to read?",

    "The Campaign describes a specific moment: crossing the finish line and feeling almost nothing. When was the last time that happened to you? Describe it in two sentences.",

    "The Campaign says he built the right thing for the wrong reason. Name one specific thing you are currently building or pursuing. What is the right reason to do it? What might the wrong reason be? Can you tell the difference from the inside?",
]

VERD_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Performance Campaign, the breaking is called <b>the Quiet Exit</b> — and the Performance's version of it is unlike any of the other breakdowns we follow in this taxonomy, and unlike any of the other Verdict breakdowns we have seen in the other mechanisms.",

    "The Architect's Verdict is a planner's exit, drafted in private the way a project plan is drafted, with the clean lines of a person who has decided how to close the file with minimal collateral damage. The Island's Verdict is the elder brother who has been physically present and spiritually absent for years, the slow evaporation of hope conducted in the household's ordinary atmosphere. The Ambassador's Verdict is an internal funeral — grieving the relationship while still performing the service, still bringing warmth to a room whose warmth has quietly stopped being an offering and has become an obligation. The Vault's Verdict is signed and sealed with the Vault's characteristic finality; the file is closed, and the Vault does not re-open closed files easily. The Adapter's Verdict is the death of a persona — a particular version of the self quietly retired while the body remains, so that what the spouse experiences is a partner who is present and yet somehow smaller, less inhabited, than they were before.",

    "The Performance's Verdict is none of these. It is uniquely catastrophic in its own way, because what it retires is not a relationship and not a persona but the campaign itself. The Performance has decided, in private and without announcement, that the running has not been worth what it has cost — and rather than continue or rest, it has chosen a third option that its own vocabulary never quite prepared it for: it has stopped investing in being seen at all. Not openly. Not with any declaration that could allow someone to respond. It has simply withdrawn the heart from the work while the body continues to show up and perform.",
]

VERD_BODY_P2 = [
    "This often looks, from the outside, like a sudden quiet. The public output continues. The achievements come. The meetings are attended, the sermons preached, the deals closed, the campaigns run. But something is different, and the people who know you most closely have probably begun to feel it without being able to name it. The work is technically correct but spiritually absent. The presence is there and yet it is not. You produce results with the accuracy of a professional and the warmth of a person who is no longer fully in the room.",

    "This is the breakdown most associated with what the world calls mid-career burnout, but the pastoral name for it is older and more specific. It is the condition Jesus addressed in his letter to the church at Ephesus in Revelation 2. I want you to hear that passage carefully, because it is addressed to a church that was, by every external measure, performing magnificently. <i>I know your works, your toil and your patient endurance, and how you cannot bear with those who are evil, and have tested those who call themselves apostles and are not, and found them to be false. I know you are enduring patiently and bearing up for my name's sake, and you have not grown weary.</i> (Revelation 2:2\u20133) This is not a failing church. This is a working church. This is a church that has been running the campaign for years with real excellence.",

    "And then comes the word that should stop every Performance in their tracks: <b><i>But I have this against you, that you have abandoned the love you had at first.</i></b> (Revelation 2:4) The church at Ephesus has not stopped doing the works. It has stopped doing them from love. The difference, from the outside, is invisible. From the inside, it is everything. This is the Performance's Verdict: the works continue and the love has quietly exited.",

    "What is the remedy Jesus prescribes? Not stopping the work — the Performance fears stopping more than almost anything else. Not pushing harder — the Performance has been pushing harder for years without the equation changing. The remedy is <i>repentance</i> — a word that means, in its root, a turning of the mind, a going back. <i>Remember therefore from where you have fallen; repent, and do the works you did at first.</i> (Revelation 2:5) Go back to the place where the running was once an offering instead of an obligation. The works the Ephesian church did <i>at first</i> were the same works they were still doing. The difference was what the works were flowing from. Repentance, for the Performance's Verdict, is not stopping. It is returning — returning to the interior place where the work was once given rather than performed, offered rather than demonstrated.",
]

VERD_BODY_P3 = [
    "Tim Keller, in <i>Walking with God through Pain and Suffering</i>, wrote this: \u201cThe dark night of the soul is when God removes the felt-sense of his presence so that we will love him rather than the experience of him.\u201d I want to read that sentence slowly, because it does something for the Performance that no other diagnosis I know of does. The Performance has, for years, been sustained not by the love of God in the simple sense of that phrase, but by the <i>experience</i> of producing for God — by the felt satisfaction of ministry done well, sermons landing, influence growing, lives visibly changed. That experience is not bad. It is a genuine gift. But when God removes it — as he periodically does, with pastoral love and perfect timing — the Performance is exposed: it has been, without quite knowing it, loving the experience rather than the One who gave it.",

    "What does the Performance do when the felt-sense is removed and the work continues without it? If it has never learned the difference between producing from love and producing from obligation, it does the only thing it knows: it continues. It performs. It delivers the talk and closes the deal and finishes the campaign. And underneath the delivery, in the place no one can see, it is quietly dying. This is not mere discouragement. It is the soul's way of announcing that what it has been producing has not been flowing from the right source, and that the source has run dry. Mark 6:31 records Jesus saying to the disciples after they had returned from a full mission — exhausted, having given everything — <i>Come away by yourselves to a desolate place and rest a while.</i> This is not a critique of the work. It is the recognition that the human soul is not a mechanism of perpetual production. It is a creature that needs refueling at a Source it did not generate.",

    "Martyn Lloyd-Jones, whose analysis of spiritual depression remains among the most pastorally acute in the English language, observed that the most dangerous spiritual condition is the one that presents as composure. Not the dramatic collapse — that at least produces urgency, the recognition that help is needed, the willingness to be reached. The dangerous condition is the calm professional who has simply stopped expecting anything from the work and is performing the obligations without the life that should animate them. This person does not appear in crisis. They appear competent. They appear, sometimes, better than before — quieter, less reactive, more measured. What they are, in pastoral reality, is a person whose interior has gone cold, and who has mistaken the cold for peace.",
]

VERD_PROMPTS = [
    "Name the last time you produced something — a sermon, a project, a presentation, a significant piece of work — and crossed the finish line feeling almost nothing. How long ago was it? How often does that happen now?",

    "Revelation 2:4 names the condition as having abandoned the love you had at first. When was the last time the work felt like an offering rather than an obligation? Write one paragraph describing what that season was like, and what has changed.",
]

TWO_TOG_BODY = [
    "Now we place them next to each other, because the Performance Campaign and the Quiet Exit are not two separate problems. They are the same longing, managed in two directions. The Campaign moves outward — building, demonstrating, running, producing. The Quiet Exit moves inward — withdrawing the heart from the work while the body continues to show up, exiting the campaign in spirit while remaining in it in form.",

    "<b>The Campaign is what your longing does when it still believes the running will answer the question.</b> The Quiet Exit is what your longing does when it has decided, privately and without announcement, that the running has cost more than it has produced. The Campaign runs so the question does not have to be asked. The Quiet Exit fires when the Campaign has been running long enough without the answer that the question has been quietly given up on.",

    "The pattern, in slow motion, looks like this. <b>(1)</b> The Campaign runs. It produces, builds, achieves. It earns credentials and recognition and a visible record of demonstrated worth. <b>(2)</b> An event lands that the record cannot address. The significance trigger fires: someone fails to see you, or sees you and does not respond as your achievements seem to warrant. <b>(3)</b> The body says, <i>I am being treated as though I am replaceable.</i> <b>(4)</b> The core question surfaces: <i>Am I enough to be remembered?</i> <b>(5)</b> The Campaign answers by running harder. The work escalates. The output increases. <b>(6)</b> But somewhere in the escalation — and this is the moment most Performances cannot pinpoint precisely — the answer stops arriving. The work is done. The recognition comes. The verdict the Campaign has been pursuing lands, and the soul does not feel it. <b>(7)</b> The Campaign continues, because stopping is not an option it has a vocabulary for. But something has quietly exited. <b>(8)</b> The works continue. The love has been abandoned. The Verdict has been rendered in private, without announcement, possibly without the Performance even recognizing it as a verdict: <i>this is not worth what it costs me, and I do not know how to stop.</i>",

    "What interrupts this pattern is not stopping the work, and it is not producing more. It is a return — the specific repentance of going back to the place where the work was once given rather than performed. It is receiving, daily and by practice, the verdict that has already been spoken: engraved on the palms of his hands, chosen before the foundation of the world, significant not by achievement but by adoption. When that verdict is received in the place that has been running the campaign — really received, in the interior, not merely affirmed as a doctrine — the Campaign begins to find it can run for different reasons. The Quiet Exit begins, slowly, to reverse. Below is your sequence. Fill in the blanks. When you are done, read it aloud. The Campaign and the Quiet Exit both lose some of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When ____________________, my body reads it as being made invisible, "
    "and the old question surfaces \u2014 <i>am I enough to be remembered?</i> "
    "My first move is to ____________________, because the Campaign in me believes "
    "that if I can produce ____________________, the threat will pass. "
    "Over time, when the running has not answered the question, something in me has begun to ____________________. "
    "The Exit looks like ____________________ to the people around me, "
    "but from the inside it is ____________________. "
    "What I most need in that moment is not a better campaign but the truth "
    "that ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of practices — each honest enough to use, each small enough to carry. None of them will resolve the Campaign's longing after a single application. All of them, used over months, will loosen the grip of the loop you have just named.",

    "I have divided them into two sets: tools for when the Campaign is overrunning — when the producing has tipped from genuine vocation into existential argument — and tools for when the Quiet Exit has begun or is beginning, and you need to interrupt the departure before it becomes the kind of permanent that is very difficult to undo. The Campaign's tools come first, because the Quiet Exit cannot be interrupted usefully until the mechanism underneath it is understood.",
]

CAMP_TOOLS = [
    ("The stopped-clock practice",
     "Once a week, spend thirty minutes doing something with no measurable output. Not productive rest. Not a walk to clear your head for the next campaign. Something genuinely unproductive: sit in a garden, read poetry, watch a bird. When the anxiety rises — and it will — name it: <i>this is the question coming up without the campaign to answer it.</i> Do not answer the question. Simply let it be present without immediately running from it. The Campaign cannot be healed without first allowing the question it has been running from to be heard."),

    ("The work-worship distinction",
     "Before beginning any significant project, ask one question: <i>If no one ever knew I did this, and it produced no visible recognition, would I still want to have done it?</i> This is not a test of purity — recognition is a legitimate good. It is a test of whether the work can be offered as worship rather than demonstration. Colossians 3:23 is the frame: <i>whatever you do, work heartily, as for the Lord and not for men.</i> Work done for the Lord does not require the audience to arrive on schedule."),

    ("The handed-back achievement",
     "Each morning, name one thing you have built or produced in the past year that you are proud of. Then say, aloud: <i>This is yours, Lord. I did not build this to be remembered. I built this because you gave me these hands. Take it.</i> This will feel artificially humble the first several mornings. By the thirtieth, something in the Campaign begins to distinguish between building for God and building for the verdict."),

    ("The presence practice",
     "Once a day, give the person closest to you ten minutes of full, undivided presence — no device, no agenda, no half-attention toward the next campaign. Not because it produces a better relationship (though it will), but because the Campaign's most consistent failure is treating the people who love it as background to the main event. This practice begins to reverse that posture, one ten-minute session at a time."),

    ("The Psalm of inscription",
     "When the significance trigger fires and the Campaign reaches for the next production cycle, pause and read Isaiah 49:15\u201316 aloud: <i>I have engraved you on the palms of my hands.</i> Not as a technique. As an act of receiving a verdict that was spoken before the Campaign ran its first race. The Campaign needs, more than almost anything else, to practice receiving significance from a source that does not require a demonstration."),
]

VERD_TOOLS = [
    ("The return practice",
     "The remedy Jesus prescribes in Revelation 2:5 is specific: <i>remember therefore from where you have fallen; repent, and do the works you did at first.</i> Each morning, before beginning the day's work, spend three minutes with this question: <i>When did I last do this work from love rather than obligation? What was that like?</i> You are not trying to manufacture the feeling. You are going back, in memory and in prayer, to the place where the offering began. The heart follows the memory when the memory is brought honestly to God."),

    ("The offering prayer before the work",
     "Before beginning any significant task — the sermon, the meeting, the presentation — pray one sentence: <i>Lord, I offer this to you, not as evidence of my significance but as a gift from yours.</i> Say it even if you do not feel it. Say it especially if you do not feel it. The Quiet Exit lives on the gap between the work done and the love that should animate it; this prayer puts something in the gap before the work begins."),

    ("Name the coldness to one person",
     "The Quiet Exit lives on secrecy. It is a private verdict, rendered privately, and it becomes entrenched because no one ever spoke into it before it sealed. Before the interior goes fully cold, tell one trusted person — a pastor, a counselor, a friend who has earned the right to your interior — that the work has stopped feeling like it matters. Not to fix it in that conversation. Simply to break the secrecy. The Quiet Exit loses significant power the moment it is no longer entirely interior."),

    ("The test of the love",
     "Ask yourself the question the Ephesian church could not answer satisfactorily: <i>When did I last do this work from love — not from obligation, not from the fear of what stopping would mean, not from the momentum of years of doing it, but from genuine love?</i> Write the honest answer. Then ask: <i>Is the love gone, or has the love been buried under years of running and simply needs to be uncovered?</i> The difference between those two answers is the difference between a cold and a death, and only one of them is as final as it feels."),

    ("The Mark 6:31 practice",
     "Jesus said to the disciples who had been working without ceasing: <i>Come away by yourselves to a desolate place and rest a while.</i> (Mark 6:31) This was not a reward for successful performance. It was a recognition that the human soul cannot produce indefinitely from its own reserves. Schedule, within the next fourteen days, a genuine day of rest — not productive rest, not strategic renewal, but the kind of rest in which you are neither building nor demonstrating. The Campaign will call this negligence. Name it instead as obedience: you are a creature, and creatures need rest, and refusing it is a form of claiming a self-sufficiency that belongs to God alone."),

    ("The confession that fits",
     "When you recognize the Quiet Exit in yourself — when you can see that the work continues but the love has been quietly absent from it — the pastoral response is not self-criticism. It is confession, specific and honest: <i>Lord, I have been doing the works without the love. I have been running the campaign without offering it to you. I have been producing for the memory of others when I had already stopped expecting anything from the work myself. Forgive me. Bring me back to where the love began. I am willing to return if you will meet me there.</i> Then wait. The Campaign is not accustomed to waiting. That is why this is the practice."),
]

PRAYER_BODY = [
    "Father,",

    "You see the Campaign in me, and you are not impressed and you are not disappointed. You knew about the running before it started. You know which early moment wrote the lesson that ordinary was forgettable, and which season it was when I decided that I would never, if I could help it, be ordinary. Thank you that the running has produced real things. Thank you that the things it produced were not wasted, even in the seasons when they were offered for the wrong reasons.",

    "But Father, I confess something I have not named clearly until now. Somewhere in the running, the love left the work. Not dramatically — I could not have told you the day it happened. But the work continued and the offering stopped, and I have been producing faithfully on the outside while something essential has been quietly absent on the inside. You named this condition in the letter to Ephesus: <i>you have abandoned the love you had at first.</i> That is my condition. I do not want it to be my permanent address. Teach me to remember from where I have fallen. Bring me back to the place where the work was first given rather than performed. Let me do the works I did at first — not better works, not more works, but the same works, again, from love.",

    "Lord Jesus, you said to the disciples who had been working without ceasing: <i>Come away and rest a while.</i> I confess that I have not known how to receive that invitation, because rest has always felt like professional death. Teach me that the One who holds me in the palm of his hand does not require my perpetual motion as evidence that I am worth keeping. Let me learn to stop without the sky falling. Let me sit in the desolate place without immediately reaching for the next campaign. And in the stopping, meet me — not with a production schedule, but with yourself.",

    "Holy Spirit, where the work has become obligation, give me back the love. Where the Campaign has been running on its own momentum long after the heart left it, interrupt it. Where I have mistaken the cold for peace — the absence of expectation for the presence of God — wake me to the difference. And where the Quiet Exit has already gone further than I have admitted even to myself, would you stand at the door before it seals, and call me back to the labor that was once an offering.",

    "In the name of the One who, in Gethsemane, stayed when every human nerve said flee — and who did it not as professional obligation but as the deepest possible act of love — I pray.",

    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Performance Campaign and the Quiet Exit have been with you long enough that one careful reading will not retire them. What follows is a short list of next steps — honest, concrete, unhurried — for the work that has just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.",
     "Different lines will land. The Campaign will want to treat this walkthrough as a completed project and move to the next item on the list. Read it again anyway. The section that felt least relevant today may be the most necessary one in a month."),

    ("Take one tool, not six.",
     "Choose the single practice from Section 7 that is most directly relevant to where you are right now — not the most comfortable one, the most necessary one. Try it for two weeks before adding another. One posture, held long enough, begins to change the shape of the body."),

    ("Tell one person what you found.",
     "Not the whole document. One sentence: <i>I learned that my mechanism is the Performance Campaign, and my breakdown is the Quiet Exit — the place where the works continued and the love left them.</i> Tell it to someone who has the right to your interior. Notice what happens when the Campaign's private verdict is spoken to a safe witness. This is the first act of returning."),

    ("Sit with the Prodigal God.",
     "Tim Keller, <i>The Prodigal God.</i> Read it specifically for the elder brother sections. Keller's portrait of the elder brother is the most precise pastoral address to what the Performance's Quiet Exit is doing that exists in modern Christian writing. The elder brother had not stopped working. He had stopped working from love. That is your condition. Read it slowly."),

    ("Read Revelation 2:1-7 every morning for one week.",
     "Not as a performance goal. As an act of honest reckoning. Each morning, read the letter to the church at Ephesus and ask one question: <i>Am I doing the works I did at first, and from the love I had at first?</i> Then read C. S. Lewis, <i>The Weight of Glory</i> — the title essay specifically. Lewis's treatment of the longing to be noticed and the only source that can finally bear its weight is precisely what the Campaign needs to hear from outside its own vocabulary."),

    ("If the door has already closed further than you have admitted, ask for help.",
     "There are seasons when the Quiet Exit has gone too far to be interrupted alone — when the work continues and the love has been absent long enough that even the memory of it is difficult to locate. A wise pastor, a Christian counselor, a trusted elder who knows you off the field — these are not signs of failure. For the Performance specifically, asking for help without framing it as a project to be successfully completed is one of the most countercultural and most healing things on this list."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a son or daughter being loved into freedom "
    "by a Father who engraved your name on the palms of his hands before you ran a single race. "
    "The Campaign did not earn that love. The Quiet Exit cannot lose it. "
    "The works you did at first were the right works. The love you had at first is still available to you. "
    "Go back. The One who began the good work in you is faithful to complete it — "
    "and he has not yet issued the final statement on the story you are in the middle of."
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
        [Paragraph("WAS I SEEN HERE?", header_style), Paragraph("your nervous system\u2019s verdict", sub_style)],
        [Paragraph("WAS MY SOUL IN DANGER?", header_style), Paragraph("the deeper question", sub_style)],
    ]
    data = [header_row] + [["", "", ""] for _ in range(rows)]
    tbl = Table(data, colWidths=[col_w]*3, rowHeights=[0.48*inch] + [0.42*inch]*rows)
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
    """Generate the Performance Campaign + Quiet Exit (Verdict) walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='CAMP', primary_breakdown='VERD',
    primary_trigger='SIG', core_question='REM'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="PERFORMANCE  \u00b7  QUIET EXIT",
        title="Take 139 Walkthrough \u2014 Performance Campaign + Quiet Exit",
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
    story.append(Paragraph("The Performance Campaign \u00a0\u00b7\u00a0 The Quiet Exit", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Significance \u00a0\u00b7\u00a0 Core Question: Am I enough to be remembered?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cYou have abandoned the love you had at first\u2026<br/>"
        "remember therefore from where you have fallen;\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Revelation 2:4\u20135",
        ParagraphStyle("cqa", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 1: Opening \u2500\u2500
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read this slowly. The chapter that follows has been a long time in the running.")
    for p in OPENING_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 2: Trigger \u2500\u2500
    section_header(story, S, "SECTION TWO  \u00b7  YOUR TRIGGER",
                   "Significance.",
                   "The three-second moment when being made invisible fires an alarm.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will frame the answer as a campaign. Your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 3: Core Question \u2500\u2500
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I enough to be remembered?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "Two kinds of producing.",
                   "From fullness, or from need. Only one of them can stop.")
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table(rows=4))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 4: Mechanism \u2500\u2500
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Performance Campaign.",
                   "The runner. The achiever. The builder of visible competence.")
    for p in CAMP_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "What the Campaign produces, and what it costs.",
                   "The gift, the history, and the question it cannot answer.")
    for p in CAMP_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in CAMP_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Campaign.",
                   "Read the Campaign\u2019s own words. He has been faithful; let him speak.")
    letter_style = ParagraphStyle(
        "CampVerdLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for line in CAMP_LETTER_INSTRUCTION:
        story.append(Paragraph(line, letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in CAMP_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 5: Breakdown \u2500\u2500
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Quiet Exit.",
                   "The place your mechanism breaks: the works continue, and the love departs.")
    for p in VERD_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The church at Ephesus.",
                   "The works still standing. The love already gone.")
    for p in VERD_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in VERD_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions before you turn the page.",
                   "Write the most honest answer you have. Not the pastoral-sounding one.")
    for prompt in VERD_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same longing, in two directions.",
                   "The Campaign and the Quiet Exit are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=5)
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
                   "When the Campaign is overrunning.",
                   "Five practices for before the heart departs.")
    for name, desc in CAMP_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Quiet Exit has begun.",
                   "Six practices for interrupting the departure before it seals.")
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


# \u2500\u2500 STANDALONE TEST \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if __name__ == "__main__":
    import os
    import re

    class FakeSub:
        primary_mechanism = "CAMP"
        primary_breakdown = "VERD"
        primary_trigger = "SIG"
        core_question = "REM"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "performance_verd_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages using /Type /Page[^s] pattern
    page_count = len(re.findall(b"/Type /Page[^s]", pdf_bytes))

    # Grab a snippet from the letter constant
    raw_letter = CAMP_LETTER_INSTRUCTION[2]  # "I need to tell you something..."
    clean_letter = re.sub(r"<[^>]+>", "", raw_letter)
    snippet = clean_letter[:120]

    print(f"DONE: performance_verd.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB) — {out_path}")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet}")
