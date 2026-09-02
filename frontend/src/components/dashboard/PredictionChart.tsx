import { useQuery } from "@tanstack/react-query";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { Skeleton } from "../common/Skeleton";
import { getFraudTrends } from "../../services/analytics";

export function PredictionChart() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["fraud-trends"],
    queryFn: getFraudTrends,
  });

  if (isLoading) return <div className="chart-loading"><Skeleton height={200} /></div>;
  if (error) return <div className="chart-error">Error loading chart</div>;

  const chartData = data?.map((item: any) => ({
    date: item.date || item.label || "Today",
    legitimate: item.legitimate ?? (item.total ? Math.max(0, item.total - (item.fraud || 0)) : item.value || 0),
    fraudulent: item.fraudulent ?? item.fraud ?? 0,
  })) || [];

  if (!chartData.length) return <div className="chart-empty">No prediction trend data available</div>;

  return (
    <div className="prediction-chart-container">
      <ResponsiveContainer width="100%" height={260}>
        <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
          <XAxis dataKey="date" stroke="#64748b" tick={{ fill: "#64748b", fontSize: 11 }} />
          <YAxis stroke="#64748b" tick={{ fill: "#64748b", fontSize: 11 }} />
          <Tooltip
            contentStyle={{ background: "#0f172a", borderColor: "rgba(255,255,255,0.1)", borderRadius: 10, color: "#fff" }}
          />
          <Legend verticalAlign="top" height={36} />
          <Line type="monotone" dataKey="legitimate" stroke="#10b981" strokeWidth={2} name="Legitimate" />
          <Line type="monotone" dataKey="fraudulent" stroke="#ef4444" strokeWidth={2} name="Fraudulent" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}