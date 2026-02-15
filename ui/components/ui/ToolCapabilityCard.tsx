import * as React from 'react';
import { Search, Filter, Terminal, Plus, ShieldCheck, AlertCircle, ExternalLink } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { Badge } from './Badge';
import { Button } from './Button';

export interface ToolCapability {
  id: string;
  name: string;
  description: string;
  status: 'connected' | 'auth_required' | 'error' | 'disabled';
  category: string;
  inputs: string[];
  successRate: number;
  avgLatency: number;
}

export interface ToolCapabilityCardProps {
  tool: ToolCapability;
  onConnect?: (id: string) => void;
  onConfigure?: (id: string) => void;
  className?: string;
}

const ToolCapabilityCard = ({
  tool,
  onConnect,
  onConfigure,
  className
}: ToolCapabilityCardProps) => {
  const statusConfigs = {
    connected: { label: 'Connected', color: 'bg-emerald-50 text-emerald-700 border-emerald-100', icon: <ShieldCheck className="h-3 w-3" /> },
    auth_required: { label: 'Auth Required', color: 'bg-amber-50 text-amber-700 border-amber-100', icon: <AlertCircle className="h-3 w-3" /> },
    error: { label: 'Error', color: 'bg-red-50 text-red-700 border-red-100', icon: <AlertCircle className="h-3 w-3" /> },
    disabled: { label: 'Disabled', color: 'bg-slate-50 text-slate-500 border-slate-200', icon: null },
  };

  const config = statusConfigs[tool.status];

  return (
    <Card className={cn('p-5 flex flex-col h-full hover:border-brand-primary/30 transition-all duration-300', className)}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 bg-slate-100 rounded-ant-md flex items-center justify-center text-slate-600">
            <Terminal className="h-5 w-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-text-primary tracking-tight">{tool.name}</h3>
            <span className="text-[10px] text-text-muted font-bold uppercase tracking-widest">{tool.category}</span>
          </div>
        </div>
        <div className={cn(
          "flex items-center space-x-1.5 px-2 py-0.5 rounded-full border text-[9px] font-bold uppercase tracking-wider",
          config.color
        )}>
          {config.icon}
          <span>{config.label}</span>
        </div>
      </div>

      <p className="text-xs text-text-secondary leading-relaxed mb-6 flex-1">
        {tool.description}
      </p>

      <div className="space-y-4">
        <div className="space-y-2">
          <span className="text-[9px] font-bold text-text-muted uppercase tracking-widest">Required Inputs</span>
          <div className="flex flex-wrap gap-1.5">
            {tool.inputs.map(input => (
              <Badge key={input} variant="outline" className="text-[8px] h-4 py-0 border-slate-200 text-slate-500">
                {input}
              </Badge>
            ))}
          </div>
        </div>

        <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
          <div className="flex space-x-4">
            <div className="flex flex-col">
              <span className="text-[9px] font-bold text-text-muted uppercase">Success</span>
              <span className="text-xs font-bold text-emerald-600">{tool.successRate}%</span>
            </div>
            <div className="flex flex-col">
              <span className="text-[9px] font-bold text-text-muted uppercase">Latency</span>
              <span className="text-xs font-bold text-text-primary">{tool.avgLatency}ms</span>
            </div>
          </div>

          <div className="flex space-x-2">
            {tool.status === 'auth_required' ? (
              <Button size="sm" onClick={() => onConnect?.(tool.id)} className="h-8 text-[10px]">
                <ExternalLink className="h-3 w-3 mr-1.5" />
                Connect
              </Button>
            ) : (
              <Button size="sm" variant="secondary" onClick={() => onConfigure?.(tool.id)} className="h-8 text-[10px]">
                Configure
              </Button>
            )}
          </div>
        </div>
      </div>
    </Card>
  );
};

export { ToolCapabilityCard };
