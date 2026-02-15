import * as React from 'react';
import { cn } from '../../lib/utils';

export interface VoiceWaveformProps {
  isActive?: boolean;
  color?: string;
  className?: string;
}

const VoiceWaveform = ({
  isActive = false,
  color = 'var(--color-brand-primary)',
  className
}: VoiceWaveformProps) => {
  const bars = Array.from({ length: 12 });

  return (
    <div className={cn('flex items-center justify-center space-x-1 h-8 px-4', className)}>
      {bars.map((_, i) => (
        <div
          key={i}
          className={cn(
            'w-1 rounded-full transition-all duration-300',
            isActive ? 'animate-waveform' : 'h-1 opacity-30'
          )}
          style={{
            backgroundColor: color,
            animationDelay: `${i * 100}ms`,
            height: isActive ? `${Math.random() * 100}%` : '4px'
          }}
        />
      ))}
      <style dangerouslySetInnerHTML={{ __html: `
        @keyframes waveform {
          0%, 100% { height: 4px; opacity: 0.5; }
          50% { height: 100%; opacity: 1; }
        }
        .animate-waveform {
          animation: waveform 1s ease-in-out infinite;
        }
      `}} />
    </div>
  );
};

export { VoiceWaveform };
