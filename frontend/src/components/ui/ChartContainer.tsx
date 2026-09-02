import React from "react";
import { ResponsiveContainer } from "recharts";
import { EmptyState } from "./EmptyState";
import { Skeleton } from "./Skeleton";

export interface ChartContainerProps {
  title?: string;
  subtitle?: string;
  height?: number;
  isLoading?: boolean;
  isEmpty?: boolean;
  emptyTitle?: string;
  action?: React.ReactNode;
  children: React.ReactElement;
  className?: string;
}

export const ChartContainer: React.FC<ChartContainerProps> = ({
  title,
  subtitle,
  height = 300,
  isLoading = false,
  isEmpty = false,
  emptyTitle = "No metric data available",
  action,
  children,
  className = "",
}) => {
  return (
    <div className={`p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 backdrop-blur-xl shadow-xl flex flex-col ${className}`}>
      {(title || action) && (
        <div className="flex items-start justify-between mb-4 pb-2 border-b border-slate-800/60">
          <div>
            {title && (
              <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-200">
                {title}
              </h3>
            )}
            {subtitle && <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>}
          </div>
          {action && <div>{action}</div>}
        </div>
      )}

      <div className="flex-1 w-full" style={{ minHeight: height }}>
        {isLoading ? (
          <div className="h-full w-full flex items-center justify-center p-4">
            <Skeleton variant="rectangular" className="h-full w-full min-h-[200px]" />
          </div>
        ) : isEmpty ? (
          <EmptyState title={emptyTitle} description="No data generated for selected date range." />
        ) : (
          <ResponsiveContainer width="100%" height={height}>
            {children}
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};
