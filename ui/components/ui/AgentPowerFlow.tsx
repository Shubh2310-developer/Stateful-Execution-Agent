import * as React from 'react';
import { cn } from '../../lib/utils';

export interface AgentPowerFlowProps {
  intensity: number; // 0 to 1
  color?: string;
  className?: string;
}

const AgentPowerFlow = ({
  intensity,
  color = 'rgba(59, 130, 246, 0.2)',
  className
}: AgentPowerFlowProps) => {
  const particles = Array.from({ length: 15 });

  return (
    <div className={cn('absolute inset-0 overflow-hidden pointer-events-none z-0', className)}>
      <div className="absolute inset-0 opacity-40">
        {particles.map((_, i) => {
          const duration = 2 + Math.random() * 8 / (intensity || 0.1);
          const size = 1 + Math.random() * 3;
          const left = Math.random() * 100;
          const delay = Math.random() * 5;

          return (
            <div
              key={i}
              className="absolute bg-white rounded-full blur-[1px]"
              style={{
                width: size,
                height: size,
                left: `${left}%`,
                top: '-20px',
                backgroundColor: color,
                boxShadow: `0 0 10px ${color}`,
                animation: `flow ${duration}s linear infinite`,
                animationDelay: `${delay}s`,
                opacity: 0.1 + Math.random() * 0.4
              }}
            />
          );
        })}
      </div>
      <style dangerouslySetInnerHTML={{ __html: `
        @keyframes flow {
          0% { transform: translateY(0) translateX(0); opacity: 0; }
          10% { opacity: 1; }
          90% { opacity: 1; }
          100% { transform: translateY(100vh) translateX(${Math.random() * 100 - 50}px); opacity: 0; }
        }
      `}} />
    </div>
  );
};

export { AgentPowerFlow };
