import * as React from 'react';
import { Search as SearchIcon, X } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Kbd } from './Kbd';

export interface SearchInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  onClear?: () => void;
  showShortcut?: boolean;
}

const SearchInput = React.forwardRef<HTMLInputElement, SearchInputProps>(
  ({ className, onClear, showShortcut = true, value, ...props }, ref) => {
    const isMac = typeof window !== 'undefined' && /Mac|iPod|iPhone|iPad/.test(navigator.platform);

    return (
      <div className={cn('relative w-full group', className)}>
        <div className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted group-focus-within:text-brand-primary transition-colors">
          <SearchIcon className="h-4 w-4" />
        </div>

        <input
          ref={ref}
          className={cn(
            'w-full rounded-full border border-slate-200 bg-slate-50 py-2 pl-10 pr-12 text-sm transition-all focus:border-brand-primary focus:bg-white focus:outline-none focus:ring-4 focus:ring-brand-primary/5 placeholder:text-text-muted text-text-primary'
          )}
          value={value}
          {...props}
        />

        <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center space-x-1">
          {value && (
            <button
              onClick={onClear}
              className="p-1 text-text-muted hover:text-text-primary transition-colors"
            >
              <X className="h-3.5 w-3.5" />
            </button>
          )}

          {showShortcut && !value && (
            <div className="hidden md:flex items-center space-x-1 opacity-50 group-focus-within:opacity-0 transition-opacity">
              <Kbd>{isMac ? '⌘' : 'Ctrl'}</Kbd>
              <Kbd>K</Kbd>
            </div>
          )}
        </div>
      </div>
    );
  }
);

SearchInput.displayName = 'SearchInput';

export { SearchInput };
