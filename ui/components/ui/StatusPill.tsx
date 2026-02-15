import * as React from 'react';
import { cn } from '../../lib/utils';

export type StatusType = 'success' | 'warning' | 'error' | 'info' | 'running' | 'pending' | 'paused';

export interface StatusPillProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: StatusType;
}

const StatusPill = React.forwardRef<HTMLSpanElement, StatusPillProps>(
  ({ className, variant = 'pending', children, ...props }, ref) => {
    const variants = {
      success: 'bg-emerald-50 text-emerald-700 border-emerald-100',
      warning: 'bg-amber-50 text-amber-700 border-amber-100',
      error: 'bg-red-50 text-red-700 border-red-100',
      info: 'bg-indigo-50 text-indigo-700 border-indigo-100',
      running: 'bg-blue-50 text-blue-700 border-blue-100 animate-pulse',
      paused: 'bg-amber-50 text-amber-700 border-amber-100',
      pending: 'bg-slate-50 text-slate-700 border-slate-100',
    };

    return (
      <span
        ref={ref}
        className={cn(
          'inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-semibold transition-colors',
          variants[variant],
          className
        )}
        {...props}
      >
        {children}
      </span>
    );
  }
);

StatusPill.displayName = 'StatusPill';

export { StatusPill };
