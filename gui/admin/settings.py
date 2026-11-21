
# ============================================================
# SETTINGS - ADMIN CONTROL PANEL
# AI ORAL EXAMINATION SYSTEM
# ============================================================
#
# This module manages GLOBAL system settings only.
#
# It does NOT directly modify:
#   backend/exams/
#   backend/students/
#   backend/exam_patterns/
#   backend/exam_sessions/
#   backend/student_answers/
#   backend/exam_results/
#   backend/exam_archive/
#
# Backup & Safety:
#   - Creates real JSON backups
#   - Can backup before delete
#   - Can backup before archive
#   - Keeps the newest 10 backups by default
#   - Automatically removes older backups
#   - Supports safe restoration
#
# DIRECT TEST:
#     python settings.py
#
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
import tempfile
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

STUDENT_ANSWERS_DIR = os.path.join(
    BACKEND_DIR,
    "student_answers"
)

RESULTS_DIR = os.path.join(
    BACKEND_DIR,
    "exam_results"
)

ARCHIVE_DIR = os.path.join(
    BACKEND_DIR,
    "exam_archive"
)

SETTINGS_FILE = os.path.join(
    BACKEND_DIR,
    "settings.json"
)

BACKUP_DIR = os.path.join(
    BACKEND_DIR,
    "backups"
)


# ============================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================

for directory in (
    BACKEND_DIR,
    EXAMS_DIR,
    STUDENTS_DIR,
    PATTERNS_DIR,
    SESSIONS_DIR,
    STUDENT_ANSWERS_DIR,
    RESULTS_DIR,
    ARCHIVE_DIR,
    BACKUP_DIR
):
    os.makedirs(
        directory,
        exist_ok=True
    )


# ============================================================
# DEFAULT SETTINGS
# ============================================================

DEFAULT_SETTINGS = {

    "system": {
        "application_name": "AI Oral Examination System",
        "auto_backup": True,
        "confirm_before_delete": True,
        "confirm_before_archive": True,
        "preserve_json_structure": True
    },

    "oral_exam": {
        "default_duration_minutes": 30,
        "default_answer_time_seconds": 60,
        "pass_percentage": 50.0,
        "allow_retake": True,
        "maximum_attempts": 0,
        "automatic_submission": True
    },

    "questions": {
        "show_question_number": True,
        "allow_question_navigation": True,
        "shuffle_questions": False,
        "shuffle_students": False,
        "show_expected_answer_to_student": False,
        "save_question_answer_time": True
    },

    "results": {
        "automatic_result_calculation": True,
        "show_percentage": True,
        "show_pass_fail": True,
        "save_student_answers": True,
        "save_attempt_history": True
    },

    "students": {
        "allow_duplicate_student_name": False,
        "require_student_id": True,
        "allow_student_retake": True
    },

    "exam_archive": {
        "enabled": True,
        "keep_question_snapshot": True,
        "keep_student_snapshot": True,
        "keep_answers_snapshot": True,
        "keep_results_snapshot": True,
        "allow_restore": True,
        "allow_permanent_delete": True
    },

    "backup": {
        "enabled": True,
        "backup_before_delete": True,
        "backup_before_archive": True,
        "maximum_backup_copies": 10,
        "backup_directory": "backups",
        "include_timestamp": True
    },

    "interface": {
        "window_width": 1200,
        "window_height": 800,
        "maximize_windows": True,
        "theme": "light"
    },

    "updated_at": ""
}


# ============================================================
# JSON HELPERS
# ============================================================

def deep_copy_json(data):
    return json.loads(
        json.dumps(
            data,
            ensure_ascii=False
        )
    )


def merge_settings(existing, defaults):

    if not isinstance(existing, dict):
        existing = {}

    if not isinstance(defaults, dict):
        return existing

    for key, default_value in defaults.items():

        if key not in existing:

            existing[key] = deep_copy_json(
                default_value
            )

        elif (
            isinstance(existing[key], dict)
            and isinstance(default_value, dict)
        ):

            existing[key] = merge_settings(
                existing[key],
                default_value
            )

    return existing


