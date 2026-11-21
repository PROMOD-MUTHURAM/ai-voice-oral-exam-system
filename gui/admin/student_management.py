import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
from datetime import datetime


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ============================================================
# BACKEND
# ============================================================

BACKEND_DIR = os.path.join(
    BASE_DIR,
    "backend"
)


STUDENTS_DIR = os.path.join(
    BACKEND_DIR,
    "students"
)


os.makedirs(
    STUDENTS_DIR,
    exist_ok=True
)


# ============================================================
# MAXIMIZE WINDOW
# ============================================================

def maximize_window(window):

    if window is None:
        return

    try:
        window.state("zoomed")

        window.after(
            100,
            lambda: safe_maximize(window)
        )

    except Exception as e:
        print(
            "Could not maximize window:",
            e
        )


def safe_maximize(window):

    try:

        if window.winfo_exists():
            window.state("zoomed")

    except Exception:
        pass


# ============================================================
# RESTORE WINDOW
# ============================================================

def restore_window(window):

    if window is None:
        return

    try:

        if window.winfo_exists():

            window.deiconify()

            maximize_window(
                window
            )

            window.lift()

            window.focus_force()

    except Exception as e:

        print(
            "Could not restore window:",
            e
        )


# ============================================================
# STUDENT MANAGEMENT
# ============================================================

