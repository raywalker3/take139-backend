"""Personal Walkthrough — Ambassador + Mask.

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Shame trigger, "Am I acceptable?" core question.
~25 pages, 9 sections.

Calibration anchor: The Ambassador+Mask is the most socially celebrated
and most spiritually dangerous profile in the thirty-six. The Ambassador's
natural warmth + the Mask's adopted persona produces a person whose
Christian community will be reluctant to ever name what is happening —
because everything looks like love, looks like ministry, looks like
sanctification. The Ambassador+Mask is the leader everyone says yes to.

Spiritual problem named in Section Five: the religion of works hiding
inside the cloak of grace. The Ambassador+Mask has built a public faith
that is, at root, a strategy to remain loved. Matthew 23 (Jesus's hardest
words, addressed to the Ambassadors who had become Masks), Bonhoeffer
on cheap grace as the deadly enemy of the church, and Spurgeon's warning
that a smiling face may cover a heart in flight from God.
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
    "Before you read any further, I want to do what a good pastor does at the beginning of a difficult conversation. What you are about to look at is not a celebration of your gifts, though you have real ones, and it is not a rebuke of your ministry. It is a patient conversation about the way your soul has learned to remain loved in a world that has made it dangerous to be found out.",
    "You have probably been, in most of the rooms you have entered, the person who made the room warmer — genuinely warmer, the way a fire is warm. You noticed who was on the edge and went to find them. You asked the question that moved conversation below the surface. People have told you, more times than you can count, that you have a gift for them. They are right. But this walkthrough is going to ask you to look at something underneath that gift — something that has been quietly, expertly, constructing a self that looks like grace but is, at its deepest root, a strategy to never be unwanted.",
    "Here is what we are going to do: name the trigger, listen to the question underneath it, understand the Ambassador, and then look carefully at the Mask. And then, only then, we will put tools in your hands.",
    "If you were sitting across from me, I would say this directly: <b>what you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father whose love for you is not a function of your usefulness to him; a Son who — on the night he was betrayed by a man he had fed and called friend — did not make himself more presentable. He simply remained who he was, and loved anyway. And a Spirit not impressed by your warmth and not frightened by what lies underneath it. So read slowly. When something catches in your throat, resist the impulse to manage it by asking whether someone else in the room is all right. Stay with it. That catch is the Lord saying, <i>look here, with me.</i> The goal is a slightly freer life — one in which you give because you are already held, not in order to find out whether you are.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it almost never announces itself as significant. You are in a gathering — a dinner, a small group, a ministry meeting — and something happens that most of the people around you do not register at all. Someone's tone shifts slightly. A person whose opinion you value says something mild but with a specific undertone. You sense a chill where there was warmth. Your face may not change. You may, in fact, be the first person to reach out to someone on the edge of the room, to generate warmth, to ask the question that moves things to a better place. But inside, a signal has fired — specific, cold, and old. The signal is not <i>I have been inconvenienced.</i> It is: <i>Something is wrong with me and they can tell.</i>",
    "This is your trigger. The word for it is <b>shame</b>, though that word is likely to feel too large and too dramatic for what you experience. You do not experience it as theatrical shame, the kind that leads to visible collapse. You experience the quieter version: the cold sense that someone, somewhere, has looked past the warmth you have been offering and glimpsed the gap between the self you present and the self you actually are. And for the Ambassador, that glimpse — real or imagined, large or microscopic — fires something very old.",
    "C. S. Lewis, writing in <i>The Four Loves</i> about the nature of affection, observed that there is a form of love that generates its own vulnerability — that the more warmly one loves, the more one is exposed to the withdrawal of that warmth. This is particularly true for you. The Ambassador has organized so much of life around being the source of warmth that when the warmth is not returned, or when it seems to be returned with a reservation the other person never states openly, the Ambassador does not register it as mere awkwardness. The Ambassador registers it as a verdict.",
    "<b>Your sensitivity to this signal is not accidental, and it is not vanity.</b> It is the residue of something specific, usually early, in which love in your world was tied — loosely or tightly, explicitly or through implication — to your usefulness or your presentation. Perhaps the household you grew up in had warmth that came and went, and you discovered, as children always do, that your behavior seemed to influence which version you got. If you were warm and helpful and pleasant, the warmth returned. If you were difficult or needy or simply tired, it receded. You drew the conclusion a child draws: <i>love is something I participate in by giving, not by being.</i>",
    "Before we go further, I want you to do something simple. Answer the two questions below in writing. Your head will offer you a composed and reasonable response. Your hand will be more honest. Trust the hand.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the shame signal fired — the moment you sensed that someone might be seeing past the warmth you were offering, or the moment the temperature dropped in someone whose warmth you had been relying on. What happened? What did you do in the thirty seconds after?",
    "What would it mean, specifically and practically, if the person whose warmth you most depend on saw the full interior — not the warm, generous, composed self you offer, but the self underneath? What are you most afraid they would conclude?",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm has been standing guard over for a very long time.",
    "Yours is this: <b>Am I acceptable?</b>",
    "It is not the same as <i>Am I lovable?</i>, though it sometimes wears that face and the two are near neighbors in the soul. It is more specifically located than lovableness. It is the question of whether you are acceptable as you actually are — not the warm, attentive, ministry-ready self you have offered the rooms of your life, but the interior self: tired, uncertain, aware of its own neediness, deeply and precisely aware of the gap between who you appear to be and who you are at eleven at night when the last person has finally gone home. The question is: <i>If they saw that version — if the warmth stopped and someone looked carefully at what is behind it — would they still keep me?</i>",
    "The taxonomy of fear has a name for this profile, and it is the right one. This is the shame question — not shame about a specific failure, but shame about a self. John Owen, in his great pastoral writing on the mortification of sin, observed that the pattern we most need to address is not always the one that announces itself in failure but the one that has quietly organized the whole life around its own avoidance. For the Ambassador, shame is that organizing principle. It runs the show from behind the warmth — and the warmth is so genuinely lovely that almost no one, including you, thinks to look behind it. And so the question stays inside — patient, persistent, gathering evidence from every slight withdrawal of warmth, waiting for the day when the giving will finally have been enough to answer it. That day has not yet come. It will not come through more giving.",
]

QUESTION_BODY_P2 = [
    "There is a reason that the Psalms — the prayer book of Israel, the book Jesus himself quoted in his dying — spend so much time in the territory of shame and exposure. The prayer book did not assume its users had their interior lives sorted. It assumed the opposite.",
    "<i>My wounds stink and fester because of my foolishness; I am utterly bowed down and prostrate; I go about mourning all day long. . . . I am feeble and crushed; I groan because of the tumult of my heart. O Lord, all my longing is before you; my sighing is not hidden from you.</i> (Psalm 38:5\u20136, 8\u20139)",
    "Notice what the psalmist does not do. He does not present well. He does not manage the impression. He names the festering, the feebleness, the groaning — without qualification, without the softening touch of one who knows the audience is watching — because he has located the one Audience before whom the management project is both unnecessary and impossible. <i>O Lord, all my longing is before you.</i> You are already fully seen. The seeing has not produced rejection. This is the foundation on which everything else in this walkthrough rests.",
    "The gospel anchor for the shame question is this: <i>There is therefore now no condemnation for those who are in Christ Jesus.</i> (Romans 8:1) Paul states it with the directness that should stop us completely: not reduced condemnation. None. The verdict was not based on the version of you that performed well.",
    "<i>For our sake he made him to be sin who knew no sin, so that in him we might become the righteousness of God.</i> (2 Corinthians 5:21) Christ entered, in his crucifixion, the full horror of public exposure — seen, mocked, stripped, found contemptible and disposable. He did not manage the impression. He absorbed every part of the exposure you most fear, in his own body, so that the verdict spoken over you would not be the verdict your shame has been predicting all these years.",
]

QUESTION_BODY_P3 = [
    "This is where honest work is required, because the Ambassador has been trying to answer the shame question with warmth. You have made yourself indispensable as a giver, a caretaker, a source of comfort — and as long as you are giving, no one is examining what is behind the giving. The strategy is brilliant, and it is killing you.",
    "The real answer to <i>Am I acceptable?</i> cannot be given through warmth. It cannot be warmed into existence. It can only be received — from outside you, from the only Verdict that does not expire when the warmth runs low. That verdict was spoken at the cross, before you had given anything, before you had managed a single impression, before you were warm or cool or anything at all. The covering you have been laboring to construct through your care for others was already provided. What you are doing, when you maintain the warmth as a strategy rather than as an overflow, is refusing to step under the covering that is already there — and the refusal is very quiet, and very presentable, and almost entirely invisible to the people who love you most.",
    "This will not resolve in a single afternoon. The reception of justification as a felt reality rather than a doctrinal affirmation is the slow work of years. But the work begins with naming what you have been doing and what you have been afraid of. Before we go further, use the table below. Your hand, not your head.",
]

AMB_BODY_P1 = [
    "You have built something. You did not sit down and draft the blueprints — no Ambassador ever does. It grew from you the way a habit grows: from necessity, from small decisions made under real pressure, from the discovery that certain behaviors produced certain outcomes, and that the outcomes were worth the cost. But it is a structure now, and it has been running the operation of your emotional life for long enough that you have difficulty distinguishing it from your personality. We are going to call it, throughout this walkthrough, <b>the Ambassador</b>.",
    "The Ambassador's strategy is straightforward and, on its face, beautiful: <i>if I am warm enough, attentive enough, giving enough, I will be necessary to the people I love, and the people who are necessary are not abandoned.</i> The Ambassador does not experience love as a stable foundation beneath the feet. The Ambassador experiences it as a temperature that must be maintained — and the Ambassador is the one who maintains it. You are the thermostat of most of the relationships in your life. You are very, very good at this.",
    "The Ambassador is not a manipulator. The warmth is genuine. The care for other people is real. When you ask someone how they are doing, you actually want to know. When you follow up three days later, it is not a technique. But underneath the genuine warmth is a strategy, put in place long before you had language for it: <i>if I am the most giving person in the room, I will not be the person left behind.</i> The giving is both real and strategic. Both things are true, and the Ambassador has never had to sit with both of them at the same time.",
    "Where does this come from? For most Ambassadors, one of several specific histories. Perhaps love in your household of origin was contingent — warm when you were performing well, withdrawn when you were not. Not cruelly withdrawn, perhaps. Simply less available. And you were a perceptive child, and you noticed the pattern, and you adjusted. If you were helpful, the warmth returned. If you were needy, it receded. You drew the natural conclusion: being helpful was safer than being needy. Being warm was a better bet than being honest about your temperature. A Proverb you may have heard many times names something true: <i>A soft answer turns away wrath, but a harsh word stirs up anger.</i> (Proverbs 15:1) The Ambassador learned this before they could read it off a page.",
]

AMB_BODY_P2 = [
    "But let me name what this strategy has cost you, because the cost is real and you have not been keeping the books honestly. The Ambassador has developed, over years, a near-complete inability to distinguish between serving and surviving. You give to people you love, and you give to people you barely know, and you give when you are depleted and hurting and when what you most need is for someone to notice that you are depleted and hurting and to give something to you. And you keep giving, because stopping feels dangerous, and because the lesson is in your bones: <i>the way to be loved is to be the one who loves.</i>",
    "J. C. Ryle, writing on the varieties of self-deception in the Christian life, observed that the soul is entirely capable of doing very righteous-looking things for very unrighteous reasons, and that the difficulty is never the behavior but the root from which it grows. The Ambassador's warmth looks like love — and a great deal of it is love. But at the root is a question that love alone cannot answer: <i>am I acceptable in return?</i> And the giving has become, in part, an attempt to force a yes to that question without ever having to ask it in a form that could be refused. The people who love you most have probably sensed something they cannot quite name: a slight weight to the generosity, not demanding, nothing they could articulate without sounding ungrateful, but present. A quality in your giving that is not quite overflow but more like the giving of a person who is quietly uncertain whether they have enough — and who is giving in order to make sure the account stays open.",
    "<b>The Ambassador is not your enemy.</b> He is a younger version of you who learned, under real conditions, that warmth was the price of connection and that connection kept you safe. He has been faithful. He has kept you in relationship, kept the rooms you inhabit at a temperature where human beings can live together. But he has been running your emotional life on a model that does not balance: giving out more than you are taking in, keeping the ledger off the books, telling himself that real love keeps no record — while quietly, unconsciously, keeping a record of every entry on the other side.",
]

AMB_BODY_P3 = [
    "What does it look like to begin retiring him, in the dignified sense of the word — not eliminating the warmth, which is real and good and the world genuinely needs — but beginning to disentangle the giving from the earning? Beginning to serve from a place of security rather than from a place of need? This is not a single decision. It is the slow, daily practice of receiving the love that has already been given to you, before you do anything to merit it, and then allowing what flows from that to be what you give.",
    "It begins with naming the assumption the Ambassador has been operating under: <i>I am safest when I am giving. My acceptability in this relationship is earned by my warmth.</i> That assumption is not merely emotionally exhausting. It is, examined in the light of the gospel, a quiet but real rejection of grace. It says: <i>I must earn my place.</i> But the gospel says your place was given to you, at enormous cost, before you had given anything to merit it. The Ambassador believes this doctrinally. He nods at it in sermons. He has not yet believed it in the place where the giving happens.",
    "The exercise below is different from the one you would find in some other walkthroughs. I am not asking you to write to the Ambassador. I am asking you to let the Ambassador write to you — to hear, in his own voice, what he has been doing and why, and what he is afraid would happen if he stopped. The Ambassador has never had this conversation. He has been too busy warming up every room to sit down and be honest about what the warming has cost him.",
]

AMB_LETTER_INSTRUCTION = [
    "The letter below is written in the Ambassador's voice — from him, to you. He is not a villain. He is exhausted, and he is frightened, and he is more ashamed than he has let on. Read it slowly. Do not manage your response to it. Then answer the three prompts that follow.",
]

AMB_LETTER = """\
Dear friend,

