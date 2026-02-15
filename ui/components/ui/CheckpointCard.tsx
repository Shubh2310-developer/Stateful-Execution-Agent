import * as React from 'react';
import { HelpCircle, Check, X, AlertCircle, Info } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';
import { Card } from './Card';
import { Badge } from './Badge';

export interface CheckpointOption {
  id: string;
  label: string;
  description?: string;
  variant?: 'default' | 'primary' | 'destructive';
}

export interface CheckpointCardProps {
  title: string;
  question: string;
  options: CheckpointOption[];
  onSelect: (optionId: string) => void;
  context?: string;
  urgency?: 'low' | 'medium' | 'high';
  className?: string;
}

const CheckpointCard = ({
  title,
  question,
  options,
  onSelect,
  context,
  urgency = 'medium',
  className
}: CheckpointCardProps) => {
  const urgencyVariants = {
    low: 'border-slate-200 bg-white',
    medium: 'border-amber-200 bg-amber-50/30',
    high: 'border-red-200 bg-red-50/30 ring-2 ring-red-500/20',
  };

  const urgencyBadge = {
    low: <Badge variant="secondary" className="bg-slate-100 text-slate-600">Standard Checkpoint</Badge>,
    medium: <Badge variant="secondary" className="bg-amber-100 text-amber-700">Approval Required</Badge>,
    high: <Badge variant="destructive">Critical Decision</Badge>,
  };

  return (
    <Card className={cn(
      'p-0 overflow-hidden shadow-lg transition-all duration-300 animate-in zoom-in-95 slide-in-from-bottom-4',
      urgencyVariants[urgency],
      className
    )}>
      <div className="p-5 border-b border-slate-100 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className={cn(
            "p-2 rounded-full",
            urgency === 'high' ? "bg-red-100 text-red-600" : "bg-amber-100 text-amber-600"
          )}>
            <HelpCircle className="h-5 w-5" />
          </div>
          <h3 className="font-bold text-text-primary">{title}</h3>
        </div>
        {urgencyBadge[urgency]}
      </div>

      <div className="p-5 space-y-4">
        <p className="text-lg font-medium text-text-primary leading-tight">
          {question}
        </p>

        {context && (
          <div className="p-3 bg-white/50 rounded-ant-md border border-slate-100 text-sm text-text-secondary flex items-start">
            <Info className="h-4 w-4 mr-2 mt-0.5 text-text-muted flex-shrink-0" />
            <p>{context}</p>
          </div>
        )}

        <div className="grid gap-3 pt-2">
          {options.map((option) => (
            <button
              key={option.id}
              onClick={() => onSelect(option.id)}
              className={cn(
                'flex flex-col items-start p-4 text-left rounded-ant-lg border transition-all duration-200 group',
                option.variant === 'primary'
                  ? 'border-brand-primary/20 bg-brand-primary/5 hover:bg-brand-primary/10 hover:border-brand-primary'
                  : option.variant === 'destructive'
                    ? 'border-red-200 bg-red-50 hover:bg-red-100 hover:border-red-400'
                    : 'border-slate-200 bg-white hover:border-brand-primary/50 hover:shadow-sm'
              )}
            >
              <div className="flex items-center justify-between w-full mb-1">
                <span className={cn(
                  "font-bold text-sm",
                  option.variant === 'primary' ? "text-brand-primary" : "text-text-primary"
                )}>
                  {option.label}
                </span>
                <Check className={cn(
                  "h-4 w-4 opacity-0 transition-opacity group-hover:opacity-100",
                  option.variant === 'primary' ? "text-brand-primary" : "text-text-muted"
                )} />
              </div>
              {option.description && (
                <p className="text-xs text-text-secondary leading-relaxed">
                  {option.description}
                </p>
              )}
            </button>
          ))}
        </div>
      </div>

      <div className="px-5 py-3 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-[10px] text-text-muted font-medium">
        <div className="flex items-center space-x-2">
          <AlertCircle className="h-3 w-3" />
          <span>The agent is paused waiting for your selection.</span>
        </div>
        <button className="hover:text-text-primary transition-colors">
          View Decision Trace
        </button>
      </div>
    </Card>
  );
};

export { CheckpointCard };
