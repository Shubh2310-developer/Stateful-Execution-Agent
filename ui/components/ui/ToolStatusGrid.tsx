import * as React from 'react';
import { cn } from '../../lib/utils';

export interface ToolStatus {
  id: string;
  name: string;
  status: 'online' | 'degraded' | 'offline';
  latency?: number;
}

export interface ToolStatusGridProps {
  tools: ToolStatus[];
  className?: string;
}

const ToolStatusGrid = ({ tools, className }: ToolStatusGridProps) => {
  const getStatusColor = (status: ToolStatus['status']) => {
    switch (status) {
      case 'online': return 'bg-status-success';
      case 'degraded': return 'bg-status-warning';
      case 'offline': return 'bg-status-error';
      default: return 'bg-slate-300';
    }
  };

  const getStatusText = (status: ToolStatus['status']) => {
    switch (status) {
      case 'online': return 'Stable';
      case 'degraded': return 'High Latency';
      case 'offline': return 'Disconnected';
      default: return 'Unknown';
    }
  };

  return (
    <div className={cn('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3', className)}>
      {tools.map((tool) => (
        <div
          key={tool.id}
          className="flex items-center justify-between p-3 bg-white border border-slate-100 rounded-ant-md shadow-sm hover:border-slate-200 transition-all duration-200"
        >
          <div className="flex items-center space-x-3">
            <div className={cn("h-2.5 w-2.5 rounded-full animate-pulse", getStatusColor(tool.status))} />
            <div className="flex flex-col">
              <span className="text-xs font-bold text-text-primary uppercase tracking-tight">
                {tool.name}
              </span>
              <span className="text-[10px] text-text-muted">
                {getStatusText(tool.status)}
              </span>
            </div>
          </div>
          {tool.latency && (
            <div className="text-right">
              <span className={cn(
                "text-[10px] font-mono font-bold",
                tool.latency > 1000 ? "text-status-warning" : "text-text-muted"
              )}>
                {tool.latency}ms
              </span>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export { ToolStatusGrid };
