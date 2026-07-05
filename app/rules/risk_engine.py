import numpy as np


class EnterpriseRiskEngine:

    """
    Enterprise Hybrid Risk Engine

    Combines:
    - ML Probability
    - Rule Score
    - Anomaly Score
    - Device Trust
    - Velocity
    - Historical Fraud
    """

    def __init__(self):

        self.weights = {

            "ml_probability":0.45,

            "rule_score":0.20,

            "anomaly_score":0.15,

            "device_trust":0.10,

            "velocity_score":0.05,

            "fraud_history":0.05

        }

    ########################################################

    def normalize(self,value):

        value=max(0,min(100,value))

        return value

    ########################################################

    def calculate_risk_score(

        self,

        ml_probability,

        rule_score,

        anomaly_score,

        device_trust,

        velocity_score,

        fraud_history

    ):

        ml_probability*=100

        device_component=100-device_trust

        score=(

            ml_probability*self.weights["ml_probability"]

            +

            rule_score*self.weights["rule_score"]

            +

            anomaly_score*self.weights["anomaly_score"]

            +

            device_component*self.weights["device_trust"]

            +

            velocity_score*self.weights["velocity_score"]

            +

            fraud_history*self.weights["fraud_history"]

        )

        return round(

            self.normalize(score),

            2

        )

    ########################################################

    def calculate_tier(

        self,

        score

    ):

        if score<20:

            return "Very Low"

        elif score<40:

            return "Low"

        elif score<60:

            return "Medium"

        elif score<80:

            return "High"

        else:

            return "Critical"

    ########################################################

    def recommended_action(

        self,

        tier

    ):

        mapping={

            "Very Low":{

                "Action":"Approve",

                "Priority":"P5"

            },

            "Low":{

                "Action":"Approve & Monitor",

                "Priority":"P4"

            },

            "Medium":{

                "Action":"Manual Review",

                "Priority":"P3"

            },

            "High":{

                "Action":"Trigger MFA",

                "Priority":"P2"

            },

            "Critical":{

                "Action":"Freeze Transaction",

                "Priority":"P1"

            }

        }

        return mapping[tier]

    ########################################################

    def evaluate(

        self,

        ml_probability,

        rule_score,

        anomaly_score,

        device_trust,

        velocity_score,

        fraud_history

    ):

        score=self.calculate_risk_score(

            ml_probability,

            rule_score,

            anomaly_score,

            device_trust,

            velocity_score,

            fraud_history

        )

        tier=self.calculate_tier(score)

        action=self.recommended_action(tier)

        return {

            "Risk Score":score,

            "Risk Tier":tier,

            "Recommended Action":action["Action"],

            "Priority":action["Priority"]

        }