import * as React from 'react';
import { User, Bot, Clock } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Avatar } from './Avatar';

export interface ChatMessage {
  id: string;
  role: 'user' | 'agent';
  content: string;
  timestamp: string;
}

export interface ChatBubbleProps {
  message: ChatMessage;
  className?: string;
}

const ChatBubble = ({ message, className }: ChatBubbleProps) => {
  const isAgent = message.role === 'agent';

  return (
    <div className={cn(
      'flex w-full space-x-3 mb-6',
      !isAgent && 'flex-row-reverse space-x-reverse',
      className
    )}>
      <Avatar
        fallback={isAgent ? 'AG' : 'OP'}
        isAgent={isAgent}
        size="sm"
        className="mt-1"
      />

      <div className={cn(
        'flex flex-col max-w-[80%]',
        !isAgent && 'items-end'
      )}>
        <div className="flex items-center space-x-2 mb-1 px-1">
          <span className="text-[10px] font-bold text-text-primary uppercase tracking-wider">
            {isAgent ? 'Antigravity' : 'You'}
          </span>
          <span className="text-[10px] text-text-muted flex items-center">
            <Clock className="h-2.5 w-2.5 mr-1" />
            {message.timestamp}
          </span>
        </div>

        <div className={cn(
          'p-4 rounded-ant-lg text-sm leading-relaxed shadow-sm transition-all duration-300',
          isAgent
            ? 'bg-white border border-slate-200 text-text-primary rounded-tl-none'
            : 'bg-brand-primary text-white rounded-tr-none'
        )}>
          {message.content}
        </div>
      </div>
    </div>
  );
};

export { ChatBubble };
