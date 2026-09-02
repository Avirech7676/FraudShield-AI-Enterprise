from app.ai.groq_report import EnterpriseFraudReporter


class ReportService:
    """
    Report Service Layer
    Interfaces with Groq Investigation Reports for regulatory compliance.
    """

    def __init__(self):
        self.reporter = EnterpriseFraudReporter()

    def generate_compliance_sar_report(self, transaction_data, prediction_output, risk_output, llm_explanation):
        return self.reporter.generate_compliance_report(
            transaction_data, prediction_output, risk_output, llm_explanation
        )

    def answer_investigator_question(self, transaction_data, prediction_output, risk_output, question):
        return self.reporter.answer_investigator_question(
            transaction_data, prediction_output, risk_output, question
        )
