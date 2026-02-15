import * as React from 'react';
import { Layers, History, Play, Save, AlertCircle, FileCode } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';
import { Badge } from './Badge';
import { CodeBlock } from './CodeBlock';

export interface PromptVersion {
  id: string;
  name: string;
  timestamp: string;
  isActive?: boolean;
}

export interface PromptEditorProps {
  content: string;
  onContentChange: (content: string) => void;
  versions: PromptVersion[];
  onSelectVersion: (id: string) => void;
  onTest: () => void;
  onSave: () => void;
  isLoading?: boolean;
  className?: string;
}

const PromptEditor = ({
  content,
  onContentChange,
  versions,
  onSelectVersion,
  onTest,
  onSave,
  isLoading = false,
  className
}: PromptEditorProps) => {
  return (
    <div className={cn('flex h-full rounded-ant-lg border border-slate-200 bg-white overflow-hidden shadow-xl', className)}>
      {/* Sidebar: Versions */}
      <aside className="w-64 border-r border-slate-200 flex flex-col bg-slate-50">
        <div className="p-4 border-b border-slate-200 bg-white">
          <h3 className="text-xs font-bold text-text-primary uppercase tracking-widest flex items-center">
            <History className="h-3.5 w-3.5 mr-2 text-text-muted" /> Version History
          </h3>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {versions.map((v) => (
            <button
              key={v.id}
              onClick={() => onSelectVersion(v.id)}
              className={cn(
                "w-full text-left p-2.5 rounded-ant-md transition-all text-xs",
                v.isActive
                  ? "bg-brand-primary text-white shadow-sm font-bold"
                  : "hover:bg-white text-text-secondary hover:text-text-primary"
              )}
            >
              <div className="flex items-center justify-between mb-0.5">
                <span className="truncate">{v.name}</span>
                {v.isActive && <Badge variant="secondary" className="bg-white/20 text-white text-[8px] h-4">Active</Badge>}
              </div>
              <span className={cn(
                "text-[9px] font-medium opacity-70",
                v.isActive ? "text-white" : "text-text-muted"
              )}>{v.timestamp}</span>
            </button>
          ))}
        </div>
        <div className="p-4 bg-white border-t border-slate-200">
          <div className="flex items-center space-x-2 text-[10px] text-text-muted">
            <AlertCircle className="h-3 w-3" />
            <span>Editing a core prompt affects all future tasks.</span>
          </div>
        </div>
      </aside>

      {/* Main Content: Editor Shell */}
      <main className="flex-1 flex flex-col min-w-0 bg-[#0F172A]">
        {/* Editor Toolbar */}
        <div className="h-12 border-b border-slate-800 flex items-center justify-between px-4">
          <div className="flex items-center space-x-3">
            <FileCode className="h-4 w-4 text-slate-400" />
            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">
              system_prompt.j2
            </span>
          </div>
          <div className="flex items-center space-x-3">
            <Button
              size="sm"
              variant="ghost"
              onClick={onTest}
              disabled={isLoading}
              className="text-slate-300 hover:text-white hover:bg-slate-800"
            >
              <Play className="h-3.5 w-3.5 mr-2" />
              Test Simulation
            </Button>
            <Button
              size="sm"
              onClick={onSave}
              disabled={isLoading}
              className="bg-brand-primary text-white"
            >
              <Save className="h-3.5 w-3.5 mr-2" />
              Save Draft
            </Button>
          </div>
        </div>

        {/* Editor Area (Textarea for now, would be Monaco in real app) */}
        <div className="flex-1 relative overflow-hidden group">
          <textarea
            value={content}
            onChange={(e) => onContentChange(e.target.value)}
            className="w-full h-full p-8 bg-transparent text-slate-300 font-mono text-sm leading-relaxed border-none focus:ring-0 resize-none selection:bg-brand-primary/30"
            spellCheck={false}
          />

          {/* Line Numbers Overlay (Visual only) */}
          <div className="absolute left-0 top-0 bottom-0 w-10 bg-slate-900/50 border-r border-slate-800/50 pointer-events-none flex flex-col items-center pt-8 text-[10px] text-slate-700 font-mono select-none">
            {Array.from({ length: 50 }).map((_, i) => (
              <span key={i} className="h-[21px] flex items-center">{i + 1}</span>
            ))}
          </div>
        </div>

        {/* Editor Footer / Info */}
        <div className="h-8 border-t border-slate-800 flex items-center justify-between px-4 text-[10px] text-slate-500 font-mono">
          <div className="flex items-center space-x-4">
            <span>UTF-8</span>
            <span>Jinja2 / Markdown</span>
          </div>
          <div className="flex items-center space-x-4">
            <span>{content.length} characters</span>
            <span>{content.split('\n').length} lines</span>
          </div>
        </div>
      </main>
    </div>
  );
};

export { PromptEditor };
