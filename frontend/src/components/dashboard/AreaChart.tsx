import { useQuery } from "@tanstack/react-query";
import { getAreaChartData } from "../../services/analytics";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";

export function AreaChartComponent() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["area-chart-data"],
    queryFn: getAreaChartData,
  });

  if (isLoading) return <div className="chart-loading">Loading...</div>;
  if (error) return <div className="chart-error">Error loading area chart data</div>;

  const chartData = data?.map((item: any) => ({
    name: item.name || "",
    value: item.value || 0,
  })) || [];

  if (!chartData.length) return <div className="chart-empty">No area chart data available</div>;

  return (
    <div className="chart-container">
      <h3>Area Chart</h3>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={chartData}>
          <defs>
            <linearGradient id="colorArea" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#3b82f6" stopOpacity={0.8} />
              <stop offset="100%" stopColor="#3b82f6" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Area type="monotone" dataKey="value" stroke="#3b82f6" fill="url(#colorArea)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}