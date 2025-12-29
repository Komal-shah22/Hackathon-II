'use client';

import { useEffect, useState } from 'react';

export default function LoadingScreen() {
  const [dots, setDots] = useState('.');

  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? '.' : prev + '.'));
    }, 500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-[#0a0e1a]"
      style={{
        backgroundImage: `
          linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px)
        `,
        backgroundSize: '40px 40px',
      }}
    >
      <div className="flex flex-col items-center gap-8">
        {/* Logo */}
        <div className="text-3xl font-bold text-white">
          SECURE<span className="text-cyan-400">_TODO</span>
        </div>

        {/* Spinner with glow effect */}
        <div className="relative">
          <div className="w-16 h-16 border-4 border-cyan-500/30 rounded-full"></div>
          <div className="absolute inset-0 w-16 h-16 border-4 border-transparent border-t-cyan-500 rounded-full animate-spin"></div>
          <div className="absolute inset-1 w-14 h-14 bg-cyan-500/10 rounded-full blur-lg"></div>
        </div>

        {/* Status text */}
        <div className="text-center">
          <p className="text-lg text-white font-medium">
            Loading{dots}
          </p>
          <p className="text-sm text-gray-400 mt-2">
            SYSTEM ONLINE V3.0
          </p>
        </div>

        {/* Progress bar */}
        <div className="w-48 h-1 bg-white/10 rounded-full overflow-hidden">
          <div className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full animate-pulse"></div>
        </div>
      </div>
    </div>
  );
}
