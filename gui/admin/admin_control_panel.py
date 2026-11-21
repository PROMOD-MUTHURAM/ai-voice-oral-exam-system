
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
# ADMIN CONTROL PANEL
# ============================================================

class AdminControlPanel:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        # Previous Admin Login window
        self.parent_window = parent_window


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Admin Control Panel - AI Oral Exam System"
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
            text="ADMIN CONTROL PANEL",
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
                "Manage the AI Oral Examination System"
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
            padx=60,
            pady=35
        )


        # ====================================================
        # WELCOME
        # ====================================================

        tk.Label(
            content_frame,
            text="Welcome, Administrator",
            font=("Arial", 20, "bold"),
            bg="#f4f6f8",
            fg="#111827"
        ).pack(
            pady=(0, 5)
        )


        tk.Label(
            content_frame,
            text=(
                "Select an option below to manage "
                "the examination system."
            ),
            font=("Arial", 11),
            bg="#f4f6f8",
            fg="#6b7280"
        ).pack(
            pady=(0, 25)
        )


        # ====================================================
        # BUTTON GRID
        # ====================================================

        button_frame = tk.Frame(
            content_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # BUTTON CONFIGURATION
        # ----------------------------------------------------

        buttons = [

            (
                "EXAM MANAGEMENT",
                "#2563eb",
                self.exam_management
            ),

            (
                "QUESTION MANAGEMENT",
                "#7c3aed",
                self.question_management
            ),

            (
                "EXAM PATTERNS",
                "#0891b2",
                self.exam_patterns
            ),

            (
                "STUDENT MANAGEMENT",
                "#16a34a",
                self.student_management
            ),

            (
                "STUDENT DETAILS CONFIGURATION",
                "#0f766e",
                self.student_details_configuration
            ),            

            (
                "EXAM SESSION MANAGEMENT",
                "#16a1b2",
                self.exam_session_management
            ),
            
            (
                "VIEW RESULTS",
                "#ea580c",
                self.view_results
            ),


            (
                "STUDENT RANK DETAILS",
                "#b45309",
                self.student_rank_details
            ),
            
            (
                "EXAM ARCHIVE",
                "#9333ea",
                self.exam_archive
            ),
            

            (
                "SETTINGS",
                "#475569",
                self.settings
            ),

            (
                "ADMIN ACCOUNT",
                "#dc2626",
                self.admin_account
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

            row = index // 3

            column = index % 3


            button = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 12, "bold"),
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                width=25,
                height=3,
                bd=0,
                cursor="hand2",
                command=command
            )


            button.grid(
                row=row,
                column=column,
                padx=15,
                pady=12,
                sticky="nsew"
            )


        # ====================================================
        # ABOUT BUTTON 
        # ====================================================

        about_button = tk.Button(
            button_frame,
            text="ABOUT",
            font=("Arial", 12, "bold"),
            bg="#64748b",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            width=25,
            height=3,
            bd=0,
            cursor="hand2",
            command=self.about
        )


        about_button.grid(
            row=3,
            column=2,
            padx=15,
            pady=12,
            sticky="nsew"
        )


        # ----------------------------------------------------
        # GRID CONFIGURATION
        # ----------------------------------------------------

        for column in range(3):

            button_frame.columnconfigure(
                column,
                weight=1
            )


        for row in range(4):

            button_frame.rowconfigure(
                row,
                weight=1
            )


        # ====================================================
        # BACK BUTTON
        # ====================================================

        back_button = tk.Button(
            main_frame,
            text="BACK TO ADMIN LOGIN",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=24,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        )

        back_button.pack(
            pady=(0, 20)
        )


    # ========================================================
    # OPEN CHILD WINDOW
    # ========================================================

    def open_child_window(
        self,
        module_path,
        class_name,
        error_title
    ):

        # ----------------------------------------------------
        # Import module
        # ----------------------------------------------------

        try:

            module = __import__(
                module_path,
                fromlist=[class_name]
            )

            window_class = getattr(
                module,
                class_name
            )

        except Exception as e:

            messagebox.showerror(
                error_title,
                (
                    f"Could not load {error_title}.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Control Panel
        # ----------------------------------------------------

        try:

            self.root.withdraw()

        except Exception:

            pass


        child_window = None


        try:

            # ------------------------------------------------
            # Create child window
            # ------------------------------------------------

            child_window = tk.Toplevel(
                self.root
            )


            # ------------------------------------------------
            # Maximize child
            # ------------------------------------------------

            maximize_window(
                child_window
            )


            # ------------------------------------------------
            # Start child module
            # ------------------------------------------------

            window_class(
                child_window,
                parent_window=self.root
            )


            # ------------------------------------------------
            # Bring child to front
            # ------------------------------------------------

            child_window.lift()

            child_window.focus_force()


        except Exception as e:

            # ------------------------------------------------
            # Clean up failed child
            # ------------------------------------------------

            try:

                if child_window is not None:

                    if child_window.winfo_exists():

                        child_window.destroy()

            except Exception:

                pass


            # ------------------------------------------------
            # Restore Control Panel
            # ------------------------------------------------

            restore_window(
                self.root
            )


            messagebox.showerror(
                error_title,
                (
                    f"Could not open {error_title}.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # TEMPORARY FEATURE MESSAGE
    # ========================================================

    def feature_message(self, feature_name):

        messagebox.showinfo(
            feature_name,
            (
                f"{feature_name} is ready to be developed.\n\n"
                "We will implement this feature "
                "step by step."
            ),
            parent=self.root
        )


    # ========================================================
    # EXAM MANAGEMENT
    # ========================================================

    def exam_management(self):

        self.open_child_window(
            "gui.admin.exam_management",
            "ExamManagement",
            "Exam Management"
        )


    # ========================================================
    # QUESTION MANAGEMENT
    # ========================================================

    def question_management(self):

        try:

            self.open_child_window(
                "gui.admin.question_management",
                "QuestionManagement",
                "Question Management"
            )

        except Exception:

            self.feature_message(
                "Question Management"
            )


    # ========================================================
    # EXAM PATTERNS
    # ========================================================

    def exam_patterns(self):

        self.open_child_window(
            "gui.admin.exam_pattern",
            "ExamPattern",
            "Exam Pattern"
        )


    # ========================================================
    # STUDENT MANAGEMENT
    # ========================================================

    def student_management(self):

        self.open_child_window(
            "gui.admin.student_management",
            "StudentManagement",
            "Student Management"
        )

    # ========================================================
    # STUDENT DETAILS CONFIGURATION
    # ========================================================

    def student_details_configuration(self):

        self.open_child_window(
            "gui.admin.student_details_configuration",
            "StudentDetailsConfiguration",
            "Student Details Configuration"
        )
        
    # ========================================================
    # EXAM SESSION MANAGEMENT
    # ========================================================

    def exam_session_management(self):

        self.open_child_window(
            "gui.admin.exam_session_management",
            "ExamSessionManagement",
            "Exam Session Management"
        )


    # ========================================================
    # VIEW RESULTS
    # ========================================================


    def view_results(self):

        self.open_child_window(
            "gui.admin.view_results",
            "ViewResults",
            "View Results"
        )


    # ========================================================
    # STUDENT RANK DETAILS
    # ========================================================

    def student_rank_details(self):

        self.open_child_window(
            "gui.admin.student_rank_details",
            "StudentRankDetails",
            "Student Rank Details"
        )

    
    #========================================================
    # EXAM ARCHIVE
    # ========================================================

    def exam_archive(self):

        self.open_child_window(
            "gui.admin.exam_archive",
            "ExamArchive",
            "Exam Archive"
        )


    # ========================================================
    # SETTINGS
    # ========================================================

    def settings(self):

        self.open_child_window(
            "gui.admin.settings",
            "Settings",
            "Settings"
        )
    

    # ========================================================
    # ADMIN ACCOUNT
    # =======================================================

    def admin_account(self):

        self.open_child_window(
            "gui.admin.admin_account",
            "AdminAccount",
            "Admin Account"
        )


    # ========================================================
    # ABOUT
    # ========================================================

    def about(self):

        self.open_child_window(
            "gui.admin.about",
            "About",
            "About"
        )



    # ========================================================
    # BACK TO ADMIN LOGIN
    # ========================================================

    def back(self):

        answer = messagebox.askyesno(
            "Back to Admin Login",
            (
                "Do you want to return to "
                "the Admin Login page?"
            ),
            parent=self.root
        )


        if not answer:

            return


        # ----------------------------------------------------
        # Save parent before destroying current window
        # ----------------------------------------------------

        parent = self.parent_window


        # ----------------------------------------------------
        # Destroy ONLY Control Panel
        # ----------------------------------------------------

        try:

            if self.root.winfo_exists():

                self.root.destroy()

        except Exception as e:

            print(
                "Could not close Admin Control Panel:",
                e
            )


        # ----------------------------------------------------
        # Restore Admin Login
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


    control_panel_window = tk.Toplevel(
        root
    )


    AdminControlPanel(
        control_panel_window,
        parent_window=root
    )


    root.mainloop()

