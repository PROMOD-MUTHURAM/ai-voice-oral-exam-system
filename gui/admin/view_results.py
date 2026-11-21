
import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
from datetime import datetime

# PDF generation
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER


# ============================================================
# PROJECT PATHS
# ============================================================

# view_results.py is inside:
# AI_Oral_Exam_System/gui/admin/
#
# Therefore we go UP THREE levels to reach:
# AI_Oral_Exam_System/

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

BACKEND_DIR = os.path.join(
    BASE_DIR,
    "backend"
)

STUDENT_ANSWERS_DIR = os.path.join(
    BACKEND_DIR,
    "student_answers"
)


# ============================================================
# HELPERS
# ============================================================

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as e:
        print(f"Could not load JSON: {path}")
        print(e)
        return None


def format_number(value):
    try:
        value = float(value)

        if value.is_integer():
            return str(int(value))

        return f"{value:.2f}"

    except Exception:
        return "0"


def format_datetime(value):
    if not value:
        return "Not available"

    try:
        return datetime.fromisoformat(
            str(value).replace("Z", "+00:00")
        ).strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )

    except Exception:
        return str(value)


def get_student_data(result):
    student = result.get("student", {})

    if not isinstance(student, dict):
        student = {}

    return student


def get_student_id(result, folder_name=""):
    student = get_student_data(result)

    value = student.get(
        "student_id",
        result.get("student_id", "")
    )

    value = str(value).strip()

    return value if value else str(folder_name).strip()


def get_student_name(result):
    student = get_student_data(result)

    return str(
        student.get(
            "student_name",
            result.get(
                "student_name",
                "Unknown Student"
            )
        )
    ).strip()


def get_exam_name(result):
    return str(
        result.get(
            "exam_name",
            "AI Oral Examination"
        )
    ).strip()


def get_exam_id(result):
    return str(
        result.get("exam_id", "")
    ).strip()


def get_session_id(result):
    return str(
        result.get("session_id", "")
    ).strip()


def get_attempt_number(result):
    try:
        return int(
            result.get(
                "attempt_number",
                0
            )
        )

    except Exception:
        return 0


def get_total_marks(result):

    # ------------------------------------------------------------
    # FIRST: use saved secured marks ONLY if they are greater than 0
    # ------------------------------------------------------------

    for key in [
        "total_secured_marks",
        "total_secured",
        "marks_secured",
        "total_marks_scored",
        "marks_obtained",
        "score"
    ]:

        if key in result:

            try:

                saved_marks = float(
                    result[key]
                )

                # Do not trust a saved 0 because the old
                # exam_result.json files contain 0 even when
                # the student actually scored marks.
                if saved_marks > 0:

                    return saved_marks

            except Exception:

                pass


    # ------------------------------------------------------------
    # FALLBACK: calculate from question-level saved marks
    # ------------------------------------------------------------

    questions = result.get(
        "questions",
        []
    )

    total = 0.0

    if isinstance(
        questions,
        list
    ):

        for question in questions:

            if not isinstance(
                question,
                dict
            ):

                continue

            for key in [
                "marks_awarded",
                "marks_secured",
                "obtained_marks",
                "score"
            ]:

                if key in question:

                    try:

                        total += float(
                            question[key]
                        )

                        break

                    except Exception:

                        pass


    # ------------------------------------------------------------
    # FINAL FALLBACK:
    # calculate from student answers when question-level
    # awarded marks are also not saved.
    # ------------------------------------------------------------

    if total == 0.0:

        student_answers = result.get(
            "student_answers",
            {}
        )

        if isinstance(
            questions,
            list
        ) and isinstance(
            student_answers,
            dict
        ):

            for index, question in enumerate(
                questions
            ):

                expected = str(
                    question.get(
                        "expected_answer",
                        ""
                    )
                ).strip().lower()

                answer = student_answers.get(
                    str(index),
                    student_answers.get(
                        index,
                        ""
                    )
                )

                answer = str(
                    answer
                    if answer is not None
                    else ""
                ).strip().lower()

                try:

                    allotted = float(
                        question.get(
                            "marks",
                            0
                        )
                    )

                except Exception:

                    allotted = 0.0


                # Exact answer
                if (
                    expected
                    and answer
                    and expected == answer
                ):

                    total += allotted

                    continue


                # Keyword answer
                keywords = question.get(
                    "keywords",
                    []
                )

                if (
                    answer
                    and isinstance(
                        keywords,
                        list
                    )
                ):

                    keyword_found = False

                    for keyword in keywords:

                        keyword = str(
                            keyword
                        ).strip().lower()

                        if (
                            keyword
                            and keyword in answer
                        ):

                            keyword_found = True

                            break


                    if keyword_found:

                        total += allotted


    return total


def get_maximum_marks(result):

    for key in [
        "total_allotted_marks",
        "total_allotted",
        "maximum_marks",
        "max_marks",
        "total_marks",
        "max_score"
    ]:

        if key in result:

            try:
                return float(
                    result[key]
                )

            except Exception:
                pass


    questions = result.get(
        "questions",
        []
    )

    total = 0.0

    if isinstance(
        questions,
        list
    ):

        for question in questions:

            if not isinstance(
                question,
                dict
            ):
                continue

            for key in [
                "marks",
                "allotted_marks",
                "maximum_marks"
            ]:

                if key in question:

                    try:

                        total += float(
                            question[key]
                        )

                        break

                    except Exception:
                        pass

    return total

def get_percentage(result):

    # First use a valid calculated percentage if it exists
    percentage = result.get("percentage")

    try:
        percentage = float(percentage)
    except (TypeError, ValueError):
        percentage = None

    # If stored percentage is greater than 0, use it
    if percentage is not None and percentage > 0:
        return percentage

    # Otherwise calculate from secured marks and maximum marks
    total_marks = get_total_marks(result)
    maximum_marks = get_maximum_marks(result)

    try:
        total_marks = float(total_marks)
        maximum_marks = float(maximum_marks)
    except (TypeError, ValueError):
        return 0.0

    if maximum_marks <= 0:
        return 0.0

    return (total_marks / maximum_marks) * 100

def get_result_status(result):
    percentage = get_percentage(result)

    if percentage >= 50.0:
        return "PASS"

    return "FAIL"



def get_total_questions(result):
    value = result.get("total_questions")

    if value is not None:

        try:
            return int(value)

        except Exception:
            pass

    questions = result.get("questions", [])

    if isinstance(questions, list):
        return len(questions)

    return 0


