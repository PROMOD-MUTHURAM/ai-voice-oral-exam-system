
# ============================================================
# ADMIN LOGIN
# AI ORAL EXAMINATION SYSTEM
# ============================================================

import tkinter as tk
from tkinter import messagebox
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
# ADMIN ACCOUNT FILE
# ============================================================

BACKEND_DIR = os.path.join(
    BASE_DIR,
    "backend"
)

ADMIN_ACCOUNT_FILE = os.path.join(
    BACKEND_DIR,
    "admin_account.json"
)


# ============================================================
# DEFAULT ADMIN LOGIN
# ============================================================

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"


# ============================================================
# LOAD ADMIN CREDENTIALS
# ============================================================

def load_admin_credentials():

    """
    Load Admin Username and Password from:

        backend/admin_account.json

    If the file does not exist or cannot be read,
    the original default credentials are used.

    Existing exam/student/session JSON files are not touched.
    """

    if not os.path.exists(
        ADMIN_ACCOUNT_FILE
    ):

        return (
            DEFAULT_ADMIN_USERNAME,
            DEFAULT_ADMIN_PASSWORD
        )

    try:

        with open(
            ADMIN_ACCOUNT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

        if not isinstance(
            data,
            dict
        ):

            raise ValueError(
                "Admin account JSON must contain an object."
            )

        username = str(
            data.get(
                "username",
                DEFAULT_ADMIN_USERNAME
            )
        ).strip()

        password = str(
            data.get(
                "password",
                DEFAULT_ADMIN_PASSWORD
            )
        )

        # ----------------------------------------------------
        # Safety fallback
        # ----------------------------------------------------

        if not username:
            username = DEFAULT_ADMIN_USERNAME

        if not password:
            password = DEFAULT_ADMIN_PASSWORD

        return (
            username,
            password
        )

    except Exception as error:

        print(
            "Could not load Admin Account:",
            error
        )

        return (
            DEFAULT_ADMIN_USERNAME,
            DEFAULT_ADMIN_PASSWORD
        )


# ============================================================
# MAXIMIZE WINDOW
# ============================================================

def maximize_window(window):

    if window is None:
        return

    try:

        window.state(
            "zoomed"
        )

        window.after(
            100,
            lambda: safe_maximize(
                window
            )
        )

    except Exception as error:

        print(
            "Could not maximize window:",
            error
        )


def safe_maximize(window):

    try:

        if window.winfo_exists():

            window.state(
                "zoomed"
            )

    except Exception:
        pass


# ============================================================
# ADMIN LOGIN
# ============================================================

class AdminLogin:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        # ----------------------------------------------------
        # Previous window
        # ----------------------------------------------------

        self.parent_window = parent_window


        # ----------------------------------------------------
        # Window settings
        # ----------------------------------------------------

        self.root.title(
            "Admin Login - AI Oral Exam System"
        )

        self.root.geometry(
            "800x600"
        )

        self.root.minsize(
            700,
            500
        )

        self.root.configure(
            bg="#f4f6f8"
        )


        # ----------------------------------------------------
        # Maximize
        # ----------------------------------------------------

        maximize_window(
            self.root
        )


        # ----------------------------------------------------
        # Window close
        # ----------------------------------------------------

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.back
        )


        # ----------------------------------------------------
        # Create GUI
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


        # ----------------------------------------------------
        # Center container
        # ----------------------------------------------------

        center_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        center_frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )


        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        tk.Label(
            center_frame,
            text="ADMIN LOGIN",
            font=("Arial", 28, "bold"),
            bg="#f4f6f8",
            fg="#1f2937"
        ).pack(
            pady=(0, 8)
        )


        # ----------------------------------------------------
        # Subtitle
        # ----------------------------------------------------

        tk.Label(
            center_frame,
            text="AI Oral Examination System",
            font=("Arial", 12),
            bg="#f4f6f8",
            fg="#6b7280"
        ).pack(
            pady=(0, 25)
        )


        # ----------------------------------------------------
        # Login card
        # ----------------------------------------------------

        login_card = tk.Frame(
            center_frame,
            bg="white",
            padx=45,
            pady=35,
            bd=1,
            relief="solid"
        )

        login_card.pack()


        # ====================================================
        # USERNAME
        # ====================================================

        tk.Label(
            login_card,
            text="Username",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            pady=(0, 6)
        )


        self.username_entry = tk.Entry(
            login_card,
            font=("Arial", 12),
            width=32,
            bd=1,
            relief="solid"
        )

        self.username_entry.pack(
            ipady=7,
            pady=(0, 18)
        )


        # ====================================================
        # PASSWORD
        # ====================================================

        tk.Label(
            login_card,
            text="Password",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            pady=(0, 6)
        )


        self.password_entry = tk.Entry(
            login_card,
            font=("Arial", 12),
            width=32,
            show="*",
            bd=1,
            relief="solid"
        )

        self.password_entry.pack(
            ipady=7,
            pady=(0, 22)
        )


        # ====================================================
        # LOGIN BUTTON
        # ====================================================

        tk.Button(
            login_card,
            text="LOGIN",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=25,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.login
        ).pack(
            pady=5
        )


        # ====================================================
        # BACK BUTTON
        # ====================================================

        tk.Button(
            center_frame,
            text="BACK",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        ).pack(
            pady=20
        )


        # ====================================================
        # ENTER KEY
        # ====================================================

        self.root.bind(
            "<Return>",
            lambda event: self.login()
        )


        # ----------------------------------------------------
        # Focus username
        # ----------------------------------------------------

        self.username_entry.focus_set()


    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        username = (
            self.username_entry
            .get()
            .strip()
        )

        password = (
            self.password_entry
            .get()
        )


        # ----------------------------------------------------
        # Empty username
        # ----------------------------------------------------

        if not username:

            messagebox.showwarning(
                "Login",
                "Please enter Admin Username.",
                parent=self.root
            )

            self.username_entry.focus_set()

            return


        # ----------------------------------------------------
        # Empty password
        # ----------------------------------------------------

        if not password:

            messagebox.showwarning(
                "Login",
                "Please enter Admin Password.",
                parent=self.root
            )

            self.password_entry.focus_set()

            return


        # ----------------------------------------------------
        # Load current credentials
        # ----------------------------------------------------

        admin_username, admin_password = (
            load_admin_credentials()
        )


        # ----------------------------------------------------
        # Check login
        # ----------------------------------------------------

        if (
            username == admin_username
            and
            password == admin_password
        ):

            self.open_control_panel()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid Admin Username or Password.",
                parent=self.root
            )

            self.password_entry.delete(
                0,
                tk.END
            )

            self.password_entry.focus_set()


    # ========================================================
    # OPEN ADMIN CONTROL PANEL
    # ========================================================

    def open_control_panel(self):

        try:

            from gui.admin.admin_control_panel import (
                AdminControlPanel
            )

        except Exception as e:

            messagebox.showerror(
                "Admin Control Panel",
                (
                    "Could not load Admin Control Panel.\n\n"
                    "Please make sure the following file exists:\n\n"
                    "gui/admin/admin_control_panel.py\n\n"
                    f"Import details:\n{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Admin Login
        # ----------------------------------------------------

        self.root.withdraw()


        # ----------------------------------------------------
        # Create Control Panel Window
        # ----------------------------------------------------

        dashboard_window = None

        try:

            dashboard_window = tk.Toplevel(
                self.root
            )

            dashboard_window.title(
                "Admin Control Panel - AI Oral Exam System"
            )

            maximize_window(
                dashboard_window
            )

            AdminControlPanel(
                dashboard_window,
                parent_window=self.root
            )

        except Exception as e:

            # ------------------------------------------------
            # Clean up failed window
            # ------------------------------------------------

            try:

                if (
                    dashboard_window is not None
                    and
                    dashboard_window.winfo_exists()
                ):

                    dashboard_window.destroy()

            except Exception:
                pass


            # ------------------------------------------------
            # Restore Admin Login
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


            messagebox.showerror(
                "Control Panel Error",
                (
                    "Could not open Admin Control Panel.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # BACK
    # ========================================================

    def back(self):

        if self.parent_window is not None:

            try:

                if self.parent_window.winfo_exists():

                    self.root.destroy()

                    self.parent_window.deiconify()

                    maximize_window(
                        self.parent_window
                    )

                    self.parent_window.lift()

                    self.parent_window.focus_force()

                    return

            except Exception as e:

                print(
                    "Could not return to previous window:",
                    e
                )


        # ----------------------------------------------------
        # No parent window
        # ----------------------------------------------------

        answer = messagebox.askyesno(
            "Exit",
            "Do you want to close the Admin Login?",
            parent=self.root
        )

        if answer:

            try:

                self.root.destroy()

            except Exception:
                pass


# ============================================================
# OPEN ADMIN LOGIN
# ============================================================

def open_admin_login(
    parent_window=None
):

    window = tk.Toplevel(
        parent_window
    )

    maximize_window(
        window
    )

    AdminLogin(
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

    open_admin_login(
        parent_window=root
    )

    root.mainloop()

