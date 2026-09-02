import React from "react";

export interface BadgeProps {
  children: React.ReactNode;
  variant?: "indigo" | "emerald" | "amber" | "rose" | "slate" | "sky" | "purple";
  size?: "sm" | "md";
  dot?: boolean;
  pulse?: boolean;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = "indigo",
  size = "md",
  dot = false,
  pulse = false,
  className = "",
}) => {
  const variantClasses = {
    indigo: "bg-indigo-500/15 text-indigo-300 border-indigo-500/30",
    emerald: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
    amber: "bg-amber-500/15 text-amber-300 border-amber-500/30",
    rose: "bg-rose-500/15 text-rose-300 border-rose-500/30",
    slate: "bg-slate-800/80 text-slate-300 border-slate-700/60",
    sky: "bg-sky-500/15 text-sky-300 border-sky-500/30",
    purple: "bg-purple-500/15 text-purple-300 border-purple-500/30",
  };

  const dotClasses = {
    indigo: "bg-indigo-400",
    emerald: "bg-emerald-400",
    amber: "bg-amber-400",
    rose: "bg-rose-400",
    slate: "bg-slate-400",
    sky: "bg-sky-400",
    purple: "bg-purple-400",
  };

  const sizeClasses = {
    sm: "px-2 py-0.5 text-[11px] gap-1",
    md: "px-2.5 py-1 text-xs gap-1.5",
  };

  return (
    <span
      className={`inline-flex items-center font-medium rounded-full border backdrop-blur-sm select-none ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
    >
      {dot && (
        <span className="relative flex h-2 w-2">
          {pulse && (
            <span
              className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${dotClasses[variant]}`}
            />
          )}
          <span
            className={`relative inline-flex rounded-full h-2 w-2 ${dotClasses[variant]}`}
          />
        </span>
      )}
      <span>{children}</span>
    </span>
  );
};
