import * as React from 'react';
import { Calendar as CalendarIcon, Clock, RefreshCw, ArrowRight, Play } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { Badge } from './Badge';
import { Button } from './Button';

export interface TemporalTrigger {
  id: string;
  type: 'cron' | 'event' | 'delay';
  value: string;
  nextRun?: string;
  lastRun?: string;
  isActive: boolean;
}

export interface TemporalTriggerCardProps {
  title: string;
  trigger: TemporalTrigger;
  onToggle?: (active: boolean) => void;
  onRunNow?: () => void;
  className?: string;
}

const TemporalTriggerCard = ({
  title,
  trigger,
  onToggle,
  onRunNow,
  className
}: TemporalTriggerCardProps) => {
  const typeIcons = {
    cron: <RefreshCw className="h-4 w-4" />,
    event: <Play className="h-4 w-4" />,
    delay: <Clock className="h-4 w-4" />,
  };

  const typeLabels = {
    cron: 'Recurring Schedule',
    event: 'Event Trigger',
    delay: 'Delayed Execution',
  };

  return (
    <Card className={cn(
      'p-5 transition-all duration-300',
      trigger.isActive ? 'border-slate-200' : 'border-slate-100 bg-slate-50/50 grayscale opacity-70',
      className
    )}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={cn(
            "p-2 rounded-ant-md shrink-0",
            trigger.isActive ? "bg-brand-primary/10 text-brand-primary" : "bg-slate-200 text-slate-400"
          )}>
            {typeIcons[trigger.type]}
          </div>
          <div>
            <h4 className="text-sm font-bold text-text-primary leading-tight">{title}</h4>
            <span className="text-[10px] text-text-muted font-bold uppercase tracking-wider">
              {typeLabels[trigger.type]}
            </span>
          </div>
        </div>
        <button
          onClick={() => onToggle?.(!trigger.isActive)}
          className={cn(
            "relative inline-flex h-5 w-9 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-offset-2",
            trigger.isActive ? "bg-brand-primary" : "bg-slate-200"
          )}
        >
          <span className={cn(
            "inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out",
            trigger.isActive ? "translate-x-4" : "translate-x-0"
          )} />
        </button>
      </div>

      <div className="bg-slate-50/50 rounded-ant-md p-3 mb-4 border border-slate-100">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[10px] text-text-muted font-bold uppercase">Trigger</span>
          <code className="text-[10px] font-mono font-bold text-brand-primary">{trigger.value}</code>
        </div>
        {trigger.nextRun && (
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-text-muted font-bold uppercase">Next Run</span>
            <span className="text-[10px] font-bold text-text-secondary">{trigger.nextRun}</span>
          </div>
        )}
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-slate-100">
        <div className="flex items-center text-[10px] text-text-muted">
          <Clock className="h-3 w-3 mr-1" />
          <span>Last: {trigger.lastRun || 'Never'}</span>
        </div>
        <Button
          size="sm"
          variant="ghost"
          onClick={onRunNow}
          className="h-8 text-brand-primary px-2"
        >
          Run Now
          <ArrowRight className="h-3 w-3 ml-1.5" />
        </Button>
      </div>
    </Card>
  );
};

export { TemporalTriggerCard };
