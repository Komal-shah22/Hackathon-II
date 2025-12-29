'use client';

import { TextareaHTMLAttributes, forwardRef } from 'react';

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  maxLength?: number;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, error, maxLength, className = '', value, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-gray-700 mb-1">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          maxLength={maxLength}
          value={value}
          className={`
            w-full px-4 py-2.5 bg-[#1e2742] border rounded-lg text-white resize-none
            focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all
            disabled:bg-[#1e2742] disabled:cursor-not-allowed
            ${error ? 'border-red-500' : 'border-white/10'}
            ${className}
          `}
          {...props}
        />
        <div className="flex justify-between mt-1">
          {error && (
            <p className="text-sm text-red-500">{error}</p>
          )}
          {maxLength && (
            <p className={`text-sm ${(value?.toString().length || 0) > maxLength * 0.9 ? 'text-red-500' : 'text-gray-400'}`}>
              {value?.toString().length || 0}/{maxLength}
            </p>
          )}
        </div>
      </div>
    );
  }
);

Textarea.displayName = 'Textarea';
