import { useLocation, Link } from "react-router-dom";

const routeLabels: Record<string, string> = {
  dashboard: "Dashboard",
  prediction: "Predict",
  history: "History",
  alerts: "Alerts",
  cases: "Cases",
  users: "Users",
  analytics: "Analytics",
  reports: "Reports",
  settings: "Settings",
  models: "Models",
  login: "Login",
  register: "Register",
  explanation: "Explanation",
};

export default function Breadcrumbs() {
  const location = useLocation();
  const pathParts = location.pathname.replace(/^\/|\/$/g, "").split("/").filter(Boolean);

  if (pathParts.length === 0) return null;

  return (
    <nav className="breadcrumbs" aria-label="Breadcrumb">
      <Link to="/dashboard">Home</Link>
      {pathParts.map((part, index) => {
        const label = routeLabels[part] || part.charAt(0).toUpperCase() + part.slice(1);
        const isLast = index === pathParts.length - 1;
        return (
          <span key={part}>
            <span className="separator">/</span>
            {isLast ? (
              <span className="current">{label}</span>
            ) : (
              <Link to={`/${pathParts.slice(0, index + 1).join("/")}`}>{label}</Link>
            )}
          </span>
        );
      })}
    </nav>
  );
}