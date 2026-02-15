import * as React from 'react';
import { AlertCircle, RefreshCcw, Settings2, SkipForward, AlertTriangle } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { Button } from './Button';

export interface RecoveryPath {
  id: string;
  label: string;
  icon: 'retry' | 'modify' | 'skip';
  description: string;
  isRecommended?: boolean;
}

export interface RecoveryCardProps {
  errorType: 'agent' | 'system';
  errorMessage: string;
  paths: RecoveryPath[];
  onSelectPath: (pathId: string) => void;
  impactWarning?: string;
  className?: string;
}

const RecoveryCard = ({
  errorType,
  errorMessage,
  paths,
  onSelectPath,
  impactWarning,
  className
}: RecoveryCardProps) => {
  const isSystemError = errorType === 'system';

  const icons = {
    retry: <RefreshCcw className="h-4 w-4" />,
    modify: <Settings2 className="h-4 w-4" />,
    skip: <SkipForward className="h-4 w-4" />,
  };

  return (
    <Card className={cn(
      'p-6 border-red-200 bg-red-50/10 shadow-xl animate-in zoom-in-95 duration-300',
      className
    )}>
      <div className="flex items-start space-x-4 mb-6">
        <div className={cn(
          "h-12 w-12 rounded-full flex items-center justify-center shrink-0 shadow-lg",
          isSystemError ? "bg-slate-900 text-white" : "bg-red-500 text-white"
        )}>
          {isSystemError ? <Settings2 size={24} /> : <AlertCircle size={24} />}
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <span className={cn(
              "text-[10px] font-bold uppercase tracking-[0.2em]",
              isSystemError ? "text-text-muted" : "text-red-600"
            )}>
              {isSystemError ? 'System Infrastructure Failure' : 'Agent Logic Error'}
            </span>
          </div>
          <h2 className="text-xl font-bold text-text-primary tracking-tight mt-1">
            Execution Interrupted
          </h2>
          <p className="mt-3 text-sm text-text-secondary bg-white/50 p-3 rounded-ant-md border border-red-100 font-mono">
            {errorMessage}
          </p>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-xs font-bold text-text-muted uppercase tracking-widest px-1">
          Select Recovery Path
        </h3>
        <div className="grid grid-cols-1 gap-3">
          {paths.map((path) => (
            <button
              key={path.id}
              onClick={() => onSelectPath(path.id)}
              className={cn(
                'flex items-center p-4 text-left rounded-ant-lg border transition-all duration-200 group relative',
                path.isRecommended
                  ? 'bg-white border-brand-primary shadow-md ring-1 ring-brand-primary/20'
                  : 'bg-white border-slate-200 hover:border-brand-primary/50'
              )}
            >
              <div className={cn(
                "h-10 w-10 rounded-full flex items-center justify-center shrink-0 mr-4 transition-colors",
                path.isRecommended ? "bg-brand-primary text-white" : "bg-slate-100 text-text-muted group-hover:bg-brand-primary/10 group-hover:text-brand-primary"
              )}>
                {icons[path.icon]}
              </div>
              <div className="flex-1">
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-sm text-text-primary">
                    {path.label}
                  </span>
                  {path.isRecommended && (
                    <Badge variant="secondary" className="bg-brand-primary/10 text-brand-primary border-transparent text-[9px]">
                      Recommended
                    </Badge>
                  )}
                </div>
                <p className="text-xs text-text-secondary mt-1">
                  {path.description}
                </p>
              </div>
              <ChevronRight className="h-4 w-4 text-text-muted opacity-0 group-hover:opacity-100 transition-opacity" />
            </button>
          ))}
        </div>
      </div>

      {impactWarning && (
        <div className="mt-6 flex items-start space-x-2 p-3 bg-amber-50 rounded-ant-md border border-amber-200 text-[11px] text-amber-800 leading-relaxed">
          <AlertTriangle className="h-3.5 w-3.5 mt-0.5 shrink-0" />
          <p>
            <span className="font-bold uppercase tracking-tight mr-1">Impact Warning:</span>
            {impactWarning}
          </p>
        </div>
      )}
    </Card>
  );
};

export { RecoveryCard };
