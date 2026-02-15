import * as React from 'react';
import { Clock, TrendingUp, Sparkles } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface TimeSavedGaugeProps {
  hoursSaved: number;
  totalAgentTime: number;
  manualEstimateMultiplier?: number;
  className?: string;
}

const TimeSavedGauge = ({
  hoursSaved,
  totalAgentTime,
  manualEstimateMultiplier = 4.5,
  className
}: TimeSavedGaugeProps) => {
  const radius = 80;
  const circumference = 2 * Math.PI * radius;

  // Calculate percentage of time saved relative to some organizational benchmark or goal
  const percentage = Math.min((hoursSaved / (hoursSaved + totalAgentTime)) * 100, 100);
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className={cn('p-8 bg-white border border-slate-200 rounded-ant-xl shadow-lg relative overflow-hidden flex flex-col items-center text-center', className)}>
      {/* Background Decor */}
      <Sparkles className="absolute -top-4 -left-4 text-emerald-500/5 h-32 w-32 rotate-12" />

      <div className="relative mb-6">
        <svg width="200" height="200" className="transform -rotate-90">
          <circle
            className="stroke-slate-100"
            strokeWidth="12"
            fill="transparent"
            r={radius}
            cx="100"
            cy="100"
          />
          <circle
            className="stroke-emerald-500 transition-all duration-1000 ease-out-ant"
            strokeWidth="12"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            fill="transparent"
            r={radius}
            cx="100"
            cy="100"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center rotate-90">
          <span className="text-4xl font-black text-text-primary tracking-tighter">{hoursSaved.toFixed(1)}</span>
          <span className="text-[10px] font-bold text-emerald-600 uppercase tracking-[0.2em]">Hours Saved</span>
        </div>
      </div>

      <div className="space-y-4 w-full">
        <div className="flex items-center justify-center space-x-2 text-text-secondary">
          <TrendingUp className="h-4 w-4 text-emerald-500" />
          <span className="text-sm font-medium">Efficiency Multiplier: <span className="font-bold text-text-primary">{manualEstimateMultiplier}x</span></span>
        </div>

        <div className="grid grid-cols-2 gap-4 pt-4 border-t border-slate-100">
          <div className="flex flex-col">
            <span className="text-[9px] font-bold text-text-muted uppercase tracking-widest">Agent Active</span>
            <span className="text-sm font-bold text-text-primary">{totalAgentTime.toFixed(1)}h</span>
          </div>
          <div className="flex flex-col">
            <span className="text-[9px] font-bold text-text-muted uppercase tracking-widest">Est. Manual</span>
            <span className="text-sm font-bold text-text-primary">{(hoursSaved + totalAgentTime).toFixed(1)}h</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export { TimeSavedGauge };
