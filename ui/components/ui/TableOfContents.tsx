import * as React from 'react';
import { List, ChevronRight } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface TOCItem {
  id: string;
  label: string;
  level: number;
}

export interface TableOfContentsProps {
  items: TOCItem[];
  activeId?: string;
  onItemClick?: (id: string) => void;
  className?: string;
}

const TableOfContents = ({
  items,
  activeId,
  onItemClick,
  className
}: TableOfContentsProps) => {
  return (
    <div className={cn('flex flex-col space-y-4 py-4', className)}>
      <div className="flex items-center space-x-2 px-2 text-text-muted">
        <List size={16} />
        <span className="text-[10px] font-bold uppercase tracking-[0.2em]">Document Structure</span>
      </div>

      <nav className="space-y-1">
        {items.map((item) => (
          <button
            key={item.id}
            onClick={() => onItemClick?.(item.id)}
            className={cn(
              'group flex items-center w-full text-left py-1.5 px-2 rounded-ant-sm text-xs transition-all duration-200',
              activeId === item.id
                ? 'bg-brand-primary/5 text-brand-primary font-bold'
                : 'text-text-secondary hover:bg-slate-50 hover:text-text-primary'
            )}
            style={{ paddingLeft: `${(item.level - 1) * 12 + 8}px` }}
          >
            {activeId === item.id && (
              <div className="absolute left-0 w-1 h-4 bg-brand-primary rounded-r-full animate-in fade-in slide-in-from-left-1" />
            )}
            <span className="truncate">{item.label}</span>
          </button>
        ))}
      </nav>
    </div>
  );
};

export { TableOfContents };
