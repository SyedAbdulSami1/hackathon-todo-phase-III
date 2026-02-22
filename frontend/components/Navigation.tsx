'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from './ui/button';

interface NavigationProps {
  user?: {
    username: string;
  };
  onLogout: () => void;
}

export const Navigation: React.FC<NavigationProps> = ({ user, onLogout }) => {
  const pathname = usePathname();

  return (
    <header className="mb-8 flex justify-between items-center border-b pb-4">
      <div>
        <h1 className="text-3xl font-bold text-foreground">
          <Link href="/">Todo App</Link>
        </h1>
        <nav className="mt-4 flex space-x-4">
          <Link
            href="/"
            className={`pb-1 px-2 ${
              pathname === '/' ? 'border-b-2 border-blue-500 font-medium' : 'text-muted-foreground'
            }`}
          >
            Tasks
          </Link>
          <Link
            href="/chat"
            className={`pb-1 px-2 ${
              pathname === '/chat' ? 'border-b-2 border-blue-500 font-medium' : 'text-muted-foreground'
            }`}
          >
            AI Chat
          </Link>
        </nav>
      </div>
      <div className="flex items-center space-x-4">
        {user && <span className="text-muted-foreground">Welcome, {user.username}!</span>}
        <Button onClick={onLogout} variant="outline">
          Logout
        </Button>
      </div>
    </header>
  );
};