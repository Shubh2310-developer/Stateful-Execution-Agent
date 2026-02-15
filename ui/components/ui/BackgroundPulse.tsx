import * as React from 'react';
import { cn } from '../../lib/utils';

export interface BackgroundPulseProps {
  isActive?: boolean;
  message?: string;
  className?: string;
}

const BackgroundPulse = ({
  isActive = false,
  message = "Daydreaming...",
  className
}: BackgroundPulseProps) => {
  return (
    <div className={cn(
      'flex items-center space-x-3 transition-all duration-500 px-3 py-1.5 rounded-full border',
      isActive ? 'bg-indigo-500/5 border-indigo-500/10' : 'opacity-0 scale-95 pointer-events-none',
      className
    )}>
      <div className="relative flex h-2 w-2">
        <div className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></div>
        <div className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></div>
      </div>
      <span className="text-[10px] font-bold text-indigo-500 uppercase tracking-[0.2em]">
        {message}
      </span>
    </div>
  );
};

export { BackgroundPulse };
