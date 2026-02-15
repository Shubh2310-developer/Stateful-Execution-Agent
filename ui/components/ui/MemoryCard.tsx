import * as React from 'react';
import { Database, Lightbulb, UserCheck, Shield, Zap } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { Badge } from './Badge';

export type MemoryType = 'preference' | 'fact' | 'pattern' | 'constraint';

export interface MemoryCardProps {
  type: MemoryType;
  content: string;
  confidence: number;
  source?: string;
  timestamp?: string;
  className?: string;
}

const MemoryCard = ({
  type,
  content,
  confidence,
  source,
  timestamp,
  className
}: MemoryCardProps) => {
  const configs = {
    preference: {
      icon: <UserCheck className="h-4 w-4" />,
      label: 'Preference',
      color: 'text-blue-600 bg-blue-50 border-blue-100',
    },
    fact: {
      icon: <Database className="h-4 w-4" />,
      label: 'Knowledge',
      color: 'text-emerald-600 bg-emerald-50 border-emerald-100',
    },
    pattern: {
      icon: <Zap className="h-4 w-4" />,
      label: 'Pattern',
      color: 'text-amber-600 bg-amber-50 border-amber-100',
    },
    constraint: {
      icon: <Shield className="h-4 w-4" />,
      label: 'Constraint',
      color: 'text-red-600 bg-red-50 border-red-100',
    },
  };

  const config = configs[type];

  return (
    <Card className={cn('p-4 hover:border-brand-primary/30 transition-all duration-300', className)}>
      <div className="flex items-center justify-between mb-3">
        <div className={cn(
          "flex items-center space-x-2 px-2.5 py-1 rounded-full border text-[10px] font-bold uppercase tracking-wider",
          config.color
        )}>
          {config.icon}
          <span>{config.label}</span>
        </div>
        <div className="flex items-center space-x-2 text-[10px] text-text-muted font-mono">
          <span>Confidence:</span>
          <span className={cn(
            "font-bold",
            confidence >= 0.9 ? "text-status-success" : "text-status-warning"
          )}>
            {Math.round(confidence * 100)}%
          </span>
        </div>
      </div>

      <p className="text-sm text-text-primary leading-relaxed font-medium">
        {content}
      </p>

      {(source || timestamp) && (
        <div className="mt-4 flex items-center justify-between pt-3 border-t border-slate-100 text-[10px] text-text-muted">
          <span className="truncate max-w-[150px]">
            Source: {source || 'Observation'}
          </span>
          <span>{timestamp}</span>
        </div>
      )}
    </Card>
  );
};

export { MemoryCard };
