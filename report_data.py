"""Content library for report generation — triggers, core questions, mechanisms, breakdowns.

This is the single source of truth for descriptions, markers, and gospel anchors.
Kept small and focused for phase 1 — expanded over time.
"""

TRIGGERS = {
    "DIS": {
        "name": "Disrespect-Sensitive",
        "short": "being dismissed, overlooked, or treated as though my perspective doesn't count",
        "long": "You feel pain most intensely when someone dismisses, overrides, or acts as if your perspective isn't worth considering. Disrespect lands harder for you than it does for most people — it touches something deeper than the moment.",
    },
    "DISC": {
        "name": "Disconnection-Sensitive",
        "short": "feeling emotionally distant or shut out from someone who matters to me",
        "long": "You feel pain most intensely when emotional warmth cools, when someone goes quiet or distant, when the thread of connection feels thin. Disconnection registers in your nervous system faster than almost anything else.",
    },
    "INJ": {
        "name": "Injustice-Sensitive",
        "short": "seeing something unfair happen and not being able to make it right",
        "long": "You feel pain most intensely when something feels unfair — when rules are bent, when someone gets away with harm, when the scales don't balance. Injustice activates something moral and protective in you.",
    },
    "CTRL": {
        "name": "Control-Sensitive",
        "short": "being pressured, managed, or forced into something not on my terms",
        "long": "You feel pain most intensely when your autonomy is threatened — when someone pushes, pressures, or tries to manage your choices. Being controlled triggers something fiercely protective in you.",
    },
    "SHAM": {
        "name": "Shame-Sensitive",
        "short": "being exposed, seen as inadequate, or having my flaws pointed out",
        "long": "You feel pain most intensely when you feel exposed — when flaws are named, when you're caught being less than you wanted to be, when there's no place to hide. Shame lands deeper and stays longer than for most people.",
    },
    "SIG": {
        "name": "Significance-Sensitive",
        "short": "feeling overlooked, unimportant, or like I don't really matter here",
        "long": "You feel pain most intensely when you feel unseen — when you're not chosen, not considered, not remembered. Feeling irrelevant or forgotten registers as real pain, not just a passing slight.",
    },
}

CORE_QUESTIONS = {
    "COMP": {
        "question": "Am I competent?",
        "long": "Underneath your daily experience is a question you've been asking since childhood: Am I good enough at this? Can I do it right? This question runs constantly in the background, and conflict often activates it.",
    },
    "LOVE": {
        "question": "Am I lovable?",
        "long": "Underneath your daily experience is a question you've been asking since childhood: Am I truly loved — for me, not for what I do? This question runs constantly in the background, and conflict often activates it.",
    },
    "SAFE": {
        "question": "Am I safe?",
        "long": "Underneath your daily experience is a question you've been asking since childhood: Is it actually okay here? Can I let my guard down? This question runs constantly in the background, and conflict often activates it.",
    },
    "FREE": {
        "question": "Am I free?",
        "long": "Underneath your daily experience is a question you've been asking since childhood: Do I have room to be who I am? Can I breathe here? This question runs constantly in the background, and conflict often activates it.",
    },
    "GOOD": {
        "question": "Am I good?",
        "long": "Underneath your daily experience is a question you've been asking since childhood: Am I fundamentally okay, or is something wrong with me? This question runs constantly in the background, and conflict often activates it.",
    },
    "SEEN": {
        "question": "Am I seen?",
        "long": "Underneath your daily experience is a question you've been asking since childhood: Does anyone actually notice me? Do I matter here? This question runs constantly in the background, and conflict often activates it.",
    },
}

