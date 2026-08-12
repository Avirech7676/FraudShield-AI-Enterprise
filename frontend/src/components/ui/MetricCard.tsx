import React from "react";
import { Card } from "./Card";
import { Badge } from "./Badge";

export interface MetricCardProps {
  title: string;
  value: string | number;
  change?: string;
  trend?: "up" | "down" | "neutral";
  subtitle?: string;
  icon?: React.ReactNode;
  iconBg?: "indigo" | "rose" | "emerald" | "amber" | "sky";
  isLoading?: boolean;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  change,
  trend = "neutral",
  subtitle,
  icon,
  iconBg = "indigo",
  isLoading = false,
}) => {
  const iconBgClasses = {
    indigo: "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20",
    rose: "bg-rose-500/10 text-rose-400 border border-rose-500/20",
    emerald: "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20",
    amber: "bg-amber-500/10 text-amber-400 border border-amber-500/20",
    sky: "bg-sky-500/10 text-sky-400 border border-sky-500/20",
  };

  const trendVariant =
    trend === "up" ? "emerald" : trend === "down" ? "rose" : "slate";

  return (
    <Card variant="glass" hoverGlow className="relative overflow-hidden">
      <div className="flex items-start justify-between">
        <div className="flex flex-col">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            {title}
          </span>
          {isLoading ? (
            <div className="h-8 w-24 bg-slate-800 animate-pulse rounded-lg mt-2" />
          ) : (
            <div className="text-2xl font-bold text-slate-100 tracking-tight mt-1.5">
              {value}
            </div>
          )}
        </div>
        {icon && (
          <div className={`p-3 rounded-xl flex items-center justify-center ${iconBgClasses[iconBg]}`}>
            {icon}
          </div>
        )}
      </div>

      {(change || subtitle) && (
        <div className="flex items-center gap-2 mt-4 pt-3 border-t border-slate-800/60">
          {change && (
            <Badge variant={trendVariant} size="sm">
              {trend === "up" ? "↑" : trend === "down" ? "↓" : "•"} {change}
            </Badge>
          )}
          {subtitle && <span className="text-xs text-slate-400">{subtitle}</span>}
        </div>
      )}
    </Card>
  );
};
