import * as React from 'react';
import { X, Info, AlertTriangle, AlertCircle, CheckCircle } from 'lucide-react';
import { cn } from '../../lib/utils';

export type BannerVariant = 'info' | 'warning' | 'error' | 'success';

export interface BannerProps {
  variant?: BannerVariant;
  children: React.ReactNode;
  onClose?: () => void;
  className?: string;
  isSticky?: boolean;
}

const Banner = ({
  variant = 'info',
  children,
  onClose,
  className,
  isSticky = false
}: BannerProps) => {
  const icons = {
    info: <Info className="h-4 w-4" />,
    warning: <AlertTriangle className="h-4 w-4" />,
    error: <AlertCircle className="h-4 w-4" />,
    success: <CheckCircle className="h-4 w-4" />,
  };

  const variants = {
    info: 'bg-indigo-600 text-white',
    warning: 'bg-amber-500 text-white',
    error: 'bg-red-600 text-white',
    success: 'bg-emerald-600 text-white',
  };

  return (
    <div className={cn(
      'w-full py-2 px-6 flex items-center justify-between text-xs font-bold transition-all animate-in slide-in-from-top duration-300',
      variants[variant],
      isSticky && 'sticky top-0 z-40',
      className
    )}>
      <div className="flex items-center space-x-3 mx-auto">
        {icons[variant]}
        <div className="uppercase tracking-widest text-center">
          {children}
        </div>
      </div>
      {onClose && (
        <button
          onClick={onClose}
          className="p-1 hover:bg-white/20 rounded transition-colors"
          aria-label="Close banner"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );
};

export { Banner };
