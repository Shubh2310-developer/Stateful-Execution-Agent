import * as React from 'react';
import { Check, Circle } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Skeleton } from './Skeleton';

export type StepStatus = 'completed' | 'running' | 'pending';

export interface Step {
  id: string | number;
  label: string;
  description?: string;
  status: StepStatus;
}

export interface StepIndicatorProps {
  steps: Step[];
  orientation?: 'horizontal' | 'vertical';
  className?: string;
  isLoading?: boolean;
}

const StepIndicator = ({ steps, orientation = 'vertical', className, isLoading = false }: StepIndicatorProps) => {
  const isVertical = orientation === 'vertical';

  if (isLoading) {
    return (
      <div className={cn(
        'flex',
        isVertical ? 'flex-col' : 'flex-row items-start justify-between w-full',
        className
      )}>
        {[1, 2, 3].map((i) => (
          <div key={i} className={cn('relative flex', isVertical ? 'flex-row mb-8' : 'flex-col items-center flex-1')}>
            <div className="h-6 w-6 rounded-full bg-slate-100 border-2 border-slate-200 animate-pulse" />
            <div className={cn(isVertical ? 'ml-4 pt-0.5' : 'mt-3 text-center')}>
              <Skeleton className="h-4 w-24 mb-2" />
              <Skeleton className="h-3 w-32" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className={cn(
      'flex',
      isVertical ? 'flex-col' : 'flex-row items-start justify-between w-full',
      className
    )}>
      {steps.map((step, index) => {
        const isLast = index === steps.length - 1;

        return (
          <div
            key={step.id}
            className={cn(
              'relative flex',
              isVertical ? 'flex-row mb-8 last:mb-0' : 'flex-col items-center flex-1'
            )}
          >
            {/* Connector Line */}
            {!isLast && (
              <div
                className={cn(
                  'absolute bg-slate-200 transition-colors duration-500',
                  isVertical
                    ? 'left-[11px] top-[24px] w-[2px] h-[calc(100%+8px)]'
                    : 'top-[11px] left-[calc(50%+12px)] w-[calc(100%-24px)] h-[2px]',
                  step.status === 'completed' && 'bg-emerald-500'
                )}
              />
            )}

            {/* Icon/Circle */}
            <div className={cn(
              'relative z-10 flex h-6 w-6 items-center justify-center rounded-full border-2 transition-all duration-300',
              step.status === 'completed'
                ? 'bg-emerald-500 border-emerald-500 text-white scale-110'
                : step.status === 'running'
                  ? 'bg-white border-brand-primary text-brand-primary animate-pulse shadow-[0_0_8px_rgba(59,130,246,0.5)]'
                  : 'bg-white border-slate-300 text-slate-300'
            )}>
              {step.status === 'completed' ? (
                <Check className="h-3.5 w-3.5 stroke-[3px]" />
              ) : step.status === 'running' ? (
                <div className="h-1.5 w-1.5 rounded-full bg-brand-primary" />
              ) : (
                <Circle className="h-3 w-3 fill-current opacity-20" />
              )}
            </div>

            {/* Text Content */}
            <div className={cn(
              isVertical ? 'ml-4 pt-0.5' : 'mt-3 text-center px-2'
            )}>
              <p className={cn(
                'text-sm font-semibold transition-colors duration-300',
                step.status === 'pending' ? 'text-text-muted' : 'text-text-primary'
              )}>
                {step.label}
              </p>
              {step.description && (
                <p className="text-xs text-text-muted mt-0.5 max-w-[200px]">
                  {step.description}
                </p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export { StepIndicator };
