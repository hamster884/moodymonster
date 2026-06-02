"""
deck_analyzer.py — Aggregates a student's weekly card deck into analysis-ready scores
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Optional

from normalize import card_to_negative_score


@dataclass
class CardData:
    """Single card selected by a student on one day."""
    day: int                    # 1-5
    emotion: str
    x: float                   # coordinate in [-5, 5]
    y: float                   # coordinate in [-5, 5]
    quadrant: str               # 'red' | 'yellow' | 'blue' | 'green'
    memo: str = ""


@dataclass
class DeckAnalysis:
    """Aggregated statistics for one student's 5-day deck."""
    total_cards: int
    negative_count: int
    negative_ratio: float          # negative_count / total_cards
    weekly_neg_score: float        # mean of daily neg_scores in [0, 1]
    daily_neg_scores: list[float]  # one per card/day
    high_intensity_cards: list[CardData] = field(default_factory=list)  # dist >= 5
    daily_variance: Optional[float] = None  # variance of daily_neg_scores
    survey_neg_normalized: Optional[float] = None   # from survey input if available
    survey_se_normalized: Optional[float] = None    # from survey input if available


_MIN_CARDS = 5
_HIGH_INTENSITY_DIST = 5.0
_MAX_DIST = math.sqrt(50)


def analyze_deck(cards: list[CardData]) -> Optional[DeckAnalysis]:
    """
    Aggregate card data into DeckAnalysis.

    Returns None when fewer than _MIN_CARDS cards are present (shows "분석중" in UI).
    """
    if len(cards) < _MIN_CARDS:
        return None

    daily_neg_scores = [card_to_negative_score(c.x, c.y) for c in cards]

    negative_cards = [c for c in cards if c.x < 0]
    negative_count = len(negative_cards)
    negative_ratio = negative_count / len(cards)
    weekly_neg_score = sum(daily_neg_scores) / len(daily_neg_scores)

    high_intensity = [
        c for c in negative_cards
        if math.sqrt(c.x ** 2 + c.y ** 2) >= _HIGH_INTENSITY_DIST
    ]

    n = len(daily_neg_scores)
    mean = weekly_neg_score
    variance = sum((s - mean) ** 2 for s in daily_neg_scores) / n if n > 1 else 0.0

    return DeckAnalysis(
        total_cards=len(cards),
        negative_count=negative_count,
        negative_ratio=negative_ratio,
        weekly_neg_score=weekly_neg_score,
        daily_neg_scores=daily_neg_scores,
        high_intensity_cards=high_intensity,
        daily_variance=variance,
    )
