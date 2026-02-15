import * as React from 'react';
import { MessageSquarePlus, Sparkles, Wand2, Info, ChevronRight } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export interface Annotation {
  id: string;
  text: string;
  agentResponse?: string;
  status: 'pending' | 'resolved' | 'applied';
}

export interface AnnotationLayerProps {
  children: React.ReactNode;
  annotations: Annotation[];
  onAddAnnotation?: (text: string) => void;
  className?: string;
}

const AnnotationLayer = ({
  children,
  annotations,
  onAddAnnotation,
  className
}: AnnotationLayerProps) => {
  return (
    <div className={cn('relative group', className)}>
      {/* Target Content */}
      <div className="relative z-0 group-hover:opacity-90 transition-opacity">
        {children}
      </div>

      {/* Annotation Markers (Gutter) */}
      <div className="absolute top-0 right-[-32px] h-full flex flex-col space-y-2 py-4">
        {annotations.map((ann) => (
          <Tooltip
            key={ann.id}
            content={
              <div className="p-2 max-w-xs">
                <p className="text-xs font-medium text-white mb-2">{ann.text}</p>
                {ann.agentResponse && (
                  <div className="mt-2 pt-2 border-t border-white/10">
                    <span className="text-[10px] font-bold text-brand-primary uppercase">Agent:</span>
                    <p className="text-[10px] italic text-slate-400 mt-0.5">{ann.agentResponse}</p>
                  </div>
                )}
              </div>
            }
          >
            <button className={cn(
              "h-8 w-8 rounded-full border-2 border-white shadow-lg flex items-center justify-center transition-all hover:scale-110",
              ann.status === 'applied' ? "bg-emerald-500 text-white" : "bg-brand-primary text-white"
            )}>
              <MessageSquarePlus size={14} />
            </button>
          </Tooltip>
        ))}

        <button
          onClick={() => onAddAnnotation?.("New refinement requested")}
          className="h-8 w-8 rounded-full bg-white border border-slate-200 text-text-muted shadow-sm flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all hover:text-brand-primary hover:border-brand-primary"
        >
          <Sparkles size={14} />
        </button>
      </div>

      {/* Overlay Reasoning Tags */}
      <div className="absolute top-2 left-2 flex flex-wrap gap-2 pointer-events-none">
        <div className="flex items-center space-x-1 bg-slate-900/80 backdrop-blur-md text-white text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity duration-500">
          <Info size={10} className="text-brand-primary" />
          <span>Anchored Reasoning</span>
        </div>
      </div>
    </div>
  );
};

export { AnnotationLayer };
