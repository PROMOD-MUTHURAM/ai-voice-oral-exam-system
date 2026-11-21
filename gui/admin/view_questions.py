import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys


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
# VIEW QUESTIONS
# ============================================================

class ViewQuestions:

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
            "View Questions - AI Oral Examination System"
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


        # ----------------------------------------------------
        # MAXIMIZE
        # ----------------------------------------------------

        maximize_window(
            self.root
        )


        # ----------------------------------------------------
        # WINDOW CLOSE
        # ----------------------------------------------------

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
        # WHOLE PAGE CANVAS
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
        # WHOLE PAGE VERTICAL SCROLLBAR
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
        # UPDATE SCROLL REGION
        # ====================================================

        self.page_frame.bind(
            "<Configure>",
            self.update_page_scrollregion
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


        # Linux mouse wheel
        self.page_canvas.bind_all(
            "<Button-4>",
            self.mouse_wheel_linux_up
        )

        self.page_canvas.bind_all(
            "<Button-5>",
            self.mouse_wheel_linux_down
        )


        # ====================================================
        # BUILD PAGE CONTENT
        # ====================================================

        self.build_page_content()


    # ========================================================
    # UPDATE PAGE SCROLL REGION
    # ========================================================

    def update_page_scrollregion(
        self,
        event=None
    ):

        self.page_canvas.configure(
            scrollregion=self.page_canvas.bbox("all")
        )


    # ========================================================
    # RESIZE PAGE FRAME
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

        self.page_canvas.yview_scroll(
            -3,
            "units"
        )


    # ========================================================
    # LINUX MOUSE WHEEL DOWN
    # ========================================================

    def mouse_wheel_linux_down(
        self,
        event
    ):

        self.page_canvas.yview_scroll(
            3,
            "units"
        )


    # ========================================================
    # BUILD PAGE CONTENT
    # ========================================================

    def build_page_content(self):

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
            text="VIEW QUESTIONS",
            font=("Arial", 27, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(18, 3)
        )


        tk.Label(
            header_frame,
            text=(
                "View questions stored in an examination"
            ),
            font=("Arial", 11),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack()


        # ====================================================
        # EXAM SELECTION
        # ====================================================

        control_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        control_frame.pack(
            fill="x",
            padx=45,
            pady=(18, 8)
        )


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
        # VIEW BUTTON
        # ====================================================

        tk.Button(
            control_frame,
            text="VIEW QUESTIONS",
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
            padx=8
        )


        # ====================================================
        # REFRESH BUTTON
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
            command=self.load_exams
        ).pack(
            side="left",
            padx=8
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
        # TABLE FRAME
        # ====================================================

        table_frame = tk.Frame(
            main_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=45,
            pady=8
        )


        # ====================================================
        # TREEVIEW STYLE
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
            rowheight=45,
            font=("Arial", 10)
        )


        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )


        # ====================================================
        # COLUMNS
        # ====================================================

        columns = (
            "question_no",
            "type",
            "question",
            "answer",
            "marks",
            "difficulty",
            "topic",
            "keywords",
            "status"
        )


        self.question_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )


        # ====================================================
        # HEADINGS
        # ====================================================

        self.question_tree.heading(
            "question_no",
            text="No."
        )

        self.question_tree.heading(
            "type",
            text="Question Type"
        )

        self.question_tree.heading(
            "question",
            text="Question"
        )

        self.question_tree.heading(
            "answer",
            text="Expected Answer"
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
            "keywords",
            text="Keywords"
        )

        self.question_tree.heading(
            "status",
            text="Status"
        )


        # ====================================================
        # COLUMN WIDTHS
        # ====================================================

        self.question_tree.column(
            "question_no",
            width=55,
            minwidth=50,
            anchor="center"
        )

        self.question_tree.column(
            "type",
            width=145,
            minwidth=120
        )

        self.question_tree.column(
            "question",
            width=300,
            minwidth=220
        )

        self.question_tree.column(
            "answer",
            width=300,
            minwidth=220
        )

        self.question_tree.column(
            "marks",
            width=65,
            minwidth=55,
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
            width=130,
            minwidth=100
        )

        self.question_tree.column(
            "keywords",
            width=180,
            minwidth=120
        )

        self.question_tree.column(
            "status",
            width=90,
            minwidth=80,
            anchor="center"
        )


        # ====================================================
        # TABLE VERTICAL SCROLLBAR
        # ====================================================

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.question_tree.yview
        )

        self.question_tree.configure(
            yscrollcommand=vertical_scrollbar.set
        )


        # ====================================================
        # TABLE HORIZONTAL SCROLLBAR
        # ====================================================

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.question_tree.xview
        )

        self.question_tree.configure(
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
        # QUESTION SELECTION
        # ====================================================

        self.question_tree.bind(
            "<<TreeviewSelect>>",
            self.question_selected
        )


        # ====================================================
        # DOUBLE CLICK
        # ====================================================

        self.question_tree.bind(
            "<Double-1>",
            self.show_question_details
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
            padx=45,
            pady=(5, 8)
        )


        # ====================================================
        # PREVIEW TITLE
        # ====================================================

        tk.Label(
            preview_frame,
            text="SELECTED QUESTION",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 4)
        )


        # ====================================================
        # QUESTION
        # ====================================================

        tk.Label(
            preview_frame,
            text="Question:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            padx=15
        )


        self.question_preview = tk.Text(
            preview_frame,
            height=4,
            font=("Arial", 10),
            bg="#f9fafb",
            fg="#111827",
            bd=1,
            relief="solid",
            wrap="word"
        )

        self.question_preview.pack(
            fill="x",
            padx=15,
            pady=(3, 7)
        )

        self.question_preview.config(
            state="disabled"
        )


        # ====================================================
        # ANSWER
        # ====================================================

        tk.Label(
            preview_frame,
            text="Expected Answer:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#374151"
        ).pack(
            anchor="w",
            padx=15
        )


        self.answer_preview = tk.Text(
            preview_frame,
            height=6,
            font=("Arial", 10),
            bg="#f9fafb",
            fg="#111827",
            bd=1,
            relief="solid",
            wrap="word"
        )

        self.answer_preview.pack(
            fill="x",
            padx=15,
            pady=(3, 7)
        )

        self.answer_preview.config(
            state="disabled"
        )


        # ====================================================
        # EXTRA INFORMATION
        # ====================================================

        self.extra_info_label = tk.Label(
            preview_frame,
            text="",
            font=("Arial", 10),
            bg="white",
            fg="#6b7280",
            anchor="w",
            justify="left",
            wraplength=1050
        )

        self.extra_info_label.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )


        # ====================================================
        # INFORMATION
        # ====================================================

        self.info_label = tk.Label(
            main_frame,
            text=(
                "Select a question to see the complete "
                "question and expected answer."
            ),
            font=("Arial", 10),
            bg="#f4f6f8",
            fg="#6b7280"
        )

        self.info_label.pack(
            pady=(0, 5)
        )


        # ====================================================
        # BACK BUTTON
        # ====================================================

        tk.Button(
            main_frame,
            text="BACK TO QUESTION MANAGEMENT",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=30,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        ).pack(
            pady=(0, 20)
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

                    display_name = (
                        f"{exam_id} - {exam_name}"
                    )

                    exam_list.append(
                        display_name
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

            self.clear_questions()

            messagebox.showwarning(
                "No Exams",
                (
                    "No exams have been created yet.\n\n"
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


        questions = exam_data.get(
            "questions",
            []
        )


        if not isinstance(
            questions,
            list
        ):

            questions = []


        self.display_questions(
            questions
        )


    # ========================================================
    # DISPLAY QUESTIONS
    # ========================================================

    def display_questions(
        self,
        questions
    ):

        # ----------------------------------------------------
        # CLEAR TABLE
        # ----------------------------------------------------

        for item in self.question_tree.get_children():

            self.question_tree.delete(
                item
            )


        # ----------------------------------------------------
        # CLEAR PREVIEW
        # ----------------------------------------------------

        self.clear_preview()


        # ----------------------------------------------------
        # SORT QUESTIONS
        # ----------------------------------------------------

        def question_sort_key(
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
            key=question_sort_key
        )


        # ----------------------------------------------------
        # ADD QUESTIONS
        # ----------------------------------------------------

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


            question_type = question.get(
                "question_type",
                ""
            )


            question_text = question.get(
                "question",
                ""
            )


            expected_answer = question.get(
                "expected_answer",
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


            keywords = question.get(
                "keywords",
                []
            )


            status = question.get(
                "status",
                "Active"
            )


            # ------------------------------------------------
            # KEYWORDS
            # ------------------------------------------------

            if isinstance(
                keywords,
                list
            ):

                keywords_display = ", ".join(
                    str(keyword)
                    for keyword in keywords
                )

            else:

                keywords_display = str(
                    keywords
                )


            # ------------------------------------------------
            # INSERT
            # ------------------------------------------------

            self.question_tree.insert(
                "",
                "end",
                values=(
                    question_no,
                    question_type,
                    question_text,
                    expected_answer,
                    marks,
                    difficulty,
                    topic,
                    keywords_display,
                    status
                )
            )


        # ----------------------------------------------------
        # QUESTION COUNT
        # ----------------------------------------------------

        count = len(
            self.question_tree.get_children()
        )


        self.question_count_label.config(
            text=f"Questions: {count}"
        )


        if count == 0:

            self.info_label.config(
                text=(
                    "This exam does not contain "
                    "any questions yet."
                )
            )

        else:

            self.info_label.config(
                text=(
                    "Select a question to see the "
                    "complete question and answer."
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

            self.clear_preview()

            return


        selected_item = selected_items[0]


        values = self.question_tree.item(
            selected_item,
            "values"
        )


        if not values:

            self.clear_preview()

            return


        (
            question_no,
            question_type,
            question,
            expected_answer,
            marks,
            difficulty,
            topic,
            keywords,
            status
        ) = values


        self.set_preview_text(
            self.question_preview,
            question
        )


        self.set_preview_text(
            self.answer_preview,
            expected_answer
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


        keywords_text = (
            keywords
            if keywords
            else "None"
        )


        status_text = (
            status
            if status
            else "Active"
        )


        self.extra_info_label.config(
            text=(
                f"Question No.: {question_no}    |    "
                f"Type: {question_type}    |    "
                f"Marks: {marks}    |    "
                f"Difficulty: {difficulty_text}    |    "
                f"Topic: {topic_text}    |    "
                f"Keywords: {keywords_text}    |    "
                f"Status: {status_text}"
            )
        )


    # ========================================================
    # SET PREVIEW TEXT
    # ========================================================

    def set_preview_text(
        self,
        text_widget,
        text
    ):

        text_widget.config(
            state="normal"
        )


        text_widget.delete(
            "1.0",
            tk.END
        )


        text_widget.insert(
            "1.0",
            str(text)
        )


        text_widget.config(
            state="disabled"
        )


    # ========================================================
    # CLEAR PREVIEW
    # ========================================================

    def clear_preview(self):

        self.set_preview_text(
            self.question_preview,
            ""
        )


        self.set_preview_text(
            self.answer_preview,
            ""
        )


        self.extra_info_label.config(
            text=""
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


        self.clear_preview()


    # ========================================================
    # DOUBLE CLICK DETAILS
    # ========================================================

    def show_question_details(
        self,
        event=None
    ):

        selected_items = (
            self.question_tree.selection()
        )


        if not selected_items:

            return


        selected_item = selected_items[0]


        values = self.question_tree.item(
            selected_item,
            "values"
        )


        if not values:

            return


        (
            question_no,
            question_type,
            question,
            expected_answer,
            marks,
            difficulty,
            topic,
            keywords,
            status
        ) = values


        details_window = tk.Toplevel(
            self.root
        )


        details_window.title(
            "Question Details"
        )


        details_window.geometry(
            "850x700"
        )


        details_window.minsize(
            700,
            550
        )


        details_window.configure(
            bg="#f4f6f8"
        )


        maximize_window(
            details_window
        )


        # ====================================================
        # HEADER
        # ====================================================

        header = tk.Frame(
            details_window,
            bg="#1f2937",
            height=80
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )


        tk.Label(
            header,
            text=f"QUESTION {question_no}",
            font=("Arial", 22, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=22
        )


        # ====================================================
        # DETAILS FRAME
        # ====================================================

        details_frame = tk.Frame(
            details_window,
            bg="white",
            bd=1,
            relief="solid"
        )

        details_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=20
        )


        # ====================================================
        # CANVAS
        # ====================================================

        canvas = tk.Canvas(
            details_frame,
            bg="white",
            highlightthickness=0
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        scrollbar = ttk.Scrollbar(
            details_frame,
            orient="vertical",
            command=canvas.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        canvas.configure(
            yscrollcommand=scrollbar.set
        )


        inner = tk.Frame(
            canvas,
            bg="white"
        )


        canvas_window = canvas.create_window(
            (0, 0),
            window=inner,
            anchor="nw"
        )


        def update_region(
            event=None
        ):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )


        def resize_inner(
            event
        ):

            canvas.itemconfig(
                canvas_window,
                width=event.width
            )


        inner.bind(
            "<Configure>",
            update_region
        )


        canvas.bind(
            "<Configure>",
            resize_inner
        )


        # ====================================================
        # DETAIL FUNCTION
        # ====================================================

        def add_detail(
            row,
            title,
            value
        ):

            tk.Label(
                inner,
                text=title,
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#374151"
            ).grid(
                row=row,
                column=0,
                sticky="nw",
                padx=20,
                pady=12
            )


            tk.Label(
                inner,
                text=(
                    str(value)
                    if value
                    else "Not specified"
                ),
                font=("Arial", 11),
                bg="white",
                fg="#111827",
                wraplength=550,
                justify="left"
            ).grid(
                row=row,
                column=1,
                sticky="nw",
                padx=20,
                pady=12
            )


        # ====================================================
        # DETAILS
        # ====================================================

        add_detail(
            0,
            "Question Number",
            question_no
        )

        add_detail(
            1,
            "Question Type",
            question_type
        )

        add_detail(
            2,
            "Question",
            question
        )

        add_detail(
            3,
            "Expected Answer",
            expected_answer
        )

        add_detail(
            4,
            "Marks",
            marks
        )

        add_detail(
            5,
            "Difficulty",
            difficulty
        )

        add_detail(
            6,
            "Topic",
            topic
        )

        add_detail(
            7,
            "Keywords",
            keywords
        )

        add_detail(
            8,
            "Status",
            status
        )


        # ====================================================
        # CLOSE BUTTON
        # ====================================================

        tk.Button(
            details_window,
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
            command=details_window.destroy
        ).pack(
            pady=(0, 15)
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


        # ----------------------------------------------------
        # CLOSE
        # ----------------------------------------------------

        try:

            self.root.destroy()

        except Exception:

            pass


        # ----------------------------------------------------
        # RESTORE QUESTION MANAGEMENT
        # ----------------------------------------------------

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
# OPEN VIEW QUESTIONS
# ============================================================

def open_view_questions(
    parent_window=None
):

    window = tk.Toplevel(
        parent_window
    )


    maximize_window(
        window
    )


    ViewQuestions(
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


    open_view_questions(
        parent_window=root
    )


    root.mainloop()
