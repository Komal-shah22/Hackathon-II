'use client';

import Link from 'next/link';
import { Button } from '../ui/button';
import { FiMenu, FiUser } from 'react-icons/fi';

interface HeaderProps {
  isDashboard?: boolean;
  onMenuToggle?: () => void;
}

export function Header({ isDashboard = false, onMenuToggle }: HeaderProps) {
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
            {/* <span className="text-gray-400 hidden md:block">SYSTEM</span>
            <span className="hidden md:blocktext-gray-300 font-semibold ml-4">
              [DASHBOARD]
            </span> */}
          </div>
          <div className="flex items-center gap-4">
            {/* User Profile Dropdown Placeholder */}
            <div className="flex items-center gap-2text-gray-300 cursor-pointer">
              {/* <FiUser className="w-5 h-5" />
              <span>User Profile</span> */}
              {/* <FiChevronDown /> */}
            </div>
          </div>
        </>
      ) : (
        <>
          <Link href="/" className="text-2xl font-bold tracking-tighter text-white">
            SECURE_TODO
          </Link>
          <nav className="hidden md:flex items-center gap-6 text-sm">
            <Link href="/specs" className="text-gray-400 hover:text-primary-text transition-colors">
              
            </Link>
            <Link href="/protocol" className="text-gray-400 hover:text-primary-text transition-colors">
              
            </Link>
          </nav>
          <div>
            <Link href="/signin">
              <Button variant="outline">LOGIN</Button>
            </Link>
          </div>
        </>
      )}
    </header>
  );
}
