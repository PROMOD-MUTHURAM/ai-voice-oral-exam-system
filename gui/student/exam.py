import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
import threading
import time
import re
import wave
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
# PYTHON PATH
# ============================================================

if BASE_DIR not in sys.path:

    sys.path.insert(
        0,
        BASE_DIR
    )


# ============================================================
# ANSWER EVALUATION
# ============================================================

class AnswerEvaluator:

    def __init__(self):
        self.model = None

    def load_model(self):
        if self.model is not None:
            return True

        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            return True
        except Exception as e:
            print("Could not load similarity model:")
            print(e)
            return False

    def similarity(self, expected_answer, student_answer):
        expected_answer = str(expected_answer or "").strip().lower()
        student_answer = str(student_answer or "").strip().lower()

        if not student_answer or not expected_answer:
            return 0.0

        if expected_answer == student_answer:
            return 100.0

        if not self.load_model():
            return 0.0

        try:
            from sentence_transformers.util import cos_sim

            embeddings = self.model.encode(
                [expected_answer, student_answer],
                convert_to_tensor=True
            )

            score = cos_sim(
                embeddings[0],
                embeddings[1]
            ).item()

            score = max(0.0, min(1.0, score))
            return round(score * 100, 2)

        except Exception as e:
            print("Similarity calculation error:")
            print(e)
            return 0.0


def calculate_marks(similarity, allotted_marks):

    try:
        allotted_marks = float(allotted_marks or 0)
    except Exception:
        allotted_marks = 0.0

    try:
        similarity = float(similarity or 0)
    except Exception:
        similarity = 0.0

    if allotted_marks == 1:
        if similarity >= 75:
            return 1.0, "Correct"
        return 0.0, "Wrong"

    if similarity >= 75:
        return allotted_marks, "Correct"

    if similarity >= 50:
        return allotted_marks * 0.50, "Partially Correct"

    if similarity >= 35:
        return allotted_marks * 0.25, "Partially Correct"

    return 0.0, "Wrong"


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


QUESTION_FILE = os.path.join(
    BACKEND_DIR,
    "questions.json"
)


# ============================================================
# ADMIN DATA DIRECTORIES
# ============================================================

EXAMS_DIR = os.path.join(
    BACKEND_DIR,
    "exams"
)


PATTERNS_DIR = os.path.join(
    BACKEND_DIR,
    "exam_patterns"
)


SESSIONS_DIR = os.path.join(
    BACKEND_DIR,
    "exam_sessions"
)


# ============================================================
# EXAM DEFAULT SETTINGS
# ============================================================

# These are ONLY fallback display values.
# When Admin has assigned a session, the values from Admin
# are used instead.

DEFAULT_EXAM_NAME = "CBT August 2026"

DEFAULT_EXAM_TIME_SECONDS = 120

ANSWER_TIME_SECONDS = 10


# ============================================================
# DYNAMIC EXAM VALUES
# ============================================================

EXAM_NAME = DEFAULT_EXAM_NAME

EXAM_TIME_SECONDS = DEFAULT_EXAM_TIME_SECONDS


# ============================================================
# LOCAL WHISPER MODEL
# ============================================================

WHISPER_MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "whisper-small-en"
)


# ============================================================
# ANSWER STORAGE
# ============================================================

STUDENT_ANSWERS_DIR = os.path.join(
    BACKEND_DIR,
    "student_answers"
)


os.makedirs(
    BACKEND_DIR,
    exist_ok=True
)


os.makedirs(
    STUDENT_ANSWERS_DIR,
    exist_ok=True
)


# ============================================================
# DEFAULT QUESTIONS
#
# IMPORTANT:
# These are retained only for backward compatibility.
# They are NOT used when an Admin session is assigned.
# ============================================================

DEFAULT_QUESTIONS = [

    {
        "question": "What is photosynthesis?",
        "expected_answer": (
            "Photosynthesis is the process by which green plants "
            "make their food using sunlight, carbon dioxide and water, "
            "producing glucose and oxygen."
        ),
        "marks": 3
    },

    {
        "question": "What is the capital of India?",
        "expected_answer": (
            "The capital of India is New Delhi."
        ),
        "marks": 2
    },

    {
        "question": "What is CPU?",
        "expected_answer": (
            "CPU stands for Central Processing Unit. It is the main "
            "processing unit of a computer that executes instructions "
            "and performs calculations."
        ),
        "marks": 2
    },

    {
        "question": "What is Python?",
        "expected_answer": (
            "Python is a high-level, interpreted, general-purpose "
            "programming language known for its simple and readable syntax."
        ),
        "marks": 3
    }

]


# ============================================================
# READ JSON
# ============================================================

def read_json_file(file_path):

    if not os.path.exists(
        file_path
    ):

        return None


    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )


        if isinstance(
            data,
            dict
        ):

            return data


    except Exception as e:

        print(
            "Could not read JSON:"
        )

        print(
            file_path
        )

        print(
            e
        )


    return None


# ============================================================
# LOAD STUDENT
# ============================================================

def load_student_details():

    if not os.path.exists(
        STUDENT_DATA_FILE
    ):

        return None


    return read_json_file(
        STUDENT_DATA_FILE
    )


# ============================================================
# SAFE FOLDER NAME
# ============================================================

def safe_folder_name(name):

    name = str(
        name
    ).strip()


    if not name:

        name = "Unknown_Student"


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


    name = name.strip(
        " ._"
    )


    if not name:

        name = "Unknown_Student"


    return name


# ============================================================
# EXAM WINDOW
# ============================================================

