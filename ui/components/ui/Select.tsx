import * as React from 'react';
import { ChevronDown, Check } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface SelectOption {
  value: string;
  label: string;
}

export interface SelectProps {
  options: SelectOption[];
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  label?: string;
  error?: string;
  className?: string;
}

const Select = ({
  options,
  value,
  onChange,
  placeholder = "Select an option",
  label,
  error,
  className
}: SelectProps) => {
  const [isOpen, setIsOpen] = React.useState(false);
  const containerRef = React.useRef<HTMLDivElement>(null);

  const selectedOption = options.find(opt => opt.value === value);

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
    <div className={cn("w-full space-y-1.5", className)} ref={containerRef}>
      {label && (
        <label className="text-sm font-medium text-text-primary">
          {label}
        </label>
      )}
      <div className="relative">
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className={cn(
            "flex w-full items-center justify-between rounded-ant-md border border-slate-300 bg-background-surface px-3 py-2 text-sm text-text-primary transition-all focus:border-brand-primary focus:outline-none focus:ring-2 focus:ring-brand-primary/20",
            error && "border-status-error",
            !selectedOption && "text-text-muted"
          )}
          aria-haspopup="listbox"
          aria-expanded={isOpen}
        >
          <span className="truncate">{selectedOption ? selectedOption.label : placeholder}</span>
          <ChevronDown className={cn("h-4 w-4 text-text-muted transition-transform duration-200", isOpen && "rotate-180")} />
        </button>

        {isOpen && (
          <ul
            role="listbox"
            className="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-ant-md border border-slate-200 bg-background-surface py-1 shadow-lg animate-in fade-in zoom-in-95 duration-150"
          >
            {options.map((option) => (
              <li
                key={option.value}
                role="option"
                aria-selected={value === option.value}
                onClick={() => {
                  onChange(option.value);
                  setIsOpen(false);
                }}
                className={cn(
                  "flex cursor-pointer items-center justify-between px-3 py-2 text-sm transition-colors hover:bg-slate-50",
                  value === option.value ? "bg-brand-primary/5 text-brand-primary font-medium" : "text-text-secondary"
                )}
              >
                {option.label}
                {value === option.value && <Check className="h-4 w-4" />}
              </li>
            ))}
          </ul>
        )}
      </div>
      {error && <p className="text-xs text-status-error">{error}</p>}
    </div>
  );
};

export { Select };
