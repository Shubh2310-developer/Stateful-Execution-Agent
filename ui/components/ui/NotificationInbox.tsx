import * as React from 'react';
import { Bell, Inbox, Check, ArrowRight, Trash2, Filter } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';
import { Badge } from './Badge';
import { ScrollArea } from './ScrollArea';

export interface Notification {
  id: string;
  title: string;
  message: string;
  type: 'action' | 'success' | 'info' | 'critical';
  timestamp: string;
  isRead: boolean;
  actionLabel?: string;
}

export interface NotificationInboxProps {
  notifications: Notification[];
  onRead: (id: string) => void;
  onReadAll: () => void;
  onClear: () => void;
  onAction?: (id: string) => void;
  className?: string;
}

const NotificationInbox = ({
  notifications,
  onRead,
  onReadAll,
  onClear,
  onAction,
  className
}: NotificationInboxProps) => {
  const [filter, setFilter] = React.useState<'all' | 'unread' | 'action'>('all');

  const filtered = notifications.filter(n => {
    if (filter === 'unread') return !n.isRead;
    if (filter === 'action') return n.type === 'action';
    return true;
  });

  const unreadCount = notifications.filter(n => !n.isRead).length;

  return (
    <div className={cn('flex flex-col h-full bg-white border border-slate-200 rounded-ant-lg shadow-2xl overflow-hidden', className)}>
      <div className="p-4 border-b border-slate-100 bg-slate-50/50 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="relative">
            <Inbox className="h-5 w-5 text-brand-primary" />
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
              </span>
            )}
          </div>
          <h3 className="text-sm font-bold text-text-primary uppercase tracking-widest">Inbox</h3>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="sm" onClick={onReadAll} className="h-7 text-[10px] px-2">
            Mark all read
          </Button>
          <Button variant="ghost" size="sm" onClick={onClear} className="h-7 w-7 p-0 text-text-muted hover:text-red-500">
            <Trash2 size={14} />
          </Button>
        </div>
      </div>

      <div className="px-4 py-2 border-b border-slate-100 flex items-center space-x-2">
        <Filter size={12} className="text-text-muted" />
        <div className="flex space-x-1">
          {['all', 'unread', 'action'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f as any)}
              className={cn(
                "px-2 py-0.5 rounded text-[9px] font-bold uppercase transition-all",
                filter === f ? "bg-brand-primary text-white shadow-sm" : "text-text-muted hover:text-text-primary"
              )}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      <ScrollArea className="flex-1">
        {filtered.length === 0 ? (
          <div className="p-12 text-center flex flex-col items-center">
            <div className="h-12 w-12 rounded-full bg-slate-100 flex items-center justify-center mb-4">
              <Check className="h-6 w-6 text-slate-400" />
            </div>
            <p className="text-sm font-bold text-text-primary">All caught up!</p>
            <p className="text-xs text-text-muted mt-1">No new notifications matching your filter.</p>
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {filtered.map((n) => (
              <div
                key={n.id}
                onClick={() => !n.isRead && onRead(n.id)}
                className={cn(
                  'p-4 transition-all hover:bg-slate-50 cursor-pointer relative group',
                  !n.isRead && 'bg-blue-50/30'
                )}
              >
                {!n.isRead && (
                  <div className="absolute left-0 top-0 bottom-0 w-1 bg-brand-primary" />
                )}
                <div className="flex items-start justify-between mb-1">
                  <span className={cn(
                    "text-[10px] font-bold uppercase tracking-widest",
                    n.type === 'critical' ? "text-red-600" :
                    n.type === 'action' ? "text-amber-600" :
                    n.type === 'success' ? "text-emerald-600" : "text-brand-primary"
                  )}>
                    {n.type}
                  </span>
                  <span className="text-[9px] text-text-muted font-mono">{n.timestamp}</span>
                </div>
                <h4 className="text-sm font-bold text-text-primary mb-1 line-clamp-1">{n.title}</h4>
                <p className="text-xs text-text-secondary leading-relaxed line-clamp-2">{n.message}</p>

                {n.type === 'action' && n.actionLabel && (
                  <Button
                    size="sm"
                    className="mt-3 w-full h-8 text-[10px] font-bold uppercase"
                    onClick={(e) => {
                      e.stopPropagation();
                      onAction?.(n.id);
                    }}
                  >
                    {n.actionLabel}
                    <ArrowRight className="ml-1.5 h-3 w-3" />
                  </Button>
                )}
              </div>
            ))}
          </div>
        )}
      </ScrollArea>
    </div>
  );
};

export { NotificationInbox };
