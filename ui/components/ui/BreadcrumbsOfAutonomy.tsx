import * as React from 'react';
import { History, ArrowRight, Lightbulb, User, Shield } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export interface IntentNode {
  id: string;
  time: string;
  label: string;
  type: 'autonomous' | 'user' | 'constraint';
  description?: string;
}

export interface BreadcrumbsOfAutonomyProps {
  intents: IntentNode[];
  className?: string;
}

const BreadcrumbsOfAutonomy = ({ intents, className }: BreadcrumbsOfAutonomyProps) => {
  const typeIcons = {
    autonomous: <Lightbulb className="h-3 w-3" />,
    user: <User className="h-3 w-3" />,
    constraint: <Shield className="h-3 w-3" />,
  };

  const typeColors = {
    autonomous: 'bg-brand-primary text-white',
    user: 'bg-indigo-500 text-white',
    constraint: 'bg-amber-500 text-white',
  };

  return (
    <div className={cn('flex items-center space-x-0 overflow-x-auto py-4 scrollbar-hide', className)}>
      <div className="flex h-10 items-center justify-center px-4 bg-slate-900 text-white rounded-l-full shrink-0">
        <History className="h-4 w-4 mr-2" />
        <span className="text-[10px] font-bold uppercase tracking-widest">History of Intent</span>
      </div>

      <div className="flex items-center">
        {intents.map((intent, index) => (
          <React.Fragment key={intent.id}>
            <div className="flex items-center group">
              {/* Connector */}
              <div className="w-8 h-[2px] bg-slate-200 group-hover:bg-brand-primary/30 transition-colors" />

              {/* Intent Node */}
              <Tooltip content={
                <div className="p-1">
                  <p className="font-bold text-xs mb-1">{intent.label}</p>
                  <p className="text-[10px] opacity-80">{intent.description}</p>
                  <p className="text-[9px] mt-2 font-mono">{intent.time}</p>
                </div>
              }>
                <div className={cn(
                  'relative h-8 w-8 rounded-full flex items-center justify-center shadow-md transition-all duration-300 hover:scale-110 cursor-pointer',
                  typeColors[intent.type]
                )}>
                  {typeIcons[intent.type]}
                  <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
                    <span className="text-[9px] font-bold text-text-muted uppercase tracking-tighter">
                      {intent.label}
                    </span>
                  </div>
                </div>
              </Tooltip>
            </div>
            {index === intents.length - 1 && (
              <div className="w-12 h-12 flex items-center justify-center">
                <div className="h-2 w-2 rounded-full bg-brand-primary animate-ping" />
              </div>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

export { BreadcrumbsOfAutonomy };
