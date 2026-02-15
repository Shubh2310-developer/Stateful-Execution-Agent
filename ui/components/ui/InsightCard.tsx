import * as React from 'react';
import { Lightbulb, Sparkles, ArrowRight, X } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';

export interface InsightCardProps {
  title: string;
  description: string;
  impact?: string;
  onApply?: () => void;
  onDismiss?: () => void;
  className?: string;
}

const InsightCard = ({
  title,
  description,
  impact,
  onApply,
  onDismiss,
  className
}: InsightCardProps) => {
  return (
    <div className={cn(
      'relative p-5 bg-gradient-to-br from-indigo-50 to-white border border-indigo-100 rounded-ant-lg shadow-sm group overflow-hidden',
      className
    )}>
      {/* Decorative Sparkles */}
      <Sparkles className="absolute -right-4 -top-4 h-24 w-24 text-indigo-500/5 group-hover:text-indigo-500/10 transition-colors" />

      <div className="relative z-10">
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-2">
            <div className="p-2 bg-indigo-500 rounded-ant-md text-white shadow-lg shadow-indigo-500/20">
              <Lightbulb size={18} />
            </div>
            <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-[0.2em]">Proactive Insight</span>
          </div>
          {onDismiss && (
            <button onClick={onDismiss} className="text-text-muted hover:text-text-primary transition-colors">
              <X size={16} />
            </button>
          )}
        </div>

        <h3 className="text-base font-bold text-text-primary mb-2 leading-tight">
          {title}
        </h3>

        <p className="text-sm text-text-secondary leading-relaxed mb-6">
          {description}
        </p>

        {impact && (
          <div className="mb-6 p-3 bg-white/60 rounded-ant-md border border-indigo-50 flex items-center justify-between">
            <span className="text-[10px] font-bold text-text-muted uppercase">Potential ROI</span>
            <span className="text-xs font-bold text-emerald-600">{impact}</span>
          </div>
        )}

        <div className="flex items-center space-x-3">
          <Button onClick={onApply} size="sm" className="bg-indigo-600 hover:bg-indigo-700 text-white">
            Apply Recommendation
            <ArrowRight className="ml-2 h-3.5 w-3.5" />
          </Button>
          <Button variant="ghost" size="sm" onClick={onDismiss} className="text-text-muted">
            Ignore
          </Button>
        </div>
      </div>
    </div>
  );
};

export { InsightCard };
