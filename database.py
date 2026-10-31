"""
database.py
------------
Handles all SQLite database operations for the Hospital Patient
Classification System.

Database file: hospital.db
Tables: users, patients
    users: username, password, role
    patients: patient health and prediction records
    id                  INTEGER PRIMARY KEY AUTOINCREMENT
    name                TEXT
    age                 INTEGER
    blood_pressure      INTEGER
    heart_rate          INTEGER
    temperature         REAL
    oxygen_saturation   INTEGER
    respiratory_rate    INTEGER
    existing_conditions INTEGER
    predicted_risk      TEXT
    created_at          TEXT (timestamp)

This module is shared by both the GUI app (gui_app.py) and the
console app (console_app.py) so every prediction made by either
interface is saved to the same database.
"""

import sqlite3
from datetime import datetime
import hashlib

DB_NAME = "hospital.db"


def get_connection():
    """Return a new connection to the hospital database."""
    return sqlite3.connect(DB_NAME)


def _hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_db():
    """Create application tables and a default admin account."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            blood_pressure INTEGER NOT NULL,
            heart_rate INTEGER NOT NULL,
            temperature REAL NOT NULL,
            oxygen_saturation INTEGER NOT NULL,
            respiratory_rate INTEGER NOT NULL,
            existing_conditions INTEGER NOT NULL,
            predicted_risk TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Admin'
        )
    """)
    cur.execute("SELECT id FROM users WHERE username = ?", ("admin",))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", _hash_password("admin123"), "Admin")
        )
    conn.commit()
    conn.close()


def authenticate_user(username, password):
    """Return the user role when credentials are valid, otherwise None."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT role FROM users WHERE username = ? AND password = ?",
        (username.strip(), _hash_password(password))
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def insert_patient(name, age, bp, hr, temp, spo2, resp, conditions, risk):
    """Insert a new patient record with its predicted risk category."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO patients
        (name, age, blood_pressure, heart_rate, temperature,
         oxygen_saturation, respiratory_rate, existing_conditions,
         predicted_risk, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, age, bp, hr, temp, spo2, resp, conditions, risk,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id


def fetch_all_patients():
    """Return all patient records, most recent first."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def fetch_patient_by_id(patient_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    row = cur.fetchone()
    conn.close()
    return row


def delete_patient(patient_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    conn.close()


def count_by_risk():
    """Return a dict like {'Low': 10, 'Medium': 5, 'High': 2}."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT predicted_risk, COUNT(*) FROM patients GROUP BY predicted_risk")
    rows = cur.fetchall()
    conn.close()
    return {risk: count for risk, count in rows}


if __name__ == "__main__":
    init_db()
    print("Database initialized ->", DB_NAME)
