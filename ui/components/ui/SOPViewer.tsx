import * as React from 'react';
import { Book, CheckCircle2, User, Bot, AlertTriangle, ChevronRight, FileText } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { Badge } from './Badge';
import { StepIndicator, Step } from './StepIndicator';

export interface SOPStep extends Step {
  owner: 'agent' | 'human';
  isCritical?: boolean;
}

export interface SOPViewerProps {
  id: string;
  title: string;
  description: string;
  version: string;
  steps: SOPStep[];
  onStartMission?: () => void;
  className?: string;
}

const SOPViewer = ({
  id,
  title,
  description,
  version,
  steps,
  onStartMission,
  className
}: SOPViewerProps) => {
  return (
    <div className={cn('flex flex-col space-y-6', className)}>
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <Book className="h-5 w-5 text-indigo-500" />
            <h2 className="text-xl font-bold text-text-primary tracking-tight">{title}</h2>
          </div>
          <p className="text-sm text-text-secondary max-w-2xl leading-relaxed">
            {description}
          </p>
        </div>
        <div className="flex flex-col items-end space-y-2">
          <Badge variant="outline" className="font-mono text-[10px]">ID: {id} / v{version}</Badge>
          <Badge className="bg-emerald-50 text-emerald-700 border-emerald-100 uppercase text-[8px] font-bold">Verified Procedure</Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <Card className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-sm font-bold text-text-primary uppercase tracking-widest">Procedure Steps</h3>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-1.5">
                  <Bot size={12} className="text-brand-primary" />
                  <span className="text-[10px] font-bold text-text-muted uppercase">Agent</span>
                </div>
                <div className="flex items-center space-x-1.5">
                  <User size={12} className="text-amber-500" />
                  <span className="text-[10px] font-bold text-text-muted uppercase">Human</span>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              {steps.map((step, index) => (
                <div key={step.id} className="flex items-start space-x-4 p-4 rounded-ant-lg bg-slate-50 border border-slate-100 group hover:border-indigo-200 transition-all">
                  <div className="flex h-6 w-6 items-center justify-center rounded-full bg-white border border-slate-200 text-xs font-bold text-text-secondary shrink-0">
                    {index + 1}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="text-sm font-bold text-text-primary">{step.label}</h4>
                      <div className="flex items-center space-x-2">
                        {step.isCritical && (
                          <Badge variant="destructive" className="h-4 py-0 text-[8px] uppercase">Critical</Badge>
                        )}
                        {step.owner === 'agent' ? (
                          <Bot size={14} className="text-brand-primary" />
                        ) : (
                          <User size={14} className="text-amber-500" />
                        )}
                      </div>
                    </div>
                    <p className="text-xs text-text-secondary leading-relaxed">{step.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        <div className="space-y-6">
          <Card className="p-6 bg-indigo-600 text-white border-none shadow-xl shadow-indigo-900/20">
            <h3 className="text-xs font-bold uppercase tracking-[0.2em] text-indigo-200 mb-4">Automation Potential</h3>
            <div className="flex items-end justify-between mb-6">
              <span className="text-4xl font-bold">
                {Math.round((steps.filter(s => s.owner === 'agent').length / steps.length) * 100)}%
              </span>
              <span className="text-xs text-indigo-200 font-medium mb-1">Agent-led steps</span>
            </div>
            <p className="text-sm text-indigo-100 leading-relaxed mb-6">
              This SOP is optimized for autonomous execution. The agent can handle data gathering and initial synthesis.
            </p>
            <Button
              onClick={onStartMission}
              className="w-full bg-white text-indigo-600 hover:bg-indigo-50 font-bold h-12 shadow-lg"
            >
              Launch Mission from SOP
              <ChevronRight size={18} className="ml-2" />
            </Button>
          </Card>

          <Card className="p-6">
            <h3 className="text-xs font-bold text-text-muted uppercase tracking-widest mb-4">Required Capabilities</h3>
            <div className="flex flex-wrap gap-2">
              <Badge variant="secondary">Web Search</Badge>
              <Badge variant="secondary">PDF Extraction</Badge>
              <Badge variant="secondary">Slack API</Badge>
              <Badge variant="secondary">JSON Mapping</Badge>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export { SOPViewer };
