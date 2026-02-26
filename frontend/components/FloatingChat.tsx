'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Bot, X, Send, Sparkles, User as UserIcon, Loader2, MessageCircle } from 'lucide-react';
import { sendChatMessage } from '@/lib/chatapi';

interface FloatingChatProps {
  user: any;
}

export const FloatingChat: React.FC<FloatingChatProps> = ({ user }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isOpen]);

  const handleSend = async () => {
    if (!input.trim() || loading || !user?.id) return;

    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await sendChatMessage(user.id.toString(), userMsg.content);
      const assistantMsg = { role: 'assistant', content: response.response };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I'm having trouble connecting right now." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed bottom-8 right-8 z-[100]">
      {/* Toggle Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="w-16 h-16 bg-[#1D1D1F] text-white rounded-full flex items-center justify-center shadow-2xl hover:scale-110 active:scale-95 transition-all duration-300 group relative"
        >
          <div className="absolute -top-1 -right-1 w-4 h-4 bg-indigo-500 rounded-full animate-pulse border-2 border-white"></div>
          <MessageCircle className="w-7 h-7" />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="w-[380px] h-[550px] apple-glass rounded-[2rem] shadow-[0_20px_60px_-15px_rgba(0,0,0,0.15)] flex flex-col overflow-hidden animate-in zoom-in-95 fade-in duration-300">
          {/* Header */}
          <div className="p-6 bg-[#1D1D1F] text-white flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-indigo-500 rounded-xl flex items-center justify-center">
                <Bot className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="font-bold tracking-tight">AI Assistant</h3>
                <div className="flex items-center text-[10px] text-indigo-300 font-bold uppercase tracking-widest">
                  <span className="w-1.5 h-1.5 bg-green-400 rounded-full mr-1.5"></span>
                  Online
                </div>
              </div>
            </div>
            <button 
              onClick={() => setIsOpen(false)}
              className="p-2 hover:bg-white/10 rounded-full transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages */}
          <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar">
            {messages.length === 0 && (
              <div className="text-center py-10 space-y-4">
                <div className="w-16 h-16 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mx-auto">
                  <Sparkles className="w-8 h-8" />
                </div>
                <p className="text-sm font-bold text-slate-400 uppercase tracking-widest px-4">
                  How can I help you manage your missions today, {user?.username}?
                </p>
              </div>
            )}
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] p-4 rounded-[1.5rem] font-medium text-sm ${
                  m.role === 'user' 
                    ? 'bg-indigo-600 text-white rounded-tr-none' 
                    : 'bg-white border border-slate-100 text-[#1D1D1F] rounded-tl-none shadow-sm'
                }`}>
                  {m.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-white border border-slate-100 p-4 rounded-[1.5rem] rounded-tl-none shadow-sm">
                  <Loader2 className="w-4 h-4 animate-spin text-indigo-500" />
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="p-6 bg-white border-t border-slate-50">
            <div className="relative flex items-center">
              <input
                type="text"
                placeholder="Message AI..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                className="w-full pl-5 pr-12 py-4 bg-[#F5F5F7] border-none rounded-2xl focus:ring-2 focus:ring-indigo-500/20 outline-none text-sm font-bold placeholder:text-slate-400 transition-all"
              />
              <button 
                onClick={handleSend}
                disabled={!input.trim() || loading}
                className="absolute right-2 p-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:bg-slate-200 transition-all shadow-lg shadow-indigo-100"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
