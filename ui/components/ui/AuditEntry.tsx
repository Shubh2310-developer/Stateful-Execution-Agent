import * as React from 'react';
import { Shield, ShieldAlert, ShieldCheck, History, User, Bot, Globe } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Badge } from './Badge';

export interface AuditEntryProps {
  timestamp: string;
  actor: { name: string; type: 'user' | 'agent'; id: string };
  action: string;
  resource: string;
  status: 'success' | 'failed';
  ip?: string;
  summary: string;
  className?: string;
}

const AuditEntry = ({
  timestamp,
  actor,
  action,
  resource,
  status,
  ip,
  summary,
  className
}: AuditEntryProps) => {
  return (
    <div className={cn(
      'group flex flex-col p-4 bg-white border-b border-slate-100 hover:bg-slate-50 transition-colors',
      className
    )}>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1.5 text-[10px] font-mono text-text-muted">
            <History className="h-3 w-3" />
            <span>{timestamp}</span>
          </div>
          <div className="h-3 w-[1px] bg-slate-200" />
          <div className="flex items-center space-x-1.5">
            {actor.type === 'user' ? <User className="h-3 w-3 text-blue-500" /> : <Bot className="h-3 w-3 text-indigo-500" />}
            <span className="text-[10px] font-bold text-text-primary uppercase tracking-tight">{actor.name}</span>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          {ip && (
            <div className="flex items-center space-x-1 text-[9px] text-text-muted font-mono bg-slate-100 px-1.5 py-0.5 rounded">
              <Globe className="h-2.5 w-2.5" />
              <span>{ip}</span>
            </div>
          )}
          <Badge
            variant={status === 'success' ? 'outline' : 'destructive'}
            className={cn(
              "text-[8px] h-4 py-0 uppercase",
              status === 'success' ? "text-emerald-600 border-emerald-100 bg-emerald-50" : ""
            )}
          >
            {status}
          </Badge>
        </div>
      </div>

      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-bold text-text-primary mb-1">
            {action} <span className="text-text-muted font-normal">on</span> <span className="text-brand-primary">{resource}</span>
          </p>
          <div className="flex items-start space-x-2 p-2 bg-slate-100/50 rounded border border-slate-100">
            <Shield className="h-3.5 w-3.5 text-text-muted mt-0.5 shrink-0" />
            <p className="text-xs text-text-secondary leading-relaxed italic">
              "{summary}"
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export { AuditEntry };
