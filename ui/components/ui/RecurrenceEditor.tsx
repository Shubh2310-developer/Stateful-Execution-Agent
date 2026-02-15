import * as React from 'react';
import { Calendar as CalendarIcon, Clock, RefreshCw } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Select } from './Select';
import { Input } from './Input';

export type RecurrenceFrequency = 'daily' | 'weekly' | 'monthly' | 'custom';

export interface RecurrenceEditorProps {
  frequency: RecurrenceFrequency;
  onFrequencyChange: (freq: RecurrenceFrequency) => void;
  time: string;
  onTimeChange: (time: string) => void;
  interval?: number;
  onIntervalChange?: (val: number) => void;
  className?: string;
}

const RecurrenceEditor = ({
  frequency,
  onFrequencyChange,
  time,
  onTimeChange,
  interval = 1,
  onIntervalChange,
  className
}: RecurrenceEditorProps) => {
  const frequencyOptions = [
    { value: 'daily', label: 'Daily' },
    { value: 'weekly', label: 'Weekly' },
    { value: 'monthly', label: 'Monthly' },
    { value: 'custom', label: 'Custom (Cron)' },
  ];

  return (
    <div className={cn('flex flex-col space-y-6 p-4 bg-slate-50 border border-slate-200 rounded-ant-lg', className)}>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Select
          label="Frequency"
          options={frequencyOptions}
          value={frequency}
          onChange={(v) => onFrequencyChange(v as RecurrenceFrequency)}
        />

        {frequency !== 'custom' && (
          <Input
            label="Execution Time"
            type="time"
            value={time}
            onChange={(e) => onTimeChange(e.target.value)}
          />
        )}

        {frequency === 'custom' && (
          <Input
            label="Cron Expression"
            placeholder="0 0 * * *"
            value={time}
            onChange={(e) => onTimeChange(e.target.value)}
          />
        )}
      </div>

      {frequency !== 'custom' && onIntervalChange && (
        <div className="flex items-center space-x-4">
          <div className="flex-1">
            <Input
              label={`Every ${frequency === 'daily' ? 'day(s)' : frequency === 'weekly' ? 'week(s)' : 'month(s)'}`}
              type="number"
              min={1}
              value={interval}
              onChange={(e) => onIntervalChange(Number(e.target.value))}
            />
          </div>
          <div className="flex-1 pt-6">
            <div className="text-[10px] text-text-muted italic flex items-start">
              <RefreshCw className="h-3 w-3 mr-1.5 mt-0.5" />
              <span>The agent will automatically initiate this mission according to the selected schedule.</span>
            </div>
          </div>
        </div>
      )}

      {frequency === 'weekly' && (
        <div className="space-y-2">
          <label className="text-xs font-bold text-text-primary uppercase tracking-widest">Repeat on</label>
          <div className="flex flex-wrap gap-2">
            {['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((day, i) => (
              <button
                key={i}
                className="h-8 w-8 rounded-full border border-slate-200 bg-white text-xs font-bold text-text-secondary hover:border-brand-primary hover:text-brand-primary transition-all"
              >
                {day}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export { RecurrenceEditor };
