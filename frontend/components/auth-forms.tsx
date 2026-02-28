'use client'

import React, { useState } from 'react'
import { authClient } from '@/lib/auth'
import { RegisterRequest } from '@/types'
import { Loader2, Mail, Lock, User as UserIcon, ArrowRight } from 'lucide-react'
import { useRouter } from 'next/navigation'

interface AuthFormsProps {
  onSuccess?: () => void
}

export function AuthForms({ onSuccess }: AuthFormsProps) {
  const [activeTab, setActiveTab] = useState<'login' | 'register'>('login')
  const [loginData, setLoginData] = useState({
    username: '',
    password: '',
  })
  const [registerData, setRegisterData] = useState<RegisterRequest>({
    username: '',
    email: '',
    password: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isSuccess, setIsSuccess] = useState(false)
  const router = useRouter()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!loginData.username || !loginData.password) {
      setError('Please fill in all fields')
      return
    }

    try {
      setLoading(true)
      setError(null)
      const response = await authClient.login(loginData as any)
      authClient.saveAuth(response.token, response.user)
      setIsSuccess(true)
      onSuccess?.()
      setTimeout(() => router.push('/'), 1000)
    } catch (err: any) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!registerData.username || !registerData.email || !registerData.password) {
      setError('Please fill in all fields')
      return
    }

    try {
      setLoading(true)
      setError(null)
      const response = await authClient.register(registerData)
      authClient.saveAuth(response.token, response.user)
      setIsSuccess(true)
      onSuccess?.()
      setTimeout(() => router.push('/'), 1000)
    } catch (err: any) {
      setError(err.message || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  if (isSuccess) {
    return (
      <div className="text-center py-10 space-y-4 animate-in zoom-in duration-300">
        <div className="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <Loader2 className="w-8 h-8 animate-spin" />
        </div>
        <h3 className="text-xl font-bold text-slate-900">Successfully Authenticated</h3>
        <p className="text-slate-500 font-medium">Entering TaskFlow...</p>
      </div>
    )
  }

  return (
    <div className="w-full">
      <div className="flex p-1.5 bg-slate-100/50 rounded-2xl mb-8 border border-slate-200/50">
        <button
          onClick={() => setActiveTab('login')}
          className={`flex-1 py-2.5 rounded-xl text-sm font-black transition-all ${
            activeTab === 'login' ? 'bg-white shadow-md text-indigo-600' : 'text-slate-400 hover:text-slate-600'
          }`}
        >
          Login
        </button>
        <button
          onClick={() => setActiveTab('register')}
          className={`flex-1 py-2.5 rounded-xl text-sm font-black transition-all ${
            activeTab === 'register' ? 'bg-white shadow-md text-indigo-600' : 'text-slate-400 hover:text-slate-600'
          }`}
        >
          Register
        </button>
      </div>

      {activeTab === 'login' ? (
        <form onSubmit={handleLogin} className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-300">
          <div className="relative group">
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500 transition-colors">
              <UserIcon className="w-5 h-5" />
            </div>
            <input
              type="text"
              placeholder="Username or Email"
              className="w-full pl-12 pr-4 py-4 bg-white/50 border border-slate-200 rounded-2xl font-bold text-slate-900 placeholder:text-slate-400 focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500/50 outline-none transition-all"
              value={loginData.username}
              onChange={(e) => setLoginData(prev => ({ ...prev, username: e.target.value }))}
              required
              disabled={loading}
            />
          </div>
          <div className="relative group">
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500 transition-colors">
              <Lock className="w-5 h-5" />
            </div>
            <input
              type="password"
              placeholder="Password"
              className="w-full pl-12 pr-4 py-4 bg-white/50 border border-slate-200 rounded-2xl font-bold text-slate-900 placeholder:text-slate-400 focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500/50 outline-none transition-all"
              value={loginData.password}
              onChange={(e) => setLoginData(prev => ({ ...prev, password: e.target.value }))}
              required
              disabled={loading}
            />
          </div>
          <button 
            type="submit" 
            className="w-full btn-premium group" 
            disabled={loading}
          >
            {loading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <span className="flex items-center justify-center">
                Get Started <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </span>
            )}
          </button>
        </form>
      ) : (
        <form onSubmit={handleRegister} className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-300">
          <div className="relative group">
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500 transition-colors">
              <UserIcon className="w-5 h-5" />
            </div>
            <input
              type="text"
              placeholder="Username"
              className="w-full pl-12 pr-4 py-4 bg-white/50 border border-slate-200 rounded-2xl font-bold text-slate-900 placeholder:text-slate-400 focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500/50 outline-none transition-all"
              value={registerData.username}
              onChange={(e) => setRegisterData(prev => ({ ...prev, username: e.target.value }))}
              required
              disabled={loading}
            />
          </div>
          <div className="relative group">
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500 transition-colors">
              <Mail className="w-5 h-5" />
            </div>
            <input
              type="email"
              placeholder="Email address"
              className="w-full pl-12 pr-4 py-4 bg-white/50 border border-slate-200 rounded-2xl font-bold text-slate-900 placeholder:text-slate-400 focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500/50 outline-none transition-all"
              value={registerData.email}
              onChange={(e) => setRegisterData(prev => ({ ...prev, email: e.target.value }))}
              required
              disabled={loading}
            />
          </div>
          <div className="relative group">
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-500 transition-colors">
              <Lock className="w-5 h-5" />
            </div>
            <input
              type="password"
              placeholder="Create Password"
              className="w-full pl-12 pr-4 py-4 bg-white/50 border border-slate-200 rounded-2xl font-bold text-slate-900 placeholder:text-slate-400 focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500/50 outline-none transition-all"
              value={registerData.password}
              onChange={(e) => setRegisterData(prev => ({ ...prev, password: e.target.value }))}
              required
              disabled={loading}
              minLength={6}
            />
          </div>
          <button 
            type="submit" 
            className="w-full btn-premium group" 
            disabled={loading}
          >
            {loading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <span className="flex items-center justify-center">
                Create Account <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </span>
            )}
          </button>
        </form>
      )}

      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-100 rounded-2xl flex items-start space-x-3 animate-in shake duration-300">
          <div className="w-5 h-5 bg-red-500 text-white rounded-full flex items-center justify-center flex-shrink-0 text-xs font-bold">!</div>
          <p className="text-xs font-bold text-red-600">{error}</p>
        </div>
      )}
    </div>
  )
}
