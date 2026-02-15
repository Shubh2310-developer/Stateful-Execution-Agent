import * as React from 'react';
import { Gauge, Zap, AlertTriangle, Info } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Slider } from './Slider';
import { Tooltip } from './Tooltip';

export interface ResourceThrottleProps {
  value: number; // 0 to 100
  onChange: (value: number) => void;
  predictedCostChange?: string;
  predictedTimeChange?: string;
  isCongested?: boolean;
  className?: string;
}

const ResourceThrottle = ({
  value,
  onChange,
  predictedCostChange = "+0%",
  predictedTimeChange = "-0%",
  isCongested = false,
  className
}: ResourceThrottleProps) => {
  const getLevelLabel = (val: number) => {
    if (val < 25) return 'Background';
    if (val < 50) return 'Balanced';
    if (val < 75) return 'High Priority';
    return 'Turbo';
  };

  const getLevelColor = (val: number) => {
    if (val < 25) return 'text-slate-500';
    if (val < 50) return 'text-blue-500';
    if (val < 75) return 'text-indigo-600';
    return 'text-brand-cta animate-pulse';
  };

  return (
    <div className={cn('p-4 bg-white border border-slate-200 rounded-ant-lg shadow-sm space-y-6', className)}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-slate-100 rounded-full text-text-secondary">
            <Gauge size={18} />
          </div>
          <div>
            <h4 className="text-sm font-bold text-text-primary uppercase tracking-wider">Agent Power Throttle</h4>
            <span className={cn("text-[10px] font-bold uppercase tracking-widest", getLevelColor(value))}>
              Mode: {getLevelLabel(value)}
            </span>
          </div>
        </div>
        {isCongested && (
          <Tooltip content="Infrastructure is currently under high load. High-priority tasks may experience delays.">
            <div className="flex items-center space-x-1.5 px-2 py-1 bg-amber-50 text-amber-700 border border-amber-200 rounded-full text-[10px] font-bold animate-pulse">
              <AlertTriangle size={12} />
              <span>Congestion Active</span>
            </div>
          </Tooltip>
        )}
      </div>

      <div className="px-2">
        <Slider
          value={value}
          onChange={onChange}
          min={0}
          max={100}
          step={5}
          showValue={false}
        />
        <div className="flex justify-between mt-2 text-[8px] font-bold text-text-muted uppercase tracking-tighter">
          <span>Efficiency</span>
          <span>Standard</span>
          <span>Priority</span>
          <span>Max Performance</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 pt-2">
        <div className="p-2 bg-slate-50 rounded border border-slate-100 flex flex-col items-center">
          <span className="text-[9px] font-bold text-text-muted uppercase mb-1">Impact on Cost</span>
          <span className={cn(
            "text-xs font-bold",
            value > 50 ? "text-amber-600" : "text-emerald-600"
          )}>{predictedCostChange}</span>
        </div>
        <div className="p-2 bg-slate-50 rounded border border-slate-100 flex flex-col items-center">
          <span className="text-[9px] font-bold text-text-muted uppercase mb-1">Impact on Speed</span>
          <span className={cn(
            "text-xs font-bold",
            value > 50 ? "text-emerald-600" : "text-text-muted"
          )}>{predictedTimeChange}</span>
        </div>
      </div>

      <div className="flex items-start space-x-2 text-[9px] text-text-muted leading-relaxed">
        <Info size={12} className="shrink-0 mt-0.5" />
        <p>Allocating more compute allows the agent to explore more reasoning branches simultaneously, increasing reliability and speed but consuming more tokens.</p>
      </div>
    </div>
  );
};

export { ResourceThrottle };
