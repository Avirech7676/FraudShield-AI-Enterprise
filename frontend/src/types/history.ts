export interface PredictionHistory {
  transaction_id: string;
  customer_id?: string;
  prediction: string;
  fraud_probability: number;
  risk_score: number;
  risk_tier: string;
  enterprise_risk_score: number;
  enterprise_risk_tier: string;
  Latency_ms: number;
  merchant: string;
  country: string;
  status?: string;
  llm_explanation: string;
  created_at: string;
}

export interface HistoryResponse {
  predictions: PredictionHistory[];
}
