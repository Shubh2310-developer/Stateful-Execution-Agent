import * as React from 'react';
import { cn } from '../../lib/utils';

export interface HolographicMarkProps {
  children: React.ReactNode;
  status?: 'emerald' | 'slate' | 'amber';
  isPulsing?: boolean;
  className?: string;
}

const HolographicMark = ({
  children,
  status = 'slate',
  isPulsing = false,
  className
}: HolographicMarkProps) => {
  const statusColors = {
    emerald: 'after:from-emerald-500/20 after:to-emerald-500/5 border-emerald-500/20',
    slate: 'after:from-slate-500/20 after:to-slate-500/5 border-slate-500/20',
    amber: 'after:from-amber-500/20 after:to-amber-500/5 border-amber-500/20',
  };

  return (
    <div className={cn(
      'relative group border rounded-ant-md transition-all duration-500 overflow-hidden',
      statusColors[status],
      className
    )}>
      {/* Shimmer/Holographic effect */}
      <div className={cn(
        "absolute inset-0 pointer-events-none z-0",
        "bg-gradient-to-tr from-transparent via-white/10 to-transparent",
        "translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000 ease-in-out",
        isPulsing && "animate-hologram-pulse"
      )} />

      {/* Background glow overlay */}
      <div className={cn(
        "absolute inset-0 pointer-events-none opacity-5 group-hover:opacity-10 transition-opacity",
        status === 'emerald' ? 'bg-emerald-500' : status === 'amber' ? 'bg-amber-500' : 'bg-slate-500'
      )} />

      <div className="relative z-10">
        {children}
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        @keyframes hologram-pulse {
          0%, 100% { opacity: 0.05; }
          50% { opacity: 0.15; }
        }
        .animate-hologram-pulse {
          animation: hologram-pulse 4s ease-in-out infinite;
        }
      `}} />
    </div>
  );
};

export { HolographicMark };
