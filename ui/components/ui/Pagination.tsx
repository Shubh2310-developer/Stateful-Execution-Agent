import * as React from 'react';
import { ChevronLeft, ChevronRight, MoreHorizontal } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';

export interface PaginationProps {
  total: number;
  pageSize: number;
  current: number;
  onChange: (page: number) => void;
  className?: string;
}

const Pagination = ({
  total,
  pageSize,
  current,
  onChange,
  className
}: PaginationProps) => {
  const totalPages = Math.ceil(total / pageSize);

  const renderPageButtons = () => {
    const pages = [];
    const showEllipsis = totalPages > 7;

    if (!showEllipsis) {
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // Logic for showing current, neighbors, and boundaries
      if (current <= 4) {
        pages.push(1, 2, 3, 4, 5, 'ellipsis', totalPages);
      } else if (current >= totalPages - 3) {
        pages.push(1, 'ellipsis', totalPages - 4, totalPages - 3, totalPages - 2, totalPages - 1, totalPages);
      } else {
        pages.push(1, 'ellipsis', current - 1, current, current + 1, 'ellipsis', totalPages);
      }
    }

    return pages.map((page, index) => {
      if (page === 'ellipsis') {
        return (
          <div key={`ellipsis-${index}`} className="flex h-9 w-9 items-center justify-center">
            <MoreHorizontal className="h-4 w-4 text-text-muted" />
          </div>
        );
      }

      const isCurrent = current === page;
      return (
        <Button
          key={page}
          variant={isCurrent ? 'primary' : 'ghost'}
          size="sm"
          className={cn('h-9 w-9 p-0 rounded-ant-md font-bold', !isCurrent && 'text-text-muted hover:text-text-primary')}
          onClick={() => onChange(page as number)}
        >
          {page}
        </Button>
      );
    });
  };

  if (totalPages <= 1) return null;

  return (
    <nav className={cn('flex items-center justify-center space-x-1', className)}>
      <Button
        variant="ghost"
        size="sm"
        disabled={current === 1}
        onClick={() => onChange(current - 1)}
        className="h-9 px-2 text-text-muted hover:text-text-primary"
      >
        <ChevronLeft className="h-4 w-4 mr-1" />
        Prev
      </Button>

      <div className="flex items-center space-x-1">
        {renderPageButtons()}
      </div>

      <Button
        variant="ghost"
        size="sm"
        disabled={current === totalPages}
        onClick={() => onChange(current + 1)}
        className="h-9 px-2 text-text-muted hover:text-text-primary"
      >
        Next
        <ChevronRight className="h-4 w-4 ml-1" />
      </Button>
    </nav>
  );
};

export { Pagination };
