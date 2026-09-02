import React, { useState } from "react";
import TransactionForm from "../components/prediction/TransactionForm";
import CustomerForm from "../components/prediction/CustomerForm";
import DeviceForm from "../components/prediction/DeviceForm";
import BehaviourForm from "../components/prediction/BehaviourForm";
import PredictionResult from "../components/prediction/PredictionResult";
import { defaultPrediction } from "../types/prediction";

import type { PredictionPayload, PredictionResponse } from "../types/prediction";
import { predict } from "../services/prediction";
import { Button } from "../components/ui/Button";
import { ErrorState } from "../components/ui/ErrorState";
import { Spinner } from "../components/ui/Spinner";
import { Play, RotateCcw, ShieldCheck } from "lucide-react";

export default function PredictionPage() {
  const [payload, setPayload] = useState<PredictionPayload>(defaultPrediction);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await predict(payload);
      setResult(response);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Prediction failed. Please check network backend connection.");
      }
    } finally {
      setLoading(false);
    }
  }

  function resetForm() {
    setPayload(defaultPrediction);
    setResult(null);
    setError("");
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }} className="animate-fade-in">
      {/* Subheader */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, paddingBottom: 16, borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 36, height: 36, borderRadius: 10, background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.25)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <ShieldCheck size={18} color="#818cf8" />
          </div>
          <div>
            <h2 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>
              Transaction Evaluation Engine
            </h2>
            <p style={{ fontSize: 12, color: "#475569", margin: "2px 0 0" }}>
              Submit payload features for instant multi-layer ML & rule-based fraud classification
            </p>
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <TransactionForm payload={payload} setPayload={setPayload} />
        <CustomerForm payload={payload} setPayload={setPayload} />
        <DeviceForm payload={payload} setPayload={setPayload} />
        <BehaviourForm payload={payload} setPayload={setPayload} />

        <div style={{ display: "flex", alignItems: "center", gap: 16, paddingTop: 16, borderTop: "1px solid rgba(255,255,255,0.06)" }}>
          <button
            type="submit"
            className="btn-primary"
            disabled={loading}
            style={{ padding: "12px 24px", fontSize: 15 }}
          >
            {loading ? (
              <>
                <span className="animate-spin" style={{ width: 16, height: 16, border: "2px solid rgba(255,255,255,0.3)", borderTopColor: "#fff", borderRadius: "50%", display: "inline-block" }} />
                Evaluating Payload...
              </>
            ) : (
              <>
                <Play size={16} />
                Run Fraud Evaluation
              </>
            )}
          </button>

          <Button
            type="button"
            variant="secondary"
            size="lg"
            leftIcon={<RotateCcw className="w-4 h-4" />}
            onClick={resetForm}
          >
            Reset Payload Defaults
          </Button>
        </div>
      </form>

      {error && (
        <ErrorState
          title="Prediction Engine Error"
          message={error}
          onRetry={handleSubmit as any}
        />
      )}

      {loading && (
        <div className="fs-card" style={{ padding: 40, textAlign: "center" }}>
          <Spinner size="lg" color="primary" className="mb-4" />
          <h3 style={{ fontSize: 16, fontWeight: 600, color: "#f1f5f9" }}>
            Running CatBoost Ensemble & Rule Matrix...
          </h3>
          <p style={{ fontSize: 13, color: "#64748b", marginTop: 4 }}>
            Evaluating 28 feature metrics against trained decision boundaries
          </p>
        </div>
      )}

      {result && <PredictionResult result={result} />}
    </div>
  );
}