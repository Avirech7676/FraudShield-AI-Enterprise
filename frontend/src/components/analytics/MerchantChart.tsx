import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Tooltip,
  Legend,
  Cell,
} from "recharts";

type Props = {
  data: Array<{ name: string; value: number }>;
};

const COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#06b6d4"];

export function MerchantChart({ data }: Props) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-placeholder">
        <h3>Merchant Distribution</h3>
        <p>No merchant data available</p>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <h3>Merchant Distribution</h3>
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={data}
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
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>

          <Tooltip
            formatter={(value) => `${value} transactions`}
            labelFormatter={(name) => `${name} Merchant`}
          />

          <Legend verticalAlign="top" />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}