from app.ai.groq_report import GroqInvestigationReport


class AICaseSummary:

    @staticmethod
    def summarize(case):

        report = GroqInvestigationReport()

        return report.generate(case)
