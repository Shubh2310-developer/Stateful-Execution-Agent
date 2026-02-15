import * as React from 'react';
import { cn } from '../../lib/utils';
import { StatusPill, StatusType } from './StatusPill';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'standard' | 'task';
  progress?: number;
  status?: string;
  statusColor?: StatusType;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'standard', progress, status, statusColor, children, ...props }, ref) => {
    const isTask = variant === 'task';

    return (
      <div
        ref={ref}
        className={cn(
          'rounded-ant-lg border border-slate-200 bg-background-surface p-6 shadow-sm transition-all duration-300 ease-out-ant hover:-translate-y-0.5 hover:border-blue-300 hover:shadow-md cursor-pointer',
          className
        )}
        {...props}
      >
        {isTask && (status || statusColor) && (
          <div className="mb-4 flex items-center justify-between">
            {status && (
              <StatusPill variant={statusColor}>
                {status}
              </StatusPill>
            )}
          </div>
        )}

        {children}

        {isTask && progress !== undefined && (
          <div className="mt-4 space-y-1.5">
            <div className="flex justify-between text-xs font-medium text-text-secondary">
              <span>Progress</span>
              <span>{Math.round(progress)}%</span>
            </div>
            <div className="h-1.5 w-full overflow-hidden rounded-full bg-background-muted">
              <div
                className="h-full bg-brand-primary transition-all duration-500 ease-out"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}
      </div>
    );
  }
);

Card.displayName = 'Card';

export { Card };
