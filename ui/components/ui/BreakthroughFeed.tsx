import * as React from 'react';
import { Zap, TrendingUp, Heart, Calendar, Target } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Timeline, TimelineEvent } from './Timeline';
import { Badge } from './Badge';

export interface BreakthroughEvent extends Omit<TimelineEvent, 'icon'> {
  impactScore: number; // 0-100
  category: 'preference' | 'skill' | 'alignment';
}

export interface BreakthroughFeedProps {
  events: BreakthroughEvent[];
  className?: string;
}

const BreakthroughFeed = ({ events, className }: BreakthroughFeedProps) => {
  const categoryIcons = {
    preference: <Heart className="h-3.5 w-3.5" />,
    skill: <Zap className="h-3.5 w-3.5" />,
    alignment: <Target className="h-3.5 w-3.5" />,
  };

  const categoryColors = {
    preference: 'bg-blue-500',
    skill: 'bg-amber-500',
    alignment: 'bg-emerald-500',
  };

  const timelineEvents: TimelineEvent[] = events.map(e => ({
    id: e.id,
    time: e.time,
    title: e.title,
    description: e.description,
    status: e.status,
    icon: (
      <div className={cn("h-full w-full flex items-center justify-center text-white rounded-full shadow-lg", categoryColors[e.category])}>
        {categoryIcons[e.category]}
      </div>
    )
  }));

  return (
    <div className={cn('p-6 bg-white border border-slate-200 rounded-ant-lg shadow-sm', className)}>
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-emerald-100 rounded-ant-md text-emerald-600">
            <TrendingUp size={18} />
          </div>
          <div>
            <h3 className="text-sm font-bold text-text-primary uppercase tracking-widest leading-tight">Breakthrough Feed</h3>
            <p className="text-[10px] text-text-muted font-medium">Historical learning milestones</p>
          </div>
        </div>
        <Badge variant="outline" className="border-slate-200 text-slate-500">
          Last 30 Days
        </Badge>
      </div>

      <Timeline events={timelineEvents} />

      <div className="mt-8 pt-6 border-t border-slate-100 text-center">
        <p className="text-[10px] text-text-muted italic">
          The agent has optimized its execution profile by 24.2% since integration.
        </p>
      </div>
    </div>
  );
};

export { BreakthroughFeed };
