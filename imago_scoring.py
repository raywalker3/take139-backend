"""IMAGO scoring engine.

Pipeline:
    raw item responses (1-5)
        → reverse-coded responses
        → aspect scores (mean of 10 items per aspect)
        → domain scores (mean of 2 aspect scores)
        → metatrait scores (Stability, Plasticity)
        → percentiles (vs. normative sample)
        → letter type (5-letter IMAGO type)
        → archetype (closest of 10)

Architecture references:
- DeYoung, Quilty & Peterson (2007) — 10-aspect BFAS
- DeYoung, Peterson & Higgins (2006) — metatraits Stability + Plasticity
- IMAGO Design Doc v1.0
- IMAGO Names Locked

The 100 production items come from imago_items.py (loaded on startup).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


# ─────────────────────────────────────────────────────────────────────
# CONSTANTS — domain/aspect architecture
# ─────────────────────────────────────────────────────────────────────

DOMAINS = [
    ("I", "Imagination"),
    ("M", "Mastery"),
    ("A", "Animation"),
    ("G", "Grace-bearing"),
    ("O", "Ortho-emotion"),
]

# Each aspect → (code, name, parent domain code)
ASPECTS = [
    ("I1", "Artistry",        "I"),
    ("I2", "Intellect",       "I"),
    ("M1", "Industriousness", "M"),
    ("M2", "Orderliness",     "M"),
    ("A1", "Enthusiasm",      "A"),
    ("A2", "Assertiveness",   "A"),
    ("G1", "Compassion",      "G"),
    ("G2", "Courtesy",        "G"),
    ("O1", "Sensitivity",     "O"),  # forward = withdrawal-prone (low Ortho-emotion)
    ("O2", "Steadiness",      "O"),  # forward = volatility-prone (low Ortho-emotion)
]

# CRITICAL: Ortho-emotion aspects are written with FORWARD items measuring the
# low-Ortho-emotion direction (i.e., "I get overwhelmed easily" measures
# Withdrawal/Volatility, which is the OPPOSITE of Ortho-emotion).
# So the aspect score must be REVERSED (6 - score) to map to Ortho-emotion's
# "high = steady" semantic. We do this at the aspect-aggregation step.
ORTHO_INVERTED_ASPECTS = {"O1", "O2"}

# Metatrait composition
#
# v3 change (May 2026): Reworked from DeYoung 2006's loose Big-5 average to
# a more pastorally-honest composition. The old formula averaged O, G, and M
# equally for Stability, which produced false positives for people who had
# very high O (genuinely steady) but very low G (prophetically direct) — they
# were being mislabeled as "low Stability / The Psalmist" when their
# emotional life is in fact rock-solid.
#
# New approach:
#   STEADINESS  (formerly Stability) = primarily Ortho-emotion. The literal
#                                       emotional steadiness of the person.
#                                       G is a small modifier (warmth helps
#                                       steadiness; sharpness doesn't kill it).
#                                       M is independent (a steady person
#                                       may or may not be disciplined).
#
#   REACH       (formerly Plasticity) = both Imagination and Animation must be
#                                       elevated to qualify as high Reach.
#                                       This honors DeYoung 2014's caution
#                                       that Plasticity is a joint construct.
METATRAIT_LOADINGS = {
    "Steadiness": {"O": 1.0, "G": 0.25},  # O dominates; G is a small modifier
    "Reach":      {"I": 1.0, "A": 1.0},   # requires BOTH (see _compute_metatrait_scores)
}

# User-facing display names for the two metatraits.
# The internal computation still uses these keys; PROVISIONAL_METATRAIT_NORMS
# below is keyed by the same names.
METATRAIT_DISPLAY_NAMES = {
    "Steadiness": "Steadiness",
    "Reach":      "Reach",
}

# Letter type threshold (60th percentile; per Design Doc §3.4)
LETTER_TYPE_PERCENTILE_CUTOFF = 60
BORDERLINE_BAND = (55, 65)  # display as i/I if percentile in this range


# ─────────────────────────────────────────────────────────────────────
# NORMS — placeholder until calibration sample exists
# ─────────────────────────────────────────────────────────────────────
# Until N>=400 calibration data is gathered, we use theoretical norms based on
# 5-point Likert items: assume aspect mean = 3.0, SD ≈ 0.7 (typical for BFAS).
# Domain norms are similar. Metatrait norms scale appropriately.
#
# Once we have real calibration data, replace this dict with empirical means/SDs
# from the calibration sample. The percentile function uses normal-approximation
# until then.

PROVISIONAL_ASPECT_NORMS = {
    "I1": (3.40, 0.75),  # Artistry — moderately positive baseline
    "I2": (3.30, 0.75),
    "M1": (3.55, 0.65),
    "M2": (3.40, 0.75),
    "A1": (3.30, 0.80),
    "A2": (3.20, 0.80),
    "G1": (3.85, 0.65),  # Compassion — elevated; people self-report kindness high
    "G2": (3.65, 0.70),
    "O1": (3.20, 0.85),  # Sensitivity (FORWARD = withdrawal-prone)
    "O2": (2.90, 0.80),  # Steadiness (FORWARD = volatility-prone)
}

PROVISIONAL_DOMAIN_NORMS = {
    "I": (3.35, 0.65),
    "M": (3.48, 0.60),
    "A": (3.25, 0.70),
    "G": (3.75, 0.60),
    "O": (3.10, 0.70),  # post-inversion mean; reflects BFAS Withdrawal/Volatility means around 3.0
}

PROVISIONAL_METATRAIT_NORMS = {
    "Steadiness": (3.30, 0.55),  # weighted O + 0.25·G
    "Reach":      (3.30, 0.65),  # joint I + A
}


def percentile_from_score(score: float, mean: float, sd: float) -> float:
    """Convert a raw mean score to a percentile using normal-approximation.

    Until we have calibration data, this is the best honest estimate.
    Returns a number 0-100, clamped.
    """
    from math import erf, sqrt
    if sd <= 0:
        return 50.0
    z = (score - mean) / sd
    # Cumulative distribution of standard normal
    cdf = 0.5 * (1 + erf(z / sqrt(2)))
    pct = max(0.0, min(100.0, cdf * 100.0))
    return round(pct, 1)


# ─────────────────────────────────────────────────────────────────────
# DATA CLASSES — the score result returned by score_imago()
# ─────────────────────────────────────────────────────────────────────

@dataclass
class AspectScore:
    code: str               # "I1"
    name: str               # "Artistry"
    domain_code: str        # "I"
    raw_mean: float         # 1.0–5.0
    percentile: float       # 0–100
    n_items_answered: int   # how many items contributed (must be 10 for production)


@dataclass
class DomainScore:
    code: str               # "I"
    name: str               # "Imagination"
    raw_mean: float         # 1.0–5.0
    percentile: float       # 0–100
    pole: str               # "high" | "low" | "borderline"
    aspects: List[AspectScore] = field(default_factory=list)


@dataclass
class MetatraitScore:
    name: str               # "Stability" | "Plasticity"
    raw_mean: float
    percentile: float
    pole: str               # "high" | "low" | "borderline"


@dataclass
class ImagoResult:
    """Complete IMAGO scoring result."""
    domains: List[DomainScore]
    metatraits: List[MetatraitScore]
    letter_type: str        # "iMago", "IMAGO", "imago", etc.
    letter_type_borderline: List[str]  # which letters are borderline (e.g., ["I"])
    soul_shape: str         # "Host" | "Anchor" | "Psalmist" | "Watchman"
    archetype: str          # "Shepherd" | "Mason" | etc.
    archetype_match_score: float  # numeric closeness to chosen archetype

    def to_dict(self) -> dict:
        return {
            "domains": [
                {
                    "code": d.code,
                    "name": d.name,
                    "raw_mean": d.raw_mean,
                    "percentile": d.percentile,
                    "pole": d.pole,
                    "aspects": [
                        {
                            "code": a.code,
                            "name": a.name,
                            "raw_mean": a.raw_mean,
                            "percentile": a.percentile,
                            "n_items_answered": a.n_items_answered,
                        }
                        for a in d.aspects
                    ],
                }
                for d in self.domains
            ],
            "metatraits": [
                {
                    "name": m.name,
                    "raw_mean": m.raw_mean,
                    "percentile": m.percentile,
                    "pole": m.pole,
                }
                for m in self.metatraits
            ],
            "letter_type": self.letter_type,
            "letter_type_borderline": self.letter_type_borderline,
            "soul_shape": self.soul_shape,
            "archetype": self.archetype,
            "archetype_match_score": round(self.archetype_match_score, 3),
        }


# ─────────────────────────────────────────────────────────────────────
# CORE SCORING PIPELINE
# ─────────────────────────────────────────────────────────────────────

def score_imago(answers: Dict[str, int], items: List[dict]) -> ImagoResult:
    """Score a complete IMAGO submission.

    Args:
        answers: dict mapping item_id (e.g., "IMAGO-001") to Likert response (1-5)
        items: list of item dicts with keys: item_id, aspect_code, direction
               (FORWARD/REVERSE), domain — typically loaded from imago_items.py

    Returns:
        ImagoResult with domains, metatraits, letter type, soul shape, archetype.
    """
    # 1. Compute aspect scores (mean of 10 items per aspect, reverse-coded as needed)
    aspect_scores = _compute_aspect_scores(answers, items)

    # 2. Compute domain scores (mean of 2 aspect scores per domain)
    domain_scores = _compute_domain_scores(aspect_scores)

    # 3. Compute metatrait scores
    metatrait_scores = _compute_metatrait_scores(domain_scores)

    # 4. Derive letter type (5-letter IMAGO from domain percentiles)
    letter_type, borderline = _derive_letter_type(domain_scores)

    # 5. Derive Soul Shape (one of four, from metatraits)
    soul_shape = _derive_soul_shape(metatrait_scores)

    # 6. Derive Archetype (closest of 10, from full domain profile)
    archetype, match_score = _derive_archetype(domain_scores)

    return ImagoResult(
        domains=domain_scores,
        metatraits=metatrait_scores,
        letter_type=letter_type,
        letter_type_borderline=borderline,
        soul_shape=soul_shape,
        archetype=archetype,
        archetype_match_score=match_score,
    )


# ─────────────────────────────────────────────────────────────────────
# Step 1 — aspect scores
# ─────────────────────────────────────────────────────────────────────

def _compute_aspect_scores(answers: Dict[str, int], items: List[dict]) -> List[AspectScore]:
    """For each of the 10 aspects, compute the mean of its 10 items.

    Reverse-keyed items: response 'r' becomes (6 - r) before averaging.
    Ortho-emotion aspects (O1, O2): the COMPUTED mean is then inverted
    (6 - mean) so that a high score on the aspect means high Ortho-emotion
    (steady), per the design doc.
    """
    # Group items by aspect_code
    by_aspect: Dict[str, List[dict]] = {}
    for item in items:
        by_aspect.setdefault(item["aspect_code"], []).append(item)

    out: List[AspectScore] = []
    for aspect_code, aspect_name, domain_code in ASPECTS:
        aspect_items = by_aspect.get(aspect_code, [])
        if not aspect_items:
            # No items for this aspect → score at midpoint
            out.append(AspectScore(
                code=aspect_code, name=aspect_name, domain_code=domain_code,
                raw_mean=3.0, percentile=50.0, n_items_answered=0,
            ))
            continue

        # Apply reverse coding and average
        responses = []
        for item in aspect_items:
            raw = answers.get(item["item_id"])
            if raw is None:
                continue
            # Clamp to 1-5
            r = max(1, min(5, int(raw)))
            if item.get("direction") == "REVERSE":
                r = 6 - r
            responses.append(r)

        if not responses:
            mean = 3.0
            n = 0
        else:
            mean = sum(responses) / len(responses)
            n = len(responses)

        # Invert Ortho-emotion aspects so high = steady
        if aspect_code in ORTHO_INVERTED_ASPECTS:
            mean = 6 - mean

        # Percentile against provisional norms
        norm_mean, norm_sd = PROVISIONAL_ASPECT_NORMS[aspect_code]
        # For Ortho aspects, the provisional norms are calibrated for the
        # forward (withdrawal-prone) direction; after inversion we need the
        # COMPLEMENTARY norm. Easiest fix: also invert the comparison.
        if aspect_code in ORTHO_INVERTED_ASPECTS:
            # Inverted norm: mean becomes 6 - norm_mean
            cmp_mean = 6 - norm_mean
            pct = percentile_from_score(mean, cmp_mean, norm_sd)
        else:
            pct = percentile_from_score(mean, norm_mean, norm_sd)

        out.append(AspectScore(
            code=aspect_code, name=aspect_name, domain_code=domain_code,
            raw_mean=round(mean, 3), percentile=pct, n_items_answered=n,
        ))

    return out


# ─────────────────────────────────────────────────────────────────────
# Step 2 — domain scores
# ─────────────────────────────────────────────────────────────────────

def _compute_domain_scores(aspect_scores: List[AspectScore]) -> List[DomainScore]:
    """Each domain = mean of its 2 aspect raw_means."""
    by_domain: Dict[str, List[AspectScore]] = {}
    for a in aspect_scores:
        by_domain.setdefault(a.domain_code, []).append(a)

    out: List[DomainScore] = []
    for code, name in DOMAINS:
        aspects = by_domain.get(code, [])
        if not aspects:
            mean = 3.0
        else:
            mean = sum(a.raw_mean for a in aspects) / len(aspects)

        norm_mean, norm_sd = PROVISIONAL_DOMAIN_NORMS[code]
        pct = percentile_from_score(mean, norm_mean, norm_sd)

        # Pole assignment
        if BORDERLINE_BAND[0] <= pct <= BORDERLINE_BAND[1]:
            pole = "borderline"
        elif pct >= LETTER_TYPE_PERCENTILE_CUTOFF:
            pole = "high"
        else:
            pole = "low"

        out.append(DomainScore(
            code=code, name=name, raw_mean=round(mean, 3),
            percentile=pct, pole=pole, aspects=aspects,
        ))
    return out


# ─────────────────────────────────────────────────────────────────────
# Step 3 — metatrait scores
# ─────────────────────────────────────────────────────────────────────

def _compute_metatrait_scores(domain_scores: List[DomainScore]) -> List[MetatraitScore]:
    """Compute Steadiness and Reach from domain scores.

    v3 logic:
      - Steadiness = weighted blend of O (1.0) + G (0.25). The Ortho-emotion
        domain dominates. G is a small modifier so that a person with high O
        but low G is still classified as steady (their emotional life is in
        fact stable; their directness is a separate trait, not turbulence).
      - Reach = JOINT measure of I + A. Both must be elevated. We take the
        MINIMUM of the two domain raw means (so the lower of the two anchors
        the metatrait) rather than the average. This honors DeYoung 2014's
        warning that Plasticity is not the same as 'high on either'.
    """
    by_domain = {d.code: d for d in domain_scores}
    out: List[MetatraitScore] = []
    for meta_name, loadings in METATRAIT_LOADINGS.items():
        if meta_name == "Reach":
            # Joint construct: take the MIN of I and A so both must elevate
            domain_means = []
            for d_code in loadings.keys():
                d = by_domain.get(d_code)
                if d is not None:
                    domain_means.append(d.raw_mean)
            mean = min(domain_means) if domain_means else 3.0
        else:
            # Steadiness: weighted average (O dominates, G modifies)
            weighted_sum = 0.0
            weight_total = 0.0
            for d_code, weight in loadings.items():
                d = by_domain.get(d_code)
                if d is None:
                    continue
                weighted_sum += d.raw_mean * weight
                weight_total += weight
            mean = weighted_sum / weight_total if weight_total > 0 else 3.0

        norm_mean, norm_sd = PROVISIONAL_METATRAIT_NORMS[meta_name]
        pct = percentile_from_score(mean, norm_mean, norm_sd)
        if BORDERLINE_BAND[0] <= pct <= BORDERLINE_BAND[1]:
            pole = "borderline"
        elif pct >= LETTER_TYPE_PERCENTILE_CUTOFF:
            pole = "high"
        else:
            pole = "low"
        out.append(MetatraitScore(
            name=meta_name, raw_mean=round(mean, 3),
            percentile=pct, pole=pole,
        ))
    return out


# ─────────────────────────────────────────────────────────────────────
# Step 4 — letter type
# ─────────────────────────────────────────────────────────────────────

def _derive_letter_type(domain_scores: List[DomainScore]) -> Tuple[str, List[str]]:
    """Build the 5-letter IMAGO type from domain percentiles.

    Order: I, M, A, G, O.
    Uppercase if pct ≥ 60. Lowercase if pct < 60.
    Borderline (55–65) flagged separately for display purposes.

    Returns:
        (letter_type, list of borderline letters)
    """
    by_domain = {d.code: d for d in domain_scores}
    letters = []
    borderline = []
    for code, name in DOMAINS:
        d = by_domain.get(code)
        if d is None:
            letters.append(code.lower())
            continue
        if d.percentile >= LETTER_TYPE_PERCENTILE_CUTOFF:
            letters.append(code.upper())
        else:
            letters.append(code.lower())
        if d.pole == "borderline":
            borderline.append(code)
    return "".join(letters), borderline


# ─────────────────────────────────────────────────────────────────────
# Step 5 — Soul Shape
# ─────────────────────────────────────────────────────────────────────

SOUL_SHAPES = {
    # (Steadiness_pole, Reach_pole) -> Soul Shape
    ("high", "high"): "Host",
    ("high", "low"):  "Anchor",
    ("low",  "high"): "Psalmist",
    ("low",  "low"):  "Watchman",
}


def _derive_soul_shape(metatraits: List[MetatraitScore]) -> str:
    """Pick the Soul Shape from the Steadiness × Reach quadrant.

    Borderline metatraits resolve to whichever side they're closer to.
    """
    steady = next(m for m in metatraits if m.name == "Steadiness")
    reach  = next(m for m in metatraits if m.name == "Reach")

    def quadrant(m: MetatraitScore) -> str:
        if m.pole == "borderline":
            return "high" if m.percentile >= 60 else "low"
        return m.pole

    return SOUL_SHAPES[(quadrant(steady), quadrant(reach))]


# ─────────────────────────────────────────────────────────────────────
# Step 6 — Archetype
# ─────────────────────────────────────────────────────────────────────
# Each archetype has a target profile of percentile points across the 5 domains.
# We compute Euclidean distance between the user's domain percentiles and each
# archetype target, then pick the closest. Match score = 1 / (1 + distance).
#
# Targets are derived from the IMAGO Names Locked file's wiring descriptions,
# converted to numeric profiles for matching.

ARCHETYPE_TARGETS: Dict[str, Dict[str, float]] = {
    # Domain percentiles for each archetype's "ideal" profile
    # Used as a centroid for nearest-neighbor matching
    "Shepherd": {
        "I": 50, "M": 50, "A": 60, "G": 80, "O": 85,
        # high G + very steady O + medium-high A + medium M + medium I
    },
    "Mason": {
        "I": 70, "M": 80, "A": 40, "G": 50, "O": 75,
        # high M + high I (Intellect) + introverted + high steady O
    },
    "Reformer": {
        "I": 70, "M": 55, "A": 75, "G": 30, "O": 50,
        # low G (Courtesy) + high Assertiveness + high Intellect + medium O
    },
    "Herald": {
        "I": 65, "M": 50, "A": 85, "G": 55, "O": 50,
        # very high A + high Artistry + medium G + medium M + medium O
    },
    "Faithful": {
        "I": 50, "M": 75, "A": 40, "G": 55, "O": 75,
        # high Industriousness + steady elsewhere
    },
    "Maker": {
        "I": 80, "M": 60, "A": 50, "G": 50, "O": 50,
        # very high Artistry + medium-high M + medium else
    },
    "Attuned": {
        "I": 80, "M": 50, "A": 25, "G": 55, "O": 40,
        # very high I (Openness) + low A + low-medium O
    },
    "Initiator": {
        "I": 50, "M": 75, "A": 80, "G": 50, "O": 75,
        # high M + high Assertiveness + steady
    },
    "Learner": {
        "I": 80, "M": 50, "A": 50, "G": 55, "O": 45,
        # high I (both aspects) + medium M + externally pursuing
    },
    "Servant": {
        "I": 35, "M": 35, "A": 30, "G": 60, "O": 45,
        # medium-low across most + relatively higher G
    },
}


# Signature domains per archetype — the traits that DEFINE the archetype
# rather than merely correlating with it. These get extra weight in matching
# so that, e.g., a Reformer profile (high A, low G, high I) is recognized
# even if M and O are average. Without this, the nearest-centroid math
# privileges archetypes with "average" targets.
ARCHETYPE_SIGNATURE_DOMAINS: Dict[str, List[str]] = {
    "Shepherd":  ["G", "O"],          # high G + steady O
    "Mason":     ["M", "I", "O"],     # high M + Intellect + steady
    "Reformer":  ["A", "G", "I"],     # high A + low G + high I (Intellect)
    "Herald":    ["A", "I"],          # very high A + high Artistry
    "Faithful":  ["M", "O"],          # high M + steady O
    "Maker":     ["I"],               # very high Artistry
    "Attuned":   ["I", "A"],          # very high I + low A (introvert)
    "Initiator": ["M", "A"],          # high M + high A
    "Learner":   ["I"],               # very high I (both aspects)
    "Servant":   ["G"],               # high G relative to rest
}

# Weight applied to signature-domain deviations. 2.0 means a 20-point miss
# on a signature domain is treated like a 40-point miss on a non-signature.
SIGNATURE_WEIGHT = 2.0


def _derive_archetype(domain_scores: List[DomainScore]) -> Tuple[str, float]:
    """Find the archetype whose target profile is closest to the user's domain
    percentiles, with extra weight on each archetype's *signature* domains.

    v3 logic: a person's archetype should be determined primarily by the
    domains that DEFINE that archetype, not by the full 5-domain Euclidean
    centroid distance. Otherwise, archetypes with average-looking targets
    (close to 50 across the board) win by default for anyone near the mean.

    Returns (archetype_name, match_score) where match_score is in (0, 1].
    Higher = closer match.
    """
    user_profile = {d.code: d.percentile for d in domain_scores}

    best_name = None
    best_dist = float("inf")
    for name, target in ARCHETYPE_TARGETS.items():
        signature = set(ARCHETYPE_SIGNATURE_DOMAINS.get(name, []))
        # Weighted Euclidean distance — signature domains count more
        sq_sum = 0.0
        for code in ["I", "M", "A", "G", "O"]:
            diff = user_profile.get(code, 50) - target.get(code, 50)
            weight = SIGNATURE_WEIGHT if code in signature else 1.0
            sq_sum += weight * diff * diff
        dist = sq_sum ** 0.5
        if dist < best_dist:
            best_dist = dist
            best_name = name

    # Convert distance to a 0-1 match score (closer = higher)
    match_score = 1 / (1 + best_dist / 50.0)
    return best_name or "Servant", match_score


# ─────────────────────────────────────────────────────────────────────
# Convenience / debug
# ─────────────────────────────────────────────────────────────────────

def score_to_pretty(result: ImagoResult) -> str:
    """For debugging — render a result as readable text."""
    lines = []
    lines.append(f"Letter type: {result.letter_type}")
    if result.letter_type_borderline:
        lines.append(f"  (borderline letters: {', '.join(result.letter_type_borderline)})")
    lines.append(f"Soul Shape: The {result.soul_shape}")
    lines.append(f"Archetype: The {result.archetype} (match: {result.archetype_match_score:.2f})")
    lines.append("")
    lines.append("Metatraits:")
    for m in result.metatraits:
        lines.append(f"  {m.name:12} {m.raw_mean:.2f}  ({m.percentile:.0f}th, {m.pole})")
    lines.append("")
    lines.append("Domains:")
    for d in result.domains:
        lines.append(f"  {d.code} {d.name:14} {d.raw_mean:.2f}  ({d.percentile:.0f}th, {d.pole})")
        for a in d.aspects:
            lines.append(f"      {a.code} {a.name:18} {a.raw_mean:.2f}  ({a.percentile:.0f}th)  n={a.n_items_answered}")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────
# Self-test (run this file directly to verify the math)
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Quick sanity test: simulate a respondent who answers all "4" (Mod accurate)
    # to FORWARD items and "2" (Mod inaccurate) to REVERSE items
    fake_items = []
    for code, _, _ in ASPECTS:
        for i in range(10):
            direction = "FORWARD" if i < 6 else "REVERSE"
            fake_items.append({
                "item_id": f"FAKE-{code}-{i}",
                "aspect_code": code,
                "direction": direction,
            })
    answers = {}
    for item in fake_items:
        answers[item["item_id"]] = 4 if item["direction"] == "FORWARD" else 2

    result = score_imago(answers, fake_items)
    print(score_to_pretty(result))
    print()
    print("JSON output:")
    print(json.dumps(result.to_dict(), indent=2))
