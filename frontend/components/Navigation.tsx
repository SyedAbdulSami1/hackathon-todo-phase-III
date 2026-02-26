'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from './ui/button';
import { MessageSquare, ListTodo, LogOut, User as UserIcon } from 'lucide-react';

interface NavigationProps {
  user?: {
    username: string;
  };
  onLogout: () => void;
}

export const Navigation: React.FC<NavigationProps> = ({ user, onLogout }) => {
  const pathname = usePathname();

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm mb-8">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-8">
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <ListTodo className="text-white w-5 h-5" />
            </div>
            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
              TaskFlow
            </span>
          </Link>
          
          <div className="hidden md:flex items-center space-x-1">
            <Link 
              href="/" 
              className={`px-4 py-2 rounded-lg transition-all flex items-center space-x-2 ${
                pathname === '/' ? 'text-blue-600 bg-blue-50 font-medium' : 'text-slate-600 hover:text-blue-600 hover:bg-blue-50'
              }`}
            >
              <ListTodo className="w-4 h-4" />
              <span>Tasks</span>
            </Link>
            <Link 
              href="/chat" 
              className={`px-4 py-2 rounded-lg transition-all flex items-center space-x-2 ${
                pathname === '/chat' ? 'text-blue-600 bg-blue-50 font-medium' : 'text-slate-600 hover:text-blue-600 hover:bg-blue-50'
              }`}
            >
              <MessageSquare className="w-4 h-4" />
              <span>AI Assistant</span>
            </Link>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {user && (
            <div className="flex items-center space-x-3 bg-slate-50 px-3 py-1.5 rounded-full border border-slate-200">
              <div className="w-6 h-6 bg-slate-200 rounded-full flex items-center justify-center">
                <UserIcon className="w-4 h-4 text-slate-500" />
              </div>
              <span className="text-sm font-medium text-slate-700">{user.username}</span>
            </div>
          )}
          <Button
            onClick={onLogout}
            variant="ghost"
            size="icon"
            className="text-slate-400 hover:text-red-600 hover:bg-red-50"
            title="Logout"
          >
            <LogOut className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </nav>
  );
};