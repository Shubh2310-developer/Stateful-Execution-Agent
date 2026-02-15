import * as React from 'react';
import { ChevronLeft, ChevronRight, FileText, ArrowRight } from 'lucide-react';
import { cn } from '../../lib/utils';
import { ArtifactPreview, ArtifactType } from './ArtifactPreview';
import { Button } from './Button';

export interface ArtifactCarouselItem {
  id: string;
  name: string;
  type: ArtifactType;
  size?: string;
  date: string;
}

export interface ArtifactCarouselProps {
  items: ArtifactCarouselItem[];
  onItemClick?: (item: ArtifactCarouselItem) => void;
  className?: string;
}

const ArtifactCarousel = ({ items, onItemClick, className }: ArtifactCarouselProps) => {
  const scrollRef = React.useRef<HTMLDivElement>(null);

  const scroll = (direction: 'left' | 'right') => {
    if (scrollRef.current) {
      const { scrollLeft, clientWidth } = scrollRef.current;
      const scrollTo = direction === 'left' ? scrollLeft - clientWidth : scrollLeft + clientWidth;
      scrollRef.current.scrollTo({ left: scrollTo, behavior: 'smooth' });
    }
  };

  return (
    <div className={cn('relative group w-full', className)}>
      <div className="flex items-center justify-between mb-4 px-1">
        <div className="flex items-center space-x-2">
          <FileText className="h-4 w-4 text-brand-primary" />
          <h3 className="text-sm font-bold text-text-primary uppercase tracking-widest">Recent Artifacts</h3>
        </div>
        <div className="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <Button variant="ghost" size="sm" onClick={() => scroll('left')} className="h-8 w-8 p-0 rounded-full">
            <ChevronLeft size={16} />
          </Button>
          <Button variant="ghost" size="sm" onClick={() => scroll('right')} className="h-8 w-8 p-0 rounded-full">
            <ChevronRight size={16} />
          </Button>
        </div>
      </div>

      <div
        ref={scrollRef}
        className="flex space-x-4 overflow-x-auto scrollbar-hide snap-x snap-mandatory pb-4 px-1"
      >
        {items.map((item) => (
          <div key={item.id} className="snap-start shrink-0 w-[280px]">
            <ArtifactPreview
              name={item.name}
              type={item.type}
              size={item.size}
              onOpen={() => onItemClick?.(item)}
              className="bg-white"
            />
          </div>
        ))}
        {items.length === 0 && (
          <div className="w-full py-8 text-center border-2 border-dashed border-slate-200 rounded-ant-lg bg-slate-50/50">
            <p className="text-sm text-text-muted italic">No artifacts generated yet.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export { ArtifactCarousel };
