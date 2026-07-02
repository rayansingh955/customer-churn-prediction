# Importing all the libraries
import streamlit as st
import pandas as pd
import numpy as np
import joblib

from datetime import datetime


from utils.prediction import predict_churn
from utils.recommendation import get_recommendations
from utils.explain import explain_prediction
from utils.report import generate_report

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CSS_FILE = BASE_DIR / "assets" / "style.css"

def load_css():
    with open(CSS_FILE) as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

columns = joblib.load("models/Columns.pkl")

# Page Configuration
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()








# Sidebar
with st.sidebar:

    st.title("📊 Customer Churn Prediction")

    st.write(...)

    st.success("Model")

    st.write("Balanced Logistic Regression")

    st.success("ROC-AUC")

    st.write("0.86")

    st.success("Recall")

    st.write("83%")

    st.success("Developer")

    st.write("Rayan Singh")

    st.write("---")

    st.info(
        """
        Predict whether
        a telecom customer
        is likely to churn.
        """
    )

# Title
st.markdown("""
<div class='main-title'>
📊 Customer Churn Prediction
</div>
""",unsafe_allow_html=True)

st.markdown("""
<div class='sub-title'>
Predict whether a telecom customer is likely to leave the company using Machine Learning.
</div>
""",unsafe_allow_html=True)

st.divider()

