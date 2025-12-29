'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { AuthCard } from '@/components/auth/AuthCard';
import { FiMail, FiLock } from 'react-icons/fi';
import LoadingScreen from '@/components/LoadingScreen';

export default function SignInPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticating, setIsAuthenticating] = useState(false);
  const { signIn } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsAuthenticating(true);

    try {
      await signIn(email, password);
      // Show loading screen briefly before redirect
      setTimeout(() => {
        router.push('/dashboard');
      }, 1500);
    } catch (err) {
      setIsAuthenticating(false);
      setError(err instanceof Error ? err.message : 'Sign in failed');
    }
  };

  if (isAuthenticating) {
    return <LoadingScreen />;
  }

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-[#0a0e1a]"
      style={{
        backgroundImage: `
          linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px)
        `,
        backgroundSize: '40px 40px',
      }}
    >
      <AuthCard>
      <h2 className="text-xl font-semibold text-center text-primary-text mb-1">
        WELCOME BACK
      </h2>
      <p className="text-center text-secondary-text text-sm mb-6">
        SIGN IN
      </p>

      <form className="space-y-4" onSubmit={handleSubmit}>
        {error && (
          <div className="p-3 bg-danger/20 border border-danger text-danger rounded-lg text-sm">
            {error}
          </div>
        )}

        <div className="relative">
          <FiMail className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-text" />
          <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email Address"
            required
            autoComplete="email"
            className="pl-10"
          />
        </div>
        
        <div className="relative">
          <FiLock className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-text" />
          <Input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
            autoComplete="current-password"
            className="pl-10"
          />
        </div>

        <div>
          <Button type="submit" className="w-full" disabled={isAuthenticating}>
            {isAuthenticating ? 'SIGNING IN...' : 'SIGN IN →'}
          </Button>
        </div>
      </form>

      <p className="mt-6 text-center text-sm text-secondary-text">
        Don't have an account?{' '}
        <Link href="/signup" className="font-medium text-primary hover:underline">
          SIGN UP
        </Link>
      </p>
      </AuthCard>
    </div>
  );
}
