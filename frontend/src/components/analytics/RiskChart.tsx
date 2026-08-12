import { useQuery } from "@tanstack/react-query";
import { getRiskDistribution } from "../../services/analytics";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Cell,
} from "recharts";
import { Skeleton } from "../../components/common/Skeleton";

export function RiskChart() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["risk-distribution"],
    queryFn: getRiskDistribution,
  });

  if (isLoading) return <div className="chart-loading"><Skeleton height={200} /></div>;
  if (error) return <div className="chart-error">Error loading risk data</div>;

  const chartData = data?.map((item) => ({
    name: item.risk_level || "Unknown",
    value: item.count || 0,
  })) || [];

  if (!chartData.length) return <div className="chart-empty">No risk data available</div>;

  const COLORS = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#10b981"]; // red, orange, yellow, green, blue-green

  return (
    <div className="chart-container">
      <h3>Risk Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value">
            {chartData.map((_entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}