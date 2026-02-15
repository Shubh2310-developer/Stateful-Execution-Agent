import * as React from 'react';
import { ShieldCheck, ShieldAlert, Key, Info } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export interface IntegrityBadgeProps {
  signature: string;
  timestamp: string;
  status?: 'verified' | 'unverified' | 'tampered';
  className?: string;
}

const IntegrityBadge = ({
  signature,
  timestamp,
  status = 'verified',
  className
}: IntegrityBadgeProps) => {
  const configs = {
    verified: {
      color: 'text-emerald-600 border-emerald-200 bg-emerald-50',
      icon: <ShieldCheck className="h-3 w-3" />,
      text: 'Cryptographically Verified'
    },
    unverified: {
      color: 'text-slate-600 border-slate-200 bg-slate-50',
      icon: <Info className="h-3 w-3" />,
      text: 'Verification Pending'
    },
    tampered: {
      color: 'text-red-600 border-red-200 bg-red-50 animate-pulse',
      icon: <ShieldAlert className="h-3 w-3" />,
      text: 'Integrity Compromised'
    },
  };

  const config = configs[status];

  return (
    <Tooltip content={
      <div className="p-2 space-y-2 max-w-[240px]">
        <p className="font-bold text-xs uppercase tracking-widest">{config.text}</p>
        <div className="space-y-1">
          <span className="text-[9px] text-white/60 uppercase font-bold">Signature ID</span>
          <code className="block p-1 bg-white/10 rounded text-[9px] break-all font-mono">{signature}</code>
        </div>
        <div className="flex justify-between items-center pt-1 border-t border-white/10">
          <span className="text-[9px] text-white/60 uppercase font-bold">Signed At</span>
          <span className="text-[9px] font-mono">{timestamp}</span>
        </div>
      </div>
    }>
      <div className={cn(
        'inline-flex items-center space-x-2 px-2 py-0.5 rounded-full border transition-all cursor-help hover:shadow-sm',
        config.color,
        className
      )}>
        {config.icon}
        <span className="text-[9px] font-bold uppercase tracking-[0.15em]">{status}</span>
        <div className="h-2.5 w-[1px] bg-current opacity-20" />
        <Key className="h-2.5 w-2.5 opacity-50" />
      </div>
    </Tooltip>
  );
};

export { IntegrityBadge };
