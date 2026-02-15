import * as React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FileText,
  Code2,
  FileDigit,
  Download,
  Copy,
  Maximize2,
  Minimize2,
  History,
  Check,
  ChevronDown,
  ExternalLink,
  Share2
} from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';
import { CodeBlock } from './CodeBlock';
import { Tabs } from './Tabs';
import { DropdownMenu } from './DropdownMenu';
import { Tooltip } from './Tooltip';

export type ArtifactType = 'text' | 'code' | 'pdf' | 'json' | 'csv' | 'image';

export interface ArtifactVersion {
  id: string;
  version: number;
  timestamp: string;
  summary: string;
}

export interface ArtifactViewerProps {
  id: string;
  type: ArtifactType;
  title: string;
  content: string;
  language?: string;
  versions?: ArtifactVersion[];
  currentVersion?: number;
  onVersionSelect?: (versionId: string) => void;
  onExport?: (format: string) => void;
  className?: string;
}

const ArtifactViewer = ({
  id,
  type,
  title,
  content,
  language,
  versions = [],
  currentVersion,
  onVersionSelect,
  onExport,
  className
}: ArtifactViewerProps) => {
  const [isFullscreen, setIsFullscreen] = React.useState(false);
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getTypeIcon = () => {
    switch (type) {
      case 'code': return <Code2 className="h-4 w-4" />;
      case 'pdf': return <FileText className="h-4 w-4" />;
      case 'json':
      case 'csv': return <FileDigit className="h-4 w-4" />;
      default: return <FileText className="h-4 w-4" />;
    }
  };

  const renderContent = () => {
    switch (type) {
      case 'code':
      case 'json':
      case 'csv':
        return (
          <CodeBlock
            code={content}
            language={language || type}
            className="border-0 rounded-none h-full shadow-none"
            showLineNumbers
          />
        );
      case 'pdf':
        return (
          <div className="flex flex-col items-center justify-center h-full bg-slate-100 dark:bg-slate-900 text-slate-500">
            <div className="p-8 border-2 border-dashed border-slate-300 dark:border-slate-800 rounded-xl flex flex-col items-center">
              <FileText className="h-12 w-12 mb-4 opacity-20" />
              <p className="text-sm font-medium mb-4">PDF Preview not available in this view</p>
              <Button variant="secondary" size="sm" onClick={() => window.open(content, '_blank')}>
                <ExternalLink className="h-4 w-4 mr-2" />
                Open in New Tab
              </Button>
            </div>
          </div>
        );
      case 'image':
        return (
          <div className="flex items-center justify-center h-full bg-slate-100 dark:bg-slate-950 overflow-auto p-4">
            <img src={content} alt={title} className="max-w-full h-auto shadow-2xl rounded-lg" />
          </div>
        );
      default:
        return (
          <div className="p-6 prose dark:prose-invert max-w-none font-sans text-slate-300">
            {content.split('\n').map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>
        );
    }
  };

  return (
    <div className={cn(
      "flex flex-col bg-slate-900 border border-slate-800 rounded-ant-xl overflow-hidden transition-all duration-300",
      isFullscreen ? "fixed inset-0 z-50 rounded-none" : "h-full min-h-[400px]",
      className
    )}>
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-slate-900 border-b border-slate-800 shrink-0">
        <div className="flex items-center space-x-3 overflow-hidden">
          <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 shrink-0">
            {getTypeIcon()}
          </div>
          <div className="flex flex-col min-w-0">
            <h3 className="text-sm font-semibold text-slate-100 truncate">{title}</h3>
            <span className="text-[10px] text-slate-500 uppercase tracking-tighter font-mono">
              ID: {id} • TYPE: {type}
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-2 shrink-0">
          {/* Version Selector */}
          {versions.length > 0 && (
            <DropdownMenu
              trigger={
                <Button variant="ghost" size="sm" className="h-8 text-xs text-slate-400 hover:text-white hover:bg-slate-800">
                  <History className="h-3.5 w-3.5 mr-1.5" />
                  v{currentVersion || versions[0].version}
                  <ChevronDown className="h-3 w-3 ml-1.5" />
                </Button>
              }
              items={versions.map((v) => ({
                id: v.id,
                label: `Version ${v.version}`,
                onClick: () => onVersionSelect?.(v.id)
              }))}
              align="right"
            />
          )}

          <div className="w-px h-4 bg-slate-800 mx-1" />

          <Tooltip content="Copy Content">
            <Button
              variant="ghost"
              size="sm"
              className="h-8 w-8 text-slate-400 hover:text-white"
              onClick={handleCopy}
            >
              {copied ? <Check className="h-4 w-4 text-emerald-400" /> : <Copy className="h-4 w-4" />}
            </Button>
          </Tooltip>

          <Tooltip content="Export">
            <DropdownMenu
              trigger={
                <Button variant="ghost" size="sm" className="h-8 w-8 text-slate-400 hover:text-white">
                  <Download className="h-4 w-4" />
                </Button>
              }
              items={[
                { id: 'raw', label: 'Download Raw File', onClick: () => onExport?.('raw') },
                { id: 'pdf', label: 'Export as PDF', onClick: () => onExport?.('pdf') },
                { id: 'markdown', label: 'Export as Markdown', onClick: () => onExport?.('markdown') }
              ]}
              align="right"
            />
          </Tooltip>

          <Tooltip content={isFullscreen ? "Exit Fullscreen" : "Fullscreen"}>
            <Button
              variant="ghost"
              size="sm"
              className="h-8 w-8 text-slate-400 hover:text-white"
              onClick={() => setIsFullscreen(!isFullscreen)}
            >
              {isFullscreen ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
            </Button>
          </Tooltip>
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-auto relative bg-slate-900">
        <AnimatePresence mode="wait">
          <motion.div
            key={`${id}-${currentVersion}`}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            className="h-full"
          >
            {renderContent()}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Footer Info */}
      <div className="px-4 py-2 bg-slate-950 border-t border-slate-800 flex items-center justify-between shrink-0">
        <div className="flex items-center space-x-4 text-[10px] text-slate-500 font-mono">
          <span>{content.length.toLocaleString()} bytes</span>
          {type === 'code' && <span>{content.split('\n').length} lines</span>}
        </div>
        <div className="flex items-center space-x-1 text-[10px] text-slate-500">
          <Share2 className="h-3 w-3" />
          <span>Artifact is shared with 2 collaborators</span>
        </div>
      </div>
    </div>
  );
};

export { ArtifactViewer };
