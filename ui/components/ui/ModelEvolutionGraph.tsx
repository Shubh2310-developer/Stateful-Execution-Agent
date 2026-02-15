import * as React from 'react';
import { cn } from '../../lib/utils';

export interface ModelEvolutionDataPoint {
  date: string;
  accuracy: number; // 0 to 1
  humanInterventionRate: number; // 0 to 1
  label?: string;
}

export interface ModelEvolutionGraphProps {
  data: ModelEvolutionDataPoint[];
  height?: number;
  className?: string;
}

const ModelEvolutionGraph = ({
  data,
  height = 240,
  className
}: ModelEvolutionGraphProps) => {
  if (!data.length) return null;

  const padding = 40;
  const width = 600; // Aspect ratio will handle scale
  const innerWidth = width - padding * 2;
  const innerHeight = height - padding * 2;

  const getX = (index: number) => padding + (index / (data.length - 1)) * innerWidth;
  const getY = (value: number) => height - padding - (value * innerHeight);

  // Line paths
  const accuracyPath = data.map((d, i) => `${getX(i)},${getY(d.accuracy)}`).join(' L ');
  const interventionPath = data.map((d, i) => `${getX(i)},${getY(1 - d.humanInterventionRate)}`).join(' L ');

  return (
    <div className={cn('w-full border border-slate-200 rounded-ant-lg bg-white p-4', className)}>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h4 className="text-sm font-bold text-text-primary uppercase tracking-widest">Model Alignment Evolution</h4>
          <p className="text-[10px] text-text-muted font-medium">Tracking improvement through RLHF cycles</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-1.5">
            <div className="h-2 w-2 rounded-full bg-brand-primary" />
            <span className="text-[9px] font-bold text-text-muted uppercase">Accuracy</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <div className="h-2 w-2 rounded-full bg-amber-500" />
            <span className="text-[9px] font-bold text-text-muted uppercase">Autonomy</span>
          </div>
        </div>
      </div>

      <svg
        viewBox={`0 0 ${width} ${height}`}
        className="w-full h-auto overflow-visible"
        style={{ height: height }}
      >
        {/* Grid Lines */}
        {[0, 0.25, 0.5, 0.75, 1].map((level) => (
          <g key={level}>
            <line
              x1={padding}
              y1={getY(level)}
              x2={width - padding}
              y2={getY(level)}
              stroke="currentColor"
              className="text-slate-100"
              strokeWidth="1"
            />
            <text
              x={padding - 10}
              y={getY(level)}
              textAnchor="end"
              alignmentBaseline="middle"
              className="text-[8px] font-bold fill-slate-400"
            >
              {Math.round(level * 100)}%
            </text>
          </g>
        ))}

        {/* Data Lines */}
        <path
          d={`M ${interventionPath}`}
          fill="none"
          stroke="var(--color-status-warning, #F59E0B)"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="transition-all duration-1000 ease-in-out"
          opacity="0.3"
        />
        <path
          d={`M ${accuracyPath}`}
          fill="none"
          stroke="var(--color-brand-primary, #3B82F6)"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="transition-all duration-1000 ease-in-out"
        />

        {/* Data Points (Dots) */}
        {data.map((d, i) => (
          <g key={i} className="group cursor-pointer">
            <circle
              cx={getX(i)}
              cy={getY(d.accuracy)}
              r="4"
              fill="var(--color-brand-primary)"
              className="transition-all duration-300 group-hover:r-6"
            />
            {i % Math.ceil(data.length / 5) === 0 && (
              <text
                x={getX(i)}
                y={height - 10}
                textAnchor="middle"
                className="text-[8px] font-bold fill-slate-400 uppercase"
              >
                {d.date}
              </text>
            )}
          </g>
        ))}
      </svg>
    </div>
  );
};

export { ModelEvolutionGraph };
