export interface PredictionPayload {
  Amount: number;
  Time: number;
  Currency: string;
  Merchant: string;
  Merchant_Category: string;
  Merchant_Country: string;
  Payment_Type: string;
  Card_Present: boolean;
  Chip_Used: boolean;
  Contactless: boolean;
  International: boolean;
  Customer_Age: number;
  Customer_Segment: string;
  KYC_Level: string;
  Customer_Lifetime: number;
  Avg_Spend: number;
  Monthly_Spend: number;
  Credit_Limit: number;
  Device_Fingerprint: string;
  Device_Trust_Score: number;
  Browser: string;
  Operating_System: string;
  Emulator_Detection: boolean;
  Rooted_Device: boolean;
  Jailbreak_Detection: boolean;
  IP_Reputation: number;
  VPN_Detection: boolean;
  TOR_Detection: boolean;
  ASN: string;
  Country: string;
  City: string;
  ISP: string;
  Transactions_Last_Hour: number;
  Transactions_Last_Day: number;
  Velocity: number;
  Time_Since_Last_Transaction: number;
  Merchant_Diversity: number;
  Location_Jump: boolean;
  Device_Change: boolean;
  Password_Reset: boolean;
  Login_Failure_Count: number;
  Merchant_Risk: number;
  Merchant_Chargeback_Rate: number;
  Previous_Fraud: number;
  V1: number;
  V2: number;
  V3: number;
  V4: number;
  V5: number;
  V6: number;
  V7: number;
  V8: number;
  V9: number;
  V10: number;
  V11: number;
  V12: number;
  V13: number;
  V14: number;
  V15: number;
  V16: number;
  V17: number;
  V18: number;
  V19: number;
  V20: number;
  V21: number;
  V22: number;
  V23: number;
  V24: number;
  V25: number;
  V26: number;
  V27: number;
  V28: number;
}

export const defaultPrediction: PredictionPayload = {
  /* Transaction */

  Amount: 150,

  Time: 0,

  Currency: "USD",

  Merchant: "Amazon",

  Merchant_Category: "Retail",

  Merchant_Country: "USA",

  Payment_Type: "Credit Card",

  Card_Present: true,

  Chip_Used: true,

  Contactless: false,

  International: false,

  /* Customer */

  Customer_Age: 30,

  Customer_Segment: "Premium",

  KYC_Level: "Full",

  Customer_Lifetime: 1200,

  Avg_Spend: 300,

  Monthly_Spend: 6000,

  Credit_Limit: 15000,

  /* Device */

  Device_Fingerprint: "DEVICE001",

  Device_Trust_Score: 95,

  Browser: "Chrome",

  Operating_System: "Windows",

  Emulator_Detection: false,

  Rooted_Device: false,

  Jailbreak_Detection: false,

  /* Network */

  IP_Reputation: 10,

  VPN_Detection: false,

  TOR_Detection: false,

  ASN: "AS12345",

  Country: "USA",

  City: "New York",

  ISP: "Comcast",

  /* Behaviour */

  Transactions_Last_Hour: 2,

  Transactions_Last_Day: 8,

  Velocity: 2,

  Time_Since_Last_Transaction: 120,

  Merchant_Diversity: 3,

  Location_Jump: false,

  Device_Change: false,

  Password_Reset: false,

  Login_Failure_Count: 0,

  Merchant_Risk: 12,

  Merchant_Chargeback_Rate: 1,

  Previous_Fraud: 0,

  /* PCA */

  V1: 0,
  V2: 0,
  V3: 0,
  V4: 0,
  V5: 0,
  V6: 0,
  V7: 0,
  V8: 0,
  V9: 0,
  V10: 0,
  V11: 0,
  V12: 0,
  V13: 0,
  V14: 0,
  V15: 0,
  V16: 0,
  V17: 0,
  V18: 0,
  V19: 0,
  V20: 0,
  V21: 0,
  V22: 0,
  V23: 0,
  V24: 0,
  V25: 0,
  V26: 0,
  V27: 0,
  V28: 0,
};

export interface PredictionResponse {
  transaction_id?: string;

  prediction?: {
    Prediction: string;

    Fraud_Probability: number;

    Risk_Score: number;

    Risk_Tier: string;

    Latency_ms: number;
  };

  risk_analysis?: {
    Priority: string;

    Recommended_Action: string;

    Components?: {
      "ML Probability": number;

      "Rule Engine": number;

      "Behavior Engine": number;

      "Device Trust": number;

      "Geo Risk": number;

      "Merchant Risk": number;
    };
  };

  top_factors?: string[];

  llm_explanation?: string;

  message?: string;
}
