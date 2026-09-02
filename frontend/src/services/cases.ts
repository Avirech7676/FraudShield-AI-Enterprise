import api from "../apiClient";

export async function getCases() {
    const response = await api.get("/cases");
    return response.data;
}

export async function assignCase(
    id: string,
    analyst: string
) {
    const response = await api.patch(`/cases/${id}/assign`, {
        assigned_to: analyst
    });
    return response.data;
}

export async function updateCase(
    id: string,
    status: string
) {
    const response = await api.patch(`/cases/${id}/status`, {
        status
    });
    return response.data;
}