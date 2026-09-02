import { useQuery } from "@tanstack/react-query";
import { getTreemapData } from "../../services/analytics";
import {
  ResponsiveContainer,
  Treemap,
} from "recharts";

const TreemapCell = (_: any) => {
  // This is a workaround for Recharts Treemap custom cell rendering
  // We return a function that will be called by Recharts with the params
  return ({ x, y, width, height, ...props }: {
    x: number;
    y: number;
    width: number;
    height: number;
    [key: string]: any
  }) => (
    <rect
      x={x}
      y={y}
      width={width}
      height={height}
      fill={`hsl(${(Math.random() * 360).toFixed(0)}, 70%, 50%)`}
      stroke="#fff"
      strokeWidth={1}
      {...props}
    />
  );
};

export function TreemapChartComponent() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["treemap-data"],
    queryFn: getTreemapData,
  });

  if (isLoading) return <div className="chart-loading">Loading...</div>;
  if (error) return <div className="chart-error">Error loading treemap data</div>;

  if (!data || data.length === 0) return <div className="chart-empty">No treemap data available</div>;

  // Format data for treemap (expects name and value properties)
  const treemapData = data.map((item: any) => ({
    name: item.name || "Unknown",
    value: item.value || 0,
  }));

  return (
    <div className="chart-container">
      <h3>Treemap</h3>
      <ResponsiveContainer width="100%" height={300}>
        <Treemap data={treemapData}>
          {(TreemapCell(null) as any)}
        </Treemap>
      </ResponsiveContainer>
    </div>
  );
}