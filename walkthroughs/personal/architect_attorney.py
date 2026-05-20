"""Personal Walkthrough — Architect + Attorney.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disrespect trigger, "Am I protected?" core question.
~25 pages, 9 sections.
"""
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Paragraph, Spacer, KeepTogether, HRFlowable, Table, TableStyle,
    PageBreak, NextPageTemplate,
)

from ..base import (
    make_doc, make_styles, finalize_buffer, ensure_fonts,
    section_header, journal_lines, divider,
    PAGE_W, MARGIN_L, MARGIN_R,
    PAPER, INK, ACCENT, MUTED, RULE, HIGHLIGHT_BG,
)


# ──────────── PROSE ────────────

OPENING_BODY = [
    "Before you read any further, I want to do for you what a good counselor does in the first session. I want to lower the lights and slow the pace, because what we are about to look at is not a list of personality traits. It is a way of seeing how your soul has learned to keep itself safe in a world that has, in real and specific ways, failed to keep you safe.",
    "We are going to walk through your trigger \u2014 the moment your nervous system says <i>something is wrong here</i>. We are going to listen to the question underneath that moment, the one that has probably been with you since you were very small. We will name the strategy you have built to answer that question on your own, and the place that strategy collapses when it cannot hold any longer. And then, only then, will we put tools in your hands.",
    "If you were sitting across from me, I would say this. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who has not, in fact, left you to defend yourself; a Son who absorbed in his own body the worst possible version of the danger you fear; and a Spirit who is, at this very moment, more committed to your healing than you are.",
    "So read slowly. Argue with what does not fit. Stay with what does. Write in the margins. Pray when something catches in your throat, because that catch is usually the Lord saying, <i>look here, with me.</i> The goal of this walkthrough is not insight. The goal is a slightly freer life, lived in front of a God who has nothing to gain from your performance and nothing to lose by your honesty.",
    "Take your time. The chapter you are about to read about yourself has been a long time in the writing. It deserves a few hours of patient attention.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most people in your life have no idea it is happening. It usually lasts under three seconds. Someone interrupts you in a meeting. A driver cuts in front of you and does not wave. A family member rolls their eyes while you are still speaking. Your spouse uses a certain tone \u2014 not loud, not even unkind, just a particular flavor of dismissive \u2014 and something inside you tightens.",
    "On the surface, this may look like irritation, a small inconvenience that anyone would feel. In reality, your body has just registered what feels to it like a deeper signal. The signal is not <i>I have been inconvenienced.</i> The signal is closer to <i>I have just been told I do not matter.</i> And because your soul has long believed that not mattering is one short step from not being safe, the response is far larger than the offense.",
    "This is your trigger. The technical word for it is <b>disrespect</b>, but the word is doing more work than it looks like it is doing. It is not vanity. It is not pride, though pride is often quick to attach itself to it. It is the involuntary alarm that goes off when you sense that another person has, in some small or large way, declined to grant you the dignity you instinctively know you possess.",
    "C. S. Lewis, in <i>The Weight of Glory</i>, said the most terrible thing one human being can do to another is treat them as if they were nothing. Most adults around you would never knowingly do this. But you, more than most, can feel even the faintest version of it.",
    "Here is what is important to see, and to see without flinching. <b>Your sensitivity to disrespect is not random.</b> It is the residue of moments \u2014 usually early, often repeated, sometimes only a handful but unforgettable \u2014 in which someone with power over you used that power carelessly, or cruelly, or coldly, and you learned that the world cannot always be trusted to handle you with care.",
    "It might have been a parent who corrected you with contempt rather than instruction. It might have been a teacher who shamed you publicly. It might have been an older sibling whose disregard registered, week after week, that you were beneath their notice. It might simply have been a household in which feelings were not given air, and so the small dismissals piled up unnamed.",
    "Whatever its origin, the lesson lodged in you was this: <i>When people stop honoring me, something bad happens next.</i> And so your system learned to be vigilant. You read faces well. You catch tone. You feel the temperature of a room before others know it has changed. This is a gift \u2014 pastors and leaders depend on people like you \u2014 but it comes at a cost, because the same sensitivity that lets you notice a hurting parishioner also lets you feel, three times a day, the small slights that most people miss entirely.",
    "Before we go further, I want you to do something simple. Take a breath and answer two questions in writing. Not in your head \u2014 your head will spin the question; your hand will not.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past week, that you felt the disrespect signal fire. What happened, in two sentences?",
    "What was the size of the actual event, and what was the size of the response inside you? If they did not match, you have just located the trigger.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding.",
    "Yours is this: <b>Am I protected?</b>",
    "It is not the same as <i>Am I loved?</i>, though it sometimes wears that face. It is not <i>Am I competent?</i>, though you have probably built a great deal of competence as a way of trying to answer it. It is more primal than either. It is the question a small child asks at three in the morning when the wind is in the trees and the door is open a crack: <i>Is there someone between me and what could hurt me?</i>",
    "Most of us would prefer to believe we long ago outgrew that question. We have not. We have only moved it underground. The adult version sounds more sophisticated \u2014 <i>Can I trust this person? Will this organization protect me if things go wrong? Did my spouse really hear what I just said, or am I alone in this?</i> \u2014 but it is the same question. And for you, it does not stay quiet. It is awake most of the time.",
]

