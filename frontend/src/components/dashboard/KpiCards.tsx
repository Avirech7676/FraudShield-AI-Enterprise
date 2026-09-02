import { useQuery } from "@tanstack/react-query";
import { getDashboardSummary } from "../../services/dashboard";
import { MetricCard } from "../ui/MetricCard";
import { Skeleton } from "../ui/Skeleton";
import { CreditCard, ShieldAlert, Bell, Activity } from "lucide-react";

export function KpiCards() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["dashboard"],
    queryFn: getDashboardSummary,
  });

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
        {[1, 2, 3, 4].map((i) => (
          <Skeleton key={i} variant="card" className="h-32" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-medium mb-8">
        Failed to load operational metrics from dashboard backend.
      </div>
    );
  }

  const { kpis } = data || {};

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
      <MetricCard
        title="Total Transactions"
        value={(kpis?.transactions ?? 0).toLocaleString()}
        change="+12.5% vs last week"
        trend="up"
        icon={<CreditCard className="w-5 h-5" />}
        iconBg="indigo"
      />

      <MetricCard
        title="Flagged Fraud Cases"
        value={(kpis?.fraud_cases ?? 0).toLocaleString()}
        change="-3.2% resolution rate"
        trend="down"
        icon={<ShieldAlert className="w-5 h-5" />}
        iconBg="rose"
      />

      <MetricCard
        title="Active Threat Alerts"
        value={(kpis?.alerts ?? 0).toLocaleString()}
        change="+8.1% new breaches"
        trend="up"
        icon={<Bell className="w-5 h-5" />}
        iconBg="amber"
      />

      <MetricCard
        title="Average Risk Score"
        value={(kpis?.average_risk ?? 0).toFixed(2)}
        subtitle="Across real-time evaluation batch"
        icon={<Activity className="w-5 h-5" />}
        iconBg="emerald"
      />
    </div>
  );
}