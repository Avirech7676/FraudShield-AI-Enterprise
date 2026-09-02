import { useQuery } from "@tanstack/react-query";
import { getRecentActivity } from "../../services/activityService";

export function ActivityTimeline() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["recent-activity"],
    queryFn: getRecentActivity,
  });

  if (isLoading) {
    return (
      <div className="card">
        <div className="card-header"><h3>Recent Activity</h3></div>
        <div className="card-body">
          <div className="skeleton skeleton-line" />
          <div className="skeleton skeleton-line" />
          <div className="skeleton skeleton-line" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <div className="card-header"><h3>Recent Activity</h3></div>
        <div className="card-body">
          <p style={{ color: "var(--red)", fontSize: 13, margin: 0 }}>
            Could not load activity data
          </p>
        </div>
      </div>
    );
  }

  const activities = data?.activities || [];

  return (
    <div className="card">
      <div className="card-header">
        <h3>Recent Activity</h3>
        {activities.length > 0 && (
          <span className="badge badge-neutral">{activities.length} events</span>
        )}
      </div>
      <div className="card-body">
        {activities.length === 0 ? (
          <p style={{ color: "var(--text-muted)", fontSize: 13, margin: 0, textAlign: "center", padding: 20 }}>
            No recent activity recorded
          </p>
        ) : (
          <div className="timeline">
            {activities.map((activity: any) => (
              <div key={activity.id} className="timeline-item">
                <div className="timeline-time">
                  {new Date(activity.timestamp).toLocaleString()}
                </div>
                <div className="timeline-title">{activity.title}</div>
                {activity.description && (
                  <div className="timeline-desc">{activity.description}</div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}