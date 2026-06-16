# pdf_services.py

import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_recruitment_pdf(applicant_data):
    """
    Generates a styled recruitment PDF supporting long-form text and payment status.
    """

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    story = []

    # Title Style
    title_style = ParagraphStyle(
        "OfficialTitle",
        parent=styles["Heading1"],
        fontSize=20,
        textColor=colors.HexColor("#003366"),
        alignment=1,
        spaceAfter=30
    )

    story.append(
        Paragraph("DUITS Recruitment Application", title_style)
    )

    normal_style = styles["Normal"]

    skills_para = Paragraph(
        str(applicant_data.get("skills", "N/A")),
        normal_style
    )

    motivation_para = Paragraph(
        str(applicant_data.get("motivation", "N/A")),
        normal_style
    )

    payment_status_raw = applicant_data.get("payment_status", applicant_data.get("is_paid"))
    payment_status = "Paid" if payment_status_raw in (True, "PAID", "COMPLETED", "Paid") else "Unpaid"

    data = [
        ["Applicant Information", ""],
        ["Full Name:", applicant_data.get("name", "N/A")],
        ["Email:", applicant_data.get("email", "N/A")],
        ["Phone:", applicant_data.get("phone", "N/A")],
        ["Department:", applicant_data.get("department", "N/A")],
        ["Session:", applicant_data.get("session", "N/A")],
        ["Hall:", applicant_data.get("hall", "N/A")],
        ["Student ID:", applicant_data.get("student_id", "N/A")],
        ["Skills:", skills_para],
        ["Motivation:", motivation_para],
        ["Payment Status:", payment_status],
        ["System Status:", "Application Received"],
    ]

    # Fixed colWidths
    table = Table(
        data,
        colWidths=[130, 350]
    )

    table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0, 0), (1, 0), colors.HexColor("#003366")),
        ("TEXTCOLOR", (0, 0), (1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (1, 0), "CENTER"),
        ("FONTNAME", (0, 0), (1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (1, 0), 10),
        ("TOPPADDING", (0, 0), (1, 0), 10),
        ("SPAN", (0, 0), (1, 0)),

        # Data rows
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 1), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 8),

        # Alignment
        ("VALIGN", (0, 0), (-1, -1), "TOP"),

        # Grid / Borders
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))

    story.append(table)
    story.append(Spacer(1, 40))

    footer_style = ParagraphStyle(
        "Footer",
        parent=styles["Italic"],
        fontSize=9,
        textColor=colors.dimgrey,
        alignment=1
    )

    story.append(
        Paragraph(
            "This is an automatically generated document from the DUITS system.",
            footer_style
        )
    )

    doc.build(story)

    buffer.seek(0)
    return buffer