class ExamWindow:

    def __init__(
        self,
        root,
        parent_window=None,
        login_window=None,
        details_window=None,
        instructions_window=None
    ):

        self.root = root
        self.exam_started_at = datetime.now()
        self.evaluator = AnswerEvaluator()

        # ====================================================
        # WINDOW REFERENCES
        # ====================================================

        self.parent_window = (
            parent_window
        )


        self.login_window = (
            login_window
        )


        self.details_window = (
            details_window
        )


        self.instructions_window = (
            instructions_window
            if instructions_window is not None
            else parent_window
        )


        # ====================================================
        # STUDENT
        # ====================================================

        self.student_data = (
            load_student_details()
        )


        if not self.student_data:

            messagebox.showerror(
                "Student Error",
                (
                    "Student information could not be loaded.\n\n"
                    "Please login again."
                ),
                parent=self.root
            )

            self.root.destroy()

            return


        self.student_id = str(
            self.student_data.get(
                "student_id",
                ""
            )
        ).strip()


        if not self.student_id:

            messagebox.showerror(
                "Student ID Error",
                (
                    "The logged-in student ID was not found.\n\n"
                    "Please login again."
                ),
                parent=self.root
            )

            self.root.destroy()

            return


        # ====================================================
        # ADMIN SESSION
        # ====================================================

        self.session_data = None

        self.admin_exam_data = None

        self.admin_pattern_data = None


        # ====================================================
        # LOAD ASSIGNED EXAM
        # ====================================================

        assigned_exam = (
            self.load_assigned_exam_for_student()
        )


        if assigned_exam is None:

            # No Admin session assigned to this student.
            # Do NOT open the old default questions.

            self.root.destroy()

            return


        # ====================================================
        # DYNAMIC EXAM INFORMATION
        # ====================================================

        global EXAM_NAME
        global EXAM_TIME_SECONDS


        EXAM_NAME = (
            self.session_data.get(
                "exam_name",
                self.admin_exam_data.get(
                    "exam_name",
                    DEFAULT_EXAM_NAME
                )
            )
        )


        try:

            duration_minutes = float(
                self.session_data.get(
                    "duration_minutes",
                    0
                )
            )


            if duration_minutes <= 0:

                raise ValueError


            EXAM_TIME_SECONDS = int(
                duration_minutes * 60
            )


        except Exception:

            # Try exam file if session duration
            # was missing.

            try:

                duration_minutes = float(
                    self.admin_exam_data.get(
                        "duration_minutes",
                        self.admin_exam_data.get(
                            "duration",
                            0
                        )
                    )
                )


                EXAM_TIME_SECONDS = int(
                    duration_minutes * 60
                )


            except Exception:

                EXAM_TIME_SECONDS = (
                    DEFAULT_EXAM_TIME_SECONDS
                )


        # ====================================================
        # QUESTIONS FROM ADMIN EXAM
        # ====================================================

        self.questions = (
            self.build_student_questions()
        )


        if not self.questions:

            messagebox.showerror(
                "Exam Error",
                (
                    "The Admin-selected examination does not "
                    "contain usable questions.\n\n"
                    f"Exam: {EXAM_NAME}\n"
                    f"Exam ID: {self.session_data.get('exam_id', '')}\n"
                    f"Pattern: {self.session_data.get('pattern_name', '')}"
                ),
                parent=self.root
            )

            self.root.destroy()

            return


        # ====================================================
        # QUESTION INDEX
        # ====================================================

        self.current_question = 0


        # ====================================================
        # ANSWERS
        # ====================================================

        self.student_answers = {}


        self.answered_questions = set()


        # ====================================================
        # QUESTION TIMES
        # ====================================================

        self.question_answer_times = {}


        self.question_start_times = {}


        # ====================================================
        # EXAM TIMER
        # ====================================================

        self.exam_remaining_seconds = (
            EXAM_TIME_SECONDS
        )


        self.exam_timer_running = False


        # ====================================================
        # ANSWER TIMER
        # ====================================================

        self.answer_remaining_seconds = 0


        self.answer_timer_running = False


        # ====================================================
        # RECORDING
        # ====================================================

        self.recording = False


        self.recording_question_index = None


        self.recording_started_at = None


        # ====================================================
        # TRANSCRIPTION
        # ====================================================

        self.transcribing = False


        # ====================================================
        # SUBMISSION
        # ====================================================

        self.exam_submitted = False


        # ====================================================
        # ATTEMPT
        # ====================================================

        self.attempt_number = 0


        self.attempt_folder = None


        self.student_folder = None


        self.create_attempt_folder()


        # ====================================================
        # GUI
        # ====================================================

        self.root.title(
            EXAM_NAME
        )


        self.root.geometry(
            "1100x750"
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


        # ====================================================
        # BLOCK CLOSE
        # ====================================================

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.block_close
        )


        # ====================================================
        # CREATE GUI
        # ====================================================

        self.create_interface()


        # ====================================================
        # SHOW FIRST QUESTION
        # ====================================================

        self.show_question(
            automatic_read=True
        )


        # ====================================================
        # START EXAM TIMER
        # ====================================================

        self.exam_timer_running = True


        self.update_exam_timer()


    # ========================================================
    # LOAD ASSIGNED EXAM SESSION
    # ========================================================

    def load_assigned_exam_for_student(self):

        student_id = str(
            self.student_id
        ).strip()


        if not os.path.isdir(
            SESSIONS_DIR
        ):

            messagebox.showwarning(
                "No Exam Session",
                (
                    "No examination sessions are available.\n\n"
                    "Please wait for the Admin to assign an examination."
                ),
                parent=self.root
            )

            return None


        matching_sessions = []


        # ----------------------------------------------------
        # Search every session created by Admin
        # ----------------------------------------------------

        try:

            session_files = os.listdir(
                SESSIONS_DIR
            )

        except Exception as e:

            messagebox.showerror(
                "Session Error",
                (
                    "Could not access the exam sessions folder.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return None


        for filename in session_files:

            if not filename.lower().endswith(
                ".json"
            ):

                continue


            file_path = os.path.join(
                SESSIONS_DIR,
                filename
            )


            session = read_json_file(
                file_path
            )


            if not session:

                continue


            # ------------------------------------------------
            # Only ACTIVE sessions
            # ------------------------------------------------

            status = str(
                session.get(
                    "status",
                    ""
                )
            ).strip().lower()


            if status != "active":

                continue


            # ------------------------------------------------
            # Student IDs selected by Admin
            # ------------------------------------------------

            student_ids = (
                session.get(
                    "student_ids",
                    []
                )
            )


            if not isinstance(
                student_ids,
                list
            ):

                student_ids = []


            student_match = any(
                str(item).strip() == student_id
                for item in student_ids
            )


            if not student_match:

                continue


            # ------------------------------------------------
            # This session belongs to this student
            # ------------------------------------------------

            session["_file_path"] = (
                file_path
            )


            matching_sessions.append(
                session
            )


        # ====================================================
        # NO MATCH
        # ====================================================

        if not matching_sessions:

            messagebox.showwarning(
                "No Examination Assigned",
                (
                    "No active examination has been assigned "
                    "to your Student ID.\n\n"
                    f"Student ID: {student_id}\n\n"
                    "Please contact the Administrator."
                ),
                parent=self.root
            )

            return None


        # ====================================================
        # SELECT LATEST ACTIVE SESSION
        # ====================================================

        matching_sessions.sort(
            key=lambda session:
            str(
                session.get(
                    "updated_at",
                    session.get(
                        "created_at",
                        ""
                    )
                )
            ),
            reverse=True
        )


        session = matching_sessions[0]


        self.session_data = session


        # ====================================================
        # SESSION INFORMATION
        # ====================================================

        exam_id = str(
            session.get(
                "exam_id",
                ""
            )
        ).strip()


        pattern_id = str(
            session.get(
                "pattern_id",
                ""
            )
        ).strip()


        if not exam_id:

            messagebox.showerror(
                "Invalid Exam Session",
                (
                    "The active session does not contain "
                    "an exam ID.\n\n"
                    f"Session: {session.get('session_id', '')}"
                ),
                parent=self.root
            )

            return None


        # ====================================================
        # LOAD ADMIN EXAM FILE
        # ====================================================

        exam_file = os.path.join(
            EXAMS_DIR,
            f"{exam_id}.json"
        )


        if not os.path.exists(
            exam_file
        ):

            messagebox.showerror(
                "Exam Not Found",
                (
                    "The examination selected by Admin "
                    "could not be found.\n\n"
                    f"Exam ID: {exam_id}\n"
                    f"Expected file:\n{exam_file}"
                ),
                parent=self.root
            )

            return None


        exam = read_json_file(
            exam_file
        )


        if not exam:

            messagebox.showerror(
                "Exam Data Error",
                (
                    "The Admin examination file could not "
                    "be read.\n\n"
                    f"Exam ID: {exam_id}"
                ),
                parent=self.root
            )

            return None


        self.admin_exam_data = exam


        # ====================================================
        # LOAD ADMIN PATTERN
        # ====================================================

        if pattern_id:

            pattern_file = os.path.join(
                PATTERNS_DIR,
                f"{pattern_id}.json"
            )


            if os.path.exists(
                pattern_file
            ):

                pattern = read_json_file(
                    pattern_file
                )


                if pattern:

                    self.admin_pattern_data = (
                        pattern
                    )


        # ====================================================
        # VERIFY PATTERN
        # ====================================================

        exam_pattern_id = str(
            exam.get(
                "pattern_id",
                exam.get(
                    "exam_pattern_id",
                    ""
                )
            )
        ).strip()


        if (
            exam_pattern_id
            and pattern_id
            and exam_pattern_id != pattern_id
        ):

            messagebox.showerror(
                "Exam Pattern Error",
                (
                    "The active session and examination "
                    "have different exam patterns.\n\n"
                    f"Session Pattern: {pattern_id}\n"
                    f"Exam Pattern: {exam_pattern_id}\n\n"
                    "Please ask the Administrator to recreate "
                    "the examination session."
                ),
                parent=self.root
            )

            return None


        # ====================================================
        # SHOW SESSION INFORMATION IN CONSOLE
        # ====================================================

        print(
            "=============================================="
        )

        print(
            "ASSIGNED EXAMINATION FOUND"
        )

        print(
            "Student ID:",
            student_id
        )

        print(
            "Session ID:",
            session.get(
                "session_id",
                ""
            )
        )

        print(
            "Exam ID:",
            exam_id
        )

        print(
            "Exam Name:",
            session.get(
                "exam_name",
                exam.get(
                    "exam_name",
                    ""
                )
            )
        )

        print(
            "Pattern ID:",
            pattern_id
        )

        print(
            "Pattern Name:",
            session.get(
                "pattern_name",
                ""
            )
        )

        print(
            "Duration:",
            session.get(
                "duration_minutes",
                ""
            ),
            "minutes"
        )

        print(
            "=============================================="
        )


        return session


    # ========================================================
    # BUILD STUDENT QUESTIONS FROM ADMIN EXAM
    # ========================================================

    def build_student_questions(self):

        if not self.admin_exam_data:

            return []


        admin_questions = (
            self.admin_exam_data.get(
                "questions",
                []
            )
        )


        if not isinstance(
            admin_questions,
            list
        ):

            admin_questions = []


        # ----------------------------------------------------
        # Remove inactive questions
        # ----------------------------------------------------

        active_questions = []


        for question in admin_questions:

            if not isinstance(
                question,
                dict
            ):

                continue


            status = str(
                question.get(
                    "status",
                    "Active"
                )
            ).strip().lower()


            if status == "inactive":

                continue


            # ------------------------------------------------
            # Make a copy.
            # Do NOT modify Admin's original dictionary.
            # ------------------------------------------------

            question_copy = dict(
                question
            )


            # ------------------------------------------------
            # Normalize fields
            # ------------------------------------------------

            question_copy["question"] = str(
                question_copy.get(
                    "question",
                    ""
                )
            )


            question_copy["expected_answer"] = str(
                question_copy.get(
                    "expected_answer",
                    ""
                )
            )


            question_copy["marks"] = question_copy.get(
                "marks",
                0
            )


            active_questions.append(
                question_copy
            )


        if not active_questions:

            return []


        # ====================================================
        # GET REQUIRED QUESTION COUNT
        # ====================================================

        required_count = 0


        if self.session_data:

            try:

                required_count = int(
                    float(
                        self.session_data.get(
                            "total_questions",
                            0
                        )
                    )
                )

            except Exception:

                required_count = 0


        # ----------------------------------------------------
        # If session count is unavailable, calculate it
        # from the pattern.
        # ----------------------------------------------------

        if required_count <= 0:

            required_count = (
                self.get_pattern_question_count()
            )


        # ====================================================
        # NO VALID PATTERN COUNT
        # ====================================================

        if required_count <= 0:

            # As a last compatibility option, use the
            # Admin exam's own questions.

            required_count = len(
                active_questions
            )


        # ====================================================
        # SELECT QUESTIONS ACCORDING TO PATTERN
        # ====================================================

        selected_questions = (
            self.select_questions_using_pattern(
                active_questions,
                required_count
            )
        )


        # ====================================================
        # SAFETY CHECK
        # ====================================================

        if not selected_questions:

            return []


        # ----------------------------------------------------
        # Never exceed Admin session question count
        # ----------------------------------------------------

        if required_count > 0:

            selected_questions = (
                selected_questions[:required_count]
            )


        return selected_questions


    # ========================================================
    # GET PATTERN QUESTION COUNT
    # ========================================================

    def get_pattern_question_count(self):

        pattern = (
            self.admin_pattern_data
        )


        if not pattern:

            return 0


        sections = pattern.get(
            "sections",
            []
        )


        count = 0


        if isinstance(
            sections,
            list
        ):

            for section in sections:

                if not isinstance(
                    section,
                    dict
                ):

                    continue


                value = section.get(
                    "number_of_questions",
                    section.get(
                        "question_count",
                        section.get(
                            "count",
                            0
                        )
                    )
                )


                try:

                    count += int(
                        float(
                            value
                        )
                    )

                except Exception:

                    pass


        if count <= 0:

            try:

                count = int(
                    float(
                        pattern.get(
                            "total_questions",
                            pattern.get(
                                "number_of_questions",
                                0
                            )
                        )
                    )
                )

            except Exception:

                count = 0


        return count


    # ========================================================
    # NORMALIZE QUESTION TYPE
    # ========================================================

    def normalize_question_type(
        self,
        value
    ):

        text = str(
            value or ""
        ).strip().lower()


        if not text:

            return ""


        aliases = {

            "one word":
                "One Word / 1 Mark",

            "one-word":
                "One Word / 1 Mark",

            "one word / 1 mark":
                "One Word / 1 Mark",

            "one word/1 mark":
                "One Word / 1 Mark",

            "1 mark":
                "One Word / 1 Mark",

            "1-mark":
                "One Word / 1 Mark",

            "short answer":
                "Short Answer",

            "short-answer":
                "Short Answer",

            "descriptive answer":
                "Descriptive Answer",

            "descriptive-answer":
                "Descriptive Answer",

            "long answer":
                "Descriptive Answer",

            "long-answer":
                "Descriptive Answer"

        }


        return aliases.get(
            text,
            str(value).strip()
        )


    # ========================================================
    # SELECT QUESTIONS USING ADMIN PATTERN
    # ========================================================

    def select_questions_using_pattern(
        self,
        active_questions,
        required_count
    ):

        # ----------------------------------------------------
        # No pattern loaded:
        # preserve Admin exam question order.
        # ----------------------------------------------------

        if not self.admin_pattern_data:

            return active_questions[
                :required_count
            ]


        pattern = (
            self.admin_pattern_data
        )


        sections = pattern.get(
            "sections",
            []
        )


        if not isinstance(
            sections,
            list
        ) or not sections:

            return active_questions[
                :required_count
            ]


        selected = []


        used_indexes = set()


        # ====================================================
        # MATCH EACH PATTERN SECTION
        # ====================================================

        for section in sections:

            if not isinstance(
                section,
                dict
            ):

                continue


            try:

                count = int(
                    float(
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
                )

            except Exception:

                count = 0


            if count <= 0:

                continue


            section_marks = section.get(
                "marks",
                section.get(
                    "mark",
                    None
                )
            )


            section_type = (
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


            section_type = (
                self.normalize_question_type(
                    section_type
                )
            )


            try:

                target_marks = (
                    float(section_marks)
                    if (
                        section_marks is not None
                        and str(section_marks).strip() != ""
                    )
                    else None
                )

            except Exception:

                target_marks = None


            section_selected = 0


            # ------------------------------------------------
            # First pass:
            # Match BOTH type and marks.
            # ------------------------------------------------

            for index, question in enumerate(
                active_questions
            ):

                if index in used_indexes:

                    continue


                if section_selected >= count:

                    break


                question_type = (
                    self.normalize_question_type(
                        question.get(
                            "question_type",
                            question.get(
                                "type",
                                ""
                            )
                        )
                    )
                )


                try:

                    question_marks = float(
                        question.get(
                            "marks",
                            0
                        )
                    )

                except Exception:

                    question_marks = 0


                type_matches = (
                    not section_type
                    or question_type == section_type
                )


                marks_matches = (
                    target_marks is None
                    or question_marks == target_marks
                )


                if (
                    type_matches
                    and marks_matches
                ):

                    selected.append(
                        question
                    )


                    used_indexes.add(
                        index
                    )


                    section_selected += 1


            # ------------------------------------------------
            # Second pass:
            # If exact type+marks could not fill section,
            # match type only.
            # ------------------------------------------------

            if section_selected < count:

                for index, question in enumerate(
                    active_questions
                ):

                    if index in used_indexes:

                        continue


                    if section_selected >= count:

                        break


                    question_type = (
                        self.normalize_question_type(
                            question.get(
                                "question_type",
                                question.get(
                                    "type",
                                    ""
                                )
                            )
                        )
                    )


                    if (
                        section_type
                        and question_type != section_type
                    ):

                        continue


                    selected.append(
                        question
                    )


                    used_indexes.add(
                        index
                    )


                    section_selected += 1


            # ------------------------------------------------
            # Third pass:
            # If still not enough, match marks only.
            # ------------------------------------------------

            if section_selected < count:

                for index, question in enumerate(
                    active_questions
                ):

                    if index in used_indexes:

                        continue


                    if section_selected >= count:

                        break


                    try:

                        question_marks = float(
                            question.get(
                                "marks",
                                0
                            )
                        )

                    except Exception:

                        question_marks = 0


                    if (
                        target_marks is not None
                        and question_marks != target_marks
                    ):

                        continue


                    selected.append(
                        question
                    )


                    used_indexes.add(
                        index
                    )


                    section_selected += 1


        # ====================================================
        # FILL REMAINING QUESTIONS
        # ====================================================

        if len(selected) < required_count:

            for index, question in enumerate(
                active_questions
            ):

                if index in used_indexes:

                    continue


                if len(selected) >= required_count:

                    break


                selected.append(
                    question
                )


                used_indexes.add(
                    index
                )


        return selected[
            :required_count
        ]


    # ========================================================
    # CREATE ATTEMPT FOLDER
    # ========================================================

    def create_attempt_folder(self):

        student_name = "Unknown_Student"


        if self.student_data:

            student_name = self.student_data.get(
                "student_name",
                "Unknown_Student"
            )


        safe_name = safe_folder_name(
            student_name
        )


        self.student_folder = os.path.join(
            STUDENT_ANSWERS_DIR,
            safe_name
        )


        os.makedirs(
            self.student_folder,
            exist_ok=True
        )


        attempt = 1


        while True:

            folder_name = (
                f"{safe_name}_attempt_{attempt}"
            )


            folder_path = os.path.join(
                self.student_folder,
                folder_name
            )


            if not os.path.exists(
                folder_path
            ):

                break


            attempt += 1


        self.attempt_number = attempt


        self.attempt_folder = os.path.join(
            self.student_folder,
            f"{safe_name}_attempt_{attempt}"
        )


        os.makedirs(
            self.attempt_folder,
            exist_ok=True
        )


        print(
            "Attempt folder:"
        )

        print(
            self.attempt_folder
        )


    # ========================================================
    # CREATE GUI
    # ========================================================

    def create_interface(self):

        self.main_frame = tk.Frame(
            self.root,
            bg="#f4f6f8"
        )


        self.main_frame.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # TOP BAR
        # ====================================================

        top_frame = tk.Frame(
            self.main_frame,
            bg="#1f2937",
            height=90
        )


        top_frame.pack(
            fill="x"
        )


        top_frame.pack_propagate(
            False
        )


        # ====================================================
        # EXAM NAME
        # ====================================================

        self.exam_name_label = tk.Label(
            top_frame,
            text=EXAM_NAME,
            font=("Arial", 18, "bold"),
            bg="#1f2937",
            fg="white"
        )


        self.exam_name_label.pack(
            side="left",
            padx=25
        )


        # ====================================================
        # PATTERN NAME
        # ====================================================

        pattern_name = (
            self.session_data.get(
                "pattern_name",
                ""
            )
            if self.session_data
            else ""
        )


        self.pattern_label = tk.Label(
            top_frame,
            text=(
                f"Pattern: {pattern_name}"
                if pattern_name
                else "Pattern: --"
            ),
            font=("Arial", 10, "bold"),
            bg="#1f2937",
            fg="#a7f3d0"
        )


        self.pattern_label.pack(
            side="left",
            padx=15
        )


        # ====================================================
        # STUDENT
        # ====================================================

        student_name = "Student"


        if self.student_data:

            student_name = self.student_data.get(
                "student_name",
                "Student"
            )


        self.student_label = tk.Label(
            top_frame,
            text=f"Student: {student_name}",
            font=("Arial", 10, "bold"),
            bg="#1f2937",
            fg="#d1d5db"
        )


        self.student_label.pack(
            side="left",
            padx=15
        )


        # ====================================================
        # STUDENT ID
        # ====================================================

        self.student_id_label = tk.Label(
            top_frame,
            text=f"ID: {self.student_id}",
            font=("Arial", 9, "bold"),
            bg="#1f2937",
            fg="#9ca3af"
        )


        self.student_id_label.pack(
            side="left",
            padx=10
        )


        # ====================================================
        # ATTEMPT
        # ====================================================

        self.attempt_label = tk.Label(
            top_frame,
            text=f"Attempt: {self.attempt_number}",
            font=("Arial", 10, "bold"),
            bg="#1f2937",
            fg="#93c5fd"
        )


        self.attempt_label.pack(
            side="left",
            padx=10
        )


        # ====================================================
        # EXAM TIMER
        # ====================================================

        self.exam_timer_label = tk.Label(
            top_frame,
            text="TIME: 00:00",
            font=("Arial", 16, "bold"),
            bg="#1f2937",
            fg="#facc15"
        )


        self.exam_timer_label.pack(
            side="right",
            padx=25
        )


        # ====================================================
        # QUESTION CONTAINER
        # ====================================================

        question_container = tk.Frame(
            self.main_frame,
            bg="#f4f6f8"
        )


        question_container.pack(
            fill="both",
            expand=True,
            padx=50,
            pady=25
        )


        # ====================================================
        # QUESTION CARD
        # ====================================================

        self.question_card = tk.Frame(
            question_container,
            bg="white",
            padx=35,
            pady=25,
            bd=1,
            relief="solid"
        )


        self.question_card.pack(
            fill="both",
            expand=True
        )


        # ====================================================
        # QUESTION NUMBER
        # ====================================================

        self.question_number_label = tk.Label(
            self.question_card,
            text="QUESTION 1",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#2563eb"
        )


        self.question_number_label.pack(
            anchor="w"
        )


        # ====================================================
        # MARKS
        # ====================================================

        self.marks_label = tk.Label(
            self.question_card,
            text="Marks: 0",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#16a34a"
        )


        self.marks_label.pack(
            anchor="w",
            pady=(5, 10)
        )


        # ====================================================
        # QUESTION
        # ====================================================

        self.question_text_label = tk.Label(
            self.question_card,
            text="",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#111827",
            wraplength=850,
            justify="left"
        )


        self.question_text_label.pack(
            fill="x",
            pady=15
        )


        # ====================================================
        # PLAY QUESTION
        # ====================================================

        self.play_question_button = tk.Button(
            self.question_card,
            text="🔊 PLAY QUESTION",
            font=("Arial", 11, "bold"),
            bg="#7c3aed",
            fg="white",
            activebackground="#6d28d9",
            activeforeground="white",
            width=22,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.play_question
        )


        self.play_question_button.pack(
            pady=8
        )


        # ====================================================
        # ANSWER TIMER
        # ====================================================

        self.answer_timer_label = tk.Label(
            self.question_card,
            text="Answer Time: --",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#dc2626"
        )


        self.answer_timer_label.pack(
            pady=5
        )


        # ====================================================
        # TRANSCRIPTION STATUS
        # ====================================================

        self.transcription_status_label = tk.Label(
            self.question_card,
            text="",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#2563eb"
        )


        self.transcription_status_label.pack(
            pady=3
        )


        # ====================================================
        # START ANSWERING
        # ====================================================

        self.start_answer_button = tk.Button(
            self.question_card,
            text="START ANSWERING",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=24,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.start_answering
        )


        self.start_answer_button.pack(
            pady=8
        )


        # ====================================================
        # YOUR ANSWER
        # ====================================================

        tk.Label(
            self.question_card,
            text="YOUR ANSWER",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            pady=(8, 4)
        )


        self.answer_text = tk.Text(
            self.question_card,
            height=5,
            width=80,
            font=("Arial", 11),
            wrap="word",
            state="disabled",
            bg="#f9fafb"
        )


        self.answer_text.pack(
            fill="x",
            pady=5
        )


        # ====================================================
        # NAVIGATION
        # ====================================================

        navigation_frame = tk.Frame(
            self.main_frame,
            bg="#f4f6f8"
        )


        navigation_frame.pack(
            fill="x",
            padx=50,
            pady=(0, 25)
        )


        self.previous_button = tk.Button(
            navigation_frame,
            text="◀ PREVIOUS",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=16,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.previous_question
        )


        self.reanswer_button = tk.Button(
            navigation_frame,
            text="↻ REANSWER",
            font=("Arial", 11, "bold"),
            bg="#f59e0b",
            fg="white",
            activebackground="#d97706",
            activeforeground="white",
            width=16,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.reanswer
        )


        self.next_button = tk.Button(
            navigation_frame,
            text="NEXT ▶",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=16,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.next_question
        )


        self.submit_button = tk.Button(
            navigation_frame,
            text="SUBMIT EXAM",
            font=("Arial", 11, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.submit_exam
        )


        self.update_navigation()


    # ========================================================
    # SHOW QUESTION
    # ========================================================

    def show_question(
        self,
        automatic_read=True
    ):

        if self.exam_submitted:

            return


        if self.recording:

            return


        question_data = self.questions[
            self.current_question
        ]


        question_text = question_data.get(
            "question",
            ""
        )


        marks = question_data.get(
            "marks",
            0
        )


        question_number = (
            self.current_question + 1
        )


        total_questions = len(
            self.questions
        )


        self.question_number_label.config(
            text=(
                f"QUESTION {question_number} "
                f"OF {total_questions}"
            )
        )


        self.marks_label.config(
            text=f"Marks: {marks}"
        )


        self.question_text_label.config(
            text=question_text
        )


        existing_answer = (
            self.student_answers.get(
                self.current_question,
                ""
            )
        )


        self.set_answer_text(
            existing_answer
        )


        self.answer_timer_running = False

        self.answer_remaining_seconds = 0

        self.recording = False

        self.recording_question_index = None


        self.answer_timer_label.config(
            text="Answer Time: --"
        )


        self.transcription_status_label.config(
            text=""
        )


        self.play_question_button.config(
            state="normal"
        )


        self.start_answer_button.config(
            state="normal"
        )


        if (
            self.current_question
            in self.answered_questions
        ):

            self.start_answer_button.config(
                text="ANSWER RECORDED",
                state="disabled"
            )

        else:

            self.start_answer_button.config(
                text="START ANSWERING",
                state="normal"
            )


        self.update_navigation()


        if automatic_read:

            self.root.after(
                500,
                self.play_question
            )


    # ========================================================
    # ANSWER TEXT
    # ========================================================

    def set_answer_text(
        self,
        text
    ):

        self.answer_text.config(
            state="normal"
        )


        self.answer_text.delete(
            "1.0",
            tk.END
        )


        if text:

            self.answer_text.insert(
                "1.0",
                str(text)
            )


        self.answer_text.config(
            state="disabled"
        )


    # ========================================================
    # PLAY QUESTION
    # ========================================================

    def play_question(self):

        if self.exam_submitted:

            return


        if self.recording:

            return


        question_data = self.questions[
            self.current_question
        ]


        question_text = question_data.get(
            "question",
            ""
        )


        if not question_text:

            return


        self.play_question_button.config(
            state="disabled"
        )


        threading.Thread(
            target=self.speak_question_worker,
            args=(question_text,),
            daemon=True
        ).start()


    # ========================================================
    # SPEAK QUESTION
    # ========================================================

    def speak_question_worker(
        self,
        question_text
    ):

        try:

            from backend.speech import speak_question


            speak_question(
                question_text
            )


        except Exception as e:

            print(
                "Speech backend error:"
            )

            print(e)


            try:

                import pyttsx3


                engine = (
                    pyttsx3.init()
                )


                engine.say(
                    question_text
                )


                engine.runAndWait()


                engine.stop()


            except Exception as fallback_error:

                print(
                    "Text-to-speech fallback error:"
                )

                print(
                    fallback_error
                )


        finally:

            try:

                self.root.after(
                    0,
                    self.question_audio_finished
                )

            except Exception:

                pass


    # ========================================================
    # QUESTION AUDIO FINISHED
    # ========================================================

    def question_audio_finished(self):

        if self.exam_submitted:

            return


        if self.recording:

            return


        try:

            self.play_question_button.config(
                state="normal"
            )

        except Exception:

            pass


    # ========================================================
    # START ANSWERING
    # ========================================================

    def start_answering(self):

        if self.exam_submitted:

            return


        if self.recording:

            return


        if self.transcribing:

            return


        self.transcription_status_label.config(
            text="Recording..."
        )


        self.play_question_button.config(
            state="disabled"
        )


        self.start_answer_button.config(
            state="disabled"
        )


        self.answer_remaining_seconds = (
            ANSWER_TIME_SECONDS
        )


        self.answer_timer_running = True


        self.recording = True


        self.recording_question_index = (
            self.current_question
        )


        self.recording_started_at = (
            time.time()
        )


        self.answer_timer_label.config(
            text="Answer Time: 10 sec"
        )


        threading.Thread(
            target=self.record_answer,
            daemon=True
        ).start()


        self.root.after(
            1000,
            self.update_answer_timer
        )


    # ========================================================
    # RECORD ANSWER
    # ========================================================

    def record_answer(self):

        audio_path = None


        try:

            print(
                f"Recording for {ANSWER_TIME_SECONDS} seconds..."
            )


            try:

                from backend.audio_recorder import (
                    record_audio
                )


                result = record_audio(
                    duration=ANSWER_TIME_SECONDS
                )


                if result:

                    audio_path = str(
                        result
                    )


            except Exception as backend_error:

                print(
                    "Audio recorder backend error:"
                )

                print(
                    backend_error
                )


            if not audio_path:

                audio_path = (
                    self.direct_record_audio()
                )


            print(
                "Recording completed."
            )


            if not audio_path:

                self.root.after(
                    0,
                    self.recording_finished_without_audio
                )

                return


            self.root.after(
                0,
                self.show_transcribing_status
            )


            answer = self.transcribe_audio(
                audio_path
            )


            try:

                if os.path.exists(
                    audio_path
                ):

                    os.remove(
                        audio_path
                    )

            except Exception:

                pass


            self.root.after(
                0,
                self.answer_recording_finished,
                answer
            )


        except Exception as e:

            print(
                "Recording/transcription error:"
            )

            print(e)


            self.root.after(
                0,
                self.answer_recording_failed,
                str(e)
            )


    # ========================================================
    # DIRECT AUDIO RECORDING
    # ========================================================

    def direct_record_audio(self):

        try:

            import sounddevice as sd
            import numpy as np


        except Exception as e:

            print(
                "sounddevice/numpy error:"
            )

            print(e)

            return None


        sample_rate = 16000

        channels = 1


        try:

            audio = sd.rec(
                int(
                    ANSWER_TIME_SECONDS
                    * sample_rate
                ),
                samplerate=sample_rate,
                channels=channels,
                dtype="int16"
            )


            sd.wait()


            filename = (
                f"question_"
                f"{self.current_question + 1}"
                f"_answer.wav"
            )


            audio_path = os.path.join(
                self.attempt_folder,
                filename
            )


            with wave.open(
                audio_path,
                "wb"
            ) as wav_file:

                wav_file.setnchannels(
                    channels
                )

                wav_file.setsampwidth(
                    2
                )

                wav_file.setframerate(
                    sample_rate
                )

                wav_file.writeframes(
                    audio.tobytes()
                )


            return audio_path


        except Exception as e:

            print(
                "Direct audio recording error:"
            )

            print(e)

            return None


    # ========================================================
    # SHOW TRANSCRIBING
    # ========================================================

    def show_transcribing_status(self):

        self.transcribing = True


        self.transcription_status_label.config(
            text="Converting speech to text..."
        )


        self.answer_timer_label.config(
            text="Answer recorded"
        )


        self.root.update_idletasks()


    # ========================================================
    # TRANSCRIBE AUDIO
    # ========================================================

    def transcribe_audio(
        self,
        audio_path
    ):

        try:

            from faster_whisper import (
                WhisperModel
            )


        except Exception as e:

            print(
                "faster-whisper import error:"
            )

            print(e)

            return ""


        print(
            "Loading local faster-whisper model..."
        )


        try:

            model = WhisperModel(
                WHISPER_MODEL_PATH,
                device="cpu",
                compute_type="int8"
            )


        except Exception as e:

            print(
                "Could not load local Whisper model:"
            )

            print(e)

            return ""


        print(
            "Converting audio to text..."
        )


        try:

            segments, info = model.transcribe(
                audio_path,
                language="en",
                beam_size=1,
                best_of=1,
                temperature=0,
                vad_filter=True,
                condition_on_previous_text=False
            )


            text_parts = []


            for segment in segments:

                text_parts.append(
                    segment.text.strip()
                )


            answer = " ".join(
                text_parts
            ).strip()


            print(
                "Converted answer:"
            )

            print(
                answer
            )


            return answer


        except Exception as e:

            print(
                "Transcription error:"
            )

            print(e)

            return ""


    # ========================================================
    # RECORDING FINISHED WITHOUT AUDIO
    # ========================================================

    def recording_finished_without_audio(self):

        self.recording = False

        self.answer_timer_running = False

        self.transcribing = False


        self.play_question_button.config(
            state="normal"
        )


        self.start_answer_button.config(
            state="normal"
        )


        self.answer_timer_label.config(
            text="Answer Time: 0 sec"
        )


        self.transcription_status_label.config(
            text="No audio was recorded."
        )


    # ========================================================
    # RECORDING FAILED
    # ========================================================

    def answer_recording_failed(
        self,
        error_text
    ):

        self.recording = False

        self.answer_timer_running = False

        self.transcribing = False


        self.play_question_button.config(
            state="normal"
        )


        self.start_answer_button.config(
            state="normal"
        )


        self.answer_timer_label.config(
            text="Answer Time: 0 sec"
        )


        self.transcription_status_label.config(
            text="Recording failed."
        )


        print(
            "Answer recording failed:"
        )

        print(
            error_text
        )


    # ========================================================
    # ANSWER RECORDING FINISHED
    # ========================================================

    def answer_recording_finished(
        self,
        answer
    ):

        if self.exam_submitted:

            return


        self.recording = False

        self.answer_timer_running = False

        self.transcribing = False


        question_index = (
            self.recording_question_index
        )


        if question_index is None:

            question_index = (
                self.current_question
            )


        answer = (
            answer
            if answer
            else ""
        )


        answer = str(
            answer
        ).strip()


        if not answer:

            answer = (
                "No speech detected."
            )


        self.student_answers[
            question_index
        ] = answer


        self.answered_questions.add(
            question_index
        )


        if self.recording_started_at:

            elapsed = (
                time.time()
                - self.recording_started_at
            )


            self.question_answer_times[
                question_index
            ] = round(
                min(
                    elapsed,
                    ANSWER_TIME_SECONDS
                ),
                2
            )


        if question_index == self.current_question:

            self.set_answer_text(
                answer
            )


        self.answer_timer_label.config(
            text="Answer Time: 0 sec"
        )


        self.transcription_status_label.config(
            text="Answer converted successfully."
        )


        self.play_question_button.config(
            state="normal"
        )


        self.start_answer_button.config(
            text="ANSWER RECORDED",
            state="disabled"
        )


        self.update_navigation()


        self.save_live_attempt()


        print(
            "Answer shown in answer box:"
        )

        print(
            answer
        )


    # ========================================================
    # ANSWER TIMER
    # ========================================================

    def update_answer_timer(self):

        if self.exam_submitted:

            return


        if not self.answer_timer_running:

            return


        self.answer_remaining_seconds -= 1


        if self.answer_remaining_seconds <= 0:

            self.answer_remaining_seconds = 0


            self.answer_timer_label.config(
                text="Answer Time: 0 sec"
            )


            self.answer_timer_running = False


            return


        self.answer_timer_label.config(
            text=(
                f"Answer Time: "
                f"{self.answer_remaining_seconds} sec"
            )
        )


        self.root.after(
            1000,
            self.update_answer_timer
        )


    # ========================================================
    # REANSWER
    # ========================================================

    def reanswer(self):

        if self.exam_submitted:

            return


        if self.recording:

            return


        if self.transcribing:

            return


        self.student_answers.pop(
            self.current_question,
            None
        )


        self.answered_questions.discard(
            self.current_question
        )


        self.question_answer_times.pop(
            self.current_question,
            None
        )


        self.set_answer_text(
            ""
        )


        self.transcription_status_label.config(
            text="Ready for new answer."
        )


        self.answer_timer_label.config(
            text="Answer Time: --"
        )


        self.start_answer_button.config(
            text="START ANSWERING",
            state="normal"
        )


        self.play_question_button.config(
            state="normal"
        )


        self.update_navigation()


        self.save_live_attempt()


    # ========================================================
    # NEXT QUESTION
    # ========================================================

    def next_question(self):

        if self.exam_submitted:

            return


        if self.recording:

            messagebox.showwarning(
                "Answer In Progress",
                (
                    "Please finish answering "
                    "the current question first."
                ),
                parent=self.root
            )

            return


        if self.transcribing:

            messagebox.showwarning(
                "Converting Answer",
                (
                    "Please wait until your answer "
                    "has been converted to text."
                ),
                parent=self.root
            )

            return


        if self.current_question >= (
            len(self.questions) - 1
        ):

            return


        self.current_question += 1


        self.show_question(
            automatic_read=True
        )


    # ========================================================
    # PREVIOUS QUESTION
    # ========================================================

    def previous_question(self):

        if self.exam_submitted:

            return


        if self.recording:

            messagebox.showwarning(
                "Answer In Progress",
                (
                    "Please finish answering "
                    "the current question first."
                ),
                parent=self.root
            )

            return


        if self.transcribing:

            messagebox.showwarning(
                "Converting Answer",
                (
                    "Please wait until your answer "
                    "has been converted to text."
                ),
                parent=self.root
            )

            return


        if self.current_question <= 0:

            return


        self.current_question -= 1


        self.show_question(
            automatic_read=True
        )


    # ========================================================
    # UPDATE NAVIGATION
    # ========================================================

    def update_navigation(self):

        if self.current_question == 0:

            self.previous_button.pack_forget()

        else:

            if not self.previous_button.winfo_ismapped():

                self.previous_button.pack(
                    side="left",
                    padx=5
                )


        if (
            self.current_question
            in self.answered_questions
        ):

            if not self.reanswer_button.winfo_ismapped():

                self.reanswer_button.pack(
                    side="left",
                    padx=5
                )

        else:

            self.reanswer_button.pack_forget()


        if self.current_question < (
            len(self.questions) - 1
        ):

            if not self.next_button.winfo_ismapped():

                self.next_button.pack(
                    side="left",
                    padx=5
                )

        else:

            self.next_button.pack_forget()


        if self.all_questions_answered():

            if not self.submit_button.winfo_ismapped():

                self.submit_button.pack(
                    side="right",
                    padx=5
                )

        else:

            self.submit_button.pack_forget()


    # ========================================================
    # ALL ANSWERED
    # ========================================================

    def all_questions_answered(self):

        return (
            len(
                self.answered_questions
            )
            == len(
                self.questions
            )
        )


    # ========================================================
    # EXAM TIMER
    # ========================================================

    def update_exam_timer(self):

        if self.exam_submitted:

            return


        if not self.exam_timer_running:

            return


        if self.exam_remaining_seconds <= 0:

            self.exam_remaining_seconds = 0


            self.exam_timer_label.config(
                text="TIME: 00:00"
            )


            self.exam_timer_running = False


            self.auto_submit_exam()


            return


        minutes = (
            self.exam_remaining_seconds
            // 60
        )


        seconds = (
            self.exam_remaining_seconds
            % 60
        )


        self.exam_timer_label.config(
            text=(
                f"TIME: "
                f"{minutes:02d}:"
                f"{seconds:02d}"
            )
        )


        self.exam_remaining_seconds -= 1


        self.root.after(
            1000,
            self.update_exam_timer
        )


    # ========================================================
    # AUTO SUBMIT
    # ========================================================

    def auto_submit_exam(self):

        if self.exam_submitted:

            return


        self.recording = False

        self.answer_timer_running = False


        messagebox.showinfo(
            "Time Up",
            (
                "The examination time has ended.\n\n"
                "Your examination will be submitted automatically."
            ),
            parent=self.root
        )


        self.finish_exam(
            automatic=True
        )


    # ========================================================
    # SUBMIT
    # ========================================================

    def submit_exam(self):

        if self.exam_submitted:

            return


        if self.recording:

            messagebox.showwarning(
                "Answer In Progress",
                (
                    "Please finish recording your "
                    "current answer first."
                ),
                parent=self.root
            )

            return


        if self.transcribing:

            messagebox.showwarning(
                "Converting Answer",
                (
                    "Please wait until the current "
                    "answer has been converted to text."
                ),
                parent=self.root
            )

            return


        if not self.all_questions_answered():

            remaining = (
                len(self.questions)
                - len(self.answered_questions)
            )


            messagebox.showwarning(
                "Questions Remaining",
                (
                    f"You still have {remaining} "
                    f"question(s) unanswered."
                ),
                parent=self.root
            )

            return


        confirmation = messagebox.askyesno(
            "Submit Examination",
            (
                "Are you sure you want to submit "
                "the examination?\n\n"
                "You cannot continue after submission."
            ),
            parent=self.root
        )


        if not confirmation:

            return


        self.finish_exam(
            automatic=False
        )


    # ========================================================
    # FINISH EXAM
    # ========================================================

    def finish_exam(
        self,
        automatic=False
    ):

        if self.exam_submitted:

            return


        self.exam_submitted = True


        self.exam_timer_running = False

        self.answer_timer_running = False

        self.recording = False


        self.save_exam_answers(
            automatic=automatic
        )


        if automatic:

            messagebox.showinfo(
                "Exam Submitted",
                (
                    "The examination has been "
                    "submitted automatically."
                ),
                parent=self.root
            )

        else:

            messagebox.showinfo(
                "Exam Submitted",
                (
                    "Your examination has been "
                    "submitted successfully."
                ),
                parent=self.root
            )


        self.return_to_login()


    # ========================================================
    # SAVE LIVE ATTEMPT
    # ========================================================

    def save_live_attempt(self):

        try:

            data = {

                "exam_name": EXAM_NAME,

                "exam_id": (
                    self.session_data.get(
                        "exam_id",
                        ""
                    )
                    if self.session_data
                    else ""
                ),

                "pattern_id": (
                    self.session_data.get(
                        "pattern_id",
                        ""
                    )
                    if self.session_data
                    else ""
                ),

                "pattern_name": (
                    self.session_data.get(
                        "pattern_name",
                        ""
                    )
                    if self.session_data
                    else ""
                ),

                "session_id": (
                    self.session_data.get(
                        "session_id",
                        ""
                    )
                    if self.session_data
                    else ""
                ),

                "student_id": self.student_id,

                "student": self.student_data,

                "attempt_number": self.attempt_number,

                "questions": self.questions,

                "student_answers": self.student_answers,

                "answered_questions": list(
                    self.answered_questions
                ),

                "question_answer_times": (
                    self.question_answer_times
                ),

                "submitted": False,

                "last_updated": (
                    datetime.now().isoformat()
                )
            }


            path = os.path.join(
                self.attempt_folder,
                "exam_progress.json"
            )


            with open(
                path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )


        except Exception as e:

            print(
                "Could not save live attempt:"
            )

            print(e)


    # ========================================================
    # SAVE FINAL EXAM
    # ========================================================

    def save_exam_answers(
        self,
        automatic=False
    ):

        try:

            os.makedirs(
                self.attempt_folder,
                exist_ok=True
            )

            def make_json_safe(value):
                if isinstance(value, datetime):
                    return value.isoformat()
                if isinstance(value, dict):
                    return {
                        str(key): make_json_safe(val)
                        for key, val in value.items()
                    }
                if isinstance(value, list):
                    return [make_json_safe(item) for item in value]
                if isinstance(value, tuple):
                    return [make_json_safe(item) for item in value]
                return value

            total_allotted_marks = 0.0
            total_secured_marks = 0.0

            for index, question in enumerate(self.questions):

                if not isinstance(question, dict):
                    continue

                try:
                    allotted_marks = float(
                        question.get("marks", 0) or 0
                    )
                except Exception:
                    allotted_marks = 0.0

                total_allotted_marks += allotted_marks

                answer = self.student_answers.get(index, "")
                expected_answer = question.get("expected_answer", "")

                similarity = self.evaluator.similarity(
                    expected_answer,
                    answer
                )

                awarded_marks, evaluation = calculate_marks(
                    similarity,
                    allotted_marks
                )

                marks_awarded = float(awarded_marks)
                total_secured_marks += marks_awarded

                # Store the calculated values in the question itself.
                question["marks_awarded"] = marks_awarded
                question["similarity"] = similarity
                question["evaluation"] = evaluation

                question_data = {
                    "exam_name": EXAM_NAME,
                    "exam_id": (
                        self.session_data.get("exam_id", "")
                        if self.session_data else ""
                    ),
                    "pattern_id": (
                        self.session_data.get("pattern_id", "")
                        if self.session_data else ""
                    ),
                    "pattern_name": (
                        self.session_data.get("pattern_name", "")
                        if self.session_data else ""
                    ),
                    "session_id": (
                        self.session_data.get("session_id", "")
                        if self.session_data else ""
                    ),
                    "student_id": self.student_id,
                    "attempt_number": self.attempt_number,
                    "question_number": index + 1,
                    "question": question.get("question", ""),
                    "expected_answer": expected_answer,
                    "question_type": question.get(
                        "question_type",
                        question.get("type", "")
                    ),
                    "marks": allotted_marks,
                    "marks_awarded": marks_awarded,
                    "similarity": similarity,
                    "evaluation": evaluation,
                    "student_answer": answer,
                    "answer_time_seconds": self.question_answer_times.get(
                        index,
                        0
                    )
                }

                answer_file = os.path.join(
                    self.attempt_folder,
                    f"question_{index + 1}_answer.json"
                )

                with open(
                    answer_file,
                    "w",
                    encoding="utf-8"
                ) as file:
                    json.dump(
                        make_json_safe(question_data),
                        file,
                        indent=4,
                        ensure_ascii=False
                    )

            if total_allotted_marks > 0:
                final_percentage = round(
                    (total_secured_marks / total_allotted_marks) * 100,
                    2
                )
            else:
                final_percentage = 0.0

            final_result = (
                "PASS"
                if final_percentage >= 50
                else "FAIL"
            )

            start_time_value = getattr(
                self,
                "exam_started_at",
                ""
            )

            start_time_value = make_json_safe(start_time_value)

            if not start_time_value:
                start_time_value = datetime.now().isoformat()

            submission_time = datetime.now().isoformat()

            exam_data = {
                "exam_name": EXAM_NAME,
                "exam_id": (
                    self.session_data.get("exam_id", "")
                    if self.session_data else ""
                ),
                "pattern_id": (
                    self.session_data.get("pattern_id", "")
                    if self.session_data else ""
                ),
                "pattern_name": (
                    self.session_data.get("pattern_name", "")
                    if self.session_data else ""
                ),
                "session_id": (
                    self.session_data.get("session_id", "")
                    if self.session_data else ""
                ),
                "student_id": self.student_id,
                "student": self.student_data,
                "attempt_number": self.attempt_number,
                "start_time": start_time_value,
                "total_questions": len(self.questions),
                "total_allotted_marks": round(
                    total_allotted_marks,
                    2
                ),
                "total_secured_marks": round(
                    total_secured_marks,
                    2
                ),
                "percentage": final_percentage,
                "result": final_result,
                "pass_percentage": 50,
                "questions": self.questions,
                "student_answers": self.student_answers,
                "answered_questions": list(
                    self.answered_questions
                ),
                "question_answer_times": self.question_answer_times,
                "submitted": True,
                "automatic_submission": automatic,
                "submitted_at": submission_time
            }

            exam_data = make_json_safe(exam_data)

            exam_file = os.path.join(
                self.attempt_folder,
                "exam_result.json"
            )

            with open(
                exam_file,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    exam_data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print("========================================")
            print("EXAM RESULT SAVED")
            print("FILE:", exam_file)
            print(
                "MARKS:",
                total_secured_marks,
                "/",
                total_allotted_marks
            )
            print("PERCENTAGE:", final_percentage)
            print("RESULT:", final_result)
            print("========================================")

        except Exception as e:
            print("Could not save exam answers:")
            print(repr(e))


    # ========================================================
    # RETURN TO LOGIN
    # ========================================================

    def return_to_login(self):

        try:

            self.root.destroy()

        except Exception:

            pass


        if self.instructions_window is not None:

            try:

                if self.instructions_window.winfo_exists():

                    self.instructions_window.destroy()

            except Exception:

                pass


        if self.details_window is not None:

            try:

                if self.details_window.winfo_exists():

                    self.details_window.destroy()

            except Exception:

                pass


        if self.login_window is not None:

            try:

                self.login_window.deiconify()

                self.login_window.state(
                    "zoomed"
                )

                self.login_window.after(
                    100,
                    lambda:
                    self.login_window.state(
                        "zoomed"
                    )
                    if self.login_window.winfo_exists()
                    else None
                )

                self.login_window.lift()

                self.login_window.focus_force()

            except Exception as e:

                print(
                    "Could not restore Student Login:"
                )

                print(e)

        else:

            print(
                "WARNING: login_window was not provided."
            )


    # ========================================================
    # BLOCK CLOSE
    # ========================================================

    def block_close(self):

        if self.exam_submitted:

            return


        messagebox.showwarning(
            "Exit Disabled",
            (
                "You cannot close the examination "
                "while the exam is running.\n\n"
                "Please complete and submit the exam."
            ),
            parent=self.root
        )


# ============================================================
# OPEN EXAM
# ============================================================

def open_exam(
    parent_window=None,
    login_window=None,
    details_window=None,
    instructions_window=None
):

    window = tk.Toplevel(
        parent_window
    )


    maximize_window(
        window
    )


    ExamWindow(
        window,
        parent_window=parent_window,
        login_window=login_window,
        details_window=details_window,
        instructions_window=instructions_window
    )


    return window


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()


    exam_window = tk.Toplevel(
        root
    )


    app = ExamWindow(
        exam_window,
        parent_window=root,
        login_window=root,
        details_window=root,
        instructions_window=root
    )


    root.mainloop()
