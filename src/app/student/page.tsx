'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

const STUDENTS_KEY = 'contest-students'
const CARDS_KEY = 'contest-cards'

const QUESTIONS = [
  "오늘 가장 인상 깊었던 점은 무엇인가요?",
  "오늘 배운 내용 중 가장 중요한 것은?",
  "어려웠던 점과 해결 방법은?",
  "내일 더 발전시키고 싶은 부분은?",
  "팀 활동에서 내가 기여한 점은?",
  "오늘의 목표를 얼마나 달성했나요?",
  "가장 잘 수행한 점 하나를 적어보세요.",
  "다음에 개선하고 싶은 점은?",
  "오늘 프로젝트에서 배운 교훈은?",
  "협업에서 느낀 점을 공유해보세요.",
]

type Student = { id: string; name: string }
type CardEntry = {
  id: string; studentId: string; day: number
  question: string; answer: string | null; answeredAt: string | null; drawnAt: string
}

export default function StudentPage() {
  const [nameInput, setNameInput] = useState('')
  const [student, setStudent] = useState<Student | null>(null)
  const [cards, setCards] = useState<CardEntry[]>([])
  const [flippedDays, setFlippedDays] = useState<Set<number>>(new Set())
  const [answers, setAnswers] = useState<Record<number, string>>({})

  useEffect(() => {
    if (!student) return
    const all: CardEntry[] = JSON.parse(localStorage.getItem(CARDS_KEY) ?? '[]')
    const mine = all.filter(c => c.studentId === student.id)
    setCards(mine)
    setFlippedDays(new Set(mine.filter(c => c.answer).map(c => c.day)))
  }, [student])

  function handleEnter() {
    const name = nameInput.trim()
    if (!name) return
    const students: Student[] = JSON.parse(localStorage.getItem(STUDENTS_KEY) ?? '[]')
    let s = students.find(s => s.name === name)
    if (!s) {
      s = { id: Date.now().toString(), name }
      localStorage.setItem(STUDENTS_KEY, JSON.stringify([...students, s]))
    }
    setStudent(s)
  }

  function handleDraw(day: number) {
    if (!student || cards.find(c => c.day === day)) return
    const all: CardEntry[] = JSON.parse(localStorage.getItem(CARDS_KEY) ?? '[]')
    const used = all.filter(c => c.studentId === student.id).map(c => c.question)
    const pool = QUESTIONS.filter(q => !used.includes(q))
    const src = pool.length ? pool : QUESTIONS
    const q = src[Math.floor(Math.random() * src.length)]
    const card: CardEntry = {
      id: `${student.id}-${day}`, studentId: student.id, day,
      question: q, answer: null, answeredAt: null, drawnAt: new Date().toISOString(),
    }
    localStorage.setItem(CARDS_KEY, JSON.stringify([...all, card]))
    setCards(prev => [...prev, card])
  }

  function handleFlip(day: number) {
    setFlippedDays(prev => {
      const next = new Set(prev)
      next.has(day) ? next.delete(day) : next.add(day)
      return next
    })
  }

  function handleSubmit(day: number) {
    const answer = answers[day]?.trim()
    if (!answer || !student) return
    const now = new Date().toISOString()
    const all: CardEntry[] = JSON.parse(localStorage.getItem(CARDS_KEY) ?? '[]')
    const updated = all.map(c =>
      c.studentId === student.id && c.day === day && !c.answer ? { ...c, answer, answeredAt: now } : c
    )
    localStorage.setItem(CARDS_KEY, JSON.stringify(updated))
    setCards(prev => prev.map(c => c.day === day ? { ...c, answer, answeredAt: now } : c))
    setFlippedDays(prev => new Set([...prev, day]))
    setAnswers(prev => { const n = { ...prev }; delete n[day]; return n })
  }

  if (!student) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-950 to-slate-900 flex items-center justify-center p-6">
        <div className="w-full max-w-sm bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 p-8">
          <h1 className="text-2xl font-bold text-white mb-2">학생창</h1>
          <p className="text-white/40 text-sm mb-6">이름을 입력해 카드를 받아보세요</p>
          <input
            type="text" value={nameInput}
            onChange={e => setNameInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleEnter()}
            placeholder="이름 입력"
            className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-white/40 focus:outline-none focus:ring-2 focus:ring-purple-400 mb-4"
          />
          <button onClick={handleEnter} disabled={!nameInput.trim()}
            className="w-full py-3 rounded-lg font-semibold text-white bg-purple-600 hover:bg-purple-500 disabled:opacity-40 transition-colors"
          >입장</button>
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-950 to-slate-900 p-6">
      <style>{`
        .flip-card{transform-style:preserve-3d;transition:transform .6s cubic-bezier(.4,.2,.2,1)}
        .flip-card.flipped{transform:rotateY(180deg)}
        .flip-face{backface-visibility:hidden;-webkit-backface-visibility:hidden}
        .flip-back{transform:rotateY(180deg)}
      `}</style>
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-white">학생창</h1>
            <p className="text-purple-300 text-sm mt-1">안녕하세요, {student.name}님</p>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/deck" className="text-sm text-purple-300 hover:text-white transition-colors underline underline-offset-2">덱창 →</Link>
            <button
              onClick={() => { setStudent(null); setCards([]); setFlippedDays(new Set()); setAnswers({}) }}
              className="text-sm text-white/30 hover:text-white transition-colors"
            >나가기</button>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4 lg:gap-6">
          {[1, 2, 3, 4, 5].map(day => {
            const card = cards.find(c => c.day === day)
            const isFlipped = flippedDays.has(day)
            const isAnswered = !!card?.answer

            return (
              <div key={day} className="flex flex-col items-center gap-2">
                <span className="text-white/40 text-xs font-medium">{day}일차</span>
                <div style={{ perspective: '1000px' }} className="w-full">
                  {!card ? (
                    <button
                      onClick={() => handleDraw(day)}
                      className="w-full aspect-[3/4] rounded-2xl border-2 border-dashed border-white/20 flex flex-col items-center justify-center gap-2 hover:border-purple-400 hover:bg-purple-900/20 transition-all group cursor-pointer"
                    >
                      <span className="text-white/20 text-3xl group-hover:text-purple-400 transition-colors">+</span>
                      <span className="text-white/20 text-xs group-hover:text-purple-400 transition-colors">카드 뽑기</span>
                    </button>
                  ) : (
                    <div
                      className={`flip-card relative w-full ${isFlipped ? 'flipped' : ''}`}
                      style={{ aspectRatio: '3/4' }}
                    >
                      {/* Front */}
                      <div
                        className="flip-face absolute inset-0 rounded-2xl bg-gradient-to-br from-purple-600 to-indigo-800 flex flex-col items-center justify-center cursor-pointer shadow-xl"
                        onClick={() => !isAnswered && handleFlip(day)}
                      >
                        <div className="text-5xl opacity-60 mb-1">✦</div>
                        <div className="text-white/30 text-xs">{day}일차</div>
                      </div>
                      {/* Back */}
                      <div
                        className="flip-face flip-back absolute inset-0 rounded-2xl bg-slate-800/95 border border-white/10 p-3 flex flex-col shadow-xl overflow-hidden"
                        onClick={e => e.stopPropagation()}
                      >
                        <p className="text-white/70 text-xs leading-relaxed flex-shrink-0 mb-2">{card.question}</p>
                        <div className="h-px bg-white/10 flex-shrink-0 mb-2" />
                        {isAnswered ? (
                          <p className="text-purple-300 text-xs leading-relaxed">{card.answer}</p>
                        ) : (
                          <div className="flex flex-col gap-1.5 flex-1 min-h-0">
                            <textarea
                              value={answers[day] ?? ''}
                              onChange={e => setAnswers(prev => ({ ...prev, [day]: e.target.value }))}
                              placeholder="답변..."
                              className="flex-1 w-full bg-white/5 border border-white/10 rounded-lg text-white text-xs placeholder-white/20 p-1.5 resize-none focus:outline-none focus:ring-1 focus:ring-purple-400 min-h-0"
                            />
                            <button
                              onClick={() => handleSubmit(day)}
                              disabled={!answers[day]?.trim()}
                              className="w-full py-1.5 rounded-lg text-xs font-semibold text-white bg-purple-600 hover:bg-purple-500 disabled:opacity-30 transition-colors flex-shrink-0"
                            >저장</button>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </main>
  )
}
