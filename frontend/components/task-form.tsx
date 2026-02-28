'use client'

import React, { useState } from 'react'
import { Plus, AlertCircle, CheckCircle, Sparkles, X } from 'lucide-react'
import { CreateTaskRequest } from '@/types'
import { cn } from '@/lib/utils'

interface TaskFormProps {
  onSubmit: (data: CreateTaskRequest) => Promise<void>
  className?: string
  isLoading?: boolean
}

export function TaskForm({ onSubmit, className, isLoading = false }: TaskFormProps) {
  const [formData, setFormData] = useState({
    title: '',
    description: ''
  })
  const [errors, setErrors] = useState<{ title?: string; description?: string }>({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [success, setSuccess] = useState(false)
  const [isOpen, setIsOpen] = useState(false)

  const validateForm = () => {
    const newErrors: { title?: string; description?: string } = {}

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!validateForm()) return

    setIsSubmitting(true)
    try {
      await onSubmit({
        title: formData.title.trim(),
        description: formData.description.trim() || undefined
      })
      setFormData({ title: '', description: '' })
      setSuccess(true)
      setTimeout(() => {
        setSuccess(false)
        setIsOpen(false)
      }, 1500)
    } catch (error) {
      console.error('Failed to create task:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className={cn("w-full mb-10", className)}>
      {!isOpen ? (
        <button 
          onClick={() => setIsOpen(true)}
          className="w-full py-5 px-8 glass rounded-3xl border border-white/50 shadow-xl shadow-indigo-100/30 flex items-center justify-between group hover:scale-[1.01] transition-all duration-500 text-left"
        >
          <div className="flex items-center gap-5">
            <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-violet-500 rounded-2xl flex items-center justify-center shadow-lg shadow-indigo-200 group-hover:rotate-12 transition-all">
              <Plus className="text-white w-6 h-6" />
            </div>
            <div>
              <h3 className="text-lg font-black text-slate-900 tracking-tight leading-none mb-1.5">Create New Task</h3>
              <p className="text-[13px] font-bold text-slate-400 uppercase tracking-widest leading-none">Stay focused and productive</p>
            </div>
          </div>
          <div className="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center text-slate-400 group-hover:text-indigo-600 group-hover:bg-indigo-50 transition-all">
            <Sparkles className="w-5 h-5" />
          </div>
        </button>
      ) : (
        <div className="glass p-8 rounded-3xl shadow-2xl shadow-indigo-200/50 border-white/50 animate-in zoom-in duration-300 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-50 rounded-full blur-3xl -z-10" />
          
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-2xl font-black text-slate-900 tracking-tight">New Mission</h2>
            <button 
              onClick={() => setIsOpen(false)}
              className="p-2 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-50 transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2 group">
              <label className="text-[11px] font-black uppercase tracking-[0.2em] text-slate-400 ml-1">Title</label>
              <input
                placeholder="What needs to be done?"
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                className="w-full px-6 py-4 bg-white border border-slate-200 rounded-2xl font-bold text-slate-900 placeholder:text-slate-300 focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500/50 outline-none transition-all"
                disabled={isSubmitting}
                autoFocus
              />
              {errors.title && <p className="text-xs font-bold text-red-500 ml-1">{errors.title}</p>}
            </div>

            <div className="space-y-2">
              <label className="text-[11px] font-black uppercase tracking-[0.2em] text-slate-400 ml-1">Notes (Optional)</label>
              <textarea
                placeholder="Add context, links, or details..."
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                className="w-full px-6 py-4 bg-white border border-slate-200 rounded-2xl font-bold text-slate-900 placeholder:text-slate-300 focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500/50 outline-none transition-all min-h-[120px] resize-none"
                disabled={isSubmitting}
              />
            </div>

            <div className="pt-2 flex gap-3">
              <button
                type="submit"
                disabled={!formData.title.trim() || isSubmitting}
                className="flex-1 btn-premium"
              >
                {isSubmitting ? (
                  <LoaderIcon className="w-5 h-5 animate-spin" />
                ) : success ? (
                  <span className="flex items-center"><CheckCircle className="w-5 h-5 mr-2" /> Task Launched</span>
                ) : (
                  <span className="flex items-center"><Plus className="w-5 h-5 mr-2" /> Create Task</span>
                )}
              </button>
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="px-6 py-3 bg-slate-50 text-slate-500 font-bold rounded-xl hover:bg-slate-100 transition-all active:scale-95"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}

function LoaderIcon({ className }: { className?: string }) {
  return (
    <svg 
      className={className} 
      xmlns="http://www.w3.org/2000/svg" 
      fill="none" 
      viewBox="0 0 24 24"
    >
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
  )
}
