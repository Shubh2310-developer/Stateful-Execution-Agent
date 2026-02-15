import * as React from 'react';
import { cn } from '../../lib/utils';

interface TooltipContextType {
  // Can be used for global tooltip configuration if needed
}

const TooltipContext = React.createContext<TooltipContextType | undefined>(undefined);

export const TooltipProvider = ({ children }: { children: React.ReactNode }) => {
  return (
    <TooltipContext.Provider value={{}}>
      {children}
    </TooltipContext.Provider>
  );
};

export interface TooltipProps {
  content: React.ReactNode;
  children: React.ReactElement;
  position?: 'top' | 'bottom' | 'left' | 'right';
  className?: string;
  delayDuration?: number;
}

const Tooltip = ({
  content,
  children,
  position = 'top',
  className,
  delayDuration = 200
}: TooltipProps) => {
  const [isVisible, setIsVisible] = React.useState(false);
  const timeoutRef = React.useRef<NodeJS.Timeout | null>(null);

  const showTooltip = () => {
    timeoutRef.current = setTimeout(() => {
      setIsVisible(true);
    }, delayDuration);
  };

  const hideTooltip = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setIsVisible(false);
  };

  const positionClasses = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
  };

  const arrowClasses = {
    top: 'top-full left-1/2 -translate-x-1/2 border-t-slate-900 border-x-transparent border-b-transparent',
    bottom: 'bottom-full left-1/2 -translate-x-1/2 border-b-slate-900 border-x-transparent border-t-transparent',
    left: 'left-full top-1/2 -translate-y-1/2 border-l-slate-900 border-y-transparent border-r-transparent',
    right: 'right-full top-1/2 -translate-y-1/2 border-r-slate-900 border-y-transparent border-l-transparent',
  };

  // Clone the child to inject event handlers for accessibility
  const trigger = React.cloneElement(children, {
    onMouseEnter: showTooltip,
    onMouseLeave: hideTooltip,
    onFocus: showTooltip,
    onBlur: hideTooltip,
    'aria-describedby': isVisible ? 'tooltip-content' : undefined,
  });

  return (
    <div className="relative inline-block">
      {trigger}
      {isVisible && (
        <div
          id="tooltip-content"
          role="tooltip"
          className={cn(
            'absolute z-50 w-max max-w-[240px] px-2.5 py-1.5 text-xs font-medium text-white bg-slate-900 rounded-ant-sm shadow-xl animate-in fade-in zoom-in-95 duration-150 pointer-events-none',
            positionClasses[position],
            className
          )}
        >
          {content}
          <div className={cn(
            'absolute border-4',
            arrowClasses[position]
          )} />
        </div>
      )}
    </div>
  );
};

export { Tooltip };
