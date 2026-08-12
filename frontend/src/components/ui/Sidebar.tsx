import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard, ShieldAlert, Sliders, FileText, Cpu,
  History, BarChart3, Users, LogOut, AlertTriangle,
  FolderGit2, ShieldCheck, ChevronRight,
} from "lucide-react";
import { useAuth } from "../../hooks/useAuth";

interface NavItem {
  to: string;
  label: string;
  icon: React.ElementType;
  badge?: string | number;
  adminOnly?: boolean;
  section?: string;
}

const NAV_ITEMS: NavItem[] = [
  { to: "/dashboard",  label: "Dashboard",      icon: LayoutDashboard, section: "OVERVIEW" },
  { to: "/prediction", label: "Predictions",    icon: ShieldCheck },
  { to: "/history",    label: "Audit Logs",     icon: History },
  { to: "/alerts",     label: "Threat Alerts",  icon: AlertTriangle,   section: "OPERATIONS" },
  { to: "/cases",      label: "Incidents",      icon: FolderGit2 },
  { to: "/analytics",  label: "Analytics",      icon: BarChart3 },
  { to: "/reports",    label: "AI Reports",     icon: FileText,        section: "INTELLIGENCE" },
  { to: "/models",     label: "Model Registry", icon: Cpu },
  { to: "/users",      label: "User Mgmt",      icon: Users,           adminOnly: true, section: "ADMIN" },
  { to: "/settings",   label: "Settings",       icon: Sliders },
];

export const Sidebar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const isAdmin = user?.role === "Admin" || user?.role === "admin";

  const filteredItems = NAV_ITEMS.filter(item => !item.adminOnly || isAdmin);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  let lastSection = "";

  return (
    <aside style={{
      width: 240,
      minWidth: 240,
      height: "100vh",
      position: "sticky",
      top: 0,
      display: "flex",
      flexDirection: "column",
      background: "linear-gradient(180deg, #060b18 0%, #02040a 100%)",
      borderRight: "1px solid rgba(255,255,255,0.05)",
      zIndex: 40,
      overflowY: "auto",
      paddingBottom: 16,
    }}>
      {/* Brand */}
      <div style={{ padding: "24px 20px 20px", display: "flex", alignItems: "center", gap: 12, borderBottom: "1px solid rgba(255,255,255,0.04)", flexShrink: 0 }}>
        <div style={{ width: 38, height: 38, borderRadius: 10, background: "linear-gradient(135deg, #6366f1, #4f46e5)", display: "flex", alignItems: "center", justifyContent: "center", boxShadow: "0 0 20px rgba(99,102,241,0.35)", border: "1px solid rgba(99,102,241,0.35)", flexShrink: 0 }}>
          <ShieldAlert size={19} color="#fff" />
        </div>
        <div>
          <div style={{ fontSize: 15, fontWeight: 800, color: "#f1f5f9", letterSpacing: "-0.02em", lineHeight: 1 }}>FraudShield</div>
          <div style={{ fontSize: 9, fontWeight: 700, color: "#818cf8", letterSpacing: "0.18em", textTransform: "uppercase", marginTop: 4 }}>Enterprise AI</div>
        </div>
      </div>

      {/* Live indicator */}
      <div style={{ display: "flex", alignItems: "center", gap: 8, padding: "10px 20px", borderBottom: "1px solid rgba(255,255,255,0.03)" }}>
        <span className="status-dot online" />
        <span style={{ fontSize: 11, color: "#10b981", fontWeight: 500 }}>All systems operational</span>
      </div>

      {/* Nav */}
      <nav style={{ flex: 1, padding: "12px 12px 8px" }}>
        {filteredItems.map(item => {
          const Icon = item.icon;
          const showSection = item.section && item.section !== lastSection;
          if (item.section) lastSection = item.section;

          return (
            <React.Fragment key={item.to}>
              {showSection && (
                <div style={{ padding: "14px 8px 5px", fontSize: 10, fontWeight: 700, color: "#334155", letterSpacing: "0.12em", textTransform: "uppercase" }}>
                  {item.section}
                </div>
              )}
              <NavLink
                to={item.to}
                className={({ isActive }) => `sidebar-item${isActive ? " active" : ""}`}
              >
                {({ isActive }) => (
                  <>
                    <Icon size={16} color={isActive ? "#818cf8" : "#475569"} style={{ flexShrink: 0, transition: "color 0.18s" }} />
                    <span style={{ flex: 1, fontSize: 13.5, fontWeight: isActive ? 600 : 450, color: isActive ? "#e2e8f0" : "#64748b", transition: "color 0.18s" }}>
                      {item.label}
                    </span>
                    {item.badge && (
                      <span style={{ padding: "2px 7px", borderRadius: 20, background: "rgba(244,63,94,0.15)", color: "#fb7185", fontSize: 10, fontWeight: 700, border: "1px solid rgba(244,63,94,0.25)" }}>
                        {item.badge}
                      </span>
                    )}
                    {isActive && <ChevronRight size={12} color="#818cf8" />}
                  </>
                )}
              </NavLink>
            </React.Fragment>
          );
        })}
      </nav>

      {/* User card */}
      <div style={{ margin: "8px 12px 0", padding: "12px", borderRadius: 12, background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
          <div style={{ width: 34, height: 34, borderRadius: 9, background: "linear-gradient(135deg, #6366f1, #a78bfa)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 700, fontSize: 13, flexShrink: 0 }}>
            {user?.username?.[0]?.toUpperCase() ?? "U"}
          </div>
          <div style={{ overflow: "hidden" }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: "#e2e8f0", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
              {user?.username ?? "Analyst"}
            </div>
            <div style={{ fontSize: 10, fontWeight: 600, color: "#818cf8", textTransform: "uppercase", letterSpacing: "0.1em", marginTop: 2 }}>
              {user?.role ?? "Analyst"}
            </div>
          </div>
        </div>
        <button
          onClick={handleLogout}
          className="btn-danger"
          style={{ width: "100%", padding: "7px 12px", fontSize: 12, gap: 6 }}
        >
          <LogOut size={13} />
          Sign Out
        </button>
      </div>
    </aside>
  );
};
