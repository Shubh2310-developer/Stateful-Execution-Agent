import * as React from 'react';
import { cn } from '../../lib/utils';

export interface AppLayoutProps {
  sidebar: React.ReactNode;
  header: React.ReactNode;
  children: React.ReactNode;
  rightPanel?: React.ReactNode;
  showRightPanel?: boolean;
}

const AppLayout = ({
  sidebar,
  header,
  children,
  rightPanel,
  showRightPanel = false
}: AppLayoutProps) => {
  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      {/* Sidebar */}
      <aside className="z-30 hidden h-full flex-shrink-0 border-r border-slate-200 bg-background-surface md:block">
        {sidebar}
      </aside>

      {/* Main Content Area */}
      <div className="relative flex flex-1 flex-col overflow-hidden">
        {/* Header */}
        <header className="z-20 h-header shrink-0 border-b border-slate-200 bg-background-surface/80 backdrop-blur-md">
          {header}
        </header>

        {/* Workspace */}
        <main className="relative flex flex-1 overflow-hidden">
          {/* Center Content */}
          <div className="relative flex flex-1 flex-col overflow-y-auto overflow-x-hidden p-6 scrollbar-hide">
            {children}
          </div>

          {/* Right Panel (Trace Panel) */}
          {rightPanel && (
            <aside
              className={cn(
                'z-10 h-full border-l border-slate-200 bg-background-surface transition-all duration-300 ease-quart-out',
                showRightPanel ? 'w-trace translate-x-0' : 'w-0 translate-x-full overflow-hidden'
              )}
            >
              <div className="w-trace h-full">
                {rightPanel}
              </div>
            </aside>
          )}
        </main>
      </div>
    </div>
  );
};

export { AppLayout };
