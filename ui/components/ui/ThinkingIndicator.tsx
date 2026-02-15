import * as React from 'react';
import { Loader2, Sparkles, Brain, Search, Terminal } from 'lucide-react';
import { cn } from '../../lib/utils';

export type ThinkingPhase = 'planning' | 'searching' | 'reasoning' | 'executing' | 'validating';

export interface ThinkingIndicatorProps {
  phase: ThinkingPhase;
  message: string;
  metadata?: string[];
  className?: string;
}

const ThinkingIndicator = ({
  phase,
  message,
  metadata = [],
  className
}: ThinkingIndicatorProps) => {
  const icons = {
    planning: <Brain className="h-4 w-4" />,
    searching: <Search className="h-4 w-4" />,
    reasoning: <Sparkles className="h-4 w-4" />,
    executing: <Terminal className="h-4 w-4" />,
    validating: <Loader2 className="h-4 w-4 animate-spin" />,
  };

  const phaseColors = {
    planning: 'text-indigo-500 bg-indigo-50',
    searching: 'text-blue-500 bg-blue-50',
    reasoning: 'text-amber-500 bg-amber-50',
    executing: 'text-emerald-500 bg-emerald-50',
    validating: 'text-purple-500 bg-purple-50',
  };

  return (
    <div className={cn(
      'flex flex-col space-y-3 p-4 bg-white border border-slate-200 rounded-ant-lg shadow-sm animate-in fade-in slide-in-from-top-1',
      className
    )}>
      <div className="flex items-center space-x-3">
        <div className={cn(
          "flex h-8 w-8 items-center justify-center rounded-full shrink-0",
          phaseColors[phase]
        )}>
          {icons[phase]}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-bold uppercase tracking-widest text-text-muted">
              Agent {phase}
            </span>
            <div className="flex space-x-1">
              <div className="h-1 w-1 rounded-full bg-brand-primary animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="h-1 w-1 rounded-full bg-brand-primary animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="h-1 w-1 rounded-full bg-brand-primary animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
          <p className="text-sm font-medium text-text-primary truncate">
            {message}
          </p>
        </div>
      </div>

      {metadata.length > 0 && (
        <div className="flex flex-wrap gap-2 pt-1">
          {metadata.map((item, i) => (
            <div
              key={i}
              className="px-2 py-0.5 bg-slate-50 text-[10px] font-mono text-text-secondary rounded border border-slate-100"
            >
              {item}
            </div>
          ))}
        </div>
      )}

      {/* Progress Shimmer */}
      <div className="h-1 w-full bg-slate-100 rounded-full overflow-hidden">
        <div className="h-full bg-brand-primary/20 w-1/3 animate-[shimmer_2s_infinite] rounded-full" />
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(300%); }
        }
      `}} />
    </div>
  );
};

export { ThinkingIndicator };
