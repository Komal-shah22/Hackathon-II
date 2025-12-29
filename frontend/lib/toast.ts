'use client';

import { useCallback } from 'react';
import { toast } from 'sonner';

type ToastType = 'success' | 'error' | 'info' | 'warning';

interface ToastOptions {
  title: string;
  description?: string;
  duration?: number;
}

export function useToast() {
  const showToast = useCallback((type: ToastType, options: ToastOptions) => {
    const { title, description, duration = 4000 } = options;

    switch (type) {
      case 'success':
        toast.success(title, {
          description,
          duration,
        });
        break;
      case 'error':
        toast.error(title, {
          description,
          duration: 5000,
        });
        break;
      case 'info':
        toast.info(title, {
          description,
          duration,
        });
        break;
      case 'warning':
        toast.warning(title, {
          description,
          duration,
        });
        break;
    }
  }, []);

  return {
    success: (options: ToastOptions) => showToast('success', options),
    error: (options: ToastOptions) => showToast('error', options),
    info: (options: ToastOptions) => showToast('info', options),
    warning: (options: ToastOptions) => showToast('warning', options),
    dismiss: toast.dismiss,
  };
}

// Convenience hooks for common operations
export function useTaskToast() {
  const toast = useToast();

  return {
    created: () =>
      toast.success({
        title: 'Task created',
        description: 'Your new task has been added.',
      }),
    updated: () =>
      toast.success({
        title: 'Task updated',
        description: 'Changes saved successfully.',
      }),
    deleted: () =>
      toast.success({
        title: 'Task deleted',
        description: 'The task has been removed.',
      }),
    completed: () =>
      toast.success({
        title: 'Task completed',
        description: 'Great job getting it done!',
      }),
    error: (message: string) =>
        toast.error({
          title: 'Something went wrong',
          description: message,
        }),
  };
}

export function useAuthToast() {
  const toast = useToast();

  return {
    signedIn: (name?: string) =>
      toast.success({
        title: 'Welcome back!',
        description: name ? `Signed in as ${name}` : 'You have been signed in.',
      }),
    signedUp: () =>
      toast.success({
        title: 'Account created',
        description: 'Welcome to your new task manager!',
      }),
    signedOut: () =>
      toast.info({
        title: 'Signed out',
        description: 'You have been logged out.',
      }),
    error: (message: string) =>
      toast.error({
        title: 'Authentication failed',
        description: message,
      }),
  };
}
