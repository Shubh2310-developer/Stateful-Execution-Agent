import * as React from 'react';
import { Star } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface StarRatingProps {
  value: number;
  max?: number;
  onChange?: (value: number) => void;
  readonly?: boolean;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const StarRating = ({
  value,
  max = 5,
  onChange,
  readonly = false,
  size = 'md',
  className
}: StarRatingProps) => {
  const [hoverValue, setHoverValue] = React.useState<number | null>(null);

  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
  };

  return (
    <div className={cn('flex items-center space-x-1', className)}>
      {Array.from({ length: max }).map((_, i) => {
        const ratingValue = i + 1;
        const isActive = (hoverValue !== null ? hoverValue : value) >= ratingValue;

        return (
          <button
            key={i}
            type="button"
            disabled={readonly}
            className={cn(
              'transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary rounded-full p-0.5',
              readonly ? 'cursor-default' : 'cursor-pointer hover:scale-110 active:scale-95',
              isActive ? 'text-amber-400' : 'text-slate-200'
            )}
            onMouseEnter={() => !readonly && setHoverValue(ratingValue)}
            onMouseLeave={() => !readonly && setHoverValue(null)}
            onClick={() => !readonly && onChange?.(ratingValue)}
            aria-label={`Rate ${ratingValue} out of ${max} stars`}
          >
            <Star
              className={cn(sizes[size], isActive && 'fill-current')}
            />
          </button>
        );
      })}
    </div>
  );
};

export { StarRating };
