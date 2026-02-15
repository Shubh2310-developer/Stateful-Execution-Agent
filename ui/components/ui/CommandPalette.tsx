import * as React from 'react';
import { Search, Command as CommandIcon } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Modal } from './Modal';

export interface CommandPaletteItem {
  id: string;
  label: string;
  category?: string;
  shortcut?: string;
  icon?: React.ReactNode;
  onSelect: () => void;
}

export interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  items: CommandPaletteItem[];
  placeholder?: string;
}

const CommandPalette = ({
  isOpen,
  onClose,
  items,
  placeholder = "Search commands or actions..."
}: CommandPaletteProps) => {
  const [search, setSearch] = React.useState('');
  const [selectedIndex, setSelectedIndex] = React.useState(0);

  const filteredItems = items.filter(item =>
    item.label.toLowerCase().includes(search.toLowerCase()) ||
    item.category?.toLowerCase().includes(search.toLowerCase())
  );

  React.useEffect(() => {
    setSelectedIndex(0);
  }, [search]);

  // Handle keyboard navigation
  React.useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex(prev => (prev + 1) % Math.max(filteredItems.length, 1));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex(prev => (prev - 1 + filteredItems.length) % Math.max(filteredItems.length, 1));
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (filteredItems[selectedIndex]) {
          filteredItems[selectedIndex].onSelect();
          onClose();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, filteredItems, selectedIndex, onClose]);

  if (!isOpen) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      className="max-w-2xl p-0 overflow-hidden"
    >
      <div className="flex items-center border-b border-slate-200 px-4 py-3">
        <Search className="h-5 w-5 text-text-muted mr-3" />
        <input
          autoFocus
          className="flex-1 bg-transparent border-none focus:ring-0 text-lg placeholder:text-text-muted text-text-primary"
          placeholder={placeholder}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <div className="flex items-center space-x-1 px-1.5 py-0.5 rounded border border-slate-200 bg-slate-50 text-[10px] text-text-muted font-mono">
          <CommandIcon className="h-2.5 w-2.5" />
          <span>K</span>
        </div>
      </div>

      <div className="max-h-[400px] overflow-y-auto p-2">
        {filteredItems.length === 0 ? (
          <div className="py-12 text-center text-text-muted">
            No commands found for "{search}"
          </div>
        ) : (
          <div className="space-y-1">
            {filteredItems.map((item, index) => (
              <button
                key={item.id}
                onClick={() => {
                  item.onSelect();
                  onClose();
                }}
                className={cn(
                  'flex w-full items-center justify-between px-3 py-2.5 rounded-ant-md transition-all text-left',
                  index === selectedIndex
                    ? 'bg-brand-primary text-white shadow-md'
                    : 'hover:bg-slate-100 text-text-primary'
                )}
              >
                <div className="flex items-center">
                  {item.icon && <span className={cn("mr-3", index === selectedIndex ? "text-white" : "text-text-muted")}>{item.icon}</span>}
                  <div>
                    <div className="text-sm font-medium">{item.label}</div>
                    {item.category && (
                      <div className={cn("text-[10px] uppercase tracking-wider font-bold", index === selectedIndex ? "text-white/70" : "text-text-muted")}>
                        {item.category}
                      </div>
                    )}
                  </div>
                </div>
                {item.shortcut && (
                  <span className={cn("text-xs font-mono", index === selectedIndex ? "text-white/80" : "text-text-muted")}>
                    {item.shortcut}
                  </span>
                )}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="border-t border-slate-100 bg-slate-50/50 px-4 py-2 flex items-center justify-between text-[10px] text-text-muted font-medium">
        <div className="flex items-center space-x-4">
          <span className="flex items-center space-x-1">
            <kbd className="px-1 rounded border bg-white">↑↓</kbd>
            <span>Navigate</span>
          </span>
          <span className="flex items-center space-x-1">
            <kbd className="px-1 rounded border bg-white">Enter</kbd>
            <span>Select</span>
          </span>
        </div>
        <span>Antigravity OS v1.0</span>
      </div>
    </Modal>
  );
};

export { CommandPalette };
