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
      <div className="container mx-auto px-4 py-8">
        <AuthForms onSuccess={() => setLoggedIn(true)} />
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