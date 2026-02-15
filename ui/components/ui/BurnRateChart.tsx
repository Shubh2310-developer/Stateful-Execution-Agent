import * as React from 'react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export interface BurnRatePoint {
  timestamp: string;
  cost: number;
}

export interface BurnRateChartProps {
  data: BurnRatePoint[];
  limit: number;
  currency?: string;
  height?: number;
  className?: string;
}

const BurnRateChart = ({
  data,
  limit,
  currency = '$',
  height = 120,
  className
}: BurnRateChartProps) => {
  if (!data.length) return null;

  const maxCost = Math.max(...data.map(d => d.cost), limit * 0.5);
  const padding = 10;
  const width = 400; // Scalable via viewBox
  const innerWidth = width - (padding * 2);
  const innerHeight = height - (padding * 2);

  const points = data.map((d, i) => {
    const x = padding + (i / (data.length - 1)) * innerWidth;
    const y = height - padding - (d.cost / maxCost) * innerHeight;
    return `${x},${y}`;
  }).join(' L ');

  const limitY = height - padding - (limit / maxCost) * innerHeight;

  return (
    <div className={cn('flex flex-col space-y-2', className)}>
      <div className="flex items-center justify-between px-1">
        <span className="text-[10px] font-bold text-text-muted uppercase tracking-widest">Token Burn Rate</span>
        <div className="flex items-center space-x-2">
          <span className="text-xs font-bold text-text-primary">{currency}{data[data.length - 1].cost.toFixed(2)}/hr</span>
          <span className="text-[10px] text-text-muted">Limit: {currency}{limit}</span>
        </div>
      </div>

      <div className="relative bg-slate-50 border border-slate-100 rounded-ant-md overflow-hidden">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="w-full h-auto overflow-visible"
          style={{ height: height }}
        >
          {/* Limit Line */}
          {limitY >= padding && (
            <line
              x1="0"
              y1={limitY}
              x2={width}
              y2={limitY}
              stroke="#EF4444"
              strokeWidth="1"
              strokeDasharray="4 4"
              className="opacity-40"
            />
          )}

          {/* Area Fill */}
          <path
            d={`M ${padding},${height - padding} L ${points} L ${width - padding},${height - padding} Z`}
            className="fill-brand-primary opacity-5"
          />

          {/* Sparkline */}
          <path
            d={`M ${points}`}
            fill="none"
            stroke="var(--color-brand-primary, #3B82F6)"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />

          {/* End point dot */}
          <circle
            cx={padding + innerWidth}
            cy={height - padding - (data[data.length - 1].cost / maxCost) * innerHeight}
            r="3"
            fill="var(--color-brand-primary)"
            className="animate-pulse"
          />
        </svg>
      </div>

      <div className="flex justify-between px-1 text-[8px] font-bold text-text-muted uppercase tracking-tighter">
        <span>{data[0].timestamp}</span>
        <span>Current</span>
      </div>
    </div>
  );
};

export { BurnRateChart };
