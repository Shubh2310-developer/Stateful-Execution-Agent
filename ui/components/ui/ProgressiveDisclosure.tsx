import * as React from 'react';
import { cn } from '../../lib/utils';

export interface ProgressiveDisclosureProps {
  level: 1 | 2 | 3;
  children: React.ReactNode;
  className?: string;
}

const ProgressiveDisclosure = ({
  level,
  children,
  className
}: ProgressiveDisclosureProps) => {
  return (
    <div className={cn(
      'transition-all duration-300 animate-in fade-in slide-in-from-top-1',
      level === 1 && 'font-bold tracking-tight',
      level === 2 && 'opacity-90',
      level === 3 && 'text-sm opacity-70 italic font-medium',
      className
    )}>
      {children}
    </div>
  );
};

export { ProgressiveDisclosure };
