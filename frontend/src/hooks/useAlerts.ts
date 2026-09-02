import { useEffect, useState } from "react";
import type { Alert } from "../types/alert";
import { getAlerts, assignAlert, updateAlert } from "../services/alerts";

export function useAlerts() {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  async function load() {
    try {
      setLoading(true);

      const response = await getAlerts();

      setAlerts(response);
    } catch (e) {
      if (e instanceof Error) {
        setError(e.message);
      }
    } finally {
      setLoading(false);
    }
  }

  async function assign(id: string, analyst: string) {
    await assignAlert(id, analyst);

    await load();
  }

  async function changeStatus(
    id: string,
    status: "Open" | "Resolved" | "Ignored",
  ) {
    await updateAlert(id, status);

    await load();
  }

  useEffect(() => {
    load();
  }, []);

  return {
    alerts,

    loading,

    error,

    refresh: load,

    assign,

    changeStatus,
  };
}
