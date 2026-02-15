import * as React from 'react';
import { cn } from '../../lib/utils';

export interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {}

function Skeleton({ className, ...props }: SkeletonProps) {
  return (
    <div
      className={cn(
        'animate-pulse rounded-ant-md bg-slate-200/60 dark:bg-slate-800/60',
        className
      )}
      {...props}
    />
  );
}

export { Skeleton };
