import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Tooltip,
  Legend,
  Cell,
} from "recharts";

import type { PredictionDistribution } from "../../types/dashboard.ts";

type Props = {
  data: PredictionDistribution[];
};

const COLORS = ["#22c55e", "#ef4444"];

export default function PredictionDistributionChart({ data }: Props) {
  if (!data.length) {
    return (
      <div className="dashboard-card">
        <h3>Prediction Distribution</h3>

        <p>No Data Available</p>
      </div>
    );
  }

  return (
    <div className="dashboard-card">
      <h3>Prediction Distribution</h3>

      <ResponsiveContainer width="100%" height={350}>
        <PieChart>
          <Pie
            data={data}
            dataKey="count"
            nameKey="label"
            outerRadius={120}
            label
          >
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
