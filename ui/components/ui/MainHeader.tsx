import * as React from 'react';
import { Search, Filter, Settings, Bell, User } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Avatar } from './Avatar';
import { Badge } from './Badge';

export interface MainHeaderProps {
  title?: string;
  showSearch?: boolean;
  onSearch?: (query: string) => void;
  notificationCount?: number;
  userName?: string;
  userRole?: string;
  className?: string;
}

const MainHeader = ({
  title,
  showSearch = true,
  onSearch,
  notificationCount = 0,
  userName = "Operator",
  userRole = "Admin",
  className
}: MainHeaderProps) => {
  return (
    <div className={cn('flex h-full items-center justify-between px-6', className)}>
      <div className="flex items-center space-x-4">
        {title && (
          <h1 className="text-lg font-bold text-text-primary tracking-tight">
            {title}
          </h1>
        )}
        {showSearch && (
          <div className="relative hidden md:block">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-text-muted" />
            <input
              type="text"
              placeholder="Search missions, artifacts, memory..."
              className="w-80 rounded-full border border-slate-200 bg-slate-50 py-1.5 pl-10 pr-4 text-sm transition-all focus:border-brand-primary focus:bg-white focus:outline-none focus:ring-2 focus:ring-brand-primary/10"
              onChange={(e) => onSearch?.(e.target.value)}
            />
          </div>
        )}
      </div>

      <div className="flex items-center space-x-6">
        <div className="flex items-center space-x-2">
          <button className="relative p-2 text-text-muted hover:text-text-primary transition-colors rounded-full hover:bg-slate-100">
            <Bell className="h-5 w-5" />
            {notificationCount > 0 && (
              <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-status-error border-2 border-white" />
            )}
          </button>
          <button className="p-2 text-text-muted hover:text-text-primary transition-colors rounded-full hover:bg-slate-100">
            <Settings className="h-5 w-5" />
          </button>
        </div>

        <div className="h-8 w-[1px] bg-slate-200" />

        <div className="flex items-center space-x-3">
          <div className="text-right hidden sm:block">
            <div className="text-sm font-bold text-text-primary leading-none">
              {userName}
            </div>
            <div className="text-[10px] font-bold text-text-muted uppercase tracking-wider mt-1">
              {userRole}
            </div>
          </div>
          <Avatar fallback={userName} />
        </div>
      </div>
    </div>
  );
};

export { MainHeader };
