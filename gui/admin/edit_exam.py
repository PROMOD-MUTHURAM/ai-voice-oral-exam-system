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

        if window.winfo_exists():

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
        return False

    try:

        if parent_window.winfo_exists():

            parent_window.deiconify()

            maximize_window(
                parent_window
            )

            parent_window.lift()

            parent_window.focus_force()

            return True

    except Exception as e:

        print(
            "Could not restore parent window:",
            e
        )

    return False


# ============================================================
# EDIT EXAM
# ============================================================

class EditExam:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        # ----------------------------------------------------
        # IMPORTANT:
        # Keep the exact window that opened Edit Exam.
        # This allows BACK to work repeatedly.
        # ----------------------------------------------------

        self.parent_window = parent_window

        # Currently selected exam
        self.selected_exam_id = None

        self.selected_exam_file = None

        # Prevent double back execution
        self.is_closing = False


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Edit Exam - AI Oral Exam System"
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
        # LOAD EXAMS
        # ----------------------------------------------------

        self.load_exams()


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
            height=105
        )

        header_frame.pack(
            fill="x"
        )

        header_frame.pack_propagate(
            False
        )


        tk.Label(
            header_frame,
            text="EDIT EXAM",
            font=("Arial", 27, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(18, 3)
        )


        tk.Label(
            header_frame,
            text="Modify examination information",
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
            padx=50,
            pady=25
        )


        # ====================================================
        # LEFT SIDE - EXAM LIST
        # ====================================================

        left_frame = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 15)
        )


        tk.Label(
            left_frame,
            text="SELECT EXAM",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 12)
        )


        # ----------------------------------------------------
        # EXAM TABLE
        # ----------------------------------------------------

        table_container = tk.Frame(
            left_frame,
            bg="white"
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )


        scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical"
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        columns = (
            "exam_id",
            "exam_name",
            "status"
        )


        self.exam_table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse"
        )


        scrollbar.config(
            command=self.exam_table.yview
        )


        self.exam_table.heading(
            "exam_id",
            text="Exam ID"
        )

        self.exam_table.heading(
            "exam_name",
            text="Exam Name"
        )

        self.exam_table.heading(
            "status",
            text="Status"
        )


        self.exam_table.column(
            "exam_id",
            width=100,
            anchor="center"
        )

        self.exam_table.column(
            "exam_name",
            width=250,
            anchor="w"
        )

        self.exam_table.column(
            "status",
            width=100,
            anchor="center"
        )


        self.exam_table.pack(
            fill="both",
            expand=True
        )


        self.exam_table.bind(
            "<<TreeviewSelect>>",
            self.select_exam
        )


        # ====================================================
        # RIGHT SIDE - EDIT FORM
        # ====================================================

        right_frame = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        right_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(15, 0)
        )


        tk.Label(
            right_frame,
            text="EXAM INFORMATION",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(
            anchor="w",
            padx=30,
            pady=(18, 15)
        )


        # ----------------------------------------------------
        # FORM
        # ----------------------------------------------------

        form_frame = tk.Frame(
            right_frame,
            bg="white"
        )

        form_frame.pack(
            fill="both",
            expand=True,
            padx=30
        )


        # ====================================================
        # EXAM ID
        # ====================================================

        tk.Label(
            form_frame,
            text="Exam ID",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=7
        )


        self.exam_id_entry = ttk.Entry(
            form_frame,
            width=38,
            state="readonly"
        )

        self.exam_id_entry.grid(
            row=0,
            column=1,
            padx=15,
            pady=7,
            sticky="ew"
        )


        # ====================================================
        # EXAM NAME
        # ====================================================

        tk.Label(
            form_frame,
            text="Exam Name",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=7
        )


        self.exam_name_entry = ttk.Entry(
            form_frame,
            width=38
        )

        self.exam_name_entry.grid(
            row=1,
            column=1,
            padx=15,
            pady=7,
            sticky="ew"
        )


        # ====================================================
        # SUBJECT
        # ====================================================

        tk.Label(
            form_frame,
            text="Subject",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=7
        )


        self.subject_entry = ttk.Entry(
            form_frame,
            width=38
        )

        self.subject_entry.grid(
            row=2,
            column=1,
            padx=15,
            pady=7,
            sticky="ew"
        )


        # ====================================================
        # DESCRIPTION
        # ====================================================

        tk.Label(
            form_frame,
            text="Description",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=3,
            column=0,
            sticky="nw",
            pady=7
        )


        self.description_text = tk.Text(
            form_frame,
            width=36,
            height=3,
            font=("Arial", 10),
            bd=1,
            relief="solid"
        )

        self.description_text.grid(
            row=3,
            column=1,
            padx=15,
            pady=7,
            sticky="ew"
        )


        # ====================================================
        # DURATION
        # ====================================================

        tk.Label(
            form_frame,
            text="Duration (minutes)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=7
        )


        self.duration_entry = ttk.Entry(
            form_frame,
            width=38
        )

        self.duration_entry.grid(
            row=4,
            column=1,
            padx=15,
            pady=7,
            sticky="ew"
        )


        # ====================================================
        # ANSWER TIME
        # ====================================================

        tk.Label(
            form_frame,
            text="Answer Time (seconds)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=7
        )


        self.answer_time_entry = ttk.Entry(
            form_frame,
            width=38
        )

        self.answer_time_entry.grid(
            row=5,
            column=1,
            padx=15,
            pady=7,
            sticky="ew"
        )


        # ====================================================
        # PASS PERCENTAGE
        # ====================================================

        tk.Label(
            form_frame,
            text="Pass Percentage (%)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=6,
            column=0,
            sticky="w",
            pady=7
        )


        self.pass_percentage_entry = ttk.Entry(
            form_frame,
            width=38
        )

        self.pass_percentage_entry.grid(
            row=6,
            column=1,
            padx=15,
            pady=7,
            sticky="ew"
        )


        # ====================================================
        # STATUS
        # ====================================================

        tk.Label(
            form_frame,
            text="Status",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=7,
            column=0,
            sticky="w",
            pady=7
        )


        self.status_combo = ttk.Combobox(
            form_frame,
            width=36,
            state="readonly",
            values=[
                "Inactive",
                "Active"
            ]
        )

        self.status_combo.grid(
            row=7,
            column=1,
            padx=15,
            pady=7,
            sticky="ew"
        )


        form_frame.columnconfigure(
            1,
            weight=1
        )


        # ====================================================
        # BUTTONS
        # ====================================================

        button_frame = tk.Frame(
            right_frame,
            bg="white"
        )

        button_frame.pack(
            pady=(5, 20)
        )


        tk.Button(
            button_frame,
            text="SAVE CHANGES",
            font=("Arial", 11, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=17,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.save_changes
        ).grid(
            row=0,
            column=0,
            padx=6
        )


        tk.Button(
            button_frame,
            text="CLEAR",
            font=("Arial", 11, "bold"),
            bg="#f59e0b",
            fg="white",
            activebackground="#d97706",
            activeforeground="white",
            width=14,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.clear_form
        ).grid(
            row=0,
            column=1,
            padx=6
        )


        tk.Button(
            button_frame,
            text="REFRESH",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=14,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.load_exams
        ).grid(
            row=0,
            column=2,
            padx=6
        )


        tk.Button(
            button_frame,
            text="BACK",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=14,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        ).grid(
            row=0,
            column=3,
            padx=6
        )


    # ========================================================
    # LOAD EXAMS
    # ========================================================

    def load_exams(self):

        for item in self.exam_table.get_children():

            self.exam_table.delete(item)


        if not os.path.exists(EXAMS_DIR):

            return


        try:

            files = sorted(
                filename
                for filename in os.listdir(EXAMS_DIR)
                if filename.lower().endswith(".json")
            )


            for filename in files:

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


                    exam_id = exam_data.get(
                        "exam_id",
                        os.path.splitext(filename)[0]
                    )


                    exam_name = exam_data.get(
                        "exam_name",
                        "-"
                    )


                    status = str(
                        exam_data.get(
                            "status",
                            "Inactive"
                        )
                    ).strip()


                    if status.lower() == "active":

                        status = "Active"

                    else:

                        status = "Inactive"


                    self.exam_table.insert(
                        "",
                        "end",
                        values=(
                            exam_id,
                            exam_name,
                            status
                        )
                    )


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


    # ========================================================
    # SELECT EXAM
    # ========================================================

    def select_exam(self, event=None):

        selected = self.exam_table.selection()

        if not selected:
            return


        values = self.exam_table.item(
            selected[0],
            "values"
        )


        if not values:
            return


        exam_id = str(
            values[0]
        ).strip()


        file_path = os.path.join(
            EXAMS_DIR,
            f"{exam_id}.json"
        )


        if not os.path.exists(file_path):

            messagebox.showerror(
                "Exam Error",
                (
                    f"Exam file for {exam_id} "
                    "could not be found."
                ),
                parent=self.root
            )

            return


        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                exam_data = json.load(file)


        except Exception as e:

            messagebox.showerror(
                "Exam Error",
                (
                    "Could not read exam data.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        self.selected_exam_id = exam_id

        self.selected_exam_file = file_path


        self.set_entry(
            self.exam_id_entry,
            exam_id
        )


        self.exam_name_entry.delete(
            0,
            tk.END
        )

        self.exam_name_entry.insert(
            0,
            exam_data.get(
                "exam_name",
                ""
            )
        )


        self.subject_entry.delete(
            0,
            tk.END
        )

        self.subject_entry.insert(
            0,
            exam_data.get(
                "subject",
                ""
            )
        )


        self.description_text.delete(
            "1.0",
            tk.END
        )

        self.description_text.insert(
            "1.0",
            exam_data.get(
                "description",
                ""
            )
        )


        self.duration_entry.delete(
            0,
            tk.END
        )

        self.duration_entry.insert(
            0,
            str(
                exam_data.get(
                    "duration_minutes",
                    30
                )
            )
        )


        self.answer_time_entry.delete(
            0,
            tk.END
        )

        self.answer_time_entry.insert(
            0,
            str(
                exam_data.get(
                    "answer_time_seconds",
                    60
                )
            )
        )


        self.pass_percentage_entry.delete(
            0,
            tk.END
        )

        self.pass_percentage_entry.insert(
            0,
            str(
                exam_data.get(
                    "pass_percentage",
                    50
                )
            )
        )


        status = str(
            exam_data.get(
                "status",
                "Inactive"
            )
        )


        if status.lower() == "active":

            self.status_combo.set(
                "Active"
            )

        else:

            self.status_combo.set(
                "Inactive"
            )


    # ========================================================
    # SET READONLY ENTRY
    # ========================================================

    def set_entry(
        self,
        entry,
        value
    ):

        entry.config(
            state="normal"
        )

        entry.delete(
            0,
            tk.END
        )

        entry.insert(
            0,
            value
        )

        entry.config(
            state="readonly"
        )


    # ========================================================
    # VALIDATE FORM
    # ========================================================

    def validate_form(self):

        if not self.selected_exam_file:

            messagebox.showwarning(
                "Select Exam",
                "Please select an examination first.",
                parent=self.root
            )

            return None


        exam_name = self.exam_name_entry.get().strip()

        subject = self.subject_entry.get().strip()

        description = self.description_text.get(
            "1.0",
            tk.END
        ).strip()

        duration = self.duration_entry.get().strip()

        answer_time = self.answer_time_entry.get().strip()

        pass_percentage = (
            self.pass_percentage_entry
            .get()
            .strip()
        )

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
                (
                    "Exam Duration must be "
                    "a positive number."
                ),
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
                (
                    "Answer Time must be "
                    "a positive number."
                ),
                parent=self.root
            )

            self.answer_time_entry.focus_set()

            return None


        try:

            pass_value = float(pass_percentage)

            if (
                pass_value < 0
                or
                pass_value > 100
            ):

                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Pass Percentage",
                (
                    "Pass Percentage must be "
                    "between 0 and 100."
                ),
                parent=self.root
            )

            self.pass_percentage_entry.focus_set()

            return None


        if status not in (
            "Active",
            "Inactive"
        ):

            status = "Inactive"


        return {
            "exam_name": exam_name,
            "subject": subject,
            "description": description,
            "duration_minutes": duration_value,
            "answer_time_seconds": answer_time_value,
            "pass_percentage": pass_value,
            "status": status
        }


    # ========================================================
    # SAVE CHANGES
    # ========================================================

    def save_changes(self):

        updated_data = self.validate_form()

        if updated_data is None:
            return


        if not self.selected_exam_file:
            return


        try:

            with open(
                self.selected_exam_file,
                "r",
                encoding="utf-8"
            ) as file:

                exam_data = json.load(file)


        except Exception as e:

            messagebox.showerror(
                "Exam Error",
                (
                    "Could not read the existing exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ====================================================
        # ACTIVE EXAM CONTROL
        # ====================================================

        if (
            updated_data["status"] == "Active"
            and
            str(
                exam_data.get(
                    "status",
                    "Inactive"
                )
            ).lower() != "active"
        ):

            answer = messagebox.askyesno(
                "Activate Exam",
                (
                    "This will activate this examination "
                    "and deactivate any other active "
                    "examination.\n\n"
                    "Do you want to continue?"
                ),
                parent=self.root
            )


            if not answer:
                return


            try:

                for filename in os.listdir(
                    EXAMS_DIR
                ):

                    if not filename.lower().endswith(
                        ".json"
                    ):
                        continue


                    other_file = os.path.join(
                        EXAMS_DIR,
                        filename
                    )


                    if other_file == self.selected_exam_file:
                        continue


                    try:

                        with open(
                            other_file,
                            "r",
                            encoding="utf-8"
                        ) as file:

                            other_data = json.load(file)


                        if not isinstance(
                            other_data,
                            dict
                        ):
                            continue


                        other_status = str(
                            other_data.get(
                                "status",
                                "Inactive"
                            )
                        ).lower()


                        if other_status == "active":

                            other_data["status"] = "Inactive"


                            with open(
                                other_file,
                                "w",
                                encoding="utf-8"
                            ) as file:

                                json.dump(
                                    other_data,
                                    file,
                                    indent=4,
                                    ensure_ascii=False
                                )


                    except Exception as e:

                        print(
                            "Could not update:",
                            other_file,
                            e
                        )


            except Exception as e:

                messagebox.showerror(
                    "Activation Error",
                    (
                        "Could not update other exams.\n\n"
                        f"{e}"
                    ),
                    parent=self.root
                )

                return


        # ====================================================
        # UPDATE DATA
        # ====================================================

        exam_data["exam_name"] = updated_data["exam_name"]

        exam_data["subject"] = updated_data["subject"]

        exam_data["description"] = updated_data["description"]

        exam_data["duration_minutes"] = (
            updated_data["duration_minutes"]
        )

        exam_data["answer_time_seconds"] = (
            updated_data["answer_time_seconds"]
        )

        exam_data["pass_percentage"] = (
            updated_data["pass_percentage"]
        )

        exam_data["status"] = updated_data["status"]

        exam_data["updated_at"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        # ====================================================
        # SAVE
        # ====================================================

        try:

            with open(
                self.selected_exam_file,
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
                "Exam Updated",
                (
                    "Exam details updated successfully.\n\n"
                    f"Exam ID: {self.selected_exam_id}"
                ),
                parent=self.root
            )


            self.load_exams()


            self.select_exam_by_id(
                self.selected_exam_id
            )


        except Exception as e:

            messagebox.showerror(
                "Save Error",
                (
                    "Could not save exam changes.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # SELECT EXAM BY ID
    # ========================================================

    def select_exam_by_id(
        self,
        exam_id
    ):

        for item in self.exam_table.get_children():

            values = self.exam_table.item(
                item,
                "values"
            )


            if values and str(
                values[0]
            ) == str(
                exam_id
            ):

                self.exam_table.selection_set(
                    item
                )

                self.exam_table.focus(
                    item
                )

                self.exam_table.see(
                    item
                )

                self.select_exam()

                break


    # ========================================================
    # CLEAR FORM
    # ========================================================

    def clear_form(self):

        self.selected_exam_id = None

        self.selected_exam_file = None


        self.set_entry(
            self.exam_id_entry,
            ""
        )


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


        self.answer_time_entry.delete(
            0,
            tk.END
        )


        self.pass_percentage_entry.delete(
            0,
            tk.END
        )


        self.status_combo.set(
            ""
        )


        for item in self.exam_table.selection():

            self.exam_table.selection_remove(
                item
            )


    # ========================================================
    # BACK
    # ========================================================

    def back(self):

        # ----------------------------------------------------
        # Prevent double-click / double-close
        # ----------------------------------------------------

        if self.is_closing:
            return


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


        self.is_closing = True


        # ----------------------------------------------------
        # Save reference before destroying child
        # ----------------------------------------------------

        parent = self.parent_window


        # ----------------------------------------------------
        # Destroy Edit Exam
        # ----------------------------------------------------

        try:

            if self.root.winfo_exists():

                self.root.destroy()

        except Exception as e:

            print(
                "Could not close Edit Exam:",
                e
            )


        # ----------------------------------------------------
        # RESTORE IMMEDIATE PARENT
        # ----------------------------------------------------

        restore_parent_window(
            parent
        )


# ============================================================
# OPEN EDIT EXAM
# ============================================================

def open_edit_exam(
    parent_window=None
):

    window = tk.Toplevel(
        parent_window
    )


    # --------------------------------------------------------
    # Hide parent while Edit Exam is open
    # --------------------------------------------------------

    if parent_window is not None:

        try:

            if parent_window.winfo_exists():

                parent_window.withdraw()

        except Exception:

            pass


    maximize_window(
        window
    )


    EditExam(
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


    open_edit_exam(
        parent_window=root
    )


    root.mainloop()
