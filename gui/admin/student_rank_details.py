import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import json
from datetime import datetime

# ============================================================
# EXCEL
# ============================================================

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    Workbook = None


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


STUDENT_ANSWERS_DIR = os.path.join(
    BACKEND_DIR,
    "student_answers"
)


# ============================================================
# EXCEL FILE
# ============================================================

RANK_EXCEL_FILE = os.path.join(
    BACKEND_DIR,
    "student_rank_details.xlsx"
)


# ============================================================
# HELPERS
# ============================================================

def load_json(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as e:

        print(
            f"Could not read JSON: {file_path}",
            e
        )

        return None


# ============================================================
# GET STUDENT DATA
# ============================================================

def get_student_data(data):

    student = data.get(
        "student",
        {}
    )

    if not isinstance(
        student,
        dict
    ):
        student = {}

    return student


def get_student_id(data, student_folder=""):

    student = get_student_data(data)

    value = (
        data.get(
            "student_id"
        )
        or student.get(
            "student_id"
        )
    )

    if value:
        return str(value)

    if student_folder:
        return os.path.basename(
            os.path.normpath(
                student_folder
            )
        )

    return ""


def get_student_name(data):

    student = get_student_data(data)

    return str(
        data.get(
            "student_name",
            student.get(
                "student_name",
                student.get(
                    "name",
                    ""
                )
            )
        )
        or ""
    )


# ============================================================
# EXAM HELPERS
# ============================================================

def get_exam_id(data):

    return str(
        data.get(
            "exam_id",
            ""
        )
        or ""
    )


def get_exam_name(data):

    return str(
        data.get(
            "exam_name",
            data.get(
                "exam",
                "AI Oral Examination"
            )
        )
        or "AI Oral Examination"
    )


def get_session_id(data):

    return str(
        data.get(
            "session_id",
            ""
        )
        or ""
    )


def get_pattern_id(data):

    return str(
        data.get(
            "pattern_id",
            ""
        )
        or ""
    )


def get_pattern_name(data):

    return str(
        data.get(
            "pattern_name",
            ""
        )
        or ""
    )


# ============================================================
# ATTEMPT
# ============================================================

def get_attempt_number(data):

    value = data.get(
        "attempt_number",
        data.get(
            "attempt",
            1
        )
    )

    try:

        return int(value)

    except Exception:

        return 1


# ============================================================
# MARKS
# ============================================================

def get_total_marks(result):

    # ------------------------------------------------------------
    # FIRST: use recalculated marks from question_N_answer.json
    # ------------------------------------------------------------

    if "_calculated_total_secured_marks" in result:

        try:
            return float(
                result["_calculated_total_secured_marks"]
            )

        except Exception:
            pass


    # ------------------------------------------------------------
    # SECOND: use saved total secured marks
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

                return float(
                    result[key]
                )

            except Exception:
                pass


    # ------------------------------------------------------------
    # THIRD: calculate from question-level marks
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
                "awarded_marks",
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


    return total



def get_maximum_marks(result):

    # ------------------------------------------------------------
    # FIRST: use recalculated maximum marks from question files
    # ------------------------------------------------------------

    if "_calculated_maximum_marks" in result:

        try:
            return float(
                result["_calculated_maximum_marks"]
            )

        except Exception:
            pass


    # ------------------------------------------------------------
    # SECOND: use saved total allotted marks
    # ------------------------------------------------------------

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


    # ------------------------------------------------------------
    # THIRD: calculate from question-level allotted marks
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

    # ------------------------------------------------------------
    # FIRST: use recalculated percentage from question files
    # ------------------------------------------------------------

    if "_calculated_percentage" in result:

        try:
            return float(
                result["_calculated_percentage"]
            )

        except Exception:
            pass


    # ------------------------------------------------------------
    # SECOND: calculate from actual secured/max marks
    # ------------------------------------------------------------

    total_marks = get_total_marks(
        result
    )

    maximum_marks = get_maximum_marks(
        result
    )


    try:

        total_marks = float(
            total_marks
        )

        maximum_marks = float(
            maximum_marks
        )

    except (
        TypeError,
        ValueError
    ):

        return 0.0


    if maximum_marks <= 0:

        return 0.0


    return round(
        (
            total_marks
            /
            maximum_marks
        )
        *
        100,
        2
    )



# ============================================================
# DATE / TIME
# ============================================================

def get_start_time(data):

    return (
        data.get(
            "start_time"
        )
        or data.get(
            "started_at"
        )
        or ""
    )


def get_submission_time(data):

    return (
        data.get(
            "submitted_at"
        )
        or data.get(
            "submission_time"
        )
        or data.get(
            "submitted_time"
        )
        or ""
    )


def format_datetime(value):

    if not value:

        return ""

    value = str(value)

    try:

        parsed = datetime.fromisoformat(
            value.replace(
                "Z",
                "+00:00"
            )
        )

        return parsed.strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )

    except Exception:

        return value


