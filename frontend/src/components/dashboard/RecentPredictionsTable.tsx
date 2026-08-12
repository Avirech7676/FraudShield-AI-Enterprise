import type { RecentPrediction } from "../../types/dashboard";
import { Table, type Column } from "../ui/Table";
import { RiskBadge } from "../ui/RiskBadge";
import { Badge } from "../ui/Badge";
import { Card, CardHeader, CardTitle } from "../ui/Card";

type Props = {
  predictions?: RecentPrediction[];
};

export default function RecentPredictionsTable({ predictions = [] }: Props) {
  const list = Array.isArray(predictions) ? predictions : [];

  const columns: Column<RecentPrediction>[] = [
    {
      key: "transaction_id",
      header: "Transaction ID",
      render: (row) => (
        <span style={{ fontFamily: "var(--font-mono)", fontSize: 12, color: "#818cf8", fontWeight: 600 }}>
          {row.transaction_id}
        </span>
      ),
    },
    {
      key: "prediction",
      header: "Assessment",
      render: (row) => (
        <Badge
          variant={row.prediction === "Fraud" ? "rose" : "emerald"}
          size="sm"
          dot
        >
          {row.prediction}
        </Badge>
      ),
    },
    {
      key: "fraud_probability",
      header: "Probability",
      render: (row) => (
        <span style={{ fontWeight: 600, color: "#e2e8f0" }}>
          {((row.fraud_probability ?? 0) * (row.fraud_probability <= 1 ? 100 : 1)).toFixed(1)}%
        </span>
      ),
    },
    {
      key: "risk_score",
      header: "Risk Score",
      render: (row) => (
        <span style={{ fontFamily: "var(--font-mono)", color: "#cbd5e1" }}>
          {row.risk_score}
        </span>
      ),
    },
    {
      key: "risk_tier",
      header: "Risk Tier",
      render: (row) => (
        <RiskBadge level={row.risk_tier} score={(row.risk_score || 0) / 100} size="sm" showScore={false} />
      ),
    },
    {
      key: "created_at",
      header: "Timestamp",
      align: "right",
      render: (row) => (
        <span style={{ fontSize: 12, color: "#64748b" }}>
          {row.created_at ? new Date(row.created_at).toLocaleTimeString() : "N/A"}
        </span>
      ),
    },
  ];

  return (
    <Card variant="glass">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <span>Recent Transaction Stream</span>
          <Badge variant="indigo" size="sm">
            {list.length} live entries
          </Badge>
        </CardTitle>
      </CardHeader>
      <Table columns={columns} data={list} emptyTitle="No stream transactions recorded" />
    </Card>
  );
}