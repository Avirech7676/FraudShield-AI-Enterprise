from app.database.connection import MongoDBConnection
from app.database.repository import FraudRepository


def main():

    db = MongoDBConnection().connect()

    repo = FraudRepository(db)

    transaction = {

        "transaction_id": "TXN10001",

        "Amount": 2500,

        "Time": 20000

    }

    prediction = {

        "transaction_id": "TXN10001",

        "Prediction": "Fraud",

        "Fraud_Probability": 0.98,

        "Risk_Score": 98,

        "Risk_Tier": "Critical"

    }
    alert = {

        "alert_id": "ALT0001",

        "transaction_id": "TXN10001",

        "priority": "P1",

        "status": "Open"

    }
    audit = {

        "user": "Admin",

        "action": "Prediction Requested"

    }


    repo.save_transaction(transaction)
    repo.save_prediction(prediction)
    repo.save_alert(alert)
    repo.save_audit_log(audit)

    print()

    print("Transaction Saved")

    print("Prediction Saved")


if __name__ == "__main__":

    main()