import api from "../apiClient";

export interface ReportRequest {
  report_type: string;
  format?: string;
  filters?: Record<string, any>;
}

export async function generateReport(request: ReportRequest) {
  const response = await api.post("/reports/generate", request, {
    // We need to handle binary responses
    responseType: "blob", // This will give us a Blob object
  });
  return response.data;
}

export async function getReportHistory() {
  const response = await api.get("/reports/history");
  return response.data;
}