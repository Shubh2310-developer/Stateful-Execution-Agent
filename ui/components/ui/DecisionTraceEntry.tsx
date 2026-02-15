import * as React from 'react';
import { ChevronDown, ChevronUp, Clock, Target, ShieldCheck } from 'lucide-react';
import { cn } from '../../lib/utils';
import { StatusPill } from './StatusPill';
import { Skeleton } from './Skeleton';
import { Markdown } from './Markdown';

export interface DecisionTraceEntryProps {
  timestamp: string;
  decisionPoint: string;
  reasoning: string;
  action: string;
  confidence: number;
  isExpanded?: boolean;
  className?: string;
  isLoading?: boolean;
}

const DecisionTraceEntry = ({
  timestamp,
  decisionPoint,
  reasoning,
  action,
  confidence,
  isExpanded: initialExpanded = false,
  className,
  isLoading = false
}: DecisionTraceEntryProps) => {
  const [isExpanded, setIsExpanded] = React.useState(initialExpanded);

  if (isLoading) {
    return (
      <div className={cn('relative border-l-2 border-slate-100 pl-6 py-4 animate-pulse', className)}>
        <div className="absolute -left-[9px] top-6 h-4 w-4 rounded-full border-2 border-white bg-slate-100" />
        <div className="flex justify-between mb-2">
          <Skeleton className="h-3 w-16" />
          <Skeleton className="h-4 w-24 rounded-full" />
        </div>
        <Skeleton className="h-5 w-48 mb-3" />
        <Skeleton className="h-4 w-full mb-1" />
        <Skeleton className="h-4 w-3/4" />
      </div>
    );
  }

  const getConfidenceColor = (score: number) => {
    if (score >= 0.9) return 'success';
    if (score >= 0.7) return 'info';
    if (score >= 0.5) return 'warning';
    return 'error';
  };

  return (
    <div
      aria-live="polite"
      className={cn(
        'group relative border-l-2 border-slate-200 pl-6 py-4 transition-all duration-300 hover:border-brand-primary/50 animate-in fade-in slide-in-from-top-4 duration-250',
        className
      )}
    >
      {/* Timeline Bullet */}
      <div className="absolute -left-[9px] top-6 h-4 w-4 rounded-full border-2 border-white bg-slate-200 transition-colors group-hover:bg-brand-primary" />

      {/* Decision Point Title - Sequential Stagger 1 */}
      <div className="flex items-start justify-between opacity-0 animate-in fade-in slide-in-from-top-1 fill-mode-forwards [animation-delay:100ms]">
        <div className="flex flex-col">
          <div className="flex items-center space-x-2 text-[10px] text-text-muted mb-1">
            <Clock className="h-3 w-3" />
            <span>{timestamp}</span>
          </div>
          <h4 className="text-sm font-bold text-text-primary flex items-center">
            <Target className="h-3.5 w-3.5 mr-2 text-brand-primary" />
            {decisionPoint}
          </h4>
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-text-muted hover:text-text-primary p-1 transition-colors"
          aria-label={isExpanded ? "Collapse reasoning" : "Expand reasoning"}
        >
          {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
        </button>
      </div>

      {/* Action Taken - Sequential Stagger 2 */}
      <div className="mt-2 text-sm text-text-secondary opacity-0 animate-in fade-in slide-in-from-top-1 fill-mode-forwards [animation-delay:200ms]">
        <span className="font-semibold text-text-primary">Action: </span>
        <code className="bg-slate-100 px-1.5 py-0.5 rounded text-[11px] font-mono text-brand-primary">{action}</code>
      </div>

      {/* Confidence Score - Sequential Stagger 3 */}
      <div className="mt-2 opacity-0 animate-in fade-in slide-in-from-top-1 fill-mode-forwards [animation-delay:300ms]">
        <StatusPill variant={getConfidenceColor(confidence)} className="text-[10px] uppercase tracking-wider font-bold">
          {Math.round(confidence * 100)}% Confidence
        </StatusPill>
      </div>

      {/* Expandable Reasoning */}
      <div className={cn(
        'overflow-hidden transition-all duration-300 ease-in-out',
        isExpanded ? 'max-h-[1000px] mt-3' : 'max-h-0'
      )}>
        <div className="p-4 bg-slate-50/50 rounded-ant-md border border-slate-100 shadow-inner">
          <Markdown content={reasoning} className="text-xs !leading-relaxed" />
        </div>
      </div>
    </div>
  );
};

export { DecisionTraceEntry };