MECHANISMS = {
    "ARCH": {
        "name": "Architect",
        "article": "an",
        "short": "I protect myself by organizing, planning, and staying in control of what happens around me",
        "long": "The Architect protects themselves through structure. You stay ahead of chaos by planning, organizing, and taking responsibility. You're the capable one — the person who handles things. Your shadow side is that you struggle to trust others to handle their own weight, and you can mistake control for care.",
    },
    "ISLE": {
        "name": "Island",
        "article": "an",
        "short": "I protect myself by handling things on my own and keeping my inner world self-contained",
        "long": "The Island protects themselves through self-sufficiency. You've learned that needing less is safer than needing more. You process alone, manage your own weather, and stay composed through almost anything. Your shadow side is that intimacy requires a kind of neediness you've worked hard to eliminate.",
    },
    "AMB": {
        "name": "Ambassador",
        "article": "an",
        "short": "I protect myself by making sure everyone around me is cared for and the peace is kept",
        "long": "The Ambassador protects themselves through care. You read the emotional room, smooth the edges, and keep people okay. You're often the glue in your relationships. Your shadow side is that you can lose yourself inside the serving, and resentment builds in the background before you realize it.",
    },
    "VAULT": {
        "name": "Vault",
        "article": "a",
        "short": "I protect myself by keeping the real stuff hidden and showing only what feels safe to show",
        "long": "The Vault protects themselves through selective disclosure. You know what's inside you — you just don't show most of it. You've learned that the people who've seen the real you haven't always handled it well. Your shadow side is that the people closest to you can feel locked out.",
    },
    "ADPT": {
        "name": "Adapter",
        "article": "an",
        "short": "I protect myself by reading the room and becoming what each situation seems to need from me",
        "long": "The Adapter protects themselves through attunement. You're skilled at sensing what a person or context wants and shaping yourself accordingly. You're the chameleon — and you're genuinely good at it. Your shadow side is that you can lose track of your own voice, your own preferences, your own self.",
    },
    "CAMP": {
        "name": "Campaign",
        "article": "a",
        "short": "I protect myself by achieving, building, and working toward something that proves I matter",
        "long": "The Campaign protects themselves through significance. You're driven — not by ego alone but by a deep conviction that your presence needs to mean something. You build, achieve, and leave a mark. Your shadow side is that rest and ordinariness feel unsafe, and you can have trouble just being instead of doing.",
    },
}

BREAKDOWNS = {
    "ATTY": {
        "name": "Attorney",
        "article": "an",
        "short": "I build a case and press for acknowledgment until the other person admits what happened",
        "long": "When the Attorney breaks down, they make a case. You gather evidence, cite past examples, and press until the other person acknowledges the truth. Your pain converts into argumentation. The breakdown isn't about being mean — it's about needing the record to reflect reality.",
    },
    "SHUT": {
        "name": "Shutdown",
        "article": "a",
        "short": "I go silent, unreachable, and pull all the way inside myself",
        "long": "When the Shutdown happens, you pull inward. Words stop, the door closes, and you become a kind of island inside the conversation. It's not punishment — it's protection. You've learned that when the pain spikes, silence is safer than saying the wrong thing.",
    },
    "FLOOD": {
        "name": "Flood",
        "article": "a",
        "short": "I hold things in until everything comes out at once — tears, grievances, intensity",
        "long": "When the Flood comes, everything you've been holding back arrives at once. Tears, stored grievances, the whole history. It's overwhelming for everyone — including you. But it's also honest. The breakdown is your nervous system finally releasing what polite conversation couldn't contain.",
    },
    "GHOST": {
        "name": "Ghost",
        "article": "a",
        "short": "I act like everything is fine while something is clearly wrong inside",
        "long": "When the Ghost pattern runs, you perform. \"I'm fine\" comes out of your mouth while something is breaking inside. You go through the motions, hoping the other person will notice without you having to say it. The breakdown is a kind of test: will they see what I'm not saying?",
    },
    "VERD": {
        "name": "Verdict",
        "article": "a",
        "short": "I quietly decide the relationship has failed me and begin pulling away",
        "long": "When the Verdict comes, you render judgment. Internally, silently, and often without the other person knowing. You begin pulling back emotionally, and the relationship starts dying by inches. The breakdown is less a rupture than a slow turning away — and it's usually been building for a long time.",
    },
    "PLEA": {
        "name": "Plea",
        "article": "a",
        "short": "I go into overdrive trying to restore the connection — apologizing, reassuring, fixing",
        "long": "When the Plea runs, you cannot tolerate the distance. You apologize, seek reassurance, over-correct, and work frantically to restore what feels broken. The breakdown is not weakness — it's an attachment system that believes disconnection is a crisis and responds with full emergency protocols.",
    },
}

