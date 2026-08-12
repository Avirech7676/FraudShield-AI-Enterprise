import React from "react";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  variant?: "glass" | "solid" | "bordered";
  hoverGlow?: boolean;
  className?: string;
}

export const Card: React.FC<CardProps> = ({
  children,
  variant = "glass",
  hoverGlow = false,
  className = "",
  ...props
}) => {
  const variantClasses = {
    glass:
      "bg-slate-900/70 border border-slate-800/80 backdrop-blur-xl shadow-xl shadow-black/40",
    solid:
      "bg-slate-900 border border-slate-800 shadow-lg shadow-black/30",
    bordered:
      "bg-transparent border border-slate-800/80 hover:border-slate-700/80",
  };

  const hoverClass = hoverGlow
    ? "transition-all duration-300 hover:-translate-y-0.5 hover:shadow-indigo-500/10 hover:border-indigo-500/30"
    : "";

  return (
    <div
      className={`rounded-2xl p-6 ${variantClasses[variant]} ${hoverClass} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export const CardHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  children,
  className = "",
  ...props
}) => (
  <div className={`flex items-center justify-between pb-4 mb-4 border-b border-slate-800/60 ${className}`} {...props}>
    {children}
  </div>
);

export const CardTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({
  children,
  className = "",
  ...props
}) => (
  <h3 className={`text-base font-semibold text-slate-100 tracking-tight ${className}`} {...props}>
    {children}
  </h3>
);

export const CardDescription: React.FC<React.HTMLAttributes<HTMLParagraphElement>> = ({
  children,
  className = "",
  ...props
}) => (
  <p className={`text-xs text-slate-400 mt-0.5 ${className}`} {...props}>
    {children}
  </p>
);

export const CardContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  children,
  className = "",
  ...props
}) => (
  <div className={`${className}`} {...props}>
    {children}
  </div>
);

export const CardFooter: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  children,
  className = "",
  ...props
}) => (
  <div className={`pt-4 mt-4 border-t border-slate-800/60 flex items-center justify-between ${className}`} {...props}>
    {children}
  </div>
);
