import * as React from 'react';
import { Package, FileText, Database, Settings, ExternalLink, Activity } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Badge } from './Badge';

export interface ResourceInput {
  id: string;
  name: string;
  type: 'file' | 'api' | 'db' | 'tool';
  status?: 'active' | 'pending' | 'error';
  metadata?: string;
}

export interface ResourceCardProps {
  resources: ResourceInput[];
  title?: string;
  className?: string;
}

const ResourceCard = ({
  resources,
  title = "Step Resources",
  className
}: ResourceCardProps) => {
  const getIcon = (type: ResourceInput['type']) => {
    switch (type) {
      case 'file': return <FileText size={14} />;
      case 'api': return <Settings size={14} />;
      case 'db': return <Database size={14} />;
      case 'tool': return <Package size={14} />;
    }
  };

  const getStatusColor = (status?: ResourceInput['status']) => {
    switch (status) {
      case 'active': return 'bg-emerald-500';
      case 'pending': return 'bg-blue-500 animate-pulse';
      case 'error': return 'bg-red-500';
      default: return 'bg-slate-300';
    }
  };

  return (
    <div className={cn('flex flex-col bg-slate-50/50 border border-slate-200 rounded-ant-lg overflow-hidden', className)}>
      <div className="px-4 py-2 border-b border-slate-200 bg-white flex items-center justify-between">
        <h4 className="text-[10px] font-bold text-text-muted uppercase tracking-widest">{title}</h4>
        <Badge variant="outline" className="text-[8px] h-4 py-0 border-slate-200">{resources.length} Inputs</Badge>
      </div>

      <div className="divide-y divide-slate-100">
        {resources.map((res) => (
          <div key={res.id} className="px-4 py-3 flex items-center justify-between group hover:bg-white transition-colors">
            <div className="flex items-center space-x-3">
              <div className="p-1.5 bg-white border border-slate-200 rounded text-slate-500 shadow-sm group-hover:text-brand-primary group-hover:border-brand-primary/30 transition-colors">
                {getIcon(res.type)}
              </div>
              <div className="flex flex-col">
                <span className="text-xs font-bold text-text-primary tracking-tight">{res.name}</span>
                {res.metadata && <span className="text-[10px] text-text-muted font-mono">{res.metadata}</span>}
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <div className={cn("h-1.5 w-1.5 rounded-full", getStatusColor(res.status))} />
              <button className="text-text-muted hover:text-brand-primary opacity-0 group-hover:opacity-100 transition-all">
                <ExternalLink size={12} />
              </button>
            </div>
          </div>
        ))}
      </div>

      {resources.length === 0 && (
        <div className="p-8 text-center flex flex-col items-center">
          <Activity size={24} className="text-slate-200 mb-2" />
          <p className="text-[10px] text-text-muted font-bold uppercase">No Active Resources</p>
        </div>
      )}
    </div>
  );
};

export { ResourceCard };
