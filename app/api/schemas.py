from typing import Optional

from pydantic import BaseModel, ConfigDict


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    Time: float = 0
    Amount: float

    V1: float = 0
    V2: float = 0
    V3: float = 0
    V4: float = 0
    V5: float = 0
    V6: float = 0
    V7: float = 0
    V8: float = 0
    V9: float = 0
    V10: float = 0
    V11: float = 0
    V12: float = 0
    V13: float = 0
    V14: float = 0
    V15: float = 0
    V16: float = 0
    V17: float = 0
    V18: float = 0
    V19: float = 0
    V20: float = 0
    V21: float = 0
    V22: float = 0
    V23: float = 0
    V24: float = 0
    V25: float = 0
    V26: float = 0
    V27: float = 0
    V28: float = 0

    Currency: str = "USD"
    Merchant: Optional[str] = None
    Merchant_Category: Optional[str] = None
    Merchant_Country: Optional[str] = None
    Payment_Type: Optional[str] = None
    Card_Present: bool = False
    Chip_Used: bool = False
    Contactless: bool = False
    International: bool = False

    Customer_Age: Optional[int] = None
    Customer_Segment: Optional[str] = None
    KYC_Level: Optional[str] = None
    Customer_Lifetime: Optional[float] = None
    Avg_Spend: Optional[float] = None
    Monthly_Spend: Optional[float] = None
    Credit_Limit: Optional[float] = None

    Device_Fingerprint: Optional[str] = None
    Device_Trust_Score: float = 80
    Browser: Optional[str] = None
    Operating_System: Optional[str] = None
    Emulator_Detection: bool = False
    Rooted_Device: bool = False
    Jailbreak_Detection: bool = False

    IP_Reputation: float = 20
    VPN_Detection: bool = False
    TOR_Detection: bool = False
    ASN: Optional[str] = None
    Country: Optional[str] = None
    City: Optional[str] = None
    ISP: Optional[str] = None

    Transactions_Last_Hour: int = 0
    Transactions_Last_Day: int = 0
    Velocity: float = 0
    Time_Since_Last_Transaction: Optional[float] = None
    Merchant_Diversity: int = 0
    Location_Jump: bool = False
    Device_Change: bool = False
    Password_Reset: bool = False
    Login_Failure_Count: int = 0

    Merchant_Risk: float = 20
    Merchant_Chargeback_Rate: float = 0
    Previous_Fraud: int = 0
