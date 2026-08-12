import React from 'react';

interface CardProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  className?: string;
  variant?: 'glass' | 'surface' | 'elevated';
}

export const ModernCard: React.FC<CardProps> = ({ 
  children, 
  title, 
  subtitle, 
  className = '', 
  variant = 'glass' 
}) => {
  const variantClass = {
    glass: 'bg-glass border-glass shadow-glass backdrop-blur-xl',
    surface: 'bg-surface border-light',
    elevated: 'bg-surface-elevated border-medium shadow-xl'
  }[variant];

  return (
    <div className={`p-6 rounded-2xl transition-all duration-300 ${variantClass} ${className}`}>
      {(title || subtitle) && (
        <div className="mb-6">
          {title && <h3 className="text-xl font-bold text-white tracking-tight">{title}</h3>}
          {subtitle && <p className="text-sm text-slate-400 mt-1">{subtitle}</p>}
        </div>
      )}
      {children}
    </div>
  );
};

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'success';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  icon?: React.ReactNode;
}

export const ModernButton: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading,
  icon,
  className = '',
  ...props
}) => {
  const baseClasses = "inline-flex items-center justify-center font-semibold transition-all active:scale-95 disabled:opacity-50 disabled:pointer-events-none rounded-xl";
  
  const sizeClasses = {
    sm: "px-3 py-1.5 text-xs",
    md: "px-5 py-2.5 text-sm",
    lg: "px-8 py-3.5 text-base"
  }[size];

  const variantClasses = {
    primary: "bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-500/20",
    secondary: "bg-slate-800 hover:bg-slate-700 text-white border border-slate-700",
    ghost: "bg-transparent hover:bg-slate-800 text-slate-300",
    danger: "bg-rose-600 hover:bg-rose-500 text-white shadow-lg shadow-rose-500/20",
    success: "bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-500/20"
  }[variant];

  return (
    <button className={`${baseClasses} ${sizeClasses} ${variantClasses} ${className}`} {...props}>
      {isLoading ? (
        <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2" />
      ) : icon ? (
        <span className="mr-2">{icon}</span>
      ) : null}
      {children}
    </button>
  );
};
