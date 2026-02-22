'use client'

import { useState, useEffect } from 'react'
import { TaskList } from '@/components/task-list'
import { AuthForms } from '@/components/auth-forms'
import { authClient } from '@/lib/auth'
import { User } from '@/types'
import { Navigation } from '@/components/Navigation'

export default function Home() {
  const [loggedIn, setLoggedIn] = useState(authClient.isAuthenticated())
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    if (loggedIn) {
      const fetchUser = async () => {
        const currentUser = await authClient.getCurrentUser()
        setUser(currentUser)
      }
      fetchUser()
    }
  }, [loggedIn])

  const handleLogout = () => {
    authClient.logout()
    setLoggedIn(false)
    setUser(null)
  }

  if (!loggedIn) {
    return <AuthForms onSuccess={() => setLoggedIn(true)} />
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <Navigation user={user || undefined} onLogout={handleLogout} />
      <TaskList />
    </div>
  )
}