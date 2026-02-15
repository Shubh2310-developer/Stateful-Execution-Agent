import * as React from 'react';
import { cn } from '../../lib/utils';

export interface TimelineEvent {
  id: string;
  time: string;
  title: string;
  description?: string;
  status?: 'success' | 'warning' | 'error' | 'info';
  icon?: React.ReactNode;
}

export interface TimelineProps {
  events: TimelineEvent[];
  className?: string;
}

const Timeline = ({ events, className }: TimelineProps) => {
  return (
    <div className={cn('space-y-0', className)}>
      {events.map((event, index) => (
        <div key={event.id} className="relative pl-8 pb-8 last:pb-0">
          {/* Line */}
          {index !== events.length - 1 && (
            <div className="absolute left-[15px] top-[24px] bottom-0 w-[2px] bg-slate-100" />
          )}

          {/* Dot/Icon */}
          <div className={cn(
            'absolute left-0 top-1.5 flex h-8 w-8 items-center justify-center rounded-full border-4 border-white shadow-sm ring-1 ring-slate-100 transition-all duration-300',
            event.status === 'success' ? 'bg-status-success text-white' :
            event.status === 'warning' ? 'bg-status-warning text-white' :
            event.status === 'error' ? 'bg-status-error text-white' :
            'bg-slate-200 text-slate-600'
          )}>
            {event.icon || <div className="h-1.5 w-1.5 rounded-full bg-current" />}
          </div>

          <div className="flex flex-col">
            <span className="text-[10px] font-bold text-text-muted uppercase tracking-wider mb-0.5">
              {event.time}
            </span>
            <h4 className="text-sm font-bold text-text-primary">
              {event.title}
            </h4>
            {event.description && (
              <p className="mt-1 text-xs text-text-secondary leading-relaxed">
                {event.description}
              </p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export { Timeline };
