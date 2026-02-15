import * as React from 'react';
import { LucideIcon, TrendingUp, TrendingDown } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';

export interface StatCardProps {
  title: string;
  value: string | number;
  icon?: LucideIcon;
  description?: string;
  trend?: {
    value: number;
    isPositive: boolean;
    label?: string;
  };
  isLoading?: boolean;
  className?: string;
}

const StatCard = ({
  title,
  value,
  icon: Icon,
  description,
  trend,
  isLoading = false,
  className
}: StatCardProps) => {
  return (
    <Card className={cn('p-5 flex flex-col justify-between h-full', className)}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-bold text-text-muted uppercase tracking-wider mb-1">
            {title}
          </p>
          {isLoading ? (
            <div className="h-8 w-24 bg-slate-100 animate-pulse rounded mt-1" />
          ) : (
            <h4 className="text-2xl font-bold text-text-primary tracking-tight">
              {value}
            </h4>
          )}
        </div>
        {Icon && (
          <div className="p-2 bg-brand-primary/5 rounded-ant-md text-brand-primary">
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>

      <div className="mt-4">
        {trend && !isLoading && (
          <div className="flex items-center space-x-2">
            <div className={cn(
              "flex items-center text-xs font-bold px-1.5 py-0.5 rounded",
              trend.isPositive ? "text-status-success bg-status-success/10" : "text-status-error bg-status-error/10"
            )}>
              {trend.isPositive ? <TrendingUp className="h-3 w-3 mr-1" /> : <TrendingDown className="h-3 w-3 mr-1" />}
              {trend.value}%
            </div>
            {trend.label && (
              <span className="text-xs text-text-muted">{trend.label}</span>
            )}
          </div>
        )}
        {description && !trend && (
          <p className="text-xs text-text-muted">{description}</p>
        )}
        {isLoading && <div className="h-3 w-32 bg-slate-50 animate-pulse rounded mt-2" />}
      </div>
    </Card>
  );
};

export { StatCard };
