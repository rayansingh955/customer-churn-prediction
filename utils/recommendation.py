def get_recommendations(probability):
    """
    Returns risk level and business recommendations
    based on churn probability.
    """

    if probability >= 0.75:

        risk = "High Risk"

        recommendations = [
            "Offer personalized discount",
            "Assign dedicated customer support",
            "Recommend a long-term contract",
            "Contact customer immediately"
        ]

    elif probability >= 0.40:

        risk = "Medium Risk"

        recommendations = [
            "Offer loyalty rewards",
            "Recommend additional value-added services",
            "Monitor customer activity regularly"
        ]

    else:

        risk = "Low Risk"

        recommendations = [
            "Maintain current service quality",
            "Keep customer engaged",
            "Send appreciation or loyalty offers"
        ]

    return risk, recommendations