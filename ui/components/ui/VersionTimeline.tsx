import * as React from 'react';
import { History, RotateCcw, ChevronRight } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface VersionItem {
  id: string;
  version: number;
  timestamp: string;
  author: string;
  summary: string;
  isCurrent?: boolean;
}

export interface VersionTimelineProps {
  versions: VersionItem[];
  activeVersionId?: string;
  onSelect?: (id: string) => void;
  onRollback?: (id: string) => void;
  className?: string;
}

const VersionTimeline = ({
  versions,
  activeVersionId,
  onSelect,
  onRollback,
  className
}: VersionTimelineProps) => {
  return (
    <div className={cn('flex flex-col space-y-1', className)}>
      {versions.map((version) => {
        const isActive = activeVersionId === version.id;

        return (
          <div
            key={version.id}
            onClick={() => onSelect?.(version.id)}
            className={cn(
              'group relative flex items-start p-3 rounded-ant-md transition-all duration-200 cursor-pointer border',
              isActive
                ? 'bg-brand-primary/5 border-brand-primary/20 shadow-sm'
                : 'bg-white border-transparent hover:bg-slate-50 hover:border-slate-200'
            )}
          >
            {/* Version Dot */}
            <div className={cn(
              'absolute left-[-5px] top-4 h-2.5 w-2.5 rounded-full border-2 border-white ring-1 ring-slate-100',
              version.isCurrent ? 'bg-emerald-500' : 'bg-slate-300'
            )} />

            <div className="flex-1 min-w-0 ml-2">
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center space-x-2">
                  <span className={cn(
                    "text-xs font-bold font-mono",
                    isActive ? "text-brand-primary" : "text-text-primary"
                  )}>
                    v{version.version}
                  </span>
                  <span className="text-[10px] text-text-muted">
                    {version.timestamp}
                  </span>
                </div>
                {version.isCurrent && (
                  <span className="text-[9px] font-bold text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-100 uppercase tracking-wider">
                    Current
                  </span>
                )}
              </div>
              <p className="text-xs text-text-secondary truncate pr-8">
                {version.summary}
              </p>
              <div className="mt-2 flex items-center text-[10px] text-text-muted">
                <span>By {version.author}</span>
              </div>
            </div>

            <div className="flex flex-col items-end justify-center space-y-2">
              <ChevronRight className={cn(
                "h-4 w-4 transition-transform",
                isActive ? "text-brand-primary translate-x-1" : "text-text-muted opacity-0 group-hover:opacity-100"
              )} />
              {onRollback && !version.isCurrent && isActive && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onRollback(version.id);
                  }}
                  className="flex items-center space-x-1 text-[10px] font-bold text-brand-primary hover:text-brand-cta transition-colors animate-in fade-in slide-in-from-right-2"
                >
                  <RotateCcw className="h-3 w-3" />
                  <span>Rollback</span>
                </button>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export { VersionTimeline };
