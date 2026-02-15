import * as React from 'react';
import {
  ChevronDown,
  ChevronUp,
  ChevronsUpDown,
  MoreHorizontal,
  Trash2,
  Download,
  Archive
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '../../lib/utils';
import {
  Table,
  TableHeader,
  TableBody,
  TableHead,
  TableRow,
  TableCell
} from './Table';
import { Checkbox } from './Checkbox';
import { Button } from './Button';
import { Skeleton } from './Skeleton';
import { Tooltip } from './Tooltip';

export interface DataTableColumn<T> {
  key: keyof T | string;
  header: string;
  sortable?: boolean;
  render?: (item: T) => React.ReactNode;
  width?: string;
  truncate?: boolean;
  align?: 'left' | 'right' | 'center';
}

export interface DataTableProps<T> {
  data: T[];
  columns: DataTableColumn<T>[];
  isLoading?: boolean;
  compact?: boolean;
  onRowClick?: (item: T) => void;
  onSort?: (key: string, direction: 'asc' | 'desc' | null) => void;
  onSelectionChange?: (selectedItems: T[]) => void;
  bulkActions?: {
    label: string;
    icon: React.ReactNode;
    onClick: (selectedItems: T[]) => void;
    variant?: 'primary' | 'secondary' | 'ghost';
  }[];
  className?: string;
}

export function DataTable<T extends { id: string | number }>({
  data,
  columns,
  isLoading,
  compact = false,
  onRowClick,
  onSort,
  onSelectionChange,
  bulkActions,
  className
}: DataTableProps<T>) {
  const [sortKey, setSortKey] = React.useState<string | null>(null);
  const [sortDirection, setSortDirection] = React.useState<'asc' | 'desc' | null>(null);
  const [selectedIds, setSelectedIds] = React.useState<Set<string | number>>(new Set());

  const handleSort = (key: string) => {
    let nextDirection: 'asc' | 'desc' | null = 'asc';
    if (sortKey === key) {
      if (sortDirection === 'asc') nextDirection = 'desc';
      else if (sortDirection === 'desc') nextDirection = null;
    }

    setSortKey(nextDirection ? key : null);
    setSortDirection(nextDirection);
    onSort?.(key, nextDirection);
  };

  const toggleAll = () => {
    if (selectedIds.size === data.length) {
      setSelectedIds(new Set());
      onSelectionChange?.([]);
    } else {
      const allIds = new Set(data.map(item => item.id));
      setSelectedIds(allIds);
      onSelectionChange?.(data);
    }
  };

  const toggleOne = (id: string | number) => {
    const next = new Set(selectedIds);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    setSelectedIds(next);

    const selectedItems = data.filter(item => next.has(item.id));
    onSelectionChange?.(selectedItems);
  };

  const selectedItems = data.filter(item => selectedIds.has(item.id));

  return (
    <div className={cn('relative w-full', className)}>
      <div className="rounded-ant-lg border border-slate-200 bg-background-surface overflow-hidden">
        <Table className="border-collapse">
          <TableHeader className="sticky top-0 z-10 bg-slate-50/90 backdrop-blur-sm shadow-[0_1px_0_0_rgba(0,0,0,0.05)]">
            <TableRow className="hover:bg-transparent">
                  <TableHead className="w-12 px-4">
                <Checkbox
                  checked={data.length > 0 && selectedIds.size === data.length}
                  indeterminate={selectedIds.size > 0 && selectedIds.size < data.length}
                  onChange={() => toggleAll()}
                />
              </TableHead>
              {columns.map((column) => (
                <TableHead
                  key={String(column.key)}
                  style={{ width: column.width }}
                  className={cn(
                    'group select-none py-3 font-bold text-text-secondary transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary focus-visible:ring-inset',
                    column.sortable && 'cursor-pointer hover:text-text-primary'
                  )}
                  onClick={() => column.sortable && handleSort(String(column.key))}
                  tabIndex={column.sortable ? 0 : -1}
                  onKeyDown={(e) => {
                    if (column.sortable && (e.key === 'Enter' || e.key === ' ')) {
                      e.preventDefault();
                      handleSort(String(column.key));
                    }
                  }}
                >
                  <div className={cn(
                    "flex items-center space-x-1.5",
                    column.align === 'right' && "justify-end",
                    column.align === 'center' && "justify-center"
                  )}>
                    <span>{column.header}</span>
                    {column.sortable && (
                      <div className="text-text-muted opacity-40 group-hover:opacity-100 transition-opacity">
                        {sortKey === column.key ? (
                          sortDirection === 'asc' ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />
                        ) : (
                          <ChevronsUpDown className="h-4 w-4" />
                        )}
                      </div>
                    )}
                  </div>
                </TableHead>
              ))}
              <TableHead className="w-12" />
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              Array.from({ length: 5 }).map((_, i) => (
                <TableRow key={i}>
                  <TableCell className="px-4"><Skeleton className="h-4 w-4 rounded" /></TableCell>
                  {columns.map((_, j) => (
                    <TableCell key={j}><Skeleton className="h-4 w-full max-w-[120px]" /></TableCell>
                  ))}
                  <TableCell />
                </TableRow>
              ))
            ) : data.length === 0 ? (
              <TableRow>
                <TableCell colSpan={columns.length + 2} className="h-24 text-center text-text-muted italic">
                  No results found.
                </TableCell>
              </TableRow>
            ) : (
              data.map((item) => (
                <TableRow
                  key={item.id}
                  data-state={selectedIds.has(item.id) ? 'selected' : undefined}
                  className={cn(
                    onRowClick && 'cursor-pointer select-none',
                    selectedIds.has(item.id) && 'bg-brand-primary/[0.02]'
                  )}
                  onClick={() => onRowClick?.(item)}
                >
                  <TableCell className={cn("px-4", compact ? "py-2" : "py-4")}>
                    <Checkbox
                      checked={selectedIds.has(item.id)}
                      onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                        e.stopPropagation();
                        toggleOne(item.id);
                      }}
                    />
                  </TableCell>
                  {columns.map((column) => (
                    <TableCell
                      key={String(column.key)}
                      className={cn(
                        'text-sm font-medium',
                        compact ? "py-2" : "py-4",
                        column.align === 'right' && 'text-right tabular-nums',
                        column.align === 'center' && 'text-center',
                        column.truncate && 'max-w-[200px]'
                      )}
                    >
                      {column.render ? (
                        column.render(item)
                      ) : (
                        <div className={cn(column.truncate && 'truncate')}>
                          {column.truncate ? (
                            <Tooltip content={String((item as any)[column.key])}>
                              <span className="truncate block cursor-help">
                                {String((item as any)[column.key])}
                              </span>
                            </Tooltip>
                          ) : (
                            String((item as any)[column.key])
                          )}
                        </div>
                      )}
                    </TableCell>
                  ))}
                  <TableCell className="text-right">
                    <Tooltip content="Actions">
                      <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* Bulk Action Bar */}
      <AnimatePresence>
        {selectedIds.size > 0 && (
          <motion.div
            initial={{ y: 100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 100, opacity: 0 }}
            transition={{ type: 'spring', damping: 20, stiffness: 300 }}
            className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50 px-6 py-3 bg-slate-900 text-white rounded-full shadow-2xl flex items-center space-x-6 border border-white/10 backdrop-blur-md"
          >
            <div className="flex items-center space-x-3 border-r border-white/20 pr-6">
              <span className="text-sm font-bold">{selectedIds.size}</span>
              <span className="text-xs text-white/60 uppercase tracking-widest font-medium">Selected</span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSelectedIds(new Set())}
                className="text-white/40 hover:text-white hover:bg-white/10 -mr-2"
              >
                Deselect
              </Button>
            </div>

            <div className="flex items-center space-x-2">
              {bulkActions ? (
                bulkActions.map((action, i) => (
                  <Button
                    key={i}
                    size="sm"
                    variant={action.variant || 'ghost'}
                    onClick={() => action.onClick(selectedItems)}
                    className={cn(
                      'text-white hover:bg-white/10',
                      action.variant === 'destructive' && 'hover:bg-red-500/20 text-red-400 hover:text-red-300'
                    )}
                  >
                    {action.icon && <span className="mr-2">{action.icon}</span>}
                    {action.label}
                  </Button>
                ))
              ) : (
                <>
                  <Button size="sm" variant="ghost" className="text-white hover:bg-white/10">
                    <Download className="h-4 w-4 mr-2" /> Export
                  </Button>
                  <Button size="sm" variant="ghost" className="text-white hover:bg-white/10">
                    <Archive className="h-4 w-4 mr-2" /> Archive
                  </Button>
                  <Button size="sm" variant="ghost" className="text-red-400 hover:text-red-300 hover:bg-red-500/20">
                    <Trash2 className="h-4 w-4 mr-2" /> Delete
                  </Button>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
