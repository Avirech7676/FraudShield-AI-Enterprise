import type { PredictionResponse } from "../../types/prediction";
import { useNavigate } from "react-router-dom";
import { Card, CardHeader, CardTitle, CardContent } from "../ui/Card";
import { RiskBadge } from "../ui/RiskBadge";
import { Badge } from "../ui/Badge";
import { Button } from "../ui/Button";
import { ShieldAlert, ShieldCheck, Zap, ArrowRight, Activity } from "lucide-react";

type Props = {
  result: PredictionResponse | null;
};

export default function PredictionResult({ result }: Props) {
  const navigate = useNavigate();

  if (!result) return null;

  const prediction = result.prediction;
  const risk = result.risk_analysis;
  const components = risk?.Components;

  const hybridScore = risk?.["Risk Score"] ?? prediction?.Risk_Score ?? 0;
  const hybridTier = risk?.["Risk Tier"] ?? prediction?.Risk_Tier ?? "Unknown";
  const isFraud = prediction?.Prediction?.toLowerCase() === "fraud" || hybridScore >= 50 || ["high", "critical"].includes(hybridTier.toLowerCase());
  const probability = (components?.["ML Probability"] ?? (prediction?.Fraud_Probability ? prediction.Fraud_Probability * 100 : 0));
  const riskScore = hybridScore;
  const latency = prediction?.Latency_ms ?? 0;
  const tier = hybridTier;
  const priority = risk?.Priority ?? "N/A";
  const action = risk?.Recommended_Action ?? risk?.["Recommended Action"] ?? "N/A";

  return (
    <div className="mt-8 space-y-6 animate-in fade-in duration-300">
      {/* Risk Alert Banner */}
      <div
        className={`p-6 rounded-2xl border backdrop-blur-xl flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xl ${
          isFraud
            ? "bg-rose-950/40 border-rose-500/50 shadow-rose-950/40"
            : "bg-emerald-950/40 border-emerald-500/50 shadow-emerald-950/40"
        }`}
      >
        <div className="flex items-start gap-4">
          <div
            className={`p-3.5 rounded-2xl ${
              isFraud
                ? "bg-rose-500/20 text-rose-400 border border-rose-500/30"
                : "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
            }`}
          >
            {isFraud ? <ShieldAlert className="w-8 h-8" /> : <ShieldCheck className="w-8 h-8" />}
          </div>
          <div>
            <h3 className="text-xl font-bold tracking-tight text-white">
              {isFraud ? "CRITICAL THREAT DETECTED" : "TRANSACTION PASSED VALIDATION"}
            </h3>
            <p className="text-xs text-slate-300 mt-1 max-w-md">
              {isFraud
                ? "This transaction shows elevated fraud risk indicators and triggers protective hold procedures."
                : "Standard risk parameters satisfied. No suspicious behavioral anomalies detected."}
            </p>
          </div>
        </div>

        <div className="flex flex-col items-end border-t md:border-t-0 md:border-l border-slate-700/50 pt-3 md:pt-0 md:pl-6">
          <div className="text-3xl font-bold font-mono text-white tracking-tight">
            {probability.toFixed(1)}%
          </div>
          <span className="text-[11px] font-semibold tracking-wider text-slate-400 uppercase">
            Fraud Probability
          </span>
        </div>
      </div>

      {/* Metric Breakdown Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Card variant="glass" className="p-4 flex flex-col justify-between">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Risk Score
          </span>
          <span className="text-2xl font-bold font-mono text-slate-100 mt-2">
            {riskScore} / 100
          </span>
        </Card>

        <Card variant="glass" className="p-4 flex flex-col justify-between">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Risk Tier
          </span>
          <div className="mt-2">
            <RiskBadge level={tier} score={probability / 100} size="sm" />
          </div>
        </Card>

        <Card variant="glass" className="p-4 flex flex-col justify-between">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Priority
          </span>
          <span className="text-sm font-semibold text-indigo-300 mt-2 uppercase tracking-wider">
            {priority}
          </span>
        </Card>

        <Card variant="glass" className="p-4 flex flex-col justify-between">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1">
            <Zap className="w-3.5 h-3.5 text-amber-400" />
            Inference Latency
          </span>
          <span className="text-2xl font-bold font-mono text-slate-100 mt-2">
            {latency} ms
          </span>
        </Card>
      </div>

      {/* Recommended Action Card */}
      <Card variant="glass">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-indigo-400" />
            Recommended Intervention
          </CardTitle>
          <Badge variant={isFraud ? "rose" : "emerald"} size="sm">
            {action}
          </Badge>
        </CardHeader>
        <CardContent className="space-y-4">
          {components && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                  ML Ensemble Probability
                </span>
                <span className="text-lg font-bold font-mono text-indigo-300 mt-1 block">
                  {((components ? (components["ML Probability"] ?? (probability * 100)) : (probability * 100))).toFixed(1)}%
                </span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                  Rule Engine Score
                </span>
                <span className="text-lg font-bold font-mono text-indigo-300 mt-1 block">
                  {components["Rule Engine"] || 0}
                </span>
              </div>
              <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                  Behavior Engine Score
                </span>
                <span className="text-lg font-bold font-mono text-indigo-300 mt-1 block">
                  {components["Behavior Engine"] || 0}
                </span>
              </div>
            </div>
          )}

          {result.transaction_id && (
            <div className="pt-4 border-t border-slate-800/80 flex flex-col sm:flex-row items-center justify-between gap-3">
              <div>
                <span className="text-xs text-slate-400 block">Evaluated Transaction ID</span>
                <span className="text-sm font-mono font-bold text-indigo-400">
                  {result.transaction_id}
                </span>
              </div>
              <Button
                variant="primary"
                size="sm"
                rightIcon={<ArrowRight className="w-4 h-4" />}
                onClick={() => navigate(`/explanation/${result.transaction_id}`)}
              >
                Inspect SHAP Feature Waterfall
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}