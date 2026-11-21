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
# BACKEND DIRECTORIES
# ============================================================

BACKEND_DIR = os.path.join(
    BASE_DIR,
    "backend"
)


EXAMS_DIR = os.path.join(
    BACKEND_DIR,
    "exams"
)


STUDENTS_DIR = os.path.join(
    BACKEND_DIR,
    "students"
)


PATTERNS_DIR = os.path.join(
    BACKEND_DIR,
    "exam_patterns"
)


SESSIONS_DIR = os.path.join(
    BACKEND_DIR,
    "exam_sessions"
)


os.makedirs(EXAMS_DIR, exist_ok=True)
os.makedirs(STUDENTS_DIR, exist_ok=True)
os.makedirs(PATTERNS_DIR, exist_ok=True)
os.makedirs(SESSIONS_DIR, exist_ok=True)


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
# EXAM SESSION MANAGEMENT
# ============================================================

class ExamSessionManagement:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root
        self.parent_window = parent_window

        self.exams = []
        self.students = []
        self.patterns = []

        self.selected_students = []


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Exam Session Management - AI Oral Examination System"
        )

        self.root.geometry(
            "1200x800"
        )

        self.root.minsize(
            1000,
            700
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

        self.load_all_data()


    # ========================================================
    # CREATE INTERFACE
    # ========================================================

    def create_interface(self):

        # ====================================================
        # OUTER FRAME
        # ====================================================

        outer_frame = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )

        outer_frame.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # MAIN CANVAS
        # ====================================================

        self.main_canvas = tk.Canvas(
            outer_frame,
            bg="#f4f6f8",
            highlightthickness=0
        )

        self.main_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ====================================================
        # ENTIRE WINDOW VERTICAL SCROLLBAR
        # ====================================================

        main_scrollbar = ttk.Scrollbar(
            outer_frame,
            orient="vertical",
            command=self.main_canvas.yview
        )

        main_scrollbar.pack(
            side="right",
            fill="y"
        )


        self.main_canvas.configure(
            yscrollcommand=main_scrollbar.set
        )


        # ====================================================
        # SCROLLABLE MAIN FRAME
        # ====================================================

        main_frame = tk.Frame(
            self.main_canvas,
            bg="#f4f6f8"
        )


        self.canvas_window = self.main_canvas.create_window(
            (0, 0),
            window=main_frame,
            anchor="nw"
        )


        # ====================================================
        # UPDATE SCROLL REGION
        # ====================================================

        def update_scroll_region(event=None):

            self.main_canvas.configure(
                scrollregion=self.main_canvas.bbox("all")
            )


        main_frame.bind(
            "<Configure>",
            update_scroll_region
        )


        # ====================================================
        # KEEP CONTENT WIDTH EQUAL TO WINDOW WIDTH
        # ====================================================

        def resize_main_frame(event):

            self.main_canvas.itemconfigure(
                self.canvas_window,
                width=event.width
            )


        self.main_canvas.bind(
            "<Configure>",
            resize_main_frame
        )


        # ====================================================
        # MOUSE WHEEL
        # ====================================================

        def mouse_wheel(event):

            try:

                self.main_canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )

            except Exception:

                pass


        self.main_canvas.bind(
            "<MouseWheel>",
            mouse_wheel
        )


        # ====================================================
        # HEADER
        # ====================================================

        header_frame = tk.Frame(
            main_frame,
            bg="#1f2937",
            height=105
        )

        header_frame.pack(
            fill="x"
        )

        header_frame.pack_propagate(
            False
        )


        tk.Label(
            header_frame,
            text="EXAM SESSION MANAGEMENT",
            font=("Arial", 26, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(18, 3)
        )


        tk.Label(
            header_frame,
            text=(
                "Prepare, review and start an examination session"
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
            fill="x",
            padx=35,
            pady=20
        )


        # ====================================================
        # EXAM SETTINGS CARD
        # ====================================================

        settings_card = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )

        settings_card.pack(
            fill="x",
            pady=(0, 12)
        )


        tk.Label(
            settings_card,
            text="Examination Settings",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#111827"
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(0, 12)
        )


        # ====================================================
        # EXAM
        # ====================================================

        tk.Label(
            settings_card,
            text="Examination",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=7
        )


        self.exam_combo = ttk.Combobox(
            settings_card,
            width=35,
            state="readonly"
        )

        self.exam_combo.grid(
            row=1,
            column=1,
            padx=15,
            pady=7,
            sticky="w"
        )


        self.exam_combo.bind(
            "<<ComboboxSelected>>",
            self.exam_selected
        )


        # ====================================================
        # PATTERN
        # ====================================================

        tk.Label(
            settings_card,
            text="Exam Pattern",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=(30, 0),
            pady=7
        )


        self.pattern_combo = ttk.Combobox(
            settings_card,
            width=30,
            state="readonly"
        )

        self.pattern_combo.grid(
            row=1,
            column=3,
            padx=15,
            pady=7,
            sticky="w"
        )


        self.pattern_combo.bind(
            "<<ComboboxSelected>>",
            self.pattern_selected
        )


        # ====================================================
        # DATE
        # ====================================================

        tk.Label(
            settings_card,
            text="Exam Date",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=7
        )


        self.date_entry = ttk.Entry(
            settings_card,
            width=38
        )

        self.date_entry.grid(
            row=2,
            column=1,
            padx=15,
            pady=7,
            sticky="w"
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )


        # ====================================================
        # START TIME
        # ====================================================

        tk.Label(
            settings_card,
            text="Start Time",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=2,
            column=2,
            sticky="w",
            padx=(30, 0),
            pady=7
        )


        self.time_entry = ttk.Entry(
            settings_card,
            width=33
        )

        self.time_entry.grid(
            row=2,
            column=3,
            padx=15,
            pady=7,
            sticky="w"
        )

        self.time_entry.insert(
            0,
            datetime.now().strftime("%H:%M")
        )


        # ====================================================
        # DURATION
        # ====================================================

        tk.Label(
            settings_card,
            text="Duration (minutes)",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=7
        )


        self.duration_entry = ttk.Entry(
            settings_card,
            width=38
        )

        self.duration_entry.grid(
            row=3,
            column=1,
            padx=15,
            pady=7,
            sticky="w"
        )

        self.duration_entry.insert(
            0,
            "30"
        )


        # ====================================================
        # LOAD BUTTON
        # ====================================================

        tk.Button(
            settings_card,
            text="LOAD / CHECK EXAM",
            font=("Arial", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=22,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.check_exam
        ).grid(
            row=3,
            column=2,
            columnspan=2,
            padx=15,
            pady=7
        )


        # ====================================================
        # EXAM SUMMARY
        # ====================================================

        summary_card = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )

        summary_card.pack(
            fill="x",
            pady=(0, 12)
        )


        tk.Label(
            summary_card,
            text="Exam Summary",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            anchor="w"
        )


        self.summary_label = tk.Label(
            summary_card,
            text=(
                "Select an examination and click "
                "\"LOAD / CHECK EXAM\"."
            ),
            font=("Arial", 11),
            bg="white",
            fg="#4b5563",
            justify="left",
            anchor="w"
        )

        self.summary_label.pack(
            fill="x",
            pady=(8, 0)
        )


        # ====================================================
        # STUDENT CARD
        # ====================================================

        student_card = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )

        student_card.pack(
            fill="x",
            pady=(0, 12)
        )


        tk.Label(
            student_card,
            text="Select Students",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            anchor="w",
            pady=(0, 8)
        )


        tk.Label(
            student_card,
            text=(
                "Only Active students are shown. "
                "Select the students who can take this exam."
            ),
            font=("Arial", 10),
            bg="white",
            fg="#6b7280"
        ).pack(
            anchor="w",
            pady=(0, 8)
        )


        # ====================================================
        # LARGE STUDENT TABLE
        # ====================================================

        student_table_frame = tk.Frame(
            student_card,
            bg="white",
            height=500
        )

        student_table_frame.pack(
            fill="x",
            expand=False
        )

        student_table_frame.pack_propagate(
            False
        )


        # ====================================================
        # STUDENT TABLE
        # ====================================================

        columns = (
            "select",
            "student_id",
            "name",
            "email",
            "status"
        )


        self.student_tree = ttk.Treeview(
            student_table_frame,
            columns=columns,
            show="headings",
            selectmode="extended"
        )


        self.student_tree.heading(
            "select",
            text="Select"
        )

        self.student_tree.heading(
            "student_id",
            text="Student ID"
        )

        self.student_tree.heading(
            "name",
            text="Student Name"
        )

        self.student_tree.heading(
            "email",
            text="Email"
        )

        self.student_tree.heading(
            "status",
            text="Status"
        )


        self.student_tree.column(
            "select",
            width=80,
            anchor="center"
        )

        self.student_tree.column(
            "student_id",
            width=150,
            anchor="center"
        )

        self.student_tree.column(
            "name",
            width=250
        )

        self.student_tree.column(
            "email",
            width=350
        )

        self.student_tree.column(
            "status",
            width=110,
            anchor="center"
        )


        # ====================================================
        # STUDENT VERTICAL SCROLLBAR
        # ====================================================

        student_scrollbar = ttk.Scrollbar(
            student_table_frame,
            orient="vertical",
            command=self.student_tree.yview
        )


        self.student_tree.configure(
            yscrollcommand=student_scrollbar.set
        )


        self.student_tree.pack(
            side="left",
            fill="both",
            expand=True
        )


        student_scrollbar.pack(
            side="right",
            fill="y"
        )


        # ====================================================
        # STUDENT SELECTION
        # ====================================================

        self.student_tree.bind(
            "<Double-1>",
            self.toggle_student_selection
        )


        # ====================================================
        # BUTTON FRAME
        # ====================================================

        button_frame = tk.Frame(
            content_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            fill="x",
            pady=(0, 12)
        )


        # ====================================================
        # SELECT ALL
        # ====================================================

        tk.Button(
            button_frame,
            text="SELECT ALL",
            font=("Arial", 10, "bold"),
            bg="#475569",
            fg="white",
            activebackground="#334155",
            activeforeground="white",
            width=15,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.select_all_students
        ).pack(
            side="left",
            padx=5
        )


        # ====================================================
        # CLEAR SELECTION
        # ====================================================

        tk.Button(
            button_frame,
            text="CLEAR SELECTION",
            font=("Arial", 10, "bold"),
            bg="#f59e0b",
            fg="white",
            activebackground="#d97706",
            activeforeground="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.clear_student_selection
        ).pack(
            side="left",
            padx=5
        )


        # ====================================================
        # START EXAM SESSION
        # ====================================================

        tk.Button(
            button_frame,
            text="START EXAM SESSION",
            font=("Arial", 11, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=25,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.start_exam_session
        ).pack(
            side="right",
            padx=5
        )


        # ====================================================
        # BACK BUTTON
        # ====================================================

        tk.Button(
            button_frame,
            text="BACK TO ADMIN CONTROL PANEL",
            font=("Arial", 10, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=27,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        ).pack(
            side="right",
            padx=5
        )


        # ====================================================
        # UPDATE SCROLL REGION
        # ====================================================

        self.root.update_idletasks()

        self.main_canvas.configure(
            scrollregion=self.main_canvas.bbox("all")
        )

        self.main_canvas.yview_moveto(
            0
        )


    # ========================================================
    # LOAD ALL DATA
    # ========================================================

    def load_all_data(self):

        self.load_exams()
        self.load_patterns()
        self.load_students()


    # ========================================================
    # READ JSON FILES
    # ========================================================

    def read_json_file(self, file_path):

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, dict):

                return data

        except Exception as e:

            print(
                "Could not read JSON:",
                file_path,
                e
            )

        return None


    # ========================================================
    # LOAD EXAMS
    # ========================================================

    def load_exams(self):

        self.exams = []

        values = []


        if os.path.isdir(EXAMS_DIR):

            for filename in os.listdir(EXAMS_DIR):

                if not filename.lower().endswith(".json"):

                    continue


                file_path = os.path.join(
                    EXAMS_DIR,
                    filename
                )


                exam = self.read_json_file(
                    file_path
                )


                if not exam:

                    continue


                exam_id = str(
                    exam.get(
                        "exam_id",
                        os.path.splitext(filename)[0]
                    )
                )


                exam_name = str(
                    exam.get(
                        "exam_name",
                        exam.get(
                            "name",
                            exam_id
                        )
                    )
                )


                exam["exam_id"] = exam_id
                exam["exam_name"] = exam_name


                self.exams.append(
                    exam
                )


                values.append(
                    f"{exam_id} - {exam_name}"
                )


        self.exam_combo["values"] = values


        if values:

            self.exam_combo.current(0)

            self.exam_selected()


    # ========================================================
    # LOAD PATTERNS
    # ========================================================

    def load_patterns(self):

        self.patterns = []

        values = []


        if os.path.isdir(PATTERNS_DIR):

            for filename in os.listdir(PATTERNS_DIR):

                if not filename.lower().endswith(".json"):

                    continue


                file_path = os.path.join(
                    PATTERNS_DIR,
                    filename
                )


                pattern = self.read_json_file(
                    file_path
                )


                if not pattern:

                    continue


                pattern_id = str(
                    pattern.get(
                        "pattern_id",
                        os.path.splitext(filename)[0]
                    )
                )


                pattern_name = str(
                    pattern.get(
                        "pattern_name",
                        pattern.get(
                            "name",
                            pattern_id
                        )
                    )
                )


                pattern["pattern_id"] = pattern_id
                pattern["pattern_name"] = pattern_name


                self.patterns.append(
                    pattern
                )


                values.append(
                    f"{pattern_id} - {pattern_name}"
                )


        self.pattern_combo["values"] = values


        if values:

            self.pattern_combo.current(0)


    # ========================================================
    # LOAD STUDENTS
    # ========================================================

    def load_students(self):

        self.students = []


        for item in self.student_tree.get_children():

            self.student_tree.delete(
                item
            )


        if not os.path.isdir(STUDENTS_DIR):

            return


        for filename in os.listdir(STUDENTS_DIR):

            if not filename.lower().endswith(".json"):

                continue


            file_path = os.path.join(
                STUDENTS_DIR,
                filename
            )


            student = self.read_json_file(
                file_path
            )


            if not student:

                continue


            status = str(
                student.get(
                    "status",
                    "Active"
                )
            )


            if status.lower() != "active":

                continue


            student_id = str(
                student.get(
                    "student_id",
                    os.path.splitext(filename)[0]
                )
            )


            name = str(
                student.get(
                    "student_name",
                    ""
                )
            )


            email = str(
                student.get(
                    "email",
                    ""
                )
            )


            self.students.append(
                student
            )


            self.student_tree.insert(
                "",
                "end",
                values=(
                    "NO",
                    student_id,
                    name,
                    email,
                    status
                )
            )


    # ========================================================
    # EXAM SELECTED
    # ========================================================

    def exam_selected(self, event=None):

        selected = self.exam_combo.get().strip()


        if not selected:

            return


        exam_id = selected.split(
            " - ",
            1
        )[0]


        for exam in self.exams:

            if exam.get("exam_id") == exam_id:

                pattern_id = exam.get(
                    "pattern_id",
                    exam.get(
                        "exam_pattern_id",
                        ""
                    )
                )


                if pattern_id:

                    for index, pattern in enumerate(
                        self.patterns
                    ):

                        if str(
                            pattern.get(
                                "pattern_id"
                            )
                        ) == str(pattern_id):

                            self.pattern_combo.current(
                                index
                            )

                            break

                break


        self.update_summary()


    # ========================================================
    # PATTERN SELECTED
    # ========================================================

    def pattern_selected(self, event=None):

        self.update_summary()


    # ========================================================
    # CHECK EXAM
    # ========================================================

    def check_exam(self):

        exam = self.get_selected_exam()
        pattern = self.get_selected_pattern()


        if exam is None:

            messagebox.showwarning(
                "Exam Required",
                "Please select an examination.",
                parent=self.root
            )

            return False


        if pattern is None:

            messagebox.showwarning(
                "Pattern Required",
                "Please select an exam pattern.",
                parent=self.root
            )

            return False


        questions_required, total_marks = (
            self.get_pattern_totals(pattern)
        )


        if questions_required <= 0:

            messagebox.showwarning(
                "Invalid Pattern",
                (
                    "The selected exam pattern does not "
                    "contain a valid question distribution."
                ),
                parent=self.root
            )

            return False


        self.update_summary(
            questions_required,
            total_marks
        )


        messagebox.showinfo(
            "Exam Check",
            (
                "Exam and pattern loaded successfully.\n\n"
                f"Required Questions: {questions_required}\n"
                f"Total Marks: {total_marks}"
            ),
            parent=self.root
        )


        return True


    # ========================================================
    # GET SELECTED EXAM
    # ========================================================

    def get_selected_exam(self):

        selected = self.exam_combo.get().strip()


        if not selected:

            return None


        exam_id = selected.split(
            " - ",
            1
        )[0]


        for exam in self.exams:

            if str(
                exam.get("exam_id")
            ) == exam_id:

                return exam


        return None


    # ========================================================
    # GET SELECTED PATTERN
    # ========================================================

    def get_selected_pattern(self):

        selected = self.pattern_combo.get().strip()


        if not selected:

            return None


        pattern_id = selected.split(
            " - ",
            1
        )[0]


        for pattern in self.patterns:

            if str(
                pattern.get("pattern_id")
            ) == pattern_id:

                return pattern


        return None


    # ========================================================
    # GET PATTERN TOTALS
    # ========================================================

    def get_pattern_totals(self, pattern):

        question_count = 0
        total_marks = 0


        # ----------------------------------------------------
        # FORMAT 1:
        # sections = [
        #   {"marks": 1, "number_of_questions": 3}
        # ]
        # ----------------------------------------------------

        sections = pattern.get(
            "sections",
            []
        )


        if isinstance(sections, list):

            for section in sections:

                if not isinstance(section, dict):

                    continue


                marks = self.to_number(
                    section.get(
                        "marks",
                        section.get(
                            "mark",
                            0
                        )
                    )
                )


                count = self.to_number(
                    section.get(
                        "number_of_questions",
                        section.get(
                            "question_count",
                            section.get(
                                "count",
                                0
                            )
                        )
                    )
                )


                question_count += int(
                    count
                )


                total_marks += (
                    marks * count
                )


        # ----------------------------------------------------
        # FORMAT 2:
        # DIRECT VALUES
        # ----------------------------------------------------

        if question_count == 0:

            question_count = int(
                self.to_number(
                    pattern.get(
                        "total_questions",
                        pattern.get(
                            "number_of_questions",
                            0
                        )
                    )
                )
            )


            total_marks = self.to_number(
                pattern.get(
                    "total_marks",
                    pattern.get(
                        "total_mark",
                        0
                    )
                )
            )


        return question_count, total_marks


    # ========================================================
    # NUMBER CONVERSION
    # ========================================================

    def to_number(self, value):

        try:

            return float(value)

        except Exception:

            return 0


    # ========================================================
    # UPDATE SUMMARY
    # ========================================================

    def update_summary(
        self,
        question_count=None,
        total_marks=None
    ):

        exam = self.get_selected_exam()
        pattern = self.get_selected_pattern()


        if exam is None:

            return


        if pattern is not None:

            if question_count is None:

                question_count, total_marks = (
                    self.get_pattern_totals(
                        pattern
                    )
                )


            pattern_name = pattern.get(
                "pattern_name",
                pattern.get(
                    "name",
                    pattern.get(
                        "pattern_id",
                        ""
                    )
                )
            )

        else:

            pattern_name = "Not selected"
            question_count = 0
            total_marks = 0


        selected_count = len(
            self.get_selected_students()
        )


        self.summary_label.config(
            text=(
                f"Examination: "
                f"{exam.get('exam_name', '')}\n"
                f"Exam ID: "
                f"{exam.get('exam_id', '')}\n"
                f"Exam Pattern: "
                f"{pattern_name}\n"
                f"Total Questions: "
                f"{question_count}\n"
                f"Total Marks: "
                f"{self.format_number(total_marks)}\n"
                f"Selected Students: "
                f"{selected_count}\n"
                f"Date: "
                f"{self.date_entry.get().strip()}\n"
                f"Start Time: "
                f"{self.time_entry.get().strip()}\n"
                f"Duration: "
                f"{self.duration_entry.get().strip()} minutes"
            )
        )


    # ========================================================
    # FORMAT NUMBER
    # ========================================================

    def format_number(self, value):

        try:

            number = float(value)

            if number.is_integer():

                return str(
                    int(number)
                )

            return str(
                number
            )

        except Exception:

            return str(value)


    # ========================================================
    # TOGGLE STUDENT
    # ========================================================

    def toggle_student_selection(self, event=None):

        selected = self.student_tree.selection()


        if not selected:

            return


        for item in selected:

            values = list(
                self.student_tree.item(
                    item,
                    "values"
                )
            )


            if values[0] == "YES":

                values[0] = "NO"

            else:

                values[0] = "YES"


            self.student_tree.item(
                item,
                values=values
            )


        self.update_summary()


    # ========================================================
    # SELECT ALL STUDENTS
    # ========================================================

    def select_all_students(self):

        for item in self.student_tree.get_children():

            values = list(
                self.student_tree.item(
                    item,
                    "values"
                )
            )

            values[0] = "YES"

            self.student_tree.item(
                item,
                values=values
            )


        self.update_summary()


    # ========================================================
    # CLEAR STUDENT SELECTION
    # ========================================================

    def clear_student_selection(self):

        for item in self.student_tree.get_children():

            values = list(
                self.student_tree.item(
                    item,
                    "values"
                )
            )

            values[0] = "NO"

            self.student_tree.item(
                item,
                values=values
            )


        self.student_tree.selection_remove(
            self.student_tree.selection()
        )


        self.update_summary()


    # ========================================================
    # GET SELECTED STUDENTS
    # ========================================================

    def get_selected_students(self):

        selected_students = []


        for item in self.student_tree.get_children():

            values = self.student_tree.item(
                item,
                "values"
            )


            if values and values[0] == "YES":

                student_id = values[1]


                for student in self.students:

                    if str(
                        student.get(
                            "student_id"
                        )
                    ) == str(student_id):

                        selected_students.append(
                            student
                        )

                        break


        return selected_students


    # ========================================================
    # VALIDATE SESSION
    # ========================================================

    # ========================================================
    # VALIDATE EXAM QUESTIONS AGAINST PATTERN
    # ========================================================

    def validate_exam_pattern_questions(
        self,
        exam,
        pattern
    ):

        questions = exam.get(
            "questions",
            []
        )

        if not isinstance(questions, list):
            questions = []

        active_questions = []

        for question in questions:

            if not isinstance(question, dict):
                continue

            status = str(
                question.get(
                    "status",
                    "Active"
                )
            ).strip().lower()

            if status == "inactive":
                continue

            active_questions.append(question)

        required_questions, required_marks = (
            self.get_pattern_totals(pattern)
        )

        if required_questions <= 0:
            return False, (
                "The selected exam pattern has no valid "
                "question requirement."
            )

        available_count = len(active_questions)

        if available_count < required_questions:
            return False, (
                "Insufficient questions for the selected "
                "exam pattern.\n\n"
                f"Required questions: {required_questions}\n"
                f"Available active questions: {available_count}\n\n"
                "Please add more questions to this examination "
                "before starting the exam."
            )

        available_marks = 0

        for question in active_questions:
            available_marks += self.to_number(
                question.get(
                    "marks",
                    0
                )
            )

        if required_marks > 0 and available_marks < required_marks:
            return False, (
                "Insufficient question marks for the selected "
                "exam pattern.\n\n"
                f"Required marks: {self.format_number(required_marks)}\n"
                f"Available active question marks: "
                f"{self.format_number(available_marks)}\n\n"
                "Please add questions with sufficient marks "
                "before starting the exam."
            )

        sections = pattern.get(
            "sections",
            []
        )

        if isinstance(sections, list) and sections:

            type_mark_counts = {}
            mark_counts = {}
            type_counts = {}

            for question in active_questions:

                question_type = self.normalize_question_type(
                    question.get(
                        "question_type",
                        question.get(
                            "type",
                            ""
                        )
                    )
                )

                marks = self.to_number(
                    question.get(
                        "marks",
                        0
                    )
                )

                mark_key = self.number_key(marks)

                mark_counts[mark_key] = (
                    mark_counts.get(mark_key, 0) + 1
                )

                if question_type:
                    type_counts[question_type] = (
                        type_counts.get(question_type, 0) + 1
                    )

                    pair_key = (
                        question_type,
                        mark_key
                    )

                    type_mark_counts[pair_key] = (
                        type_mark_counts.get(pair_key, 0) + 1
                    )

            section_errors = []

            for index, section in enumerate(sections, start=1):

                if not isinstance(section, dict):
                    continue

                count = int(self.to_number(
                    section.get(
                        "number_of_questions",
                        section.get(
                            "question_count",
                            section.get(
                                "count",
                                0
                            )
                        )
                    )
                ))

                if count <= 0:
                    continue

                marks_value = section.get(
                    "marks",
                    section.get(
                        "mark",
                        None
                    )
                )

                section_marks = None

                if (
                    marks_value is not None
                    and str(marks_value).strip() != ""
                ):
                    section_marks = self.to_number(
                        marks_value
                    )

                section_type = self.normalize_question_type(
                    section.get(
                        "question_type",
                        section.get(
                            "type",
                            section.get(
                                "question_type_name",
                                section.get(
                                    "type_name",
                                    ""
                                )
                            )
                        )
                    )
                )

                if not section_type:
                    possible_name = self.normalize_question_type(
                        section.get(
                            "name",
                            ""
                        )
                    )

                    if possible_name in self.get_known_question_types():
                        section_type = possible_name

                available_for_section = None

                if section_type and section_marks is not None:
                    available_for_section = type_mark_counts.get(
                        (
                            section_type,
                            self.number_key(section_marks)
                        ),
                        0
                    )

                elif section_type:
                    available_for_section = type_counts.get(
                        section_type,
                        0
                    )

                elif section_marks is not None:
                    available_for_section = mark_counts.get(
                        self.number_key(section_marks),
                        0
                    )

                if available_for_section is None:
                    continue

                if available_for_section < count:

                    requirement_text = []

                    if section_type:
                        requirement_text.append(
                            f"Type: {section_type}"
                        )

                    if section_marks is not None:
                        requirement_text.append(
                            f"Marks: {self.format_number(section_marks)}"
                        )

                    requirement_text = ", ".join(
                        requirement_text
                    )

                    section_errors.append(
                        f"Section {index}: required {count}, "
                        f"available {available_for_section}"
                        + (
                            f" ({requirement_text})"
                            if requirement_text
                            else ""
                        )
                    )

            if section_errors:
                return False, (
                    "The questions in this examination do not "
                    "match the selected exam pattern.\n\n"
                    + "\n".join(section_errors)
                    + "\n\nPlease add or correct the questions "
                    "before starting the exam."
                )

        return True, ""


    # ========================================================
    # NORMALIZE QUESTION TYPE
    # ========================================================

    def normalize_question_type(
        self,
        value
    ):

        text = str(value or "").strip().lower()

        if not text:
            return ""

        aliases = {
            "one word": "One Word / 1 Mark",
            "one-word": "One Word / 1 Mark",
            "one word / 1 mark": "One Word / 1 Mark",
            "one word/1 mark": "One Word / 1 Mark",
            "1 mark": "One Word / 1 Mark",
            "1-mark": "One Word / 1 Mark",
            "short answer": "Short Answer",
            "short-answer": "Short Answer",
            "descriptive answer": "Descriptive Answer",
            "descriptive-answer": "Descriptive Answer",
            "long answer": "Descriptive Answer",
            "long-answer": "Descriptive Answer"
        }

        return aliases.get(
            text,
            str(value).strip()
        )


    # ========================================================
    # KNOWN QUESTION TYPES
    # ========================================================

    def get_known_question_types(self):

        return {
            "One Word / 1 Mark",
            "Short Answer",
            "Descriptive Answer"
        }


    # ========================================================
    # NUMBER KEY
    # ========================================================

    def number_key(
        self,
        value
    ):

        try:
            return round(
                float(value),
                6
            )
        except Exception:
            return 0


    # ========================================================
    # VALIDATE SESSION
    # ========================================================

    def validate_session(self):

        exam = self.get_selected_exam()
        pattern = self.get_selected_pattern()


        if exam is None:

            messagebox.showwarning(
                "Exam Required",
                "Please select an examination.",
                parent=self.root
            )

            return None


        if pattern is None:

            messagebox.showwarning(
                "Pattern Required",
                "Please select an exam pattern.",
                parent=self.root
            )

            return None


        students = self.get_selected_students()


        if not students:

            messagebox.showwarning(
                "Students Required",
                "Please select at least one active student.",
                parent=self.root
            )

            return None


        exam_date = (
            self.date_entry
            .get()
            .strip()
        )


        start_time = (
            self.time_entry
            .get()
            .strip()
        )


        duration_text = (
            self.duration_entry
            .get()
            .strip()
        )


        if not exam_date:

            messagebox.showwarning(
                "Date Required",
                "Please enter the exam date.",
                parent=self.root
            )

            return None


        if not start_time:

            messagebox.showwarning(
                "Start Time Required",
                "Please enter the exam start time.",
                parent=self.root
            )

            return None


        try:

            datetime.strptime(
                exam_date,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Date",
                "Use date format YYYY-MM-DD.",
                parent=self.root
            )

            return None


        try:

            datetime.strptime(
                start_time,
                "%H:%M"
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Time",
                "Use 24-hour time format HH:MM.",
                parent=self.root
            )

            return None


        try:

            duration = int(
                duration_text
            )

            if duration <= 0:

                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Duration",
                "Duration must be a positive number of minutes.",
                parent=self.root
            )

            return None


        questions_required, total_marks = (
            self.get_pattern_totals(
                pattern
            )
        )

        # ----------------------------------------------------
        # ENSURE THE SELECTED PATTERN BELONGS TO THE EXAM
        # ----------------------------------------------------
        exam_pattern_id = exam.get(
            "pattern_id",
            exam.get(
                "exam_pattern_id",
                exam.get(
                    "pattern",
                    ""
                )
            )
        )

        selected_pattern_id = pattern.get(
            "pattern_id",
            ""
        )

        if exam_pattern_id and selected_pattern_id:

            if str(exam_pattern_id) != str(selected_pattern_id):

                messagebox.showwarning(
                    "Exam Pattern Mismatch",
                    (
                        "The selected exam pattern does not "
                        "belong to this examination.\n\n"
                        f"Exam pattern: {exam_pattern_id}\n"
                        f"Selected pattern: {selected_pattern_id}\n\n"
                        "Please select the correct exam pattern "
                        "before starting the exam."
                    ),
                    parent=self.root
                )

                return None



        if questions_required <= 0:

            messagebox.showwarning(
                "Invalid Pattern",
                "The exam pattern has no valid questions.",
                parent=self.root
            )

            return None


        # ----------------------------------------------------
        # FINAL QUESTION/PATTERN COMPATIBILITY CHECK
        # ----------------------------------------------------
        questions_match, mismatch_message = (
            self.validate_exam_pattern_questions(
                exam,
                pattern
            )
        )

        if not questions_match:

            messagebox.showwarning(
                "Insufficient / Mismatched Questions",
                mismatch_message,
                parent=self.root
            )

            return None

        return {
            "exam": exam,
            "pattern": pattern,
            "students": students,
            "exam_date": exam_date,
            "start_time": start_time,
            "duration": duration,
            "total_questions": questions_required,
            "total_marks": total_marks
        }


    # ========================================================
    # START EXAM SESSION
    # ========================================================

    def start_exam_session(self):

        session_data = self.validate_session()


        if session_data is None:

            return


        exam = session_data["exam"]
        pattern = session_data["pattern"]
        students = session_data["students"]


        student_ids = [
            student.get(
                "student_id"
            )
            for student in students
        ]


        summary = (
            f"Examination: "
            f"{exam.get('exam_name', '')}\n\n"
            f"Pattern: "
            f"{pattern.get('pattern_name', '')}\n\n"
            f"Questions: "
            f"{session_data['total_questions']}\n"
            f"Total Marks: "
            f"{self.format_number(session_data['total_marks'])}\n\n"
            f"Students: "
            f"{len(student_ids)}\n"
            f"Date: "
            f"{session_data['exam_date']}\n"
            f"Start Time: "
            f"{session_data['start_time']}\n"
            f"Duration: "
            f"{session_data['duration']} minutes\n\n"
            "Do you want to start this examination session?"
        )


        answer = messagebox.askyesno(
            "Start Exam Session",
            summary,
            parent=self.root
        )


        if not answer:

            return


        session_id = self.generate_session_id()


        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        session = {

            "session_id": session_id,

            "exam_id": exam.get(
                "exam_id",
                ""
            ),

            "exam_name": exam.get(
                "exam_name",
                ""
            ),

            "pattern_id": pattern.get(
                "pattern_id",
                ""
            ),

            "pattern_name": pattern.get(
                "pattern_name",
                ""
            ),

            "total_questions":
                session_data[
                    "total_questions"
                ],

            "total_marks":
                session_data[
                    "total_marks"
                ],

            "student_ids":
                student_ids,

            "exam_date":
                session_data[
                    "exam_date"
                ],

            "start_time":
                session_data[
                    "start_time"
                ],

            "duration_minutes":
                session_data[
                    "duration"
                ],

            "status": "Active",

            "created_at": now,

            "updated_at": now
        }


        file_path = os.path.join(
            SESSIONS_DIR,
            f"{session_id}.json"
        )


        try:

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    session,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except Exception as e:

            messagebox.showerror(
                "Session Error",
                (
                    "Could not create the exam session.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        messagebox.showinfo(
            "Exam Session Started",
            (
                "Exam session created successfully.\n\n"
                f"Session ID: {session_id}\n"
                f"Exam: {session['exam_name']}\n"
                f"Students: {len(student_ids)}\n\n"
                "The session status is ACTIVE."
            ),
            parent=self.root
        )


        self.clear_student_selection()


    # ========================================================
    # GENERATE SESSION ID
    # ========================================================

    def generate_session_id(self):

        number = 1


        while True:

            session_id = (
                f"SES{number:04d}"
            )


            file_path = os.path.join(
                SESSIONS_DIR,
                f"{session_id}.json"
            )


            if not os.path.exists(
                file_path
            ):

                return session_id


            number += 1


    # ========================================================
    # BACK TO ADMIN CONTROL PANEL
    # ========================================================

    def back(self):

        answer = messagebox.askyesno(
            "Back to Admin Control Panel",
            (
                "Do you want to return to "
                "the Admin Control Panel?"
            ),
            parent=self.root
        )


        if not answer:

            return


        parent = self.parent_window


        try:

            if self.root.winfo_exists():

                self.root.destroy()

        except Exception as e:

            print(
                "Could not close Exam Session Management:",
                e
            )


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


    session_window = tk.Toplevel(
        root
    )


    ExamSessionManagement(
        session_window,
        parent_window=root
    )


    root.mainloop()
