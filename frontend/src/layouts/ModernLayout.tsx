import React from "react";
import { Outlet } from "react-router-dom";
import { Sidebar } from "../components/ui/Sidebar";
import { Topbar } from "../components/ui/Topbar";
import { ErrorBoundary } from "../components/ui/ErrorBoundary";

const ModernLayout: React.FC = () => {
  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#02040a" }}>
      <Sidebar />

      <main style={{ flex: 1, minWidth: 0, display: "flex", flexDirection: "column", overflowX: "hidden" }}>
        <Topbar />
        <div style={{ flex: 1, padding: "0 24px 40px" }}>
          <ErrorBoundary>
            <div className="animate-fade-in">
              <Outlet />
            </div>
          </ErrorBoundary>
        </div>
      </main>
    </div>
  );
};

export default ModernLayout;
