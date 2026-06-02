"""
feedback_generator.py — Role-specific feedback messages for 무디몬스터
"""

from __future__ import annotations
from typing import Optional
from classifier import ClassificationResult


# ── Student-facing messages (NO "위기/위험" language) ──────────────────────────
_STUDENT_MESSAGES = {
    "정상": [
        "이번 주도 감정을 잘 돌보고 있어요. 앞으로도 계속 기록해봐요!",
        "다양한 감정을 느끼면서 잘 지내고 있군요. 내일도 카드를 골라봐요.",
        "이번 주 감정 기록 완료! 나의 감정을 아는 것이 가장 큰 힘이에요.",
    ],
    "주의": [
        "요즘 조금 힘든 감정이 많았군요. 오늘은 좋아하는 것을 하나 해봐요.",
        "마음이 무거울 때는 잠깐 쉬어가도 괜찮아요. 가까운 사람에게 말을 걸어보는 건 어때요?",
        "이번 주 힘든 감정을 잘 표현했어요. 선생님이나 가족에게 오늘 하루를 이야기해봐요.",
    ],
    "위기": [
        "요즘 많이 지치고 힘들었을 것 같아요. 혼자 참지 말고 가까운 어른에게 이야기해주세요.",
        "무거운 감정을 계속 혼자 안고 있었군요. 선생님이나 부모님께 오늘 기분을 꼭 알려주세요.",
        "마음이 많이 아팠던 한 주였군요. 당신 곁에 도움을 줄 수 있는 사람이 있어요.",
    ],
}

# ── Teacher-facing messages ────────────────────────────────────────────────────
_TEACHER_MESSAGES = {
    "정상": [
        "이번 주 감정 상태가 안정적입니다. 꾸준히 관찰을 이어가주세요.",
        "감정 패턴이 건강한 범위에 있습니다. 긍정적인 피드백으로 동기를 유지해주세요.",
    ],
    "주의": [
        "부정적 감정 비율이 다소 높습니다. 개별 면담이나 관심 있는 대화를 권장합니다.",
        "이번 주 감정 강도가 평균보다 높습니다. 학생의 생활 환경 변화가 있었는지 확인해보세요.",
        "주의 신호가 감지되었습니다. 학생과 가벼운 대화를 통해 상태를 확인해주세요.",
    ],
    "위기": [
        "[위기 신호] 이 학생의 부정 감정 강도가 임계값을 초과했습니다. 즉각적인 면담과 보호자 연락을 권고합니다.",
        "[위기 신호] 지속적인 고강도 부정 감정이 확인됩니다. Wee클래스 또는 전문 상담 연계를 검토해주세요.",
        "[위기 신호] 이번 주 감정 패턴이 심각한 수준입니다. 학생 안전을 최우선으로 확인해주세요.",
    ],
}


def _pick_message(bank: dict, status: str, seed: int = 0) -> str:
    msgs = bank.get(status, bank["정상"])
    return msgs[seed % len(msgs)]


def generate_student_feedback(result: ClassificationResult, seed: int = 0) -> str:
    """
    Return a student-facing feedback string.
    Never uses "위기" or "위험" — uses supportive, non-alarming language.
    """
    return _pick_message(_STUDENT_MESSAGES, result.status, seed)


def generate_teacher_feedback(result: ClassificationResult, seed: int = 0) -> str:
    """
    Return a teacher-facing feedback string with clinical detail.
    Includes active flags and scores as context.
    """
    base = _pick_message(_TEACHER_MESSAGES, result.status, seed)
    details = []
    if result.neg_z_score is not None:
        details.append(f"부정감정 Z={result.neg_z_score:.2f}")
    if result.se_z_score is not None:
        details.append(f"자존감 Z={result.se_z_score:.2f}")
    if result.flags:
        details.append(f"플래그: {', '.join(result.flags)}")
    if details:
        base += f" ({'; '.join(details)})"
    return base


def generate_feedback_report(
    student_name: str,
    result: Optional[ClassificationResult],
    audience: str = "teacher",
    seed: int = 0,
) -> dict:
    """
    Return a structured report dict suitable for JSON serialization.

    audience: 'student' | 'teacher'
    result=None means fewer than 5 cards collected → status '분석중'.
    """
    if result is None:
        return {
            "student": student_name,
            "status": "분석중",
            "message": "카드가 5개 이상 모이면 분석이 시작돼요." if audience == "student"
                       else "아직 카드가 충분히 수집되지 않았습니다 (5장 미만).",
            "flags": [],
            "scores": {},
        }

    if audience == "student":
        message = generate_student_feedback(result, seed)
    else:
        message = generate_teacher_feedback(result, seed)

    return {
        "student": student_name,
        "status": result.status,
        "message": message,
        "flags": result.flags,
        "scores": {
            "weekly_neg_score": round(result.weekly_neg_score, 4),
            "negative_ratio": round(result.negative_ratio, 4),
            "neg_z_score": round(result.neg_z_score, 4) if result.neg_z_score is not None else None,
            "se_z_score": round(result.se_z_score, 4) if result.se_z_score is not None else None,
        },
    }
