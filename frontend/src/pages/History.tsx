import { useMemo, useState } from "react";
import { useHistory } from "../hooks/useHealth";
import HistoryTable from "../components/history/HistoryTable";
import HistoryDetailModal from "../components/history/HistoryDetailModal";
import type { PredictionHistory } from "../types/history";

import { Input } from "../components/ui/Input";
import { Button } from "../components/ui/Button";
import { Skeleton } from "../components/ui/Skeleton";
import { ErrorState } from "../components/ui/ErrorState";
import { Search, Download, FileSpreadsheet, RefreshCw, ChevronLeft, ChevronRight, History } from "lucide-react";

const PAGE_SIZE = 10;

export default function HistoryPage() {
  const [filters] = useState({
    customerId: "",
    transactionId: "",
    dateFrom: "",
    dateTo: "",
    amountMin: "",
    amountMax: "",
    riskLevel: "",
    merchant: "",
    status: "",
  });

  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState<PredictionHistory | null>(null);
  const [page, setPage] = useState(1);

  const { predictions, loading, error, refresh } = useHistory({
    filters,
    page,
    size: PAGE_SIZE,
  });

  const safeList = useMemo(() => {
    return Array.isArray(predictions) ? predictions : [];
  }, [predictions]);

  const filtered = useMemo(() => {
    if (!search) return safeList;
    const searchLower = search.toLowerCase();
    return safeList.filter((item) => {
      return (
        item.transaction_id?.toLowerCase().includes(searchLower) ||
        item.customer_id?.toLowerCase().includes(searchLower) ||
        item.merchant?.toLowerCase().includes(searchLower) ||
        item.country?.toLowerCase().includes(searchLower) ||
        item.prediction?.toLowerCase().includes(searchLower) ||
        item.risk_tier?.toLowerCase().includes(searchLower) ||
        item.status?.toLowerCase().includes(searchLower)
      );
    });
  }, [safeList, search]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));

  const paginated = useMemo(() => {
    const start = (page - 1) * PAGE_SIZE;
    return filtered.slice(start, start + PAGE_SIZE);
  }, [filtered, page]);

  function exportJSON() {
    const blob = new Blob([JSON.stringify(filtered, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `prediction_history_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function exportCSV() {
    const header = [
      "Transaction",
      "Customer ID",
      "Prediction",
      "Risk Score",
      "Risk Tier",
      "Merchant",
      "Country",
      "Latency",
      "Created",
    ];

    const rows = filtered.map((item) => [
      item.transaction_id,
      item.customer_id || "",
      item.prediction,
      item.risk_score,
      item.risk_tier,
      item.merchant || "",
      item.country || "",
      item.Latency_ms,
      item.created_at,
    ]);

    const csv = [header, ...rows].map((r) => r.join(",")).join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `prediction_history_${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }

  if (loading) {
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
        <Skeleton variant="rectangular" className="h-16 w-full" />
        <Skeleton variant="rectangular" className="h-96 w-full" />
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: "40px 0" }}>
        <ErrorState
          title="History Query Failed"
          message="Could not load prediction audit logs from repository."
          onRetry={refresh}
        />
      </div>
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 24 }} className="animate-fade-in">
      {/* Subheader Toolbar */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, paddingBottom: 16, borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 36, height: 36, borderRadius: 10, background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.25)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <History size={18} color="#818cf8" />
          </div>
          <div>
            <h2 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>Prediction Audit Trail & Logs</h2>
            <p style={{ fontSize: 12, color: "#475569", margin: "2px 0 0" }}>Searchable historical record of all evaluated transactions, probabilities, and latencies</p>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <Button
            variant="outline"
            size="sm"
            leftIcon={<FileSpreadsheet className="w-3.5 h-3.5" />}
            onClick={exportCSV}
          >
            Export CSV
          </Button>

          <Button
            variant="outline"
            size="sm"
            leftIcon={<Download className="w-3.5 h-3.5" />}
            onClick={exportJSON}
          >
            Export JSON
          </Button>
        </div>
      </div>

      {/* Filter Controls */}
      <div className="fs-card" style={{ padding: 16, display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16 }}>
        <div style={{ flex: 1, maxWidth: 380 }}>
          <Input
            placeholder="Search across all fields (Ref, Customer, Geo, Tier)..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
            leftIcon={<Search className="w-4 h-4" />}
          />
        </div>

        <Button
          variant="ghost"
          size="sm"
          leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
          onClick={refresh}
        >
          Refresh Logs
        </Button>
      </div>

      {/* History Data Table */}
      <div className="fs-card" style={{ overflow: "hidden" }}>
        <HistoryTable data={paginated} onView={setSelected} />
      </div>

      {/* Pagination Controls */}
      <div className="fs-card" style={{ padding: "12px 20px", display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, fontSize: 13, color: "#64748b" }}>
        <span>
          Showing {filtered.length === 0 ? 0 : (page - 1) * PAGE_SIZE + 1}-
          {Math.min(page * PAGE_SIZE, filtered.length)} of {filtered.length} total entries
        </span>

        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <Button
            variant="outline"
            size="sm"
            disabled={page <= 1}
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            leftIcon={<ChevronLeft className="w-4 h-4" />}
          >
            Previous
          </Button>

          <span style={{ fontWeight: 600, color: "#e2e8f0", padding: "0 8px" }}>
            Page {page} of {totalPages}
          </span>

          <Button
            variant="outline"
            size="sm"
            disabled={page >= totalPages}
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            rightIcon={<ChevronRight className="w-4 h-4" />}
          >
            Next
          </Button>
        </div>
      </div>

      <HistoryDetailModal
        prediction={selected}
        onClose={() => setSelected(null)}
      />
    </div>
  );
}