'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
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
    <nav className="sticky top-0 z-50 w-full px-4 h-20 apple-glass flex items-center shadow-sm">
      <div className="section-container w-full flex items-center justify-between">
        <div className="flex items-center space-x-12">
          <Link href="/" className="flex items-center space-x-2 group">
            <div className="w-10 h-10 bg-[#1D1D1F] rounded-xl flex items-center justify-center shadow-lg group-hover:scale-110 transition-all">
              <ListTodo className="text-white w-6 h-6" />
            </div>
            <span className="text-2xl font-bold tracking-tight text-[#1D1D1F]">
              Task<span className="text-indigo-600">Flow</span>
            </span>
          </Link>
          
          <div className="hidden md:flex items-center space-x-2">
            <Link 
              href="/" 
              className={`px-5 py-2.5 rounded-full transition-all text-sm font-bold ${
                pathname === '/' 
                  ? 'bg-[#1D1D1F] text-white shadow-xl' 
                  : 'text-slate-500 hover:text-[#1D1D1F] hover:bg-slate-100'
              }`}
            >
              <span>Dashboard</span>
            </Link>
            <Link 
              href="/chat" 
              className={`px-5 py-2.5 rounded-full transition-all text-sm font-bold ${
                pathname === '/chat' 
                  ? 'bg-[#1D1D1F] text-white shadow-xl' 
                  : 'text-slate-500 hover:text-[#1D1D1F] hover:bg-slate-100'
              }`}
            >
              <span>AI Chat</span>
            </Link>
          </div>
        </div>

        <div className="flex items-center space-x-6">
          {user && (
            <div className="hidden sm:flex items-center space-x-3 bg-white px-4 py-2 rounded-full border border-slate-100 shadow-sm">
              <div className="w-7 h-7 bg-slate-50 rounded-lg flex items-center justify-center border border-slate-100">
                <UserIcon className="w-4 h-4 text-slate-500" />
              </div>
              <div className="flex flex-col">
                <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400 leading-none mb-1">Founder</span>
                <span className="text-xs font-bold text-slate-700 leading-none">{user.username}</span>
              </div>
            </div>
          )}
          <button
            onClick={onLogout}
            className="p-2.5 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-all"
            title="Logout"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </div>
    </nav>
  );
};
