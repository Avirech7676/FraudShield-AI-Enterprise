export const EmptyState = ({
  icon = "📭",
  title = "No Data Available",
  subtitle = "There's nothing to show here yet.",
  actionText,
  onAction,
  className = "",
}) => {
  return (
    <div className={`empty-state ${className}`} style={{ textAlign: "center", padding: "40px 20px" }}>
      <div className="empty-state-icon" style={{ fontSize: "48px", marginBottom: "16px" }}>
        {icon}
      </div>
      <h3 className="empty-state-title" style={{ marginBottom: "8px", color: "#374151" }}>
        {title}
      </h3>
      <p className="empty-state-subtitle" style={{ color: "#6b7280", marginBottom: "24px" }}>
        {subtitle}
      </p>
      {actionText && (
        <button
          onClick={onAction}
          className="empty-state-action"
          style={{
            backgroundColor: "#3b82f6",
            color: "white",
            border: "none",
            padding: "8px 16px",
            borderRadius: "4px",
            cursor: "pointer",
            fontWeight: "500",
          }}
        >
          {actionText}
        </button>
      )}
    </div>
  );
};

export default EmptyState;