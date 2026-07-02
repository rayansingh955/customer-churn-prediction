from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from utils.recommendation import get_recommendations

def generate_report(
    prediction,
    probability,
    SeniorCitizen,
    Partner,
    Dependents,
    tenure,
    InternetService,
    OnlineSecurity,
    TechSupport,
    Contract,
    PaymentMethod,
    MonthlyCharges,
    TotalCharges,
    reasons,
):
    

    filename = "Customer_Churn_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1E40AF"),
        fontSize=26,
        spaceAfter=25,
    )

    story = []

    # ===========================
    # Title
    # ===========================

    story.append(
        Paragraph(
            "CUSTOMER CHURN PREDICTION REPORT",
            title_style,
        )
    )

    story.append(Spacer(1, 15))

    # ===========================
    # Report Information
    # ===========================

    report_info = [
        ["Generated On", datetime.now().strftime("%d %B %Y")],
        ["Model", "Balanced Logistic Regression"],
        ["ROC-AUC", "0.86"],
        ["Recall", "83%"],
    ]

    report_table = Table(report_info, colWidths=[170, 250])

    report_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EAF2FF")),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#D6E8FF")),
    ]))

    story.append(report_table)

    story.append(Spacer(1, 20))

    # ===========================
    # Prediction Summary
    # ===========================

    if prediction == 1:
        pred = "Customer Likely to Churn"
    else:
        pred = "Customer Likely to Stay"

    if probability >= 0.75:
        risk = "HIGH RISK"

    elif probability >= 0.40:
        risk = "MEDIUM RISK"

    else:
        risk = "LOW RISK"

    prediction_table = [
        ["Prediction", pred],
        ["Risk Level", risk],
        ["Probability", f"{probability*100:.2f}%"],
    ]

    pred_table = Table(prediction_table, colWidths=[170, 250])

    pred_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF8DC")),
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#FFE9A8")),
    ]))

    story.append(pred_table)

    story.append(Spacer(1, 20))

    # ===========================
    # Customer Details
    # ===========================

    story.append(Paragraph("<b>Customer Details</b>", styles["Heading2"]))

    customer_table = [

        ["Field", "Value"],

        ["Senior Citizen", SeniorCitizen],

        ["Partner", Partner],

        ["Dependents", Dependents],

        ["Tenure", f"{tenure} Months"],

        ["Internet Service", InternetService],

        ["Online Security", OnlineSecurity],

        ["Tech Support", TechSupport],

        ["Contract", Contract],

        ["Payment Method", PaymentMethod],

        ["Monthly Charges", f"${MonthlyCharges:.2f}"],

        ["Total Charges", f"${TotalCharges:.2f}"],

    ]

    table = Table(customer_table, colWidths=[180,220])

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2563EB")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("BACKGROUND",(0,1),(-1,-1),colors.HexColor("#F8FAFC")),

        ("BOTTOMPADDING",(0,0),(-1,-1),8),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

    ]))

    story.append(table)

    story.append(Spacer(1,20))

    # ===========================
    # Why This Prediction?
    # ===========================

    story.append(Paragraph("<b>Why This Prediction?</b>", styles["Heading2"]))

    story.append(
    Paragraph(
        "<b>Key Factors Influencing Prediction</b>",
        styles["Heading3"],
    )
)

    for reason in reasons:

        story.append(
            Paragraph(
                f"✔ {reason}",
                styles["Normal"],
            )
        )

    story.append(Spacer(1, 20))

    # ===========================
    # Business Recommendation
    # ===========================

    story.append(Paragraph("<b>Business Recommendation</b>", styles["Heading2"]))

    risk, recommendations = get_recommendations(probability)

    story.append(
        Paragraph(
            "<b>Recommended Actions</b>",
            styles["Heading3"],
        )
    )

    for recommendation in recommendations:

        story.append(
            Paragraph(
                f"✔ {recommendation}",
                styles["Normal"],
            )
        )

    story.append(Spacer(1, 20))

    # ===========================
    # Footer
    # ===========================

    story.append(
        Paragraph(
            "<b>Generated by Customer Churn Prediction Dashboard</b>",
            styles["Heading3"],
        )
    )

    story.append(
        Paragraph(
            "Developed by Rayan Singh",
            styles["Normal"],
        )
    )

    story.append(Spacer(1,25))

    story.append(
        Paragraph(
            "<hr/>",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            "<b>Customer Churn Prediction Dashboard</b>",
            styles["Heading3"],
        )
    )

    story.append(
        Paragraph(
            "Developed by Rayan Singh",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"Generated on {datetime.now().strftime('%d %B %Y %I:%M %p')}",
            styles["Normal"],
        )
    )

    doc.build(story)

    return filename
