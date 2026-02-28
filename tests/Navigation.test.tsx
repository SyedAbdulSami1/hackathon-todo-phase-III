/** Tests for the Navigation component */

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Navigation } from '../components/Navigation';
import { useRouter } from 'next/navigation';
import { usePathname } from 'next/navigation';

// Mock next/navigation
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
  usePathname: jest.fn(),
}));

// Mock next/link
jest.mock('next/link', () => ({
  __esModule: true,
  default: ({ children, href }: { children: React.ReactNode; href: string }) => (
    <a href={href}>{children}</a>
  ),
}));

describe('Navigation', () => {
  const mockOnLogout = jest.fn();
  const mockPush = jest.fn();

  beforeEach(() => {
    (useRouter as jest.Mock).mockReturnValue({
      push: mockPush,
    });
    (usePathname as jest.Mock).mockReturnValue('/');
    mockOnLogout.mockClear();
    mockPush.mockClear();
  });

  it('renders navigation with user info and logout button', () => {
    render(
      <Navigation
        user={{ username: 'testuser' }}
        onLogout={mockOnLogout}
      />
    );

    expect(screen.getByText('Todo App')).toBeInTheDocument();
    expect(screen.getByText('Welcome, testuser!')).toBeInTheDocument();
    expect(screen.getByText('Logout')).toBeInTheDocument();
  });

  it('renders navigation without user info when user is not provided', () => {
    render(
      <Navigation
        onLogout={mockOnLogout}
      />
    );

    expect(screen.getByText('Todo App')).toBeInTheDocument();
    expect(screen.queryByText('Welcome,')).not.toBeInTheDocument();
    expect(screen.getByText('Logout')).toBeInTheDocument();
  });

  it('calls onLogout when logout button is clicked', () => {
    render(
      <Navigation
        user={{ username: 'testuser' }}
        onLogout={mockOnLogout}
      />
    );

    fireEvent.click(screen.getByText('Logout'));
    expect(mockOnLogout).toHaveBeenCalledTimes(1);
  });

  it('has active link styling for current page', () => {
    (usePathname as jest.Mock).mockReturnValue('/');

    render(
      <Navigation
        user={{ username: 'testuser' }}
        onLogout={mockOnLogout}
      />
    );

    // Check that the Tasks link is active
    const tasksLink = screen.getByText('Tasks').closest('a');
    expect(tasksLink).toHaveClass('border-b-2');
    expect(tasksLink).toHaveClass('border-blue-500');
    expect(tasksLink).toHaveClass('font-medium');

    // Check that the AI Chat link is not active
    const chatLink = screen.getByText('AI Chat').closest('a');
    expect(chatLink).toHaveClass('text-muted-foreground');
  });

  it('has active link styling for chat page', () => {
    (usePathname as jest.Mock).mockReturnValue('/chat');

    render(
      <Navigation
        user={{ username: 'testuser' }}
        onLogout={mockOnLogout}
      />
    );

    // Check that the AI Chat link is active
    const chatLink = screen.getByText('AI Chat').closest('a');
    expect(chatLink).toHaveClass('border-b-2');
    expect(chatLink).toHaveClass('border-blue-500');
    expect(chatLink).toHaveClass('font-medium');

    // Check that the Tasks link is not active
    const tasksLink = screen.getByText('Tasks').closest('a');
    expect(tasksLink).toHaveClass('text-muted-foreground');
  });

  it('navigates to home page when logo is clicked', () => {
    render(
      <Navigation
        user={{ username: 'testuser' }}
        onLogout={mockOnLogout}
      />
    );

    fireEvent.click(screen.getByText('Todo App'));
    // The link component would handle navigation, so we just check that the link exists
    expect(screen.getByText('Todo App')).toBeInTheDocument();
  });

  it('does not crash when user is undefined', () => {
    expect(() => {
      render(
        <Navigation
          onLogout={mockOnLogout}
        />
      );
    }).not.toThrow();
  });

  it('renders navigation with correct structure', () => {
    render(
      <Navigation
        user={{ username: 'testuser' }}
        onLogout={mockOnLogout}
      />
    );

    // Check for header element
    const header = screen.getByRole('banner');
    expect(header).toBeInTheDocument();

    // Check for navigation links container
    const navContainer = screen.getByText('Tasks').closest('nav');
    expect(navContainer).toBeInTheDocument();

    // Check for logout button container
    const logoutContainer = screen.getByText('Logout').closest('div');
    expect(logoutContainer).toBeInTheDocument();
  });
});