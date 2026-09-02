import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { getAuditLogs } from "../../services/auditLogService";
import type { AuditLogItem } from "../../types/auditLog";

export interface AuditLogFilters {
  page?: number;
  limit?: number;
  userId?: string;
  action?: string;
  startDate?: string;
  endDate?: string;
  search?: string;
}

export default function AuditLogViewer() {
  const queryClient = useQueryClient();
  const [filters, setFilters] = useState<AuditLogFilters>({
    page: 1,
    limit: 20,
    userId: "",
    action: "",
    startDate: "",
    endDate: "",
    search: "",
  });

  const {
    data: auditLogs,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["audit-logs", filters],
    queryFn: () => getAuditLogs(filters),
    refetchInterval: false,
  });

  const handleFiltersChange = (newFilters: Partial<AuditLogFilters>) => {
    setFilters((prev) => ({ ...prev, ...newFilters, page: 1 }));
  };

  const handlePageChange = (newPage: number) => {
    setFilters((prev) => ({ ...prev, page: newPage }));
  };

  const handleRefresh = () => {
    queryClient.invalidateQueries({ queryKey: ["audit-logs", filters] });
  };

  if (isLoading) return <div className="audit-log-loading">Loading audit logs...</div>;
  if (error) return <div className="audit-log-error">Error loading audit logs: {(error as Error).message}</div>;

  const logs: AuditLogItem[] = (auditLogs as any)?.logs || [];
  const pagination = (auditLogs as any)?.pagination || { total: 0, page: 1, limit: 20, hasNext: false, hasPrev: false };

  return (
    <div className="audit-log-viewer">
      <div className="audit-log-header">
        <h2>Audit Logs</h2>
        <div className="audit-log-actions">
          <button onClick={handleRefresh} className="btn btn-outline-primary btn-sm">
            Refresh
          </button>
        </div>
      </div>

      <div className="audit-log-filters">
        <div className="filters-row">
          <div className="filter-group">
            <label>User ID:</label>
            <input
              type="text"
              value={filters.userId || ""}
              onChange={(e) => handleFiltersChange({ userId: e.target.value })}
              placeholder="Filter by user ID"
              className="filter-input"
            />
          </div>

          <div className="filter-group">
            <label>Action:</label>
            <select
              value={filters.action || ""}
              onChange={(e) => handleFiltersChange({ action: e.target.value })}
              className="filter-select"
            >
              <option value="">All Actions</option>
              <option value="user_login">User Login</option>
              <option value="user_logout">User Logout</option>
              <option value="user_created">User Created</option>
              <option value="user_updated">User Updated</option>
              <option value="user_deleted">User Deleted</option>
              <option value="password_changed">Password Changed</option>
              <option value="transaction_created">Transaction Created</option>
              <option value="transaction_updated">Transaction Updated</option>
              <option value="fraud_status_changed">Fraud Status Changed</option>
              <option value="model_trained">Model Trained</option>
              <option value="settings_updated">Settings Updated</option>
            </select>
          </div>

          <div className="filter-group">
            <label>Date From:</label>
            <input
              type="date"
              value={filters.startDate || ""}
              onChange={(e) => handleFiltersChange({ startDate: e.target.value })}
              className="filter-input"
            />
          </div>

          <div className="filter-group">
            <label>Date To:</label>
            <input
              type="date"
              value={filters.endDate || ""}
              onChange={(e) => handleFiltersChange({ endDate: e.target.value })}
              className="filter-input"
            />
          </div>

          <div className="filter-group">
            <label>Search:</label>
            <input
              type="text"
              value={filters.search || ""}
              onChange={(e) => handleFiltersChange({ search: e.target.value })}
              placeholder="Search in descriptions"
              className="filter-input"
            />
          </div>
        </div>
      </div>

      <div className="audit-log-table">
        <table className="audit-table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>User</th>
              <th>Action</th>
              <th>Resource</th>
              <th>Description</th>
              <th>IP Address</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center">
                  No audit logs found matching the current filters
                </td>
              </tr>
            ) : (
              logs.map((log: any) => (
                <tr key={log.id} className={!log.success ? "table-danger" : ""}>
                  <td>{new Date(log.timestamp).toLocaleString()}</td>
                  <td>
                    {log.username || log.user_email || "System"}
                    <br />
                    <small className="text-muted">{log.user_id}</small>
                  </td>
                  <td>
                    <span className={`badge bg-${getActionBadgeColor(log.action)}`}>
                      {formatActionName(log.action)}
                    </span>
                  </td>
                  <td>
                    {log.resource_type || "-"}
                    <br />
                    <small className="text-muted">{log.resource_id || ""}</small>
                  </td>
                  <td title={log.description || ""}>
                    {(log.description || "").length > 50
                      ? (log.description || "").substring(0, 50) + "..."
                      : log.description || ""}
                  </td>
                  <td>{log.ip_address || "-"}</td>
                  <td>
                    <span className={`badge bg-${log.success ? "success" : "danger"}`}>
                      {log.success ? "Success" : "Failed"}
                    </span>
                    {!log.success && log.error_message && (
                      <div className="small text-danger mt-1">{log.error_message}</div>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="audit-log-pagination">
        <nav aria-label="Audit logs pagination">
          <ul className="pagination">
            <li className={`page-item ${!pagination.hasPrev ? "disabled" : ""}`}>
              <button className="page-link" onClick={() => handlePageChange(pagination.page - 1)}>
                Previous
              </button>
            </li>

            {Array.from({ length: Math.min(5, pagination.total || 1) }, (_, i) => {
              const pageNum = i + 1;
              return (
                <li key={pageNum} className={`page-item ${pageNum === pagination.page ? "active" : ""}`}>
                  <button className="page-link" onClick={() => handlePageChange(pageNum)}>
                    {pageNum}
                  </button>
                </li>
              );
            })}

            <li className={`page-item ${!pagination.hasNext ? "disabled" : ""}`}>
              <button className="page-link" onClick={() => handlePageChange(pagination.page + 1)}>
                Next
              </button>
            </li>
          </ul>
        </nav>

        <div className="pagination-info">
          Showing {(pagination.page - 1) * pagination.limit + 1}-
          {Math.min(pagination.page * pagination.limit, pagination.total)} of {pagination.total} entries
        </div>
      </div>
    </div>
  );
}

function getActionBadgeColor(action: string): string {
  const colorMap: Record<string, string> = {
    user_login: "success",
    user_logout: "secondary",
    user_created: "success",
    user_updated: "info",
    user_deleted: "danger",
    password_changed: "warning",
    transaction_created: "primary",
    transaction_updated: "info",
    fraud_status_changed: "warning",
    model_trained: "success",
    model_deployed: "success",
    settings_updated: "secondary",
  };
  return colorMap[action] || "secondary";
}

function formatActionName(action: string): string {
  return action
    .split("_")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}