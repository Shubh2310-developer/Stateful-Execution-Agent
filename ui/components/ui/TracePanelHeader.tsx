import * as React from 'react';
import { Search, Filter, Download, MoreVertical, Terminal, FileJson, Info } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';
import { Tabs } from './Tabs';

export interface TracePanelHeaderProps {
  title?: string;
  onFilter?: (filter: string) => void;
  onDownload?: () => void;
  className?: string;
}

const TracePanelHeader = ({
  title = "Decision Trace",
  onFilter,
  onDownload,
  className
}: TracePanelHeaderProps) => {
  const [activeTab, setActiveTab] = React.useState('all');

  const tabs = [
    { id: 'all', label: 'All' },
    { id: 'thoughts', label: 'Thoughts', icon: <Terminal className="h-3.5 w-3.5" /> },
    { id: 'tools', label: 'Tools', icon: <Terminal className="h-3.5 w-3.5" /> },
    { id: 'errors', label: 'Errors', icon: <Info className="h-3.5 w-3.5" /> },
  ];

  return (
    <div className={cn('flex flex-col border-b border-slate-200 bg-background-surface', className)}>
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center space-x-2">
          <Terminal className="h-4 w-4 text-brand-primary" />
          <h2 className="text-sm font-bold text-text-primary uppercase tracking-wider">
            {title}
          </h2>
        </div>
        <div className="flex items-center space-x-1">
          <Button variant="ghost" size="sm" onClick={onDownload} className="h-8 w-8 p-0">
            <Download className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
            <MoreVertical className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="px-4 pb-2">
        <div className="relative mb-3">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-text-muted" />
          <input
            type="text"
            placeholder="Search trace..."
            className="w-full rounded-ant-md border border-slate-200 bg-slate-50 py-1.5 pl-8 pr-3 text-xs focus:border-brand-primary focus:bg-white focus:outline-none focus:ring-1 focus:ring-brand-primary/20"
          />
        </div>

        <Tabs
          tabs={tabs}
          activeTab={activeTab}
          onChange={(id) => {
            setActiveTab(id);
            onFilter?.(id);
          }}
          variant="pills"
          className="w-full bg-slate-50/50"
        />
      </div>
    </div>
  );
};

export { TracePanelHeader };
