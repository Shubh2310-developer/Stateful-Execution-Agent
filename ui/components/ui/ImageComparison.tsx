import * as React from 'react';
import { cn } from '../../lib/utils';

export interface ImageComparisonProps {
  beforeSrc: string;
  afterSrc: string;
  beforeLabel?: string;
  afterLabel?: string;
  className?: string;
}

const ImageComparison = ({
  beforeSrc,
  afterSrc,
  beforeLabel = "Original",
  afterLabel = "Refined",
  className
}: ImageComparisonProps) => {
  const [position, setPosition] = React.useState(50);
  const containerRef = React.useRef<HTMLDivElement>(null);

  const handleMove = (e: React.MouseEvent | React.TouchEvent) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = 'touches' in e ? e.touches[0].clientX : e.clientX;
    const relativeX = x - rect.left;
    const percentage = Math.max(0, Math.min(100, (relativeX / rect.width) * 100));
    setPosition(percentage);
  };

  return (
    <div
      ref={containerRef}
      className={cn('relative w-full aspect-video overflow-hidden rounded-ant-lg border border-slate-200 cursor-col-resize select-none shadow-xl', className)}
      onMouseMove={handleMove}
      onTouchMove={handleMove}
    >
      {/* After Image (Base) */}
      <img
        src={afterSrc}
        alt="After refinement"
        className="absolute inset-0 w-full h-full object-cover"
      />
      <div className="absolute top-4 right-4 z-20">
        <span className="bg-brand-primary text-white text-[10px] font-bold px-2 py-1 rounded uppercase tracking-widest shadow-lg">
          {afterLabel}
        </span>
      </div>

      {/* Before Image (Clipped Overlay) */}
      <div
        className="absolute inset-0 w-full h-full border-r-2 border-white shadow-[4px_0_15px_rgba(0,0,0,0.3)] z-10"
        style={{ clipPath: `inset(0 ${100 - position}% 0 0)` }}
      >
        <img
          src={beforeSrc}
          alt="Before refinement"
          className="absolute inset-0 w-full h-full object-cover"
        />
        <div className="absolute top-4 left-4">
          <span className="bg-slate-900 text-white text-[10px] font-bold px-2 py-1 rounded uppercase tracking-widest shadow-lg">
            {beforeLabel}
          </span>
        </div>
      </div>

      {/* Handle */}
      <div
        className="absolute top-0 bottom-0 z-20 w-1 bg-white flex items-center justify-center"
        style={{ left: `${position}%` }}
      >
        <div className="h-10 w-10 rounded-full bg-white shadow-xl flex items-center justify-center border-2 border-slate-200">
          <div className="flex space-x-0.5">
            <div className="w-0.5 h-4 bg-slate-400 rounded-full" />
            <div className="w-0.5 h-4 bg-slate-400 rounded-full" />
          </div>
        </div>
      </div>
    </div>
  );
};

export { ImageComparison };
