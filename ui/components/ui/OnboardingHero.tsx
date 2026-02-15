import * as React from 'react';
import { Rocket, ShieldCheck, Sparkles, ArrowRight, Play } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';
import { Stepper } from './Stepper';

export interface OnboardingHeroProps {
  userName?: string;
  onStart: () => void;
  setupProgress: number; // 0-100
  className?: string;
}

const OnboardingHero = ({
  userName = "Operator",
  onStart,
  setupProgress,
  className
}: OnboardingHeroProps) => {
  return (
    <div className={cn(
      'relative flex flex-col items-center text-center max-w-4xl mx-auto py-12 px-6 bg-white border border-slate-200 rounded-ant-xl shadow-2xl overflow-hidden',
      className
    )}>
      {/* Background Animated Elements */}
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-brand-primary via-emerald-500 to-brand-cta animate-pulse" />
      <div className="absolute -top-24 -right-24 h-64 w-64 bg-brand-primary/5 rounded-full blur-3xl" />
      <div className="absolute -bottom-24 -left-24 h-64 w-64 bg-emerald-500/5 rounded-full blur-3xl" />

      <div className="z-10 w-full">
        <div className="mb-8 flex justify-center">
          <div className="relative">
            <div className="absolute inset-0 bg-brand-primary/20 rounded-full blur-xl animate-pulse" />
            <div className="relative h-20 w-20 bg-slate-900 rounded-ant-lg flex items-center justify-center shadow-2xl border border-slate-800 rotate-3 transition-transform hover:rotate-0 duration-500">
              <span className="text-4xl font-black text-white italic">A</span>
            </div>
          </div>
        </div>

        <h1 className="text-4xl md:text-5xl font-black text-text-primary tracking-tighter mb-4">
          Hello, {userName}.
        </h1>
        <p className="text-lg md:text-xl text-text-secondary font-medium mb-12 max-w-2xl mx-auto leading-relaxed">
          Your persistent knowledge worker is ready to execute. Let's configure your autonomy profile and launch your first mission.
        </p>

        <div className="max-w-md mx-auto mb-12 space-y-4">
          <div className="flex items-center justify-between text-[10px] font-bold text-text-muted uppercase tracking-widest px-1">
            <span>Operational Readiness</span>
            <span>{setupProgress}%</span>
          </div>
          <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden border border-slate-200 shadow-inner">
            <div
              className="h-full bg-brand-primary shadow-[0_0_10px_rgba(59,130,246,0.5)] transition-all duration-1000 ease-out-ant"
              style={{ width: `${setupProgress}%` }}
            />
          </div>
          <p className="text-xs text-text-muted italic">
            Complete the interactive walkthrough to unlock multi-agent swarms.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Button
            size="lg"
            onClick={onStart}
            className="h-14 px-8 text-base font-bold shadow-xl shadow-brand-primary/25 group"
          >
            Start Introduction Mission
            <Rocket className="ml-3 h-5 w-5 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
          </Button>
          <Button
            variant="secondary"
            size="lg"
            className="h-14 px-8 text-base font-bold"
          >
            <ShieldCheck className="mr-3 h-5 w-5 text-emerald-500" />
            Security & Privacy Overview
          </Button>
        </div>

        <div className="mt-16 flex items-center justify-center space-x-8 opacity-50">
          <div className="flex items-center space-x-2 grayscale">
            <div className="h-2 w-2 rounded-full bg-emerald-500" />
            <span className="text-[10px] font-bold uppercase tracking-widest text-text-muted">SOC2 Certified</span>
          </div>
          <div className="flex items-center space-x-2 grayscale">
            <div className="h-2 w-2 rounded-full bg-blue-500" />
            <span className="text-[10px] font-bold uppercase tracking-widest text-text-muted">Agent Isolation active</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export { OnboardingHero };
