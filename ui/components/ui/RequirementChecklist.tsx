import * as React from 'react';
import { Check, X, Shield, ShieldCheck, ShieldAlert } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface Requirement {
  id: string;
  label: string;
  isMet: boolean;
  critical?: boolean;
}

export interface RequirementChecklistProps {
  requirements: Requirement[];
  title?: string;
  className?: string;
}

const RequirementChecklist = ({
  requirements,
  title = "Constraint Compliance",
  className
}: RequirementChecklistProps) => {
  const metCount = requirements.filter(r => r.isMet).length;
  const totalCount = requirements.length;
  const allMet = metCount === totalCount;

  return (
    <div className={cn('flex flex-col space-y-4', className)}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Shield className="h-4 w-4 text-brand-primary" />
          <h3 className="text-sm font-bold text-text-primary uppercase tracking-wider">
            {title}
          </h3>
        </div>
        <div className={cn(
          "text-[10px] font-bold px-2 py-0.5 rounded-full border",
          allMet
            ? "text-emerald-700 bg-emerald-50 border-emerald-100"
            : "text-amber-700 bg-amber-50 border-amber-100"
        )}>
          {metCount}/{totalCount} Requirements
        </div>
      </div>

      <div className="space-y-2">
        {requirements.map((req) => (
          <div
            key={req.id}
            className={cn(
              'flex items-center justify-between p-3 rounded-ant-md border transition-all duration-200',
              req.isMet
                ? 'bg-white border-slate-100 opacity-100'
                : 'bg-slate-50 border-slate-200 opacity-80'
            )}
          >
            <div className="flex items-center space-x-3">
              <div className={cn(
                "flex h-5 w-5 items-center justify-center rounded-full shrink-0",
                req.isMet ? "bg-emerald-500 text-white" : "bg-slate-200 text-slate-400"
              )}>
                {req.isMet ? <Check className="h-3 w-3 stroke-[3px]" /> : <X className="h-3 w-3" />}
              </div>
              <span className={cn(
                "text-sm font-medium",
                req.isMet ? "text-text-primary" : "text-text-muted line-through decoration-slate-400"
              )}>
                {req.label}
              </span>
            </div>

            {req.critical && !req.isMet && (
              <div className="flex items-center space-x-1 text-red-600">
                <ShieldAlert className="h-3.5 w-3.5" />
                <span className="text-[10px] font-bold uppercase tracking-tight">Violation</span>
              </div>
            )}

            {req.critical && req.isMet && (
              <ShieldCheck className="h-4 w-4 text-emerald-500" />
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export { RequirementChecklist };
