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

type Props = {
  data: Array<{ name: string; uv: number; pv: number }>;
};

export function FraudChart({ data }: Props) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-placeholder">
        <h3>Fraud Trends</h3>
        <p>No fraud trend data available</p>
      </div>
    );
  }

  const chartData = data.map((item) => ({
    name: item.name,
    uv: item.uv || 0,
    pv: item.pv || 0,
  }));

  return (
    <div className="chart-container">
      <h3>Fraud Trends</h3>
      <ResponsiveContainer width="100%" height={200}>
        <AreaChart data={chartData}>
          <defs>
            <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#ff8c00" stopOpacity={0.8} />
              <stop offset="100%" stopColor="#ff8c00" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#8884d8" stopOpacity={0.8} />
              <stop offset="100%" stopColor="#8884d8" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Area type="monotone" dataKey="uv" stroke="#ff8c00" fill="url(#colorUv)" />
          <Area type="monotone" dataKey="pv" stroke="#8884d8" fill="url(#colorPv)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}