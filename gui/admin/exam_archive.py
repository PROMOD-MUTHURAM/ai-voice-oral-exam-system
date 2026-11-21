
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import json
import shutil
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

SESSIONS_DIR = os.path.join(
    BACKEND_DIR,
    "exam_sessions"
)

STUDENTS_DIR = os.path.join(
    BACKEND_DIR,
    "students"
)

STUDENT_ANSWERS_DIR = os.path.join(
    BACKEND_DIR,
    "student_answers"
)

ARCHIVE_DIR = os.path.join(
    BACKEND_DIR,
    "exam_archive"
)

ARCHIVE_INDEX_FILE = os.path.join(
    ARCHIVE_DIR,
    "archive_index.json"
)


# ============================================================
# CREATE DIRECTORIES
# ============================================================

os.makedirs(
    ARCHIVE_DIR,
    exist_ok=True
)


# ============================================================
# HELPERS
# ============================================================

def now_iso():

    return datetime.now().isoformat(
        timespec="seconds"
    )


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


def save_json(
    file_path,
    data
):

    directory = os.path.dirname(
        file_path
    )

    if directory:

        os.makedirs(
            directory,
            exist_ok=True
        )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def safe_remove_directory(
    directory
):

    if os.path.exists(
        directory
    ):

        shutil.rmtree(
            directory
        )


# ============================================================
# ARCHIVE INDEX
# ============================================================

def load_archive_index():

    if not os.path.exists(
        ARCHIVE_INDEX_FILE
    ):

        return []

    data = load_json(
        ARCHIVE_INDEX_FILE
    )

    if isinstance(
        data,
        dict
    ):

        data = data.get(
            "archives",
            []
        )

    if not isinstance(
        data,
        list
    ):

        return []

    return data


def save_archive_index(
    archives
):

    os.makedirs(
        ARCHIVE_DIR,
        exist_ok=True
    )

    save_json(
        ARCHIVE_INDEX_FILE,
        {
            "archives": archives
        }
    )


# ============================================================
# SESSION DIRECTORY
# ============================================================

def get_session_file(
    session_id
):

    return os.path.join(
        SESSIONS_DIR,
        f"{session_id}.json"
    )


# ============================================================
# ARCHIVE DIRECTORY
# ============================================================

def get_archive_directory(
    session_id
):

    return os.path.join(
        ARCHIVE_DIR,
        str(session_id)
    )


# ============================================================
# DISCOVER EXAM SESSIONS
# ============================================================

def discover_sessions():

    sessions = []

    if not os.path.isdir(
        SESSIONS_DIR
    ):

        return sessions

    for filename in sorted(
        os.listdir(
            SESSIONS_DIR
        )
    ):

        if not filename.lower().endswith(
            ".json"
        ):

            continue

        file_path = os.path.join(
            SESSIONS_DIR,
            filename
        )

        session = load_json(
            file_path
        )

        if not isinstance(
            session,
            dict
        ):

            continue

        session_id = str(
            session.get(
                "session_id",
                os.path.splitext(
                    filename
                )[0]
            )
        )

        session["session_id"] = session_id

        session["_file_path"] = file_path

        sessions.append(
            session
        )

    return sessions


# ============================================================
# LOAD EXAM DEFINITION
# ============================================================

def load_exam_definition(
    exam_id
):

    if not exam_id:

        return None

    # --------------------------------------------------------
    # Format 1:
    # exams/EXAM001.json
    # --------------------------------------------------------

    direct_file = os.path.join(
        EXAMS_DIR,
        f"{exam_id}.json"
    )

    if os.path.exists(
        direct_file
    ):

        data = load_json(
            direct_file
        )

        if isinstance(
            data,
            dict
        ):

            return data

    # --------------------------------------------------------
    # Format 2:
    # exams/EXAM001/exam.json
    # --------------------------------------------------------

    directory_file = os.path.join(
        EXAMS_DIR,
        str(exam_id),
        "exam.json"
    )

    if os.path.exists(
        directory_file
    ):

        data = load_json(
            directory_file
        )

        if isinstance(
            data,
            dict
        ):

            return data

    return None


# ============================================================
# GET SESSION STUDENTS
# ============================================================

def get_session_students(
    session
):

    student_ids = session.get(
        "student_ids",
        []
    )

    if not isinstance(
        student_ids,
        list
    ):

        student_ids = []

    students = []

    for student_id in student_ids:

        student_id = str(
            student_id
        ).strip()

        if not student_id:

            continue

        student_data = None

        student_file = os.path.join(
            STUDENTS_DIR,
            f"{student_id}.json"
        )

        if os.path.exists(
            student_file
        ):

            student_data = load_json(
                student_file
            )

        if not isinstance(
            student_data,
            dict
        ):

            student_data = {
                "student_id": student_id
            }

        student_data["student_id"] = (
            student_id
        )

        students.append(
            student_data
        )

    return students


# ============================================================
# FIND STUDENT RESULT FOR SESSION
# ============================================================

def find_student_result(
    student_id,
    session_id
):

    student_id = str(
        student_id
    ).strip()

    session_id = str(
        session_id
    ).strip()

    if not student_id:

        return None

    if not os.path.isdir(
        STUDENT_ANSWERS_DIR
    ):

        return None

    # --------------------------------------------------------
    # First try:
    # student_answers/STUDENT_ID/exam_result.json
    # --------------------------------------------------------

    direct_student_dir = os.path.join(
        STUDENT_ANSWERS_DIR,
        student_id
    )

    if os.path.isdir(
        direct_student_dir
    ):

        for root, dirs, files in os.walk(
            direct_student_dir
        ):

            for filename in files:

                if filename.lower() != (
                    "exam_result.json"
                ):

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

                result_session_id = str(
                    data.get(
                        "session_id",
                        ""
                    )
                ).strip()

                if (
                    result_session_id
                    and result_session_id
                    == session_id
                ):

                    return {
                        "file": file_path,
                        "data": data
                    }

    # --------------------------------------------------------
    # Fallback: search entire student_answers directory
    # --------------------------------------------------------

    for root, dirs, files in os.walk(
        STUDENT_ANSWERS_DIR
    ):

        for filename in files:

            if filename.lower() != (
                "exam_result.json"
            ):

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

            result_student_id = str(
                data.get(
                    "student_id",
                    ""
                )
            ).strip()

            result_session_id = str(
                data.get(
                    "session_id",
                    ""
                )
            ).strip()

            if (
                result_student_id == student_id
                and result_session_id == session_id
            ):

                return {
                    "file": file_path,
                    "data": data
                }

    return None


