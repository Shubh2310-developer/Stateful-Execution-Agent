import * as React from 'react';
import { cn } from '../../lib/utils';
import { Check } from 'lucide-react';

export interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  indeterminate?: boolean;
}

const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className, label, error, indeterminate, ...props }, ref) => {
    const localRef = React.useRef<HTMLInputElement>(null);
    const combinedRef = (ref as React.RefObject<HTMLInputElement>) || localRef;

    React.useEffect(() => {
      if (combinedRef.current) {
        combinedRef.current.indeterminate = !!indeterminate;
      }
    }, [indeterminate, combinedRef]);

    return (
      <div className="flex flex-col space-y-1">
        <label className={cn("flex items-center space-x-2 cursor-pointer group", className)}>
          <div className="relative">
            <input
              type="checkbox"
              ref={combinedRef}
              className="peer sr-only"
              {...props}
            />
            <div className={cn(
              "h-5 w-5 rounded border border-slate-300 bg-background-surface transition-all duration-150 peer-focus-visible:ring-2 peer-focus-visible:ring-brand-primary peer-focus-visible:ring-offset-2 peer-checked:bg-brand-primary peer-checked:border-brand-primary",
              indeterminate && "bg-brand-primary border-brand-primary",
              error && "border-status-error"
            )} />
            {indeterminate ? (
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-0.5 w-2.5 bg-white rounded-full" />
            ) : (
              <Check className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-3.5 w-3.5 text-white opacity-0 transition-opacity peer-checked:opacity-100" />
            )}
          </div>
          {label && (
            <span className="text-sm font-medium text-text-primary select-none group-hover:text-brand-primary transition-colors">
              {label}
            </span>
          )}
        </label>
        {error && <p className="text-xs text-status-error ml-7">{error}</p>}
      </div>
    );
  }
);

Checkbox.displayName = 'Checkbox';

export { Checkbox };
