import * as React from 'react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export interface RateLimitGaugeProps {
  current: number;
  limit: number;
  unit?: string;
  provider: string;
  className?: string;
}

const RateLimitGauge = ({
  current,
  limit,
  unit = 'TPM',
  provider,
  className
}: RateLimitGaugeProps) => {
  const percentage = Math.min((current / limit) * 100, 100);
  const isHigh = percentage > 80;

  return (
    <div className={cn('p-4 bg-white border border-slate-200 rounded-ant-lg shadow-sm', className)}>
      <div className="flex items-center justify-between mb-3">
        <div>
          <h4 className="text-xs font-bold text-text-primary uppercase tracking-widest leading-none">{provider}</h4>
          <span className="text-[8px] font-bold text-text-muted uppercase tracking-tighter">Rate Limit Visibility</span>
        </div>
        <div className={cn(
          "text-[10px] font-mono font-bold px-1.5 py-0.5 rounded",
          isHigh ? "bg-red-50 text-red-600" : "bg-emerald-50 text-emerald-600"
        )}>
          {percentage.toFixed(1)}%
        </div>
      </div>

      <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden mb-3">
        <div
          className={cn(
            "h-full transition-all duration-1000 ease-out-ant",
            isHigh ? "bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.3)]" : "bg-brand-primary shadow-[0_0_10px_rgba(59,130,246,0.3)]"
          )}
          style={{ width: `${percentage}%` }}
        />
      </div>

      <div className="flex items-center justify-between text-[10px] font-mono text-text-muted">
        <span>{current.toLocaleString()} {unit}</span>
        <span>{limit.toLocaleString()} MAX</span>
      </div>
    </div>
  );
};

export { RateLimitGauge };
