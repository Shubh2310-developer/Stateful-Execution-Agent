import * as React from 'react';
import { Package, Download, Star, ShieldCheck, Users, Clock, ExternalLink } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Card } from './Card';
import { Badge } from './Badge';
import { Button } from './Button';

export interface MarketplaceListingProps {
  title: string;
  publisher: string;
  description: string;
  version: string;
  rating: number;
  installCount: string;
  capabilities: string[];
  isVerified?: boolean;
  price?: string; // e.g. "Free" or "$2.00/task"
  onInstall?: () => void;
  onViewDetails?: () => void;
  className?: string;
}

const MarketplaceListing = ({
  title,
  publisher,
  description,
  version,
  rating,
  installCount,
  capabilities,
  isVerified = false,
  price = "Free",
  onInstall,
  onViewDetails,
  className
}: MarketplaceListingProps) => {
  return (
    <Card className={cn('p-0 overflow-hidden flex flex-col h-full hover:shadow-xl transition-all duration-300 border-slate-200 group', className)}>
      {/* Header/Banner Area */}
      <div className="h-24 bg-gradient-to-br from-slate-900 to-brand-primary/40 relative overflow-hidden flex items-center justify-center">
        <Package size={48} className="text-white/20 group-hover:scale-110 transition-transform duration-500" />
        <div className="absolute bottom-0 left-0 w-full h-1 bg-brand-primary" />
        <div className="absolute top-3 right-3">
          <Badge className="bg-white/20 backdrop-blur-md text-white border-transparent text-[10px] font-bold uppercase tracking-widest">
            {price}
          </Badge>
        </div>
      </div>

      <div className="p-5 flex flex-col flex-1">
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2 mb-0.5">
              <h3 className="text-base font-bold text-text-primary truncate">{title}</h3>
              {isVerified && (
                <Tooltip content="Verified Secure by Antigravity Audit">
                  <ShieldCheck size={14} className="text-emerald-500 shrink-0" />
                </Tooltip>
              )}
            </div>
            <p className="text-[10px] text-text-muted font-bold uppercase tracking-widest">By {publisher} • v{version}</p>
          </div>
        </div>

        <p className="text-xs text-text-secondary line-clamp-2 leading-relaxed mb-6">
          {description}
        </p>

        <div className="space-y-4 mt-auto">
          <div className="flex flex-wrap gap-1.5">
            {capabilities.slice(0, 3).map(cap => (
              <Badge key={cap} variant="outline" className="text-[8px] h-4 py-0 border-slate-200 text-slate-500 font-bold uppercase tracking-tighter">
                {cap}
              </Badge>
            ))}
            {capabilities.length > 3 && <span className="text-[8px] text-text-muted font-bold">+{capabilities.length - 3} MORE</span>}
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-slate-100">
            <div className="flex items-center space-x-4">
              <div className="flex items-center text-[10px] font-bold text-amber-500">
                <Star size={12} className="fill-current mr-1" />
                {rating.toFixed(1)}
              </div>
              <div className="flex items-center text-[10px] font-bold text-text-muted">
                <Users size={12} className="mr-1" />
                {installCount}
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <Button size="sm" variant="ghost" onClick={onViewDetails} className="h-8 w-8 p-0 rounded-full">
                <ExternalLink size={14} />
              </Button>
              <Button size="sm" onClick={onInstall} className="h-8 text-[10px] font-bold uppercase tracking-widest px-4">
                Install
              </Button>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

export { MarketplaceListing };
