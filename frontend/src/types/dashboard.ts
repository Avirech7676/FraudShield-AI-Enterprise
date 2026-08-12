export interface DashboardKpis {
  transactions: number;
  predictions: number;
  fraud_cases: number;
  alerts: number;
  critical_alerts: number;
  average_risk: number;
  features_used: number;
  models_loaded: number;
}

export interface PredictionDistribution {
  label: string;
  count: number;
}

export interface RiskTier {
  label: string;
  count: number;
}

export interface RecentPrediction {
  transaction_id: string;
  prediction: string;
  fraud_probability: number;
  risk_score: number;
  risk_tier: string;

  enterprise_risk_score: number;
  enterprise_risk_tier: string;

  Latency_ms: number;

  merchant: string;
  country: string;

  llm_explanation: string;

  created_at: string;
}

export interface ModelInformation {
  loaded: boolean;
  version: string;

  model_path: string;
  preprocessor_path: string;

  model_name?: string;
  algorithm?: string;
  accuracy?: number;
  precision?: number;
  recall?: number;
  f1_score?: number;
  production_model?: string;
  status?: string;
  feature_count?: number;
  features?: string[];
}

export interface DashboardSummary {
  kpis: DashboardKpis;

  prediction_distribution: PredictionDistribution[];

  risk_tiers: RiskTier[];

  recent_predictions: RecentPrediction[];

  model: ModelInformation;

  features: string[];
}

export interface HealthResponse {
  status: string;

  timestamp: string;

  database: boolean;

  prediction_engine: {
    ready: boolean;

    model_loaded: boolean;

    preprocessor_loaded: boolean;

    version: string;
  };

  version: string;
}
