'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

type Student = { id: string; name: string }
type CardEntry = {
  id: string
  studentId: string
  day: number
  question: string
  answer: string | null
  answeredAt: string | null
  drawnAt: string
}

function loadData() {
  const students: Student[] = JSON.parse(localStorage.getItem('contest-students') ?? '[]')
  const cards: CardEntry[] = JSON.parse(localStorage.getItem('contest-cards') ?? '[]')
  return { students, cards }
}

function clearAll() {
  // 구버전 키 포함 전부 삭제
  localStorage.removeItem('memos')
  localStorage.removeItem('contest-students')
  localStorage.removeItem('contest-cards')
}

export default function DeckPage() {
  const [students, setStudents] = useState<Student[]>([])
  const [cards, setCards] = useState<CardEntry[]>([])

  useEffect(() => {
    const { students, cards } = loadData()
    setStudents(students)
    setCards(cards)
  }, [])

  function handleRefresh() {
    const { students, cards } = loadData()
    setStudents(students)
    setCards(cards)
  }

  function handleClearAll() {
    clearAll()
    setStudents([])
    setCards([])
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-950 to-slate-900 p-6">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-bold text-white">덱창</h1>
          <div className="flex items-center gap-4">
            <button
              onClick={handleClearAll}
              className="text-sm text-red-400/60 hover:text-red-400 transition-colors"
            >
              초기화
            </button>
            <button
              onClick={handleRefresh}
              className="text-sm text-white/40 hover:text-white transition-colors"
            >
              새로고침
            </button>
            <Link
              href="/student"
              className="text-sm text-purple-300 hover:text-white transition-colors underline underline-offset-2"
            >
              ← 학생창
            </Link>
          </div>
        </div>

        {students.length === 0 ? (
          <div className="text-center text-white/30 mt-32">
            학생창에서 학생이 입장하면 카드가 여기에 표시됩니다.
          </div>
        ) : (
          <div className="space-y-10">
            {students.map(student => {
              const mine = cards.filter(c => c.studentId === student.id)
              return (
                <div key={student.id}>
                  <p className="text-white font-semibold mb-4">{student.name}</p>
                  <div className="grid grid-cols-5 gap-4">
                    {[1, 2, 3, 4, 5].map(day => {
                      const card = mine.find(c => c.day === day)
                      return (
                        <div key={day} style={{ aspectRatio: '3/4' }}>
                          {!card ? (
                            <div className="w-full h-full rounded-2xl border border-dashed border-white/10" />
                          ) : !card.answer ? (
                            <div className="w-full h-full rounded-2xl bg-gradient-to-br from-purple-600/40 to-indigo-800/40 flex items-center justify-center">
                              <span className="text-white/20 text-3xl">✦</span>
                            </div>
                          ) : (
                            <div className="w-full h-full rounded-2xl bg-white/5 border border-white/10 p-3 flex flex-col overflow-hidden">
                              <p className="text-white/50 text-[10px] leading-snug mb-2">{card.question}</p>
                              <div className="h-px bg-white/10 mb-2" />
                              <p className="text-purple-300 text-[10px] leading-snug">{card.answer}</p>
                            </div>
                          )}
                        </div>
                      )
                    })}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </main>
  )
}
