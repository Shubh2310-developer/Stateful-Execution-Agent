import * as React from 'react';
import { ChevronRight, Home } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface BreadcrumbItem {
  label: string;
  href?: string;
  isCurrent?: boolean;
}

export interface BreadcrumbsProps {
  items: BreadcrumbItem[];
  className?: string;
}

const Breadcrumbs = ({ items, className }: BreadcrumbsProps) => {
  return (
    <nav aria-label="Breadcrumb" className={cn('flex items-center text-sm', className)}>
      <ol className="flex items-center space-x-2">
        <li>
          <a href="/" className="text-text-muted hover:text-text-primary transition-colors">
            <Home className="h-4 w-4" />
          </a>
        </li>
        {items.map((item, index) => (
          <li key={index} className="flex items-center space-x-2">
            <ChevronRight className="h-4 w-4 text-text-muted flex-shrink-0" />
            {item.isCurrent ? (
              <span className="font-semibold text-text-primary truncate max-w-[200px]" aria-current="page">
                {item.label}
              </span>
            ) : (
              <a
                href={item.href || '#'}
                className="text-text-muted hover:text-text-primary transition-colors truncate max-w-[150px]"
              >
                {item.label}
              </a>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
};

export { Breadcrumbs };
