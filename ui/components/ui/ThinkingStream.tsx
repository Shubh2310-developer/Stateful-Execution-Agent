import * as React from 'react';
import { Terminal, Sparkles } from 'lucide-react';
import { cn } from '../../lib/utils';
import { ScrollArea } from './ScrollArea';

export interface ThoughtLogEntry {
  id: string;
  text: string;
  type: 'observation' | 'plan' | 'action' | 'validation';
  timestamp: string;
}

export interface ThinkingStreamProps {
  entries: ThoughtLogEntry[];
  isThinking?: boolean;
  className?: string;
}

const ThinkingStream = ({
  entries,
  isThinking = false,
  className
}: ThinkingStreamProps) => {
  const scrollRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [entries]);

  const typeStyles = {
    observation: 'text-blue-400',
    plan: 'text-emerald-400',
    action: 'text-amber-400',
    validation: 'text-purple-400',
  };

  return (
    <div className={cn('flex flex-col bg-slate-900 rounded-ant-lg border border-slate-800 overflow-hidden shadow-inner h-64', className)}>
      <div className="px-3 py-2 border-b border-slate-800 bg-slate-900/50 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Terminal className="h-3 w-3 text-slate-500" />
          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Thought Stream</span>
        </div>
        {isThinking && (
          <div className="flex items-center space-x-2">
            <span className="text-[10px] font-bold text-brand-primary animate-pulse uppercase tracking-tight">Processing</span>
            <Sparkles className="h-3 w-3 text-brand-primary animate-spin" />
          </div>
        )}
      </div>

      <ScrollArea className="flex-1 p-4 font-mono text-[11px] leading-relaxed" ref={scrollRef}>
        <div className="space-y-2">
          {entries.map((entry) => (
            <div key={entry.id} className="flex space-x-3 opacity-0 animate-in fade-in slide-in-from-left-1 duration-300 fill-mode-forwards">
              <span className="text-slate-600 shrink-0 select-none">[{entry.timestamp}]</span>
              <p className="text-slate-300">
                <span className={cn('font-bold mr-2 uppercase', typeStyles[entry.type])}>
                  {entry.type}:
                </span>
                {entry.text}
              </p>
            </div>
          ))}
          {isThinking && (
            <div className="flex items-center space-x-2 text-brand-primary">
              <span className="animate-bounce">·</span>
              <span className="animate-bounce" style={{ animationDelay: '100ms' }}>·</span>
              <span className="animate-bounce" style={{ animationDelay: '200ms' }}>·</span>
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
};

export { ThinkingStream };
