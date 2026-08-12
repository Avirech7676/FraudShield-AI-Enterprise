import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { getAlerts, assignAlert, updateAlert } from "../services/alerts";
import { Table, type Column } from "../components/ui/Table";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { Select } from "../components/ui/Select";
import { Badge } from "../components/ui/Badge";
import { RiskBadge } from "../components/ui/RiskBadge";
import { Modal } from "../components/ui/Modal";
import { Drawer } from "../components/ui/Drawer";
import { Skeleton } from "../components/ui/Skeleton";
import { ErrorState } from "../components/ui/ErrorState";
import { Bell, Search, UserCheck, ShieldAlert, Eye } from "lucide-react";

export interface AlertItem {
  id?: string;
  _id?: string;
  alert_id?: string;
  transaction_id: string;
  rule_triggered?: string;
  severity?: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | string;
  risk_score?: number;
  assigned_to?: string;
  status: "ACTIVE" | "ACKNOWLEDGED" | "RESOLVED" | "FALSE_POSITIVE" | string;
  details?: string;
  created_at: string;
}

export default function AlertsPage() {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [severityFilter, setSeverityFilter] = useState("ALL");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [selectedAlert, setSelectedAlert] = useState<AlertItem | null>(null);
  const [isAssignModalOpen, setIsAssignModalOpen] = useState(false);
  const [newAnalyst, setNewAnalyst] = useState("");

  const { data: alertsData, isLoading, isError, error, refetch } = useQuery({
    queryKey: ["alerts"],
    queryFn: getAlerts,
  });

  const alertsList: AlertItem[] = Array.isArray(alertsData)
    ? alertsData
    : alertsData?.alerts || [];

  const filteredAlerts = alertsList.filter((item) => {
    const matchesSearch =
      (item.alert_id || item.id || "").toLowerCase().includes(search.toLowerCase()) ||
      (item.transaction_id || "").toLowerCase().includes(search.toLowerCase()) ||
      (item.rule_triggered || "").toLowerCase().includes(search.toLowerCase()) ||
      (item.assigned_to || "").toLowerCase().includes(search.toLowerCase());

    const matchesSeverity =
      severityFilter === "ALL" || (item.severity || "").toUpperCase() === severityFilter;

    const matchesStatus =
      statusFilter === "ALL" || item.status === statusFilter;

    return matchesSearch && matchesSeverity && matchesStatus;
  });

  const handleAssignAnalyst = async () => {
    if (!selectedAlert || !newAnalyst) return;
    try {
      const alertId = selectedAlert.alert_id || selectedAlert.id || selectedAlert._id || "";
      await assignAlert(alertId, newAnalyst);
      queryClient.invalidateQueries({ queryKey: ["alerts"] });
      setIsAssignModalOpen(false);
      setNewAnalyst("");
    } catch (err: any) {
      alert("Failed to assign alert: " + err.message);
    }
  };

  const handleUpdateStatus = async (item: AlertItem, newStatus: string) => {
    try {
      const alertId = item.alert_id || item.id || item._id || "";
      await updateAlert(alertId, newStatus);
      queryClient.invalidateQueries({ queryKey: ["alerts"] });
    } catch (err: any) {
      alert("Failed to update alert status: " + err.message);
    }
  };

  const columns: Column<AlertItem>[] = [
    {
      key: "alert_id",
      header: "Alert ID",
      render: (row) => (
        <span className="font-mono text-xs text-rose-300 font-bold flex items-center gap-1.5">
          <Bell className="w-3.5 h-3.5 text-rose-400" />
          {row.alert_id || row.id || row._id || "ALT-9041"}
        </span>
      ),
    },
    {
      key: "transaction_id",
      header: "Transaction Ref",
      render: (row) => (
        <span className="font-mono text-xs text-indigo-300 font-semibold">
          {row.transaction_id}
        </span>
      ),
    },
    {
      key: "rule_triggered",
      header: "Rule Vector",
      render: (row) => (
        <span className="text-xs font-semibold text-slate-200">
          {row.rule_triggered || "GEO_VELOCITY_ANOMALY"}
        </span>
      ),
    },
    {
      key: "severity",
      header: "Severity",
      render: (row) => (
        <RiskBadge
          level={row.severity || "HIGH"}
          score={(row.risk_score || 88) / 100}
          size="sm"
        />
      ),
    },
    {
      key: "assigned_to",
      header: "Assigned Analyst",
      render: (row) => (
        <Badge variant={row.assigned_to ? "indigo" : "slate"} size="sm">
          {row.assigned_to || "Unassigned"}
        </Badge>
      ),
    },
    {
      key: "status",
      header: "Status",
      render: (row) => {
        const variantMap: Record<string, "rose" | "amber" | "emerald" | "slate"> = {
          ACTIVE: "rose",
          ACKNOWLEDGED: "amber",
          RESOLVED: "emerald",
          FALSE_POSITIVE: "slate",
        };
        return (
          <Badge variant={variantMap[row.status || "ACTIVE"] || "slate"} size="sm" dot pulse={row.status === "ACTIVE"}>
            {(row.status || "ACTIVE").replace(/_/g, " ")}
          </Badge>
        );
      },
    },
    {
      key: "created_at",
      header: "Timestamp",
      align: "right",
      render: (row) => (
        <span className="text-xs text-slate-400">
          {row.created_at ? new Date(row.created_at).toLocaleTimeString() : "Live"}
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
            onClick={() => setSelectedAlert(row)}
          >
            Inspect
          </Button>

          {row.status === "ACTIVE" && (
            <Button
              variant="outline"
              size="sm"
              onClick={() => handleUpdateStatus(row, "ACKNOWLEDGED")}
            >
              Ack
            </Button>
          )}
        </div>
      ),
    },
  ];

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton variant="rectangular" className="h-16 w-full" />
        <Skeleton variant="rectangular" className="h-96 w-full" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="py-12">
        <ErrorState
          title="Threat Alert Stream Failed"
          message={(error as Error)?.message || "Unable to pull live alert feeds from engine."}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Subheader Toolbar */}
      <div className="pb-2 border-b border-slate-800/60 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 tracking-tight">
            Real-Time Threat Alerts
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Automated threat alert dispatch, rule triggers, and risk severity prioritization
          </p>
        </div>

        <Badge variant="rose" size="md" dot pulse>
          {filteredAlerts.filter((a) => a.status === "ACTIVE").length} Active Threats
        </Badge>
      </div>

      {/* Filter Controls */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-2xl bg-slate-900/70 border border-slate-800/80 backdrop-blur-xl">
        <div className="w-full sm:w-72">
          <Input
            placeholder="Search Alert ID, Rule, or Ref..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            leftIcon={<Search className="w-4 h-4" />}
          />
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <Select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            options={[
              { value: "ALL", label: "All Severities" },
              { value: "CRITICAL", label: "Critical Severity" },
              { value: "HIGH", label: "High Severity" },
              { value: "MEDIUM", label: "Medium Severity" },
              { value: "LOW", label: "Low Severity" },
            ]}
          />

          <Select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            options={[
              { value: "ALL", label: "All Statuses" },
              { value: "ACTIVE", label: "Active Only" },
              { value: "ACKNOWLEDGED", label: "Acknowledged" },
              { value: "RESOLVED", label: "Resolved" },
              { value: "FALSE_POSITIVE", label: "False Positive" },
            ]}
          />
        </div>
      </div>

      {/* Alerts Table */}
      <Table
        columns={columns}
        data={filteredAlerts}
        emptyTitle="No Threat Alerts Triggered"
        emptyDescription="All security parameters within acceptable bounds for current filter scope."
        onRowClick={(row) => setSelectedAlert(row)}
      />

      {/* Reassign Analyst Modal */}
      <Modal
        isOpen={isAssignModalOpen}
        onClose={() => setIsAssignModalOpen(false)}
        title="Assign Alert to Security Analyst"
        subtitle={`Alert ID: ${selectedAlert?.alert_id || selectedAlert?.id || "ALT-9041"}`}
        footer={
          <>
            <Button variant="ghost" onClick={() => setIsAssignModalOpen(false)}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleAssignAnalyst}>
              Confirm Assignment
            </Button>
          </>
        }
      >
        <div className="space-y-4">
          <Input
            label="Analyst Handle / Email"
            placeholder="e.g. sec_op@company.com"
            value={newAnalyst}
            onChange={(e) => setNewAnalyst(e.target.value)}
            leftIcon={<UserCheck className="w-4 h-4" />}
            autoFocus
          />
        </div>
      </Modal>

      {/* Alert Details Drawer */}
      <Drawer
        isOpen={Boolean(selectedAlert) && !isAssignModalOpen}
        onClose={() => setSelectedAlert(null)}
        title={
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-rose-400" />
            <span>Threat Vector Inspection</span>
          </div>
        }
        subtitle={`ID: ${selectedAlert?.alert_id || selectedAlert?.id || selectedAlert?._id}`}
      >
        {selectedAlert && (
          <div className="space-y-6">
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase">
                  Transaction Reference
                </span>
                <span className="font-mono text-sm text-indigo-300 font-bold">
                  {selectedAlert.transaction_id}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase">
                  Triggered Rule Engine
                </span>
                <span className="font-mono text-xs text-rose-300 font-bold">
                  {selectedAlert.rule_triggered || "HIGH_VELOCITY_BURST"}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase">
                  Severity Assessment
                </span>
                <RiskBadge level={selectedAlert.severity || "HIGH"} score={0.92} size="sm" />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-300 block">
                Threat Action Toggles
              </label>
              <div className="grid grid-cols-1 gap-2">
                {[
                  { status: "ACKNOWLEDGED", label: "Acknowledge Alert" },
                  { status: "RESOLVED", label: "Resolve Threat & Escalated" },
                  { status: "FALSE_POSITIVE", label: "Mark as False Positive" },
                ].map((st) => (
                  <Button
                    key={st.status}
                    variant={selectedAlert.status === st.status ? "primary" : "outline"}
                    size="sm"
                    fullWidth
                    onClick={() => {
                      handleUpdateStatus(selectedAlert, st.status);
                      setSelectedAlert({ ...selectedAlert, status: st.status });
                    }}
                  >
                    {st.label}
                  </Button>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-300 block">
                Rule Telemetry Payload
              </label>
              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 text-xs text-slate-300 leading-relaxed font-mono">
                {selectedAlert.details ||
                  JSON.stringify(
                    {
                      velocity_burst: "5 tx / 10s",
                      geo_distance_km: 4200,
                      device_fingerprint_match: false,
                    },
                    null,
                    2
                  )}
              </div>
            </div>
          </div>
        )}
      </Drawer>
    </div>
  );
}