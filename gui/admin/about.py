
# ============================================================
# ABOUT - ADMIN CONTROL PANEL
# AI ORAL EXAMINATION SYSTEM
# ============================================================

import tkinter as tk
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
# ABOUT
# ============================================================

class About:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root
        self.parent_window = parent_window


        # ====================================================
        # WINDOW SETTINGS
        # ====================================================

        self.root.title(
            "About - AI Oral Examination System"
        )

        self.root.geometry(
            "900x650"
        )

        self.root.minsize(
            750,
            550
        )

        self.root.configure(
            bg="#f4f6f8"
        )


        # ====================================================
        # MAXIMIZE
        # ====================================================

        maximize_window(
            self.root
        )


        # ====================================================
        # WINDOW CLOSE
        # ====================================================

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.back
        )


        # ====================================================
        # CREATE INTERFACE
        # ====================================================

        self.create_interface()


    # ========================================================
    # CREATE INTERFACE
    # ========================================================

    def create_interface(self):

        # ====================================================
        # MAIN FRAME
        # ====================================================

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
            height=120
        )

        header_frame.pack(
            fill="x"
        )

        header_frame.pack_propagate(
            False
        )


        tk.Label(
            header_frame,
            text="ABOUT",
            font=("Arial", 28, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(22, 3)
        )


        tk.Label(
            header_frame,
            text="AI Oral Examination System",
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
        # INFORMATION CARD
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


        # ====================================================
        # APPLICATION NAME
        # ====================================================

        tk.Label(
            card,
            text="AI Oral Examination System",
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            pady=(35, 8)
        )


        # ====================================================
        # VERSION
        # ====================================================

        tk.Label(
            card,
            text="Version 1.0",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#6b7280"
        ).pack(
            pady=(0, 20)
        )


        # ====================================================
        # DESCRIPTION
        # ====================================================

        description = (
            "The AI Oral Examination System is designed "
            "to manage oral examinations, students, "
            "questions, examination sessions, answers, "
            "results and examination archives."
        )

        tk.Label(
            card,
            text=description,
            font=("Arial", 11),
            bg="white",
            fg="#374151",
            wraplength=650,
            justify="center"
        ).pack(
            pady=10
        )


        # ====================================================
        # ADMIN FEATURES
        # ====================================================

        tk.Label(
            card,
            text="Admin Control Panel",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(
            pady=(25, 10)
        )


        features = (
            "Exam Management\n"
            "Question Management\n"
            "Exam Patterns\n"
            "Student Management\n"
            "Student Details Configuration\n"
            "Exam Session Management\n"
            "View Results\n"
            "Student Rank Details\n"
            "Exam Archive\n"
            "System Settings\n"
            "Admin Account"
        )

        tk.Label(
            card,
            text=features,
            font=("Arial", 10),
            bg="white",
            fg="#4b5563",
            justify="center"
        ).pack(
            pady=5
        )


        # ====================================================
        # DATA SAFETY INFORMATION
        # ====================================================

        tk.Label(
            card,
            text=(
                "The application preserves the existing "
                "JSON data structures used by the system."
            ),
            font=("Arial", 9),
            bg="white",
            fg="#6b7280",
            wraplength=650,
            justify="center"
        ).pack(
            pady=(20, 5)
        )


        # ====================================================
        # BACK BUTTON
        # ====================================================

        tk.Button(
            main_frame,
            text="BACK TO ADMIN CONTROL PANEL",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=28,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        ).pack(
            pady=(0, 20)
        )


    # ========================================================
    # BACK TO ADMIN CONTROL PANEL
    # ========================================================

    def back(self):

        try:

            if self.root.winfo_exists():

                self.root.destroy()

        except Exception as e:

            print(
                "Could not close About window:",
                e
            )


        # ====================================================
        # RESTORE ADMIN CONTROL PANEL
        # ====================================================

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
                    "Could not restore Admin Control Panel:",
                    e
                )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()


    about_window = tk.Toplevel(
        root
    )


    About(
        about_window,
        parent_window=root
    )


    root.mainloop()

