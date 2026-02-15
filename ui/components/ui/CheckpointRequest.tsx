import * as React from 'react';
import { AlertCircle, Check, X, ShieldAlert, ArrowRight, UserCheck } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';
import { Badge } from './Badge';

export interface CheckpointRequestProps {
  title: string;
  description: string;
  impact: 'low' | 'medium' | 'high';
  onApprove: () => void;
  onDeny: () => void;
  onModify?: () => void;
  className?: string;
}

const CheckpointRequest = ({
  title,
  description,
  impact,
  onApprove,
  onDeny,
  onModify,
  className
}: CheckpointRequestProps) => {
  const impactStyles = {
    low: 'bg-blue-50 text-blue-700 border-blue-100',
    medium: 'bg-amber-50 text-amber-700 border-amber-100 shadow-amber-500/10',
    high: 'bg-red-50 text-red-700 border-red-100 shadow-red-500/10 animate-pulse-subtle',
  };

  return (
    <div className={cn(
      'relative p-6 border-2 rounded-ant-xl transition-all duration-300 shadow-lg bg-white',
      impactStyles[impact],
      className
    )}>
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className={cn(
            "p-2.5 rounded-full shadow-inner",
            impact === 'high' ? 'bg-red-500 text-white' : 'bg-white border border-current'
          )}>
            <ShieldAlert size={20} />
          </div>
          <div>
            <div className="flex items-center space-x-2 mb-1">
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] opacity-70">Human Intervention Required</span>
              <Badge variant="secondary" className="text-[8px] h-4 py-0 uppercase">{impact} Impact</Badge>
            </div>
            <h3 className="text-base font-bold tracking-tight">{title}</h3>
          </div>
        </div>
      </div>

      <p className="text-sm font-medium leading-relaxed mb-8 opacity-90">
        {description}
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <Button
          onClick={onApprove}
          className={cn(
            "h-12 font-bold text-white shadow-xl shadow-emerald-500/20 transition-all active:scale-95",
            impact === 'high' ? 'bg-red-600 hover:bg-red-700' : 'bg-emerald-600 hover:bg-emerald-700'
          )}
        >
          <Check size={18} className="mr-2 stroke-[3px]" />
          Approve and Continue
        </Button>

        <div className="flex gap-2">
          {onModify && (
            <Button
              variant="secondary"
              onClick={onModify}
              className="flex-1 h-12 border-slate-200 hover:border-brand-primary text-text-primary font-bold"
            >
              Modify
            </Button>
          )}
          <Button
            variant="ghost"
            onClick={onDeny}
            className="flex-1 h-12 text-status-error hover:bg-red-50 font-bold"
          >
            <X size={18} className="mr-2" />
            Abort Task
          </Button>
        </div>
      </div>

      <div className="mt-6 pt-4 border-t border-current/10 flex items-center justify-between opacity-60">
        <div className="flex items-center space-x-2 text-[10px] font-bold uppercase">
          <UserCheck size={12} />
          <span>Operator Override Enabled</span>
        </div>
        <span className="text-[10px] font-mono">CODE: HITL-SEC-049</span>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        @keyframes pulse-subtle {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.01); }
        }
        .animate-pulse-subtle {
          animation: pulse-subtle 3s ease-in-out infinite;
        }
      `}} />
    </div>
  );
};

export { CheckpointRequest };
