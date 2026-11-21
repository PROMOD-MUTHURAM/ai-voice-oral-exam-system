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


QUESTIONS_FILE = os.path.join(
    BACKEND_DIR,
    "questions.json"
)


# ============================================================
# STUDENT DETAILS CONFIGURATION
# ============================================================

# IMPORTANT:
# This is the SAME configuration file written by the
# Admin Control Panel -> Student Details Configuration.
#
# The previous student-side code used:
#     student_details_configuration.json
#
# while the Admin Control Panel saves:
#     student_details_config.json
#
# The mismatch is why Admin changes were not appearing here.
STUDENT_DETAILS_CONFIG_FILE = os.path.join(
    BACKEND_DIR,
    "student_details_config.json"
)

# Backward-compatible old filename. This is only used if the
# new Admin configuration file does not exist.
LEGACY_STUDENT_DETAILS_CONFIG_FILE = os.path.join(
    BACKEND_DIR,
    "student_details_configuration.json"
)


DEFAULT_STUDENT_DETAILS_CONFIG = {
    "student_id": {
        "label": "Student ID",
        "enabled": True,
        "required": True,
        "type": "text"
    },

    "student_name": {
        "label": "Student Name",
        "enabled": True,
        "required": True,
        "type": "text"
    },

    "date_of_birth": {
        "label": "Date of Birth",
        "enabled": True,
        "required": True,
        "type": "date"
    },

    "age": {
        "label": "Age",
        "enabled": False,
        "required": False,
        "type": "number"
    },

    "gender": {
        "label": "Gender",
        "enabled": True,
        "required": True,
        "type": "choice"
    },

    "email": {
        "label": "Email",
        "enabled": True,
        "required": False,
        "type": "email"
    },

    "phone": {
        "label": "Phone",
        "enabled": True,
        "required": False,
        "type": "phone"
    },

    "course": {
        "label": "Course",
        "enabled": False,
        "required": False,
        "type": "text"
    },

    "department": {
        "label": "Department",
        "enabled": False,
        "required": False,
        "type": "text"
    }
}


def load_student_details_configuration():

    config = {}

    # --------------------------------------------------------
    # Admin file has priority.
    # --------------------------------------------------------

    config_file = None

    if os.path.exists(
        STUDENT_DETAILS_CONFIG_FILE
    ):
        config_file = STUDENT_DETAILS_CONFIG_FILE

    elif os.path.exists(
        LEGACY_STUDENT_DETAILS_CONFIG_FILE
    ):
        config_file = LEGACY_STUDENT_DETAILS_CONFIG_FILE


    if config_file is not None:

        try:

            with open(
                config_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)


            if isinstance(
                data,
                dict
            ):

                # Admin configuration format:
                # {
                #     "fields": {
                #         ...
                #     }
                # }

                if isinstance(
                    data.get("fields"),
                    dict
                ):

                    config = data.get(
                        "fields",
                        {}
                    )

                else:

                    # Also support a direct field dictionary.
                    config = data


        except Exception as e:

            print(
                "Could not load student details configuration:"
            )

            print(
                f"Configuration file: {config_file}"
            )

            print(e)


    # --------------------------------------------------------
    # Merge the Admin configuration with defaults.
    #
    # IMPORTANT:
    # Do NOT force old student-side fields such as
    # mobile_number/class/section/roll_number.
    #
    # The Admin Control Panel is now the source of truth.
    # --------------------------------------------------------

    final_config = {}

    if isinstance(
        config,
        dict
    ):

        for field_name, field_data in config.items():

            if not isinstance(
                field_data,
                dict
            ):
                continue

            default_data = (
                DEFAULT_STUDENT_DETAILS_CONFIG.get(
                    field_name,
                    {
                        "label": field_name,
                        "enabled": True,
                        "required": False,
                        "type": "text"
                    }
                )
            )

            merged_data = default_data.copy()

            merged_data.update(
                field_data
            )

            final_config[field_name] = (
                merged_data
            )


    # --------------------------------------------------------
    # If the Admin file is missing or empty, use defaults.
    # --------------------------------------------------------

    if not final_config:

        final_config = json.loads(
            json.dumps(
                DEFAULT_STUDENT_DETAILS_CONFIG
            )
        )


    # --------------------------------------------------------
    # Student ID is supplied by Student Login.
    # Keep it available for compatibility.
    # --------------------------------------------------------

    if "student_id" not in final_config:

        final_config["student_id"] = (
            DEFAULT_STUDENT_DETAILS_CONFIG[
                "student_id"
            ].copy()
        )


    return final_config


os.makedirs(
    BACKEND_DIR,
    exist_ok=True
)


os.makedirs(
    STUDENT_ANSWERS_DIR,
    exist_ok=True
)


# ============================================================
# RESULT SETTINGS
# ============================================================

# Overall percentage required to PASS.
# This can later be changed from the Admin page.
PASS_PERCENTAGE = 50.0


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
# SAFE FILE/FOLDER NAME
# ============================================================

def safe_filename(name):

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


    name = name.strip(
        " ._"
    )


    if not name:

        name = "Student"


    return name


# ============================================================
# LOAD QUESTIONS
# ============================================================

