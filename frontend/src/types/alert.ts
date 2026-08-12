export interface Alert {
  _id: string;

  transaction_id: string;

  prediction: string;

  risk_score: number;

  risk_tier: string;

  priority: "P1" | "P2" | "P3";

  assigned_to: string;

  status: "Open" | "Resolved" | "Ignored";

  created_at: string;
}
