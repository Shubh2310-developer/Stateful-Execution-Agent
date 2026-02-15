import * as React from 'react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';
import { Badge } from './Badge';

export interface KnowledgeGraphNodeProps {
  label: string;
  category: 'preference' | 'fact' | 'pattern' | 'constraint';
  confidence: number; // 0 to 1
  recency: number; // 0 to 1 (1 is very recent)
  isActive?: boolean;
  onClick?: () => void;
  className?: string;
}

const KnowledgeGraphNode = ({
  label,
  category,
  confidence,
  recency,
  isActive = false,
  onClick,
  className
}: KnowledgeGraphNodeProps) => {
  const categoryColors = {
    preference: 'bg-blue-500 border-blue-600 shadow-blue-500/20',
    fact: 'bg-emerald-500 border-emerald-600 shadow-emerald-500/20',
    pattern: 'bg-amber-500 border-amber-600 shadow-amber-500/20',
    constraint: 'bg-red-500 border-red-600 shadow-red-500/20',
  };

  const nodeSize = 60 + (confidence * 40); // 60px to 100px based on confidence

  return (
    <Tooltip content={
      <div className="p-2 space-y-1">
        <p className="font-bold text-xs">{label}</p>
        <div className="flex justify-between text-[10px]">
          <span>Confidence:</span>
          <span className="font-mono">{Math.round(confidence * 100)}%</span>
        </div>
        <div className="flex justify-between text-[10px]">
          <span>Category:</span>
          <span className="uppercase font-bold">{category}</span>
        </div>
      </div>
    }>
      <div
        onClick={onClick}
        className={cn(
          'relative flex flex-col items-center justify-center rounded-full border-4 text-white transition-all duration-500 cursor-pointer hover:scale-110 shadow-xl group',
          categoryColors[category],
          isActive && 'ring-4 ring-white ring-offset-4 ring-offset-brand-primary scale-110 z-10',
          className
        )}
        style={{
          width: nodeSize,
          height: nodeSize,
          opacity: 0.3 + (recency * 0.7) // Node brightness reflects recency
        }}
      >
        <span className="text-[10px] font-bold text-center px-2 line-clamp-2 leading-tight uppercase tracking-tighter">
          {label}
        </span>

        {/* Confidence Aura */}
        <div
          className="absolute inset-0 rounded-full animate-ping opacity-20"
          style={{
            animationDuration: `${3 - confidence * 2}s`,
            backgroundColor: 'currentColor'
          }}
        />

        {/* Category Badge (Floating) */}
        <div className="absolute -top-1 -right-1 scale-75 opacity-0 group-hover:opacity-100 transition-opacity">
          <Badge className="bg-white text-slate-900 border-slate-200">
            {category[0].toUpperCase()}
          </Badge>
        </div>
      </div>
    </Tooltip>
  );
};

export { KnowledgeGraphNode };
