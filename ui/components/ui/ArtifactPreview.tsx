import * as React from 'react';
import { FileText, FileJson, FileCode, Download, ExternalLink, MoreVertical } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export type ArtifactType = 'pdf' | 'markdown' | 'json' | 'code' | 'generic';

export interface ArtifactPreviewProps {
  name: string;
  type: ArtifactType;
  size?: string;
  onOpen?: () => void;
  onDownload?: () => void;
  className?: string;
  isLoading?: boolean;
}

const ArtifactPreview = ({
  name,
  type,
  size,
  onOpen,
  onDownload,
  className,
  isLoading = false
}: ArtifactPreviewProps) => {
  const getIcon = () => {
    switch (type) {
      case 'pdf': return <FileText className="h-5 w-5 text-red-500" />;
      case 'markdown': return <FileText className="h-5 w-5 text-blue-500" />;
      case 'json': return <FileJson className="h-5 w-5 text-amber-500" />;
      case 'code': return <FileCode className="h-5 w-5 text-emerald-500" />;
      default: return <FileText className="h-5 w-5 text-slate-500" />;
    }
  };

  if (isLoading) {
    return (
      <div className={cn(
        'flex items-center justify-between p-3 bg-white border border-slate-200 rounded-lg animate-pulse',
        className
      )}>
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 bg-slate-100 rounded" />
          <div className="space-y-2">
            <div className="h-3 w-32 bg-slate-100 rounded" />
            <div className="h-2 w-16 bg-slate-100 rounded" />
          </div>
        </div>
        <div className="h-8 w-8 bg-slate-50 rounded-full" />
      </div>
    );
  }

  return (
    <div className={cn(
      'group flex items-center justify-between p-3 bg-white border border-slate-200 rounded-ant-lg shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-brand-primary/40 hover:shadow-md animate-in zoom-in-95 fade-in duration-300',
      className
    )}>
      <div className="flex items-center space-x-3 min-w-0">
        <div className="flex-shrink-0 h-10 w-10 flex items-center justify-center bg-slate-50 rounded-ant-md border border-slate-100 group-hover:bg-brand-primary/5 transition-colors">
          {getIcon()}
        </div>
        <div className="min-w-0">
          <h5 className="text-sm font-bold text-text-primary truncate" title={name}>
            {name}
          </h5>
          {size && (
            <span className="text-[10px] font-medium text-text-muted uppercase tracking-tight">{size}</span>
          )}
        </div>
      </div>

      <div className="flex items-center space-x-1">
        {onOpen && (
          <Tooltip content="Open Artifact">
            <button
              onClick={onOpen}
              className="p-1.5 text-text-muted hover:text-brand-primary hover:bg-brand-primary/5 rounded-ant-sm transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary"
              aria-label="Open artifact"
            >
              <ExternalLink className="h-4 w-4" />
            </button>
          </Tooltip>
        )}
        {onDownload && (
          <Tooltip content="Download Artifact">
            <button
              onClick={onDownload}
              className="p-1.5 text-text-muted hover:text-brand-primary hover:bg-brand-primary/5 rounded-ant-sm transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary"
              aria-label="Download artifact"
            >
              <Download className="h-4 w-4" />
            </button>
          </Tooltip>
        )}
        <Tooltip content="More Options">
          <button
            className="p-1.5 text-text-muted hover:text-text-primary rounded-ant-sm transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary"
            aria-label="More options"
          >
            <MoreVertical className="h-4 w-4" />
          </button>
        </Tooltip>
      </div>
    </div>
  );
};

export { ArtifactPreview };
