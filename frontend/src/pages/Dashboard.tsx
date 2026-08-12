import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { RefreshCw, Clock, Shield, AlertTriangle, Activity } from "lucide-react";

import { getDashboardSummary } from "../services/dashboard";
import { getHealth } from "../services/health";
import { KpiCards } from "../components/dashboard/KpiCards";
import { PredictionChart } from "../components/dashboard/PredictionChart";
import { RiskChart } from "../components/dashboard/RiskChart";
import RecentPredictionsTable from "../components/dashboard/RecentPredictionsTable";
import ModelInformation from "../components/dashboard/ModelInformation";
import SystemStatus from "../components/dashboard/SystemStatus";
import { BarChartComponent } from "../components/dashboard/BarChart";
import { AreaChartComponent } from "../components/dashboard/AreaChart";
import { RadarChartComponent } from "../components/dashboard/RadarChart";
import { TreemapChartComponent } from "../components/dashboard/TreemapChart";
import { ActivityTimeline } from "../components/dashboard/ActivityTimeline";

/* ── Skeleton Cards ── */
function DashboardSkeleton() {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
      <div className="grid-4">
        {[0, 1, 2, 3].map(i => (
          <div key={i} className="skeleton" style={{ height: 120, borderRadius: 14 }} />
        ))}
      </div>
      <div className="skeleton" style={{ height: 320, borderRadius: 14 }} />
      <div className="grid-2">
        <div className="skeleton" style={{ height: 280, borderRadius: 14 }} />
        <div className="skeleton" style={{ height: 280, borderRadius: 14 }} />
      </div>
    </div>
  );
}

/* ── Error Banner ── */
function ErrorBanner({ message, onRetry }: { message: string; onRetry: () => void }) {
  return (
    <div style={{ padding: "20px 24px", borderRadius: 14, background: "rgba(244,63,94,0.08)", border: "1px solid rgba(244,63,94,0.2)", display: "flex", alignItems: "center", gap: 16 }}>
      <AlertTriangle size={22} color="#f43f5e" />
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 14, fontWeight: 600, color: "#fb7185", marginBottom: 2 }}>Dashboard Telemetry Failed</div>
        <div style={{ fontSize: 12, color: "#64748b" }}>{message}</div>
      </div>
      <button className="btn-danger" onClick={onRetry} style={{ padding: "8px 16px", fontSize: 12 }}>
        <RefreshCw size={13} />
        Retry
      </button>
    </div>
  );
}

/* ── Section Header ── */
function SectionHeader({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div style={{ marginBottom: 16, paddingBottom: 12, borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
      <h2 style={{ fontSize: 14, fontWeight: 700, color: "#94a3b8", letterSpacing: "0.08em", textTransform: "uppercase", margin: 0 }}>{title}</h2>
      {subtitle && <p style={{ fontSize: 12, color: "#334155", marginTop: 3 }}>{subtitle}</p>}
    </div>
  );
}

/* ── Chart Wrapper Card ── */
function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="fs-card" style={{ padding: "20px 20px 16px" }}>
      <div style={{ fontSize: 12, fontWeight: 700, color: "#64748b", letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 16, paddingBottom: 10, borderBottom: "1px solid rgba(255,255,255,0.05)" }}>
        {title}
      </div>
      {children}
    </div>
  );
}

