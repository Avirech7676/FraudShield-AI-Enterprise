import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { getModels, deployModel, rollbackModel, type ModelInfo } from "../services/modelService";
import { Table, type Column } from "../components/ui/Table";
import { Badge } from "../components/ui/Badge";
import { Skeleton } from "../components/ui/Skeleton";
import { ErrorState } from "../components/ui/ErrorState";
import { Cpu, RotateCcw, Rocket, CheckCircle2 } from "lucide-react";

export default function ModelManagement() {
  const queryClient = useQueryClient();
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const { data: modelsList = [], isLoading, isError, error, refetch } = useQuery({
    queryKey: ["models-registry"],
    queryFn: getModels,
  });

  const activeProduction = modelsList.find((m) => m.status === "PRODUCTION") || modelsList[0];

  const handleDeploy = async (model: ModelInfo) => {
    setActionLoading(`deploy-${model.version}`);
    try {
      await deployModel(model.version, model.model_name);
      queryClient.invalidateQueries({ queryKey: ["models-registry"] });
    } catch (err: any) {
      alert(`Failed to deploy model v${model.version}: ${err.message}`);
    } finally {
      setActionLoading(null);
    }
  };

  const handleRollback = async () => {
    setActionLoading("rollback");
    try {
      await rollbackModel();
      queryClient.invalidateQueries({ queryKey: ["models-registry"] });
    } catch (err: any) {
      alert(`Rollback failed: ${err.message}`);
    } finally {
      setActionLoading(null);
    }
  };

  const columns: Column<ModelInfo>[] = [
    {
      key: "model_name",
      header: "Model Architecture",
      render: (row) => (
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <Cpu size={16} color="#818cf8" />
          <span style={{ fontWeight: 600, color: "#f1f5f9" }}>{row.model_name}</span>
        </div>
      ),
    },
    {
      key: "version",
      header: "Version",
      render: (row) => (
        <span style={{ fontFamily: "var(--font-mono)", fontSize: 12, fontWeight: 700, color: "#818cf8" }}>
          v{row.version}
        </span>
      ),
    },
    {
      key: "accuracy",
      header: "Accuracy",
      render: (row) => (
        <span style={{ fontWeight: 600, color: "#34d399" }}>
          {row.accuracy}%
        </span>
      ),
    },
    {
      key: "f1_score",
      header: "F1 Score",
      render: (row) => (
        <span style={{ fontFamily: "var(--font-mono)", color: "#cbd5e1" }}>
          {row.f1_score}%
        </span>
      ),
    },
    {
      key: "roc_auc",
      header: "ROC AUC",
      render: (row) => (
        <span style={{ fontFamily: "var(--font-mono)", color: "#e2e8f0", fontWeight: 600 }}>
          {row.roc_auc}
        </span>
      ),
    },
    {
      key: "status",
      header: "Status",
      render: (row) => (
        <Badge
          variant={row.status === "PRODUCTION" ? "emerald" : "indigo"}
          size="sm"
          dot={row.status === "PRODUCTION"}
          pulse={row.status === "PRODUCTION"}
        >
          {row.status}
        </Badge>
      ),
    },
    {
      key: "actions",
      header: "Deploy Action",
      align: "right",
      render: (row) => (
        <div style={{ display: "flex", alignItems: "center", justifyContent: "flex-end", gap: 8 }}>
          {row.status === "PRODUCTION" ? (
            <span style={{ fontSize: 12, color: "#10b981", fontWeight: 600, display: "flex", alignItems: "center", gap: 4 }}>
              <CheckCircle2 size={14} /> Active Engine
            </span>
          ) : (
            <button
              className="btn-primary"
              style={{ padding: "5px 12px", fontSize: 12 }}
              disabled={actionLoading === `deploy-${row.version}`}
              onClick={() => handleDeploy(row)}
            >
              <Rocket size={13} />
              Deploy to Prod
            </button>
          )}
        </div>
      ),
    },
  ];

  if (isLoading) {
    return (
      <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
        <Skeleton variant="rectangular" className="h-40 w-full" />
        <Skeleton variant="rectangular" className="h-96 w-full" />
      </div>
    );
  }

  if (isError) {
    return (
      <div style={{ padding: "40px 0" }}>
        <ErrorState
          title="Model Registry Unavailable"
          message={(error as Error)?.message || "Failed to query ML model registry."}
          onRetry={() => refetch()}
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
            <Cpu size={18} color="#818cf8" />
          </div>
          <div>
            <h2 style={{ fontSize: 16, fontWeight: 700, color: "#f1f5f9", margin: 0 }}>
              ML Model Registry &amp; Lifecycle Management
            </h2>
            <p style={{ fontSize: 12, color: "#475569", margin: "2px 0 0" }}>
              CatBoost ensemble model versions, accuracy benchmarking, and instant zero-downtime deployment
            </p>
          </div>
        </div>

        <button
          className="btn-danger"
          style={{ padding: "7px 14px", fontSize: 12 }}
          disabled={actionLoading === "rollback"}
          onClick={handleRollback}
        >
          <RotateCcw size={13} className={actionLoading === "rollback" ? "animate-spin" : ""} />
          Rollback Model Version
        </button>
      </div>

      {/* Production Hero Banner */}
      {activeProduction && (
        <div className="fs-card" style={{ padding: 24, background: "linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(16,185,129,0.08) 100%)", border: "1px solid rgba(99,102,241,0.25)" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, flexWrap: "wrap" }}>
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
                <span className="status-dot online" />
                <span style={{ fontSize: 11, fontWeight: 700, color: "#10b981", letterSpacing: "0.1em", textTransform: "uppercase" }}>Active Production Deployment</span>
              </div>
              <h3 style={{ fontSize: 20, fontWeight: 800, color: "#f1f5f9", letterSpacing: "-0.02em", margin: 0 }}>
                {activeProduction.model_name} <span style={{ color: "#818cf8" }}>v{activeProduction.version}</span>
              </h3>
              <p style={{ fontSize: 12, color: "#64748b", marginTop: 4 }}>
                Artifact Path: <span style={{ fontFamily: "var(--font-mono)", color: "#94a3b8" }}>{activeProduction.model_path}</span>
              </p>
            </div>

            <div style={{ display: "flex", gap: 16 }}>
              <div style={{ textAlign: "center", padding: "10px 18px", borderRadius: 10, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}>
                <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.06em" }}>Accuracy</div>
                <div style={{ fontSize: 20, fontWeight: 800, color: "#34d399" }}>{activeProduction.accuracy}%</div>
              </div>
              <div style={{ textAlign: "center", padding: "10px 18px", borderRadius: 10, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}>
                <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.06em" }}>ROC AUC</div>
                <div style={{ fontSize: 20, fontWeight: 800, color: "#818cf8" }}>{activeProduction.roc_auc}</div>
              </div>
              <div style={{ textAlign: "center", padding: "10px 18px", borderRadius: 10, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}>
                <div style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: "0.06em" }}>F1 Score</div>
                <div style={{ fontSize: 20, fontWeight: 800, color: "#fbbf24" }}>{activeProduction.f1_score}%</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Registry Table */}
      <div className="fs-card" style={{ overflow: "hidden" }}>
        <Table columns={columns} data={modelsList} emptyTitle="No models in registry" />
      </div>
    </div>
  );
}