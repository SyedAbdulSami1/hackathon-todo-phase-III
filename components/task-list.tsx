'use client'

import { useState, useEffect, useCallback } from 'react'
import { TaskCard } from './task-card'
import { TaskFilters } from './task-filters'
import { TaskForm } from './task-form'
import { NoTasksEmptyState, AllTasksCompletedEmptyState, NoFilteredTasksEmptyState } from './empty-state'
import { LoadingSkeleton } from './loading-skeleton'
import { ErrorBoundary } from './error-boundary'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { apiClient, getApiError } from '@/lib/api-client'
import { Task, CreateTaskRequest, UpdateTaskRequest } from '@/types'
import { TaskStatus } from '@/types'
import { cn } from '@/lib/utils'

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filterStatus, setFilterStatus] = useState<TaskStatus>('all')
  const [isCreating, setIsCreating] = useState(false)

  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await apiClient.getTasks(filterStatus)
      setTasks(data)
    } catch (err) {
      console.error('Error fetching tasks:', err)
      setError(getApiError(err))
    } finally {
      setLoading(false)
    }
  }, [filterStatus])

  useEffect(() => {
    fetchTasks()
  }, [fetchTasks])

  const createTask = async (taskData: CreateTaskRequest) => {
    setIsCreating(true)
    try {
      await apiClient.createTask(taskData)
      await fetchTasks() // Refresh the task list
      setIsCreating(false)
    } catch (err) {
      console.error('Error creating task:', err)
      setIsCreating(false)
      throw err
    }
  }

  const toggleTaskCompletion = async (taskId: number) => {
    try {
      const task = tasks.find(t => t.id === taskId)
      if (!task) return

      const newStatus = task.status === 'completed' ? 'pending' : 'completed'

      await apiClient.updateTask(taskId, {
        status: newStatus,
      })

      await fetchTasks() // Refresh the task list
    } catch (err) {
      console.error('Error updating task:', err)
      setError('Failed to update task. Please try again.')
    }
  }

  const deleteTask = async (taskId: number) => {
    if (typeof window !== 'undefined' && !window.confirm('Are you sure you want to delete this task?')) {
      return
    }

    try {
      await apiClient.deleteTask(taskId)
      await fetchTasks() // Refresh the task list
    } catch (err) {
      console.error('Error deleting task:', err)
      setError('Failed to delete task. Please try again.')
    }
  }

  const clearFilter = () => {
    setFilterStatus('all')
  }

  // Filter tasks based on status
  const filteredTasks = tasks.filter(task => {
    if (filterStatus === 'all') return true
    return task.status === filterStatus
  })

  const completedCount = tasks.filter(t => t.status === 'completed').length
  const pendingCount = tasks.filter(t => t.status === 'pending').length

  return (
    <ErrorBoundary>
      <div className={cn("space-y-12 pb-20")}>
        {/* Create Task Form */}
        <TaskForm
          onSubmit={createTask}
          isLoading={isCreating}
        />

        {/* Main Content Section */}
        <div className="space-y-8">
          {/* Header & Filters */}
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
            <div className="space-y-1">
              <h2 className="text-3xl font-black text-slate-900 tracking-tight flex items-center gap-3">
                Current Missions
                <span className="text-[10px] bg-slate-100 text-slate-400 px-2 py-1 rounded-lg uppercase tracking-[0.2em] font-bold">
                  {tasks.length} Total
                </span>
              </h2>
              <p className="text-sm font-bold text-slate-400 uppercase tracking-widest">
                Manage your daily objectives
              </p>
            </div>
            
            <TaskFilters
              currentFilter={filterStatus}
              onFilterChange={setFilterStatus}
            />
          </div>

          {/* Task Grid/List */}
          <div className="min-h-[400px]">
            {loading ? (
              <div className="space-y-4">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="h-32 bg-white/50 animate-pulse rounded-3xl border border-slate-100" />
                ))}
              </div>
            ) : error ? (
              <div className="glass p-12 text-center rounded-3xl border-red-100">
                <div className="w-16 h-16 bg-red-50 text-red-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <AlertCircle className="w-8 h-8" />
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">Sync Failed</h3>
                <p className="text-slate-500 font-medium mb-6">{error}</p>
                <button
                  onClick={fetchTasks}
                  className="px-6 py-2 bg-slate-900 text-white font-bold rounded-xl hover:bg-slate-800 transition-all"
                >
                  Retry Connection
                </button>
              </div>
            ) : filteredTasks.length === 0 ? (
              <div className="space-y-4">
                {tasks.length === 0 ? (
                  <NoTasksEmptyState
                    onCreateTask={() => document.querySelector('form')?.scrollIntoView({ behavior: 'smooth' })}
                  />
                ) : (
                  <NoFilteredTasksEmptyState
                    filter={filterStatus}
                    onClearFilter={clearFilter}
                    onCreateTask={() => {
                      if (filterStatus === 'completed') {
                        setFilterStatus('pending')
                      }
                      document.querySelector('form')?.scrollIntoView({ behavior: 'smooth' })
                    }}
                  />
                )}
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-4 animate-in fade-in duration-700">
                {filterStatus !== 'completed' && completedCount === tasks.length && tasks.length > 0 && (
                  <AllTasksCompletedEmptyState
                    onCreateTask={() => setFilterStatus('pending')}
                  />
                )}

                {filteredTasks.map((task) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onToggleComplete={toggleTaskCompletion}
                    onDelete={deleteTask}
                    className="animate-in slide-in-from-bottom-4 duration-500"
                  />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </ErrorBoundary>
  )
}

function AlertCircle({ className }: { className?: string }) {
  return (
    <svg 
      className={className} 
      xmlns="http://www.w3.org/2000/svg" 
      width="24" 
      height="24" 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="2" 
      strokeLinecap="round" 
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10"></circle>
      <line x1="12" y1="8" x2="12" y2="12"></line>
      <line x1="12" y1="16" x2="12.01" y2="16"></line>
    </svg>
  )
}