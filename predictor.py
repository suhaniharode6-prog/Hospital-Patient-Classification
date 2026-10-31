"""
predictor.py
-------------
Loads the trained model + scaler and exposes a single function,
predict_risk(), used by both the GUI and console applications.
"""

import pickle
import os
import pandas as pd

MODEL_PATH = "model.pkl"
SCALER_PATH = "scaler.pkl"

FEATURES = [
    "Age", "BloodPressure", "HeartRate", "Temperature",
    "OxygenSaturation", "RespiratoryRate", "ExistingConditions",
]

_model = None
_scaler = None


def _load():
    global _model, _scaler
    if _model is None or _scaler is None:
        if not (os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH)):
            raise FileNotFoundError(
                "model.pkl / scaler.pkl not found. "
                "Run 'python train_model.py' first to train the model."
            )
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
        with open(SCALER_PATH, "rb") as f:
            _scaler = pickle.load(f)
    return _model, _scaler


def predict_risk(age, bp, hr, temp, spo2, resp, conditions):
    """
    Predict the risk category for a single patient.

    Returns:
        (risk_label:str, probabilities:dict{label: prob})
    """
    model, scaler = _load()

    row = pd.DataFrame([[age, bp, hr, temp, spo2, resp, conditions]], columns=FEATURES)
    row_scaled = scaler.transform(row)

    pred = model.predict(row_scaled)[0]
    proba = model.predict_proba(row_scaled)[0]
    prob_dict = {label: round(p * 100, 1) for label, p in zip(model.classes_, proba)}

    return pred, prob_dict


def validate_inputs(age, bp, hr, temp, spo2, resp, conditions):
    """
    Basic range validation. Raises ValueError with a helpful message
    if something is out of a plausible clinical range.
    Returns nothing if all good.
    """
    checks = [
        (0 < age <= 120, "Age must be between 1 and 120."),
        (40 <= bp <= 260, "Blood Pressure (systolic) must be between 40 and 260 mmHg."),
        (20 <= hr <= 250, "Heart Rate must be between 20 and 250 bpm."),
        (90 <= temp <= 110, "Temperature must be between 90 and 110 F."),
        (0 <= spo2 <= 100, "Oxygen Saturation must be between 0 and 100%."),
        (5 <= resp <= 60, "Respiratory Rate must be between 5 and 60 breaths/min."),
        (0 <= conditions <= 10, "Existing Conditions must be between 0 and 10."),
    ]
    for ok, message in checks:
        if not ok:
            raise ValueError(message)
