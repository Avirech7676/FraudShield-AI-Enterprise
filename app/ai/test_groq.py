from app.ai.groq_report import EnterpriseFraudReporter

prediction = {

    "Prediction":"Fraud",

    "Fraud_Probability":0.982,

    "Risk_Score":98.2,

    "Risk_Tier":"Critical"

}
risk = {

    "Priority":"P1",

    "Recommended Action":"Block Transaction"

}
reporter = EnterpriseFraudReporter()
report = reporter.generate_report(

    prediction,

    risk

)
print(report)