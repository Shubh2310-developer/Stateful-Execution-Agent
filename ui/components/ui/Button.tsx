import * as React from 'react';
import { LucideIcon, Loader2 } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: LucideIcon;
  rightIcon?: LucideIcon;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', isLoading, leftIcon: LeftIcon, rightIcon: RightIcon, children, disabled, ...props }, ref) => {
    const variants = {
      primary: 'bg-brand-primary text-white hover:bg-blue-700 shadow-sm',
      secondary: 'bg-background-surface border border-slate-200 text-text-primary hover:bg-background-muted shadow-sm',
      ghost: 'text-text-muted hover:text-text-primary hover:bg-background-muted',
    };

    const sizes = {
      sm: 'px-3 py-1.5 text-xs',
      md: 'px-4 py-2 text-sm',
      lg: 'px-6 py-3 text-base',
    };

    const baseStyles = 'inline-flex items-center justify-center rounded-ant-md font-medium transition-all duration-150 active:scale-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none cursor-pointer';

    // "Lift" effect from ANIMATION_SPECS.md: translateY(-2px), 200ms, ease-out
    const liftEffect = 'hover:-translate-y-0.5 duration-200 ease-out-ant';

    return (
      <button
        ref={ref}
        disabled={isLoading || disabled}
        className={cn(
          baseStyles,
          variants[variant],
          sizes[size],
          variant !== 'ghost' && liftEffect,
          className
        )}
        {...props}
      >
        {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
        {!isLoading && LeftIcon && <LeftIcon className={cn('mr-2', size === 'sm' ? 'h-3 w-3' : 'h-4 w-4')} />}
        {children}
        {!isLoading && RightIcon && <RightIcon className={cn('ml-2', size === 'sm' ? 'h-3 w-3' : 'h-4 w-4')} />}
      </button>
    );
  }
);

Button.displayName = 'Button';

export { Button };
