from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class PDFExporter:

    @staticmethod
    def export(data, filename):

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        story = []

        story.append(

            Paragraph(

                "<b>FraudShield AI Enterprise Report</b>",

                styles["Heading1"]

            )

        )

        story.append(

            Paragraph(

                str(data),

                styles["BodyText"]

            )

        )

        doc.build(story)