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
    <nav className="sticky top-4 z-50 px-4 mb-8">
      <div className="container mx-auto">
        <div className="glass rounded-2xl px-6 h-16 flex items-center justify-between shadow-lg shadow-indigo-100/50 border border-white/40">
          <div className="flex items-center space-x-10">
            <Link href="/" className="flex items-center space-x-2 group">
              <div className="w-9 h-9 bg-gradient-to-br from-indigo-600 to-violet-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-200 group-hover:scale-110 transition-transform">
                <ListTodo className="text-white w-5 h-5" />
              </div>
              <span className="text-xl font-black tracking-tight text-slate-900">
                Task<span className="text-indigo-600">Flow</span>
              </span>
            </Link>
            
            <div className="hidden md:flex items-center space-x-1">
              <Link 
                href="/" 
                className={`px-4 py-2 rounded-xl transition-all flex items-center space-x-2 text-sm font-bold ${
                  pathname === '/' 
                    ? 'text-indigo-600 bg-indigo-50/50' 
                    : 'text-slate-500 hover:text-indigo-600 hover:bg-indigo-50/30'
                }`}
              >
                <ListTodo className="w-4 h-4" />
                <span>Tasks</span>
              </Link>
              <Link 
                href="/chat" 
                className={`px-4 py-2 rounded-xl transition-all flex items-center space-x-2 text-sm font-bold ${
                  pathname === '/chat' 
                    ? 'text-indigo-600 bg-indigo-50/50' 
                    : 'text-slate-500 hover:text-indigo-600 hover:bg-indigo-50/30'
                }`}
              >
                <MessageSquare className="w-4 h-4" />
                <span>AI Assistant</span>
              </Link>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {user && (
              <div className="hidden sm:flex items-center space-x-3 bg-white/50 px-4 py-1.5 rounded-xl border border-slate-100 shadow-sm">
                <div className="w-7 h-7 bg-gradient-to-tr from-slate-200 to-slate-100 rounded-lg flex items-center justify-center border border-slate-200">
                  <UserIcon className="w-4 h-4 text-slate-500" />
                </div>
                <div className="flex flex-col">
                  <span className="text-[10px] font-black uppercase tracking-widest text-slate-400 leading-none mb-1">Authenticated</span>
                  <span className="text-xs font-bold text-slate-700 leading-none">{user.username}</span>
                </div>
              </div>
            )}
            <div className="h-8 w-[1px] bg-slate-200/60 mx-1 hidden sm:block"></div>
            <Button
              onClick={onLogout}
              variant="ghost"
              size="icon"
              className="rounded-xl text-slate-400 hover:text-red-600 hover:bg-red-50 transition-colors"
              title="Logout"
            >
              <LogOut className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
};