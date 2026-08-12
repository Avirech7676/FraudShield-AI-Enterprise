import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getTransactionExplanation, getFeatureExplanation, type ExplanationResult } from "../services/explanation";
import { ShieldCheck, ShieldAlert, Cpu, Sparkles, ArrowLeft, Sliders, RefreshCw } from "lucide-react";
import { Badge } from "../components/ui/Badge";
import { Skeleton } from "../components/ui/Skeleton";
import { ErrorState } from "../components/ui/ErrorState";

export default function Explanation() {
  const { transactionId } = useParams<{ transactionId: string }>();
  const navigate = useNavigate();

  const [explanation, setExplanation] = useState<ExplanationResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [manualInput, setManualInput] = useState<boolean>(false);
  const [manualFeatures, setManualFeatures] = useState<Record<string, any>>({
    amount: 5500.0,
    merchant_category: "Crypto Exchange",
    hour: 14,
    device_trust: 35.0,
    ip_reputation: 80.0,
    velocity: 6.0,
    location_jump: true,
    vpn_detected: true,
  });

  useEffect(() => {
    if (transactionId) {
      loadTransactionExplanation();
    } else {
      loadFeatureExplanation();
    }
  }, [transactionId]);

  const loadTransactionExplanation = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await getTransactionExplanation(transactionId!);
      setExplanation(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load explanation for transaction.");
    } finally {
      setLoading(false);
    }
  };

  const loadFeatureExplanation = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await getFeatureExplanation(manualFeatures);
      setExplanation(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate feature explanation.");
    } finally {
      setLoading(false);
    }
  };

  if (loading && !explanation) {
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
        <Skeleton variant="rectangular" className="h-40 w-full" />
        <Skeleton variant="rectangular" className="h-96 w-full" />
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: "40px 0" }}>
        <ErrorState
          title="SHAP Explainability Error"
          message={error}
          onRetry={() => (transactionId ? loadTransactionExplanation() : loadFeatureExplanation())}
        />
      </div>
    );
  }

  const isFraud = Boolean(explanation?.is_fraud);
  const rawProb = typeof explanation?.fraud_probability === "number" ? explanation.fraud_probability : parseFloat(explanation?.fraud_probability as any) || 0;
  const prob = rawProb * (rawProb <= 1 ? 100 : 1);
  const rawConf = typeof explanation?.confidence === "number" ? explanation.confidence : parseFloat(explanation?.confidence as any) || 0;
  const conf = rawConf * (rawConf <= 1 ? 100 : 1);

  const rawShap = explanation?.shap_values || (explanation as any)?.top_factors || {};
  let shapEntries: [string, number][] = [];

  if (Array.isArray(rawShap)) {
    shapEntries = rawShap.map((item: any) => [
      String(item.feature || item.name || item.description || "Feature"),
      typeof item.impact === "number" ? item.impact : (typeof item.value === "number" ? item.value : parseFloat(item.impact || item.value || 0))
    ]);
  } else if (typeof rawShap === "object" && rawShap !== null) {
    shapEntries = Object.entries(rawShap).map(([key, val]) => [
      key,
      typeof val === "number" ? val : parseFloat(val as any) || 0
    ]);
  }

  shapEntries.sort(([, a], [, b]) => Math.abs(b) - Math.abs(a));

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }} className="animate-fade-in">
      {/* Subheader Toolbar */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, paddingBottom: 16, borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <button
            onClick={() => navigate(-1)}
            style={{ width: 34, height: 34, borderRadius: 8, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)", color: "#94a3b8", display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer" }}
          >
            <ArrowLeft size={16} />
          </button>
          <div>
            <h2 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>
              AI SHAP Explainability &amp; What-If Counterfactual Simulator
            </h2>
            <p style={{ fontSize: 12, color: "#475569", margin: "2px 0 0" }}>
              {transactionId ? `Target Transaction: ${transactionId}` : "Interactive Risk Vector Simulation & Feature Attribution"}
            </p>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <button
            className={`btn-secondary${!manualInput ? " active" : ""}`}
            style={{ padding: "6px 14px", fontSize: 12 }}
            onClick={() => setManualInput(false)}
          >
            Transaction Lookup
          </button>
          <button
            className={`btn-secondary${manualInput ? " active" : ""}`}
            style={{ padding: "6px 14px", fontSize: 12 }}
            onClick={() => setManualInput(true)}
          >
            <Sliders size={13} /> Interactive What-If Simulator
          </button>
        </div>
      </div>

      {/* Interactive What-If Simulator Form */}
      {manualInput && (
        <div className="fs-card" style={{ padding: 24 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 15, fontWeight: 700, color: "#f1f5f9", marginBottom: 16 }}>
            <Sliders size={18} color="#818cf8" />
            Interactive Counterfactual Feature Sliders
          </div>
          <div className="grid-3" style={{ gap: 20, marginBottom: 20 }}>
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>
                <span>Transaction Amount ($)</span>
                <span style={{ color: "#818cf8", fontFamily: "var(--font-mono)" }}>${manualFeatures.amount}</span>
              </div>
              <input
                type="range"
                min="10"
                max="25000"
                step="100"
                style={{ width: "100%", accentColor: "#6366f1" }}
                value={manualFeatures.amount || 100}
                onChange={(e) => setManualFeatures(p => ({ ...p, amount: parseFloat(e.target.value) || 0 }))}
              />
            </div>

            <div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>
                <span>Device Trust Score (0-100)</span>
                <span style={{ color: "#818cf8", fontFamily: "var(--font-mono)" }}>{manualFeatures.device_trust}</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                style={{ width: "100%", accentColor: "#6366f1" }}
                value={manualFeatures.device_trust || 0}
                onChange={(e) => setManualFeatures(p => ({ ...p, device_trust: parseFloat(e.target.value) || 0 }))}
              />
            </div>

            <div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, fontWeight: 600, color: "#94a3b8", marginBottom: 6 }}>
                <span>IP Anomaly Score (0-100)</span>
                <span style={{ color: "#818cf8", fontFamily: "var(--font-mono)" }}>{manualFeatures.ip_reputation}</span>
              </div>
              <input
                type="range"
                min="0"
                max="100"
                style={{ width: "100%", accentColor: "#6366f1" }}
                value={manualFeatures.ip_reputation || 0}
                onChange={(e) => setManualFeatures(p => ({ ...p, ip_reputation: parseFloat(e.target.value) || 0 }))}
              />
            </div>
          </div>

          <div style={{ display: "flex", gap: 12 }}>
            <button className="btn-primary" onClick={loadFeatureExplanation} disabled={loading} style={{ padding: "9px 20px", fontSize: 13 }}>
              <Sparkles size={14} /> Recalculate Risk &amp; SHAP Vectors
            </button>
          </div>
        </div>
      )}

      {/* Result Card */}
      {explanation && (
        <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
          {/* Header Banner */}
          <div
            className="fs-card"
            style={{
              padding: 24,
              background: isFraud
                ? "linear-gradient(135deg, rgba(244,63,94,0.15) 0%, rgba(2,4,10,0.8) 100%)"
                : "linear-gradient(135deg, rgba(16,185,129,0.15) 0%, rgba(2,4,10,0.8) 100%)",
              border: isFraud ? "1px solid rgba(244,63,94,0.3)" : "1px solid rgba(16,185,129,0.3)",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: 20,
              flexWrap: "wrap",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
              <div style={{ width: 48, height: 48, borderRadius: 14, background: isFraud ? "rgba(244,63,94,0.2)" : "rgba(16,185,129,0.2)", border: isFraud ? "1px solid rgba(244,63,94,0.4)" : "1px solid rgba(16,185,129,0.4)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                {isFraud ? <ShieldAlert size={24} color="#f43f5e" /> : <ShieldCheck size={24} color="#10b981" />}
              </div>
              <div>
                <div style={{ fontSize: 18, fontWeight: 800, color: "#f1f5f9", letterSpacing: "-0.02em" }}>
                  {isFraud ? "ELEVATED FRAUD RISK VECTOR" : "AUTHENTICATED SAFE TRANSACTION"}
                </div>
                <div style={{ fontSize: 13, color: "#94a3b8", marginTop: 2 }}>
                  Classification: <span style={{ marginLeft: 6 }}><Badge variant={isFraud ? "rose" : "emerald"} size="sm">{isFraud ? "FRAUD" : "GENUINE"}</Badge></span>
                </div>
              </div>
            </div>

            <div style={{ display: "flex", gap: 24, textAlign: "right" }}>
              <div>
                <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.06em" }}>Fraud Probability</div>
                <div style={{ fontSize: 26, fontWeight: 800, color: isFraud ? "#fb7185" : "#34d399", fontFamily: "var(--font-mono)" }}>
                  {prob.toFixed(1)}%
                </div>
              </div>
              <div>
                <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.06em" }}>Model Confidence</div>
                <div style={{ fontSize: 26, fontWeight: 800, color: "#818cf8", fontFamily: "var(--font-mono)" }}>
                  {conf.toFixed(1)}%
                </div>
              </div>
            </div>
          </div>

          {/* Natural Language Explanation Brief */}
          <div className="fs-card" style={{ padding: 24 }}>
            <div style={{ fontSize: 14, fontWeight: 700, color: "#f1f5f9", marginBottom: 12, display: "flex", alignItems: "center", gap: 8 }}>
              <Cpu size={16} color="#818cf8" /> Groq LLM Synthesized Risk Summary
            </div>
            <div style={{ fontSize: 14, color: "#cbd5e1", lineHeight: 1.7, padding: 16, borderRadius: 10, background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)" }}>
              {explanation.explanation}
            </div>
          </div>

          {/* Counterfactual Guidance */}
          {explanation.counterfactual && Object.keys(explanation.counterfactual).length > 0 && (
            <div className="fs-card" style={{ padding: 20, borderLeft: "4px solid #6366f1" }}>
              <div style={{ fontSize: 14, fontWeight: 700, color: "#818cf8", marginBottom: 8, display: "flex", alignItems: "center", gap: 6 }}>
                <RefreshCw size={15} /> Counterfactual Recourse Recommendation
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: 12 }}>
                {Object.entries(explanation.counterfactual).map(([k, v]) => (
                  <div key={k} style={{ padding: 10, borderRadius: 8, background: "rgba(0,0,0,0.3)", border: "1px solid rgba(255,255,255,0.05)", fontSize: 12, color: "#cbd5e1" }}>
                    <span style={{ color: "#a5b4fc", fontWeight: 600 }}>{k}:</span> {String(v)}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* SHAP Waterfall Feature Table */}
          <div className="fs-card" style={{ padding: 24 }}>
            <div style={{ fontSize: 14, fontWeight: 700, color: "#f1f5f9", marginBottom: 16 }}>
              Top Feature Contributions (SHAP Values)
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
              {shapEntries.slice(0, 10).map(([feature, val]) => {
                const isPositive = val > 0;
                const absVal = Math.abs(val);
                const barWidth = Math.min(100, Math.max(8, absVal * 300));

                return (
                  <div key={feature} style={{ display: "flex", alignItems: "center", gap: 16, padding: "8px 12px", borderRadius: 8, background: "rgba(255,255,255,0.02)" }}>
                    <div style={{ width: 200, fontSize: 13, fontWeight: 500, color: "#e2e8f0", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                      {feature}
                    </div>
                    <div style={{ flex: 1, display: "flex", alignItems: "center" }}>
                      <div
                        style={{
                          height: 8,
                          width: `${barWidth}%`,
                          borderRadius: 4,
                          background: isPositive ? "linear-gradient(90deg, #f43f5e, #fb7185)" : "linear-gradient(90deg, #10b981, #34d399)",
                          transition: "width 0.6s ease",
                        }}
                      />
                    </div>
                    <div style={{ width: 80, textAlign: "right", fontFamily: "var(--font-mono)", fontSize: 12, fontWeight: 700, color: isPositive ? "#fb7185" : "#34d399" }}>
                      {isPositive ? "+" : ""}{(Number(val) || 0).toFixed(4)}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}