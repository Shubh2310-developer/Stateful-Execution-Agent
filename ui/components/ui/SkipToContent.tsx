import * as React from 'react';
import { cn } from '../../lib/utils';

interface SkipToContentProps {
  contentId?: string;
  className?: string;
}

const SkipToContent = ({ contentId = 'main-content', className }: SkipToContentProps) => {
  return (
    <a
      href={`#${contentId}`}
      className={cn(
        'sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[100] focus:px-4 focus:py-2 focus:bg-brand-primary focus:text-white focus:rounded-ant-md focus:shadow-2xl focus:ring-4 focus:ring-brand-primary/20 transition-all outline-none',
        className
      )}
    >
      Skip to main content
    </a>
  );
};

export { SkipToContent };
