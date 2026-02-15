import * as React from 'react';
import { Zap, Gauge, Cpu, Check } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { Badge } from './Badge';

export interface ModelOption {
  id: string;
  name: string;
  provider: string;
  pricePer1k: string;
  latency: 'low' | 'medium' | 'high';
  capabilities: string[];
  isRecommended?: boolean;
}

export interface ModelSelectorProps {
  models: ModelOption[];
  selectedId: string;
  onSelect: (id: string) => void;
  className?: string;
}

const ModelSelector = ({
  models,
  selectedId,
  onSelect,
  className
}: ModelSelectorProps) => {
  return (
    <div className={cn('grid grid-cols-1 md:grid-cols-3 gap-4', className)}>
      {models.map((model) => {
        const isSelected = selectedId === model.id;

        return (
          <button
            key={model.id}
            onClick={() => onSelect(model.id)}
            className={cn(
              'flex flex-col text-left p-4 rounded-ant-lg border-2 transition-all duration-300 relative group',
              isSelected
                ? 'border-brand-primary bg-brand-primary/[0.02] shadow-md'
                : 'border-slate-200 bg-white hover:border-slate-300'
            )}
          >
            {isSelected && (
              <div className="absolute top-2 right-2 h-5 w-5 bg-brand-primary rounded-full flex items-center justify-center text-white">
                <Check className="h-3 w-3 stroke-[3px]" />
              </div>
            )}

            <div className="mb-3">
              <div className="flex items-center space-x-2 mb-1">
                <span className="text-sm font-bold text-text-primary">{model.name}</span>
                {model.isRecommended && (
                  <Badge variant="secondary" className="bg-emerald-100 text-emerald-700 text-[8px] h-4">Recommended</Badge>
                )}
              </div>
              <span className="text-[10px] text-text-muted uppercase font-bold tracking-widest">{model.provider}</span>
            </div>

            <div className="flex-1 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center text-[10px] text-text-secondary font-medium">
                  <Zap className="h-3 w-3 mr-1 text-amber-500" />
                  <span>{model.pricePer1k}/1k tokens</span>
                </div>
                <div className="flex items-center text-[10px] text-text-secondary font-medium">
                  <Gauge className="h-3 w-3 mr-1 text-blue-500" />
                  <span className="capitalize">{model.latency} Latency</span>
                </div>
              </div>

              <div className="flex flex-wrap gap-1">
                {model.capabilities.map(cap => (
                  <span key={cap} className="px-1.5 py-0.5 bg-slate-100 text-[9px] text-slate-600 rounded font-bold uppercase">
                    {cap}
                  </span>
                ))}
              </div>
            </div>
          </button>
        );
      })}
    </div>
  );
};

export { ModelSelector };