def load_questions():

    if not os.path.exists(
        QUESTIONS_FILE
    ):

        return []


    try:

        with open(
            QUESTIONS_FILE,
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

            questions = data.get(
                "questions",
                []
            )

        else:

            questions = data


        if isinstance(
            questions,
            list
        ):

            return questions


    except Exception as e:

        print(
            "Could not load questions.json:"
        )

        print(e)


    return []


# ============================================================
# LOAD JSON
# ============================================================

def load_json(path):

    if not os.path.exists(
        path
    ):

        return None


    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except Exception as e:

        print(
            "Could not load JSON:"
        )

        print(path)

        print(e)

        return None


# ============================================================
# FIND STUDENT ATTEMPTS
# ============================================================

def find_student_attempts(student_id):

    attempts = []


    if not os.path.exists(
        STUDENT_ANSWERS_DIR
    ):

        return attempts


    student_id = str(
        student_id
    ).strip()


    # --------------------------------------------------------
    # First try exact Student ID folder
    # --------------------------------------------------------

    possible_folders = []


    exact_folder = os.path.join(
        STUDENT_ANSWERS_DIR,
        student_id
    )


    if os.path.isdir(
        exact_folder
    ):

        possible_folders.append(
            exact_folder
        )


    # --------------------------------------------------------
    # Also search all folders.
    # This keeps compatibility with existing attempts.
    # --------------------------------------------------------

    try:

        for folder_name in os.listdir(
            STUDENT_ANSWERS_DIR
        ):

            folder_path = os.path.join(
                STUDENT_ANSWERS_DIR,
                folder_name
            )


            if not os.path.isdir(
                folder_path
            ):

                continue


            if folder_path not in possible_folders:

                possible_folders.append(
                    folder_path
                )

    except Exception:

        pass


    # --------------------------------------------------------
    # Search attempts
    # --------------------------------------------------------

    for student_folder in possible_folders:

        try:

            folder_items = os.listdir(
                student_folder
            )

        except Exception:

            continue


        for item in folder_items:

            attempt_path = os.path.join(
                student_folder,
                item
            )


            if not os.path.isdir(
                attempt_path
            ):

                continue


            result_file = os.path.join(
                attempt_path,
                "exam_result.json"
            )


            if not os.path.exists(
                result_file
            ):

                continue


            result_data = load_json(
                result_file
            )


            if not isinstance(
                result_data,
                dict
            ):

                continue


            # ------------------------------------------------
            # Verify student ID when possible
            # ------------------------------------------------

            result_student = result_data.get(
                "student",
                {}
            )


            if isinstance(
                result_student,
                dict
            ):

                result_student_id = str(
                    result_student.get(
                        "student_id",
                        ""
                    )
                ).strip()


                # If result contains a student ID,
                # only show matching student's results.
                if (
                    result_student_id
                    and result_student_id != student_id
                ):

                    continue


            attempts.append(
                {
                    "folder": attempt_path,
                    "folder_name": item,
                    "data": result_data
                }
            )


    # --------------------------------------------------------
    # Sort by attempt number
    # --------------------------------------------------------

    attempts.sort(
        key=lambda x: int(
            x["data"].get(
                "attempt_number",
                0
            )
        )
        if str(
            x["data"].get(
                "attempt_number",
                ""
            )
        ).isdigit()
        else 0
    )


    return attempts


# ============================================================
# CALCULATE SEMANTIC SIMILARITY
# ============================================================

def calculate_similarity(
    expected_answer,
    student_answer
):

    expected_answer = str(
        expected_answer or ""
    ).strip()


    student_answer = str(
        student_answer or ""
    ).strip()


    if not expected_answer:

        return 0.0


    if not student_answer:

        return 0.0


    # --------------------------------------------------------
    # Exact same answer
    # --------------------------------------------------------

    if (
        expected_answer.lower()
        ==
        student_answer.lower()
    ):

        return 100.0


    # --------------------------------------------------------
    # Try Sentence Transformers
    # --------------------------------------------------------

    try:

        from sentence_transformers import (
            SentenceTransformer
        )

        import numpy as np


        # ----------------------------------------------------
        # Cache model
        # ----------------------------------------------------

        if not hasattr(
            calculate_similarity,
            "model"
        ):

            print(
                "Loading semantic similarity model..."
            )


            calculate_similarity.model = (
                SentenceTransformer(
                    "all-MiniLM-L6-v2"
                )
            )


        model = (
            calculate_similarity.model
        )


        embeddings = model.encode(
            [
                expected_answer,
                student_answer
            ],
            normalize_embeddings=True
        )


        similarity = float(
            np.dot(
                embeddings[0],
                embeddings[1]
            )
        )


        # Cosine similarity can theoretically
        # produce values below zero.
        similarity = max(
            0.0,
            min(
                1.0,
                similarity
            )
        )


        return round(
            similarity * 100,
            2
        )


    except Exception as e:

        print(
            "Semantic similarity error:"
        )

        print(e)


        # ----------------------------------------------------
        # Fallback word similarity
        # ----------------------------------------------------

        return calculate_word_similarity(
            expected_answer,
            student_answer
        )


# ============================================================
# FALLBACK WORD SIMILARITY
# ============================================================

def calculate_word_similarity(
    expected_answer,
    student_answer
):

    expected_words = set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            expected_answer.lower()
        )
    )


    student_words = set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            student_answer.lower()
        )
    )


    if not expected_words:

        return 0.0


    if not student_words:

        return 0.0


    intersection = (
        expected_words
        &
        student_words
    )


    # Jaccard similarity
    union = (
        expected_words
        |
        student_words
    )


    if not union:

        return 0.0


    similarity = (
        len(intersection)
        /
        len(union)
    ) * 100


    return round(
        similarity,
        2
    )


# ============================================================
# CALCULATE MARKS
# ============================================================

def calculate_question_marks(
    similarity,
    allotted_marks
):

    try:

        allotted_marks = float(
            allotted_marks
        )

    except Exception:

        allotted_marks = 0.0


    similarity = float(
        similarity
    )


    # --------------------------------------------------------
    # 1-MARK QUESTION
    #
    # >=75% = 100%
    # <75% = 0
    # --------------------------------------------------------

    if allotted_marks == 1:

        if similarity >= 75:

            return 1.0

        return 0.0


    # --------------------------------------------------------
    # MORE THAN 1 MARK
    #
    # 75-100% = 100%
    # 50-<75% = 50%
    # 35-<50% = 25%
    # <35% = 0%
    # --------------------------------------------------------

    if similarity >= 75:

        return allotted_marks


    if similarity >= 50:

        return allotted_marks * 0.50


    if similarity >= 35:

        return allotted_marks * 0.25


    return 0.0


# ============================================================
# EVALUATION TEXT
# ============================================================

def get_evaluation_text(
    similarity,
    marks_awarded,
    allotted_marks
):

    if allotted_marks == 1:

        if similarity >= 75:

            return "CORRECT"

        return "INCORRECT"


    if similarity >= 75:

        return "CORRECT"


    if similarity >= 50:

        return "PARTIALLY CORRECT"


    if similarity >= 35:

        return "WEAK / PARTIALLY CORRECT"


    return "INCORRECT"


# ============================================================
# FORMAT MARKS
# ============================================================

