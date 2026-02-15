import * as React from 'react';
import { X } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface SheetProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  children: React.ReactNode;
  side?: 'left' | 'right' | 'top' | 'bottom';
  className?: string;
}

const Sheet = ({
  isOpen,
  onClose,
  title,
  description,
  children,
  side = 'right',
  className
}: SheetProps) => {
  React.useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const sideClasses = {
    right: 'inset-y-0 right-0 h-full w-full sm:max-w-md border-l animate-in slide-in-from-right duration-300 ease-quart-out',
    left: 'inset-y-0 left-0 h-full w-full sm:max-w-md border-r animate-in slide-in-from-left duration-300 ease-quart-out',
    top: 'inset-x-0 top-0 w-full border-b animate-in slide-in-from-top duration-300 ease-quart-out',
    bottom: 'inset-x-0 bottom-0 w-full border-t animate-in slide-in-from-bottom duration-300 ease-quart-out',
  };

  return (
    <div className="fixed inset-0 z-50 flex">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity animate-in fade-in duration-300"
        onClick={onClose}
      />

      {/* Sheet Content */}
      <div
        className={cn(
          'fixed z-50 bg-background-surface shadow-2xl transition-transform',
          sideClasses[side],
          className
        )}
      >
        <div className="flex flex-col h-full">
          <div className="flex items-center justify-between p-6 border-b border-slate-100">
            <div className="space-y-1">
              {title && <h2 className="text-lg font-bold text-text-primary tracking-tight">{title}</h2>}
              {description && <p className="text-xs text-text-muted font-medium">{description}</p>}
            </div>
            <button
              onClick={onClose}
              className="rounded-full p-2 text-text-muted hover:bg-slate-100 hover:text-text-primary transition-all"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-6">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
};

export { Sheet };
