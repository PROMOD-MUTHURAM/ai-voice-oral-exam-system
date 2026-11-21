import tkinter as tk
from tkinter import messagebox
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
# EXAM MANAGEMENT
# ============================================================

class ExamManagement:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        # ----------------------------------------------------
        # Previous Admin Control Panel
        # ----------------------------------------------------

        self.parent_window = parent_window


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Exam Management - AI Oral Exam System"
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


    # ========================================================
    # CREATE INTERFACE
    # ========================================================

    def create_interface(self):

        # ----------------------------------------------------
        # MAIN FRAME
        # ----------------------------------------------------

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
            text="EXAM MANAGEMENT",
            font=("Arial", 28, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(20, 3)
        )


        tk.Label(
            header_frame,
            text=(
                "Create, manage and control examinations"
            ),
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
            padx=60,
            pady=35
        )


        # ====================================================
        # INFORMATION
        # ====================================================

        tk.Label(
            content_frame,
            text="Examination Management",
            font=("Arial", 20, "bold"),
            bg="#f4f6f8",
            fg="#111827"
        ).pack(
            pady=(0, 5)
        )


        tk.Label(
            content_frame,
            text=(
                "Select an option to manage the examinations."
            ),
            font=("Arial", 11),
            bg="#f4f6f8",
            fg="#6b7280"
        ).pack(
            pady=(0, 25)
        )


        # ====================================================
        # BUTTON FRAME
        # ====================================================

        button_frame = tk.Frame(
            content_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # BUTTONS
        # ====================================================

        buttons = [

            (
                "CREATE NEW EXAM",
                "#2563eb",
                self.create_new_exam
            ),

            (
                "VIEW ACTIVE EXAM",
                "#16a34a",
                self.view_active_exam
            ),

            (
                "EDIT EXAM",
                "#7c3aed",
                self.edit_exam
            ),

            (
                "ACTIVATE / DEACTIVATE",
                "#0891b2",
                self.activate_deactivate_exam
            ),

            (
                "DELETE EXAM",
                "#dc2626",
                self.delete_exam
            ),

            (
                "VIEW EXAM DETAILS",
                "#ea580c",
                self.view_exam_details
            )
        ]


        # ====================================================
        # CREATE BUTTONS
        # ====================================================

        for index, (
            text,
            color,
            command
        ) in enumerate(buttons):

            row = index // 2

            column = index % 2


            button = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 12, "bold"),
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                width=30,
                height=3,
                bd=0,
                cursor="hand2",
                command=command
            )


            button.grid(
                row=row,
                column=column,
                padx=25,
                pady=18,
                sticky="nsew"
            )


        # ----------------------------------------------------
        # GRID CONFIGURATION
        # ----------------------------------------------------

        for column in range(2):

            button_frame.columnconfigure(
                column,
                weight=1
            )


        for row in range(3):

            button_frame.rowconfigure(
                row,
                weight=1
            )


        # ====================================================
        # BACK BUTTON
        # ====================================================

        back_button = tk.Button(
            main_frame,
            text="BACK TO CONTROL PANEL",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=25,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        )

        back_button.pack(
            pady=(0, 20)
        )


    # ========================================================
    # CREATE NEW EXAM
    # ========================================================

    def create_new_exam(self):

        try:

            from gui.admin.create_exam import (
                CreateExam
            )

        except Exception as e:

            messagebox.showerror(
                "Create New Exam",
                (
                    "Could not load Create New Exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Exam Management
        # ----------------------------------------------------

        try:

            self.root.withdraw()

        except Exception:

            pass


        create_exam_window = None


        try:

            create_exam_window = tk.Toplevel(
                self.root
            )


            maximize_window(
                create_exam_window
            )


            CreateExam(
                create_exam_window,
                parent_window=self.root
            )


            create_exam_window.lift()

            create_exam_window.focus_force()


        except Exception as e:

            try:

                if create_exam_window is not None:

                    create_exam_window.destroy()

            except Exception:

                pass


            restore_window(
                self.root
            )


            messagebox.showerror(
                "Create Exam Error",
                (
                    "Could not open Create New Exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # VIEW ACTIVE EXAM
    # ========================================================

    def view_active_exam(self):

        try:

            from gui.admin.view_active_exam import (
                ViewActiveExam
            )

        except Exception as e:

            messagebox.showerror(
                "View Active Exam",
                (
                    "Could not load View Active Exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Exam Management
        # ----------------------------------------------------

        try:

            self.root.withdraw()

        except Exception:

            pass


        view_window = None


        try:

            view_window = tk.Toplevel(
                self.root
            )


            maximize_window(
                view_window
            )


            ViewActiveExam(
                view_window,
                parent_window=self.root
            )


            view_window.lift()

            view_window.focus_force()


        except Exception as e:

            try:

                if view_window is not None:

                    view_window.destroy()

            except Exception:

                pass


            restore_window(
                self.root
            )


            messagebox.showerror(
                "View Active Exam Error",
                (
                    "Could not open View Active Exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # EDIT EXAM
    # ========================================================

    def edit_exam(self):

        try:

            from gui.admin.edit_exam import (
                EditExam
            )

        except Exception as e:

            messagebox.showerror(
                "Edit Exam",
                (
                    "Could not load Edit Exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Exam Management
        # ----------------------------------------------------

        try:

            self.root.withdraw()

        except Exception:

            pass


        edit_window = None


        try:

            edit_window = tk.Toplevel(
                self.root
            )


            maximize_window(
                edit_window
            )


            EditExam(
                edit_window,
                parent_window=self.root
            )


            edit_window.lift()

            edit_window.focus_force()


        except Exception as e:

            try:

                if edit_window is not None:

                    edit_window.destroy()

            except Exception:

                pass


            restore_window(
                self.root
            )


            messagebox.showerror(
                "Edit Exam Error",
                (
                    "Could not open Edit Exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # ACTIVATE / DEACTIVATE
    # ========================================================

    def activate_deactivate_exam(self):

        try:

            from gui.admin.activate_deactivate_exam import (
                ActivateDeactivateExam
            )

        except Exception as e:

            messagebox.showerror(
                "Activate / Deactivate Exam",
                (
                    "Could not load "
                    "Activate / Deactivate Exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Exam Management
        # ----------------------------------------------------

        try:

            self.root.withdraw()

        except Exception:

            pass


        activate_window = None


        try:

            activate_window = tk.Toplevel(
                self.root
            )


            maximize_window(
                activate_window
            )


            ActivateDeactivateExam(
                activate_window,
                parent_window=self.root
            )


            activate_window.lift()

            activate_window.focus_force()


        except Exception as e:

            try:

                if activate_window is not None:

                    activate_window.destroy()

            except Exception:

                pass


            restore_window(
                self.root
            )


            messagebox.showerror(
                "Activate / Deactivate Error",
                (
                    "Could not open "
                    "Activate / Deactivate Exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # DELETE EXAM
    # ========================================================

    def delete_exam(self):

        try:

            from gui.admin.delete_exam import (
                DeleteExam
            )

        except Exception as e:

            messagebox.showerror(
                "Delete Exam",
                (
                    "Could not load Delete Exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Exam Management
        # ----------------------------------------------------

        try:

            self.root.withdraw()

        except Exception:

            pass


        delete_exam_window = None


        try:

            delete_exam_window = tk.Toplevel(
                self.root
            )


            maximize_window(
                delete_exam_window
            )


            DeleteExam(
                delete_exam_window,
                parent_window=self.root
            )


            delete_exam_window.lift()

            delete_exam_window.focus_force()


        except Exception as e:

            try:

                if delete_exam_window is not None:

                    delete_exam_window.destroy()

            except Exception:

                pass


            restore_window(
                self.root
            )


            messagebox.showerror(
                "Delete Exam Error",
                (
                    "Could not open Delete Exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # VIEW EXAM DETAILS
    # ========================================================

    def view_exam_details(self):

        try:

            from gui.admin.view_exam_details import (
                ViewExamDetails
            )

        except Exception as e:

            messagebox.showerror(
                "View Exam Details",
                (
                    "Could not load View Exam Details.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Exam Management
        # ----------------------------------------------------

        try:

            self.root.withdraw()

        except Exception:

            pass


        details_window = None


        try:

            details_window = tk.Toplevel(
                self.root
            )


            maximize_window(
                details_window
            )


            ViewExamDetails(
                details_window,
                parent_window=self.root
            )


            details_window.lift()

            details_window.focus_force()


        except Exception as e:

            try:

                if details_window is not None:

                    details_window.destroy()

            except Exception:

                pass


            restore_window(
                self.root
            )


            messagebox.showerror(
                "View Exam Details Error",
                (
                    "Could not open View Exam Details.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # TEMPORARY MESSAGE
    # ========================================================

    def feature_message(self, feature_name):

        messagebox.showinfo(
            feature_name,
            (
                f"{feature_name} will be implemented "
                "in the next part of Exam Management."
            ),
            parent=self.root
        )


    # ========================================================
    # BACK TO CONTROL PANEL
    # ========================================================

    def back(self):

        answer = messagebox.askyesno(
            "Back to Control Panel",
            (
                "Do you want to return to "
                "the Admin Control Panel?"
            ),
            parent=self.root
        )


        if not answer:

            return


        # ----------------------------------------------------
        # Save parent reference BEFORE destroying this window
        # ----------------------------------------------------

        parent = self.parent_window


        # ----------------------------------------------------
        # Close Exam Management ONLY
        # ----------------------------------------------------

        try:

            if self.root.winfo_exists():

                self.root.destroy()

        except Exception as e:

            print(
                "Could not close Exam Management:",
                e
            )


        # ----------------------------------------------------
        # Restore Control Panel
        # ----------------------------------------------------

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


    exam_window = tk.Toplevel(
        root
    )


    ExamManagement(
        exam_window,
        parent_window=root
    )


    root.mainloop()
