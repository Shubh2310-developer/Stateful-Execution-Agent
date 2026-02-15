import * as React from 'react';
import { cn } from '../../lib/utils';

export interface KbdProps extends React.HTMLAttributes<HTMLElement> {}

const Kbd = React.forwardRef<HTMLElement, KbdProps>(
  ({ className, ...props }, ref) => {
    return (
      <kbd
        ref={ref}
        className={cn(
          'pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border border-slate-200 bg-slate-50 px-1.5 font-mono text-[10px] font-medium text-text-muted opacity-100 shadow-[0_1px_0_0_rgba(0,0,0,0.1)]',
          className
        )}
        {...props}
      />
    );
  }
);

Kbd.displayName = 'Kbd';

export { Kbd };
