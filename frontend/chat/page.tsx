'use client';

import { useRouter } from 'next/navigation';
import { ChatProvider } from '../../contexts/ChatContext';
import ChatKitWrapper from '../../components/ChatKitWrapper';
import { useEffect, useState } from 'react';
import { authClient } from '../../lib/auth';
import { Navigation } from '../../components/Navigation';
import { User } from '../../types';

export default function ChatPage() {
  const router = useRouter();
  const [status, setStatus] = useState<'loading' | 'authenticated' | 'unauthenticated'>('loading');
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const checkAuth = () => {
      const isAuthenticated = authClient.isAuthenticated();
      if (!isAuthenticated) {
        setStatus('unauthenticated');
        router.push('/');
      } else {
        const currentUser = authClient.getUser();
        setUser(currentUser);
        setStatus('authenticated');
      }
    };
    checkAuth();
  }, [router]);

  const handleLogout = () => {
    authClient.logout();
    router.push('/');
  };

  if (status === 'loading') {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (status === 'unauthenticated') {
    return null;
  }

  return (
    <ChatProvider>
      <div className="min-h-screen bg-gray-50">
        <Navigation user={user || undefined} onLogout={handleLogout} />
        <div className="container mx-auto px-4 pb-8">
          <div className="bg-white rounded-xl shadow-md overflow-hidden border border-slate-200">
            <ChatKitWrapper />
          </div>
        </div>
      </div>
    </ChatProvider>
  );
}