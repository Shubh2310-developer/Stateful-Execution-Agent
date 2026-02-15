import * as React from 'react';
import { cn } from '../../lib/utils';

export interface ToggleGroupOption {
  value: string;
  label: React.ReactNode;
  title?: string;
}

export interface ToggleGroupProps {
  options: ToggleGroupOption[];
  value: string;
  onChange: (value: string) => void;
  className?: string;
  size?: 'sm' | 'md';
}

const ToggleGroup = ({
  options,
  value,
  onChange,
  className,
  size = 'md'
}: ToggleGroupProps) => {
  return (
    <div className={cn(
      'inline-flex p-1 bg-slate-100 rounded-ant-lg border border-slate-200 shadow-inner',
      className
    )}>
      {options.map((option) => {
        const isActive = value === option.value;

        return (
          <button
            key={option.value}
            onClick={() => onChange(option.value)}
            title={option.title}
            className={cn(
              'flex items-center justify-center transition-all duration-200 font-bold uppercase tracking-widest',
              size === 'sm' ? 'px-2 py-1 text-[9px]' : 'px-4 py-1.5 text-[10px]',
              isActive
                ? 'bg-white text-brand-primary shadow-sm rounded-ant-md'
                : 'text-text-muted hover:text-text-secondary'
            )}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
};

export { ToggleGroup };
