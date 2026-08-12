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

export function RiskTierChart() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["risk-tiers"],
    queryFn: getRiskDistribution,
  });

  if (isLoading) return <Skeleton height={100} />;
  if (error) return <div className="chart-error">Error loading risk tier data</div>;

  const chartData = data?.map((item: any) => ({
    name: item.risk_level || "Unknown",
    value: item.count || 0,
  })) || [];

  if (!chartData.length) return <div className="chart-empty">No risk tier data</div>;

  const COLORS = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#10b981"];

  return (
    <div className="chart-container">
      <h3>Risk Tiers</h3>
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