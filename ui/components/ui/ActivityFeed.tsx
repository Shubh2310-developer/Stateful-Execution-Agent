import * as React from 'react';
import { cn } from '../../lib/utils';
import { Avatar } from './Avatar';
import { Clock } from 'lucide-react';

export interface ActivityItem {
  id: string;
  user: { name: string; avatar?: string; fallback: string };
  action: string;
  target?: string;
  timestamp: string;
}

export interface ActivityFeedProps {
  items: ActivityItem[];
  className?: string;
}

const ActivityFeed = ({ items, className }: ActivityFeedProps) => {
  return (
    <div className={cn('space-y-6', className)}>
      {items.map((item) => (
        <div key={item.id} className="flex space-x-3">
          <Avatar
            src={item.user.avatar}
            fallback={item.user.fallback}
            size="sm"
            className="mt-0.5"
          />
          <div className="flex-1 min-w-0">
            <p className="text-xs text-text-primary leading-snug">
              <span className="font-bold">{item.user.name}</span>{' '}
              <span className="text-text-secondary">{item.action}</span>{' '}
              {item.target && <span className="font-semibold text-brand-primary">{item.target}</span>}
            </p>
            <div className="flex items-center mt-1 text-[10px] text-text-muted">
              <Clock className="h-2.5 w-2.5 mr-1" />
              <span>{item.timestamp}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export { ActivityFeed };
