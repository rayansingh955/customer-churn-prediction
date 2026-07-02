def explain_prediction(
    tenure,
    Contract,
    InternetService,
    OnlineSecurity,
    TechSupport,
    PaymentMethod,
    PaperlessBilling,
    Dependents,
):
    """
    Returns the reasons behind the churn prediction.
    """

    reasons = []

    # High Risk Factors
    if tenure < 12:
        reasons.append("📅 Customer has a short tenure, making churn more likely.")

    if Contract == "Month-to-month":
        reasons.append("📄 Customer is on a Month-to-month contract.")

    if InternetService == "Fiber optic":
        reasons.append("🌐 Customer uses Fiber Optic Internet.")

    if OnlineSecurity == "No":
        reasons.append("🔒 Customer does not have Online Security.")

    if TechSupport == "No":
        reasons.append("🛠 Customer does not have Technical Support.")

    if PaymentMethod == "Electronic check":
        reasons.append("💳 Customer pays using Electronic Check.")

    if PaperlessBilling == "Yes":
        reasons.append("📧 Customer uses Paperless Billing.")

    # Low Risk Factors
    if tenure >= 24:
        reasons.append("✅ Customer has been with the company for a long time.")

    if Contract == "Two year":
        reasons.append("🤝 Customer has a long-term contract.")

    if OnlineSecurity == "Yes":
        reasons.append("🛡 Customer has Online Security enabled.")

    if TechSupport == "Yes":
        reasons.append("👨‍💻 Customer has Technical Support.")

    if Dependents == "Yes":
        reasons.append("👨‍👩‍👧 Customer has Dependents.")

    return reasons