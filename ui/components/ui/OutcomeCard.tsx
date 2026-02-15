import * as React from 'react';
import { CheckCircle2, Trophy, ArrowRight, Target } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { Button } from './Button';

export interface OutcomeCardProps {
  goal: string;
  summary: string;
  impactMetrics?: { label: string; value: string }[];
  onViewDetails?: () => void;
  className?: string;
}

const OutcomeCard = ({
  goal,
  summary,
  impactMetrics = [],
  onViewDetails,
  className
}: OutcomeCardProps) => {
  return (
    <Card className={cn(
      'relative overflow-hidden border-emerald-100 bg-emerald-50/20 p-8 shadow-md',
      className
    )}>
      {/* Background Decoration */}
      <div className="absolute -right-8 -top-8 text-emerald-500/10">
        <Trophy size={160} strokeWidth={1} />
      </div>

      <div className="relative z-10">
        <div className="flex items-center space-x-3 mb-6">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500 text-white shadow-lg shadow-emerald-500/25">
            <CheckCircle2 className="h-6 w-6" />
          </div>
          <div>
            <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-emerald-600">
              Mission Success
            </span>
            <h2 className="text-xl font-bold text-text-primary tracking-tight">
              Goal Achieved
            </h2>
          </div>
        </div>

        <div className="mb-8 max-w-2xl">
          <div className="flex items-start space-x-3 mb-3">
            <Target className="h-5 w-5 text-emerald-500 mt-1 flex-shrink-0" />
            <p className="text-lg font-bold text-text-primary leading-tight">
              {goal}
            </p>
          </div>
          <p className="text-sm text-text-secondary leading-relaxed pl-8">
            {summary}
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8 border-t border-emerald-100 pt-6">
          {impactMetrics.map((metric, i) => (
            <div key={i} className="flex flex-col">
              <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-600 mb-1">
                {metric.label}
              </span>
              <span className="text-2xl font-bold text-text-primary">
                {metric.value}
              </span>
            </div>
          ))}
        </div>

        {onViewDetails && (
          <Button
            onClick={onViewDetails}
            className="bg-emerald-600 hover:bg-emerald-700 text-white shadow-lg shadow-emerald-600/20"
          >
            Full Mission Report
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        )}
      </div>
    </Card>
  );
};

export { OutcomeCard };
