import * as React from 'react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export interface GanttTask {
  id: string;
  label: string;
  start: number; // Percentage 0-100
  duration: number; // Percentage 0-100
  type?: 'autonomous' | 'manual' | 'tool';
  status?: 'completed' | 'failed' | 'running';
}

export interface GanttChartProps {
  tasks: GanttTask[];
  className?: string;
}

const GanttChart = ({ tasks, className }: GanttChartProps) => {
  const typeColors = {
    autonomous: 'bg-brand-primary',
    manual: 'bg-amber-500',
    tool: 'bg-indigo-500',
  };

  const statusOpacities = {
    completed: 'opacity-100',
    failed: 'opacity-50 saturate-50',
    running: 'animate-pulse',
  };

  return (
    <div className={cn('w-full border border-slate-200 rounded-ant-lg bg-white overflow-hidden', className)}>
      <div className="grid grid-cols-[160px_1fr] border-b border-slate-100 bg-slate-50/50">
        <div className="p-3 text-[10px] font-bold text-text-muted uppercase tracking-widest border-r border-slate-100">
          Step / Action
        </div>
        <div className="p-3 text-[10px] font-bold text-text-muted uppercase tracking-widest relative">
          Timeline
          <div className="absolute inset-y-0 left-1/4 w-px bg-slate-200/50" />
          <div className="absolute inset-y-0 left-2/4 w-px bg-slate-200/50" />
          <div className="absolute inset-y-0 left-3/4 w-px bg-slate-200/50" />
        </div>
      </div>

      <div className="divide-y divide-slate-100">
        {tasks.map((task) => (
          <div key={task.id} className="grid grid-cols-[160px_1fr] group hover:bg-slate-50 transition-colors">
            <div className="p-3 text-xs font-medium text-text-primary border-r border-slate-100 truncate">
              {task.label}
            </div>
            <div className="p-3 relative flex items-center h-10">
              <Tooltip content={`${task.label}: ${task.duration}% duration`}>
                <div
                  className={cn(
                    'h-4 rounded-full shadow-sm transition-all duration-500 group-hover:scale-y-110',
                    typeColors[task.type || 'autonomous'],
                    statusOpacities[task.status || 'completed']
                  )}
                  style={{
                    marginLeft: `${task.start}%`,
                    width: `${task.duration}%`,
                  }}
                />
              </Tooltip>
            </div>
          </div>
        ))}
      </div>

      <div className="p-3 bg-slate-50/30 border-t border-slate-100 flex items-center space-x-6 text-[9px] font-bold text-text-muted uppercase tracking-tighter">
        <div className="flex items-center">
          <div className="w-2 h-2 rounded-full bg-brand-primary mr-1.5" />
          Autonomous
        </div>
        <div className="flex items-center">
          <div className="w-2 h-2 rounded-full bg-amber-500 mr-1.5" />
          Manual
        </div>
        <div className="flex items-center">
          <div className="w-2 h-2 rounded-full bg-indigo-500 mr-1.5" />
          Tool Call
        </div>
      </div>
    </div>
  );
};

export { GanttChart };
