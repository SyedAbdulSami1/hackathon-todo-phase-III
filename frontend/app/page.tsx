'use client'

import { useState, useEffect } from 'react'
import { TaskList } from '@/components/task-list'
import { AuthForms } from '@/components/auth-forms'
import { authClient } from '@/lib/auth'
import { User } from '@/types'
import { Navigation } from '@/components/Navigation'

export default function Home() {
  const [loggedIn, setLoggedIn] = useState(false)
  const [user, setUser] = useState<User | null>(null)
  const [isMounted, setIsMounted] = useState(false)

  useEffect(() => {
    setIsMounted(true)
    const isAuthenticated = authClient.isAuthenticated()
    setLoggedIn(isAuthenticated)

    if (isAuthenticated) {
      const fetchUser = async () => {
        const currentUser = await authClient.getCurrentUser()
        setUser(currentUser)
      }
      fetchUser()
    }
  }, [])

  const handleLogout = () => {
    authClient.logout()
    setLoggedIn(false)
    setUser(null)
  }

  if (!isMounted) {
    return null
  }

  if (!loggedIn) {
    return (
      <div className="min-h-screen flex flex-col">
        <div className="container mx-auto px-4 py-16 flex-1 flex flex-col lg:flex-row items-center justify-center gap-16">
          <div className="flex-1 text-center lg:text-left space-y-8 animate-in fade-in slide-in-from-left-8 duration-700">
            <div className="inline-flex items-center space-x-2 px-4 py-2 bg-indigo-50 border border-indigo-100 rounded-full text-indigo-600 font-bold text-xs uppercase tracking-widest shadow-sm shadow-indigo-100/50">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
              </span>
              <span>Next-Gen Task Management</span>
            </div>
            
            <h1 className="text-6xl lg:text-7xl font-black text-slate-900 tracking-tight leading-[0.9]">
              Master your day with <span className="text-gradient">TaskFlow</span>
            </h1>
            
            <p className="text-xl text-slate-500 max-w-xl mx-auto lg:mx-0 font-medium leading-relaxed">
              The only AI-powered todo app that understands you. Organize tasks, chat with your personal assistant, and boost your productivity to founder levels.
            </p>
            
            <div className="flex flex-wrap items-center justify-center lg:justify-start gap-6 pt-4">
              <div className="flex -space-x-3">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i} className="w-12 h-12 rounded-2xl border-4 border-white bg-slate-100 flex items-center justify-center shadow-sm overflow-hidden">
                    <img src={`https://i.pravatar.cc/150?u=${i + 10}`} alt="User" />
                  </div>
                ))}
                <div className="w-12 h-12 rounded-2xl border-4 border-white bg-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-200 text-white text-xs font-bold">
                  +2k
                </div>
              </div>
              <div className="text-sm font-bold text-slate-400 uppercase tracking-widest">
                Trusted by 2,000+ Founders
              </div>
            </div>
          </div>

          <div className="w-full max-w-md animate-in fade-in slide-in-from-right-8 duration-700 delay-200">
            <div className="glass p-8 rounded-3xl shadow-2xl shadow-indigo-200/50 border-white/50 relative">
              <div className="absolute -top-6 -right-6 w-24 h-24 bg-gradient-to-br from-indigo-500 to-violet-500 rounded-3xl shadow-xl shadow-indigo-200 rotate-12 -z-10 animate-float"></div>
              <div className="absolute -bottom-6 -left-6 w-16 h-16 bg-gradient-to-br from-amber-400 to-orange-400 rounded-2xl shadow-xl shadow-amber-200 -rotate-12 -z-10 animate-float" style={{ animationDelay: '1s' }}></div>
              
              <h2 className="text-2xl font-black text-slate-900 mb-8 tracking-tight">Welcome to the future</h2>
              <AuthForms onSuccess={() => setLoggedIn(true)} />
            </div>
          </div>
        </div>
        
        <footer className="py-10 border-t border-slate-200/50 text-center">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-[0.2em]">
            Built for the Hackathon Phase III • 2026
          </p>
        </footer>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <Navigation user={user || undefined} onLogout={handleLogout} />
      <TaskList />
    </div>
  )
}