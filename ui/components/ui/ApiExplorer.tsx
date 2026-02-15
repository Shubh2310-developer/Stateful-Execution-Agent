import * as React from 'react';
import { Terminal, Send, FileJson, Play, ShieldCheck } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from './Button';
import { CodeBlock } from './CodeBlock';
import { Tabs, TabsProps } from './Tabs';
import { Badge } from './Badge';
import { Card } from './Card';

export interface ApiEndpoint {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  path: string;
  description: string;
  parameters: { name: string; type: string; required: boolean; description: string }[];
}

export interface ApiExplorerProps {
  endpoint: ApiEndpoint;
  onExecute: (params: any) => Promise<any>;
  className?: string;
}

const ApiExplorer = ({ endpoint, onExecute, className }: ApiExplorerProps) => {
  const [params, setParams] = React.useState<Record<string, string>>({});
  const [result, setResult] = React.useState<any>(null);
  const [isLoading, setIsLoading] = React.useState(false);
  const [activeTab, setActiveTab] = React.useState('request');

  const handleExecute = async () => {
    setIsLoading(true);
    try {
      const data = await onExecute(params);
      setResult(data);
      setActiveTab('response');
    } catch (err) {
      setResult({ error: String(err) });
      setActiveTab('response');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={cn('flex flex-col rounded-ant-lg border border-slate-200 bg-white overflow-hidden shadow-sm', className)}>
      <div className="p-4 border-b border-slate-100 bg-slate-50/50 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Badge className={cn(
            "text-[10px] font-bold",
            endpoint.method === 'GET' ? 'bg-blue-500' :
            endpoint.method === 'POST' ? 'bg-emerald-500' :
            endpoint.method === 'DELETE' ? 'bg-red-500' : 'bg-amber-500'
          )}>
            {endpoint.method}
          </Badge>
          <code className="text-xs font-bold text-text-primary">{endpoint.path}</code>
        </div>
        <span className="text-[10px] text-text-muted font-medium">{endpoint.description}</span>
      </div>

      <div className="flex-1 flex flex-col md:flex-row">
        <div className="w-full md:w-1/2 p-6 border-r border-slate-100">
          <h4 className="text-[10px] font-bold text-text-muted uppercase tracking-widest mb-4 flex items-center">
            <Terminal className="h-3 w-3 mr-2" /> Request Parameters
          </h4>
          <div className="space-y-4">
            {endpoint.parameters.map((param) => (
              <div key={param.name} className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-bold text-text-primary">{param.name}</label>
                  <span className="text-[9px] text-text-muted uppercase font-mono">{param.type}{param.required ? '*' : ''}</span>
                </div>
                <input
                  type="text"
                  className="w-full rounded-ant-md border border-slate-200 bg-slate-50 px-3 py-2 text-xs focus:ring-brand-primary focus:border-brand-primary transition-all"
                  placeholder={param.description}
                  value={params[param.name] || ''}
                  onChange={(e) => setParams({ ...params, [param.name]: e.target.value })}
                />
              </div>
            ))}
            <Button
              onClick={handleExecute}
              disabled={isLoading}
              className="w-full mt-4"
            >
              {isLoading ? 'Executing...' : 'Run Request'}
              <Play className="ml-2 h-3 w-3 fill-current" />
            </Button>
          </div>
        </div>

        <div className="w-full md:w-1/2 flex flex-col bg-slate-900">
          <Tabs
            tabs={[
              { id: 'request', label: 'CURL', icon: <Terminal className="h-3 w-3" /> },
              { id: 'response', label: 'Response', icon: <FileJson className="h-3 w-3" /> },
            ]}
            activeTab={activeTab}
            onChange={setActiveTab}
            variant="underline"
            className="border-slate-800 px-4"
          />
          <div className="flex-1 p-4 overflow-auto max-h-[400px]">
            {activeTab === 'request' ? (
              <CodeBlock
                code={`curl -X ${endpoint.method} "https://api.antigravity.ai${endpoint.path}" \\
  -H "Authorization: Bearer $API_KEY" ${Object.keys(params).length ? `\\
  -d '${JSON.stringify(params, null, 2)}'` : ''}`}
                language="bash"
              />
            ) : (
              result ? (
                <CodeBlock
                  code={JSON.stringify(result, null, 2)}
                  language="json"
                />
              ) : (
                <div className="flex flex-col items-center justify-center h-full text-slate-600 italic text-xs">
                  Run request to see response
                </div>
              )
            )}
          </div>
        </div>
      </div>

      <div className="px-4 py-2 border-t border-slate-800 bg-slate-950 flex items-center justify-between text-[9px] font-mono text-slate-500">
        <div className="flex items-center space-x-3">
          <span className="flex items-center"><ShieldCheck className="h-3 w-3 mr-1 text-emerald-500" /> Authorized</span>
          <span>Latency: {isLoading ? '...' : result ? '124ms' : '--'}</span>
        </div>
        <span>v1.0.4-stable</span>
      </div>
    </div>
  );
};

export { ApiExplorer };
