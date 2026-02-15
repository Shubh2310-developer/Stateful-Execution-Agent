import * as React from 'react';
import { Filter, Search, X, RotateCcw, ChevronDown } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';
import { Input } from './Input';
import { Badge } from './Badge';

export interface FilterOption {
  label: string;
  value: string;
}

export interface DataTableFilter {
  key: string;
  label: string;
  options?: FilterOption[];
  type: 'select' | 'text' | 'date';
}

export interface DataTableFilterBarProps {
  filters: DataTableFilter[];
  activeFilters: Record<string, any>;
  onFilterChange: (key: string, value: any) => void;
  onClearAll: () => void;
  className?: string;
  searchPlaceholder?: string;
  searchValue?: string;
  onSearchChange?: (value: string) => void;
}

const DataTableFilterBar = ({
  filters,
  activeFilters,
  onFilterChange,
  onClearAll,
  className,
  searchPlaceholder = "Search records...",
  searchValue,
  onSearchChange
}: DataTableFilterBarProps) => {
  const hasActiveFilters = Object.keys(activeFilters).length > 0 || searchValue;

  return (
    <div className={cn('flex flex-col space-y-3 p-4 bg-slate-50/50 border-b border-slate-200', className)}>
      <div className="flex items-center justify-between gap-4">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-muted" />
          <input
            type="text"
            placeholder={searchPlaceholder}
            className="w-full pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-ant-md text-sm focus:outline-none focus:ring-2 focus:ring-brand-primary/20 focus:border-brand-primary transition-all"
            value={searchValue || ''}
            onChange={(e) => onSearchChange?.(e.target.value)}
          />
        </div>

        <div className="flex items-center space-x-2">
          {filters.map((filter) => (
            <div key={filter.key} className="relative group">
              <Button
                variant="secondary"
                size="sm"
                className={cn(
                  "h-9 px-3 border-slate-200 font-medium",
                  activeFilters[filter.key] && "border-brand-primary text-brand-primary bg-brand-primary/[0.02]"
                )}
              >
                <Filter className="h-3.5 w-3.5 mr-2 opacity-60" />
                {filter.label}
                {activeFilters[filter.key] && (
                  <Badge className="ml-2 px-1 py-0 h-4 min-w-[16px] bg-brand-primary text-white border-none">
                    1
                  </Badge>
                )}
                <ChevronDown className="h-3.5 w-3.5 ml-2 opacity-40" />
              </Button>
            </div>
          ))}

          {hasActiveFilters && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onClearAll}
              className="h-9 px-3 text-text-muted hover:text-text-primary"
            >
              <RotateCcw className="h-3.5 w-3.5 mr-2" />
              Reset
            </Button>
          )}
        </div>
      </div>

      {hasActiveFilters && (
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-[10px] font-bold text-text-muted uppercase tracking-widest mr-1">Active Filters:</span>
          {searchValue && (
            <Badge variant="secondary" className="bg-white border-slate-200 text-slate-700 py-1 pr-1 pl-2 gap-1.5 shadow-sm">
              <span className="text-[10px] text-text-muted mr-1 font-bold">Query:</span>
              {searchValue}
              <button onClick={() => onSearchChange?.('')} className="hover:text-red-500 p-0.5 rounded-full hover:bg-slate-100">
                <X size={12} />
              </button>
            </Badge>
          )}
          {Object.entries(activeFilters).map(([key, value]) => {
            const filter = filters.find(f => f.key === key);
            if (!filter || !value) return null;
            return (
              <Badge key={key} variant="secondary" className="bg-white border-slate-200 text-slate-700 py-1 pr-1 pl-2 gap-1.5 shadow-sm">
                <span className="text-[10px] text-text-muted mr-1 font-bold">{filter.label}:</span>
                {String(value)}
                <button onClick={() => onFilterChange(key, null)} className="hover:text-red-500 p-0.5 rounded-full hover:bg-slate-100">
                  <X size={12} />
                </button>
              </Badge>
            );
          })}
        </div>
      )}
    </div>
  );
};

export { DataTableFilterBar };
