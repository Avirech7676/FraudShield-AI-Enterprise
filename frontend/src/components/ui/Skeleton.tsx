import React from "react";

export interface SkeletonProps {
  variant?: "text" | "circular" | "rectangular" | "card";
  width?: string | number;
  height?: string | number;
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  variant = "text",
  width,
  height,
  className = "",
}) => {
  const baseClass = "animate-pulse bg-slate-800/70 border border-slate-700/30 backdrop-blur-sm";

  const variantClasses = {
    text: "h-4 rounded-md w-full",
    circular: "rounded-full",
    rectangular: "rounded-xl",
    card: "h-36 rounded-2xl w-full",
  };

  const style: React.CSSProperties = {
    width: width !== undefined ? width : undefined,
    height: height !== undefined ? height : undefined,
  };

  return <div className={`${baseClass} ${variantClasses[variant]} ${className}`} style={style} />;
};

export const TableSkeleton: React.FC<{ rows?: number; columns?: number }> = ({
  rows = 5,
  columns = 5,
}) => {
  return (
    <div className="w-full space-y-3">
      <div className="flex gap-4 pb-2 border-b border-slate-800">
        {Array.from({ length: columns }).map((_, i) => (
          <Skeleton key={i} variant="text" className="h-4 flex-1" />
        ))}
      </div>
      {Array.from({ length: rows }).map((_, r) => (
        <div key={r} className="flex gap-4 py-2 border-b border-slate-800/40">
          {Array.from({ length: columns }).map((_, c) => (
            <Skeleton key={c} variant="text" className="h-5 flex-1" />
          ))}
        </div>
      ))}
    </div>
  );
};
