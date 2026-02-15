import * as React from 'react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export interface MetricItem {
  label: string;
  value: string | number;
  icon?: React.ReactNode;
  unit?: string;
}

export interface MetricsClusterProps {
  metrics: MetricItem[];
  className?: string;
}

const MetricsCluster = ({ metrics, className }: MetricsClusterProps) => {
  return (
    <div className={cn('flex items-center space-x-3', className)}>
      {metrics.map((metric, i) => (
        <Tooltip key={i} content={metric.label}>
          <div className="flex flex-col items-start min-w-[40px]">
            <div className="flex items-center space-x-1">
              {metric.icon && <span className="text-text-muted">{metric.icon}</span>}
              <span className="text-[11px] font-bold text-text-primary tabular-nums tracking-tight">
                {metric.value}{metric.unit}
              </span>
            </div>
            <span className="text-[8px] font-bold text-text-muted uppercase tracking-tighter leading-none mt-0.5">
              {metric.label}
            </span>
          </div>
        </Tooltip>
      ))}
    </div>
  );
};

export { MetricsCluster };
