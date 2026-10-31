"""Login screen for the Hospital Patient Classification System."""

import tkinter as tk
from tkinter import messagebox
import database


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.parent = parent
        self.on_success = on_success
        self.title("Hospital System - Login")
        self.geometry("460x430")
        self.resizable(False, False)
        self.configure(bg="#eef6ff")
        self.protocol("WM_DELETE_WINDOW", parent.destroy)
        self.transient(parent)
        self.grab_set()

        card = tk.Frame(self, bg="white", highlightbackground="#c6def3", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=28, pady=28)

        tk.Label(card, text="🏥", font=("Segoe UI Emoji", 42), fg="#1268b3", bg="white").pack(pady=(20, 0))
        tk.Label(card, text="Hospital Patient Classification", font=("Segoe UI", 17, "bold"), fg="#174d7c", bg="white").pack(pady=(4, 2))
        tk.Label(card, text="Secure Login", font=("Segoe UI", 10), fg="#71869a", bg="white").pack(pady=(0, 18))

        form = tk.Frame(card, bg="white")
        form.pack(fill="x", padx=38)

        tk.Label(form, text="Username", font=("Segoe UI", 10, "bold"), fg="#254b6b", bg="white").pack(anchor="w")
        self.username = tk.Entry(form, font=("Segoe UI", 11), relief="solid", bd=1)
        self.username.pack(fill="x", ipady=7, pady=(4, 12))

        tk.Label(form, text="Password", font=("Segoe UI", 10, "bold"), fg="#254b6b", bg="white").pack(anchor="w")
        self.password = tk.Entry(form, show="•", font=("Segoe UI", 11), relief="solid", bd=1)
        self.password.pack(fill="x", ipady=7, pady=(4, 16))
        self.password.bind("<Return>", lambda e: self.login())

        tk.Button(form, text="🔐  LOGIN", command=self.login, font=("Segoe UI", 11, "bold"), fg="white", bg="#1479e8", activebackground="#0b5fba", activeforeground="white", relief="flat", cursor="hand2", pady=10).pack(fill="x")

        tk.Label(card, text="Authorized access only", font=("Segoe UI", 9), fg="#91a5b8", bg="white").pack(pady=(15, 5))
        tk.Label(card, text="Demo account: admin / admin123", font=("Segoe UI", 8), fg="#9aabba", bg="white").pack(pady=(0, 12))
        self.username.focus_set()

    def login(self):
        username = self.username.get().strip()
        password = self.password.get()
        if not username or not password:
            messagebox.showwarning("Login Required", "Please enter username and password.", parent=self)
            return
        role = database.authenticate_user(username, password)
        if role:
            self.grab_release()
            self.destroy()
            self.on_success(username, role)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.", parent=self)
            self.password.delete(0, tk.END)
            self.password.focus_set()
