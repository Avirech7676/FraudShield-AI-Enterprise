import React from "react";

export const Footer: React.FC = () => {
  return (
    <footer className="mt-12 pt-6 border-t border-slate-800/60 flex flex-col md:flex-row items-center justify-between text-xs text-slate-500 gap-3 select-none">
      <div className="flex items-center gap-2">
        <span className="font-semibold text-slate-400">FraudShield AI Enterprise</span>
        <span>•</span>
        <span>Version 2.0.0</span>
      </div>

      <div className="flex items-center gap-6 text-slate-400">
        <a href="#docs" className="hover:text-indigo-400 transition-colors">API Docs</a>
        <a href="#compliance" className="hover:text-indigo-400 transition-colors">PCI-DSS Security</a>
        <a href="#support" className="hover:text-indigo-400 transition-colors">System Support</a>
      </div>
    </footer>
  );
};
