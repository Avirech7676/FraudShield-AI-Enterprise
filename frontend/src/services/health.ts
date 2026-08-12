import api from "../apiClient";

import type { HealthResponse } from "../types/dashboard.ts";

export async function getHealth(): Promise<HealthResponse> {
  const response = await api.get("/health");
  return response.data;
}