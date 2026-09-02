import api from "../apiClient";

export async function getAnalyticsSummary() {
    const response = await api.get("/analytics/summary");
    return response.data;
}

export async function getRiskDistribution() {
    const response = await api.get("/analytics/risk-distribution");
    return response.data;
}

export async function getPredictionDistribution() {
    const response = await api.get("/analytics/prediction-distribution");
    return response.data;
}

export async function getModelPerformance() {
    const response = await api.get("/analytics/model-performance");
    return response.data;
}

export async function getFraudTrends(): Promise<any[]> {
    try {
        const response = await api.get("/analytics/fraud-trends");
        return response.data;
    } catch {
        return [];
    }
}

export async function getCountryDistribution(): Promise<any[]> {
    try {
        const response = await api.get("/analytics/country-distribution");
        return response.data;
    } catch {
        return [];
    }
}

export async function getMerchantDistribution(): Promise<any[]> {
    try {
        const response = await api.get("/analytics/merchant-distribution");
        return response.data;
    } catch {
        return [];
    }
}

export async function getBarChartData(): Promise<any[]> {
    try {
        const response = await api.get("/dashboard/bar-chart");
        return response.data;
    } catch {
        return [];
    }
}

export async function getAreaChartData(): Promise<any[]> {
    try {
        const response = await api.get("/dashboard/area-chart");
        return response.data;
    } catch {
        return [];
    }
}

export async function getRadarChartData(): Promise<any[]> {
    try {
        const response = await api.get("/dashboard/radar-chart");
        return response.data;
    } catch {
        return [];
    }
}

export async function getTreemapData(): Promise<any[]> {
    try {
        const response = await api.get("/dashboard/treemap");
        return response.data;
    } catch {
        return [];
    }
}