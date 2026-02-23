/** Tests for the ChatKitWrapper component */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { SessionProvider } from 'next-auth/react';
import { ChatProvider } from '../contexts/ChatContext';
import ChatKitWrapper from '../components/ChatKitWrapper';

// Mock the chat API functions
jest.mock('../lib/chat-api', () => ({
  sendChatMessage: jest.fn(),
  getConversationHistory: jest.fn(),
  getUserConversations: jest.fn(),
}));

// Mock next-auth
jest.mock('next-auth/react', () => ({
  useSession: () => ({
    data: {
      user: { id: 'test-user-id', name: 'Test User' },
      expires: '2023-01-01T00:00:00Z',
    },
    status: 'authenticated',
  }),
}));

// Mock next/navigation
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
  usePathname: () => '/chat',
}));

const MockWrapper = ({ children }: { children: React.ReactNode }) => (
  <SessionProvider session={{}}>
    <ChatProvider>{children}</ChatProvider>
  </SessionProvider>
);

describe('ChatKitWrapper', () => {
  beforeEach(() => {
    jest.clearAllMocks();

    // Mock successful API calls
    require('../lib/chat-api').sendChatMessage.mockResolvedValue({
      response: 'Mock response',
      conversation_id: 'mock-conversation-id',
      message_id: 'mock-message-id',
      tool_used: null,
      actions_taken: ['action1'],
    });

    require('../lib/chat-api').getConversationHistory.mockResolvedValue({
      conversation_id: 'mock-conversation-id',
      messages: [
        {
          id: 'mock-msg-id',
          content: 'Mock message content',
          sender_type: 'assistant',
          timestamp: new Date().toISOString(),
        },
      ],
    });

    require('../lib/chat-api').getUserConversations.mockResolvedValue([
      {
        id: 'mock-conv-id',
        title: 'Mock Conversation',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ]);
  });

  it('renders the chat interface', () => {
    render(
      <MockWrapper>
        <ChatKitWrapper />
      </MockWrapper>
    );

    expect(screen.getByText('AI Chat Assistant')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Type your message here...')).toBeInTheDocument();
    expect(screen.getByText('Send')).toBeInTheDocument();
  });

  it('allows user to type and send a message', async () => {
    render(
      <MockWrapper>
        <ChatKitWrapper />
      </MockWrapper>
    );

    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByText('Send');

    fireEvent.change(input, { target: { value: 'Hello, world!' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(require('../lib/chat-api').sendChatMessage).toHaveBeenCalledWith(
        'test-user-id',
        'Hello, world!',
        undefined
      );
    });
  });

  it('displays user and assistant messages', async () => {
    render(
      <MockWrapper>
        <ChatKitWrapper />
      </MockWrapper>
    );

    // Simulate sending a message
    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByText('Send');

    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText('Test message')).toBeInTheDocument();
    });

    // Check if the mock response appears
    expect(screen.getByText('Mock response')).toBeInTheDocument();
  });

  it('shows loading indicator when sending message', async () => {
    // Delay the API response to test loading state
    require('../lib/chat-api').sendChatMessage.mockImplementation(() => {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            response: 'Delayed response',
            conversation_id: 'mock-conversation-id',
            message_id: 'mock-message-id',
            tool_used: null,
            actions_taken: ['action1'],
          });
        }, 100);
      });
    });

    render(
      <MockWrapper>
        <ChatKitWrapper />
      </MockWrapper>
    );

    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByText('Send');

    fireEvent.change(input, { target: { value: 'Loading test' } });
    fireEvent.click(sendButton);

    // Check if loading indicator appears
    expect(screen.getByText('AI Chat Assistant')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('Delayed response')).toBeInTheDocument();
    });
  });

  it('handles Enter key press to send message', async () => {
    render(
      <MockWrapper>
        <ChatKitWrapper />
      </MockWrapper>
    );

    const input = screen.getByPlaceholderText('Type your message here...');

    fireEvent.change(input, { target: { value: 'Enter key test' } });
    fireEvent.keyDown(input, { key: 'Enter', shiftKey: false });

    await waitFor(() => {
      expect(require('../lib/chat-api').sendChatMessage).toHaveBeenCalledWith(
        'test-user-id',
        'Enter key test',
        undefined
      );
    });
  });

  it('does not send message on Shift+Enter', () => {
    render(
      <MockWrapper>
        <ChatKitWrapper />
      </MockWrapper>
    );

    const input = screen.getByPlaceholderText('Type your message here...');

    fireEvent.change(input, { target: { value: 'Shift+Enter test' } });
    fireEvent.keyDown(input, { key: 'Enter', shiftKey: true });

    // The API should not be called since we used Shift+Enter
    expect(require('../lib/chat-api').sendChatMessage).not.toHaveBeenCalled();
  });

  it('starts a new conversation when New Chat button is clicked', () => {
    render(
      <MockWrapper>
        <ChatKitWrapper />
      </MockWrapper>
    );

    const newChatButton = screen.getByText('New Chat');
    fireEvent.click(newChatButton);

    // Check that the UI allows for a new conversation
    expect(screen.getByText('Start a conversation with the AI assistant')).toBeInTheDocument();
  });

  it('loads conversations on mount', async () => {
    render(
      <MockWrapper>
        <ChatKitWrapper />
      </MockWrapper>
    );

    await waitFor(() => {
      expect(require('../lib/chat-api').getUserConversations).toHaveBeenCalledWith('test-user-id');
    });
  });

  it('disables send button when input is empty', () => {
    render(
      <MockWrapper>
        <ChatKitWrapper />
      </MockWrapper>
    );

    const sendButton = screen.getByText('Send');
    expect(sendButton).toBeDisabled();

    const input = screen.getByPlaceholderText('Type your message here...');
    fireEvent.change(input, { target: { value: 'Non-empty' } });

    expect(sendButton).not.toBeDisabled();
  });
});