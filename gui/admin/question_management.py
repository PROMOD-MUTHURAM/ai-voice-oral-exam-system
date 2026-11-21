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
# QUESTION MANAGEMENT
# ============================================================

class QuestionManagement:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        # Previous Admin Control Panel
        self.parent_window = parent_window


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Question Management - AI Oral Exam System"
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


        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        tk.Label(
            header_frame,
            text="QUESTION MANAGEMENT",
            font=("Arial", 28, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(20, 3)
        )


        # ----------------------------------------------------
        # SUBTITLE
        # ----------------------------------------------------

        tk.Label(
            header_frame,
            text=(
                "Add, view, edit and delete examination questions"
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
            text="Question Management",
            font=("Arial", 20, "bold"),
            bg="#f4f6f8",
            fg="#111827"
        ).pack(
            pady=(0, 5)
        )


        tk.Label(
            content_frame,
            text=(
                "Select an option to manage examination questions."
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
                "ADD QUESTION",
                "#2563eb",
                self.add_question
            ),

            (
                "VIEW QUESTIONS",
                "#16a34a",
                self.view_questions
            ),

            (
                "EDIT QUESTION",
                "#7c3aed",
                self.edit_question
            ),

            (
                "DELETE QUESTION",
                "#dc2626",
                self.delete_question
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
                pady=25,
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


        for row in range(2):

            button_frame.rowconfigure(
                row,
                weight=1
            )


        # ====================================================
        # INFORMATION NOTE
        # ====================================================

        note_frame = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        note_frame.pack(
            fill="x",
            pady=(10, 15)
        )


        tk.Label(
            note_frame,
            text=(
                "Question fields: Exam ID, Question No., "
                "Question, Expected Answer, Marks, "
                "Difficulty, Topic, Keywords and Status."
            ),
            font=("Arial", 10),
            bg="white",
            fg="#6b7280",
            wraplength=900,
            justify="center"
        ).pack(
            padx=20,
            pady=12
        )


        tk.Label(
            note_frame,
            text=(
                "Keywords are optional. "
                "For one-word questions, one keyword can be used. "
                "For descriptive questions, multiple keywords "
                "can be entered separated by commas."
            ),
            font=("Arial", 10),
            bg="white",
            fg="#6b7280",
            wraplength=900,
            justify="center"
        ).pack(
            padx=20,
            pady=(0, 12)
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
    # TEMPORARY MESSAGE
    # ========================================================

    def feature_message(self, feature_name):

        messagebox.showinfo(
            feature_name,
            (
                f"{feature_name} will be implemented "
                "in the next part of Question Management."
            ),
            parent=self.root
        )


    # ========================================================
    # ADD QUESTION
    # ========================================================

    def add_question(self):

        try:

            from gui.admin.add_question import (
                AddQuestion
            )

        except Exception as e:

            messagebox.showerror(
                "Add Question",
                (
                    "Could not load Add Question.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Question Management
        # ----------------------------------------------------

        self.root.withdraw()


        # ----------------------------------------------------
        # Create ONE Add Question Window
        # ----------------------------------------------------

        add_question_window = None

        try:

            add_question_window = tk.Toplevel(
                self.root
            )


            maximize_window(
                add_question_window
            )


            AddQuestion(
                add_question_window,
                parent_window=self.root
            )


        except Exception as e:

            try:

                if add_question_window is not None:

                    add_question_window.destroy()

            except Exception:

                pass


            self.root.deiconify()

            maximize_window(
                self.root
            )


            messagebox.showerror(
                "Add Question Error",
                (
                    "Could not open Add Question.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # VIEW QUESTIONS
    # ========================================================

    def view_questions(self):

        try:

            from gui.admin.view_questions import (
                ViewQuestions
            )

        except Exception as e:

            messagebox.showerror(
                "View Questions",
                (
                    "Could not load View Questions.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Question Management
        # ----------------------------------------------------

        self.root.withdraw()


        # ----------------------------------------------------
        # Create View Questions Window
        # ----------------------------------------------------

        view_question_window = None

        try:

            view_question_window = tk.Toplevel(
                self.root
            )


            maximize_window(
                view_question_window
            )


            ViewQuestions(
                view_question_window,
                parent_window=self.root
            )


        except Exception as e:

            try:

                if view_question_window is not None:

                    view_question_window.destroy()

            except Exception:

                pass


            self.root.deiconify()

            maximize_window(
                self.root
            )


            messagebox.showerror(
                "View Questions Error",
                (
                    "Could not open View Questions.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )
        


    # ========================================================
    # EDIT QUESTION
    # ========================================================

    def edit_question(self):

        try:

            from gui.admin.edit_question import (
                EditQuestion
            )

        except Exception as e:

            messagebox.showerror(
                "Edit Question",
                (
                    "Could not load Edit Question.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Question Management
        # ----------------------------------------------------

        self.root.withdraw()


        # ----------------------------------------------------
        # Create Edit Question Window
        # ----------------------------------------------------

        edit_question_window = None

        try:

            edit_question_window = tk.Toplevel(
                self.root
            )


            maximize_window(
                edit_question_window
            )


            EditQuestion(
                edit_question_window,
                parent_window=self.root
            )


        except Exception as e:

            try:

                if edit_question_window is not None:

                    edit_question_window.destroy()

            except Exception:

                pass


            self.root.deiconify()

            maximize_window(
                self.root
            )


            messagebox.showerror(
                "Edit Question Error",
                (
                    "Could not open Edit Question.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # DELETE QUESTION
    # ========================================================

    def delete_question(self):

        try:

            from gui.admin.delete_question import (
                DeleteQuestion
            )

        except Exception as e:

            messagebox.showerror(
                "Delete Question",
                (
                    "Could not load Delete Question.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Question Management
        # ----------------------------------------------------

        self.root.withdraw()


        # ----------------------------------------------------
        # Create Delete Question Window
        # ----------------------------------------------------

        delete_question_window = None

        try:

            delete_question_window = tk.Toplevel(
                self.root
            )


            maximize_window(
                delete_question_window
            )


            DeleteQuestion(
                delete_question_window,
                parent_window=self.root
            )


        except Exception as e:

            try:

                if delete_question_window is not None:

                    delete_question_window.destroy()

            except Exception:

                pass


            self.root.deiconify()

            maximize_window(
                self.root
            )


            messagebox.showerror(
                "Delete Question Error",
                (
                    "Could not open Delete Question.\n\n"
                    f"{e}"
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
        # Close Question Management
        # ----------------------------------------------------

        try:

            self.root.destroy()

        except Exception:

            pass


        # ----------------------------------------------------
        # Restore Control Panel
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
                    "Could not restore "
                    "Admin Control Panel:"
                )

                print(e)


# ============================================================
# OPEN QUESTION MANAGEMENT
# ============================================================

def open_question_management(
    parent_window=None
):

    window = tk.Toplevel(
        parent_window
    )


    maximize_window(
        window
    )


    QuestionManagement(
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


    open_question_management(
        parent_window=root
    )


    root.mainloop()
