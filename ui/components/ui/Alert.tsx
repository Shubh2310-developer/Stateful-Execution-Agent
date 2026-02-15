import * as React from 'react';
import { AlertCircle, AlertTriangle, CheckCircle, Info, X } from 'lucide-react';
import { cn } from '../../lib/utils';

export type AlertVariant = 'default' | 'destructive' | 'warning' | 'success' | 'info';

export interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: AlertVariant;
  title?: string;
  onClose?: () => void;
}

const Alert = React.forwardRef<HTMLDivElement, AlertProps>(
  ({ className, variant = 'default', title, children, onClose, ...props }, ref) => {
    const icons = {
      default: <Info className="h-5 w-5" />,
      destructive: <AlertCircle className="h-5 w-5" />,
      warning: <AlertTriangle className="h-5 w-5" />,
      success: <CheckCircle className="h-5 w-5" />,
      info: <Info className="h-5 w-5" />,
    };

    const variants = {
      default: 'bg-slate-50 text-slate-900 border-slate-200',
      destructive: 'bg-red-50 text-red-900 border-red-200',
      warning: 'bg-amber-50 text-amber-900 border-amber-200',
      success: 'bg-emerald-50 text-emerald-900 border-emerald-200',
      info: 'bg-indigo-50 text-indigo-900 border-indigo-200',
    };

    return (
      <div
        ref={ref}
        role="alert"
        className={cn(
          'relative w-full rounded-ant-lg border p-4 flex items-start space-x-3 transition-all animate-in fade-in slide-in-from-top-2 duration-300',
          variants[variant],
          className
        )}
        {...props}
      >
        <div className="shrink-0 pt-0.5">
          {icons[variant]}
        </div>
        <div className="flex-1 min-w-0">
          {title && (
            <h5 className="mb-1 font-bold leading-none tracking-tight">
              {title}
            </h5>
          )}
          <div className="text-sm opacity-90 leading-relaxed">
            {children}
          </div>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="shrink-0 rounded-ant-sm p-1 hover:bg-black/5 transition-colors"
            aria-label="Close alert"
          >
            <X className="h-4 w-4" />
          </button>
        )}
      </div>
    );
  }
);

Alert.displayName = 'Alert';

export { Alert };
