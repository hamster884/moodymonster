"""
test_cases.py — 5 representative test cases for 무디몬스터 crisis algorithm
"""

from deck_analyzer import CardData, analyze_deck
from classifier import classify
from feedback_generator import generate_feedback_report


# ── Test case definitions ─────────────────────────────────────────────────────

CASES = [
    {
        "name": "정상 케이스 (이로은)",
        "desc": "긍정/중립 감정 주도, 부정 없음",
        "cards": [
            CardData(day=1, emotion="행복한",    x=3,  y=3,  quadrant="yellow"),
            CardData(day=2, emotion="평온한",    x=1,  y=-1, quadrant="green"),
            CardData(day=3, emotion="기분 좋은", x=2,  y=2,  quadrant="yellow"),
            CardData(day=4, emotion="감사하는",  x=3,  y=-5, quadrant="green"),
            CardData(day=5, emotion="만족스러운",x=2,  y=1,  quadrant="yellow"),
        ],
        "survey_neg": None,
        "survey_se": None,
        "expected_status": "정상",
    },
    {
        "name": "주의 케이스 (김민준)",
        "desc": "부정 카드 80%(HIGH_NEGATIVE_RATIO), 고강도 1개만 — 플래그 1개로 주의",
        "cards": [
            CardData(day=1, emotion="슬픈",      x=-1, y=-5, quadrant="blue"),   # dist≈5.1 ≥5
            CardData(day=2, emotion="외로운",    x=-2, y=-3, quadrant="blue"),   # dist≈3.6 <5
            CardData(day=3, emotion="피로한",    x=-2, y=-2, quadrant="blue"),   # dist≈2.8 <5
            CardData(day=4, emotion="기분 좋은", x=2,  y=2,  quadrant="yellow"), # positive
            CardData(day=5, emotion="멍한",      x=-1, y=-1, quadrant="blue"),   # dist≈1.4 <5
        ],
        "survey_neg": None,
        "survey_se": None,
        "expected_status": "주의",
    },
    {
        "name": "위기 케이스 (박서연)",
        "desc": "5일 내내 고강도 부정 감정, HIGH_INTENSITY + HIGH_NEGATIVE_RATIO",
        "cards": [
            CardData(day=1, emotion="분노한",    x=-4, y=5,  quadrant="red"),
            CardData(day=2, emotion="격노한",    x=-5, y=5,  quadrant="red"),
            CardData(day=3, emotion="절망적인",  x=-4, y=-5, quadrant="blue"),
            CardData(day=4, emotion="좌절한",    x=-2, y=4,  quadrant="red"),
            CardData(day=5, emotion="비통한",    x=-3, y=-5, quadrant="blue"),
        ],
        "survey_neg": None,
        "survey_se": None,
        "expected_status": "위기",
    },
    {
        "name": "혼합 케이스 (최지우) — 설문 포함",
        "desc": "카드 자체는 주의 경계, 설문 자존감 낮아 위기로 상승",
        "cards": [
            CardData(day=1, emotion="우울한",    x=-2, y=-4, quadrant="blue"),
            CardData(day=2, emotion="슬픈",      x=-1, y=-5, quadrant="blue"),
            CardData(day=3, emotion="평온한",    x=1,  y=-1, quadrant="green"),
            CardData(day=4, emotion="지친",      x=-3, y=-3, quadrant="blue"),
            CardData(day=5, emotion="외로운",    x=-3, y=-4, quadrant="blue"),
        ],
        "survey_neg": 0.75,   # normalized Likert: high negative emotion reported
        "survey_se": 0.10,    # normalized: very low self-esteem
        "expected_status": "위기",
    },
    {
        "name": "결측 케이스 (정하은)",
        "desc": "카드 3장 — 분석 불가 (5장 미만)",
        "cards": [
            CardData(day=1, emotion="슬픈",   x=-1, y=-5, quadrant="blue"),
            CardData(day=2, emotion="행복한", x=3,  y=3,  quadrant="yellow"),
            CardData(day=3, emotion="피로한", x=-2, y=-2, quadrant="blue"),
        ],
        "survey_neg": None,
        "survey_se": None,
        "expected_status": "분석중",
    },
]


# ── Runner ────────────────────────────────────────────────────────────────────

def run_all():
    print("=" * 60)
    print("무디몬스터 알고리즘 테스트")
    print("=" * 60)

    passed = 0
    for i, case in enumerate(CASES, 1):
        analysis = analyze_deck(case["cards"])
        if analysis is None:
            result = None
        else:
            result = classify(
                analysis,
                survey_neg_normalized=case.get("survey_neg"),
                survey_se_normalized=case.get("survey_se"),
            )

        student_report = generate_feedback_report(
            case["name"], result, audience="student", seed=i
        )
        teacher_report = generate_feedback_report(
            case["name"], result, audience="teacher", seed=i
        )

        actual_status = student_report["status"]
        ok = actual_status == case["expected_status"]
        mark = "PASS" if ok else "FAIL"
        if ok:
            passed += 1

        print(f"\n[{i}] {case['name']} — {case['desc']}")
        print(f"  예상: {case['expected_status']}  실제: {actual_status}  [{mark}]")
        print(f"  학생 메시지: {student_report['message']}")
        print(f"  교사 메시지: {teacher_report['message']}")
        if result:
            print(f"  점수: {student_report['scores']}")
            print(f"  플래그: {result.flags}")

    print("\n" + "=" * 60)
    print(f"결과: {passed}/{len(CASES)} 통과")
    print("=" * 60)


if __name__ == "__main__":
    run_all()
