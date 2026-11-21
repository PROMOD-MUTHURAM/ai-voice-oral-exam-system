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
# BACKEND
# ============================================================

BACKEND_DIR = os.path.join(
    BASE_DIR,
    "backend"
)

EXAMS_DIR = os.path.join(
    BACKEND_DIR,
    "exams"
)

# NEW: EXAM PATTERNS DIRECTORY
PATTERNS_DIR = os.path.join(
    BACKEND_DIR,
    "exam_patterns"
)

os.makedirs(
    EXAMS_DIR,
    exist_ok=True
)

os.makedirs(
    PATTERNS_DIR,
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
# EXAM PATTERN
# ============================================================

class ExamPattern:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        self.parent_window = parent_window

        self.selected_exam_id = None

        self.content_canvas = None


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Exam Pattern - AI Oral Examination System"
        )

        self.root.geometry(
            "1100x800"
        )

        self.root.minsize(
            900,
            650
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

        self.load_exams()


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
            text="EXAM PATTERN",
            font=("Arial", 27, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(20, 3)
        )


        tk.Label(
            header_frame,
            text=(
                "Configure questions and marks "
                "for an examination"
            ),
            font=("Arial", 11),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack()


        # ====================================================
        # SCROLLABLE AREA
        # ====================================================

        outer_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        outer_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )


        self.content_canvas = tk.Canvas(
            outer_frame,
            bg="#f4f6f8",
            highlightthickness=0
        )

        self.content_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        scrollbar = ttk.Scrollbar(
            outer_frame,
            orient="vertical",
            command=self.content_canvas.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.content_canvas.configure(
            yscrollcommand=scrollbar.set
        )


        content_frame = tk.Frame(
            self.content_canvas,
            bg="#f4f6f8"
        )


        content_window = self.content_canvas.create_window(
            (0, 0),
            window=content_frame,
            anchor="nw"
        )


        def update_scroll_region(event=None):

            try:

                if (
                    self.content_canvas is not None
                    and
                    self.content_canvas.winfo_exists()
                ):

                    self.content_canvas.configure(
                        scrollregion=(
                            self.content_canvas.bbox("all")
                        )
                    )

            except tk.TclError:
                pass


        content_frame.bind(
            "<Configure>",
            update_scroll_region
        )


        def update_content_width(event):

            try:

                if (
                    self.content_canvas is not None
                    and
                    self.content_canvas.winfo_exists()
                ):

                    self.content_canvas.itemconfigure(
                        content_window,
                        width=event.width
                    )

            except tk.TclError:
                pass


        self.content_canvas.bind(
            "<Configure>",
            update_content_width
        )


        # ====================================================
        # MOUSE WHEEL
        # ====================================================

        def mouse_wheel(event):

            try:

                if (
                    self.content_canvas is not None
                    and
                    self.content_canvas.winfo_exists()
                ):

                    self.content_canvas.yview_scroll(
                        int(
                            -1 *
                            (event.delta / 120)
                        ),
                        "units"
                    )

            except tk.TclError:
                pass


        self.content_canvas.bind(
            "<MouseWheel>",
            mouse_wheel
        )


        # ====================================================
        # PATTERN CARD
        # ====================================================

        pattern_card = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid",
            padx=35,
            pady=25
        )

        pattern_card.pack(
            fill="x",
            padx=30,
            pady=10
        )


        # ====================================================
        # EXAM SELECTION
        # ====================================================

        tk.Label(
            pattern_card,
            text="Select Exam",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=10
        )


        self.exam_combo = ttk.Combobox(
            pattern_card,
            width=48,
            state="readonly"
        )

        self.exam_combo.grid(
            row=0,
            column=1,
            columnspan=3,
            padx=25,
            pady=10,
            sticky="w"
        )


        self.exam_combo.bind(
            "<<ComboboxSelected>>",
            self.exam_selected
        )


        # ====================================================
        # EXAM INFORMATION
        # ====================================================

        self.exam_info_label = tk.Label(
            pattern_card,
            text="No exam selected",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151",
            anchor="w"
        )

        self.exam_info_label.grid(
            row=1,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(5, 20)
        )


        # ====================================================
        # QUESTION PATTERN TITLE
        # ====================================================

        tk.Label(
            pattern_card,
            text="QUESTION TYPE DISTRIBUTION",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#111827"
        ).grid(
            row=2,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(5, 15)
        )


        # ====================================================
        # TABLE HEADERS
        # ====================================================

        tk.Label(
            pattern_card,
            text="Question Type",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=7
        )


        tk.Label(
            pattern_card,
            text="No. of Questions",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=3,
            column=1,
            padx=20,
            pady=7
        )


        tk.Label(
            pattern_card,
            text="Marks Each",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=3,
            column=2,
            padx=20,
            pady=7
        )


        tk.Label(
            pattern_card,
            text="Total Marks",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=3,
            column=3,
            padx=20,
            pady=7
        )


        # ====================================================
        # ONE WORD
        # ====================================================

        tk.Label(
            pattern_card,
            text="One Word / 1 Mark",
            font=("Arial", 11),
            bg="white",
            fg="#374151"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            pady=10
        )


        self.one_word_entry = ttk.Entry(
            pattern_card,
            width=15
        )

        self.one_word_entry.grid(
            row=4,
            column=1,
            padx=20,
            pady=10
        )


        self.one_word_marks_entry = ttk.Entry(
            pattern_card,
            width=15
        )

        self.one_word_marks_entry.grid(
            row=4,
            column=2,
            padx=20,
            pady=10
        )


        self.one_word_total_label = tk.Label(
            pattern_card,
            text="0",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#2563eb"
        )

        self.one_word_total_label.grid(
            row=4,
            column=3,
            padx=20,
            pady=10
        )


        # ====================================================
        # SHORT ANSWER
        # ====================================================

        tk.Label(
            pattern_card,
            text="Short Answer",
            font=("Arial", 11),
            bg="white",
            fg="#374151"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=10
        )


        self.short_answer_entry = ttk.Entry(
            pattern_card,
            width=15
        )

        self.short_answer_entry.grid(
            row=5,
            column=1,
            padx=20,
            pady=10
        )


        self.short_answer_marks_entry = ttk.Entry(
            pattern_card,
            width=15
        )

        self.short_answer_marks_entry.grid(
            row=5,
            column=2,
            padx=20,
            pady=10
        )


        self.short_answer_total_label = tk.Label(
            pattern_card,
            text="0",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#2563eb"
        )

        self.short_answer_total_label.grid(
            row=5,
            column=3,
            padx=20,
            pady=10
        )


        # ====================================================
        # DESCRIPTIVE ANSWER
        # ====================================================

        tk.Label(
            pattern_card,
            text="Descriptive Answer",
            font=("Arial", 11),
            bg="white",
            fg="#374151"
        ).grid(
            row=6,
            column=0,
            sticky="w",
            pady=10
        )


        self.descriptive_entry = ttk.Entry(
            pattern_card,
            width=15
        )

        self.descriptive_entry.grid(
            row=6,
            column=1,
            padx=20,
            pady=10
        )


        self.descriptive_marks_entry = ttk.Entry(
            pattern_card,
            width=15
        )

        self.descriptive_marks_entry.grid(
            row=6,
            column=2,
            padx=20,
            pady=10
        )


        self.descriptive_total_label = tk.Label(
            pattern_card,
            text="0",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#2563eb"
        )

        self.descriptive_total_label.grid(
            row=6,
            column=3,
            padx=20,
            pady=10
        )


        # ====================================================
        # SEPARATOR
        # ====================================================

        ttk.Separator(
            pattern_card,
            orient="horizontal"
        ).grid(
            row=7,
            column=0,
            columnspan=4,
            sticky="ew",
            pady=15
        )


        # ====================================================
        # TOTAL QUESTIONS
        # ====================================================

        tk.Label(
            pattern_card,
            text="TOTAL QUESTIONS",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#111827"
        ).grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="w",
            pady=8
        )


        self.total_questions_label = tk.Label(
            pattern_card,
            text="0",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#2563eb"
        )

        self.total_questions_label.grid(
            row=8,
            column=1,
            padx=20,
            pady=8
        )


        # ====================================================
        # TOTAL MARKS
        # ====================================================

        tk.Label(
            pattern_card,
            text="TOTAL MARKS",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#111827"
        ).grid(
            row=9,
            column=0,
            columnspan=2,
            sticky="w",
            pady=8
        )


        self.total_marks_label = tk.Label(
            pattern_card,
            text="0",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#16a34a"
        )

        self.total_marks_label.grid(
            row=9,
            column=1,
            padx=20,
            pady=8
        )


        # ====================================================
        # BUTTON FRAME
        # ====================================================

        button_frame = tk.Frame(
            content_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            pady=(10, 25)
        )


        # ====================================================
        # LOAD
        # ====================================================

        tk.Button(
            button_frame,
            text="LOAD PATTERN",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.load_selected_exam
        ).grid(
            row=0,
            column=0,
            padx=7
        )


        # ====================================================
        # SAVE
        # ====================================================

        tk.Button(
            button_frame,
            text="SAVE PATTERN",
            font=("Arial", 11, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.save_pattern
        ).grid(
            row=0,
            column=1,
            padx=7
        )


        # ====================================================
        # CLEAR
        # ====================================================

        tk.Button(
            button_frame,
            text="CLEAR",
            font=("Arial", 11, "bold"),
            bg="#f59e0b",
            fg="white",
            activebackground="#d97706",
            activeforeground="white",
            width=15,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.clear_pattern
        ).grid(
            row=0,
            column=2,
            padx=7
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
            width=15,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        ).grid(
            row=0,
            column=3,
            padx=7
        )


        # ====================================================
        # AUTO UPDATE
        # ====================================================

        entries = [
            self.one_word_entry,
            self.one_word_marks_entry,
            self.short_answer_entry,
            self.short_answer_marks_entry,
            self.descriptive_entry,
            self.descriptive_marks_entry
        ]

        for entry in entries:

            entry.bind(
                "<KeyRelease>",
                self.update_totals
            )


    # ========================================================
    # LOAD EXAMS
    # ========================================================

    def load_exams(self):

        exam_list = []


        if not os.path.exists(EXAMS_DIR):

            self.exam_combo["values"] = []

            return


        try:

            files = os.listdir(
                EXAMS_DIR
            )

        except Exception as e:

            messagebox.showerror(
                "Exam Error",
                (
                    "Could not access the exams folder.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        for filename in files:

            if not filename.lower().endswith(".json"):
                continue


            file_path = os.path.join(
                EXAMS_DIR,
                filename
            )


            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    exam_data = json.load(
                        file
                    )


                if not isinstance(
                    exam_data,
                    dict
                ):
                    continue


                exam_id = str(
                    exam_data.get(
                        "exam_id",
                        ""
                    )
                ).strip()


                exam_name = str(
                    exam_data.get(
                        "exam_name",
                        ""
                    )
                ).strip()


                if not exam_id:
                    continue


                if exam_name:

                    display_name = (
                        f"{exam_id} - {exam_name}"
                    )

                else:

                    display_name = exam_id


                exam_list.append(
                    display_name
                )


            except Exception:

                continue


        exam_list.sort(
            key=lambda value: value.lower()
        )


        self.exam_combo["values"] = exam_list


        if exam_list:

            self.exam_combo.current(0)

            self.load_selected_exam()

        else:

            messagebox.showwarning(
                "No Exams",
                (
                    "No examinations have been created yet.\n\n"
                    "Please create an exam first."
                ),
                parent=self.root
            )


    # ========================================================
    # GET SELECTED EXAM ID
    # ========================================================

    def get_selected_exam_id(self):

        selected = (
            self.exam_combo
            .get()
            .strip()
        )


        if not selected:
            return None


        if " - " in selected:

            return selected.split(
                " - ",
                1
            )[0].strip()


        return selected


    # ========================================================
    # EXAM SELECTED
    # ========================================================

    def exam_selected(
        self,
        event=None
    ):

        self.load_selected_exam()


    # ========================================================
    # SET ENTRY VALUE
    # ========================================================

    def set_entry_value(
        self,
        entry,
        value
    ):

        entry.delete(
            0,
            tk.END
        )

        entry.insert(
            0,
            str(value)
        )


    # ========================================================
    # LOAD SELECTED EXAM
    # ========================================================

    def load_selected_exam(self):

        exam_id = self.get_selected_exam_id()


        if not exam_id:

            self.selected_exam_id = None

            self.exam_info_label.config(
                text="No exam selected"
            )

            self.clear_pattern()

            return


        file_path = os.path.join(
            EXAMS_DIR,
            f"{exam_id}.json"
        )


        if not os.path.isfile(
            file_path
        ):

            messagebox.showerror(
                "Exam Not Found",
                (
                    f"Exam ID: {exam_id}\n\n"
                    "The exam JSON file could not be found."
                ),
                parent=self.root
            )

            return


        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                exam_data = json.load(
                    file
                )

        except Exception as e:

            messagebox.showerror(
                "Read Error",
                (
                    "Could not read the exam file.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        if not isinstance(
            exam_data,
            dict
        ):

            messagebox.showerror(
                "Invalid Exam",
                "Invalid exam data.",
                parent=self.root
            )

            return


        self.selected_exam_id = exam_id


        exam_name = str(
            exam_data.get(
                "exam_name",
                ""
            )
        ).strip()


        if exam_name:

            self.exam_info_label.config(
                text=(
                    f"Exam ID: {exam_id}"
                    f"    |    "
                    f"Exam Name: {exam_name}"
                )
            )

        else:

            self.exam_info_label.config(
                text=f"Exam ID: {exam_id}"
            )


        pattern = exam_data.get(
            "exam_pattern",
            {}
        )


        if not isinstance(
            pattern,
            dict
        ):

            pattern = {}


        question_distribution = pattern.get(
            "question_distribution",
            {}
        )


        if not isinstance(
            question_distribution,
            dict
        ):

            question_distribution = {}


        marks_per_question = pattern.get(
            "marks_per_question",
            {}
        )


        if not isinstance(
            marks_per_question,
            dict
        ):

            marks_per_question = {}


        # ----------------------------------------------------
        # QUESTIONS
        # ----------------------------------------------------

        one_word_questions = question_distribution.get(
            "One Word / 1 Mark",
            0
        )

        short_answer_questions = question_distribution.get(
            "Short Answer",
            0
        )

        descriptive_questions = question_distribution.get(
            "Descriptive Answer",
            0
        )


        # ----------------------------------------------------
        # MARKS
        # ----------------------------------------------------

        one_word_marks = marks_per_question.get(
            "One Word / 1 Mark",
            1
        )

        short_answer_marks = marks_per_question.get(
            "Short Answer",
            2
        )

        descriptive_marks = marks_per_question.get(
            "Descriptive Answer",
            5
        )


        self.set_entry_value(
            self.one_word_entry,
            one_word_questions
        )

        self.set_entry_value(
            self.short_answer_entry,
            short_answer_questions
        )

        self.set_entry_value(
            self.descriptive_entry,
            descriptive_questions
        )


        self.set_entry_value(
            self.one_word_marks_entry,
            one_word_marks
        )

        self.set_entry_value(
            self.short_answer_marks_entry,
            short_answer_marks
        )

        self.set_entry_value(
            self.descriptive_marks_entry,
            descriptive_marks
        )


        self.update_totals()


    # ========================================================
    # GET NON-NEGATIVE NUMBER
    # ========================================================

    def get_non_negative_number(
        self,
        value
    ):

        try:

            number = float(
                str(value).strip()
            )

            if number < 0:
                return None

            return number

        except Exception:

            return None


    # ========================================================
    # GET NON-NEGATIVE INTEGER
    # ========================================================

    def get_non_negative_integer(
        self,
        value
    ):

        try:

            number = int(
                str(value).strip()
            )

            if number < 0:
                return None

            return number

        except Exception:

            return None


    # ========================================================
    # FORMAT NUMBER
    # ========================================================

    def format_number(
        self,
        value
    ):

        try:

            value = float(value)

            if value.is_integer():

                return str(
                    int(value)
                )

            return str(
                round(value, 2)
            )

        except Exception:

            return "0"


    # ========================================================
    # UPDATE TOTALS
    # ========================================================

    def update_totals(
        self,
        event=None
    ):

        one_word = self.get_non_negative_integer(
            self.one_word_entry.get()
        )

        short_answer = self.get_non_negative_integer(
            self.short_answer_entry.get()
        )

        descriptive = self.get_non_negative_integer(
            self.descriptive_entry.get()
        )


        one_word_marks = self.get_non_negative_number(
            self.one_word_marks_entry.get()
        )

        short_answer_marks = self.get_non_negative_number(
            self.short_answer_marks_entry.get()
        )

        descriptive_marks = self.get_non_negative_number(
            self.descriptive_marks_entry.get()
        )


        if one_word is None:
            one_word = 0

        if short_answer is None:
            short_answer = 0

        if descriptive is None:
            descriptive = 0


        if one_word_marks is None:
            one_word_marks = 0

        if short_answer_marks is None:
            short_answer_marks = 0

        if descriptive_marks is None:
            descriptive_marks = 0


        one_word_total = (
            one_word *
            one_word_marks
        )


        short_answer_total = (
            short_answer *
            short_answer_marks
        )


        descriptive_total = (
            descriptive *
            descriptive_marks
        )


        self.one_word_total_label.config(
            text=self.format_number(
                one_word_total
            )
        )


        self.short_answer_total_label.config(
            text=self.format_number(
                short_answer_total
            )
        )


        self.descriptive_total_label.config(
            text=self.format_number(
                descriptive_total
            )
        )


        total_questions = (
            one_word
            +
            short_answer
            +
            descriptive
        )


        self.total_questions_label.config(
            text=str(
                total_questions
            )
        )


        total_marks = (
            one_word_total
            +
            short_answer_total
            +
            descriptive_total
        )


        self.total_marks_label.config(
            text=self.format_number(
                total_marks
            )
        )


    # ========================================================
    # SAVE PATTERN
    # ========================================================

    def save_pattern(self):

        exam_id = self.get_selected_exam_id()


        if not exam_id:

            messagebox.showwarning(
                "No Exam Selected",
                "Please select an exam first.",
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # QUESTIONS
        # ----------------------------------------------------

        one_word = self.get_non_negative_integer(
            self.one_word_entry.get()
        )

        short_answer = self.get_non_negative_integer(
            self.short_answer_entry.get()
        )

        descriptive = self.get_non_negative_integer(
            self.descriptive_entry.get()
        )


        # ----------------------------------------------------
        # MARKS
        # ----------------------------------------------------

        one_word_marks = self.get_non_negative_number(
            self.one_word_marks_entry.get()
        )

        short_answer_marks = self.get_non_negative_number(
            self.short_answer_marks_entry.get()
        )

        descriptive_marks = self.get_non_negative_number(
            self.descriptive_marks_entry.get()
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if (
            one_word is None
            or
            short_answer is None
            or
            descriptive is None
        ):

            messagebox.showwarning(
                "Invalid Questions",
                (
                    "Number of questions must be "
                    "non-negative whole numbers."
                ),
                parent=self.root
            )

            return


        if (
            one_word_marks is None
            or
            short_answer_marks is None
            or
            descriptive_marks is None
        ):

            messagebox.showwarning(
                "Invalid Marks",
                (
                    "Marks for each question must be "
                    "non-negative numbers."
                ),
                parent=self.root
            )

            return


        total_questions = (
            one_word
            +
            short_answer
            +
            descriptive
        )


        if total_questions <= 0:

            messagebox.showwarning(
                "Invalid Pattern",
                (
                    "The exam pattern must contain "
                    "at least one question."
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # EXAM FILE
        # ----------------------------------------------------

        file_path = os.path.join(
            EXAMS_DIR,
            f"{exam_id}.json"
        )


        if not os.path.isfile(
            file_path
        ):

            messagebox.showerror(
                "Exam Not Found",
                (
                    f"The exam file for {exam_id} "
                    "could not be found."
                ),
                parent=self.root
            )

            return


        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                exam_data = json.load(
                    file
                )

        except Exception as e:

            messagebox.showerror(
                "Read Error",
                (
                    "Could not read the exam file.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        if not isinstance(
            exam_data,
            dict
        ):

            messagebox.showerror(
                "Invalid Exam",
                "Invalid exam data.",
                parent=self.root
            )

            return


        # ====================================================
        # EXAM NAME
        # ====================================================

        exam_name = str(
            exam_data.get(
                "exam_name",
                exam_id
            )
        ).strip()


        # ====================================================
        # PATTERN ID
        # ====================================================

        pattern_id = f"PAT_{exam_id}"


        # ====================================================
        # PATTERN NAME
        # ====================================================

        pattern_name = f"{exam_name} Pattern"


        # ====================================================
        # CALCULATE TOTALS
        # ====================================================

        one_word_total = (
            one_word *
            one_word_marks
        )

        short_answer_total = (
            short_answer *
            short_answer_marks
        )

        descriptive_total = (
            descriptive *
            descriptive_marks
        )

        total_marks = (
            one_word_total
            +
            short_answer_total
            +
            descriptive_total
        )


        # ====================================================
        # CREATE PATTERN DATA
        # ====================================================

        pattern_data = {

            "pattern_id":
                pattern_id,

            "pattern_name":
                pattern_name,

            "exam_id":
                exam_id,

            "exam_name":
                exam_name,

            "sections": [

                {
                    "question_type":
                        "One Word / 1 Mark",

                    "number_of_questions":
                        one_word,

                    "marks":
                        one_word_marks,

                    "total_marks":
                        one_word_total
                },

                {
                    "question_type":
                        "Short Answer",

                    "number_of_questions":
                        short_answer,

                    "marks":
                        short_answer_marks,

                    "total_marks":
                        short_answer_total
                },

                {
                    "question_type":
                        "Descriptive Answer",

                    "number_of_questions":
                        descriptive,

                    "marks":
                        descriptive_marks,

                    "total_marks":
                        descriptive_total
                }

            ],

            "question_distribution": {

                "One Word / 1 Mark":
                    one_word,

                "Short Answer":
                    short_answer,

                "Descriptive Answer":
                    descriptive
            },

            "marks_per_question": {

                "One Word / 1 Mark":
                    one_word_marks,

                "Short Answer":
                    short_answer_marks,

                "Descriptive Answer":
                    descriptive_marks
            },

            "question_type_total_marks": {

                "One Word / 1 Mark":
                    one_word_total,

                "Short Answer":
                    short_answer_total,

                "Descriptive Answer":
                    descriptive_total
            },

            "total_questions":
                total_questions,

            "total_marks":
                total_marks,

            "updated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        }


        # ====================================================
        # SAVE SEPARATE PATTERN JSON
        # ====================================================

        os.makedirs(
            PATTERNS_DIR,
            exist_ok=True
        )


        pattern_file_path = os.path.join(
            PATTERNS_DIR,
            f"{pattern_id}.json"
        )


        try:

            with open(
                pattern_file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    pattern_data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except Exception as e:

            messagebox.showerror(
                "Pattern Save Error",
                (
                    "Could not save the exam pattern "
                    "file.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ====================================================
        # ALSO SAVE PATTERN INSIDE EXAM JSON
        # ====================================================

        exam_data["exam_pattern"] = {

            "pattern_id":
                pattern_id,

            "pattern_name":
                pattern_name,

            "question_distribution": {

                "One Word / 1 Mark":
                    one_word,

                "Short Answer":
                    short_answer,

                "Descriptive Answer":
                    descriptive
            },

            "marks_per_question": {

                "One Word / 1 Mark":
                    one_word_marks,

                "Short Answer":
                    short_answer_marks,

                "Descriptive Answer":
                    descriptive_marks
            },

            "question_type_total_marks": {

                "One Word / 1 Mark":
                    one_word_total,

                "Short Answer":
                    short_answer_total,

                "Descriptive Answer":
                    descriptive_total
            },

            "total_questions":
                total_questions,

            "total_marks":
                total_marks,

            "updated_at":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
        }


        # ====================================================
        # BACKWARD COMPATIBILITY
        # ====================================================

        exam_data["pattern_id"] = (
            pattern_id
        )

        exam_data["pattern_name"] = (
            pattern_name
        )

        exam_data["pattern_total_questions"] = (
            total_questions
        )

        exam_data["pattern_total_marks"] = (
            total_marks
        )

        exam_data["updated_at"] = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )


        # ====================================================
        # SAVE UPDATED EXAM JSON
        # ====================================================

        try:

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    exam_data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

        except Exception as e:

            messagebox.showerror(
                "Exam Save Error",
                (
                    "The separate pattern file was created, "
                    "but the exam file could not be updated.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ====================================================
        # SUCCESS
        # ====================================================

        messagebox.showinfo(
            "Pattern Saved",
            (
                "Exam pattern saved successfully.\n\n"
                f"Pattern ID: {pattern_id}\n"
                f"Pattern Name: {pattern_name}\n\n"
                f"Exam ID: {exam_id}\n"
                f"Total Questions: {total_questions}\n"
                f"Total Marks: "
                f"{self.format_number(total_marks)}\n\n"
                "Pattern file saved in:\n"
                "backend/exam_patterns/"
            ),
            parent=self.root
        )


    # ========================================================
    # CLEAR PATTERN
    # ========================================================

    def clear_pattern(self):

        self.set_entry_value(
            self.one_word_entry,
            0
        )

        self.set_entry_value(
            self.short_answer_entry,
            0
        )

        self.set_entry_value(
            self.descriptive_entry,
            0
        )


        self.set_entry_value(
            self.one_word_marks_entry,
            1
        )

        self.set_entry_value(
            self.short_answer_marks_entry,
            2
        )

        self.set_entry_value(
            self.descriptive_marks_entry,
            5
        )


        self.update_totals()


    # ========================================================
    # BACK
    # ========================================================

    def back(self):

        answer = messagebox.askyesno(
            "Back",
            (
                "Do you want to return "
                "to the previous page?"
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
                "Could not close Exam Pattern:",
                e
            )


        if parent is not None:

            restore_window(
                parent
            )


# ============================================================
# OPEN EXAM PATTERN
# ============================================================

def open_exam_pattern(
    parent_window=None
):

    window = tk.Toplevel(
        parent_window
    )


    maximize_window(
        window
    )


    ExamPattern(
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


    open_exam_pattern(
        parent_window=root
    )


    root.mainloop()
