import * as React from 'react';
import { cn } from '../../lib/utils';
import { Loader2 } from 'lucide-react';

export interface InfiniteScrollProps {
  onLoadMore: () => void;
  hasMore: boolean;
  isLoading: boolean;
  children: React.ReactNode;
  className?: string;
  threshold?: number;
}

const InfiniteScroll = ({
  onLoadMore,
  hasMore,
  isLoading,
  children,
  className,
  threshold = 200
}: InfiniteScrollProps) => {
  const observerRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore && !isLoading) {
          onLoadMore();
        }
      },
      { rootMargin: `${threshold}px` }
    );

    const currentRef = observerRef.current;
    if (currentRef) {
      observer.observe(currentRef);
    }

    return () => {
      if (currentRef) {
        observer.unobserve(currentRef);
      }
    };
  }, [onLoadMore, hasMore, isLoading, threshold]);

  return (
    <div className={cn('flex flex-col', className)}>
      {children}
      <div ref={observerRef} className="h-10 w-full flex items-center justify-center mt-4">
        {isLoading && (
          <div className="flex items-center space-x-2 text-text-muted">
            <Loader2 className="h-4 w-4 animate-spin" />
            <span className="text-xs font-bold uppercase tracking-widest">Loading entries...</span>
          </div>
        )}
      </div>
    </div>
  );
};

export { InfiniteScroll };