# ============================================================
# COLLECT SESSION RESULTS
# ============================================================

def collect_session_results(
    session
):

    session_id = str(
        session.get(
            "session_id",
            ""
        )
    )

    results = []

    students = get_session_students(
        session
    )

    for student in students:

        student_id = student.get(
            "student_id",
            ""
        )

        result = find_student_result(
            student_id,
            session_id
        )

        if result is None:

            continue

        results.append(
            {
                "student_id": student_id,
                "student": student,
                "source_file": result["file"],
                "data": result["data"]
            }
        )

    return results


# ============================================================
# CREATE QUESTION SNAPSHOT
# ============================================================

def create_question_snapshot(
    session,
    exam
):

    questions = []

    if isinstance(
        exam,
        dict
    ):

        questions = exam.get(
            "questions",
            []
        )

        if not isinstance(
            questions,
            list
        ):

            questions = []

    return {
        "session_id": session.get(
            "session_id",
            ""
        ),
        "exam_id": session.get(
            "exam_id",
            ""
        ),
        "exam_name": session.get(
            "exam_name",
            ""
        ),
        "pattern_id": session.get(
            "pattern_id",
            ""
        ),
        "pattern_name": session.get(
            "pattern_name",
            ""
        ),
        "created_at": now_iso(),
        "questions": questions
    }


# ============================================================
# ARCHIVE SESSION
# ============================================================

