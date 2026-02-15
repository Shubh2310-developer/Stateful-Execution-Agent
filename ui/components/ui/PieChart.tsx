import * as React from 'react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export interface PieData {
  label: string;
  value: number;
  color: string;
}

export interface PieChartProps {
  data: PieData[];
  size?: number;
  className?: string;
  innerRadius?: number; // For donut chart
}

const PieChart = ({ data, size = 160, innerRadius = 40, className }: PieChartProps) => {
  const total = data.reduce((acc, d) => acc + d.value, 0);
  let cumulativeAngle = 0;

  const getCoordinatesForPercent = (percent: number) => {
    const x = Math.cos(2 * Math.PI * percent);
    const y = Math.sin(2 * Math.PI * percent);
    return [x, y];
  };

  return (
    <div className={cn('flex items-center space-x-6', className)}>
      <svg width={size} height={size} viewBox="-1 -1 2 2" className="transform -rotate-90">
        {data.map((slice, i) => {
          const startPercent = cumulativeAngle / total;
          cumulativeAngle += slice.value;
          const endPercent = cumulativeAngle / total;

          const [startX, startY] = getCoordinatesForPercent(startPercent);
          const [endX, endY] = getCoordinatesForPercent(endPercent);

          const largeArcFlag = endPercent - startPercent > 0.5 ? 1 : 0;

          const pathData = [
            `M ${startX} ${startY}`,
            `A 1 1 0 ${largeArcFlag} 1 ${endX} ${endY}`,
            `L 0 0`,
          ].join(' ');

          return (
            <path
              key={i}
              d={pathData}
              fill={slice.color}
              className="transition-all duration-300 hover:opacity-80 cursor-pointer"
            />
          );
        })}
        {innerRadius > 0 && (
          <circle cx="0" cy="0" r={innerRadius / (size / 2)} fill="white" />
        )}
      </svg>

      <div className="flex flex-col space-y-2">
        {data.map((slice, i) => (
          <div key={i} className="flex items-center space-x-2">
            <div className="h-2 w-2 rounded-full" style={{ backgroundColor: slice.color }} />
            <span className="text-[10px] font-bold text-text-primary uppercase tracking-tighter truncate max-w-[80px]">
              {slice.label}
            </span>
            <span className="text-[10px] text-text-muted font-mono">
              {Math.round((slice.value / total) * 100)}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export { PieChart };
