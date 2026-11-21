import tkinter as tk
from tkinter import messagebox
import json
import os


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
# BACKEND
# ============================================================

BACKEND_DIR = os.path.join(
    BASE_DIR,
    "backend"
)

STUDENT_DATA_FILE = os.path.join(
    BACKEND_DIR,
    "current_student.json"
)


os.makedirs(
    BACKEND_DIR,
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
# LOAD STUDENT DETAILS
# ============================================================

def load_student_details():

    if not os.path.exists(
        STUDENT_DATA_FILE
    ):

        return None


    try:

        with open(
            STUDENT_DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    except Exception as e:

        print(
            "Could not load student details:"
        )

        print(e)

        return None


# ============================================================
# EXAM INSTRUCTIONS
# ============================================================

class ExamInstructions:

    def __init__(
        self,
        root,
        parent_window=None,
        login_window=None,
        details_window=None
    ):

        self.root = root

        # Student Details
        self.parent_window = parent_window

        # Student Login
        self.login_window = (
            login_window
            if login_window is not None
            else None
        )

        # Explicit Details window
        self.details_window = (
            details_window
            if details_window is not None
            else parent_window
        )

        # Exam window
        self.exam_window = None

        # Student information
        self.student_data = (
            load_student_details()
        )


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Exam Instructions - AI Oral Exam System"
        )

        self.root.geometry(
            "1000x750"
        )

        self.root.minsize(
            850,
            650
        )

        self.root.configure(
            bg="#f4f6f8"
        )

        maximize_window(self.root)


        # ----------------------------------------------------
        # CREATE GUI
        # ----------------------------------------------------

        self.create_interface()


        # ----------------------------------------------------
        # CLOSE
        # ----------------------------------------------------

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.go_back
        )


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
        # TITLE
        # ====================================================

        tk.Label(
            main_frame,
            text="EXAM INSTRUCTIONS",
            font=("Arial", 26, "bold"),
            bg="#f4f6f8",
            fg="#1f2937"
        ).pack(
            pady=(25, 5)
        )


        tk.Label(
            main_frame,
            text=(
                "Please read all instructions carefully "
                "before starting the examination."
            ),
            font=("Arial", 11),
            bg="#f4f6f8",
            fg="#6b7280"
        ).pack(
            pady=(0, 15)
        )


        # ====================================================
        # STUDENT INFORMATION
        # ====================================================

        student_frame = tk.Frame(
            main_frame,
            bg="white",
            padx=20,
            pady=14
        )

        student_frame.pack(
            padx=50,
            fill="x"
        )


        if self.student_data:

            name = self.student_data.get(
                "student_name",
                ""
            )

            student_id = self.student_data.get(
                "student_id",
                ""
            )

            student_class = self.student_data.get(
                "class",
                ""
            )

            section = self.student_data.get(
                "section",
                ""
            )

        else:

            name = "Unknown"
            student_id = "Unknown"
            student_class = "Unknown"
            section = "Unknown"


        student_text = (
            f"Student Name : {name}     |     "
            f"Student ID : {student_id}     |     "
            f"Class : {student_class}     |     "
            f"Section : {section}"
        )


        tk.Label(
            student_frame,
            text=student_text,
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w"
        )


        # ====================================================
        # INSTRUCTIONS CONTAINER
        # ====================================================

        instruction_container = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        instruction_container.pack(
            padx=50,
            pady=15,
            fill="both",
            expand=True
        )


        canvas = tk.Canvas(
            instruction_container,
            bg="white",
            highlightthickness=1,
            highlightbackground="#d1d5db"
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        scrollbar = tk.Scrollbar(
            instruction_container,
            orient="vertical",
            command=canvas.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        canvas.configure(
            yscrollcommand=scrollbar.set
        )


        inner_frame = tk.Frame(
            canvas,
            bg="white"
        )


        canvas_window = canvas.create_window(
            (0, 0),
            window=inner_frame,
            anchor="nw"
        )


        def update_scroll_region(event=None):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )


        inner_frame.bind(
            "<Configure>",
            update_scroll_region
        )


        def update_canvas_width(event):

            canvas.itemconfig(
                canvas_window,
                width=event.width
            )


        canvas.bind(
            "<Configure>",
            update_canvas_width
        )


        # ====================================================
        # HEADING
        # ====================================================

        tk.Label(
            inner_frame,
            text="EXAM INFORMATION",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2563eb"
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 12)
        )


        # ====================================================
        # INSTRUCTIONS
        # ====================================================

        instructions = [

            "1. Questions will be displayed one at a time.",

            "2. Each question will display its allotted marks.",

            "3. The first question will be automatically read aloud.",

            "4. Every new question will be automatically read aloud.",

            "5. You can click PLAY QUESTION to hear the current question again.",

            "6. Click START ANSWERING before giving your answer.",

            "7. You will have 10 seconds to answer each question.",

            "8. The 10-second answering timer starts after START ANSWERING.",

            "9. The PLAY QUESTION button is disabled while answering.",

            "10. Your spoken answer will be recorded.",

            "11. Whisper will convert your spoken answer into text.",

            "12. The converted answer will appear in the YOUR ANSWER box.",

            "13. REANSWER allows you to record the answer again.",

            "14. A new REANSWER recording replaces the previous answer.",

            "15. You can move between previous and next questions.",

            "16. The Previous button is not shown on Question 1.",

            "17. The original/expected answer is NOT displayed during the examination.",

            "18. Answers are evaluated only after the examination is submitted.",

            "19. The entire examination has a separate countdown timer.",

            "20. If the examination timer reaches zero, the exam is submitted automatically.",

            "21. The examination window cannot be closed while the exam is running.",

            "22. SUBMIT EXAM becomes available after all questions are answered.",

            "23. Each student's answers are saved separately.",

            "24. Multiple attempts are stored separately for the same student.",

            "25. The student's complete examination record is saved.",

            "26. After submission, the student is automatically returned to Student Login."
        ]


        for instruction in instructions:

            tk.Label(
                inner_frame,
                text=instruction,
                font=("Arial", 10),
                bg="white",
                fg="#374151",
                anchor="w",
                justify="left",
                wraplength=850
            ).pack(
                fill="x",
                padx=25,
                pady=4
            )


        # ====================================================
        # WARNING
        # ====================================================

        tk.Label(
            inner_frame,
            text=(
                "IMPORTANT: Once the examination starts, "
                "do not close the examination window."
            ),
            font=("Arial", 10, "bold"),
            bg="#fef3c7",
            fg="#92400e",
            padx=12,
            pady=12
        ).pack(
            fill="x",
            padx=25,
            pady=20
        )


        # ====================================================
        # BUTTON FRAME
        # ====================================================

        button_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            fill="x",
            padx=50,
            pady=(0, 20)
        )


        # ====================================================
        # START EXAM
        # ====================================================

        self.start_button = tk.Button(
            button_frame,
            text="I UNDERSTAND - START EXAM",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=28,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.start_exam
        )

        self.start_button.pack(
            side="left",
            expand=True,
            padx=10
        )


        # ====================================================
        # BACK
        # ====================================================

        tk.Button(
            button_frame,
            text="BACK",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=12,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.go_back
        ).pack(
            side="left",
            padx=10
        )


        # ====================================================
        # MOUSE WHEEL
        # ====================================================

        def mouse_wheel(event):

            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )


        canvas.bind(
            "<MouseWheel>",
            mouse_wheel
        )


    # ========================================================
    # START EXAM
    # ========================================================

    def start_exam(self):

        # ----------------------------------------------------
        # Prevent second exam window
        # ----------------------------------------------------

        if self.exam_window is not None:

            try:

                if self.exam_window.winfo_exists():

                    self.exam_window.lift()

                    self.exam_window.focus_force()

                    return

            except Exception:

                self.exam_window = None


        # ----------------------------------------------------
        # Student check
        # ----------------------------------------------------

        if not self.student_data:

            messagebox.showerror(
                "Student Information Missing",
                "Student details could not be found.",
                parent=self.root
            )

            return


        student_name = self.student_data.get(
            "student_name",
            "Student"
        )


        # ----------------------------------------------------
        # Confirmation
        # ----------------------------------------------------

        confirmation = messagebox.askyesno(
            "Start Examination",
            (
                f"Student: {student_name}\n\n"
                "Are you ready to start the examination?\n\n"
                "The examination will begin after you click YES."
            ),
            parent=self.root
        )


        if not confirmation:

            return


        # ----------------------------------------------------
        # Disable button
        # ----------------------------------------------------

        self.start_button.config(
            state="disabled"
        )


        # ----------------------------------------------------
        # Import Exam
        # ----------------------------------------------------

        try:

            from gui.student.exam import ExamWindow


        except Exception as e:

            self.start_button.config(
                state="normal"
            )

            messagebox.showerror(
                "Import Error",
                (
                    "Could not load the examination.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Instructions
        # ----------------------------------------------------

        self.root.withdraw()


        # ----------------------------------------------------
        # Create ONE Exam window
        # ----------------------------------------------------

        try:

            self.exam_window = tk.Toplevel(
                self.root
            )

            self.exam_window.title(
                "CBT August 2026"
            )

            self.exam_window.geometry(
                "1100x750"
            )

            self.exam_window.minsize(
                900,
                650
            )

            self.exam_window.configure(
                bg="#f4f6f8"
            )

            maximize_window(self.exam_window)


            # ------------------------------------------------
            # PASS EVERYTHING
            # ------------------------------------------------

            ExamWindow(
                self.exam_window,
                parent_window=self.root,
                login_window=self.login_window,
                details_window=self.details_window,
                instructions_window=self.root
            )


        except Exception as e:

            try:

                self.exam_window.destroy()

            except Exception:

                pass


            self.exam_window = None

            self.root.deiconify()

            self.start_button.config(
                state="normal"
            )

            messagebox.showerror(
                "Exam Error",
                (
                    "Could not open the examination.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # BACK
    # ========================================================

    def go_back(self):

        answer = messagebox.askyesno(
            "Back",
            (
                "Do you want to return to "
                "Student Details?"
            ),
            parent=self.root
        )


        if not answer:

            return


        try:

            self.root.destroy()

        except Exception:

            pass


        if self.parent_window is not None:

            try:

                self.parent_window.deiconify()

                maximize_window(self.parent_window)

                self.parent_window.lift()

                self.parent_window.focus_force()

            except Exception as e:

                print(
                    "Could not restore Student Details:"
                )

                print(e)


# ============================================================
# OPEN EXAM INSTRUCTIONS
# ============================================================

def open_exam_instructions(
    parent_window=None,
    login_window=None,
    details_window=None
):

    window = tk.Toplevel(
        parent_window
    )


    maximize_window(window)


    ExamInstructions(
        window,
        parent_window=parent_window,
        login_window=login_window,
        details_window=details_window
    )


    return window


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()


    window = tk.Toplevel(
        root
    )


    ExamInstructions(
        window,
        parent_window=root,
        login_window=root,
        details_window=root
    )


    root.mainloop()