def load_settings():

    if not os.path.exists(
        SETTINGS_FILE
    ):

        settings = deep_copy_json(
            DEFAULT_SETTINGS
        )

        save_settings(
            settings
        )

        return settings

    try:

        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

        if not isinstance(
            data,
            dict
        ):

            raise ValueError(
                "settings.json must contain a JSON object."
            )

        settings = merge_settings(
            data,
            DEFAULT_SETTINGS
        )

        return settings

    except Exception as error:

        print(
            "Could not load settings:",
            error
        )

        return deep_copy_json(
            DEFAULT_SETTINGS
        )


def save_settings(settings):

    if not isinstance(
        settings,
        dict
    ):

        raise ValueError(
            "Settings must be a dictionary."
        )

    settings["updated_at"] = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    os.makedirs(
        BACKEND_DIR,
        exist_ok=True
    )

    temp_file = None

    try:

        fd, temp_file = tempfile.mkstemp(
            prefix="settings_",
            suffix=".tmp",
            dir=BACKEND_DIR
        )

        with os.fdopen(
            fd,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                settings,
                file,
                indent=4,
                ensure_ascii=False
            )

            file.flush()

            os.fsync(
                file.fileno()
            )

        shutil.move(
            temp_file,
            SETTINGS_FILE
        )

        temp_file = None

    finally:

        if temp_file is not None:

            try:
                os.remove(
                    temp_file
                )
            except Exception:
                pass


# ============================================================
# GET SETTING
# ============================================================

def get_setting(
    section,
    key,
    default=None
):

    settings = load_settings()

    section_data = settings.get(
        section,
        {}
    )

    if not isinstance(
        section_data,
        dict
    ):

        return default

    return section_data.get(
        key,
        default
    )


# ============================================================
# SET SETTING
# ============================================================

def set_setting(
    section,
    key,
    value
):

    settings = load_settings()

    if not isinstance(
        settings.get(section),
        dict
    ):

        settings[section] = {}

    settings[section][key] = value

    save_settings(
        settings
    )


# ============================================================
# BACKUP DIRECTORY
# ============================================================

def get_backup_directory():

    settings = load_settings()

    backup_settings = settings.get(
        "backup",
        {}
    )

    directory = backup_settings.get(
        "backup_directory",
        "backups"
    )

    if os.path.isabs(
        directory
    ):

        backup_dir = directory

    else:

        backup_dir = os.path.join(
            BACKEND_DIR,
            directory
        )

    os.makedirs(
        backup_dir,
        exist_ok=True
    )

    return backup_dir


# ============================================================
# CLEAN OLD BACKUPS
# ============================================================

def cleanup_old_backups():

    settings = load_settings()

    backup_settings = settings.get(
        "backup",
        {}
    )

    try:

        maximum = int(
            backup_settings.get(
                "maximum_backup_copies",
                10
            )
        )

    except Exception:

        maximum = 10

    if maximum < 1:
        maximum = 1

    backup_dir = get_backup_directory()

    if not os.path.exists(
        backup_dir
    ):

        return

    files = []

    for filename in os.listdir(
        backup_dir
    ):

        file_path = os.path.join(
            backup_dir,
            filename
        )

        if not os.path.isfile(
            file_path
        ):
            continue

        if not filename.lower().endswith(
            ".json"
        ):
            continue

        try:

            modified_time = os.path.getmtime(
                file_path
            )

            files.append(
                (
                    modified_time,
                    file_path
                )
            )

        except Exception:
            continue

    files.sort(
        key=lambda item: item[0],
        reverse=True
    )

    old_files = files[
        maximum:
    ]

    for _, file_path in old_files:

        try:

            os.remove(
                file_path
            )

        except Exception as error:

            print(
                "Could not remove old backup:",
                file_path,
                error
            )


# ============================================================
# CREATE BACKUP
# ============================================================

