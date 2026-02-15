import * as React from 'react';
import { cn } from '../../lib/utils';

export interface AvatarProps extends React.HTMLAttributes<HTMLDivElement> {
  src?: string;
  alt?: string;
  fallback: string;
  size?: 'sm' | 'md' | 'lg';
  isAgent?: boolean;
}

const Avatar = ({ src, alt, fallback, size = 'md', isAgent = false, className, ...props }: AvatarProps) => {
  const [error, setError] = React.useState(false);

  const sizes = {
    sm: 'h-8 w-8 text-xs',
    md: 'h-10 w-10 text-sm',
    lg: 'h-12 w-12 text-base',
  };

  return (
    <div
      className={cn(
        'relative flex shrink-0 overflow-hidden rounded-full transition-all duration-200',
        sizes[size],
        isAgent ? 'ring-2 ring-brand-primary/30' : 'bg-slate-100',
        className
      )}
      {...props}
    >
      {src && !error ? (
        <img
          src={src}
          alt={alt}
          onError={() => setError(true)}
          className="aspect-square h-full w-full object-cover"
        />
      ) : (
        <div className={cn(
          "flex h-full w-full items-center justify-center font-bold uppercase",
          isAgent ? "bg-brand-primary text-white" : "text-slate-500"
        )}>
          {fallback.substring(0, 2)}
        </div>
      )}

      {isAgent && (
        <div className="absolute bottom-0 right-0 h-2.5 w-2.5 rounded-full border-2 border-white bg-status-success animate-pulse" />
      )}
    </div>
  );
};

export { Avatar };
