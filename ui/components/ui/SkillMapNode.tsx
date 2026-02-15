import * as React from 'react';
import { Star, TrendingUp } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Progress } from './Progress';

export interface SkillMapNodeProps {
  name: string;
  level: number;
  maxLevel?: number;
  xp: number;
  nextLevelXp: number;
  icon?: React.ReactNode;
  category?: string;
  isUnlocked?: boolean;
  className?: string;
}

const SkillMapNode = ({
  name,
  level,
  maxLevel = 10,
  xp,
  nextLevelXp,
  icon,
  category,
  isUnlocked = true,
  className
}: SkillMapNodeProps) => {
  const progress = (xp / nextLevelXp) * 100;

  return (
    <div className={cn(
      'group relative flex flex-col p-4 bg-white border rounded-ant-lg transition-all duration-300',
      isUnlocked ? 'border-slate-200 hover:border-brand-primary/50 hover:shadow-md' : 'border-slate-100 opacity-60 grayscale bg-slate-50',
      className
    )}>
      <div className="flex items-start justify-between mb-4">
        <div className={cn(
          "h-10 w-10 rounded-ant-md flex items-center justify-center transition-colors",
          isUnlocked ? "bg-brand-primary/10 text-brand-primary" : "bg-slate-200 text-slate-400"
        )}>
          {icon || <Star className="h-5 w-5" />}
        </div>
        <div className="text-right">
          <div className="text-[10px] font-bold text-text-muted uppercase tracking-widest">Level</div>
          <div className="text-lg font-bold text-text-primary leading-none">
            {level}<span className="text-xs text-text-muted">/{maxLevel}</span>
          </div>
        </div>
      </div>

      <div className="flex-1 mb-4">
        <h4 className="text-sm font-bold text-text-primary mb-1">{name}</h4>
        {category && (
          <span className="text-[10px] text-text-muted uppercase font-bold tracking-tight">
            {category}
          </span>
        )}
      </div>

      <div className="space-y-1.5">
        <div className="flex justify-between text-[10px] font-bold text-text-muted uppercase">
          <span>{Math.round(xp)} XP</span>
          <span>Next: {Math.round(nextLevelXp)}</span>
        </div>
        <Progress value={progress} size="sm" className={isUnlocked ? 'bg-brand-primary/10' : 'bg-slate-200'} />
      </div>

      {isUnlocked && progress > 80 && (
        <div className="absolute -top-1 -right-1">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-primary opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-brand-primary"></span>
          </span>
        </div>
      )}

      {!isUnlocked && (
        <div className="mt-4 pt-4 border-t border-slate-100 flex items-center text-[10px] font-bold text-text-muted uppercase">
          <TrendingUp className="h-3 w-3 mr-1.5" />
          <span>Locked capability</span>
        </div>
      )}
    </div>
  );
};

export { SkillMapNode };
