import { useState } from "react";
import { useLocation } from "react-router-dom";
import NotificationCenter from "../common/NotificationCenter";
import ProfileDropdown from "../common/ProfileDropdown";
import { useTheme } from "../../context/ThemeContext";

const pageTitles: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/prediction": "Transaction Prediction",
  "/history": "Prediction History",
  "/alerts": "Alerts",
  "/cases": "Cases",
  "/analytics": "Analytics",
  "/reports": "Reports",
  "/settings": "Settings",
  "/models": "Model Registry",
  "/users": "User Management",
};

export default function Navbar() {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();
  const [search, setSearch] = useState("");
  const [notificationDrawerOpen, setNotificationDrawerOpen] = useState(false);

  const pageTitle = pageTitles[location.pathname] || "FraudShield";

  const toggleSidebar = () => {
    document.documentElement.classList.toggle("sidebar-open");
  };

  return (
    <header className="navbar">
      <div className="navbar-left">
        <button className="btn btn-icon" onClick={toggleSidebar} title="Toggle menu" style={{ display: 'none' }}>
          ☰
        </button>
        <span className="navbar-page-title">{pageTitle}</span>
      </div>

      <div className="navbar-search">
        <span className="search-icon">⌕</span>
        <input
          placeholder="Search transactions, customers..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="navbar-right">
        <button className="navbar-btn" onClick={toggleTheme} title={theme === "dark" ? "Light mode" : "Dark mode"}>
          {theme === "dark" ? "☀" : "☾"}
        </button>

        <div className="notification-dropdown">
          <button
            className="navbar-btn"
            onClick={() => setNotificationDrawerOpen(!notificationDrawerOpen)}
            title="Notifications"
          >
            ◷
            <span className="indicator" />
          </button>
          {notificationDrawerOpen && (
            <NotificationCenter onClose={() => setNotificationDrawerOpen(false)} />
          )}
        </div>

        <ProfileDropdown />
      </div>
    </header>
  );
}