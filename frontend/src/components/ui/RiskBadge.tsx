import React from "react";
import { Badge } from "./Badge";

export interface RiskBadgeProps {
  score?: number; // 0.0 - 1.0
  level?: "critical" | "high" | "medium" | "low" | "safe" | string;
  size?: "sm" | "md";
  showScore?: boolean;
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({
  score,
  level,
  size = "md",
  showScore = true,
}) => {
  let resolvedLevel = (level || "").toLowerCase();

  if (!resolvedLevel && score !== undefined) {
    if (score >= 0.85) resolvedLevel = "critical";
    else if (score >= 0.65) resolvedLevel = "high";
    else if (score >= 0.35) resolvedLevel = "medium";
    else if (score >= 0.15) resolvedLevel = "low";
    else resolvedLevel = "safe";
  }

  const variantMap: Record<string, "rose" | "amber" | "emerald" | "sky" | "slate"> = {
    critical: "rose",
    high: "rose",
    medium: "amber",
    low: "emerald",
    safe: "emerald",
  };

  const labelMap: Record<string, string> = {
    critical: "CRITICAL RISK",
    high: "HIGH RISK",
    medium: "MEDIUM RISK",
    low: "LOW RISK",
    safe: "SAFE",
  };

  const variant = variantMap[resolvedLevel || "safe"] || "slate";
  const label = labelMap[resolvedLevel || "safe"] || (resolvedLevel?.toUpperCase() || "UNKNOWN");
  const isHighRisk = resolvedLevel === "critical" || resolvedLevel === "high";

  return (
    <Badge variant={variant} size={size} dot pulse={isHighRisk}>
      {label} {showScore && score !== undefined ? `(${Math.round(score * 100)}%)` : ""}
    </Badge>
  );
};
