import AuditLogViewer from "../components/audit/AuditLogViewer";

export function AuditLogsPage() {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Audit Logs</h1>
        <p>Complete audit trail of all system activities</p>
      </div>
      <AuditLogViewer />
    </div>
  );
}