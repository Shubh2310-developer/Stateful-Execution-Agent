import * as React from 'react';
import { cn } from '../../lib/utils';

export interface TabItem {
  id: string;
  label: string;
  icon?: React.ReactNode;
  disabled?: boolean;
}

export interface TabsProps {
  tabs: TabItem[];
  activeTab: string;
  onChange: (id: string) => void;
  variant?: 'underline' | 'pills';
  className?: string;
}

const Tabs = ({ tabs, activeTab, onChange, variant = 'underline', className }: TabsProps) => {
  return (
    <div className={cn(
      'flex space-x-1',
      variant === 'underline' ? 'border-b border-slate-200' : 'bg-slate-100 p-1 rounded-ant-lg',
      className
    )}>
      {tabs.map((tab) => {
        const isActive = activeTab === tab.id;

        return (
          <button
            key={tab.id}
            onClick={() => !tab.disabled && onChange(tab.id)}
            disabled={tab.disabled}
            className={cn(
              'relative flex items-center px-4 py-2 text-sm font-medium transition-all duration-200 focus-visible:outline-none disabled:opacity-50 disabled:cursor-not-allowed',
              variant === 'underline'
                ? cn(
                    'text-text-muted hover:text-text-primary',
                    isActive && 'text-brand-primary'
                  )
                : cn(
                    'rounded-ant-md px-3 py-1.5',
                    isActive ? 'bg-white text-brand-primary shadow-sm' : 'text-text-muted hover:text-text-primary hover:bg-white/50'
                  )
            )}
          >
            {tab.icon && <span className="mr-2">{tab.icon}</span>}
            {tab.label}

            {variant === 'underline' && isActive && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-brand-primary animate-in fade-in zoom-in-x-0" />
            )}
          </button>
        );
      })}
    </div>
  );
};

export { Tabs };
