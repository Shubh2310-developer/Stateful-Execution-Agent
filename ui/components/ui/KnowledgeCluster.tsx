import * as React from 'react';
import { cn } from '../../lib/utils';
import { MemoryCard, MemoryCardProps } from './MemoryCard';
import { Folder } from 'lucide-react';

export interface KnowledgeClusterProps {
  title: string;
  description?: string;
  memories: MemoryCardProps[];
  className?: string;
}

const KnowledgeCluster = ({
  title,
  description,
  memories,
  className
}: KnowledgeClusterProps) => {
  return (
    <div className={cn('flex flex-col space-y-4', className)}>
      <div className="flex items-center space-x-3 px-1">
        <div className="h-8 w-8 rounded-ant-md bg-brand-primary/10 flex items-center justify-center text-brand-primary">
          <Folder className="h-4 w-4" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-text-primary uppercase tracking-widest">{title}</h3>
          {description && <p className="text-[10px] text-text-muted font-medium">{description}</p>}
        </div>
        <div className="ml-auto">
          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-500">
            {memories.length} Entries
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {memories.map((memory, i) => (
          <MemoryCard key={i} {...memory} className="bg-white/50 hover:bg-white" />
        ))}
      </div>
    </div>
  );
};

export { KnowledgeCluster };