def archive_exam_session(
    session
):

    session_id = str(
        session.get(
            "session_id",
            ""
        )
    ).strip()

    if not session_id:

        raise ValueError(
            "Session ID is missing."
        )

    session_file = get_session_file(
        session_id
    )

    if not os.path.exists(
        session_file
    ):

        raise ValueError(
            "Session file was not found:\n"
            f"{session_file}"
        )

    session_data = load_json(
        session_file
    )

    if not isinstance(
        session_data,
        dict
    ):

        raise ValueError(
            "Session JSON is invalid."
        )

    current_status = str(
        session_data.get(
            "status",
            ""
        )
    ).strip().upper()

    if current_status == "ARCHIVED":

        raise ValueError(
            "This examination session is already archived."
        )

    # --------------------------------------------------------
    # Exam definition
    # --------------------------------------------------------

    exam_id = str(
        session_data.get(
            "exam_id",
            ""
        )
    )

    exam = load_exam_definition(
        exam_id
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    results = collect_session_results(
        session_data
    )

    students = get_session_students(
        session_data
    )

    # --------------------------------------------------------
    # Archive directory
    # --------------------------------------------------------

    archive_dir = get_archive_directory(
        session_id
    )

    if os.path.exists(
        archive_dir
    ):

        raise ValueError(
            "Archive directory already exists:\n"
            f"{archive_dir}"
        )

    os.makedirs(
        archive_dir,
        exist_ok=True
    )

    results_archive_dir = os.path.join(
        archive_dir,
        "results"
    )

    os.makedirs(
        results_archive_dir,
        exist_ok=True
    )

    # ========================================================
    # SAVE SESSION SNAPSHOT
    # ========================================================

    archived_at = now_iso()

    archived_session = dict(
        session_data
    )

    archived_session[
        "archive_status"
    ] = "ARCHIVED"

    archived_session[
        "archived_at"
    ] = archived_at

    archived_session[
        "original_status"
    ] = current_status

    save_json(
        os.path.join(
            archive_dir,
            "session.json"
        ),
        archived_session
    )

    # ========================================================
    # SAVE EXAM SNAPSHOT
    # ========================================================

    if isinstance(
        exam,
        dict
    ):

        exam_snapshot = dict(
            exam
        )

    else:

        exam_snapshot = {
            "exam_id": exam_id,
            "exam_name": session_data.get(
                "exam_name",
                ""
            )
        }

    exam_snapshot[
        "archive_session_id"
    ] = session_id

    exam_snapshot[
        "archived_at"
    ] = archived_at

    save_json(
        os.path.join(
            archive_dir,
            "exam_snapshot.json"
        ),
        exam_snapshot
    )

    # ========================================================
    # SAVE QUESTION SNAPSHOT
    # ========================================================

    question_snapshot = create_question_snapshot(
        session_data,
        exam
    )

    question_snapshot[
        "archived_at"
    ] = archived_at

    save_json(
        os.path.join(
            archive_dir,
            "question_snapshot.json"
        ),
        question_snapshot
    )

    # ========================================================
    # SAVE STUDENTS
    # ========================================================

    save_json(
        os.path.join(
            archive_dir,
            "students.json"
        ),
        {
            "session_id": session_id,
            "students": students
        }
    )

    # ========================================================
    # COPY RESULTS
    # ========================================================

    archived_result_count = 0

    for result in results:

        student_id = str(
            result.get(
                "student_id",
                ""
            )
        )

        if not student_id:

            continue

        student_result_dir = os.path.join(
            results_archive_dir,
            student_id
        )

        os.makedirs(
            student_result_dir,
            exist_ok=True
        )

        source_file = result.get(
            "source_file"
        )

        destination_file = os.path.join(
            student_result_dir,
            "exam_result.json"
        )

        if source_file and os.path.exists(
            source_file
        ):

            shutil.copy2(
                source_file,
                destination_file
            )

            archived_result_count += 1

    # ========================================================
    # CREATE ARCHIVE METADATA
    # ========================================================

    exam_date = session_data.get(
        "exam_date",
        ""
    )

    academic_year = session_data.get(
        "academic_year",
        ""
    )

    # --------------------------------------------------------
    # If academic year isn't stored in session,
    # derive it from exam date.
    # --------------------------------------------------------

    if not academic_year and exam_date:

        try:

            academic_year = str(
                datetime.strptime(
                    str(exam_date),
                    "%Y-%m-%d"
                ).year
            )

        except Exception:

            academic_year = ""

    archive_metadata = {

        "archive_id":
            session_id,

        "session_id":
            session_id,

        "exam_id":
            session_data.get(
                "exam_id",
                ""
            ),

        "exam_name":
            session_data.get(
                "exam_name",
                ""
            ),

        "academic_year":
            academic_year,

        "batch":
            session_data.get(
                "batch",
                ""
            ),

        "pattern_id":
            session_data.get(
                "pattern_id",
                ""
            ),

        "pattern_name":
            session_data.get(
                "pattern_name",
                ""
            ),

        "exam_date":
            exam_date,

        "start_time":
            session_data.get(
                "start_time",
                ""
            ),

        "duration_minutes":
            session_data.get(
                "duration_minutes",
                ""
            ),

        "total_questions":
            session_data.get(
                "total_questions",
                ""
            ),

        "total_marks":
            session_data.get(
                "total_marks",
                ""
            ),

        "student_count":
            len(students),

        "result_count":
            archived_result_count,

        "original_status":
            current_status,

        "status":
            "ARCHIVED",

        "archived_at":
            archived_at,

        "archived_by":
            "admin"
    }

    save_json(
        os.path.join(
            archive_dir,
            "archive.json"
        ),
        archive_metadata
    )

    # ========================================================
    # UPDATE ORIGINAL SESSION
    # ========================================================

    session_data[
        "status"
    ] = "ARCHIVED"

    session_data[
        "archived_at"
    ] = archived_at

    session_data[
        "archive_version"
    ] = 1

    session_data[
        "archived_result_count"
    ] = archived_result_count

    session_data[
        "archived_student_count"
    ] = len(students)

    save_json(
        session_file,
        session_data
    )

    # ========================================================
    # UPDATE ARCHIVE INDEX
    # ========================================================

    archive_index = load_archive_index()

    archive_index = [
        item
        for item in archive_index
        if str(
            item.get(
                "session_id",
                ""
            )
        ) != session_id
    ]

    archive_index.append(
        archive_metadata
    )

    archive_index.sort(
        key=lambda item: (
            str(
                item.get(
                    "academic_year",
                    ""
                )
            ),
            str(
                item.get(
                    "exam_date",
                    ""
                )
            ),
            str(
                item.get(
                    "session_id",
                    ""
                )
            )
        ),
        reverse=True
    )

    save_archive_index(
        archive_index
    )

    return archive_metadata


# ============================================================
# RESTORE EXAM SESSION
# ============================================================

def restore_exam_session(
    archive
):

    session_id = str(
        archive.get(
            "session_id",
            archive.get(
                "archive_id",
                ""
            )
        )
    ).strip()

    if not session_id:

        raise ValueError(
            "Session ID is missing."
        )

    archive_dir = get_archive_directory(
        session_id
    )

    if not os.path.isdir(
        archive_dir
    ):

        raise ValueError(
            "Archive directory was not found:\n"
            f"{archive_dir}"
        )

    archived_session_file = os.path.join(
        archive_dir,
        "session.json"
    )

    if not os.path.exists(
        archived_session_file
    ):

        raise ValueError(
            "Archived session.json was not found."
        )

    archived_session = load_json(
        archived_session_file
    )

    if not isinstance(
        archived_session,
        dict
    ):

        raise ValueError(
            "Archived session.json is invalid."
        )

    session_file = get_session_file(
        session_id
    )

    # --------------------------------------------------------
    # Restore original session
    # --------------------------------------------------------

    restored_session = dict(
        archived_session
    )

    original_status = str(
        restored_session.get(
            "original_status",
            "COMPLETED"
        )
    ).strip()

    if not original_status:

        original_status = "COMPLETED"

    restored_session[
        "status"
    ] = original_status

    restored_session[
        "restored_at"
    ] = now_iso()

    restored_session.pop(
        "archive_status",
        None
    )

    save_json(
        session_file,
        restored_session
    )

    # --------------------------------------------------------
    # Update archive metadata
    # --------------------------------------------------------

    archive_file = os.path.join(
        archive_dir,
        "archive.json"
    )

    if os.path.exists(
        archive_file
    ):

        archive_data = load_json(
            archive_file
        )

        if isinstance(
            archive_data,
            dict
        ):

            archive_data[
                "status"
            ] = "RESTORED"

            archive_data[
                "restored_at"
            ] = now_iso()

            save_json(
                archive_file,
                archive_data
            )

    # --------------------------------------------------------
    # Update index
    # --------------------------------------------------------

    archive_index = load_archive_index()

    for item in archive_index:

        if str(
            item.get(
                "session_id",
                ""
            )
        ) == session_id:

            item[
                "status"
            ] = "RESTORED"

            item[
                "restored_at"
            ] = now_iso()

    save_archive_index(
        archive_index
    )

    return restored_session


# ============================================================
# DELETE ARCHIVED SESSION
# ============================================================

def delete_archived_session(
    archive
):

    session_id = str(
        archive.get(
            "session_id",
            archive.get(
                "archive_id",
                ""
            )
        )
    ).strip()

    if not session_id:

        raise ValueError(
            "Session ID is missing."
        )

    archive_dir = get_archive_directory(
        session_id
    )

    if not os.path.isdir(
        archive_dir
    ):

        raise ValueError(
            "Archive directory was not found."
        )

    archive_file = os.path.join(
        archive_dir,
        "archive.json"
    )

    archive_data = load_json(
        archive_file
    )

    if not isinstance(
        archive_data,
        dict
    ):

        raise ValueError(
            "Invalid archive metadata."
        )

    if str(
        archive_data.get(
            "status",
            ""
        )
    ).upper() != "ARCHIVED":

        raise ValueError(
            "Only archived sessions can be permanently deleted."
        )

    # --------------------------------------------------------
    # Delete archive only
    # --------------------------------------------------------

    safe_remove_directory(
        archive_dir
    )

    # --------------------------------------------------------
    # Remove from archive index
    # --------------------------------------------------------

    archive_index = load_archive_index()

    archive_index = [
        item
        for item in archive_index
        if str(
            item.get(
                "session_id",
                ""
            )
        ) != session_id
    ]

    save_archive_index(
        archive_index
    )


# ============================================================
# EXAM ARCHIVE WINDOW
# ============================================================

class ExamArchive:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        self.parent_window = parent_window

        self.all_sessions = []

        self.root.title(
            "Exam Archive - AI Oral Examination System"
        )

        self.root.geometry(
            "1500x850"
        )

        self.root.minsize(
            1100,
            700
        )

        self.root.configure(
            bg="#f4f6f8"
        )

        try:

            self.root.state(
                "zoomed"
            )

        except Exception:

            pass

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.go_back
        )

        self.create_interface()

        self.show_loading()

        self.root.after(
            100,
            self.start_archive_loading
        )

    # ========================================================
    # LOADING SCREEN
    # ========================================================

    def show_loading(self):

        self.loading_frame = tk.Frame(
            self.root,
            bg="#111827"
        )

        self.loading_frame.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        tk.Label(
            self.loading_frame,
            text="EXAM ARCHIVE",
            font=("Arial", 26, "bold"),
            bg="#111827",
            fg="white"
        ).pack(
            pady=(300, 10)
        )

        tk.Label(
            self.loading_frame,
            text="Loading examination archive...",
            font=("Arial", 12),
            bg="#111827",
            fg="#d1d5db"
        ).pack(
            pady=10
        )

        self.loading_bar = ttk.Progressbar(
            self.loading_frame,
            mode="indeterminate",
            length=350
        )

        self.loading_bar.pack(
            pady=15
        )

        self.loading_bar.start(10)

        self.root.update_idletasks()


    def start_archive_loading(self):

        self.refresh_sessions()

        try:

            self.loading_bar.stop()

        except Exception:

            pass

        try:

            self.loading_frame.destroy()

        except Exception:

            pass


    # ========================================================
    # INTERFACE
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
            height=110
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        tk.Label(
            header,
            text="EXAM ARCHIVE",
            font=("Arial", 26, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(18, 3)
        )

        tk.Label(
            header,
            text=(
                "Archive and restore examination sessions "
                "without mixing students, questions or results"
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
        # FILTER FRAME
        # ====================================================

        filter_frame = tk.Frame(
            content,
            bg="#f4f6f8"
        )

        filter_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            filter_frame,
            text="Search:",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#111827"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.search_var = tk.StringVar()

        self.search_entry = tk.Entry(
            filter_frame,
            textvariable=self.search_var,
            font=("Arial", 11),
            width=35
        )

        self.search_entry.pack(
            side="left",
            padx=(0, 15)
        )

        self.search_var.trace_add(
            "write",
            lambda *args:
                self.apply_filter()
        )

        tk.Label(
            filter_frame,
            text="Year:",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#111827"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.year_var = tk.StringVar(
            value="ALL"
        )

        self.year_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.year_var,
            state="readonly",
            width=12
        )

        self.year_combo.pack(
            side="left",
            padx=(0, 15)
        )

        self.year_combo.bind(
            "<<ComboboxSelected>>",
            lambda event:
                self.apply_filter()
        )

        tk.Label(
            filter_frame,
            text="Status:",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#111827"
        ).pack(
            side="left",
            padx=(0, 5)
        )

        self.status_var = tk.StringVar(
            value="ALL"
        )

        self.status_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=[
                "ALL",
                "ARCHIVED",
                "RESTORED"
            ],
            state="readonly",
            width=14
        )

        self.status_combo.pack(
            side="left"
        )

        self.status_combo.bind(
            "<<ComboboxSelected>>",
            lambda event:
                self.apply_filter()
        )

        # ====================================================
        # TABLE
        # ====================================================

        table_frame = tk.Frame(
            content,
            bg="white",
            bd=1,
            relief="solid"
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "session_id",
            "year",
            "exam_id",
            "exam_name",
            "pattern",
            "date",
            "start_time",
            "duration",
            "students",
            "results",
            "status",
            "archived_at"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {

            "session_id":
                "Session ID",

            "year":
                "Academic Year",

            "exam_id":
                "Exam ID",

            "exam_name":
                "Exam",

            "pattern":
                "Question Pattern",

            "date":
                "Exam Date",

            "start_time":
                "Start Time",

            "duration":
                "Duration",

            "students":
                "Students",

            "results":
                "Results",

            "status":
                "Status",

            "archived_at":
                "Archived At"
        }

        widths = {

            "session_id": 110,

            "year": 110,

            "exam_id": 100,

            "exam_name": 220,

            "pattern": 180,

            "date": 120,

            "start_time": 110,

            "duration": 100,

            "students": 90,

            "results": 90,

            "status": 110,

            "archived_at": 170
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                minwidth=70,
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

        table_frame.rowconfigure(
            0,
            weight=1
        )

        table_frame.columnconfigure(
            0,
            weight=1
        )

        # ====================================================
        # STYLE
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

        tk.Button(
            button_frame,
            text="REFRESH",
            font=("Arial", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            bd=0,
            padx=22,
            pady=10,
            cursor="hand2",
            command=self.refresh_sessions
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="VIEW DETAILS",
            font=("Arial", 10, "bold"),
            bg="#0891b2",
            fg="white",
            activebackground="#0e7490",
            bd=0,
            padx=22,
            pady=10,
            cursor="hand2",
            command=self.view_session
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="VIEW QUESTIONS",
            font=("Arial", 10, "bold"),
            bg="#7c3aed",
            fg="white",
            activebackground="#6d28d9",
            bd=0,
            padx=22,
            pady=10,
            cursor="hand2",
            command=self.view_questions
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="VIEW STUDENTS",
            font=("Arial", 10, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            bd=0,
            padx=22,
            pady=10,
            cursor="hand2",
            command=self.view_students
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="ARCHIVE SESSION",
            font=("Arial", 10, "bold"),
            bg="#9333ea",
            fg="white",
            activebackground="#7e22ce",
            bd=0,
            padx=22,
            pady=10,
            cursor="hand2",
            command=self.archive_selected
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="RESTORE SESSION",
            font=("Arial", 10, "bold"),
            bg="#ea580c",
            fg="white",
            activebackground="#c2410c",
            bd=0,
            padx=22,
            pady=10,
            cursor="hand2",
            command=self.restore_selected
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="DELETE ARCHIVE",
            font=("Arial", 10, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            bd=0,
            padx=22,
            pady=10,
            cursor="hand2",
            command=self.delete_selected
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="BACK TO ADMIN PANEL",
            font=("Arial", 10, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            bd=0,
            padx=22,
            pady=10,
            cursor="hand2",
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
            text="Loading examination sessions...",
            font=("Arial", 10),
            bg="#f4f6f8",
            fg="#6b7280"
        )

        self.status_label.pack(
            pady=(8, 0)
        )


    # ========================================================
    # REFRESH SESSIONS
    # ========================================================

    def refresh_sessions(self):

        try:

            self.all_sessions = []

            # ------------------------------------------------
            # Load current sessions
            # ------------------------------------------------

            sessions = discover_sessions()

            for session in sessions:

                self.all_sessions.append(
                    session
                )

            # ------------------------------------------------
            # Load archived sessions
            # ------------------------------------------------

            archive_index = load_archive_index()

            for archive in archive_index:

                if not isinstance(
                    archive,
                    dict
                ):

                    continue

                session_id = str(
                    archive.get(
                        "session_id",
                        ""
                    )
                )

                if not session_id:

                    continue

                # ------------------------------------------------
                # If current session already exists, update its
                # archive information rather than duplicating it.
                # ------------------------------------------------

                found = False

                for existing in self.all_sessions:

                    if str(
                        existing.get(
                            "session_id",
                            ""
                        )
                    ) == session_id:

                        existing[
                            "_archive_metadata"
                        ] = archive

                        found = True

                        break

                if not found:

                    archive_copy = dict(
                        archive
                    )

                    archive_copy[
                        "_archived_only"
                    ] = True

                    self.all_sessions.append(
                        archive_copy
                    )

            # ------------------------------------------------
            # Update year list
            # ------------------------------------------------

            years = set()

            for session in self.all_sessions:

                year = self.get_academic_year(
                    session
                )

                if year:

                    years.add(
                        year
                    )

            year_values = [
                "ALL"
            ] + sorted(
                years,
                reverse=True
            )

            self.year_combo[
                "values"
            ] = year_values

            if self.year_var.get() not in year_values:

                self.year_var.set(
                    "ALL"
                )

            self.apply_filter()

            self.status_label.configure(
                text=(
                    f"{len(self.all_sessions)} "
                    "examination session(s) loaded."
                ),
                fg="#166534"
            )

        except Exception as e:

            self.status_label.configure(
                text="Could not load examination sessions.",
                fg="#991b1b"
            )

            messagebox.showerror(
                "Archive Error",
                (
                    "Could not load examination sessions.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # ACADEMIC YEAR
    # ========================================================

    def get_academic_year(
        self,
        session
    ):

        year = str(
            session.get(
                "academic_year",
                ""
            )
        ).strip()

        if year:

            return year

        exam_date = str(
            session.get(
                "exam_date",
                ""
            )
        ).strip()

        if exam_date:

            try:

                return str(
                    datetime.strptime(
                        exam_date,
                        "%Y-%m-%d"
                    ).year
                )

            except Exception:

                pass

        return ""


    # ========================================================
    # APPLY FILTER
    # ========================================================

    def apply_filter(self):

        for item in self.tree.get_children():

            self.tree.delete(
                item
            )

        search_text = (
            self.search_var
            .get()
            .strip()
            .lower()
        )

        selected_year = (
            self.year_var
            .get()
            .strip()
        )

        selected_status = (
            self.status_var
            .get()
            .strip()
            .upper()
        )

        for session in self.all_sessions:

            session_id = str(
                session.get(
                    "session_id",
                    ""
                )
            )

            exam_id = str(
                session.get(
                    "exam_id",
                    ""
                )
            )

            exam_name = str(
                session.get(
                    "exam_name",
                    ""
                )
            )

            pattern_name = str(
                session.get(
                    "pattern_name",
                    ""
                )
            )

            year = self.get_academic_year(
                session
            )

            batch = str(
                session.get(
                    "batch",
                    ""
                )
            )

            exam_date = str(
                session.get(
                    "exam_date",
                    ""
                )
            )

            searchable = " ".join(
                [
                    session_id,
                    exam_id,
                    exam_name,
                    pattern_name,
                    year,
                    batch,
                    exam_date
                ]
            ).lower()

            if (
                search_text
                and search_text not in searchable
            ):

                continue

            if (
                selected_year != "ALL"
                and year != selected_year
            ):

                continue

            archive_metadata = session.get(
                "_archive_metadata"
            )

            if isinstance(
                archive_metadata,
                dict
            ):

                status = str(
                    archive_metadata.get(
                        "status",
                        session.get(
                            "status",
                            ""
                        )
                    )
                ).upper()

            else:

                status = str(
                    session.get(
                        "status",
                        ""
                    )
                ).upper()

            if (
                selected_status != "ALL"
                and status != selected_status
            ):

                continue

            students = get_session_students(
                session
            )

            result_count = 0

            if status == "ARCHIVED":

                result_count = int(
                    archive_metadata.get(
                        "result_count",
                        0
                    )
                )

            else:

                result_count = len(
                    collect_session_results(
                        session
                    )
                )

            archived_at = ""

            if isinstance(
                archive_metadata,
                dict
            ):

                archived_at = archive_metadata.get(
                    "archived_at",
                    ""
                )

            self.tree.insert(
                "",
                "end",
                iid=session_id,
                values=(

                    session_id,

                    year,

                    exam_id,

                    exam_name,

                    pattern_name,

                    exam_date,

                    session.get(
                        "start_time",
                        ""
                    ),

                    (
                        f"{session.get('duration_minutes', '')} "
                        "minutes"
                    ),

                    len(students),

                    result_count,

                    status,

                    archived_at
                )
            )


    # ========================================================
    # GET SELECTED SESSION
    # ========================================================

    def get_selected_session(
        self
    ):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Select Session",
                (
                    "Please select an examination "
                    "session first."
                ),
                parent=self.root
            )

            return None

        session_id = selected[0]

        for session in self.all_sessions:

            if str(
                session.get(
                    "session_id",
                    ""
                )
            ) == str(
                session_id
            ):

                return session

        return None


    # ========================================================
    # VIEW SESSION DETAILS
    # ========================================================

    def view_session(self):

        session = self.get_selected_session()

        if session is None:

            return

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Exam Session Details"
        )

        window.geometry(
            "900x750"
        )


        window.transient(
            self.root
        )


        # Maximize the Exam Session Details window
        maximize_window(
            window
        )


        frame = tk.Frame(
            window,
            bg="#f4f6f8"
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(20,5)
        )

        tk.Label(
            frame,
            text="EXAM SESSION DETAILS",
            font=("Arial", 22, "bold"),
            bg="#f4f6f8",
            fg="#111827"
        ).pack(
            pady=(0, 20)
        )

        fields = [

            (
                "Session ID",
                "session_id"
            ),

            (
                "Academic Year",
                None
            ),

            (
                "Exam ID",
                "exam_id"
            ),

            (
                "Exam Name",
                "exam_name"
            ),

            (
                "Pattern ID",
                "pattern_id"
            ),

            (
                "Pattern Name",
                "pattern_name"
            ),

            (
                "Exam Date",
                "exam_date"
            ),

            (
                "Start Time",
                "start_time"
            ),

            (
                "Duration",
                "duration_minutes"
            ),

            (
                "Total Questions",
                "total_questions"
            ),

            (
                "Total Marks",
                "total_marks"
            ),

            (
                "Students",
                None
            ),

            (
                "Results",
                None
            ),

            (
                "Status",
                "status"
            ),

            (
                "Created At",
                "created_at"
            ),

            (
                "Archived At",
                "archived_at"
            )
        ]

        values_frame = tk.Frame(
            frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        values_frame.pack(
            fill="both",
            expand=True
        )

        archive_metadata = session.get(
            "_archive_metadata"
        )

        for index, (
            label,
            key
        ) in enumerate(fields):

            if key is None:

                if label == "Academic Year":

                    value = self.get_academic_year(
                        session
                    )

                elif label == "Students":

                    value = len(
                        get_session_students(
                            session
                        )
                    )

                elif label == "Results":

                    if isinstance(
                        archive_metadata,
                        dict
                    ):

                        value = archive_metadata.get(
                            "result_count",
                            0
                        )

                    else:

                        value = len(
                            collect_session_results(
                                session
                            )
                        )

                else:

                    value = ""

            else:

                value = session.get(
                    key,
                    ""
                )

                if (
                    label == "Archived At"
                    and not value
                    and isinstance(
                        archive_metadata,
                        dict
                    )
                ):

                    value = archive_metadata.get(
                        "archived_at",
                        ""
                    )

            if label == "Duration" and value:

                value = f"{value} minutes"

            tk.Label(
                values_frame,
                text=label,
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#374151",
                anchor="w",
                width=25
            ).grid(
                row=index,
                column=0,
                sticky="w",
                padx=15,
                pady=8
            )

            tk.Label(
                values_frame,
                text=str(value),
                font=("Arial", 10),
                bg="white",
                fg="#111827",
                anchor="w"
            ).grid(
                row=index,
                column=1,
                sticky="w",
                padx=15,
                pady=8
            )

        # ====================================================
        # BOTTOM BUTTON BAR
        # ====================================================

        button_frame = tk.Frame(
            window,
            bg="#f4f6f8",
            height=60
        )

        button_frame.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=(5,20)
        )

        button_frame.pack_propagate(False)


        tk.Button(
            button_frame,
            text="CLOSE",
            font=("Arial", 10, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            bd=0,
            padx=30,
            pady=6,
            command=window.destroy
        ).pack(pady=5)


    # ========================================================
    # VIEW QUESTIONS
    # ========================================================

    def view_questions(self):

        session = self.get_selected_session()

        if session is None:

            return

        session_id = str(
            session.get(
                "session_id",
                ""
            )
        )

        archive_dir = get_archive_directory(
            session_id
        )

        snapshot_file = os.path.join(
            archive_dir,
            "question_snapshot.json"
        )

        # ----------------------------------------------------
        # If archived, read archive snapshot.
        # ----------------------------------------------------

        if os.path.exists(
            snapshot_file
        ):

            snapshot = load_json(
                snapshot_file
            )

        else:

            exam = load_exam_definition(
                session.get(
                    "exam_id",
                    ""
                )
            )

            snapshot = create_question_snapshot(
                session,
                exam
            )

        if not isinstance(
            snapshot,
            dict
        ):

            messagebox.showerror(
                "Questions",
                "Question snapshot could not be loaded.",
                parent=self.root
            )

            return

        questions = snapshot.get(
            "questions",
            []
        )

        window = tk.Toplevel(
            self.root
        )

        window.title(
            f"Questions - {session_id}"
        )

        window.geometry(
            "1050x700"
        )

        # ----------------------------------------------------
        # MAXIMIZE VIEW QUESTIONS WINDOW
        # ----------------------------------------------------

        try:

            window.state("zoomed")

        except Exception:

            try:

                window.attributes(
                    "-zoomed",
                    True
                )

            except Exception:

                pass

    
        window.transient(
            self.root
        )

        frame = tk.Frame(
            window,
            bg="#f4f6f8"
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            frame,
            text=(
                f"QUESTION SNAPSHOT\n"
                f"Session: {session_id}"
            ),
            font=("Arial", 20, "bold"),
            bg="#f4f6f8",
            fg="#111827"
        ).pack(
            pady=(0, 15)
        )

        text_frame = tk.Frame(
            frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        text_frame.pack(
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            text_frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        text = tk.Text(
            text_frame,
            font=("Arial", 11),
            wrap="word",
            yscrollcommand=scrollbar.set,
            bg="white",
            fg="#111827",
            padx=15,
            pady=15
        )

        text.pack(
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=text.yview
        )

        if isinstance(
            questions,
            list
        ):

            for index, question in enumerate(
                questions,
                start=1
            ):

                text.insert(
                    "end",
                    f"{index}. "
                )

                if isinstance(
                    question,
                    dict
                ):

                    question_text = (
                        question.get(
                            "question",
                            question.get(
                                "text",
                                str(question)
                            )
                        )
                    )

                    text.insert(
                        "end",
                        str(
                            question_text
                        )
                    )

                else:

                    text.insert(
                        "end",
                        str(question)
                    )

                text.insert(
                    "end",
                    "\n\n"
                )

        else:

            text.insert(
                "end",
                json.dumps(
                    questions,
                    indent=4,
                    ensure_ascii=False
                )
            )

        text.config(
            state="disabled"
        )

        # ====================================================
        # BOTTOM BUTTON BAR
        # ====================================================

        button_frame = tk.Frame(
            window,
            bg="#f4f6f8",
            height=60
        )

        button_frame.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=(5, 20)
        )

        button_frame.pack_propagate(False)

        tk.Button(
            button_frame,
            text="CLOSE",
            font=("Arial", 10, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            bd=0,
            padx=30,
            pady=6,
            command=window.destroy
        ).pack(
            pady=5
        )

    # ========================================================
    # VIEW STUDENTS
    # ========================================================

    def view_students(self):

        session = self.get_selected_session()

        if session is None:

            return

        session_id = str(
            session.get(
                "session_id",
                ""
            )
        )

        archive_dir = get_archive_directory(
            session_id
        )

        students_file = os.path.join(
            archive_dir,
            "students.json"
        )

        if os.path.exists(
            students_file
        ):

            data = load_json(
                students_file
            )

            if isinstance(
                data,
                dict
            ):

                students = data.get(
                    "students",
                    []
                )

            elif isinstance(
                data,
                list
            ):

                students = data

            else:

                students = []

        else:

            students = get_session_students(
                session
            )

        window = tk.Toplevel(
            self.root
        )

        window.title(
            f"Students - {session_id}"
        )

        window.geometry(
            "1050x650"
        )

        window.transient(
            self.root
        )

        # ----------------------------------------------------
        # MAXIMIZE STUDENTS WINDOW
        # ----------------------------------------------------

        maximize_window(
            window
        )


        frame = tk.Frame(
            window,
            bg="#f4f6f8"
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            frame,
            text=(
                f"EXAM SESSION STUDENTS\n"
                f"{session_id}"
            ),
            font=("Arial", 20, "bold"),
            bg="#f4f6f8",
            fg="#111827"
        ).pack(
            pady=(0, 15)
        )

        table = ttk.Treeview(
            frame,
            columns=(
                "student_id",
                "student_name",
                "roll_number",
                "email",
                "status"
            ),
            show="headings"
        )

        headings = {

            "student_id":
                "Student ID",

            "student_name":
                "Student Name",

            "roll_number":
                "Roll Number",

            "email":
                "Email",

            "status":
                "Status"
        }

        for column in headings:

            table.heading(
                column,
                text=headings[column]
            )

            table.column(
                column,
                width=180,
                anchor="center"
            )

        table.pack(
            fill="both",
            expand=True
        )

        for student in students:

            if not isinstance(
                student,
                dict
            ):

                student = {
                    "student_id":
                        str(student)
                }

            table.insert(
                "",
                "end",
                values=(

                    student.get(
                        "student_id",
                        ""
                    ),

                    student.get(
                        "student_name",
                        student.get(
                            "name",
                            ""
                        )
                    ),

                    student.get(
                        "roll_number",
                        ""
                    ),

                    student.get(
                        "email",
                        ""
                    ),

                    student.get(
                        "status",
                        ""
                    )
                )
            )

        # ====================================================
        # BOTTOM BUTTON BAR
        # ====================================================

        button_frame = tk.Frame(
            window,
            bg="#f4f6f8",
            height=60
        )

        button_frame.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=(5, 20)
        )

        button_frame.pack_propagate(False)

        tk.Button(
            button_frame,
            text="CLOSE",
            font=("Arial", 10, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            bd=0,
            padx=30,
            pady=6,
            command=window.destroy
        ).pack(
            pady=5
        )

    # ========================================================
    # ARCHIVE SELECTED
    # ========================================================

    def archive_selected(self):

        session = self.get_selected_session()

        if session is None:

            return

        session_id = session.get(
            "session_id",
            ""
        )

        status = str(
            session.get(
                "status",
                ""
            )
        ).upper()

        if status == "ARCHIVED":

            messagebox.showinfo(
                "Already Archived",
                (
                    "This examination session "
                    "is already archived."
                ),
                parent=self.root
            )

            return

        student_count = len(
            get_session_students(
                session
            )
        )

        result_count = len(
            collect_session_results(
                session
            )
        )

        answer = messagebox.askyesno(
            "Archive Examination Session",
            (
                "The following examination session "
                "will be archived:\n\n"

                f"Session ID: {session_id}\n"
                f"Exam: {session.get('exam_name', '')}\n"
                f"Exam ID: {session.get('exam_id', '')}\n"
                f"Academic Year: "
                f"{self.get_academic_year(session)}\n"
                f"Exam Date: "
                f"{session.get('exam_date', '')}\n"
                f"Students: {student_count}\n"
                f"Results: {result_count}\n\n"

                "The questions, students and results "
                "will be copied into a separate session "
                "archive.\n\n"

                "Continue?"
            ),
            parent=self.root
        )

        if not answer:

            return

        try:

            metadata = archive_exam_session(
                session
            )

            self.refresh_sessions()

            messagebox.showinfo(
                "Exam Session Archived",
                (
                    "Examination session archived successfully.\n\n"

                    f"Session ID: "
                    f"{metadata['session_id']}\n"

                    f"Academic Year: "
                    f"{metadata['academic_year']}\n"

                    f"Students: "
                    f"{metadata['student_count']}\n"

                    f"Results: "
                    f"{metadata['result_count']}\n\n"

                    "The archived data is now separated "
                    "from future examination sessions."
                ),
                parent=self.root
            )

        except Exception as e:

            messagebox.showerror(
                "Archive Error",
                (
                    "Could not archive the examination session.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # RESTORE SELECTED
    # ========================================================

    def restore_selected(self):

        session = self.get_selected_session()

        if session is None:

            return

        archive_metadata = session.get(
            "_archive_metadata"
        )

        if not isinstance(
            archive_metadata,
            dict
        ):

            messagebox.showinfo(
                "Restore",
                (
                    "This session does not have "
                    "an archive."
                ),
                parent=self.root
            )

            return

        status = str(
            archive_metadata.get(
                "status",
                ""
            )
        ).upper()

        if status != "ARCHIVED":

            messagebox.showinfo(
                "Restore",
                (
                    "Only archived sessions "
                    "can be restored."
                ),
                parent=self.root
            )

            return

        session_id = session.get(
            "session_id",
            ""
        )

        answer = messagebox.askyesno(
            "Restore Examination Session",
            (
                f"Do you want to restore:\n\n"
                f"Session ID: {session_id}\n\n"

                "The original session information "
                "will be restored.\n\n"

                "The archived questions and results "
                "will remain preserved."
            ),
            parent=self.root
        )

        if not answer:

            return

        try:

            restore_exam_session(
                archive_metadata
            )

            self.refresh_sessions()

            messagebox.showinfo(
                "Session Restored",
                (
                    f"{session_id} has been restored successfully.\n\n"
                    "The original historical data "
                    "has been preserved."
                ),
                parent=self.root
            )

        except Exception as e:

            messagebox.showerror(
                "Restore Error",
                (
                    "Could not restore the examination session.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # DELETE SELECTED
    # ========================================================

    def delete_selected(self):

        session = self.get_selected_session()

        if session is None:

            return

        archive_metadata = session.get(
            "_archive_metadata"
        )

        if not isinstance(
            archive_metadata,
            dict
        ):

            messagebox.showwarning(
                "Delete Archive",
                (
                    "This examination session "
                    "has no archive."
                ),
                parent=self.root
            )

            return

        status = str(
            archive_metadata.get(
                "status",
                ""
            )
        ).upper()

        if status != "ARCHIVED":

            messagebox.showwarning(
                "Delete Archive",
                (
                    "Only archived sessions can "
                    "be permanently deleted."
                ),
                parent=self.root
            )

            return

        session_id = session.get(
            "session_id",
            ""
        )

        answer = messagebox.askyesno(
            "Delete Exam Archive",
            (
                "WARNING\n\n"

                f"Session: {session_id}\n\n"

                "This will permanently delete the "
                "archived copy containing:\n\n"

                "• Exam information\n"
                "• Question snapshot\n"
                "• Student list\n"
                "• Student results\n\n"

                "The original session file will NOT "
                "be deleted.\n\n"

                "This action cannot be undone.\n\n"

                "Continue?"
            ),
            parent=self.root
        )

        if not answer:

            return

        confirm = messagebox.askyesno(
            "Permanent Delete",
            (
                f"Are you absolutely sure you want "
                f"to permanently delete archive "
                f"{session_id}?"
            ),
            parent=self.root
        )

        if not confirm:

            return

        try:

            delete_archived_session(
                archive_metadata
            )

            self.refresh_sessions()

            messagebox.showinfo(
                "Archive Deleted",
                (
                    f"Archive {session_id} "
                    "was permanently deleted.\n\n"
                    "The original examination session "
                    "was not deleted."
                ),
                parent=self.root
            )

        except Exception as e:

            messagebox.showerror(
                "Delete Error",
                (
                    "Could not delete the archive.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # BACK
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

    ExamArchive(
        window,
        parent_window=root
    )

    root.mainloop()

