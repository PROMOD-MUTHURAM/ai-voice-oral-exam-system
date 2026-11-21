
# ============================================================
# ADMIN ACCOUNT - ADMIN CONTROL PANEL
# AI ORAL EXAMINATION SYSTEM
# ============================================================
#
# This module manages the Admin Account settings.
#
# It does NOT modify:
#   backend/exams/
#   backend/students/
#   backend/exam_patterns/
#   backend/exam_sessions/
#   backend/student_answers/
#   backend/exam_results/
#   backend/exam_archive/
#
# DIRECT TEST:
#     python admin_account.py
#
# ============================================================

import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
import tempfile
import shutil
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

ADMIN_ACCOUNT_FILE = os.path.join(
    BACKEND_DIR,
    "admin_account.json"
)


# ============================================================
# CREATE BACKEND DIRECTORY
# ============================================================

os.makedirs(
    BACKEND_DIR,
    exist_ok=True
)


# ============================================================
# DEFAULT ADMIN ACCOUNT
# ============================================================

DEFAULT_ADMIN_ACCOUNT = {
    "username": "admin",
    "password": "admin123",
    "updated_at": ""
}


# ============================================================
# JSON HELPERS
# ============================================================

def deep_copy_json(data):

    return json.loads(
        json.dumps(
            data,
            ensure_ascii=False
        )
    )


def load_admin_account():

    if not os.path.exists(
        ADMIN_ACCOUNT_FILE
    ):

        account = deep_copy_json(
            DEFAULT_ADMIN_ACCOUNT
        )

        save_admin_account(
            account
        )

        return account

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
                "Admin account file must contain a JSON object."
            )

        username = data.get(
            "username",
            DEFAULT_ADMIN_ACCOUNT["username"]
        )

        password = data.get(
            "password",
            DEFAULT_ADMIN_ACCOUNT["password"]
        )

        return {
            "username": username,
            "password": password,
            "updated_at": data.get(
                "updated_at",
                ""
            )
        }

    except Exception as error:

        print(
            "Could not load Admin Account:",
            error
        )

        return deep_copy_json(
            DEFAULT_ADMIN_ACCOUNT
        )


def save_admin_account(account):

    if not isinstance(
        account,
        dict
    ):

        raise ValueError(
            "Admin account must be a dictionary."
        )

    account["updated_at"] = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    os.makedirs(
        BACKEND_DIR,
        exist_ok=True
    )

    temp_file = None

    try:

        fd, temp_file = tempfile.mkstemp(
            prefix="admin_account_",
            suffix=".tmp",
            dir=BACKEND_DIR
        )

        with os.fdopen(
            fd,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                account,
                file,
                indent=4,
                ensure_ascii=False
            )

            file.flush()

            os.fsync(
                file.fileno()
            )

        shutil.move(
            temp_file,
            ADMIN_ACCOUNT_FILE
        )

        temp_file = None

    finally:

        if temp_file is not None:

            try:

                os.remove(
                    temp_file
                )

            except Exception:
                pass


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
# ADMIN ACCOUNT
# ============================================================

