/** Tests for the chat API client */

import { sendChatMessage, getConversationHistory, getUserConversations } from '../lib/chat-api';

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
};
global.localStorage = localStorageMock;

// Mock fetch
const mockFetch = jest.fn();
(global as any).fetch = mockFetch;

describe('Chat API Client', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorageMock.getItem.mockReturnValue('test-token');
  });

  describe('sendChatMessage', () => {
    it('should send a chat message successfully', async () => {
      const mockResponse = {
        response: 'Test response',
        conversation_id: 'test-conv-id',
        message_id: 'test-msg-id',
        tool_used: 'test-tool',
        actions_taken: ['action1'],
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await sendChatMessage('user123', 'Hello, world!');

      expect(mockFetch).toHaveBeenCalledWith(
        `${process.env.API_BASE_URL || 'http://localhost:8000'}/api/user123/chat`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-token',
          },
          body: JSON.stringify({
            message: 'Hello, world!',
            conversation_id: undefined,
          }),
        }
      );

      expect(result).toEqual(mockResponse);
    });

    it('should send a chat message with conversation ID', async () => {
      const mockResponse = {
        response: 'Test response',
        conversation_id: 'test-conv-id',
        message_id: 'test-msg-id',
        tool_used: null,
        actions_taken: [],
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await sendChatMessage('user123', 'Hello!', 'existing-conv-id');

      expect(mockFetch).toHaveBeenCalledWith(
        `${process.env.API_BASE_URL || 'http://localhost:8000'}/api/user123/chat`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-token',
          },
          body: JSON.stringify({
            message: 'Hello!',
            conversation_id: 'existing-conv-id',
          }),
        }
      );

      expect(result).toEqual(mockResponse);
    });

    it('should throw an error on API failure', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        statusText: 'Not Found',
      });

      await expect(sendChatMessage('user123', 'Hello!')).rejects.toThrow('Chat API error: Not Found');
    });
  });

  describe('getConversationHistory', () => {
    it('should fetch conversation history successfully', async () => {
      const mockHistory = {
        conversation_id: 'test-conv-id',
        messages: [
          { id: 'msg1', content: 'Hello', sender_type: 'user', timestamp: '2023-01-01T00:00:00Z' },
        ],
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockHistory,
      });

      const result = await getConversationHistory('user123', 'test-conv-id');

      expect(mockFetch).toHaveBeenCalledWith(
        `${process.env.API_BASE_URL || 'http://localhost:8000'}/api/user123/conversations/test-conv-id`,
        {
          headers: {
            'Authorization': 'Bearer test-token',
          },
        }
      );

      expect(result).toEqual(mockHistory);
    });

    it('should throw an error when fetching conversation history fails', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        statusText: 'Forbidden',
      });

      await expect(getConversationHistory('user123', 'test-conv-id')).rejects.toThrow(
        'Failed to get conversation history: Forbidden'
      );
    });
  });

  describe('getUserConversations', () => {
    it('should fetch user conversations successfully', async () => {
      const mockConversations = [
        { id: 'conv1', title: 'Test Conversation', created_at: '2023-01-01T00:00:00Z', updated_at: '2023-01-01T00:00:00Z' },
      ];

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockConversations,
      });

      const result = await getUserConversations('user123');

      expect(mockFetch).toHaveBeenCalledWith(
        `${process.env.API_BASE_URL || 'http://localhost:8000'}/api/user123/conversations`,
        {
          headers: {
            'Authorization': 'Bearer test-token',
          },
        }
      );

      expect(result).toEqual(mockConversations);
    });

    it('should throw an error when fetching user conversations fails', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        statusText: 'Unauthorized',
      });

      await expect(getUserConversations('user123')).rejects.toThrow(
        'Failed to get user conversations: Unauthorized'
      );
    });
  });
});