import * as React from 'react';
import { cn } from '../../lib/utils';
import { CodeBlock } from './CodeBlock';

export interface MarkdownProps {
  content: string;
  className?: string;
}

const Markdown = ({ content, className }: MarkdownProps) => {
  // A very simple regex-based markdown renderer for demonstration.
  // In a real app, use 'react-markdown' or 'remark'.
  const parts = content.split(/(```[\s\S]*?```)/g);

  return (
    <div className={cn('prose prose-slate max-w-none dark:prose-invert', className)}>
      {parts.map((part, i) => {
        if (part.startsWith('```')) {
          const match = part.match(/```(\w+)?\n([\s\S]*?)```/);
          const lang = match?.[1] || '';
          const code = match?.[2] || '';
          return <CodeBlock key={i} code={code} language={lang} className="my-4" />;
        }

        // Process simple markdown bits
        return (
          <div
            key={i}
            className="whitespace-pre-wrap leading-relaxed space-y-4"
            dangerouslySetInnerHTML={{
              __html: part
                .replace(/^# (.*$)/gm, '<h1 class="text-2xl font-bold mt-6 mb-4">$1</h1>')
                .replace(/^## (.*$)/gm, '<h2 class="text-xl font-bold mt-5 mb-3">$1</h2>')
                .replace(/^### (.*$)/gm, '<h3 class="text-lg font-bold mt-4 mb-2">$1</h3>')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/^- (.*$)/gm, '<li class="ml-4 list-disc">$1</li>')
                .replace(/`(.*?)`/g, '<code class="bg-slate-100 px-1 py-0.5 rounded text-sm font-mono text-pink-600">$1</code>')
            }}
          />
        );
      })}
    </div>
  );
};

export { Markdown };
