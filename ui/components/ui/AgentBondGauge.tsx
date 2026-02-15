import * as React from 'react';
import { Heart, Shield, Zap, TrendingUp } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export interface AgentBondGaugeProps {
  alignment: number; // 0 to 100
  trust: number; // 0 to 100
  historyCount: number;
  className?: string;
}

const AgentBondGauge = ({
  alignment,
  trust,
  historyCount,
  className
}: AgentBondGaugeProps) => {
  const radius = 36;
  const circumference = 2 * Math.PI * radius;
  const alignmentOffset = circumference - (alignment / 100) * circumference;
  const trustOffset = circumference - (trust / 100) * circumference;

  return (
    <div className={cn('relative p-6 bg-white border border-slate-200 rounded-ant-xl shadow-sm overflow-hidden group', className)}>
      {/* Background decoration */}
      <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
        <Heart size={80} className="text-brand-primary" fill="currentColor" />
      </div>

      <div className="relative z-10 flex items-center space-x-8">
        <div className="relative flex items-center justify-center">
          <svg width="100" height="100" className="-rotate-90">
            {/* Background Track */}
            <circle
              cx="50"
              cy="50"
              r={radius}
              className="fill-none stroke-slate-100"
              strokeWidth="8"
            />
            {/* Alignment Track (Outer) */}
            <circle
              cx="50"
              cy="50"
              r={radius}
              className="fill-none stroke-brand-primary transition-all duration-1000 ease-out-ant"
              strokeWidth="8"
              strokeDasharray={circumference}
              strokeDashoffset={alignmentOffset}
              strokeLinecap="round"
            />
            {/* Trust Track (Inner) */}
            <circle
              cx="50"
              cy="50"
              r={radius - 12}
              className="fill-none stroke-emerald-500 transition-all duration-1000 ease-out-ant"
              strokeWidth="6"
              strokeDasharray={2 * Math.PI * (radius - 12)}
              strokeDashoffset={(2 * Math.PI * (radius - 12)) - (trust / 100) * (2 * Math.PI * (radius - 12))}
              strokeLinecap="round"
              opacity="0.6"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-xl font-bold text-text-primary leading-none">{alignment}%</span>
            <span className="text-[8px] font-bold text-text-muted uppercase tracking-tighter">Aligned</span>
          </div>
        </div>

        <div className="flex-1 space-y-4">
          <div>
            <h4 className="text-sm font-bold text-text-primary uppercase tracking-widest mb-1">Human-Agent Bond</h4>
            <p className="text-[10px] text-text-muted leading-relaxed">Your agent is learning your style patterns. High alignment reduces manual refinement.</p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center space-x-2">
              <div className="p-1.5 bg-emerald-50 rounded text-emerald-600">
                <Shield size={14} />
              </div>
              <div>
                <div className="text-[10px] font-bold text-text-primary">{trust}%</div>
                <div className="text-[8px] text-text-muted uppercase font-bold">Trust</div>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <div className="p-1.5 bg-blue-50 rounded text-brand-primary">
                <TrendingUp size={14} />
              </div>
              <div>
                <div className="text-[10px] font-bold text-text-primary">{historyCount}</div>
                <div className="text-[8px] text-text-muted uppercase font-bold">Patterns</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export { AgentBondGauge };
