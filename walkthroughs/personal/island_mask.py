"""Personal Walkthrough — Island + Mask.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Shame trigger, "Am I acceptable?" core question.
~25 pages, 9 sections.

Calibration anchor: The Island+Mask is the deepest cover in the 36.
The Island already lives in self-containment; the Mask adds a layer of
socially-acceptable performance on top. This is the person who hosts
brilliantly, listens deeply, gives sage counsel — and tells no one
anything real. Where the Architect+Mask is an executive in motion
(charm + control), the Island+Mask is more like a wise friend behind
glass: warm, present, unreachable.
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
    "Before you read any further, I want to do what a good pastor does at the beginning of a hard conversation. I want to lower the lights and slow the room down, because what you are about to look at is not a diagnosis. It is a picture of the way your soul has learned to stay alive in a world that has made it feel dangerous to be fully seen.",
    "You are, in a particular and important sense, an Island. Not because you are cold or incapable of love — you may in fact be one of the warmest presences in the lives of the people around you. But something in your history taught you that the distance between your interior world and the world outside was not a gap to be closed but a perimeter to be kept. You learned to process alone, to keep your deepest things inside, where they could not be mishandled or returned to you in a form you did not recognize. And on top of that interior perimeter, you have built something more sophisticated still: a presence that is genuinely engaging, deeply attentive, and socially gracious — a Mask that serves everyone in the room while protecting the room no one enters.",
    "We are going to walk through your trigger — the specific wound that fires the alarm in you when almost no one else notices anything is wrong. We will listen to the question underneath that wound, the one that has been with you since you were young. We will name the Island you have built in response, and the Mask you have learned to wear while living on it. And then, only then, will we put tools in your hands.",
    "If you were sitting across from me, I would say this plainly. <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who has seen the interior that no one else has been permitted to enter, and who has not looked away; a Son who entered, in his own person, the full horror of public exposure and shame so that the exposure you most fear would never again have to define you; and a Spirit who is at this moment more interested in what is happening behind your composed exterior than you have allowed yourself to be.",
    "So read slowly. The Island in you will want to keep a polite distance from what follows — to observe rather than receive it. Resist that. Argue with what does not fit. Stay with what does. Pray when something catches in your throat, because that catch is the Lord opening a door you have kept shut for a long time. The goal is a slightly freer life, lived before a God who has seen everything the Mask was built to hide and has not changed his mind about you. Take your time.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it almost never looks like anything from the outside. You are in a gathering — a dinner, a small group, a meeting — and you are, as you usually are, genuinely present. You are listening well. You may be the best listener in the room. And then something happens that most of the people around you do not register at all.",
    "Perhaps someone shares something vulnerable, and you respond with care and wisdom, and the conversation moves on — and something inside you notes that no one thought to ask how you are doing. Perhaps a friend mentions a struggle, and you hold it attentively, and you think: I have never told anyone this equivalent thing. Perhaps someone glances at you in a way that seems to look past the composure, to see something you did not intend to show, and a quiet alarm fires in your chest even as your face remains entirely still.",
    "The signal your body has registered is this: <i>I am about to be seen in a way I have not managed.</i> Or its inverse: <i>I have just given everything to this room, and the room will never know who gave it.</i> Both fire the same trigger. The word for it is <b>shame</b> — not the large theatrical version, but its quieter cousin: the sense that there is a gap between who you appear to be and who you actually are, and that the gap, if anyone found it, would change things.",
    "C. S. Lewis, in <i>The Weight of Glory</i>, wrote with unusual honesty about the longing every human being carries to be known and affirmed by something larger than any human verdict — to hear one's name spoken by the highest authority. He refused to be embarrassed by this longing, because he recognized in it something God-shaped. What he also observed was that when this longing goes underground — when it is denied rather than brought to God — it does not disappear. It goes to work in the dark, shaping behavior and expectation in ways that are no longer visible to the person carrying it.",
    "The Island has made this longing go underground. You have learned to perform a beautiful selflessness — to give attention, to listen deeply, to be the wise friend in the corner who has a word for everyone — and in that performance the deeper question has been buried: <i>Am I acceptable as I actually am? Not as the careful, composed, attentive self I have offered this room, but as the self no one in this room has been allowed to see?</i>",
    "Here is what I want you to see before we go further. The sensitivity you carry to exposure — the vigilance with which the Island monitors whether the gap is showing — is not random vanity. It is the residue of real moments, usually early, in which being seen went badly. A home where emotional expression was met with embarrassment or indifference, not care. A season in which something real about you was exposed and the exposure cost you something. A household in which the rule, spoken or unspoken, was that certain things stayed inside. Whatever its origin, the lesson lodged: <i>The self people see is safer than the self I actually am. I will manage the difference, and I will do it so well they will never know I am managing anything at all.</i>",
    "Before we continue, I want you to do something simple. Answer the two questions below in writing — not in your head, where the Island will draft a composed and reasonable response, but on paper, where something more honest tends to come through.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the exposure signal fired — the moment you sensed that someone might be seeing past what you had arranged for them to see, or the moment you gave something real to a room that would never know you gave it. What happened? What did you do in the ten seconds after?",
    "What would it mean, practically and specifically, if the person you were most guarded around actually saw the full interior — not the attentive, generous, composed self, but the self underneath? What are you most afraid they would conclude?",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm has been standing over for a very long time.",
    "Yours is this: <b>Am I acceptable?</b>",
    "It is not the same as <i>Am I lovable?</i>, though it sometimes wears that face. It is more specifically located: the question of whether you are acceptable as you actually are — not the generous, attentive, composed self you have offered the world, but the interior one: tired, uncertain, aware of its own gaps, deeply unwilling to let anyone else be aware of them. The question, at root, is: <i>If someone saw the whole of me — not just what I give, but what I actually am — would they still want to be near me?</i>",
    "The taxonomy of fear has a name for this profile, and it is the right one. This is the shame question — not shame about a specific act, though acts are woven into it, but shame about a self. The haunting sense that there is something fundamentally not-right about you, something that your composure and your care for others has been constructing, over years, to conceal. John Owen, in his great pastoral writing on the mortification of sin, observed that the sin we most need to examine is not always the one that announces itself in failure, but the one that has quietly organized the whole life around its own avoidance. For the Island, shame is that organizing principle. It runs the show from behind the Mask — and the Mask is convincing enough that even those closest to you rarely see through it.",
    "For you, this question is particularly alive because the Island has made it almost impossible to ask it out loud. The Island does not petition. The Island does not say, <i>I need to know if you still find me acceptable when you have seen everything.</i> That kind of exposure would require dismantling the entire management project. And so the question stays inside — forming and reforming, gathering evidence, losing none.",
]

QUESTION_BODY_P2 = [
    "There is a reason that the Psalms — the prayer book of Israel, and of Jesus himself — spend so much time in the territory of exposure, shame, and the fear of being found wanting. The prayer book did not assume that God's people would have their interior lives sorted. It assumed the opposite.",
    "<i>My wounds stink and fester because of my foolishness; I am utterly bowed down and prostrate . . . I am feeble and crushed; I groan because of the tumult of my heart. O Lord, all my longing is before you; my sighing is not hidden from you.</i> (Psalm 38:5–6, 8–9)",
    "Notice what the psalmist does not do. He does not present well. He names the festering, the feebleness, the groaning, without concern for impression — because he has located the one Audience before whom the management project is both unnecessary and impossible. You are already fully seen, by the only One whose verdict finally counts, and the seeing has not produced rejection.",
    "The gospel anchor for the shame question is this: <i>I am in Christ — covered, clean, belonging — and I am justified: just as if I had never sinned, and just as if I had always perfectly obeyed.</i> Paul states it with directness that should arrest us: <i>There is therefore now no condemnation for those who are in Christ Jesus.</i> (Romans 8:1) Not reduced condemnation. None. The verdict has been rendered, and it was not based on the version of you that performed well. <i>For our sake he made him to be sin who knew no sin, so that in him we might become the righteousness of God.</i> (2 Corinthians 5:21) Christ entered the full horror of public exposure at the cross — seen, mocked, stripped, found contemptible — to absorb, once and finally, the shame you have been managing and building over ever since.",
]

QUESTION_BODY_P3 = [
    "This is where honest work is required, because the Island has been trying to answer the shame question with solitude and performance. You have made yourself indispensable as a listener, a counselor, a wise and caring presence — and as long as you are giving, no one looks too carefully at what is behind the giving. But a strategy, however good, cannot answer a question about a self. It can only defer it, gathering by gathering.",
    "The real answer to <i>Am I acceptable?</i> cannot be performed into existence. It can only be received. It comes not from the beautiful, selfless, composed presence you have offered the world, but from the verdict spoken over you at the cross, before you had done anything to merit it — and before you had done anything to conceal it. The covering you have been laboring to construct through your care for others was already provided. What is required is not more performance. It is the courage to step inside the covering that is already there.",
    "This will not resolve in a single reading. The reception of justification as a felt reality rather than a doctrinal affirmation is the slow work of years. But it begins with naming, clearly and without flinching, what you have been doing and what you have been afraid of. Before we move further, use the table below to begin that naming.",
]

ISLE_BODY_P1 = [
    "You have built something. You did not build it in a season, and you almost certainly did not know you were building it. But over years — and usually over a handful of specific moments in which the world showed you what it did and did not keep safe — you constructed a way of being in the world that we are going to call, throughout this walkthrough, <b>the Island</b>.",
    "The Island's strategy is this: <i>if I process everything internally, if I give generously and ask for little, if I make myself necessary to others without becoming transparent to them, then the question of whether I am acceptable as I actually am can remain unanswered — and unanswerable — indefinitely.</i> The Island is not a recluse. You may be, in the eyes of everyone who knows you, one of the most present and caring people in the room. But the Island has learned that there is a safe distance between caring for someone and being known by them, and it maintains that distance with extraordinary skill.",
    "There is a great deal in Scripture that commends certain dimensions of what the Island does. Proverbs values the person whose words are measured, who does not pour out every interior thing on every occasion: <i>Whoever guards his mouth preserves his life; he who opens wide his lips comes to ruin.</i> (Proverbs 13:3) The ability to hold your own counsel, to process before speaking, to be genuinely present to another person without requiring their presence in your inner world — these are gifts, and the Island has developed them to a rare degree.",
    "But there is a cost the Island rarely acknowledges. The same self-containment that protects you from the exposure you fear also prevents you from being genuinely known — and the shame question underneath your trigger cannot be answered by a soul that has made itself invisible to the people whose company it keeps. The Island's strategy and the Island's deepest longing are working against each other at the root.",
]

ISLE_BODY_P2 = [
    "The Island usually formed in one of several ways. Perhaps emotional expression was not welcome in your household growing up — not punished, exactly, but not valued. Feelings were handled privately until they passed. Perhaps you learned early that needing people set you up for disappointment, and self-sufficiency began to feel not merely safer but more honest. Perhaps you watched someone close to you need too much from others, always in crisis, and you decided you would never become that. Whatever the origin, the lesson lodged: <i>manage alone, and you will not be disappointed by what others fail to give.</i>",
    "John Owen, writing on the mortification of sin, observed that the desires of the soul do not die simply because they go unnamed. They go underground, where they continue to press and shape behavior without the light of examination. The Island's longing — to be known as it actually is, and found acceptable — has gone underground. It has not gone away. It surfaces in the tally the Island keeps of who has asked and who has not, of which conversations stayed safely on the surface and which went somewhere real. The tally is not visible. But it is running.",
    "<b>The Island is not your enemy.</b> He is a younger version of you who learned, in some real circumstance, that managing alone was safer than hoping for company. He deserves your respect. But he is working overtime on a project — keeping you safe from the exposure of need — that is also keeping you from the very thing the shame question is asking for. The water surrounding the Island is not protection. It has become a kind of loneliness that looks exactly like contentment.",
]

ISLE_BODY_P3 = [
    "What does it look like to begin loosening the Island's hold? Not demolishing it — the Island was built for a reason, and the reason was real. But beginning, slowly, to allow one person to see further in than you have typically permitted. Not everyone. One person. And before that — most importantly — God, who has already crossed the water, who is already inside, who has known everything you have processed alone and has never once turned away from what he found.",
    "The exercise below is the place to begin. What follows is a letter from the Island — not a letter to him, but from him, written in his voice, to you. The Island has been protecting you for a long time. Give him a moment to say what he has actually been afraid of. Read it slowly. Then answer the three prompts that follow.",
]

ISLE_LETTER_INSTRUCTION = [
    "The letter below is written in the Island's voice — in the voice he would use if he were honest, for once, about what has been running the operation. He is not a villain; he is frightened. Read it as you would read a letter from someone who has been faithful to you for years and is, finally, telling you the truth about why.",
]

ISLE_LETTER = """\
Dear friend,

