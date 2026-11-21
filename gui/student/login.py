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


# ============================================================
# PYTHON PATH
# ============================================================

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
        window.after(100, lambda: safe_maximize(window))
    except Exception as e:
        print("Could not maximize window:", e)


def safe_maximize(window):

    try:
        if window.winfo_exists():
            window.state("zoomed")
    except Exception:
        pass


# ============================================================
# IMPORT STUDENT DETAILS
# ============================================================

from gui.student.details import open_student_details


# ============================================================
# STUDENT LOGIN
# ============================================================

def open_student_login(parent_window=None):

    login_window = tk.Toplevel(parent_window)

    login_window.title("Student Login - AI Oral Exam System")
    login_window.geometry("500x400")
    login_window.resizable(False, False)
    maximize_window(login_window)

    title_label = tk.Label(
        login_window,
        text="STUDENT LOGIN",
        font=("Arial", 24, "bold")
    )
    title_label.pack(pady=30)

    student_id_label = tk.Label(
        login_window,
        text="Student ID",
        font=("Arial", 12)
    )
    student_id_label.pack(pady=(10, 5))

    student_id_entry = tk.Entry(
        login_window,
        width=35,
        font=("Arial", 12)
    )
    student_id_entry.pack()

    password_label = tk.Label(
        login_window,
        text="Password",
        font=("Arial", 12)
    )
    password_label.pack(pady=(20, 5))

    password_entry = tk.Entry(
        login_window,
        width=35,
        font=("Arial", 12),
        show="*"
    )
    password_entry.pack()


    # ========================================================
    # SHOW PASSWORD
    # ========================================================

    show_password_var = tk.BooleanVar(
        value=False
    )


    def toggle_password():

        if show_password_var.get():

            password_entry.config(
                show=""
            )

        else:

            password_entry.config(
                show="*"
            )


    tk.Checkbutton(
        login_window,
        text="Show Password",
        variable=show_password_var,
        command=toggle_password,
        font=("Arial", 10),
        bg=login_window.cget("bg"),
        activebackground=login_window.cget("bg")
    ).pack(
        pady=(8, 0)
    )
    
    def login_student():

        student_id = student_id_entry.get().strip().upper()
        password = password_entry.get().strip()

        if not student_id:
            messagebox.showwarning(
                "Missing Information",
                "Please enter Student ID.",
                parent=login_window
            )
            return

        if not password:
            messagebox.showwarning(
                "Missing Information",
                "Please enter password.",
                parent=login_window
            )
            return

        # ====================================================
        # VERIFY STUDENT ACCOUNT
        # ====================================================

        students_dir = os.path.join(
            BASE_DIR,
            "backend",
            "students"
        )

        student_file = os.path.join(
            students_dir,
            f"{student_id}.json"
        )

        # ----------------------------------------------------
        # Check whether student exists
        # ----------------------------------------------------

        if not os.path.isfile(student_file):

            messagebox.showerror(
                "Login Failed",
                (
                    "Student ID or password is incorrect."
                ),
                parent=login_window
            )

            return

        # ----------------------------------------------------
        # Read student information
        # ----------------------------------------------------

        try:

            import json

            with open(
                student_file,
                "r",
                encoding="utf-8"
            ) as file:

                student_data = json.load(file)

        except Exception as e:

            messagebox.showerror(
                "Login Error",
                (
                    "Could not read student account information.\n\n"
                    f"{e}"
                ),
                parent=login_window
            )

            return

        # ----------------------------------------------------
        # Check account status
        # ----------------------------------------------------

        student_status = str(
            student_data.get(
                "status",
                "Inactive"
            )
        ).strip().lower()

        if student_status != "active":

            messagebox.showwarning(
                "Account Inactive",
                (
                    "Your student account is currently inactive.\n\n"
                    "Please contact the administrator."
                ),
                parent=login_window
            )

            return

        # ----------------------------------------------------
        # Check password
        # ----------------------------------------------------

        stored_password = str(
            student_data.get(
                "password",
                ""
            )
        )

        if password != stored_password:

            messagebox.showerror(
                "Login Failed",
                (
                    "Student ID or password is incorrect."
                ),
                parent=login_window
            )

            return

        # ====================================================
        # LOGIN SUCCESSFUL
        # ====================================================

        messagebox.showinfo(
            "Login Successful",
            (
                f"Welcome, "
                f"{student_data.get('student_name', student_id)}!"
            ),
            parent=login_window
        )

        login_window.withdraw()

        try:

            details_window = open_student_details(
                student_id=student_id,
                parent_window=login_window,
                login_window=login_window
            )

            maximize_window(details_window)

        except Exception as e:

            login_window.deiconify()
            maximize_window(login_window)

            messagebox.showerror(
                "Student Details Error",
                "Could not open Student Details.\n\n" + str(e),
                parent=login_window
            )

            return

        def details_closed():

            try:

                if details_window.winfo_exists():

                    details_window.destroy()

            except Exception:

                pass

            login_window.deiconify()

            maximize_window(
                login_window
            )

            login_window.lift()

            login_window.focus_force()


        details_window.protocol(
            "WM_DELETE_WINDOW",
            details_closed
        )
        
    tk.Button(
        login_window,
        text="LOGIN",
        width=20,
        font=("Arial", 12, "bold"),
        command=login_student
    ).pack(pady=30)

    def back_to_mainpage():

        try:
            login_window.destroy()
        except Exception:
            pass

        if parent_window is not None:
            try:
                parent_window.deiconify()
                maximize_window(parent_window)
                parent_window.lift()
                parent_window.focus_force()
            except Exception as e:
                print("Could not restore Main Page:")
                print(e)

    tk.Button(
        login_window,
        text="BACK",
        width=20,
        font=("Arial", 11),
        command=back_to_mainpage
    ).pack()

    login_window.protocol(
        "WM_DELETE_WINDOW",
        back_to_mainpage
    )

    student_id_entry.focus()

    maximize_window(login_window)

    return login_window


# ============================================================
# DIRECT TEST LOGIN PAGE
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()
    root.withdraw()

    open_student_login(parent_window=root)

    root.mainloop()