QUESTION_BODY_P2 = [
    "There is a reason theologians from Augustine to Calvin to your own pastoral tradition have insisted that the deepest human longings are God-shaped. The longing for protection is one of these. The Psalms \u2014 the prayer book Jesus himself prayed \u2014 return to this longing again and again.",
    "<i>The Lord is my rock and my fortress and my deliverer, my God, my rock, in whom I take refuge, my shield, and the horn of my salvation, my stronghold.</i> (Psalm 18:2)",
    "Notice the pile-up. Rock, fortress, deliverer, rock again, refuge, shield, horn of salvation, stronghold. David does not say it once and move on. He says it seven different ways because the question <i>Am I protected?</i> does not stay answered. It needs answering again in the morning. The Bible is not embarrassed by this. It hands you a hymnbook of people whose question was the same as yours.",
    "But \u2014 and this is where it gets harder for you than for most \u2014 the biblical answer to <i>Am I protected?</i> is not the answer your nervous system wants. Your nervous system wants <i>nothing bad will happen to you.</i> Scripture refuses to say that. Job did not get that answer. Joseph did not get that answer. Paul, who had every reason to expect divine air cover, did not get that answer; he got shipwrecks and beatings and a thorn in the flesh that never went away.",
    "What Scripture gives you is something stranger and, in the long run, better. It says: <i>You are protected, but not from everything. You are protected from the only thing that could finally undo you.</i> The fortress is real, but it does not surround your circumstances. It surrounds your soul.",
]

QUESTION_BODY_P3 = [
    "This is where you have to do some honest work, because the Architect in you has spent years trying to build the wrong kind of fortress. You have been constructing a perimeter around your circumstances \u2014 your reputation, your schedule, your finances, your children's choices, your church's stability \u2014 and calling it protection. It is not. It is exhaustion dressed up as faith.",
    "The real fortress is the one Jesus stepped into on your behalf when, in Gethsemane, he prayed <i>not my will but yours be done</i> \u2014 a prayer that did not protect him from anything, and that secured for you a kind of protection circumstances cannot give and cannot take away. Paul names it in Romans 8: <i>If God is for us, who can be against us? . . . Who shall separate us from the love of Christ? Shall tribulation, or distress, or persecution, or famine, or nakedness, or danger, or sword?</i> The list itself is a confession that all of those things will, in fact, come. Paul is not promising you a life without them. He is promising you that none of them can do the one thing your soul most fears \u2014 separate you from the love that holds you.",
    "So when you ask, <i>Am I protected?</i>, the honest pastoral answer is: <b>yes, in the place that finally matters; no, in many places that hurt anyway.</b> Both halves are true. Both halves have to be said. Soften either one and you will not be able to live with the other.",
]

