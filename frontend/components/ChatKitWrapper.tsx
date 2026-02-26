'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useChat } from '../contexts/ChatContext';
import { sendChatMessage, getConversationHistory, getUserConversations } from '../lib/chatapi';
import { authClient } from '../lib/auth';
import { 
  MessageSquare, 
  PlusCircle, 
  Send, 
  Bot, 
  User as UserIcon, 
  Clock, 
  Hash,
  ChevronRight,
  MoreVertical,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: string;
  actions_taken?: string[];
}

interface Conversation {
  id: string;
  title: string | null;
  created_at: string;
  updated_at: string;
}

const ChatKitWrapper: React.FC = () => {
  const [user, setUser] = useState<any>(null);
  const { state, dispatch } = useChat();
  const [inputValue, setInputValue] = useState<string>('');
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  // Load user on mount
  useEffect(() => {
    const currentUser = authClient.getUser();
    setUser(currentUser);
  }, []);

  const loadConversations = React.useCallback(async () => {
    if (!user?.id) return;

    try {
      const userConversations = await getUserConversations(user.id.toString());
      // Sort by updated_at descending
      const sorted = userConversations.sort((a: any, b: any) => 
        new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
      );
      setConversations(sorted);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  }, [user?.id]);

  // Load user conversations when user is available
  useEffect(() => {
    if (user?.id) {
      loadConversations();
    }
  }, [user?.id, loadConversations]);

  const loadConversation = async (convId: string) => {
    if (!user?.id) return;

    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const history = await getConversationHistory(user.id.toString(), convId);

      // Transform the history to our internal format
      const transformedMessages: Message[] = history.messages.map((msg: any) => ({
        id: msg.id,
        content: msg.content,
        sender: msg.sender_type === 'user' ? 'user' : 'assistant',
        timestamp: msg.timestamp,
        actions_taken: msg.tool_used ? [msg.tool_used] : []
      }));

      dispatch({ type: 'SET_MESSAGES', payload: transformedMessages });
      dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: convId });
    } catch (error) {
      console.error('Failed to load conversation:', error);
      dispatch({ type: 'SET_ERROR', payload: 'Failed to load conversation' });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || state.isLoading || !user?.id) return;

    const userMessageContent = inputValue;
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      content: userMessageContent,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    // Add user message to UI immediately
    dispatch({ type: 'ADD_MESSAGE', payload: userMessage });
    setInputValue('');
    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      const response = await sendChatMessage(
        user.id.toString(),
        userMessageContent,
        state.currentConversationId || undefined
      );

      const assistantMessage: Message = {
        id: response.message_id,
        content: response.response,
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        actions_taken: response.actions_taken
      };

      dispatch({ type: 'ADD_MESSAGE', payload: assistantMessage });
      dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: response.conversation_id });

      // Refresh conversations list to update titles/previews
      loadConversations();
    } catch (error: any) {
      console.error('Failed to send message:', error);

      const errorText = error.response?.data?.detail || 'I encountered an issue connecting to my AI core. Please check your API key and try again.';
      
      // Add error message to UI
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        content: `Error: ${errorText}`,
        sender: 'assistant',
        timestamp: new Date().toISOString()
      };
      dispatch({ type: 'ADD_MESSAGE', payload: errorMessage });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const startNewConversation = () => {
    dispatch({ type: 'CLEAR_MESSAGES' });
    dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: null });
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    const now = new Date();
    if (date.toDateString() === now.toDateString()) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
  };

  return (
    <div className="flex h-[700px] bg-white rounded-2xl shadow-2xl overflow-hidden border border-slate-200/60 backdrop-blur-xl">
      {/* Premium Sidebar */}
      <div className={`flex flex-col bg-slate-50/50 border-r border-slate-200/60 transition-all duration-300 ease-in-out ${isSidebarOpen ? 'w-72' : 'w-0'}`}>
        <div className="p-6 border-b border-slate-200/60 flex items-center justify-between bg-white/50">
          <h3 className="text-sm font-bold text-slate-900 tracking-tight flex items-center">
            <Clock className="w-4 h-4 mr-2 text-blue-500" />
            Recent Chats
          </h3>
          <button 
            onClick={startNewConversation}
            className="p-1.5 hover:bg-white hover:shadow-sm rounded-lg transition-all text-blue-600"
          >
            <PlusCircle className="w-5 h-5" />
          </button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-3 space-y-1 custom-scrollbar">
          {conversations.length === 0 ? (
            <div className="py-10 px-4 text-center">
              <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <Hash className="w-6 h-6 text-slate-300" />
              </div>
              <p className="text-slate-400 text-xs font-medium">No previous chats</p>
            </div>
          ) : (
            conversations.map(conv => (
              <button
                key={conv.id}
                onClick={() => loadConversation(conv.id)}
                className={`w-full group text-left p-3.5 rounded-xl transition-all relative flex items-center space-x-3 ${
                  state.currentConversationId === conv.id 
                    ? 'bg-white shadow-md shadow-slate-200/50 border border-slate-200/60' 
                    : 'hover:bg-white/80 text-slate-600'
                }`}
              >
                <div className={`w-2 h-2 rounded-full transition-all ${
                  state.currentConversationId === conv.id ? 'bg-blue-500 scale-125' : 'bg-slate-300 group-hover:bg-slate-400'
                }`} />
                <div className="flex-1 min-w-0">
                  <p className={`text-sm font-semibold truncate ${
                    state.currentConversationId === conv.id ? 'text-slate-900' : 'text-slate-600'
                  }`}>
                    {conv.title || 'New Conversation'}
                  </p>
                  <p className="text-[10px] text-slate-400 mt-0.5 font-medium uppercase tracking-wider">
                    {formatDate(conv.updated_at)}
                  </p>
                </div>
                <ChevronRight className={`w-4 h-4 transition-all ${
                  state.currentConversationId === conv.id ? 'text-blue-500 opacity-100' : 'text-slate-300 opacity-0 group-hover:opacity-100'
                }`} />
              </button>
            ))
          )}
        </div>
      </div>

      {/* Main Chat Interface */}
      <div className="flex-1 flex flex-col relative bg-white">
        {/* Modern Header */}
        <header className="h-16 border-b border-slate-100/80 flex items-center justify-between px-6 z-10 bg-white/80 backdrop-blur-md">
          <div className="flex items-center space-x-4">
            <button 
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 hover:bg-slate-50 rounded-lg text-slate-400 md:hidden"
            >
              <MoreVertical className="w-5 h-5" />
            </button>
            <div className="flex items-center">
              <div className="w-9 h-9 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-200 ring-4 ring-blue-50">
                <Bot className="text-white w-5 h-5" />
              </div>
              <div className="ml-3">
                <h2 className="text-sm font-bold text-slate-900 leading-none">AI Agent</h2>
                <div className="flex items-center mt-1">
                  <span className="w-1.5 h-1.5 bg-green-500 rounded-full mr-1.5 animate-pulse"></span>
                  <span className="text-[10px] font-bold text-green-600 uppercase tracking-widest">Active</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <div className="hidden sm:flex flex-col items-end mr-2">
              <span className="text-[10px] text-slate-400 font-bold uppercase tracking-tight">System Status</span>
              <span className="text-[11px] text-slate-900 font-bold tracking-tight">Operational</span>
            </div>
            <div className="w-8 h-8 bg-slate-50 rounded-full border border-slate-100 flex items-center justify-center">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            </div>
          </div>
        </header>

        {/* Messages Feed */}
        <div className="flex-1 overflow-y-auto p-6 md:p-10 space-y-8 custom-scrollbar bg-gradient-to-b from-white to-slate-50/30">
          {state.messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center animate-in fade-in zoom-in duration-500">
              <div className="w-20 h-20 bg-blue-50 rounded-3xl flex items-center justify-center mb-6 ring-8 ring-blue-50/50">
                <MessageSquare className="w-10 h-10 text-blue-600" />
              </div>
              <h3 className="text-2xl font-black text-slate-900 mb-2 tracking-tight">How can I help you today?</h3>
              <p className="text-slate-500 text-sm max-w-sm font-medium leading-relaxed">
                I&apos;m your intelligent task assistant. Ask me to list your todos, add new tasks, or mark them as complete.
              </p>
              <div className="mt-8 flex flex-wrap justify-center gap-2">
                {['List my tasks', 'Add a task to buy groceries', 'What\'s pending?'].map((suggestion) => (
                  <button 
                    key={suggestion}
                    onClick={() => setInputValue(suggestion)}
                    className="px-4 py-2 bg-white border border-slate-200 rounded-full text-xs font-semibold text-slate-600 hover:border-blue-400 hover:text-blue-600 transition-all shadow-sm"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="max-w-3xl mx-auto w-full">
              {state.messages.map((message, idx) => (
                <div
                  key={message.id}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} mb-8 animate-in slide-in-from-bottom-4 duration-300 fill-mode-both`}
                  style={{ animationDelay: `${idx * 50}ms` }}
                >
                  <div className={`flex items-start max-w-[85%] ${message.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                    <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-1 ${
                      message.sender === 'user' ? 'ml-3 bg-slate-100' : 'mr-3 bg-blue-100'
                    }`}>
                      {message.sender === 'user' ? <UserIcon className="w-4 h-4 text-slate-500" /> : <Bot className="w-4 h-4 text-blue-600" />}
                    </div>
                    
                    <div>
                      <div className={`p-4 shadow-sm ${
                        message.sender === 'user'
                          ? 'bg-slate-900 text-white rounded-2xl rounded-tr-none'
                          : 'bg-white border border-slate-200/80 text-slate-800 rounded-2xl rounded-tl-none'
                      }`}>
                        <div className="text-[15px] leading-relaxed whitespace-pre-wrap font-medium">
                          {message.content}
                        </div>
                        
                        {/* Action Badges */}
                        {message.actions_taken && message.actions_taken.length > 0 && (
                          <div className="mt-3 pt-3 border-t border-slate-100 flex flex-wrap gap-2">
                            {message.actions_taken.map((action, i) => (
                              <div key={i} className="flex items-center bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-widest ring-1 ring-blue-100">
                                <CheckCircle2 className="w-3 h-3 mr-1" />
                                {action.replace('Action: ', '')}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                      <div className={`text-[10px] mt-2 font-bold uppercase tracking-widest text-slate-400 ${
                        message.sender === 'user' ? 'text-right' : 'text-left'
                      }`}>
                        {new Date(message.timestamp).toLocaleTimeString([], {
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              
              {state.isLoading && (
                <div className="flex justify-start mb-8 animate-in fade-in duration-300">
                  <div className="flex items-start max-w-[85%]">
                    <div className="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0 mt-1 mr-3 ring-4 ring-blue-50">
                      <Bot className="w-4 h-4 text-blue-600" />
                    </div>
                    <div className="bg-white border border-slate-200/80 p-4 rounded-2xl rounded-tl-none shadow-sm">
                      <div className="flex space-x-1.5 h-5 items-center">
                        <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce [animation-duration:0.8s]"></div>
                        <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce [animation-duration:0.8s] [animation-delay:0.2s]"></div>
                        <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce [animation-duration:0.8s] [animation-delay:0.4s]"></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Premium Input Bar */}
        <div className="p-6 bg-white border-t border-slate-100/80">
          <div className="max-w-3xl mx-auto relative">
            <div className="relative flex items-end group">
              <div className="absolute left-4 bottom-4 text-slate-400 group-focus-within:text-blue-500 transition-colors">
                <Hash className="w-5 h-5" />
              </div>
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask your assistant anything..."
                className="w-full bg-slate-50 border border-slate-200 rounded-2xl pl-12 pr-16 py-4 resize-none max-h-32 text-[15px] font-medium focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500/50 focus:bg-white outline-none transition-all placeholder:text-slate-400 custom-scrollbar shadow-inner"
                rows={1}
                disabled={state.isLoading}
              />
              <button
                onClick={handleSendMessage}
                disabled={state.isLoading || !inputValue.trim()}
                className={`absolute right-2 bottom-2 p-2.5 rounded-xl transition-all ${
                  state.isLoading || !inputValue.trim()
                    ? 'bg-slate-100 text-slate-300'
                    : 'bg-blue-600 text-white hover:bg-blue-700 shadow-lg shadow-blue-200 hover:scale-105 active:scale-95'
                }`}
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
            <p className="mt-3 text-[10px] text-center font-bold text-slate-400 uppercase tracking-widest">
              Powered by Google Gemini 1.5 Flash • MCP Enabled
            </p>
          </div>
        </div>
      </div>

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #e2e8f0;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #cbd5e1;
        }
      `}</style>
    </div>
  );
};

export default ChatKitWrapper;