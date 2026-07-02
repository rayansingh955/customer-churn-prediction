from pathlib import Path
import joblib

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load model and scaler only once
MODEL = joblib.load(BASE_DIR / "models" / "churn_prediction_model.pkl")
SCALER = joblib.load(BASE_DIR / "models" / "scaler.pkl")


def predict_churn(user_df):
    """
    Scale input data and return prediction & probability.
    """

    user_scaled = SCALER.transform(user_df)

    prediction = MODEL.predict(user_scaled)[0]

    probability = MODEL.predict_proba(user_scaled)[0][1]

    return prediction, probability