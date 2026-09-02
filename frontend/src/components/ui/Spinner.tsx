import React from "react";

export interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  color?: "primary" | "current" | "white";
  className?: string;
}

export const Spinner: React.FC<SpinnerProps> = ({
  size = "md",
  color = "primary",
  className = "",
}) => {
  const sizeClasses = {
    sm: "w-4 h-4 border-2",
    md: "w-6 h-6 border-2",
    lg: "w-8 h-8 border-3",
  };

  const colorClasses = {
    primary: "border-indigo-500/20 border-t-indigo-500",
    current: "border-current/20 border-t-current",
    white: "border-white/20 border-t-white",
  };

  return (
    <div
      className={`inline-block rounded-full animate-spin ${sizeClasses[size]} ${colorClasses[color]} ${className}`}
      role="status"
      aria-label="loading"
    >
      <span className="sr-only">Loading...</span>
    </div>
  );
};
