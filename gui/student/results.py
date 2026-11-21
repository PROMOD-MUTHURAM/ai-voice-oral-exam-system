import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re
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


STUDENT_ANSWERS_DIR = os.path.join(
    BACKEND_DIR,
    "student_answers"
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

    except Exception as e:

        print(
            "Could not maximize window:",
            e
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
# SAFE FILE NAME
# ============================================================

def safe_file_name(name):

    name = str(
        name
    ).strip()

    name = re.sub(
        r'[<>:"/\\|?*]',
        "_",
        name
    )

    name = re.sub(
        r"\s+",
        "_",
        name
    )

    return name


# ============================================================
# LOAD CURRENT STUDENT
# ============================================================

def load_current_student():

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

            return json.load(
                file
            )

    except Exception as e:

        print(
            "Could not load current student:",
            e
        )

        return None


# ============================================================
# SEMANTIC SIMILARITY
# ============================================================

class AnswerEvaluator:

    def __init__(self):

        self.model = None


    def load_model(self):

        if self.model is not None:

            return True

        try:

            from sentence_transformers import (
                SentenceTransformer
            )

            print(
                "Loading semantic similarity model..."
            )

            self.model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

            print(
                "Semantic similarity model loaded."
            )

            return True

        except Exception as e:

            print(
                "Could not load similarity model:"
            )

            print(e)

            return False


    def similarity(
        self,
        expected_answer,
        student_answer
    ):

        if expected_answer is None:
            expected_answer = ""

        if student_answer is None:
            student_answer = ""

        expected_answer = str(
            expected_answer
        ).strip().lower()

        student_answer = str(
            student_answer
        ).strip().lower()


        # ----------------------------------------------------
        # Empty answer
        # ----------------------------------------------------

        if not student_answer:

            return 0.0


        if not expected_answer:

            return 0.0


        # ----------------------------------------------------
        # Exact match
        # ----------------------------------------------------

        if (
            expected_answer
            ==
            student_answer
        ):

            return 100.0


        # ----------------------------------------------------
        # Load model
        # ----------------------------------------------------

        if not self.load_model():

            return 0.0


        try:

            from sentence_transformers.util import (
                cos_sim
            )

            embeddings = self.model.encode(
                [
                    expected_answer,
                    student_answer
                ],
                convert_to_tensor=True
            )


            score = cos_sim(
                embeddings[0],
                embeddings[1]
            ).item()


            score = max(
                0.0,
                min(
                    1.0,
                    score
                )
            )


            return round(
                score * 100,
                2
            )


        except Exception as e:

            print(
                "Similarity calculation error:"
            )

            print(e)

            return 0.0


# ============================================================
# MARK CALCULATION
# ============================================================

def calculate_marks(
    similarity,
    allotted_marks
):

    try:

        allotted_marks = float(
            allotted_marks
        )

    except Exception:

        allotted_marks = 0.0


    try:

        similarity = float(
            similarity
        )

    except Exception:

        similarity = 0.0


    # ========================================================
    # 1 MARK QUESTION
    # ========================================================

    if allotted_marks == 1:

        if similarity >= 75:

            return (
                1.0,
                "Correct"
            )

        else:

            return (
                0.0,
                "Wrong"
            )


    # ========================================================
    # MORE THAN 1 MARK
    # ========================================================

    if similarity >= 75:

        return (
            allotted_marks,
            "Correct"
        )


    elif similarity >= 50:

        return (
            allotted_marks * 0.50,
            "Partially Correct"
        )


    elif similarity >= 35:

        return (
            allotted_marks * 0.25,
            "Partially Correct"
        )


    else:

        return (
            0.0,
            "Wrong"
        )


# ============================================================
# JSON SAFE
# ============================================================

def make_json_safe(value):

    if isinstance(
        value,
        datetime
    ):

        return value.isoformat()


    if isinstance(
        value,
        dict
    ):

        return {
            str(key): make_json_safe(
                val
            )
            for key, val in value.items()
        }


    if isinstance(
        value,
        list
    ):

        return [
            make_json_safe(
                item
            )
            for item in value
        ]


    if isinstance(
        value,
        tuple
    ):

        return [
            make_json_safe(
                item
            )
            for item in value
        ]


    return value


# ============================================================
# RESULTS WINDOW
# ============================================================

class StudentResults:

    def __init__(
        self,
        root,
        student_id,
        parent_window=None,
        login_window=None
    ):

        self.root = root

        self.student_id = (
            str(student_id)
        )

        self.parent_window = (
            parent_window
        )

        self.login_window = (
            login_window
        )

        self.current_student = (
            load_current_student()
        )

        self.attempts = []

        self.current_result = None

        # IMPORTANT:
        # AnswerEvaluator is defined in THIS FILE.
        # There is no answer_evaluator module import.
        self.evaluator = AnswerEvaluator()


        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.root.title(
            "Student Results - AI Oral Exam System"
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


        # ----------------------------------------------------
        # GUI
        # ----------------------------------------------------

        self.create_interface()


        # ----------------------------------------------------
        # LOAD RESULTS
        # ----------------------------------------------------

        self.load_results()


        # ----------------------------------------------------
        # CLOSE
        # ----------------------------------------------------

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.back_to_details
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
        # HEADER
        # ====================================================

        header = tk.Frame(
            main_frame,
            bg="#1f2937",
            height=85
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )


        tk.Label(
            header,
            text="STUDENT RESULTS",
            font=("Arial", 22, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            side="left",
            padx=25
        )


        self.student_label = tk.Label(
            header,
            text="Student",
            font=("Arial", 11, "bold"),
            bg="#1f2937",
            fg="#d1d5db"
        )

        self.student_label.pack(
            side="right",
            padx=25
        )


        # ====================================================
        # ATTEMPT SELECTOR
        # ====================================================

        top_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        top_frame.pack(
            fill="x",
            padx=30,
            pady=20
        )


        tk.Label(
            top_frame,
            text="Select Attempt:",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#374151"
        ).pack(
            side="left"
        )


        self.attempt_combo = ttk.Combobox(
            top_frame,
            state="readonly",
            width=55
        )

        self.attempt_combo.pack(
            side="left",
            padx=15
        )


        self.attempt_combo.bind(
            "<<ComboboxSelected>>",
            self.attempt_selected
        )


        # ====================================================
        # SUMMARY
        # ====================================================

        self.summary_frame = tk.Frame(
            main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        self.summary_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )


        self.summary_label = tk.Label(
            self.summary_frame,
            text="No result selected.",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#111827",
            justify="left"
        )

        self.summary_label.pack(
            anchor="w",
            padx=20,
            pady=15
        )


        # ====================================================
        # TABLE FRAME
        # ====================================================

        table_frame = tk.Frame(
            main_frame,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )


        columns = (
            "question_no",
            "question",
            "original_answer",
            "student_answer",
            "similarity",
            "evaluation",
            "allotted",
            "awarded"
        )


        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )


        self.tree.heading(
            "question_no",
            text="Q.No"
        )

        self.tree.heading(
            "question",
            text="Question"
        )

        self.tree.heading(
            "original_answer",
            text="Original Answer"
        )

        self.tree.heading(
            "student_answer",
            text="Student Answer"
        )

        self.tree.heading(
            "similarity",
            text="Similarity"
        )

        self.tree.heading(
            "evaluation",
            text="Evaluation"
        )

        self.tree.heading(
            "allotted",
            text="Allotted Marks"
        )

        self.tree.heading(
            "awarded",
            text="Awarded Marks"
        )


        self.tree.column(
            "question_no",
            width=60,
            anchor="center"
        )

        self.tree.column(
            "question",
            width=230
        )

        self.tree.column(
            "original_answer",
            width=300
        )

        self.tree.column(
            "student_answer",
            width=300
        )

        self.tree.column(
            "similarity",
            width=90,
            anchor="center"
        )

        self.tree.column(
            "evaluation",
            width=130,
            anchor="center"
        )

        self.tree.column(
            "allotted",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "awarded",
            width=100,
            anchor="center"
        )


        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )


        horizontal_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )


        self.tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )


        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )


        vertical_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )


        horizontal_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )


        table_frame.rowconfigure(
            0,
            weight=1
        )

        table_frame.columnconfigure(
            0,
            weight=1
        )


        # ====================================================
        # BUTTONS
        # ====================================================

        button_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            fill="x",
            padx=30,
            pady=20
        )


        self.download_button = tk.Button(
            button_frame,
            text="DOWNLOAD ANSWER SCRIPT",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=25,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.download_answer_script
        )

        self.download_button.pack(
            side="left",
            padx=5
        )


        self.back_button = tk.Button(
            button_frame,
            text="BACK TO STUDENT DETAILS",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=25,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back_to_details
        )

        self.back_button.pack(
            side="right",
            padx=5
        )


    # ========================================================
    # FIND ATTEMPTS
    # ========================================================

    def load_results(self):

        self.attempts = []


        if not os.path.exists(
            STUDENT_ANSWERS_DIR
        ):

            self.show_no_results()

            return


        # ----------------------------------------------------
        # Search every student folder
        # ----------------------------------------------------

        try:

            student_folders = os.listdir(
                STUDENT_ANSWERS_DIR
            )

        except Exception as e:

            print(
                "Could not list student answers:",
                e
            )

            self.show_no_results()

            return


        for student_folder_name in student_folders:

            student_folder = os.path.join(
                STUDENT_ANSWERS_DIR,
                student_folder_name
            )


            if not os.path.isdir(
                student_folder
            ):

                continue


            for attempt_folder_name in os.listdir(
                student_folder
            ):

                attempt_folder = os.path.join(
                    student_folder,
                    attempt_folder_name
                )


                if not os.path.isdir(
                    attempt_folder
                ):

                    continue


                result_file = os.path.join(
                    attempt_folder,
                    "exam_result.json"
                )


                if not os.path.exists(
                    result_file
                ):

                    continue


                try:

                    with open(
                        result_file,
                        "r",
                        encoding="utf-8"
                    ) as file:

                        result = json.load(
                            file
                        )


                except Exception as e:

                    print(
                        "Could not read result:",
                        result_file
                    )

                    print(e)

                    continue


                student = result.get(
                    "student",
                    {}
                )


                result_student_id = str(
                    result.get(
                        "student_id",
                        student.get(
                            "student_id",
                            ""
                        )
                    )
                )


                if (
                    result_student_id
                    ==
                    str(self.student_id)
                ):

                    result["_attempt_folder"] = (
                        attempt_folder
                    )

                    result["_result_file"] = (
                        result_file
                    )

                    self.attempts.append(
                        result
                    )


        # ----------------------------------------------------
        # Sort by attempt number
        # ----------------------------------------------------

        def attempt_sort_key(item):

            try:

                return int(
                    item.get(
                        "attempt_number",
                        0
                    )
                )

            except Exception:

                return 0


        self.attempts.sort(
            key=attempt_sort_key
        )


        if not self.attempts:

            self.show_no_results()

            return


        # ----------------------------------------------------
        # Student label
        # ----------------------------------------------------

        student = self.attempts[-1].get(
            "student",
            {}
        )


        self.student_label.config(
            text=(
                f"Student: "
                f"{student.get('student_name', '')}"
                f"   |   "
                f"ID: "
                f"{student.get('student_id', self.student_id)}"
            )
        )


        # ----------------------------------------------------
        # Combo box
        # ----------------------------------------------------

        values = []


        for result in self.attempts:

            attempt_number = result.get(
                "attempt_number",
                0
            )

            submitted_at = result.get(
                "submitted_at",
                ""
            )


            values.append(
                (
                    f"Attempt {attempt_number}"
                    f"   |   "
                    f"{submitted_at}"
                )
            )


        self.attempt_combo["values"] = values


        # IMPORTANT:
        # Always select the newest attempt.

        latest_index = (
            len(values) - 1
        )


        self.attempt_combo.current(
            latest_index
        )


        self.display_result(
            latest_index
        )


    # ========================================================
    # SAVE CALCULATED RESULT BACK TO JSON
    # ========================================================

    def save_calculated_result(
        self,
        result,
        questions,
        total_allotted,
        total_awarded,
        percentage,
        final_result
    ):

        result_file = result.get(
            "_result_file",
            ""
        )


        if not result_file:

            attempt_folder = result.get(
                "_attempt_folder",
                ""
            )

            if attempt_folder:

                result_file = os.path.join(
                    attempt_folder,
                    "exam_result.json"
                )


        if not result_file:

            print(
                "WARNING: Result file path not available."
            )

            return


        try:

            # ------------------------------------------------
            # Update question marks
            # ------------------------------------------------

            for index, question in enumerate(
                questions
            ):

                if not isinstance(
                    question,
                    dict
                ):

                    continue


                question["marks_awarded"] = float(
                    question.get(
                        "marks_awarded",
                        0
                    )
                    or 0
                )


            # ------------------------------------------------
            # Update final result
            # ------------------------------------------------

            result["total_allotted_marks"] = round(
                float(total_allotted),
                2
            )

            result["total_secured_marks"] = round(
                float(total_awarded),
                2
            )

            result["percentage"] = round(
                float(percentage),
                2
            )

            result["result"] = (
                final_result
            )


            result["pass_percentage"] = 50


            result["questions"] = questions


            # ------------------------------------------------
            # Do not save temporary internal fields
            # ------------------------------------------------

            result.pop(
                "_calculated",
                None
            )

            result.pop(
                "_attempt_folder",
                None
            )

            result.pop(
                "_result_file",
                None
            )


            result = make_json_safe(
                result
            )


            # ------------------------------------------------
            # WRITE exam_result.json
            # ------------------------------------------------

            with open(
                result_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    result,
                    file,
                    indent=4,
                    ensure_ascii=False
                )


            print(
                "Updated exam_result.json:"
            )

            print(
                result_file
            )

            print(
                "Marks:",
                round(
                    total_awarded,
                    2
                ),
                "/",
                round(
                    total_allotted,
                    2
                )
            )

            print(
                "Percentage:",
                round(
                    percentage,
                    2
                )
            )

            print(
                "Result:",
                final_result
            )


            # ------------------------------------------------
            # Restore internal paths in memory
            # ------------------------------------------------

            result["_result_file"] = (
                result_file
            )

            result["_attempt_folder"] = (
                os.path.dirname(
                    result_file
                )
            )


        except Exception as e:

            print(
                "Could not update exam_result.json:"
            )

            print(e)


    # ========================================================
    # NO RESULTS
    # ========================================================

    def show_no_results(self):

        self.summary_label.config(
            text=(
                "No completed examination results "
                "are available for this student."
            )
        )


        self.download_button.config(
            state="disabled"
        )


        self.attempt_combo["values"] = []


    # ========================================================
    # ATTEMPT SELECTED
    # ========================================================

    def attempt_selected(
        self,
        event=None
    ):

        index = (
            self.attempt_combo.current()
        )


        if index < 0:

            return


        self.display_result(
            index
        )


    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    def display_result(
        self,
        index
    ):

        if (
            index < 0
            or
            index >= len(
                self.attempts
            )
        ):

            return


        self.current_result = (
            self.attempts[index]
        )


        # ----------------------------------------------------
        # Clear table
        # ----------------------------------------------------

        for item in self.tree.get_children():

            self.tree.delete(
                item
            )


        result = self.current_result


        questions = result.get(
            "questions",
            []
        )


        student_answers = result.get(
            "student_answers",
            {}
        )


        total_allotted = 0.0

        total_awarded = 0.0


        # ----------------------------------------------------
        # Evaluate every question
        # ----------------------------------------------------

        for index, question in enumerate(
            questions
        ):

            if not isinstance(
                question,
                dict
            ):

                continue


            question_number = (
                index + 1
            )


            question_text = question.get(
                "question",
                ""
            )


            expected_answer = question.get(
                "expected_answer",
                ""
            )


            allotted_marks = question.get(
                "marks",
                0
            )


            try:

                allotted_marks = float(
                    allotted_marks
                )

            except Exception:

                allotted_marks = 0.0


            # ------------------------------------------------
            # Get student answer
            # ------------------------------------------------

            student_answer = ""


            if isinstance(
                student_answers,
                dict
            ):

                student_answer = (
                    student_answers.get(
                        index,
                        student_answers.get(
                            str(index),
                            ""
                        )
                    )
                )


            # ------------------------------------------------
            # Calculate similarity
            # ------------------------------------------------

            similarity = (
                self.evaluator.similarity(
                    expected_answer,
                    student_answer
                )
            )


            # ------------------------------------------------
            # Calculate awarded marks
            # ------------------------------------------------

            awarded_marks, evaluation = (
                calculate_marks(
                    similarity,
                    allotted_marks
                )
            )


            awarded_marks = float(
                awarded_marks
            )


            # ------------------------------------------------
            # IMPORTANT:
            # Store calculated marks in question itself
            # ------------------------------------------------

            question["marks_awarded"] = (
                awarded_marks
            )


            question["similarity"] = (
                round(
                    similarity,
                    2
                )
            )


            question["evaluation"] = (
                evaluation
            )


            total_allotted += (
                allotted_marks
            )


            total_awarded += (
                awarded_marks
            )


            # ------------------------------------------------
            # Table
            # ------------------------------------------------

            self.tree.insert(
                "",
                "end",
                values=(

                    question_number,

                    question_text,

                    expected_answer,

                    student_answer,

                    f"{similarity:.2f}%",

                    evaluation,

                    f"{allotted_marks:.2f}",

                    f"{awarded_marks:.2f}"
                )
            )


        # ----------------------------------------------------
        # Percentage
        # ----------------------------------------------------

        if total_allotted > 0:

            percentage = (
                total_awarded
                /
                total_allotted
                *
                100
            )

        else:

            percentage = 0.0


        percentage = round(
            percentage,
            2
        )


        # ----------------------------------------------------
        # Overall result
        # ----------------------------------------------------

        if percentage >= 50:

            final_result = "PASS"

        else:

            final_result = "FAIL"


        # ----------------------------------------------------
        # Save calculated result to JSON
        #
        # THIS IS THE IMPORTANT CHANGE.
        # ----------------------------------------------------

        self.save_calculated_result(
            result,
            questions,
            total_allotted,
            total_awarded,
            percentage,
            final_result
        )


        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        attempt_number = result.get(
            "attempt_number",
            0
        )


        submitted_at = result.get(
            "submitted_at",
            "Not available"
        )


        self.summary_label.config(
            text=(

                f"Attempt: {attempt_number}"
                f"     |     "

                f"Total Questions: "
                f"{len(questions)}"
                f"     |     "

                f"Total Marks: "
                f"{total_allotted:.2f}"
                f"     |     "

                f"Marks Obtained: "
                f"{total_awarded:.2f}"
                f"     |     "

                f"Percentage: "
                f"{percentage:.2f}%"
                f"     |     "

                f"Result: "
                f"{final_result}"

                f"\n\n"

                f"Submitted At: "
                f"{submitted_at}"
            )
        )


        self.download_button.config(
            state="normal"
        )


        # ----------------------------------------------------
        # Keep calculated data in memory
        # ----------------------------------------------------

        result["_calculated"] = {

            "total_allotted": (
                total_allotted
            ),

            "total_awarded": (
                total_awarded
            ),

            "percentage": (
                percentage
            ),

            "result": (
                final_result
            )
        }


    # ========================================================
    # DOWNLOAD ANSWER SCRIPT
    # ========================================================

    def download_answer_script(self):

        if self.current_result is None:

            messagebox.showwarning(
                "No Result",
                (
                    "Please select an examination "
                    "attempt first."
                ),
                parent=self.root
            )

            return


        result = self.current_result


        calculated = result.get(
            "_calculated",
            {}
        )


        student = result.get(
            "student",
            {}
        )


        attempt_number = result.get(
            "attempt_number",
            0
        )


        questions = result.get(
            "questions",
            []
        )


        student_answers = result.get(
            "student_answers",
            {}
        )


        total_allotted = calculated.get(
            "total_allotted",
            result.get(
                "total_allotted_marks",
                0
            )
        )


        total_awarded = calculated.get(
            "total_awarded",
            result.get(
                "total_secured_marks",
                0
            )
        )


        percentage = calculated.get(
            "percentage",
            result.get(
                "percentage",
                0
            )
        )


        final_result = calculated.get(
            "result",
            result.get(
                "result",
                "FAIL"
            )
        )


        # ====================================================
        # DOWNLOAD FOLDER
        # ====================================================

        downloads_folder = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )


        os.makedirs(
            downloads_folder,
            exist_ok=True
        )


        student_name = safe_file_name(
            student.get(
                "student_name",
                "Student"
            )
        )


        file_name = (
            f"{student_name}_"
            f"Attempt_{attempt_number}_"
            f"Answer_Script.txt"
        )


        file_path = os.path.join(
            downloads_folder,
            file_name
        )


        # ====================================================
        # CREATE ANSWER SCRIPT
        # ====================================================

        lines = []


        lines.append(
            "=" * 75
        )

        lines.append(
            "AI-BASED AUTOMATED ORAL EXAMINATION"
        )

        lines.append(
            "STUDENT ANSWER SCRIPT"
        )

        lines.append(
            "=" * 75
        )


        lines.append("")


        lines.append(
            f"Exam Name: "
            f"{result.get('exam_name', '')}"
        )


        lines.append(
            f"Exam ID: "
            f"{result.get('exam_id', '')}"
        )


        lines.append(
            f"Pattern ID: "
            f"{result.get('pattern_id', '')}"
        )


        lines.append(
            f"Student ID: "
            f"{student.get('student_id', '')}"
        )


        lines.append(
            f"Student Name: "
            f"{student.get('student_name', '')}"
        )


        lines.append(
            f"Class: "
            f"{student.get('class', '')}"
        )


        lines.append(
            f"Section: "
            f"{student.get('section', '')}"
        )


        lines.append(
            f"Roll Number: "
            f"{student.get('roll_number', '')}"
        )


        lines.append(
            f"Attempt Number: "
            f"{attempt_number}"
        )


        lines.append(
            f"Submitted At: "
            f"{result.get('submitted_at', '')}"
        )


        lines.append("")


        lines.append(
            "=" * 75
        )

        lines.append(
            "FINAL RESULT"
        )

        lines.append(
            "=" * 75
        )


        lines.append(
            f"Total Questions: "
            f"{len(questions)}"
        )


        lines.append(
            f"Total Marks: "
            f"{float(total_allotted):.2f}"
        )


        lines.append(
            f"Marks Obtained: "
            f"{float(total_awarded):.2f}"
        )


        lines.append(
            f"Percentage: "
            f"{float(percentage):.2f}%"
        )


        lines.append(
            f"Pass Percentage: 50%"
        )


        lines.append(
            f"RESULT: "
            f"{final_result}"
        )


        lines.append("")


        lines.append(
            "=" * 75
        )

        lines.append(
            "QUESTION-WISE EVALUATION"
        )

        lines.append(
            "=" * 75
        )


        # ====================================================
        # QUESTION DETAILS
        # ====================================================

        for index, question in enumerate(
            questions
        ):

            if not isinstance(
                question,
                dict
            ):

                continue


            question_number = (
                index + 1
            )


            question_text = question.get(
                "question",
                ""
            )


            expected_answer = question.get(
                "expected_answer",
                ""
            )


            allotted_marks = question.get(
                "marks",
                0
            )


            try:

                allotted_marks = float(
                    allotted_marks
                )

            except Exception:

                allotted_marks = 0.0


            student_answer = ""


            if isinstance(
                student_answers,
                dict
            ):

                student_answer = (
                    student_answers.get(
                        index,
                        student_answers.get(
                            str(index),
                            ""
                        )
                    )
                )


            similarity = (
                self.evaluator.similarity(
                    expected_answer,
                    student_answer
                )
            )


            awarded_marks, evaluation = (
                calculate_marks(
                    similarity,
                    allotted_marks
                )
            )


            awarded_marks = float(
                awarded_marks
            )


            lines.append("")


            lines.append(
                "-" * 75
            )


            lines.append(
                f"QUESTION {question_number}"
            )


            lines.append(
                "-" * 75
            )


            lines.append("")


            lines.append(
                "Question:"
            )


            lines.append(
                str(question_text)
            )


            lines.append("")


            lines.append(
                "Original / Expected Answer:"
            )


            lines.append(
                str(expected_answer)
            )


            lines.append("")


            lines.append(
                "Student Answer:"
            )


            lines.append(
                (
                    str(student_answer)
                    if student_answer
                    else
                    "No answer recorded."
                )
            )


            lines.append("")


            lines.append(
                f"Answer Similarity: "
                f"{similarity:.2f}%"
            )


            lines.append(
                f"Evaluation: "
                f"{evaluation}"
            )


            lines.append(
                f"Allotted Marks: "
                f"{allotted_marks:.2f}"
            )


            lines.append(
                f"Awarded Marks: "
                f"{awarded_marks:.2f}"
            )


        lines.append("")


        lines.append(
            "=" * 75
        )

        lines.append(
            "END OF ANSWER SCRIPT"
        )

        lines.append(
            "=" * 75
        )


        # ====================================================
        # WRITE FILE
        # ====================================================

        try:

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    "\n".join(
                        lines
                    )
                )


            messagebox.showinfo(
                "Download Successful",
                (
                    "Answer script downloaded successfully.\n\n"
                    f"Location:\n{file_path}"
                ),
                parent=self.root
            )


        except Exception as e:

            messagebox.showerror(
                "Download Error",
                (
                    "Could not download the answer script.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # BACK TO DETAILS
    # ========================================================

    def back_to_details(self):

        try:

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

            except Exception as e:

                print(
                    "Could not restore Student Details:",
                    e
                )


# ============================================================
# OPEN RESULTS
# ============================================================

def open_student_results(
    student_id,
    parent_window=None,
    login_window=None
):

    window = tk.Toplevel(
        parent_window
    )


    StudentResults(
        window,
        student_id,
        parent_window=parent_window,
        login_window=login_window
    )


    return window


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()


    open_student_results(
        "STUDENT001",
        parent_window=root,
        login_window=root
    )


    root.mainloop()
