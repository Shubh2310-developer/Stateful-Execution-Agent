import * as React from 'react';
import { MessageSquare, Smile, ShieldAlert, Zap, Info } from 'lucide-react';
import { cn } from '../../lib/utils';

export type SentimentType = 'neutral' | 'positive' | 'urgent' | 'critical';

export interface SentimentSelectorProps {
  value: SentimentType;
  onChange: (value: SentimentType) => void;
  className?: string;
}

const SentimentSelector = ({ value, onChange, className }: SentimentSelectorProps) => {
  const options: { id: SentimentType; label: string; icon: any; color: string }[] = [
    { id: 'neutral', label: 'Neutral', icon: Info, color: 'text-slate-500 bg-slate-100' },
    { id: 'positive', label: 'Positive', icon: Smile, color: 'text-emerald-500 bg-emerald-100' },
    { id: 'urgent', label: 'Urgent', icon: Zap, color: 'text-amber-500 bg-amber-100' },
    { id: 'critical', label: 'Critical', icon: ShieldAlert, color: 'text-red-500 bg-red-100' },
  ];

  return (
    <div className={cn('flex items-center space-x-1 bg-slate-100/50 p-1 rounded-full border border-slate-200', className)}>
      {options.map((opt) => {
        const Icon = opt.icon;
        const isActive = value === opt.id;

        return (
          <button
            key={opt.id}
            onClick={() => onChange(opt.id)}
            className={cn(
              'flex items-center justify-center p-1.5 rounded-full transition-all duration-200',
              isActive ? cn(opt.color, 'shadow-sm scale-110') : 'text-text-muted hover:text-text-secondary hover:bg-white'
            )}
            title={opt.label}
          >
            <Icon className="h-3.5 w-3.5" />
          </button>
        );
      })}
    </div>
  );
};

export { SentimentSelector };
