import { useQuery } from "@tanstack/react-query";
import { getRecentActivity } from "../../services/activityService";

export function ActivityTimeline() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["recent-activity"],
    queryFn: getRecentActivity,
  });

  if (isLoading) return <div className="timeline-loading">Loading activity timeline...</div>;
  if (error) return <div className="timeline-error">Error loading activity: {(error as Error).message}</div>;

  const activities = data || [];

  return (
    <div className="activity-timeline">
      <h2>Recent Activity</h2>
      <div className="timeline-container">
        {activities.length === 0 ? (
          <div className="timeline-empty">
            <p>No recent activity</p>
          </div>
        ) : (
          <div className="timeline-items">
            {activities.map((activity: any, index: number) => (
              <div key={activity.id || index} className={`timeline-item ${activity.type === 'error' ? 'timeline-error' : activity.type === 'warning' ? 'timeline-warning' : 'timeline-info'}`}>
                <div className="timeline-marker"></div>
                <div className="timeline-content">
                  <div className="timeline-header">
                    <span className="timeline-icon">{getActivityIcon(activity.type)}</span>
                    <span className="timeline-title">{activity.title}</span>
                    <span className="timeline-time">{new Date(activity.timestamp).toLocaleTimeString()}</span>
                  </div>
                  <p className="timeline-description">{activity.description}</p>
                  {activity.details && (
                    <div className="timeline-details">
                      <small>{activity.details}</small>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// Helper functions
function getActivityIcon(type: string): string {
  const icons: Record<string, string> = {
    info: "ℹ️",
    success: "✅",
    warning: "⚠️",
    error: "❌",
    transaction: "💳",
    login: "👤",
    logout: "👋",
    model: "🤖",
    report: "📊",
    upload: "📤",
    download: "📥"
  };
  return icons[type] || "•";
}