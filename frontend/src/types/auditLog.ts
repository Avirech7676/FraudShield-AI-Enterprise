export interface AuditLogItem {
  id: string;
  timestamp: string;
  user: string;
  action: string;
  resource: string;
  details: string;
  ip_address?: string;
  status: "success" | "warning" | "error" | string;
}

export interface AuditLogResponse {
  logs: AuditLogItem[];
  pagination: {
    total: number;
    page: number;
    limit: number;
    pages: number;
  };
}
