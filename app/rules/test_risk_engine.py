from app.rules.risk_engine import EnterpriseRiskEngine

engine=EnterpriseRiskEngine()

result=engine.evaluate(

    ml_probability=0.93,

    rule_score=80,

    anomaly_score=72,

    device_trust=30,

    velocity_score=90,

    fraud_history=100

)

print(result)
