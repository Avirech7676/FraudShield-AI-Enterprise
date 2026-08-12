import api from "../apiClient";

export interface ExplanationResult {
  transaction_id: string;
  prediction?: string;
  fraud_probability: number;
  is_fraud: boolean;
  risk_score?: number;
  risk_tier?: string;
  confidence: number;
  shap_values: Record<string, number> | Array<{ feature: string; impact: number; description?: string }>;
  top_factors?: Array<{ feature: string; impact: number; description?: string }>;
  explanation: string;
  llm_explanation?: string;
  counterfactual: Record<string, string>;
  features?: Record<string, any>;
}

export async function getTransactionExplanation(transactionId: string): Promise<ExplanationResult> {
  const response = await api.get(`/explanation/${transactionId}`);
  return response.data;
}

export async function getFeatureExplanation(features: Record<string, any>): Promise<ExplanationResult> {
  const response = await api.post("/explanation", features);
  return response.data;
}