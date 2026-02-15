import * as React from 'react';
import { cn } from '../../lib/utils';

export interface RadioOption {
  value: string;
  label: string;
  description?: string;
}

export interface RadioGroupProps {
  options: RadioOption[];
  value: string;
  onChange: (value: string) => void;
  name: string;
  className?: string;
}

const RadioGroup = ({
  options,
  value,
  onChange,
  name,
  className
}: RadioGroupProps) => {
  return (
    <div className={cn('space-y-2', className)}>
      {options.map((option) => {
        const isSelected = value === option.value;
        const id = `${name}-${option.value}`;

        return (
          <label
            key={option.value}
            htmlFor={id}
            className={cn(
              'flex items-start p-3 rounded-ant-md border cursor-pointer transition-all duration-200',
              isSelected
                ? 'bg-brand-primary/5 border-brand-primary/40 ring-1 ring-brand-primary/20'
                : 'bg-white border-slate-200 hover:border-slate-300'
            )}
          >
            <div className="relative flex items-center h-5 mr-3">
              <input
                type="radio"
                id={id}
                name={name}
                value={option.value}
                checked={isSelected}
                onChange={() => onChange(option.value)}
                className="sr-only"
              />
              <div className={cn(
                'h-4 w-4 rounded-full border transition-all',
                isSelected ? 'border-brand-primary' : 'border-slate-300'
              )}>
                {isSelected && (
                  <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-2 w-2 rounded-full bg-brand-primary" />
                )}
              </div>
            </div>
            <div className="flex flex-col">
              <span className={cn(
                'text-sm font-bold',
                isSelected ? 'text-brand-primary' : 'text-text-primary'
              )}>
                {option.label}
              </span>
              {option.description && (
                <span className="text-xs text-text-muted mt-0.5">
                  {option.description}
                </span>
              )}
            </div>
          </label>
        );
      })}
    </div>
  );
};

export { RadioGroup };
