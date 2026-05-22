"""Personal Walkthrough — Architect + Flood.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Disrespect trigger, "Am I protected?" core question.
~25 pages, 9 sections.

Key insight: The Architect holds everything in under perfect blueprints until the
pressure has been building for months — then the dam breaks all at once: tears,
accumulated grievance, an unsorted avalanche. The pastoral move is to learn the
spiritual discipline of small, regular release — confession, lament, the Psalms of
complaint — before the dam goes.
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
    "Before you read any further, I want to do for you what a good pastor does in a long conversation — lower the lights, slow the pace, and make it safe to say the true thing. What you are about to read is not a personality survey or a list of traits to be improved. It is a careful look at the way your soul has learned to hold itself together in a world that has, in real and specific ways, failed to hold you.",
    "If you were sitting across from me, I would say this. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who has not abandoned you to manage your own safety; a Son who absorbed in his body the full weight of the danger you most fear; and a Spirit who is, at this very moment, more committed to your freedom than you are.",
    "There is something particular about your profile that I want you to hear before we go further. You are, by temperament, someone who holds things together — who plans, who prepares, who builds the structures that keep the people you love from harm. You are good at carrying. What you may not yet fully see is that carrying too long, without the small, regular releases that keep the soul from going rigid, is one of the most dangerous things a person like you can do. Not dramatic danger. Slow danger. The kind that accumulates quietly behind perfect blueprints, until one day something gives, and everything held in comes out at once — in a heap, in a way that frightens both you and the people you love.",
    "This walkthrough is about that moment. But more than the moment, it is about the spiritual practice that could prevent the moment — the practice of small, regular lament, of honest prayer, of the kind of complaint before God that the Psalms model and that the Architect almost never allows himself.",
    "So read slowly. Argue with what does not fit. Write in the margins. Pray when something catches in your throat, because that catch is usually the Lord saying, <i>look here, with me.</i> The goal is not insight alone, but a somewhat freer life — one in which the pressure does not have to build until it overwhelms. Take your time. The chapter you are about to read about yourself has been a long time in the writing.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and most of the people in your life do not know it is happening. It moves fast — under three seconds, usually. Someone takes credit for your work in a meeting. A colleague bypasses you on a decision that was yours to make. Your spouse uses a tone that is not loud, not cruel, just slightly dismissive — a half-degree of condescension — and something inside you tightens immediately.",
    "On the surface, this registers as irritation. A small inconvenience. In reality, your body has just detected what it reads as a more serious signal. The signal is not <i>I have been inconvenienced.</i> The signal is something closer to <i>I have just been told that my dignity does not matter here</i> — and because your soul has long carried the conviction that disregarded dignity is one short step from genuine danger, the response is considerably larger than the offense.",
    "This is your trigger. We call it <b>disrespect</b>, but the word is doing more work than it looks like it is doing. It is not vanity. It is not a fragile ego, though the ego is quick to attach itself to the genuine wound and complicate things. It is the involuntary alarm that fires when another person has, in some small or large way, declined to honor your personhood — and in doing so has activated something that was written in you long before you had the vocabulary for it.",
    "C. S. Lewis, in <i>The Weight of Glory</i>, observed that the most terrible thing one human being can do to another is to treat them as less than human — to erase them, even momentarily, from the category of those who deserve recognition. Most people would never do this intentionally. But you, more than most, feel even the faintest version of it. You notice the tone. You read the room. You catch the microsecond of dismissal before the other person has finished speaking.",
    "This is not a character flaw. It is a form of sensitivity, and it has real gifts. People like you make exceptional pastors, leaders, and friends, because you notice what others miss. But it comes at a cost, because the same attunement that helps you see a hurting parishioner also registers, three times a day, the small slights that most people shed before they reach the car.",
    "Here is the harder thing to see, and to see without flinching. <b>Your sensitivity to disrespect is not random.</b> It is the residue of moments — usually early, sometimes only a handful, but lodged deeply — in which someone with genuine power over you used that power carelessly, or coldly, or with contempt, and you learned that the world could not always be trusted to handle you with care.",
    "It might have been a parent who dismissed your efforts with a word. A teacher who corrected you publicly, with a pleasure you still remember. A household in which the emotional climate was unpredictable, and you learned early that vigilance — reading faces, anticipating moods, staying ahead of the change — was how you survived the unpredictability. Whatever its precise origin, the lesson lodged in you like a nail: <i>when people stop honoring me, something bad happens next.</i>",
    "Before we go any further, I want you to pause and write. Not in your head — your head will perform the question; your hand will not.",
]

TRIGGER_PROMPTS = [
    "Name the most recent time, in the past week, that the disrespect signal fired in you. What happened? Write it in two sentences.",
    "Describe the size of the actual event, and then describe the size of the response inside you. If they did not match, you have just located the trigger.",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm is guarding.",
    "Yours is this: <b>Am I protected?</b>",
    "It is not the same as <i>Am I loved?</i>, though it sometimes wears that face. It is not <i>Am I competent?</i>, though you have built enormous competence as a partial answer to it. It is more primal than either. It is the question a child asks in the dark when the floorboard creaks and the door is ajar: <i>Is there someone standing between me and what could hurt me?</i>",
    "Most of us prefer to believe we outgrew that question decades ago. We have not. We have only moved it underground. The adult form sounds more measured — <i>Can I trust this person? Will this institution protect me if things go wrong? Does my spouse actually hear what I am carrying, or am I managing this alone?</i> — but it is the same question, wearing grown-up clothes. And for you, it does not stay quiet. It is awake most of the time, scanning.",
    "The theologians from Augustine to Calvin have insisted that the deepest human longings are God-shaped — that what we most urgently seek, in the wrong places, is something only God can provide. The longing for protection is one of these. It was written into the fabric of what you are, not as a defect but as a declaration: you were made for a world in which you would be held. The problem is that this world is not yet that world.",
]

QUESTION_BODY_P2 = [
    "The Psalms — the hymnbook Jesus himself prayed from beginning to end — return to this longing with a frequency that should startle us. David, who faced lions and kings and armies and betrayal, kept asking the same question in a hundred different forms, and the psalter handed him a hundred different ways to ask it.",
    "<i>The Lord is my rock and my fortress and my deliverer, my God, my rock, in whom I take refuge, my shield, and the horn of my salvation, my stronghold.</i> (Psalm 18:2)",
    "Count the images. Rock, fortress, deliverer, rock again, refuge, shield, horn of salvation, stronghold. David does not name the protection once and move on. He says it seven ways in a single verse because the question <i>Am I protected?</i> does not stay answered. It needs answering again the next morning, and the morning after that. The Bible is not embarrassed by this. It hands you a prayer book written by people whose question was exactly yours.",
    "But — and this is where it gets genuinely difficult — the biblical answer to <i>Am I protected?</i> is not the answer your nervous system most wants to hear. Your nervous system wants <i>nothing will harm you.</i> Scripture will not say that. Job was not given that answer. Joseph was not given that answer. Paul — who had every theological reason to expect divine protection — was given shipwrecks and beatings and a thorn that never went away. The Bible does not clean this up.",
    "What Scripture gives you is something stranger and, in the long run, more durable. It says: <i>You are protected, but not from everything. You are protected from the one thing that could finally undo you.</i> The fortress is real, but it does not surround your circumstances. It surrounds your soul.",
]

QUESTION_BODY_P3 = [
    "This is where the honest work begins, because the Architect in you has been constructing, for years, the wrong kind of fortress. The blueprints are beautiful. The work is impressive. But what you have been trying to build is a perimeter around your circumstances — your reputation, your relationships, your family's wellbeing, your church's stability — and calling it security. It is not security. It is exhaustion that has learned to look like faithfulness.",
    "The real fortress is the one Jesus stepped into on your behalf when, in Gethsemane, he prayed <i>not my will, but yours be done</i> — a prayer that did not protect him from suffering, and that secured for you a protection that no circumstance can give and no circumstance can take. Paul names it in Romans 8 with a list that is itself a concession: <i>Who shall separate us from the love of Christ? Shall tribulation, or distress, or persecution, or famine, or nakedness, or danger, or sword?</i> The list is a confession that all of these things will, in fact, come. Paul is not promising you a life without them. He is promising that none of them can do what your soul most fears — separate you from the love that holds you.",
    "So when you ask, <i>Am I protected?</i>, the honest pastoral answer is: <b>yes, in the place that finally matters; no, in many places that hurt anyway.</b> Both halves must be held. Soften either one and you cannot live honestly with the other.",
    "Before we move on, take a moment with the question below. Write slowly.",
]

ARCH_BODY_P1 = [
    "You have built something. You probably did not intend to build it with quite this much weight on it — most architects of this particular kind do not. But over years and dozens of small decisions, you have constructed a way of moving through the world that we are going to call, throughout this walkthrough, <b>the Architect</b>.",
    "The Architect's strategy is straightforward and, on its surface, admirable. <i>If I can think this through carefully enough, prepare for it thoroughly enough, anticipate the failure modes precisely enough, then nothing important will go wrong, and the people I love will be kept from harm.</i> The Architect believes — not in his head but in his bones — that suffering is largely a function of insufficient preparation. He is sure that if he had simply read the right book, asked the right question, built one more contingency into the plan, the bad thing could have been avoided. And so the Architect does not stop building.",
    "Scripture commends careful planning. Proverbs is full of it. <i>The plans of the diligent lead surely to abundance, but everyone who is hasty comes only to poverty.</i> (Proverbs 21:5) The Bible does not romanticize impulsiveness. The Architect's diligence is a genuine gift, and it is worth saying plainly: you are not wrong to plan. You are not wrong to prepare. You are not wrong to carry weight for the people who depend on you.",
    "The trouble is not with planning. The trouble is with what the planning has become. Underneath your carefully drafted blueprints is the conviction we have already named: <i>If I do not protect myself and the people I love, no one will.</i> When you say it that plainly, you can hear what it confesses about God.",
]

ARCH_BODY_P2 = [
    "J. I. Packer, in <i>Knowing God</i>, wrote something that helps architects like you see themselves clearly. He observed that the root sin of humanity is not gross immorality but the more respectable sin of living as though God were not immediately and continuously necessary — conducting one's affairs as a competent manager who occasionally checks in with an absentee owner. The Architect does not think of himself as autonomous. He believes in God. But his calendar, his contingencies, his nightly rehearsals of what could go wrong tomorrow — those tell a different story. They confess that, at the level where decisions are actually made, he operates as though the specifics are his problem and God's sovereignty is a doctrine rather than a present reality.",
    "The person closest to an Architect usually says some version of the same sentence, and you may have heard it. <i>You're not actually here with me. You're three moves ahead.</i> They are right. The plan is so beautiful that when it works, no one sees the cost. The cost becomes visible only on the day the plan fails, when the distance between the size of the failure and the size of the internal collapse is impossible to explain to anyone watching.",
    "Hear me carefully. <b>The Architect is not your enemy.</b> He is a younger version of you who learned, in some real circumstance, that vigilance kept things together and that lapses in vigilance could cost you something important. He deserves your respect. He has been faithful. But he is no longer twelve, and you are no longer in the household that first required him. He is working overtime on a project that was, in important ways, completed long ago. The assumption underneath the overtime is worth naming plainly: <i>God is good, but God is not detail-oriented enough to be trusted with the specifics.</i> The Architect would never say that aloud. But his behavior tells the story his words do not.",
]

ARCH_BODY_P3 = [
    "Letting go of that assumption is not a single decision. It is a practice, repeated daily, of handing back to God the rooms you have been securing on his behalf. It will feel, at first, like negligence. It is not. It is the slow recovery of the difference between stewardship — which God has asked of you — and sovereignty — which he has reserved for himself.",
    "There is one more thing to say about the Architect before we move on to where he breaks, and it is the thing that most directly prepares you for what follows. The Architect, in his commitment to holding things together, has almost certainly learned to suppress the small releases that keep the soul from going rigid. He does not complain easily, because complaint feels like admitting the plan has a gap. He does not lament easily, because lament feels like losing ground. He does not pray the Psalms of complaint — Psalm 13, Psalm 22, Psalm 88 — because they sound, to him, like weakness. And so the pressure builds, silently and steadily, behind the very competence that looks, from the outside, like health. What the Architect has forgotten is that those psalms were written precisely for him. David — the military strategist, the man who could lay out a battle plan with genius — was also the man who prayed, <i>How long, O Lord? Will you forget me forever?</i> (Psalm 13:1) David was not collapsing when he wrote that. He was doing the spiritual work that kept him from collapsing. He was releasing the pressure in small doses, before the dam could go.",
    "The letter exercise that follows this section is an invitation into that kind of small release. The Architect has been carrying something. I want you to let him say it.",
]

ARCH_LETTER_INSTRUCTION = [
    "Below, write a letter from the Architect — in his own voice — to you, the person who has been housing him. Let him name what he is afraid of. Let him say the thing he has never been allowed to say aloud. The letter is not for performance. It is not for anyone else's eyes. It is for honest reckoning.",
    "A model first, to prime the voice. Then three prompts to continue on your own.",
]

ARCH_LETTER_MODEL = """Dear friend,

