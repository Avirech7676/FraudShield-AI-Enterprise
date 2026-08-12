import { useState, useEffect } from "react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

const navItems = [
  { to: "/dashboard", label: "Dashboard", icon: "◉" },
  { to: "/prediction", label: "Predict", icon: "◆" },
  { to: "/history", label: "History", icon: "≡" },
  { to: "/alerts", label: "Alerts", icon: "△" },
  { to: "/cases", label: "Cases", icon: "○" },
  { to: "/analytics", label: "Analytics", icon: "▣" },
  { to: "/reports", label: "Reports", icon: "◇" },
  { to: "/models", label: "Models", icon: "⊕" },
  { to: "/settings", label: "Settings", icon: "⊙" },
];

export default function Sidebar() {
  const { user, logout } = useAuth();
  const role = user?.role;
  const [isCollapsed, setIsCollapsed] = useState(false);

  useEffect(() => {
    const checkScreenSize = () => {
      if (window.innerWidth < 768) {
        setIsCollapsed(true);
      }
    };
    checkScreenSize();
    window.addEventListener("resize", checkScreenSize);
    return () => window.removeEventListener("resize", checkScreenSize);
  }, []);

  const handleLogout = () => {
    logout();
    window.location.href = "/login";
  };

  return (
    <aside className={`sidebar ${isCollapsed ? "collapsed" : ""}`}>
      <div className="sidebar-brand">
        <div className="brand-icon">FS</div>
        {!isCollapsed && (
          <div className="brand-name">
            FraudShield
            <small>Enterprise Platform</small>
          </div>
        )}
      </div>

      <button
        className="sidebar-toggle"
        onClick={() => setIsCollapsed(!isCollapsed)}
        title={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
      >
        {isCollapsed ? "→" : "←"}
      </button>

      <nav className="sidebar-nav">
        {!isCollapsed && <div className="nav-section-label">Main</div>}

        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end
            className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}
          >
            <span className="nav-icon">{item.icon}</span>
            {!isCollapsed && <span className="nav-text">{item.label}</span>}
          </NavLink>
        ))}

        {role === "Admin" && (
          <>
            {!isCollapsed && <div className="nav-section-label">Admin</div>}
            <NavLink
              to="/users"
              end
              className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}
            >
              <span className="nav-icon">✦</span>
              {!isCollapsed && <span className="nav-text">Users</span>}
            </NavLink>
          </>
        )}
      </nav>

      <div className="sidebar-footer">
        <div className="nav-link" onClick={handleLogout} style={{ cursor: "pointer" }}>
          <span className="nav-icon">←</span>
          {!isCollapsed && <span className="nav-text">Sign out</span>}
        </div>
      </div>
    </aside>
  );
}