I want to tell you something I have never allowed to be said, because saying it would require sitting still long enough, and I have never sat still long enough. I have been afraid of what would happen if the warmth stopped.

I learned very early that warmth was not merely a gift I could offer but a condition on which things depended. If I was warm, the room was warm. If I was warm, the people I loved stayed near. If I was warm, the question I have been carrying since I was very young — whether I am acceptable as I actually am, underneath the warmth — did not have to be answered out loud. The warmth answered it provisionally, for the duration of each gathering. And then I woke up the next morning and it had to be answered again.

I have been keeping a record. Not deliberately — I would have denied it if you had asked, and I would have believed my denial. But somewhere below the surface of the giving, I have been keeping count. Of the times I gave and the giving was absorbed without acknowledgment, the way furniture is absorbed, as though it simply belonged in the room. Of the times the temperature dropped in someone whose warmth I depended on, and I worked harder to bring it back, and the working harder was never the same as being genuinely wanted. I told myself the ledger was closed. What I did not see was that I was keeping a record of my own giving while telling myself the book was shut.

I am more afraid than I have admitted. And I am more needy than I have allowed you to know. I want — with a specificity I have never spoken out loud — to be known as I am, not as I appear, and to be found acceptable anyway. I do not know how to get there while I am still running the warmth. I think I need to stop. I do not know who I am if I stop.