class StudentManagement:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        self.parent_window = parent_window

        self.selected_student_id = None


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Student Management - AI Oral Examination System"
        )

        self.root.geometry(
            "1100x750"
        )

        self.root.minsize(
            900,
            650
        )

        self.root.configure(
            bg="#f4f6f8"
        )


        maximize_window(
            self.root
        )


        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.back
        )


        # ----------------------------------------------------
        # CREATE GUI
        # ----------------------------------------------------

        self.create_interface()

        self.clear_form()

        self.load_students()


    # ========================================================
    # CREATE INTERFACE
    # ========================================================

    def create_interface(self):

        main_frame = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )

        main_frame.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # FIXED BOTTOM BACK BUTTON
        # ====================================================

        back_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8",
            height=65
        )

        back_frame.pack(
            side="bottom",
            fill="x"
        )

        back_frame.pack_propagate(
            False
        )

        tk.Button(
            back_frame,
            text="BACK TO ADMIN CONTROL PANEL",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=28,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        ).pack(
            pady=8
        )


        # ====================================================
        # HEADER
        # ====================================================

        header_frame = tk.Frame(
            main_frame,
            bg="#1f2937",
            height=110
        )

        header_frame.pack(
            fill="x"
        )

        header_frame.pack_propagate(
            False
        )


        tk.Label(
            header_frame,
            text="STUDENT MANAGEMENT",
            font=("Arial", 28, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(20, 3)
        )


        tk.Label(
            header_frame,
            text="Create, manage and control student accounts",
            font=("Arial", 11),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack()


        # ====================================================
        # CONTENT
        # ====================================================

        content_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        content_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(20, 5)
        )


        # ====================================================
        # FORM CARD
        # ====================================================

        form_card = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid",
            padx=25,
            pady=18
        )

        form_card.pack(
            fill="x",
            pady=(0, 15)
        )


        tk.Label(
            form_card,
            text="Student Information",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#111827"
        ).grid(
            row=0,
            column=0,
            columnspan=6,
            sticky="w",
            pady=(0, 12)
        )


        # ====================================================
        # STUDENT ID
        # ====================================================

        tk.Label(
            form_card,
            text="Student ID",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=6
        )


        self.student_id_entry = ttk.Entry(
            form_card,
            width=23
        )

        self.student_id_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=6,
            sticky="w"
        )


        # ====================================================
        # STUDENT NAME
        # ====================================================

        tk.Label(
            form_card,
            text="Student Name",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=(20, 0),
            pady=6
        )


        self.name_entry = ttk.Entry(
            form_card,
            width=23
        )

        self.name_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=6,
            sticky="w"
        )


        # ====================================================
        # AGE
        # ====================================================

        tk.Label(
            form_card,
            text="Age (Optional)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=1,
            column=4,
            sticky="w",
            padx=(20, 0),
            pady=6
        )


        self.age_entry = ttk.Entry(
            form_card,
            width=15
        )

        self.age_entry.grid(
            row=1,
            column=5,
            padx=10,
            pady=6,
            sticky="w"
        )


        # ====================================================
        # GENDER
        # ====================================================

        tk.Label(
            form_card,
            text="Gender (Optional)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=6
        )


        self.gender_combo = ttk.Combobox(
            form_card,
            width=20,
            state="readonly",
            values=[
                "",
                "Male",
                "Female",
                "Other"
            ]
        )

        self.gender_combo.grid(
            row=2,
            column=1,
            padx=10,
            pady=6,
            sticky="w"
        )

        self.gender_combo.set("")


        # ====================================================
        # DEPARTMENT
        # ====================================================

        tk.Label(
            form_card,
            text="Department (Optional)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=2,
            column=2,
            sticky="w",
            padx=(20, 0),
            pady=6
        )


        self.department_entry = ttk.Entry(
            form_card,
            width=23
        )

        self.department_entry.grid(
            row=2,
            column=3,
            padx=10,
            pady=6,
            sticky="w"
        )


        # ====================================================
        # CLASS
        # ====================================================

        tk.Label(
            form_card,
            text="Class (Optional)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=2,
            column=4,
            sticky="w",
            padx=(20, 0),
            pady=6
        )


        self.class_entry = ttk.Entry(
            form_card,
            width=15
        )

        self.class_entry.grid(
            row=2,
            column=5,
            padx=10,
            pady=6,
            sticky="w"
        )


        # ====================================================
        # EMAIL
        # ====================================================

        tk.Label(
            form_card,
            text="Email (Optional)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=6
        )


        self.email_entry = ttk.Entry(
            form_card,
            width=23
        )

        self.email_entry.grid(
            row=3,
            column=1,
            padx=10,
            pady=6,
            sticky="w"
        )


        # ====================================================
        # PHONE
        # ====================================================

        tk.Label(
            form_card,
            text="Phone (Optional)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=3,
            column=2,
            sticky="w",
            padx=(20, 0),
            pady=6
        )


        self.phone_entry = ttk.Entry(
            form_card,
            width=23
        )

        self.phone_entry.grid(
            row=3,
            column=3,
            padx=10,
            pady=6,
            sticky="w"
        )


        # ====================================================
        # PASSWORD
        # ====================================================

        tk.Label(
            form_card,
            text="Password",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=3,
            column=4,
            sticky="w",
            padx=(20, 0),
            pady=6
        )


        password_frame = tk.Frame(
            form_card,
            bg="white"
        )

        password_frame.grid(
            row=3,
            column=5,
            padx=10,
            pady=6,
            sticky="w"
        )


        self.password_entry = ttk.Entry(
            password_frame,
            width=12,
            show="*"
        )

        self.password_entry.pack(
            side="left"
        )


        self.show_password_var = tk.BooleanVar(
            value=False
        )


        tk.Checkbutton(
            password_frame,
            text="Show",
            variable=self.show_password_var,
            command=self.toggle_password,
            bg="white",
            activebackground="white"
        ).pack(
            side="left",
            padx=4
        )


        # ====================================================
        # STATUS
        # ====================================================

        tk.Label(
            form_card,
            text="Status",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=6
        )


        self.status_combo = ttk.Combobox(
            form_card,
            width=20,
            state="readonly",
            values=[
                "Active",
                "Inactive"
            ]
        )

        self.status_combo.grid(
            row=4,
            column=1,
            padx=10,
            pady=6,
            sticky="w"
        )

        self.status_combo.set(
            "Active"
        )


        # ====================================================
        # FORM BUTTONS
        # ====================================================

        form_button_frame = tk.Frame(
            form_card,
            bg="white"
        )

        form_button_frame.grid(
            row=4,
            column=2,
            columnspan=4,
            pady=6
        )


        tk.Button(
            form_button_frame,
            text="ADD STUDENT",
            font=("Arial", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=17,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.add_student
        ).grid(
            row=0,
            column=0,
            padx=5
        )


        tk.Button(
            form_button_frame,
            text="UPDATE STUDENT",
            font=("Arial", 10, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=17,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.update_student
        ).grid(
            row=0,
            column=1,
            padx=5
        )


        tk.Button(
            form_button_frame,
            text="CLEAR",
            font=("Arial", 10, "bold"),
            bg="#f59e0b",
            fg="white",
            activebackground="#d97706",
            activeforeground="white",
            width=17,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.clear_form
        ).grid(
            row=0,
            column=2,
            padx=5
        )


        # ====================================================
        # STUDENT LIST CARD
        # ====================================================

        list_card = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )

        list_card.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # SEARCH
        # ====================================================

        search_frame = tk.Frame(
            list_card,
            bg="white"
        )

        search_frame.pack(
            fill="x",
            pady=(0, 10)
        )


        tk.Label(
            search_frame,
            text="Search Student:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            side="left"
        )


        self.search_entry = ttk.Entry(
            search_frame,
            width=35
        )

        self.search_entry.pack(
            side="left",
            padx=10
        )


        self.search_entry.bind(
            "<KeyRelease>",
            self.search_students
        )


        tk.Button(
            search_frame,
            text="REFRESH",
            font=("Arial", 9, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=12,
            bd=0,
            cursor="hand2",
            command=self.load_students
        ).pack(
            side="left",
            padx=5
        )


        tk.Button(
            search_frame,
            text="DELETE SELECTED",
            font=("Arial", 9, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            width=16,
            bd=0,
            cursor="hand2",
            command=self.delete_student
        ).pack(
            side="left",
            padx=5
        )


        # ====================================================
        # TABLE
        # ====================================================

        table_frame = tk.Frame(
            list_card,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True
        )


        columns = (
            "student_id",
            "name",
            "age",
            "gender",
            "department",
            "class",
            "email",
            "phone",
            "status"
        )


        self.student_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )


        # ----------------------------------------------------
        # HEADINGS
        # ----------------------------------------------------

        self.student_tree.heading(
            "student_id",
            text="Student ID"
        )

        self.student_tree.heading(
            "name",
            text="Student Name"
        )

        self.student_tree.heading(
            "age",
            text="Age"
        )

        self.student_tree.heading(
            "gender",
            text="Gender"
        )

        self.student_tree.heading(
            "department",
            text="Department"
        )

        self.student_tree.heading(
            "class",
            text="Class"
        )

        self.student_tree.heading(
            "email",
            text="Email"
        )

        self.student_tree.heading(
            "phone",
            text="Phone"
        )

        self.student_tree.heading(
            "status",
            text="Status"
        )


        # ----------------------------------------------------
        # COLUMN WIDTHS
        # ----------------------------------------------------

        self.student_tree.column(
            "student_id",
            width=110,
            anchor="center"
        )

        self.student_tree.column(
            "name",
            width=180
        )

        self.student_tree.column(
            "age",
            width=60,
            anchor="center"
        )

        self.student_tree.column(
            "gender",
            width=90,
            anchor="center"
        )

        self.student_tree.column(
            "department",
            width=150
        )

        self.student_tree.column(
            "class",
            width=130
        )

        self.student_tree.column(
            "email",
            width=220
        )

        self.student_tree.column(
            "phone",
            width=130
        )

        self.student_tree.column(
            "status",
            width=100,
            anchor="center"
        )


        # ====================================================
        # SCROLLBARS
        # ====================================================

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.student_tree.yview
        )


        horizontal_scrollbar = ttk.Scrollbar(
            list_card,
            orient="horizontal",
            command=self.student_tree.xview
        )


        self.student_tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )


        self.student_tree.pack(
            side="left",
            fill="both",
            expand=True
        )


        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )


        horizontal_scrollbar.pack(
            side="bottom",
            fill="x"
        )


        self.student_tree.bind(
            "<Double-1>",
            self.select_student
        )





    # ========================================================
    # TOGGLE PASSWORD
    # ========================================================

    def toggle_password(self):

        if self.show_password_var.get():

            self.password_entry.config(
                show=""
            )

        else:

            self.password_entry.config(
                show="*"
            )


    # ========================================================
    # GET STUDENT FILE
    # ========================================================

    def get_student_file(
        self,
        student_id
    ):

        return os.path.join(
            STUDENTS_DIR,
            f"{student_id}.json"
        )


    # ========================================================
    # GENERATE STUDENT ID
    # ========================================================

    def generate_student_id(self):

        number = 1

        while True:

            student_id = (
                f"STU{number:04d}"
            )

            file_path = self.get_student_file(
                student_id
            )

            if not os.path.exists(
                file_path
            ):

                return student_id

            number += 1


    # ========================================================
    # CLEAR FORM
    # ========================================================

    def clear_form(self):

        self.selected_student_id = None


        self.student_id_entry.delete(
            0,
            tk.END
        )

        self.student_id_entry.insert(
            0,
            self.generate_student_id()
        )


        self.name_entry.delete(
            0,
            tk.END
        )


        self.age_entry.delete(
            0,
            tk.END
        )


        self.gender_combo.set(
            ""
        )


        self.department_entry.delete(
            0,
            tk.END
        )


        self.class_entry.delete(
            0,
            tk.END
        )


        self.email_entry.delete(
            0,
            tk.END
        )


        self.phone_entry.delete(
            0,
            tk.END
        )


        self.password_entry.delete(
            0,
            tk.END
        )


        self.status_combo.set(
            "Active"
        )


        self.show_password_var.set(
            False
        )

        self.password_entry.config(
            show="*"
        )


    # ========================================================
    # VALIDATE FORM
    # ========================================================

    def validate_form(self):

        student_id = (
            self.student_id_entry
            .get()
            .strip()
            .upper()
        )

        name = (
            self.name_entry
            .get()
            .strip()
        )

        age = (
            self.age_entry
            .get()
            .strip()
        )

        gender = (
            self.gender_combo
            .get()
            .strip()
        )

        department = (
            self.department_entry
            .get()
            .strip()
        )

        student_class = (
            self.class_entry
            .get()
            .strip()
        )

        email = (
            self.email_entry
            .get()
            .strip()
        )

        phone = (
            self.phone_entry
            .get()
            .strip()
        )

        password = (
            self.password_entry
            .get()
            .strip()
        )

        status = (
            self.status_combo
            .get()
            .strip()
        )


        if not student_id:

            messagebox.showwarning(
                "Invalid Student",
                "Student ID is required.",
                parent=self.root
            )

            return None


        if not name:

            messagebox.showwarning(
                "Invalid Student",
                "Student name is required.",
                parent=self.root
            )

            return None


        # ----------------------------------------------------
        # OPTIONAL AGE VALIDATION
        # ----------------------------------------------------

        if age:

            if not age.isdigit():

                messagebox.showwarning(
                    "Invalid Age",
                    "Age must contain numbers only.",
                    parent=self.root
                )

                return None


            age_number = int(age)


            if age_number < 1 or age_number > 120:

                messagebox.showwarning(
                    "Invalid Age",
                    "Please enter a valid age.",
                    parent=self.root
                )

                return None


        if not password:

            messagebox.showwarning(
                "Invalid Student",
                "Student password is required.",
                parent=self.root
            )

            return None


        if not status:

            status = "Active"


        return {

            "student_id": student_id,

            "student_name": name,

            "age": age,

            "gender": gender,

            "department": department,

            "class": student_class,

            "email": email,

            "phone": phone,

            "password": password,

            "status": status
        }


    # ========================================================
    # ADD STUDENT
    # ========================================================

    def add_student(self):

        data = self.validate_form()


        if data is None:
            return


        student_id = data["student_id"]


        file_path = self.get_student_file(
            student_id
        )


        if os.path.exists(
            file_path
        ):

            messagebox.showwarning(
                "Student Exists",
                (
                    f"Student ID {student_id} "
                    "already exists."
                ),
                parent=self.root
            )

            return


        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        student_data = {

            "student_id": student_id,

            "student_name": data[
                "student_name"
            ],

            "age": data[
                "age"
            ],

            "gender": data[
                "gender"
            ],

            "department": data[
                "department"
            ],

            "class": data[
                "class"
            ],

            "email": data[
                "email"
            ],

            "phone": data[
                "phone"
            ],

            "password": data[
                "password"
            ],

            "status": data[
                "status"
            ],

            "created_at": now,

            "updated_at": now
        }


        try:

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    student_data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )


        except Exception as e:

            messagebox.showerror(
                "Save Error",
                (
                    "Could not create the student.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        messagebox.showinfo(
            "Student Created",
            (
                "Student account created successfully.\n\n"
                f"Student ID: {student_id}\n"
                f"Student Name: {data['student_name']}\n"
                f"Age: {data['age'] or 'Not provided'}\n"
                f"Gender: {data['gender'] or 'Not provided'}\n"
                f"Department: {data['department'] or 'Not provided'}\n"
                f"Class: {data['class'] or 'Not provided'}\n\n"
                "The password entered here will be used "
                "by the student to log in to the examination."
            ),
            parent=self.root
        )


        self.load_students()

        self.clear_form()


    # ========================================================
    # LOAD STUDENTS
    # ========================================================

    def load_students(self):

        for item in self.student_tree.get_children():

            self.student_tree.delete(
                item
            )


        if not os.path.exists(
            STUDENTS_DIR
        ):
            return


        try:

            files = os.listdir(
                STUDENTS_DIR
            )

        except Exception as e:

            messagebox.showerror(
                "Student Error",
                (
                    "Could not access the students folder.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        students = []


        for filename in files:

            if not filename.lower().endswith(
                ".json"
            ):
                continue


            file_path = os.path.join(
                STUDENTS_DIR,
                filename
            )


            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    student = json.load(
                        file
                    )


                if not isinstance(
                    student,
                    dict
                ):
                    continue


                students.append(
                    student
                )


            except Exception:
                continue


        students.sort(
            key=lambda student:
            str(
                student.get(
                    "student_id",
                    ""
                )
            ).lower()
        )


        for student in students:

            self.student_tree.insert(
                "",
                "end",
                values=(
                    student.get(
                        "student_id",
                        ""
                    ),

                    student.get(
                        "student_name",
                        ""
                    ),

                    student.get(
                        "age",
                        ""
                    ),

                    student.get(
                        "gender",
                        ""
                    ),

                    student.get(
                        "department",
                        ""
                    ),

                    student.get(
                        "class",
                        ""
                    ),

                    student.get(
                        "email",
                        ""
                    ),

                    student.get(
                        "phone",
                        ""
                    ),

                    student.get(
                        "status",
                        "Active"
                    )
                )
            )


    # ========================================================
    # SEARCH STUDENTS
    # ========================================================

    def search_students(
        self,
        event=None
    ):

        search_text = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )


        for item in self.student_tree.get_children():

            self.student_tree.delete(
                item
            )


        if not os.path.exists(
            STUDENTS_DIR
        ):
            return


        try:

            files = os.listdir(
                STUDENTS_DIR
            )

        except Exception:
            return


        for filename in files:

            if not filename.lower().endswith(
                ".json"
            ):
                continue


            file_path = os.path.join(
                STUDENTS_DIR,
                filename
            )


            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    student = json.load(
                        file
                    )


                if not isinstance(
                    student,
                    dict
                ):
                    continue


                searchable_values = [

                    str(
                        student.get(
                            "student_id",
                            ""
                        )
                    ),

                    str(
                        student.get(
                            "student_name",
                            ""
                        )
                    ),

                    str(
                        student.get(
                            "age",
                            ""
                        )
                    ),

                    str(
                        student.get(
                            "gender",
                            ""
                        )
                    ),

                    str(
                        student.get(
                            "department",
                            ""
                        )
                    ),

                    str(
                        student.get(
                            "class",
                            ""
                        )
                    ),

                    str(
                        student.get(
                            "email",
                            ""
                        )
                    ),

                    str(
                        student.get(
                            "phone",
                            ""
                        )
                    )
                ]


                searchable_text = " ".join(
                    searchable_values
                ).lower()


                if (
                    not search_text
                    or search_text in searchable_text
                ):

                    self.student_tree.insert(
                        "",
                        "end",
                        values=(
                            student.get(
                                "student_id",
                                ""
                            ),

                            student.get(
                                "student_name",
                                ""
                            ),

                            student.get(
                                "age",
                                ""
                            ),

                            student.get(
                                "gender",
                                ""
                            ),

                            student.get(
                                "department",
                                ""
                            ),

                            student.get(
                                "class",
                                ""
                            ),

                            student.get(
                                "email",
                                ""
                            ),

                            student.get(
                                "phone",
                                ""
                            ),

                            student.get(
                                "status",
                                "Active"
                            )
                        )
                    )


            except Exception:
                continue


    # ========================================================
    # SELECT STUDENT
    # ========================================================

    def select_student(
        self,
        event=None
    ):

        selected = (
            self.student_tree.selection()
        )


        if not selected:
            return


        values = (
            self.student_tree
            .item(
                selected[0],
                "values"
            )
        )


        if not values:
            return


        student_id = str(
            values[0]
        ).upper()


        file_path = self.get_student_file(
            student_id
        )


        if not os.path.isfile(
            file_path
        ):
            return


        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                student = json.load(
                    file
                )


        except Exception as e:

            messagebox.showerror(
                "Read Error",
                (
                    "Could not read student data.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        self.selected_student_id = student_id


        # ----------------------------------------------------
        # STUDENT ID
        # ----------------------------------------------------

        self.student_id_entry.delete(
            0,
            tk.END
        )

        self.student_id_entry.insert(
            0,
            str(
                student.get(
                    "student_id",
                    ""
                )
            ).upper()
        )


        # ----------------------------------------------------
        # NAME
        # ----------------------------------------------------

        self.name_entry.delete(
            0,
            tk.END
        )

        self.name_entry.insert(
            0,
            student.get(
                "student_name",
                ""
            )
        )


        # ----------------------------------------------------
        # AGE
        # ----------------------------------------------------

        self.age_entry.delete(
            0,
            tk.END
        )

        self.age_entry.insert(
            0,
            student.get(
                "age",
                ""
            )
        )


        # ----------------------------------------------------
        # GENDER
        # ----------------------------------------------------

        self.gender_combo.set(
            student.get(
                "gender",
                ""
            )
        )


        # ----------------------------------------------------
        # DEPARTMENT
        # ----------------------------------------------------

        self.department_entry.delete(
            0,
            tk.END
        )

        self.department_entry.insert(
            0,
            student.get(
                "department",
                ""
            )
        )


        # ----------------------------------------------------
        # CLASS
        # ----------------------------------------------------

        self.class_entry.delete(
            0,
            tk.END
        )

        self.class_entry.insert(
            0,
            student.get(
                "class",
                ""
            )
        )


        # ----------------------------------------------------
        # EMAIL
        # ----------------------------------------------------

        self.email_entry.delete(
            0,
            tk.END
        )

        self.email_entry.insert(
            0,
            student.get(
                "email",
                ""
            )
        )


        # ----------------------------------------------------
        # PHONE
        # ----------------------------------------------------

        self.phone_entry.delete(
            0,
            tk.END
        )

        self.phone_entry.insert(
            0,
            student.get(
                "phone",
                ""
            )
        )


        # ----------------------------------------------------
        # PASSWORD
        # ----------------------------------------------------

        self.password_entry.delete(
            0,
            tk.END
        )

        self.password_entry.insert(
            0,
            student.get(
                "password",
                ""
            )
        )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status_combo.set(
            student.get(
                "status",
                "Active"
            )
        )


    # ========================================================
    # UPDATE STUDENT
    # ========================================================

    def update_student(self):

        if not self.selected_student_id:

            messagebox.showwarning(
                "No Student Selected",
                (
                    "Double-click a student from the "
                    "student list first."
                ),
                parent=self.root
            )

            return


        data = self.validate_form()


        if data is None:
            return


        old_id = self.selected_student_id

        new_id = data["student_id"]


        old_file = self.get_student_file(
            old_id
        )

        new_file = self.get_student_file(
            new_id
        )


        if old_id != new_id:

            if os.path.exists(
                new_file
            ):

                messagebox.showwarning(
                    "Student Exists",
                    (
                        f"Student ID {new_id} "
                        "already exists."
                    ),
                    parent=self.root
                )

                return


        try:

            with open(
                old_file,
                "r",
                encoding="utf-8"
            ) as file:

                existing = json.load(
                    file
                )


        except Exception as e:

            messagebox.showerror(
                "Read Error",
                (
                    "Could not read the student data.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        existing.update({

            "student_id": new_id,

            "student_name": data[
                "student_name"
            ],

            "age": data[
                "age"
            ],

            "gender": data[
                "gender"
            ],

            "department": data[
                "department"
            ],

            "class": data[
                "class"
            ],

            "email": data[
                "email"
            ],

            "phone": data[
                "phone"
            ],

            "password": data[
                "password"
            ],

            "status": data[
                "status"
            ],

            "updated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        })


        try:

            if old_id != new_id:

                with open(
                    new_file,
                    "w",
                    encoding="utf-8"
                ) as file:

                    json.dump(
                        existing,
                        file,
                        indent=4,
                        ensure_ascii=False
                    )


                os.remove(
                    old_file
                )

            else:

                with open(
                    old_file,
                    "w",
                    encoding="utf-8"
                ) as file:

                    json.dump(
                        existing,
                        file,
                        indent=4,
                        ensure_ascii=False
                    )


        except Exception as e:

            messagebox.showerror(
                "Update Error",
                (
                    "Could not update the student.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        messagebox.showinfo(
            "Student Updated",
            "Student information updated successfully.",
            parent=self.root
        )


        # ----------------------------------------------------
        # REFRESH STUDENT INFORMATION
        # ----------------------------------------------------

        self.selected_student_id = new_id

        self.load_students()


        # ----------------------------------------------------
        # CLEAR OLD/STale FORM INFORMATION
        # ----------------------------------------------------

        self.clear_form()


    # ========================================================
    # DELETE STUDENT
    # ========================================================

    def delete_student(self):

        selected = (
            self.student_tree.selection()
        )


        if not selected:

            if self.selected_student_id:

                student_id = (
                    self.selected_student_id
                )

            else:

                messagebox.showwarning(
                    "No Student Selected",
                    (
                        "Please select a student "
                        "from the list."
                    ),
                    parent=self.root
                )

                return

        else:

            values = (
                self.student_tree.item(
                    selected[0],
                    "values"
                )
            )

            student_id = str(
                values[0]
            ).upper()


        answer = messagebox.askyesno(
            "Delete Student",
            (
                f"Are you sure you want to delete "
                f"student {student_id}?\n\n"
                "This will permanently remove the "
                "student account."
            ),
            parent=self.root
        )


        if not answer:
            return


        file_path = self.get_student_file(
            student_id
        )


        try:

            if os.path.isfile(
                file_path
            ):

                os.remove(
                    file_path
                )

            else:

                messagebox.showwarning(
                    "Student Not Found",
                    "Student file could not be found.",
                    parent=self.root
                )

                return


        except Exception as e:

            messagebox.showerror(
                "Delete Error",
                (
                    "Could not delete the student.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        messagebox.showinfo(
            "Student Deleted",
            (
                f"Student {student_id} "
                "was deleted successfully."
            ),
            parent=self.root
        )


        self.selected_student_id = None

        self.load_students()

        self.clear_form()


    # ========================================================
    # BACK TO ADMIN CONTROL PANEL
    # ========================================================

    def back(self):

        answer = messagebox.askyesno(
            "Back to Admin Control Panel",
            (
                "Do you want to return to "
                "the Admin Control Panel?"
            ),
            parent=self.root
        )


        if not answer:
            return


        parent = self.parent_window


        try:

            if self.root.winfo_exists():

                self.root.destroy()

        except Exception as e:

            print(
                "Could not close Student Management:",
                e
            )


        if parent is not None:

            restore_window(
                parent
            )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()


    student_window = tk.Toplevel(
        root
    )


    StudentManagement(
        student_window,
        parent_window=root
    )


    root.mainloop()
