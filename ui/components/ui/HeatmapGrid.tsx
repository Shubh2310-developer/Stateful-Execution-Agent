import * as React from 'react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export interface HeatmapValue {
  x: string | number;
  y: string | number;
  value: number; // 0 to 1
  label?: string;
}

export interface HeatmapGridProps {
  data: HeatmapValue[];
  xLabels: string[];
  yLabels: string[];
  className?: string;
}

const HeatmapGrid = ({ data, xLabels, yLabels, className }: HeatmapGridProps) => {
  const getValueAt = (x: string, y: string) => {
    return data.find(d => d.x === x && d.y === y);
  };

  const getColor = (value: number) => {
    // Brand primary with varying opacity
    return `rgba(59, 130, 246, ${0.1 + value * 0.9})`;
  };

  return (
    <div className={cn('flex flex-col overflow-x-auto', className)}>
      <div className="flex">
        {/* Y-Axis Corner */}
        <div className="w-20 h-8 shrink-0" />
        {/* X-Axis Labels */}
        <div className="flex">
          {xLabels.map(x => (
            <div key={x} className="w-8 h-8 flex items-center justify-center text-[9px] font-bold text-text-muted uppercase tracking-tighter">
              {x}
            </div>
          ))}
        </div>
      </div>

      <div className="flex flex-col">
        {yLabels.map(y => (
          <div key={y} className="flex">
            {/* Y-Axis Label */}
            <div className="w-20 h-8 flex items-center justify-end pr-3 text-[9px] font-bold text-text-muted uppercase tracking-tighter">
              {y}
            </div>
            {/* Grid Row */}
            <div className="flex">
              {xLabels.map(x => {
                const item = getValueAt(x, y);
                const val = item?.value || 0;
                return (
                  <Tooltip key={`${x}-${y}`} content={`${item?.label || 'Value'}: ${Math.round(val * 100)}%`}>
                    <div
                      className="w-8 h-8 border border-white transition-all duration-300 hover:scale-110 hover:z-10 hover:rounded-sm cursor-help"
                      style={{ backgroundColor: getColor(val) }}
                    />
                  </Tooltip>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export { HeatmapGrid };
