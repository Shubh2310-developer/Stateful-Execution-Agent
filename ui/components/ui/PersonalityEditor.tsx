import * as React from 'react';
import { User, Bot, Sparkles, Terminal, BookOpen, MessageSquare, Save, RotateCcw } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { Button } from './Button';
import { Slider } from './Slider';
import { Badge } from './Badge';
import { Avatar } from './Avatar';
import { SentimentSlider } from './SentimentSlider';

export type PersonaType = 'specialist' | 'analyst' | 'creative';

export interface PersonalitySettings {
  persona: PersonaType;
  verbosity: number;
  creativity: number;
  tone: number;
}

export interface PersonalityEditorProps {
  initialSettings?: PersonalitySettings;
  onSave?: (settings: PersonalitySettings) => void;
  className?: string;
}

const PersonalityEditor = ({
  initialSettings = {
    persona: 'analyst',
    verbosity: 50,
    creativity: 40,
    tone: 70
  },
  onSave,
  className
}: PersonalityEditorProps) => {
  const [settings, setSettings] = React.useState<PersonalitySettings>(initialSettings);

  const personas = [
    {
      id: 'specialist',
      label: 'The Specialist',
      description: 'Precise, technical, and minimal narrative.',
      icon: <Terminal size={20} />,
      color: 'indigo'
    },
    {
      id: 'analyst',
      label: 'The Analyst',
      description: 'Deep reasoning and comprehensive reports.',
      icon: <BookOpen size={20} />,
      color: 'blue'
    },
    {
      id: 'creative',
      label: 'The Creative',
      description: 'Narrative flow and high-impact visuals.',
      icon: <Sparkles size={20} />,
      color: 'amber'
    }
  ];

  const getPreviewText = () => {
    const { persona, verbosity } = settings;
    if (persona === 'specialist') {
      return "Goal identified. Analyzing 15 data points. System status: Nominal.";
    }
    if (persona === 'creative') {
      return "I've discovered some fascinating trends in your data! By weaving these insights together, we can build a compelling story for your Q4 update. Ready to dive in?";
    }
    return "I have completed the analysis. The core finding suggests a 12% improvement in operational efficiency. I've prepared three alternative paths for the next phase.";
  };

  return (
    <div className={cn('max-w-4xl mx-auto space-y-8', className)}>
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-text-primary tracking-tight">Agent Personality</h2>
          <p className="text-sm text-text-muted">Tune the character and communication style of your agent.</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="sm" onClick={() => setSettings(initialSettings)}>
            <RotateCcw className="h-4 w-4 mr-2" />
            Reset
          </Button>
          <Button size="sm" onClick={() => onSave?.(settings)}>
            <Save className="h-4 w-4 mr-2" />
            Save Changes
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {personas.map((p) => {
          const isActive = settings.persona === p.id;
          return (
            <button
              key={p.id}
              onClick={() => setSettings({ ...settings, persona: p.id as PersonaType })}
              className={cn(
                "flex flex-col text-left p-5 rounded-ant-lg border-2 transition-all duration-300 relative group",
                isActive
                  ? "border-brand-primary bg-brand-primary/[0.02] shadow-md ring-4 ring-brand-primary/5"
                  : "border-slate-200 bg-white hover:border-slate-300"
              )}
            >
              <div className={cn(
                "h-10 w-10 rounded-ant-md flex items-center justify-center mb-4 transition-colors",
                isActive ? "bg-brand-primary text-white" : "bg-slate-100 text-slate-500 group-hover:bg-slate-200"
              )}>
                {p.icon}
              </div>
              <h3 className="font-bold text-text-primary mb-1">{p.label}</h3>
              <p className="text-xs text-text-muted leading-relaxed">{p.description}</p>
              {isActive && (
                <div className="absolute top-3 right-3">
                  <div className="h-2 w-2 rounded-full bg-brand-primary animate-pulse" />
                </div>
              )}
            </button>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card className="p-6 space-y-8">
          <h3 className="text-sm font-bold text-text-primary uppercase tracking-widest border-b border-slate-100 pb-4">
            Voice & Tone Controls
          </h3>

          <div className="space-y-6">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold text-text-primary uppercase tracking-tight">Verbosity</label>
                <Badge variant="secondary" className="text-[10px] uppercase">
                  {settings.verbosity > 70 ? 'Comprehensive' : settings.verbosity < 30 ? 'Concise' : 'Balanced'}
                </Badge>
              </div>
              <Slider
                value={settings.verbosity}
                onChange={(val) => setSettings({ ...settings, verbosity: val })}
                min={0}
                max={100}
                showValue={false}
              />
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold text-text-primary uppercase tracking-tight">Creativity</label>
                <Badge variant="secondary" className="text-[10px] uppercase">
                  {settings.creativity > 70 ? 'Synthesis' : settings.creativity < 30 ? 'Logical' : 'Standard'}
                </Badge>
              </div>
              <Slider
                value={settings.creativity}
                onChange={(val) => setSettings({ ...settings, creativity: val })}
                min={0}
                max={100}
                showValue={false}
              />
            </div>

            <SentimentSlider
              label="Collaborative Tone"
              value={settings.tone}
              onChange={(val) => setSettings({ ...settings, tone: val })}
            />
          </div>
        </Card>

        <Card className="p-0 border-slate-200 overflow-hidden flex flex-col bg-slate-50/50">
          <div className="p-4 border-b border-slate-200 bg-white flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Avatar
                fallback="AG"
                isAgent
                size="sm"
                className={cn(
                  settings.persona === 'specialist' ? 'bg-indigo-500' :
                  settings.persona === 'creative' ? 'bg-amber-500' : 'bg-blue-500'
                )}
              />
              <div>
                <h4 className="text-xs font-bold text-text-primary uppercase tracking-widest leading-none">Antigravity</h4>
                <span className="text-[10px] text-text-muted font-bold uppercase tracking-tighter">Current Voice Preview</span>
              </div>
            </div>
            <MessageSquare size={16} className="text-text-muted" />
          </div>

          <div className="flex-1 p-8 flex items-center justify-center italic">
            <p className="text-sm text-text-secondary leading-relaxed text-center max-w-sm">
              "{getPreviewText()}"
            </p>
          </div>

          <div className="p-4 bg-white border-t border-slate-200 flex items-center justify-between">
            <div className="flex space-x-1">
              <div className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
              <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 opacity-40" />
              <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 opacity-20" />
            </div>
            <span className="text-[9px] font-bold text-text-muted uppercase tracking-widest">Calibration: Optimal</span>
          </div>
        </Card>
      </div>
    </div>
  );
};

export { PersonalityEditor };
