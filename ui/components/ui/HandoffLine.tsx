import * as React from 'react';
import { cn } from '../../lib/utils';

export interface HandoffLineProps {
  sourceId: string;
  targetId: string;
  status?: 'active' | 'completed' | 'failed';
  className?: string;
}

const HandoffLine = ({ status = 'active', className }: HandoffLineProps) => {
  const statusColors = {
    active: 'stroke-brand-primary',
    completed: 'stroke-emerald-500',
    failed: 'stroke-red-500',
  };

  return (
    <div className={cn('relative h-12 flex items-center justify-center overflow-visible', className)}>
      <svg className="w-full h-full" preserveAspectRatio="none">
        <defs>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="7"
            refX="9"
            refY="3.5"
            orient="auto"
          >
            <polygon points="0 0, 10 3.5, 0 7" className={cn('fill-current', statusColors[status])} />
          </marker>
        </defs>
        <line
          x1="0"
          y1="50%"
          x2="100%"
          y2="50%"
          strokeWidth="2"
          markerEnd="url(#arrowhead)"
          className={cn('transition-all duration-1000', statusColors[status])}
          strokeDasharray={status === 'active' ? '8 4' : 'none'}
        >
          {status === 'active' && (
            <animate
              attributeName="stroke-dashoffset"
              from="24"
              to="0"
              dur="1s"
              repeatCount="indefinite"
            />
          )}
        </line>
      </svg>
    </div>
  );
};

export { HandoffLine };
