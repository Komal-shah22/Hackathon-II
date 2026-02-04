'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

interface AvatarProps extends React.HTMLAttributes<HTMLDivElement> {
  children?: React.ReactNode;
}

interface AvatarImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {}

interface AvatarFallbackProps extends React.HTMLAttributes<HTMLSpanElement> {}

const AvatarContext = React.createContext<{
  size?: 'sm' | 'md' | 'lg';
  variant?: 'circle' | 'square';
}>({
  size: 'md',
  variant: 'circle',
});

const Avatar = React.forwardRef<
  HTMLDivElement,
  AvatarProps & { size?: 'sm' | 'md' | 'lg'; variant?: 'circle' | 'square' }
>(({ className, size = 'md', variant = 'circle', children, ...props }, ref) => {
  return (
    <AvatarContext.Provider value={{ size, variant }}>
      <div
        ref={ref}
        className={cn(
          'relative flex shrink-0 overflow-hidden',
          variant === 'circle' ? 'rounded-full' : 'rounded-md',
          size === 'sm' ? 'h-8 w-8' : size === 'md' ? 'h-10 w-10' : 'h-12 w-12',
          className
        )}
        {...props}
      >
        {children}
      </div>
    </AvatarContext.Provider>
  );
});
Avatar.displayName = 'Avatar';

const AvatarImage = React.forwardRef<HTMLImageElement, AvatarImageProps>(
  ({ className, ...props }, ref) => {
    return (
      <img
        ref={ref}
        className={cn('aspect-square h-full w-full', className)}
        {...props}
      />
    );
  }
);
AvatarImage.displayName = 'AvatarImage';

const AvatarFallback = React.forwardRef<
  HTMLSpanElement,
  AvatarFallbackProps
>(({ className, children, ...props }, ref) => {
  const { size } = React.useContext(AvatarContext);

  return (
    <span
      ref={ref}
      className={cn(
        'flex h-full w-full items-center justify-center rounded-full bg-muted',
        size === 'sm' ? 'text-xs' : size === 'md' ? 'text-sm' : 'text-base',
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
});
AvatarFallback.displayName = 'AvatarFallback';

export { Avatar, AvatarImage, AvatarFallback };