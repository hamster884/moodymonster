"""
normalize.py — Min-Max normalization utilities for 무디몬스터 algorithm
"""

import math

# Card coordinate space: x, y ∈ [-5, 5]
_MAX_DIST = math.sqrt(50)  # √(5²+5²) ≈ 7.071


def card_to_negative_score(x: float, y: float) -> float:
    """
    Map card (x, y) coordinates to a negative intensity score in [0, 1].

    Only cards in the negative half (x < 0) contribute; positive/neutral cards score 0.
    Score = Euclidean distance / √50 so the maximum (corner x=-5, y=±5) maps to 1.0.
    """
    if x >= 0:
        return 0.0
    dist = math.sqrt(x ** 2 + y ** 2)
    return dist / _MAX_DIST


def survey_to_normalized(score: float, min_val: float = 1.0, max_val: float = 4.0) -> float:
    """
    Normalize a Likert survey score to [0, 1].

    Default range matches the 4-point scale used in 아동청소년인권실태조사.
    Returns None if score is outside [min_val, max_val].
    """
    if score is None:
        return None
    score = float(score)
    if not (min_val <= score <= max_val):
        return None
    return (score - min_val) / (max_val - min_val)


def z_score(value: float, mean: float, std: float) -> float:
    """Return Z = (value - mean) / std. Returns None if std == 0."""
    if std == 0:
        return None
    return (value - mean) / std


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    """Clamp value to [lo, hi]."""
    return max(lo, min(hi, value))
