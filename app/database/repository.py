from datetime import datetime


class FraudRepository:

    def __init__(self, db):

        self.db = db

        self.transactions = db["transactions"]
        self.predictions = db["predictions"]
        self.alerts = db["alerts"]
        self.audit_logs = db["audit_logs"]

    ##################################################
    # Transactions
    ##################################################

    def save_transaction(self, transaction):

        transaction["created_at"] = datetime.utcnow()

        result = self.transactions.insert_one(transaction)

        return result.inserted_id

    ##################################################
    # Predictions
    ##################################################

    def save_prediction(self, prediction):

        prediction["created_at"] = datetime.utcnow()

        result = self.predictions.insert_one(prediction)

        return result.inserted_id

    ##################################################
    # Alerts
    ##################################################

    def save_alert(self, alert):

        alert["created_at"] = datetime.utcnow()

        result = self.alerts.insert_one(alert)

        print("Alert Saved")

        return result.inserted_id

    ##################################################
    # Audit Logs
    ##################################################

    def save_audit_log(self, log):

        log["created_at"] = datetime.utcnow()

        result = self.audit_logs.insert_one(log)

        print("Audit Log Saved")

        return result.inserted_id

    ##################################################
    # Prediction Queries
    ##################################################

    def get_prediction(self, transaction_id):

        return self.predictions.find_one(

            {

                "transaction_id": transaction_id

            }

        )

    def get_all_predictions(self):

        return list(

            self.predictions.find()

        )

    def delete_prediction(self, transaction_id):

        return self.predictions.delete_one(

            {

                "transaction_id": transaction_id

            }

        )

    ##################################################
    # User Management
    ##################################################

    def get_user(self, username):

        return self.db.users.find_one(

            {

                "username": username

            }

        )
    def get_all_users(self):
        return list(
            self.db.users.find(
                {},
                {
                    "_id": 0,
                    "password": 0
                }
            )
        )

    def add_user(self, user):

        return self.db.users.insert_one(user)

    def update_user_role(self, username, role):

        return self.db.users.update_one(

            {
                "username": username
            },
            {
                "$set": {
                    "role": role
                }
            }
        )
    def reset_password(
            self, username, password):
        return self.db.users.update_one(
            {
            "username": username
            },
            {
                "$set":{
                    "password": password
                }
            }
        )
    
    
    def delete_user(self, username):
        return self.db.users.delete_one(
            {
                "username": username
            }
        )