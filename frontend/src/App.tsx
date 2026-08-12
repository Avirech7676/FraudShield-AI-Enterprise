import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";
import ModernLayout from "./layouts/ModernLayout";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import AdminRoute from "./components/auth/AdminRoute";
import { PulseLoader } from "./components/ui/PulseLoader";

const LoginPage = lazy(() => import("./pages/Login"));
const RegisterPage = lazy(() => import("./pages/Register"));
const DashboardPage = lazy(() => import("./pages/Dashboard").then(m => ({ default: m.DashboardPage })));
const PredictionPage = lazy(() => import("./pages/Prediction"));
const HistoryPage = lazy(() => import("./pages/History"));
const UsersPage = lazy(() => import("./pages/Users"));
const AlertsPage = lazy(() => import("./pages/Alerts"));
const CasesPage = lazy(() => import("./pages/Cases"));
const Analytics = lazy(() => import("./pages/Analytics").then(m => ({ default: m.Analytics })));
const ReportsPage = lazy(() => import("./pages/Reports"));
const SettingsPage = lazy(() => import("./pages/Settings"));
const ModelManagement = lazy(() => import("./pages/ModelManagement"));
const Explanation = lazy(() => import("./pages/Explanation"));

const Error401Page = lazy(() => import("./pages/401"));
const Error403Page = lazy(() => import("./pages/403"));
const Error404Page = lazy(() => import("./pages/404"));
const Error500Page = lazy(() => import("./pages/500"));

const LoadingFallback = () => (
  <div className="flex items-center justify-center min-h-[60vh]">
    <PulseLoader label="Loading enterprise module..." size="md" />
  </div>
);

export default function App() {
    return (
        <BrowserRouter>
            <Suspense fallback={<LoadingFallback />}>
                <Routes>
                    <Route path="/" element={<Navigate to="/dashboard" replace />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/401" element={<Error401Page />} />
                    <Route path="/403" element={<Error403Page />} />
                    <Route path="/404" element={<Error404Page />} />
                    <Route path="/500" element={<Error500Page />} />

                    <Route
                        element={
                            <ProtectedRoute>
                                <ModernLayout />
                            </ProtectedRoute>
                        }
                    >
                        <Route path="/dashboard" element={<DashboardPage />} />
                        <Route path="/prediction" element={<PredictionPage />} />
                        <Route path="/history" element={<HistoryPage />} />
                        <Route path="/alerts" element={<AlertsPage />} />
                        <Route path="/cases" element={<CasesPage />} />
                        <Route path="/analytics" element={<Analytics />} />
                        <Route path="/reports" element={<ReportsPage />} />
                        <Route path="/settings" element={<SettingsPage />} />
                        <Route path="/models" element={<ModelManagement />} />
                        <Route path="/explanation/:transactionId" element={<Explanation />} />
                        <Route path="/explanation" element={<Explanation />} />

                        <Route
                            path="/users"
                            element={
                                <AdminRoute>
                                    <UsersPage />
                                </AdminRoute>
                            }
                        />
                    </Route>

                    {/* Catch-all for 404 - must be last */}
                    <Route path="*" element={<Navigate to="/404" replace />} />
                </Routes>
            </Suspense>
        </BrowserRouter>
    );
}