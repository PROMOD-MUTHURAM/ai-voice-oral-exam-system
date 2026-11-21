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
# DELETE EXAM
# ============================================================

class DeleteExam:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        # Previous Exam Management window
        self.parent_window = parent_window

        self.selected_exam_id = None
        self.selected_exam_file = None


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Delete Exam - AI Oral Exam System"
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
            text="DELETE EXAM",
            font=("Arial", 28, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(20, 3)
        )


        tk.Label(
            header_frame,
            text="Remove an examination from the system",
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
            pady=30
        )


        # ====================================================
        # CARD
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
            text="SELECT EXAMINATION TO DELETE",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 12)
        )


        # ====================================================
        # TABLE
        # ====================================================

        table_container = tk.Frame(
            card,
            bg="white"
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
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
            "subject",
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
            "subject",
            text="Subject"
        )

        self.exam_table.heading(
            "status",
            text="Status"
        )


        self.exam_table.column(
            "exam_id",
            width=120,
            anchor="center"
        )

        self.exam_table.column(
            "exam_name",
            width=300,
            anchor="w"
        )

        self.exam_table.column(
            "subject",
            width=250,
            anchor="w"
        )

        self.exam_table.column(
            "status",
            width=120,
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
        # BUTTON FRAME
        # ====================================================

        button_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            pady=(5, 20)
        )


        # ----------------------------------------------------
        # DELETE
        # ----------------------------------------------------

        tk.Button(
            button_frame,
            text="DELETE EXAM",
            font=("Arial", 11, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.delete_exam
        ).grid(
            row=0,
            column=0,
            padx=8
        )


        # ----------------------------------------------------
        # REFRESH
        # ----------------------------------------------------

        tk.Button(
            button_frame,
            text="REFRESH",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=17,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.load_exams
        ).grid(
            row=0,
            column=1,
            padx=8
        )


        # ----------------------------------------------------
        # BACK
        # ----------------------------------------------------

        tk.Button(
            button_frame,
            text="BACK",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=17,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        ).grid(
            row=0,
            column=2,
            padx=8
        )


    # ========================================================
    # LOAD EXAMS
    # ========================================================

    def load_exams(self):

        for item in self.exam_table.get_children():

            self.exam_table.delete(
                item
            )


        self.selected_exam_id = None
        self.selected_exam_file = None


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


                    subject = exam_data.get(
                        "subject",
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
                            subject,
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


        self.selected_exam_id = exam_id
        self.selected_exam_file = file_path


    # ========================================================
    # DELETE EXAM
    # ========================================================

    def delete_exam(self):

        if not self.selected_exam_file:

            messagebox.showwarning(
                "Select Exam",
                "Please select an examination first.",
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Read exam before deleting
        # ----------------------------------------------------

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
                    "Could not read the selected examination.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        exam_name = exam_data.get(
            "exam_name",
            self.selected_exam_id
        )


        # ----------------------------------------------------
        # Confirmation
        # ----------------------------------------------------

        answer = messagebox.askyesno(
            "Delete Exam",
            (
                "Are you sure you want to delete this "
                "examination?\n\n"
                f"Exam ID: {self.selected_exam_id}\n"
                f"Exam Name: {exam_name}\n\n"
                "This action cannot be undone."
            ),
            parent=self.root
        )


        if not answer:
            return


        # ----------------------------------------------------
        # Delete file
        # ----------------------------------------------------

        try:

            os.remove(
                self.selected_exam_file
            )


            messagebox.showinfo(
                "Exam Deleted",
                (
                    f"Exam {self.selected_exam_id} "
                    "was deleted successfully."
                ),
                parent=self.root
            )


            self.selected_exam_id = None
            self.selected_exam_file = None


            self.load_exams()


        except Exception as e:

            messagebox.showerror(
                "Delete Error",
                (
                    "Could not delete the examination.\n\n"
                    f"{e}"
                ),
                parent=self.root
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
# OPEN DELETE EXAM
# ============================================================

def open_delete_exam(
    parent_window=None
):

    window = tk.Toplevel(
        parent_window
    )


    maximize_window(
        window
    )


    DeleteExam(
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


    open_delete_exam(
        parent_window=root
    )


    root.mainloop()
