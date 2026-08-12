import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class PDFExporter:
    @staticmethod
    def export(data, filename):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Heading1"],
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#1A365D"),
            spaceAfter=15
        )
        body_style = styles["BodyText"]

        story.append(Paragraph("<b>FraudShield AI Enterprise Report</b>", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(str(data), body_style))
        doc.build(story)
        print(f"Basic PDF saved to {filename}")

    @staticmethod
    def export_investigation_report(transaction, prediction, risk, explanation, filename):
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        
        styles = getSampleStyleSheet()
        story = []

        # Color Palette
        primary_color = colors.HexColor("#0F172A")    # Deep slate
        accent_color = colors.HexColor("#4F46E5")     # Indigo
        text_muted = colors.HexColor("#64748B")       # Muted gray

        # Custom Typography Styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=20,
            leading=24,
            textColor=primary_color,
            spaceAfter=5
        )
        
        subtitle_style = ParagraphStyle(
            "DocSub",
            parent=styles["Normal"],
            fontSize=10,
            leading=12,
            textColor=text_muted,
            spaceAfter=15
        )

        h2_style = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading2"],
            fontSize=12,
            leading=16,
            textColor=accent_color,
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True
        )

        body_style = ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#334155")
        )

        # Header Block
        story.append(Paragraph("<b>SUSPICIOUS ACTIVITY INVESTIGATION REPORT (SAR)</b>", title_style))
        story.append(Paragraph("FraudShield AI Enterprise Compliance & Risk Engine Output", subtitle_style))
        story.append(Spacer(1, 5))

        # Metadata Table
        meta_data = [
            [
                Paragraph(f"<b>Transaction ID:</b> {transaction.get('transaction_id')}", body_style),
                Paragraph(f"<b>Risk Score:</b> {risk.get('Risk Score')}/100", body_style)
            ],
            [
                Paragraph(f"<b>Merchant:</b> {transaction.get('Merchant', 'Unknown')}", body_style),
                Paragraph(f"<b>Risk Tier:</b> {risk.get('Risk Tier')}", body_style)
            ],
            [
                Paragraph(f"<b>Country:</b> {transaction.get('Country', 'Unknown')}", body_style),
                Paragraph(f"<b>Recommended Action:</b> {risk.get('Recommended Action')}", body_style)
            ]
        ]
        
        meta_table = Table(meta_data, colWidths=[260, 260])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
            ('PADDING', (0,0), (-1,-1), 8),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 10))

        # Risk Components Section
        story.append(Paragraph("<b>I. RISK ENGINE COMPONENTS</b>", h2_style))
        components = risk.get("Components", {})
        
        table_data = [
            ["Risk Component", "Raw Score", "Weight"],
            ["ML Stacking Probability", f"{components.get('ML Probability', 0):.1f}%", "35%"],
            ["Rules Engine Penalty", f"{components.get('Rule Engine', 0):.1f}/100", "15%"],
            ["Behavioral Velocity", f"{components.get('Behavior Engine', 0):.1f}/100", "15%"],
            ["Anomaly Detection (AE/IF/LOF)", f"{components.get('Anomaly Score', 0):.1f}/100", "10%"],
            ["Device Reputation Score", f"{components.get('Device Trust', 0):.1f}/100", "10%"],
            ["Geographic Risk Profile", f"{components.get('Geo Risk', 0):.1f}/100", "5%"],
            ["Merchant Risk Coefficient", f"{components.get('Merchant Risk', 0):.1f}/100", "5%"],
            ["Customer Historical Violations", f"{components.get('Fraud History', 0):.1f}/100", "5%"]
        ]
        
        comp_table = Table(table_data, colWidths=[280, 120, 120])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#4F46E5")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('TOPPADDING', (0,0), (-1,0), 6),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F8FAFC")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('FONTSIZE', (0,1), (-1,-1), 9),
            ('PADDING', (0,1), (-1,-1), 5),
        ]))
        story.append(comp_table)
        story.append(Spacer(1, 10))

        # SHAP Features Section
        story.append(Paragraph("<b>II. SHAP EXPLAINABILITY (TOP RISK DRIVERS)</b>", h2_style))
        top_factors = explanation.get("top_factors", []) if isinstance(explanation, dict) else []
        
        if top_factors:
            factors_text = []
            for idx, f in enumerate(top_factors[:5], start=1):
                sign = "+" if f.get("impact", 0) > 0 else ""
                factors_text.append(f"<b>{idx}. {f.get('feature')}</b> ({sign}{f.get('impact')})")
            
            story.append(Paragraph(", &nbsp; &nbsp; ".join(factors_text), body_style))
        else:
            story.append(Paragraph("No local explainability factors provided for this transaction.", body_style))
            
        story.append(Spacer(1, 10))

        # LLM Reasoning Section
        story.append(Paragraph("<b>III. INVESTIGATION SUMMARY & NARRATIVE</b>", h2_style))
        reason = "Model and risk engine flagged the transaction."
        if isinstance(explanation, dict):
            reason = explanation.get("explanation_text") or explanation.get("reason") or reason
        elif isinstance(explanation, str):
            reason = explanation
            
        story.append(Paragraph(reason, body_style))
        story.append(Spacer(1, 10))

        # Compliance Directive Section
        story.append(Paragraph("<b>IV. REGULATORY COMPLIANCE DIRECTIVE</b>", h2_style))
        compliance_text = (
            "This document constitutes an official transaction audit trail. Under AML regulations, transactions "
            "graded as 'Critical' or 'High' risk must undergo manual investigator validation before fund settlement. "
            "Model parameters and SHAP coefficients are logged in the database to satisfy Explainable AI (XAI) auditing criteria."
        )
        story.append(Paragraph(compliance_text, body_style))

        # Build Document
        doc.build(story)
        print(f"Investigation report saved to {filename}")
