import { useEffect, useState } from "react";

import type { DashboardSummary } from "../types/dashboard.ts";

import { getDashboardSummary } from "../services/dashboard";

export function useDashboard() {
  const [data, setData] = useState<DashboardSummary>();

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  async function loadDashboard() {
    try {
      setLoading(true);

      const response = await getDashboardSummary();

      setData(response);
    } catch (e) {
      if (e instanceof Error) {
        setError(e.message);
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();

    const interval = setInterval(
      loadDashboard,

      30000,
    );

    return () => clearInterval(interval);
  }, []);

  return {
    data,

    loading,

    error,

    refresh: loadDashboard,
  };
}