def get_submission_time(result):
    return result.get(
        "submitted_at",
        result.get(
            "submission_time",
            result.get(
                "submitted_time",
                ""
            )
        )
    )


def get_start_time(result):
    return result.get(
        "start_time",
        result.get(
            "started_at",
            ""
        )
    )


def get_submission_status(result):
    return str(
        result.get(
            "submission_status",
            result.get(
                "status",
                "SUBMITTED"
            )
        )
    ).upper()


# ============================================================
# LOAD RESULTS
# ============================================================

def load_all_results():

    results = []

    print("\n========================================")
    print("VIEW RESULTS - LOADING DATA")
    print("========================================")

    print("view_results.py location:")
    print(os.path.abspath(__file__))

    print("\nBASE_DIR:")
    print(BASE_DIR)

    print("\nBACKEND_DIR:")
    print(BACKEND_DIR)

    print("\nSTUDENT_ANSWERS_DIR:")
    print(STUDENT_ANSWERS_DIR)

    if not os.path.isdir(STUDENT_ANSWERS_DIR):

        print("\nERROR:")
        print("student_answers folder does NOT exist.")
        print("========================================\n")

        return results

    print("\nstudent_answers folder exists.")

    try:
        student_folders = os.listdir(
            STUDENT_ANSWERS_DIR
        )

    except Exception as e:

        print(
            "Could not read student_answers folder:"
        )
        print(e)

        return results

    print("\nStudent folders found:")
    print(student_folders)

    for student_folder in student_folders:

        student_folder_path = os.path.join(
            STUDENT_ANSWERS_DIR,
            student_folder
        )

        if not os.path.isdir(student_folder_path):
            continue

        print("\nStudent folder:")
        print(student_folder_path)

        try:
            attempt_folders = os.listdir(
                student_folder_path
            )

        except Exception as e:

            print(
                "Could not read student folder:"
            )
            print(e)

            continue

        print("Attempt folders:")
        print(attempt_folders)

        for attempt_folder in attempt_folders:

            attempt_folder_path = os.path.join(
                student_folder_path,
                attempt_folder
            )

            if not os.path.isdir(
                attempt_folder_path
            ):
                continue

            result_file = os.path.join(
                attempt_folder_path,
                "exam_result.json"
            )

            print("\nChecking:")
            print(result_file)

            if not os.path.isfile(result_file):

                print(
                    "  -> exam_result.json NOT FOUND"
                )

                continue

            print(
                "  -> exam_result.json FOUND"
            )

            result_data = load_json(
                result_file
            )

            if not isinstance(
                result_data,
                dict
            ):

                print(
                    "  -> Invalid JSON data"
                )

                continue

            print(
                "  -> JSON loaded successfully"
            )

            results.append({
                "folder": attempt_folder_path,
                "student_folder": student_folder,
                "attempt_folder": attempt_folder,
                "file": result_file,
                "data": result_data
            })

    print("\n========================================")
    print(
        "TOTAL RESULTS FOUND:",
        len(results)
    )
    print("========================================\n")

    results.sort(
        key=lambda item: (
            str(
                get_submission_time(
                    item["data"]
                )
            ),
            get_attempt_number(
                item["data"]
            )
        ),
        reverse=True
    )

    return results


# ============================================================
# RANKING
# ============================================================

def build_ranking(results):

    best_by_student = {}

    for item in results:

        data = item["data"]

        student_id = get_student_id(
            data,
            item.get(
                "student_folder",
                ""
            )
        )

        if not student_id:
            student_id = "UNKNOWN"

        key = (
            get_exam_id(data),
            get_exam_name(data),
            get_session_id(data),
            student_id
        )

        score = (
            get_percentage(data),
            get_total_marks(data),
            get_attempt_number(data),
            str(
                get_submission_time(data)
            )
        )

        if key not in best_by_student:

            best_by_student[key] = (
                item,
                score
            )

        else:

            _, current_score = (
                best_by_student[key]
            )

            if score > current_score:

                best_by_student[key] = (
                    item,
                    score
                )

    ranking_items = [
        item
        for item, _
        in best_by_student.values()
    ]

    ranking_items.sort(
        key=lambda item: (
            get_percentage(
                item["data"]
            ),
            get_total_marks(
                item["data"]
            )
        ),
        reverse=True
    )

    ranking = []

    previous_percentage = None
    previous_marks = None
    current_rank = 0

    for index, item in enumerate(
        ranking_items,
        start=1
    ):

        data = item["data"]

        percentage = get_percentage(
            data
        )

        marks = get_total_marks(
            data
        )

        if (
            previous_percentage is None
            or percentage != previous_percentage
            or marks != previous_marks
        ):

            current_rank = index

        ranking.append({
            "rank": current_rank,
            "item": item
        })

        previous_percentage = percentage
        previous_marks = marks

    return ranking


# ============================================================
# VIEW RESULTS
# ============================================================

