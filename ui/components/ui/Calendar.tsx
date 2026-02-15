import * as React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';

export interface CalendarEvent {
  id: string;
  date: Date;
  title: string;
  type?: 'success' | 'running' | 'pending' | 'failed';
}

export interface CalendarProps {
  events: CalendarEvent[];
  onDateClick?: (date: Date) => void;
  className?: string;
}

const Calendar = ({ events, onDateClick, className }: CalendarProps) => {
  const [currentDate, setCurrentDate] = React.useState(new Date());

  const daysInMonth = (year: number, month: number) => new Date(year, month + 1, 0).getDate();
  const firstDayOfMonth = (year: number, month: number) => new Date(year, month, 1).getDay();

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const days = daysInMonth(year, month);
  const startDay = firstDayOfMonth(year, month);

  const prevMonth = () => setCurrentDate(new Date(year, month - 1, 1));
  const nextMonth = () => setCurrentDate(new Date(year, month + 1, 1));

  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

  const getEventsForDay = (day: number) => {
    return events.filter(e =>
      e.date.getDate() === day &&
      e.date.getMonth() === month &&
      e.date.getFullYear() === year
    );
  };

  return (
    <div className={cn('bg-white rounded-ant-lg border border-slate-200 overflow-hidden shadow-sm', className)}>
      <div className="flex items-center justify-between p-4 border-b border-slate-100">
        <h3 className="text-sm font-bold text-text-primary uppercase tracking-widest">
          {monthNames[month]} {year}
        </h3>
        <div className="flex items-center space-x-1">
          <Button variant="ghost" size="sm" onClick={prevMonth} className="h-8 w-8 p-0">
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" onClick={nextMonth} className="h-8 w-8 p-0">
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-7 border-b border-slate-100">
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
          <div key={day} className="py-2 text-center text-[10px] font-bold text-text-muted uppercase tracking-tighter">
            {day}
          </div>
        ))}
      </div>

      <div className="grid grid-cols-7 gap-px bg-slate-100">
        {/* Empty days before start */}
        {Array.from({ length: startDay }).map((_, i) => (
          <div key={`empty-${i}`} className="bg-slate-50/50 h-24 md:h-32 p-2" />
        ))}

        {/* Calendar days */}
        {Array.from({ length: days }).map((_, i) => {
          const day = i + 1;
          const dayEvents = getEventsForDay(day);
          const isToday = day === new Date().getDate() && month === new Date().getMonth() && year === new Date().getFullYear();

          return (
            <div
              key={day}
              onClick={() => onDateClick?.(new Date(year, month, day))}
              className={cn(
                "bg-white h-24 md:h-32 p-2 transition-colors hover:bg-slate-50 cursor-pointer overflow-hidden",
                isToday && "ring-1 ring-inset ring-brand-primary bg-brand-primary/[0.02]"
              )}
            >
              <div className="flex justify-between items-start">
                <span className={cn(
                  "text-xs font-bold",
                  isToday ? "text-brand-primary" : "text-text-secondary"
                )}>
                  {day}
                </span>
                {dayEvents.length > 0 && (
                  <span className="text-[10px] font-bold text-text-muted">
                    {dayEvents.length}
                  </span>
                )}
              </div>

              <div className="mt-2 space-y-1">
                {dayEvents.slice(0, 3).map((event) => (
                  <div
                    key={event.id}
                    className={cn(
                      "text-[9px] font-bold px-1.5 py-0.5 rounded border truncate",
                      event.type === 'success' ? "bg-emerald-50 text-emerald-700 border-emerald-100" :
                      event.type === 'running' ? "bg-blue-50 text-blue-700 border-blue-100" :
                      event.type === 'failed' ? "bg-red-50 text-red-700 border-red-100" :
                      "bg-slate-50 text-slate-700 border-slate-200"
                    )}
                  >
                    {event.title}
                  </div>
                ))}
                {dayEvents.length > 3 && (
                  <div className="text-[8px] text-text-muted font-bold text-center">
                    +{dayEvents.length - 3} more
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {/* Empty days after end to fill grid */}
        {Array.from({ length: (7 - (startDay + days) % 7) % 7 }).map((_, i) => (
          <div key={`empty-end-${i}`} className="bg-slate-50/50 h-24 md:h-32 p-2" />
        ))}
      </div>
    </div>
  );
};

export { Calendar };
