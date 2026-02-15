import * as React from 'react';
import { Scale, MessageSquare, ShieldCheck, ChevronRight, AlertCircle } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { Badge } from './Badge';
import { Avatar } from './Avatar';

export interface ConflictAgent {
  name: string;
  role: string;
  avatarFallback: string;
  reasoning: string;
  evidence: string[];
}

export interface ConflictResolutionCardProps {
  title: string;
  agents: [ConflictAgent, ConflictAgent];
  resolution?: {
    winnerName: string;
    rationale: string;
  };
  onResolveManual?: (agentName: string) => void;
  className?: string;
}

const ConflictResolutionCard = ({
  title,
  agents,
  resolution,
  onResolveManual,
  className
}: ConflictResolutionCardProps) => {
  return (
    <Card className={cn('p-0 overflow-hidden border-amber-200 bg-amber-50/10', className)}>
      <div className="bg-amber-50 p-4 border-b border-amber-200 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Scale className="h-5 w-5 text-amber-600" />
          <h3 className="font-bold text-text-primary text-sm uppercase tracking-wider">
            Conflict: {title}
          </h3>
        </div>
        {!resolution && (
          <Badge variant="secondary" className="bg-amber-200 text-amber-800 animate-pulse">
            Awaiting Resolution
          </Badge>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-amber-100">
        {agents.map((agent, i) => (
          <div key={agent.name} className={cn(
            "p-5 flex flex-col h-full transition-all duration-300",
            resolution?.winnerName === agent.name ? "bg-emerald-50/30" : resolution ? "opacity-50 grayscale" : ""
          )}>
            <div className="flex items-center space-x-3 mb-4">
              <Avatar fallback={agent.avatarFallback} size="sm" />
              <div>
                <div className="text-sm font-bold text-text-primary">{agent.name}</div>
                <div className="text-[10px] text-text-muted uppercase font-bold">{agent.role}</div>
              </div>
              {resolution?.winnerName === agent.name && (
                <Badge variant="secondary" className="ml-auto bg-emerald-100 text-emerald-700 border-emerald-200">
                  Selected Path
                </Badge>
              )}
            </div>

            <div className="flex-1 space-y-4">
              <div className="p-3 bg-white rounded-ant-md border border-amber-100 text-xs leading-relaxed italic text-text-secondary">
                "{agent.reasoning}"
              </div>

              <div className="space-y-2">
                <span className="text-[10px] font-bold text-text-muted uppercase tracking-widest flex items-center">
                  <ShieldCheck className="h-3 w-3 mr-1" /> Supporting Evidence
                </span>
                <ul className="space-y-1">
                  {agent.evidence.map((item, j) => (
                    <li key={j} className="text-[11px] text-text-secondary flex items-start">
                      <ChevronRight className="h-3 w-3 mr-1 mt-0.5 text-amber-500 shrink-0" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {!resolution && onResolveManual && (
              <button
                onClick={() => onResolveManual(agent.name)}
                className="mt-6 w-full py-2 bg-white border border-amber-200 rounded-ant-md text-xs font-bold text-amber-700 hover:bg-amber-100 transition-all"
              >
                Select this path
              </button>
            )}
          </div>
        ))}
      </div>

      {resolution && (
        <div className="bg-emerald-50/50 p-4 border-t border-emerald-100">
          <div className="flex items-start space-x-3">
            <div className="h-6 w-6 rounded-full bg-emerald-100 flex items-center justify-center shrink-0">
              <MessageSquare className="h-3.5 w-3.5 text-emerald-600" />
            </div>
            <div>
              <span className="text-[10px] font-bold text-emerald-700 uppercase tracking-wider">
                Arbiter Resolution
              </span>
              <p className="text-xs text-text-secondary mt-1 leading-relaxed">
                {resolution.rationale}
              </p>
            </div>
          </div>
        </div>
      )}

      {!resolution && !onResolveManual && (
        <div className="p-3 bg-white/50 border-t border-amber-100 flex items-center justify-center space-x-2 text-[10px] text-text-muted italic">
          <AlertCircle className="h-3 w-3" />
          <span>Arbiter agent is currently evaluating evidence...</span>
        </div>
      )}
    </Card>
  );
};

export { ConflictResolutionCard };
