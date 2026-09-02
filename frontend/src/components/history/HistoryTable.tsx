import type { PredictionHistory } from "../../types/history";
import { useNavigate } from "react-router-dom";
import { Table, type Column } from "../ui/Table";
import { RiskBadge } from "../ui/RiskBadge";
import { Badge } from "../ui/Badge";
import { Button } from "../ui/Button";
import { Eye, Zap } from "lucide-react";

type Props = {
  data: PredictionHistory[];
  onView: (prediction: PredictionHistory) => void;
};

export default function HistoryTable({ data, onView }: Props) {
  const navigate = useNavigate();

  const columns: Column<PredictionHistory>[] = [
    {
      key: "transaction_id",
      header: "Transaction ID",
      render: (row) => (
        <span className="font-mono text-xs text-indigo-300 font-semibold">
          {row.transaction_id}
        </span>
      ),
    },
    {
      key: "customer_id",
      header: "Customer Ref",
      render: (row) => (
        <span className="font-mono text-xs text-slate-300">
          {row.customer_id || "CUST-ANON"}
        </span>
      ),
    },
    {
      key: "prediction",
      header: "Assessment",
      render: (row) => (
        <Badge variant={row.prediction === "Fraud" ? "rose" : "emerald"} size="sm" dot>
          {row.prediction}
        </Badge>
      ),
    },
    {
      key: "risk_score",
      header: "Score",
      render: (row) => (
        <span className="font-mono text-slate-200">{row.risk_score}</span>
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
      key: "merchant",
      header: "Merchant",
      render: (row) => (
        <span className="text-xs font-medium text-slate-300">
          {row.merchant || "Standard Payment"}
        </span>
      ),
    },
    {
      key: "country",
      header: "Geo",
      render: (row) => (
        <Badge variant="slate" size="sm">
          {row.country || "US"}
        </Badge>
      ),
    },
    {
      key: "Latency_ms",
      header: "Latency",
      render: (row) => (
        <span className="font-mono text-xs text-amber-400">
          {(Number(row.Latency_ms) || 0).toFixed(1)} ms
        </span>
      ),
    },
    {
      key: "created_at",
      header: "Logged At",
      align: "right",
      render: (row) => (
        <span className="text-xs text-slate-400">
          {row.created_at ? new Date(row.created_at).toLocaleString() : "Just now"}
        </span>
      ),
    },
    {
      key: "actions",
      header: "Action",
      align: "right",
      render: (row) => (
        <div className="flex items-center justify-end gap-2" onClick={(e) => e.stopPropagation()}>
          <Button
            variant="ghost"
            size="sm"
            leftIcon={<Eye className="w-3.5 h-3.5" />}
            onClick={() => onView(row)}
          >
            Details
          </Button>

          <Button
            variant="outline"
            size="sm"
            leftIcon={<Zap className="w-3.5 h-3.5" />}
            onClick={() => navigate(`/explanation/${row.transaction_id}`)}
          >
            SHAP
          </Button>
        </div>
      ),
    },
  ];

  return (
    <Table
      columns={columns}
      data={data}
      emptyTitle="No Evaluation History Records"
      emptyDescription="No past prediction events match your active search filters."
    />
  );
}