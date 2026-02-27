'use client'

import React from 'react'
import { TaskStatus } from '@/types'
import { Filter, ListTodo, Clock, CheckCircle2 } from 'lucide-react'
import { cn } from '@/lib/utils'

interface TaskFiltersProps {
  currentFilter: TaskStatus
  onFilterChange: (filter: TaskStatus) => void
  className?: string
}

const statusOptions = [
  { value: 'all' as TaskStatus, label: 'All Missions', icon: ListTodo },
  { value: 'pending' as TaskStatus, label: 'Pending', icon: Clock },
  { value: 'completed' as TaskStatus, label: 'Completed', icon: CheckCircle2 }
] as const

export function TaskFilters({
  currentFilter,
  onFilterChange,
  className
}: TaskFiltersProps) {
  return (
    <div className={cn("flex flex-wrap p-1.5 bg-slate-100/50 rounded-2xl border border-slate-200/50 w-fit", className)}>
      {statusOptions.map((option) => {
        const Icon = option.icon;
        const isActive = currentFilter === option.value;
        return (
          <button
            key={option.value}
            onClick={() => onFilterChange(option.value)}
            className={cn(
              "flex items-center gap-2.5 px-6 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all duration-300",
              isActive 
                ? "bg-white text-indigo-600 shadow-md shadow-indigo-100/50 border border-slate-200/60" 
                : "text-slate-400 hover:text-slate-600 hover:bg-white/50"
            )}
          >
            <Icon className={cn("w-3.5 h-3.5", isActive ? "text-indigo-500" : "text-slate-300")} />
            {option.label}
          </button>
        )
      })}
    </div>
  )
}
