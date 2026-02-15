import * as React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Plus,
  Minus,
  Edit3,
  ChevronDown,
  ChevronRight,
  Filter,
  Code,
  Languages,
  ArrowRight,
  History
} from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';
import { Badge } from './Badge';
import { Tooltip } from './Tooltip';
import { JsonView } from './JsonView';

export type DiffType = 'added' | 'removed' | 'modified';

export interface StateChange {
  path: string;
  type: DiffType;
  oldValue?: any;
  newValue?: any;
  semanticSummary: string;
  category: 'plan' | 'artifact' | 'memory' | 'trace' | 'other';
}

export interface StateDiffProps {
  baselineVersion: number;
  comparisonVersion: number;
  changes: StateChange[];
  onJumpToTrace?: (path: string) => void;
  className?: string;
}

const StateDiff = ({
  baselineVersion,
  comparisonVersion,
  changes,
  onJumpToTrace,
  className
}: StateDiffProps) => {
  const [viewMode, setViewMode] = React.useState<'semantic' | 'technical'>('semantic');
  const [filter, setFilter] = React.useState<string[]>([]);
  const [expandedGroups, setExpandedGroups] = React.useState<Record<string, boolean>>({});

  const categories = Array.from(new Set(changes.map(c => c.category)));

  const filteredChanges = changes.filter(c =>
    filter.length === 0 || filter.includes(c.category)
  );

  // Group by top-level key (first part of path)
  const groupedChanges = filteredChanges.reduce((acc, change) => {
    const root = change.path.split('.')[0] || 'other';
    if (!acc[root]) acc[root] = [];
    acc[root].push(change);
    return acc;
  }, {} as Record<string, StateChange[]>);

  const toggleGroup = (group: string) => {
    setExpandedGroups(prev => ({
      ...prev,
      [group]: !prev[group]
    }));
  };

  const getDiffColor = (type: DiffType) => {
    switch (type) {
      case 'added': return 'emerald';
      case 'removed': return 'red';
      case 'modified': return 'blue';
    }
  };

  return (
    <div className={cn("flex flex-col space-y-4", className)}>
      {/* Controls */}
      <div className="flex items-center justify-between bg-slate-900/50 p-2 rounded-lg border border-slate-800">
        <div className="flex items-center space-x-2">
          <History className="h-4 w-4 text-slate-400" />
          <div className="flex items-center text-xs font-mono">
            <span className="text-slate-500">Comparing</span>
            <Badge variant="outline" className="mx-1.5 py-0 px-1.5 h-5 bg-slate-800 border-slate-700">v{baselineVersion}</Badge>
            <ArrowRight className="h-3 w-3 text-slate-600 mx-1" />
            <Badge variant="outline" className="mx-1.5 py-0 px-1.5 h-5 bg-indigo-500/10 border-indigo-500/30 text-indigo-400">v{comparisonVersion}</Badge>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <div className="flex bg-slate-800 rounded-md p-0.5 border border-slate-700">
            <button
              onClick={() => setViewMode('semantic')}
              className={cn(
                "px-2 py-1 text-[10px] font-bold uppercase rounded transition-all",
                viewMode === 'semantic' ? "bg-slate-700 text-white shadow-sm" : "text-slate-500 hover:text-slate-300"
              )}
            >
              <Languages className="h-3 w-3 inline mr-1" />
              Semantic
            </button>
            <button
              onClick={() => setViewMode('technical')}
              className={cn(
                "px-2 py-1 text-[10px] font-bold uppercase rounded transition-all",
                viewMode === 'technical' ? "bg-slate-700 text-white shadow-sm" : "text-slate-500 hover:text-slate-300"
              )}
            >
              <Code className="h-3 w-3 inline mr-1" />
              Technical
            </button>
          </div>
        </div>
      </div>

      {/* Filter Chips */}
      <div className="flex flex-wrap gap-2">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => {
              setFilter(prev =>
                prev.includes(cat) ? prev.filter(c => c !== cat) : [...prev, cat]
              );
            }}
            className={cn(
              "px-2 py-1 rounded-full text-[10px] font-bold uppercase border transition-all",
              filter.includes(cat)
                ? "bg-indigo-500/20 border-indigo-500/50 text-indigo-400"
                : "bg-slate-900 border-slate-800 text-slate-500 hover:border-slate-700"
            )}
          >
            {cat}
          </button>
        ))}
        {filter.length > 0 && (
          <button
            onClick={() => setFilter([])}
            className="text-[10px] text-slate-500 hover:text-slate-300 underline underline-offset-2 ml-2"
          >
            Clear Filters
          </button>
        )}
      </div>

      {/* Diff Content */}
      <div className="space-y-3">
        {Object.entries(groupedChanges).map(([group, groupChanges]) => (
          <div key={group} className="border border-slate-800 rounded-ant-lg bg-slate-900/30 overflow-hidden">
            <div
              className="flex items-center justify-between px-4 py-2 bg-slate-900/50 cursor-pointer hover:bg-slate-800/50 transition-colors border-b border-slate-800"
              onClick={() => toggleGroup(group)}
            >
              <div className="flex items-center space-x-2">
                {expandedGroups[group] === false ? <ChevronRight className="h-4 w-4 text-slate-500" /> : <ChevronDown className="h-4 w-4 text-slate-500" />}
                <span className="text-xs font-bold font-mono text-slate-300 uppercase tracking-widest">{group}</span>
                <span className="text-[10px] text-slate-600 bg-slate-800 px-1.5 rounded-full">{groupChanges.length}</span>
              </div>
            </div>

            <AnimatePresence initial={false}>
              {expandedGroups[group] !== false && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.2 }}
                  className="overflow-hidden"
                >
                  <div className="divide-y divide-slate-800/50">
                    {groupChanges.map((change, idx) => (
                      <div key={`${change.path}-${idx}`} className="p-3 hover:bg-white/[0.02] transition-colors group">
                        <div className="flex items-start justify-between">
                          <div className="flex items-start space-x-3 flex-1 min-w-0">
                            <div className={cn(
                              "p-1.5 rounded mt-0.5 shrink-0",
                              change.type === 'added' && "bg-emerald-500/10 text-emerald-500",
                              change.type === 'removed' && "bg-red-500/10 text-red-500",
                              change.type === 'modified' && "bg-blue-500/10 text-blue-500"
                            )}>
                              {change.type === 'added' && <Plus className="h-3 w-3" />}
                              {change.type === 'removed' && <Minus className="h-3 w-3" />}
                              {change.type === 'modified' && <Edit3 className="h-3 w-3" />}
                            </div>

                            <div className="flex flex-col min-w-0 flex-1">
                              <div className="flex items-center space-x-2 mb-1">
                                <span className="text-[10px] font-mono text-slate-500 truncate">{change.path}</span>
                                <Badge
                                  className={cn(
                                    "text-[8px] h-3 px-1 font-bold uppercase",
                                    catColors[change.category]
                                  )}
                                >
                                  {change.category}
                                </Badge>
                              </div>

                              {viewMode === 'semantic' ? (
                                <p className="text-sm text-slate-200 leading-relaxed">
                                  {change.semanticSummary}
                                </p>
                              ) : (
                                <div className="space-y-2 mt-1">
                                  {change.type === 'modified' && (
                                    <div className="flex flex-col space-y-1">
                                      <div className="text-[10px] text-slate-500 flex items-center">
                                        <Minus className="h-2 w-2 mr-1" /> WAS
                                      </div>
                                      <div className="bg-red-500/5 border border-red-500/20 rounded p-2 overflow-x-auto max-h-32 scrollbar-hide">
                                        <JsonView data={change.oldValue} className="bg-transparent p-0" />
                                      </div>
                                    </div>
                                  )}
                                  <div className="flex flex-col space-y-1">
                                    <div className="text-[10px] text-slate-500 flex items-center">
                                      <Plus className="h-2 w-2 mr-1" /> {change.type === 'modified' ? 'IS' : 'CONTENT'}
                                    </div>
                                    <div className={cn(
                                      "border rounded p-2 overflow-x-auto max-h-32 scrollbar-hide",
                                      change.type === 'added' ? "bg-emerald-500/5 border-emerald-500/20" :
                                      change.type === 'removed' ? "bg-red-500/5 border-red-500/20 text-red-400 opacity-60" :
                                      "bg-blue-500/5 border-blue-500/20"
                                    )}>
                                      <JsonView data={change.newValue} className="bg-transparent p-0" />
                                    </div>
                                  </div>
                                </div>
                              )}
                            </div>
                          </div>

                          <div className="flex items-center space-x-2 shrink-0 ml-4 opacity-0 group-hover:opacity-100 transition-opacity">
                            <Tooltip content="Jump to Trace">
                              <Button
                                variant="ghost"
                                size="icon"
                                className="h-7 w-7 text-slate-500 hover:text-indigo-400"
                                onClick={() => onJumpToTrace?.(change.path)}
                              >
                                <ArrowRight className="h-3.5 w-3.5" />
                              </Button>
                            </Tooltip>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}

        {Object.keys(groupedChanges).length === 0 && (
          <div className="py-12 flex flex-col items-center justify-center text-slate-500 bg-slate-900/20 rounded-xl border border-dashed border-slate-800">
            <Filter className="h-8 w-8 mb-3 opacity-20" />
            <p className="text-sm">No changes found matching the selected filters</p>
          </div>
        )}
      </div>
    </div>
  );
};

const catColors: Record<string, string> = {
  plan: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  artifact: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
  memory: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
  trace: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
  other: 'bg-slate-500/10 text-slate-400 border-slate-500/20'
};

export { StateDiff };
