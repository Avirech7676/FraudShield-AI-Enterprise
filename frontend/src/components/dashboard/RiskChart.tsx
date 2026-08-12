import { useQuery } from "@tanstack/react-query";
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Tooltip,
  Legend,
  Cell,
} from "recharts";
import { Skeleton } from "../../components/common/Skeleton";
import { getRiskDistribution } from "../../services/analytics";

export function RiskChart() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["risk-distribution"],
    queryFn: getRiskDistribution,
  });

  if (isLoading) return <div className="chart-loading"><Skeleton height={200} /></div>;
  if (error) return <div className="chart-error">Error loading risk data</div>;

  const chartData = data?.map((item: any) => ({
    name: item.label || item.risk_level || item.name || "Unknown",
    value: item.value ?? item.count ?? 0,
  })) || [];

  if (!chartData.length) return <div className="chart-empty">No risk data available</div>;

  const COLORS = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#10b981"]; // red, orange, yellow, green, blue-green

  return (
    <div className="chart-container">
      <h3>Risk Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={120}
            labelLine={false}
            label={({ name }) => (
              <text textAnchor="middle" dy={4} fontSize={12} fill="#fff">
                {name}
              </text>
            )}
          >
            {chartData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>

          <Tooltip
            formatter={(value) => `${value} transactions`}
            labelFormatter={(name) => `${name} Risk`}
          />

          <Legend verticalAlign="top" />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}