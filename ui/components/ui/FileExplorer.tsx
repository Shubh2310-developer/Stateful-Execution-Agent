import * as React from 'react';
import { File, Folder, ChevronRight, ChevronDown, FileCode, FileText, FileJson } from 'lucide-react';
import { cn } from '../../lib/utils';

export interface FileNode {
  id: string;
  name: string;
  type: 'file' | 'folder';
  extension?: string;
  children?: FileNode[];
}

export interface FileExplorerProps {
  data: FileNode[];
  onSelect?: (node: FileNode) => void;
  selectedId?: string;
  className?: string;
}

const FileExplorerNode = ({
  node,
  depth,
  onSelect,
  selectedId
}: {
  node: FileNode;
  depth: number;
  onSelect?: (node: FileNode) => void;
  selectedId?: string;
}) => {
  const [isOpen, setIsOpen] = React.useState(true);
  const isSelected = selectedId === node.id;
  const isFolder = node.type === 'folder';

  const getIcon = () => {
    if (isFolder) {
      return isOpen ? (
        <ChevronDown className="h-4 w-4 text-text-muted" />
      ) : (
        <ChevronRight className="h-4 w-4 text-text-muted" />
      );
    }

    switch (node.extension) {
      case 'ts':
      case 'tsx':
      case 'js':
      case 'jsx':
        return <FileCode className="h-4 w-4 text-blue-500" />;
      case 'json':
        return <FileJson className="h-4 w-4 text-amber-500" />;
      case 'md':
        return <FileText className="h-4 w-4 text-emerald-500" />;
      default:
        return <File className="h-4 w-4 text-slate-400" />;
    }
  };

  return (
    <div className="flex flex-col">
      <button
        onClick={() => {
          if (isFolder) setIsOpen(!isOpen);
          onSelect?.(node);
        }}
        className={cn(
          'flex items-center py-1 px-2 rounded-ant-sm text-sm transition-colors group',
          isSelected ? 'bg-brand-primary/10 text-brand-primary' : 'hover:bg-slate-100 text-text-secondary'
        )}
        style={{ paddingLeft: `${depth * 12 + 8}px` }}
      >
        <span className="mr-2 shrink-0">{getIcon()}</span>
        {isFolder && <Folder className="h-4 w-4 mr-2 text-brand-primary/60" />}
        <span className="truncate">{node.name}</span>
      </button>

      {isFolder && isOpen && node.children && (
        <div className="flex flex-col">
          {node.children.map((child) => (
            <FileExplorerNode
              key={child.id}
              node={child}
              depth={depth + 1}
              onSelect={onSelect}
              selectedId={selectedId}
            />
          ))}
        </div>
      )}
    </div>
  );
};

const FileExplorer = ({ data, onSelect, selectedId, className }: FileExplorerProps) => {
  return (
    <div className={cn('flex flex-col space-y-1 py-2 overflow-auto', className)}>
      {data.map((node) => (
        <FileExplorerNode
          key={node.id}
          node={node}
          depth={0}
          onSelect={onSelect}
          selectedId={selectedId}
        />
      ))}
    </div>
  );
};

export { FileExplorer };
