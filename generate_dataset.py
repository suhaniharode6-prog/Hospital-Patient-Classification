"""
generate_dataset.py
--------------------
Generates a synthetic hospital patient dataset used to train the
Patient Risk Classification model.

Features used:
    Age                 : Patient age (years)
    BloodPressure       : Systolic BP (mmHg)
    HeartRate           : Beats per minute
    Temperature         : Body temperature (Fahrenheit)
    OxygenSaturation    : SpO2 (%)
    RespiratoryRate     : Breaths per minute
    ExistingConditions  : Number of pre-existing conditions (0-4)

Target:
    RiskCategory : Low / Medium / High  (patient triage class)

The data is generated with realistic rule-based logic + random noise
so the trained model reflects sensible medical thresholds while still
needing to learn from data (not just an if/else rule engine).
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N_SAMPLES = 1200


def generate_patient_row():
    age = int(np.clip(np.random.normal(45, 20), 1, 95))
    bp = int(np.clip(np.random.normal(120, 20), 80, 200))
    hr = int(np.clip(np.random.normal(80, 15), 40, 160))
    temp = round(np.clip(np.random.normal(98.6, 1.2), 95, 106), 1)
    spo2 = int(np.clip(np.random.normal(96, 3), 70, 100))
    resp = int(np.clip(np.random.normal(16, 4), 8, 40))
    conditions = np.random.choice([0, 1, 2, 3, 4], p=[0.45, 0.25, 0.15, 0.10, 0.05])

    # ---- Rule-based risk scoring (used to build the label) ----
    score = 0
    if age > 65:
        score += 2
    elif age > 45:
        score += 1

    if bp > 160 or bp < 90:
        score += 2
    elif bp > 140:
        score += 1

    if hr > 120 or hr < 50:
        score += 2
    elif hr > 100:
        score += 1

    if temp > 102:
        score += 2
    elif temp > 100.4:
        score += 1

    if spo2 < 90:
        score += 3
    elif spo2 < 95:
        score += 1

    if resp > 24 or resp < 10:
        score += 2
    elif resp > 20:
        score += 1

    score += conditions

    # add a little noise so the boundary isn't perfectly deterministic
    score += np.random.choice([-1, 0, 0, 0, 1])

    if score <= 3:
        risk = "Low"
    elif score <= 5:
        risk = "Medium"
    else:
        risk = "High"

    return {
        "Age": age,
        "BloodPressure": bp,
        "HeartRate": hr,
        "Temperature": temp,
        "OxygenSaturation": spo2,
        "RespiratoryRate": resp,
        "ExistingConditions": conditions,
        "RiskCategory": risk,
    }


def main():
    rows = [generate_patient_row() for _ in range(N_SAMPLES)]
    df = pd.DataFrame(rows)
    df.to_csv("patients_dataset.csv", index=False)
    print(f"Generated {len(df)} rows -> patients_dataset.csv")
    print(df["RiskCategory"].value_counts())


if __name__ == "__main__":
    main()
