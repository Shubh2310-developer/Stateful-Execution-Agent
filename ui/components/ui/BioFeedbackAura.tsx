import * as React from 'react';
import { cn } from '../../lib/utils';

export interface BioFeedbackAuraProps {
  children: React.ReactNode;
  focusLevel: number; // 0 to 100
  stressLevel?: number; // 0 to 100
  isActive?: boolean;
  className?: string;
}

const BioFeedbackAura = ({
  children,
  focusLevel,
  stressLevel = 0,
  isActive = true,
  className
}: BioFeedbackAuraProps) => {
  // Focus color: Indigo -> Blue -> Emerald
  // Stress color: Slate -> Amber -> Red

  const getAuraColor = () => {
    if (stressLevel > 70) return 'rgba(239, 68, 68, 0.4)'; // Red
    if (stressLevel > 40) return 'rgba(245, 158, 11, 0.4)'; // Amber
    if (focusLevel > 80) return 'rgba(16, 185, 129, 0.4)'; // Emerald
    if (focusLevel > 50) return 'rgba(59, 130, 246, 0.4)'; // Blue
    return 'rgba(99, 102, 241, 0.4)'; // Indigo
  };

  const auraSize = 4 + (focusLevel / 100) * 12; // 4px to 16px
  const pulseSpeed = 4 - (focusLevel / 100) * 3; // 4s to 1s

  return (
    <div className={cn('relative inline-flex items-center justify-center p-2', className)}>
      {isActive && (
        <div
          className="absolute inset-0 rounded-full animate-pulse blur-md transition-all duration-1000"
          style={{
            boxShadow: `0 0 ${auraSize}px ${auraSize/2}px ${getAuraColor()}`,
            animationDuration: `${pulseSpeed}s`
          }}
        />
      )}
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
};

export { BioFeedbackAura };