# ============================================================
# DURATION
# ============================================================

def calculate_duration(
    start_time,
    submission_time
):

    if not start_time or not submission_time:

        return ""

    try:

        start = datetime.fromisoformat(
            str(start_time).replace(
                "Z",
                "+00:00"
            )
        )

        end = datetime.fromisoformat(
            str(submission_time).replace(
                "Z",
                "+00:00"
            )
        )

        seconds = int(
            (end - start).total_seconds()
        )

        if seconds < 0:

            return ""

        minutes = seconds // 60

        remaining_seconds = (
            seconds % 60
        )

        return (
            f"{minutes} min "
            f"{remaining_seconds} sec"
        )

    except Exception:

        return ""


# ============================================================
# RESULT STATUS
# ============================================================

def get_result_status(data):

    # ------------------------------------------------------------
    # FIRST: use the recalculated result from question files
    # ------------------------------------------------------------

    calculated_result = data.get(
        "_calculated_result"
    )

    if calculated_result:

        return str(
            calculated_result
        ).upper()


    # ------------------------------------------------------------
    # SECOND: use saved result
    # ------------------------------------------------------------

    result = data.get(
        "result",
        data.get(
            "overall_result",
            ""
        )
    )


    if result:

        return str(
            result
        ).upper()


    # ------------------------------------------------------------
    # LAST FALLBACK: calculate from percentage
    # ------------------------------------------------------------

    percentage = get_percentage(
        data
    )


    try:

        pass_percentage = float(
            data.get(
                "pass_percentage",
                50
            )
        )

    except Exception:

        pass_percentage = 50.0


    if percentage >= pass_percentage:

        return "PASS"

    return "FAIL"


# ============================================================
# LOAD ALL RESULTS
# ============================================================

def load_all_results():

    results = []

    if not os.path.exists(
        STUDENT_ANSWERS_DIR
    ):

        return results


    # ============================================================
    # LOAD EVERY exam_result.json
    # ============================================================

    for root, dirs, files in os.walk(
        STUDENT_ANSWERS_DIR
    ):

        for filename in files:

            if filename.lower() != "exam_result.json":
                continue


            result_file = os.path.join(
                root,
                filename
            )


            result_data = load_json(
                result_file
            )


            if not isinstance(
                result_data,
                dict
            ):

                continue


            # ====================================================
            # IMPORTANT:
            #
            # root is the attempt folder.
            #
            # Example:
            #
            # student_answers/
            #   Rahul_Kumar/
            #       Rahul_Kumar_attempt_18/
            #           exam_result.json
            #           question_1_answer.json
            #           question_2_answer.json
            #           ...
            #
            # Read the question files from THIS SAME folder.
            # ====================================================

            attempt_folder_path = root


            total_secured_marks = 0.0

            total_allotted_marks = 0.0

            question_files_found = 0

            question_records = []


            # ====================================================
            # READ QUESTION ANSWER FILES
            # ====================================================

            for question_filename in sorted(
                files
            ):

                if not (
                    question_filename.lower().startswith(
                        "question_"
                    )
                    and
                    question_filename.lower().endswith(
                        "_answer.json"
                    )
                ):

                    continue


                question_file = os.path.join(
                    attempt_folder_path,
                    question_filename
                )


                question_data = load_json(
                    question_file
                )


                if not isinstance(
                    question_data,
                    dict
                ):

                    continue


                question_files_found += 1


                # =================================================
                # ALLOTTED MARKS
                # =================================================

                allotted_marks = question_data.get(
                    "marks",
                    question_data.get(
                        "allotted_marks",
                        0
                    )
                )


                try:

                    allotted_marks = float(
                        allotted_marks
                        or 0
                    )

                except Exception:

                    allotted_marks = 0.0


                # =================================================
                # SECURED MARKS
                #
                # Student-side file uses "marks_awarded".
                # =================================================

                marks_awarded = question_data.get(
                    "marks_awarded",
                    question_data.get(
                        "marks_secured",
                        question_data.get(
                            "obtained_marks",
                            question_data.get(
                                "score",
                                0
                            )
                        )
                    )
                )


                try:

                    marks_awarded = float(
                        marks_awarded
                        or 0
                    )

                except Exception:

                    marks_awarded = 0.0


                total_allotted_marks += (
                    allotted_marks
                )

                total_secured_marks += (
                    marks_awarded
                )


                # =================================================
                # KEEP QUESTION DATA
                #
                # This also makes the in-memory questions contain
                # marks_awarded so other functions can use them.
                # =================================================

                question_data[
                    "marks"
                ] = allotted_marks

                question_data[
                    "marks_awarded"
                ] = marks_awarded


                question_records.append(
                    question_data
                )


            # ====================================================
            # IF QUESTION FILES WERE FOUND:
            # USE THEM AS THE SOURCE OF TRUTH
            # ====================================================

            if question_files_found > 0:

                result_data[
                    "_calculated_total_secured_marks"
                ] = round(
                    total_secured_marks,
                    2
                )


                result_data[
                    "_calculated_maximum_marks"
                ] = round(
                    total_allotted_marks,
                    2
                )


                if total_allotted_marks > 0:

                    calculated_percentage = round(
                        (
                            total_secured_marks
                            /
                            total_allotted_marks
                        )
                        *
                        100,
                        2
                    )

                else:

                    calculated_percentage = 0.0


                result_data[
                    "_calculated_percentage"
                ] = calculated_percentage


                # =================================================
                # RECALCULATE PASS / FAIL
                # =================================================

                pass_percentage = result_data.get(
                    "pass_percentage",
                    50
                )


                try:

                    pass_percentage = float(
                        pass_percentage
                    )

                except Exception:

                    pass_percentage = 50.0


                if (
                    calculated_percentage
                    >=
                    pass_percentage
                ):

                    result_data[
                        "_calculated_result"
                    ] = "PASS"

                else:

                    result_data[
                        "_calculated_result"
                    ] = "FAIL"


                # =================================================
                # REPLACE QUESTIONS WITH QUESTION ANSWER DATA
                #
                # This means old records can now display the
                # actual marks from question_N_answer.json.
                # =================================================

                if question_records:

                    result_data[
                        "questions"
                    ] = question_records


            # ====================================================
            # STORE RESULT
            # ====================================================

            results.append(
                {
                    "file": result_file,

                    "student_folder":
                        os.path.dirname(
                            attempt_folder_path
                        ),

                    "attempt_folder":
                        attempt_folder_path,

                    "data":
                        result_data
                }
            )


    return results


    # --------------------------------------------------------
    # Only load exam_result.json.
    # Individual question answer JSON files are ignored.
    # --------------------------------------------------------

    for root, dirs, files in os.walk(
        STUDENT_ANSWERS_DIR
    ):

        for filename in files:

            if filename.lower() != "exam_result.json":
                continue

            file_path = os.path.join(
                root,
                filename
            )

            data = load_json(
                file_path
            )

            if not isinstance(
                data,
                dict
            ):
                continue

            results.append(
                {
                    "file": file_path,
                    "student_folder":
                        root,
                    "data": data
                }
            )

    return results

