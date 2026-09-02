import type { PredictionPayload } from "../../types/prediction";

type Props = {
  payload: PredictionPayload;
  setPayload: React.Dispatch<React.SetStateAction<PredictionPayload>>;
};

export default function CustomerForm({ payload, setPayload }: Props) {
  function updateField(key: keyof PredictionPayload, value: unknown) {
    setPayload((prev) => ({ ...prev, [key]: value }));
  }

  return (
    <div className="fs-card" style={{ padding: 24, marginBottom: 20 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
        <h3 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>
          2. Customer Profile
        </h3>
        <span style={{ fontSize: 11, fontWeight: 700, color: "#818cf8", background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.25)", padding: "3px 10px", borderRadius: 20 }}>
          Step 2 of 4
        </span>
      </div>

      <div className="grid-3" style={{ marginBottom: 16 }}>
        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Customer Age</label>
          <input
            type="number"
            className="fs-input"
            min={18}
            max={100}
            value={payload.Customer_Age}
            onChange={(e) => updateField("Customer_Age", Number(e.target.value))}
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Customer Segment</label>
          <select
            className="fs-input"
            value={payload.Customer_Segment}
            onChange={(e) => updateField("Customer_Segment", e.target.value)}
          >
            <option>Regular</option>
            <option>Premium</option>
            <option>Business</option>
            <option>VIP</option>
          </select>
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>KYC Level</label>
          <select
            className="fs-input"
            value={payload.KYC_Level}
            onChange={(e) => updateField("KYC_Level", e.target.value)}
          >
            <option>None</option>
            <option>Partial</option>
            <option>Full</option>
          </select>
        </div>
      </div>

      <div className="grid-3">
        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Customer Lifetime (Days)</label>
          <input
            type="number"
            className="fs-input"
            value={payload.Customer_Lifetime}
            onChange={(e) => updateField("Customer_Lifetime", Number(e.target.value))}
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Average Spend ($)</label>
          <input
            type="number"
            className="fs-input"
            value={payload.Avg_Spend}
            onChange={(e) => updateField("Avg_Spend", Number(e.target.value))}
          />
        </div>

        <div>
          <label style={{ display: "block", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>Credit Limit ($)</label>
          <input
            type="number"
            className="fs-input"
            value={payload.Credit_Limit}
            onChange={(e) => updateField("Credit_Limit", Number(e.target.value))}
          />
        </div>
      </div>
    </div>
  );
}