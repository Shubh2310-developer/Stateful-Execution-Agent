import * as React from 'react';
import { Layout, Clock, Zap, Users } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { Badge } from './Badge';

export interface TemplateCardProps {
  title: string;
  description: string;
  category: string;
  estimatedTimeSaved: string;
  usageCount?: number;
  capabilities: string[];
  isPinned?: boolean;
  onClick?: () => void;
  className?: string;
}

const TemplateCard = ({
  title,
  description,
  category,
  estimatedTimeSaved,
  usageCount,
  capabilities,
  isPinned = false,
  onClick,
  className
}: TemplateCardProps) => {
  return (
    <Card
      onClick={onClick}
      className={cn(
        'group flex flex-col h-full border-slate-200 hover:border-brand-primary/50 hover:shadow-lg transition-all duration-300',
        isPinned && 'ring-1 ring-brand-primary/20 bg-brand-primary/[0.02]',
        className
      )}
    >
      <div className="flex items-start justify-between mb-3">
        <Badge variant="secondary" className="bg-slate-100 text-slate-600 text-[10px] uppercase">
          {category}
        </Badge>
        {isPinned && (
          <div className="text-brand-primary">
            <Zap className="h-4 w-4 fill-current" />
          </div>
        )}
      </div>

      <h3 className="text-base font-bold text-text-primary group-hover:text-brand-primary transition-colors mb-2">
        {title}
      </h3>

      <p className="text-xs text-text-secondary line-clamp-2 mb-6">
        {description}
      </p>

      <div className="mt-auto space-y-4">
        <div className="flex flex-wrap gap-1.5">
          {capabilities.slice(0, 3).map((cap) => (
            <span key={cap} className="px-1.5 py-0.5 bg-slate-50 text-[10px] text-text-muted rounded border border-slate-100">
              {cap}
            </span>
          ))}
          {capabilities.length > 3 && (
            <span className="text-[10px] text-text-muted self-center">+{capabilities.length - 3} more</span>
          )}
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-slate-100">
          <div className="flex items-center text-[10px] font-bold text-emerald-600 uppercase tracking-wider">
            <Clock className="h-3 w-3 mr-1" />
            <span>~{estimatedTimeSaved} saved</span>
          </div>
          {usageCount !== undefined && (
            <div className="flex items-center text-[10px] text-text-muted font-medium">
              <Users className="h-3 w-3 mr-1" />
              <span>{usageCount} runs</span>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
};

export { TemplateCard };
