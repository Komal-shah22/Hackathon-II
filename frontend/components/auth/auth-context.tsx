'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, UserResponse } from '@/lib/types';
import { api } from '@/lib/api';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, name: string) => Promise<void>;
  signOut: () => Promise<void>;
  setUser: (user: User | null) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

function mapUserResponseToUser(user: UserResponse): User {
  return {
    id: user.id,
    email: user.email,
    name: user.name,
    created_at: user.created_at,
    updated_at: user.updated_at || undefined,
  };
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');

    if (token && userData) {
      try {
        setUser(JSON.parse(userData));
      } catch {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
    setLoading(false);
  }, []);

  const signIn = async (email: string, password: string) => {
    if (!email || !password) {
      throw new Error('Email and password are required');
    }

    const response = await api.signin(email, password);
    const user = response.user;

    localStorage.setItem('token', response.token);
    localStorage.setItem('user', JSON.stringify(mapUserResponseToUser(user)));
    setUser(mapUserResponseToUser(user));
  };

  const signUp = async (email: string, password: string, name: string) => {
    if (!email || !password) {
      throw new Error('Email and password are required');
    }

    if (password.length < 8) {
      throw new Error('Password must be at least 8 characters');
    }

    const response = await api.signup(email, password, name || undefined);
    const user = response.user;

    localStorage.setItem('token', response.token);
    localStorage.setItem('user', JSON.stringify(mapUserResponseToUser(user)));
    setUser(mapUserResponseToUser(user));
  };

  const signOut = async () => {
    try {
      await api.logout();
    } catch {
      // Ignore logout errors - we still clear local state
    }
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, signIn, signUp, signOut, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
