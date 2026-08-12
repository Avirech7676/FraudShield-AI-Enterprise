import type { HealthResponse } from "../../types/dashboard";

type Props = {
  health: HealthResponse;
};

function StatusIndicator({ value }: { value: boolean }) {
  return (
    <span className={`badge ${value ? "badge-success" : "badge-danger"}`}>
      {value ? "Healthy" : "Offline"}
    </span>
  );
}

export default function SystemStatus({ health }: Props) {
  const rows = [
    { label: "API Status", value: <span className={`badge ${health.status === "healthy" ? "badge-success" : "badge-danger"}`}>{health.status}</span> },
    { label: "Database", value: <StatusIndicator value={health.database} /> },
    { label: "Prediction Engine", value: <StatusIndicator value={health.prediction_engine?.ready} /> },
    { label: "Model Loaded", value: <StatusIndicator value={health.prediction_engine?.model_loaded} /> },
    { label: "Preprocessor", value: <StatusIndicator value={health.prediction_engine?.preprocessor_loaded} /> },
    { label: "Model Version", value: <span style={{ fontWeight: 500 }}>{health.prediction_engine?.version || "N/A"}</span> },
    { label: "API Version", value: <span style={{ fontWeight: 500 }}>{health.version}</span> },
  ];

  return (
    <div className="card">
      <div className="card-header">
        <h3>System Status</h3>
        <span className={`badge ${health.status === "healthy" ? "badge-success" : "badge-danger"}`}>
          {health.status === "healthy" ? "All Systems Go" : "Issues Detected"}
        </span>
      </div>
      <div className="card-body">
        {rows.map((row) => (
          <div
            key={row.label}
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              padding: "7px 0",
              borderBottom: "1px solid var(--border)",
              fontSize: 13,
            }}
          >
            <span style={{ color: "var(--text-muted)" }}>{row.label}</span>
            <span>{row.value}</span>
          </div>
        ))}
        <div style={{ fontSize: 12, color: "var(--text-faint)", marginTop: 10 }}>
          Last checked: {new Date(health.timestamp).toLocaleString()}
        </div>
      </div>
    </div>
  );
}