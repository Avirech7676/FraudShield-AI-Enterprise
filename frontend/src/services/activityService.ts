import api from "../apiClient";

export async function getRecentActivity() {
    const response = await api.get("/activity/recent");
    return response.data;
}