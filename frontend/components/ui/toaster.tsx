'use client';

import { Toaster as SonnerToaster } from 'sonner';

export function Toaster() {
  return (
    <SonnerToaster
      position="top-right"
      toastOptions={{
        className:
          'bg-surface-light text-primary-text border-border shadow-lg',
        descriptionClassName: 'text-secondary-text',
      }}
    />
  );
}
