import React from "react";

export interface PulseLoaderProps {
  label?: string;
  size?: "sm" | "md";
}

export const PulseLoader: React.FC<PulseLoaderProps> = ({
  label = "Processing stream...",
  size = "md",
}) => {
  return (
    <div className="flex items-center gap-2 select-none">
      <span className="relative flex h-2.5 w-2.5">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
        <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500" />
      </span>
      {label && (
        <span
          className={`${
            size === "sm" ? "text-xs" : "text-sm"
          } font-medium text-emerald-400 tracking-wide`}
        >
          {label}
        </span>
      )}
    </div>
  );
};
