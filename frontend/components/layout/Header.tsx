'use client';

import Link from 'next/link';
import { Button } from '../ui/button';
import { FiMenu, FiUser } from 'react-icons/fi';
import { useAuth } from '@/components/auth';

interface HeaderProps {
  isDashboard?: boolean;
  onMenuToggle?: () => void;
}

export function Header({ isDashboard = false, onMenuToggle }: HeaderProps) {
  const { user, loading } = useAuth();

  return (
    <header className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-4 md:px-8 py-4 bg-[#141b2e] border-b border-white/10">
      {isDashboard ? (
        <>
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" className="md:hidden transition-all duration-300" onClick={onMenuToggle}>
              <FiMenu className="w-5 h-5" />
            </Button>
            <Link href="/dashboard" className="text-xl font-bold text-white">
              SECURE_TODO
            </Link>
          </div>
          <div className="flex items-center gap-4">
            {!loading && user && (
              <Link href="/chat">
                <Button variant="outline" className="mr-2">AI Chatbot</Button>
              </Link>
            )}
            <Link href="/dashboard/profile">
              <div className="flex items-center gap-2 text-gray-300 cursor-pointer hover:text-white">
                <FiUser className="w-5 h-5" />
                <span className="hidden sm:inline">{user?.name || user?.email}</span>
              </div>
            </Link>
          </div>
        </>
      ) : (
        <>
          <Link href="/" className="text-2xl font-bold tracking-tighter text-white">
            SECURE_TODO
          </Link>
          <nav className="hidden md:flex items-center gap-6 text-sm">
            <Link href="/specs" className="text-gray-400 hover:text-primary-text transition-colors">
              Specs
            </Link>
            <Link href="/protocol" className="text-gray-400 hover:text-primary-text transition-colors">
              Protocol
            </Link>
          </nav>
          <div className="flex items-center gap-2">
            {!loading && user ? (
              <>
                <Link href="/chat">
                  <Button variant="outline">AI Chatbot</Button>
                </Link>
                <Link href="/dashboard">
                  <Button variant="outline">Dashboard</Button>
                </Link>
              </>
            ) : (
              <Link href="/signin">
                <Button variant="outline">LOGIN</Button>
              </Link>
            )}
          </div>
        </>
      )}
    </header>
  );
}
