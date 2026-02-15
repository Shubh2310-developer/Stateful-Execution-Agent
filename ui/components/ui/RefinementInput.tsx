import * as React from 'react';
import { Wand2, Sparkles, MessageSquare, ArrowRight } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';

export interface RefinementSuggestion {
  id: string;
  label: string;
  action: string;
}

export interface RefinementInputProps {
  onRefine: (text: string) => void;
  suggestions?: RefinementSuggestion[];
  placeholder?: string;
  className?: string;
  isLoading?: boolean;
}

const RefinementInput = ({
  onRefine,
  suggestions = [],
  placeholder = "How can I improve this artifact?",
  className,
  isLoading = false
}: RefinementInputProps) => {
  const [text, setText] = React.useState('');
  const inputRef = React.useRef<HTMLInputElement>(null);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (text.trim() && !isLoading) {
      onRefine(text);
      setText('');
    }
  };

  const handleSuggestionClick = (suggestion: RefinementSuggestion) => {
    onRefine(suggestion.action);
  };

  return (
    <div className={cn('w-full space-y-4', className)}>
      {/* Suggestions Row */}
      {suggestions.length > 0 && (
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-[10px] font-bold text-text-muted uppercase tracking-wider mr-1">
            Suggestions:
          </span>
          {suggestions.map((s) => (
            <button
              key={s.id}
              onClick={() => handleSuggestionClick(s)}
              className="px-3 py-1 bg-white border border-slate-200 rounded-full text-xs font-medium text-text-secondary hover:border-brand-primary hover:text-brand-primary transition-all duration-200 shadow-sm flex items-center space-x-1.5"
            >
              <Sparkles className="h-3 w-3" />
              <span>{s.label}</span>
            </button>
          ))}
        </div>
      )}

      {/* Main Input Area */}
      <form
        onSubmit={handleSubmit}
        className={cn(
          "relative flex items-center p-1 bg-white border-2 border-slate-200 rounded-ant-lg shadow-lg focus-within:border-brand-primary transition-all duration-300",
          isLoading && "opacity-70 grayscale pointer-events-none"
        )}
      >
        <div className="flex h-10 w-10 shrink-0 items-center justify-center text-brand-primary">
          <Wand2 className="h-5 w-5" />
        </div>
        <input
          ref={inputRef}
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={placeholder}
          className="flex-1 bg-transparent border-none focus:ring-0 text-sm py-3 px-2 placeholder:text-text-muted text-text-primary"
        />
        <div className="flex items-center space-x-2 px-2">
          <Button
            type="submit"
            size="sm"
            disabled={!text.trim() || isLoading}
            className="rounded-ant-md"
          >
            {isLoading ? (
              <span className="flex items-center space-x-2">
                <Sparkles className="h-3.5 w-3.5 animate-spin" />
                <span>Refining...</span>
              </span>
            ) : (
              <span className="flex items-center space-x-2">
                <span>Refine</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </span>
            )}
          </Button>
        </div>
      </form>

      {/* Footer Info */}
      <div className="flex items-center justify-center space-x-4 text-[10px] text-text-muted font-medium">
        <div className="flex items-center space-x-1">
          <MessageSquare className="h-3 w-3" />
          <span>The agent will iterate on the artifact based on your feedback.</span>
        </div>
      </div>
    </div>
  );
};

export { RefinementInput };