class AdminAccount:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root
        self.parent_window = parent_window

        self.account = load_admin_account()

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.root.title(
            "Admin Account - AI Oral Examination System"
        )

        self.root.geometry(
            "1000x700"
        )

        self.root.minsize(
            850,
            600
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

        self.load_values()


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

        header = tk.Frame(
            main_frame,
            bg="#1f2937",
            height=110
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        tk.Label(
            header,
            text="ADMIN ACCOUNT",
            font=("Arial", 25, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(18, 3)
        )

        tk.Label(
            header,
            text=(
                "Manage the Administrator username and password"
            ),
            font=("Arial", 11),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack()


        # ====================================================
        # CONTENT
        # ====================================================

        content = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        content.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # ACCOUNT CARD
        # ====================================================

        card = tk.Frame(
            content,
            bg="white",
            bd=1,
            relief="solid",
            padx=45,
            pady=35
        )

        card.place(
            relx=0.5,
            rely=0.45,
            anchor="center"
        )


        # ====================================================
        # SECTION TITLE
        # ====================================================

        tk.Label(
            card,
            text="Administrator Credentials",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        tk.Label(
            card,
            text=(
                "Change the credentials used to access "
                "the Admin Control Panel."
            ),
            font=("Arial", 10),
            bg="white",
            fg="#6b7280"
        ).pack(
            anchor="w",
            pady=(0, 25)
        )


        # ====================================================
        # USERNAME
        # ====================================================

        tk.Label(
            card,
            text="Admin Username",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            pady=(0, 6)
        )

        self.username_var = tk.StringVar()

        self.username_entry = tk.Entry(
            card,
            textvariable=self.username_var,
            font=("Arial", 12),
            width=35,
            bd=1,
            relief="solid"
        )

        self.username_entry.pack(
            ipady=7,
            pady=(0, 18)
        )


        # ====================================================
        # NEW PASSWORD
        # ====================================================

        tk.Label(
            card,
            text="New Password",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            pady=(0, 6)
        )

        self.password_var = tk.StringVar()

        self.password_entry = tk.Entry(
            card,
            textvariable=self.password_var,
            font=("Arial", 12),
            width=35,
            show="*",
            bd=1,
            relief="solid"
        )

        self.password_entry.pack(
            ipady=7,
            pady=(0, 18)
        )


        # ====================================================
        # CONFIRM PASSWORD
        # ====================================================

        tk.Label(
            card,
            text="Confirm Password",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            pady=(0, 6)
        )

        self.confirm_password_var = tk.StringVar()

        self.confirm_password_entry = tk.Entry(
            card,
            textvariable=self.confirm_password_var,
            font=("Arial", 12),
            width=35,
            show="*",
            bd=1,
            relief="solid"
        )

        self.confirm_password_entry.pack(
            ipady=7,
            pady=(0, 12)
        )


        # ====================================================
        # SHOW PASSWORD
        # ====================================================

        self.show_password_var = tk.BooleanVar(
            value=False
        )

        tk.Checkbutton(
            card,
            text="Show password",
            variable=self.show_password_var,
            command=self.toggle_password,
            font=("Arial", 10),
            bg="white",
            activebackground="white",
            anchor="w"
        ).pack(
            anchor="w",
            pady=(0, 20)
        )


        # ====================================================
        # SAVE BUTTON
        # ====================================================

        tk.Button(
            card,
            text="SAVE ADMIN ACCOUNT",
            font=("Arial", 11, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=25,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.save
        ).pack(
            pady=(5, 10)
        )


        # ====================================================
        # BACK BUTTON
        # ====================================================

        tk.Button(
            card,
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
            pady=5
        )


        # ====================================================
        # ENTER KEY
        # ====================================================

        self.root.bind(
            "<Return>",
            lambda event: self.save()
        )


    # ========================================================
    # LOAD VALUES
    # ========================================================

    def load_values(self):

        self.username_var.set(
            self.account.get(
                "username",
                "admin"
            )
        )

        self.password_var.set("")

        self.confirm_password_var.set("")


    # ========================================================
    # SHOW / HIDE PASSWORD
    # ========================================================

    def toggle_password(self):

        try:

            if self.show_password_var.get():

                self.password_entry.config(
                    show=""
                )

                self.confirm_password_entry.config(
                    show=""
                )

            else:

                self.password_entry.config(
                    show="*"
                )

                self.confirm_password_entry.config(
                    show="*"
                )

        except Exception:
            pass


    # ========================================================
    # SAVE
    # ========================================================

    def save(self):

        username = (
            self.username_var
            .get()
            .strip()
        )

        password = (
            self.password_var
            .get()
        )

        confirm_password = (
            self.confirm_password_var
            .get()
        )


        # ----------------------------------------------------
        # VALIDATE USERNAME
        # ----------------------------------------------------

        if not username:

            messagebox.showwarning(
                "Admin Account",
                "Admin Username cannot be empty.",
                parent=self.root
            )

            self.username_entry.focus_set()

            return


        if len(username) < 3:

            messagebox.showwarning(
                "Admin Account",
                "Admin Username must contain at least 3 characters.",
                parent=self.root
            )

            self.username_entry.focus_set()

            return


        # ----------------------------------------------------
        # PASSWORD REQUIRED
        # ----------------------------------------------------

        if not password:

            messagebox.showwarning(
                "Admin Account",
                "Please enter a new password.",
                parent=self.root
            )

            self.password_entry.focus_set()

            return


        if len(password) < 4:

            messagebox.showwarning(
                "Admin Account",
                "Password must contain at least 4 characters.",
                parent=self.root
            )

            self.password_entry.focus_set()

            return


        # ----------------------------------------------------
        # CONFIRM PASSWORD
        # ----------------------------------------------------

        if password != confirm_password:

            messagebox.showerror(
                "Admin Account",
                "New Password and Confirm Password do not match.",
                parent=self.root
            )

            self.confirm_password_entry.focus_set()

            return


        # ----------------------------------------------------
        # CONFIRM SAVE
        # ----------------------------------------------------

        answer = messagebox.askyesno(
            "Save Admin Account",
            (
                "Save the new Admin Account credentials?\n\n"
                "The new username and password will be used "
                "for future Admin Login attempts."
            ),
            parent=self.root
        )

        if not answer:
            return


        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        try:

            new_account = {
                "username": username,
                "password": password,
                "updated_at": ""
            }

            save_admin_account(
                new_account
            )

            self.account = new_account

            self.password_var.set("")

            self.confirm_password_var.set("")

            messagebox.showinfo(
                "Admin Account",
                (
                    "Admin Account updated successfully.\n\n"
                    "The new credentials will be used for "
                    "future Admin Login attempts."
                ),
                parent=self.root
            )

        except Exception as error:

            messagebox.showerror(
                "Save Error",
                (
                    "Could not save Admin Account.\n\n"
                    f"{error}"
                ),
                parent=self.root
            )


    # ========================================================
    # BACK
    # ========================================================

    def back(self):

        try:

            if self.root.winfo_exists():

                self.root.destroy()

        except Exception:
            pass


        if self.parent_window is not None:

            try:

                self.parent_window.deiconify()

                maximize_window(
                    self.parent_window
                )

                self.parent_window.lift()

                self.parent_window.focus_force()

            except Exception:
                pass


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    window = tk.Toplevel(
        root
    )

    AdminAccount(
        window,
        parent_window=root
    )

    root.mainloop()


