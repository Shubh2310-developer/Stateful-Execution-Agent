import * as React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ChevronDown,
  ChevronRight,
  AlertCircle,
  CheckCircle2,
  Info,
  HelpCircle,
  ExternalLink,
  Brain
} from 'lucide-react';
import { cn } from '../../lib/utils';
import { Badge } from './Badge';
import { Button } from './Button';
import { Card } from './Card';
import { Tooltip } from './Tooltip';

export interface ThoughtOption {
  id: string;
  label: string;
  rationale: string;
  isChosen: boolean;
  confidence?: number;
}

export interface ThoughtUnit {
  id: string;
  timestamp: string;
  point: string;
  options: ThoughtOption[];
  rationale: string;
  source?: {
    type: 'memory' | 'artifact' | 'preference';
    label: string;
    id: string;
  };
  confidence: number;
  dependencies?: string[];
}

export interface ReasoningTreeProps {
  thoughts: ThoughtUnit[];
  onAskHuman?: (thought: ThoughtUnit) => void;
  onSourceClick?: (source: NonNullable<ThoughtUnit['source']>) => void;
  className?: string;
}

const ReasoningTree = ({
  thoughts,
  onAskHuman,
  onSourceClick,
  className
}: ReasoningTreeProps) => {
  return (
    <div className={cn('flex flex-col space-y-4 p-4', className)}>
      <div className="flex items-center space-x-2 mb-2">
        <Brain className="h-5 w-5 text-indigo-500" />
        <h3 className="text-lg font-semibold text-slate-100">Reasoning Trace</h3>
      </div>

      <div className="relative space-y-6">
        {/* Connector Line */}
        <div className="absolute left-6 top-2 bottom-2 w-px bg-slate-800" />

        {thoughts.map((thought, index) => (
          <ThoughtCard
            key={thought.id}
            thought={thought}
            index={index}
            onAskHuman={onAskHuman}
            onSourceClick={onSourceClick}
          />
        ))}
      </div>
    </div>
  );
};

const ThoughtCard = ({
  thought,
  index,
  onAskHuman,
  onSourceClick
}: {
  thought: ThoughtUnit;
  index: number;
  onAskHuman?: (thought: ThoughtUnit) => void;
  onSourceClick?: (source: NonNullable<ThoughtUnit['source']>) => void;
}) => {
  const [isExpanded, setIsExpanded] = React.useState(true);
  const isLowConfidence = thought.confidence < 0.7;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.3 }}
      className="relative pl-12"
    >
      {/* Timeline Bullet */}
      <div className={cn(
        "absolute left-4 top-2 h-4 w-4 rounded-full border-2 bg-slate-900 z-10",
        isLowConfidence ? "border-amber-500" : "border-indigo-500"
      )} />

      <Card className={cn(
        "overflow-hidden transition-all duration-300 border-l-4",
        isLowConfidence
          ? "bg-amber-500/5 border-amber-500 shadow-amber-500/10"
          : "bg-slate-900/50 border-indigo-500 shadow-indigo-500/10",
        "border-t-slate-800 border-r-slate-800 border-b-slate-800"
      )}>
        {/* Header */}
        <div
          className="flex items-center justify-between p-4 cursor-pointer hover:bg-white/5 transition-colors"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          <div className="flex items-center space-x-3 flex-1">
            <span className="text-sm font-medium text-slate-100">{thought.point}</span>
            <Badge
              variant={isLowConfidence ? "warning" : "default"}
              className={cn(
                "text-[10px] font-mono",
                isLowConfidence ? "bg-amber-500/20 text-amber-400" : "bg-indigo-500/20 text-indigo-400"
              )}
            >
              {(thought.confidence * 100).toFixed(0)}% Confidence
            </Badge>
          </div>
          <div className="flex items-center space-x-2">
            {isLowConfidence && (
              <Tooltip content="Uncertain decision point">
                <AlertCircle className="h-4 w-4 text-amber-500" />
              </Tooltip>
            )}
            {isExpanded ? <ChevronDown className="h-4 w-4 text-slate-400" /> : <ChevronRight className="h-4 w-4 text-slate-400" />}
          </div>
        </div>

        {/* Content */}
        <AnimatePresence>
          {isExpanded && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.25 }}
              className="overflow-hidden"
            >
              <div className="p-4 pt-0 space-y-4 border-t border-slate-800/50 mt-2">
                {/* Options */}
                <div className="space-y-2">
                  <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Options Evaluated</h4>
                  <div className="grid grid-cols-1 gap-2">
                    {thought.options.map((option) => (
                      <div
                        key={option.id}
                        className={cn(
                          "flex items-start space-x-2 p-2 rounded-md border text-xs",
                          option.isChosen
                            ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-100"
                            : "bg-slate-800/30 border-slate-700/50 text-slate-400"
                        )}
                      >
                        {option.isChosen ? (
                          <CheckCircle2 className="h-3 w-3 mt-0.5 text-emerald-500" />
                        ) : (
                          <div className="h-3 w-3 mt-0.5 rounded-full border border-slate-600" />
                        )}
                        <div className="flex-1">
                          <span className="font-semibold block">{option.label}</span>
                          <p className="text-[11px] mt-0.5 opacity-80 leading-relaxed">{option.rationale}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Rationale */}
                <div className="space-y-2">
                  <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Decision Rationale</h4>
                  <p className="text-sm text-slate-300 leading-relaxed bg-slate-800/30 p-3 rounded-md border border-slate-700/50">
                    {thought.rationale}
                  </p>
                </div>

                {/* Dependencies */}
                {thought.dependencies && thought.dependencies.length > 0 && (
                  <div className="space-y-2">
                    <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Dependencies</h4>
                    <div className="flex flex-wrap gap-2">
                      {thought.dependencies.map((depId) => (
                        <Badge key={depId} variant="outline" className="text-[9px] border-slate-700 text-slate-400">
                          {depId}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {/* Footer / Actions */}
                <div className="flex items-center justify-between pt-2">
                  <div className="flex items-center space-x-3">
                    {thought.source && (
                      <button
                        onClick={() => onSourceClick?.(thought.source!)}
                        className="flex items-center space-x-1.5 text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
                      >
                        <Info className="h-3 w-3" />
                        <span>Source: {thought.source.label}</span>
                        <ExternalLink className="h-2 w-2" />
                      </button>
                    )}
                  </div>

                  {isLowConfidence && onAskHuman && (
                    <Button
                      size="sm"
                      variant="outline"
                      className="h-7 text-[11px] border-amber-500/50 text-amber-500 hover:bg-amber-500/10"
                      onClick={() => onAskHuman(thought)}
                    >
                      <HelpCircle className="h-3 w-3 mr-1.5" />
                      Is this correct?
                    </Button>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </Card>
    </motion.div>
  );
};

export { ReasoningTree };