# Gospel anchors mapped to core questions
GOSPEL_ANCHORS = {
    "COMP": {
        "title": "You are not your performance.",
        "truth": "In Christ, your identity is not held up by what you produce or how well you do. You are not a project to be completed. You are a child to be received. Your worth was settled before you did anything right — and it can't be shaken by anything you do wrong.",
        "scripture": "\"For it is by grace you have been saved, through faith — and this not from yourselves, it is the gift of God — not by works, so that no one can boast.\" — Ephesians 2:8-9",
        "expansion": "The question 'Am I competent?' will always feel live in your conflict. The gospel doesn't remove the question — it reframes it. You don't have to prove yourself in every conflict. You already have the only approval that ultimately matters."
    },
    "LOVE": {
        "title": "You are loved in your truest form.",
        "truth": "In Christ, you are loved not for the version of yourself you present, but for the one you actually are — the hidden parts, the parts you're ashamed of, the parts you don't even know yet. God's love is not conditional on your attractiveness. It is fixed on your person.",
        "scripture": "\"But God demonstrates his own love for us in this: While we were still sinners, Christ died for us.\" — Romans 5:8",
        "expansion": "The question 'Am I lovable?' will keep surfacing in conflict — especially when closeness feels threatened. The gospel answers it once and for all. You are loved in the most disqualifying version of yourself. That can hold you when love in this world feels uncertain."
    },
    "SAFE": {
        "title": "You are held by someone who does not fail.",
        "truth": "In Christ, you are kept by a Father who is fully attentive, fully competent, and fully for you. The world has not always been safe. People have not always been safe. But the one who holds your ultimate story has been entirely reliable, even when you couldn't see it.",
        "scripture": "\"The Lord himself goes before you and will be with you; he will never leave you nor forsake you. Do not be afraid; do not be discouraged.\" — Deuteronomy 31:8",
        "expansion": "The question 'Am I safe?' will always be loud in conflict. The gospel doesn't promise that people will always be safe. It promises that God is safe — and that your ultimate belonging is already secure, whatever the present conversation holds."
    },
    "FREE": {
        "title": "You are fully known and fully free.",
        "truth": "In Christ, you are not owned, manipulated, or consumed. The God who loves you is the same God who made you distinct — and he has no interest in erasing the self he designed. You are free to be fully seen and fully yourself at the same time.",
        "scripture": "\"It is for freedom that Christ has set us free. Stand firm, then, and do not let yourselves be burdened again by a yoke of slavery.\" — Galatians 5:1",
        "expansion": "The question 'Am I free?' will always tug at you in conflict. The gospel reframes the question: freedom in Christ is not freedom from intimacy, it is freedom inside intimacy. You can be close without being consumed."
    },
    "GOOD": {
        "title": "You are covered by a righteousness that is not your own.",
        "truth": "In Christ, your standing does not depend on whether you are good. It depends on whether he is — and he is. Your flaws have been named, carried, and answered. You don't have to hide. The worst of you has already been dealt with by the best of him.",
        "scripture": "\"God made him who had no sin to be sin for us, so that in him we might become the righteousness of God.\" — 2 Corinthians 5:21",
        "expansion": "The question 'Am I good?' will surface in every conflict, especially when you feel exposed. The gospel answers it with a surprising generosity: you are covered. You can be honest about what's in you, because the verdict has already been rendered in your favor."
    },
    "SEEN": {
        "title": "You are fully known by the one who knows everything.",
        "truth": "In Christ, you are not invisible. You are not overlooked. The God who made the stars also counts your tears and tracks your name. Even if every human in your life has failed to see you, one has not, and never will.",
        "scripture": "\"Search me, God, and know my heart; test me and know my anxious thoughts.\" — Psalm 139:23",
        "expansion": "The question 'Am I seen?' will always be present in conflict. The gospel doesn't promise that every person will notice you. It promises that God has already seen you, down to the roots — and he calls what he sees beloved."
    },
}

# Simplified behavioral markers — phase 1 placeholder; will be expanded from personalization-content.md
# These are sample markers; the full library is large and will be loaded from JSON in later phases

