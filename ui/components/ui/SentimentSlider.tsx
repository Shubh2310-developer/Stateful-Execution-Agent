import * as React from 'react';
import { cn } from '../../lib/utils';
import { Smile, Meh, Frown, Zap, Info } from 'lucide-react';

export interface SentimentSliderProps {
  value: number; // 0 to 100
  onChange: (value: number) => void;
  label?: string;
  className?: string;
}

const SentimentSlider = ({
  value,
  onChange,
  label = "Agent Tone Preference",
  className
}: SentimentSliderProps) => {
  const getIcon = () => {
    if (value > 75) return <Smile size={20} className="text-emerald-500" />;
    if (value > 40) return <Meh size={20} className="text-amber-500" />;
    return <Frown size={20} className="text-red-500" />;
  };

  const getLabel = () => {
    if (value > 85) return 'Concise & Direct';
    if (value > 65) return 'Professional';
    if (value > 35) return 'Conversational';
    return 'Detailed & Creative';
  };

  return (
    <div className={cn('p-4 bg-slate-50 border border-slate-200 rounded-ant-lg', className)}>
      <div className="flex items-center justify-between mb-4">
        <span className="text-[10px] font-bold text-text-muted uppercase tracking-widest">{label}</span>
        <div className="flex items-center space-x-2 bg-white px-2 py-1 rounded-full border border-slate-200 shadow-sm transition-all duration-300">
          {getIcon()}
          <span className="text-[11px] font-bold text-text-primary uppercase tracking-tight">{getLabel()}</span>
        </div>
      </div>

      <div className="px-2">
        <input
          type="range"
          min="0"
          max="100"
          value={value}
          onChange={(e) => onChange(parseInt(e.target.value))}
          className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-brand-primary focus:outline-none focus:ring-2 focus:ring-brand-primary/20"
        />
        <div className="flex justify-between mt-2 text-[8px] font-bold text-text-muted uppercase tracking-tighter">
          <span>Creative</span>
          <span>Standard</span>
          <span>Hyper-Efficient</span>
        </div>
      </div>

      <div className="mt-6 flex items-start space-x-2">
        <div className="p-1 bg-brand-primary/10 rounded text-brand-primary">
          <Zap size={10} />
        </div>
        <p className="text-[9px] text-text-muted leading-relaxed">
          This setting adjusts the <span className="font-bold text-text-secondary">Instruction Temperature</span> and <span className="font-bold text-text-secondary">Verbosity Constraints</span> in the agent's core prompt system.
        </p>
      </div>
    </div>
  );
};

export { SentimentSlider };
