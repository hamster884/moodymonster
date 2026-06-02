// ─────────────────────────────────────────
//  무디몬스터 감정 구조: 4 × 5 × 5 = 100
//  1단계: 사분면 (4)  →  2단계: 강도 그룹 (5)  →  3단계: 세부 감정 (5)
// ─────────────────────────────────────────

const EMOTION_CATEGORIES = [
  {
    id: 'red',
    name: '빨강',
    description: '화나는',
    color: '#E24B4A',
    groups: [
      { level: 1, label: '살짝', emotions: ['불편한', '언짢은', '초조한', '질투하는', '신경질적인'] },
      { level: 2, label: '좀',   emotions: ['미움', '짜증 난', '심술궂은', '안절부절못하는', '짓궂은'] },
      { level: 3, label: '꽤',   emotions: ['욱하는', '좌절한', '기가 죽은', '약 오른', '불안한'] },
      { level: 4, label: '많이', emotions: ['당황한', '경쟁심을 느끼는', '메스꺼운', '겁에 질린', '스트레스 받는'] },
      { level: 5, label: '너무', emotions: ['공황상태의', '충격받은', '분노한', '격분한', '격노한'] }
    ]
  },
  {
    id: 'yellow',
    name: '노랑',
    description: '신나는',
    color: '#EF9F27',
    groups: [
      { level: 1, label: '살짝', emotions: ['기분 좋은', '생기 있는', '만족스러운', '따뜻한', '영감을 받은'] },
      { level: 2, label: '좀',   emotions: ['희망찬', '즐거운', '호기심 가득한', '유쾌한', '놀란'] },
      { level: 3, label: '꽤',   emotions: ['행복한', '쾌활한', '집중하는', '의욕적인', '활발한'] },
      { level: 4, label: '많이', emotions: ['자신감 있는', '희열에 찬', '자부심 있는', '낙관적인', '흥분된'] },
      { level: 5, label: '너무', emotions: ['기운이 넘치는', '전율하는', '활기찬', '황홀한', '열광적인'] }
    ]
  },
  {
    id: 'blue',
    name: '파랑',
    description: '슬픈',
    color: '#378ADD',
    groups: [
      { level: 1, label: '살짝', emotions: ['멍한', '무관심한', '냉담한', '낙심한', '실망한'] },
      { level: 2, label: '좀',   emotions: ['지루한', '피로한', '풀 죽은', '무기력한', '비관적인'] },
      { level: 3, label: '꽤',   emotions: ['피곤한', '소외된', '위축된', '외로운', '지친'] },
      { level: 4, label: '많이', emotions: ['슬픈', '침울한', '낙담한', '구슬픈', '우울한'] },
      { level: 5, label: '너무', emotions: ['비통한', '통곡하는', '절망적인', '비참한', '혐오스러운'] }
    ]
  },
  {
    id: 'green',
    name: '초록',
    description: '편안한',
    color: '#639922',
    groups: [
      { level: 1, label: '살짝', emotions: ['평온한', '신중한', '수줍은', '정적인', '고독한'] },
      { level: 2, label: '좀',   emotions: ['수용적인', '누그러진', '겸손한', '안락한', '사려 깊은'] },
      { level: 3, label: '꽤',   emotions: ['평범한', '차분한', '느긋한', '만족한', '안도하는'] },
      { level: 4, label: '많이', emotions: ['돌보는', '위로받은', '안전한', '아늑한', '편안한'] },
      { level: 5, label: '너무', emotions: ['감사하는', '평온한', '평화로운', '충만한', '고요한'] }
    ]
  }
];

// ─────────────────────────────────────────
//  감정 → 카드 이미지 매핑 (순서대로 001~100)
//  cards/ 폴더에 해당 이미지 넣으면 됨
// ─────────────────────────────────────────

const EMOTION_TO_CARD = (() => {
  const map = {};
  let idx = 1;
  EMOTION_CATEGORIES.forEach(cat => {
    cat.groups.forEach(group => {
      group.emotions.forEach(emotion => {
        if (!map[emotion]) map[emotion] = `cards/${String(idx).padStart(3, '0')}.png`;
        idx++;
      });
    });
  });
  return map;
})();
