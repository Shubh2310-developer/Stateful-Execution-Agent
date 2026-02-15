import * as React from 'react';
import { Shield, Zap, Target, Cpu, MessageSquare } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { Avatar } from './Avatar';
import { Badge } from './Badge';
import { Progress } from './Progress';
import { Button } from './Button';

export interface AgentIdentityCardProps {
  name: string;
  role: string;
  avatarSrc?: string;
  avatarFallback: string;
  status: 'active' | 'idle' | 'busy' | 'offline';
  skills: string[];
  traits: { label: string; value: number }[];
  performance: {
    successRate: number;
    efficiency: number;
  };
  className?: string;
}

const AgentIdentityCard = ({
  name,
  role,
  avatarSrc,
  avatarFallback,
  status,
  skills,
  traits,
  performance,
  className
}: AgentIdentityCardProps) => {
  const statusColors = {
    active: 'bg-emerald-500',
    idle: 'bg-slate-400',
    busy: 'bg-amber-500',
    offline: 'bg-red-500',
  };

  return (
    <Card className={cn('p-6 hover:shadow-lg transition-all duration-300 border-slate-200', className)}>
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Avatar src={avatarSrc} fallback={avatarFallback} size="lg" isAgent />
            <div className={cn(
              "absolute bottom-0 right-0 h-3.5 w-3.5 rounded-full border-2 border-white",
              statusColors[status]
            )} />
          </div>
          <div>
            <h3 className="text-lg font-bold text-text-primary tracking-tight">{name}</h3>
            <span className="text-xs font-bold text-text-muted uppercase tracking-widest">{role}</span>
          </div>
        </div>
        <Badge variant="secondary" className="bg-slate-100 text-slate-600">
          Agent Node
        </Badge>
      </div>

      <div className="space-y-6">
        {/* Traits */}
        <div className="space-y-3">
          <h4 className="text-[10px] font-bold text-text-muted uppercase tracking-[0.2em] flex items-center">
            <Cpu className="h-3 w-3 mr-2" /> Personality Matrix
          </h4>
          <div className="grid grid-cols-2 gap-4">
            {traits.map((trait) => (
              <div key={trait.label} className="space-y-1">
                <div className="flex justify-between text-[10px] font-medium text-text-secondary">
                  <span>{trait.label}</span>
                  <span>{trait.value}%</span>
                </div>
                <Progress value={trait.value} size="sm" className="bg-slate-100" />
              </div>
            ))}
          </div>
        </div>

        {/* Skills */}
        <div className="space-y-3">
          <h4 className="text-[10px] font-bold text-text-muted uppercase tracking-[0.2em] flex items-center">
            <Zap className="h-3 w-3 mr-2" /> Core Capabilities
          </h4>
          <div className="flex flex-wrap gap-2">
            {skills.map((skill) => (
              <Badge key={skill} variant="outline" className="border-slate-200 text-text-secondary font-medium">
                {skill}
              </Badge>
            ))}
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="pt-6 border-t border-slate-100 grid grid-cols-2 gap-4">
          <div className="flex flex-col">
            <span className="text-[10px] font-bold text-text-muted uppercase tracking-wider mb-1">
              Success Rate
            </span>
            <span className="text-lg font-bold text-emerald-600">
              {performance.successRate}%
            </span>
          </div>
          <div className="flex flex-col">
            <span className="text-[10px] font-bold text-text-muted uppercase tracking-wider mb-1">
              Efficiency
            </span>
            <div className="flex items-center space-x-2">
              <span className="text-lg font-bold text-brand-primary">
                {performance.efficiency}x
              </span>
              <span className="text-[10px] text-text-muted">vs manual</span>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 flex items-center space-x-2 pt-4">
        <Button variant="ghost" size="sm" className="flex-1 h-9 text-xs">
          <MessageSquare className="h-3.5 w-3.5 mr-2" />
          View Logs
        </Button>
        <Button variant="ghost" size="sm" className="flex-1 h-9 text-xs">
          <Target className="h-3.5 w-3.5 mr-2" />
          Adjust Prompt
        </Button>
      </div>
    </Card>
  );
};

export { AgentIdentityCard };
