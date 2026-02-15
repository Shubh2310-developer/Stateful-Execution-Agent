import * as React from 'react';
import { cn } from '../../lib/utils';
import { Avatar } from './Avatar';

export interface AvatarGroupProps {
  avatars: { src?: string; fallback: string; alt?: string; isAgent?: boolean }[];
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const AvatarGroup = ({ avatars, max = 3, size = 'sm', className }: AvatarGroupProps) => {
  const visibleAvatars = avatars.slice(0, max);
  const remainingCount = avatars.length - max;

  return (
    <div className={cn('flex -space-x-2 overflow-hidden', className)}>
      {visibleAvatars.map((avatar, i) => (
        <Avatar
          key={i}
          src={avatar.src}
          fallback={avatar.fallback}
          alt={avatar.alt}
          size={size}
          isAgent={avatar.isAgent}
          className="ring-2 ring-white"
        />
      ))}
      {remainingCount > 0 && (
        <div className={cn(
          "flex items-center justify-center rounded-full bg-slate-100 ring-2 ring-white text-[10px] font-bold text-text-secondary",
          size === 'sm' ? 'h-8 w-8' : size === 'md' ? 'h-10 w-10' : 'h-12 w-12'
        )}>
          +{remainingCount}
        </div>
      )}
    </div>
  );
};

export { AvatarGroup };
