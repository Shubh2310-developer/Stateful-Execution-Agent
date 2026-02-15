import * as React from 'react';
import { Lock, Unlock, Shield, AlertTriangle } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Checkbox } from './Checkbox';

export interface Permission {
  id: string;
  label: string;
  description: string;
}

export interface Role {
  id: string;
  label: string;
}

export interface PermissionMatrixProps {
  permissions: Permission[];
  roles: Role[];
  values: Record<string, string[]>; // roleId -> permissionIds[]
  onChange?: (roleId: string, permissionId: string, enabled: boolean) => void;
  className?: string;
}

const PermissionMatrix = ({
  permissions,
  roles,
  values,
  onChange,
  className
}: PermissionMatrixProps) => {
  return (
    <div className={cn('w-full border border-slate-200 rounded-ant-lg bg-white overflow-hidden', className)}>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200">
              <th className="p-4 text-[10px] font-bold text-text-muted uppercase tracking-widest min-w-[200px]">
                Permission Scope
              </th>
              {roles.map((role) => (
                <th key={role.id} className="p-4 text-[10px] font-bold text-text-primary uppercase tracking-widest text-center">
                  {role.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {permissions.map((permission) => (
              <tr key={permission.id} className="hover:bg-slate-50/50 transition-colors">
                <td className="p-4">
                  <div className="flex flex-col">
                    <span className="text-sm font-bold text-text-primary">{permission.label}</span>
                    <span className="text-xs text-text-muted">{permission.description}</span>
                  </div>
                </td>
                {roles.map((role) => {
                  const isEnabled = values[role.id]?.includes(permission.id);
                  return (
                    <td key={role.id} className="p-4 text-center">
                      <div className="flex justify-center">
                        <Checkbox
                          checked={isEnabled}
                          onChange={(e) => onChange?.(role.id, permission.id, e.target.checked)}
                          className="m-0"
                        />
                      </div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export { PermissionMatrix };
