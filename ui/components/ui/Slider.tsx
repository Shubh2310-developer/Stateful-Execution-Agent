import * as React from 'react';
import { cn } from '../../lib/utils';

export interface SliderProps {
  min?: number;
  max?: number;
  step?: number;
  value: number;
  onChange: (value: number) => void;
  label?: string;
  className?: string;
  showValue?: boolean;
}

const Slider = ({
  min = 0,
  max = 100,
  step = 1,
  value,
  onChange,
  label,
  className,
  showValue = true
}: SliderProps) => {
  const percentage = ((value - min) / (max - min)) * 100;

  return (
    <div className={cn('w-full space-y-2', className)}>
      <div className="flex items-center justify-between">
        {label && (
          <label className="text-xs font-bold text-text-muted uppercase tracking-wider">
            {label}
          </label>
        )}
        {showValue && (
          <span className="text-xs font-mono font-bold text-brand-primary bg-brand-primary/10 px-1.5 py-0.5 rounded">
            {value}
          </span>
        )}
      </div>

      <div className="relative flex items-center h-6 group">
        {/* Track Background */}
        <div className="absolute w-full h-1.5 bg-slate-100 rounded-full" />

        {/* Track Active */}
        <div
          className="absolute h-1.5 bg-brand-primary rounded-full transition-all duration-300 ease-out-ant"
          style={{ width: `${percentage}%` }}
        />

        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          className="absolute w-full h-1.5 bg-transparent appearance-none cursor-pointer z-10 focus:outline-none"
          style={{
            WebkitAppearance: 'none',
          }}
        />

        {/* Custom Thumb CSS via style tag for cross-browser */}
        <style dangerouslySetInnerHTML={{ __html: `
          input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            height: 18px;
            width: 18px;
            border-radius: 50%;
            background: #ffffff;
            border: 2px solid var(--color-brand-primary, #3B82F6);
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.2s;
          }
          input[type=range]::-webkit-slider-thumb:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
          }
          input[type=range]:focus::-webkit-slider-thumb {
            box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
          }
          input[type=range]::-moz-range-thumb {
            height: 18px;
            width: 18px;
            border-radius: 50%;
            background: #ffffff;
            border: 2px solid var(--color-brand-primary, #3B82F6);
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          }
        `}} />
      </div>
    </div>
  );
};

export { Slider };
