import { useEffect, useState } from "react";
import { getNotifications, markAsRead, markAllAsRead, deleteNotification, getUnreadCount } from "../../services/notifications";
import { useAuth } from "../../hooks/useAuth";

export interface NotificationCenterProps {
  onClose?: () => void;
}

export default function NotificationCenter({ onClose }: NotificationCenterProps) {
  const { user } = useAuth();
  const [notifications, setNotifications] = useState<any[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);

  const handleClose = () => {
    onClose?.();
  };

  useEffect(() => {
    if (user) {
      fetchNotifications();
    }
  }, [user]);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const data = await getNotifications();
      setNotifications(data);

      const countData = await getUnreadCount();
      setUnreadCount(countData.count);
    } catch (error) {
      console.error("Failed to fetch notifications:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleMarkAsRead = async (id: string) => {
    try {
      await markAsRead(id);
      await fetchNotifications();
    } catch (error) {
      console.error("Failed to mark notification as read:", error);
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      await markAllAsRead();
      await fetchNotifications();
    } catch (error) {
      console.error("Failed to mark all notifications as read:", error);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteNotification(id);
      await fetchNotifications();
    } catch (error) {
      console.error("Failed to delete notification:", error);
    }
  };

  if (loading) {
    return (
      <div className="notification-dropdown">
        <div className="notification-header">
          <h3>Notifications</h3>
          <button onClick={handleClose}>×</button>
        </div>
        <div className="notification-loading">Loading notifications...</div>
      </div>
    );
  }

  return (
    <div className="notification-dropdown">
      <div className="notification-header">
        <div>
          <span>🔔</span>
          <h3>Notifications ({unreadCount} unread)</h3>
        </div>
        <button onClick={handleClose}>×</button>
      </div>

      {notifications.length === 0 ? (
        <div className="notification-empty">
          <p>No notifications</p>
        </div>
      ) : (
        <div className="notification-list">
          {notifications.map((notification: any) => (
            <div
              key={notification.id}
              className={`notification-item ${!notification.read ? 'unread' : ''}`}
            >
              <div className="notification-content">
                <div className="notification-title">{notification.title}</div>
                <div className="notification-message">{notification.message}</div>
                <div className="notification-time">
                  {new Date(notification.createdAt).toLocaleString()}
                </div>
              </div>
              <div className="notification-actions">
                {!notification.read && (
                  <button
                    onClick={() => handleMarkAsRead(notification.id)}
                    className="btn btn-sm btn-outline-primary"
                  >
                    Mark as Read
                  </button>
                )}
                <button
                  onClick={() => handleDelete(notification.id)}
                  className="btn btn-sm btn-outline-danger"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}

          <div className="notification-footer">
            <button
              onClick={handleMarkAllAsRead}
              className="btn btn-sm btn-outline-secondary"
              disabled={unreadCount === 0}
            >
              Mark All as Read
            </button>
          </div>
        </div>
      )}
    </div>
  );
}