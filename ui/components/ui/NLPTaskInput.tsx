import * as React from 'react';
import { Send, Hash, Sparkles, X } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface ConstraintTag {
  id: string;
  label: string;
  value: string;
}

export interface NLPTaskInputProps {
  placeholder?: string;
  onLaunch?: (text: string, tags: ConstraintTag[]) => void;
  className?: string;
  initialTags?: ConstraintTag[];
  sentiment?: 'neutral' | 'positive' | 'urgent' | 'critical';
}

const NLPTaskInput = ({
  placeholder = "Describe your goal (e.g., 'Analyze the performance of the Q4 marketing campaign')...",
  onLaunch,
  className,
  initialTags = [],
  sentiment = 'neutral'
}: NLPTaskInputProps) => {
  const [text, setText] = React.useState('');
  const [tags, setTags] = React.useState<ConstraintTag[]>(initialTags);
  const textareaRef = React.useRef<HTMLTextAreaElement>(null);

  const sentimentStyles = {
    neutral: 'border-slate-200 focus-within:border-brand-primary focus-within:ring-brand-primary/20',
    positive: 'border-emerald-200 focus-within:border-emerald-500 focus-within:ring-emerald-500/20',
    urgent: 'border-amber-200 focus-within:border-amber-500 focus-within:ring-amber-500/20',
    critical: 'border-red-200 focus-within:border-red-500 focus-within:ring-red-500/20',
  };

  const sentimentGlow = {
    neutral: 'bg-brand-primary/5',
    positive: 'bg-emerald-500/5',
    urgent: 'bg-amber-500/5',
    critical: 'bg-red-500/5',
  };

  // Auto-expand textarea
  const adjustHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${Math.max(textarea.scrollHeight, 80)}px`;
    }
  };

  React.useEffect(() => {
    adjustHeight();
  }, [text]);

  const removeTag = (id: string) => {
    setTags(tags.filter(t => t.id !== id));
  };

  const handleLaunch = () => {
    if (text.trim() && onLaunch) {
      onLaunch(text, tags);
    }
  };

  return (
    <div className={cn(
      'relative flex flex-col w-full bg-white border rounded-ant-lg shadow-lg transition-all duration-300',
      sentimentStyles[sentiment],
      className
    )}>
      {/* Sentiment Background Glow */}
      <div className={cn(
        "absolute inset-0 rounded-ant-lg pointer-events-none transition-colors duration-500",
        sentimentGlow[sentiment]
      )} />

      {/* Input Header/Sparkle Icon */}
      <div className="absolute top-4 left-4 pointer-events-none z-10">
        <Sparkles className={cn(
          "h-5 w-5 animate-pulse",
          sentiment === 'neutral' ? 'text-brand-primary' :
          sentiment === 'positive' ? 'text-emerald-500' :
          sentiment === 'urgent' ? 'text-amber-500' : 'text-red-500'
        )} />
      </div>

      <textarea
        ref={textareaRef}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={placeholder}
        className="w-full pl-12 pr-4 pt-4 pb-16 min-h-[120px] text-lg bg-transparent border-none focus:ring-0 resize-none placeholder:text-text-muted text-text-primary"
      />

      {/* Constraints/Tags Area */}
      <div className="flex flex-wrap gap-2 px-4 pb-4">
        {tags.map((tag) => (
          <div
            key={tag.id}
            className="flex items-center space-x-1.5 bg-slate-100 text-slate-700 px-2 py-1 rounded-full text-xs font-medium border border-slate-200 animate-in zoom-in-90"
          >
            <Hash className="h-3 w-3 text-slate-400" />
            <span>{tag.label}: {tag.value}</span>
            <button
              onClick={() => removeTag(tag.id)}
              className="hover:text-red-500 transition-colors"
            >
              <X className="h-3 w-3" />
            </button>
          </div>
        ))}
      </div>

      {/* Action Bar */}
      <div className="absolute bottom-3 right-3 flex items-center space-x-3">
        <span className="text-xs text-text-muted mr-2">
          Press <kbd className="px-1.5 py-0.5 rounded border border-slate-200 bg-slate-50 font-sans">Enter</kbd> to launch
        </span>
        <button
          onClick={handleLaunch}
          disabled={!text.trim()}
          className={cn(
            'flex items-center space-x-2 px-5 py-2 rounded-ant-md font-semibold transition-all duration-200',
            text.trim()
              ? 'bg-brand-primary text-white shadow-md shadow-brand-primary/25 hover:translate-y-[-1px] hover:shadow-lg active:scale-95'
              : 'bg-slate-100 text-slate-400 cursor-not-allowed'
          )}
        >
          <span>Launch Mission</span>
          <Send className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
};

export { NLPTaskInput };
