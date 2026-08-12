import { useEffect, useState } from "react";
import { useAuth } from "../../hooks/useAuth";

export default function NotificationBadge() {
  const [count, setCount] = useState(0);
  const { user } = useAuth();

  useEffect(() => {
    // In a real app, this would fetch from an API endpoint
    // For now, we'll simulate with a random number or use mock data
    const fetchNotifications = async () => {
      try {
        // This would normally be an API call
        // const response = await api.get("/notifications/unread-count");
        // setCount(response.data.count);

        // For demo purposes, we'll set a random number or use a mock
        // In development, you might want to simulate some notifications
        setCount(Math.floor(Math.random() * 10)); // Random 0-9
      } catch (error) {
        console.error("Failed to fetch notification count:", error);
        setCount(0);
      }
    };

    if (user) {
      fetchNotifications();
    }
  }, [user]);

  return (
    <div className="notification-badge">
      <span>🔔</span>
      {count > 0 && (
        <span className="notification-count">{count}</span>
      )}
    </div>
  );
}