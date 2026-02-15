import * as React from 'react';
import { Check } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface StepperStep {
  id: string | number;
  label: string;
  description?: string;
}

export interface StepperProps {
  steps: StepperStep[];
  currentStep: number;
  className?: string;
}

const Stepper = ({ steps, currentStep, className }: StepperProps) => {
  return (
    <div className={cn('flex items-center w-full', className)}>
      {steps.map((step, index) => {
        const isCompleted = index < currentStep;
        const isActive = index === currentStep;
        const isLast = index === steps.length - 1;

        return (
          <React.Fragment key={step.id}>
            <div className="flex flex-col items-center relative z-10">
              <div className={cn(
                'flex h-10 w-10 items-center justify-center rounded-full border-2 transition-all duration-300',
                isCompleted ? 'bg-brand-primary border-brand-primary text-white' :
                isActive ? 'border-brand-primary text-brand-primary ring-4 ring-brand-primary/10' :
                'border-slate-200 bg-white text-slate-400'
              )}>
                {isCompleted ? <Check className="h-5 w-5" /> : <span className="text-sm font-bold">{index + 1}</span>}
              </div>
              <div className="absolute top-12 whitespace-nowrap text-center">
                <p className={cn(
                  "text-[10px] font-bold uppercase tracking-widest",
                  isActive ? "text-brand-primary" : "text-text-muted"
                )}>
                  {step.label}
                </p>
              </div>
            </div>

            {!isLast && (
              <div className="flex-1 h-[2px] mx-4 bg-slate-100 relative">
                <div
                  className="absolute inset-0 bg-brand-primary transition-all duration-500"
                  style={{ width: isCompleted ? '100%' : '0%' }}
                />
              </div>
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
};

export { Stepper };
