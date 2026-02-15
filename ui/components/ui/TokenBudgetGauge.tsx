import * as React from 'react';
import { cn } from '../../lib/utils';
import { Progress } from './Progress';
import { AlertCircle } from 'lucide-react';

export interface TokenBudgetGaugeProps {
  spent: number;
  limit: number;
  currency?: string;
  approxStepsRemaining?: number;
  className?: string;
}

const TokenBudgetGauge = ({
  spent,
  limit,
  currency = '$',
  approxStepsRemaining,
  className
}: TokenBudgetGaugeProps) => {
  const percentage = (spent / limit) * 100;
  const isHigh = percentage > 80;
  const isCritical = percentage >= 100;

  return (
    <div className={cn('p-4 bg-white border border-slate-200 rounded-ant-lg shadow-sm', className)}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex flex-col">
          <span className="text-[10px] font-bold text-text-muted uppercase tracking-widest">Spent / Budget</span>
          <div className="flex items-baseline space-x-1">
            <span className="text-xl font-bold text-text-primary">{currency}{spent.toFixed(2)}</span>
            <span className="text-xs text-text-muted">/ {currency}{limit.toFixed(2)}</span>
          </div>
        </div>
        {isHigh && (
          <div className={cn(
            "p-2 rounded-full",
            isCritical ? "bg-red-100 text-red-600" : "bg-amber-100 text-amber-600"
          )}>
            <AlertCircle className="h-5 w-5" />
          </div>
        )}
      </div>

      <Progress
        value={spent}
        max={limit}
        variant={isCritical ? 'error' : isHigh ? 'warning' : 'default'}
        className="mb-4"
      />

      <div className="flex items-center justify-between pt-3 border-t border-slate-100">
        <div className="flex flex-col">
          <span className="text-[9px] font-bold text-text-muted uppercase tracking-tight">Runway</span>
          <span className="text-xs font-bold text-text-secondary">
            {approxStepsRemaining !== undefined ? `~${approxStepsRemaining} steps left` : 'Calculating...'}
          </span>
        </div>
        <div className="text-right">
          <span className="text-[9px] font-bold text-text-muted uppercase tracking-tight">Utilization</span>
          <div className={cn(
            "text-xs font-bold",
            isCritical ? "text-red-600" : isHigh ? "text-amber-600" : "text-emerald-600"
          )}>
            {Math.round(percentage)}%
          </div>
        </div>
      </div>
    </div>
  );
};

export { TokenBudgetGauge };
