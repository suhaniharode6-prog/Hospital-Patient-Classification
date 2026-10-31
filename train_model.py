"""
train_model.py
---------------
Trains a RandomForestClassifier on the synthetic patient dataset to
classify patients into risk categories: Low, Medium, High.

Run this once (or whenever you want to retrain) before using the
GUI or console application:

    python train_model.py

It saves two files:
    model.pkl   -> trained sklearn model
    scaler.pkl  -> fitted StandardScaler used to preprocess input
"""

import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

FEATURES = [
    "Age", "BloodPressure", "HeartRate", "Temperature",
    "OxygenSaturation", "RespiratoryRate", "ExistingConditions",
]
TARGET = "RiskCategory"


def main():
    df = pd.read_csv("patients_dataset.csv")

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)

    print(f"Test Accuracy: {acc * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Feature importance
    print("\nFeature Importances:")
    for feat, imp in sorted(zip(FEATURES, model.feature_importances_),
                             key=lambda x: -x[1]):
        print(f"  {feat:20s} {imp:.3f}")

    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print("\nSaved trained model  -> model.pkl")
    print("Saved fitted scaler  -> scaler.pkl")


if __name__ == "__main__":
    main()
