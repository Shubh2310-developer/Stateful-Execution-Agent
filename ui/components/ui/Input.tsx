import * as React from 'react';
import { XCircle } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  onClear?: () => void;
  floating?: boolean;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, helperText, onClear, floating, type, id, ...props }, ref) => {
    const inputId = id || React.useId();
    const [isFocused, setIsFocused] = React.useState(false);
    const [hasValue, setHasValue] = React.useState(!!props.value || !!props.defaultValue);

    const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
      setIsFocused(false);
      setHasValue(!!e.target.value);
      props.onBlur?.(e);
    };

    const handleFocus = (e: React.FocusEvent<HTMLInputElement>) => {
      setIsFocused(true);
      props.onFocus?.(e);
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setHasValue(!!e.target.value);
      props.onChange?.(e);
    };

    const baseInputClasses = cn(
      'block w-full rounded-ant-md border border-slate-300 bg-background-surface px-3 py-2 text-text-primary transition-all duration-150 placeholder:text-text-muted focus:border-brand-primary focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50',
      error && 'border-status-error focus:ring-status-error',
      floating && 'pt-6 pb-2',
      className
    );

    return (
      <div className="w-full space-y-1.5">
        <div className="relative">
          {label && !floating && (
            <label
              htmlFor={inputId}
              className="text-sm font-medium text-text-primary mb-1 block"
            >
              {label}
            </label>
          )}

          <div className="relative">
            <input
              id={inputId}
              ref={ref}
              type={type}
              className={baseInputClasses}
              onBlur={handleBlur}
              onFocus={handleFocus}
              onChange={handleChange}
              {...props}
            />

            {floating && label && (
              <label
                htmlFor={inputId}
                className={cn(
                  'absolute left-3 transition-all duration-200 pointer-events-none',
                  (isFocused || hasValue)
                    ? 'top-1.5 text-xs text-brand-primary font-medium'
                    : 'top-4 text-base text-text-muted'
                )}
              >
                {label}
              </label>
            )}

            {onClear && hasValue && (
              <button
                type="button"
                onClick={onClear}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-text-muted hover:text-text-primary transition-colors p-1"
                aria-label="Clear input"
              >
                <XCircle className="h-4 w-4" />
              </button>
            )}
          </div>
        </div>

        {error && (
          <p className="text-sm text-status-error animate-in fade-in slide-in-from-top-1 duration-200">
            {error}
          </p>
        )}

        {!error && helperText && (
          <p className="text-sm text-text-muted">
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export { Input };
