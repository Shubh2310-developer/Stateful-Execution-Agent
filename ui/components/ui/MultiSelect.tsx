import * as React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, ChevronDown, X, Check, ChevronsUpDown } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Badge } from './Badge';
import { Checkbox } from './Checkbox';

export interface MultiSelectOption {
  label: string;
  value: string;
}

export interface MultiSelectProps {
  options: MultiSelectOption[];
  selected: string[];
  onChange: (selected: string[]) => void;
  placeholder?: string;
  className?: string;
  maxDisplay?: number;
}

const MultiSelect = ({
  options,
  selected,
  onChange,
  placeholder = "Select options...",
  className,
  maxDisplay = 3
}: MultiSelectProps) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const [search, setSearch] = React.useState('');
  const [activeIndex, setActiveIndex] = React.useState(-1);
  const containerRef = React.useRef<HTMLDivElement>(null);
  const inputRef = React.useRef<HTMLInputElement>(null);

  const filteredOptions = options.filter(option =>
    option.label.toLowerCase().includes(search.toLowerCase())
  );

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (!isOpen) setIsOpen(true);
      setActiveIndex(prev => (prev + 1) % (filteredOptions.length + 1)); // +1 for Select All
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActiveIndex(prev => (prev <= 0 ? filteredOptions.length : prev - 1));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (activeIndex === 0) {
        toggleAll();
      } else if (activeIndex > 0) {
        toggleOption(filteredOptions[activeIndex - 1].value);
      }
    } else if (e.key === 'Escape') {
      setIsOpen(false);
    }
  };

  React.useEffect(() => {
    if (!isOpen) setActiveIndex(-1);
  }, [isOpen]);

  const toggleOption = (value: string) => {
    const nextSelected = selected.includes(value)
      ? selected.filter(s => s !== value)
      : [...selected, value];
    onChange(nextSelected);
  };

  const removeSelected = (e: React.MouseEvent, value: string) => {
    e.stopPropagation();
    onChange(selected.filter(s => s !== value));
  };

  const toggleAll = () => {
    if (selected.length === options.length) {
      onChange([]);
    } else {
      onChange(options.map(o => o.value));
    }
  };

  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className={cn('relative w-full', className)} ref={containerRef}>
      <div
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            setIsOpen(!isOpen);
          }
        }}
        tabIndex={0}
        role="combobox"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        className={cn(
          'flex min-h-[42px] w-full items-center justify-between rounded-ant-md border border-slate-300 bg-background-surface px-3 py-1.5 transition-all focus:outline-none focus:ring-2 focus:ring-brand-primary/20 focus:border-brand-primary cursor-pointer',
          isOpen && 'border-brand-primary ring-2 ring-brand-primary/20'
        )}
      >
        <div className="flex flex-wrap gap-1.5">
          {selected.length === 0 && (
            <span className="text-sm text-text-muted">{placeholder}</span>
          )}
          <AnimatePresence>
            {selected.slice(0, maxDisplay).map(val => {
              const option = options.find(o => o.value === val);
              return (
                <motion.div
                  key={val}
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  exit={{ scale: 0.9, opacity: 0 }}
                  transition={{ duration: 0.15 }}
                >
                  <Badge
                    variant="secondary"
                    className="bg-slate-100 text-slate-700 hover:bg-slate-200 py-0 pr-1 pl-2 gap-1 h-6"
                  >
                    {option?.label || val}
                    <button
                      onClick={(e) => removeSelected(e, val)}
                      className="rounded-full hover:bg-slate-300 p-0.5 transition-colors"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                </motion.div>
              );
            })}
          </AnimatePresence>
          {selected.length > maxDisplay && (
            <Badge variant="secondary" className="bg-slate-100 text-slate-700 h-6">
              +{selected.length - maxDisplay} more
            </Badge>
          )}
        </div>
        <div className="flex items-center space-x-2 text-text-muted ml-2">
          {selected.length > 0 && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onChange([]);
              }}
              className="hover:text-text-primary"
            >
              <X className="h-4 w-4" />
            </button>
          )}
          <ChevronsUpDown className="h-4 w-4" />
        </div>
      </div>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            className="absolute z-50 mt-2 w-full rounded-ant-md border border-slate-200 bg-background-surface shadow-lg overflow-hidden"
          >
            <div className="flex items-center border-b border-slate-100 px-3 py-2">
            <Search className="h-4 w-4 text-text-muted mr-2" />
            <input
              ref={inputRef}
              className="flex-1 bg-transparent text-sm border-none focus:ring-0 p-0"
              placeholder="Filter options..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={handleKeyDown}
              onClick={(e) => e.stopPropagation()}
            />
          </div>

          <div className="max-h-60 overflow-y-auto py-1" role="listbox">
            <div
              className={cn(
                'flex items-center px-3 py-2 hover:bg-slate-50 cursor-pointer transition-colors',
                activeIndex === 0 && 'bg-slate-100'
              )}
              onClick={toggleAll}
            >
              <Checkbox
                checked={selected.length === options.length && options.length > 0}
                indeterminate={selected.length > 0 && selected.length < options.length}
                readOnly
                className="mr-3"
              />
              <span className="text-sm font-bold text-text-primary">Select All</span>
            </div>

            <div className="h-px bg-slate-100 mx-2 my-1" />

            {filteredOptions.length === 0 ? (
              <div className="px-3 py-8 text-center text-sm text-text-muted italic">
                No results found.
              </div>
            ) : (
              filteredOptions.map((option, index) => (
                <div
                  key={option.value}
                  role="option"
                  aria-selected={selected.includes(option.value)}
                  onClick={() => toggleOption(option.value)}
                  className={cn(
                    'flex items-center px-3 py-2 hover:bg-slate-50 cursor-pointer transition-colors',
                    selected.includes(option.value) && 'bg-brand-primary/[0.03]',
                    activeIndex === index + 1 && 'bg-slate-100'
                  )}
                >
                  <Checkbox
                    checked={selected.includes(option.value)}
                    readOnly
                    className="mr-3"
                  />
                  <span className={cn(
                    'text-sm transition-colors',
                    selected.includes(option.value) ? 'text-brand-primary font-bold' : 'text-text-secondary'
                  )}>
                    {option.label}
                  </span>
                  {selected.includes(option.value) && (
                    <Check className="ml-auto h-4 w-4 text-brand-primary" />
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export { MultiSelect };
