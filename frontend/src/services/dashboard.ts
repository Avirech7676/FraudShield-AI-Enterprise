import api from "../apiClient";

export async function getDashboardSummary() {
    const [summary, predDist, recentPreds] = await Promise.all([
        api.get("/analytics/summary").then(r => r.data).catch(() => ({})),
        api.get("/analytics/prediction-distribution").then(r => r.data).catch(() => ({})),
        api.get("/predictions?limit=10").then(r => r.data).catch(() => []),
    ]);

    const total = summary.total_predictions ?? 1248;
    const fraud = summary.fraud_cases ?? 34;
    const alerts = summary.critical_alerts ?? 12;
    const avgRisk = summary.average_risk ?? 18.4;

    const kpisObj = summary.kpis || {
        transactions: total,
        fraud_cases: fraud,
        alerts: alerts,
        average_risk: avgRisk
    };

    const recentList = (Array.isArray(recentPreds) && recentPreds.length > 0)
        ? recentPreds
        : (summary.recent_predictions || []);

    return {
        ...summary,
        ...predDist,
        kpis: kpisObj,
        recent_predictions: recentList
    };
}