"""
gui_app.py
-----------
Colorful, professional Tkinter GUI for the Hospital Patient Classification System.

The ML prediction logic and SQLite database logic are unchanged.
Only the presentation/UI has been redesigned.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import database
import predictor
from login import LoginWindow


class HospitalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Patient Classification System")
        self.geometry("1180x760")
        self.minsize(1050, 680)
        self.configure(bg="#eef6ff")

        database.init_db()
        self.last_prediction = None
        self.current_user = None
        self.current_role = None

        self._build_style()
        # Keep the main window available so the login dialog cannot remain hidden.
        self.deiconify()
        self.after(100, self.show_login)

    # ================================================================
    # LOGIN / LOGOUT
    # ================================================================
    def show_login(self):
        login = LoginWindow(self, self.on_login_success)
        login.lift()
        login.attributes("-topmost", True)
        login.after(300, lambda: login.attributes("-topmost", False))

    def on_login_success(self, username, role):
        self.current_user = username
        self.current_role = role
        self.title(f"Hospital Patient Classification System - {username}")
        self.deiconify()
        self._build_layout()
        self.refresh_records()
        self.refresh_stats()

    def logout(self):
        if not messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=self):
            return
        for widget in self.winfo_children():
            widget.destroy()
        self.last_prediction = None
        self.current_user = None
        self.current_role = None
        # Keep the main window available so the login dialog cannot remain hidden.
        self.deiconify()
        self.after(100, self.show_login)

    # ================================================================
    # COLORS / STYLE
    # ================================================================
    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TNotebook", background="#eef6ff", borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            font=("Segoe UI", 11, "bold"),
            padding=(22, 12),
            background="#dceeff",
            foreground="#164a7a",
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#1479e8")],
            foreground=[("selected", "white")],
        )

        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 24, "bold"),
            foreground="white",
            background="#1268b3",
        )
        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11),
            foreground="#d8efff",
            background="#1268b3",
        )
        style.configure(
            "Section.TLabel",
            font=("Segoe UI", 16, "bold"),
            foreground="#174d7c",
            background="white",
        )
        style.configure(
            "Small.TLabel",
            font=("Segoe UI", 10),
            foreground="#61758a",
            background="white",
        )
        style.configure(
            "TEntry",
            font=("Segoe UI", 11),
            padding=7,
        )
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(18, 10),
            foreground="white",
            background="#1479e8",
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#0b5fba")],
            foreground=[("active", "white")],
        )
        style.configure(
            "Success.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(18, 10),
            foreground="white",
            background="#18a66a",
        )
        style.map(
            "Success.TButton",
            background=[("active", "#108552")],
            foreground=[("active", "white")],
        )
        style.configure(
            "Danger.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 8),
            foreground="white",
            background="#e65353",
        )
        style.map(
            "Danger.TButton",
            background=[("active", "#c83c3c")],
            foreground=[("active", "white")],
        )
        style.configure(
            "Treeview",
            font=("Segoe UI", 9),
            rowheight=30,
            background="white",
            fieldbackground="white",
            foreground="#183b56",
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background="#1479e8",
            foreground="white",
            padding=7,
        )
        style.map(
            "Treeview",
            background=[("selected", "#cfe7ff")],
            foreground=[("selected", "#123b60")],
        )

    # ================================================================
    # MAIN LAYOUT
    # ================================================================
    def _build_layout(self):
        # Header
        header = tk.Frame(self, bg="#1268b3", height=115)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg="#1268b3")
        left.pack(side="left", padx=28, pady=16)

        tk.Label(
            left,
            text="🏥  Hospital Patient Classification System",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg="#1268b3",
        ).pack(anchor="w")

        tk.Label(
            left,
            text="AI Powered  •  Better Prediction  •  Healthier Tomorrow",
            font=("Segoe UI", 11),
            fg="#d8efff",
            bg="#1268b3",
        ).pack(anchor="w", pady=(4, 0))

        right = tk.Frame(header, bg="#1268b3")
        right.pack(side="right", padx=25)

        tk.Label(
            right, text=f"👤  Logged in: {self.current_user} ({self.current_role})",
            font=("Segoe UI", 10, "bold"), fg="white", bg="#1268b3"
        ).pack(anchor="e", pady=(6, 6))
        tk.Button(
            right, text="🚪 Logout", command=self.logout,
            font=("Segoe UI", 10, "bold"), fg="white", bg="#0b5fba",
            activebackground="#084b92", activeforeground="white",
            relief="flat", cursor="hand2", padx=14, pady=6
        ).pack(anchor="e")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=14, pady=14)

        self.predict_tab = tk.Frame(notebook, bg="#eef6ff")
        self.records_tab = tk.Frame(notebook, bg="#eef6ff")
        self.stats_tab = tk.Frame(notebook, bg="#eef6ff")

        notebook.add(self.predict_tab, text="  👤  New Patient / Predict  ")
        notebook.add(self.records_tab, text="  📋  Patient Records  ")
        notebook.add(self.stats_tab, text="  📊  Statistics  ")

        self._build_predict_tab()
        self._build_records_tab()
        self._build_stats_tab()

    # ================================================================
    # PREDICTION TAB
    # ================================================================
    def _build_predict_tab(self):
        container = tk.Frame(self.predict_tab, bg="#eef6ff")
        container.pack(fill="both", expand=True, padx=8, pady=8)

        # ---------- LEFT CARD ----------
        form_card = tk.Frame(
            container,
            bg="white",
            highlightbackground="#c6def3",
            highlightthickness=1,
            bd=0,
        )
        form_card.pack(side="left", fill="both", expand=True, padx=(5, 8))

        title_bar = tk.Frame(form_card, bg="#e8f4ff", height=58)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)

        tk.Label(
            title_bar,
            text="👤  Enter Patient Details",
            font=("Segoe UI", 16, "bold"),
            fg="#174d7c",
            bg="#e8f4ff",
        ).pack(side="left", padx=20)

        form = tk.Frame(form_card, bg="white")
        form.pack(fill="both", expand=True, padx=22, pady=16)

        self.entries = {}
        fields = [
            ("Name", "name", "Enter patient name"),
            ("Age (years)", "age", "Enter age"),
            ("Blood Pressure - systolic (mmHg)", "bp", "Enter systolic BP"),
            ("Heart Rate (bpm)", "hr", "Enter heart rate"),
            ("Temperature (F)", "temp", "Enter temperature"),
            ("Oxygen Saturation SpO2 (%)", "spo2", "Enter SpO2 percentage"),
            ("Respiratory Rate (breaths/min)", "resp", "Enter respiratory rate"),
            ("Existing Conditions (0-10)", "conditions", "Enter conditions level"),
        ]

        for i, (label_text, key, placeholder) in enumerate(fields):
            tk.Label(
                form,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                fg="#254b6b",
                bg="white",
            ).grid(row=i, column=0, sticky="w", pady=7, padx=(0, 12))

            entry = ttk.Entry(form, width=27)
            entry.grid(row=i, column=1, sticky="ew", pady=7)
            self.entries[key] = entry

            # Light placeholder text. It disappears on first click.
            entry.insert(0, placeholder)
            entry.configure(foreground="#91a5b8")
            entry.bind(
                "<FocusIn>",
                lambda e, ent=entry, ph=placeholder: self._clear_placeholder(ent, ph),
            )
            entry.bind(
                "<FocusOut>",
                lambda e, ent=entry, ph=placeholder: self._restore_placeholder(ent, ph),
            )

        form.grid_columnconfigure(1, weight=1)

        buttons = tk.Frame(form_card, bg="white")
        buttons.pack(pady=(0, 22))

        ttk.Button(
            buttons,
            text="🧠  Predict Risk",
            command=self.on_predict,
            style="Primary.TButton",
        ).pack(side="left", padx=6)

        tk.Button(
            buttons,
            text="↻  Clear Form",
            command=self.on_clear,
            font=("Segoe UI", 11, "bold"),
            fg="white",
            bg="#71869a",
            activebackground="#596e81",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
        ).pack(side="left", padx=6)

        # ---------- RIGHT CARD ----------
        result_card = tk.Frame(
            container,
            bg="white",
            highlightbackground="#c6def3",
            highlightthickness=1,
            bd=0,
        )
        result_card.pack(side="right", fill="both", expand=True, padx=(8, 5))

        result_header = tk.Frame(result_card, bg="#3f55e8", height=58)
        result_header.pack(fill="x")
        result_header.pack_propagate(False)

        tk.Label(
            result_header,
            text="📊  Prediction Result",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#3f55e8",
        ).pack(side="left", padx=20)

        # Risk display
        risk_box = tk.Frame(result_card, bg="#edf5ff", highlightbackground="#c7def4",
                            highlightthickness=1)
        risk_box.pack(fill="x", padx=20, pady=(18, 12))

        self.risk_label = tk.Label(
            risk_box,
            text="—",
            font=("Segoe UI", 25, "bold"),
            fg="#174d7c",
            bg="#edf5ff",
        )
        self.risk_label.pack(pady=(15, 2))

        self.risk_caption = tk.Label(
            risk_box,
            text="Risk Level",
            font=("Segoe UI", 10, "bold"),
            fg="#53728e",
            bg="#edf5ff",
        )
        self.risk_caption.pack(pady=(0, 5))

        self.risk_message = tk.Label(
            risk_box,
            text="Enter patient details and predict risk.",
            font=("Segoe UI", 10),
            fg="#53728e",
            bg="#edf5ff",
            wraplength=420,
            justify="center",
        )
        self.risk_message.pack(padx=15, pady=(0, 14))

        # Probability box
        prob_box = tk.Frame(
            result_card,
            bg="#f7fbff",
            highlightbackground="#c7def4",
            highlightthickness=1,
        )
        prob_box.pack(fill="both", expand=True, padx=20, pady=8)

        tk.Label(
            prob_box,
            text="◔  Confidence Probabilities",
            font=("Segoe UI", 13, "bold"),
            fg="#174d7c",
            bg="#f7fbff",
        ).pack(anchor="w", padx=16, pady=(12, 4))

        self.prob_text = tk.Text(
            prob_box,
            height=7,
            width=35,
            state="disabled",
            font=("Consolas", 11),
            bg="white",
            fg="#234d6c",
            relief="flat",
            padx=14,
            pady=10,
        )
        self.prob_text.pack(fill="both", expand=True, padx=12, pady=(4, 12))

        self.save_button = ttk.Button(
            result_card,
            text="💾  Save to Database",
            command=self.on_save,
            state="disabled",
            style="Success.TButton",
        )
        self.save_button.pack(fill="x", padx=20, pady=10)

        # Legend
        legend = tk.Frame(result_card, bg="white")
        legend.pack(fill="x", padx=18, pady=(4, 18))

        self._legend_card(legend, "LOW", "0 – 0.33", "#18a66a", "#e7f8ef").pack(
            side="left", fill="both", expand=True, padx=3
        )
        self._legend_card(legend, "MEDIUM", "0.34 – 0.66", "#ef9518", "#fff4df").pack(
            side="left", fill="both", expand=True, padx=3
        )
        self._legend_card(legend, "HIGH", "0.67 – 1.00", "#ed4c5c", "#ffeaed").pack(
            side="left", fill="both", expand=True, padx=3
        )

    def _legend_card(self, parent, title, range_text, color, bg):
        card = tk.Frame(parent, bg=bg, highlightbackground=color, highlightthickness=1)
        tk.Label(
            card, text=f"●  {title} RISK", font=("Segoe UI", 9, "bold"),
            fg=color, bg=bg
        ).pack(anchor="w", padx=8, pady=(7, 1))
        tk.Label(
            card, text=range_text, font=("Segoe UI", 8),
            fg="#637d93", bg=bg
        ).pack(anchor="w", padx=8, pady=(0, 7))
        return card

    def _clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(foreground="#183b56")

    def _restore_placeholder(self, entry, placeholder):
        if not entry.get().strip():
            entry.insert(0, placeholder)
            entry.configure(foreground="#91a5b8")

    def _entry_value(self, key):
        value = self.entries[key].get().strip()
        placeholders = {
            "name": "Enter patient name",
            "age": "Enter age",
            "bp": "Enter systolic BP",
            "hr": "Enter heart rate",
            "temp": "Enter temperature",
            "spo2": "Enter SpO2 percentage",
            "resp": "Enter respiratory rate",
            "conditions": "Enter conditions level",
        }
        return "" if value == placeholders.get(key) else value

    # ================================================================
    # PREDICTION LOGIC - unchanged
    # ================================================================
    def on_predict(self):
        try:
            name = self._entry_value("name")
            if not name:
                raise ValueError("Please enter the patient's name.")

            age = int(self._entry_value("age"))
            bp = int(self._entry_value("bp"))
            hr = int(self._entry_value("hr"))
            temp = float(self._entry_value("temp"))
            spo2 = int(self._entry_value("spo2"))
            resp = int(self._entry_value("resp"))
            conditions = int(self._entry_value("conditions"))

            predictor.validate_inputs(age, bp, hr, temp, spo2, resp, conditions)

        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        try:
            risk, probs = predictor.predict_risk(
                age, bp, hr, temp, spo2, resp, conditions
            )
        except FileNotFoundError as e:
            messagebox.showerror("Model Not Found", str(e))
            return

        colors = {"Low": "#18a66a", "Medium": "#ef9518", "High": "#ed4c5c"}
        bg_colors = {"Low": "#e7f8ef", "Medium": "#fff4df", "High": "#ffeaed"}

        self.risk_label.config(
            text=f"{risk} Risk",
            foreground=colors.get(risk, "#174d7c"),
            background=bg_colors.get(risk, "#edf5ff"),
        )
        self.risk_caption.config(background=bg_colors.get(risk, "#edf5ff"))

        risk_messages = {
            "Low": "No critical risk indicated by the model. The patient appears stable based on the prediction.",
            "Medium": "Moderate risk indicated by the model. Additional monitoring and clinical review are recommended.",
            "High": "High risk indicated by the model. Immediate clinical attention and further evaluation are recommended.",
        }

        self.risk_message.config(
            text=risk_messages.get(risk, "Please review the prediction."),
            background=bg_colors.get(risk, "#edf5ff"),
        )

        self.prob_text.config(state="normal")
        self.prob_text.delete("1.0", tk.END)
        self.prob_text.insert(tk.END, "Confidence breakdown\n\n")

        for label, pct in probs.items():
            self.prob_text.insert(tk.END, f"  {label:<8}: {pct:>5}%\n")

        self.prob_text.config(state="disabled")

        self.last_prediction = {
            "name": name, "age": age, "bp": bp, "hr": hr, "temp": temp,
            "spo2": spo2, "resp": resp, "conditions": conditions, "risk": risk,
        }
        self.save_button.config(state="normal")

    def on_save(self):
        if not self.last_prediction:
            return

        p = self.last_prediction
        database.insert_patient(
            p["name"], p["age"], p["bp"], p["hr"], p["temp"],
            p["spo2"], p["resp"], p["conditions"], p["risk"]
        )

        messagebox.showinfo("Saved", f"Patient '{p['name']}' saved to database.")
        self.save_button.config(state="disabled")
        self.refresh_records()
        self.refresh_stats()

    def on_clear(self):
        placeholders = {
            "name": "Enter patient name",
            "age": "Enter age",
            "bp": "Enter systolic BP",
            "hr": "Enter heart rate",
            "temp": "Enter temperature",
            "spo2": "Enter SpO2 percentage",
            "resp": "Enter respiratory rate",
            "conditions": "Enter conditions level",
        }

        for key, entry in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, placeholders[key])
            entry.configure(foreground="#91a5b8")

        self.risk_label.config(text="—", foreground="#174d7c", background="#edf5ff")
        self.risk_caption.config(background="#edf5ff")
        self.risk_message.config(
            text="Enter patient details and predict risk.",
            background="#edf5ff"
        )

        self.prob_text.config(state="normal")
        self.prob_text.delete("1.0", tk.END)
        self.prob_text.insert(tk.END, "No prediction made yet\n\n"
                                       "Enter patient details and click Predict Risk.")
        self.prob_text.config(state="disabled")

        self.save_button.config(state="disabled")
        self.last_prediction = None

    # ================================================================
    # RECORDS TAB
    # ================================================================
    def _build_records_tab(self):
        card = tk.Frame(
            self.records_tab, bg="white",
            highlightbackground="#c6def3", highlightthickness=1
        )
        card.pack(fill="both", expand=True, padx=8, pady=8)

        top = tk.Frame(card, bg="#e8f4ff", height=58)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(
            top, text="📋  Patient Records",
            font=("Segoe UI", 16, "bold"),
            fg="#174d7c", bg="#e8f4ff"
        ).pack(side="left", padx=18)

        ttk.Button(
            top, text="↻ Refresh", command=self.refresh_records,
            style="Primary.TButton"
        ).pack(side="right", padx=8, pady=8)

        ttk.Button(
            top, text="🗑 Delete Selected", command=self.on_delete_selected,
            style="Danger.TButton"
        ).pack(side="right", padx=5, pady=8)

        table_frame = tk.Frame(card, bg="white")
        table_frame.pack(fill="both", expand=True, padx=12, pady=12)

        columns = (
            "id", "name", "age", "bp", "hr", "temp", "spo2",
            "resp", "cond", "risk", "saved_at"
        )
        headers = (
            "ID", "Name", "Age", "BP", "HR", "Temp", "SpO2",
            "Resp", "Cond", "Risk", "Saved At"
        )

        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=18
        )

        widths = {
            "id": 50, "name": 145, "age": 55, "bp": 65, "hr": 60,
            "temp": 70, "spo2": 65, "resp": 65, "cond": 65,
            "risk": 80, "saved_at": 145
        }

        for col, head in zip(columns, headers):
            self.tree.heading(col, text=head)
            self.tree.column(
                col, width=widths.get(col, 70),
                anchor="center",
                stretch=(col in ("name", "saved_at"))
            )

        self.tree.tag_configure("Low", foreground="#16885a", background="#f0fbf5")
        self.tree.tag_configure("Medium", foreground="#b86b00", background="#fff8eb")
        self.tree.tag_configure("High", foreground="#c5303e", background="#fff0f2")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_records(self):
        if not hasattr(self, "tree"):
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in database.fetch_all_patients():
            risk = row[9] if len(row) > 9 else ""
            self.tree.insert("", "end", values=row, tags=(risk,))

    def on_delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "No Selection", "Please select a record to delete."
            )
            return

        values = self.tree.item(selected[0], "values")
        patient_id = values[0]

        if messagebox.askyesno(
            "Confirm Delete", f"Delete patient record ID {patient_id}?"
        ):
            database.delete_patient(patient_id)
            self.refresh_records()
            self.refresh_stats()

    # ================================================================
    # STATISTICS TAB
    # ================================================================
    def _build_stats_tab(self):
        outer = tk.Frame(self.stats_tab, bg="#eef6ff")
        outer.pack(fill="both", expand=True, padx=8, pady=8)

        tk.Label(
            outer,
            text="📊  Risk Category Statistics",
            font=("Segoe UI", 20, "bold"),
            fg="#174d7c",
            bg="#eef6ff",
        ).pack(pady=(15, 8))

        tk.Label(
            outer,
            text="Overview of patient records classified by the ML model",
            font=("Segoe UI", 10),
            fg="#6c8398",
            bg="#eef6ff",
        ).pack(pady=(0, 18))

        self.stats_frame = tk.Frame(outer, bg="#eef6ff")
        self.stats_frame.pack(fill="x", padx=20)

        self.chart_frame = tk.Frame(
            outer,
            bg="white",
            highlightbackground="#c6def3",
            highlightthickness=1,
        )
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=(18, 0))

        ttk.Button(
            outer,
            text="↻  Refresh Statistics",
            command=self.refresh_stats,
            style="Primary.TButton",
        ).pack(pady=22)

    def refresh_stats(self):
        if not hasattr(self, "stats_frame"):
            return

        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        counts = database.count_by_risk()
        total = sum(counts.values())

        if total == 0:
            empty = tk.Frame(
                self.stats_frame, bg="white",
                highlightbackground="#c6def3", highlightthickness=1
            )
            empty.pack(fill="x", pady=10, ipady=35)

            tk.Label(
                empty,
                text="📋  No patient data yet.",
                font=("Segoe UI", 14, "bold"),
                fg="#61758a", bg="white"
            ).pack()

            tk.Label(
                self.chart_frame,
                text="Risk Distribution Graph",
                font=("Segoe UI", 15, "bold"),
                fg="#174d7c",
                bg="white",
            ).pack(pady=(18, 5))

            tk.Label(
                self.chart_frame,
                text="The graph will appear after patient records are saved.",
                font=("Segoe UI", 10),
                fg="#6c8398",
                bg="white",
            ).pack(pady=(0, 18))
            return

        risk_info = [
            ("Low", "#18a66a", "#e7f8ef"),
            ("Medium", "#ef9518", "#fff4df"),
            ("High", "#ed4c5c", "#ffeaed"),
        ]

        for risk, color, bg in risk_info:
            c = counts.get(risk, 0)
            pct = (c / total * 100) if total else 0

            card = tk.Frame(
                self.stats_frame,
                bg=bg,
                highlightbackground=color,
                highlightthickness=1,
                width=280,
                height=150,
            )
            card.pack(side="left", fill="both", expand=True, padx=7)
            card.pack_propagate(False)

            tk.Label(
                card, text=f"●  {risk} Risk",
                font=("Segoe UI", 15, "bold"),
                fg=color, bg=bg
            ).pack(anchor="w", padx=18, pady=(16, 5))

            tk.Label(
                card, text=str(c),
                font=("Segoe UI", 28, "bold"),
                fg="#234d6c", bg=bg
            ).pack(anchor="w", padx=18)

            tk.Label(
                card, text=f"{pct:.1f}% of all patients",
                font=("Segoe UI", 10),
                fg="#637d93", bg=bg
            ).pack(anchor="w", padx=18, pady=(0, 10))

        total_card = tk.Frame(
            self.stats_frame,
            bg="white",
            highlightbackground="#c6def3",
            highlightthickness=1,
        )
        total_card.pack(fill="x", pady=(18, 0))

        tk.Label(
            total_card,
            text=f"Total Patients: {total}",
            font=("Segoe UI", 16, "bold"),
            fg="#174d7c", bg="white"
        ).pack(pady=16)

        # Risk distribution bar graph
        tk.Label(
            self.chart_frame,
            text="📊  Risk Distribution Graph",
            font=("Segoe UI", 15, "bold"),
            fg="#174d7c",
            bg="white",
        ).pack(pady=(16, 4))

        tk.Label(
            self.chart_frame,
            text="Number of patients in each risk category",
            font=("Segoe UI", 10),
            fg="#6c8398",
            bg="white",
        ).pack(pady=(0, 5))

        canvas = tk.Canvas(
            self.chart_frame,
            height=270,
            bg="white",
            highlightthickness=0,
        )
        canvas.pack(fill="x", padx=25, pady=(0, 18))
        self.chart_frame.update_idletasks()

        chart_width = max(self.chart_frame.winfo_width() - 50, 500)
        chart_height = 220
        canvas.configure(width=chart_width, height=chart_height)

        left = 70
        right = chart_width - 30
        top = 20
        bottom = chart_height - 45
        max_count = max(
            counts.get("Low", 0),
            counts.get("Medium", 0),
            counts.get("High", 0),
            1,
        )

        for i in range(5):
            value = max_count * i / 4
            y = bottom - (bottom - top) * i / 4
            canvas.create_line(left, y, right, y, fill="#e4edf5")
            canvas.create_text(
                left - 12, y,
                text=f"{value:.0f}",
                fill="#6c8398",
                font=("Segoe UI", 9),
                anchor="e",
            )

        bar_data = [
            ("Low", counts.get("Low", 0), "#18a66a"),
            ("Medium", counts.get("Medium", 0), "#ef9518"),
            ("High", counts.get("High", 0), "#ed4c5c"),
        ]

        slot = (right - left) / 3
        bar_width = min(90, slot * 0.45)

        for i, (label, count, color) in enumerate(bar_data):
            center_x = left + slot * (i + 0.5)
            bar_height = ((bottom - top) * count / max_count)
            x1 = center_x - bar_width / 2
            x2 = center_x + bar_width / 2
            y1 = bottom - bar_height
            y2 = bottom

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
            canvas.create_text(
                center_x, y1 - 12,
                text=str(count),
                fill="#234d6c",
                font=("Segoe UI", 11, "bold"),
            )
            canvas.create_text(
                center_x, bottom + 18,
                text=label,
                fill="#234d6c",
                font=("Segoe UI", 10, "bold"),
            )

        canvas.create_line(left, bottom, right, bottom, fill="#b8cddd", width=1)


if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()

