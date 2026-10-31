# Hospital Patient Classification System (AIML Project)

A complete Machine Learning based Hospital Patient Risk Classification
system, built in Python. The system predicts a patient's **risk
category (Low / Medium / High)** based on their vitals, and provides
both a **Tkinter GUI (window) application** and a **Console
application**, both backed by a shared **SQLite database**.

---

## 1. Project Overview

Hospitals need to quickly triage patients based on their vitals to
decide how urgently they need attention. This project uses a
**Random Forest Classifier** trained on patient vitals to predict a
risk category:

| Risk Category | Meaning                                   |
|----------------|--------------------------------------------|
| Low            | Patient is stable, routine care sufficient |
| Medium         | Patient needs monitoring / attention       |
| High           | Patient needs urgent/critical attention    |

### Input Features
- Age (years)
- Blood Pressure – systolic (mmHg)
- Heart Rate (bpm)
- Temperature (°F)
- Oxygen Saturation / SpO2 (%)
- Respiratory Rate (breaths/min)
- Number of Existing Conditions (0–10)

---

## 2. Project Structure

```
hospital_project/
│
├── generate_dataset.py   # Creates the synthetic training dataset (patients_dataset.csv)
├── train_model.py        # Trains the RandomForest model -> model.pkl, scaler.pkl
├── predictor.py           # Shared prediction helper used by GUI & console apps
├── database.py             # SQLite database layer (create table, insert, fetch, delete)
├── gui_app.py               # Tkinter GUI (window) application
├── console_app.py            # Command-line console application
├── patients_dataset.csv        # Generated synthetic dataset (1200 records)
├── model.pkl                    # Trained ML model (generated after training)
├── scaler.pkl                     # Fitted StandardScaler (generated after training)
├── requirements.txt                 # Python dependencies
└── README.md                          # This file
```

---

## 3. How It Works (Architecture)

```
                    ┌──────────────────────┐
                    │ generate_dataset.py  │
                    │  (synthetic data)    │
                    └──────────┬───────────┘
                               │ patients_dataset.csv
                               ▼
                    ┌──────────────────────┐
                    │   train_model.py     │
                    │ (RandomForest + StdScaler) │
                    └──────────┬───────────┘
                               │ model.pkl / scaler.pkl
                               ▼
                    ┌──────────────────────┐
                    │    predictor.py      │◄──────────────┐
                    │  predict_risk()      │                │
                    └──────────┬───────────┘                │
                               │                             │
              ┌────────────────┴───────────────┐            │
              ▼                                 ▼            │
    ┌──────────────────┐             ┌──────────────────┐    │
    │    gui_app.py     │             │  console_app.py   │────┘
    │ (Tkinter Window)   │             │ (CLI Menu)         │
    └─────────┬──────────┘             └─────────┬──────────┘
              │                                    │
              └───────────────┬────────────────────┘
                               ▼
                      ┌──────────────────┐
                      │   database.py     │
                      │  (SQLite - hospital.db) │
                      └──────────────────┘
```

Both the GUI and console apps call the **same** `predictor.py` and
**same** `database.py`, so every patient added from either interface
is saved into the single shared `hospital.db` file.

---

## 4. Setup Instructions

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Generate the dataset
```bash
python generate_dataset.py
```
This creates `patients_dataset.csv` with 1200 synthetic patient
records.

### Step 3: Train the model
```bash
python train_model.py
```
This prints accuracy/classification report and saves `model.pkl` and
`scaler.pkl`.

### Step 4: Run the GUI application
```bash
python gui_app.py
```

### Step 5: Run the Console application
```bash
python console_app.py
```

Both applications automatically create `hospital.db` (SQLite) the
first time they run.

---

## 5. GUI Application (gui_app.py)

Three tabs:
1. **New Patient / Predict** – Enter vitals → click **Predict Risk**
   → see risk category + confidence % for each class → click
   **Save to Database** to store the record.
2. **Patient Records** – Table view of all saved patients, with
   Refresh and Delete Selected buttons.
3. **Statistics** – Shows count and percentage of patients in each
   risk category.

## 6. Console Application (console_app.py)

A simple numbered menu:
```
1. Add new patient & predict risk
2. View all patients
3. View risk statistics
4. Delete a patient record
5. Exit
```

---

## 7. Model Details

- **Algorithm**: Random Forest Classifier (`n_estimators=200,
  max_depth=8, class_weight="balanced"`)
- **Preprocessing**: StandardScaler on all numeric features
- **Train/Test split**: 80/20, stratified by risk category
- **Typical performance**: ~78–80% test accuracy (synthetic data)

You can regenerate the dataset with different randomness or expand
`generate_dataset.py`'s rule logic, then re-run `train_model.py` to
retrain.

## 8. Database Schema (SQLite: hospital.db)

Table `patients`:

| Column              | Type    |
|---------------------|---------|
| id                  | INTEGER PRIMARY KEY AUTOINCREMENT |
| name                | TEXT    |
| age                 | INTEGER |
| blood_pressure      | INTEGER |
| heart_rate          | INTEGER |
| temperature         | REAL    |
| oxygen_saturation   | INTEGER |
| respiratory_rate    | INTEGER |
| existing_conditions | INTEGER |
| predicted_risk      | TEXT    |
| created_at          | TEXT (timestamp) |

---

## 9. Notes for Viva / Presentation

- This is a **supervised, multi-class classification** ML problem.
- Explain: data generation → preprocessing (scaling) → model
  training (Random Forest) → evaluation (accuracy, confusion
  matrix) → deployment (GUI + console using the saved model).
- Mention that in a real hospital system, the synthetic dataset
  would be replaced with real, anonymized patient records (with
  appropriate ethical/privacy approvals).
- You can extend this project further by adding: login/authentication,
  charts (matplotlib) in the GUI, exporting records to Excel/PDF, or
  swapping SQLite for MySQL/PostgreSQL for a multi-user setup.


## Privacy and Demo Login

- The local SQLite database (`hospital.db`) is intentionally not included in this GitHub-ready package because it can contain patient records.
- On first run, the application creates a fresh local database.
- Demo login shown in the application: `admin` / `admin123`. This is for a college demonstration only; change it before using the application with real users.
- This is an educational project, not a medical device. Predictions must not be used for real clinical decisions.