MECHANISM_MARKERS = {
    "ARCH": [
        "You're often the one organizing plans, making reservations, or building the agenda.",
        "You feel anxious when things are unplanned or when someone else is 'running point.'",
        "You offer solutions quickly — sometimes before the other person has finished sharing.",
        "You've been called controlling or intense, and it stung because you didn't mean it that way.",
        "You can struggle to ask for help, even when you clearly need it.",
        "Mistakes — especially your own — bother you far more than they should.",
    ],
    "ISLE": [
        "You find you need significantly more alone time than the people around you seem to need.",
        "When stressed, your instinct is to withdraw rather than reach out.",
        "You genuinely believe needing less from others is the more adult path.",
        "Emotional conversations can feel slightly exhausting, even when they're with people you love.",
        "People tell you you're 'unreadable' or 'hard to figure out' — and you don't quite know why.",
        "You've been self-sufficient for so long you're not entirely sure what needing someone would look like.",
    ],
    "AMB": [
        "You often know what others are feeling before they say it out loud.",
        "Your 'yes' comes out automatically, even when your 'no' would be more honest.",
        "You keep mental lists of what people need and you try to deliver.",
        "You can be surprised by how much resentment has built without you noticing.",
        "You sometimes wonder if people like the real you or just the helpful version.",
        "The thought of someone being upset with you can occupy your mind for days.",
    ],
    "VAULT": [
        "People describe you as charming or fun, but few would say they really know you.",
        "You share strong opinions freely and tender things rarely.",
        "You can go days without anyone knowing something significant is happening inside you.",
        "Humor is often the thing you reach for when the conversation gets too close.",
        "You've shown the real you before and regretted it — and you haven't forgotten.",
        "Your closest people sometimes wish they knew what you were actually thinking.",
    ],
    "ADPT": [
        "You find you're a slightly different person with different groups — and this is automatic, not manipulative.",
        "You can have a hard time answering 'what do you want?' because you're used to orienting around others.",
        "Other people's moods shift your mood fast.",
        "You're a remarkable listener, but struggle to let others do the same for you.",
        "You can look back at seasons of your life and barely recognize the version of yourself you were.",
        "Being alone can feel disorienting — without another person to reflect, you lose the signal.",
    ],
    "CAMP": [
        "Idle time makes you uncomfortable in a way you've stopped trying to explain.",
        "You're building or dreaming of building most of the time — a brand, a mission, a legacy.",
        "Rest feels earned, never automatic.",
        "You find it hard to celebrate what you've done before moving to the next thing.",
        "You can struggle to be 'just' a spouse, a friend, a regular person — there's always more to accomplish.",
        "You've wondered if you'd still matter if you stopped producing.",
    ],
}

BREAKDOWN_MARKERS = {
    "ATTY": [
        "When hurt, you instinctively start gathering evidence — dates, words, past patterns.",
        "You need the record to reflect what actually happened, and you won't let it go until it does.",
        "You can win arguments but feel worse afterward — you wanted acknowledgment, not victory.",
        "You've been told you're exhausting to fight with, and some part of you knows they're right.",
        "You replay conversations hours or days after they're over, refining your case.",
    ],
    "SHUT": [
        "When overwhelmed, your words just stop — not chosen, not strategic, just gone.",
        "You become physically unreachable, sometimes for hours.",
        "Your partner has learned that pressing in when you shut down usually makes it worse.",
        "You come back eventually, but the re-entry is often awkward.",
        "Shutting down feels involuntary — you didn't choose it, your system did.",
    ],
    "FLOOD": [
        "Things build quietly until they don't — then it's tears, grievances, and the whole backlog.",
        "You've brought up things from years ago in the middle of an argument about something else.",
        "Afterward you often feel relief even though the person you love looks shaken.",
        "People close to you have told you that the flood is hard to be on the receiving end of.",
        "You sometimes feel ashamed of the flood but also can't imagine containing it forever.",
    ],
    "GHOST": [
        "\"I'm fine\" comes out of your mouth when you are clearly not fine.",
        "You wait for the other person to notice — and it tells you something when they don't.",
        "You go through the motions of normal life while something is breaking inside.",
        "You can hold this pattern for days, sometimes weeks.",
        "Part of you wants them to see; another part of you doesn't want to have to say it.",
    ],
    "VERD": [
        "You can feel a kind of door quietly closing inside you during conflict.",
        "The withdrawal doesn't look dramatic — it's a slow, quiet pulling back.",
        "By the time you say anything, the verdict has usually already been rendered.",
        "You can go through the motions in a relationship for a long time after you've internally decided.",
        "You've walked away from things other people thought were fine, and they never quite understood why.",
    ],
    "PLEA": [
        "You cannot tolerate unresolved distance — it registers as an emergency.",
        "You'll apologize for things you're not sure you did wrong just to close the gap.",
        "You've sent long texts at 1am trying to make sure things are okay.",
        "\"Are we okay?\" is a phrase you've said more times than you can count.",
        "You've been told you're too much in conflict — and it's landed because part of you knows.",
    ],
}

