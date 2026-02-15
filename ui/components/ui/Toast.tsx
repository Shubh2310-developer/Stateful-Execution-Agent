import * as React from 'react';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';
import { cn } from '../../lib/utils';

export type ToastVariant = 'success' | 'error' | 'warning' | 'info';

export interface ToastProps {
  id: string;
  title?: string;
  description?: string;
  variant?: ToastVariant;
  onClose: (id: string) => void;
  action?: React.ReactNode;
}

const Toast = ({ id, title, description, variant = 'info', onClose, action }: ToastProps) => {
  const icons = {
    success: <CheckCircle className="h-5 w-5 text-status-success" />,
    error: <AlertCircle className="h-5 w-5 text-status-error" />,
    warning: <AlertTriangle className="h-5 w-5 text-status-warning" />,
    info: <Info className="h-5 w-5 text-status-info" />,
  };

  const variants = {
    success: 'border-status-success/20 bg-emerald-50/50',
    error: 'border-status-error/20 bg-red-50/50',
    warning: 'border-status-warning/20 bg-amber-50/50',
    info: 'border-status-info/20 bg-indigo-50/50',
  };

  // Auto-dismiss logic
  React.useEffect(() => {
    const timer = setTimeout(() => onClose(id), 5000);
    return () => clearTimeout(timer);
  }, [id, onClose]);

  return (
    <div
      role="alert"
      className={cn(
        'group relative flex w-full max-w-md items-start space-x-4 rounded-ant-lg border p-4 shadow-lg backdrop-blur-sm transition-all animate-in slide-in-from-right-full duration-300',
        variants[variant]
      )}
    >
      <div className="flex-shrink-0 pt-0.5">{icons[variant]}</div>
      <div className="flex-1 min-w-0">
        {title && (
          <h5 className="text-sm font-bold text-text-primary mb-1">
            {title}
          </h5>
        )}
        {description && (
          <p className="text-xs text-text-secondary leading-relaxed">
            {description}
          </p>
        )}
        {action && <div className="mt-3">{action}</div>}
      </div>
      <button
        onClick={() => onClose(id)}
        className="flex-shrink-0 rounded-ant-sm p-1 text-text-muted hover:text-text-primary transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary"
        aria-label="Close notification"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
};

export { Toast };