class ViewResults:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        # ----------------------------------------------------
        # IMPORTANT:
        #
        # ALWAYS CREATE A NEW TOPLEVEL WINDOW.
        #
        # The Admin Control Panel root must NEVER be reused
        # as the View Results window.
        # ----------------------------------------------------

        self.window = root
        self.parent_window = parent_window

        
        self.results = []
        self.filtered_results = []
        self.current_mode = "all"

        # ----------------------------------------------------
        # CONFIGURE WINDOW
        # ----------------------------------------------------

        self.window.title(
            "View Results - Admin Control Panel"
        )

        self.window.configure(
            bg="#f4f6f8"
        )

        self.window.minsize(
            1100,
            700
        )

        self.window.geometry(
            "1200x750"
        )

        # ----------------------------------------------------
        # SHOW THIS WINDOW IN FRONT
        # ----------------------------------------------------

        self.window.update_idletasks()

        try:
            self.window.state("zoomed")

        except Exception:

            try:
                self.window.attributes(
                    "-zoomed",
                    True
                )

            except Exception:
                pass

        # ----------------------------------------------------
        # ADMIN PANEL STAYS BEHIND
        # ----------------------------------------------------

        if (
            self.parent_window is not None
            and self.parent_window.winfo_exists()
        ):

            try:
                self.parent_window.withdraw()

            except Exception:
                pass

        # ----------------------------------------------------
        # WINDOW CLOSE
        # ----------------------------------------------------

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.go_back
        )

    
        # ----------------------------------------------------
        # CREATE INTERFACE
        # ----------------------------------------------------

        self.create_interface()

        self.show_loading()

        self.window.after(
            100,
            self.load_results_after_loading
        )


    # ========================================================
    # LOADING SCREEN
    # ========================================================

    def show_loading(self):

        # Remove anything currently inside the window
        for widget in self.window.winfo_children():
            widget.destroy()

        loading_frame = tk.Frame(
            self.window,
            bg="#f4f6f8"
        )

        loading_frame.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            loading_frame,
            text="VIEW RESULTS",
            font=("Arial", 28, "bold"),
            bg="#f4f6f8",
            fg="#1f2937"
        ).pack(
            pady=(200, 20)
        )

        tk.Label(
            loading_frame,
            text="Loading student results...",
            font=("Arial", 14),
            bg="#f4f6f8",
            fg="#6b7280"
        ).pack(
            pady=10
        )

        self.loading_bar = ttk.Progressbar(
            loading_frame,
            mode="indeterminate",
            length=350
        )

        self.loading_bar.pack(
            pady=20
        )

        self.loading_bar.start(10)

        # Force the loading screen to appear immediately
        self.window.update_idletasks()


    # ========================================================
    # LOAD RESULTS AFTER LOADING SCREEN IS VISIBLE
    # ========================================================

    def load_results_after_loading(self):

        try:

            # Stop progress bar
            if hasattr(
                self,
                "loading_bar"
            ):

                self.loading_bar.stop()

            # Remove loading screen
            for widget in self.window.winfo_children():
                widget.destroy()

            # Re-create the actual View Results interface
            self.create_interface()

            # Load the results
            self.load_results()

        except Exception as e:

            messagebox.showerror(
                "View Results Error",
                f"Could not load View Results.\n\n{e}",
                parent=self.window
            )


    # ========================================================
    # CLOSE WINDOW
    # ========================================================

    def go_back(self):

        try:

            if self.window.winfo_exists():
                self.window.destroy()

        except Exception:
            pass

        try:

            if (
                self.parent_window is not None
                and self.parent_window.winfo_exists()
            ):

                self.parent_window.deiconify()
                self.parent_window.state("zoomed")
                self.parent_window.lift()
                self.parent_window.focus_force()

        except Exception:
            pass


        
        # ----------------------------------------------------
        # BRING VIEW RESULTS TO FRONT
        # ----------------------------------------------------

        try:
            self.window.lift()
            self.window.focus_force()

        except Exception:
            pass


    # ========================================================
    # INTERFACE
    # ========================================================

    def create_interface(self):

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            self.window,
            bg="#1f2937",
            height=80
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="STUDENT RESULTS",
            font=("Arial", 23, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            side="left",
            padx=25
        )

        self.count_label = tk.Label(
            header,
            text="",
            font=("Arial", 11),
            bg="#1f2937",
            fg="#d1d5db"
        )

        self.count_label.pack(
            side="left",
            padx=15
        )

        # ----------------------------------------------------
        # FILTER BAR
        # ----------------------------------------------------

        filter_frame = tk.Frame(
            self.window,
            bg="#f4f6f8"
        )

        filter_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )

        tk.Label(
            filter_frame,
            text="Exam:",
            font=("Arial", 10, "bold"),
            bg="#f4f6f8",
            fg="#374151"
        ).pack(
            side="left"
        )

        self.exam_combo = ttk.Combobox(
            filter_frame,
            state="readonly",
            width=35
        )

        self.exam_combo.pack(
            side="left",
            padx=(8, 20)
        )

        tk.Label(
            filter_frame,
            text="Session:",
            font=("Arial", 10, "bold"),
            bg="#f4f6f8",
            fg="#374151"
        ).pack(
            side="left"
        )

        self.session_combo = ttk.Combobox(
            filter_frame,
            state="readonly",
            width=25
        )

        self.session_combo.pack(
            side="left",
            padx=8
        )

        self.exam_combo.bind(
            "<<ComboboxSelected>>",
            lambda event:
                self.apply_filters()
        )

        self.session_combo.bind(
            "<<ComboboxSelected>>",
            lambda event:
                self.apply_filters()
        )

        tk.Button(
            filter_frame,
            text="CLEAR FILTERS",
            font=("Arial", 10, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2",
            command=self.clear_filters
        ).pack(
            side="left",
            padx=10
        )

        tk.Button(
            filter_frame,
            text="REFRESH",
            font=("Arial", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2",
            command=self.load_results
        ).pack(
            side="left",
            padx=5
        )

        # ----------------------------------------------------
        # MODE BUTTONS
        # ----------------------------------------------------

        mode_frame = tk.Frame(
            self.window,
            bg="#f4f6f8"
        )

        mode_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 10)
        )

        self.all_button = tk.Button(
            mode_frame,
            text="ALL RESULTS",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.show_all_results
        )

        self.all_button.pack(
            side="left",
            padx=(0, 8)
        )

        self.ranking_button = tk.Button(
            mode_frame,
            text="RANKING",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.show_ranking
        )

        self.ranking_button.pack(
            side="left"
        )

        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        table_frame = tk.Frame(
            self.window,
            bg="white",
            bd=1,
            relief="solid"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 15)
        )

        columns = (
            "rank",
            "student_id",
            "student_name",
            "exam",
            "attempt",
            "marks",
            "percentage",
            "submitted"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "rank": "Rank",
            "student_id": "Student ID",
            "student_name": "Student Name",
            "exam": "Exam",
            "attempt": "Attempt",
            "marks": "Marks",
            "percentage": "Percentage",
            "submitted": "Submitted At"
        }

        widths = {
            "rank": 70,
            "student_id": 130,
            "student_name": 180,
            "exam": 220,
            "attempt": 80,
            "marks": 110,
            "percentage": 110,
            "submitted": 190
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        scrollbar_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.grid_rowconfigure(
            0,
            weight=1
        )

        table_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.tree.bind(
            "<Double-1>",
            self.open_selected_result
        )

        # ----------------------------------------------------
        # BOTTOM BAR
        # ----------------------------------------------------

        bottom_frame = tk.Frame(
            self.window,
            bg="#f4f6f8"
        )

        bottom_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        tk.Button(
            bottom_frame,
            text="VIEW DETAILS",
            font=("Arial", 11, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            bd=0,
            padx=25,
            pady=10,
            cursor="hand2",
            command=self.open_selected_result
        ).pack(
            side="left"
        )

        tk.Button(
            bottom_frame,
            text="← BACK TO ADMIN PANEL",
            font=("Arial", 11, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            bd=0,
            padx=25,
            pady=10,
            cursor="hand2",
            command=self.go_back
        ).pack(
            side="right"
        )

    # ========================================================
    # LOAD
    # ========================================================

    def load_results(self):

        self.results = load_all_results()

        self.populate_filters()

        self.apply_filters()

    # ========================================================
    # FILTERS
    # ========================================================

    def populate_filters(self):

        exams = set()
        sessions = set()

        for item in self.results:

            data = item["data"]

            exam_id = get_exam_id(data)
            exam_name = get_exam_name(data)

            if exam_id:

                exams.add(
                    f"{exam_id} | {exam_name}"
                )

            else:

                exams.add(
                    exam_name
                )

            session_id = get_session_id(data)

            if session_id:
                sessions.add(session_id)

        exam_values = ["All Exams"]
        exam_values.extend(
            sorted(exams)
        )

        session_values = ["All Sessions"]
        session_values.extend(
            sorted(sessions)
        )

        self.exam_combo["values"] = (
            exam_values
        )

        self.session_combo["values"] = (
            session_values
        )

        self.exam_combo.current(0)
        self.session_combo.current(0)

    # ========================================================
    # APPLY FILTERS
    # ========================================================

    def apply_filters(self):

        selected_exam = (
            self.exam_combo.get()
        )

        selected_session = (
            self.session_combo.get()
        )

        filtered = []

        for item in self.results:

            data = item["data"]

            if (
                selected_exam
                and selected_exam != "All Exams"
            ):

                exam_id = get_exam_id(data)
                exam_name = get_exam_name(data)

                if exam_id:

                    exam_display = (
                        f"{exam_id} | {exam_name}"
                    )

                else:

                    exam_display = exam_name

                if exam_display != selected_exam:
                    continue

            if (
                selected_session
                and selected_session != "All Sessions"
            ):

                if (
                    get_session_id(data)
                    != selected_session
                ):
                    continue

            filtered.append(item)

        self.filtered_results = filtered

        if self.current_mode == "ranking":

            self.display_ranking()

        else:

            self.display_all()

    # ========================================================
    # CLEAR FILTERS
    # ========================================================

    def clear_filters(self):

        if self.exam_combo["values"]:
            self.exam_combo.current(0)

        if self.session_combo["values"]:
            self.session_combo.current(0)

        self.apply_filters()

    # ========================================================
    # MODES
    # ========================================================

    def show_all_results(self):

        self.current_mode = "all"

        self.all_button.configure(
            bg="#2563eb"
        )

        self.ranking_button.configure(
            bg="#6b7280"
        )

        self.display_all()

    def show_ranking(self):

        self.current_mode = "ranking"

        self.all_button.configure(
            bg="#6b7280"
        )

        self.ranking_button.configure(
            bg="#2563eb"
        )

        self.display_ranking()

    # ========================================================
    # CLEAR TABLE
    # ========================================================

    def clear_table(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

    # ========================================================
    # DISPLAY ALL
    # ========================================================

    def display_all(self):

        self.clear_table()

        for item in self.filtered_results:

            data = item["data"]

            student_id = get_student_id(
                data,
                item.get(
                    "student_folder",
                    ""
                )
            )

            student_name = get_student_name(
                data
            )

            exam_name = get_exam_name(
                data
            )

            attempt = get_attempt_number(
                data
            )

            marks = get_total_marks(
                data
            )

            maximum = get_maximum_marks(
                data
            )

            percentage = get_percentage(
                data
            )

            submitted = format_datetime(
                get_submission_time(data)
            )

            marks_text = (
                f"{format_number(marks)} / "
                f"{format_number(maximum)}"
            )

            self.tree.insert(
                "",
                "end",
                values=(
                    "",
                    student_id,
                    student_name,
                    exam_name,
                    attempt,
                    marks_text,
                    f"{percentage:.2f}%",
                    submitted
                ),
                tags=(item["file"],)
            )

        self.count_label.configure(
            text=(
                f"{len(self.filtered_results)} "
                f"submitted attempts"
            )
        )

    # ========================================================
    # DISPLAY RANKING
    # ========================================================

    def display_ranking(self):

        self.clear_table()

        ranking = build_ranking(
            self.filtered_results
        )

        for entry in ranking:

            item = entry["item"]

            data = item["data"]

            student_id = get_student_id(
                data,
                item.get(
                    "student_folder",
                    ""
                )
            )

            student_name = get_student_name(
                data
            )

            exam_name = get_exam_name(
                data
            )

            attempt = get_attempt_number(
                data
            )

            marks = get_total_marks(
                data
            )

            maximum = get_maximum_marks(
                data
            )

            percentage = get_percentage(
                data
            )

            submitted = format_datetime(
                get_submission_time(data)
            )

            marks_text = (
                f"{format_number(marks)} / "
                f"{format_number(maximum)}"
            )

            self.tree.insert(
                "",
                "end",
                values=(
                    entry["rank"],
                    student_id,
                    student_name,
                    exam_name,
                    attempt,
                    marks_text,
                    f"{percentage:.2f}%",
                    submitted
                ),
                tags=(item["file"],)
            )

        self.count_label.configure(
            text=(
                f"{len(ranking)} students "
                f"in ranking"
            )
        )

    # ========================================================
    # SELECTED RESULT
    # ========================================================

    def get_selected_file(self):

        selection = self.tree.selection()

        if not selection:

            messagebox.showwarning(
                "No Selection",
                "Please select a result first.",
                parent=self.window
            )

            return None

        tags = self.tree.item(
            selection[0],
            "tags"
        )

        if not tags:
            return None

        return tags[0]

    # ========================================================
    # OPEN DETAILS
    # ========================================================

    def open_selected_result(
        self,
        event=None
    ):

        file_path = self.get_selected_file()

        if not file_path:
            return

        result_data = load_json(
            file_path
        )

        if not isinstance(
            result_data,
            dict
        ):

            messagebox.showerror(
                "Result Error",
                "Could not read the selected result.",
                parent=self.window
            )

            return

        self.show_result_details(
            result_data,
            file_path
        )


    # ========================================================
    # DOWNLOAD RESULT DETAILS AS PDF
    # ========================================================

    def download_result_details(self, data):

        try:

            # ------------------------------------------------
            # WINDOWS DOWNLOADS FOLDER
            # ------------------------------------------------

            downloads_folder = os.path.join(
                os.path.expanduser("~"),
                "Downloads"
            )

            # Create Downloads folder if it does not exist
            os.makedirs(
                downloads_folder,
                exist_ok=True
            )

            # ------------------------------------------------
            # STUDENT / EXAM INFORMATION
            # ------------------------------------------------

            student = get_student_data(data)

            student_id = get_student_id(data)
            student_name = get_student_name(data)
            exam_name = get_exam_name(data)
            exam_id = get_exam_id(data)
            session_id = get_session_id(data)

            attempt = get_attempt_number(data)

            marks = get_total_marks(data)
            maximum = get_maximum_marks(data)
            percentage = get_percentage(data)

            # ------------------------------------------------
            # PASS / FAIL RESULT
            # PASS if percentage is 50% or higher
            # ------------------------------------------------

            pass_percentage = 50.0

            result = (
                "PASS"
                if percentage >= pass_percentage
                else "FAIL"
            )
                        

            # ------------------------------------------------
            # SAFE FILE NAME
            # ------------------------------------------------

            safe_student_name = "".join(
                c for c in student_name
                if c.isalnum() or c in (" ", "_", "-")
            ).strip()

            safe_student_name = (
                safe_student_name
                .replace(" ", "_")
            )

            if not safe_student_name:
                safe_student_name = "Student"

            file_name = (
                f"{safe_student_name}_"
                f"{student_id}_"
                f"Result.pdf"
            )

            pdf_path = os.path.join(
                downloads_folder,
                file_name
            )

            # ------------------------------------------------
            # PDF DOCUMENT
            # ------------------------------------------------

            document = SimpleDocTemplate(
                pdf_path,
                pagesize=A4,
                rightMargin=35,
                leftMargin=35,
                topMargin=35,
                bottomMargin=35
            )

            styles = getSampleStyleSheet()

            title_style = ParagraphStyle(
                "ResultTitle",
                parent=styles["Title"],
                fontSize=20,
                leading=24,
                alignment=TA_CENTER,
                spaceAfter=15
            )

            section_style = ParagraphStyle(
                "Section",
                parent=styles["Heading2"],
                fontSize=13,
                leading=16,
                textColor=colors.white,
                backColor=colors.HexColor("#1f2937"),
                spaceBefore=12,
                spaceAfter=8,
                leftIndent=5,
                rightIndent=5
            )

            normal_style = ParagraphStyle(
                "NormalResult",
                parent=styles["Normal"],
                fontSize=9,
                leading=13
            )

            question_style = ParagraphStyle(
                "Question",
                parent=styles["Heading3"],
                fontSize=11,
                leading=14,
                textColor=colors.HexColor("#2563eb"),
                spaceBefore=8,
                spaceAfter=6
            )

            story = []

            # ------------------------------------------------
            # TITLE
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "STUDENT RESULT DETAILS",
                    title_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Generated:</b> "
                    f"{datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}",
                    normal_style
                )
            )

            story.append(
                Spacer(1, 10)
            )

            # ------------------------------------------------
            # STUDENT INFORMATION
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "STUDENT INFORMATION",
                    section_style
                )
            )

            student_data = [
                ["Student ID", student_id],
                ["Student Name", student_name],
                ["Course", student.get("course", "")],
                ["Department", student.get("department", "")],
                ["Date of Birth", student.get("date_of_birth", "")],
                ["Age", student.get("age", "")],
                ["Gender", student.get("gender", "")],
                ["Email", student.get("email", "")],
                [
                    "Phone",
                    student.get(
                        "phone",
                        student.get(
                            "mobile_number",
                            ""
                        )
                    )
                ]
            ]

            student_data = [
                row
                for row in student_data
                if str(row[1]).strip()
            ]

            table = Table(
                student_data,
                colWidths=[140, 360]
            )

            table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.HexColor("#e5e7eb")
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (0, -1),
                        "Helvetica-Bold"
                    ),
                    (
                        "FONTNAME",
                        (1, 0),
                        (1, -1),
                        "Helvetica"
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        9
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        7
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6
                    )
                ])
            )

            story.append(table)

            # ------------------------------------------------
            # EXAMINATION INFORMATION
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "EXAMINATION INFORMATION",
                    section_style
                )
            )

            exam_data = [
                ["Exam ID", exam_id],
                ["Exam Name", exam_name],
                ["Session ID", session_id],
                [
                    "Pattern ID",
                    data.get("pattern_id", "")
                ],
                [
                    "Pattern Name",
                    data.get("pattern_name", "")
                ],
                ["Attempt Number", attempt],
                [
                    "Start Time",
                    format_datetime(
                        get_start_time(data)
                    )
                ],
                [
                    "Submission Time",
                    format_datetime(
                        get_submission_time(data)
                    )
                ],
                [
                    "Submission Status",
                    get_submission_status(data)
                ]
            ]

            exam_data = [
                [str(a), str(b)]
                for a, b in exam_data
                if str(b).strip()
            ]

            table = Table(
                exam_data,
                colWidths=[140, 360]
            )

            table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.HexColor("#e5e7eb")
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (0, -1),
                        "Helvetica-Bold"
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        9
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    )
                ])
            )

            story.append(table)

            # ------------------------------------------------
            # FINAL RESULT
            # ------------------------------------------------

            story.append(
                Paragraph(
                    "FINAL RESULT",
                    section_style
                )
            )

            final_data = [
                [
                    "Total Questions",
                    str(get_total_questions(data))
                ],
                [
                    "Marks Scored",
                    (
                        f"{format_number(marks)} / "
                        f"{format_number(maximum)}"
                    )
                ],
                [
                    "Percentage",
                    f"{percentage:.2f}%"
                ],
                [
                    "Pass Percentage",
                    f"{pass_percentage:.2f}%"
                ],
                [
                    "Result",
                    result
                ]
            ]

            
            table = Table(
                final_data,
                colWidths=[140, 360]
            )

            table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.HexColor("#e5e7eb")
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (0, -1),
                        "Helvetica-Bold"
                    ),
                    (
                        "FONTNAME",
                        (1, 0),
                        (1, -1),
                        "Helvetica-Bold"
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        10
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    )
                ])
            )

            story.append(table)

            # ------------------------------------------------
            # EVALUATION / FEEDBACK
            # ------------------------------------------------

            evaluation = data.get(
                "evaluation",
                data.get(
                    "feedback",
                    ""
                )
            )

            if evaluation:

                story.append(
                    Paragraph(
                        "EVALUATION / FEEDBACK",
                        section_style
                    )
                )

                story.append(
                    Paragraph(
                        str(evaluation),
                        normal_style
                    )
                )

            # ------------------------------------------------
            # QUESTION-WISE RESULT
            # ------------------------------------------------

            questions = data.get(
                "questions",
                []
            )

            student_answers = data.get(
                "student_answers",
                {}
            )

            if isinstance(questions, list):

                story.append(
                    Paragraph(
                        "QUESTION-WISE RESULT",
                        section_style
                    )
                )

                for index, question in enumerate(
                    questions
                ):

                    if not isinstance(
                        question,
                        dict
                    ):
                        continue

                    question_number = index + 1

                    question_text = question.get(
                        "question",
                        question.get(
                            "text",
                            ""
                        )
                    )

                    expected = question.get(
                        "expected_answer",
                        question.get(
                            "correct_answer",
                            question.get(
                                "answer",
                                ""
                            )
                        )
                    )

                    answer = ""

                    if isinstance(
                        student_answers,
                        dict
                    ):

                        answer = student_answers.get(
                            str(index),
                            student_answers.get(
                                index,
                                ""
                            )
                        )

                    marks_awarded = question.get(
                        "marks_awarded",
                        question.get(
                            "marks_secured",
                            question.get(
                                "obtained_marks",
                                question.get(
                                    "score",
                                    ""
                                )
                            )
                        )
                    )

                    allotted_marks = question.get(
                        "marks",
                        question.get(
                            "allotted_marks",
                            ""
                        )
                    )

                    question_data = [
                        [
                            "Question",
                            question_text
                        ],
                        [
                            "Question Type",
                            question.get(
                                "question_type",
                                question.get(
                                    "type",
                                    ""
                                )
                            )
                        ],
                        [
                            "Correct / Expected Answer",
                            expected
                        ],
                        [
                            "Student Answer",
                            answer
                        ],
                        [
                            "Marks",
                            (
                                f"{format_number(marks_awarded)} / "
                                f"{format_number(allotted_marks)}"
                            )
                        ]
                    ]

                    similarity = question.get(
                        "similarity",
                        question.get(
                            "semantic_similarity",
                            ""
                        )
                    )

                    if similarity != "":

                        try:
                            similarity_text = (
                                f"{float(similarity):.2f}%"
                            )
                        except Exception:
                            similarity_text = str(
                                similarity
                            )

                        question_data.append(
                            [
                                "Similarity",
                                similarity_text
                            ]
                        )

                    question_evaluation = question.get(
                        "evaluation",
                        question.get(
                            "feedback",
                            ""
                        )
                    )

                    if question_evaluation:

                        question_data.append(
                            [
                                "Evaluation",
                                question_evaluation
                            ]
                        )

                    story.append(
                        Paragraph(
                            f"QUESTION {question_number}",
                            question_style
                        )
                    )

                    question_table = Table(
                        [
                            [
                                Paragraph(
                                    str(label),
                                    normal_style
                                ),
                                Paragraph(
                                    str(value),
                                    normal_style
                                )
                            ]
                            for label, value
                            in question_data
                        ],
                        colWidths=[150, 350]
                    )

                    question_table.setStyle(
                        TableStyle([
                            (
                                "BACKGROUND",
                                (0, 0),
                                (0, -1),
                                colors.HexColor("#f3f4f6")
                            ),
                            (
                                "FONTNAME",
                                (0, 0),
                                (0, -1),
                                "Helvetica-Bold"
                            ),
                            (
                                "GRID",
                                (0, 0),
                                (-1, -1),
                                0.5,
                                colors.grey
                            ),
                            (
                                "VALIGN",
                                (0, 0),
                                (-1, -1),
                                "TOP"
                            ),
                            (
                                "FONTSIZE",
                                (0, 0),
                                (-1, -1),
                                9
                            ),
                            (
                                "LEFTPADDING",
                                (0, 0),
                                (-1, -1),
                                6
                            ),
                            (
                                "RIGHTPADDING",
                                (0, 0),
                                (-1, -1),
                                6
                            ),
                            (
                                "TOPPADDING",
                                (0, 0),
                                (-1, -1),
                                6
                            ),
                            (
                                "BOTTOMPADDING",
                                (0, 0),
                                (-1, -1),
                                6
                            )
                        ])
                    )

                    story.append(
                        question_table
                    )

                    story.append(
                        Spacer(1, 8)
                    )

            # ------------------------------------------------
            # BUILD PDF
            # ------------------------------------------------

            document.build(story)

            # ------------------------------------------------
            # SUCCESS MESSAGE
            # ------------------------------------------------

            messagebox.showinfo(
                "Download Complete",
                (
                    "Result details downloaded successfully.\n\n"
                    f"Saved to:\n{pdf_path}"
                )
            )

            # ------------------------------------------------
            # OPEN DOWNLOADS FOLDER
            # ------------------------------------------------

            try:

                os.startfile(
                    downloads_folder
                )

            except Exception:
                pass

        except Exception as e:

            messagebox.showerror(
                "Download Error",
                (
                    "Could not download the result details.\n\n"
                    f"Error:\n{e}"
                )
            )


    # ========================================================
    # RESULT DETAILS
    # ========================================================

    def show_result_details(
        self,
        data,
        file_path
    ):

        window = tk.Toplevel(
            self.window
        )

        window.title(
            "Result Details"
        )

        window.configure(
            bg="#f4f6f8"
        )

        window.minsize(
            900,
            650
        )

        window.geometry(
            "1100x800"
        )

        window.update_idletasks()

        try:

            window.state(
                "zoomed"
            )

        except Exception:

            try:

                window.attributes(
                    "-zoomed",
                    True
                )

            except Exception:
                pass

        window.protocol(
            "WM_DELETE_WINDOW",
            window.destroy
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            window,
            bg="#1f2937",
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="RESULT DETAILS",
            font=("Arial", 20, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            side="left",
            padx=20
        )

        # ----------------------------------------------------
        # SCROLLABLE AREA
        # ----------------------------------------------------

        outer = tk.Frame(
            window,
            bg="#f4f6f8"
        )

        outer.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        canvas = tk.Canvas(
            outer,
            bg="#f4f6f8",
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            outer,
            orient="vertical",
            command=canvas.yview
        )

        frame = tk.Frame(
            canvas,
            bg="#f4f6f8"
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=frame,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        frame.bind(
            "<Configure>",
            lambda event:
                canvas.configure(
                    scrollregion=
                    canvas.bbox("all")
                )
        )

        canvas.bind(
            "<Configure>",
            lambda event:
                canvas.itemconfig(
                    canvas_window,
                    width=event.width
                )
        )

        # ----------------------------------------------------
        # STUDENT
        # ----------------------------------------------------

        student = get_student_data(
            data
        )

        self.add_section(
            frame,
            "STUDENT INFORMATION"
        )

        student_fields = [

            (
                "Student ID",
                get_student_id(data)
            ),

            (
                "Student Name",
                get_student_name(data)
            ),

            (
                "Course",
                student.get(
                    "course",
                    data.get(
                        "course",
                        ""
                    )
                )
            ),

            (
                "Department",
                student.get(
                    "department",
                    data.get(
                        "department",
                        ""
                    )
                )
            ),

            (
                "Date of Birth",
                student.get(
                    "date_of_birth",
                    data.get(
                        "date_of_birth",
                        ""
                    )
                )
            ),

            (
                "Age",
                student.get(
                    "age",
                    data.get(
                        "age",
                        ""
                    )
                )
            ),

            (
                "Gender",
                student.get(
                    "gender",
                    data.get(
                        "gender",
                        ""
                    )
                )
            ),

            (
                "Email",
                student.get(
                    "email",
                    data.get(
                        "email",
                        ""
                    )
                )
            ),

            (
                "Phone",
                student.get(
                    "phone",
                    data.get(
                        "phone",
                        data.get(
                            "mobile_number",
                            ""
                        )
                    )
                )
            )
        ]

        for label, value in student_fields:

            if str(value).strip():

                self.add_info_row(
                    frame,
                    label,
                    value
                )

        # ----------------------------------------------------
        # EXAMINATION
        # ----------------------------------------------------

        self.add_section(
            frame,
            "EXAMINATION INFORMATION"
        )

        exam_fields = [

            (
                "Exam ID",
                get_exam_id(data)
            ),

            (
                "Exam Name",
                get_exam_name(data)
            ),

            (
                "Session ID",
                get_session_id(data)
            ),

            (
                "Pattern ID",
                data.get(
                    "pattern_id",
                    ""
                )
            ),

            (
                "Pattern Name",
                data.get(
                    "pattern_name",
                    ""
                )
            ),

            (
                "Attempt Number",
                get_attempt_number(data)
            ),

            (
                "Start Time",
                format_datetime(
                    get_start_time(data)
                )
            ),

            (
                "Submission Time",
                format_datetime(
                    get_submission_time(data)
                )
            ),

            (
                "Submission Status",
                get_submission_status(data)
            )
        ]

        for label, value in exam_fields:

            self.add_info_row(
                frame,
                label,
                value
            )

        # ----------------------------------------------------
        # FINAL RESULT
        # ----------------------------------------------------

        self.add_section(
            frame,
            "FINAL RESULT"
        )

        marks = get_total_marks(
            data
        )

        maximum = get_maximum_marks(
            data
        )

        percentage = get_percentage(
            data
        )

        self.add_info_row(
            frame,
            "Total Questions",
            get_total_questions(data)
        )

        self.add_info_row(
            frame,
            "Marks Scored",
            (
                f"{format_number(marks)} / "
                f"{format_number(maximum)}"
            )
        )

        self.add_info_row(
            frame,
            "Percentage",
            f"{percentage:.2f}%"
        )

        self.add_info_row(
            frame,
            "Result",
            get_result_status(data)
        )        

        evaluation = data.get(
            "evaluation",
            data.get(
                "feedback",
                ""
            )
        )

        if evaluation:

            self.add_info_row(
                frame,
                "Evaluation / Feedback",
                evaluation
            )

        # ----------------------------------------------------
        # QUESTIONS
        # ----------------------------------------------------

        questions = data.get(
            "questions",
            []
        )

        student_answers = data.get(
            "student_answers",
            {}
        )

        if (
            isinstance(
                questions,
                list
            )
            and questions
        ):

            self.add_section(
                frame,
                "QUESTION-WISE RESULT"
            )

            for index, question in enumerate(
                questions
            ):

                if not isinstance(
                    question,
                    dict
                ):
                    continue

                self.add_question_detail(
                    frame,
                    index + 1,
                    question,
                    student_answers
                )

        # ----------------------------------------------------
        # ANSWER SCRIPT
        # ----------------------------------------------------

        answer_script = data.get(
            "answer_script_path",
            data.get(
                "answer_script",
                data.get(
                    "answer_script_location",
                    ""
                )
            )
        )

        if answer_script:

            self.add_section(
                frame,
                "ANSWER SCRIPT"
            )

            self.add_info_row(
                frame,
                "Location",
                answer_script
            )

        # ----------------------------------------------------
        # BACKEND STORAGE
        # ----------------------------------------------------

        self.add_section(
            frame,
            "BACKEND STORAGE"
        )

        self.add_info_row(
            frame,
            "Result File",
            file_path
        )

        # ----------------------------------------------------
        # BOTTOM BUTTONS
        # ----------------------------------------------------

        bottom_buttons = tk.Frame(
            window,
            bg="#f4f6f8"
        )

        bottom_buttons.pack(
            fill="x",
            pady=(0, 20)
        )

        # DOWNLOAD RESULT
        tk.Button(
            bottom_buttons,
            text="⬇ DOWNLOAD RESULT",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2",
            command=lambda:
                self.download_result_details(data)
        ).pack(
            side="left",
            padx=(0, 10)
        )

        # BACK TO RESULTS
        tk.Button(
            bottom_buttons,
            text="← BACK TO RESULTS",
            font=("Arial", 11, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            bd=0,
            padx=30,
            pady=10,
            cursor="hand2",
            command=window.destroy
        ).pack(
            side="left"
        )

        
    # ========================================================
    # SECTION
    # ========================================================

    def add_section(
        self,
        parent,
        title
    ):

        frame = tk.Frame(
            parent,
            bg="#1f2937",
            padx=15,
            pady=10
        )

        frame.pack(
            fill="x",
            pady=(15, 5)
        )

        tk.Label(
            frame,
            text=title,
            font=("Arial", 13, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            anchor="w"
        )

    # ========================================================
    # INFO ROW
    # ========================================================

    def add_info_row(
        self,
        parent,
        label,
        value
    ):

        frame = tk.Frame(
            parent,
            bg="white",
            padx=15,
            pady=10
        )

        frame.pack(
            fill="x",
            pady=2
        )

        tk.Label(
            frame,
            text=f"{label}:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151",
            width=25,
            anchor="w"
        ).pack(
            side="left",
            anchor="nw"
        )

        tk.Label(
            frame,
            text=str(value),
            font=("Arial", 10),
            bg="white",
            fg="#111827",
            anchor="w",
            justify="left",
            wraplength=900
        ).pack(
            side="left",
            fill="x",
            expand=True
        )

    # ========================================================
    # QUESTION DETAIL
    # ========================================================


    def add_question_detail(
        self,
        parent,
        number,
        question,
        student_answers
    ):

        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )

        card.pack(
            fill="x",
            pady=7
        )

        tk.Label(
            card,
            text=f"QUESTION {number}",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#2563eb"
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        question_text = question.get(
            "question",
            question.get(
                "text",
                ""
            )
        )

        self.add_info_row(
            card,
            "Question",
            question_text
        )

        question_type = question.get(
            "question_type",
            question.get(
                "type",
                ""
            )
        )

        if question_type:

            self.add_info_row(
                card,
                "Question Type",
                question_type
            )

        expected = question.get(
            "expected_answer",
            question.get(
                "correct_answer",
                question.get(
                    "answer",
                    ""
                )
            )
        )

        self.add_info_row(
            card,
            "Correct / Expected Answer",
            expected
        )

        # ----------------------------------------------------
        # GET STUDENT ANSWER
        # ----------------------------------------------------

        answer = ""

        if isinstance(
            student_answers,
            dict
        ):

            answer = student_answers.get(
                number - 1,
                student_answers.get(
                    str(number - 1),
                    student_answers.get(
                        number,
                        student_answers.get(
                            str(number),
                            ""
                        )
                    )
                )
            )

        if answer is None:
            answer = ""

        self.add_info_row(
            card,
            "Student Answer",
            answer
            if str(answer).strip()
            else "No answer recorded."
        )

        # ----------------------------------------------------
        # ALLOTTED MARKS
        # ----------------------------------------------------

        allotted = question.get(
            "marks",
            question.get(
                "allotted_marks",
                question.get(
                    "maximum_marks",
                    0
                )
            )
        )

        try:
            allotted = float(allotted)
        except Exception:
            allotted = 0.0

        # ----------------------------------------------------
        # SECURED MARKS
        #
        # First use any saved secured/awarded value.
        # If it does not exist, calculate from similarity.
        # ----------------------------------------------------

        marks = None

        for key in [
            "marks_awarded",
            "marks_secured",
            "obtained_marks",
            "score"
        ]:

            if key in question:

                try:

                    marks = float(
                        question[key]
                    )

                    break

                except Exception:

                    pass

        # ----------------------------------------------------
        # SIMILARITY
        # ----------------------------------------------------

        similarity = question.get(
            "similarity",
            question.get(
                "semantic_similarity",
                ""
            )
        )

        try:

            similarity_value = float(
                similarity
            )

        except Exception:

            similarity_value = None

        # ----------------------------------------------------
        # CALCULATE MARKS WHEN NOT SAVED
        # ----------------------------------------------------

        if marks is None:

            # Exact normalized answer match
            expected_text = str(
                expected
                if expected is not None
                else ""
            ).strip().lower()

            student_text = str(
                answer
                if answer is not None
                else ""
            ).strip().lower()

            if (
                expected_text
                and student_text
                and expected_text == student_text
            ):

                similarity_value = 100.0

            # Keyword match for one-word questions
            elif (
                student_text
                and isinstance(
                    question.get(
                        "keywords",
                        []
                    ),
                    list
                )
            ):

                keywords = question.get(
                    "keywords",
                    []
                )

                keyword_match = False

                for keyword in keywords:

                    keyword_text = str(
                        keyword
                    ).strip().lower()

                    if (
                        keyword_text
                        and keyword_text
                        in student_text
                    ):

                        keyword_match = True

                        break

                if keyword_match:

                    similarity_value = 100.0

            # Otherwise use saved similarity if available
            if similarity_value is None:

                similarity_value = 0.0

            # Same rule used for 1-mark questions:
            # 75% or above = full mark.
            if allotted == 1.0:

                if similarity_value >= 75.0:

                    marks = 1.0

                else:

                    marks = 0.0

            else:

                if similarity_value >= 75.0:

                    marks = allotted

                elif similarity_value >= 50.0:

                    marks = allotted * 0.50

                elif similarity_value >= 35.0:

                    marks = allotted * 0.25

                else:

                    marks = 0.0

        # ----------------------------------------------------
        # MARKS DISPLAY
        # ----------------------------------------------------

        self.add_info_row(
            card,
            "Marks",
            (
                f"{format_number(marks)} / "
                f"{format_number(allotted)}"
            )
        )

        # ----------------------------------------------------
        # SIMILARITY DISPLAY
        # ----------------------------------------------------

        if similarity_value is not None:

            self.add_info_row(
                card,
                "Similarity",
                f"{similarity_value:.2f}%"
            )

        # ----------------------------------------------------
        # EVALUATION
        # ----------------------------------------------------

        evaluation = question.get(
            "evaluation",
            question.get(
                "feedback",
                ""
            )
        )

        if not evaluation:

            if marks >= allotted and allotted > 0:

                evaluation = "CORRECT"

            elif marks > 0:

                evaluation = "PARTIALLY CORRECT"

            else:

                evaluation = "INCORRECT"

        self.add_info_row(
            card,
            "Evaluation",
            evaluation
        )



# ============================================================
# OPEN FUNCTION
# ============================================================


def open_view_results(parent=None):

    if parent is None:
        root = tk.Tk()
        root.withdraw()

        window = tk.Toplevel(root)

        ViewResults(
            window,
            parent_window=root
        )

        root.mainloop()

        return

    window = tk.Toplevel(parent)

    ViewResults(
        window,
        parent_window=parent
    )

    return window



# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()

    ViewResults(root)

    root.mainloop()

