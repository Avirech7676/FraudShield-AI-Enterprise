import { Navigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import type { ReactNode } from "react";
import { PulseLoader } from "../ui/PulseLoader";

export default function AdminRoute({ children }: { children: ReactNode }) {
  const { user, loading, isAuthenticated } = useAuth();

  // Wait for AuthProvider to restore session from localStorage.
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-950">
        <PulseLoader label="Verifying access..." size="md" />
      </div>
    );
  }

  // Not authenticated at all → send to login.
  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />;
  }

  // Authenticated but not Admin → show 401 Unauthorized page.
  if (user.role !== "Admin") {
    return <Navigate to="/401" replace />;
  }

  return <>{children}</>;
}