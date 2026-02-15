import * as React from 'react';
import { cn } from '../../lib/utils';

export interface DiffViewerProps {
  oldValue: string;
  newValue: string;
  className?: string;
}

const DiffViewer = ({ oldValue, newValue, className }: DiffViewerProps) => {
  // Very basic diff implementation for display purposes
  const oldLines = oldValue.split('\n');
  const newLines = newValue.split('\n');

  return (
    <div className={cn('grid grid-cols-1 md:grid-cols-2 gap-4', className)}>
      {/* Original Version */}
      <div className="flex flex-col rounded-ant-lg border border-slate-200 bg-slate-50 overflow-hidden">
        <div className="px-4 py-2 border-b border-slate-200 bg-slate-100 flex items-center justify-between">
          <span className="text-[10px] font-bold text-text-muted uppercase tracking-widest">Original</span>
          <span className="text-[10px] text-text-muted">{oldLines.length} lines</span>
        </div>
        <div className="p-4 overflow-auto max-h-[400px] font-mono text-xs leading-relaxed text-text-secondary whitespace-pre bg-white">
          {oldValue}
        </div>
      </div>

      {/* Revised Version */}
      <div className="flex flex-col rounded-ant-lg border border-brand-primary/20 bg-brand-primary/5 overflow-hidden shadow-sm">
        <div className="px-4 py-2 border-b border-brand-primary/10 bg-brand-primary/10 flex items-center justify-between">
          <span className="text-[10px] font-bold text-brand-primary uppercase tracking-widest">Revised</span>
          <span className="text-[10px] text-brand-primary">{newLines.length} lines</span>
        </div>
        <div className="p-4 overflow-auto max-h-[400px] font-mono text-xs leading-relaxed text-text-primary whitespace-pre bg-white">
          {newValue}
        </div>
      </div>
    </div>
  );
};

export { DiffViewer };
