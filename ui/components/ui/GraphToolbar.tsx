import * as React from 'react';
import { Maximize2, Minimize2, ZoomIn, ZoomOut, Scissors, GitMerge, MousePointer2, PanHand } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';
import { Separator } from './Separator';

export interface GraphToolbarProps {
  onZoomIn?: () => void;
  onZoomOut?: () => void;
  onReset?: () => void;
  onToggleTool?: (tool: string) => void;
  activeTool?: string;
  className?: string;
}

const GraphToolbar = ({
  onZoomIn,
  onZoomOut,
  onReset,
  onToggleTool,
  activeTool = 'select',
  className
}: GraphToolbarProps) => {
  const tools = [
    { id: 'select', icon: MousePointer2, label: 'Select' },
    { id: 'pan', icon: PanHand, label: 'Pan' },
    { id: 'scissors', icon: Scissors, label: 'Prune Relationship' },
    { id: 'merge', icon: GitMerge, label: 'Merge Concepts' },
  ];

  return (
    <div className={cn(
      'flex items-center space-x-1 p-1 bg-white/80 backdrop-blur-md border border-slate-200 rounded-ant-lg shadow-xl ring-1 ring-black/5',
      className
    )}>
      <div className="flex items-center px-1">
        {tools.map((tool) => (
          <Tooltip key={tool.id} content={tool.label}>
            <button
              onClick={() => onToggleTool?.(tool.id)}
              className={cn(
                'p-2 rounded-ant-md transition-all duration-200',
                activeTool === tool.id
                  ? 'bg-brand-primary text-white shadow-md'
                  : 'text-text-secondary hover:bg-slate-100 hover:text-text-primary'
              )}
            >
              <tool.icon size={18} />
            </button>
          </Tooltip>
        ))}
      </div>

      <Separator orientation="vertical" className="h-6 mx-1" />

      <div className="flex items-center px-1">
        <Tooltip content="Zoom In">
          <button onClick={onZoomIn} className="p-2 text-text-secondary hover:bg-slate-100 hover:text-text-primary rounded-ant-md">
            <ZoomIn size={18} />
          </button>
        </Tooltip>
        <Tooltip content="Zoom Out">
          <button onClick={onZoomOut} className="p-2 text-text-secondary hover:bg-slate-100 hover:text-text-primary rounded-ant-md">
            <ZoomOut size={18} />
          </button>
        </Tooltip>
        <Tooltip content="Fit to View">
          <button onClick={onReset} className="p-2 text-text-secondary hover:bg-slate-100 hover:text-text-primary rounded-ant-md">
            <Maximize2 size={18} />
          </button>
        </Tooltip>
      </div>
    </div>
  );
};

export { GraphToolbar };
