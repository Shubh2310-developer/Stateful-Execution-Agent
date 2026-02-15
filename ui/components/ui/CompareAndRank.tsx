import * as React from 'react';
import { ThumbsUp, MessageSquare, CheckCircle2, ChevronRight, HelpCircle } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';
import { Card } from './Card';
import { Badge } from './Badge';

export interface RankableOption {
  id: string;
  title: string;
  content: React.ReactNode;
  metadata?: { label: string; value: string }[];
}

export interface CompareAndRankProps {
  title: string;
  description?: string;
  options: [RankableOption, RankableOption];
  onVote: (optionId: string, feedback?: string) => void;
  isLoading?: boolean;
  className?: string;
}

const CompareAndRank = ({
  title,
  description,
  options,
  onVote,
  isLoading = false,
  className
}: CompareAndRankProps) => {
  const [selectedId, setSelectedId] = React.useState<string | null>(null);
  const [feedback, setFeedback] = React.useState('');

  const handleVote = () => {
    if (selectedId) {
      onVote(selectedId, feedback);
    }
  };

  return (
    <div className={cn('flex flex-col space-y-6', className)}>
      <div className="flex flex-col space-y-1">
        <div className="flex items-center space-x-2">
          <div className="p-1.5 bg-brand-primary/10 rounded text-brand-primary">
            <HelpCircle size={16} />
          </div>
          <h3 className="text-lg font-bold text-text-primary tracking-tight">{title}</h3>
        </div>
        {description && <p className="text-sm text-text-secondary pl-8">{description}</p>}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {options.map((option) => {
          const isSelected = selectedId === option.id;
          return (
            <Card
              key={option.id}
              onClick={() => setSelectedId(option.id)}
              className={cn(
                'relative flex flex-col p-6 cursor-pointer transition-all duration-300 border-2 h-full',
                isSelected
                  ? 'border-brand-primary bg-brand-primary/[0.02] shadow-lg ring-4 ring-brand-primary/5'
                  : 'border-slate-200 bg-white hover:border-slate-300'
              )}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <div className={cn(
                    "flex h-6 w-6 items-center justify-center rounded-full text-[10px] font-bold",
                    isSelected ? "bg-brand-primary text-white" : "bg-slate-100 text-slate-500"
                  )}>
                    {option.id === options[0].id ? 'A' : 'B'}
                  </div>
                  <h4 className="font-bold text-text-primary">{option.title}</h4>
                </div>
                {isSelected && (
                  <Badge variant="brand" className="animate-in zoom-in-50">Selected Winner</Badge>
                )}
              </div>

              <div className="flex-1 bg-slate-50/50 rounded-ant-md p-4 mb-4 border border-slate-100 overflow-auto max-h-[300px]">
                {option.content}
              </div>

              {option.metadata && (
                <div className="flex flex-wrap gap-3 mt-auto pt-4 border-t border-slate-100">
                  {option.metadata.map((m, i) => (
                    <div key={i} className="flex flex-col">
                      <span className="text-[9px] font-bold text-text-muted uppercase tracking-widest">{m.label}</span>
                      <span className="text-xs font-bold text-text-secondary">{m.value}</span>
                    </div>
                  ))}
                </div>
              )}
            </Card>
          );
        })}
      </div>

      {selectedId && (
        <Card className="p-6 bg-slate-50 border-slate-200 animate-in slide-in-from-bottom-2 duration-500">
          <div className="flex flex-col space-y-4">
            <div className="flex items-center space-x-2">
              <MessageSquare size={16} className="text-brand-primary" />
              <span className="text-xs font-bold text-text-primary uppercase tracking-widest">Why is this version better? (Optional)</span>
            </div>
            <textarea
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              placeholder="Provide context for the agent to learn from this preference..."
              className="w-full p-3 bg-white border border-slate-200 rounded-ant-md text-sm focus:ring-brand-primary focus:border-brand-primary min-h-[80px] resize-none"
            />
            <div className="flex justify-end">
              <Button
                onClick={handleVote}
                disabled={isLoading}
                className="min-w-[160px]"
              >
                {isLoading ? 'Saving Feedback...' : 'Submit Choice'}
                <CheckCircle2 className="ml-2 h-4 w-4" />
              </Button>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};

export { CompareAndRank };