I have to be honest with you, because I think it is past time.

I am afraid. Not of any one thing — I have worked very hard to make sure there is no single point of failure — but of the accumulation of things I cannot control, things that do not respond to planning, things that could go wrong in the night when I am not watching. I am afraid of the moment when you need me and I have run out of blueprint. I am afraid you will discover that all the structures I built were, in the end, not enough, and that you will conclude from that discovery that the fault was mine — that I was insufficient. That I failed you.

I know that you have sometimes wished I would just stop. Stop anticipating. Stop preparing. Stop worrying about the room we haven't entered yet. I have heard that. I have not been able to stop, because stopping feels, from inside, like abandoning you to whatever the next room contains. I am not sure I know how to love you without securing you. And I am not sure what I am without the work.

That is the thing I most needed to say. I have made myself necessary, and I am not sure that is entirely an accident. As long as you need me, I exist. As long as the building requires an architect, I have a place. The thought of genuine rest — real rest, where the blueprints are in someone else's hands — does not feel like peace to me. It feels like disappearing.

With more honesty than I have managed before,
The Architect"""

FLOOD_BODY_P1 = [
    "Every mechanism has a place it breaks. For the Architect, the breaking looks nothing like what you would expect from the outside, and it probably surprises you every time.",
    "Here is what happens. The Architect has been building. He has done his work faithfully — planned, prepared, anticipated, held the weight. Then something arrives that the plan did not account for. Not always a single large event. Sometimes it is an accumulation of small ones, each of which was manageable on its own, but which have been stacking up behind the infrastructure for weeks, or months, or longer. A recurring tension with a colleague that was never quite addressed. A pattern in your marriage that you have been documenting internally but have not yet brought to the table. A private grief, a low-grade loneliness, a sense that the people closest to you have been receiving your organizational competence but not the person underneath it. The building looks solid from the outside. Inside, the pressure has been building for a long time.",
    "Then something lands — often something small, disproportionately small — and it acts as the last weight on a structure that has been absorbing weight for months. And what happens next is not an argument. It is not a calm and organized presentation of grievances. It is a flood.",
    "We call it <b>the Flood</b>, and the word is carefully chosen. A flood does not build — it releases. A flood does not discriminate — it carries everything that has been waiting behind the dam. Tears that have been held for months. Grievances that are real but that arrive unsorted, layered on top of one another, undifferentiated by size or relevance. Intensity that does not match, apparently, the event that triggered it. And over it all, a kind of relief — a terrible, exhausting relief — that it is finally out.",
]

FLOOD_BODY_P2 = [
    "I want to say something here that I would only say to someone like you, and I want to say it with precision. What you are experiencing during a Flood is not a loss of control, exactly. It is the consequence of a particular kind of self-control that has been applied for too long, to too many things, without adequate release. The Architect is exquisitely good at holding. He is not trained in the discipline of releasing a little at a time. And so the only release available to him, after the structure has held long enough, is total release.",
    "David Powlison, in <i>Good and Angry</i>, observed that unexpressed emotions do not disappear — they compound. What is not grieved becomes a weight. What is not confessed becomes a pressure. What is not lamented accumulates behind the silence and eventually finds its exit, usually through a crack you did not anticipate. The Architect's mistake is not that he has feelings. It is that he has filed them, rather than prayed them.",
    "Here is what the Flood is looking for, underneath the intensity. The taxonomy of your profile names it with unusual clarity: you want to be <i>seen — fully, finally.</i> You have been managing and containing yourself for so long, and at the moment of the Flood, what you most need is for someone to see the whole thing — not the composed professional, not the careful strategist, but the person who has been underneath all of that, carrying weight in the dark. The Flood is, in its deepest grammar, a bid for witness.",
    "The cruelty of the Flood — and it is genuinely cruel, to you and to the people you love — is that it arrives in a form that makes witness almost impossible. Unsorted grief is very hard to receive. Accumulated grievances that arrive simultaneously are very hard to address. The person being flooded often does not know which item to respond to first, and the person doing the flooding is often not sure which item matters most. The bid for witness becomes, in the intensity of the moment, a kind of drowning that no one is equipped to prevent.",
]

FLOOD_BODY_P3 = [
    "Scripture is unusually direct about the alternative. The Psalms of complaint — psalms that theologians call the psalms of lament — are precisely the small, regular release that the Architect suppresses and the Flood is desperate for. <i>How long, O Lord? Will you forget me forever?</i> (Psalm 13:1) <i>My God, my God, why have you forsaken me? Why are you so far from saving me?</i> (Psalm 22:1) These are not the words of a man who has lost faith. They are the words of a man doing the spiritual discipline of honest complaint before God — releasing, in a purposeful way, the pressure that otherwise compounds into an avalanche. Martyn Lloyd-Jones observed that the psalms of complaint teach the church something it tends to suppress in its rush toward resolution: that it is more honest, and more faithful, to cry out in the dark than to perform a peace you do not have.",
    "The unique pastoral word for the Architect+Flood is this: <b>learn the discipline of small, regular release before the structure fails.</b> Confession before the accumulation. Lament before the overflow. The Psalm of complaint prayed weekly, not only on the day of collapse. This is not weakness. It is what David did. It is what Jesus did, when he prayed in Gethsemane — openly, in agony, in front of witnesses — before the worst thing happened. He was not composed at the cross because he was suppressing; he was composed because he had been releasing honestly all the way to the cross.",
]

FLOOD_PROMPTS = [
    "Think of the last time the Flood happened — the last time everything came out at once, in a way that surprised you or the people around you. What had been building, and for how long?",
    "What was the small event that finally broke the structure? And what would it have taken — what small, earlier release — to prevent the break?",
]

TWO_TOG_BODY = [
    "Now we put them side by side, because the Architect and the Flood are not two separate problems. They are the same person in two different moments — one before the pressure gives, and one after.",
    "<b>The Architect is what your soul does when it has time.</b> The Flood is what your soul does when the time has run out. The Architect plans so the dam will never break. The Flood is what happens when the dam breaks anyway. Together they form a cycle, and the cycle will run for the rest of your life if nothing interrupts it.",
    "The pattern, in slow motion, looks like this. <b>(1)</b> You build. You carry. You hold. You prepare carefully, absorb the weight that comes, maintain the external competence. <b>(2)</b> An event lands — often a small one — that disrespects you, that signals to your body that your dignity is not being honored, that the plan is not holding. <b>(3)</b> The trigger fires: <i>something is wrong here.</i> <b>(4)</b> The question wakes up: <i>Am I protected?</i> <b>(5)</b> The Architect tries to answer it by building faster, holding tighter, suppressing whatever is rising in order to maintain the structure. <b>(6)</b> The suppression works, until it doesn't. The accumulated weight behind the suppression finds a crack. <b>(7)</b> The Flood comes — tears, accumulated grievance, unsorted intensity — and everything the Architect held in for weeks or months exits simultaneously. <b>(8)</b> Afterward, the Architect is ashamed of the Flood, resolves to hold tighter next time, and the cycle restarts.",
    "What breaks the cycle is not better planning, and it is not stronger willpower. It is a different practice: the regular, small, honest release of what you are actually carrying to a God who is actually listening. Until the Architect learns to do this — to pray complaint as well as petition, to lament as well as praise, to say to God what he cannot yet say to anyone else — the pressure will keep building until the structure fails. With this practice in place, slowly, the Floods become less catastrophic, and then less frequent, and eventually rare.",
    "Below is your sequence. Fill in the blanks. Read it aloud when you are done. The Architect and the Flood both lose some of their power when they hear themselves named.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, my body reads it as disrespect, and "
    "the old question wakes up \u2014 <i>am I protected?</i> My first move is to "
    "____________________, because the Architect in me believes that if I "
    "can hold it together, the danger will pass. What I do not usually "
    "notice is that I have been carrying ____________________ for "
    "____________________, and that the holding has been adding pressure "
    "rather than preventing it. When the structure finally fails, the Flood "
    "releases everything at once \u2014 the accumulated ____________________ "
    "that needed to be said, and wasn\u2019t. What I actually needed, before "
    "the Flood, was to release a little of it to ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of practices — each simple enough to actually use and durable enough to make a difference. None of them will resolve everything. All of them, used consistently over months, will loosen the grip of the cycle you have just named.",
    "I have divided them into two sets: tools for the Architect in his overworking mode (when you have time and your planning has tipped into anxiety and suppression) and tools for the moment of or after the Flood (when the structure has failed and you are in or recovering from the overflow). The integration at the end names the single practice that connects both.",
]

ARCH_TOOLS = [
    ("The evening small release", "At the end of each day, before you review tomorrow's agenda, write two sentences: one naming something you are worried about, and one handing it to God by name. Not a performance of trust — an honest transfer. <i>Lord, I am carrying this and I do not know how to fix it. It is yours.</i> The Architect is most dangerous when he keeps his worries classified. Make them spoken."),
    ("The Psalm of complaint, weekly", "Once a week — perhaps Sunday evening, when the week is still a blank — read a lament psalm aloud. Psalm 13, Psalm 22, Psalm 42, Psalm 88. Not as a devotional exercise but as a practice of learning to say to God what is actually true. You may feel, at first, that these psalms do not represent you. Persist. They were written for people exactly like you."),
    ("Stewardship vs. Sovereignty, daily", "When you catch the Architect drawing up a new contingency plan, ask him one question: <i>Is this stewardship, or am I trying to be sovereign?</i> Stewardship is what God has asked of you. Sovereignty is what he has reserved for himself. Most Architects confuse the two so routinely that the question, asked honestly, produces immediate clarity."),
    ("Name one thing you cannot fix", "Each morning, name one situation — a person, a problem, a relationship, a piece of your church's life — that you cannot resolve through planning. Sit with it for ninety seconds without drafting a solution. This is not passivity. It is the rehearsal of creatureliness, and it is one of the most important things an Architect can practice."),
    ("The ten-minute Sabbath", "Once a day, set down every device, every plan, every list, and sit for ten minutes doing nothing productive. The Architect will tell you this is wasteful. He is wrong. It is the smallest possible rehearsal of the truth that the world does not, in fact, depend on your vigilance. It is still standing at the end of the ten minutes. It will be standing at the end of your life."),
]

FLOOD_TOOLS = [
    ("Name it before it is a flood", "When you feel the pressure building — when the weight behind the structure has been growing for more than a week — say it to someone. Not the whole accumulation. One sentence: <i>I have been carrying something I haven't named yet.</i> This single practice, done early, prevents most Floods. The Flood happens because the naming was delayed too long."),
    ("After the Flood: the sorting conversation", "In the hours after a Flood — not during it, not immediately after, but once the waters have receded — sit with the person most affected and do the work of sorting. <i>Of everything that came out, what was the thing I most needed you to hear? What was the accumulated weight I had been carrying?</i> The Flood itself is often unsortable; the sorting conversation afterward is the actual repair."),
    ("The apology with a boundary", "After a Flood, the Architect often over-apologizes for the intensity without naming the truth that produced it. Try this instead: <i>I am sorry for the way that came out. The intensity was real, and it was mine. But the thing underneath it was also real, and I want to find a better way to bring it to you earlier.</i> Honesty about both the form and the content."),
    ("The pre-flood prayer", "When you feel the structure starting to strain — when you sense that you have been holding something for too long — pray Psalm 13 or Psalm 22 aloud. Not as a mood management technique, but as an act of releasing what you are carrying to the only One who can actually hold it. The Flood is often prayer that has been delayed until it is no longer orderly."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Architect in me, and you do not despise him. You know why he was built. You know which rooms in my early life first required him, and the faithfulness with which he has tried to keep things from falling apart. Thank you that he is, in his way, a kind of love. But Father, he does not know how to release. He only knows how to hold. And the holding has been going on for longer than is good for either of us. Teach me the discipline I have avoided: the small, honest prayer before the pressure builds too high. Teach me to bring my complaint to you — not as spiritual performance, but as genuine transfer of what I cannot carry alone.",
    "Lord Jesus, when the Flood comes — when everything I have been holding exits at once, and I am ashamed of the intensity and the disorder — remind me that you are not ashamed of me in my breaking. You wept at Lazarus's grave. You prayed in agony in Gethsemane, in front of witnesses. You are not a God who handles only the composed and competent version of my soul.",
    "Holy Spirit, where I am holding too long, give me the courage of small release. Where I have already flooded and am now rebuilding the walls higher, give me instead the grace to leave a door in the structure — a door that opens regularly, in prayer, in honest confession, in lament — so that the pressure does not have to find its own crack.",
    "In the name of the One who said, <i>Come to me, all who are weary and heavy laden, and I will give you rest</i> — because he knew there would be people who had been carrying things that were never theirs to carry alone — I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Architect has been with you for a long time, and the Flood has surprised you more than once. Neither will retire after a single reading. What follows is a short list of next steps — some immediate, some long-term — for the work you have just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different sentences will land. The Architect will resist a second reading; do it anyway. The Flood may look different once the waters have receded from the first reading."),
    ("Take one tool, not five.", "Choose a single practice from Section 7 and try it for two weeks before adding another. The Architect's instinct is to implement all six simultaneously. That instinct is itself part of the pattern."),
    ("Read the psalms of lament.", "Read Psalm 13, 22, 42, 73, and 88 in a single sitting. Notice which ones you cannot get through without stopping. Those are the ones the Spirit is pointing you toward. Return to them weekly."),
    ("Read further on carrying and release.", "Tim Keller, <i>Walking with God through Pain and Suffering</i> — especially the chapters on lament. C. S. Lewis, <i>A Grief Observed</i> — not because your situation mirrors his, but because Lewis shows you what it looks like to be an intelligent, composed man who stopped pretending and started being honest with God. David Powlison, <i>Good and Angry</i> — on what unexpressed emotion does, and the spiritual practice of bringing it to God."),
    ("Tell one person what the Flood is.", "Not the whole document. One sentence: <i>I have a pattern of holding things in too long, and then everything comes out at once, and I want to learn to release earlier.</i> Say it to your spouse, or to a trusted elder, or to a Christian friend who knows you. Secrecy is the dam's structural material. Spoken aloud to a safe witness, the pressure begins to decrease."),
    ("If you are stuck, ask for help.", "There are seasons when the Architect and the Flood are too entrenched to shift alone. A wise pastor, a Christian counselor, a trusted friend — these are not signs of failure. They are part of the answer to the prayer you just prayed."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a son or daughter being loved into freedom "
    "by a Father who has all the time in the world and who is not, not even slightly, "
    "surprised by your flood. The One who began the good work in you "
    "will be the one to finish it \u2014 and he does his best work "
    "in people who have stopped pretending they can finish it themselves."
)


def _three_column_table(rows=7):
    """Three-column journal table for the core question exercise."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE EVENT", header_style), Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WAS I PROTECTED HERE?", header_style), Paragraph("your nervous system\u2019s answer", sub_style)],
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
    """Generate the Architect+Flood walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="ARCHITECT  \u00b7  FLOOD",
        title="Take 139 Walkthrough \u2014 Architect + Flood",
    )

    story = []

    # ── COVER ──
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor\u2019s<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the way<br/>you have learned to keep yourself safe.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph("The Architect &nbsp;\u00b7&nbsp; The Flood", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Disrespect &nbsp;\u00b7&nbsp; Core Question: Am I protected?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cThe psalms teach us that the road to wholeness runs through the valley\u2014<br/>"
        "not around it, not over it\u2014<br/>"
        "and that God meets us there, in the honest dark.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Tim Keller, <i>Walking with God through Pain and Suffering</i>",
        ParagraphStyle("cqa", parent=S["CoverProfileSub"], fontSize=9)))

    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ── SECTION 1: Opening ──
    section_header(story, S, "SECTION ONE  \u00b7  OPENING",
                   "A word before we begin.",
                   "Read this slowly. It has been a long time in the writing.")
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
                   "Where the sensitivity came from.",
                   "What was lodged in you, and what to do with what you find.")
    for p in TRIGGER_BODY[4:]:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, written by hand.",
                   "Your head will perform the question; your hand will not.")
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
                   "Exhaustion that has learned to look like faithfulness.")
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
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
                   "The assumption underneath.",
                   "What the calendar confesses that the doctrine does not.")
    for p in ARCH_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "What David knew that the Architect forgot.",
                   "The psalms of complaint as spiritual discipline.")
    for p in ARCH_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Architect.",
                   "Let him say what he has never been allowed to say.")
    for p in ARCH_LETTER_INSTRUCTION:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 6))
    story.append(_callout(S, "MODEL LETTER — THE ARCHITECT SPEAKS", ARCH_LETTER_MODEL))
    story.append(Spacer(1, 10))
    tool_h = ParagraphStyle("ToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("ToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)
    story.append(Paragraph("Now continue in your own words:", S["Prompt"]))
    story.append(Paragraph("1.  What is the Architect most afraid you will discover about him?", S["Prompt"]))
    journal_lines(story, n=4)
    story.append(Spacer(1, 8))
    story.append(Paragraph("2.  What has he been holding that was never his to carry alone?", S["Prompt"]))
    journal_lines(story, n=4)
    story.append(Spacer(1, 8))
    story.append(Paragraph("3.  What would you say back to him, if he could hear you?", S["Prompt"]))
    journal_lines(story, n=4)
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Flood.",
                   "What happens when the structure that has been holding everything finally gives.")
    for p in FLOOD_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "What the Flood is looking for.",
                   "A bid for witness, arriving in a form that makes witness almost impossible.")
    for p in FLOOD_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The practice the Architect suppressed.",
                   "Lament as the spiritual discipline that prevents the dam from going.")
    for p in FLOOD_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions about the last Flood.",
                   "Sit with these before you turn the page.")
    for prompt in FLOOD_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=5)
        story.append(Spacer(1, 12))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same person in two different moments.",
                   "Architect and Flood are not two problems. They are one cycle.")
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
                   "Small enough to carry. Useful enough to reach for.",
                   "What to do when you feel the cycle begin.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Architect is overworking.",
                   "Five practices for the time before the pressure becomes critical.")
    for name, desc in ARCH_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Flood has come or is coming.",
                   "Four practices for the overflow and its aftermath.")
    for name, desc in FLOOD_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "<b>Integration:</b> The single discipline that connects both sides is this — "
        "the regular, small, honest prayer of lament and transfer. Before the planning tips into "
        "anxiety, bring it to God. Before the accumulation becomes a flood, bring it to God. "
        "Not as a last resort. As a first practice. The Psalms are, among many things, a "
        "curriculum for this discipline, and they were given to you to use.",
        S["BodyJ"]))
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
