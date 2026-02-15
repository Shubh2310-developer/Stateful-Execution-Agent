import * as React from 'react';
import { Moon, Zap, Power } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';

export interface IdleOverlayProps {
  isAsleep: boolean;
  wakeTime?: string;
  wakeReason?: string;
  onWake: () => void;
  className?: string;
}

const IdleOverlay = ({
  isAsleep,
  wakeTime,
  wakeReason,
  onWake,
  className
}: IdleOverlayProps) => {
  if (!isAsleep) return null;

  return (
    <div className={cn(
      'fixed inset-0 z-[100] flex flex-col items-center justify-center bg-slate-950/80 backdrop-blur-xl transition-all duration-500 animate-in fade-in',
      className
    )}>
      <div className="relative mb-12">
        <div className="absolute inset-0 bg-indigo-500/20 rounded-full blur-3xl animate-pulse" />
        <div className="relative flex h-24 w-24 items-center justify-center rounded-full bg-slate-900 border border-slate-800 shadow-2xl">
          <Moon size={40} className="text-indigo-400 animate-bounce" style={{ animationDuration: '4s' }} />
        </div>
      </div>

      <div className="text-center space-y-2 mb-12">
        <h2 className="text-2xl font-bold text-white tracking-tight">Agent in Deep Sleep</h2>
        <p className="text-slate-400 text-sm max-w-xs mx-auto">
          {wakeReason || 'The agent is currently in low-power mode to preserve resources and maintain focus.'}
        </p>
      </div>

      {wakeTime && (
        <div className="mb-12 p-4 bg-slate-900/50 border border-slate-800 rounded-ant-lg text-center">
          <div className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em] mb-1">Auto-wake schedule</div>
          <div className="text-lg font-mono font-bold text-indigo-400">{wakeTime}</div>
        </div>
      )}

      <div className="flex flex-col items-center space-y-4">
        <Button
          size="lg"
          onClick={onWake}
          className="bg-white text-slate-950 hover:bg-indigo-50 px-12 h-14 text-base font-bold shadow-xl shadow-indigo-500/10"
        >
          <Power className="h-5 w-5 mr-3" />
          Wake Agent
        </Button>
        <div className="flex items-center space-x-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">
          <Zap className="h-3 w-3" />
          <span>Daydreaming Optimization Active</span>
        </div>
      </div>
    </div>
  );
};

export { IdleOverlay };
