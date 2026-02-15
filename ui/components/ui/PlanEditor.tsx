import * as React from 'react';
import { GripVertical, Plus, Trash2, User, Bot, ChevronRight, ChevronDown } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';
import { Badge } from './Badge';

export interface PlanStep {
  id: string;
  label: string;
  type: 'autonomous' | 'manual';
  status: 'pending' | 'running' | 'completed' | 'failed';
  description?: string;
}

export interface PlanEditorProps {
  steps: PlanStep[];
  onUpdateSteps: (steps: PlanStep[]) => void;
  className?: string;
}

const PlanEditor = ({ steps, onUpdateSteps, className }: PlanEditorProps) => {
  const [editingId, setEditingId] = React.useState<string | null>(null);

  const toggleType = (id: string) => {
    onUpdateSteps(
      steps.map((step) =>
        step.id === id
          ? { ...step, type: step.type === 'autonomous' ? 'manual' : 'autonomous' }
          : step
      )
    );
  };

  const removeStep = (id: string) => {
    onUpdateSteps(steps.filter((step) => step.id !== id));
  };

  const addStep = () => {
    const newStep: PlanStep = {
      id: Math.random().toString(36).substr(2, 9),
      label: 'New step...',
      type: 'autonomous',
      status: 'pending',
      description: 'Describe the action...'
    };
    onUpdateSteps([...steps, newStep]);
    setEditingId(newStep.id);
  };

  return (
    <div className={cn('flex flex-col space-y-4', className)}>
      <div className="flex items-center justify-between px-2">
        <h3 className="text-sm font-bold text-text-primary uppercase tracking-wider">
          Execution Plan
        </h3>
        <Button size="sm" variant="ghost" onClick={addStep} className="h-8 text-brand-primary">
          <Plus className="h-4 w-4 mr-1" />
          Add Step
        </Button>
      </div>

      <div className="space-y-2">
        {steps.map((step, index) => (
          <div
            key={step.id}
            className={cn(
              'group relative flex items-start p-3 bg-white border border-slate-200 rounded-ant-lg transition-all duration-200',
              editingId === step.id ? 'ring-2 ring-brand-primary/20 border-brand-primary' : 'hover:border-slate-300'
            )}
          >
            <div className="mt-1 mr-3 cursor-grab text-text-muted hover:text-text-primary transition-colors">
              <GripVertical className="h-4 w-4" />
            </div>

            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2 mb-1">
                <span className="text-[10px] font-bold text-text-muted w-4">
                  {index + 1}.
                </span>
                {editingId === step.id ? (
                  <input
                    autoFocus
                    className="flex-1 text-sm font-bold text-text-primary bg-transparent border-none p-0 focus:ring-0"
                    value={step.label}
                    onChange={(e) => {
                      onUpdateSteps(steps.map(s => s.id === step.id ? { ...s, label: e.target.value } : s));
                    }}
                    onBlur={() => setEditingId(null)}
                    onKeyDown={(e) => e.key === 'Enter' && setEditingId(null)}
                  />
                ) : (
                  <span
                    className="text-sm font-bold text-text-primary truncate cursor-text"
                    onClick={() => setEditingId(step.id)}
                  >
                    {step.label}
                  </span>
                )}
              </div>

              <div className="flex items-center space-x-3 ml-6">
                <button
                  onClick={() => toggleType(step.id)}
                  className={cn(
                    "flex items-center space-x-1 px-1.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-tight transition-colors",
                    step.type === 'autonomous'
                      ? "text-brand-primary bg-brand-primary/5 border border-brand-primary/10"
                      : "text-amber-600 bg-amber-50 border border-amber-100"
                  )}
                >
                  {step.type === 'autonomous' ? <Bot className="h-3 w-3" /> : <User className="h-3 w-3" />}
                  <span>{step.type}</span>
                </button>
                <span className="text-[10px] text-text-muted font-mono">
                  {step.status}
                </span>
              </div>
            </div>

            <div className="flex items-center opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                onClick={() => removeStep(step.id)}
                className="p-1.5 text-text-muted hover:text-status-error transition-colors"
                aria-label="Remove step"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {steps.length === 0 && (
        <div className="py-12 text-center border-2 border-dashed border-slate-200 rounded-ant-lg bg-slate-50/50">
          <p className="text-sm text-text-muted">No steps defined. Add a step to begin the plan.</p>
        </div>
      )}
    </div>
  );
};

export { PlanEditor };
