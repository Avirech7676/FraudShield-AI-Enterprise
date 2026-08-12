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

type Props = {
  data: Array<{ name: string; value: number }>;
};

const COLORS = ["#10b981", "#3b82f6", "#8b5cf6", "#ec4899", "#f97316"];

export function PerformanceCard({ data }: Props) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-placeholder">
        <h3>Performance Metrics</h3>
        <p>No performance data available</p>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <h3>Performance Metrics</h3>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value">
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}