import * as React from 'react';
import { WifiOff, Activity, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export interface LatencyIndicatorProps {
  status: 'optimal' | 'degraded' | 'critical';
  latencyMs?: number;
  label?: string;
  className?: string;
}

const LatencyIndicator = ({
  status,
  latencyMs,
  label = "LLM Provider",
  className
}: LatencyIndicatorProps) => {
  const configs = {
    optimal: {
      color: 'text-emerald-500',
      bg: 'bg-emerald-500/10',
      icon: <Activity className="h-3 w-3" />,
      text: 'Optimal Performance'
    },
    degraded: {
      color: 'text-amber-500',
      bg: 'bg-amber-500/10',
      icon: <AlertTriangle className="h-3 w-3" />,
      text: 'Higher Latency Detected'
    },
    critical: {
      color: 'text-red-500',
      bg: 'bg-red-500/10',
      icon: <WifiOff className="h-3 w-3" />,
      text: 'Provider Unstable'
    },
  };

  const config = configs[status];

  return (
    <Tooltip content={`${label}: ${config.text} ${latencyMs ? `(${latencyMs}ms)` : ''}`}>
      <div className={cn(
        'inline-flex items-center space-x-2 px-2 py-1 rounded-ant-md border border-transparent transition-all cursor-help',
        config.bg,
        className
      )}>
        <div className={cn('relative', config.color)}>
          {config.icon}
          {status !== 'optimal' && (
            <div className="absolute inset-0 animate-ping opacity-50">
              {config.icon}
            </div>
          )}
        </div>
        <span className={cn('text-[10px] font-bold uppercase tracking-widest', config.color)}>
          {status}
        </span>
      </div>
    </Tooltip>
  );
};

export { LatencyIndicator };
