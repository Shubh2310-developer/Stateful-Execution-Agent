import * as React from 'react';
import { Copy, Check, Terminal } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface CodeBlockProps {
  code: string;
  language?: string;
  title?: string;
  showLineNumbers?: boolean;
  className?: string;
}

const CodeBlock = ({
  code,
  language,
  title,
  showLineNumbers = false,
  className
}: CodeBlockProps) => {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const lines = code.trim().split('\n');

  return (
    <div className={cn(
      'group relative flex flex-col rounded-ant-lg bg-slate-900 overflow-hidden border border-slate-800 shadow-xl',
      className
    )}>
      {/* Header */}
      {(title || language) && (
        <div className="flex items-center justify-between px-4 py-2 border-b border-slate-800 bg-slate-900/50">
          <div className="flex items-center space-x-2">
            <Terminal className="h-3.5 w-3.5 text-slate-400" />
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
              {title || language || 'Code'}
            </span>
          </div>
          <button
            onClick={handleCopy}
            className="flex items-center space-x-1.5 text-slate-400 hover:text-white transition-colors"
          >
            {copied ? (
              <>
                <Check className="h-3 w-3 text-emerald-400" />
                <span className="text-[10px] font-bold text-emerald-400">COPIED</span>
              </>
            ) : (
              <>
                <Copy className="h-3 w-3" />
                <span className="text-[10px] font-bold">COPY</span>
              </>
            )}
          </button>
        </div>
      )}

      {/* Code Area */}
      <div className="relative overflow-x-auto p-4 font-mono text-sm leading-relaxed text-slate-300 scrollbar-hide">
        {!title && !language && (
          <button
            onClick={handleCopy}
            className="absolute right-4 top-4 p-1.5 rounded-ant-sm bg-slate-800 text-slate-400 hover:text-white opacity-0 group-hover:opacity-100 transition-all duration-200 z-10"
          >
            {copied ? <Check className="h-4 w-4 text-emerald-400" /> : <Copy className="h-4 w-4" />}
          </button>
        )}

        <div className="flex">
          {showLineNumbers && (
            <div className="flex flex-col pr-4 text-slate-600 text-right select-none min-w-[2.5rem]">
              {lines.map((_, i) => (
                <span key={i}>{i + 1}</span>
              ))}
            </div>
          )}
          <pre className="flex-1 whitespace-pre">
            <code>{code.trim()}</code>
          </pre>
        </div>
      </div>
    </div>
  );
};

export { CodeBlock };
