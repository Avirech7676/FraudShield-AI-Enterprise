from fastapi import APIRouter
from app.services.prediction_service import PredictionService

router = APIRouter()
prediction_service = PredictionService()

RICH_FEATURE_NAMES = [
    "Amount", "Currency", "Merchant", "Merchant_Category", "Payment_Type",
    "Card_Present", "Chip_Used", "Contactless", "International",
    "Customer_Age", "Customer_Segment", "KYC_Level", "Customer_Lifetime",
    "Avg_Spend", "Monthly_Spend", "Credit_Limit", "Device_Fingerprint",
    "Device_Trust_Score", "Browser", "Operating_System", "Emulator_Detection",
    "Rooted_Device", "Jailbreak_Detection", "IP_Reputation", "VPN_Detection",
    "TOR_Detection", "ASN", "Country", "City", "ISP",
    "Transactions_Last_Hour", "Transactions_Last_Day", "Velocity",
    "Time_Since_Last_Transaction", "Merchant_Diversity", "Location_Jump",
    "Device_Change", "Password_Reset", "Login_Failure_Count",
    "Merchant_Risk", "Merchant_Chargeback_Rate", "Merchant_Country",
    "Previous_Fraud",
]


@router.get("/model/metadata")
def model_metadata():
    meta = prediction_service.get_model_metadata()
    meta["feature_count"] = len(RICH_FEATURE_NAMES)
    meta["features"] = RICH_FEATURE_NAMES
    return meta
