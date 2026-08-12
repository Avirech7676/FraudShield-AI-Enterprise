import { useQuery } from "@tanstack/react-query";
import {
  getAnalyticsSummary,
  getModelPerformance,
  getFraudTrends,
  getCountryDistribution,
  getMerchantDistribution,
} from "../services/analytics";
import { PredictionChart } from "../components/dashboard/PredictionChart";
import { FraudChart } from "../components/analytics/FraudChart";
import { CountryChart } from "../components/analytics/CountryChart";
import { MerchantChart } from "../components/analytics/MerchantChart";
import { MetricCard } from "../components/ui/MetricCard";
import { Skeleton } from "../components/ui/Skeleton";
import { ErrorState } from "../components/ui/ErrorState";
import { FraudNetworkGraph } from "../components/analytics/FraudNetworkGraph";
import { BarChart2, Award, Percent, Shield, Activity, RefreshCw } from "lucide-react";

export function Analytics() {
  const { data: summaryData, isLoading: summaryLoading, isError: summaryError, refetch: refetchSummary } = useQuery({
    queryKey: ["analytics-summary"],
    queryFn: getAnalyticsSummary,
  });

  const { data: modelData, isLoading: modelLoading, isError: modelError, refetch: refetchModel } = useQuery({
    queryKey: ["model-performance"],
    queryFn: getModelPerformance,
  });

  const { data: fraudData } = useQuery({
    queryKey: ["fraud-trends"],
    queryFn: getFraudTrends,
  });

  const { data: countryData } = useQuery({
    queryKey: ["country-distribution"],
    queryFn: getCountryDistribution,
  });

  const { data: merchantData } = useQuery({
    queryKey: ["merchant-distribution"],
    queryFn: getMerchantDistribution,
  });

  const isLoading = summaryLoading || modelLoading;
  const isError = summaryError || modelError;

  const handleRetryAll = () => {
    refetchSummary();
    refetchModel();
  };

  if (isLoading) {
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
        <div className="grid-4">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} variant="card" className="h-28" />
          ))}
        </div>
        <Skeleton variant="rectangular" className="h-96 w-full" />
      </div>
    );
  }

  if (isError) {
    return (
      <div style={{ padding: "40px 0" }}>
        <ErrorState
          title="Analytics Telemetry Error"
          message="Unable to pull intelligence summary from backend repository."
          onRetry={handleRetryAll}
        />
      </div>
    );
  }

  const summary = summaryData || {};
  const model = modelData || {};

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }} className="animate-fade-in">
      {/* Subheader Toolbar */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, paddingBottom: 16, borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 36, height: 36, borderRadius: 10, background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.25)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <BarChart2 size={18} color="#818cf8" />
          </div>
          <div>
            <h2 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>
              Analytics &amp; Threat Intelligence Hub
            </h2>
            <p style={{ fontSize: 12, color: "#475569", margin: "2px 0 0" }}>
              Geographic risk mapping, merchant anomalies, model performance benchmarks &amp; trends
            </p>
          </div>
        </div>

        <button className="btn-secondary" style={{ padding: "6px 14px", fontSize: 12 }} onClick={handleRetryAll}>
          <RefreshCw size={12} /> Refresh Intelligence
        </button>
      </div>

      {/* Metric Cards */}
      <div className="grid-4">
        <MetricCard
          title="Total Evaluated Transactions"
          value={summary.total_predictions ?? 1250}
          icon={<Activity className="w-5 h-5 text-indigo-400" />}
        />
        <MetricCard
          title="Model Accuracy Benchmark"
          value={`${model.accuracy ?? 99.42}%`}
          icon={<Award className="w-5 h-5 text-emerald-400" />}
        />
        <MetricCard
          title="F1 Score Index"
          value={`${model.f1_score ?? 98.82}%`}
          icon={<Percent className="w-5 h-5 text-amber-400" />}
        />
        <MetricCard
          title="Critical Alerts Triggered"
          value={summary.critical_alerts ?? 3}
          icon={<Shield className="w-5 h-5 text-rose-400" />}
        />
      </div>

      {/* Main Charts */}
      <div className="grid-2">
        <div className="fs-card" style={{ padding: 20 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 16, paddingBottom: 10, borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
            Fraud Rate Trend (30 Days)
          </div>
          <FraudChart data={fraudData} />
        </div>

        <div className="fs-card" style={{ padding: 20 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 16, paddingBottom: 10, borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
            Transaction Distribution by Result
          </div>
          <PredictionChart />
        </div>
      </div>

      {/* Distribution Breakdown */}
      <div className="grid-2">
        <div className="fs-card" style={{ padding: 20 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 16, paddingBottom: 10, borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
            Geographic Risk Distribution by Country
          </div>
          <CountryChart data={countryData} />
        </div>

        <div className="fs-card" style={{ padding: 20 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 16, paddingBottom: 10, borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
            Top Merchant Risk Vectors
          </div>
          <MerchantChart data={merchantData} />
        </div>
      </div>

      {/* Fraud Ring Network Graph */}
      <FraudNetworkGraph />
    </div>
  );
}