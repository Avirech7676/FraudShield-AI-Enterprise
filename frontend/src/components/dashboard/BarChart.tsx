import { useQuery } from "@tanstack/react-query";
import { getBarChartData } from "../../services/analytics";
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

export function BarChartComponent() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["bar-chart-data"],
    queryFn: getBarChartData,
  });

  if (isLoading) return <div className="chart-loading">Loading...</div>;
  if (error) return <div className="chart-error">Error loading bar chart data</div>;

  const chartData = data?.map((item: any) => ({
    name: item.name || "Unknown",
    value: item.value || 0,
  })) || [];

  if (!chartData.length) return <div className="chart-empty">No bar chart data available</div>;

  const COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"];

  return (
    <div className="chart-container">
      <h3>Bar Chart</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value">
            {chartData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}