ARCH_BODY_P1 = [
    "You have built something. You probably did not mean to build it; most architects of this kind do not. But over years and small decisions, you have constructed a way of moving through the world that we are going to call, throughout this walkthrough, <b>the Architect</b>.",
    "The Architect's strategy is simple and, on its face, admirable. <i>If I can think it through carefully enough, prepare for it thoroughly enough, anticipate the failure modes precisely enough, then nothing important will go wrong, and the people I love will be safe.</i> The Architect believes \u2014 not in his head, but in his bones \u2014 that suffering is largely a function of insufficient planning. The Architect is sure that if he had simply read the right book, asked the right question, foreseen the right contingency, the bad thing would not have happened. And so the Architect does not stop building.",
    "There is a great deal in Scripture that commends careful planning. Proverbs is full of it. <i>The plans of the diligent lead surely to abundance, but everyone who is hasty comes only to poverty.</i> (Proverbs 21:5) The Bible does not romanticize spontaneity at the expense of wisdom. So the Architect is not, in himself, a sin. He is a gift that has gone slightly feral.",
    "The trouble is not with planning. The trouble is with what the planning is for. Underneath your beautifully drafted blueprints is the conviction we already named: <i>If I do not protect myself and the people I love, no one will.</i> Which is, when you say it that plainly, a statement about God.",
]

ARCH_BODY_P2 = [
    "Tolkien, in his letters about <i>The Lord of the Rings</i>, said something that I think names what is happening inside you. He wrote that the ring of Sauron was a picture of the placing of one's life, or power, in some external object, which is thereby exposed to capture or destruction, with disastrous results to oneself. The Architect has done this with his systems. He has placed too much of his soul into his structures, and so every threat to a structure feels like a threat to the soul.",
    "I have sat with men and women like you \u2014 pastors, executives, parents of large families, leaders whose people depend on them \u2014 and watched the same thing happen over and over. The plan is so good that when it works, no one notices the cost. The cost shows up only on the day the plan fails, when the disproportion between the size of the failure and the size of the collapse becomes impossible to ignore.",
    "Your spouse may have seen this in you long before you did. The person closest to an Architect usually says some version of the same sentence: <i>You're not actually here. You're three meetings ahead of me.</i> They are right. The Architect is rarely fully in the room he is in, because he is securing the next three rooms.",
    "Hear me carefully. <b>The Architect is not your enemy.</b> He is a younger version of you who learned, in some real circumstance, that vigilance kept you safe and that lapses in vigilance cost you. He deserves your respect, not your contempt. But he is no longer twelve, and you are no longer in the household, the school, the relationship, that required him. He is working overtime on a building project that was finished years ago.",
]

ARCH_BODY_P3 = [
    "What does it look like to begin retiring him? Not firing him \u2014 he has been faithful. <i>Retiring</i> him, in the dignified sense of the word. Giving him fewer hours. Letting him still consult, still draft the occasional blueprint, but no longer carry the whole weight of your safety on his shoulders.",
    "It begins with naming the assumption he has been operating under. The assumption is: <i>God is good, but God is not detail-oriented enough to be trusted with the specifics.</i> The Architect would never say that out loud. He believes in God's sovereignty as a doctrine. But his calendar, his contingency plans, his nightly run-throughs of what could go wrong tomorrow \u2014 those tell a different story. They confess that, at the level where it counts, he believes the specifics are his problem.",
    "Letting go of that assumption is not a single decision. It is a practice, repeated daily, of handing back to God the rooms you have been securing on his behalf. It will feel, at first, like negligence. It is not. It is the slow recovery of the difference between <i>being a steward</i> and <i>being God</i>.",
    "Before we close this section, I want you to do something that may feel strange. I want you to write a letter to the Architect. Not <i>about</i> him. <i>To</i> him. Treat him as a real part of yourself, because he is. Thank him for what he has done. Tell him what you are now able to take off his desk. Tell him what you still need him to hold, and for how long. Be honest. He will know if you are pretending.",
]

