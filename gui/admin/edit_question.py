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

os.makedirs(
    EXAMS_DIR,
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
# EDIT QUESTION
# ============================================================

class EditQuestion:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        self.parent_window = parent_window

        self.exam_data = None

        self.current_file_path = None

        self.original_question_no = None


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Edit Question - AI Oral Examination System"
        )

        self.root.geometry(
            "1150x850"
        )

        self.root.minsize(
            950,
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

        self.load_exams()


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
            text="EDIT QUESTION",
            font=("Arial", 27, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(18, 3)
        )


        tk.Label(
            header_frame,
            text=(
                "Select an examination and edit an existing question"
            ),
            font=("Arial", 11),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack()


        # ====================================================
        # EXAM SELECTION
        # ====================================================

        exam_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        exam_frame.pack(
            fill="x",
            padx=55,
            pady=(18, 8)
        )


        tk.Label(
            exam_frame,
            text="Select Exam:",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#374151"
        ).pack(
            side="left",
            padx=(0, 10)
        )


        self.exam_combo = ttk.Combobox(
            exam_frame,
            width=50,
            state="readonly"
        )

        self.exam_combo.pack(
            side="left",
            padx=(0, 10)
        )


        self.exam_combo.bind(
            "<<ComboboxSelected>>",
            self.exam_selected
        )


        tk.Button(
            exam_frame,
            text="LOAD QUESTIONS",
            font=("Arial", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.load_selected_exam
        ).pack(
            side="left",
            padx=8
        )


        # ====================================================
        # QUESTION SELECTION
        # ====================================================

        selection_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        selection_frame.pack(
            fill="x",
            padx=55,
            pady=(5, 10)
        )


        tk.Label(
            selection_frame,
            text="Select Question:",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#374151"
        ).pack(
            side="left",
            padx=(0, 10)
        )


        self.question_combo = ttk.Combobox(
            selection_frame,
            width=70,
            state="readonly"
        )

        self.question_combo.pack(
            side="left"
        )


        self.question_combo.bind(
            "<<ComboboxSelected>>",
            self.question_selected
        )


        # ====================================================
        # FORM OUTER FRAME
        # ====================================================

        form_outer = tk.Frame(
            main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        form_outer.pack(
            fill="both",
            expand=True,
            padx=55,
            pady=(0, 10)
        )


        # ====================================================
        # CANVAS
        # ====================================================

        self.canvas = tk.Canvas(
            form_outer,
            bg="white",
            highlightthickness=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ====================================================
        # VERTICAL SCROLLBAR
        # ====================================================

        scrollbar = ttk.Scrollbar(
            form_outer,
            orient="vertical",
            command=self.canvas.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )


        # ====================================================
        # INNER FORM
        # ====================================================

        self.form_frame = tk.Frame(
            self.canvas,
            bg="white"
        )


        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.form_frame,
            anchor="nw"
        )


        self.form_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )


        self.canvas.bind(
            "<Configure>",
            self.resize_form
        )


        # ====================================================
        # FORM CONTENT
        # ====================================================

        self.create_form_fields()


        # ====================================================
        # BUTTONS
        # ====================================================

        button_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            pady=(0, 15)
        )


        tk.Button(
            button_frame,
            text="SAVE CHANGES",
            font=("Arial", 12, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.save_question
        ).grid(
            row=0,
            column=0,
            padx=8
        )


        tk.Button(
            button_frame,
            text="CLEAR",
            font=("Arial", 12, "bold"),
            bg="#f59e0b",
            fg="white",
            activebackground="#d97706",
            activeforeground="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.clear_form
        ).grid(
            row=0,
            column=1,
            padx=8
        )


        tk.Button(
            button_frame,
            text="BACK",
            font=("Arial", 12, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        ).grid(
            row=0,
            column=2,
            padx=8
        )


    # ========================================================
    # FORM FIELDS
    # ========================================================

    def create_form_fields(self):

        # ----------------------------------------------------
        # CONFIGURE COLUMNS
        # ----------------------------------------------------

        self.form_frame.columnconfigure(
            1,
            weight=1
        )


        # ====================================================
        # QUESTION NUMBER
        # ====================================================

        tk.Label(
            self.form_frame,
            text="Question Number",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=30,
            pady=10
        )


        self.question_number_entry = ttk.Entry(
            self.form_frame,
            width=55
        )

        self.question_number_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=20,
            pady=10
        )


        # ====================================================
        # QUESTION TYPE
        # ====================================================

        tk.Label(
            self.form_frame,
            text="Question Type",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=30,
            pady=10
        )


        self.question_type_combo = ttk.Combobox(
            self.form_frame,
            width=52,
            state="readonly",
            values=[
                "One Word / 1 Mark",
                "Short Answer",
                "Descriptive Answer"
            ]
        )

        self.question_type_combo.grid(
            row=1,
            column=1,
            sticky="w",
            padx=20,
            pady=10
        )


        # ====================================================
        # MARKS
        # ====================================================

        tk.Label(
            self.form_frame,
            text="Marks",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=30,
            pady=10
        )


        self.marks_entry = ttk.Entry(
            self.form_frame,
            width=55
        )

        self.marks_entry.grid(
            row=2,
            column=1,
            sticky="w",
            padx=20,
            pady=10
        )


        self.marks_entry.bind(
            "<KeyRelease>",
            self.marks_changed
        )


        # ====================================================
        # ANSWER TIME
        # ====================================================

        tk.Label(
            self.form_frame,
            text="Answer Time (seconds)",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=30,
            pady=10
        )


        self.answer_time_entry = ttk.Entry(
            self.form_frame,
            width=55
        )

        self.answer_time_entry.grid(
            row=3,
            column=1,
            sticky="w",
            padx=20,
            pady=10
        )


        tk.Label(
            self.form_frame,
            text=(
                "Suggested time: Marks × 10 seconds. "
                "You can manually change this value."
            ),
            font=("Arial", 9),
            bg="white",
            fg="#6b7280"
        ).grid(
            row=4,
            column=1,
            sticky="w",
            padx=20,
            pady=(0, 8)
        )


        # ====================================================
        # QUESTION
        # ====================================================

        tk.Label(
            self.form_frame,
            text="Question",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=5,
            column=0,
            sticky="nw",
            padx=30,
            pady=10
        )


        self.question_text = tk.Text(
            self.form_frame,
            width=55,
            height=5,
            font=("Arial", 11),
            bd=1,
            relief="solid",
            wrap="word"
        )

        self.question_text.grid(
            row=5,
            column=1,
            sticky="ew",
            padx=20,
            pady=10
        )


        # ====================================================
        # EXPECTED ANSWER
        # ====================================================

        tk.Label(
            self.form_frame,
            text="Expected Answer",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=6,
            column=0,
            sticky="nw",
            padx=30,
            pady=10
        )


        self.expected_answer_text = tk.Text(
            self.form_frame,
            width=55,
            height=6,
            font=("Arial", 11),
            bd=1,
            relief="solid",
            wrap="word"
        )

        self.expected_answer_text.grid(
            row=6,
            column=1,
            sticky="ew",
            padx=20,
            pady=10
        )


        # ====================================================
        # DIFFICULTY
        # ====================================================

        tk.Label(
            self.form_frame,
            text="Difficulty (Optional)",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=7,
            column=0,
            sticky="w",
            padx=30,
            pady=10
        )


        self.difficulty_combo = ttk.Combobox(
            self.form_frame,
            width=52,
            state="readonly",
            values=[
                "",
                "Easy",
                "Medium",
                "Hard"
            ]
        )

        self.difficulty_combo.grid(
            row=7,
            column=1,
            sticky="w",
            padx=20,
            pady=10
        )


        # ====================================================
        # TOPIC
        # ====================================================

        tk.Label(
            self.form_frame,
            text="Topic (Optional)",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=8,
            column=0,
            sticky="w",
            padx=30,
            pady=10
        )


        self.topic_entry = ttk.Entry(
            self.form_frame,
            width=55
        )

        self.topic_entry.grid(
            row=8,
            column=1,
            sticky="ew",
            padx=20,
            pady=10
        )


        # ====================================================
        # KEYWORDS
        # ====================================================

        tk.Label(
            self.form_frame,
            text="Keywords (Optional)",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=9,
            column=0,
            sticky="nw",
            padx=30,
            pady=10
        )


        self.keywords_text = tk.Text(
            self.form_frame,
            width=55,
            height=3,
            font=("Arial", 11),
            bd=1,
            relief="solid",
            wrap="word"
        )

        self.keywords_text.grid(
            row=9,
            column=1,
            sticky="ew",
            padx=20,
            pady=10
        )


        tk.Label(
            self.form_frame,
            text=(
                "Enter multiple keywords separated by commas."
            ),
            font=("Arial", 9),
            bg="white",
            fg="#6b7280"
        ).grid(
            row=10,
            column=1,
            sticky="w",
            padx=20,
            pady=(0, 8)
        )


        # ====================================================
        # STATUS
        # ====================================================

        tk.Label(
            self.form_frame,
            text="Status",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=11,
            column=0,
            sticky="w",
            padx=30,
            pady=10
        )


        self.status_combo = ttk.Combobox(
            self.form_frame,
            width=52,
            state="readonly",
            values=[
                "Active",
                "Inactive"
            ]
        )

        self.status_combo.grid(
            row=11,
            column=1,
            sticky="w",
            padx=20,
            pady=10
        )


        self.status_combo.set(
            "Active"
        )


        # ====================================================
        # NOTE
        # ====================================================

        note_frame = tk.Frame(
            self.form_frame,
            bg="#f9fafb",
            bd=1,
            relief="solid"
        )

        note_frame.grid(
            row=12,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=30,
            pady=20
        )


        tk.Label(
            note_frame,
            text=(
                "Difficulty, Topic and Keywords are optional. "
                "Status is required and defaults to Active. "
                "Answer Time is stored separately for each question."
            ),
            font=("Arial", 10),
            bg="#f9fafb",
            fg="#6b7280",
            wraplength=900,
            justify="left"
        ).pack(
            padx=15,
            pady=12
        )


    # ========================================================
    # SCROLL REGION
    # ========================================================

    def update_scroll_region(
        self,
        event=None
    ):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )


    # ========================================================
    # RESIZE FORM
    # ========================================================

    def resize_form(
        self,
        event
    ):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )


    # ========================================================
    # MOUSE WHEEL
    # ========================================================

    def mouse_wheel(
        self,
        event
    ):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )


    # ========================================================
    # LOAD EXAMS
    # ========================================================

    def load_exams(self):

        exam_list = []


        if not os.path.exists(
            EXAMS_DIR
        ):

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

            if not filename.lower().endswith(
                ".json"
            ):

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


                exam_id = exam_data.get(
                    "exam_id",
                    ""
                )


                exam_name = exam_data.get(
                    "exam_name",
                    ""
                )


                if exam_id:

                    exam_list.append(
                        f"{exam_id} - {exam_name}"
                    )


            except Exception:

                continue


        exam_list.sort()

        self.exam_combo["values"] = exam_list


        if exam_list:

            self.exam_combo.current(
                0
            )

            self.load_selected_exam()

        else:

            messagebox.showwarning(
                "No Exams",
                (
                    "No exams have been created yet.\n\n"
                    "Please create an exam first."
                ),
                parent=self.root
            )


    # ========================================================
    # GET EXAM ID
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
    # LOAD SELECTED EXAM
    # ========================================================

    def load_selected_exam(self):

        exam_id = self.get_selected_exam_id()


        if not exam_id:

            return


        file_path = os.path.join(
            EXAMS_DIR,
            f"{exam_id}.json"
        )


        if not os.path.exists(
            file_path
        ):

            messagebox.showerror(
                "Exam Not Found",
                (
                    f"Exam file for {exam_id} "
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
                "The exam file contains invalid data.",
                parent=self.root
            )

            return


        self.exam_data = exam_data

        self.current_file_path = file_path


        questions = exam_data.get(
            "questions",
            []
        )


        if not isinstance(
            questions,
            list
        ):

            questions = []


        self.populate_question_combo(
            questions
        )


    # ========================================================
    # POPULATE QUESTION COMBO
    # ========================================================

    def populate_question_combo(
        self,
        questions
    ):

        self.question_combo["values"] = []


        question_values = []


        valid_questions = []


        def sort_key(
            question
        ):

            try:

                return int(
                    question.get(
                        "question_no",
                        0
                    )
                )

            except Exception:

                return 0


        questions = sorted(
            questions,
            key=sort_key
        )


        for question in questions:

            if not isinstance(
                question,
                dict
            ):

                continue


            question_no = question.get(
                "question_no",
                ""
            )


            question_text = question.get(
                "question",
                ""
            )


            display_question = str(
                question_text
            ).replace(
                "\n",
                " "
            )


            if len(display_question) > 75:

                display_question = (
                    display_question[:75]
                    + "..."
                )


            display_value = (
                f"Question {question_no}: "
                f"{display_question}"
            )


            question_values.append(
                display_value
            )


            valid_questions.append(
                question
            )


        self.question_combo["values"] = (
            question_values
        )


        self.questions_for_combo = (
            valid_questions
        )


        if question_values:

            self.question_combo.current(
                0
            )

            self.load_question_into_form(
                valid_questions[0]
            )

        else:

            self.clear_form()


    # ========================================================
    # QUESTION SELECTED
    # ========================================================

    def question_selected(
        self,
        event=None
    ):

        index = self.question_combo.current()


        if index < 0:

            return


        if index >= len(
            self.questions_for_combo
        ):

            return


        question = (
            self.questions_for_combo[index]
        )


        self.load_question_into_form(
            question
        )


    # ========================================================
    # LOAD QUESTION INTO FORM
    # ========================================================

    def load_question_into_form(
        self,
        question
    ):

        if not isinstance(
            question,
            dict
        ):

            return


        self.original_question_no = question.get(
            "question_no"
        )


        # ----------------------------------------------------
        # QUESTION NUMBER
        # ----------------------------------------------------

        self.question_number_entry.delete(
            0,
            tk.END
        )

        self.question_number_entry.insert(
            0,
            str(
                question.get(
                    "question_no",
                    ""
                )
            )
        )


        # ----------------------------------------------------
        # QUESTION TYPE
        # ----------------------------------------------------

        question_type = question.get(
            "question_type",
            "One Word / 1 Mark"
        )


        self.question_type_combo.set(
            question_type
        )


        # ----------------------------------------------------
        # MARKS
        # ----------------------------------------------------

        marks = question.get(
            "marks",
            1
        )


        self.marks_entry.delete(
            0,
            tk.END
        )

        self.marks_entry.insert(
            0,
            str(marks)
        )


        # ----------------------------------------------------
        # ANSWER TIME
        # ----------------------------------------------------

        answer_time = question.get(
            "answer_time_seconds",
            None
        )


        if answer_time is None:

            try:

                answer_time = int(
                    float(marks) * 10
                )

            except Exception:

                answer_time = 10


        self.answer_time_entry.delete(
            0,
            tk.END
        )

        self.answer_time_entry.insert(
            0,
            str(answer_time)
        )


        # ----------------------------------------------------
        # QUESTION
        # ----------------------------------------------------

        self.question_text.delete(
            "1.0",
            tk.END
        )

        self.question_text.insert(
            "1.0",
            str(
                question.get(
                    "question",
                    ""
                )
            )
        )


        # ----------------------------------------------------
        # EXPECTED ANSWER
        # ----------------------------------------------------

        self.expected_answer_text.delete(
            "1.0",
            tk.END
        )

        self.expected_answer_text.insert(
            "1.0",
            str(
                question.get(
                    "expected_answer",
                    ""
                )
            )
        )


        # ----------------------------------------------------
        # DIFFICULTY
        # ----------------------------------------------------

        difficulty = question.get(
            "difficulty",
            ""
        )


        if difficulty not in (
            "",
            "Easy",
            "Medium",
            "Hard"
        ):

            difficulty = ""


        self.difficulty_combo.set(
            difficulty
        )


        # ----------------------------------------------------
        # TOPIC
        # ----------------------------------------------------

        topic = question.get(
            "topic",
            ""
        )


        self.topic_entry.delete(
            0,
            tk.END
        )

        self.topic_entry.insert(
            0,
            str(topic)
        )


        # ----------------------------------------------------
        # KEYWORDS
        # ----------------------------------------------------

        keywords = question.get(
            "keywords",
            []
        )


        if isinstance(
            keywords,
            list
        ):

            keywords_text = ", ".join(
                str(keyword)
                for keyword in keywords
            )

        else:

            keywords_text = str(
                keywords
            )


        self.keywords_text.delete(
            "1.0",
            tk.END
        )

        self.keywords_text.insert(
            "1.0",
            keywords_text
        )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        status = question.get(
            "status",
            "Active"
        )


        if status not in (
            "Active",
            "Inactive"
        ):

            status = "Active"


        self.status_combo.set(
            status
        )


        # ----------------------------------------------------
        # SCROLL TO TOP
        # ----------------------------------------------------

        self.canvas.yview_moveto(
            0
        )


    # ========================================================
    # MARKS CHANGED
    # ========================================================

    def marks_changed(
        self,
        event=None
    ):

        marks_text = (
            self.marks_entry
            .get()
            .strip()
        )


        if not marks_text:

            return


        try:

            marks = float(
                marks_text
            )


            if marks <= 0:

                return


            suggested_time = int(
                marks * 10
            )


            # ------------------------------------------------
            # Only automatically update if the current answer
            # time appears to be the old calculated value.
            # ------------------------------------------------

            current_time_text = (
                self.answer_time_entry
                .get()
                .strip()
            )


            if not current_time_text:

                self.answer_time_entry.insert(
                    0,
                    str(suggested_time)
                )

                return


            try:

                current_time = int(
                    current_time_text
                )

            except ValueError:

                current_time = None


            old_marks = None


            if self.exam_data is not None:

                old_marks = None


            # ------------------------------------------------
            # Do not overwrite a manually entered answer time.
            #
            # If the current time is equal to the previous
            # marks-based suggestion, update it.
            # ------------------------------------------------

            if current_time is not None:

                if self.original_question_no is not None:

                    original_question = (
                        self.find_original_question()
                    )


                    if original_question is not None:

                        original_marks = original_question.get(
                            "marks",
                            1
                        )


                        try:

                            original_suggested = int(
                                float(original_marks) * 10
                            )

                        except Exception:

                            original_suggested = None


                        original_answer_time = (
                            original_question.get(
                                "answer_time_seconds",
                                None
                            )
                        )


                        if original_answer_time is None:

                            original_answer_time = (
                                original_suggested
                            )


                        if (
                            current_time
                            ==
                            original_answer_time
                        ):

                            self.answer_time_entry.delete(
                                0,
                                tk.END
                            )

                            self.answer_time_entry.insert(
                                0,
                                str(suggested_time)
                            )

        except Exception:

            pass


    # ========================================================
    # FIND ORIGINAL QUESTION
    # ========================================================

    def find_original_question(self):

        if self.exam_data is None:

            return None


        questions = self.exam_data.get(
            "questions",
            []
        )


        if not isinstance(
            questions,
            list
        ):

            return None


        for question in questions:

            if not isinstance(
                question,
                dict
            ):

                continue


            if (
                str(
                    question.get(
                        "question_no"
                    )
                )
                ==
                str(
                    self.original_question_no
                )
            ):

                return question


        return None


    # ========================================================
    # VALIDATE FORM
    # ========================================================

    def validate_form(self):

        # ----------------------------------------------------
        # EXAM
        # ----------------------------------------------------

        exam_id = self.get_selected_exam_id()


        if not exam_id:

            messagebox.showwarning(
                "Missing Exam",
                "Please select an exam.",
                parent=self.root
            )

            return None


        # ----------------------------------------------------
        # QUESTION NUMBER
        # ----------------------------------------------------

        question_number_text = (
            self.question_number_entry
            .get()
            .strip()
        )


        try:

            question_number = int(
                question_number_text
            )


            if question_number <= 0:

                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Question Number",
                (
                    "Question Number must be "
                    "a positive whole number."
                ),
                parent=self.root
            )

            self.question_number_entry.focus_set()

            return None


        # ----------------------------------------------------
        # QUESTION TYPE
        # ----------------------------------------------------

        question_type = (
            self.question_type_combo
            .get()
            .strip()
        )


        if question_type not in (
            "One Word / 1 Mark",
            "Short Answer",
            "Descriptive Answer"
        ):

            messagebox.showwarning(
                "Question Type",
                "Please select a Question Type.",
                parent=self.root
            )

            return None


        # ----------------------------------------------------
        # MARKS
        # ----------------------------------------------------

        marks_text = (
            self.marks_entry
            .get()
            .strip()
        )


        try:

            marks = float(
                marks_text
            )


            if marks <= 0:

                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Marks",
                (
                    "Marks must be a "
                    "positive number."
                ),
                parent=self.root
            )

            self.marks_entry.focus_set()

            return None


        # ----------------------------------------------------
        # ANSWER TIME
        # ----------------------------------------------------

        answer_time_text = (
            self.answer_time_entry
            .get()
            .strip()
        )


        try:

            answer_time = int(
                answer_time_text
            )


            if answer_time <= 0:

                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Invalid Answer Time",
                (
                    "Answer Time must be a "
                    "positive whole number of seconds."
                ),
                parent=self.root
            )

            self.answer_time_entry.focus_set()

            return None


        # ----------------------------------------------------
        # QUESTION
        # ----------------------------------------------------

        question = (
            self.question_text
            .get(
                "1.0",
                tk.END
            )
            .strip()
        )


        if not question:

            messagebox.showwarning(
                "Missing Question",
                "Please enter the question.",
                parent=self.root
            )

            self.question_text.focus_set()

            return None


        # ----------------------------------------------------
        # EXPECTED ANSWER
        # ----------------------------------------------------

        expected_answer = (
            self.expected_answer_text
            .get(
                "1.0",
                tk.END
            )
            .strip()
        )


        if not expected_answer:

            messagebox.showwarning(
                "Missing Expected Answer",
                "Please enter the expected answer.",
                parent=self.root
            )

            self.expected_answer_text.focus_set()

            return None


        # ----------------------------------------------------
        # DIFFICULTY
        # ----------------------------------------------------

        difficulty = (
            self.difficulty_combo
            .get()
            .strip()
        )


        # ----------------------------------------------------
        # TOPIC
        # ----------------------------------------------------

        topic = (
            self.topic_entry
            .get()
            .strip()
        )


        # ----------------------------------------------------
        # KEYWORDS
        # ----------------------------------------------------

        keywords_text = (
            self.keywords_text
            .get(
                "1.0",
                tk.END
            )
            .strip()
        )


        keywords = []


        if keywords_text:

            for keyword in keywords_text.split(","):

                keyword = keyword.strip()


                if keyword:

                    keywords.append(
                        keyword
                    )


        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        status = (
            self.status_combo
            .get()
            .strip()
        )


        if status not in (
            "Active",
            "Inactive"
        ):

            status = "Active"


        # ----------------------------------------------------
        # RETURN DATA
        # ----------------------------------------------------

        return {

            "question_no": question_number,

            "question_type": question_type,

            "question": question,

            "expected_answer": expected_answer,

            "keywords": keywords,

            "marks": marks,

            "answer_time_seconds": answer_time,

            "difficulty": difficulty,

            "topic": topic,

            "status": status
        }


    # ========================================================
    # SAVE QUESTION
    # ========================================================

    def save_question(self):

        question_data = self.validate_form()


        if question_data is None:

            return


        if self.exam_data is None:

            messagebox.showerror(
                "No Exam",
                "Please select an exam first.",
                parent=self.root
            )

            return


        questions = self.exam_data.get(
            "questions",
            []
        )


        if not isinstance(
            questions,
            list
        ):

            messagebox.showerror(
                "Question Error",
                "Invalid questions data.",
                parent=self.root
            )

            return


        # ====================================================
        # FIND QUESTION BEING EDITED
        # ====================================================

        target_question = None


        for question in questions:

            if not isinstance(
                question,
                dict
            ):

                continue


            if (
                str(
                    question.get(
                        "question_no"
                    )
                )
                ==
                str(
                    self.original_question_no
                )
            ):

                target_question = question

                break


        if target_question is None:

            messagebox.showerror(
                "Question Not Found",
                "The selected question could not be found.",
                parent=self.root
            )

            return


        # ====================================================
        # DUPLICATE QUESTION NUMBER
        # ====================================================

        for question in questions:

            if question is target_question:

                continue


            if not isinstance(
                question,
                dict
            ):

                continue


            existing_number = question.get(
                "question_no"
            )


            try:

                existing_number = int(
                    existing_number
                )

            except Exception:

                continue


            if (
                existing_number
                ==
                question_data["question_no"]
            ):

                messagebox.showerror(
                    "Duplicate Question Number",
                    (
                        f"Question number "
                        f"{question_data['question_no']} "
                        "already exists in this exam."
                    ),
                    parent=self.root
                )

                return


        # ====================================================
        # PRESERVE CREATED DATE
        # ====================================================

        created_at = target_question.get(
            "created_at",
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )


        # ====================================================
        # UPDATE QUESTION
        # ====================================================

        target_question.clear()


        target_question.update(
            question_data
        )


        target_question[
            "created_at"
        ] = created_at


        target_question[
            "updated_at"
        ] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        # ====================================================
        # UPDATE EXAM SUMMARY
        # ====================================================

        self.exam_data[
            "total_questions"
        ] = len(
            questions
        )


        total_marks = 0


        for question in questions:

            if not isinstance(
                question,
                dict
            ):

                continue


            try:

                total_marks += float(
                    question.get(
                        "marks",
                        0
                    )
                )

            except Exception:

                pass


        self.exam_data[
            "total_marks"
        ] = total_marks


        self.exam_data[
            "updated_at"
        ] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        # ====================================================
        # SAVE JSON
        # ====================================================

        try:

            with open(
                self.current_file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.exam_data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )


        except Exception as e:

            messagebox.showerror(
                "Save Error",
                (
                    "Could not save the question.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ====================================================
        # SUCCESS
        # ====================================================

        messagebox.showinfo(
            "Question Updated",
            (
                "Question updated successfully.\n\n"
                f"Exam: {self.get_selected_exam_id()}\n"
                f"Question No.: "
                f"{question_data['question_no']}\n"
                f"Marks: {question_data['marks']}\n"
                f"Answer Time: "
                f"{question_data['answer_time_seconds']} seconds"
            ),
            parent=self.root
        )


        # ====================================================
        # RELOAD QUESTIONS
        # ====================================================

        self.load_selected_exam()


        # ====================================================
        # SELECT UPDATED QUESTION
        # ====================================================

        for index, question in enumerate(
            self.questions_for_combo
        ):

            if (
                str(
                    question.get(
                        "question_no"
                    )
                )
                ==
                str(
                    question_data["question_no"]
                )
            ):

                self.question_combo.current(
                    index
                )

                self.load_question_into_form(
                    question
                )

                break


    # ========================================================
    # CLEAR FORM
    # ========================================================

    def clear_form(self):

        self.question_number_entry.delete(
            0,
            tk.END
        )


        self.question_type_combo.set(
            "One Word / 1 Mark"
        )


        self.marks_entry.delete(
            0,
            tk.END
        )

        self.marks_entry.insert(
            0,
            "1"
        )


        self.answer_time_entry.delete(
            0,
            tk.END
        )

        self.answer_time_entry.insert(
            0,
            "10"
        )


        self.question_text.delete(
            "1.0",
            tk.END
        )


        self.expected_answer_text.delete(
            "1.0",
            tk.END
        )


        self.difficulty_combo.set(
            ""
        )


        self.topic_entry.delete(
            0,
            tk.END
        )


        self.keywords_text.delete(
            "1.0",
            tk.END
        )


        self.status_combo.set(
            "Active"
        )


        self.canvas.yview_moveto(
            0
        )


    # ========================================================
    # BACK
    # ========================================================

    def back(self):

        answer = messagebox.askyesno(
            "Back",
            (
                "Do you want to return to "
                "Question Management?"
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
                    "Question Management:"
                )

                print(e)


# ============================================================
# OPEN EDIT QUESTION
# ============================================================

def open_edit_question(
    parent_window=None
):

    window = tk.Toplevel(
        parent_window
    )


    maximize_window(
        window
    )


    EditQuestion(
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


    open_edit_question(
        parent_window=root
    )


    root.mainloop()
