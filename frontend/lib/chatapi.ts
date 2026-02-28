/** API client for chat functionality */

// On Vercel, if NEXT_PUBLIC_API_URL is not set, we prefer relative paths
const getBaseUrl = () => {
  if (process.env.NEXT_PUBLIC_API_URL) return process.env.NEXT_PUBLIC_API_URL;
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    if (hostname === 'localhost' || hostname === '127.0.0.1') return 'http://localhost:8000';
    return '';
  }
  return 'http://localhost:8000';
}
const API_BASE_URL = getBaseUrl();

interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
  message_id: string;
  tool_used: string | null;
  actions_taken: string[];
}

/**
 * Send a chat message to the backend
 */
export const sendChatMessage = async (
  userId: string,
  message: string,
  conversationId?: string
): Promise<ChatResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('auth_token')}` // Assuming token is stored
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId
    })
  });

  if (!response.ok) {
    throw new Error(`Chat API error: ${response.statusText}`);
  }

  return response.json();
};

/**
 * Get conversation history
 */
export const getConversationHistory = async (
  userId: string,
  conversationId: string
): Promise<{
  conversation_id: string;
  messages: ChatMessage[];
}> => {
  const response = await fetch(`${API_BASE_URL}/api/${userId}/conversations/${conversationId}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
    }
  });

  if (!response.ok) {
    throw new Error(`Failed to get conversation history: ${response.statusText}`);
  }

  return response.json();
};

/**
 * Get user's conversations
 */
export const getUserConversations = async (
  userId: string
): Promise<Array<{
  id: string;
  title: string | null;
  created_at: string;
  updated_at: string;
}>> => {
  const response = await fetch(`${API_BASE_URL}/api/${userId}/conversations`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
    }
  });

  if (!response.ok) {
    throw new Error(`Failed to get user conversations: ${response.statusText}`);
  }

  return response.json();
};