def format_number(value):

    try:

        value = float(
            value
        )

        if value.is_integer():

            return str(
                int(value)
            )

        return f"{value:.2f}"

    except Exception:

        return "0"


# ============================================================
# STUDENT DETAILS
# ============================================================

class StudentDetails:

    def __init__(
        self,
        root,
        student_id,
        parent_window=None,
        login_window=None
    ):

        self.root = root

        self.student_id = student_id

        # ----------------------------------------------------
        # LOAD ADMIN STUDENT DETAILS CONFIGURATION
        # ----------------------------------------------------

        self.student_details_config = (
            load_student_details_configuration()
        )

        # Widgets are stored here so validation and results
        # continue to work when the admin hides a field.
        self.field_widgets = {}

        # Student Login
        self.parent_window = parent_window

        # Explicit login reference
        self.login_window = (
            login_window
            if login_window is not None
            else parent_window
        )

        # Instructions window
        self.instructions_window = None


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Student Details - AI Oral Exam System"
        )

        self.root.geometry(
            "700x650"
        )

        self.root.minsize(
            700,
            650
        )

        self.root.configure(
            bg="#f4f6f8"
        )

        maximize_window(
            self.root
        )


        # ----------------------------------------------------
        # CREATE GUI
        # ----------------------------------------------------

        self.create_interface()


        # ----------------------------------------------------
        # WINDOW CLOSE
        # ----------------------------------------------------

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.back_to_login
        )


    # ========================================================
    # STUDENT DETAILS CONFIGURATION HELPERS
    # ========================================================

    def get_field_config(
        self,
        field_name
    ):

        return self.student_details_config.get(
            field_name,
            DEFAULT_STUDENT_DETAILS_CONFIG.get(
                field_name,
                {
                    "label": field_name,
                    "enabled": True,
                    "required": False
                }
            )
        )


    def is_field_enabled(
        self,
        field_name
    ):

        config = self.get_field_config(
            field_name
        )

        return bool(
            config.get(
                "enabled",
                True
            )
        )


    def is_field_required(
        self,
        field_name
    ):

        config = self.get_field_config(
            field_name
        )

        return bool(
            config.get(
                "required",
                False
            )
        )


    def get_field_label(
        self,
        field_name
    ):

        config = self.get_field_config(
            field_name
        )

        return config.get(
            "label",
            field_name
        )


    def get_field_value(
        self,
        field_name
    ):

        widget = self.field_widgets.get(
            field_name
        )

        if widget is None:
            return ""

        try:
            return widget.get().strip()
        except Exception:
            return ""


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

        title = tk.Label(
            main_frame,
            text="STUDENT DETAILS",
            font=("Arial", 24, "bold"),
            bg="#f4f6f8",
            fg="#1f2937"
        )

        title.pack(
            pady=(30, 5)
        )


        subtitle = tk.Label(
            main_frame,
            text="Enter your details before starting the exam",
            font=("Arial", 11),
            bg="#f4f6f8",
            fg="#6b7280"
        )

        subtitle.pack(
            pady=(0, 20)
        )


        # ====================================================
        # FORM
        # ====================================================

        form_frame = tk.Frame(
            main_frame,
            bg="white",
            padx=35,
            pady=20
        )

        form_frame.pack(
            padx=70,
            fill="x"
        )


        # ====================================================
        # STUDENT ID
        # ====================================================

        tk.Label(
            form_frame,
            text="Student ID",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=7
        )


        self.student_id_entry = ttk.Entry(
            form_frame,
            width=40
        )

        self.student_id_entry.grid(
            row=0,
            column=1,
            padx=20,
            pady=7
        )


        self.student_id_entry.insert(
            0,
            self.student_id
        )


        self.student_id_entry.config(
            state="readonly"
        )


        # ====================================================
        # CONFIGURED STUDENT FIELDS
        # ====================================================
        #
        # The Admin Control Panel is the source of truth.
        # Every enabled field from student_details_config.json
        # is created here automatically.
        #
        # This means Admin can enable/disable fields without
        # modifying details.py again.
        # ====================================================

        current_row = 0

        for field_name, field_config in (
            self.student_details_config.items()
        ):

            if not self.is_field_enabled(
                field_name
            ):
                continue


            # ------------------------------------------------
            # FIELD LABEL
            # ------------------------------------------------

            tk.Label(
                form_frame,
                text=self.get_field_label(
                    field_name
                ),
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#374151"
            ).grid(
                row=current_row,
                column=0,
                sticky="w",
                pady=7
            )


            field_type = str(
                field_config.get(
                    "type",
                    "text"
                )
            ).lower().strip()


            # ------------------------------------------------
            # STUDENT ID
            #
            # Student ID comes from Student Login and must not
            # be manually edited on this page.
            # ------------------------------------------------

            if field_name == "student_id":

                widget = ttk.Entry(
                    form_frame,
                    width=40
                )

                widget.grid(
                    row=current_row,
                    column=1,
                    padx=20,
                    pady=7
                )

                widget.insert(
                    0,
                    self.student_id
                )

                widget.config(
                    state="readonly"
                )


            # ------------------------------------------------
            # CHOICE FIELD
            # ------------------------------------------------

            elif field_type == "choice":

                widget = ttk.Combobox(
                    form_frame,
                    width=37,
                    state="readonly"
                )

                # Gender is currently the Admin-configured
                # choice field. Keep this flexible for future
                # choice fields as well.
                choices = field_config.get(
                    "options",
                    field_config.get(
                        "choices",
                        []
                    )
                )

                if not isinstance(
                    choices,
                    list
                ) or not choices:

                    if field_name == "gender":

                        choices = [
                            "Male",
                            "Female",
                            "Other"
                        ]

                    else:

                        choices = [
                            "Male",
                            "Female",
                            "Other"
                        ]

                widget["values"] = [
                    str(value)
                    for value in choices
                ]

                widget.grid(
                    row=current_row,
                    column=1,
                    padx=20,
                    pady=7
                )


            # ------------------------------------------------
            # ALL OTHER FIELD TYPES
            # ------------------------------------------------

            else:

                widget = ttk.Entry(
                    form_frame,
                    width=40
                )

                widget.grid(
                    row=current_row,
                    column=1,
                    padx=20,
                    pady=7
                )


            # ------------------------------------------------
            # Store widget using the same field ID used by
            # the Admin configuration.
            # ------------------------------------------------

            self.field_widgets[
                field_name
            ] = widget


            current_row += 1


        # ====================================================
        # BUTTON FRAME
        # ====================================================

        button_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            pady=25
        )


        # ====================================================
        # START EXAM
        # ====================================================

        start_button = tk.Button(
            button_frame,
            text="START EXAM",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.start_exam
        )

        start_button.grid(
            row=0,
            column=0,
            padx=8
        )


        # ====================================================
        # VIEW RESULTS
        # ====================================================

        results_button = tk.Button(
            button_frame,
            text="VIEW RESULTS",
            font=("Arial", 12, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.view_results
        )

        results_button.grid(
            row=0,
            column=1,
            padx=8
        )


        # ====================================================
        # BACK
        # ====================================================

        back_button = tk.Button(
            main_frame,
            text="BACK TO LOGIN",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back_to_login
        )

        back_button.pack(
            pady=(0, 20)
        )


    # ========================================================
    # VALIDATE
    # ========================================================

    def validate_details(self):

        student_data = {
            "student_id": self.student_id
        }


        # ----------------------------------------------------
        # Read every field currently enabled by Admin.
        # ----------------------------------------------------

        for field_name, field_config in (
            self.student_details_config.items()
        ):

            # Student ID is already supplied by Login.
            if field_name == "student_id":

                student_data[
                    "student_id"
                ] = self.student_id

                continue


            if not self.is_field_enabled(
                field_name
            ):

                # Keep compatibility with the old code/result
                # structure by storing an empty value.
                student_data[
                    field_name
                ] = ""

                continue


            value = self.get_field_value(
                field_name
            )


            # ------------------------------------------------
            # Required validation
            # ------------------------------------------------

            if (
                self.is_field_required(
                    field_name
                )
                and not value
            ):

                messagebox.showwarning(
                    "Missing Information",
                    (
                        f"Please enter "
                        f"{self.get_field_label(field_name)}."
                    ),
                    parent=self.root
                )


                widget = self.field_widgets.get(
                    field_name
                )

                if widget is not None:

                    try:

                        widget.focus_set()

                    except Exception:

                        pass


                return None


            # ------------------------------------------------
            # Basic number validation
            # ------------------------------------------------

            field_type = str(
                field_config.get(
                    "type",
                    "text"
                )
            ).lower().strip()


            if value and field_type == "number":

                try:

                    number_value = float(
                        value
                    )

                    if (
                        number_value < 0
                    ):

                        raise ValueError

                except Exception:

                    messagebox.showwarning(
                        "Invalid Information",
                        (
                            f"{self.get_field_label(field_name)} "
                            "must contain a valid number."
                        ),
                        parent=self.root
                    )


                    widget = self.field_widgets.get(
                        field_name
                    )

                    if widget is not None:

                        try:

                            widget.focus_set()

                        except Exception:

                            pass


                    return None


            # ------------------------------------------------
            # Basic email validation
            # ------------------------------------------------

            if value and field_type == "email":

                if not re.match(
                    r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                    value
                ):

                    messagebox.showwarning(
                        "Invalid Email",
                        (
                            f"Please enter a valid "
                            f"{self.get_field_label(field_name)}."
                        ),
                        parent=self.root
                    )


                    widget = self.field_widgets.get(
                        field_name
                    )

                    if widget is not None:

                        try:

                            widget.focus_set()

                        except Exception:

                            pass


                    return None


            student_data[
                field_name
            ] = value


        # ----------------------------------------------------
        # Compatibility keys.
        #
        # Older parts of the project expect these keys to
        # exist even when Admin has hidden them.
        # ----------------------------------------------------

        compatibility_fields = [
            "student_name",
            "mobile_number",
            "class",
            "section",
            "roll_number",
            "date_of_birth",
            "age",
            "gender",
            "email",
            "phone",
            "course",
            "department"
        ]


        for field_name in compatibility_fields:

            if field_name not in student_data:

                student_data[
                    field_name
                ] = ""


        return student_data


    # ========================================================
    # SAVE DETAILS
    # ========================================================

    def save_student_details(self):

        student_data = (
            self.validate_details()
        )


        if student_data is None:

            return None


        try:

            with open(
                STUDENT_DATA_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    student_data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )


            return student_data


        except Exception as e:

            messagebox.showerror(
                "Save Error",
                (
                    "Could not save student details.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return None


    # ========================================================
    # START EXAM
    # ========================================================

    def start_exam(self):

        student_data = (
            self.save_student_details()
        )


        if student_data is None:

            return


        try:

            from gui.student.instructions import (
                ExamInstructions
            )


        except Exception as e:

            messagebox.showerror(
                "Import Error",
                (
                    "Could not load Exam Instructions.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # Hide Details
        # ----------------------------------------------------

        self.root.withdraw()


        # ----------------------------------------------------
        # Create ONE Instructions window
        # ----------------------------------------------------

        try:

            self.instructions_window = tk.Toplevel(
                self.root
            )


            self.instructions_window.title(
                "Exam Instructions - AI Oral Exam System"
            )


            self.instructions_window.geometry(
                "1000x750"
            )


            self.instructions_window.minsize(
                850,
                650
            )


            maximize_window(
                self.instructions_window
            )


            ExamInstructions(
                self.instructions_window,
                parent_window=self.root,
                login_window=self.login_window,
                details_window=self.root
            )


        except Exception as e:

            try:

                self.instructions_window.destroy()

            except Exception:

                pass


            self.instructions_window = None


            self.root.deiconify()


            messagebox.showerror(
                "Instructions Error",
                (
                    "Could not open Exam Instructions.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )


    # ========================================================
    # VIEW RESULTS
    # ========================================================

    def view_results(self):

        # ----------------------------------------------------
        # Make sure latest student details are available
        # ----------------------------------------------------

        student_data = load_json(
            STUDENT_DATA_FILE
        )


        if not isinstance(
            student_data,
            dict
        ):

            student_data = {

                "student_id": self.student_id,

                "student_name":
                    self.get_field_value(
                        "student_name"
                    ),

                "mobile_number":
                    self.get_field_value(
                        "mobile_number"
                    ),

                "class":
                    self.get_field_value(
                        "class"
                    ),

                "section":
                    self.get_field_value(
                        "section"
                    ),

                "roll_number":
                    self.get_field_value(
                        "roll_number"
                    ),

                "date_of_birth":
                    self.get_field_value(
                        "date_of_birth"
                    ),

                "age":
                    self.get_field_value(
                        "age"
                    )
            }


        attempts = find_student_attempts(
            self.student_id
        )


        if not attempts:

            messagebox.showinfo(
                "No Results",
                (
                    "No completed examination results "
                    "were found for this student."
                ),
                parent=self.root
            )

            return


        self.open_results_window(
            student_data,
            attempts
        )


    # ========================================================
    # OPEN RESULTS WINDOW
    # ========================================================

    def open_results_window(
        self,
        student_data,
        attempts
    ):

        result_window = tk.Toplevel(
            self.root
        )


        result_window.title(
            "Student Results - AI Oral Exam System"
        )


        result_window.geometry(
            "1100x750"
        )


        result_window.minsize(
            900,
            650
        )


        result_window.configure(
            bg="#f4f6f8"
        )


        maximize_window(
            result_window
        )


        # ====================================================
        # HEADER
        # ====================================================

        header = tk.Frame(
            result_window,
            bg="#1f2937",
            height=100
        )


        header.pack(
            fill="x"
        )


        header.pack_propagate(
            False
        )


        tk.Label(
            header,
            text="EXAM RESULTS",
            font=("Arial", 22, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            side="left",
            padx=30
        )


        student_name = student_data.get(
            "student_name",
            "Student"
        )


        tk.Label(
            header,
            text=f"Student: {student_name}",
            font=("Arial", 11, "bold"),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack(
            side="left",
            padx=20
        )


        # ====================================================
        # ATTEMPT SELECTION
        # ====================================================

        selection_frame = tk.Frame(
            result_window,
            bg="#f4f6f8"
        )


        selection_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )


        tk.Label(
            selection_frame,
            text="Select Attempt:",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#374151"
        ).pack(
            side="left"
        )


        attempt_values = []


        for attempt in attempts:

            data = attempt["data"]


            attempt_number = data.get(
                "attempt_number",
                "?"
            )


            submitted_at = data.get(
                "submitted_at",
                ""
            )


            if submitted_at:

                try:

                    submitted_dt = datetime.fromisoformat(
                        submitted_at
                    )


                    submitted_text = (
                        submitted_dt.strftime(
                            "%d-%m-%Y %I:%M %p"
                        )
                    )

                except Exception:

                    submitted_text = str(
                        submitted_at
                    )

            else:

                submitted_text = "Date not available"


            display_text = (
                f"Attempt {attempt_number} "
                f"- {submitted_text}"
            )


            attempt_values.append(
                display_text
            )


        attempt_combo = ttk.Combobox(
            selection_frame,
            values=attempt_values,
            state="readonly",
            width=45
        )


        attempt_combo.pack(
            side="left",
            padx=15
        )


        attempt_combo.current(
            len(attempt_values) - 1
        )


        # ====================================================
        # CONTENT AREA
        # ====================================================

        content_frame = tk.Frame(
            result_window,
            bg="#f4f6f8"
        )


        content_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )


        # ====================================================
        # SCROLLABLE CANVAS
        # ====================================================

        canvas = tk.Canvas(
            content_frame,
            bg="#f4f6f8",
            highlightthickness=0
        )


        scrollbar = ttk.Scrollbar(
            content_frame,
            orient="vertical",
            command=canvas.yview
        )


        scroll_frame = tk.Frame(
            canvas,
            bg="#f4f6f8"
        )


        scroll_window = canvas.create_window(
            (0, 0),
            window=scroll_frame,
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


        def update_scroll_region(event=None):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )


        scroll_frame.bind(
            "<Configure>",
            update_scroll_region
        )


        def resize_scroll_frame(event):

            try:

                canvas.itemconfig(
                    scroll_window,
                    width=event.width
                )

            except Exception:

                pass


        canvas.bind(
            "<Configure>",
            resize_scroll_frame
        )


        # ====================================================
        # DISPLAY SELECTED RESULT
        # ====================================================

        def display_selected_result(event=None):

            for widget in scroll_frame.winfo_children():

                widget.destroy()


            selected_index = (
                attempt_combo.current()
            )


            if selected_index < 0:

                return


            selected_attempt = attempts[
                selected_index
            ]


            self.render_result(
                scroll_frame,
                selected_attempt,
                student_data,
                result_window
            )


            canvas.yview_moveto(
                0
            )


        attempt_combo.bind(
            "<<ComboboxSelected>>",
            display_selected_result
        )


        # Initial result
        display_selected_result()


        # ====================================================
        # CLOSE BUTTON
        # ====================================================

        close_button = tk.Button(
            result_window,
            text="CLOSE",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=result_window.destroy
        )


        close_button.pack(
            pady=(0, 15)
        )


    # ========================================================
    # RENDER RESULT
    # ========================================================

    def render_result(
        self,
        parent,
        attempt,
        student_data,
        result_window
    ):

        result_data = attempt[
            "data"
        ]


        attempt_folder = attempt[
            "folder"
        ]


        attempt_number = result_data.get(
            "attempt_number",
            "?"
        )


        questions = result_data.get(
            "questions",
            []
        )


        student_answers = result_data.get(
            "student_answers",
            {}
        )


        question_answer_times = (
            result_data.get(
                "question_answer_times",
                {}
            )
        )


        # ----------------------------------------------------
        # If older result doesn't contain questions,
        # load current questions.json.
        # ----------------------------------------------------

        if not questions:

            questions = load_questions()


        # ====================================================
        # ATTEMPT INFORMATION
        # ====================================================

        info_card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid",
            padx=25,
            pady=20
        )


        info_card.pack(
            fill="x",
            pady=(0, 15)
        )


        tk.Label(
            info_card,
            text=f"ATTEMPT {attempt_number}",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#2563eb"
        ).pack(
            anchor="w"
        )


        student_id = student_data.get(
            "student_id",
            ""
        )


        roll_number = student_data.get(
            "roll_number",
            ""
        )


        exam_name = result_data.get(
            "exam_name",
            "AI Oral Examination"
        )


        submitted_at = result_data.get(
            "submitted_at",
            ""
        )


        if submitted_at:

            try:

                submitted_at = (
                    datetime.fromisoformat(
                        submitted_at
                    ).strftime(
                        "%d-%m-%Y %I:%M:%S %p"
                    )
                )

            except Exception:

                pass


        tk.Label(
            info_card,
            text=f"Exam: {exam_name}",
            font=("Arial", 10),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            pady=(8, 2)
        )


        tk.Label(
            info_card,
            text=f"Student ID: {student_id}",
            font=("Arial", 10),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            pady=2
        )


        tk.Label(
            info_card,
            text=f"Roll Number: {roll_number}",
            font=("Arial", 10),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            pady=2
        )


        tk.Label(
            info_card,
            text=f"Submitted: {submitted_at}",
            font=("Arial", 10),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            pady=2
        )


        # ====================================================
        # RESULT CALCULATION
        # ====================================================

        total_allotted = 0.0

        total_secured = 0.0


        question_results = []


        for index, question in enumerate(
            questions
        ):

            # ------------------------------------------------
            # Question number generated automatically
            # ------------------------------------------------

            question_number = index + 1


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


            # ------------------------------------------------
            # student_answers may have integer keys
            # or string keys depending on JSON.
            # ------------------------------------------------

            student_answer = (
                student_answers.get(
                    index,
                    None
                )
            )


            if student_answer is None:

                student_answer = (
                    student_answers.get(
                        str(index),
                        ""
                    )
                )


            if student_answer is None:

                student_answer = ""


            student_answer = str(
                student_answer
            ).strip()


            # ------------------------------------------------
            # Calculate similarity
            # ------------------------------------------------

            similarity = calculate_similarity(
                expected_answer,
                student_answer
            )


            # ------------------------------------------------
            # Calculate marks
            # ------------------------------------------------

            marks_awarded = (
                calculate_question_marks(
                    similarity,
                    allotted_marks
                )
            )


            evaluation = (
                get_evaluation_text(
                    similarity,
                    marks_awarded,
                    float(
                        allotted_marks
                    )
                )
            )


            try:

                allotted_numeric = float(
                    allotted_marks
                )

            except Exception:

                allotted_numeric = 0.0


            total_allotted += (
                allotted_numeric
            )


            total_secured += (
                marks_awarded
            )


            answer_time = (
                question_answer_times.get(
                    str(index),
                    question_answer_times.get(
                        index,
                        0
                    )
                )
            )


            question_results.append(
                {
                    "question_number":
                        question_number,

                    "question":
                        question_text,

                    "expected_answer":
                        expected_answer,

                    "student_answer":
                        student_answer,

                    "similarity":
                        similarity,

                    "evaluation":
                        evaluation,

                    "allotted_marks":
                        allotted_numeric,

                    "marks_awarded":
                        marks_awarded,

                    "answer_time":
                        answer_time
                }
            )


        # ====================================================
        # TOTAL PERCENTAGE
        # ====================================================

        if total_allotted > 0:

            percentage = (
                total_secured
                /
                total_allotted
            ) * 100

        else:

            percentage = 0.0


        percentage = round(
            percentage,
            2
        )


        if percentage >= PASS_PERCENTAGE:

            overall_result = "PASS"

            result_bg = "#dcfce7"

            result_fg = "#166534"

        else:

            overall_result = "FAIL"

            result_bg = "#fee2e2"

            result_fg = "#991b1b"


        # ====================================================
        # QUESTION RESULTS
        # ====================================================

        for result in question_results:

            self.create_question_result_card(
                parent,
                result
            )


        # ====================================================
        # TOTAL RESULT CARD
        # ====================================================

        total_card = tk.Frame(
            parent,
            bg="white",
            bd=2,
            relief="solid",
            padx=30,
            pady=25
        )


        total_card.pack(
            fill="x",
            pady=15
        )


        tk.Label(
            total_card,
            text="FINAL RESULT",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(
            anchor="w",
            pady=(0, 15)
        )


        # ----------------------------------------------------
        # Total questions
        # ----------------------------------------------------

        tk.Label(
            total_card,
            text=(
                f"Total Questions: "
                f"{len(question_results)}"
            ),
            font=("Arial", 12),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            pady=3
        )


        # ----------------------------------------------------
        # Total allotted
        # ----------------------------------------------------

        tk.Label(
            total_card,
            text=(
                f"Total Allotted Marks: "
                f"{format_number(total_allotted)}"
            ),
            font=("Arial", 12),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            pady=3
        )


        # ----------------------------------------------------
        # Secured
        # ----------------------------------------------------

        tk.Label(
            total_card,
            text=(
                f"Marks Secured: "
                f"{format_number(total_secured)}"
            ),
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2563eb"
        ).pack(
            anchor="w",
            pady=3
        )


        # ----------------------------------------------------
        # Percentage
        # ----------------------------------------------------

        tk.Label(
            total_card,
            text=(
                f"Percentage: "
                f"{percentage:.2f}%"
            ),
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#7c3aed"
        ).pack(
            anchor="w",
            pady=5
        )


        # ----------------------------------------------------
        # PASS / FAIL
        # ----------------------------------------------------

        result_label = tk.Label(
            total_card,
            text=(
                f"{overall_result}"
            ),
            font=("Arial", 20, "bold"),
            bg=result_bg,
            fg=result_fg,
            padx=25,
            pady=10
        )


        result_label.pack(
            anchor="w",
            pady=(10, 5)
        )


        tk.Label(
            total_card,
            text=(
                f"Pass Percentage: "
                f"{PASS_PERCENTAGE:.0f}% or above"
            ),
            font=("Arial", 10),
            bg="white",
            fg="#6b7280"
        ).pack(
            anchor="w"
        )


        # ====================================================
        # DOWNLOAD BUTTON
        # ====================================================

        download_button = tk.Button(
            total_card,
            text="DOWNLOAD ANSWER SCRIPT",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=28,
            height=2,
            bd=0,
            cursor="hand2",
            command=lambda: self.download_answer_script(
                student_data,
                result_data,
                question_results,
                total_allotted,
                total_secured,
                percentage,
                overall_result
            )
        )


        download_button.pack(
            anchor="w",
            pady=(20, 5)
        )


    # ========================================================
    # QUESTION RESULT CARD
    # ========================================================

    def create_question_result_card(
        self,
        parent,
        result
    ):

        card = tk.Frame(
            parent,
            bg="white",
            bd=1,
            relief="solid",
            padx=25,
            pady=20
        )


        card.pack(
            fill="x",
            pady=8
        )


        # ====================================================
        # QUESTION HEADER
        # ====================================================

        header_text = (
            f"QUESTION "
            f"{result['question_number']}"
        )


        tk.Label(
            card,
            text=header_text,
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2563eb"
        ).pack(
            anchor="w",
            pady=(0, 12)
        )


        # ====================================================
        # QUESTION
        # ====================================================

        tk.Label(
            card,
            text="Question:",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w"
        )


        tk.Label(
            card,
            text=result["question"],
            font=("Arial", 11),
            bg="white",
            fg="#111827",
            wraplength=900,
            justify="left"
        ).pack(
            anchor="w",
            fill="x",
            pady=(3, 12)
        )


        # ====================================================
        # ORIGINAL ANSWER
        # ====================================================

        tk.Label(
            card,
            text="Original / Expected Answer:",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w"
        )


        expected_answer = (
            result["expected_answer"]
        )


        if not expected_answer:

            expected_answer = (
                "Expected answer not available."
            )


        expected_label = tk.Label(
            card,
            text=expected_answer,
            font=("Arial", 11),
            bg="#f0fdf4",
            fg="#166534",
            wraplength=900,
            justify="left",
            anchor="w",
            padx=12,
            pady=10
        )


        expected_label.pack(
            anchor="w",
            fill="x",
            pady=(3, 12)
        )


        # ====================================================
        # STUDENT ANSWER
        # ====================================================

        tk.Label(
            card,
            text="Student Answer:",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w"
        )


        student_answer = (
            result["student_answer"]
        )


        if not student_answer:

            student_answer = (
                "No answer recorded."
            )


        student_label = tk.Label(
            card,
            text=student_answer,
            font=("Arial", 11),
            bg="#eff6ff",
            fg="#1e3a8a",
            wraplength=900,
            justify="left",
            anchor="w",
            padx=12,
            pady=10
        )


        student_label.pack(
            anchor="w",
            fill="x",
            pady=(3, 12)
        )


        # ====================================================
        # EVALUATION
        # ====================================================

        evaluation = (
            result["evaluation"]
        )


        similarity = (
            result["similarity"]
        )


        if evaluation == "CORRECT":

            evaluation_bg = "#dcfce7"

            evaluation_fg = "#166534"

        elif evaluation == "PARTIALLY CORRECT":

            evaluation_bg = "#fef3c7"

            evaluation_fg = "#92400e"

        elif evaluation == "WEAK / PARTIALLY CORRECT":

            evaluation_bg = "#ffedd5"

            evaluation_fg = "#9a3412"

        else:

            evaluation_bg = "#fee2e2"

            evaluation_fg = "#991b1b"


        evaluation_frame = tk.Frame(
            card,
            bg=evaluation_bg,
            padx=12,
            pady=10
        )


        evaluation_frame.pack(
            fill="x",
            pady=(0, 12)
        )


        tk.Label(
            evaluation_frame,
            text=(
                f"Evaluation: {evaluation}"
            ),
            font=("Arial", 11, "bold"),
            bg=evaluation_bg,
            fg=evaluation_fg
        ).pack(
            anchor="w"
        )


        tk.Label(
            evaluation_frame,
            text=(
                f"Semantic Similarity: "
                f"{similarity:.2f}%"
            ),
            font=("Arial", 11, "bold"),
            bg=evaluation_bg,
            fg=evaluation_fg
        ).pack(
            anchor="w",
            pady=(4, 0)
        )


        # ====================================================
        # MARKS
        # ====================================================

        marks_frame = tk.Frame(
            card,
            bg="white"
        )


        marks_frame.pack(
            fill="x",
            pady=3
        )


        tk.Label(
            marks_frame,
            text=(
                "Allotted Marks: "
                f"{format_number(result['allotted_marks'])}"
            ),
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w"
        )


        tk.Label(
            marks_frame,
            text=(
                "Marks Secured: "
                f"{format_number(result['marks_awarded'])}"
            ),
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#16a34a"
        ).pack(
            anchor="w",
            pady=(4, 0)
        )


        # ====================================================
        # ANSWER TIME
        # ====================================================

        tk.Label(
            card,
            text=(
                "Answer Time: "
                f"{result['answer_time']} seconds"
            ),
            font=("Arial", 10),
            bg="white",
            fg="#6b7280"
        ).pack(
            anchor="w",
            pady=(8, 0)
        )


    # ========================================================
    # DOWNLOAD ANSWER SCRIPT
    # ========================================================

    def download_answer_script(
        self,
        student_data,
        result_data,
        question_results,
        total_allotted,
        total_secured,
        percentage,
        overall_result
    ):

        # ----------------------------------------------------
        # Windows Downloads folder
        # ----------------------------------------------------

        downloads_folder = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )


        try:

            os.makedirs(
                downloads_folder,
                exist_ok=True
            )

        except Exception as e:

            messagebox.showerror(
                "Download Error",
                (
                    "Could not access the Downloads folder.\n\n"
                    f"{e}"
                )
            )

            return


        student_name = safe_filename(
            student_data.get(
                "student_name",
                "Student"
            )
        )


        student_id = safe_filename(
            student_data.get(
                "student_id",
                self.student_id
            )
        )


        attempt_number = result_data.get(
            "attempt_number",
            "Unknown"
        )


        filename = (
            f"{student_name}_"
            f"{student_id}_"
            f"Attempt_{attempt_number}_"
            f"Answer_Script.txt"
        )


        file_path = os.path.join(
            downloads_folder,
            filename
        )


        # ----------------------------------------------------
        # Avoid overwriting an existing answer script
        # ----------------------------------------------------

        if os.path.exists(
            file_path
        ):

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )


            filename = (
                f"{student_name}_"
                f"{student_id}_"
                f"Attempt_{attempt_number}_"
                f"Answer_Script_"
                f"{timestamp}.txt"
            )


            file_path = os.path.join(
                downloads_folder,
                filename
            )


        # ====================================================
        # CREATE ANSWER SCRIPT
        # ====================================================

        lines = []


        lines.append(
            "=" * 70
        )


        lines.append(
            "AI-BASED AUTOMATED ORAL EXAMINATION"
        )


        lines.append(
            "STUDENT ANSWER SCRIPT / RESULT"
        )


        lines.append(
            "=" * 70
        )


        lines.append("")


        lines.append(
            f"Exam Name: "
            f"{result_data.get('exam_name', 'AI Oral Exam')}"
        )


        lines.append(
            f"Student ID: "
            f"{student_data.get('student_id', '')}"
        )


        lines.append(
            f"Student Name: "
            f"{student_data.get('student_name', '')}"
        )


        lines.append(
            f"Mobile Number: "
            f"{student_data.get('mobile_number', '')}"
        )


        lines.append(
            f"Class: "
            f"{student_data.get('class', '')}"
        )


        lines.append(
            f"Section: "
            f"{student_data.get('section', '')}"
        )


        lines.append(
            f"Roll Number: "
            f"{student_data.get('roll_number', '')}"
        )

        if student_data.get(
            "date_of_birth",
            ""
        ):

            lines.append(
                f"Date of Birth: "
                f"{student_data.get('date_of_birth', '')}"
            )

        if student_data.get(
            "age",
            ""
        ):

            lines.append(
                f"Age: "
                f"{student_data.get('age', '')}"
            )


        lines.append(
            f"Attempt Number: "
            f"{result_data.get('attempt_number', '')}"
        )


        lines.append(
            f"Submitted At: "
            f"{result_data.get('submitted_at', '')}"
        )


        lines.append("")


        lines.append(
            "=" * 70
        )


        lines.append(
            "QUESTION-WISE RESULT"
        )


        lines.append(
            "=" * 70
        )


        lines.append("")


        # ====================================================
        # QUESTIONS
        # ====================================================

        for result in question_results:

            lines.append(
                "-" * 70
            )


            lines.append(
                f"QUESTION "
                f"{result['question_number']}"
            )


            lines.append(
                "-" * 70
            )


            lines.append("")


            lines.append(
                "QUESTION:"
            )


            lines.append(
                result["question"]
            )


            lines.append("")


            lines.append(
                "ORIGINAL / EXPECTED ANSWER:"
            )


            lines.append(
                result["expected_answer"]
                if result["expected_answer"]
                else "Not available."
            )


            lines.append("")


            lines.append(
                "STUDENT ANSWER:"
            )


            lines.append(
                result["student_answer"]
                if result["student_answer"]
                else "No answer recorded."
            )


            lines.append("")


            lines.append(
                "EVALUATION:"
            )


            lines.append(
                result["evaluation"]
            )


            lines.append("")


            lines.append(
                "SEMANTIC SIMILARITY:"
            )


            lines.append(
                f"{result['similarity']:.2f}%"
            )


            lines.append("")


            lines.append(
                "ALLOTTED MARKS:"
            )


            lines.append(
                format_number(
                    result["allotted_marks"]
                )
            )


            lines.append("")


            lines.append(
                "MARKS SECURED:"
            )


            lines.append(
                format_number(
                    result["marks_awarded"]
                )
            )


            lines.append("")


            lines.append(
                "ANSWER TIME:"
            )


            lines.append(
                f"{result['answer_time']} seconds"
            )


            lines.append("")


        # ====================================================
        # FINAL RESULT
        # ====================================================

        lines.append(
            "=" * 70
        )


        lines.append(
            "FINAL RESULT"
        )


        lines.append(
            "=" * 70
        )


        lines.append("")


        lines.append(
            f"Total Questions: "
            f"{len(question_results)}"
        )


        lines.append(
            f"Total Allotted Marks: "
            f"{format_number(total_allotted)}"
        )


        lines.append(
            f"Marks Secured: "
            f"{format_number(total_secured)}"
        )


        lines.append(
            f"Percentage: "
            f"{percentage:.2f}%"
        )


        lines.append(
            f"Pass Percentage: "
            f"{PASS_PERCENTAGE:.0f}%"
        )


        lines.append(
            f"RESULT: "
            f"{overall_result}"
        )


        lines.append("")


        lines.append(
            "=" * 70
        )


        lines.append(
            "END OF ANSWER SCRIPT"
        )


        lines.append(
            "=" * 70
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
                    "The answer script has been "
                    "downloaded successfully.\n\n"
                    f"Location:\n{file_path}"
                )
            )


        except Exception as e:

            messagebox.showerror(
                "Download Error",
                (
                    "Could not create the answer script.\n\n"
                    f"{e}"
                )
            )


    # ========================================================
    # RETURN TO LOGIN
    # ========================================================

    def back_to_login(self):

        answer = messagebox.askyesno(
            "Back to Login",
            (
                "Do you want to return to "
                "the Student Login page?"
            ),
            parent=self.root
        )


        if not answer:

            return


        self.close_and_return_to_login()


    # ========================================================
    # CLOSE AND RETURN LOGIN
    # ========================================================

    def close_and_return_to_login(self):

        # ----------------------------------------------------
        # Close Details
        # ----------------------------------------------------

        try:

            self.root.destroy()

        except Exception:

            pass


        # ----------------------------------------------------
        # Restore Login
        # ----------------------------------------------------

        if self.login_window is not None:

            try:

                self.login_window.deiconify()

                maximize_window(
                    self.login_window
                )

                self.login_window.lift()

                self.login_window.focus_force()

            except Exception as e:

                print(
                    "Could not restore Student Login:"
                )

                print(e)


# ============================================================
# OPEN STUDENT DETAILS
# ============================================================

def open_student_details(
    student_id,
    parent_window=None,
    login_window=None
):

    if login_window is None:

        login_window = parent_window


    window = tk.Toplevel(
        parent_window
    )


    maximize_window(
        window
    )


    StudentDetails(
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


    open_student_details(
        "STUDENT001",
        parent_window=root,
        login_window=root
    )


    root.mainloop()