export function DashboardPage() {
  const {
    data: dashboardData,
    isLoading: dashboardLoading,
    isError: dashboardError,
    error: dashboardErrorObj,
    refetch: refetchDashboard,
  } = useQuery({ queryKey: ["dashboard"], queryFn: getDashboardSummary });

  const {
    data: healthData,
    isLoading: healthLoading,
    isError: healthError,
    error: healthErrorObj,
    refetch: refetchHealth,
  } = useQuery({ queryKey: ["health"], queryFn: getHealth });

  const [lastRefresh, setLastRefresh] = useState(new Date());
  const [countdown, setCountdown] = useState(30);

  useEffect(() => {
    if (dashboardData) setLastRefresh(new Date());
  }, [dashboardData]);

  useEffect(() => {
    if (dashboardLoading || healthLoading) return;
    const timer = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) { refetchDashboard(); refetchHealth(); return 30; }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [dashboardLoading, healthLoading, refetchDashboard, refetchHealth]);

  const isLoading = dashboardLoading || healthLoading;
  const isError   = dashboardError || healthError;
  const errMsg    = ((dashboardErrorObj || healthErrorObj) instanceof Error)
    ? (dashboardErrorObj || healthErrorObj as Error).message
    : "Failed to connect to backend telemetry service.";

  if (isLoading) return <DashboardSkeleton />;

  if (isError) {
    return (
      <div style={{ paddingTop: 8 }}>
        <ErrorBanner message={errMsg} onRetry={() => { refetchDashboard(); refetchHealth(); }} />
      </div>
    );
  }

  const summary = dashboardData;
  if (!summary) {
    return (
      <div style={{ textAlign: "center", padding: "60px 20px", color: "#475569" }}>
        <Activity size={40} style={{ marginBottom: 12, opacity: 0.4 }} />
        <div style={{ fontSize: 16, fontWeight: 600, color: "#64748b" }}>No dashboard data available</div>
        <div style={{ fontSize: 13, marginTop: 6, marginBottom: 20 }}>Backend returned an empty response</div>
        <button className="btn-secondary" onClick={() => { refetchDashboard(); refetchHealth(); }}>
          <RefreshCw size={14} /> Refresh Data
        </button>
      </div>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 28 }} className="animate-fade-in">
      {/* ── Toolbar ── */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, padding: "10px 16px", borderRadius: 12, background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <Shield size={16} color="#818cf8" />
          <span style={{ fontSize: 14, fontWeight: 600, color: "#e2e8f0" }}>Operational Overview</span>
          <span style={{ fontSize: 12, color: "#334155" }}>— Real-time metric telemetry & threat indicators</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 7, padding: "6px 12px", borderRadius: 8, background: "rgba(99,102,241,0.08)", border: "1px solid rgba(99,102,241,0.15)", fontSize: 12, color: "#818cf8" }}>
            <Clock size={12} />
            Updated {lastRefresh.toLocaleTimeString()}
            <span style={{ color: "#4f46e5" }}>•</span>
            <span style={{ fontWeight: 700 }}>{countdown}s</span>
          </div>
          <button
            className="btn-secondary"
            style={{ padding: "6px 14px", fontSize: 12, gap: 6 }}
            onClick={() => { refetchDashboard(); refetchHealth(); setCountdown(30); }}
          >
            <RefreshCw size={12} />
            Refresh
          </button>
        </div>
      </div>

      {/* ── KPI Cards ── */}
      <section>
        <SectionHeader title="Key Performance Indicators" subtitle="Live metrics from fraud detection pipeline" />
        <KpiCards />
      </section>

      {/* ── Recent Predictions ── */}
      <section>
        <SectionHeader title="Recent Predictions Stream" />
        <div className="fs-card" style={{ overflow: "hidden" }}>
          <RecentPredictionsTable predictions={summary.recent_predictions || []} />
        </div>
      </section>

      {/* ── Main Charts ── */}
      <section>
        <SectionHeader title="Distribution Analysis" />
        <div className="grid-2">
          <ChartCard title="Prediction Distribution">
            <PredictionChart />
          </ChartCard>
          <ChartCard title="Risk Tier Score Distribution">
            <RiskChart />
          </ChartCard>
        </div>
      </section>

      {/* ── System Health ── */}
      <section>
        <SectionHeader title="Model & System Health" />
        <div className="grid-2">
          <ModelInformation model={summary.model || {}} />
          <SystemStatus health={healthData!} />
        </div>
      </section>

      {/* ── Extended Analytics ── */}
      <section>
        <SectionHeader title="Advanced Statistical Distributions" subtitle="Deep-dive analytics and behavioral patterns" />
        <div className="grid-2">
          <ChartCard title="Transaction Volume by Channel">
            <BarChartComponent />
          </ChartCard>
          <ChartCard title="Fraud Trend (30 Days)">
            <AreaChartComponent />
          </ChartCard>
          <ChartCard title="Feature Risk Radar">
            <RadarChartComponent />
          </ChartCard>
          <ChartCard title="Risk Category Treemap">
            <TreemapChartComponent />
          </ChartCard>
        </div>
      </section>

      {/* ── Activity Timeline ── */}
      <section>
        <SectionHeader title="Activity Timeline" />
        <div className="fs-card" style={{ padding: 20 }}>
          <ActivityTimeline />
        </div>
      </section>
    </div>
  );
}