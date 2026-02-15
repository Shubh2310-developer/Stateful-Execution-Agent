import * as React from 'react';
import { Play, RotateCcw, Info, ArrowRight } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';

export interface ResumptionBannerProps {
  stepNumber: number;
  summary: string;
  onResume: () => void;
  onRestart?: () => void;
  className?: string;
}

const ResumptionBanner = ({
  stepNumber,
  summary,
  onResume,
  onRestart,
  className
}: ResumptionBannerProps) => {
  return (
    <div className={cn(
      'w-full bg-indigo-600 text-white rounded-ant-lg shadow-xl overflow-hidden transition-all duration-300 animate-in slide-in-from-top-4',
      className
    )}>
      <div className="px-6 py-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-start space-x-4">
          <div className="h-10 w-10 bg-white/20 rounded-full flex items-center justify-center shrink-0 backdrop-blur-sm">
            <Info className="h-6 w-6" />
          </div>
          <div className="flex flex-col">
            <div className="flex items-center space-x-2">
              <span className="text-[10px] font-bold uppercase tracking-widest text-indigo-200">
                Resumption Context
              </span>
              <span className="h-1 w-1 rounded-full bg-indigo-300" />
              <span className="text-[10px] font-bold uppercase tracking-widest text-indigo-200">
                Paused at Step {stepNumber}
              </span>
            </div>
            <p className="text-sm font-medium leading-relaxed mt-1 max-w-2xl">
              {summary}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          {onRestart && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onRestart}
              className="text-white hover:bg-white/10"
            >
              <RotateCcw className="h-4 w-4 mr-2" />
              Restart Task
            </Button>
          )}
          <Button
            size="md"
            onClick={onResume}
            className="bg-white text-indigo-600 hover:bg-indigo-50 font-bold shadow-lg shadow-indigo-900/20"
          >
            <Play className="h-4 w-4 mr-2 fill-current" />
            Resume Execution
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </div>
      </div>
      {/* Visual background element */}
      <div className="absolute right-0 top-0 bottom-0 w-1/4 bg-gradient-to-l from-white/5 to-transparent pointer-events-none" />
    </div>
  );
};

export { ResumptionBanner };
