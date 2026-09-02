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

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884D8"];

export function CountryChart({ data }: Props) {
  if (!data || data.length === 0) {
    return (
      <div className="chart-placeholder">
        <h3>Geographic Distribution</h3>
        <p>No geographic data available</p>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <h3>Geographic Distribution</h3>
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            labelLine={false}
            label
          >
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>

          <Tooltip formatter={(value) => `${value}%`} />
          <Legend verticalAlign="top" />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}