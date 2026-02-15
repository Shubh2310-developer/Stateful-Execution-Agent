import * as React from 'react';
import { cn } from '../../lib/utils';

export interface GaugeProps {
  value: number; // 0 to 100
  size?: 'sm' | 'md' | 'lg';
  label?: string;
  showValue?: boolean;
  className?: string;
}

const Gauge = ({
  value,
  size = 'md',
  label,
  showValue = true,
  className
}: GaugeProps) => {
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (value / 100) * circumference;

  const sizes = {
    sm: { box: 60, stroke: 6, font: 'text-[10px]' },
    md: { box: 100, stroke: 8, font: 'text-sm' },
    lg: { box: 140, stroke: 10, font: 'text-xl' },
  };

  const getColor = (val: number) => {
    if (val >= 90) return 'stroke-status-success';
    if (val >= 70) return 'stroke-brand-primary';
    if (val >= 40) return 'stroke-status-warning';
    return 'stroke-status-error';
  };

  const config = sizes[size];

  return (
    <div className={cn('flex flex-col items-center justify-center', className)}>
      <div className="relative" style={{ width: config.box, height: config.box }}>
        <svg
          className="h-full w-full -rotate-90"
          viewBox="0 0 100 100"
        >
          {/* Background circle */}
          <circle
            className="stroke-slate-100"
            strokeWidth={config.stroke}
            fill="transparent"
            r={radius}
            cx="50"
            cy="50"
          />
          {/* Progress circle */}
          <circle
            className={cn('transition-all duration-1000 ease-out-ant', getColor(value))}
            strokeWidth={config.stroke}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            fill="transparent"
            r={radius}
            cx="50"
            cy="50"
          />
        </svg>
        {showValue && (
          <div className="absolute inset-0 flex items-center justify-center">
            <span className={cn('font-bold text-text-primary', config.font)}>
              {Math.round(value)}%
            </span>
          </div>
        )}
      </div>
      {label && (
        <span className="mt-2 text-xs font-medium text-text-secondary">
          {label}
        </span>
      )}
    </div>
  );
};

export { Gauge };
