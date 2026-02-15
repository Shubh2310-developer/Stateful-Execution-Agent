import * as React from 'react';
import { Toast, ToastProps } from './Toast';
import { cn } from '../../lib/utils';

export interface ToasterProps {
  className?: string;
}

export interface ToastMessage extends Omit<ToastProps, 'onClose'> {
  id: string;
}

const Toaster = ({ className }: ToasterProps) => {
  const [toasts, setToasts] = React.useState<ToastMessage[]>([]);

  // This is a simplified version. In a real app, use a context or a store.
  // We're exposing a global window method just for demonstration.
  React.useEffect(() => {
    (window as any).addToast = (toast: Omit<ToastMessage, 'id'>) => {
      const id = Math.random().toString(36).substr(2, 9);
      setToasts((prev) => [...prev, { ...toast, id }]);
    };
  }, []);

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  return (
    <div
      className={cn(
        'fixed bottom-0 right-0 z-[100] flex max-h-screen w-full flex-col-reverse p-4 sm:bottom-0 sm:right-0 sm:top-auto sm:flex-col md:max-w-[420px] space-y-4 space-y-reverse',
        className
      )}
    >
      {toasts.map((toast) => (
        <Toast key={toast.id} {...toast} onClose={removeToast} />
      ))}
    </div>
  );
};

export { Toaster };
