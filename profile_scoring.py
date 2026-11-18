"""Server-side mirror of the frontend calculateScores()/getResults() logic.

Recomputes the four score sets (trigger, core question, mechanism, breakdown)
from a submission's stored raw answers, so every PDF, including those for
submissions made before the frontend sent these scores, can show all four
bar charts. scoring_spec.json is exported directly from the live
index.html question definitions (P1-P4 + free-text keyword patterns).
"""
import json
import math
import os
import re

_SPEC = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scoring_spec.json")))

TRIGGER_CATS = ["DIS", "DISC", "INJ", "CTRL", "SHM", "SIG"]
CQ_CATS = ["COMP", "LOV", "PROT", "FREE", "ACC", "REM"]
MECH_CATS = ["ARCH", "ISLE", "AMB", "VAULT", "ADPT", "CAMP"]
BD_CATS = ["COURT", "DISAP", "FLOOD", "GHOST", "VERD", "PLEA"]

_FT = {qid: (v["points"], [(c, re.compile(p, re.I)) for c, p in v["patterns"].items()])
       for qid, v in _SPEC["FREETEXT"].items()}


def _free_text(qid, text):
    text = (text or "").lower() if isinstance(text, str) else ""
    if not text or text == "__skipped__" or qid not in _FT:
        return {}
    pts, pats = _FT[qid]
    out = {}
    for cat, rx in pats:
        if rx.search(text):
            out[cat] = out.get(cat, 0) + pts
    if qid == "p2q2" and not out and len(text) > 10 and len(text) > 80:
        out["LOV"] = 1
    if qid == "p2q6" and re.search(r"\b(more.?than|beneath.?the.?surface|really.?am)\b", text, re.I):
        out["REM"] = out.get("REM", 0) + 1
    return out


def _score_phase(questions, cats, answers):
    totals = {c: 0.0 for c in cats}

    def add(points, w):
        for cat, p in (points or {}).items():
            if cat in totals:
                totals[cat] += p * w

    for q in questions:
        a = answers.get(q["id"])
        if a is None:
            continue
        w = q.get("weight") or 1.0
        sc = q.get("scoring")
        if q["type"] == "scale":
            try:
                idx = int(a) - 1
            except (TypeError, ValueError):
                continue
            if isinstance(sc, list) and 0 <= idx < len(sc):
                add(sc[idx], w)
            elif isinstance(sc, dict):
                add(sc.get(str(idx)), w)
        elif q["type"] == "mc":
            if isinstance(sc, dict):
                add(sc.get(str(a)), w)
            elif isinstance(sc, list):
                try:
                    add(sc[int(a)], w)
                except (TypeError, ValueError, IndexError):
                    pass
        elif q["type"] == "freetext":
            add(_free_text(q["id"], a), w)
    return totals


def _pct(totals, cats):
    total = sum(totals.values()) or 1
    return {c: int(math.floor(totals[c] / total * 100 + 0.5)) for c in cats}


def compute_profile_scores(answers):
    """Return {'trigger':{..}, 'core_question':{..}, 'mechanism':{..}, 'breakdown':{..}}
    as percentage-of-total dicts, or None if there are no usable answers."""
    if not isinstance(answers, dict) or not answers:
        return None
    phases = [("trigger", "P1", TRIGGER_CATS), ("core_question", "P2", CQ_CATS),
              ("mechanism", "P3", MECH_CATS), ("breakdown", "P4", BD_CATS)]
    out = {}
    for key, phase, cats in phases:
        totals = _score_phase(_SPEC[phase], cats, answers)
        if sum(totals.values()) <= 0:
            return None
        out[key] = _pct(totals, cats)
    return out
