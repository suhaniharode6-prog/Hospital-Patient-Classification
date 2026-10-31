"""
console_app.py
---------------
Command-line interface for the Hospital Patient Classification
System. Lets the user:
    1. Add a new patient (enter vitals -> get predicted risk -> saved to DB)
    2. View all saved patients
    3. View risk-category statistics
    4. Delete a patient record
    5. Exit

Run with:
    python console_app.py
"""

import database
import predictor


def print_header():
    print("=" * 60)
    print("   HOSPITAL PATIENT CLASSIFICATION SYSTEM - CONSOLE APP")
    print("=" * 60)


def print_menu():
    print("\nMain Menu")
    print("  1. Add new patient & predict risk")
    print("  2. View all patients")
    print("  3. View risk statistics")
    print("  4. Delete a patient record")
    print("  5. Exit")


def read_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Please enter a valid number.")


def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  Please enter a valid whole number.")


def add_patient():
    print("\n--- Add New Patient ---")
    name = input("Patient Name: ").strip()
    while not name:
        name = input("Patient Name (cannot be blank): ").strip()

    age = read_int("Age (years): ")
    bp = read_int("Blood Pressure - systolic (mmHg): ")
    hr = read_int("Heart Rate (bpm): ")
    temp = read_float("Temperature (F): ")
    spo2 = read_int("Oxygen Saturation SpO2 (%): ")
    resp = read_int("Respiratory Rate (breaths/min): ")
    conditions = read_int("Number of existing conditions (0-10): ")

    try:
        predictor.validate_inputs(age, bp, hr, temp, spo2, resp, conditions)
    except ValueError as e:
        print(f"\n  Input error: {e}")
        return

    risk, probs = predictor.predict_risk(age, bp, hr, temp, spo2, resp, conditions)

    patient_id = database.insert_patient(
        name, age, bp, hr, temp, spo2, resp, conditions, risk
    )

    print("\n  Prediction complete.")
    print(f"  Patient ID     : {patient_id}")
    print(f"  Predicted Risk : {risk}")
    print("  Probabilities  :", ", ".join(f"{k}: {v}%" for k, v in probs.items()))
    print("  Record saved to database.")


def view_patients():
    rows = database.fetch_all_patients()
    if not rows:
        print("\n  No patient records found yet.")
        return

    print(f"\n--- All Patients ({len(rows)} records) ---")
    header = (f"{'ID':<4}{'Name':<15}{'Age':<5}{'BP':<6}{'HR':<5}"
              f"{'Temp':<7}{'SpO2':<6}{'Resp':<6}{'Cond':<6}{'Risk':<8}{'Saved At'}")
    print(header)
    print("-" * len(header))
    for row in rows:
        (pid, name, age, bp, hr, temp, spo2, resp, cond, risk, created_at) = row
        print(f"{pid:<4}{name:<15}{age:<5}{bp:<6}{hr:<5}{temp:<7}{spo2:<6}"
              f"{resp:<6}{cond:<6}{risk:<8}{created_at}")


def view_stats():
    counts = database.count_by_risk()
    if not counts:
        print("\n  No data yet to calculate statistics.")
        return

    total = sum(counts.values())
    print("\n--- Risk Category Statistics ---")
    for risk in ["Low", "Medium", "High"]:
        c = counts.get(risk, 0)
        pct = (c / total * 100) if total else 0
        bar = "#" * int(pct / 2)
        print(f"  {risk:<8}: {c:<5} ({pct:5.1f}%) {bar}")
    print(f"  {'Total':<8}: {total}")


def delete_patient():
    view_patients()
    rows = database.fetch_all_patients()
    if not rows:
        return
    pid = read_int("\nEnter Patient ID to delete: ")
    existing = database.fetch_patient_by_id(pid)
    if not existing:
        print("  No record found with that ID.")
        return
    database.delete_patient(pid)
    print(f"  Patient ID {pid} deleted.")


def main():
    database.init_db()
    print_header()

    try:
        predictor._load()
    except FileNotFoundError as e:
        print(f"\n  WARNING: {e}")

    while True:
        print_menu()
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            add_patient()
        elif choice == "2":
            view_patients()
        elif choice == "3":
            view_stats()
        elif choice == "4":
            delete_patient()
        elif choice == "5":
            print("\nExiting. Goodbye!")
            break
        else:
            print("  Invalid option, please choose 1-5.")


if __name__ == "__main__":
    main()