ARCH_LETTER_INSTRUCTION = [
    "Use the lines below. If you need more space, continue in your journal \u2014 but begin here, where you can come back to it.",
]

ATT_BODY_P1 = [
    "Every mechanism has a place it breaks. Yours is called <b>the Attorney</b>, and you have probably been in the courtroom more recently than you would like to admit.",
    "Here is how it happens. The Architect has done his work \u2014 has planned, prepared, anticipated. Then something exposes a flaw in the plan. A meeting goes sideways. A sermon lands wrong. A family member levels a criticism that, even if half true, lands as a verdict on the whole. The Architect cannot fix it from his usual position, because the fix would require admitting the plan was not complete. So a different part of you takes the floor.",
    "The Attorney does not solve the problem. The Attorney <i>litigates</i> it. He marshals the evidence \u2014 the things you have done, the things they have not done, the context they did not understand, the precedent that proves you were right. He builds a brief. He sometimes delivers it out loud, in a tone that surprises the people who know you. More often he delivers it silently, late at night, to an imagined jury that will, in the morning, vindicate him.",
    "I want to say something here that I would only say to someone like you. On the surface, this may look like self-defense or righteous anger, and there are moments when one or both of those is appropriate. In reality, what is most often happening when the Attorney takes the floor is much sadder. The Attorney is not trying to win an argument. He is trying to prove he is safe. He believes, somewhere underneath the words, that if he can just establish that he was not in the wrong, the danger will recede.",
]

ATT_BODY_P2 = [
    "It will not. The Attorney has never, in his long career, succeeded in making you feel protected. He has only, on his best days, succeeded in making you feel temporarily un-accused. And then, within the hour, the same fear comes back and asks to be litigated again.",
    "Scripture is unusually direct about this pattern. Paul, who knew something about being misunderstood \u2014 <i>I have been falsely accused, slandered, treated as the scum of the world</i> \u2014 refused to put his soul's safety in the hands of his own self-defense. <i>It is the Lord who judges me</i>, he wrote to a Corinthian church that was hammering him. <i>Therefore do not pronounce judgment before the time, before the Lord comes.</i> (1 Corinthians 4:4-5)",
    "Notice what Paul did <i>not</i> do. He did not stop caring about the truth. He did not roll over. He kept defending the gospel and his apostleship vigorously. What he stopped doing was carrying the weight of the verdict himself. He handed it to Christ and got back to work. The Attorney in you has not yet learned to do this. He keeps thinking that if he tries one more case, this time he will get the verdict that finally settles the question.",
    "The cruelty of the Attorney is that he turns the people closest to you into the jury, and they did not ask for the job. Your spouse, your children, your elders, your friends \u2014 they become an audience whose approval you need in order to feel safe. This is not love. It is a kind of low-grade hostage situation, conducted with charm and reasonableness, and the people you love often cannot name why being around you in those seasons feels exhausting. It is exhausting because they are working a courtroom shift they never agreed to.",
]

ATT_BODY_P3 = [
    "If you want a single picture of what it looks like to step out of the courtroom, look at Jesus before Pilate. Pilate offered him a microphone. The Attorney in any of us would have taken it. Jesus did not. <i>Like a sheep that before its shearers is silent, so he opened not his mouth.</i> (Isaiah 53:7) Not because the case did not matter. Because the verdict had already been settled in the only court that finally counts.",
    "I am not asking you to go silent the next time you are misunderstood. There are moments to speak, and you usually know which ones they are. I am asking you to notice the moment the Architect quits and the Attorney takes the floor, and to recognize what he is really after. He is after the verdict <i>safe</i>, and he is trying to earn it. The gospel is the announcement that the verdict has already been spoken over you, and that the One who spoke it was not your accuser but your advocate. <i>If anyone does sin, we have an advocate with the Father, Jesus Christ the righteous.</i> (1 John 2:1)",
    "You already have the Attorney you need. He is not in your head. He is at the right hand of the Father, pleading your case better than you ever could, with evidence \u2014 his own blood \u2014 you could never have introduced.",
]

