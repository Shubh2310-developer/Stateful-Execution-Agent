import * as React from 'react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export interface ContextWindowVisualizerProps {
  usedTokens: number;
  totalTokens: number;
  label?: string;
  className?: string;
}

const ContextWindowVisualizer = ({
  usedTokens,
  totalTokens,
  label = "LLM Context Window",
  className
}: ContextWindowVisualizerProps) => {
  const percentage = (usedTokens / totalTokens) * 100;
  const isWarning = percentage > 70;
  const isCritical = percentage > 90;

  return (
    <div className={cn('p-4 bg-slate-900 rounded-ant-lg border border-slate-800', className)}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{label}</span>
        <span className={cn(
          "text-[10px] font-mono font-bold",
          isCritical ? "text-red-400" : isWarning ? "text-amber-400" : "text-emerald-400"
        )}>
          {Math.round(percentage)}% Full
        </span>
      </div>

      <div className="relative h-6 w-full bg-slate-800 rounded-ant-sm overflow-hidden flex">
        {/* Visual blocks representing token usage */}
        {Array.from({ length: 20 }).map((_, i) => {
          const threshold = (i / 20) * 100;
          const isFilled = percentage > threshold;
          return (
            <div
              key={i}
              className={cn(
                "flex-1 border-r border-slate-900 transition-all duration-1000",
                isFilled
                  ? (threshold > 90 ? "bg-red-500" : threshold > 70 ? "bg-amber-500" : "bg-brand-primary")
                  : "bg-slate-700/30"
              )}
            />
          );
        })}
      </div>

      <div className="mt-3 flex items-center justify-between text-[10px] font-mono text-slate-500">
        <span>{usedTokens.toLocaleString()} tokens</span>
        <span>{totalTokens.toLocaleString()} max</span>
      </div>
    </div>
  );
};

export { ContextWindowVisualizer };