def create_backup(
    source_file,
    reason="manual"
):

    if not source_file:
        return None

    if not os.path.exists(
        source_file
    ):
        return None

    settings = load_settings()

    backup_settings = settings.get(
        "backup",
        {}
    )

    if not backup_settings.get(
        "enabled",
        True
    ):

        return None

    backup_dir = get_backup_directory()

    filename = os.path.basename(
        source_file
    )

    name, extension = os.path.splitext(
        filename
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    safe_reason = str(
        reason
    ).replace(
        " ",
        "_"
    )

    backup_filename = (
        f"{name}"
        f"__{safe_reason}"
        f"__{timestamp}"
        f"{extension}"
    )

    backup_file = os.path.join(
        backup_dir,
        backup_filename
    )

    try:

        shutil.copy2(
            source_file,
            backup_file
        )

        cleanup_old_backups()

        return backup_file

    except Exception as error:

        print(
            "Could not create backup:",
            error
        )

        return None


# ============================================================
# BACKUP BEFORE DELETE
# ============================================================

def backup_before_delete(
    source_file
):

    settings = load_settings()

    backup_settings = settings.get(
        "backup",
        {}
    )

    if not backup_settings.get(
        "backup_before_delete",
        True
    ):

        return None

    return create_backup(
        source_file,
        "before_delete"
    )


# ============================================================
# BACKUP BEFORE ARCHIVE
# ============================================================

def backup_before_archive(
    source_file
):

    settings = load_settings()

    backup_settings = settings.get(
        "backup",
        {}
    )

    if not backup_settings.get(
        "backup_before_archive",
        True
    ):

        return None

    return create_backup(
        source_file,
        "before_archive"
    )


# ============================================================
# BACKUP DIRECTORY
# ============================================================

def create_directory_backup(
    directory,
    reason="manual"
):

    if not os.path.exists(
        directory
    ):

        return []

    settings = load_settings()

    backup_settings = settings.get(
        "backup",
        {}
    )

    if not backup_settings.get(
        "enabled",
        True
    ):

        return []

    backup_files = []

    for filename in os.listdir(
        directory
    ):

        source_file = os.path.join(
            directory,
            filename
        )

        if not os.path.isfile(
            source_file
        ):
            continue

        if not filename.lower().endswith(
            ".json"
        ):
            continue

        try:

            backup_file = create_backup(
                source_file,
                reason
            )

            if backup_file:
                backup_files.append(
                    backup_file
                )

        except Exception as error:

            print(
                "Backup failed:",
                source_file,
                error
            )

    cleanup_old_backups()

    return backup_files


# ============================================================
# BACKUP COUNT
# ============================================================

def get_backup_count():

    backup_dir = get_backup_directory()

    if not os.path.exists(
        backup_dir
    ):

        return 0

    count = 0

    for filename in os.listdir(
        backup_dir
    ):

        file_path = os.path.join(
            backup_dir,
            filename
        )

        if (
            os.path.isfile(file_path)
            and filename.lower().endswith(".json")
        ):

            count += 1

    return count


# ============================================================
# LIST BACKUPS
# ============================================================

def list_backups():

    backup_dir = get_backup_directory()

    if not os.path.exists(
        backup_dir
    ):

        return []

    backups = []

    for filename in os.listdir(
        backup_dir
    ):

        file_path = os.path.join(
            backup_dir,
            filename
        )

        if not os.path.isfile(
            file_path
        ):
            continue

        if not filename.lower().endswith(
            ".json"
        ):
            continue

        try:

            created_at = datetime.fromtimestamp(
                os.path.getmtime(
                    file_path
                )
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        except Exception:

            created_at = ""

        backups.append(
            {
                "filename": filename,
                "path": file_path,
                "created_at": created_at
            }
        )

    backups.sort(
        key=lambda item: item["created_at"],
        reverse=True
    )

    return backups


# ============================================================
# RESTORE BACKUP
# ============================================================

def restore_backup(
    backup_file,
    destination_file
):

    if not os.path.exists(
        backup_file
    ):

        raise FileNotFoundError(
            "Backup file does not exist."
        )

    if os.path.exists(
        destination_file
    ):

        create_backup(
            destination_file,
            "before_restore"
        )

    destination_directory = os.path.dirname(
        destination_file
    )

    os.makedirs(
        destination_directory,
        exist_ok=True
    )

    shutil.copy2(
        backup_file,
        destination_file
    )

    return destination_file


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

    except Exception as error:

        print(
            "Could not maximize window:",
            error
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
# SETTINGS WINDOW
# ============================================================

class Settings:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root
        self.parent_window = parent_window

        self.settings = load_settings()

        self.vars = {}

        self.root.title(
            "Settings - AI Oral Examination System"
        )

        self.root.geometry(
            "1250x850"
        )

        self.root.minsize(
            1050,
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

        self.create_interface()

        self.load_values()


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
            text="SYSTEM SETTINGS",
            font=("Arial", 25, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(18, 3)
        )

        tk.Label(
            header,
            text=(
                "Configure Exam Management, Oral Exam Timing, "
                "Questions, Results, Students, Archive and Safety"
            ),
            font=("Arial", 11),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack()

        outer = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        outer.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
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

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.content_frame = tk.Frame(
            canvas,
            bg="#f4f6f8"
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=self.content_frame,
            anchor="nw"
        )

        def configure_scroll_region(event=None):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        def configure_canvas_width(event):

            canvas.itemconfig(
                canvas_window,
                width=event.width
            )

        self.content_frame.bind(
            "<Configure>",
            configure_scroll_region
        )

        canvas.bind(
            "<Configure>",
            configure_canvas_width
        )

        self.create_system_section()

        self.create_oral_exam_section()

        self.create_questions_section()

        self.create_results_section()

        self.create_students_section()

        self.create_archive_section()

        self.create_backup_section()

        self.create_interface_section()

        button_frame = tk.Frame(
            main_frame,
            bg="#e5e7eb",
            height=75
        )

        button_frame.pack(
            fill="x",
            side="bottom"
        )

        button_frame.pack_propagate(
            False
        )

        tk.Button(
            button_frame,
            text="RESET TO DEFAULTS",
            font=("Arial", 10, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.reset_defaults
        ).pack(
            side="left",
            padx=20,
            pady=15
        )

        tk.Button(
            button_frame,
            text="SAVE SETTINGS",
            font=("Arial", 10, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.save
        ).pack(
            side="right",
            padx=10,
            pady=15
        )

        tk.Button(
            button_frame,
            text="BACK TO ADMIN CONTROL PANEL",
            font=("Arial", 10, "bold"),
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
            side="right",
            padx=10,
            pady=15
        )


    # ========================================================
    # SECTION HELPER
    # ========================================================

    def create_section(
        self,
        title,
        subtitle=""
    ):

        frame = tk.Frame(
            self.content_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        frame.pack(
            fill="x",
            padx=5,
            pady=8
        )

        header = tk.Frame(
            frame,
            bg="#eef2ff"
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text=title,
            font=("Arial", 14, "bold"),
            bg="#eef2ff",
            fg="#1f2937"
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 2)
        )

        if subtitle:

            tk.Label(
                header,
                text=subtitle,
                font=("Arial", 9),
                bg="#eef2ff",
                fg="#6b7280"
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 10)
            )

        body = tk.Frame(
            frame,
            bg="white"
        )

        body.pack(
            fill="x",
            padx=15,
            pady=10
        )

        return body


    # ========================================================
    # CHECKBOX
    # ========================================================

    def add_checkbutton(
        self,
        parent,
        section,
        key,
        text
    ):

        variable = tk.BooleanVar()

        self.vars[
            f"{section}.{key}"
        ] = variable

        tk.Checkbutton(
            parent,
            text=text,
            variable=variable,
            font=("Arial", 10),
            bg="white",
            activebackground="white",
            anchor="w"
        ).pack(
            fill="x",
            pady=4
        )


    # ========================================================
    # ENTRY
    # ========================================================

    def add_entry(
        self,
        parent,
        section,
        key,
        label,
        width=15
    ):

        row = tk.Frame(
            parent,
            bg="white"
        )

        row.pack(
            fill="x",
            pady=5
        )

        tk.Label(
            row,
            text=label,
            font=("Arial", 10),
            bg="white",
            fg="#374151",
            width=38,
            anchor="w"
        ).pack(
            side="left"
        )

        variable = tk.StringVar()

        self.vars[
            f"{section}.{key}"
        ] = variable

        entry = tk.Entry(
            row,
            textvariable=variable,
            font=("Arial", 10),
            width=width
        )

        entry.pack(
            side="left"
        )

        return entry


    # ========================================================
    # SYSTEM
    # ========================================================

    def create_system_section(self):

        body = self.create_section(
            "SYSTEM BEHAVIOR",
            "General behavior of the AI Oral Examination System."
        )

        self.add_entry(
            body,
            "system",
            "application_name",
            "Application Name:",
            45
        )

        self.add_checkbutton(
            body,
            "system",
            "auto_backup",
            "Enable automatic backup behavior"
        )

        self.add_checkbutton(
            body,
            "system",
            "confirm_before_delete",
            "Ask for confirmation before deleting data"
        )

        self.add_checkbutton(
            body,
            "system",
            "confirm_before_archive",
            "Ask for confirmation before archiving exams"
        )

        self.add_checkbutton(
            body,
            "system",
            "preserve_json_structure",
            "Preserve existing JSON structure"
        )


    # ========================================================
    # ORAL EXAM
    # ========================================================

    def create_oral_exam_section(self):

        body = self.create_section(
            "ORAL EXAM TIMING & RULES",
            (
                "These values are global defaults. "
                "Existing exam-specific JSON values are not changed."
            )
        )

        self.add_entry(
            body,
            "oral_exam",
            "default_duration_minutes",
            "Default Exam Duration (minutes):"
        )

        self.add_entry(
            body,
            "oral_exam",
            "default_answer_time_seconds",
            "Default Answer Time (seconds):"
        )

        self.add_entry(
            body,
            "oral_exam",
            "pass_percentage",
            "Pass Percentage:"
        )

        self.add_entry(
            body,
            "oral_exam",
            "maximum_attempts",
            "Maximum Attempts (0 = unlimited):"
        )

        self.add_checkbutton(
            body,
            "oral_exam",
            "allow_retake",
            "Allow students to retake an examination"
        )

        self.add_checkbutton(
            body,
            "oral_exam",
            "automatic_submission",
            "Enable automatic submission when exam time expires"
        )


    # ========================================================
    # QUESTIONS
    # ========================================================

    def create_questions_section(self):

        body = self.create_section(
            "QUESTION SETTINGS",
            "Controls how oral examination questions behave."
        )

        self.add_checkbutton(
            body,
            "questions",
            "show_question_number",
            "Show question number to the student"
        )

        self.add_checkbutton(
            body,
            "questions",
            "allow_question_navigation",
            "Allow navigation between questions"
        )

        self.add_checkbutton(
            body,
            "questions",
            "shuffle_questions",
            "Shuffle questions for each attempt"
        )

        self.add_checkbutton(
            body,
            "questions",
            "shuffle_students",
            "Shuffle student order when starting a session"
        )

        self.add_checkbutton(
            body,
            "questions",
            "show_expected_answer_to_student",
            "Show expected answers to students"
        )

        self.add_checkbutton(
            body,
            "questions",
            "save_question_answer_time",
            "Save answer time for every question"
        )


    # ========================================================
    # RESULTS
    # ========================================================

    def create_results_section(self):

        body = self.create_section(
            "RESULT SETTINGS",
            "Controls result calculation and result history."
        )

        self.add_checkbutton(
            body,
            "results",
            "automatic_result_calculation",
            "Automatically calculate secured marks and result"
        )

        self.add_checkbutton(
            body,
            "results",
            "show_percentage",
            "Show percentage in student results"
        )

        self.add_checkbutton(
            body,
            "results",
            "show_pass_fail",
            "Show PASS / FAIL status"
        )

        self.add_checkbutton(
            body,
            "results",
            "save_student_answers",
            "Save student answers"
        )

        self.add_checkbutton(
            body,
            "results",
            "save_attempt_history",
            "Keep previous examination attempts"
        )


    # ========================================================
    # STUDENTS
    # ========================================================

    def create_students_section(self):

        body = self.create_section(
            "STUDENT SETTINGS",
            "Controls student validation and examination attempts."
        )

        self.add_checkbutton(
            body,
            "students",
            "allow_duplicate_student_name",
            "Allow students with duplicate names"
        )

        self.add_checkbutton(
            body,
            "students",
            "require_student_id",
            "Require Student ID"
        )

        self.add_checkbutton(
            body,
            "students",
            "allow_student_retake",
            "Allow student retakes"
        )


    # ========================================================
    # ARCHIVE
    # ========================================================

    def create_archive_section(self):

        body = self.create_section(
            "EXAM ARCHIVE SETTINGS",
            (
                "Archive behavior for completed examination sessions. "
                "An exam will not appear in Exam Archive until it is "
                "actually archived."
            )
        )

        self.add_checkbutton(
            body,
            "exam_archive",
            "enabled",
            "Enable Exam Archive"
        )

        self.add_checkbutton(
            body,
            "exam_archive",
            "keep_question_snapshot",
            "Keep question snapshot in archived examination"
        )

        self.add_checkbutton(
            body,
            "exam_archive",
            "keep_student_snapshot",
            "Keep student snapshot in archived examination"
        )

        self.add_checkbutton(
            body,
            "exam_archive",
            "keep_answers_snapshot",
            "Keep student answers in archived examination"
        )

        self.add_checkbutton(
            body,
            "exam_archive",
            "keep_results_snapshot",
            "Keep student results in archived examination"
        )

        self.add_checkbutton(
            body,
            "exam_archive",
            "allow_restore",
            "Allow restoring an archived examination"
        )

        self.add_checkbutton(
            body,
            "exam_archive",
            "allow_permanent_delete",
            "Allow permanent deletion of an archived examination"
        )


    # ========================================================
    # BACKUP & SAFETY
    # ========================================================

    def create_backup_section(self):

        body = self.create_section(
            "BACKUP & SAFETY",
            (
                "Real safety backups are created before deletion "
                "or archiving when enabled."
            )
        )

        self.add_checkbutton(
            body,
            "backup",
            "enabled",
            "Enable automatic safety backups"
        )

        self.add_checkbutton(
            body,
            "backup",
            "backup_before_delete",
            "Create a backup before deleting data"
        )

        self.add_checkbutton(
            body,
            "backup",
            "backup_before_archive",
            "Create a backup before archiving an examination"
        )

        self.add_entry(
            body,
            "backup",
            "maximum_backup_copies",
            "Maximum Backup Copies:",
            10
        )

        self.add_entry(
            body,
            "backup",
            "backup_directory",
            "Backup Directory:",
            35
        )

        backup_info = tk.Label(
            body,
            text=(
                "Default safety limit: 10 newest backup copies.\n"
                "When the limit is exceeded, the oldest backup "
                "is automatically removed.\n"
                "Backups are stored separately from your existing "
                "exam JSON files."
            ),
            font=("Arial", 9),
            bg="white",
            fg="#6b7280",
            justify="left",
            anchor="w"
        )

        backup_info.pack(
            fill="x",
            pady=(8, 5)
        )

        count_label = tk.Label(
            body,
            text="Current Backup Count: 0",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151",
            anchor="w"
        )

        count_label.pack(
            fill="x",
            pady=4
        )

        self.backup_count_label = count_label

        tk.Button(
            body,
            text="REFRESH BACKUP COUNT",
            font=("Arial", 9, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=self.refresh_backup_count
        ).pack(
            anchor="w",
            pady=(5, 0)
        )


    # ========================================================
    # INTERFACE
    # ========================================================

    def create_interface_section(self):

        body = self.create_section(
            "INTERFACE SETTINGS",
            "General window behavior."
        )

        self.add_entry(
            body,
            "interface",
            "window_width",
            "Default Window Width:"
        )

        self.add_entry(
            body,
            "interface",
            "window_height",
            "Default Window Height:"
        )

        self.add_checkbutton(
            body,
            "interface",
            "maximize_windows",
            "Maximize application windows"
        )

        self.add_entry(
            body,
            "interface",
            "theme",
            "Theme:",
            15
        )


    # ========================================================
    # LOAD VALUES
    # ========================================================

    def load_values(self):

        self.settings = merge_settings(
            self.settings,
            DEFAULT_SETTINGS
        )

        for variable_name, variable in self.vars.items():

            try:

                section, key = variable_name.split(
                    ".",
                    1
                )

                value = self.settings.get(
                    section,
                    {}
                ).get(
                    key,
                    ""
                )

                variable.set(
                    value
                )

            except Exception as error:

                print(
                    "Could not load setting:",
                    variable_name,
                    error
                )

        self.refresh_backup_count()


    # ========================================================
    # REFRESH BACKUP COUNT
    # ========================================================

    def refresh_backup_count(self):

        try:

            count = get_backup_count()

            if hasattr(
                self,
                "backup_count_label"
            ):

                self.backup_count_label.config(
                    text=f"Current Backup Count: {count}"
                )

        except Exception as error:

            print(
                "Could not count backups:",
                error
            )


    # ========================================================
    # BOOLEAN
    # ========================================================

    def get_bool(
        self,
        section,
        key
    ):

        variable = self.vars.get(
            f"{section}.{key}"
        )

        if variable is None:
            return False

        return bool(
            variable.get()
        )


    # ========================================================
    # INTEGER VALIDATION
    # ========================================================

    def validate_integer(
        self,
        value,
        field_name,
        minimum=0
    ):

        try:

            number = int(
                str(value).strip()
            )

        except Exception:

            raise ValueError(
                f"{field_name} must be a whole number."
            )

        if number < minimum:

            raise ValueError(
                f"{field_name} cannot be less than {minimum}."
            )

        return number


    # ========================================================
    # FLOAT VALIDATION
    # ========================================================

    def validate_float(
        self,
        value,
        field_name,
        minimum=0.0,
        maximum=None
    ):

        try:

            number = float(
                str(value).strip()
            )

        except Exception:

            raise ValueError(
                f"{field_name} must be a number."
            )

        if number < minimum:

            raise ValueError(
                f"{field_name} cannot be less than {minimum}."
            )

        if (
            maximum is not None
            and number > maximum
        ):

            raise ValueError(
                f"{field_name} cannot be greater than {maximum}."
            )

        return number


    # ========================================================
    # COLLECT SETTINGS
    # ========================================================

    def collect_settings(self):

        new_settings = merge_settings(
            deep_copy_json(self.settings),
            DEFAULT_SETTINGS
        )

        # ----------------------------------------------------
        # SYSTEM
        # ----------------------------------------------------

        new_settings["system"][
            "application_name"
        ] = self.vars[
            "system.application_name"
        ].get().strip()

        new_settings["system"][
            "auto_backup"
        ] = self.get_bool(
            "system",
            "auto_backup"
        )

        new_settings["system"][
            "confirm_before_delete"
        ] = self.get_bool(
            "system",
            "confirm_before_delete"
        )

        new_settings["system"][
            "confirm_before_archive"
        ] = self.get_bool(
            "system",
            "confirm_before_archive"
        )

        new_settings["system"][
            "preserve_json_structure"
        ] = self.get_bool(
            "system",
            "preserve_json_structure"
        )

        # ----------------------------------------------------
        # ORAL EXAM
        # ----------------------------------------------------

        duration = self.validate_integer(
            self.vars[
                "oral_exam.default_duration_minutes"
            ].get(),
            "Default Exam Duration",
            1
        )

        answer_time = self.validate_integer(
            self.vars[
                "oral_exam.default_answer_time_seconds"
            ].get(),
            "Default Answer Time",
            1
        )

        pass_percentage = self.validate_float(
            self.vars[
                "oral_exam.pass_percentage"
            ].get(),
            "Pass Percentage",
            0.0,
            100.0
        )

        maximum_attempts = self.validate_integer(
            self.vars[
                "oral_exam.maximum_attempts"
            ].get(),
            "Maximum Attempts",
            0
        )

        new_settings["oral_exam"][
            "default_duration_minutes"
        ] = duration

        new_settings["oral_exam"][
            "default_answer_time_seconds"
        ] = answer_time

        new_settings["oral_exam"][
            "pass_percentage"
        ] = pass_percentage

        new_settings["oral_exam"][
            "maximum_attempts"
        ] = maximum_attempts

        new_settings["oral_exam"][
            "allow_retake"
        ] = self.get_bool(
            "oral_exam",
            "allow_retake"
        )

        new_settings["oral_exam"][
            "automatic_submission"
        ] = self.get_bool(
            "oral_exam",
            "automatic_submission"
        )

        # ----------------------------------------------------
        # QUESTIONS
        # ----------------------------------------------------

        question_keys = [
            "show_question_number",
            "allow_question_navigation",
            "shuffle_questions",
            "shuffle_students",
            "show_expected_answer_to_student",
            "save_question_answer_time"
        ]

        for key in question_keys:

            new_settings["questions"][key] = (
                self.get_bool(
                    "questions",
                    key
                )
            )

        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        result_keys = [
            "automatic_result_calculation",
            "show_percentage",
            "show_pass_fail",
            "save_student_answers",
            "save_attempt_history"
        ]

        for key in result_keys:

            new_settings["results"][key] = (
                self.get_bool(
                    "results",
                    key
                )
            )

        # ----------------------------------------------------
        # STUDENTS
        # ----------------------------------------------------

        student_keys = [
            "allow_duplicate_student_name",
            "require_student_id",
            "allow_student_retake"
        ]

        for key in student_keys:

            new_settings["students"][key] = (
                self.get_bool(
                    "students",
                    key
                )
            )

        # ----------------------------------------------------
        # EXAM ARCHIVE
        # ----------------------------------------------------

        archive_keys = [
            "enabled",
            "keep_question_snapshot",
            "keep_student_snapshot",
            "keep_answers_snapshot",
            "keep_results_snapshot",
            "allow_restore",
            "allow_permanent_delete"
        ]

        for key in archive_keys:

            new_settings["exam_archive"][key] = (
                self.get_bool(
                    "exam_archive",
                    key
                )
            )

        # ----------------------------------------------------
        # BACKUP
        # ----------------------------------------------------

        new_settings["backup"][
            "enabled"
        ] = self.get_bool(
            "backup",
            "enabled"
        )

        new_settings["backup"][
            "backup_before_delete"
        ] = self.get_bool(
            "backup",
            "backup_before_delete"
        )

        new_settings["backup"][
            "backup_before_archive"
        ] = self.get_bool(
            "backup",
            "backup_before_archive"
        )

        maximum_backup_copies = self.validate_integer(
            self.vars[
                "backup.maximum_backup_copies"
            ].get(),
            "Maximum Backup Copies",
            1
        )

        backup_directory = self.vars[
            "backup.backup_directory"
        ].get().strip()

        if not backup_directory:

            backup_directory = "backups"

        new_settings["backup"][
            "maximum_backup_copies"
        ] = maximum_backup_copies

        new_settings["backup"][
            "backup_directory"
        ] = backup_directory

        new_settings["backup"][
            "include_timestamp"
        ] = True

        # ----------------------------------------------------
        # INTERFACE
        # ----------------------------------------------------

        window_width = self.validate_integer(
            self.vars[
                "interface.window_width"
            ].get(),
            "Window Width",
            600
        )

        window_height = self.validate_integer(
            self.vars[
                "interface.window_height"
            ].get(),
            "Window Height",
            400
        )

        theme = self.vars[
            "interface.theme"
        ].get().strip()

        if not theme:

            theme = "light"

        new_settings["interface"][
            "window_width"
        ] = window_width

        new_settings["interface"][
            "window_height"
        ] = window_height

        new_settings["interface"][
            "maximize_windows"
        ] = self.get_bool(
            "interface",
            "maximize_windows"
        )

        new_settings["interface"][
            "theme"
        ] = theme

        return new_settings


    # ========================================================
    # SAVE
    # ========================================================

    def save(self):

        try:

            new_settings = self.collect_settings()

            save_settings(
                new_settings
            )

            self.settings = new_settings

            cleanup_old_backups()

            self.refresh_backup_count()

            messagebox.showinfo(
                "Settings Saved",
                (
                    "Settings saved successfully.\n\n"
                    f"File:\n{SETTINGS_FILE}\n\n"
                    "Backup & Safety is enabled according "
                    "to the selected settings.\n\n"
                    "Existing exam, student, session, "
                    "question and result JSON files were "
                    "not modified."
                ),
                parent=self.root
            )

        except Exception as error:

            messagebox.showerror(
                "Save Error",
                (
                    "Could not save Settings.\n\n"
                    f"{error}"
                ),
                parent=self.root
            )


    # ========================================================
    # RESET DEFAULTS
    # ========================================================

    def reset_defaults(self):

        answer = messagebox.askyesno(
            "Reset Settings",
            (
                "Reset all Settings values to the "
                "system defaults?\n\n"
                "This will change only settings.json.\n"
                "Existing exams, students, sessions, "
                "answers, results and backups will not "
                "be deleted."
            ),
            parent=self.root
        )

        if not answer:
            return

        self.settings = deep_copy_json(
            DEFAULT_SETTINGS
        )

        self.load_values()

        messagebox.showinfo(
            "Defaults Loaded",
            (
                "Default Settings have been loaded "
                "into the form.\n\n"
                "Click SAVE SETTINGS to permanently save them."
            ),
            parent=self.root
        )


    # ========================================================
    # BACK
    # ========================================================

    def back(self):

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

    Settings(
        window,
        parent_window=root
    )

    root.mainloop()

