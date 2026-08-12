import api from "../apiClient";

export async function getAlerts() {
    const response = await api.get("/alerts");
    return response.data;
}

export async function assignAlert(
    id: string,
    analyst: string
) {
    const response = await api.patch(`/alerts/${id}/assign`, {
        assigned_to: analyst
    });
    return response.data;
}

export async function updateAlert(
    id: string,
    status: string
) {
    const response = await api.patch(`/alerts/${id}/status`, {
        status
    });
    return response.data;
}