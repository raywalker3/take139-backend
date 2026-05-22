"""Personal Walkthrough — Vault + Quiet Exit (Verdict).

Voice: Tim Keller (from Walking with God through Pain and Suffering).
Profile: Shame trigger, "Am I acceptable?" core question.
Breakdown: Quiet Exit (VERD) — quietly decides "I'm done"; stops investing;
           withdraws into a verdict that is often invisible to the other person.

Breakdown code: VERD. Walkthrough #23 of 36.

Calibration note: This is the most legally final of all the Verdict breakdowns.
The Architect's Verdict is a planner's exit drafted in private. The Island's
Verdict is the elder brother who never left home. The Ambassador's Verdict is
an internal funeral disguised as gentleness. The Vault's Verdict is signed and
sealed in a vault that already contained the case file.

The Vault did not merely decide; it recorded the decision and filed it. Because
the Vault has organizational habits that resist re-opening any closed file, this
breakdown is the hardest of all six to retract once it has been rendered.

KEY MOVES:
- Section Five: The Vault has confused finality with peace. The verdict feels
  settled because it is filed, not because it is true.
- 1 Kings 19 Elijah under the broom tree: God did not honor his "I have had
  enough" verdict; God sent food, sleep, and a conversation in the cave.
- Lloyd-Jones (depression sermons) on the dangerous spiritual stillness that
  is not peace but resignation.
- Calvin on the difference between godly limits (which God blesses) and
  self-imposed verdicts (which God patiently undoes).

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
    "Before you read any further, I want to do for you what a good counselor does in the first session. I want to lower the lights, slow the pace, and ask you to sit with something that is, if you are honest, not a comfortable posture for you. The person this walkthrough describes does not easily sit still. Not because they are restless in the ordinary sense, but because stillness, for a Vault, has always carried a risk: that if you stop moving, stop managing, stop filing, something you have been carefully containing will surface before you have decided whether to show it.",
    "If you were sitting across from me, I would say this plainly and mean every word of it: <b>What you are about to read is true, but it is not the whole truth about you.</b> The whole truth includes a Father who does not require you to present a finished interior before he will receive you; a Son who absorbed, publicly and completely, the exposure you have spent years managing in private; and a Spirit who is, at this very moment, attending to the parts of you that have never been shown to anyone, and is not alarmed by what he finds.",
    "So read slowly. Argue with what does not fit. Stay with what does. Write in the margins if you have a pen nearby. Pray when something catches in your throat, because that catch is usually the Lord saying, <i>look here, with me.</i> The goal of this walkthrough is not insight. The goal is a slightly freer life, lived before a God who has already seen every document in every folder and has, without waiting for your summary, spoken the verdict that matters. Take your time. The chapter you are about to read about yourself has been a long time in the writing.",
]

TRIGGER_BODY = [
    "There is a moment that keeps happening to you, and it arrives without warning and leaves no visible trace. You are in a conversation, or a meeting, or a quiet evening at home, and something shifts. Someone says something that lands close to the interior \u2014 not carelessly, perhaps even kindly \u2014 but close enough that something in you moves to meet it. Not to answer it. To intercept it. To decide, in a fraction of a second, what version of yourself will be presented in response, and what will remain behind the door.",
    "The trigger is not always dramatic. Sometimes it is a specific question you were not prepared for \u2014 someone asking, with genuine care, how you really are. Sometimes it is an observation that is accurate enough to feel like a violation: a colleague noting that you seemed quieter than usual; a spouse saying something that names, precisely, a struggle you had not decided to name yet. Sometimes it is simply the sense that a conversation has moved into territory where you cannot control what is seen, and the alarm fires not because the other person has done anything wrong, but because the Vault cannot guarantee the outcome.",
    "This is your trigger. The word for it is <b>shame</b>, and that word is doing more work here than it usually appears to do. Shame is not guilt. Guilt says <i>I did something wrong</i> and points at an action. Shame says <i>something about me, as I am, might be fundamentally unacceptable</i> and points at a self. The shame trigger fires not when you have made a mistake but when the possibility of being seen \u2014 fully, without preparation \u2014 becomes real. The Vault's response to that possibility is fast, efficient, and largely invisible: close the relevant doors, present what has been selected, and maintain the appearance that nothing is being managed.",
    "<b>Your sensitivity to shame is not random, and it is not weakness.</b> It is the residue of something specific, something that happened in the history of a person who once showed something interior and the person who received it did not handle it well. Maybe they used it. Maybe they dismissed it. Maybe they simply looked at it with an expression that communicated, with terrible efficiency, that what you had offered was more than they knew what to do with. Whatever the particular history, the lesson was inscribed clearly: <i>what is shown can be weighed and found wanting, and what stays inside stays safe.</i>",
    "And so the Vault was built \u2014 not as a decision, exactly, but as a slow accumulation of choices that all moved in the same direction. Toward selectivity. Toward presenting what has been prepared. Toward a very careful management of the threshold between the interior world and the world other people can see. This is not, as I have said, a small achievement. The Vault processes things internally with a thoroughness that most mechanisms cannot match. When the Vault speaks, it has already considered what it is saying. When the Vault acts, it has already thought about the implications. These are real gifts. They serve you in many settings. But the same mechanism that makes you a careful communicator also makes the question underneath your trigger very difficult to answer, because the question can only be answered in the territory the Vault has been most systematically protecting.",
]

TRIGGER_PROMPTS = [
    "Name the last time, within the past two weeks, that the shame trigger fired in you. It does not need to be a large event \u2014 look for the moment when something in you moved to intercept: when the possibility of being seen without preparation became real, and you felt the interior door move. What happened, in two sentences?",
    "What was the size of the actual event, and what was the size of the response inside you? If the response was significantly larger than the event, you have just located your trigger. What does the gap between them tell you about what was actually at stake?",
]

QUESTION_BODY_P1 = [
    "Under every trigger is a question, and the question is older than the trigger. The trigger is the alarm; the question is the wound the alarm has been standing over, and standing guard over, for a very long time. The Vault has been guarding this question with unusual thoroughness. It has organized the defenses with care and precision. What it has not done \u2014 what the Vault almost never does \u2014 is ask the question out loud.",
    "The question is this: <b>Am I acceptable?</b>",
    "It is not quite the same as <i>Am I lovable?</i>, though the questions are neighbors. It is not <i>Am I competent?</i>, though the Vault has built impressive competence partly as a way of trying to answer it. It is something more specific and more frightening than either: <i>If someone saw what is actually in here \u2014 not the organized presentation, not the finished conclusion, not the exterior that has been carefully maintained \u2014 would they find me acceptable? Would they stay?</i>",
    "Most people would prefer to believe they have long since settled this question. They have not. They have only moved it. For the Vault, the question is particularly alive because you know the interior more honestly than almost anyone else knows theirs. The Vault has done real work in there. It has processed, honestly, the failures and fears and doubts and longings that most people leave in an unexamined pile. And it is precisely because you know what is in there that the exposure of it feels so acute. You are not afraid of a phantom self. You are afraid of a real one.",
]

QUESTION_BODY_P2 = [
    "There is a reason the theologians from Augustine through the Reformers insisted that the deepest human hunger is for justification \u2014 not merely forgiveness in the everyday sense, but the settled verdict of the court that finally matters: <i>you are acceptable. Not despite what is inside you, but acceptable \u2014 covered, held, named, kept \u2014 because of what has been done for you.</i> This hunger is not neurosis. It is the precise intuition of a creature that has a genuinely disordered interior and knows it, and longs for someone with the authority to say so to look at what is there and speak the verdict anyway.",
    "The Psalms tell the truth about this longing with an honesty that the Vault often finds either deeply comforting or quietly threatening. Psalm 139 does not permit the possibility of a hidden interior: <i>O Lord, you have searched me and known me. You know when I sit down and when I rise up; you discern my thoughts from afar. You search out my path and my lying down and are acquainted with all my ways. Even before a word is on my tongue, behold, O Lord, you know it altogether.</i> (Psalm 139:1-4) David does not end this Psalm in despair. He ends it with an invitation: <i>Search me, O God, and know my heart. Try me and know my thoughts.</i> He is asking to be seen by the one he has already acknowledged sees everything \u2014 because he has discovered, across a life lived in very honest acquaintance with his own failures, that the God who already sees does not turn away from what he finds.",
    "Paul, in 2 Corinthians 5:21, gives the theological answer with precision: <i>For our sake he made him to be sin who knew no sin, so that in him we might become the righteousness of God.</i> This is not a transaction on a ledger at a distance. This is the permanent answer to the question <i>Am I acceptable?</i> Christ took on himself, publicly and deliberately, the full weight of the shame that you have been managing internally. He was exposed \u2014 completely, without preparation, before an audience that was not sympathetic. He absorbed that exposure into himself and carried it to the grave and left it there. The one who is united to him stands before God not as acceptable-pending-inspection but as <i>covered</i>. Not as adequate-if-the-messy-parts-stay-hidden but as <i>righteous, in Christ, now and forever.</i>",
    "Here is the honest pastoral difficulty, and it is specific to you. The Vault hears this and files it accurately. You may well have the doctrine memorized. You can likely state justification with theological precision. But there is a specific difficulty the Vault has with this answer, and it is not an intellectual difficulty. The difficulty is this: <b>receiving the verdict requires letting it in.</b> Receiving means opening. It means a kind of interior permeability \u2014 an openness to being given something you did not produce, did not curate, did not present in organized form. And the Vault has spent years constructing walls specifically to prevent that kind of permeability. The gospel's answer to <i>Am I acceptable?</i> is addressed to an interior the Vault has been systematically protecting from entry. Receiving it requires the same movement the Vault most resists: letting something in without controlling what it sees.",
]

QUESTION_BODY_P3 = [
    "1 Samuel 16:7 gives the oldest version of this problem in Scripture. God says to Samuel, standing before Eliab who looks exactly right: <i>Do not look on his appearance or on the height of his stature, because I have rejected him. For the Lord sees not as man sees: man looks on the outward appearance, but the Lord looks on the heart.</i> The Vault has organized its entire strategy around the outward appearance \u2014 around presenting what has been selected, finishing what is shown before it is shown, keeping the heart behind the walls. But the God of Scripture has already entered through the walls. He does not inspect the exterior presentation. He looks on the heart, and he has been looking all along, and he has spoken his verdict not after inspection but before it, in Christ, on your behalf.",
    "Romans 8:1 is the anchor: <i>There is therefore now no condemnation for those who are in Christ Jesus.</i> Not no condemnation once you have organized the interior. Not no condemnation when the messy middle has been resolved. <i>Now. In Christ. No condemnation.</i> The Vault has been working to make the interior presentable before showing it to anyone. God has already seen it and called it covered.",
    "The work this section is asking of you is not the work of further self-inventory \u2014 the Vault already has more than enough inventory. The work is the practice of receiving the verdict. Not as a feeling, and not as a rush of relief, but as a daily, quiet return to the news that the case has been decided in your favor \u2014 not by your management but by your advocate. Before we close this section, use the table below to bring a few recent events into the light of the question and the answer together.",
]

VAULT_BODY_P1 = [
    "You have built something. You did not sit down one morning and decide to build it; it grew from years of small choices that all pointed in the same direction, and one day you looked up and it was already there. Throughout this walkthrough we are going to call it <b>the Vault</b>, and it deserves a careful introduction before we say anything about what it costs you.",
    "The Vault is not the Island. This distinction matters enormously, and I want to make it before you read anything else about the mechanism, because the two are sometimes confused and the confusion leads to pastoral missteps. The Island processes alone because that is the Island's natural wiring \u2014 the distance is temperamental, not primarily fear-driven. The Island's walls are thin; it is simply self-contained by nature, like a plant that grows best in its own pot. The Vault has thick walls with locks, and the locks were installed for a specific reason. The Island stays inside because inside is comfortable. The Vault stays inside because outside has been shown, at some point in its specific history, to be dangerous.",
    "The Vault's strategy, stated plainly, is this: <i>I will show you what I have chosen to show you, and what I have chosen to show you will have been organized and finished and considered, and what I have not chosen to show you will remain mine, and this arrangement will protect me from the specific danger that comes when unfinished things are seen and judged.</i> This is not dishonesty. The Vault does not perform a false self. What is shown is real. But it is real material that has been selected, arranged, and prepared before presentation. The messy middle \u2014 the doubt not yet resolved, the fear not yet organized into a conclusion, the grief not yet processed into something speakable \u2014 stays inside.",
    "There is a great deal in Scripture that honors the person who holds their counsel with care. Proverbs 17:27 observes: <i>Whoever restrains his words has knowledge, and he who has a cool spirit is a man of understanding.</i> The Vault has known this verse in its bones long before reading it off a page. Self-command is a genuine virtue, and the Vault exercises it with real skill. <b>The Vault is not, in itself, a sin.</b> It is a gift that has been overemployed until the gift has become a wall and the wall has become, over time, a kind of isolation that the gift was never meant to produce.",
]

VAULT_BODY_P2 = [
    "The Vault usually formed in one of several recognizable patterns, and it is worth pausing to see which of them fits your history, because the Vault that formed from one history will have slightly different specific locks than the one that formed from another.",
    "The first pattern is the history of <i>exposure that went badly.</i> You gave something interior \u2014 a genuine vulnerability, a half-formed thought, an honest confession of something difficult \u2014 and the person who received it handled it carelessly, or dismissively, or they used what you gave them in a way that cost you. The lesson was immediate and precise: <i>what I show can be turned against me.</i>",
    "The second pattern is <i>shame about the interior itself.</i> Not merely fear of how it will be received, but a genuine suspicion that what is inside is more disordered than what other people carry \u2014 that the particular textures of your doubt, failure, longing, and fear are not merely ordinary human material but something more specifically problematic. The Vault in this case is not just cautious; it is protective of something it has come to believe is, at some level, genuinely disqualifying if seen clearly.",
    "The fourth pattern is <i>a household in which expression was discouraged or distorted.</i> Perhaps feelings were handled privately and quietly, as a matter of personal management rather than shared currency. Or perhaps expression was over-valued \u2014 every difficulty made into an event, every feeling requiring an audience \u2014 and you retreated into privacy as the only available peace. Either extreme teaches the same lesson: <i>the interior is better handled alone.</i>",
    "Bonhoeffer, in <i>Life Together</i>, observed that the Christian who keeps the struggle private and brings only the resolution to the community has severed themselves from one of the great mercies of the church: the mercy of being known in one's actual condition and received anyway. The Vault brings the finished product to God and to the people it loves. It holds the process alone. And so it remains, in the deepest sense, not quite known — even in the rooms where it is most present.",
]

VAULT_BODY_P3 = [
    "What does the Vault cost you? Let me name three things directly, because the Vault is very good at acknowledging costs in the abstract and then filing the acknowledgment without sitting with the particular.",
    "It costs you <i>the intimacy you most want.</i> The question at the center of you \u2014 <i>Am I acceptable?</i> \u2014 can only be answered by someone who knows what is actually inside and chooses, freely, to stay. But the Vault's mechanism ensures that no one ever has access to that interior in its actual condition. Their love \u2014 however genuine, however consistent \u2014 is love offered to the Vault's presentation. It cannot satisfy the question because it has not been given the information required to answer it.",
    "<b>The Vault is not your enemy.</b> It is a younger version of you that learned, in some real circumstance, that the unlocked version was not safe. It has been faithful. It has kept you functioning, kept your relationships intact, kept the presentation adequate across many seasons. But it is working on a project that has long outgrown the original danger. The walls that protected you once are now preventing the one thing the question underneath your trigger most needs: to bring the actual interior into the actual light and discover that the light is not what the Vault was afraid of.",
    "Before we close this section, I want you to read a letter \u2014 not one you wrote to the Vault, but one from the Vault, in his own voice, to you. He has never been asked to account for himself honestly. He has simply been doing what he was built to do, faithfully and without acknowledgment. Read the letter slowly. Then answer the prompts below it.",
]

VAULT_LETTER_INSTRUCTION = [
    "The letter below is written in the Vault's voice. He is not cold. He is careful, and he is frightened, and he has been faithful to an assignment that cost him more than he was able to say. Read it without hurrying. Then answer the three prompts that follow.",
    "Dear [your name],",
    "I want to tell you something I have never been given the opportunity to say, because no one has ever been able to see me clearly enough to ask. I want to tell you what I have been doing, and why, and what I am afraid will happen if I stop.",
    "I have been keeping a file. Not as a conscious project \u2014 not as something I decided. But everything that has come in \u2014 every wound, every moment of exposure that went badly, every grief I processed before showing anyone the conclusion \u2014 has been organized. Filed by date. Cross-referenced. I am thorough in all things. This is no different.",
    "I built the walls because the alternative was worse. I know you do not remember every specific moment, but I remember each one. I learned what you learned: that the finished version is safer than the unfinished one, and that the messy middle belongs to us alone. Not because you are too proud to share it. Because the evidence said that sharing it produced outcomes I could not protect you from.",
    "The system has worked. The interior has stayed interior. But I want to tell you something that costs me something to say. I have kept the file so long that I have begun to confuse the keeping of it with the closing of it. When a wound came that I could not process to a conclusion, that stayed raw inside no matter how I organized it, I quietly began to close the account. I reduced the investment, withdrew the hope, moved the care slightly further from the surface. I called it honest accounting. I am not certain, any longer, that it was. The verdict was settled in a private court where the other party had no representation.",
    "I am still here. And I am still filing. And I would like, if it is possible, for someone to tell me whether the verdict was mine to render.",
    "The Vault",
]

VAULT_LETTER_PROMPTS = [
    "What part of the Vault's letter surprised you most? Not the part you saw coming \u2014 the part you were not quite ready to read.",
    "The Vault says he has been making a mistake: confusing the keeping of the file with the closing of it. Can you name one specific account he has closed \u2014 one relationship or situation in which the Vault rendered a private verdict and began to withdraw? You do not need to resolve it here. Simply name that the file exists.",
    "The Vault asks whether the verdict was his to render. What would need to be true \u2014 about God, about one other person, about safety \u2014 for the Vault to hold a door open that he has been closing?",
]

VERD_BODY_P1 = [
    "Every mechanism has a place it breaks. The Vault's breakdown is called <b>the Quiet Exit</b>, and of all six breakdowns in this taxonomy, the Vault's version of it is the most legally final. I say that carefully and with pastoral intention, because the difference between the Vault's Quiet Exit and the Island's, or the Ambassador's, or the Architect's is not a difference in degree. It is a difference in kind. And the difference matters for what the pastoral work of this section will require.",
    "Here is the specific difference. The Island who renders a Quiet Exit is the elder brother who never left home: he has been present all along and has already gone in the only sense that matters, conducting his departure invisibly from inside the household. The Ambassador who renders a Quiet Exit is an internal funeral disguised as gentleness: a person who has given love long enough to conclude, with great sadness and great weariness, that it is not coming back. The Architect who renders a Quiet Exit has made a planner's calculation: the cost-benefit analysis has been run and the investment has been withdrawn.",
    "The Vault's Quiet Exit is different from all of these. The Vault's Quiet Exit is signed and sealed in a vault that already contained the case file. The Vault did not merely decide. It <i>recorded</i> the decision, organized it into the filing system, and closed the folder. The verdict has a date. It has supporting documentation. It has been cross-referenced against prior exhibits. And because the Vault's organizational habits are what they are \u2014 because the Vault does not, by nature, re-open closed files \u2014 this verdict is the hardest of all six to retract. Not because the Vault is harder-hearted than the others, but because the Vault has given the verdict the same organizational finality it gives to everything it determines to be settled.",
    "Elijah, in 1 Kings 19, gives us the most dramatic scriptural picture of this moment. He had just experienced the single greatest spiritual vindication of his prophetic career \u2014 the fire on Carmel, the prophets of Baal, the rain that ended the drought. And then Jezebel sends a threat, and Elijah runs. He goes a full day's journey into the wilderness and sits under a broom tree and says, plainly and in prayer: <i>It is enough; now, O Lord, take away my life, for I am no better than my fathers.</i> (1 Kings 19:4) This is a verdict. Elijah has assessed the evidence, run the calculation, and concluded: <i>I am done. The account is closed.</i> The remarkable thing is not that he said it. It is what God did in response.",
]

VERD_BODY_P2 = [
    "God did not argue with Elijah. He did not rebuke the verdict, or challenge the theology of it, or produce a counterargument. He sent an angel with food and water. Twice. He let Elijah sleep. And then, forty days later, in a cave on Horeb, he asked a question: <i>What are you doing here, Elijah?</i> (1 Kings 19:9) Not an accusation. A genuine question \u2014 the kind a pastor asks someone who has closed an account and needs to be invited back into the conversation about whether the closing was premature. And Elijah's answer is the Vault's answer exactly: <i>I, even I only, am left, and they seek my life, to take it away.</i> The file has been organized. The conclusion has been drawn. The case is closed.",
    "What God gave Elijah was not a theological correction. It was not a rebuke of his discouragement. It was an honest conversation in which the conclusion Elijah had drawn was gently, persistently, refused the status of a final verdict. <i>Go out and stand on the mount before the Lord.</i> Not: <i>your verdict is wrong.</i> Rather: <i>there is more story than the file you are holding, and I am not finished, and the account you have closed still belongs to me.</i> And at the end of the conversation, after the still small voice, God gave Elijah a next step. Not a reassurance that things would feel better. A task. Because the Vault's Quiet Exit is most effectively interrupted not by argument but by commission \u2014 by the discovery that the story God is writing has a chapter that the filed verdict had not accounted for.",
    "D. Martyn Lloyd-Jones, in his sermons on spiritual depression, observed with characteristic precision that the most dangerous spiritual condition is one that has acquired the characteristics of peace without its substance. He was not speaking primarily of gross sin; he was speaking of the composed, organized withdrawal of a soul that has decided, quietly and on apparently reasonable grounds, that it has had enough. He called this a stillness that is not rest but resignation \u2014 and he warned his congregation that the danger of it is precisely that it does not feel dangerous. It feels like arrival. It presents as maturity. <i>I have come to terms with this. I have stopped expecting more than is realistic. I have found a certain equanimity.</i> These sentences sound like wisdom. They can also be the Vault's most sophisticated account entry: the filing of hope under the heading of naivete, neatly and with a date.",
]

VERD_BODY_P3 = [
    "Here is the pastoral distinction that this section must make, and it must be made with care because the Vault will be quick to use the distinction to re-file the verdict under a different heading. There is a genuine and God-honored category of godly limits. Calvin, in his treatment of Christian liberty in the <i>Institutes</i>, wrote of limits that God himself establishes for the protection of a soul that has been genuinely harmed \u2014 the acknowledgment, in some circumstances, that a relationship has reached the boundary of what one person's faithfulness can sustain, and that naming that boundary is not unbelief but wisdom. God does not require the soul to remain infinitely permeable to ongoing harm. There are seasons in which the closing of a door is the right action, and the one who closes it is not rendering an unauthorized verdict but simply acknowledging what God has already permitted to end.",
    "The Vault's Quiet Exit is usually not this. The Vault's Quiet Exit is usually a verdict rendered on the basis of accumulated evidence, organized with the Vault's characteristic thoroughness, in a private court where the other party had no representation, on a question that was never honestly put to the relationship. The Vault has not said, out loud, in the hearing of the other person: <i>I need to know if this is safe. I need to bring you what is actually inside and find out what you do with it.</i> The Vault has not done that, because the Vault's mechanism is specifically constructed to avoid exactly that test. And yet the Vault has rendered a verdict on the basis of what it imagines the outcome of that test would be. This is the problem Calvin is pointing at when he distinguishes godly limits from self-imposed verdicts: the godly limit follows an honest process; the self-imposed verdict substitutes a private conclusion for the honest test.",
    "<b>The pastoral word to the Vault is not that the file is wrong.</b> The wounds are real. The evidence is accurate. The specific dates and contexts are not imagined. The pastoral word is this: a file is not a verdict, and a verdict rendered by you alone, in a private court, without allowing the other party to answer, is not the final word on a story that God has not yet finished writing. Romans 8:1 \u2014 <i>There is therefore now no condemnation for those who are in Christ Jesus</i> \u2014 is the gospel's interruption of every verdict rendered in a court where God was not the judge. Including yours. The file does not need to be sealed. The verdict does not need to be finalized. The One who has already seen everything in the folder has not issued the closing statement on the relationship or situation the Vault has been quietly exiting.",
]

VERD_PROMPTS = [
    "Name the relationship or situation in which the Vault's Quiet Exit has most recently been active. You may not have announced it; you may barely have admitted it to yourself. Describe what it has felt like from the inside: has it been a single moment of closing, or an accumulation of small reductions in investment and hope that you noticed only in retrospect?",
    "Ask yourself the honest question: <i>Is the verdict I have rendered in this situation a godly limit that God himself has given me \u2014 or is it a conclusion I reached alone, on evidence organized in a private court, on a question that was never honestly put to the relationship?</i> Write the most honest answer you can. Do not edit it for acceptability.",
]

TWO_TOG_BODY = [
    "Now we place them next to each other, because the Vault and the Quiet Exit are not two separate problems. They are the same wound organized in two different modes, at two different stages of the same management project. The Vault organizes the interior for safety. The Quiet Exit organizes the interior for closure. Both are working with the same long accumulation of what has been kept inside, and both are trying to answer the same question \u2014 one in the mode of defense, one in the mode of finality.",
    "<b>The Vault is what your fear does when it still has time.</b> The Quiet Exit is what your fear does when it has run out of time and reached a conclusion. The Vault files carefully so the wound will not have to be shown. The Quiet Exit files the verdict so the wound does not have to be felt any more. Together they form a closed system \u2014 the most tightly organized closed system among all thirty-six profiles \u2014 and it will run all your life if nothing interrupts it from outside.",
    "The pattern, in slow motion: <b>(1)</b> The Vault manages the interior \u2014 presenting finished conclusions, filing what cannot be shown, maintaining the outer presentation. <b>(2)</b> A wound arrives that is too large for the usual management. The trigger fires: <i>something has been seen that I did not authorize.</i> <b>(3)</b> The question wakes up: <i>Am I acceptable?</i> <b>(4)</b> The Vault takes the wound inside. <b>(5)</b> The wound joins the file. It is labeled and dated and cross-referenced. <b>(6)</b> This happens again. And again. <b>(7)</b> At some point, the file reaches a threshold the Vault has never announced to anyone, including itself. The folder closes. <b>(8)</b> The Quiet Exit begins \u2014 not loudly, not visibly, but in the quiet reduction of investment and hope. <b>(9)</b> Because the withdrawal looks exactly like the Vault's normal composure, no one notices. The departure continues. The story God had not finished writing is quietly filed under a heading that says: <i>closed.</i>",
    "What breaks this loop is not better file management. It is not a more sophisticated organizational system. It is a different answer to the question \u2014 received, not merely affirmed \u2014 at the level where the filing happens. Until the Vault receives, in the interior where the organization occurs, that the God who already sees every document has spoken the verdict <i>acceptable, covered, in Christ, now and forever</i>, the loop has nothing to push against. With that answer practiced over time, in the specific pastoral disciplines that Section Seven will name, the Vault begins to find less need for the locks. The Quiet Exit begins to reverse. Not because the file was wrong, but because the verdict in the file was rendered in a court that has now been superseded.",
]

TWO_TOG_TEMPLATE = (
    "When I am ____________________, something in me reads it as exposure \u2014 as being seen "
    "in a way I did not authorize \u2014 and the old question wakes up: "
    "<i>am I acceptable?</i> My first move is to ____________________, because "
    "the Vault in me believes that if I can ____________________, the interior "
    "will remain safe. When a wound is too large for that management, it goes "
    "into the file and becomes ____________________. Over time, the file reaches "
    "a threshold and the Vault quietly begins to ____________________. The Exit "
    "feels like ____________________, but what it actually is, underneath, is "
    "____________________. What I most need is not a better filing system but "
    "the truth that ____________________."
)

TOOLS_INTRO = [
    "What follows is not a program. It is a small set of practices, each one honest enough to matter and concrete enough to use. None of them will dissolve the Vault's pattern in a single application. All of them, practiced over months, will loosen the grip of the loop you have just named.",
    "I have divided them into two sets: tools for when the Vault is overworking its defenses \u2014 when the management of the interior has tipped from wisdom into hiding \u2014 and tools for when the Quiet Exit has begun or is beginning, and you need something to interrupt the closing before it becomes the kind of final that the Vault, by nature, does not re-open. The Vault's tools come first, because the Quiet Exit cannot be interrupted usefully until the mechanism underneath it is understood and, in some measure, named.",
]

VAULT_TOOLS = [
    ("The half-built house practice",
     "Once a week, share one thing with one trusted person before it is organized into a conclusion. Not a crisis, not a resolved question \u2014 simply something you are in the middle of: a question that has not yet answered itself, a feeling not yet processed into a position. The Vault will insist this is premature. Do it before you know what you think. Over a month, the practice begins to demonstrate that unfinished things, shared with care to a trusted person, do not produce the catastrophe the Vault has been guarding against."),
    ("The audit of what is being filed",
     "Once a week, ask: <i>What went inside this week that I have not named to anyone?</i> You do not need to disclose it all at once. Simply name, to yourself and if possible to God in prayer, that the material exists and is in there. The Vault's most dangerous work is invisible. Naming the contents \u2014 even privately \u2014 begins to interrupt the automatic filing reflex before it becomes permanent."),
    ("The Psalm of the searched heart",
     "When the Vault is in full management mode, open to Psalm 139 and pray it aloud \u2014 all of it, not selected verses. It does not end in shame. It ends in an invitation: <i>Search me, O God, and know my heart. Try me and know my thoughts. And see if there be any grievous way in me.</i> (Psalm 139:23-24) The Vault needs practice asking to be known by God before it can practice asking to be known by people. The Psalm models that practice, in the prayer of a man who had more in his interior than he was comfortable with and brought it to God anyway."),
    ("The one-degree opening",
     "Identify one person who has demonstrated, over time, that they can be trusted with your interior. Choose one item from the file \u2014 one old grief, one unresolved question, one thing you have been carrying alone \u2014 and name it to that person. Not as a test, not as a full disclosure, but as a practice of the thing the Vault most resists: bringing the unfinished version into another person's presence before it is resolved. The Vault was built to prevent precisely this. That is why it is the most important item on this list."),
    ("Receive the verdict before you file the wound",
     "When the shame trigger fires, before the wound goes into the filing system, say aloud: <i>God has already seen this, and the verdict is covered. I am in Christ. There is therefore now no condemnation. I do not need to manage this alone.</i> (Romans 8:1) The Vault's instinct, the moment a wound registers, is to receive it silently and begin organizing. This practice interrupts the organizing and replaces it with the gospel's prior answer to the question the wound re-opens."),
]

VERD_TOOLS = [
    ("The age test for the file",
     "When the Quiet Exit is active \u2014 when you notice that investment and hope have been reducing in a specific relationship or situation \u2014 ask: <i>How old is the oldest document in this file?</i> If the answer is more than a month, you are not responding to a fresh wound; you are executing a verdict based on accumulated history. The pastoral difference between processing a current wound and enforcing a prior verdict is enormous. Name which one is happening."),
    ("Name the verdict before it seals",
     "When you recognize the Quiet Exit beginning, write it out explicitly: <i>I have rendered the following verdict about this relationship or situation: ____. The evidence I am holding is: ____. The question I never honestly put to the other person is: ____.</i> The Vault's verdict derives much of its power from never being spoken. Written out in full, with the evidence and the unasked question, it often becomes clear that the verdict was formed in a court that lacked the most important witness."),
    ("Bring the wound, not the verdict",
     "When you must speak to the person or situation the Exit is leaving, bring one wound, not the file. One sentence: <i>When this happened, I felt exposed in a way I did not choose, and I have been carrying it without telling you.</i> Not the full file. Not the pattern, the precedent, the organized history. A relationship can sustain an honest wound expressed simply. It is far less certain it can sustain the discovery that years of wounds were filed in private and a verdict was rendered without the other party's knowledge."),
    ("The Elijah prayer",
     "When the verdict feels settled and you feel the Vault's characteristic composure that is not peace but resignation, pray the words Elijah prayed and then receive the answer God gave. Say: <i>Lord, I have said it is enough. I have filed the verdict. The account feels closed.</i> Then wait, in the practice of 1 Kings 19: not for an argument, not for a theological correction, but for the food and sleep and honest question that God sent to the prophet who had closed the account before God was finished. God's interruption of Elijah's verdict was not a rebuke. It was a commission. Ask what yours is."),
    ("Tell one person the door is closing",
     "The Quiet Exit lives on secrecy. It is a verdict rendered privately that becomes permanent because no one speaks into it before it seals. Before the folder closes, tell one trusted person \u2014 a pastor, a counselor, a friend who has earned the right to your interior \u2014 that you have been quietly withdrawing from something. Not to resolve it in that conversation. Simply to break the secrecy before the verdict is final. The Vault loses authority over its own conclusions the moment they are required to be spoken aloud to a witness."),
    ("The confession that fits",
     "When you recognize the Quiet Exit in yourself, the pastoral response is not self-condemnation. It is specific, honest confession: <i>I have rendered a verdict on a story that God has not yet finished writing. I have filed the account as closed in a court where I was the only judge. I hand the folder back to you, Lord. I am willing to find out what you intend to add to it.</i> Then, as God told Elijah: go out and stand before the Lord. Take the next small step. The Vault is not dismantled by grand gestures. It is loosened by the daily practice of not closing the accounts that God has left open."),
]

PRAYER_BODY = [
    "Father,",
    "You see the Vault in me, and you have been looking at it \u2014 at all of it, the full interior, every folder, every dated entry, every grief I processed alone before anyone else was invited to see the conclusion \u2014 since before I had the capacity to begin organizing it. You have not waited for my summary. You have not required my prepared presentation. You have been inside the walls all along, and your verdict about what you found there was not rendered by the court I was afraid of but by the one I most need: the court where Christ presented his own blood as the only exhibit, and the verdict came back covered, righteous, acceptable, in him, now and forever.",
    "But Father, the Vault is still filing. And somewhere in the filing, I have been doing something I called honest accounting and something that was, in part, closing accounts you had not yet closed. I have rendered verdicts in private courts where the evidence was real and the conclusions felt careful and the withdrawal felt like wisdom, and I have not given you the folder before sealing it. Forgive me for confusing finality with peace. Teach me to tell the difference. Teach me, when the shame trigger fires and the old question wakes up \u2014 <i>Am I acceptable?</i> \u2014 to hear your answer before I hear the Vault's. <i>There is therefore now no condemnation for those who are in Christ Jesus.</i> Let that land somewhere below the level of my theology, where the filing actually happens.",
    "Lord Jesus, I think of Elijah under the broom tree, saying: <i>It is enough.</i> You did not rebuke him. You sent him food, and rest, and an honest question in a cave: <i>What are you doing here?</i> Ask me that question in whatever relationship or situation I have been quietly exiting. I am willing to be asked. I am willing, slowly, to find out that the story had another chapter that my verdict had not accounted for.",
    "Holy Spirit, where I have been hiding the interior, give me the practice of offering it \u2014 first to God, then to the people who have earned the right to receive it. Where I have been quietly closing accounts, give me the courage to hold the folder open and wait. And where the Quiet Exit has already gone further than I have admitted even to myself \u2014 would you be the one who stands at the door before it seals and asks, gently and without accusation: <i>is this verdict yours to render?</i>",
    "In the name of the One who absorbed the exposure I have been managing, and who bore it to the grave and left it there, so that the interior I have been protecting might be permanently covered and freely shown \u2014 I pray.",
    "Amen.",
]

GOING_FURTHER_INTRO = [
    "This walkthrough is a beginning, not an ending. The Vault and the Quiet Exit have been with you long enough to have deep organizational roots, and one careful afternoon's reading will not fully re-open the closed folders. What follows is a short list of next steps \u2014 honest, concrete, and unhurried \u2014 for the work that has just begun.",
]

GOING_FURTHER_ITEMS = [
    ("Read this again in thirty days.",
     "Different sections will land differently. The Vault will prefer to receive information once, file it, and consider the matter processed. That preference is itself part of the pattern. Come back in a month. The section that felt least applicable today may be the most necessary one then. Particularly: Section Five on Elijah, and the two prompts that follow it."),
    ("Take one tool, not six.",
     "Choose the single practice from Section 7 that is most directly relevant to where you are right now \u2014 not the most comfortable one, the most necessary one. Try it for two weeks before adding another. The tools are postures, not a program. One posture, held long enough, begins to change the shape of the interior."),
    ("Name the folder that is closing.",
     "Tell one trusted person \u2014 a pastor, a spouse, a friend who has earned access to your interior \u2014 that there is a specific relationship or situation in which the Vault has been quietly rendering a verdict. Not to resolve it in that conversation. One sentence: <i>I have been filing something away that I have not told you about, and I am not sure it is mine to close.</i> The Vault loses a great deal of its authority over its own conclusions the moment they are required to be spoken aloud."),
    ("Pray Psalm 139 slowly, once a week, for a month.",
     "All of it. Not the parts that feel safe. Verse 23 especially: <i>Search me, O God, and know my heart. Try me and know my thoughts.</i> This is the Vault's hardest prayer because it is the explicit invitation of the God who already sees. Practice the invitation. The Vault needs to practice asking to be known before it can practice allowing it."),
    ("Read further on the shame the gospel answers.",
     "Tim Keller, <i>Walking with God through Pain and Suffering</i> \u2014 particularly his treatment of why suffering feels like exposure and how the gospel reframes it in the life of a person who does not easily let the reframe in. C. S. Lewis, <i>The Weight of Glory</i> \u2014 the title essay, slowly, on the longing to be known and approved by the highest authority, which will name the Vault's deepest longing with unusual precision. Dietrich Bonhoeffer, <i>Life Together</i> \u2014 the chapters on confession and community are the most direct pastoral address available to what the Vault most needs and most avoids."),
    ("If you are stuck, ask for help.",
     "There are seasons when the Vault and the Quiet Exit are too entrenched to be interrupted alone, and the Vault, by nature, will not ask for help without being asked to ask. A wise pastor, a Christian counselor, a trusted elder who knows you well \u2014 these are not signs of failure. For the Vault specifically, asking for help is one of the most specifically countercultural practices this walkthrough can recommend. The Vault was built to manage alone. Asking someone in is the beginning of its healing, and one of the most direct available tests of whether the God who has already seen everything inside is trusted to be present on the other side of the opening."),
]

GOING_FURTHER_CLOSING = (
    "You are not a problem to be solved. You are a soul being loved into freedom by a Father "
    "who has already seen everything in the file and has spoken the verdict before you could "
    "organize a single document in your defense. The Vault kept you alive. The Quiet Exit "
    "was the Vault's last act of self-protection in a story that God has not finished writing. "
    "Go gently with yourself. The One who began the good work in you will be the one to finish it, "
    "and he does not close accounts before he is done."
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
        [Paragraph("WAS I EXPOSED HERE?", header_style), Paragraph("what your nervous system concluded", sub_style)],
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
    """Generate the Vault + Quiet Exit (Verdict) walkthrough PDF.

    submission: the Take 139 Submission row. Used for personalization
    (name on cover, etc.) but the prose is constant for this profile.
    primary_mechanism='VAULT', primary_breakdown='VERD',
    primary_trigger='SHM', core_question='ACC'
    """
    ensure_fonts()
    S = make_styles()

    doc, buf = make_doc(
        brand_text="Take 139  \u00b7  A Counselor\u2019s Walkthrough",
        cover_top_label="TAKE 139  \u00b7  COUNSELOR\u2019S WALKTHROUGH",
        cover_right_label="VAULT  \u00b7  QUIET EXIT",
        title="Take 139 Walkthrough \u2014 Vault + Quiet Exit",
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
    story.append(Paragraph("The Vault &nbsp;\u00b7&nbsp; The Quiet Exit", S["CoverProfileVal"]))
    story.append(Paragraph(
        "Trigger: Shame &nbsp;\u00b7&nbsp; Core Question: Am I acceptable?",
        S["CoverProfileSub"]))
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph(
        "<i>\u201cIt is enough; now, O Lord, take away my life,<br/>"
        "for I am no better than my fathers.\u201d</i>",
        ParagraphStyle("cq", parent=S["CoverSub"], fontSize=11, leading=18, textColor=MUTED)))
    story.append(Paragraph(
        "1 Kings 19:4 \u2014 Elijah under the broom tree",
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
                   "The moment of unauthorized exposure, and what the Vault does with it.")
    for p in TRIGGER_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>Two questions, in writing.</b>", S["H3"]))
    story.append(Paragraph("Your head will organize the question. Your hand will not.", S["BodyJ"]))
    for prompt in TRIGGER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 3: Core Question \u2500\u2500
    section_header(story, S, "SECTION THREE  \u00b7  YOUR CORE QUESTION",
                   "Am I acceptable?",
                   "The wound the alarm has been guarding.")
    for p in QUESTION_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  CONTINUED",
                   "What Scripture says, and what receiving it costs you.",
                   "The God who already sees, and the verdict he has already spoken.")
    for p in QUESTION_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    for p in QUESTION_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION THREE  \u00b7  A PAUSE FOR HONESTY",
                   "Three columns, written by hand.",
                   "Where was I actually exposed? Where was my soul in danger?")
    story.append(Paragraph(
        "Use the table below. In the first column, name a recent event in which "
        "the shame trigger fired. In the second, write what your nervous system concluded: "
        "<i>was I exposed here?</i> In the third, answer the deeper question: "
        "<i>was the part of me that finally matters \u2014 my soul, my standing before "
        "God \u2014 at any point in danger?</i>",
        S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(_three_column_table())
    story.append(PageBreak())

    # \u2500\u2500 SECTION 4: Mechanism \u2500\u2500
    section_header(story, S, "SECTION FOUR  \u00b7  YOUR MECHANISM",
                   "The Vault.",
                   "The one who keeps the interior close, processes alone, and shows only what has been chosen.")
    for p in VAULT_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>How the Vault formed.</b>", S["H3"]))
    for p in VAULT_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>What the Vault costs you.</b>", S["H3"]))
    for p in VAULT_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FOUR  \u00b7  EXERCISE",
                   "A letter from the Vault.",
                   "Read his own words. He has been faithful; let him speak.")

    letter_style = ParagraphStyle(
        "VaultVerdLetter", fontName="Inter-Italic", fontSize=10.5, leading=16,
        textColor=INK, leftIndent=18, rightIndent=18, spaceAfter=8, spaceBefore=4)
    for line in VAULT_LETTER_INSTRUCTION:
        story.append(Paragraph(line, letter_style))
    story.append(Spacer(1, 10))
    divider(story)
    story.append(Spacer(1, 10))
    for prompt in VAULT_LETTER_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 5: Breakdown \u2500\u2500
    section_header(story, S, "SECTION FIVE  \u00b7  YOUR BREAKDOWN",
                   "The Quiet Exit.",
                   "The most legally final of all the Verdict breakdowns. Signed, sealed, filed.")
    for p in VERD_BODY_P1:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  CONTINUED",
                   "Elijah under the broom tree.",
                   "God did not honor the verdict. He sent food, sleep, and a question.")
    for p in VERD_BODY_P2:
        story.append(Paragraph(p, S["BodyJ"]))
    divider(story)
    story.append(Paragraph("<b>Finality confused with peace.</b>", S["H3"]))
    for p in VERD_BODY_P3:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(PageBreak())
    section_header(story, S, "SECTION FIVE  \u00b7  A PAUSE FOR HONESTY",
                   "Two questions before you turn the page.",
                   "Write the honest answer, not the one that sounds settled.")
    for prompt in VERD_PROMPTS:
        story.append(Paragraph(prompt, S["Prompt"]))
        journal_lines(story, n=3)
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # \u2500\u2500 SECTION 6: The Two Together \u2500\u2500
    section_header(story, S, "SECTION SIX  \u00b7  THE TWO TOGETHER",
                   "The same wound, in two modes.",
                   "The Vault and the Quiet Exit are not two problems. They are one loop.")
    for p in TWO_TOG_BODY:
        story.append(Paragraph(p, S["BodyJ"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>YOUR SEQUENCE</b>", S["H3"]))
    story.append(_callout(S, "YOUR SEQUENCE", TWO_TOG_TEMPLATE))
    story.append(Spacer(1, 8))
    journal_lines(story, n=4)
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
    for name, desc in VAULT_TOOLS:
        story.append(KeepTogether([
            Paragraph(name, tool_h),
            Paragraph(desc, tool_body),
        ]))
    story.append(PageBreak())
    section_header(story, S, "SECTION SEVEN  \u00b7  CONTINUED",
                   "When the Quiet Exit has begun.",
                   "Six practices for interrupting the departure before the folder closes.")
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


# \u2500\u2500 STANDALONE TEST \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
if __name__ == "__main__":
    import os

    class FakeSub:
        primary_mechanism = "VAULT"
        primary_breakdown = "VERD"
        primary_trigger = "SHM"
        core_question = "ACC"
        name = "Test User"

    pdf_bytes = build(FakeSub())
    out_path = os.path.join(os.path.dirname(__file__), "vault_verd_test.pdf")
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

    print(f"DONE: vault_verd.py")
    print(f"PDF size: {len(pdf_bytes):,} bytes ({size_kb} KB)")
    print(f"Page count: {page_count}")
    print(f"Letter snippet: {snippet!r}")
