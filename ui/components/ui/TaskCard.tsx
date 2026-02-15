import * as React from 'react';
import { Clock, ArrowRight } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { StatusPill, StatusType } from './StatusPill';
import { Button } from './Button';

export interface TaskCardProps {
  title: string;
  status: string;
  statusVariant: StatusType;
  progress: number;
  lastActivity: string;
  onViewTrace?: () => void;
  className?: string;
}

const TaskCard = ({
  title,
  status,
  statusVariant,
  progress,
  lastActivity,
  onViewTrace,
  className
}: TaskCardProps) => {
  return (
    <Card
      variant="task"
      progress={progress}
      className={cn('flex flex-col h-full', className)}
    >
      <div className="flex items-start justify-between mb-4">
        <h3 className="text-base font-bold text-text-primary line-clamp-2 pr-2">
          {title}
        </h3>
        <StatusPill variant={statusVariant} className="flex-shrink-0">
          {status}
        </StatusPill>
      </div>

      <div className="flex-grow" />

      <div className="mt-6 flex items-center justify-between pt-4 border-t border-slate-100">
        <div className="flex items-center text-xs text-text-muted">
          <Clock className="h-3.5 w-3.5 mr-1.5" />
          <span>{lastActivity}</span>
        </div>

        {onViewTrace && (
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onViewTrace();
            }}
            className="text-brand-primary hover:bg-brand-primary/5 -mr-2"
          >
            View Trace
            <ArrowRight className="ml-1.5 h-3.5 w-3.5" />
          </Button>
        )}
      </div>
    </Card>
  );
};

export { TaskCard };