I have been with you longer than you realize. You probably do not think of me as a distinct thing — you think of me as simply how you are, the way some people share freely and others hold their interior close. But I want to be honest with you, because I think you are ready to hear it.

I am afraid. That is what has been running the whole operation. Not privacy as a virtue, not self-sufficiency as a strength, though I have worn those clothes and they have fit well enough to be convincing. Underneath is a much older fear: that if the people you give the most to ever saw what is actually inside you, they would find the gap too large. They would see that the person who gives so much has been protecting something — a self that is not certain it is acceptable.

So I built the Island. I gave you the gift of deep listening, because a person truly attending to another cannot be accused of withholding. I gave you a reputation — the wise friend, the steady presence, the one who always has a word for the difficult moment — and that reputation became its own protection. No one looks carefully at the interior of the person they depend on.

What I did not account for is that the distance I built to protect you from exposure also protected you from being known. The question underneath your trigger — Am I acceptable as I actually am? — cannot be answered by a soul that has never allowed anyone close enough to answer it. I am not the solution to the question I was built to avoid. I am the question, asking itself in the form of a life very carefully arranged.

The Island
"""

ISLE_LETTER_PROMPTS = [
    "What is the one line in that letter you most wanted to dismiss or argue with? What does your resistance to it tell you about what the Island has been protecting?",
    "The Island says he built a life in which 'the person who gives so much cannot be accused of withholding.' Name one relationship in your life where that has been true. What have you given freely? What have you never offered?",
    "What would it cost the Island to let one person — just one — see the interior it has been protecting? Name the person. Name the cost honestly, without softening it.",
]

MASK_BODY_P1 = [
    "Every mechanism has a place where it breaks, and for the Island, the breaking has a particular shape — one that is uniquely difficult to name, because it does not look like breaking. It looks like composure. It looks like presence. It looks like someone who is, by all appearances, handling everything with grace. This is called <b>the Mask</b>, and for the Island it is the deepest concealment in the whole of the thirty-six profiles.",
    "Here is how it happens. The Island has been holding the perimeter — processing internally, giving generously, maintaining the warm and safe distance. Then something arrives that crosses the perimeter anyway: a moment of genuine intimacy that the Island cannot quite manage into something comfortable, a wound that is too specific to deflect, a question from someone close enough to have noticed the gap, or sometimes just a season of accumulated loneliness that has become too heavy to carry alone without it beginning to show.",
    "In that moment, the Island does not argue. It does not collapse. It does not ghost or retreat into silence. Instead, it does something far more sophisticated: it becomes even more present. It listens more deeply. It offers a more perfectly calibrated version of itself — wiser, warmer, more generous — and the person on the other side of the conversation feels, genuinely, that they have just had access to something rare. They have. They have just been given the Island's finest gift. What they have not been given is the Island itself.",
    "C. S. Lewis, in <i>The Four Loves</i>, made an observation about friendship that cuts close here. He noted the danger of a friendship in which one person gives everything and receives nothing — not because the giving is false, but because it is asymmetrical in a way that produces, in the one who always gives, a kind of unrequited intimacy. The Island+Mask is the warm friend behind glass. Every room is warmer for your presence. No room has full access to you.",
]

MASK_BODY_P2 = [
    "The Mask is not lying. That is what makes it so extraordinarily durable. Almost everything the Mask presents is true. You do care about the people in the room. The listening is genuine. The wisdom is real. The Mask does not fabricate; it selects. With remarkable precision it chooses which parts of the true self to offer, and it keeps everything else behind a door that looks, from the outside, like contentment.",
    "The specific genius of the Island-Mask combination is that the Mask is built from the Island's finest materials: attentiveness, warmth, steadiness, the capacity to hold another person's pain without flinching. When the shame question fires — when possible exposure rises — the Island does not retreat. It gives more. It leans in. And from the outside, this looks exactly like the kind of selfless, other-centered presence everyone aspires to. <b>The ministry and the hiding use the same face.</b>",
    "This is the theological problem with the Island-Mask combination, and it is a serious one. Bonhoeffer, in <i>Life Together</i>, wrote: <i>He who is alone with his sin is utterly alone.</i> The Mask guarantees a particular kind of aloneness, because it prevents the honest, confessional speech by which Christian community breaks the power of hiddenness. The Mask will give you a version of openness that is credible enough to seem real — a carefully chosen vulnerability offered at precisely the right angle so that it creates the feeling of intimacy without actually creating the condition of being known. And in that gap — between the appearance of openness and genuine transparency — the wound continues its work underground.",
    "D. Martyn Lloyd-Jones, writing on spiritual depression, observed that many of the most apparently functioning people he had known were the most spiritually lonely, because their competence — or in the Island's case, their other-centeredness — had insulated them from the honest disclosure that genuine fellowship requires. He was describing this profile exactly. The Island who wears the Mask is admired, sought out, depended upon — and, at the level that finally matters, fundamentally alone.",
]

MASK_BODY_P3 = [
    "What the Island's Mask has constructed, over time, is what we might call a <b>ministry of selflessness</b> — and the pastoral move here is to name it plainly. The giving is real. The care is genuine. But underneath it, the ministry has a second purpose: it keeps the question <i>Am I acceptable as I am?</i> from ever having to be answered, because as long as you are giving, no one is looking. No one examines the interior of the person they depend on. The ministry of selflessness is, at its root, a refusal to be known.",
    "John Owen's famous line applies here with particular force: <i>Be killing sin, or sin will be killing you.</i> Owen was not speaking of dramatic moral failure. He was speaking of the quiet, organized, deeply-entrenched patterns by which the soul avoids the light of honest examination. The Island's Mask is exactly this kind of pattern — not dramatic, not obviously sinful, indeed admirable by most measures. But it is keeping you from the life that is being offered: the life of a soul genuinely known by at least one or two people in its world, who has discovered that being known did not produce the outcome it most feared.",
    "Here is the question the Mask has never been asked: <b>What would you lose if it came off?</b> Not who would leave. Not how people would respond. What would be at risk inside you if the performance of perfect attentiveness stopped? My guess is this: you would lose the ability to tell yourself that the distance is wisdom. And the distance has been, for a long time, the only kindness the shame question has ever been offered.",
    "Peter, who was remarkably skilled at performing bravely and retreating whenever the performance became costly, was asked three times by the risen Christ: <i>Do you love me?</i> (John 21:15\u201317) The question was not asked because Christ did not know the answer. It was asked because Peter needed to say the true thing, out loud, without mediation, to the one Audience who could receive it without mishandling it. The Mask does not survive that question — not because the love is not real, but because the question insists on the unmediated self, and the Mask can only offer the curated one.",
]

MASK_PROMPTS = [
    "Name the last time the Mask went on — not the dramatic version, but the ordinary one: the moment you became more present, more giving, more composed, specifically because the wound had just fired and you could not afford to let it show. What had just happened? What did you offer the room? What did you actually feel?",
    "The Island's ministry of selflessness has a second purpose: keeping the shame question from having to be answered. Name one specific relationship in which this is true. What have you given consistently in that relationship? What have you never asked for, and what has your not-asking protected you from?",
]

TWO_TOG_BODY = [
    "Now we place them next to each other, because the Island and the Mask are not two separate problems. They are the same wound, wearing two different uniforms — and together they form the deepest cover in the whole of the thirty-six profiles.",
    "<b>The Island is what the wound does when it has time to organize itself.</b> The Mask is what it does when something gets through the organization. The Island builds the perimeter: processing alone, giving without receiving, maintaining the warm distance. The Mask is what the Island reaches for when something threatens to breach the perimeter: more presence, more generosity, more of the beautiful selfless performance that keeps the question from having to be asked. Together they form a closed system in which the shame question never quite has to be answered, because the Island ensures that no one ever gets close enough to ask it, and the Mask ensures that when someone does get close, what they receive is a performance so convincing that they forget they were about to ask.",
    "The pattern, in slow motion, looks like this. <b>(1)</b> The Island moves through the world in its characteristic mode: attentive, warm, giving, maintaining the interior perimeter. <b>(2)</b> Something arrives that crosses the perimeter — a wound specific enough to penetrate the composure, or an accumulation of loneliness too heavy to carry invisibly. <b>(3)</b> The trigger fires: <i>I am about to be seen in a way I have not managed.</i> <b>(4)</b> The question wakes up: <i>Am I acceptable as I actually am?</i> <b>(5)</b> The Island tries to restore the perimeter: more listening, more giving, more wisdom offered. <b>(6)</b> When that cannot hold, the Mask engages fully — warm, present, composed, apparently fine. <b>(7)</b> The wound goes underground. The loop restarts.",
    "What breaks the loop is not a better Island — a more self-sufficient Island only produces a more convincing Mask. What breaks it is a different answer to the question. Not the answer constructed through ministry and selflessness, but the one given at the cross: you are already covered, already seen, already acceptable — not because of what you have given, but because of what was given on your behalf, before you had given anything at all. That answer, received rather than performed, is the only thing the Mask does not know how to improve upon. Below, name your sequence in your own words. The Island and the Mask both lose some of their grip when they hear themselves named in plain speech.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, my body reads it as exposure, and "
    "the old question wakes up \u2014 <i>am I acceptable as I actually am?</i> My first move "
    "is to ____________________, because the Island in me believes that if I can "
    "____________________, the question will not have to be asked. When that does not "
    "hold, the Mask engages: I become ____________________ \u2014 and the room receives "
    "____________________ while the wound goes underground. What I am actually after, "
    "underneath all of it, is the verdict ____________________ \u2014 a verdict Christ "
    "has already spoken over me, not earned but given, in ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a set of small, portable practices, each calibrated to a specific moment in the loop you just named. None of them will resolve in a week what years have put in place. All of them, practiced faithfully over months, will begin to loosen the grip of the Island and the Mask.",
    "I have divided them into two sets: tools for when the Island is overworking its defenses — when the generous giving has tipped into the managed distance — and tools for when the Mask is going on, for the narrow window between the wound and the concealment. That second window is brief, but it is real, and it is where the most important work of this season will happen.",
]

ISLE_TOOLS = [
    ("The one honest sentence", "Once each day — not more, because the Island cannot sustain more without the defenses rising — say one honest sentence about your interior to someone who is present to you. Not a report. Not a shared problem you are framing for their consideration. One sentence about what you are actually carrying: what is hard, what is lonely, what you have been processing alone. The Island will insist this is unnecessary. Do it anyway. Over a month, the practice begins to widen the aperture between your interior world and the people who love you."),
    ("The audit of the giving", "Once a week, ask yourself this question about your closest relationships: <i>In the past seven days, what did I give freely — attention, presence, care — and what did I receive?</i> Do not keep the tally to use against anyone. Keep it only so that you can see whether the asymmetry is structural. If you have given significantly and received little, the question is not whether the other person is generous. The question is whether you have made it possible for them to give to you."),
    ("The Psalm of disclosure", "When the Island's solitude tips into hiding, open to Psalm 62 or Psalm 139 and pray one section aloud. The Psalms are the one place in Scripture where the interior world is required to speak without management, and they model a disclosure to God that is too honest to be performance. Psalm 139: <i>You have searched me and known me . . . Where shall I flee from your presence?</i> The Island's great project is to manage the distance between the interior and the outside. Psalm 139 names that project as impossible before the One who matters most — and impossible in a way that is finally not terrifying but freeing."),
    ("The handed-back ministry", "Once a week, name one thing you did this week in service of another person, and ask honestly: <i>Was this given freely, or was it given in part to keep the distance from showing?</i> You do not need to stop giving. You need to begin to know why you are giving. The ministry of selflessness is only a ministry when it comes from a soul that has first received. The Island who gives from an unresupplied interior is not serving — it is surviving. Hand the motivation back to God, and ask him to resupply what you have been drawing from without refilling."),
    ("The ten-minute unlocked door", "Once a week, initiate a conversation about something interior — something you are actually carrying — with one person you trust. Not a problem you are framing for their wisdom. Something you are not sure about, something you are afraid of, something you have been processing alone and have reached no conclusion on. The Island will call this exposure. It is. That is the point. The shame question cannot be answered by a soul that has never allowed anyone to see what the question is about."),
]

MASK_TOOLS = [
    ("Name the seam", "The Mask has a seam — a moment between the wound and the slide, before the composed, giving, present self has fully engaged. It is brief: sometimes only three or four seconds. Your only task in this season is to notice that moment. Simply feel the Mask going on and know, as it goes on, what is happening. <i>The wound fired. I am now managing the presentation.</i> Noticing is not the same as stopping. But noticing is the beginning of choice, and choice is what the Mask has been preventing."),
    ("The three-word honesty prayer", "In the moment after the wound fires — before the Mask has fully engaged — say these three words silently, to God: <i>I am hurting.</i> Not as a petition. Not asking for anything. Simply as a statement of what is true. He already knows. The saying is for you. The Island's Mask depends on the wound going underground immediately, without acknowledgment even by the person carrying it. Three words, said honestly to the right Audience, interrupt that process at its source."),
    ("The deferred confession", "You will not always be able to take the Mask off in the moment — and in some moments it would not be appropriate to do so. But within twenty-four hours, find the one person you trust most and say: <i>I put the Mask on yesterday when ___. What was actually happening was ___.</i> Do this once, with one person, within one day of the wound. The Island+Mask draws its power from secrecy and from the time that passes between the wound and its naming. One honest sentence, spoken to a safe witness within twenty-four hours, breaks both."),
    ("The advocate prayer", "When the Mask is on and you can feel it: <i>Lord Jesus, you were exposed for me. I do not have to manage the exposure. The verdict over me is already spoken. Help me receive it.</i> The Island trusts what it has built with its own hands. Give this prayer the same trust you give the Mask — say it deliberately, even before you feel it, even when it sounds like doctrine rather than truth. It is both."),
    ("Write the ungiving word", "At the end of any week when the Mask was particularly active, write one paragraph for your own eyes only. Name what happened: what the wound was, what the Mask offered in its place, and what you did not give that you needed to give. Writing the true thing, even to no audience but yourself and God, is a form of the exposure the Mask is specifically designed to prevent. The Island will say this is unnecessary. The Island is wrong."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Island in me, and you see the Mask it wears, and you are not surprised by either of them. You know why I built them both. You were present for the moments that made them feel necessary — the moments I have never named to another person, and that I have barely named to myself. Thank you that you were there, and that you did not look away, and that you are not looking away now.",
    "Father, I am tired of the managing. I am tired of the distance that looks like contentment, of the giving that never quite allows anyone in, of the way I can hold another person's wound with real care while my own wound continues its work underground, untouched, unnamed. I do not know how to stop on my own. When I have tried to stop, I have built a better Mask. So I am asking you to do what I cannot: teach me, slowly, what it means to be seen by another person and not destroyed. Teach me that the interior you have already entered, without invitation and without turning away, can be opened, carefully and in safety, to at least one other person in my world. Teach me to say the true thing before the presentation has fully assembled.",
    "Lord Jesus, you know what it is to be fully exposed — naked before the crowd, mocked, found contemptible by those who watched, bearing in your own body the shame of a verdict you did not earn. You did not manage the exposure. You absorbed it. And in the absorbing you reversed its verdict over me forever: covered, clean, acceptable not because of what I have given but because of what was given for me. Help me receive that reversal not as a doctrine I affirm but as the felt covering of a soul that has been managing its own exposure for a very long time.",
    "Holy Spirit, where the Mask goes on today, give me the grace to notice it. Where I am giving in order to stay hidden, give me the courage to simply be present without the performance. Where the question <i>am I acceptable?</i> rises in me, remind me of the answer that has already been spoken, at the cross, in a way that no subsequent evidence can overturn. Keep speaking it until I can hear it in the part of myself I have worked hardest to conceal.",
    "In the name of the One who, to the woman who had managed her own exposure for years, said: <i>your faith has made you well; go in peace</i> \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Island and the Mask have been with you a long time, and they will not retire after one reading. What follows is a short list of next steps — some for the next week, some for the longer work ahead.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different lines will land the second time. The Island will want to file this document away, having extracted what is useful. Read it again slowly, thirty days from now, and notice which paragraphs you could not receive on the first pass. The Mask performs better in your head than on paper; a second reading is harder to manage."),
    ("Take one tool, not all of them.", "Choose the practice from Section Seven that felt most uncomfortable — not the most manageable one. Tools that cost nothing protect nothing. Try the one that made the Island want to skip past it. Use it for two weeks before evaluating."),
    ("Tell one person what you found here.", "Not the whole document. One sentence: <i>I learned that my pattern is the Island, and that what I do when I am wounded is put on a Mask. I am working on letting the Mask come off.</i> The Island+Mask draws its power from secrecy. Breaking the secrecy once, with one trusted person, changes the architecture in ways that a hundred private insights do not."),
    ("Read Tim Keller's Counterfeit Gods.", "Keller's treatment of the things we place at the center of our identity addresses the Island's hidden foundation with precision. The Island who makes self-sufficiency and the ministry of selflessness into a counterfeit god will find themselves, somewhere in these pages, with uncomfortable accuracy."),
    ("Read C. S. Lewis's The Four Loves.", "Lewis's chapter on friendship gives you language for what the Island+Mask has been preventing. His account of the dangerous safety of asymmetric giving — the friend who is always present and never accessible — describes this profile with a clarity that is easier to receive from a novelist than from a counselor."),
    ("If you are stuck, ask for help.", "There are seasons when the Island and the Mask are too entrenched to dislodge alone — which is, of course, precisely the kind of acknowledgment the Island most resists. A wise pastor, a Christian counselor, a friend who has earned access to your interior — these are not signs of failure. For the Island, asking for this kind of help is itself the beginning of the answer to the question. The Mask was built to prevent you from asking. Ask anyway."),
]

GOING_FURTHER_CLOSING = (
    "You are not a project to be managed into acceptability. You are a son or daughter "
    "being loved into freedom by a Father who has already seen everything the Mask was "
    "built to hide, who has entered the exposure you most feared, and who has not "
    "changed his mind about you. Go gently with yourself. "
    "The One who began this work in you will be the one to finish it."
)


def _three_column_table(rows=7):
    """Three-column journal table for the acceptability/shame reflection exercise."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "ColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "ColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE MOMENT", header_style), Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WHAT I SHOWED", header_style), Paragraph("the Mask\u2019s offering", sub_style)],
        [Paragraph("WHAT WAS ACTUALLY TRUE", header_style), Paragraph("the interior I did not show", sub_style)],
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
    """Generate the Island+Mask walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='ISLE', primary_breakdown='MASK',
    primary_trigger='SHM', core_question='ACC'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="ISLAND  \u00b7  MASK",
        title="Take 139 Walkthrough \u2014 Island + Mask",
    )

    story = []

    # ── COVER ──
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor\u2019s<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the self you give to every room<br/>and the self no room has ever fully seen.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph("The Island &nbsp;\u00b7&nbsp; The Mask", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Shame &nbsp;\u00b7&nbsp; Core Question: Am I acceptable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cThere is therefore now no condemnation<br/>"
        "for those who are in Christ Jesus.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Romans 8:1",
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
                   "Shame.",
                   "The moment no one else notices \u2014 and what the Island does in the ten seconds after.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will present the answer; your hand will tell the truth.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ── SECTION 3: Core Question ──
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I acceptable?",
                   "The wound the alarm has been standing over.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "What the psalmist knew \u2014 and what the cross answers.",
                   "Already fully seen. Already not rejected.")
    for p in QUESTION_BODY_P2 + QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "The gap between what I showed and what was actually true.")
    story.append(Paragraph(
        "Use the table below. In the first column, name a recent moment when the exposure alarm fired. "
        "In the second, describe what you showed \u2014 what the Mask presented. "
        "In the third, write what was actually true of you in that moment, "
        "<i>behind the presentation</i>.",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table(rows=4))
    story.append(PageBreak())

    # ── SECTION 4: Mechanism ──
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Island.",
                   "What you have built, and what the building was built to protect.")
    for p in ISLE_BODY_P1 + ISLE_BODY_P2 + ISLE_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Island.",
                   "Read the Island\u2019s own words. Then answer the three questions below.")
    for p in ISLE_LETTER_INSTRUCTION:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    letter_style = ParagraphStyle(
        "IslandMaskLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for para in ISLE_LETTER.strip().split("\n\n"):
        story.append(Paragraph(para.replace("\n", " "), letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in ISLE_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=2)
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # ── SECTION 5: Breakdown ──
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Mask.",
                   "The place the Island breaks \u2014 and the face it shows while breaking.")
    for p in MASK_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The ministry and the hiding wear the same face.",
                   "Why the Island+Mask is the deepest cover in the thirty-six.")
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
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ── SECTION 6: The Two Together ──
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same wound, in two modes.",
                   "The Island and the Mask are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SIX  \u00b7  YOUR SEQUENCE",
                   "Write it in your own words.",
                   "Fill the blanks. Read it aloud when you are done.")
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
                   "Small enough to carry; concrete enough to use.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 14))

    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Island is overworking its defenses.",
                   "Five practices for the time before the alarm fires.")
    for name, desc in ISLE_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Mask is going on.",
                   "Five practices for the narrow window between the wound and the concealment.")
    for name, desc in MASK_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())

    # ── SECTION 8: Prayer ──
    section_header(story, S, "SECTION EIGHT  \u00b7  A PRAYER",
                   "Pray this slowly.",
                   "Out loud, if you can. Sit in the silence after the Amen.")
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
        primary_breakdown = "MASK"
        primary_trigger = "SHM"
        core_question = "ACC"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "island_mask_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages (rough: count %%Page markers or use PyPDF2 if available)
    try:
        import io
        from reportlab.lib.pagesizes import LETTER
        page_count = pdf_bytes.count(b"/Page\n") or pdf_bytes.count(b"%%Page")
        if page_count == 0:
            # try another approach
            page_count = pdf_bytes.count(b"ET\n")
    except Exception:
        page_count = "unknown"

    # Letter snippet: first 200 chars of the letter
    snippet = ISLE_LETTER.strip()[:200].replace("\n", " ")

    print(f"DONE: island_mask.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB) — {out_path}")
    print(f"Letter snippet: {snippet}...")