# ============================================================
# AUTOMATIC EXCEL UPDATE WATCHER
# ============================================================

def get_results_signature():

    signature = []

    if not os.path.exists(
        STUDENT_ANSWERS_DIR
    ):

        return tuple(signature)

    for root, dirs, files in os.walk(
        STUDENT_ANSWERS_DIR
    ):

        for filename in files:

            if not filename.lower().endswith(
                ".json"
            ):
                continue

            file_path = os.path.join(
                root,
                filename
            )

            try:

                modified_time = os.path.getmtime(
                    file_path
                )

                file_size = os.path.getsize(
                    file_path
                )

                signature.append(
                    (
                        file_path,
                        modified_time,
                        file_size
                    )
                )

            except Exception:

                continue

    signature.sort()

    return tuple(signature)


def automatic_update_excel():

    try:

        current_signature = (
            get_results_signature()
        )

        # ----------------------------------------------------
        # First run
        # ----------------------------------------------------

        if not hasattr(
            automatic_update_excel,
            "_last_signature"
        ):

            automatic_update_excel._last_signature = (
                current_signature
            )

            return False

        # ----------------------------------------------------
        # Nothing changed
        # ----------------------------------------------------

        if (
            current_signature ==
            automatic_update_excel._last_signature
        ):

            return False

        # ----------------------------------------------------
        # Store new signature
        # ----------------------------------------------------

        automatic_update_excel._last_signature = (
            current_signature
        )

        # ----------------------------------------------------
        # No result files
        # ----------------------------------------------------

        if not current_signature:

            return False

        # ----------------------------------------------------
        # Update Excel
        # ----------------------------------------------------

        save_ranking_to_excel()

        print(
            "Student Rank Details Excel "
            "automatically updated."
        )

        return True

    except Exception as e:

        print(
            "Automatic Excel update failed:",
            e
        )

        return False


# ============================================================
# BUILD RANKING
# ============================================================

