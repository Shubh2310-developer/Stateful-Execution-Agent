import * as React from 'react';
import { Play, Clock, Globe, Laptop, ChevronDown, Check } from 'lucide-react';
import { cn } from '../../lib/utils';
import { DropdownMenu } from './DropdownMenu';
import { Badge } from './Badge';

export interface StatefulSession {
  id: string;
  name: string;
  lastActive: string;
  environment: 'production' | 'staging' | 'local';
  isActive?: boolean;
}

export interface SessionSwitcherProps {
  sessions: StatefulSession[];
  onSwitch: (id: string) => void;
  className?: string;
}

const SessionSwitcher = ({ sessions, onSwitch, className }: SessionSwitcherProps) => {
  const activeSession = sessions.find(s => s.isActive) || sessions[0];

  const envIcons = {
    production: <Globe className="h-3 w-3" />,
    staging: <Globe className="h-3 w-3 opacity-50" />,
    local: <Laptop className="h-3 w-3" />,
  };

  return (
    <div className={cn('relative', className)}>
      <DropdownMenu
        align="left"
        trigger={
          <button className="flex items-center space-x-3 p-2 rounded-ant-md hover:bg-slate-100 transition-all border border-transparent hover:border-slate-200">
            <div className="h-8 w-8 rounded bg-brand-primary/10 flex items-center justify-center text-brand-primary font-bold text-xs shadow-inner">
              {activeSession?.name.charAt(0)}
            </div>
            <div className="text-left hidden md:block">
              <div className="flex items-center space-x-2">
                <span className="text-xs font-bold text-text-primary leading-none">{activeSession?.name}</span>
                <Badge variant="secondary" className="text-[8px] h-3.5 px-1.5 bg-slate-100">
                  {activeSession?.environment}
                </Badge>
              </div>
              <span className="text-[10px] text-text-muted leading-none mt-1 flex items-center">
                <Clock className="h-2 w-2 mr-1" /> {activeSession?.lastActive}
              </span>
            </div>
            <ChevronDown className="h-4 w-4 text-text-muted" />
          </button>
        }
        items={sessions.map(session => ({
          id: session.id,
          label: session.name,
          icon: session.isActive ? <Check className="h-3 w-3 text-brand-primary" /> : envIcons[session.environment],
          onClick: () => onSwitch(session.id),
          className: session.isActive ? 'bg-brand-primary/5 font-bold' : ''
        }))}
      />
    </div>
  );
};

export { SessionSwitcher };
