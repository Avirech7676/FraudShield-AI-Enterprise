// This file re-exports the canonical ProtectedRoute from components/auth.
// It exists only for backward-compatibility with any imports that still
// reference this path. Do not duplicate logic here.
export { default } from "../components/auth/ProtectedRoute";
