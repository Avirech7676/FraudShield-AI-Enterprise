import type { PredictionPayload } from "../../types/prediction";

type Props = {
  payload: PredictionPayload;
  setPayload: React.Dispatch<React.SetStateAction<PredictionPayload>>;
};

export default function TransactionForm({ payload, setPayload }: Props) {
  function updateField(key: keyof PredictionPayload, value: unknown) {
    setPayload((prev) => ({ ...prev, [key]: value }));
  }

  return (
    <div className="fs-card" style={{ padding: 24, marginBottom: 20 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
        <h3 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>
          1. Transaction Parameters
        </h3>
        <span style={{ fontSize: 11, fontWeight: 700, color: "#818cf8", background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.25)", padding: "3px 10px", borderRadius: 20 }}>
          Step 1 of 4
        </span>
      </div>

      <div className="grid-3" style={{ marginBottom: 16 }}>
        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Amount ($)</label>
          <input
            type="number"
            className="fs-input"
            value={payload.Amount}
            onChange={(e) => updateField("Amount", Number(e.target.value))}
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Transaction Time (sec)</label>
          <input
            type="number"
            className="fs-input"
            value={payload.Time}
            onChange={(e) => updateField("Time", Number(e.target.value))}
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Currency</label>
          <select
            className="fs-input"
            value={payload.Currency}
            onChange={(e) => updateField("Currency", e.target.value)}
          >
            <option value="USD">USD ($)</option>
            <option value="INR">INR (₹)</option>
            <option value="EUR">EUR (€)</option>
            <option value="GBP">GBP (£)</option>
          </select>
        </div>
      </div>

      <div className="grid-3" style={{ marginBottom: 16 }}>
        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Merchant Name</label>
          <input
            type="text"
            className="fs-input"
            value={payload.Merchant}
            onChange={(e) => updateField("Merchant", e.target.value)}
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Merchant Category</label>
          <select
            className="fs-input"
            value={payload.Merchant_Category}
            onChange={(e) => updateField("Merchant_Category", e.target.value)}
          >
            <option>Retail</option>
            <option>Travel</option>
            <option>Food</option>
            <option>Electronics</option>
            <option>Healthcare</option>
            <option>Entertainment</option>
          </select>
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Merchant Country</label>
          <input
            type="text"
            className="fs-input"
            value={payload.Merchant_Country}
            onChange={(e) => updateField("Merchant_Country", e.target.value)}
          />
        </div>
      </div>

      <div className="grid-3" style={{ marginBottom: 20 }}>
        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Payment Type</label>
          <select
            className="fs-input"
            value={payload.Payment_Type}
            onChange={(e) => updateField("Payment_Type", e.target.value)}
          >
            <option>Credit Card</option>
            <option>Debit Card</option>
            <option>UPI</option>
            <option>Wallet</option>
            <option>Net Banking</option>
          </select>
        </div>
      </div>

      <div style={{ fontSize: 11, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 12, paddingTop: 12, borderTop: "1px solid rgba(255,255,255,0.05)" }}>
        Transaction Flags
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 16 }}>
        {[
          { label: "Card Present", key: "Card_Present" },
          { label: "Chip Used", key: "Chip_Used" },
          { label: "Contactless", key: "Contactless" },
          { label: "International", key: "International" },
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