'use client';

import { useRouter } from 'next/navigation';
import { ChatProvider } from '../../contexts/ChatContext';
import ChatKitWrapper from '../../components/ChatKitWrapper';
import { useEffect, useState } from 'react';
import { authClient } from '../../lib/auth';

export default function ChatPage() {
  const router = useRouter();
  const [status, setStatus] = useState<'loading' | 'authenticated' | 'unauthenticated'>('loading');

  useEffect(() => {
    // Check authentication on mount
    const checkAuth = () => {
      const isAuthenticated = authClient.isAuthenticated();
      if (!isAuthenticated) {
        setStatus('unauthenticated');
        router.push('/login');
      } else {
        setStatus('authenticated');
      }
    };
    checkAuth();
  }, [router]);

  if (status === 'loading') {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (status === 'unauthenticated') {
    return null; // Redirect happens in useEffect
  }

  return (
    <ChatProvider>
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <ChatKitWrapper />
          </div>
        </div>
      </div>
    </ChatProvider>
  );
}