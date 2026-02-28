'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import { TaskList } from '@/components/task-list'
import { AuthForms } from '@/components/auth-forms'
import { authClient } from '@/lib/auth'
import { User } from '@/types'
import { Navigation } from '@/components/Navigation'
import { FloatingChat } from '@/components/FloatingChat'
import { 
  Sparkles, 
  ShieldCheck, 
  Zap, 
  Cpu, 
  ArrowRight, 
  Github, 
  Linkedin,
  BrainCircuit,
  Layout,
  MessageSquare,
  Mail,
  MessageCircle
} from 'lucide-react'

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

  if (!isMounted) return null

  if (!loggedIn) {
    return (
      <div className="overflow-x-hidden">
        {/* Navigation for Landing */}
        <nav className="fixed top-0 w-full z-50 apple-glass h-20 flex items-center">
          <div className="section-container w-full flex justify-between items-center">
            <div className="text-2xl font-bold tracking-tight">Task<span className="text-indigo-600">Flow</span></div>
            <button 
              onClick={() => document.getElementById('auth-section')?.scrollIntoView({ behavior: 'smooth' })}
              className="px-6 py-2 bg-[#1D1D1F] text-white rounded-full text-sm font-semibold hover:bg-black transition-all"
            >
              Sign In
            </button>
          </div>
        </nav>

        {/* HERO SECTION */}
        <section className="pt-40 pb-20 bg-white">
          <div className="section-container text-center space-y-8">
            <div className="inline-flex items-center space-x-2 px-4 py-2 bg-indigo-50 rounded-full text-indigo-600 font-bold text-xs uppercase tracking-widest animate-slide-up">
              <Sparkles className="w-4 h-4" />
              <span>Intelligent Task Management</span>
            </div>
            <h1 className="text-hero animate-slide-up [animation-delay:100ms]">
              Organize everything. <br />
              <span className="text-indigo-600">Aided by Intelligence.</span>
            </h1>
            <p className="max-w-2xl mx-auto text-xl text-[#86868B] font-medium animate-slide-up [animation-delay:200ms]">
              TaskFlow merges the simplicity of a todo list with the power of Google Gemini AI. 
              Designed for high-performers who want to master their day.
            </p>
            <div className="pt-8 animate-slide-up [animation-delay:300ms]">
              <button 
                onClick={() => document.getElementById('auth-section')?.scrollIntoView({ behavior: 'smooth' })}
                className="btn-indigo text-lg"
              >
                Get Started for Free
              </button>
            </div>
          </div>
        </section>

        {/* BENTO FEATURES */}
        <section className="py-20 bg-[#F5F5F7]">
          <div className="section-container">
            <h2 className="text-4xl md:text-5xl font-bold text-center mb-16 tracking-tight">Built for the future of work.</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-white p-10 rounded-[2.5rem] space-y-4 shadow-sm hover:shadow-xl transition-all duration-500 border border-slate-100">
                <div className="w-14 h-14 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mb-6">
                  <BrainCircuit className="w-8 h-8" />
                </div>
                <h3 className="text-2xl font-bold">AI Native</h3>
                <p className="text-[#86868B] font-medium leading-relaxed">Integrated with Google Gemini 1.5 Flash to understand context and manage your tasks via natural language.</p>
              </div>

              <div className="bg-white p-10 rounded-[2.5rem] space-y-4 shadow-sm hover:shadow-xl transition-all duration-500 border border-slate-100">
                <div className="w-14 h-14 bg-rose-50 text-rose-600 rounded-2xl flex items-center justify-center mb-6">
                  <Zap className="w-8 h-8" />
                </div>
                <h3 className="text-2xl font-bold">MCP Enabled</h3>
                <p className="text-[#86868B] font-medium leading-relaxed">Uses Model Context Protocol for secure, local-first task manipulation. Your data, your rules.</p>
              </div>

              <div className="bg-white p-10 rounded-[2.5rem] space-y-4 shadow-sm hover:shadow-xl transition-all duration-500 border border-slate-100">
                <div className="w-14 h-14 bg-amber-50 text-amber-600 rounded-2xl flex items-center justify-center mb-6">
                  <Layout className="w-8 h-8" />
                </div>
                <h3 className="text-2xl font-bold">Apple Aesthetic</h3>
                <p className="text-[#86868B] font-medium leading-relaxed">Clean, minimal, and distraction-free. Designed to let you focus on what truly matters.</p>
              </div>
            </div>
          </div>
        </section>

        {/* FOUNDER SECTION */}
        <section className="py-32 bg-white overflow-hidden">
          <div className="section-container flex flex-col md:flex-row items-center gap-16">
            <div className="flex-1 relative">
              <div className="absolute -top-10 -left-10 w-40 h-40 bg-indigo-100 rounded-full blur-3xl opacity-50"></div>
              <div className="relative z-10 p-2 bg-gradient-to-br from-slate-200 to-indigo-100 rounded-[3rem] shadow-2xl rotate-2">
                <Image 
                  src="https://yt3.googleusercontent.com/ytc/AIdro_nDvqZTu9DGV1ZrV_k8H00SJpHawVKCDhJbUnMO-dPTtjY=s160-c-k-c0x00ffffff-no-rj" 
                  alt="Syed Abdul Sami" 
                  width={400}
                  height={400}
                  className="rounded-[2.8rem] bg-white w-full h-[400px] object-cover"
                />
              </div>
            </div>
            <div className="flex-1 space-y-6">
              <h2 className="text-4xl md:text-5xl font-bold tracking-tight text-indigo-600">Meet the Visionary</h2>
              <h3 className="text-2xl font-bold text-[#1D1D1F]">Syed Abdul Sami <span className="text-[#86868B] font-medium">— Lead Architect</span></h3>
              <p className="text-lg text-[#86868B] font-medium leading-relaxed">
                &quot;TaskFlow was born out of a simple need: To make technology serve us, not the other way around. 
                I built this platform to bridge the gap between human intent and machine execution, using the latest 
                advancements in Agentic AI and MCP.&quot;
              </p>
              <div className="flex flex-wrap gap-4 pt-4">
                <a href="https://github.com/SyedAbdulSami1" target="_blank" rel="noopener noreferrer" className="p-3 bg-slate-100 rounded-full hover:bg-indigo-50 hover:text-indigo-600 transition-all shadow-sm" title="GitHub">
                  <Github className="w-6 h-6" />
                </a>
                <a href="https://www.linkedin.com/in/syed-abdul-sami-964a36277/" target="_blank" rel="noopener noreferrer" className="p-3 bg-slate-100 rounded-full hover:bg-indigo-50 hover:text-indigo-600 transition-all shadow-sm" title="LinkedIn">
                  <Linkedin className="w-6 h-6" />
                </a>
                <a href="mailto:samiwpp@gmail.com" className="p-3 bg-slate-100 rounded-full hover:bg-indigo-50 hover:text-indigo-600 transition-all shadow-sm" title="Email">
                  <Mail className="w-6 h-6" />
                </a>
                <a href="https://wa.me/923018420180" target="_blank" rel="noopener noreferrer" className="p-3 bg-slate-100 rounded-full hover:bg-green-50 hover:text-green-600 transition-all shadow-sm" title="WhatsApp">
                  <MessageCircle className="w-6 h-6" />
                </a>
              </div>
            </div>
          </div>
        </section>

        {/* AUTH SECTION */}
        <section id="auth-section" className="py-32 bg-[#F5F5F7]">
          <div className="max-w-md mx-auto px-6">
            <div className="text-center mb-10 space-y-2">
              <h2 className="text-3xl font-bold tracking-tight">Join TaskFlow</h2>
              <p className="text-[#86868B] font-medium">Start your journey to absolute productivity.</p>
            </div>
            <div className="bg-white p-10 rounded-[2.5rem] shadow-2xl shadow-slate-200/50">
              <AuthForms onSuccess={() => setLoggedIn(true)} />
            </div>
          </div>
        </section>

        <footer className="py-20 bg-white border-t border-slate-100">
          <div className="section-container text-center space-y-4">
            <div className="text-xl font-bold tracking-tight mb-4">Task<span className="text-indigo-600">Flow</span></div>
            <p className="text-sm font-bold text-slate-400 uppercase tracking-[0.2em]">Designed & Developed by Syed Abdul Sami</p>
            <p className="text-xs text-slate-300">© 2026 Hackathon Phase III Edition. All rights reserved.</p>
          </div>
        </footer>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#FBFBFD] pb-20">
      <Navigation user={user || undefined} onLogout={handleLogout} />
      <div className="max-w-4xl mx-auto px-6 pt-10">
        <TaskList />
      </div>
      <FloatingChat user={user} />
    </div>
  )
}
