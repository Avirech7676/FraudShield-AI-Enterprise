import React, { forwardRef } from "react";

export interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  description?: string;
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, description, className = "", id, ...props }, ref) => {
    const checkboxId = id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className="flex items-start gap-3 select-none">
        <div className="relative flex items-center pt-0.5">
          <input
            type="checkbox"
            id={checkboxId}
            ref={ref}
            className={`w-4 h-4 bg-slate-900 border border-slate-700 rounded text-indigo-600 focus:ring-2 focus:ring-indigo-500/40 focus:ring-offset-slate-900 cursor-pointer transition-all ${className}`}
            {...props}
          />
        </div>
        {(label || description) && (
          <div className="flex flex-col">
            {label && (
              <label
                htmlFor={checkboxId}
                className="text-sm font-medium text-slate-200 cursor-pointer"
              >
                {label}
              </label>
            )}
            {description && (
              <span className="text-xs text-slate-400">{description}</span>
            )}
          </div>
        )}
      </div>
    );
  }
);

Checkbox.displayName = "Checkbox";
