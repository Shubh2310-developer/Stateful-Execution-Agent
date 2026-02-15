import * as React from 'react';
import { Send, Sparkles, Wand2 } from 'lucide-react';
import { cn } from '../../lib/utils';
import { ChatBubble, ChatMessage } from './ChatBubble';
import { Button } from './Button';
import { SentimentSelector, SentimentType } from './SentimentSelector';

export interface ChatInterfaceProps {
  messages: ChatMessage[];
  onSendMessage: (text: string, sentiment: SentimentType) => void;
  isLoading?: boolean;
  className?: string;
}

const ChatInterface = ({
  messages,
  onSendMessage,
  isLoading = false,
  className
}: ChatInterfaceProps) => {
  const [input, setInput] = React.useState('');
  const [sentiment, setSentiment] = React.useState<SentimentType>('neutral');
  const scrollRef = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input, sentiment);
      setInput('');
    }
  };

  return (
    <div className={cn('flex flex-col h-full bg-slate-50 rounded-ant-lg border border-slate-200 overflow-hidden', className)}>
      {/* Messages Area */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-6 space-y-2 scroll-smooth"
      >
        {messages.map((msg) => (
          <ChatBubble key={msg.id} message={msg} />
        ))}
        {isLoading && (
          <div className="flex space-x-3 mb-6 animate-in fade-in duration-500">
            <div className="h-8 w-8 rounded-full bg-slate-200 animate-pulse" />
            <div className="flex flex-col space-y-2">
              <div className="h-10 w-48 bg-white border border-slate-200 rounded-ant-lg rounded-tl-none animate-pulse" />
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t border-slate-200 shadow-lg">
        <form onSubmit={handleSubmit} className="relative flex items-end space-x-2">
          <div className="flex-1 relative">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              rows={1}
              className="w-full pl-4 pr-12 py-3 bg-slate-50 border-slate-200 rounded-ant-lg text-sm focus:ring-brand-primary focus:border-brand-primary transition-all resize-none max-h-32"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
            />
            <div className="absolute right-3 bottom-2">
              <SentimentSelector value={sentiment} onChange={setSentiment} />
            </div>
          </div>

          <Button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="h-[46px] w-[46px] p-0 shrink-0"
          >
            <Send className="h-5 w-5" />
          </Button>
        </form>

        <div className="mt-2 flex items-center justify-between">
          <div className="flex items-center space-x-2 text-[10px] text-text-muted">
            <Sparkles className="h-3 w-3" />
            <span>The agent uses your sentiment to adjust its tone.</span>
          </div>
          <div className="flex items-center space-x-2 text-[10px] text-text-muted">
            <span>Press <kbd className="px-1 bg-slate-50 rounded border">Enter</kbd> to send</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export { ChatInterface };
