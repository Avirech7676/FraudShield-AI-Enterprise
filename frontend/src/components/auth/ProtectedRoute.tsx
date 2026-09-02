import { Navigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import type { ReactNode } from "react";
import { PulseLoader } from "../ui/PulseLoader";

export default function ProtectedRoute({
    children,
}: {
    children: ReactNode;
}) {
    const { isAuthenticated, loading } = useAuth();

    // Wait for AuthProvider to read localStorage before making a decision.
    // Without this guard every page refresh would briefly see isAuthenticated=false
    // and redirect to /login even when a valid token exists in storage.
    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-slate-950">
                <PulseLoader label="Authenticating..." size="md" />
            </div>
        );
    }

    if (!isAuthenticated) {
        // Unauthenticated → send to login, NOT to the 401 error page.
        return <Navigate to="/login" replace />;
    }

    return <>{children}</>;
}