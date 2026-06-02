"""
classifier.py — Z-score + multi-flag crisis classification for 무디몬스터
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from normalize import z_score
from deck_analyzer import DeckAnalysis

# ── Thresholds (수정 2026-05-31: 올바른 변수 매핑 적용) ──
# NEG: 5개년 풀링 (Q23/Q27/Q30A1~A3, n=14001)
# SE:  2024 단독 (Q30A4~A6 3문항 척도, n=2725)
NEG_MEAN_NORM  = 0.2325
NEG_STD_NORM   = 0.2710
NEG_WARN_NORM  = 0.5035   # μ + 1σ
NEG_CRISIS_NORM = 0.7745  # μ + 2σ

SE_MEAN_NORM   = 0.7206
SE_STD_NORM    = 0.2378
SE_WARN_NORM   = 0.4828   # μ - 1σ  (lower = worse)
SE_CRISIS_NORM = 0.2450   # μ - 2σ

Z_WARN   = 1.0
Z_CRISIS = 2.0

FLAG_WARN_COUNT   = 1
FLAG_CRISIS_COUNT = 2

# Auxiliary flag thresholds
HIGH_NEG_RATIO_THRESH     = 0.80
HIGH_INTENSITY_MIN_CARDS  = 2
PERSISTENT_NEG_MAX_VAR    = 0.04   # [0,1]-bounded scores have max variance 0.25; 0.04 ≈ truly flat pattern
PERSISTENT_NEG_MIN_SCORE  = 0.30


@dataclass
class ClassificationResult:
    status: str                     # '정상' | '주의' | '위기'
    neg_z_score: Optional[float]
    se_z_score: Optional[float]     # None if no survey data
    flags: list[str] = field(default_factory=list)
    flag_count: int = 0
    weekly_neg_score: float = 0.0
    negative_ratio: float = 0.0


def _compute_flags(analysis: DeckAnalysis) -> list[str]:
    flags = []

    if analysis.negative_ratio >= HIGH_NEG_RATIO_THRESH:
        flags.append("HIGH_NEGATIVE_RATIO")

    if len(analysis.high_intensity_cards) >= HIGH_INTENSITY_MIN_CARDS:
        flags.append("HIGH_INTENSITY")

    if (
        analysis.daily_variance is not None
        and analysis.daily_variance < PERSISTENT_NEG_MAX_VAR
        and analysis.weekly_neg_score > PERSISTENT_NEG_MIN_SCORE
    ):
        flags.append("PERSISTENT_NEGATIVE")

    return flags


def classify(
    analysis: DeckAnalysis,
    survey_neg_normalized: Optional[float] = None,
    survey_se_normalized: Optional[float] = None,
) -> ClassificationResult:
    """
    Classify a student's emotional state using Z-score and auxiliary flags.

    Priority: 위기 > 주의 > 정상.
    Falls back to card-only analysis when survey scores are absent.
    """
    # Use card score as primary; blend survey score if available
    if survey_neg_normalized is not None:
        neg_score = (analysis.weekly_neg_score + survey_neg_normalized) / 2
    else:
        neg_score = analysis.weekly_neg_score

    neg_z = z_score(neg_score, NEG_MEAN_NORM, NEG_STD_NORM)

    se_z = None
    if survey_se_normalized is not None:
        # Self-esteem: low score = bad, so negate Z for crisis detection
        se_z = z_score(survey_se_normalized, SE_MEAN_NORM, SE_STD_NORM)

    flags = _compute_flags(analysis)
    flag_count = len(flags)

    # Combine signals: crisis if any primary signal is critical
    is_crisis = (
        (neg_z is not None and neg_z >= Z_CRISIS)
        or (se_z is not None and se_z <= -Z_CRISIS)
        or flag_count >= FLAG_CRISIS_COUNT
    )
    is_warning = (
        (neg_z is not None and neg_z >= Z_WARN)
        or (se_z is not None and se_z <= -Z_WARN)
        or flag_count >= FLAG_WARN_COUNT
    )

    if is_crisis:
        status = "위기"
    elif is_warning:
        status = "주의"
    else:
        status = "정상"

    return ClassificationResult(
        status=status,
        neg_z_score=neg_z,
        se_z_score=se_z,
        flags=flags,
        flag_count=flag_count,
        weekly_neg_score=analysis.weekly_neg_score,
        negative_ratio=analysis.negative_ratio,
    )
