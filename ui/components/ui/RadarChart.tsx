import * as React from 'react';
import { cn } from '../../lib/utils';

export interface RadarPoint {
  label: string;
  value: number; // 0 to 1
  fullMark: number;
}

export interface RadarChartProps {
  data: RadarPoint[];
  size?: number;
  className?: string;
}

const RadarChart = ({ data, size = 200, className }: RadarChartProps) => {
  const center = size / 2;
  const radius = (size / 2) * 0.8;
  const angleStep = (Math.PI * 2) / data.length;

  const getPointCoords = (index: number, value: number) => {
    const angle = index * angleStep - Math.PI / 2;
    const r = radius * value;
    return {
      x: center + r * Math.cos(angle),
      y: center + r * Math.sin(angle),
    };
  };

  const points = data.map((d, i) => getPointCoords(i, d.value));
  const polygonPath = points.map(p => `${p.x},${p.y}`).join(' ');

  // Grid levels (25%, 50%, 75%, 100%)
  const gridLevels = [0.25, 0.5, 0.75, 1.0];

  return (
    <div className={cn('flex flex-col items-center', className)}>
      <svg width={size} height={size} className="overflow-visible">
        {/* Grid Circles/Polygons */}
        {gridLevels.map(level => {
          const gridPoints = data.map((_, i) => getPointCoords(i, level));
          const path = gridPoints.map(p => `${p.x},${p.y}`).join(' ');
          return (
            <polygon
              key={level}
              points={path}
              fill="none"
              stroke="currentColor"
              className="text-slate-100"
              strokeWidth="1"
            />
          );
        })}

        {/* Axis Lines */}
        {data.map((_, i) => {
          const end = getPointCoords(i, 1);
          return (
            <line
              key={i}
              x1={center}
              y1={center}
              x2={end.x}
              y2={end.y}
              stroke="currentColor"
              className="text-slate-100"
              strokeWidth="1"
            />
          );
        })}

        {/* Data Area */}
        <polygon
          points={polygonPath}
          fill="var(--color-brand-primary)"
          fillOpacity="0.2"
          stroke="var(--color-brand-primary)"
          strokeWidth="2"
          strokeLinejoin="round"
          className="transition-all duration-1000 ease-out-ant"
        />

        {/* Data Points */}
        {points.map((p, i) => (
          <circle
            key={i}
            cx={p.x}
            cy={p.y}
            r="3"
            fill="var(--color-brand-primary)"
          />
        ))}

        {/* Labels */}
        {data.map((d, i) => {
          const pos = getPointCoords(i, 1.15);
          return (
            <text
              key={i}
              x={pos.x}
              y={pos.y}
              textAnchor="middle"
              className="text-[9px] font-bold fill-slate-500 uppercase tracking-tighter"
            >
              {d.label}
            </text>
          );
        })}
      </svg>
    </div>
  );
};

export { RadarChart };