def build_ranking(results):

    # --------------------------------------------------------
    # Keep the BEST attempt for each student/exam/session.
    #
    # This follows the same ranking principle already used
    # by ViewResults.
    # --------------------------------------------------------

    best_by_student = {}

    for item in results:

        data = item[
            "data"
        ]

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

    # --------------------------------------------------------
    # Highest percentage first.
    # If percentage is equal, highest marks first.
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Competition ranking:
    #
    # 1
    # 2
    # 2
    # 4
    # --------------------------------------------------------

    ranking = []

    previous_percentage = None
    previous_marks = None
    current_rank = 0

    for index, item in enumerate(
        ranking_items,
        start=1
    ):

        data = item[
            "data"
        ]

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

        ranking.append(
            {
                "rank": current_rank,
                "item": item
            }
        )

        previous_percentage = percentage
        previous_marks = marks

    return ranking


# ============================================================
# CREATE / UPDATE EXCEL
# ============================================================

def save_ranking_to_excel():

    if Workbook is None:

        raise ImportError(
            "openpyxl is not installed.\n\n"
            "Install it using:\n"
            "pip install openpyxl"
        )

    results = load_all_results()

    if not results:

        raise ValueError(
            "No completed examination results "
            "were found."
        )

    ranking = build_ranking(
        results
    )

    # --------------------------------------------------------
    # Create workbook
    # --------------------------------------------------------

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = (
        "Student Rank Details"
    )

    # ========================================================
    # HEADERS
    # ========================================================

    headers = [

        "Rank",

        "Student ID",

        "Student Name",

        "Roll Number",

        "Class",

        "Section",

        "Course",

        "Department",

        "Gender",

        "Date of Birth",

        "Age",

        "Email",

        "Phone",

        "Exam ID",

        "Exam",

        "Session ID",

        "Pattern ID",

        "Pattern Name",

        "Attempt",

        "Total Questions",

        "Marks",

        "Maximum Marks",

        "Percentage",

        "Result",

        "Start Time",

        "Submission Date/Time",

        "Duration",

        "Result File"
    ]

    worksheet.append(
        headers
    )

    # ========================================================
    # HEADER STYLE
    # ========================================================

    header_fill = PatternFill(
        "solid",
        fgColor="1F2937"
    )

    header_font = Font(
        color="FFFFFF",
        bold=True
    )

    thin_side = Side(
        style="thin",
        color="D1D5DB"
    )

    border = Border(
        left=thin_side,
        right=thin_side,
        top=thin_side,
        bottom=thin_side
    )

    for cell in worksheet[1]:

        cell.fill = header_fill

        cell.font = header_font

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

        cell.border = border

    # ========================================================
    # DATA
    # ========================================================

    for entry in ranking:

        rank = entry[
            "rank"
        ]

        item = entry[
            "item"
        ]

        data = item[
            "data"
        ]

        student = get_student_data(
            data
        )

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

        roll_number = (
            data.get(
                "roll_number"
            )
            or student.get(
                "roll_number",
                ""
            )
        )

        student_class = (
            data.get(
                "class"
            )
            or student.get(
                "class",
                ""
            )
        )

        section = (
            data.get(
                "section"
            )
            or student.get(
                "section",
                ""
            )
        )

        course = (
            data.get(
                "course"
            )
            or student.get(
                "course",
                ""
            )
        )

        department = (
            data.get(
                "department"
            )
            or student.get(
                "department",
                ""
            )
        )

        gender = (
            data.get(
                "gender"
            )
            or student.get(
                "gender",
                ""
            )
        )

        date_of_birth = (
            data.get(
                "date_of_birth"
            )
            or student.get(
                "date_of_birth",
                ""
            )
        )

        age = (
            data.get(
                "age"
            )
            or student.get(
                "age",
                ""
            )
        )

        email = (
            data.get(
                "email"
            )
            or student.get(
                "email",
                ""
            )
        )

        phone = (
            data.get(
                "phone"
            )
            or data.get(
                "mobile_number"
            )
            or student.get(
                "phone",
                ""
            )
        )

        exam_id = get_exam_id(
            data
        )

        exam_name = get_exam_name(
            data
        )

        session_id = get_session_id(
            data
        )

        pattern_id = get_pattern_id(
            data
        )

        pattern_name = get_pattern_name(
            data
        )

        attempt = get_attempt_number(
            data
        )

        marks = get_total_marks(
            data
        )

        maximum_marks = get_maximum_marks(
            data
        )

        percentage = get_percentage(
            data
        )

        result_status = get_result_status(
            data
        )

        # --------------------------------------------------------
        # START / SUBMISSION / DURATION
        # --------------------------------------------------------

        start_time = get_start_time(data)

        submission_time = get_submission_time(data)

        formatted_start_time = format_datetime(
            start_time
        )

        formatted_submission_time = format_datetime(
            submission_time
        )

        duration = calculate_duration(
            start_time,
            submission_time
        )

        # Make sure Excel receives actual text values
        if not duration:
            duration = ""

        duration = str(duration)

        formatted_start_time = str(
            formatted_start_time or ""
        )

        formatted_submission_time = str(
            formatted_submission_time or ""
        )


        questions = data.get(
            "questions",
            []
        )

        if isinstance(
            questions,
            list
        ):

            total_questions = len(
                questions
            )

        else:

            total_questions = 0

        worksheet.append(
            [

                rank,

                student_id,

                student_name,

                roll_number,

                student_class,

                section,

                course,

                department,

                gender,

                date_of_birth,

                age,

                email,

                phone,

                exam_id,

                exam_name,

                session_id,

                pattern_id,

                pattern_name,

                attempt,

                total_questions,

                marks,

                maximum_marks,

                round(
                    percentage,
                    2
                ),

                result_status,

                formatted_start_time,

                formatted_submission_time,

                duration,
                
                item.get(
                    "file",
                    ""
                )
            ]
        )

    # ========================================================
    # FORMAT DATA
    # ========================================================

    for row in worksheet.iter_rows():

        for cell in row:

            cell.border = border

            cell.alignment = Alignment(
                vertical="center"
            )

    # ========================================================
    # FREEZE HEADER
    # ========================================================

    worksheet.freeze_panes = "A2"

    # ========================================================
    # FILTER
    # ========================================================

    worksheet.auto_filter.ref = (
        worksheet.dimensions
    )

    # ========================================================
    # COLUMN WIDTHS
    # ========================================================

    widths = {

        "A": 8,
        "B": 18,
        "C": 25,
        "D": 16,
        "E": 14,
        "F": 12,
        "G": 18,
        "H": 20,
        "I": 12,
        "J": 16,
        "K": 10,
        "L": 30,
        "M": 18,
        "N": 15,
        "O": 30,
        "P": 18,
        "Q": 15,
        "R": 22,
        "S": 10,
        "T": 16,
        "U": 12,
        "V": 16,
        "W": 14,
        "X": 12,
        "Y": 25,
        "Z": 25,
        "AA": 15,
        "AB": 60
    }

    for column, width in widths.items():

        worksheet.column_dimensions[
            column
        ].width = width

    # ========================================================
    # NUMBER FORMATTING
    # ========================================================

    for row in range(
        2,
        worksheet.max_row + 1
    ):

        worksheet.cell(
            row=row,
            column=21
        ).number_format = "0.00"

        worksheet.cell(
            row=row,
            column=22
        ).number_format = "0.00"

        worksheet.cell(
            row=row,
            column=23
        ).number_format = "0.00"

    # ========================================================
    # SAVE
    # ========================================================

    os.makedirs(
        BACKEND_DIR,
        exist_ok=True
    )

    workbook.save(
        RANK_EXCEL_FILE
    )

    return (
        RANK_EXCEL_FILE,
        len(ranking)
    )


