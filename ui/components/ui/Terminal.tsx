import * as React from 'react';
import { Terminal as TerminalIcon, Maximize2, Minimize2, X } from 'lucide-react';
import { cn } from '../../lib/utils';
import { ScrollArea } from './ScrollArea';

export interface TerminalLine {
  type: 'input' | 'output' | 'error' | 'info';
  content: string;
  timestamp?: string;
}

export interface TerminalProps {
  lines: TerminalLine[];
  onCommand?: (command: string) => void;
  title?: string;
  prompt?: string;
  className?: string;
}

const Terminal = ({
  lines,
  onCommand,
  title = "Antigravity REPL",
  prompt = "antigravity >",
  className
}: TerminalProps) => {
  const [input, setInput] = React.useState('');
  const scrollRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [lines]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && onCommand) {
      onCommand(input);
      setInput('');
    }
  };

  return (
    <div className={cn(
      'flex flex-col bg-slate-950 rounded-ant-lg border border-slate-800 shadow-2xl overflow-hidden font-mono text-sm h-96',
      className
    )}>
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-2 bg-slate-900 border-b border-slate-800">
        <div className="flex items-center space-x-3">
          <TerminalIcon className="h-4 w-4 text-emerald-500" />
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
            {title}
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2.5 h-2.5 rounded-full bg-slate-700" />
          <div className="w-2.5 h-2.5 rounded-full bg-slate-700" />
          <div className="w-2.5 h-2.5 rounded-full bg-slate-700" />
        </div>
      </div>

      {/* Output Area */}
      <ScrollArea className="flex-1 p-4" ref={scrollRef}>
        <div className="space-y-1">
          {lines.map((line, i) => (
            <div key={i} className="flex flex-col">
              <div className="flex items-start">
                <span className={cn(
                  "mr-2 shrink-0",
                  line.type === 'input' ? "text-brand-primary" :
                  line.type === 'error' ? "text-red-400" :
                  line.type === 'info' ? "text-amber-400" : "text-slate-300"
                )}>
                  {line.type === 'input' ? '➜' : '·'}
                </span>
                <span className={cn(
                  "break-all",
                  line.type === 'input' ? "text-white font-bold" :
                  line.type === 'error' ? "text-red-400" :
                  line.type === 'info' ? "text-amber-400/80" : "text-slate-400"
                )}>
                  {line.content}
                </span>
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>

      {/* Input Area */}
      <div className="p-4 bg-slate-900/50 border-t border-slate-800">
        <form onSubmit={handleSubmit} className="flex items-center">
          <span className="text-emerald-500 font-bold mr-3 whitespace-nowrap">
            {prompt}
          </span>
          <input
            autoFocus
            className="flex-1 bg-transparent border-none p-0 focus:ring-0 text-white placeholder:text-slate-700"
            placeholder="Type a command..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
        </form>
      </div>
    </div>
  );
};

export { Terminal };
