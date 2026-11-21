import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys


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
# VIEW ACTIVE EXAM
# ============================================================

class ViewActiveExam:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        # ----------------------------------------------------
        # Previous Exam Management window
        # ----------------------------------------------------

        self.parent_window = parent_window


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "View Active Exam - AI Oral Exam System"
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


        # ----------------------------------------------------
        # LOAD ACTIVE EXAM
        # ----------------------------------------------------

        self.load_active_exam()


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
            text="VIEW ACTIVE EXAM",
            font=("Arial", 28, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(20, 3)
        )


        tk.Label(
            header_frame,
            text="View details of the currently active examination",
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
            padx=70,
            pady=30
        )


        # ====================================================
        # ACTIVE EXAM CARD
        # ====================================================

        card = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        card.pack(
            fill="both",
            expand=True
        )


        tk.Label(
            card,
            text="ACTIVE EXAMINATION",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            pady=(25, 20)
        )


        # ----------------------------------------------------
        # INFORMATION FRAME
        # ----------------------------------------------------

        self.info_frame = tk.Frame(
            card,
            bg="white"
        )

        self.info_frame.pack(
            fill="both",
            expand=True,
            padx=60,
            pady=10
        )


        # ----------------------------------------------------
        # Exam ID
        # ----------------------------------------------------

        self.exam_id_label = tk.Label(
            self.info_frame,
            text="Exam ID: -",
            font=("Arial", 13),
            bg="white",
            fg="#374151",
            anchor="w"
        )

        self.exam_id_label.pack(
            fill="x",
            pady=8
        )


        # ----------------------------------------------------
        # Exam Name
        # ----------------------------------------------------

        self.exam_name_label = tk.Label(
            self.info_frame,
            text="Exam Name: -",
            font=("Arial", 13),
            bg="white",
            fg="#374151",
            anchor="w"
        )

        self.exam_name_label.pack(
            fill="x",
            pady=8
        )


        # ----------------------------------------------------
        # Subject
        # ----------------------------------------------------

        self.subject_label = tk.Label(
            self.info_frame,
            text="Subject: -",
            font=("Arial", 13),
            bg="white",
            fg="#374151",
            anchor="w"
        )

        self.subject_label.pack(
            fill="x",
            pady=8
        )


        # ----------------------------------------------------
        # Description
        # ----------------------------------------------------

        tk.Label(
            self.info_frame,
            text="Description:",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#374151",
            anchor="w"
        ).pack(
            fill="x",
            pady=(15, 5)
        )


        self.description_text = tk.Text(
            self.info_frame,
            height=5,
            font=("Arial", 11),
            bd=1,
            relief="solid",
            wrap="word"
        )

        self.description_text.pack(
            fill="x"
        )


        self.description_text.config(
            state="disabled"
        )


        # ----------------------------------------------------
        # Other information
        # ----------------------------------------------------

        self.duration_label = tk.Label(
            self.info_frame,
            text="Duration: -",
            font=("Arial", 12),
            bg="white",
            fg="#374151",
            anchor="w"
        )

        self.duration_label.pack(
            fill="x",
            pady=(15, 5)
        )


        self.answer_time_label = tk.Label(
            self.info_frame,
            text="Answer Time: -",
            font=("Arial", 12),
            bg="white",
            fg="#374151",
            anchor="w"
        )

        self.answer_time_label.pack(
            fill="x",
            pady=5
        )


        self.pass_percentage_label = tk.Label(
            self.info_frame,
            text="Pass Percentage: -",
            font=("Arial", 12),
            bg="white",
            fg="#374151",
            anchor="w"
        )

        self.pass_percentage_label.pack(
            fill="x",
            pady=5
        )


        self.status_label = tk.Label(
            self.info_frame,
            text="Status: -",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#16a34a",
            anchor="w"
        )

        self.status_label.pack(
            fill="x",
            pady=5
        )


        # ====================================================
        # BOTTOM BUTTON
        # ====================================================

        button_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            pady=(5, 20)
        )


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
        ).pack()


    # ========================================================
    # LOAD ACTIVE EXAM
    # ========================================================

    def load_active_exam(self):

        active_exam = None


        try:

            for filename in os.listdir(EXAMS_DIR):

                if not filename.lower().endswith(".json"):
                    continue


                file_path = os.path.join(
                    EXAMS_DIR,
                    filename
                )


                try:

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8"
                    ) as file:

                        exam_data = json.load(file)


                    if not isinstance(
                        exam_data,
                        dict
                    ):
                        continue


                    status = str(
                        exam_data.get(
                            "status",
                            "Inactive"
                        )
                    ).strip().lower()


                    if status == "active":

                        active_exam = exam_data
                        break


                except Exception as e:

                    print(
                        "Could not read:",
                        filename,
                        e
                    )


        except Exception as e:

            messagebox.showerror(
                "Exam Error",
                (
                    "Could not load examinations.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ====================================================
        # NO ACTIVE EXAM
        # ====================================================

        if active_exam is None:

            self.exam_id_label.config(
                text="Exam ID: No Active Exam"
            )

            self.exam_name_label.config(
                text="Exam Name: -"
            )

            self.subject_label.config(
                text="Subject: -"
            )

            self.description_text.config(
                state="normal"
            )

            self.description_text.delete(
                "1.0",
                tk.END
            )

            self.description_text.insert(
                "1.0",
                "There is currently no active examination."
            )

            self.description_text.config(
                state="disabled"
            )

            self.duration_label.config(
                text="Duration: -"
            )

            self.answer_time_label.config(
                text="Answer Time: -"
            )

            self.pass_percentage_label.config(
                text="Pass Percentage: -"
            )

            self.status_label.config(
                text="Status: No Active Exam",
                fg="#dc2626"
            )

            return


        # ====================================================
        # DISPLAY ACTIVE EXAM
        # ====================================================

        self.exam_id_label.config(
            text=(
                "Exam ID: "
                f"{active_exam.get('exam_id', '-')}"
            )
        )


        self.exam_name_label.config(
            text=(
                "Exam Name: "
                f"{active_exam.get('exam_name', '-')}"
            )
        )


        self.subject_label.config(
            text=(
                "Subject: "
                f"{active_exam.get('subject', '-')}"
            )
        )


        self.description_text.config(
            state="normal"
        )

        self.description_text.delete(
            "1.0",
            tk.END
        )

        self.description_text.insert(
            "1.0",
            active_exam.get(
                "description",
                ""
            )
        )

        self.description_text.config(
            state="disabled"
        )


        self.duration_label.config(
            text=(
                "Duration: "
                f"{active_exam.get('duration_minutes', '-')}"
                " minutes"
            )
        )


        self.answer_time_label.config(
            text=(
                "Answer Time: "
                f"{active_exam.get('answer_time_seconds', '-')}"
                " seconds per question"
            )
        )


        self.pass_percentage_label.config(
            text=(
                "Pass Percentage: "
                f"{active_exam.get('pass_percentage', '-')}"
                "%"
            )
        )


        self.status_label.config(
            text="Status: ACTIVE",
            fg="#16a34a"
        )


    # ========================================================
    # BACK
    # ========================================================

    def back(self):

        answer = messagebox.askyesno(
            "Back to Exam Management",
            (
                "Do you want to return to "
                "Exam Management?"
            ),
            parent=self.root
        )


        if not answer:
            return


        # ----------------------------------------------------
        # Destroy current child window
        # ----------------------------------------------------

        try:

            self.root.destroy()

        except Exception:
            pass


        # ----------------------------------------------------
        # Restore Exam Management
        # ----------------------------------------------------

        if self.parent_window is not None:

            try:

                if self.parent_window.winfo_exists():

                    self.parent_window.deiconify()

                    maximize_window(
                        self.parent_window
                    )

                    self.parent_window.lift()

                    self.parent_window.focus_force()

            except Exception as e:

                print(
                    "Could not restore Exam Management:",
                    e
                )


# ============================================================
# OPEN VIEW ACTIVE EXAM
# ============================================================

def open_view_active_exam(
    parent_window=None
):

    window = tk.Toplevel(
        parent_window
    )


    maximize_window(
        window
    )


    ViewActiveExam(
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


    open_view_active_exam(
        parent_window=root
    )


    root.mainloop()
