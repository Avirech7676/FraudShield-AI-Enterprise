import React from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";
import { Button } from "./Button";

export interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  className?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = "System Error Encountered",
  message = "Failed to load data from server. Please verify network connection or try again.",
  onRetry,
  className = "",
}) => {
  return (
    <div className={`flex flex-col items-center justify-center p-10 text-center rounded-2xl bg-rose-950/20 border border-rose-500/30 backdrop-blur-sm ${className}`}>
      <div className="p-3.5 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-400 mb-4 shadow-lg shadow-rose-950/40">
        <AlertTriangle className="w-8 h-8" />
      </div>
      <h3 className="text-base font-semibold text-rose-200 tracking-tight mb-1">{title}</h3>
      <p className="text-sm text-slate-300 max-w-md mb-6">{message}</p>
      {onRetry && (
        <Button variant="danger" size="sm" leftIcon={<RefreshCw className="w-4 h-4" />} onClick={onRetry}>
          Retry Request
        </Button>
      )}
    </div>
  );
};
