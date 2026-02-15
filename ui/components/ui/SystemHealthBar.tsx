import * as React from 'react';
import { Activity, Database, Zap, Cpu, ShieldCheck } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export type ServiceStatus = 'operational' | 'degraded' | 'outage';

export interface HealthMetric {
  id: string;
  name: string;
  status: ServiceStatus;
}

export interface SystemHealthBarProps {
  metrics: HealthMetric[];
  className?: string;
}

const SystemHealthBar = ({ metrics, className }: SystemHealthBarProps) => {
  const statusColors = {
    operational: 'bg-emerald-500',
    degraded: 'bg-amber-500',
    outage: 'bg-red-500',
  };

  const statusGlow = {
    operational: 'shadow-emerald-500/20',
    degraded: 'shadow-amber-500/20 animate-pulse',
    outage: 'shadow-red-500/20 animate-ping',
  };

  return (
    <div className={cn('flex items-center space-x-6 px-4', className)}>
      <div className="flex items-center space-x-2 text-text-muted">
        <ShieldCheck className="h-4 w-4 text-emerald-500" />
        <span className="text-[10px] font-bold uppercase tracking-[0.2em]">System Health</span>
      </div>

      <div className="flex items-center space-x-4">
        {metrics.map((metric) => (
          <Tooltip key={metric.id} content={`${metric.name}: ${metric.status}`}>
            <div className="flex items-center space-x-1.5 cursor-help group">
              <div className={cn(
                "h-2 w-2 rounded-full shadow-sm transition-all duration-300 group-hover:scale-125",
                statusColors[metric.status],
                statusGlow[metric.status]
              )} />
              <span className="text-[9px] font-bold text-text-secondary uppercase tracking-tighter">
                {metric.name}
              </span>
            </div>
          </Tooltip>
        ))}
      </div>
    </div>
  );
};

export { SystemHealthBar };
