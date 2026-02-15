import * as React from 'react';
import { cn } from '../../lib/utils';

export interface PriceIndicatorProps {
  amount: string | number;
  unit?: string;
  label?: string;
  className?: string;
}

const PriceIndicator = ({
  amount,
  unit = '1k tokens',
  label,
  className
}: PriceIndicatorProps) => {
  return (
    <div className={cn('inline-flex flex-col', className)}>
      {label && (
        <span className="text-[9px] font-bold text-text-muted uppercase tracking-widest mb-0.5">
          {label}
        </span>
      )}
      <div className="flex items-center space-x-1.5 bg-slate-50 border border-slate-200 px-2 py-1 rounded-ant-md">
        <span className="text-xs font-bold text-text-primary">${amount}</span>
        <span className="text-[10px] text-text-muted">/ {unit}</span>
      </div>
    </div>
  );
};

export { PriceIndicator };
