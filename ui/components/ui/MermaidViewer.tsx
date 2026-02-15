"use client";

import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';
import { getTaskMermaid } from '../../lib/api';
import { Loader2, AlertCircle } from 'lucide-react';
import { cn } from '../../lib/utils';

interface MermaidViewerProps {
  taskId: string;
  className?: string;
}

/**
 * MermaidViewer renders a Mermaid diagram for a given taskId.
 * It applies 'Dark Minimalism' styling based on design tokens.
 */
export const MermaidViewer: React.FC<MermaidViewerProps> = ({ taskId, className }) => {
  const [chart, setChart] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Initialize Mermaid with Dark Minimalism configuration
  useEffect(() => {
    mermaid.initialize({
      startOnLoad: false,
      theme: 'base',
      themeVariables: {
        darkMode: true,
        background: '#0F172A', // color-bg-dark
        mainBkg: '#1E293B', // Slate-800 equivalent for nodes
        nodeBorder: '#3B82F6', // color-brand-primary
        clusterBkg: '#0F172A',
        clusterBorder: '#475569', // color-text-secondary
        lineColor: '#94A3B8', // color-text-muted
        fontFamily: '"Plus Jakarta Sans", "JetBrains Mono", sans-serif',
        fontSize: '12px',
        primaryColor: '#3B82F6',
        primaryTextColor: '#F8FAFC', // color-text-on-dark
        primaryBorderColor: '#3B82F6',
        labelTextColor: '#F8FAFC',
        secondaryColor: '#F97316', // color-brand-cta
        tertiaryColor: '#10B981', // color-status-success
      },
      flowchart: {
        htmlLabels: true,
        curve: 'basis',
      },
      securityLevel: 'loose',
    });
  }, []);

  useEffect(() => {
    const fetchAndRender = async () => {
      if (!taskId) return;

      setLoading(true);
      setError(null);
      try {
        const data = await getTaskMermaid(taskId);

        if (data && data.trim()) {
          setChart(data);

          // Use a timeout to ensure container is ready
          setTimeout(async () => {
            if (containerRef.current) {
              try {
                containerRef.current.innerHTML = '';
                const { svg } = await mermaid.render(`mermaid-${taskId.replace(/[^a-zA-Z0-9]/g, '-')}`, data);
                containerRef.current.innerHTML = svg;
              } catch (renderErr) {
                console.error('Mermaid render error:', renderErr);
                setError('Failed to render mission graph');
              }
            }
          }, 0);
        } else {
          setError('No diagram data available for this task');
        }
      } catch (err) {
        console.error('Fetch error:', err);
        setError('Failed to load mission plan visualization');
      } finally {
        setLoading(false);
      }
    };

    fetchAndRender();
  }, [taskId]);

  return (
    <div className={cn("rounded-ant-lg border border-slate-200 dark:border-slate-800 bg-background-surface overflow-hidden shadow-sm", className)}>
      <div className="flex items-center justify-between px-4 py-2 border-b border-slate-200 dark:border-slate-800 bg-background-muted/30">
        <span className="text-[10px] font-bold uppercase tracking-widest text-text-muted">Mission Architecture</span>
      </div>
      <div className="relative p-6 flex flex-col items-center justify-center min-h-[350px] bg-[#0F172A] transition-all duration-300">
        {loading && (
          <div className="flex flex-col items-center gap-3 animate-in fade-in">
            <Loader2 className="h-5 w-5 animate-spin text-brand-primary" />
            <span className="text-[10px] font-medium text-text-muted uppercase tracking-tight">Synthesizing Graph...</span>
          </div>
        )}

        {error && !loading && (
          <div className="flex flex-col items-center gap-3 text-status-error/80 animate-in zoom-in-95">
            <AlertCircle className="h-5 w-5" />
            <span className="text-[11px] font-medium">{error}</span>
          </div>
        )}

        <div
          ref={containerRef}
          className={cn(
            "w-full flex justify-center mermaid-container overflow-auto transition-opacity duration-500",
            (loading || error) ? "opacity-0 invisible h-0" : "opacity-100 visible"
          )}
        />
      </div>
    </div>
  );
};
