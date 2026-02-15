import * as React from 'react';
import { Shield, Lock, CheckCircle2, AlertCircle } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Input } from './Input';
import { Label } from './Label';
import { Button } from './Button';
import { Checkbox } from './Checkbox';

export interface ConnectionFormProps {
  toolName: string;
  fields: { id: string; label: string; type: string; placeholder?: string; required?: boolean }[];
  onSubmit: (data: Record<string, string>) => void;
  onCancel: () => void;
  isLoading?: boolean;
  className?: string;
}

const ConnectionForm = ({
  toolName,
  fields,
  onSubmit,
  onCancel,
  isLoading = false,
  className
}: ConnectionFormProps) => {
  const [formData, setFormData] = React.useState<Record<string, string>>({});
  const [agreed, setAgreed] = React.useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (agreed) {
      onSubmit(formData);
    }
  };

  return (
    <div className={cn('flex flex-col space-y-6', className)}>
      <div className="flex items-center space-x-3 p-4 bg-blue-50 border border-blue-100 rounded-ant-lg">
        <div className="h-10 w-10 rounded-full bg-brand-primary text-white flex items-center justify-center shrink-0 shadow-lg shadow-brand-primary/20">
          <Lock className="h-5 w-5" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-text-primary tracking-tight">Secure Connection</h3>
          <p className="text-[10px] text-text-secondary leading-relaxed">
            Your credentials for <span className="font-bold">{toolName}</span> are encrypted and stored in your organization's private vault.
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-4">
          {fields.map((field) => (
            <div key={field.id} className="space-y-1.5">
              <Label htmlFor={field.id} required={field.required}>{field.label}</Label>
              <Input
                id={field.id}
                type={field.type}
                placeholder={field.placeholder}
                value={formData[field.id] || ''}
                onChange={(e) => setFormData({ ...formData, [field.id]: e.target.value })}
                required={field.required}
                className="bg-white"
              />
            </div>
          ))}
        </div>

        <div className="p-4 bg-slate-50 rounded-ant-lg border border-slate-100">
          <Checkbox
            label={`I authorize Antigravity to access my ${toolName} data on my behalf.`}
            checked={agreed}
            onChange={(e) => setAgreed(e.target.checked)}
          />
        </div>

        <div className="flex items-center justify-end space-x-3 pt-2">
          <Button variant="ghost" onClick={onCancel} disabled={isLoading}>
            Cancel
          </Button>
          <Button type="submit" disabled={!agreed || isLoading} className="min-w-[120px]">
            {isLoading ? 'Connecting...' : 'Test & Save'}
          </Button>
        </div>
      </form>

      <div className="flex items-center justify-center space-x-4 text-[10px] text-text-muted font-medium">
        <div className="flex items-center">
          <Shield className="h-3 w-3 mr-1 text-emerald-500" />
          <span>AES-256 Encryption</span>
        </div>
        <div className="flex items-center">
          <CheckCircle2 className="h-3 w-3 mr-1 text-emerald-500" />
          <span>SOC2 Compliant</span>
        </div>
      </div>
    </div>
  );
};

export { ConnectionForm };
