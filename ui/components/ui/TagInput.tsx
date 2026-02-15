import * as React from 'react';
import { X, Plus, Hash } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '../../lib/utils';
import { Badge } from './Badge';

export interface TagInputProps {
  tags: string[];
  onChange: (tags: string[]) => void;
  suggestions?: string[];
  placeholder?: string;
  className?: string;
  prefix?: React.ReactNode;
}

const TagInput = ({
  tags,
  onChange,
  suggestions = [],
  placeholder = "Add tag...",
  className,
  prefix
}: TagInputProps) => {
  const [inputValue, setInputValue] = React.useState('');
  const [showSuggestions, setShowSuggestions] = React.useState(false);
  const containerRef = React.useRef<HTMLDivElement>(null);

  const filteredSuggestions = suggestions.filter(
    s => s.toLowerCase().includes(inputValue.toLowerCase()) && !tags.includes(s)
  );

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' || e.key === ',' || e.key === ';') {
      e.preventDefault();
      if (filteredSuggestions.length > 0 && showSuggestions) {
        addTag(filteredSuggestions[0]);
      } else {
        addTag(inputValue);
      }
    } else if (e.key === 'Backspace' && !inputValue && tags.length > 0) {
      removeTag(tags.length - 1);
    } else if (e.key === 'Escape') {
      setInputValue('');
      setShowSuggestions(false);
      (e.target as HTMLInputElement).blur();
    } else if (e.key === 'ArrowDown' && filteredSuggestions.length > 0) {
      setShowSuggestions(true);
    }
  };

  const addTag = (tag: string) => {
    const trimmed = tag.trim();
    if (trimmed && !tags.includes(trimmed)) {
      onChange([...tags, trimmed]);
      setInputValue('');
      setShowSuggestions(false);
    }
  };

  const removeTag = (index: number) => {
    const newTags = [...tags];
    newTags.splice(index, 1);
    onChange(newTags);
  };

  React.useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative w-full" ref={containerRef}>
      <div
        className={cn(
          'flex flex-wrap items-center gap-2 p-2 w-full rounded-ant-md border border-slate-300 bg-background-surface min-h-[42px] focus-within:ring-2 focus-within:ring-brand-primary/20 focus-within:border-brand-primary transition-all duration-150',
          className
        )}
      >
        {prefix && (
          <div className="pl-1 text-text-muted">
            {prefix}
          </div>
        )}

        <AnimatePresence>
          {tags.map((tag, index) => (
            <motion.div
              key={tag}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              transition={{ duration: 0.15 }}
            >
              <Badge
                variant="secondary"
                className="bg-slate-100 text-slate-700 hover:bg-slate-200 py-1 pr-1 pl-2 gap-1.5 border-slate-200"
              >
                <span className="flex items-center">
                  <Hash className="h-3 w-3 mr-1 text-text-muted" />
                  {tag}
                </span>
                <button
                  type="button"
                  onClick={() => removeTag(index)}
                  className="rounded-full hover:bg-slate-300 p-0.5 transition-colors"
                  aria-label={`Remove ${tag} tag`}
                >
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            </motion.div>
          ))}
        </AnimatePresence>

        <input
          type="text"
          value={inputValue}
          onChange={(e) => {
            setInputValue(e.target.value);
            setShowSuggestions(true);
          }}
          onKeyDown={handleKeyDown}
          onFocus={() => setShowSuggestions(true)}
          placeholder={tags.length === 0 ? placeholder : ""}
          className="flex-1 min-w-[120px] bg-transparent text-sm border-none focus:ring-0 p-1 placeholder:text-text-muted text-text-primary"
        />
      </div>

      {showSuggestions && inputValue && filteredSuggestions.length > 0 && (
        <div className="absolute z-50 mt-1 w-full rounded-ant-md border border-slate-200 bg-background-surface shadow-lg py-1 animate-in fade-in zoom-in-95 duration-150">
          {filteredSuggestions.map((suggestion) => (
            <button
              key={suggestion}
              onClick={() => addTag(suggestion)}
              className="flex w-full items-center px-3 py-2 text-sm text-text-secondary hover:bg-slate-50 hover:text-text-primary transition-colors text-left"
            >
              <Plus className="h-3 w-3 mr-2 text-text-muted" />
              {suggestion}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export { TagInput };
