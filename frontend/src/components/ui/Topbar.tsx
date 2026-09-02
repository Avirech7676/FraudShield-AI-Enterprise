import React, { useState } from "react";
import { useLocation } from "react-router-dom";
import { Search, Bell, RefreshCw, Clock } from "lucide-react";
import { useAuth } from "../../hooks/useAuth";

const PAGE_META: Record<string, { title: string; subtitle: string }> = {
  "/dashboard":  { title: "Fraud Monitoring Center",   subtitle: "Real-time threat detection, AI predictions & risk intelligence" },
  "/prediction": { title: "Fraud Prediction Engine",   subtitle: "Submit transactions for instant AI-powered risk assessment" },
  "/history":    { title: "Audit Log",                 subtitle: "Complete tamper-evident transaction and prediction history" },
  "/alerts":     { title: "Threat Alerts",             subtitle: "Live fraud signals, anomaly detections and rule triggers" },
  "/cases":      { title: "Incident Management",       subtitle: "Investigate, escalate and resolve fraud incidents" },
  "/analytics":  { title: "Analytics & Insights",      subtitle: "Trend analysis, model performance and risk distribution" },
  "/reports":    { title: "AI Executive Reports",      subtitle: "Groq LLM-generated risk briefings and compliance summaries" },
  "/models":     { title: "Model Registry",            subtitle: "CatBoost ensemble versions, drift monitoring and retraining" },
  "/users":      { title: "User Management",           subtitle: "Operators, roles, permissions and audit trails" },
  "/settings":   { title: "System Settings",           subtitle: "Configuration, integrations, thresholds and alerting rules" },
};

function useNow() {
  const [now] = useState(() => new Date());
  return now;
}

export const Topbar: React.FC = () => {
  const { pathname } = useLocation();
  const { user } = useAuth();
  const now = useNow();

  const meta = PAGE_META[pathname] ?? { title: "FraudShield Enterprise", subtitle: "AI-powered fraud detection platform" };

  return (
    <div className="topbar" style={{ padding: "14px 24px", marginBottom: 28 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16 }}>
        {/* Left: page title */}
        <div>
          <h1 style={{ fontSize: 18, fontWeight: 700, color: "#f1f5f9", letterSpacing: "-0.02em", margin: 0, lineHeight: 1 }}>
            {meta.title}
          </h1>
          <p style={{ fontSize: 12, color: "#475569", margin: "5px 0 0", lineHeight: 1 }}>
            {meta.subtitle}
          </p>
        </div>

        {/* Right: controls */}
        <div style={{ display: "flex", alignItems: "center", gap: 10, flexShrink: 0 }}>
          {/* Search */}
          <div style={{ position: "relative", display: "flex", alignItems: "center" }}>
            <Search size={13} color="#475569" style={{ position: "absolute", left: 11, pointerEvents: "none" }} />
            <input
              type="text"
              placeholder="Search... (Ctrl+K)"
              className="fs-input"
              style={{ width: 220, paddingLeft: 32, paddingRight: 12, paddingTop: 8, paddingBottom: 8, fontSize: 13, borderRadius: 8 }}
            />
          </div>

          {/* Live pill */}
          <div style={{ display: "flex", alignItems: "center", gap: 7, padding: "6px 12px", borderRadius: 8, background: "rgba(16,185,129,0.08)", border: "1px solid rgba(16,185,129,0.2)" }}>
            <span style={{ position: "relative", width: 8, height: 8, display: "flex", flexShrink: 0 }}>
              <span style={{ position: "absolute", inset: 0, borderRadius: "50%", background: "#10b981", opacity: 0.4, animation: "pulse-glow 2s ease infinite" }} />
              <span style={{ position: "absolute", inset: 1, borderRadius: "50%", background: "#10b981" }} />
            </span>
            <span style={{ fontSize: 11, fontWeight: 600, color: "#10b981", letterSpacing: "0.06em", textTransform: "uppercase" }}>Live</span>
          </div>

          {/* Timestamp */}
          <div style={{ display: "flex", alignItems: "center", gap: 6, padding: "6px 12px", borderRadius: 8, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)", fontSize: 11, color: "#475569" }}>
            <Clock size={12} />
            {now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })} UTC+5:30
          </div>

          {/* Refresh */}
          <button
            onClick={() => window.location.reload()}
            title="Refresh data"
            style={{ width: 34, height: 34, borderRadius: 8, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)", color: "#64748b", display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer", transition: "all 0.18s" }}
            onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.color = "#e2e8f0"; (e.currentTarget as HTMLButtonElement).style.background = "rgba(255,255,255,0.07)"; }}
            onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.color = "#64748b"; (e.currentTarget as HTMLButtonElement).style.background = "rgba(255,255,255,0.03)"; }}
          >
            <RefreshCw size={14} />
          </button>

          {/* Bell */}
          <button
            title="Notifications"
            style={{ width: 34, height: 34, borderRadius: 8, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)", color: "#64748b", display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer", position: "relative", transition: "all 0.18s" }}
            onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.color = "#e2e8f0"; (e.currentTarget as HTMLButtonElement).style.background = "rgba(255,255,255,0.07)"; }}
            onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.color = "#64748b"; (e.currentTarget as HTMLButtonElement).style.background = "rgba(255,255,255,0.03)"; }}
          >
            <Bell size={14} />
            <span style={{ position: "absolute", top: 6, right: 6, width: 7, height: 7, borderRadius: "50%", background: "#f43f5e", border: "1.5px solid #02040a" }} />
          </button>

          {/* User avatar */}
          <div style={{ width: 34, height: 34, borderRadius: 9, background: "linear-gradient(135deg, #6366f1, #a78bfa)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 700, fontSize: 13, cursor: "pointer", flexShrink: 0 }} title={user?.username}>
            {user?.username?.[0]?.toUpperCase() ?? "U"}
          </div>
        </div>
      </div>
    </div>
  );
};
