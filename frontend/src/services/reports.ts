import api from "../apiClient";

export async function generateReport(data: { report_type: string; format?: string; filters?: any }) {
  const response = await api.post("/reports/generate", data, {
    responseType: data.format && data.format !== "json" ? "blob" : "json",
  });
  return response.data;
}

export async function getReports() {
  const response = await api.get("/reports/history");
  return response.data;
}
