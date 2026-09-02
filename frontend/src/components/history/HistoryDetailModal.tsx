import type { PredictionHistory } from "../../types/history";
import { useNavigate } from "react-router-dom";

type Props = {
  prediction: PredictionHistory | null;
  onClose: () => void;
};

export default function HistoryDetailModal({ prediction, onClose }: Props) {
  const navigate = useNavigate();

  if (!prediction) return null;

  const isFraud = prediction.prediction === "Fraud";
  const rawProb = typeof prediction.fraud_probability === "number" ? prediction.fraud_probability : parseFloat(prediction.fraud_probability as any) || 0;
  const probVal = rawProb * (rawProb <= 1 ? 100 : 1);
  const confidence = Math.abs(probVal - 50) * 2;
  const latency = typeof prediction.Latency_ms === "number" ? prediction.Latency_ms : parseFloat(prediction.Latency_ms as any) || 0;

  const details = [
    { label: "Transaction ID", value: prediction.transaction_id },
    { label: "Customer ID", value: prediction.customer_id || "-" },
    { label: "Prediction", value: prediction.prediction },
    { label: "Fraud Probability", value: `${probVal.toFixed(1)}%` },
    { label: "Confidence", value: `${confidence.toFixed(1)}%` },
    { label: "Risk Score", value: String(prediction.risk_score || 0) },
    { label: "Risk Tier", value: prediction.risk_tier || "N/A" },
    { label: "Merchant", value: prediction.merchant || "-" },
    { label: "Country", value: prediction.country || "-" },
    { label: "Latency", value: `${latency.toFixed(2)} ms` },
    { label: "Created", value: prediction.created_at ? new Date(prediction.created_at).toLocaleString() : "Just now" },
  ];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Prediction Details</h3>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        <div className="modal-body">
          <div className="result-banner" style={{ marginBottom: 16, ...(isFraud ? {
            background: "var(--red-light)",
            border: "1px solid rgba(193, 66, 74, 0.2)",
            padding: "12px 16px",
            borderRadius: "var(--radius-md)",
          } : {
            background: "var(--green-light)",
            border: "1px solid rgba(45, 125, 90, 0.2)",
            padding: "12px 16px",
            borderRadius: "var(--radius-md)",
          })} as React.CSSProperties}>
            <div style={{ fontSize: 16, fontWeight: 700, color: "var(--text-strong)" }}>
              <span className={`badge ${isFraud ? "badge-danger" : "badge-success"}`}>
                {prediction.prediction}
              </span>
            </div>
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
            {details.slice(1).map((d) => (
              <div key={d.label} style={{ fontSize: 13 }}>
                <div style={{ color: "var(--text-muted)", fontSize: 11, marginBottom: 2 }}>{d.label}</div>
                <div style={{ fontWeight: 500, color: "var(--text-strong)" }}>{d.value}</div>
              </div>
            ))}
          </div>

          {prediction.llm_explanation && (
            <div style={{ marginTop: 16, padding: 12, background: "var(--bg-alt)", borderRadius: "var(--radius-sm)" }}>
              <div style={{ fontSize: 11, fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", marginBottom: 4 }}>
                Analysis
              </div>
              <p style={{ margin: 0, fontSize: 13, lineHeight: 1.6 }}>{prediction.llm_explanation}</p>
            </div>
          )}
        </div>
        <div className="modal-footer">
          <button className="btn" onClick={onClose}>Close</button>
          <button
            className="btn btn-primary"
            onClick={() => navigate(`/explanation/${prediction.transaction_id}`)}
          >
            View Full Explanation
          </button>
        </div>
      </div>
    </div>
  );
}