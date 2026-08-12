import api from "../apiClient";

export async function getNotifications() {
    const response = await api.get("/notifications");
    return response.data;
}

export async function getUnreadCount() {
    const response = await api.get("/notifications/unread-count");
    return response.data;
}

export async function markAsRead(notificationId) {
    const response = await api.patch(`/notifications/${notificationId}/read`);
    return response.data;
}

export async function markAllAsRead() {
    const response = await api.patch("/notifications/read-all");
    return response.data;
}

export async function deleteNotification(notificationId) {
    const response = await api.delete(`/notifications/${notificationId}`);
    return response.data;
}