The Ambassador
"""

AMB_LETTER_PROMPTS = [
    "What is the one sentence in that letter you most wanted to put down and not finish reading? What does your resistance to it tell you about what the Ambassador has been protecting?",
    "The Ambassador says he has been keeping a record while telling himself the book was closed. Name one specific relationship or season in your life where this was true. What was on the record that you have never spoken aloud?",
    "The Ambassador says: <i>I want to be known as I am, not as I appear, and found acceptable anyway.</i> What would it cost you, practically and specifically, to let one person — just one — see the interior that the warmth has been covering? Name the person. Name the cost. Do not soften either.",
]

MASK_BODY_P1 = [
    "Every mechanism has a place where it breaks, and for the Ambassador, the breaking has a shape that is, among the six breakdowns in this series, uniquely difficult to address \u2014 not because it is the most dramatic, but because it is the most invisible. The Ambassador who breaks does not argue. Does not collapse. Does not go cold. Instead, when the wound becomes too deep to manage through warmth alone, something far more sophisticated engages. This breakdown is called <b>the Mask</b>.",
    "Here is how it happens. Something arrives that the giving cannot absorb \u2014 a wound too specific, a withdrawal too extended, a moment in which someone reveals that the acceptance the Ambassador has been earning is more conditional than believed. The old question wakes: <i>Am I acceptable?</i> And for the first time in a long time, the warmth does not answer it. In that moment, the Ambassador does not show the wound, does not petition for comfort. Instead, a persona engages \u2014 not a fabricated self, but a functional, credible, entirely convincing version of the Ambassador that can handle this moment without letting the wound show. The Mask slides on. The person wearing it continues to love, to serve, to minister \u2014 genuinely, or close enough to genuinely that no one, not even the Ambassador much of the time, can locate the seam between the performance and the person.",
    "Charles Haddon Spurgeon, who knew something about the difference between public warmth and private anguish, gave a warning worth holding: <i>a smiling face may cover a heart in flight from God.</i> He was not speaking of hypocrisy in the common sense, but of something more subtle: the person whose public face is so consistently warm, so evidently given to the care of others, that no one \u2014 including the person herself \u2014 thinks to ask what the smile is covering. This is the Ambassador who has put on the Mask. The face is real. The smile is real. What it is covering is also real, and it has never been spoken.",
]
MASK_BODY_P2 = [
    "The Mask is not lying. That is what makes it so extraordinarily durable, and so extraordinarily dangerous. Almost everything the Mask presents is true. You do care about the people in the room. The warmth is not performed in the sense of being false. The Mask does not fabricate; it selects. With remarkable precision, it chooses which parts of the true self to offer — the warmth, the attentiveness, the generosity — and it keeps the wounded, uncertain, shame-carrying interior behind a door that looks, from outside, exactly like what a healthy, sanctified, others-centered Christian person looks like.",
    "The specific genius of the Ambassador-Mask combination is that the Mask is built from the Ambassador's finest materials. The warmth that conceals the wound is the same warmth that is genuinely beautiful and genuinely given. The giving that keeps the question from having to be answered is the same giving that others have called ministry, have called grace, have called Christlikeness. <b>The gift and the hiding wear the same face.</b> And because they wear the same face, the people around the Ambassador+Mask will be the last people on earth to name what is happening. They will name the warmth. They will celebrate the giving. They will hold this person up as a model of what Christian love looks like. They will be right about everything except the room behind the smile.",
    "Dietrich Bonhoeffer, in <i>The Cost of Discipleship</i>, wrote one of the most searching and uncomfortable sentences in twentieth-century Christian literature: <i>Cheap grace is the deadly enemy of our church.</i> He was writing about a particular failure of the German church, but the diagnosis goes far deeper. Cheap grace, as Bonhoeffer understood it, is grace received as doctrine but never as death — grace affirmed from the outside without the cross that produces it doing its work on the inside. The Ambassador+Mask does not reject the grace of the gospel. The Ambassador+Mask has built an entire public ministry on the language of grace. But the question the Mask prevents from being asked is precisely the question that genuine grace is designed to answer: <i>Am I acceptable as I actually am, in the part that no one sees?</i> Cheap grace is, for the Ambassador, the grace that keeps the wound comfortable, keeps the question at a manageable distance, keeps the warmth flowing — without ever requiring the exposure that true justification both demands and provides.",
    "Jesus, in Matthew 23 — the most direct confrontation in all four gospels — spoke with a precision that should catch in the throat of every Ambassador who has been wearing the Mask. <i>You are like whitewashed tombs, which outwardly appear beautiful, but within are full of dead people's bones and all uncleanness. So you also outwardly appear righteous to others, but within you are full of hypocrisy and lawlessness.</i> (Matthew 23:27\u201328) The Pharisees were not bad men pretending to be good. Many were genuinely warm, genuinely given to their communities, genuinely believed to be models of the devout life. They were Ambassadors who had become Masks. The religious performance was not a cover for wickedness; it was a cover for the wound — one that had never been brought to God in the way genuine repentance requires: not as a managed disclosure, but as the full interior, offered to the only One who can receive it without being scandalized.",
]

MASK_BODY_P3 = [
    "The problem the Mask creates is not merely personal. The self that the Ambassador+Mask has built \u2014 warm, giving, ministry-oriented, beloved by the community \u2014 feels entirely like faith, entirely like sanctification, entirely like the fruit of the Spirit. Paul, in 2 Corinthians 13:5, gives the instruction: <i>Examine yourselves, to see whether you are in the faith.</i> This is precisely the examination the Mask was built to prevent. It is, at its root, the religion of works hiding inside the vocabulary of grace \u2014 and it will keep hiding there for as long as the warmth holds.",
    "Here is the question the Mask has never been asked: <b>What would you lose if it came off?</b> Not who would leave. What would be at risk inside you if the warmth stopped? You would lose the ability to tell yourself that you are acceptable. The warmth has been, for a very long time, the only evidence you have been able to produce. If it stops, the question comes back full-size, unanswered. The Mask is the only kindness the shame question has ever been offered \u2014 and it is costing you the one thing you were made for: to be known as you are, by the God who made you, and found not merely tolerable but beloved.",
    "Peter, who knew warmth and performance in equal measure, was asked three times by the risen Christ: <i>Do you love me?</i> (John 21:15\u201317) Not because Christ did not know the answer, but because Peter needed to say the true thing out loud, with nothing between him and the words. Three times. The Mask does not survive that question, because it insists on the unmediated self, and the Mask can only offer the mediated one.",
]
MASK_PROMPTS = [
    "Name the last time the Mask went on — not the dramatic version, but the ordinary one: the moment the wound fired and you became warmer, more present, more giving, specifically because you could not afford to let the wound show. What had just happened? What did you offer the room? What were you actually feeling while you offered it?",
    "The Ambassador+Mask is the leader everyone says yes to — the person whose community will be reluctant to name what is happening because everything looks like love. Name one person in your life who has come the closest to naming it. What did they say, or almost say? What stopped you from letting them finish?",
]

TWO_TOG_BODY = [
    "Now we put them next to each other, because the Ambassador and the Mask are not two separate problems. They are the same soul, organized around the same fear, wearing two different faces. <b>The Ambassador is what your fear does when it has warmth to work with.</b> The Mask is what it does when the warmth is not enough. Together they form a closed system in which the shame question can be kept at a safe, ministry-covered distance indefinitely. Until something breaks it open.",
    "The pattern, in slow motion, looks like this. <b>(1)</b> The Ambassador moves through the world giving \u2014 warmth, attention, service \u2014 because giving feels like love and love feels like acceptance. <b>(2)</b> Something happens: a withdrawal, a moment of exposure. <b>(3)</b> The trigger fires: <i>something is wrong with me and they can tell.</i> <b>(4)</b> The core question wakes: <i>Am I acceptable?</i> <b>(5)</b> The Ambassador responds by warming up further. <b>(6)</b> When that is not enough, the Mask engages: composed, warm, apparently fine, performing the Christlike life so convincingly that no one looks behind it. <b>(7)</b> The wound goes underground. The loop restarts.",
    "What breaks this loop is not more warmth, and it is not a more convincing persona. It is a different answer to the question \u2014 received, not earned; given, not generated. Until the Ambassador receives, really receives, not as a doctrine to affirm but as a verdict to rest in, that he is already acceptable in the only court that finally matters, the loop has nothing to push against. With that answer received and practiced, the Ambassador begins to give from a different place: not to earn acceptance, but to share the acceptance already given. Fill in your sequence below. Read it aloud when you finish. Both the Ambassador and the Mask lose some of their grip when they hear themselves named in plain speech.",
]
TWO_TOG_TEMPLATE = (
    "When I encounter ____________________, something in me reads it as exposure, "
    "and the old question wakes up: <i>am I acceptable?</i> My first move is to "
    "____________________, because the Ambassador in me believes that if I can "
    "____________________, the question will not have to be answered. When that is not "
    "enough, the Mask engages: I become ____________________ \u2014 and the room receives "
    "____________________ while the wound goes underground. What I am actually after, "
    "underneath all of it, is the verdict ____________________ \u2014 a verdict Christ "
    "has already spoken over me, not earned but given, in ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of tools, each simple enough to carry and honest enough to use. None of them will resolve in a week what years have put in place. All of them, practiced faithfully over months, will begin to loosen the grip of the loop you just named.",
    "I have divided them into two sets: tools for when the Ambassador is overworking its warmth — when giving has tipped from love into survival — and tools for when the Mask is going on, for the narrow window between the wound and the concealment. The Ambassador's tools come first, because the Mask cannot be addressed usefully until the mechanism that produces it is understood. Both sets are small. Use one before you reach for five.",
]

AMB_TOOLS = [
    ("The motive audit", "Once a week, ask one question about the most significant giving you did in the past seven days: <i>was this warmth given freely, as an overflow of love already received — or was it given in part to secure something, to keep the temperature up, to prevent the question from having to be asked?</i> Do not scold yourself for what you find. Simply name it. The Ambassador loses power when required, once a week, to account for its own motives."),
    ("The gift received", "Each day, practice receiving something from someone without immediately giving something back. A compliment, an offer of help, a text that says you are being thought of. Let it land without deflecting or redirecting the attention back to them. The Ambassador is extraordinarily practiced at giving and unpracticed at receiving. Receiving is not passivity. It is where the gospel lands."),
    ("The Abba prayer before the giving", "Once a day, before you have done anything warm for anyone, say aloud: <i>Father, I am your child. Not your employee. Your child. I am acceptable before I have given anything today.</i> This establishes the right order: accepted first. Warmth after. The warmth that comes after will be different from the warmth that comes before."),
    ("One unexpressed need per week", "Once a week, name one genuine need and express it to one person directly — without framing it as a concern for them, without the warmth that makes the ask feel less like an ask. The shame question cannot be answered while you are managing the answer by making yourself warm. Asking a need is the first act of letting someone love you without your earning it."),
    ("The handed-back ledger", "Each evening, name one thing you gave today that you quietly hoped would be noticed or returned. Then say, aloud: <i>Lord, I hand this entry back to you. The account is yours to keep, not mine.</i> This is the daily practice of returning the ledger to the only Treasurer qualified to hold it."),
]

MASK_TOOLS = [
    ("Name the seam", "The Mask has a seam \u2014 a moment between the wound and the slide, before the ministry-ready self has fully engaged. Your only task is to notice it: <i>the wound fired. I am now managing the presentation.</i> Noticing is not stopping. But noticing is the beginning of choice, and choice is what the Mask has been preventing."),
    ("The three-word honesty prayer", "In the moment after the wound fires, say these three words silently to God: <i>I am hurting.</i> Not as a petition \u2014 simply as a statement of what is true, said to the one Audience who already knows and has not turned away. Three words, said honestly, interrupt the underground process at its root."),
    ("The deferred confession", "You will not always be able to take the Mask off in the moment. But within twenty-four hours, find the one person you trust most and say: <i>I put the Mask on yesterday when ___. What was actually happening was ___.</i> One honest sentence, spoken to a safe witness, breaks the secrecy that gives the Ambassador+Mask its power."),
    ("The Matthew 23 examination", "Once a month, read Matthew 23 slowly \u2014 not as a description of people unlike you, but as a mirror. Ask: <i>is there a version of this whitewashing in my own ministry?</i> This is not self-condemnation. It is costly grace \u2014 the grace that requires the whole self, not the presented version."),
    ("The advocate prayer when the Mask is on", "When the Mask is on and you can feel it: <i>Lord Jesus, you were exposed for me. You did not manage the impression. You absorbed the exposure I most fear and reversed its verdict. I do not have to manage mine. Help me receive it rather than perform it.</i> Give this prayer the same trust you give the warmth."),
]
PRAYER_BODY = [
    "Father,",
    "You see the Ambassador in me, and you see the Mask he wears, and you are not surprised by either of them. You know why I built them both. You know the specific households and seasons in which I learned that warmth was safer than honesty and that the managed self was safer than the real one. Thank you that you were present for those moments, and that you did not look away, and that you are not looking away now.",
    "Father, I am tired of the management. I am tired of warming rooms I am not actually in, of giving in ways that are not entirely free, of the way I can love people all day and come home feeling that no one has actually been with me \u2014 because I have not allowed anyone to be with me, only with the version of me I decided was safe. Teach me, slowly, what it means to be seen as I actually am and not abandoned. Teach me to let the people who love me come further in. Teach me to say the true thing before the warmth has assembled around it.",
    "Lord Jesus, you stood before Pilate and did not make yourself more presentable. You stood before the crowd and did not turn it warmer. You absorbed the exposure I most fear, in your own body, so that the verdict spoken over me would be covered, clean, beloved \u2014 not earned, given; not performed into existence, spoken. Help me receive that verdict not merely as doctrine but as the felt covering of a soul that has been managing its own acceptability for a very long time.",
    "Holy Spirit, where the Mask goes on today, give me the grace to notice it. Where I am warming a room in order to keep the question from having to be asked, give me the courage to set the warmth down for one moment and simply be present as I am. Where the shame question rises in me, remind me of the answer already spoken at the cross, in a form that no subsequent exposure can overturn.",
    "In the name of the One who asked Peter, three times, to say the true thing out loud \u2014 not the warm thing, not the presented thing, but the true thing \u2014 I pray.",
    "Amen.",
]
GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Ambassador and the Mask have been with you a long time, and they will not retire after one afternoon's reading. What follows is a short list of next steps \u2014 some for the coming week, some for the longer work ahead.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.", "Different sections will land differently the second time. The Mask will try to let you read this efficiently the first time, to extract the useful parts without being changed by them. The Ambassador will give this document a warm reception and then go check on how everyone else is doing. Read it again slowly, thirty days from now, and notice which paragraphs you could not fully receive on the first pass."),
    ("Take one tool, not six.", "Choose a single practice from Section Seven and try it for two weeks before adding another. Choose the one that felt most uncomfortable \u2014 not the one that felt most manageable. Tools that cost nothing protect nothing. The Mask is specifically designed to make the costly practices feel unnecessary. They are not unnecessary. They are the point."),
    ("Tell one person what you found.", "Not the whole document. One sentence: <i>I learned that my mechanism is the Ambassador and my breakdown is the Mask \u2014 that I hide behind warmth, and that the warmth is both real and a strategy, and I am learning to tell the difference.</i> The Ambassador+Mask lives in communal admiration and private aloneness. Breaking the secrecy once, with one trusted person, changes the architecture of the loop."),
    ("Read Tim Keller's Counterfeit Gods.", "Keller's treatment of the things we place at the center of our identity \u2014 the things we serve as gods while believing we are serving God \u2014 will address the Ambassador's specific pattern with precision. The counterfeit god of the Ambassador+Mask is not money or success or security. It is acceptability. Keller will name it, and the naming will be uncomfortable, and that discomfort is the beginning of something."),
    ("Read C. S. Lewis's The Four Loves.", "Lewis's chapter on affection and his observations on the dangerous asymmetry of love that gives and gives without allowing itself to receive will give you language for what the Ambassador has been doing and what the Mask has been preventing. He writes about the interior life with the kind of unguarded honesty the Mask has been making very difficult for you. Let him model it."),
    ("If you are stuck, ask for help.", "There are seasons when the Ambassador and the Mask are too entrenched to dislodge alone \u2014 which is, of course, precisely the kind of admission the Mask was built to prevent. A wise pastor, a Christian counselor, a trusted friend who has earned access to your interior \u2014 these are not signs of failure. For the Ambassador, asking for this kind of help is itself the most countercultural act this walkthrough can recommend. The Mask will tell you it is unnecessary. It is not unnecessary. It is where the loop finally breaks."),
]

GOING_FURTHER_CLOSING = (
    "You are not a project to be warmed into acceptability. You are a son or daughter "
    "being loved into freedom by a Father who has already seen everything the Mask was "
    "built to hide \u2014 who has seen behind the warmth, behind the ministry, behind the "
    "composed and giving and beautiful self you have offered the world \u2014 and who has "
    "not changed his mind about you. His love for you is not a function of your warmth. "
    "It was decided before you had given anything, and it will hold after everything you "
    "have given has been spent. Go gently. The One who began this work in you "
    "will be the one to finish it."
)


def _three_column_table(rows=7):
    """Three-column journal table for the shame/acceptability reflection exercise."""
    col_w = (PAGE_W - MARGIN_L - MARGIN_R) / 3.0
    header_style = ParagraphStyle(
        "AMBMColHeader", fontName="Inter-SemiBold", fontSize=9, leading=12,
        textColor=ACCENT)
    sub_style = ParagraphStyle(
        "AMBMColSub", fontName="Inter-Italic", fontSize=8.5, leading=11,
        textColor=MUTED, spaceBefore=2)
    header_row = [
        [Paragraph("THE MOMENT", header_style), Paragraph("what happened, briefly", sub_style)],
        [Paragraph("WHAT I SHOWED", header_style), Paragraph("the Mask\u2019s offering", sub_style)],
        [Paragraph("WHAT WAS ACTUALLY TRUE", header_style), Paragraph("the interior the warmth covered", sub_style)],
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
            "AMBMCalloutLabel", fontName="Inter-SemiBold", fontSize=9, leading=13,
            textColor=ACCENT, leftIndent=12, spaceBefore=2, spaceAfter=4)))
    body.append(Paragraph(text, ParagraphStyle(
        "AMBMCallout", fontName="Inter", fontSize=10.5, leading=17,
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
    """Generate the Ambassador+Mask walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='AMB', primary_breakdown='MASK',
    primary_trigger='SHM', core_question='ACC'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="AMBASSADOR  \u00b7  MASK",
        title="Take 139 Walkthrough \u2014 Ambassador + Mask",
    )

    story = []

    # \u2500\u2500 COVER \u2500\u2500
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("TAKE 139", S["CoverEyebrow"]))
    story.append(Paragraph("A Counselor\u2019s<br/>Walkthrough", S["CoverTitle"]))
    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph(
        "A patient conversation about the warmth you give every room<br/>"
        "and the wound no room has ever been allowed to see.",
        S["CoverSub"]))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph("PREPARED FOR YOU", S["CoverProfileLabel"]))
    story.append(Paragraph("The Ambassador &nbsp;\u00b7&nbsp; The Mask", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Shame &nbsp;\u00b7&nbsp; Core Question: Am I acceptable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cCheap grace is the deadly enemy of our church.<br/>"
        "We are fighting today for costly grace.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "Dietrich Bonhoeffer, <i>The Cost of Discipleship</i>",
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
                   "The moment the room is still warm \u2014 and something inside you has gone very cold.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION TWO  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions, in writing.",
                   "Your head will offer a composed answer. Your hand will not.")
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 3: Core Question \u2500\u2500
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I acceptable?",
                   "The wound the alarm has been standing guard over.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "What the psalmist knew \u2014 and what the cross answers.",
                   "Already fully seen. Already not rejected.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "The gap between what I showed and what was actually true.")
    story.append(Paragraph(
        "Use the table below. In the first column, name a recent moment when the shame "
        "signal fired. In the second, describe what you showed \u2014 what the warmth "
        "presented to the room. In the third, write what was actually true of you in that "
        "moment, <i>behind the presentation</i>.",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table(rows=5))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 4: Mechanism \u2500\u2500
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Ambassador.",
                   "The caretaker. The peace-holder. The one who warms every room.")
    for p in AMB_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  CONTINUED",
                   "What the warmth has cost.",
                   "Serving and surviving, and the unsustainable ledger underneath them.")
    for p in AMB_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in AMB_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Ambassador.",
                   "Read the Ambassador\u2019s own words. He has been faithful; let him speak.")
    for p in AMB_LETTER_INSTRUCTION:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))

    letter_style = ParagraphStyle(
        "AMBMaskLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for para in AMB_LETTER.strip().split("\n\n"):
        story.append(Paragraph(para.replace("\n", " "), letter_style))

    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in AMB_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 5: Breakdown \u2500\u2500
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Mask.",
                   "The place the mechanism breaks \u2014 and the face it shows while breaking.")
    for p in MASK_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "The gift and the hiding wear the same face.",
                   "The religion of works inside the warmth, and what the gospel requires.")
    for p in MASK_BODY_P2 + MASK_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions to sit with.",
                   "Write, not think. The Mask performs better in your head than on paper.")
    for prompt in MASK_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=4)
        story.append(Spacer(1, 10))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same fear, in two faces.",
                   "The Ambassador and the Mask are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 10))
    journal_lines(story, n=4)
    story.append(PageBreak())

    # \u2500\u2500 SECTION 7: Tools \u2500\u2500
    tool_h = ParagraphStyle("AMBMToolH", parent=S["H3"], fontSize=10.5, leading=14,
                            spaceBefore=6, spaceAfter=3)
    tool_body = ParagraphStyle("AMBMToolBody", parent=S["BodyJ"], fontSize=10, leading=15,
                               spaceAfter=6)

    section_header(story, S, "SECTION SEVEN  \u00b7  TOOLS FOR THE NEXT TIME",
                   "When the Ambassador is overworking its warmth.",
                   "Five practices for the time before the alarm fires.")
    for p in TOOLS_INTRO:
        story.append(Paragraph(p, S["BodyJ"]))
    for name, desc in AMB_TOOLS:
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


# \u2500\u2500 STANDALONE TEST \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "AMB"
        primary_breakdown = "MASK"
        primary_trigger = "SHM"
        core_question = "ACC"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "ambassador_mask_test.pdf")
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    size_kb = len(pdf_bytes) // 1024

    # Count pages using pypdf
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

    print(f"DONE: ambassador_mask.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
