import * as React from 'react';
import { LucideIcon, Plus } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';

export interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  className?: string;
}

const EmptyState = ({
  icon: Icon,
  title,
  description,
  actionLabel,
  onAction,
  className
}: EmptyStateProps) => {
  return (
    <div className={cn(
      'flex flex-col items-center justify-center text-center p-12 rounded-ant-lg border-2 border-dashed border-slate-200 bg-slate-50/50 transition-all duration-300',
      className
    )}>
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-white shadow-sm border border-slate-100 mb-6">
        <Icon className="h-8 w-8 text-text-muted" />
      </div>
      <h3 className="text-lg font-bold text-text-primary mb-2">{title}</h3>
      <p className="text-sm text-text-muted max-w-xs mb-8">
        {description}
      </p>
      {actionLabel && onAction && (
        <Button onClick={onAction} className="shadow-brand-primary/20">
          <Plus className="mr-2 h-4 w-4" />
          {actionLabel}
        </Button>
      )}
    </div>
  );
};

export { EmptyState };
