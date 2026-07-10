import os
from groq import Groq
from dotenv import load_dotenv
from app.config.logging_config import logger

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

class EnterpriseFraudReporter:
    def __init__(self):
        self.api_key = API_KEY
        if not self.api_key:
            logger.warning("GROQ_API_KEY is not set. LLM capabilities will run in simulation mode.")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)

    def _call_llm(self, prompt, system_prompt="You are a Senior Fraud Investigation Officer."):
        if not self.client:
            # Simulated responses when API key is missing
            return self._simulate_llm_response(prompt)
            
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq API call failed: {e}")
            return f"LLM error: {str(e)}. Falling back to local rules-based summary."

    def explain_flag(self, transaction_data, prediction_output, risk_output, top_factors):
        prompt = f"""
        Analyze this flagged transaction and write a concise, professional explanation for a fraud analyst:
        
        Transaction Details:
        - Amount: {transaction_data.get('Amount')}
        - Merchant: {transaction_data.get('Merchant')}
        - Country: {transaction_data.get('Country')}
        - IP Reputation: {transaction_data.get('IP_Reputation')}
        - VPN Detected: {transaction_data.get('VPN_Detection')}
        - Device Trust Score: {transaction_data.get('Device_Trust_Score')}
        
        Model Outputs:
        - ML Fraud Probability: {prediction_output.get('Fraud_Probability')}
        - Enterprise Risk Score: {risk_output.get('Risk Score')}/100
        - Risk Tier: {risk_output.get('Risk Tier')}
        - Recommended Action: {risk_output.get('Recommended Action')}
        
        SHAP Feature Impacts (Top Contributors):
        {chr(10).join([f"- {f.get('feature')}: {f.get('impact'):+}" for f in top_factors])}
        
        Write a 3-4 sentence summary explaining exactly why this was flagged, highlighting the most suspicious factors (e.g. location jumps, IP/VPN issues, low device trust) and the recommended action.
        """
        return self._call_llm(prompt, "You are a Senior Fraud Risk Analyst.")

    def summarize_case(self, case_details, notes, timeline):
        prompt = f"""
        Provide a structured, executive summary of this fraud case:
        
        Case Info:
        - Case ID: {case_details.get('case_id')}
        - Status: {case_details.get('status')}
        - Assigned To: {case_details.get('assigned_to')}
        - Priority: {case_details.get('priority')}
        - Created At: {case_details.get('created_at')}
        
        Timeline Events:
        {chr(10).join([f"- {t.get('event')} at {t.get('timestamp')}" for t in timeline])}
        
        Analyst Notes:
        {chr(10).join([f"- {n}" for n in notes]) if notes else "No analyst notes yet."}
        
        Summarize:
        1. Current Status & History
        2. Suspicious Indicators Identified
        3. Analyst Findings Summary
        4. Next Steps
        """
        return self._call_llm(prompt)

    def generate_compliance_report(self, transaction_data, prediction_output, risk_output, llm_explanation):
        prompt = f"""
        Generate a formal Suspicious Activity Report (SAR) compliance statement for a financial regulator.
        
        Subject Transaction:
        - Transaction ID: {transaction_data.get('transaction_id')}
        - Date: {transaction_data.get('created_at', 'Today')}
        - Amount: ${transaction_data.get('Amount')}
        - Merchant: {transaction_data.get('Merchant')}
        - Geo Location: {transaction_data.get('Country')}
        
        Risk Analysis Summary:
        - Risk Score: {risk_output.get('Risk Score')}/100
        - Risk Tier: {risk_output.get('Risk Tier')}
        - Local Risk Explanation: {llm_explanation}
        
        Format your response as a formal SAR document, containing:
        - SECTION I: SUSPICIOUS ACTIVITY SUMMARY
        - SECTION II: RISK ENGINE FINDINGS & SHAP EXPLANABILITY
        - SECTION III: COMPLIANCE ASSESSMENT & INVESTIGATION DIRECTIVES
        """
        return self._call_llm(prompt, "You are an Enterprise Compliance and AML Officer.")

    def answer_investigator_question(self, transaction_data, prediction_output, risk_output, question):
        prompt = f"""
        You are answering a question from a fraud investigator about a specific transaction.
        
        Transaction Info:
        {str(transaction_data)}
        
        Model & Risk Output:
        {str(prediction_output)}
        {str(risk_output)}
        
        Investigator's Question:
        "{question}"
        
        Provide a direct, factual, and professional answer based only on the provided transaction data and model outputs. If the data does not contain the answer, state that it is not available.
        """
        return self._call_llm(prompt, "You are a Fraud Analyst Assistant.")

    def _simulate_llm_response(self, prompt):
        # Fallback simulator when Groq API key is missing
        if "SAR compliance" in prompt or "regulatory" in prompt:
            return (
                "=== SUSPICIOUS ACTIVITY REPORT (SAR) ===\n"
                "SECTION I: SUSPICIOUS ACTIVITY SUMMARY\n"
                "The transaction represents an elevated risk profile. The transfer value combined with device/location mismatch triggers regulatory review.\n\n"
                "SECTION II: RISK ENGINE FINDINGS\n"
                "Automated risk scoring is above acceptable thresholds. SHAP analysis points to key anomalies in VPN connection status and device metadata.\n\n"
                "SECTION III: COMPLIANCE STATUS\n"
                "Under current AML guidelines, this transaction has been frozen. Immediate identity verification is recommended."
            )
        elif "Case Info" in prompt:
            return (
                "Case Summary: The case is currently open and assigned. Timeline shows automated P1 trigger and subsequent analyst routing. "
                "Suspicious factors include high transaction frequency and low device reputation scores."
            )
        elif "investigator" in prompt:
            return "Based on the transaction data, the device trust score is low (under 40) and VPN detection is enabled, which suggests high probability of unauthorized access."
        else:
            return (
                "The transaction was flagged as critical risk. "
                "Key indicators show active VPN routing and a Device Trust Score significantly below average. "
                "The geographic location jump indicates a high probability of credential takeover. "
                "Recommended action: Freeze account and require Multi-Factor Authentication."
            )

    def generate_report(self, prediction_output, risk_output):
        transaction_data = {
            "Amount": prediction_output.get("Amount", 0),
            "Merchant": "Unknown",
            "Country": "Unknown",
            "IP_Reputation": 50.0,
            "VPN_Detection": False,
            "Device_Trust_Score": 80.0
        }
        return self.explain_flag(transaction_data, prediction_output, risk_output, [])

# Re-expose as name in README
GroqInvestigationReport = EnterpriseFraudReporter
