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


EXAMS_DIR = os.path.join(
    BACKEND_DIR,
    "exams"
)


os.makedirs(
    EXAMS_DIR,
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
# RESTORE PARENT WINDOW
# ============================================================

def restore_parent_window(parent_window):

    if parent_window is None:
        return

    try:

        if parent_window.winfo_exists():

            parent_window.deiconify()

            maximize_window(
                parent_window
            )

            parent_window.lift()

            parent_window.focus_force()

    except Exception as e:

        print(
            "Could not restore parent window:",
            e
        )


# ============================================================
# CREATE EXAM
# ============================================================

class CreateExam:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        # Immediate previous window
        self.parent_window = parent_window


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Create New Exam - AI Oral Exam System"
        )

        self.root.geometry(
            "1000x750"
        )

        self.root.minsize(
            850,
            650
        )

        self.root.configure(
            bg="#f4f6f8"
        )


        # ----------------------------------------------------
        # MAXIMIZE
        # ----------------------------------------------------

        maximize_window(
            self.root
        )


        # ----------------------------------------------------
        # WINDOW CLOSE
        # ----------------------------------------------------

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.back
        )


        # ----------------------------------------------------
        # CREATE GUI
        # ----------------------------------------------------

        self.create_interface()


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
            text="CREATE NEW EXAM",
            font=("Arial", 28, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(20, 3)
        )


        tk.Label(
            header_frame,
            text=(
                "Create and configure a new oral examination"
            ),
            font=("Arial", 11),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack()


        # ====================================================
        # CONTENT AREA
        # ====================================================

        content_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        content_frame.pack(
            fill="both",
            expand=True,
            padx=80,
            pady=30
        )


        # ====================================================
        # FORM CARD
        # ====================================================

        form_card = tk.Frame(
            content_frame,
            bg="white",
            padx=45,
            pady=30,
            bd=1,
            relief="solid"
        )

        form_card.pack(
            fill="x"
        )


        # ====================================================
        # EXAM ID
        # ====================================================

        tk.Label(
            form_card,
            text="Exam ID",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=10
        )


        self.exam_id_entry = ttk.Entry(
            form_card,
            width=45
        )

        self.exam_id_entry.grid(
            row=0,
            column=1,
            padx=25,
            pady=10,
            sticky="w"
        )


        self.exam_id_entry.insert(
            0,
            self.generate_exam_id()
        )


        self.exam_id_entry.config(
            state="readonly"
        )


        # ====================================================
        # EXAM NAME
        # ====================================================

        tk.Label(
            form_card,
            text="Exam Name",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=10
        )


        self.exam_name_entry = ttk.Entry(
            form_card,
            width=45
        )

        self.exam_name_entry.grid(
            row=1,
            column=1,
            padx=25,
            pady=10,
            sticky="w"
        )


        # ====================================================
        # SUBJECT
        # ====================================================

        tk.Label(
            form_card,
            text="Subject",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=10
        )


        self.subject_entry = ttk.Entry(
            form_card,
            width=45
        )

        self.subject_entry.grid(
            row=2,
            column=1,
            padx=25,
            pady=10,
            sticky="w"
        )


        # ====================================================
        # DESCRIPTION
        # ====================================================

        tk.Label(
            form_card,
            text="Description",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=3,
            column=0,
            sticky="nw",
            pady=10
        )


        self.description_text = tk.Text(
            form_card,
            width=43,
            height=4,
            font=("Arial", 11),
            bd=1,
            relief="solid"
        )

        self.description_text.grid(
            row=3,
            column=1,
            padx=25,
            pady=10,
            sticky="w"
        )


        # ====================================================
        # EXAM DURATION
        # ====================================================

        tk.Label(
            form_card,
            text="Exam Duration (minutes)",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=10
        )


        self.duration_entry = ttk.Entry(
            form_card,
            width=45
        )

        self.duration_entry.grid(
            row=4,
            column=1,
            padx=25,
            pady=10,
            sticky="w"
        )


        self.duration_entry.insert(
            0,
            "30"
        )


        # ====================================================
        # ANSWER TIME
        # ====================================================

        tk.Label(
            form_card,
            text="Answer Time / Question (seconds)",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=10
        )


        self.answer_time_entry = ttk.Entry(
            form_card,
            width=45
        )

        self.answer_time_entry.grid(
            row=5,
            column=1,
            padx=25,
            pady=10,
            sticky="w"
        )


        self.answer_time_entry.insert(
            0,
            "60"
        )


        # ====================================================
        # PASS PERCENTAGE
        # ====================================================

        tk.Label(
            form_card,
            text="Pass Percentage (%)",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=6,
            column=0,
            sticky="w",
            pady=10
        )


        self.pass_percentage_entry = ttk.Entry(
            form_card,
            width=45
        )

        self.pass_percentage_entry.grid(
            row=6,
            column=1,
            padx=25,
            pady=10,
            sticky="w"
        )


        self.pass_percentage_entry.insert(
            0,
            "50"
        )


        # ====================================================
        # STATUS
        # ====================================================

        tk.Label(
            form_card,
            text="Status",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=7,
            column=0,
            sticky="w",
            pady=10
        )


        self.status_combo = ttk.Combobox(
            form_card,
            width=42,
            state="readonly",
            values=[
                "Inactive",
                "Active"
            ]
        )

        self.status_combo.grid(
            row=7,
            column=1,
            padx=25,
            pady=10,
            sticky="w"
        )


        self.status_combo.set(
            "Inactive"
        )


        # ====================================================
        # BUTTON FRAME
        # ====================================================

        button_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            pady=(5, 25)
        )


        # ====================================================
        # SAVE EXAM
        # ====================================================

        tk.Button(
            button_frame,
            text="SAVE EXAM",
            font=("Arial", 12, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.save_exam
        ).grid(
            row=0,
            column=0,
            padx=10
        )


        # ====================================================
        # CLEAR
        # ====================================================

        tk.Button(
            button_frame,
            text="CLEAR",
            font=("Arial", 12, "bold"),
            bg="#f59e0b",
            fg="white",
            activebackground="#d97706",
            activeforeground="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.clear_form
        ).grid(
            row=0,
            column=1,
            padx=10
        )


        # ====================================================
        # BACK
        # ====================================================

        tk.Button(
            button_frame,
            text="BACK",
            font=("Arial", 12, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        ).grid(
            row=0,
            column=2,
            padx=10
        )


    # ========================================================
    # GENERATE EXAM ID
    # ========================================================

    def generate_exam_id(self):

        number = 1

        while True:

            exam_id = (
                f"EXAM{number:03d}"
            )

            file_path = os.path.join(
                EXAMS_DIR,
                f"{exam_id}.json"
            )

            if not os.path.exists(file_path):

                return exam_id

            number += 1


    # ========================================================
    # VALIDATE FORM
    # ========================================================

    def validate_form(self):

        exam_id = self.exam_id_entry.get().strip()

        exam_name = self.exam_name_entry.get().strip()

        subject = self.subject_entry.get().strip()

        description = self.description_text.get(
            "1.0",
            tk.END
        ).strip()

        duration = self.duration_entry.get().strip()

        answer_time = self.answer_time_entry.get().strip()

        pass_percentage = self.pass_percentage_entry.get().strip()

        status = self.status_combo.get().strip()


        if not exam_name:

            messagebox.showwarning(
                "Missing Information",
                "Please enter Exam Name.",
                parent=self.root
            )

            self.exam_name_entry.focus_set()

            return None


        if not subject:

            messagebox.showwarning(
                "Missing Information",
                "Please enter Subject.",
                parent=self.root
            )

            self.subject_entry.focus_set()

            return None


        try:

            duration_value = int(duration)

            if duration_value <= 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Duration",
                "Exam Duration must be a positive number.",
                parent=self.root
            )

            self.duration_entry.focus_set()

            return None


        try:

            answer_time_value = int(answer_time)

            if answer_time_value <= 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Answer Time",
                "Answer Time must be a positive number.",
                parent=self.root
            )

            self.answer_time_entry.focus_set()

            return None


        try:

            pass_value = float(pass_percentage)

            if pass_value < 0 or pass_value > 100:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Pass Percentage",
                "Pass Percentage must be between 0 and 100.",
                parent=self.root
            )

            self.pass_percentage_entry.focus_set()

            return None


        if status not in ("Active", "Inactive"):
            status = "Inactive"


        return {

            "exam_id": exam_id,

            "exam_name": exam_name,

            "subject": subject,

            "description": description,

            "duration_minutes": duration_value,

            "answer_time_seconds": answer_time_value,

            "pass_percentage": pass_value,

            "status": status,

            "total_questions": 0,

            "total_marks": 0,

            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "updated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }


    # ========================================================
    # SAVE EXAM
    # ========================================================

    def save_exam(self):

        exam_data = self.validate_form()

        if exam_data is None:
            return


        exam_id = exam_data["exam_id"]


        file_path = os.path.join(
            EXAMS_DIR,
            f"{exam_id}.json"
        )


        if os.path.exists(file_path):

            messagebox.showerror(
                "Exam Already Exists",
                (
                    f"Exam ID {exam_id} "
                    "already exists."
                ),
                parent=self.root
            )

            return


        try:

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    exam_data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )


            messagebox.showinfo(
                "Exam Created",
                (
                    "Exam created successfully.\n\n"
                    f"Exam ID: {exam_id}\n"
                    f"Exam Name: "
                    f"{exam_data['exam_name']}"
                ),
                parent=self.root
            )


            self.clear_form()


            self.exam_id_entry.config(
                state="normal"
            )

            self.exam_id_entry.delete(
                0,
                tk.END
            )

            self.exam_id_entry.insert(
                0,
                self.generate_exam_id()
            )

            self.exam_id_entry.config(
                state="readonly"
            )


        except Exception as e:

            messagebox.showerror(
                "Save Error",
                (
                    "Could not save the exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # CLEAR FORM
    # ========================================================

    def clear_form(self):

        self.exam_name_entry.delete(
            0,
            tk.END
        )

        self.subject_entry.delete(
            0,
            tk.END
        )

        self.description_text.delete(
            "1.0",
            tk.END
        )

        self.duration_entry.delete(
            0,
            tk.END
        )

        self.duration_entry.insert(
            0,
            "30"
        )

        self.answer_time_entry.delete(
            0,
            tk.END
        )

        self.answer_time_entry.insert(
            0,
            "60"
        )

        self.pass_percentage_entry.delete(
            0,
            tk.END
        )

        self.pass_percentage_entry.insert(
            0,
            "50"
        )

        self.status_combo.set(
            "Inactive"
        )


    # ========================================================
    # BACK
    # ========================================================

    def back(self):

        answer = messagebox.askyesno(
            "Back",
            (
                "Do you want to return to "
                "Exam Management?"
            ),
            parent=self.root
        )


        if not answer:
            return


        # ----------------------------------------------------
        # Destroy current window
        # ----------------------------------------------------

        try:

            self.root.destroy()

        except Exception:
            pass


        # ----------------------------------------------------
        # Restore immediate parent
        # ----------------------------------------------------

        restore_parent_window(
            self.parent_window
        )


# ============================================================
# OPEN CREATE EXAM
# ============================================================

def open_create_exam(
    parent_window=None
):

    window = tk.Toplevel(
        parent_window
    )


    maximize_window(
        window
    )


    CreateExam(
        window,
        parent_window=parent_window
    )


    return window


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()


    open_create_exam(
        parent_window=root
    )


    root.mainloop()