ATT_PROMPTS = [
    "Name the last courtroom session you ran in your own head. Who was on trial \u2014 you, or them?",
    "What verdict were you trying to earn? Write it in one sentence beginning, <i>If I could just prove that ___, I would feel safe.</i>",
    "What verdict has Christ already spoken over you that makes that sentence unnecessary?",
]

TWO_TOG_BODY = [
    "Now we put them next to each other, because the Architect and the Attorney are not two separate problems. They are the same fear, dressed in two suits.",
    "<b>The Architect is what your fear does when it has time.</b> The Attorney is what your fear does when it has run out of time. The Architect plans so the alarm will not have to ring. The Attorney argues when the alarm rings anyway. Together they form a closed loop, and the loop will run all your life if no one interrupts it.",
    "The pattern, in slow motion, looks like this. <b>(1)</b> You build. You prepare carefully, anticipate well, secure the perimeter around something that matters to you. <b>(2)</b> An event lands that the building did not anticipate. Someone disregards you, dismisses you, refuses to grant you the dignity you instinctively know you possess. <b>(3)</b> The trigger fires. Your body says, <i>something is wrong here.</i> <b>(4)</b> The question wakes up: <i>Am I protected?</i> <b>(5)</b> The Architect tries to answer it by rebuilding faster. <b>(6)</b> When the rebuild cannot catch up, the Attorney takes over and tries to answer it by argument. <b>(7)</b> Whether or not he wins the argument, the question is back inside the hour, and the loop restarts.",
    "What breaks the loop is not better planning, and it is not a better argument. It is a different answer to the question. Until you receive \u2014 really receive, not just affirm doctrinally \u2014 that you are already protected in the place that finally matters, the loop has nothing to push against. With that answer received, the loop begins, slowly, to lose its grip. The Architect drafts fewer blueprints. The Attorney leaves the courtroom earlier. Neither retires fully in this life, but both begin to work shorter hours.",
    "Below is your sequence, written as a short paragraph in your own words. Fill in the blanks. When you finish, read it aloud. The Architect and the Attorney both lose some of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, my body reads it as disrespect, and "
    "the old question wakes up \u2014 <i>am I protected?</i> My first move is to "
    "____________________ , because the Architect in me believes that if I "
    "can ____________________, the danger will pass. When that does not "
    "work, the Attorney takes the floor and argues that ____________________. "
    "What I am actually after, underneath all of it, is the verdict "
    "____________________ \u2014 a verdict Christ has already spoken over me in "
    "____________________ ."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a set of tools, each of which is small enough to carry in a pocket and useful enough to reach for. None of them will fix you. All of them, used over months, will loosen the grip of the loop you just named.",
    "I have divided them into two sets: tools for when the Architect is overworking (when you have time and your planning has tipped into anxiety) and tools for when the Attorney is on his feet (when an event has just fired the trigger and you can feel the courtroom assembling).",
]

ARCH_TOOLS = [
    ("Five-minute audit", "At the end of each day, write down one thing you planned for that did not need the level of preparation you gave it. Do not scold yourself; simply notice. Over a month, the Architect begins to see his own pattern from the outside, which is the first step toward retiring him."),
    ("The handed-back list", "Each morning, write the names of two or three specific situations \u2014 a meeting, a child, a sermon, a relationship \u2014 and after each one write the sentence: <i>This is yours today, Lord. I will steward, not secure.</i> Read it aloud. You will not feel it the first thirty mornings. By the sixtieth, something begins to give."),
    ("Stewardship vs. Sovereignty", "When you catch the Architect drawing up another contingency, ask him one question: <i>Is this stewardship, or am I trying to be sovereign?</i> Stewardship is what God has asked of you. Sovereignty is what he has reserved for himself. Most Architects mix the two without noticing."),
    ("The ten-minute Sabbath", "Once a day, set down every device, every plan, every list, and sit for ten minutes doing nothing productive. The Architect will tell you this is wasteful. He is wrong. It is the smallest possible rehearsal of the truth that the world does not, in fact, fall apart when you stop holding it up."),
    ("The Psalm that fits", "When you feel the urge to over-plan, open to Psalm 23, Psalm 27, Psalm 46, Psalm 91, or Psalm 121 \u2014 the protection psalms \u2014 and pray one of them aloud. Not to manage your feelings. To put your soul back inside a story bigger than the one the Architect is writing."),
    ("Confess the structure as worship", "Once a week, name one structure in your life \u2014 a plan, a system, a contingency \u2014 and ask, <i>am I trusting this, or am I trusting God through this?</i> If the honest answer is the former, confess it. Not dramatically. Just say it to the Lord and let him receive it. The Architect is starved when he is not allowed to keep his work secret."),
]