# Customer Information
st.markdown("""
<div class='section-title'>
👤 Customer Details
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    SeniorCitizen = st.selectbox(
        "Senior Citizen",
        ["No", "Yes"]
    )

    Partner = st.selectbox(
        "Partner",
        ["No", "Yes"]
    )

    Dependents = st.selectbox(
        "Dependents",
        ["No", "Yes"]
    )

with col2:
    tenure = st.slider(
        "Tenure (Months)",
        0, 72, 12
    )

    PhoneService = st.selectbox(
        "Phone Service",
        ["No", "Yes"]
    )

    MultipleLines = st.selectbox(
        "Multiple Lines",
        ["No", "Yes", "No phone service"]
    )

# Internet Services
st.markdown("""
<div class='section-title'>
🌐 Internet & Services
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    InternetService = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

    OnlineSecurity = st.selectbox(
        "Online Security",
        ["No", "Yes", "No internet service"]
    )

    OnlineBackup = st.selectbox(
        "Online Backup",
        ["No", "Yes", "No internet service"]
    )

with col2:

    DeviceProtection = st.selectbox(
        "Device Protection",
        ["No", "Yes", "No internet service"]
    )

    TechSupport = st.selectbox(
        "Tech Support",
        ["No", "Yes", "No internet service"]
    )

    StreamingTV = st.selectbox(
        "Streaming TV",
        ["No", "Yes", "No internet service"]
    )

StreamingMovies = st.selectbox(
    "Streaming Movies",
    ["No", "Yes", "No internet service"]
)

# Account Info
st.markdown("""
<div class='section-title'>
💳 Billing & Contract
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    Contract = st.selectbox(
        "Contract",
        ["Month-to-month", "One year", "Two year"]
    )

    PaperlessBilling = st.selectbox(
        "Paperless Billing",
        ["No", "Yes"]
    )

    PaymentMethod = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

with col2:

    MonthlyCharges = st.slider(
        "Monthly Charges",
        0.0, 120.0, 70.0
    )

    TotalCharges = st.number_input(
        "Total Charges",
        min_value=0.0,
        value=1000.0
    )

# Predict Button
st.write("")
st.write("")

predict = st.button(
    "🔍 Predict Customer Churn",
    use_container_width=True
)

# Create a dictionary from user inputs
if predict:
    user_data = {
        "SeniorCitizen": 1 if SeniorCitizen == "Yes" else 0,
        "Partner": 1 if Partner == "Yes" else 0,
        "Dependents": 1 if Dependents == "Yes" else 0,
        "tenure": tenure,
        "PhoneService": 1 if PhoneService == "Yes" else 0,
        "MultipleLines": MultipleLines,
        "InternetService": InternetService,
        "OnlineSecurity": OnlineSecurity,
        "OnlineBackup": OnlineBackup,
        "DeviceProtection": DeviceProtection,
        "TechSupport": TechSupport,
        "StreamingTV": StreamingTV,
        "StreamingMovies": StreamingMovies,
        "Contract": Contract,
        "PaperlessBilling": 1 if PaperlessBilling == "Yes" else 0,
        "PaymentMethod": PaymentMethod,
        "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges
    }

    # Convert to DataFrame
    user_df = pd.DataFrame([user_data])

    # One-Hot Encoding
    user_df = pd.get_dummies(user_df)

    # Replace True/False
    bool_cols = user_df.select_dtypes(include="bool").columns

    user_df[bool_cols] = user_df[bool_cols].astype(int)

    # Match Training Columns
    user_df = user_df.reindex(columns=columns, fill_value=0)

    # Scale the data

    prediction, probability = predict_churn(user_df)

    if probability >= 0.75:
        css_class = "high-risk"
        status = "🔴 HIGH CHURN RISK"

    elif probability >= 0.40:
        css_class = "medium-risk"
        status = "🟡 MEDIUM CHURN RISK"

    else:
        css_class = "low-risk"
        status = "🟢 LOW CHURN RISK"

# Display Prediction
    st.write("")
    st.divider()



    st.markdown(f"""
    <div class="hero-card {css_class}">

    <div class="hero-title">

    {status}

    </div>

    <div class="hero-prob">

    {probability*100:.2f}%

    </div>

    <div style="font-size:20px; opacity:.9;">
    Probability of Customer Churn
    </div>

    <br>

    <div class="hero-model">

    Prediction using Balanced Logistic Regression

    </div>

    </div>
    """, unsafe_allow_html=True)



    # Buisness recomendation

    st.markdown("## 💡 Business Recommendation")

    if probability >= 0.75:

        st.markdown("""
        <div class="recommend-card high-rec">

        <h3>🔴 High Risk Customer</h3>

        <p>This customer has a high probability of churning.</p>

        <b>Recommended Actions</b>

        <ul>
            <li>Offer a personalized discount</li>
            <li>Assign a dedicated customer support agent</li>
            <li>Recommend a long-term contract</li>
            <li>Contact the customer within 24 hours</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    elif probability >= 0.40:

        st.markdown("""
        <div class="recommend-card medium-rec">

        <h3>🟡 Medium Risk Customer</h3>

        <p>This customer may churn if service quality decreases.</p>

        <b>Recommended Actions</b>

        <ul>
            <li>Offer loyalty rewards</li>
            <li>Recommend additional value-added services</li>
            <li>Monitor customer activity regularly</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="recommend-card low-rec">

        <h3>🟢 Low Risk Customer</h3>

        <p>This customer is likely to stay with the company.</p>

        <b>Recommended Actions</b>

        <ul>
            <li>Maintain current service quality</li>
            <li>Keep customer engaged with new offers</li>
            <li>Continue regular communication</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 📌 Why This Prediction?")

    reasons = explain_prediction(
        tenure,
        Contract,
        InternetService,
        OnlineSecurity,
        TechSupport,
        PaymentMethod,
        PaperlessBilling,
        Dependents,
    )

    if len(reasons) > 0:

        for reason in reasons:

            st.markdown(f"""
            <div class="reason-card">
            {reason}
            </div>
            """, unsafe_allow_html=True)

    else:

        st.info("No significant churn indicators found.")

    st.markdown("# 📋 Customer Summary")
    st.write("")
    col1, col2 = st.columns(2)


    # Customer Profile Card
    with col1:

        st.markdown(f"""
        <div class="summary-card">

        <div class="summary-title">

        👤 Customer Profile

        </div>

        <div class="summary-item">
        <span>Senior Citizen</span>
        <span>{SeniorCitizen}</span>
        </div>

        <div class="summary-item">
        <span>Partner</span>
        <span>{Partner}</span>
        </div>

        <div class="summary-item">
        <span>Dependents</span>
        <span>{Dependents}</span>
        </div>

        <div class="summary-item">
        <span>Tenure</span>
        <span>{tenure} Months</span>
        </div>

        </div>
        """, unsafe_allow_html=True)

    # Services Card

    with col2:

        st.markdown(f"""
        <div class="summary-card">

        <div class="summary-title">

        🌐 Services

        </div>

        <div class="summary-item">
        <span>Internet</span>
        <span>{InternetService}</span>
        </div>

        <div class="summary-item">
        <span>Online Security</span>
        <span>{OnlineSecurity}</span>
        </div>

        <div class="summary-item">
        <span>Online Backup</span>
        <span>{OnlineBackup}</span>
        </div>

        <div class="summary-item">
        <span>Tech Support</span>
        <span>{TechSupport}</span>
        </div>

        </div>
        """, unsafe_allow_html=True)

    # Billing Card

    st.markdown(f"""
    <div class="summary-card">

    <div class="summary-title">

    💳 Billing Information

    </div>

    <div class="summary-item">
    <span>Contract</span>
    <span>{Contract}</span>
    </div>

    <div class="summary-item">
    <span>Payment Method</span>
    <span>{PaymentMethod}</span>
    </div>

    <div class="summary-item">
    <span>Monthly Charges</span>
    <span>${MonthlyCharges:.2f}</span>
    </div>

    <div class="summary-item">
    <span>Total Charges</span>
    <span>${TotalCharges:.2f}</span>
    </div>

    </div>
    """, unsafe_allow_html=True)

    pdf = generate_report(
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
    )

    with open(pdf, "rb") as file:

        st.download_button(
            "📄 Download Prediction Report",
            data=file,
            file_name="Customer_Churn_Report.pdf",
            mime="application/pdf",
        )

