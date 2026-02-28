/** Tests for the ChatContext */

import React from 'react';
import { render, act } from '@testing-library/react';
import { ChatProvider, useChat } from '../contexts/ChatContext';

// Mock component to test the context
const TestComponent = () => {
  const { state, dispatch } = useChat();

  const addMessage = () => {
    dispatch({
      type: 'ADD_MESSAGE',
      payload: {
        id: 'test-id',
        content: 'Test message',
        sender: 'user',
        timestamp: new Date().toISOString(),
      },
    });
  };

  const setLoading = (isLoading: boolean) => {
    dispatch({ type: 'SET_LOADING', payload: isLoading });
  };

  const setError = (error: string | null) => {
    dispatch({ type: 'SET_ERROR', payload: error });
  };

  return (
    <div>
      <div data-testid="messages-count">{state.messages.length}</div>
      <div data-testid="loading-status">{state.isLoading.toString()}</div>
      <div data-testid="error-message">{state.error || 'no-error'}</div>
      <button onClick={addMessage}>Add Message</button>
      <button onClick={() => setLoading(true)}>Set Loading</button>
      <button onClick={() => setError('test-error')}>Set Error</button>
    </div>
  );
};

describe('ChatContext', () => {
  it('should provide initial state', () => {
    const { getByTestId } = render(
      <ChatProvider>
        <TestComponent />
      </ChatProvider>
    );

    expect(getByTestId('messages-count').textContent).toBe('0');
    expect(getByTestId('loading-status').textContent).toBe('false');
    expect(getByTestId('error-message').textContent).toBe('no-error');
  });

  it('should add a message via dispatch', () => {
    const { getByTestId, getByText } = render(
      <ChatProvider>
        <TestComponent />
      </ChatProvider>
    );

    expect(getByTestId('messages-count').textContent).toBe('0');

    act(() => {
      getByText('Add Message').click();
    });

    expect(getByTestId('messages-count').textContent).toBe('1');
  });

  it('should set loading state via dispatch', () => {
    const { getByTestId, getByText } = render(
      <ChatProvider>
        <TestComponent />
      </ChatProvider>
    );

    expect(getByTestId('loading-status').textContent).toBe('false');

    act(() => {
      getByText('Set Loading').click();
    });

    expect(getByTestId('loading-status').textContent).toBe('true');
  });

  it('should set error state via dispatch', () => {
    const { getByTestId, getByText } = render(
      <ChatProvider>
        <TestComponent />
      </ChatProvider>
    );

    expect(getByTestId('error-message').textContent).toBe('no-error');

    act(() => {
      getByText('Set Error').click();
    });

    expect(getByTestId('error-message').textContent).toBe('test-error');
  });

  it('should throw error when used outside provider', () => {
    const ConsoleError = console.error;
    console.error = jest.fn(); // Suppress the error that will be thrown

    expect(() => {
      render(<TestComponent />);
    }).toThrow('useChat must be used within a ChatProvider');

    console.error = ConsoleError; // Restore console.error
  });
});