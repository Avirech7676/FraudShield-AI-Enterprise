import api from "../apiClient";

export async function getHistory(params: { filters?: any; skip?: number; limit?: number } = {}) {
  const { filters = {}, skip = 0, limit = 100 } = params;
  const response = await api.get("/predictions", { params: { ...filters, skip, limit } });
  const data = response.data;
  
  if (Array.isArray(data)) {
    return data;
  }
  if (data && Array.isArray(data.predictions)) {
    return data.predictions;
  }
  if (data && Array.isArray(data.items)) {
    return data.items;
  }
  return [];
}