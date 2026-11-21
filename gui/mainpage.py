import tkinter as tk
from tkinter import messagebox
import os
import sys
import traceback


# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ============================================================
# ADD PROJECT ROOT TO PYTHON PATH
# ============================================================

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ============================================================
# MAXIMIZE WINDOW FUNCTION
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
# MAIN PAGE
# ============================================================

class MainPage:

    def __init__(self, root):

        self.root = root

        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "AI Oral Examination System"
        )

        self.root.configure(
            bg="#f4f6f8"
        )

        # ----------------------------------------------------
        # MAXIMIZE MAIN PAGE
        # ----------------------------------------------------

        maximize_window(
            self.root
        )

        # ----------------------------------------------------
        # CLOSE BUTTON
        # ----------------------------------------------------

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
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
        # MAIN CONTAINER
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
            height=100
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
            text="AI ORAL EXAMINATION SYSTEM",
            font=("Arial", 28, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(18, 2)
        )


        # ----------------------------------------------------
        # SUBTITLE
        # ----------------------------------------------------

        tk.Label(
            header_frame,
            text="Computer Based Oral Examination Platform",
            font=("Arial", 11),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack()


        # ====================================================
        # CENTER AREA
        # ====================================================

        center_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        center_frame.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # WELCOME
        # ====================================================

        tk.Label(
            center_frame,
            text="WELCOME",
            font=("Arial", 30, "bold"),
            bg="#f4f6f8",
            fg="#111827"
        ).pack(
            pady=(80, 10)
        )


        tk.Label(
            center_frame,
            text=(
                "Please select your login type "
                "to continue."
            ),
            font=("Arial", 13),
            bg="#f4f6f8",
            fg="#6b7280"
        ).pack(
            pady=(0, 40)
        )


        # ====================================================
        # LOGIN BUTTON FRAME
        # ====================================================

        login_frame = tk.Frame(
            center_frame,
            bg="#f4f6f8"
        )

        login_frame.pack()


        # ====================================================
        # STUDENT LOGIN CARD
        # ====================================================

        student_card = tk.Frame(
            login_frame,
            bg="white",
            width=350,
            height=260,
            bd=1,
            relief="solid"
        )

        student_card.grid(
            row=0,
            column=0,
            padx=30
        )

        student_card.pack_propagate(
            False
        )


        tk.Label(
            student_card,
            text="🎓",
            font=("Arial", 45),
            bg="white"
        ).pack(
            pady=(25, 5)
        )


        tk.Label(
            student_card,
            text="STUDENT",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#2563eb"
        ).pack()


        tk.Label(
            student_card,
            text=(
                "Login to attend your "
                "oral examination."
            ),
            font=("Arial", 10),
            bg="white",
            fg="#6b7280",
            justify="center"
        ).pack(
            pady=10
        )


        tk.Button(
            student_card,
            text="STUDENT LOGIN",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.open_student_login
        ).pack(
            pady=10
        )


        # ====================================================
        # ADMIN LOGIN CARD
        # ====================================================

        admin_card = tk.Frame(
            login_frame,
            bg="white",
            width=350,
            height=260,
            bd=1,
            relief="solid"
        )

        admin_card.grid(
            row=0,
            column=1,
            padx=30
        )

        admin_card.pack_propagate(
            False
        )


        tk.Label(
            admin_card,
            text="⚙",
            font=("Arial", 45),
            bg="white"
        ).pack(
            pady=(25, 5)
        )


        tk.Label(
            admin_card,
            text="ADMIN",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#16a34a"
        ).pack()


        tk.Label(
            admin_card,
            text=(
                "Manage examinations, questions, "
                "students and results."
            ),
            font=("Arial", 10),
            bg="white",
            fg="#6b7280",
            justify="center"
        ).pack(
            pady=10
        )


        tk.Button(
            admin_card,
            text="ADMIN LOGIN",
            font=("Arial", 12, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.open_admin_login
        ).pack(
            pady=10
        )


        # ====================================================
        # FOOTER
        # ====================================================

        footer_frame = tk.Frame(
            main_frame,
            bg="#1f2937",
            height=55
        )

        footer_frame.pack(
            fill="x",
            side="bottom"
        )

        footer_frame.pack_propagate(
            False
        )


        tk.Label(
            footer_frame,
            text="AI Oral Examination System",
            font=("Arial", 10),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack(
            pady=18
        )


    # ========================================================
    # STUDENT LOGIN
    # ========================================================

    def open_student_login(self):

        try:

            from gui.student.login import (
                open_student_login
            )

            # ------------------------------------------------
            # Hide Main Page
            # ------------------------------------------------

            self.root.withdraw()

            # ------------------------------------------------
            # Open Student Login
            # ------------------------------------------------

            student_window = open_student_login(
                parent_window=self.root
            )

            # ------------------------------------------------
            # Maximize
            # ------------------------------------------------

            maximize_window(
                student_window
            )

            student_window.deiconify()
            student_window.lift()
            student_window.focus_force()

        except Exception as e:

            # ------------------------------------------------
            # Restore Main Page
            # ------------------------------------------------

            try:

                self.root.deiconify()

                maximize_window(
                    self.root
                )

            except Exception:
                pass


            print("\n========================================")
            print("STUDENT LOGIN ERROR")
            print("========================================")

            traceback.print_exc()

            print("========================================\n")


            messagebox.showerror(
                "Student Login Error",
                (
                    "Could not open Student Login.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # ADMIN LOGIN
    # ========================================================

    def open_admin_login(self):

        print("\n========================================")
        print("ADMIN LOGIN BUTTON CLICKED")
        print("========================================")

        try:

            # ------------------------------------------------
            # Make sure project root is available
            # ------------------------------------------------

            if BASE_DIR not in sys.path:

                sys.path.insert(
                    0,
                    BASE_DIR
                )


            # ------------------------------------------------
            # Import Admin Login
            # ------------------------------------------------

            print(
                "Loading gui.admin.login..."
            )

            from gui.admin.login import (
                open_admin_login
            )


            print(
                "Admin Login module imported successfully."
            )


            # ------------------------------------------------
            # Hide Main Page
            # ------------------------------------------------

            self.root.withdraw()

            print(
                "Main Page hidden."
            )


            # ------------------------------------------------
            # Open Admin Login
            # ------------------------------------------------

            admin_window = open_admin_login(
                parent_window=self.root
            )


            print(
                "Admin Login window created."
            )


            # ------------------------------------------------
            # Maximize
            # ------------------------------------------------

            maximize_window(
                admin_window
            )


            # ------------------------------------------------
            # Make Visible
            # ------------------------------------------------

            admin_window.deiconify()

            admin_window.lift()

            admin_window.focus_force()


            print(
                "Admin Login opened successfully."
            )

            print(
                "========================================\n"
            )


        except Exception as e:

            # ------------------------------------------------
            # Restore Main Page
            # ------------------------------------------------

            try:

                self.root.deiconify()

                maximize_window(
                    self.root
                )

                self.root.lift()

                self.root.focus_force()

            except Exception:
                pass


            # ------------------------------------------------
            # Print Complete Error
            # ------------------------------------------------

            print("\n========================================")
            print("ADMIN LOGIN ERROR")
            print("========================================")

            traceback.print_exc()

            print("========================================\n")


            # ------------------------------------------------
            # Show Error
            # ------------------------------------------------

            messagebox.showerror(
                "Admin Login Error",
                (
                    "Could not open Admin Login.\n\n"
                    f"Error:\n{e}\n\n"
                    "Please check the Python IDLE "
                    "shell for the complete error."
                ),
                parent=self.root
            )


    # ========================================================
    # CLOSE APPLICATION
    # ========================================================

    def close_application(self):

        answer = messagebox.askyesno(
            "Exit Application",
            (
                "Are you sure you want to "
                "exit the application?"
            ),
            parent=self.root
        )


        if not answer:

            return


        try:

            self.root.destroy()

        except Exception:

            pass


# ============================================================
# OPEN MAIN PAGE
# ============================================================

def open_mainpage():

    root = tk.Tk()

    maximize_window(
        root
    )

    MainPage(
        root
    )

    root.mainloop()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    open_mainpage()
