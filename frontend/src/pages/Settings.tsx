import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  getSettings,
  getSystem,
  reloadModel,
  clearCache,
  restartEngine,
} from "../services/settings";
import { Sliders, Cpu, RefreshCw, Trash2, RotateCcw, Server, CheckCircle2, AlertTriangle } from "lucide-react";

export default function SettingsPage() {
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  const { data: userSettings } = useQuery({
    queryKey: ["settings-user"],
    queryFn: getSettings,
  });

  const { data: systemInfo } = useQuery({
    queryKey: ["settings-system"],
    queryFn: getSystem,
  });

  const handleAction = async (actionName: string, actionFn: () => Promise<any>) => {
    setActionLoading(actionName);
    setActionMessage(null);
    try {
      const res = await actionFn();
      setActionMessage(res.message || `${actionName} completed successfully.`);
    } catch (err: any) {
      setActionMessage(`Failed to execute ${actionName}: ${err.message}`);
    } finally {
      setActionLoading(null);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }} className="animate-fade-in">
      {/* Subheader Toolbar */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, paddingBottom: 16, borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 36, height: 36, borderRadius: 10, background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.25)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <Sliders size={18} color="#818cf8" />
          </div>
          <div>
            <h2 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>
              System Configuration &amp; Operations
            </h2>
            <p style={{ fontSize: 12, color: "#475569", margin: "2px 0 0" }}>
              Engine controls, pipeline parameters, model retraining &amp; system health
            </p>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 8, padding: "6px 12px", borderRadius: 20, background: "rgba(16,185,129,0.12)", border: "1px solid rgba(16,185,129,0.25)", fontSize: 12, color: "#10b981", fontWeight: 600 }}>
          <span className="status-dot online" />
          System Normal
        </div>
      </div>

      {/* Action Notification */}
      {actionMessage && (
        <div style={{ padding: "12px 16px", borderRadius: 10, background: actionMessage.startsWith("Failed") ? "rgba(244,63,94,0.1)" : "rgba(16,185,129,0.1)", border: actionMessage.startsWith("Failed") ? "1px solid rgba(244,63,94,0.25)" : "1px solid rgba(16,185,129,0.25)", color: actionMessage.startsWith("Failed") ? "#fb7185" : "#34d399", fontSize: 13, display: "flex", alignItems: "center", gap: 10 }}>
          {actionMessage.startsWith("Failed") ? <AlertTriangle size={16} /> : <CheckCircle2 size={16} />}
          {actionMessage}
        </div>
      )}

      <div className="grid-2">
        {/* System & Hardware Telemetry */}
        <div className="fs-card" style={{ padding: 24 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 15, fontWeight: 700, color: "#f1f5f9", marginBottom: 20 }}>
            <Server size={18} color="#818cf8" />
            Engine Telemetry &amp; Specs
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {[
              { label: "Environment", value: userSettings?.system_defaults?.environment || "Production" },
              { label: "Engine Version", value: userSettings?.system_defaults?.version || "v2.0 Enterprise" },
              { label: "Operating System", value: systemInfo?.os || "Windows 11 x64" },
              { label: "Python Runtime", value: systemInfo?.python_version || "3.12.10" },
              { label: "Database Engine", value: systemInfo?.database || "MongoDB Community 7.0" },
              { label: "Streaming Broker", value: systemInfo?.streaming_broker || "Kafka 3.6 Cluster" },
              { label: "System Uptime", value: systemInfo?.uptime || "99.98% (30 days)" },
            ].map((item) => (
              <div key={item.label} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "10px 14px", borderRadius: 8, background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)", fontSize: 13 }}>
                <span style={{ color: "#64748b" }}>{item.label}</span>
                <span style={{ fontWeight: 600, color: "#e2e8f0", fontFamily: "var(--font-mono)", fontSize: 12 }}>{item.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Administration Actions */}
        <div className="fs-card" style={{ padding: 24 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 15, fontWeight: 700, color: "#f1f5f9", marginBottom: 20 }}>
            <Cpu size={18} color="#818cf8" />
            Administrative Operations
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            <div style={{ padding: 16, borderRadius: 12, background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <div>
                <div style={{ fontSize: 14, fontWeight: 600, color: "#f1f5f9" }}>Reload ML Model Registry</div>
                <div style={{ fontSize: 12, color: "#64748b", marginTop: 2 }}>Force hot-reload CatBoost ensemble into RAM</div>
              </div>
              <button
                className="btn-secondary"
                disabled={actionLoading === "Reload Model"}
                onClick={() => handleAction("Reload Model", reloadModel)}
                style={{ padding: "8px 14px", fontSize: 12 }}
              >
                <RefreshCw size={13} className={actionLoading === "Reload Model" ? "animate-spin" : ""} />
                Reload
              </button>
            </div>

            <div style={{ padding: 16, borderRadius: 12, background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <div>
                <div style={{ fontSize: 14, fontWeight: 600, color: "#f1f5f9" }}>Clear Inference Cache</div>
                <div style={{ fontSize: 12, color: "#64748b", marginTop: 2 }}>Purge in-memory SHAP waterfall cache</div>
              </div>
              <button
                className="btn-secondary"
                disabled={actionLoading === "Clear Cache"}
                onClick={() => handleAction("Clear Cache", clearCache)}
                style={{ padding: "8px 14px", fontSize: 12 }}
              >
                <Trash2 size={13} />
                Clear
              </button>
            </div>

            <div style={{ padding: 16, borderRadius: 12, background: "rgba(244,63,94,0.05)", border: "1px solid rgba(244,63,94,0.15)", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
              <div>
                <div style={{ fontSize: 14, fontWeight: 600, color: "#fb7185" }}>Restart Risk Engine</div>
                <div style={{ fontSize: 12, color: "#64748b", marginTop: 2 }}>Re-initialize rule evaluation engine &amp; pipelines</div>
              </div>
              <button
                className="btn-danger"
                disabled={actionLoading === "Restart Engine"}
                onClick={() => handleAction("Restart Engine", restartEngine)}
                style={{ padding: "8px 14px", fontSize: 12 }}
              >
                <RotateCcw size={13} className={actionLoading === "Restart Engine" ? "animate-spin" : ""} />
                Restart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}