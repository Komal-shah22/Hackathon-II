'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth';
import { AuthGuard } from '@/components/auth/auth-guard';
import { Header } from '@/components/layout/Header';
import { Sidebar } from '@/components/layout/Sidebar';
import { cn } from '@/lib/utils';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <AuthGuard>
      <div
        className="flex min-h-screen bg-[#0a0e1a]"
        style={{
          backgroundImage: `
            linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px)
          `,
          backgroundSize: '40px 40px',
        }}
      >
        <Sidebar isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />
        <div
          className={cn(
            "flex flex-col flex-grow transition-all duration-300 ease-in-out pl-6",
            "md:pt-0"
          )}
        >
          <Header isDashboard={true} onMenuToggle={() => setIsSidebarOpen(!isSidebarOpen)} />
          <main className="flex-grow p-4 md:p-8 mt-16">
            {children}
          </main>
        </div>
      </div>
    </AuthGuard>
  );
}
