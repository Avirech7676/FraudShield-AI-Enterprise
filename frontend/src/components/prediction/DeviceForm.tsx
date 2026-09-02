import type { PredictionPayload } from "../../types/prediction";

type Props = {
  payload: PredictionPayload;
  setPayload: React.Dispatch<React.SetStateAction<PredictionPayload>>;
};

export default function DeviceForm({ payload, setPayload }: Props) {
  function updateField(key: keyof PredictionPayload, value: unknown) {
    setPayload((prev) => ({ ...prev, [key]: value }));
  }

  return (
    <div className="fs-card" style={{ padding: 24, marginBottom: 20 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
        <h3 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>
          3. Device &amp; Security Fingerprint
        </h3>
        <span style={{ fontSize: 11, fontWeight: 700, color: "#818cf8", background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.25)", padding: "3px 10px", borderRadius: 20 }}>
          Step 3 of 4
        </span>
      </div>

      <div className="grid-3" style={{ marginBottom: 16 }}>
        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Device Fingerprint ID</label>
          <input
            type="text"
            className="fs-input"
            value={payload.Device_Fingerprint}
            onChange={(e) => updateField("Device_Fingerprint", e.target.value)}
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Browser Agent</label>
          <select
            className="fs-input"
            value={payload.Browser}
            onChange={(e) => updateField("Browser", e.target.value)}
          >
            <option>Chrome</option>
            <option>Firefox</option>
            <option>Edge</option>
            <option>Safari</option>
            <option>Opera</option>
          </select>
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Operating System</label>
          <select
            className="fs-input"
            value={payload.Operating_System}
            onChange={(e) => updateField("Operating_System", e.target.value)}
          >
            <option>Windows</option>
            <option>Linux</option>
            <option>Android</option>
            <option>iOS</option>
            <option>macOS</option>
          </select>
        </div>
      </div>

      <div className="grid-3" style={{ marginBottom: 20 }}>
        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Device Trust Score (0-100)</label>
          <input
            type="number"
            className="fs-input"
            min={0}
            max={100}
            value={payload.Device_Trust_Score}
            onChange={(e) => updateField("Device_Trust_Score", Number(e.target.value))}
          />
        </div>
      </div>

      <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 12, paddingTop: 12, borderTop: "1px solid rgba(255,255,255,0.05)" }}>
        Security Flags
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 16 }}>
        {[
          { label: "VPN Detected", key: "VPN_Detection" },
          { label: "TOR Network", key: "TOR_Detection" },
          { label: "Emulator", key: "Emulator_Detection" },
          { label: "Rooted Device", key: "Rooted_Device" },
          { label: "Jailbreak", key: "Jailbreak_Detection" },
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