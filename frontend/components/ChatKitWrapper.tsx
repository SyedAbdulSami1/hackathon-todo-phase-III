'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useChat } from '../contexts/ChatContext';
import { sendChatMessage, getConversationHistory, getUserConversations } from '../lib/chat-api';
import { authClient } from '../lib/auth';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: string;
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

  // Load user on mount
  useEffect(() => {
    const currentUser = authClient.getUser();
    setUser(currentUser);
  }, []);

  // Load user conversations when user is available
  useEffect(() => {
    if (user?.id) {
      loadConversations();
    }
  }, [user]);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [state.messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversations = async () => {
    if (!user?.id) return;

    try {
      const userConversations = await getUserConversations(user.id.toString());
      setConversations(userConversations);
    } catch (error) {
      console.error('Failed to load conversations:', error);
    }
  };

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
        timestamp: msg.timestamp
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

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
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
        inputValue,
        state.currentConversationId || undefined
      );

      const assistantMessage: Message = {
        id: response.message_id,
        content: response.response,
        sender: 'assistant',
        timestamp: new Date().toISOString()
      };

      dispatch({ type: 'ADD_MESSAGE', payload: assistantMessage });
      dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: response.conversation_id });

      // Add to conversations list if it's a new conversation
      if (!conversations.some(c => c.id === response.conversation_id)) {
        loadConversations(); // Refresh the list
      }
    } catch (error) {
      console.error('Failed to send message:', error);

      // Add error message to UI
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        content: 'Sorry, I encountered an error processing your request. Please try again.',
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

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Header */}
      <div className="bg-white border-b p-4 flex justify-between items-center">
        <h2 className="text-xl font-bold">AI Chat Assistant</h2>
        <button
          onClick={startNewConversation}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
        >
          New Chat
        </button>
      </div>

      {/* Sidebar - Conversations List */}
      <div className="hidden md:flex flex-col w-64 bg-gray-50 border-r p-4 overflow-y-auto">
        <h3 className="font-semibold mb-2">Your Conversations</h3>
        {conversations.length === 0 ? (
          <p className="text-gray-500 text-sm">No conversations yet</p>
        ) : (
          <ul className="space-y-1">
            {conversations.map(conv => (
              <li key={conv.id}>
                <button
                  onClick={() => loadConversation(conv.id)}
                  className={`w-full text-left p-2 rounded hover:bg-gray-100 truncate ${
                    state.currentConversationId === conv.id ? 'bg-blue-100' : ''
                  }`}
                >
                  {conv.title || `Chat ${new Date(conv.created_at).toLocaleDateString()}`}
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
          {state.messages.length === 0 ? (
            <div className="h-full flex items-center justify-center">
              <div className="text-center text-gray-500">
                <p className="text-lg mb-2">Start a conversation with the AI assistant</p>
                <p className="text-sm">Ask me to help you manage your tasks!</p>
              </div>
            </div>
          ) : (
            <div className="space-y-4 max-w-3xl mx-auto">
              {state.messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-2 ${
                      message.sender === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-white border'
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{message.content}</div>
                    <div
                      className={`text-xs mt-1 ${
                        message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'
                      }`}
                    >
                      {new Date(message.timestamp).toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </div>
                  </div>
                </div>
              ))}
              {state.isLoading && (
                <div className="flex justify-start">
                  <div className="bg-white border rounded-lg px-4 py-2 max-w-[80%]">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-75"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="border-t bg-white p-4">
          <div className="flex max-w-3xl mx-auto">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message here..."
              className="flex-1 border rounded-l-lg p-3 resize-none h-16 focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={state.isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={state.isLoading || !inputValue.trim()}
              className={`px-6 rounded-r-lg ${
                state.isLoading || !inputValue.trim()
                  ? 'bg-gray-300 text-gray-500'
                  : 'bg-blue-500 text-white hover:bg-blue-600'
              }`}
            >
              Send
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2 text-center">
            Ask me to create, update, or manage your tasks!
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatKitWrapper;