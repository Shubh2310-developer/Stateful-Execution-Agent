import * as React from 'react';
import { LucideIcon } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface SidebarItemProps {
  icon: LucideIcon;
  label: string;
  isActive?: boolean;
  isCollapsed?: boolean;
  onClick?: () => void;
  badge?: string | number;
  className?: string;
}

const SidebarItem = ({
  icon: Icon,
  label,
  isActive = false,
  isCollapsed = false,
  onClick,
  badge,
  className
}: SidebarItemProps) => {
  return (
    <button
      onClick={onClick}
      className={cn(
        'group relative flex items-center w-full px-3 py-2 rounded-ant-md transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary',
        isActive
          ? 'bg-brand-primary/10 text-brand-primary'
          : 'text-text-secondary hover:bg-slate-100 hover:text-text-primary',
        className
      )}
    >
      <Icon className={cn(
        'h-5 w-5 flex-shrink-0 transition-colors',
        isActive ? 'text-brand-primary' : 'text-text-muted group-hover:text-text-primary'
      )} />

      {!isCollapsed && (
        <span className="ml-3 text-sm font-medium truncate animate-in fade-in slide-in-from-left-2 duration-300">
          {label}
        </span>
      )}

      {!isCollapsed && badge !== undefined && (
        <span className={cn(
          'ml-auto text-[10px] font-bold px-1.5 py-0.5 rounded-full min-w-[20px] flex items-center justify-center',
          isActive ? 'bg-brand-primary text-white' : 'bg-slate-200 text-slate-600'
        )}>
          {badge}
        </span>
      )}

      {/* Tooltip for collapsed state */}
      {isCollapsed && (
        <div className="absolute left-full ml-4 px-2 py-1 bg-slate-900 text-white text-xs rounded opacity-0 pointer-events-none group-hover:opacity-100 transition-opacity whitespace-nowrap z-50">
          {label}
        </div>
      )}

      {/* Active Indicator Line */}
      {isActive && (
        <div className="absolute left-0 w-1 h-6 bg-brand-primary rounded-r-full" />
      )}
    </button>
  );
};

export { SidebarItem };
