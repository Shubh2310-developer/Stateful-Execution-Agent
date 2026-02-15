import * as React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Plus, Hash, X } from 'lucide-react';
import { cn } from '../../lib/utils';
import { ConstraintChip } from './ConstraintChip';

export interface Constraint {
  id: string;
  label: string;
  value: string;
}

export interface ConstraintTagInputProps {
  constraints: Constraint[];
  onChange: (constraints: Constraint[]) => void;
  className?: string;
  placeholder?: string;
}

const ConstraintTagInput = ({
  constraints,
  onChange,
  className,
  placeholder = "Add constraint (e.g. --deadline:tomorrow)..."
}: ConstraintTagInputProps) => {
  const [inputValue, setInputValue] = React.useState('');
  const inputRef = React.useRef<HTMLInputElement>(null);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addConstraint();
    } else if (e.key === 'Backspace' && !inputValue && constraints.length > 0) {
      removeConstraint(constraints[constraints.length - 1].id);
    }
  };

  const addConstraint = () => {
    const trimmed = inputValue.trim();
    if (!trimmed) return;

    // Support --key:value or --key=value or just value
    let label = 'Tag';
    let value = trimmed;

    if (trimmed.startsWith('--')) {
      const parts = trimmed.substring(2).split(/[:=]/);
      if (parts.length >= 2) {
        label = parts[0];
        value = parts.slice(1).join(':');
      }
    }

    const newConstraint: Constraint = {
      id: Math.random().toString(36).substr(2, 9),
      label: label.charAt(0).toUpperCase() + label.slice(1),
      value: value.trim()
    };

    onChange([...constraints, newConstraint]);
    setInputValue('');
  };

  const removeConstraint = (id: string) => {
    onChange(constraints.filter(c => c.id !== id));
  };

  return (
    <div
      className={cn(
        'flex flex-wrap items-center gap-2 p-2 w-full rounded-ant-md border border-slate-300 bg-background-surface min-h-[42px] focus-within:ring-2 focus-within:ring-brand-primary/20 focus-within:border-brand-primary transition-all duration-150',
        className
      )}
      onClick={() => inputRef.current?.focus()}
    >
      <AnimatePresence initial={false}>
        {constraints.map((c) => (
          <ConstraintChip
            key={c.id}
            label={c.label}
            value={c.value}
            onRemove={() => removeConstraint(c.id)}
          />
        ))}
      </AnimatePresence>

      <input
        ref={inputRef}
        type="text"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyDown={handleKeyDown}
        onBlur={addConstraint}
        placeholder={constraints.length === 0 ? placeholder : ""}
        className="flex-1 min-w-[150px] bg-transparent text-sm border-none focus:ring-0 p-1 placeholder:text-text-muted text-text-primary"
      />
    </div>
  );
};

export { ConstraintTagInput };
