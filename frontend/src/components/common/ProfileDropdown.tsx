import { useState, useRef, useEffect } from "react";
import { useAuth } from "../../hooks/useAuth";

export default function ProfileDropdown() {
  const { user, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  const username = user?.username ?? "User";
  const role = user?.role ?? "user";
  const initials = username.slice(0, 2).toUpperCase();

  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  const handleLogout = () => {
    logout();
    window.location.href = "/login";
  };

  return (
    <div className="profile-dropdown" ref={ref} style={{ position: "relative" }}>
      <div className="profile-trigger" onClick={() => setIsOpen(!isOpen)}>
        <div className="profile-avatar">{initials}</div>
        <span className="profile-name">{username}</span>
      </div>

      {isOpen && (
        <div
          style={{
            position: "absolute",
            top: "calc(100% + 8px)",
            right: 0,
            width: 200,
            background: "var(--surface)",
            border: "1px solid var(--border)",
            borderRadius: "var(--radius-md)",
            boxShadow: "var(--shadow-xl)",
            zIndex: 150,
            overflow: "hidden",
          }}
        >
          <div style={{ padding: "12px 14px", borderBottom: "1px solid var(--border)" }}>
            <div style={{ fontSize: 14, fontWeight: 600, color: "var(--text-strong)" }}>{username}</div>
            <div style={{ fontSize: 12, color: "var(--text-muted)", textTransform: "capitalize" }}>{role}</div>
          </div>
          <div
            onClick={handleLogout}
            style={{
              padding: "10px 14px",
              fontSize: 13,
              color: "var(--red)",
              cursor: "pointer",
              transition: "background var(--transition)",
            }}
            onMouseEnter={(e: React.MouseEvent<HTMLDivElement>) => {
              (e.currentTarget as HTMLElement).style.background = "var(--red-light)";
            }}
            onMouseLeave={(e: React.MouseEvent<HTMLDivElement>) => {
              (e.currentTarget as HTMLElement).style.background = "transparent";
            }}
          >
            Sign out
          </div>
        </div>
      )}
    </div>
  );
}