# ============================================================
# OPEN EXCEL FILE
# ============================================================

def open_excel_file():

    if not os.path.exists(
        RANK_EXCEL_FILE
    ):

        return False

    try:

        if sys.platform.startswith(
            "win"
        ):

            os.startfile(
                RANK_EXCEL_FILE
            )

        elif sys.platform == "darwin":

            os.system(
                f'open "{RANK_EXCEL_FILE}"'
            )

        else:

            os.system(
                f'xdg-open "{RANK_EXCEL_FILE}"'
            )

        return True

    except Exception as e:

        print(
            "Could not open Excel:",
            e
        )

        return False


# ============================================================
# ADMIN WINDOW
# ============================================================

class StudentRankDetails:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root
        self.parent_window = parent_window

        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Student Rank Details - AI Oral Examination System"
        )

        self.root.geometry(
            "1400x800"
        )

        self.root.minsize(
            1000,
            650
        )

        self.root.configure(
            bg="#f4f6f8"
        )

        try:
            self.root.state("zoomed")
        except Exception:
            pass

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.go_back
        )

        # ----------------------------------------------------
        # CREATE GUI
        # ----------------------------------------------------

        self.create_interface()

        # ----------------------------------------------------
        # LOAD RANKING AUTOMATICALLY
        # ----------------------------------------------------

        self.root.after(
            100,
            self.refresh_ranking
        )

        # ----------------------------------------------------
        # START AUTOMATIC SUBMISSION WATCHER
        # ----------------------------------------------------

        self.root.after(
            1500,
            self.check_for_new_submissions
        )


    # ========================================================
    # INTERFACE
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

        header = tk.Frame(
            main_frame,
            bg="#1f2937",
            height=105
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        tk.Label(
            header,
            text="STUDENT RANK DETAILS",
            font=("Arial", 26, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(18, 3)
        )

        tk.Label(
            header,
            text=(
                "View complete student examination ranking "
                "and performance details"
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
            expand=True,
            padx=25,
            pady=20
        )

        # ====================================================
        # TOP INFORMATION
        # ====================================================

        info_frame = tk.Frame(
            content,
            bg="#f4f6f8"
        )

        info_frame.pack(
            fill="x",
            pady=(0, 12)
        )

        self.title_label = tk.Label(
            info_frame,
            text="Student Ranking",
            font=("Arial", 20, "bold"),
            bg="#f4f6f8",
            fg="#111827"
        )

        self.title_label.pack(
            side="left"
        )

        self.count_label = tk.Label(
            info_frame,
            text="Students: 0",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#4b5563"
        )

        self.count_label.pack(
            side="right",
            padx=10
        )

        # ====================================================
        # TABLE FRAME
        # ====================================================

        table_container = tk.Frame(
            content,
            bg="white",
            bd=1,
            relief="solid"
        )

        table_container.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # TREEVIEW
        # ====================================================

        columns = (

            "rank",
            "student_id",
            "student_name",
            "roll_number",
            "class",
            "section",
            "course",
            "department",
            "gender",
            "date_of_birth",
            "age",
            "email",
            "phone",
            "exam_id",
            "exam",
            "session_id",
            "pattern_id",
            "pattern_name",
            "attempt",
            "total_questions",
            "marks",
            "maximum_marks",
            "percentage",
            "result",
            "start_time",
            "submission_time",
            "duration",
            "result_file"

        )

        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # ====================================================
        # HEADINGS
        # ====================================================

        headings = {

            "rank":
                "Rank",

            "student_id":
                "Student ID",

            "student_name":
                "Student Name",

            "roll_number":
                "Roll Number",

            "class":
                "Class",

            "section":
                "Section",

            "course":
                "Course",

            "department":
                "Department",

            "gender":
                "Gender",

            "date_of_birth":
                "Date of Birth",

            "age":
                "Age",

            "email":
                "Email",

            "phone":
                "Phone",

            "exam_id":
                "Exam ID",

            "exam":
                "Exam",

            "session_id":
                "Session ID",

            "pattern_id":
                "Pattern ID",

            "pattern_name":
                "Pattern Name",

            "attempt":
                "Attempt",

            "total_questions":
                "Total Questions",

            "marks":
                "Marks",

            "maximum_marks":
                "Maximum Marks",

            "percentage":
                "Percentage",

            "result":
                "Result",

            "start_time":
                "Start Time",

            "submission_time":
                "Submission Date/Time",

            "duration":
                "Duration",

            "result_file":
                "Result File"

        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

        # ====================================================
        # COLUMN WIDTHS
        # ====================================================

        widths = {

            "rank": 70,

            "student_id": 130,

            "student_name": 180,

            "roll_number": 110,

            "class": 90,

            "section": 90,

            "course": 130,

            "department": 140,

            "gender": 90,

            "date_of_birth": 120,

            "age": 70,

            "email": 200,

            "phone": 130,

            "exam_id": 110,

            "exam": 180,

            "session_id": 120,

            "pattern_id": 110,

            "pattern_name": 160,

            "attempt": 80,

            "total_questions": 120,

            "marks": 90,

            "maximum_marks": 120,

            "percentage": 100,

            "result": 100,

            "start_time": 170,

            "submission_time": 180,

            "duration": 120,

            "result_file": 300

        }

        for column in columns:

            self.tree.column(
                column,
                width=widths[column],
                minwidth=60,
                anchor="center"
            )

        # ====================================================
        # HEADER STYLE
        # ====================================================

        style = ttk.Style()

        try:

            style.theme_use(
                "clam"
            )

        except Exception:

            pass

        style.configure(
            "Treeview",
            background="white",
            foreground="#111827",
            rowheight=32,
            fieldbackground="white",
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#1f2937",
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=8
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#2563eb")
            ],
            foreground=[
                ("selected", "white")
            ]
        )

        # ====================================================
        # SCROLLBARS
        # ====================================================

        vertical_scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_container,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_container.rowconfigure(
            0,
            weight=1
        )

        table_container.columnconfigure(
            0,
            weight=1
        )

        # ====================================================
        # BUTTON FRAME
        # ====================================================

        button_frame = tk.Frame(
            content,
            bg="#f4f6f8"
        )

        button_frame.pack(
            fill="x",
            pady=(15, 0)
        )

        # ----------------------------------------------------
        # REFRESH
        # ----------------------------------------------------

        tk.Button(
            button_frame,
            text="REFRESH RANKING",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=10,
            command=self.refresh_ranking
        ).pack(
            side="left",
            padx=5
        )

        # ----------------------------------------------------
        # OPEN EXCEL
        # ----------------------------------------------------

        tk.Button(
            button_frame,
            text="OPEN EXCEL REPORT",
            font=("Arial", 11, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=10,
            command=self.open_excel
        ).pack(
            side="left",
            padx=5
        )

        # ----------------------------------------------------
        # UPDATE EXCEL
        # ----------------------------------------------------

        tk.Button(
            button_frame,
            text="UPDATE EXCEL",
            font=("Arial", 11, "bold"),
            bg="#b45309",
            fg="white",
            activebackground="#92400e",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=10,
            command=self.generate_excel
        ).pack(
            side="left",
            padx=5
        )

        # ----------------------------------------------------
        # BACK
        # ----------------------------------------------------

        tk.Button(
            button_frame,
            text="← BACK TO ADMIN PANEL",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=10,
            command=self.go_back
        ).pack(
            side="right",
            padx=5
        )

        # ====================================================
        # STATUS
        # ====================================================

        self.status_label = tk.Label(
            content,
            text="Loading student ranking...",
            font=("Arial", 10),
            bg="#f4f6f8",
            fg="#6b7280"
        )

        self.status_label.pack(
            pady=(8, 0)
        )


    # ========================================================
    # AUTOMATIC EXCEL UPDATE
    # ========================================================

    def check_for_new_submissions(self):

        try:

            updated = automatic_update_excel()

            if updated:

                # ------------------------------------------------
                # Refresh visible ranking table
                # ------------------------------------------------

                self.refresh_ranking()

                self.status_label.configure(
                    text=(
                        "New student submission detected. "
                        "Excel report updated automatically."
                    ),
                    fg="#166534"
                )

        except Exception as e:

            print(
                "Automatic submission check error:",
                e
            )

        # ----------------------------------------------------
        # Check again after 2 seconds
        # ----------------------------------------------------

        try:

            if self.root.winfo_exists():

                self.root.after(
                    2000,
                    self.check_for_new_submissions
                )

        except Exception:

            pass


    # ========================================================
    # REFRESH RANKING
    # ========================================================

    def refresh_ranking(self):

        try:

            self.status_label.configure(
                text="Loading latest student ranking...",
                fg="#2563eb"
            )

            self.root.update_idletasks()

            # ------------------------------------------------
            # Load all completed results
            # ------------------------------------------------

            results = load_all_results()

            if not results:

                self.clear_table()

                self.count_label.configure(
                    text="Students: 0"
                )

                self.status_label.configure(
                    text=(
                        "No completed examination results "
                        "were found."
                    ),
                    fg="#92400e"
                )

                return

            # ------------------------------------------------
            # Build ranking
            # ------------------------------------------------

            ranking = build_ranking(
                results
            )

            # ------------------------------------------------
            # Clear existing table
            # ------------------------------------------------

            self.clear_table()

            # ------------------------------------------------
            # Insert ranking
            # ------------------------------------------------

            for entry in ranking:

                rank = entry[
                    "rank"
                ]

                item = entry[
                    "item"
                ]

                data = item[
                    "data"
                ]

                student = get_student_data(
                    data
                )

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

                roll_number = (
                    data.get(
                        "roll_number"
                    )
                    or student.get(
                        "roll_number",
                        ""
                    )
                )

                student_class = (
                    data.get(
                        "class"
                    )
                    or student.get(
                        "class",
                        ""
                    )
                )

                section = (
                    data.get(
                        "section"
                    )
                    or student.get(
                        "section",
                        ""
                    )
                )

                course = (
                    data.get(
                        "course"
                    )
                    or student.get(
                        "course",
                        ""
                    )
                )

                department = (
                    data.get(
                        "department"
                    )
                    or student.get(
                        "department",
                        ""
                    )
                )

                gender = (
                    data.get(
                        "gender"
                    )
                    or student.get(
                        "gender",
                        ""
                    )
                )

                date_of_birth = (
                    data.get(
                        "date_of_birth"
                    )
                    or student.get(
                        "date_of_birth",
                        ""
                    )
                )

                age = (
                    data.get(
                        "age"
                    )
                    or student.get(
                        "age",
                        ""
                    )
                )

                email = (
                    data.get(
                        "email"
                    )
                    or student.get(
                        "email",
                        ""
                    )
                )

                phone = (
                    data.get(
                        "phone"
                    )
                    or data.get(
                        "mobile_number",
                        ""
                    )
                    or student.get(
                        "phone",
                        ""
                    )
                )

                exam_id = get_exam_id(
                    data
                )

                exam_name = get_exam_name(
                    data
                )

                session_id = get_session_id(
                    data
                )

                pattern_id = get_pattern_id(
                    data
                )

                pattern_name = get_pattern_name(
                    data
                )

                attempt = get_attempt_number(
                    data
                )

                marks = get_total_marks(
                    data
                )

                maximum_marks = get_maximum_marks(
                    data
                )

                percentage = get_percentage(
                    data
                )

                result_status = get_result_status(
                    data
                )

                start_time = get_start_time(
                    data
                )

                submission_time = get_submission_time(
                    data
                )

                duration = calculate_duration(
                    start_time,
                    submission_time
                )

                questions = data.get(
                    "questions",
                    []
                )

                if isinstance(
                    questions,
                    list
                ):

                    total_questions = len(
                        questions
                    )

                else:

                    total_questions = 0

                values = (

                    rank,

                    student_id,

                    student_name,

                    roll_number,

                    student_class,

                    section,

                    course,

                    department,

                    gender,

                    date_of_birth,

                    age,

                    email,

                    phone,

                    exam_id,

                    exam_name,

                    session_id,

                    pattern_id,

                    pattern_name,

                    attempt,

                    total_questions,

                    f"{marks:.2f}",

                    f"{maximum_marks:.2f}",

                    f"{percentage:.2f}%",

                    result_status,

                    format_datetime(
                        start_time
                    ),

                    format_datetime(
                        submission_time
                    ),

                    duration,

                    item.get(
                        "file",
                        ""
                    )

                )

                self.tree.insert(
                    "",
                    "end",
                    values=values
                )

            # ------------------------------------------------
            # Update count
            # ------------------------------------------------

            self.count_label.configure(
                text=(
                    f"Students: {len(ranking)}"
                )
            )

            self.status_label.configure(
                text=(
                    "Ranking loaded successfully."
                ),
                fg="#166534"
            )

        except Exception as e:

            self.status_label.configure(
                text=(
                    "Could not load student ranking."
                ),
                fg="#991b1b"
            )

            messagebox.showerror(
                "Ranking Error",
                (
                    "Could not load Student Rank Details.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # CLEAR TABLE
    # ========================================================

    def clear_table(self):

        for item in self.tree.get_children():

            self.tree.delete(
                item
            )


    # ========================================================
    # GENERATE / UPDATE EXCEL
    # ========================================================

    def generate_excel(self):

        try:

            file_path, count = (
                save_ranking_to_excel()
            )

            # Refresh visible table too
            self.refresh_ranking()

            # Update watcher signature so the current state
            # is considered processed.
            automatic_update_excel._last_signature = (
                get_results_signature()
            )

            messagebox.showinfo(
                "Excel Updated",
                (
                    "Student Rank Details Excel file "
                    "has been updated successfully.\n\n"
                    f"Students ranked: {count}\n\n"
                    f"Location:\n{file_path}"
                ),
                parent=self.root
            )

        except Exception as e:

            messagebox.showerror(
                "Excel Error",
                (
                    "Could not update Student Rank Details.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # OPEN EXCEL
    # ========================================================

    def open_excel(self):

        try:

            # ------------------------------------------------
            # If Excel file does not exist, create it first.
            # ------------------------------------------------

            if not os.path.exists(RANK_EXCEL_FILE):

                file_path, count = (
                    save_ranking_to_excel()
                )

                automatic_update_excel._last_signature = (
                    get_results_signature()
                )

            else:

                file_path = RANK_EXCEL_FILE

                # ------------------------------------------------
                # Do NOT save/overwrite the Excel file here.
                # This prevents "Permission denied" when Excel
                # already has the file open.
                # ------------------------------------------------

                try:

                    workbook = load_workbook(
                        RANK_EXCEL_FILE
                    )

                    worksheet = workbook.active

                    count = max(
                        worksheet.max_row - 1,
                        0
                    )

                    workbook.close()

                except Exception:

                    count = 0

            # ------------------------------------------------
            # Open Excel
            # ------------------------------------------------

            opened = open_excel_file()

            if not opened:

                messagebox.showinfo(
                    "Excel Report",
                    (
                        "The Student Rank Details Excel file "
                        "is available, but could not be opened "
                        "automatically.\n\n"
                        f"Location:\n{file_path}"
                    ),
                    parent=self.root
                )

                return

            self.status_label.configure(
                text=(
                    f"Excel report opened successfully. "
                    f"Students ranked: {count}"
                ),
                fg="#166534"
            )

        except PermissionError:

            messagebox.showerror(
                "Excel Permission Error",
                (
                    "The Student Rank Details Excel file is "
                    "currently being used by another program.\n\n"
                    "Please close the Excel file and try again."
                ),
                parent=self.root
            )

        except Exception as e:

            messagebox.showerror(
                "Open Excel Error",
                (
                    "Could not open the Student Rank Details "
                    "Excel report.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # BACK TO ADMIN PANEL
    # ========================================================

    def go_back(self):

        try:

            if self.root.winfo_exists():

                self.root.destroy()

        except Exception:

            pass

        if self.parent_window is not None:

            try:

                self.parent_window.deiconify()

                try:

                    self.parent_window.state(
                        "zoomed"
                    )

                except Exception:

                    pass

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

    StudentRankDetails(
        window,
        parent_window=root
    )

    root.mainloop()
