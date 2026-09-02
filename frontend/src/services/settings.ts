import api from "../apiClient";

export async function getSettings() {
  const response = await api.get("/settings");
  return response.data;
}

export async function getSystem() {
  const response = await api.get("/settings/system");
  return response.data;
}

export async function getHealth() {
  const response = await api.get("/settings/health");
  return response.data;
}

export async function reloadModel() {
  const response = await api.post("/settings/reload-model");
  return response.data;
}

export async function clearCache() {
  const response = await api.post("/settings/clear-cache");
  return response.data;
}

export async function restartEngine() {
  const response = await api.post("/settings/restart-engine");
  return response.data;
}