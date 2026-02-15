import * as React from 'react';
import { cn } from '../../lib/utils';

export interface ProbabilityGlowProps {
  children: React.ReactNode;
  probability: number; // 0 to 1.0
  variant?: 'superposition' | 'confidence' | 'entropy';
  className?: string;
}

const ProbabilityGlow = ({
  children,
  probability,
  variant = 'confidence',
  className
}: ProbabilityGlowProps) => {
  const getStyles = () => {
    switch (variant) {
      case 'superposition':
        return {
          opacity: 0.3 + probability * 0.7,
          filter: `blur(${ (1 - probability) * 4 }px)`,
          borderStyle: probability < 0.5 ? 'dashed' : 'solid',
          borderColor: `rgba(99, 102, 241, ${probability})`
        };
      case 'confidence':
        const color = probability > 0.8 ? 'rgba(16, 185, 129, 0.1)' : probability > 0.5 ? 'rgba(59, 130, 246, 0.1)' : 'rgba(245, 158, 11, 0.1)';
        return {
          backgroundColor: color,
          boxShadow: `0 0 ${probability * 20}px rgba(59, 130, 246, ${probability * 0.2})`
        };
      case 'entropy':
        return {
          filter: `grayscale(${ 1 - probability })`,
          opacity: 0.5 + probability * 0.5
        };
      default:
        return {};
    }
  };

  return (
    <div
      className={cn('transition-all duration-500 rounded-ant-md', className)}
      style={getStyles()}
    >
      {children}
    </div>
  );
};

export { ProbabilityGlow };
