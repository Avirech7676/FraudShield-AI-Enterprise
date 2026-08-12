import { useEffect, useState } from "react";
import type { PredictionHistory } from "../types/history";
import { getHistory } from "../services/history";

export function useHistory(params: { filters: any; page: number; size: number }) {
  const { filters, page, size } = params;
  const [predictions, setPredictions] = useState<PredictionHistory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const skip = (page - 1) * size;
  const limit = size;

  async function load() {
    try {
      setLoading(true);
      setError("");
      const response = await getHistory({ filters, skip, limit });
      const list = Array.isArray(response) ? response : (response?.predictions || response?.items || []);
      setPredictions(list);
    } catch (e) {
      if (e instanceof Error) {
        setError(e.message);
      } else {
        setError("Failed to fetch history");
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [filters, page, size]);

  return {
    predictions,
    loading,
    error,
    refresh: load,
  };
}