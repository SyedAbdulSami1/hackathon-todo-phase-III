'use client'

import React from 'react'
import { 
  CheckCircle2, 
  Circle, 
  Trash2, 
  Calendar, 
  Clock,
  ChevronRight,
  MoreVertical
} from 'lucide-react'
import { Task } from '@/types'
import { cn } from '@/lib/utils'

interface TaskCardProps {
  task: Task
  onToggleComplete: (taskId: number) => void
  onDelete: (taskId: number) => void
  className?: string
}

export function TaskCard({
  task,
  onToggleComplete,
  onDelete,
  className
}: TaskCardProps) {
  const isCompleted = task.status === 'completed'

  return (
    <div
      className={cn(
        "group relative bg-white rounded-3xl p-6 border border-slate-200/60 shadow-sm hover:shadow-xl hover:shadow-indigo-100/50 transition-all duration-500 overflow-hidden",
        isCompleted && "bg-slate-50/50 border-slate-100",
        className
      )}
    >
      {/* Dynamic Background Element */}
      <div className={cn(
        "absolute -right-8 -top-8 w-24 h-24 rounded-full blur-3xl transition-opacity duration-500",
        isCompleted ? "bg-green-100/40 opacity-100" : "bg-indigo-100/40 opacity-0 group-hover:opacity-100"
      )} />

      <div className="relative flex items-start gap-5">
        {/* Modern Checkbox */}
        <button
          onClick={() => onToggleComplete(task.id)}
          className={cn(
            "mt-1 w-7 h-7 rounded-xl flex items-center justify-center transition-all duration-300 ring-4",
            isCompleted 
              ? "bg-green-500 text-white ring-green-50 shadow-lg shadow-green-200" 
              : "bg-white border-2 border-slate-200 text-transparent ring-transparent hover:border-indigo-400 hover:ring-indigo-50"
          )}
        >
          <CheckCircle2 className={cn("w-4 h-4 transition-transform duration-300", isCompleted ? "scale-100" : "scale-0")} />
        </button>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-3 mb-1.5">
            <h3
              className={cn(
                "text-lg font-black tracking-tight transition-all duration-300",
                isCompleted ? "text-slate-400 line-through" : "text-slate-900"
              )}
            >
              {task.title}
            </h3>
            {isCompleted && (
              <span className="px-2 py-0.5 bg-green-100 text-green-600 text-[10px] font-black uppercase tracking-widest rounded-lg ring-1 ring-green-200">
                Done
              </span>
            )}
          </div>

          {task.description && (
            <p
              className={cn(
                "text-[14px] font-medium leading-relaxed mb-4 line-clamp-2 transition-all duration-300",
                isCompleted ? "text-slate-300" : "text-slate-500"
              )}
            >
              {task.description}
            </p>
          )}

          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2 text-[11px] font-bold text-slate-400 uppercase tracking-widest">
              <Calendar className="w-3.5 h-3.5 text-indigo-400" />
              <span>{new Date(task.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}</span>
            </div>
            
            {task.updated_at !== task.created_at && (
              <div className="flex items-center gap-2 text-[11px] font-bold text-slate-400 uppercase tracking-widest">
                <Clock className="w-3.5 h-3.5 text-slate-300" />
                <span>Updated</span>
              </div>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-1">
          <button
            onClick={() => onDelete(task.id)}
            className="p-2.5 rounded-xl text-slate-300 hover:text-red-500 hover:bg-red-50 transition-all active:scale-90"
            title="Delete Task"
          >
            <Trash2 className="w-5 h-5" />
          </button>
          <button className="p-2.5 rounded-xl text-slate-300 hover:text-slate-600 hover:bg-slate-50 transition-all md:hidden">
            <MoreVertical className="w-5 h-5" />
          </button>
        </div>
      </div>
      
      {/* Subtle indicator for incomplete high-priority tasks (future) */}
      {!isCompleted && (
        <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-indigo-500 rounded-r-full opacity-0 group-hover:opacity-100 transition-opacity" />
      )}
    </div>
  )
}
