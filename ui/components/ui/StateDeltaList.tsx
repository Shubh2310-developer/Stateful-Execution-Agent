import * as React from 'react';
import { Plus, Minus, Edit3, ChevronRight } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface StateDelta {
  path: string;
  type: 'added' | 'removed' | 'modified';
  description: string;
  category: 'plan' | 'artifact' | 'memory' | 'trace';
}

export interface StateDeltaListProps {
  deltas: StateDelta[];
  onDeltaClick?: (delta: StateDelta) => void;
  className?: string;
}

const StateDeltaList = ({ deltas, onDeltaClick, className }: StateDeltaListProps) => {
  const typeIcons = {
    added: <Plus className="h-3 w-3" />,
    removed: <Minus className="h-3 w-3" />,
    modified: <Edit3 className="h-3 w-3" />,
  };

  const typeStyles = {
    added: 'text-emerald-600 bg-emerald-50 border-emerald-100',
    removed: 'text-red-600 bg-red-50 border-red-100',
    modified: 'text-blue-600 bg-blue-50 border-blue-100',
  };

  const categoryStyles = {
    plan: 'bg-indigo-50 text-indigo-700',
    artifact: 'bg-amber-50 text-amber-700',
    memory: 'bg-emerald-50 text-emerald-700',
    trace: 'bg-slate-50 text-slate-700',
  };

  return (
    <div className={cn('flex flex-col space-y-2', className)}>
      {deltas.map((delta, i) => (
        <button
          key={i}
          onClick={() => onDeltaClick?.(delta)}
          className="flex items-start p-3 bg-white border border-slate-200 rounded-ant-md hover:border-brand-primary/40 hover:shadow-sm transition-all duration-200 text-left group"
        >
          <div className={cn(
            'flex h-6 w-6 shrink-0 items-center justify-center rounded-full border mr-3 mt-0.5',
            typeStyles[delta.type]
          )}>
            {typeIcons[delta.type]}
          </div>

          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2 mb-1">
              <span className={cn(
                "text-[10px] font-bold uppercase tracking-widest px-1.5 py-0.5 rounded",
                categoryStyles[delta.category]
              )}>
                {delta.category}
              </span>
              <span className="text-[10px] font-mono text-text-muted truncate">
                {delta.path}
              </span>
            </div>
            <p className="text-sm font-medium text-text-primary leading-snug">
              {delta.description}
            </p>
          </div>

          <ChevronRight className="h-4 w-4 text-text-muted opacity-0 group-hover:opacity-100 transition-all duration-200 ml-2 mt-1" />
        </button>
      ))}
    </div>
  );
};

export { StateDeltaList };