CORE_QUESTION_MARKERS = {
    "COMP": [
        "Feedback — even well-meant feedback — can ruin your day.",
        "You've defined yourself by what you do for a long time.",
        "You feel a sharp internal 'failure' when you fall short of your own standards.",
        "You find it hard to receive a compliment without deflecting or qualifying.",
        "You work harder when you're anxious — even when rest is what's actually needed.",
    ],
    "LOVE": [
        "You're attuned to small shifts in how people treat you, sometimes hyper-attuned.",
        "When someone is distant, you often assume it's something you did.",
        "You've asked 'are we okay?' more times than you wish you had.",
        "Feeling unloved can register in your body before your mind even catches up.",
        "You sometimes earn love in ways you know are unhealthy — and you still do it.",
    ],
    "SAFE": [
        "You scan rooms, read faces, and pick up on tension before most people do.",
        "You have a heightened startle response, especially to raised voices.",
        "You prefer predictability to novelty in ways other people don't fully understand.",
        "You've been 'okay' in situations that, looking back, were not okay at all.",
        "Safe relationships can feel strange at first — you have to learn to trust them.",
    ],
    "FREE": [
        "Pressure — even gentle pressure — can make you want to bolt.",
        "You have a strong internal sense of what belongs to you and what doesn't.",
        "You've struggled with commitment more than you wish you had.",
        "You pull away when things feel too intense, even when you want closeness.",
        "You can mistake being let alone for being loved.",
    ],
    "GOOD": [
        "Shame lands harder and stays longer for you than it does for most people.",
        "You often feel an undercurrent of 'something is wrong with me' you can't quite name.",
        "You find it hard to believe people genuinely like you without a performance reason.",
        "Exposure — being seen in an unflattering light — is one of your deepest fears.",
        "You've worked hard to be the kind of person no one could criticize, and it's exhausting.",
    ],
    "SEEN": [
        "Being overlooked in a group can wound you more than it 'should.'",
        "You've kept quiet about significant things and watched to see if anyone would ask.",
        "You sometimes feel invisible in rooms full of people.",
        "Recognition matters to you more than you usually let on.",
        "You've wondered, more than once, if you actually left a mark.",
    ],
}

# Reflection questions tailored by mechanism
MECHANISM_REFLECTIONS = {
    "ARCH": [
        "Where does your instinct to control come from — a specific season, a specific person, or something more diffuse?",
        "What does it cost your partner when you take responsibility for things that aren't actually yours to hold?",
        "When was the last time you let someone else lead and trusted the outcome, even imperfectly?",
        "What would it look like to let your partner see the anxious version of you, not just the capable one?",
        "Where in your faith have you confused sovereignty with control — trying to do God's job rather than yours?",
    ],
    "ISLE": [
        "Name one person in your life who has earned the right to see beyond your self-sufficiency. What would it look like to let them?",
        "What did needing feel like in your childhood home? What did you learn to do with that need?",
        "Where might your partner be receiving your independence as a message of rejection you don't mean to send?",
        "What is the difference, for you, between solitude and isolation?",
        "What would it look like to bring a specific unmet need to God before trying to manage it yourself?",
    ],
    "AMB": [
        "Whose needs did you grow up managing? How old were you when that pattern formed?",
        "Where is resentment quietly building in you that you haven't named out loud?",
        "What would change if your partner felt the full weight of their own emotional responsibilities instead of you absorbing them?",
        "Can you name a time you said yes when your real answer was no? What was the cost?",
        "Where in your faith has caring for others become a substitute for being cared for by God?",
    ],
    "VAULT": [
        "Who has had access to the real you, and what did they do with it? What did that teach you?",
        "What are you most afraid your partner will discover about you?",
        "What is the difference between privacy and hiding, and which are you actually practicing?",
        "When was the last time you let someone in on something before you had it figured out?",
        "Where has your ability to keep things hidden shaped your relationship with God?",
    ],
    "ADPT": [
        "What are your actual preferences — your favorite meal, your ideal Saturday, your unfiltered opinion on a hard topic?",
        "When were you last alone in a way that felt restorative rather than disorienting?",
        "Where in your relationship are you performing an identity rather than bringing one?",
        "What would it cost you to disappoint your partner — and what might it gain you?",
        "How might God be inviting you to a more settled sense of self, rooted in him rather than in your audience?",
    ],
    "CAMP": [
        "What would happen, in your inner world, if you accomplished nothing for six months?",
        "Where has your drive been confused for calling — where did you pick up the idea that you have to earn your existence?",
        "What does your partner see that you struggle to see — the parts of you that aren't about output?",
        "When was the last time you rested without guilt or plans?",
        "How is the gospel offering you a significance that doesn't need to be built?",
    ],
}

