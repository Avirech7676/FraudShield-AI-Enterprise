import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { getCases, assignCase, updateCase } from "../services/cases";
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
import { FolderGit2, Search, UserCheck, Eye } from "lucide-react";

export interface CaseItem {
  id?: string;
  _id?: string;
  case_id?: string;
  transaction_id: string;
  assigned_to?: string;
  status: "OPEN" | "UNDER_INVESTIGATION" | "RESOLVED_FRAUD" | "RESOLVED_GENUINE" | "DISMISSED" | string;
  risk_level?: string;
  risk_score?: number;
  investigation_notes?: string;
  created_at: string;
}

export default function CasesPage() {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [selectedCase, setSelectedCase] = useState<CaseItem | null>(null);
  const [isAssignModalOpen, setIsAssignModalOpen] = useState(false);
  const [newAnalyst, setNewAnalyst] = useState("");

  const { data: casesData, isLoading, isError, error, refetch } = useQuery({
    queryKey: ["cases"],
    queryFn: getCases,
  });

  const casesList: CaseItem[] = Array.isArray(casesData)
    ? casesData
    : casesData?.cases || [];

  const filteredCases = casesList.filter((item) => {
    const matchesSearch =
      (item.case_id || item.id || "").toLowerCase().includes(search.toLowerCase()) ||
      (item.transaction_id || "").toLowerCase().includes(search.toLowerCase()) ||
      (item.assigned_to || "").toLowerCase().includes(search.toLowerCase());

    const matchesStatus =
      statusFilter === "ALL" || item.status === statusFilter;

    return matchesSearch && matchesStatus;
  });

  const handleAssignAnalyst = async () => {
    if (!selectedCase || !newAnalyst) return;
    try {
      const caseId = selectedCase.case_id || selectedCase.id || selectedCase._id || "";
      await assignCase(caseId, newAnalyst);
      queryClient.invalidateQueries({ queryKey: ["cases"] });
      setIsAssignModalOpen(false);
      setNewAnalyst("");
    } catch (err: any) {
      alert("Failed to assign case: " + err.message);
    }
  };

  const handleUpdateStatus = async (item: CaseItem, newStatus: string) => {
    try {
      const caseId = item.case_id || item.id || item._id || "";
      await updateCase(caseId, newStatus);
      queryClient.invalidateQueries({ queryKey: ["cases"] });
    } catch (err: any) {
      alert("Failed to update status: " + err.message);
    }
  };

  const columns: Column<CaseItem>[] = [
    {
      key: "case_id",
      header: "Case ID",
      render: (row) => (
        <span className="font-mono text-xs text-indigo-300 font-semibold">
          {row.case_id || row.id || row._id || "CASE-8842"}
        </span>
      ),
    },
    {
      key: "transaction_id",
      header: "Transaction Ref",
      render: (row) => (
        <span className="font-mono text-xs text-slate-300">
          {row.transaction_id}
        </span>
      ),
    },
    {
      key: "risk_level",
      header: "Risk Tier",
      render: (row) => (
        <RiskBadge
          level={row.risk_level || "HIGH"}
          score={(row.risk_score || 85) / 100}
          size="sm"
        />
      ),
    },
    {
      key: "assigned_to",
      header: "Assigned Investigator",
      render: (row) => (
        <div className="flex items-center gap-1.5">
          <Badge variant={row.assigned_to ? "slate" : "amber"} size="sm">
            <UserCheck className="w-3 h-3" />
            {row.assigned_to || "Unassigned"}
          </Badge>
        </div>
      ),
    },
    {
      key: "status",
      header: "Investigation Status",
      render: (row) => {
        const variantMap: Record<string, "rose" | "amber" | "emerald" | "indigo" | "slate"> = {
          OPEN: "amber",
          UNDER_INVESTIGATION: "indigo",
          RESOLVED_FRAUD: "rose",
          RESOLVED_GENUINE: "emerald",
          DISMISSED: "slate",
        };
        return (
          <Badge variant={variantMap[row.status || "OPEN"] || "slate"} size="sm" dot>
            {(row.status || "OPEN").replace(/_/g, " ")}
          </Badge>
        );
      },
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
            onClick={() => setSelectedCase(row)}
          >
            Details
          </Button>

          <Button
            variant="outline"
            size="sm"
            leftIcon={<UserCheck className="w-3.5 h-3.5" />}
            onClick={() => {
              setSelectedCase(row);
              setIsAssignModalOpen(true);
            }}
          >
            Assign
          </Button>
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
          title="Failed to Load Incident Cases"
          message={(error as Error)?.message || "Server case management service unreachable."}
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
            Fraud Incident Case Management
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Escalated fraud cases, analyst assignments, and security resolution workflows
          </p>
        </div>
      </div>

      {/* Filter Controls */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-2xl bg-slate-900/70 border border-slate-800/80 backdrop-blur-xl">
        <div className="w-full sm:w-72">
          <Input
            placeholder="Filter by Case ID, Ref, or Analyst..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            leftIcon={<Search className="w-4 h-4" />}
          />
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <Select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            options={[
              { value: "ALL", label: "All Statuses" },
              { value: "OPEN", label: "Open Cases" },
              { value: "UNDER_INVESTIGATION", label: "Under Investigation" },
              { value: "RESOLVED_FRAUD", label: "Resolved Fraud" },
              { value: "RESOLVED_GENUINE", label: "Resolved Genuine" },
              { value: "DISMISSED", label: "Dismissed" },
            ]}
          />
        </div>
      </div>

      {/* Data Table */}
      <Table
        columns={columns}
        data={filteredCases}
        emptyTitle="No Incident Cases Matched"
        emptyDescription="There are currently no active cases matching your filter parameters."
        onRowClick={(row) => setSelectedCase(row)}
      />

      {/* Reassign Analyst Modal */}
      <Modal
        isOpen={isAssignModalOpen}
        onClose={() => setIsAssignModalOpen(false)}
        title="Assign Case to Analyst"
        subtitle={`Case ID: ${selectedCase?.case_id || selectedCase?.id || "CASE-8842"}`}
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
            placeholder="e.g. analyst_john@company.com"
            value={newAnalyst}
            onChange={(e) => setNewAnalyst(e.target.value)}
            leftIcon={<UserCheck className="w-4 h-4" />}
            autoFocus
          />
        </div>
      </Modal>

      {/* Case Details Drawer */}
      <Drawer
        isOpen={Boolean(selectedCase) && !isAssignModalOpen}
        onClose={() => setSelectedCase(null)}
        title={
          <div className="flex items-center gap-2">
            <FolderGit2 className="w-5 h-5 text-indigo-400" />
            <span>Case Inspection Panel</span>
          </div>
        }
        subtitle={`ID: ${selectedCase?.case_id || selectedCase?.id || selectedCase?._id}`}
      >
        {selectedCase && (
          <div className="space-y-6">
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase">
                  Transaction Reference
                </span>
                <span className="font-mono text-sm text-indigo-300 font-bold">
                  {selectedCase.transaction_id}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase">
                  Assigned Investigator
                </span>
                <Badge variant="indigo" size="sm">
                  {selectedCase.assigned_to || "Unassigned"}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-400 uppercase">
                  Risk Level
                </span>
                <RiskBadge level={selectedCase.risk_level || "HIGH"} score={0.85} size="sm" />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-300 block">
                Update Investigation Status
              </label>
              <div className="grid grid-cols-1 gap-2">
                {[
                  { status: "UNDER_INVESTIGATION", label: "Mark Under Investigation", color: "indigo" },
                  { status: "RESOLVED_FRAUD", label: "Confirm Confirmed Fraud", color: "rose" },
                  { status: "RESOLVED_GENUINE", label: "Confirm Genuine Customer", color: "emerald" },
                  { status: "DISMISSED", label: "Dismiss Case", color: "slate" },
                ].map((st) => (
                  <Button
                    key={st.status}
                    variant={selectedCase.status === st.status ? "primary" : "outline"}
                    size="sm"
                    fullWidth
                    onClick={() => {
                      handleUpdateStatus(selectedCase, st.status);
                      setSelectedCase({ ...selectedCase, status: st.status });
                    }}
                  >
                    {st.label}
                  </Button>
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-300 block">
                Investigation Notes
              </label>
              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 text-xs text-slate-300 leading-relaxed font-mono">
                {selectedCase.investigation_notes ||
                  "Initial anomaly flagged by CatBoost model due to velocity & geo mismatch."}
              </div>
            </div>
          </div>
        )}
      </Drawer>
    </div>
  );
}