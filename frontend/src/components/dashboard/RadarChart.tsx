import { useQuery } from "@tanstack/react-query";
import { getRadarChartData } from "../../services/analytics";
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Tooltip,
  Legend,
  Radar,
} from "recharts";

// Helper component for radar chart series
const RadarChartSeries = ({ dataKey, name, ...props }: any) => (
  <Radar
    dataKey={dataKey}
    name={name}
    {...props}
  />
);

export function RadarChartComponent() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["radar-chart-data"],
    queryFn: getRadarChartData,
  });

  if (isLoading) return <div className="chart-loading">Loading...</div>;
  if (error) return <div className="chart-error">Error loading radar chart data</div>;

  if (!data || data.length === 0) return <div className="chart-empty">No radar chart data available</div>;

  // Extract unique data keys for the radar chart (excluding 'name')
  const dataKeys = Object.keys(data[0] || {}).filter(key => key !== 'name');

  return (
    <div className="chart-container">
      <h3>Radar Chart</h3>
      <ResponsiveContainer width="100%" height={300}>
        <RadarChart
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={20}
          outerRadius={80}
        >
          <PolarGrid />
          <PolarAngleAxis dataKey="name" />
          <PolarRadiusAxis />
          <Tooltip />
          <Legend />
          {dataKeys.map((_, index) => (
            <RadarChartSeries
              key={`radar-${index}`}
              dataKey={dataKeys[index]}
              name={dataKeys[index]}
              strokeWidth={2}
              stroke={`hsl(${(index * 60) % 360}, 70%, 50%)`}
              fillOpacity={0.2}
            />
          ))}
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}