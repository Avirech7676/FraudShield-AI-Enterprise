import type { ModelInformation as ModelInfo } from "../../types/dashboard";

type Props = {
  model: ModelInfo;
};

export default function ModelInformation({ model }: Props) {
  const rows = [
    { label: "Version", value: model.version || "N/A" },
    { label: "Algorithm", value: model.algorithm || "N/A" },
    { label: "Accuracy", value: model.accuracy != null ? `${model.accuracy}%` : "N/A" },
    { label: "Precision", value: model.precision != null ? `${model.precision}%` : "N/A" },
    { label: "Recall", value: model.recall != null ? `${model.recall}%` : "N/A" },
    { label: "F1 Score", value: model.f1_score != null ? `${model.f1_score}%` : "N/A" },
    { label: "Production Model", value: model.production_model || "N/A" },
  ];

  return (
    <div className="card">
      <div className="card-header">
        <h3>Model Information</h3>
        <span className={`badge ${model.production_model ? "badge-success" : "badge-neutral"}`}>
          {model.production_model ? "Active" : "Inactive"}
        </span>
      </div>
      <div className="card-body">
        {rows.map((row) => (
          <div
            key={row.label}
            style={{
              display: "flex",
              justifyContent: "space-between",
              padding: "7px 0",
              borderBottom: "1px solid var(--border)",
              fontSize: 13,
            }}
          >
            <span style={{ color: "var(--text-muted)" }}>{row.label}</span>
            <span style={{ fontWeight: 500, color: "var(--text-strong)" }}>{row.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}