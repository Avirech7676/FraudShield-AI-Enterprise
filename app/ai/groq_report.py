import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

class EnterpriseFraudReporter:
    def __init__(self):
        self.client = Groq(api_key=API_KEY)

    def build_prompt(self, prediction, risk):
        prompt = f"""

You are a Senior Fraud Investigation Officer.

Generate a professional fraud investigation report.

Prediction:

{prediction["Prediction"]}

Fraud Probability:

{prediction["Fraud_Probability"]}

Risk Score:

{prediction["Risk_Score"]}

Risk Tier:

{prediction["Risk_Tier"]}

Priority:

{risk["Priority"]}

Recommended Action:

{risk["Recommended Action"]}

Generate:

1. Executive Summary

2. Risk Assessment

3. Business Impact

4. Investigation Steps

5. Recommendations

"""
        return prompt

    def generate_report(self, prediction, risk):
        prompt = self.build_prompt(prediction, risk)
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return response.choices[0].message.content