import api from "../apiClient";

export async function predict(
    payload: any
) {
    const response = await api.post("/predict", payload);
    return response.data;
}