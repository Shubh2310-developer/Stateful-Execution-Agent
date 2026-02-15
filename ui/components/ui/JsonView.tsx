import * as React from 'react';
import { cn } from '../../lib/utils';
import { ScrollArea } from './ScrollArea';

export interface JsonViewProps {
  data: any;
  depth?: number;
  maxDepth?: number;
  className?: string;
}

const JsonView = ({
  data,
  depth = 0,
  maxDepth = 10,
  className
}: JsonViewProps) => {
  const renderValue = (value: any, key?: string | number) => {
    const type = typeof value;

    if (value === null) {
      return <span className="text-red-400">null</span>;
    }

    if (type === 'boolean') {
      return <span className="text-amber-400">{String(value)}</span>;
    }

    if (type === 'number') {
      return <span className="text-blue-400">{value}</span>;
    }

    if (type === 'string') {
      return <span className="text-emerald-400">"{value}"</span>;
    }

    if (Array.isArray(value)) {
      if (depth >= maxDepth) return <span className="text-slate-500">[Array]</span>;
      return (
        <div className="flex flex-col">
          <span className="text-slate-500">[</span>
          <div className="pl-4 border-l border-slate-800 ml-1">
            {value.map((v, i) => (
              <div key={i} className="flex">
                <span className="text-slate-600 mr-2">{i}:</span>
                {renderValue(v)}
                {i < value.length - 1 && <span className="text-slate-500">,</span>}
              </div>
            ))}
          </div>
          <span className="text-slate-500">]</span>
        </div>
      );
    }

    if (type === 'object') {
      if (depth >= maxDepth) return <span className="text-slate-500">{"{Object}"}</span>;
      const keys = Object.keys(value);
      return (
        <div className="flex flex-col">
          <span className="text-slate-500">{"{"}</span>
          <div className="pl-4 border-l border-slate-800 ml-1">
            {keys.map((k, i) => (
              <div key={k} className="flex">
                <span className="text-slate-400 mr-2">"{k}":</span>
                <JsonView data={value[k]} depth={depth + 1} maxDepth={maxDepth} />
                {i < keys.length - 1 && <span className="text-slate-500">,</span>}
              </div>
            ))}
          </div>
          <span className="text-slate-500">{"}"}</span>
        </div>
      );
    }

    return <span>{String(value)}</span>;
  };

  return (
    <div className={cn(
      'font-mono text-xs overflow-x-auto',
      depth === 0 && 'bg-slate-900 p-4 rounded-ant-lg text-slate-300',
      className
    )}>
      {renderValue(data)}
    </div>
  );
};

export { JsonView };
