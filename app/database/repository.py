from datetime import datetime

from app.config.logging_config import logger


class FraudRepository:

    def __init__(self, db):

        self.db = db
        self.cases = db["cases"]
        self.feedback = db["analyst_feedback"]
        self.legacy_feedback = db["feedback"]
        self.transactions = db["transactions"]
        self.predictions = db["predictions"]
        self.alerts = db["alerts"]
        self.audit_logs = db["audit_logs"]
        self.models = db["models"]
        self.notifications = db["notifications"]

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

        logger.info("Alert saved")

        return result.inserted_id

    ##################################################
    # Audit Logs
    ##################################################

    def save_audit_log(self, log):

        log["created_at"] = datetime.utcnow()

        result = self.audit_logs.insert_one(log)

        logger.info("Audit log saved")

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

    def get_recent_predictions(self, limit=200):

        return list(
            self.predictions.find().sort("created_at", -1).limit(limit)
        )

    def count_transactions(self, query=None):

        return self.transactions.count_documents(query or {})

    def count_predictions(self, query=None):

        return self.predictions.count_documents(query or {})

    def count_alerts(self, query=None):

        return self.alerts.count_documents(query or {})

    def average_prediction_value(self, field):

        result = list(
            self.predictions.aggregate(
                [
                    {
                        "$group": {
                            "_id": None,
                            "value": {
                                "$avg": f"${field}"
                            }
                        }
                    }
                ]
            )
        )

        if not result:
            return 0

        return result[0].get("value") or 0

    def count_predictions_by_field(self, field):

        rows = self.predictions.aggregate(
            [
                {
                    "$group": {
                        "_id": f"${field}",
                        "count": {
                            "$sum": 1
                        }
                    }
                },
                {
                    "$sort": {
                        "count": -1
                    }
                }
            ]
        )

        return [
            {
                "label": row.get("_id") or "Unknown",
                "count": row["count"]
            }
            for row in rows
        ]

    def count_predictions_by_fields(self, primary_field, fallback_field):

        rows = self.predictions.aggregate(
            [
                {
                    "$group": {
                        "_id": {
                            "$ifNull": [
                                f"${primary_field}",
                                f"${fallback_field}"
                            ]
                        },
                        "count": {
                            "$sum": 1
                        }
                    }
                },
                {
                    "$sort": {
                        "count": -1
                    }
                }
            ]
        )

        return [
            {
                "label": row.get("_id") or "Unknown",
                "count": row["count"]
            }
            for row in rows
        ]

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

    ##################################################
    # Case Management
    ##################################################

    def save_case(self, case):

        result = self.cases.insert_one(case)

        return result.inserted_id


    def get_case(self, case_id):

        return self.cases.find_one(
            {
                "case_id": case_id
            }
        )


    def get_all_cases(self):

        return list(
            self.cases.find()
        )


    def update_case(self, case_id, data):

        return self.cases.update_one(
            {
                "case_id": case_id
            },
            {
                "$set": data
            }
        )


    def delete_case(self, case_id):

        return self.cases.delete_one(
            {
                "case_id": case_id
            }
        )
    
    def get_case_statistics(self):

        return {
            "total": self.cases.count_documents({}),
            "open": self.cases.count_documents(
             {
                    "status":"OPEN"
            }
         ),
            "closed": self.cases.count_documents(
              {
                  "status":"CLOSED"
            }
        ),
        "escalated": self.cases.count_documents(
            {
                "status":"ESCALATED"
            }
        )
    }
    def delete_all_closed_cases(self):
        return self.cases.delete_many(
        {
            "status":"CLOSED"
        }
    )
    #########################################################
    # Continuous Learning
    #########################################################

    def save_feedback(

        self,

        feedback

    ):

        result = self.feedback.insert_one(

            feedback

        )
        self.legacy_feedback.update_one(
            {"transaction_id": feedback.get("transaction_id")},
            {"$set": feedback},
            upsert=True
        )
        return result

    def get_feedback(self):

        return list(

            self.feedback.find()

        )

    def delete_feedback(self):

        return self.feedback.delete_many({})

    #########################################################
    # Models
    #########################################################

    def save_model_record(self, model):

        model["created_at"] = datetime.utcnow()

        return self.models.insert_one(model)

    def get_model_record(self, version):

        return self.models.find_one(
            {
                "version": version
            }
        )

    #########################################################
    # Notifications
    #########################################################

    def save_notification(self, notification):

        notification["created_at"] = datetime.utcnow()

        return self.notifications.insert_one(notification)

    def get_notifications(self):

        return list(self.notifications.find())
    #########################################################
    # Case Notes
    #########################################################

    def add_case_note(self, case_id, note):

        return self.cases.update_one(

            {

                "case_id": case_id

            },

            {

                "$push": {

                    "notes": note,

                    "timeline": {

                        "event": "Note Added",

                        "note": note,

                        "timestamp": datetime.utcnow()

                    }

                }

            }

        )
    def add_evidence(

        self,

        case_id,

        evidence

    ):

        return self.cases.update_one(

            {

                "case_id": case_id

            },

            {

                "$push": {

                    "evidence": evidence,

                    "timeline": {

                        "event": "Evidence Uploaded",

                        "timestamp": datetime.utcnow()

                    }

                }

            }

        )


    #########################################################

    def assign_case(self, case_id, analyst):

        return self.cases.update_one(

            {

                "case_id": case_id

            },

            {

                "$set": {

                    "assigned_to": analyst,

                    "updated_at": datetime.utcnow()

                },

                "$push": {

                    "timeline": {

                        "event": f"Assigned to {analyst}",

                        "timestamp": datetime.utcnow()

                    }

                }

            }

        )

    #########################################################

    def close_case(self, case_id, resolution):

        return self.cases.update_one(

            {

                "case_id": case_id

            },

            {

                "$set": {

                    "status": "CLOSED",

                    "resolution": resolution,

                    "updated_at": datetime.utcnow()

                },

                "$push": {

                    "timeline": {

                        "event": "Closed",

                        "timestamp": datetime.utcnow()

                    }

                }

            }

        )

    #########################################################

    def reopen_case(self, case_id):

        return self.cases.update_one(

            {

                "case_id": case_id

            },

            {

                "$set": {

                    "status": "OPEN",

                    "updated_at": datetime.utcnow()

                },

                "$push": {

                    "timeline": {

                        "event": "Reopened",

                        "timestamp": datetime.utcnow()

                    }

                }

            }

        )
    #########################################################
    # Escalation
    #########################################################

    def escalate_case(self, case_id):
        return self.cases.update_one(
            {
                "case_id": case_id
            },
            {
                "$set": {
                    "status": "ESCALATED",
                    "updated_at": datetime.utcnow()
                },
                "$push": {
                    "timeline": {
                        "event": "Case Escalated",
                        "timestamp": datetime.utcnow()
                    }
                }
            }
        )


        
