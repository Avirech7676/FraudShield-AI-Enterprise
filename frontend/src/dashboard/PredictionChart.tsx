import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Tooltip,
  Legend,
  Cell,
} from "recharts";

type Props = {
  data: any[];
};

const COLORS = ["#16a34a", "#dc2626"];

export default function PredictionChart({ data }: Props) {
  return (
    <div className="prediction-card">
      <h2>Prediction Distribution</h2>

      <ResponsiveContainer width="100%" height={350}>
        <PieChart>
          <Pie data={data} dataKey="count" nameKey="label" outerRadius={120}>
            {data.map((_, index) => (
              <Cell key={index} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>

          <Tooltip />

          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
