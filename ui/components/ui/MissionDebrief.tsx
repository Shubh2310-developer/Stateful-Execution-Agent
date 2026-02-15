import * as React from 'react';
import {
  Trophy,
  Target,
  TrendingUp,
  Zap,
  Brain,
  History,
  Download,
  Share2,
  CheckCircle2,
  ChevronRight,
  Clock,
  Layout
} from 'lucide-react';
import { motion } from 'framer-motion';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { Button } from './Button';
import { Badge } from './Badge';
import { OutcomeCard } from './OutcomeCard';
import { GanttChart, GanttTask } from './GanttChart';
import { RequirementChecklist, Requirement } from './RequirementChecklist';
import { StatCard } from './StatCard';

export interface Achievement {
  id: string;
  label: string;
  description: string;
}

export interface LearningItem {
  id: string;
  text: string;
  type: 'preference' | 'fact' | 'pattern';
}

export interface MissionDebriefProps {
  missionId: string;
  goal: string;
  summary: string;
  achievements: Achievement[];
  requirements: Requirement[];
  ganttTasks: GanttTask[];
  learnings: LearningItem[];
  timeSaved: string;
  computeCost: string;
  onExport?: (format: 'pdf' | 'json') => void;
  onShare?: () => void;
  onPromoteToTemplate?: () => void;
  className?: string;
}

const MissionDebrief = ({
  missionId,
  goal,
  summary,
  achievements,
  requirements,
  ganttTasks,
  learnings,
  timeSaved,
  computeCost,
  onExport,
  onShare,
  onPromoteToTemplate,
  className
}: MissionDebriefProps) => {
  return (
    <div className={cn('max-w-5xl mx-auto space-y-8 pb-20', className)}>
      {/* Header Actions */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-text-primary tracking-tight">Mission Debrief</h1>
          <p className="text-sm text-text-muted font-mono uppercase">ID: {missionId}</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="secondary" size="sm" onClick={() => onExport?.('pdf')}>
            <Download className="h-4 w-4 mr-2" />
            Download PDF
          </Button>
          <Button variant="secondary" size="sm" onClick={onShare}>
            <Share2 className="h-4 w-4 mr-2" />
            Share
          </Button>
          <Button variant="primary" size="sm" onClick={onPromoteToTemplate} className="bg-brand-cta border-brand-cta hover:opacity-90">
            <Layout className="h-4 w-4 mr-2" />
            Save as Template
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Summary & Achievements */}
        <div className="lg:col-span-2 space-y-8">
          <OutcomeCard
            goal={goal}
            summary={summary}
            impactMetrics={[
              { label: 'Time Saved', value: timeSaved },
              { label: 'Compute Cost', value: computeCost },
              { label: 'Confidence', value: '98%' }
            ]}
          />

          <Card className="p-6">
            <div className="flex items-center space-x-2 mb-6">
              <Trophy className="h-5 w-5 text-amber-500" />
              <h3 className="text-lg font-bold text-text-primary uppercase tracking-widest">Key Achievements</h3>
            </div>
            <div className="space-y-4">
              {achievements.map((achievement, i) => (
                <div key={achievement.id} className="flex items-start space-x-4 p-4 rounded-ant-md bg-slate-50 border border-slate-100 transition-all hover:border-amber-200">
                  <div className="flex h-6 w-6 items-center justify-center rounded-full bg-white border border-slate-200 text-xs font-bold text-amber-600 shadow-sm shrink-0">
                    {i + 1}
                  </div>
                  <div>
                    <h4 className="text-sm font-bold text-text-primary">{achievement.label}</h4>
                    <p className="text-xs text-text-secondary mt-1 leading-relaxed">{achievement.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center space-x-2 mb-6">
              <Clock className="h-5 w-5 text-brand-primary" />
              <h3 className="text-lg font-bold text-text-primary uppercase tracking-widest">Execution Timeline</h3>
            </div>
            <GanttChart tasks={ganttTasks} />
          </Card>
        </div>

        {/* Right Column: Compliance & Learning */}
        <div className="space-y-8">
          <Card className="p-6 bg-slate-900 border-slate-800 text-white">
            <RequirementChecklist
              requirements={requirements}
              title="Constraint Compliance"
              className="[&_h3]:text-white [&_span]:text-slate-300"
            />
          </Card>

          <Card className="p-6 overflow-hidden relative group">
            {/* Background pattern */}
            <div className="absolute -right-4 -bottom-4 opacity-5 group-hover:scale-110 transition-transform duration-500">
              <Brain size={120} />
            </div>

            <div className="relative z-10">
              <div className="flex items-center space-x-2 mb-6">
                <Brain className="h-5 w-5 text-emerald-500" />
                <h3 className="text-lg font-bold text-text-primary uppercase tracking-widest">Learning Summary</h3>
              </div>
              <div className="space-y-3">
                {learnings.map((learning) => (
                  <div key={learning.id} className="p-3 rounded-ant-md bg-emerald-50 border border-emerald-100 animate-in slide-in-from-right-4 duration-300">
                    <div className="flex items-center space-x-2 mb-1">
                      <Badge variant="secondary" className="bg-emerald-100 text-emerald-700 text-[8px] uppercase">
                        {learning.type}
                      </Badge>
                      <span className="text-[10px] font-bold text-emerald-800 uppercase tracking-tighter">New Knowledge</span>
                    </div>
                    <p className="text-xs font-medium text-emerald-900">{learning.text}</p>
                  </div>
                ))}
              </div>
            </div>
          </Card>

          <Card className="p-6 border-indigo-100 bg-indigo-50/10">
            <div className="flex items-center space-x-2 mb-4">
              <TrendingUp className="h-5 w-5 text-indigo-500" />
              <h3 className="text-lg font-bold text-text-primary uppercase tracking-widest">Retrospective</h3>
            </div>
            <p className="text-xs text-text-secondary leading-relaxed mb-4 italic">
              "The mission followed the 'Fast Mode' reasoning profile. Efficiency was optimal, though a high-precision model would have reduced data-gathering latency by 12%."
            </p>
            <div className="space-y-4 pt-4 border-t border-indigo-100">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold text-text-muted uppercase">Confidence Avg.</span>
                <span className="text-sm font-bold text-indigo-600">94%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold text-text-muted uppercase">Manual Refinements</span>
                <span className="text-sm font-bold text-indigo-600">0</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export { MissionDebrief };
