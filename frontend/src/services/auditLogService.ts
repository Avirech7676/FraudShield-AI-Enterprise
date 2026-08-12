import api from "../apiClient";

export interface AuditLogFilters {
  page?: number;
  limit?: number;
  userId?: string;
  action?: string;
  startDate?: string;
  endDate?: string;
  search?: string;
}

export interface AuditLogResponse {
  logs: Array<any>;
  pagination: {
    total: number;
    page: number;
    limit: number;
    hasNext: boolean;
    hasPrev: boolean;
  };
}

export async function getAuditLogs(filters: AuditLogFilters): Promise<AuditLogResponse> {
    // Build query parameters
    const params: Record<string, any> = {};

    if (filters.page) params.page = filters.page;
    if (filters.limit) params.limit = filters.limit;
    if (filters.userId) params.userId = filters.userId;
    if (filters.action) params.action = filters.action;
    if (filters.startDate) params.startDate = filters.startDate;
    if (filters.endDate) params.endDate = filters.endDate;
    if (filters.search) params.search = filters.search;

    const response = await api.get("/audit-logs", { params });
    return response.data;
}

export async function getAuditLogStats() {
    const response = await api.get("/audit-logs/stats");
    return response.data;
}