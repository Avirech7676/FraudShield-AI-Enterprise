import api from "../apiClient";

export async function getUsers() {
  const response = await api.get("/users");
  const data = response.data;
  if (Array.isArray(data)) return data;
  if (data && Array.isArray(data.users)) return data.users;
  return [];
}

export async function updateUserRole(username: string, role: string) {
  const response = await api.patch(`/users/${username}/role`, { role });
  return response.data;
}

export async function deleteUser(username: string) {
  const response = await api.delete(`/users/${username}`);
  return response.data;
}