ATT_TOOLS = [
    ("The thirty-second pause", "When the trigger fires and you feel the Attorney rising, give yourself thirty seconds before you speak. Not to compose a better argument. To notice that you are about to litigate, and to ask whether the courtroom is necessary. Most often it is not."),
    ("Name the jury", "Ask yourself, silently, <i>who am I trying to convince right now?</i> If the answer is a person not in the room \u2014 a parent, a critic, an old voice \u2014 the Attorney has the wrong client. Dismiss the case."),
    ("The single sentence", "When you must speak, choose one sentence. Not a brief. Not a paragraph. One sentence that names the truth and stops. The Attorney is not allowed to call witnesses. This single discipline, practiced for a month, will change the temperature of your marriage."),
    ("The advocate prayer", "When the Attorney is loudest, pray these words: <i>Lord Jesus, you are my advocate. I do not need to be my own. I receive the verdict you have spoken over me.</i> Say it three times. The third time is usually when the courtroom begins to empty."),
    ("Write the brief and burn it", "If the argument will not leave you alone, write it out in full \u2014 every point, every witness, every counter \u2014 on paper. Then, slowly, tear the paper into pieces and throw it away. You have given the case its hearing. You do not have to deliver it to anyone."),
    ("Ask one trusted person", "Within twenty-four hours of a courtroom session, tell one trusted person \u2014 your spouse, an elder, a friend \u2014 that the Attorney was up last night, and ask them to pray. Secrecy is the Attorney's oxygen. Spoken aloud to a safe witness, he loses most of his power."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Architect in me, and you do not despise him. You know why I built him. You know which rooms in my history he was first asked to secure. Thank you that he has, in his way, kept me alive.",
    "But Father, he is tired, and I am tired, and the building is too large now for either of us to hold. Teach me to hand back to you the rooms you never asked me to carry. Teach me the difference between stewardship and sovereignty. Teach me, when the alarm fires and the old question wakes up \u2014 <i>am I protected?</i> \u2014 to hear your answer before I hear my own.",
    "Lord Jesus, when the Attorney rises in me and begins to assemble his evidence, would you remind me that you are at the right hand of the Father, pleading my case with your own blood as the only exhibit. I do not need to argue. I do not need to win. The verdict has already been spoken. Help me to receive it again today.",
    "Holy Spirit, where I am vigilant, give me peace. Where I am litigating, give me silence. Where I am securing my own perimeter, give me the courage to step inside the fortress that was built for me before the foundation of the world.",
    "In the name of the One who, before Pilate, did not open his mouth \u2014 because he knew the verdict was already his \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Architect and the Attorney have been with you a long time, and they will not retire after one reading. What follows is a short list of next steps \u2014 some practical, some longer-term \u2014 for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different lines will land. The Architect will resist a second reading; do it anyway."),
    ("Take one tool, not six.", "Choose a single practice from Section 7 and try it for two weeks. Tools used poorly are worse than tools never tried."),
    ("Tell one person what you read.", "Not the whole document. One sentence: <i>I learned my mechanism is the Architect, and my breakdown is the Attorney.</i> Watch what happens when the secrecy is broken."),
    ("Re-read the protection psalms.", "Psalm 23, 27, 46, 91, 121. Pray one aloud each morning for a week. Notice which lines you cannot get through without stopping."),
    ("Read further on suffering.", "Tim Keller, <i>Walking with God through Pain and Suffering.</i> David Powlison, <i>God's Grace in Your Suffering.</i> Elisabeth Elliot, <i>No Graven Image.</i> Each is a faithful companion for the work you are doing."),
    ("If you are stuck, ask for help.", "There are seasons when the Architect and the Attorney are too entrenched to dislodge alone. A wise pastor, a Christian counselor, a trusted friend who knows you \u2014 these are not signs of failure. They are part of the answer to your prayer."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a son or daughter being loved into freedom by a Father who has all the time in the world. "
    "Go gently with yourself. The One who began the good work in you will be the one to finish it."
)


def _three_column_table(rows=7):
    """Three-column journal table for Section 3's 'three columns by hand' exercise."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE EVENT", header_style), Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WAS I PROTECTED HERE?", header_style), Paragraph("your nervous system's question", sub_style)],
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
    """Generate the Architect+Attorney walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor's Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR'S WALKTHROUGH",
        cover_right_label="ARCHITECT  \u00b7  ATTORNEY",
        title="Take 139 Walkthrough \u2014 Architect + Attorney",
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
    story.append(Paragraph("The Architect &nbsp;\u00b7&nbsp; The Attorney", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disrespect &nbsp;\u00b7&nbsp; Core Question: Am I protected?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cOnly if you make God matter the most&nbsp;\u2014&nbsp;<br/>"
        "which means only if you glorify him and give him the glory&nbsp;\u2014&nbsp;<br/>"
        "will you have a safe life.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Tim Keller, <i>Walking with God through Pain and Suffering</i>",
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
                   "Disrespect.",
                   "The three-second moment that keeps happening to you.")
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
                   "Your head will spin the question; your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=5)
        story.append(Spacer(1, 14))
    story.append(PageBreak())

    # ── SECTION 3: Core Question ──
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I protected?",
                   "The wound the alarm is guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "What Scripture actually says.",
                   "A stranger and, in the long run, better answer.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "The wrong kind of fortress.",
                   "Exhaustion dressed up as faith.")
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "Where was my soul actually in danger? Where was it not?")
    story.append(Paragraph(
        "Use the table below. In the first column, name an event from the last week. "
        "In the second, answer the question your nervous system was asking: "
        "<i>was I protected here?</i> In the third, answer the deeper question: "
        "<i>was the part of me that finally matters &mdash; my soul, my standing before "
        "God &mdash; at any point in danger?</i>",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table())
    story.append(PageBreak())

    # ── SECTION 4: Mechanism ──
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Architect.",
                   "What you have built, and what it was built for.")
    for p in ARCH_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "What Tolkien saw.",
                   "The cost of placing your soul in your structures.")
    for p in ARCH_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "Retiring him, not firing him.",
                   "The slow recovery of the difference between stewardship and sovereignty.")
    for p in ARCH_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter to the Architect.",
                   "Write to him directly. He has been faithful; speak to him as one.")
    for p in ARCH_LETTER_INSTRUCTION:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Paragraph("Dear Architect,", S["Prompt"]))
    journal_lines(story, n=18)
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Attorney.",
                   "The place your mechanism breaks, and the courtroom it builds.")
    for p in ATT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "What the Attorney is really after.",
                   "Not to win the argument. To prove he is safe.")
    for p in ATT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The Advocate you already have.",
                   "The case has been settled in the only court that finally counts.")
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
                   "The same fear, in two suits.",
                   "Architect and Attorney are not two problems. They are one loop.")
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
    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "What to do when you feel the loop start.",
                   "Small enough to carry; useful enough to reach for.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())

    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Architect is overworking.",
                   "Six practices for the time before the alarm fires.")
    for name, desc in ARCH_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Attorney is on his feet.",
                   "Six practices for the moment the courtroom assembles.")
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
