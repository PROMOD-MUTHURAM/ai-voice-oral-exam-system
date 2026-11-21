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
# DELETE QUESTION
# ============================================================

class DeleteQuestion:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root
        self.parent_window = parent_window
        self.selected_exam_id = None

        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Delete Question - AI Oral Examination System"
        )

        self.root.geometry(
            "1250x800"
        )

        self.root.minsize(
            900,
            600
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
        # PAGE CANVAS
        # ====================================================

        self.page_canvas = tk.Canvas(
            outer_frame,
            bg="#f4f6f8",
            highlightthickness=0
        )

        self.page_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ====================================================
        # PAGE SCROLLBAR
        # ====================================================

        page_scrollbar = ttk.Scrollbar(
            outer_frame,
            orient="vertical",
            command=self.page_canvas.yview
        )

        page_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.page_canvas.configure(
            yscrollcommand=page_scrollbar.set
        )

        # ====================================================
        # PAGE FRAME
        # ====================================================

        self.page_frame = tk.Frame(
            self.page_canvas,
            bg="#f4f6f8"
        )

        self.page_window = self.page_canvas.create_window(
            (0, 0),
            window=self.page_frame,
            anchor="nw"
        )

        # ====================================================
        # SCROLL REGION
        # ====================================================

        self.page_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.page_canvas.bind(
            "<Configure>",
            self.resize_page_frame
        )

        # ====================================================
        # MOUSE WHEEL
        # ====================================================

        self.page_canvas.bind_all(
            "<MouseWheel>",
            self.mouse_wheel
        )

        self.page_canvas.bind_all(
            "<Button-4>",
            self.mouse_wheel_linux_up
        )

        self.page_canvas.bind_all(
            "<Button-5>",
            self.mouse_wheel_linux_down
        )

        # ====================================================
        # BUILD PAGE
        # ====================================================

        self.build_page()

    # ========================================================
    # UPDATE SCROLL REGION
    # ========================================================

    def update_scroll_region(
        self,
        event=None
    ):

        self.page_canvas.configure(
            scrollregion=self.page_canvas.bbox("all")
        )

    # ========================================================
    # RESIZE PAGE
    # ========================================================

    def resize_page_frame(
        self,
        event
    ):

        self.page_canvas.itemconfig(
            self.page_window,
            width=event.width
        )

    # ========================================================
    # MOUSE WHEEL
    # ========================================================

    def mouse_wheel(
        self,
        event
    ):

        try:

            self.page_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        except Exception:
            pass

    # ========================================================
    # LINUX MOUSE WHEEL UP
    # ========================================================

    def mouse_wheel_linux_up(
        self,
        event
    ):

        try:

            self.page_canvas.yview_scroll(
                -3,
                "units"
            )

        except Exception:
            pass

    # ========================================================
    # LINUX MOUSE WHEEL DOWN
    # ========================================================

    def mouse_wheel_linux_down(
        self,
        event
    ):

        try:

            self.page_canvas.yview_scroll(
                3,
                "units"
            )

        except Exception:
            pass

    # ========================================================
    # BUILD PAGE
    # ========================================================

    def build_page(self):

        main_frame = tk.Frame(
            self.page_frame,
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
            text="DELETE QUESTION",
            font=("Arial", 27, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(20, 3)
        )

        tk.Label(
            header_frame,
            text=(
                "Select an examination and delete "
                "a question from that examination"
            ),
            font=("Arial", 11),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack()

        # ====================================================
        # CONTROL FRAME
        # ====================================================

        control_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        control_frame.pack(
            fill="x",
            padx=35,
            pady=(18, 10)
        )

        # ====================================================
        # SELECT EXAM
        # ====================================================

        tk.Label(
            control_frame,
            text="Select Exam:",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#374151"
        ).pack(
            side="left",
            padx=(0, 10)
        )

        self.exam_combo = ttk.Combobox(
            control_frame,
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

        # ====================================================
        # LOAD BUTTON
        # ====================================================

        tk.Button(
            control_frame,
            text="LOAD QUESTIONS",
            font=("Arial", 10, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.load_selected_exam
        ).pack(
            side="left",
            padx=5
        )

        # ====================================================
        # REFRESH
        # ====================================================

        tk.Button(
            control_frame,
            text="REFRESH",
            font=("Arial", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=12,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.refresh_exams
        ).pack(
            side="left",
            padx=5
        )

        # ====================================================
        # QUESTION COUNT
        # ====================================================

        self.question_count_label = tk.Label(
            control_frame,
            text="Questions: 0",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#374151"
        )

        self.question_count_label.pack(
            side="right",
            padx=10
        )

        # ====================================================
        # EXAM INFORMATION
        # ====================================================

        self.exam_info_label = tk.Label(
            main_frame,
            text="No exam selected",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#374151",
            anchor="w"
        )

        self.exam_info_label.pack(
            fill="x",
            padx=40,
            pady=(0, 8)
        )

        # ====================================================
        # TABLE FRAME
        # ====================================================

        table_frame = tk.Frame(
            main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        table_frame.pack(
            fill="x",
            padx=35,
            pady=8
        )

        # ====================================================
        # TREEVIEW STYLE
        # ====================================================

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Treeview",
            rowheight=42,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        # ====================================================
        # TABLE COLUMNS
        # ====================================================

        columns = (
            "exam_id",
            "question_no",
            "question_type",
            "question",
            "marks",
            "difficulty",
            "topic",
            "status"
        )

        self.question_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=12
        )

        # ====================================================
        # HEADINGS
        # ====================================================

        self.question_tree.heading(
            "exam_id",
            text="Exam ID"
        )

        self.question_tree.heading(
            "question_no",
            text="Question No."
        )

        self.question_tree.heading(
            "question_type",
            text="Question Type"
        )

        self.question_tree.heading(
            "question",
            text="Question"
        )

        self.question_tree.heading(
            "marks",
            text="Marks"
        )

        self.question_tree.heading(
            "difficulty",
            text="Difficulty"
        )

        self.question_tree.heading(
            "topic",
            text="Topic"
        )

        self.question_tree.heading(
            "status",
            text="Status"
        )

        # ====================================================
        # COLUMN WIDTHS
        # ====================================================

        self.question_tree.column(
            "exam_id",
            width=110,
            minwidth=90,
            anchor="center"
        )

        self.question_tree.column(
            "question_no",
            width=100,
            minwidth=80,
            anchor="center"
        )

        self.question_tree.column(
            "question_type",
            width=150,
            minwidth=120
        )

        self.question_tree.column(
            "question",
            width=420,
            minwidth=250
        )

        self.question_tree.column(
            "marks",
            width=70,
            minwidth=60,
            anchor="center"
        )

        self.question_tree.column(
            "difficulty",
            width=100,
            minwidth=80,
            anchor="center"
        )

        self.question_tree.column(
            "topic",
            width=140,
            minwidth=100
        )

        self.question_tree.column(
            "status",
            width=90,
            minwidth=80,
            anchor="center"
        )

        # ====================================================
        # TABLE SCROLLBARS
        # ====================================================

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.question_tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.question_tree.xview
        )

        self.question_tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        # ====================================================
        # TABLE GRID
        # ====================================================

        self.question_tree.grid(
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

        table_frame.rowconfigure(
            0,
            weight=1
        )

        table_frame.columnconfigure(
            0,
            weight=1
        )

        # ====================================================
        # SELECTION
        # ====================================================

        self.question_tree.bind(
            "<<TreeviewSelect>>",
            self.question_selected
        )

        # ====================================================
        # PREVIEW FRAME
        # ====================================================

        preview_frame = tk.Frame(
            main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        preview_frame.pack(
            fill="x",
            padx=35,
            pady=(8, 5)
        )

        tk.Label(
            preview_frame,
            text="SELECTED QUESTION",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        self.selected_question_label = tk.Label(
            preview_frame,
            text="No question selected.",
            font=("Arial", 10),
            bg="white",
            fg="#374151",
            justify="left",
            anchor="w",
            wraplength=1100
        )

        self.selected_question_label.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        # ============================================================
        # BUTTON FRAME
        # ============================================================

        button_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            fill="x",
            padx=35,
            pady=(10, 25)
        )


        # ============================================================
        # DELETE BUTTON
        # ============================================================

        self.delete_button = tk.Button(
            button_frame,
            text="DELETE SELECTED QUESTION",
            font=("Arial", 11, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            width=32,
            height=2,
            padx=10,
            pady=5,
            bd=0,
            cursor="hand2",
            state="disabled",
            command=self.delete_question
        )

        self.delete_button.grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )


        # ============================================================
        # BACK BUTTON
        # ============================================================

        back_button = tk.Button(
            button_frame,
            text="BACK TO QUESTION MANAGEMENT",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=32,
            height=2,
            padx=10,
            pady=5,
            bd=0,
            cursor="hand2",
            command=self.back
        )

        back_button.grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )


        # ============================================================
        # BUTTON FRAME CONFIGURATION
        # ============================================================

        button_frame.columnconfigure(
            0,
            weight=0
        )

        button_frame.columnconfigure(
            1,
            weight=0
        )

    # ========================================================
    # LOAD EXAMS
    # ========================================================

    def load_exams(self):

        exam_list = []

        if not os.path.exists(EXAMS_DIR):

            self.exam_combo["values"] = []

            self.clear_questions()

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

                    exam_data = json.load(file)

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

            except Exception as e:

                print(
                    f"Could not load {filename}: {e}"
                )

                continue

        exam_list.sort(
            key=lambda value: value.lower()
        )

        self.exam_combo["values"] = exam_list

        if exam_list:

            old_exam_id = self.selected_exam_id

            selected_index = 0

            if old_exam_id:

                for index, display_name in enumerate(
                    exam_list
                ):

                    exam_id = self.extract_exam_id(
                        display_name
                    )

                    if exam_id == old_exam_id:

                        selected_index = index
                        break

            self.exam_combo.current(
                selected_index
            )

            self.load_selected_exam()

        else:

            self.selected_exam_id = None

            self.clear_questions()

            self.exam_info_label.config(
                text="No examinations available."
            )

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh_exams(self):
        self.load_exams()

    # ========================================================
    # EXTRACT EXAM ID
    # ========================================================

    def extract_exam_id(
        self,
        display_name
    ):

        display_name = str(
            display_name
        ).strip()

        if not display_name:
            return None

        if " - " in display_name:

            return display_name.split(
                " - ",
                1
            )[0].strip()

        return display_name

    # ========================================================
    # GET SELECTED EXAM ID
    # ========================================================

    def get_selected_exam_id(self):

        selected = self.exam_combo.get().strip()

        if not selected:
            return None

        return self.extract_exam_id(
            selected
        )

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

            self.selected_exam_id = None

            self.clear_questions()

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
                    "The corresponding exam JSON file "
                    "could not be found."
                ),
                parent=self.root
            )

            self.clear_questions()

            return

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                exam_data = json.load(file)

        except Exception as e:

            messagebox.showerror(
                "Read Error",
                (
                    "Could not read the selected exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            self.clear_questions()

            return

        if not isinstance(
            exam_data,
            dict
        ):

            messagebox.showerror(
                "Invalid Exam",
                (
                    f"The file for exam {exam_id} "
                    "contains invalid data."
                ),
                parent=self.root
            )

            self.clear_questions()

            return

        self.selected_exam_id = exam_id

        questions = exam_data.get(
            "questions",
            []
        )

        if not isinstance(
            questions,
            list
        ):

            questions = []

        exam_name = str(
            exam_data.get(
                "exam_name",
                ""
            )
        ).strip()

        if exam_name:

            self.exam_info_label.config(
                text=(
                    f"Selected Exam ID: {exam_id}"
                    f"    |    "
                    f"Exam Name: {exam_name}"
                )
            )

        else:

            self.exam_info_label.config(
                text=(
                    f"Selected Exam ID: {exam_id}"
                )
            )

        self.display_questions(
            exam_id,
            questions
        )

    # ========================================================
    # DISPLAY QUESTIONS
    # ========================================================

    def display_questions(
        self,
        exam_id,
        questions
    ):

        for item in self.question_tree.get_children():

            self.question_tree.delete(
                item
            )

        self.clear_selected_question()

        def question_sort_key(
            question
        ):

            if not isinstance(
                question,
                dict
            ):

                return 0

            try:

                return int(
                    question.get(
                        "question_no",
                        0
                    )
                )

            except Exception:

                return 0

        valid_questions = []

        for question in questions:

            if isinstance(
                question,
                dict
            ):

                valid_questions.append(
                    question
                )

        valid_questions.sort(
            key=question_sort_key
        )

        for question in valid_questions:

            question_no = question.get(
                "question_no",
                ""
            )

            question_type = question.get(
                "question_type",
                ""
            )

            question_text = question.get(
                "question",
                ""
            )

            marks = question.get(
                "marks",
                ""
            )

            difficulty = question.get(
                "difficulty",
                ""
            )

            topic = question.get(
                "topic",
                ""
            )

            status = question.get(
                "status",
                "Active"
            )

            self.question_tree.insert(
                "",
                "end",
                values=(
                    exam_id,
                    question_no,
                    question_type,
                    question_text,
                    marks,
                    difficulty,
                    topic,
                    status
                )
            )

        count = len(
            self.question_tree.get_children()
        )

        self.question_count_label.config(
            text=f"Questions: {count}"
        )

        if count == 0:

            self.selected_question_label.config(
                text=(
                    "This exam does not contain "
                    "any questions."
                )
            )

    # ========================================================
    # QUESTION SELECTED
    # ========================================================

    def question_selected(
        self,
        event=None
    ):

        selected_items = (
            self.question_tree.selection()
        )

        if not selected_items:

            self.clear_selected_question()

            return

        selected_item = selected_items[0]

        values = self.question_tree.item(
            selected_item,
            "values"
        )

        if not values:

            self.clear_selected_question()

            return

        exam_id = values[0]
        question_no = values[1]
        question_type = values[2]
        question_text = values[3]
        marks = values[4]
        difficulty = values[5]
        topic = values[6]
        status = values[7]

        if (
            self.selected_exam_id
            and
            exam_id != self.selected_exam_id
        ):

            self.clear_selected_question()

            return

        self.delete_button.config(
            state="normal"
        )

        difficulty_text = (
            difficulty
            if difficulty
            else "Not specified"
        )

        topic_text = (
            topic
            if topic
            else "Not specified"
        )

        status_text = (
            status
            if status
            else "Active"
        )

        self.selected_question_label.config(
            text=(
                f"Exam ID: {exam_id}\n"
                f"Question No.: {question_no}\n"
                f"Question Type: {question_type}\n"
                f"Marks: {marks}\n"
                f"Difficulty: {difficulty_text}\n"
                f"Topic: {topic_text}\n"
                f"Status: {status_text}\n\n"
                f"Question:\n{question_text}"
            )
        )

    # ========================================================
    # CLEAR SELECTED QUESTION
    # ========================================================

    def clear_selected_question(self):

        self.delete_button.config(
            state="disabled"
        )

        self.selected_question_label.config(
            text="No question selected."
        )

    # ========================================================
    # CLEAR QUESTIONS
    # ========================================================

    def clear_questions(self):

        for item in self.question_tree.get_children():

            self.question_tree.delete(
                item
            )

        self.question_count_label.config(
            text="Questions: 0"
        )

        self.clear_selected_question()

        self.exam_info_label.config(
            text="No exam selected"
        )

    # ========================================================
    # DELETE QUESTION
    # ========================================================

    def delete_question(self):

        selected_items = (
            self.question_tree.selection()
        )

        if not selected_items:

            messagebox.showwarning(
                "No Question Selected",
                (
                    "Please select a question "
                    "from the table first."
                ),
                parent=self.root
            )

            return

        exam_id = self.selected_exam_id

        if not exam_id:

            messagebox.showwarning(
                "No Exam Selected",
                "Please select an exam first.",
                parent=self.root
            )

            return

        selected_item = selected_items[0]

        values = self.question_tree.item(
            selected_item,
            "values"
        )

        if not values:
            return

        row_exam_id = str(
            values[0]
        ).strip()

        question_no = values[1]
        question_text = values[3]

        if row_exam_id != exam_id:

            messagebox.showerror(
                "Exam Mismatch",
                (
                    "The selected question does not "
                    "belong to the selected exam.\n\n"
                    f"Selected Exam: {exam_id}\n"
                    f"Question Exam: {row_exam_id}"
                ),
                parent=self.root
            )

            return

        confirmation = messagebox.askyesno(
            "Confirm Delete",
            (
                "Are you sure you want to delete "
                "this question?\n\n"
                f"Exam ID: {exam_id}\n"
                f"Question No.: {question_no}\n\n"
                f"Question:\n"
                f"{question_text}\n\n"
                "This action cannot be undone."
            ),
            parent=self.root
        )

        if not confirmation:
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
                    "The exam file could not be found."
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

                exam_data = json.load(file)

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

        questions = exam_data.get(
            "questions",
            []
        )

        if not isinstance(
            questions,
            list
        ):

            messagebox.showerror(
                "Invalid Questions",
                (
                    "The selected exam does not "
                    "contain a valid questions list."
                ),
                parent=self.root
            )

            return

        new_questions = []
        deleted = False

        for question in questions:

            if not isinstance(
                question,
                dict
            ):

                new_questions.append(
                    question
                )

                continue

            existing_number = question.get(
                "question_no"
            )

            try:

                same_question = (
                    int(existing_number)
                    ==
                    int(question_no)
                )

            except Exception:

                same_question = (
                    str(existing_number).strip()
                    ==
                    str(question_no).strip()
                )

            if (
                same_question
                and
                not deleted
            ):

                deleted = True
                continue

            new_questions.append(
                question
            )

        if not deleted:

            messagebox.showwarning(
                "Question Not Found",
                (
                    f"Question No. {question_no} "
                    f"was not found in exam {exam_id}."
                ),
                parent=self.root
            )

            self.load_selected_exam()

            return

        exam_data["questions"] = new_questions

        exam_data["total_questions"] = len(
            new_questions
        )

        total_marks = 0

        for question in new_questions:

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

        exam_data["total_marks"] = total_marks

        exam_data["updated_at"] = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

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
                "Delete Error",
                (
                    "Could not save the updated exam.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return

        messagebox.showinfo(
            "Question Deleted",
            (
                "Question deleted successfully.\n\n"
                f"Exam ID: {exam_id}\n"
                f"Question No.: {question_no}\n\n"
                f"Remaining Questions: "
                f"{len(new_questions)}"
            ),
            parent=self.root
        )

        self.load_selected_exam()

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
# OPEN DELETE QUESTION
# ============================================================

def open_delete_question(
    parent_window=None
):

    window = tk.Toplevel(
        parent_window
    )

    DeleteQuestion(
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

    open_delete_question(
        parent_window=root
    )

    root.mainloop()
