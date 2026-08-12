import { API_BASE_URL } from "./api";

export async function apiClient(
    endpoint: string,
    options: RequestInit = {}
) {
    const token = localStorage.getItem("token");

    const headers: HeadersInit = {
        "Content-Type": "application/json",
        ...(options.headers || {}),
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(
        `${API_BASE_URL}${endpoint}`,
        {
            ...options,
            headers,
        }
    );

    if (response.status === 401) {
        localStorage.clear();
        window.location.href = "/login";
        throw new Error("Session Expired");
    }

    if (!response.ok) {
        let message = "Request Failed";

        try {
            const error = await response.json();
            message =
                error.detail ||
                error.message ||
                message;
        }
        catch {}

        throw new Error(message);
    }

    return response;
}