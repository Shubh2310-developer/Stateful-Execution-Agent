import * as React from 'react';
import { cn } from '../../lib/utils';

export interface GhostCursorProps {
  className?: string;
}

const GhostCursor = ({ className }: GhostCursorProps) => {
  return (
    <span className={cn(
      'inline-block w-2 h-4 ml-0.5 bg-brand-primary align-middle animate-pulse shadow-[0_0_8px_rgba(59,130,246,0.5)]',
      className
    )} />
  );
};

export { GhostCursor };
