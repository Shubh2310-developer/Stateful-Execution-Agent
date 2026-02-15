import * as React from 'react';
import { cn } from '../../lib/utils';

export interface GraphNodeProps {
  id: string;
  label: string;
  status?: 'pending' | 'running' | 'success' | 'failed';
  type?: 'task' | 'tool' | 'decision';
  isActive?: boolean;
  progress?: number;
  onClick?: () => void;
  className?: string;
}

const GraphNode = ({
  id,
  label,
  status = 'pending',
  type = 'task',
  isActive = false,
  progress,
  onClick,
  className
}: GraphNodeProps) => {
  const statusColors = {
    pending: 'bg-white border-slate-200 text-slate-400',
    running: 'bg-white border-brand-primary text-brand-primary ring-2 ring-brand-primary/20 animate-pulse',
    success: 'bg-emerald-50 border-emerald-500 text-emerald-700',
    failed: 'bg-red-50 border-red-500 text-red-700',
  };

  const typeIcons = {
    task: '○',
    tool: '⚡',
    decision: '◇',
  };

  return (
    <div
      onClick={onClick}
      className={cn(
        'relative flex items-center p-3 rounded-ant-md border-2 shadow-sm transition-all duration-300 min-w-[160px] cursor-pointer',
        statusColors[status],
        isActive && 'scale-105 shadow-md border-brand-primary',
        className
      )}
    >
      <div className="flex h-6 w-6 shrink-0 items-center justify-center font-bold mr-3 rounded-full bg-slate-100/50">
        <span className="text-xs">{typeIcons[type]}</span>
      </div>

      <div className="flex flex-col min-w-0 flex-1">
        <span className="text-xs font-bold truncate leading-tight">
          {label}
        </span>
        {status === 'running' && progress !== undefined && (
          <div className="mt-1.5 h-1 w-full bg-slate-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-brand-primary transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        )}
        {status !== 'pending' && status !== 'running' && (
          <span className="text-[9px] uppercase font-bold tracking-wider mt-0.5 opacity-70">
            {status}
          </span>
        )}
      </div>

      {isActive && (
        <div className="absolute -top-1 -right-1 h-3 w-3 bg-brand-primary rounded-full ring-2 ring-white" />
      )}
    </div>
  );
};

export { GraphNode };
