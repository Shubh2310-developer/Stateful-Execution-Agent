import * as React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Hash, X, AlertCircle } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Tooltip } from './Tooltip';

export interface ConstraintChipProps {
  label: string;
  value: string;
  onRemove?: () => void;
  isInvalid?: boolean;
  errorMessage?: string;
  className?: string;
}

const ConstraintChip = ({
  label,
  value,
  onRemove,
  isInvalid = false,
  errorMessage,
  className
}: ConstraintChipProps) => {
  const content = (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0.9, opacity: 0 }}
      className={cn(
        'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full border text-[11px] font-bold transition-all shadow-sm group',
        isInvalid
          ? 'bg-red-50 text-red-700 border-red-200 shadow-red-100/50'
          : 'bg-indigo-50 text-indigo-700 border-indigo-100 hover:border-indigo-300 shadow-indigo-100/50',
        className
      )}
    >
      <Hash className={cn(
        "h-3 w-3",
        isInvalid ? "text-red-400" : "text-indigo-400 group-hover:text-indigo-600"
      )} />
      <span className="opacity-70 font-medium">{label}:</span>
      <span className="tracking-tight">{value}</span>

      {isInvalid && <AlertCircle className="h-3 w-3 ml-0.5 animate-pulse" />}

      {onRemove && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onRemove();
          }}
          className={cn(
            'ml-1 p-0.5 rounded-full transition-colors',
            isInvalid ? 'hover:bg-red-200 text-red-500' : 'hover:bg-indigo-200 text-indigo-400 hover:text-indigo-600'
          )}
          aria-label={`Remove ${label} constraint`}
        >
          <X className="h-3 w-3" />
        </button>
      )}
    </motion.div>
  );

  if (isInvalid && errorMessage) {
    return (
      <Tooltip content={errorMessage} position="top">
        {content}
      </Tooltip>
    );
  }

  return content;
};

export { ConstraintChip };
