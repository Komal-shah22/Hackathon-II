'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState, useRef, useEffect } from 'react';
import { FiX, FiLogOut, FiUser, FiGrid, FiCheckSquare, FiBarChart2, FiSettings, FiMessageSquare } from 'react-icons/fi';
import { useAuth } from '@/components/auth';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  const { user, signOut } = useAuth();
  const router = useRouter();
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const isLoading = !user;

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = async () => {
    try {
      await signOut();
      router.push('/signin');
    } catch (error) {
      console.error('Logout failed:', error);
    }
    setShowDropdown(false);
  };

  const navLinks = [
    { href: '/dashboard', label: 'DASHBOARD', icon: FiGrid },
    { href: '/dashboard/tasks', label: 'TASKS', icon: FiCheckSquare },
    { href: '/dashboard/statistics', label: 'STATISTICS', icon: FiBarChart2 },
    { href: '/chatbot', label: 'CHATBOT', icon: FiMessageSquare },
    { href: '/dashboard/settings', label: 'SETTINGS', icon: FiSettings },
  ];

  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm md:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-50 w-80 h-screen bg-surface p-4 flex flex-col justify-between transition-transform duration-300 ease-in-out",
          isOpen ? "translate-x-0" : "-translate-x-full",
          "md:translate-x-0 md:static"
        )}
      >
        {/* <button
          variant="ghost"
          size="sm"
          className="absolute top-4 right-4 text-muted-text hover:text-primary-text md:hidden p-2"
          onClick={onClose}
        >
          <FiX className="w-5 h-5" />
        </button> */}

        <Button
  variant="ghost"
  size="sm"
  className="absolute top-4 right-4 text-muted-text hover:text-primary-text md:hidden p-2"
  onClick={onClose}
>
  <FiX className="w-5 h-5" />
</Button>


        <div>
          <div className="mb-8 mt-4 md:mt-0">
            <h1 className="text-2xl font-bold text-gradient">SECURE_OS</h1>
          </div>

          <nav className="flex flex-col gap-4">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-primary-text hover:bg-surface-light p-2 rounded-md transition-colors flex items-center gap-3"
              >
                <link.icon className="w-5 h-5" />
                <span>{link.label}</span>
              </Link>
            ))}
          </nav>
        </div>

        <div ref={dropdownRef} className="relative">
          {isLoading ? (
            <div className="w-full p-3 bg-surface-light rounded-md text-center text-sm text-muted-text">
              Loading...
            </div>
          ) : (
            <>
              <button
                onClick={() => setShowDropdown(!showDropdown)}
                className="w-full p-3 bg-surface-light rounded-md text-left hover:bg-surface-light/80 transition-colors flex items-center gap-3 group"
              >
                <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0">
                  <FiUser className="w-4 h-4 text-primary" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-primary-text truncate font-medium">
                    {user?.email || 'User'}
                  </p>
                  <p className="text-xs text-muted-text truncate">
                    Click to logout
                  </p>
                </div>
              </button>

              {showDropdown && (
                <div className="absolute bottom-full left-0 right-0 mb-2 bg-surface-light rounded-md shadow-lg border border-border overflow-hidden animate-in fade-in slide-in-from-bottom-2 duration-200">
                  <button
                    onClick={handleLogout}
                    className="w-full px-4 py-3 text-left text-sm text-red-400 hover:bg-red-500/10 transition-colors flex items-center gap-3"
                  >
                    <FiLogOut className="w-4 h-4" />
                    <span>Logout</span>
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </aside>
    </>
  );
}
