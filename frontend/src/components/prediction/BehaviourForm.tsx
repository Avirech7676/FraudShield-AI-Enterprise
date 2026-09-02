import type { PredictionPayload } from "../../types/prediction";

type Props = {
  payload: PredictionPayload;
  setPayload: React.Dispatch<React.SetStateAction<PredictionPayload>>;
};

export default function BehaviourForm({ payload, setPayload }: Props) {
  function updateField(key: keyof PredictionPayload, value: unknown) {
    setPayload((prev) => ({ ...prev, [key]: value }));
  }

  return (
    <div className="fs-card" style={{ padding: 24, marginBottom: 20 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
        <h3 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>
          4. Behavioral Telemetry &amp; Velocity
        </h3>
        <span style={{ fontSize: 11, fontWeight: 700, color: "#818cf8", background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.25)", padding: "3px 10px", borderRadius: 20 }}>
          Step 4 of 4
        </span>
      </div>

      <div className="grid-3" style={{ marginBottom: 16 }}>
        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Velocity Score (0-100)</label>
          <input
            type="number"
            className="fs-input"
            min={0}
            max={100}
            value={payload.Velocity}
            onChange={(e) => updateField("Velocity", Number(e.target.value))}
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Previous Fraud Count</label>
          <input
            type="number"
            className="fs-input"
            min={0}
            value={payload.Previous_Fraud}
            onChange={(e) => updateField("Previous_Fraud", Number(e.target.value))}
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Merchant Risk Index (0-100)</label>
          <input
            type="number"
            className="fs-input"
            min={0}
            max={100}
            value={payload.Merchant_Risk}
            onChange={(e) => updateField("Merchant_Risk", Number(e.target.value))}
          />
        </div>
      </div>

      <div className="grid-3" style={{ marginBottom: 20 }}>
        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Transactions Last Hour</label>
          <input
            type="number"
            className="fs-input"
            min={0}
            value={payload.Transactions_Last_Hour}
            onChange={(e) => updateField("Transactions_Last_Hour", Number(e.target.value))}
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Transactions Last Day</label>
          <input
            type="number"
            className="fs-input"
            min={0}
            value={payload.Transactions_Last_Day}
            onChange={(e) => updateField("Transactions_Last_Day", Number(e.target.value))}
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Login Failure Count</label>
          <input
            type="number"
            className="fs-input"
            min={0}
            value={payload.Login_Failure_Count}
            onChange={(e) => updateField("Login_Failure_Count", Number(e.target.value))}
          />
        </div>
      </div>

      <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 12, paddingTop: 12, borderTop: "1px solid rgba(255,255,255,0.05)" }}>
        Behavioral Flags
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 16 }}>
        {[
          { label: "Location Jump", key: "Location_Jump" },
          { label: "Device Changed", key: "Device_Change" },
          { label: "Password Reset", key: "Password_Reset" },
        ].map((flag) => (
          <label key={flag.key} style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 13, color: "#cbd5e1", cursor: "pointer", padding: "6px 12px", borderRadius: 8, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}>
            <input
              type="checkbox"
              checked={Boolean(payload[flag.key as keyof PredictionPayload])}
              onChange={(e) => updateField(flag.key as keyof PredictionPayload, e.target.checked)}
              style={{ accentColor: "#6366f1" }}
            />
            {flag.label}
          </label>
        ))}
      </div>
    </div>
  );
}