# Prayers by mechanism
MECHANISM_PRAYERS = {
    "ARCH": "Father, I confess that I have used control as a substitute for trust. Where I've tried to hold what was never mine to hold, teach me to set it down. Where I have confused my competence for faith, grow me into someone who trusts you more than my own plans. Let my partner see the version of me that doesn't need to run the show to be loved. In the name of the One who holds all things together, Amen.",
    "ISLE": "Father, I confess that I have used self-sufficiency as a kind of armor. Where I've decided that needing less is the safer path, soften me. Help me accept that you designed me to be known — fully, patiently, imperfectly — and that isolation is not strength. Give my partner the gift of seeing me. And give me the grace of being seen. Amen.",
    "AMB": "Father, I confess that I have confused serving with being loved. Where I have absorbed weights that were never mine to carry, lift them from me. Teach me the difference between genuine care and anxious caretaking. Give me the courage to say no, the honesty to name what I need, and the humility to be on the receiving end of love. Amen.",
    "VAULT": "Father, I confess that I have chosen hiddenness over honesty. Where I have believed that exposure would end me, remind me that you have already seen everything and loved me still. Give me one step — one disclosure, one unveiling — that trusts the grace I'm standing on. And give my partner eyes to see me gently. Amen.",
    "ADPT": "Father, I confess that I have shaped myself around others and lost the shape you gave me. Where I have become a mirror, grow in me a self. Remind me that you did not make me to be a reflection of my audience but a reflection of you. Let my partner know the real me, not the useful me. And let me know the real me, too. Amen.",
    "CAMP": "Father, I confess that I have tried to earn a significance you have already given. Where striving has replaced worship, slow me down. Teach me to rest without guilt, to be without producing, and to find my name in your voice instead of in my accomplishments. Let my partner enjoy me, not my output. Amen.",
}


def get_report_data(primary_trigger: str, core_question: str, mechanism: str,
                    breakdown: str, trigger_scores: dict, home_desc: str,
                    name: str, pair_code: str) -> dict:
    """Build the complete template data dict for report generation."""
    from datetime import datetime

    trigger = TRIGGERS.get(primary_trigger, TRIGGERS["DIS"])
    cq = CORE_QUESTIONS.get(core_question, CORE_QUESTIONS["COMP"])
    mech = MECHANISMS.get(mechanism, MECHANISMS["ARCH"])
    brk = BREAKDOWNS.get(breakdown, BREAKDOWNS["ATTY"])
    gospel = GOSPEL_ANCHORS.get(core_question, GOSPEL_ANCHORS["COMP"])

    # Sorted trigger scores for display (top down)
    trigger_display = []
    trigger_key_to_name = {
        "DIS": "Disrespect",
        "DISC": "Disconnection",
        "INJ": "Injustice",
        "CTRL": "Control",
        "SHAM": "Shame",
        "SIG": "Significance",
    }
    sorted_triggers = sorted(trigger_scores.items(), key=lambda x: -x[1])
    for key, score in sorted_triggers:
        trigger_display.append({
            "name": trigger_key_to_name.get(key, key),
            "score": int(score),
        })

    return {
        "name": name or "Friend",
        "pair_code": pair_code,
        "date": datetime.utcnow().strftime("%B %d, %Y"),
        "year": datetime.utcnow().year,
        "home_desc": home_desc or "your childhood home",

        "primary_trigger_name": trigger["name"],
        "primary_trigger_short": trigger["short"],
        "primary_trigger_long": trigger["long"],

        "core_question": cq["question"],
        "core_question_long": cq["long"],
        "core_question_markers": CORE_QUESTION_MARKERS.get(core_question, CORE_QUESTION_MARKERS["COMP"]),

        "mechanism_name": mech["name"],
        "mechanism_article": mech["article"],
        "mechanism_short": mech["short"],
        "mechanism_long": mech["long"],
        "mechanism_markers": MECHANISM_MARKERS.get(mechanism, MECHANISM_MARKERS["ARCH"]),

        "breakdown_name": brk["name"],
        "breakdown_article": brk["article"],
        "breakdown_short": brk["short"],
        "breakdown_long": brk["long"],
        "breakdown_markers": BREAKDOWN_MARKERS.get(breakdown, BREAKDOWN_MARKERS["ATTY"]),

        "gospel_title": gospel["title"],
        "gospel_truth": gospel["truth"],
        "gospel_scripture": gospel["scripture"],
        "gospel_expansion": gospel["expansion"],

        "trigger_scores": trigger_display,
        "reflection_questions": MECHANISM_REFLECTIONS.get(mechanism, MECHANISM_REFLECTIONS["ARCH"]),
        "prayer": MECHANISM_PRAYERS.get(mechanism, MECHANISM_PRAYERS["ARCH"]),

        "greeting": f"Dear {name}" if name else "Hello",
    }
