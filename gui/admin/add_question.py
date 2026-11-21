
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
# ADD QUESTION
# ============================================================

class AddQuestion:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        # Previous Question Management window
        self.parent_window = parent_window


        # ----------------------------------------------------
        # WINDOW SETTINGS
        # ----------------------------------------------------

        self.root.title(
            "Add New Question - AI Oral Examination System"
        )

        self.root.geometry(
            "1100x800"
        )

        self.root.minsize(
            900,
            700
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
            text="ADD NEW QUESTION",
            font=("Arial", 27, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(18, 3)
        )


        tk.Label(
            header_frame,
            text=(
                "Add a question to an examination"
            ),
            font=("Arial", 11),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack()


        # ====================================================
        # SCROLLABLE CONTENT OUTER FRAME
        # ====================================================

        content_outer_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        content_outer_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )


        # ====================================================
        # CANVAS
        # ====================================================

        content_canvas = tk.Canvas(
            content_outer_frame,
            bg="#f4f6f8",
            highlightthickness=0
        )

        content_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ====================================================
        # VERTICAL SCROLLBAR
        # ====================================================

        content_scrollbar = ttk.Scrollbar(
            content_outer_frame,
            orient="vertical",
            command=content_canvas.yview
        )

        content_scrollbar.pack(
            side="right",
            fill="y"
        )


        content_canvas.configure(
            yscrollcommand=content_scrollbar.set
        )


        # ====================================================
        # SCROLLABLE CONTENT FRAME
        # ====================================================

        content_frame = tk.Frame(
            content_canvas,
            bg="#f4f6f8"
        )


        content_window = content_canvas.create_window(
            (0, 0),
            window=content_frame,
            anchor="nw"
        )


        # ====================================================
        # UPDATE SCROLL REGION
        # ====================================================

        def update_scroll_region(event=None):

            try:

                if content_canvas.winfo_exists():

                    content_canvas.configure(
                        scrollregion=content_canvas.bbox("all")
                    )

            except tk.TclError:

                pass


        content_frame.bind(
            "<Configure>",
            update_scroll_region
        )


        # ====================================================
        # MAKE CONTENT WIDTH MATCH CANVAS
        # ====================================================

        def update_content_width(event):

            try:

                if content_canvas.winfo_exists():

                    content_canvas.itemconfig(
                        content_window,
                        width=event.width
                    )

            except tk.TclError:

                pass


        content_canvas.bind(
            "<Configure>",
            update_content_width
        )


        # ====================================================
        # SAFE MOUSE WHEEL
        # ====================================================

        def mouse_wheel(event):

            try:

                if not self.root.winfo_exists():

                    return


                if not content_canvas.winfo_exists():

                    return


                # Windows mouse wheel
                delta = event.delta


                if delta == 0:

                    return


                content_canvas.yview_scroll(
                    int(-1 * (delta / 120)),
                    "units"
                )


            except tk.TclError:

                pass


            except Exception as e:

                print(
                    "Mouse wheel error:",
                    e
                )


        # ----------------------------------------------------
        # Enable mouse wheel when pointer enters canvas
        # ----------------------------------------------------

        def enable_mouse_wheel(event=None):

            try:

                if content_canvas.winfo_exists():

                    content_canvas.bind(
                        "<MouseWheel>",
                        mouse_wheel
                    )

            except tk.TclError:

                pass


        # ----------------------------------------------------
        # Disable mouse wheel when pointer leaves canvas
        # ----------------------------------------------------

        def disable_mouse_wheel(event=None):

            try:

                if content_canvas.winfo_exists():

                    content_canvas.unbind(
                        "<MouseWheel>"
                    )

            except tk.TclError:

                pass


        content_canvas.bind(
            "<Enter>",
            enable_mouse_wheel
        )


        content_canvas.bind(
            "<Leave>",
            disable_mouse_wheel
        )


        # ====================================================
        # FORM CARD
        # ====================================================

        form_card = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid",
            padx=40,
            pady=25
        )

        form_card.pack(
            fill="x",
            padx=40,
            pady=10
        )


        # ====================================================
        # EXAM SELECTION
        # ====================================================

        tk.Label(
            form_card,
            text="Select Exam",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=9
        )


        self.exam_combo = ttk.Combobox(
            form_card,
            width=48,
            state="readonly"
        )

        self.exam_combo.grid(
            row=0,
            column=1,
            padx=25,
            pady=9,
            sticky="w"
        )


        # ====================================================
        # QUESTION NUMBER
        # ====================================================

        tk.Label(
            form_card,
            text="Question Number",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=9
        )


        self.question_number_entry = ttk.Entry(
            form_card,
            width=51
        )

        self.question_number_entry.grid(
            row=1,
            column=1,
            padx=25,
            pady=9,
            sticky="w"
        )


        # ====================================================
        # QUESTION TYPE
        # ====================================================

        tk.Label(
            form_card,
            text="Question Type",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=9
        )


        self.question_type_combo = ttk.Combobox(
            form_card,
            width=48,
            state="readonly",
            values=[
                "One Word / 1 Mark",
                "Short Answer",
                "Descriptive Answer"
            ]
        )

        self.question_type_combo.grid(
            row=2,
            column=1,
            padx=25,
            pady=9,
            sticky="w"
        )


        self.question_type_combo.set(
            "One Word / 1 Mark"
        )


        # ====================================================
        # MARKS
        # ====================================================

        tk.Label(
            form_card,
            text="Marks",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=9
        )


        self.marks_entry = ttk.Entry(
            form_card,
            width=51
        )

        self.marks_entry.grid(
            row=3,
            column=1,
            padx=25,
            pady=9,
            sticky="w"
        )


        self.marks_entry.insert(
            0,
            "1"
        )


        # ====================================================
        # QUESTION
        # ====================================================

        tk.Label(
            form_card,
            text="Question",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=4,
            column=0,
            sticky="nw",
            pady=9
        )


        self.question_text = tk.Text(
            form_card,
            width=49,
            height=4,
            font=("Arial", 11),
            bd=1,
            relief="solid",
            wrap="word"
        )

        self.question_text.grid(
            row=4,
            column=1,
            padx=25,
            pady=9,
            sticky="w"
        )


        # ====================================================
        # EXPECTED ANSWER
        # ====================================================

        tk.Label(
            form_card,
            text="Expected Answer",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=5,
            column=0,
            sticky="nw",
            pady=9
        )


        self.expected_answer_text = tk.Text(
            form_card,
            width=49,
            height=4,
            font=("Arial", 11),
            bd=1,
            relief="solid",
            wrap="word"
        )

        self.expected_answer_text.grid(
            row=5,
            column=1,
            padx=25,
            pady=9,
            sticky="w"
        )


        # ====================================================
        # DIFFICULTY - OPTIONAL
        # ====================================================

        tk.Label(
            form_card,
            text="Difficulty (Optional)",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=6,
            column=0,
            sticky="w",
            pady=9
        )


        self.difficulty_combo = ttk.Combobox(
            form_card,
            width=48,
            state="readonly",
            values=[
                "",
                "Easy",
                "Medium",
                "Hard"
            ]
        )

        self.difficulty_combo.grid(
            row=6,
            column=1,
            padx=25,
            pady=9,
            sticky="w"
        )


        self.difficulty_combo.set("")


        # ====================================================
        # TOPIC - OPTIONAL
        # ====================================================

        tk.Label(
            form_card,
            text="Topic (Optional)",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=7,
            column=0,
            sticky="w",
            pady=9
        )


        self.topic_entry = ttk.Entry(
            form_card,
            width=51
        )

        self.topic_entry.grid(
            row=7,
            column=1,
            padx=25,
            pady=9,
            sticky="w"
        )


        # ====================================================
        # KEYWORDS - OPTIONAL
        # ====================================================

        tk.Label(
            form_card,
            text="Keywords (Optional)",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=8,
            column=0,
            sticky="nw",
            pady=9
        )


        self.keywords_text = tk.Text(
            form_card,
            width=49,
            height=3,
            font=("Arial", 11),
            bd=1,
            relief="solid",
            wrap="word"
        )

        self.keywords_text.grid(
            row=8,
            column=1,
            padx=25,
            pady=9,
            sticky="w"
        )


        tk.Label(
            form_card,
            text=(
                "Optional: enter one or multiple keywords "
                "separated by commas."
            ),
            font=("Arial", 9),
            bg="white",
            fg="#6b7280"
        ).grid(
            row=9,
            column=1,
            sticky="w",
            padx=25,
            pady=(0, 8)
        )


        # ====================================================
        # STATUS - REQUIRED
        # ====================================================

        tk.Label(
            form_card,
            text="Status *",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=10,
            column=0,
            sticky="w",
            pady=9
        )


        self.status_combo = ttk.Combobox(
            form_card,
            width=48,
            state="readonly",
            values=[
                "Active",
                "Inactive"
            ]
        )

        self.status_combo.grid(
            row=10,
            column=1,
            padx=25,
            pady=9,
            sticky="w"
        )


        # Required field - default Active
        self.status_combo.set(
            "Active"
        )


        tk.Label(
            form_card,
            text=(
                "Required. New questions are Active by default."
            ),
            font=("Arial", 9),
            bg="white",
            fg="#6b7280"
        ).grid(
            row=11,
            column=1,
            sticky="w",
            padx=25,
            pady=(0, 8)
        )


        # ====================================================
        # BUTTON FRAME
        # ====================================================

        button_frame = tk.Frame(
            content_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            pady=(10, 20)
        )


        # ====================================================
        # SAVE
        # ====================================================

        tk.Button(
            button_frame,
            text="SAVE QUESTION",
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


        # ====================================================
        # CLEAR
        # ====================================================

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


        # ====================================================
        # BACK
        # ====================================================

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
    # LOAD EXAMS
    # ========================================================

    def load_exams(self):

        exam_list = []


        if not os.path.exists(EXAMS_DIR):

            self.exam_combo["values"] = []

            return


        try:

            files = os.listdir(
                EXAMS_DIR
            )


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


        except Exception as e:

            messagebox.showerror(
                "Exam Error",
                (
                    "Could not load examinations.\n\n"
                    f"{e}"
                ),
                parent=self.root
            )

            return


        exam_list.sort()


        self.exam_combo["values"] = exam_list


        if exam_list:

            self.exam_combo.current(
                0
            )

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

            exam_id = selected.split(
                " - ",
                1
            )[0].strip()

        else:

            exam_id = selected


        return exam_id


    # ========================================================
    # GET NEXT QUESTION NUMBER
    # ========================================================

    def get_next_question_number(
        self,
        exam_data
    ):

        questions = exam_data.get(
            "questions",
            []
        )


        if not isinstance(
            questions,
            list
        ):

            return 1


        highest_number = 0


        for question in questions:

            if not isinstance(
                question,
                dict
            ):

                continue


            number = question.get(
                "question_no",
                0
            )


            try:

                number = int(
                    number
                )

                if number > highest_number:

                    highest_number = number

            except Exception:

                pass


        return highest_number + 1


    # ========================================================
    # VALIDATE FORM
    # ========================================================

    def validate_form(self):

        exam_id = self.get_selected_exam_id()


        if not exam_id:

            messagebox.showwarning(
                "Missing Exam",
                "Please select an exam.",
                parent=self.root
            )

            self.exam_combo.focus_set()

            return None


        question_number = (
            self.question_number_entry
            .get()
            .strip()
        )


        question_type = (
            self.question_type_combo
            .get()
            .strip()
        )


        marks = (
            self.marks_entry
            .get()
            .strip()
        )


        question = (
            self.question_text
            .get(
                "1.0",
                tk.END
            )
            .strip()
        )


        expected_answer = (
            self.expected_answer_text
            .get(
                "1.0",
                tk.END
            )
            .strip()
        )


        difficulty = (
            self.difficulty_combo
            .get()
            .strip()
        )


        topic = (
            self.topic_entry
            .get()
            .strip()
        )


        keywords_text = (
            self.keywords_text
            .get(
                "1.0",
                tk.END
            )
            .strip()
        )


        status = (
            self.status_combo
            .get()
            .strip()
        )


        # ====================================================
        # QUESTION NUMBER
        # ====================================================

        try:

            question_number_value = int(
                question_number
            )

            if question_number_value <= 0:

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


        # ====================================================
        # QUESTION TYPE
        # ====================================================

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

            self.question_type_combo.focus_set()

            return None


        # ====================================================
        # MARKS
        # ====================================================

        try:

            marks_value = float(
                marks
            )

            if marks_value <= 0:

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


        # ====================================================
        # QUESTION
        # ====================================================

        if not question:

            messagebox.showwarning(
                "Missing Question",
                "Please enter the question.",
                parent=self.root
            )

            self.question_text.focus_set()

            return None


        # ====================================================
        # EXPECTED ANSWER
        # ====================================================

        if not expected_answer:

            messagebox.showwarning(
                "Missing Expected Answer",
                "Please enter the expected answer.",
                parent=self.root
            )

            self.expected_answer_text.focus_set()

            return None


        # ====================================================
        # STATUS
        # ====================================================

        if status not in (
            "Active",
            "Inactive"
        ):

            messagebox.showwarning(
                "Invalid Status",
                (
                    "Please select a valid question status."
                ),
                parent=self.root
            )

            self.status_combo.focus_set()

            return None


        # ====================================================
        # KEYWORDS
        # ====================================================

        keywords = []


        if keywords_text:

            raw_keywords = (
                keywords_text.split(",")
            )


            for keyword in raw_keywords:

                keyword = keyword.strip()


                if keyword:

                    keywords.append(
                        keyword
                    )


        # ====================================================
        # RETURN DATA
        # ====================================================

        return {

            "question_no": question_number_value,

            "question_type": question_type,

            "question": question,

            "expected_answer": expected_answer,

            "keywords": keywords,

            "marks": marks_value,

            "difficulty": difficulty,

            "topic": topic,

            "status": status,

            "created_at": (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            ),

            "updated_at": (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        }


    # ========================================================
    # SAVE QUESTION
    # ========================================================

    def save_question(self):

        question_data = self.validate_form()


        if question_data is None:

            return


        exam_id = self.get_selected_exam_id()


        file_path = os.path.join(
            EXAMS_DIR,
            f"{exam_id}.json"
        )


        # ----------------------------------------------------
        # CHECK EXAM FILE
        # ----------------------------------------------------

        if not os.path.exists(file_path):

            messagebox.showerror(
                "Exam Not Found",
                (
                    f"Exam file for {exam_id} "
                    "could not be found."
                ),
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # LOAD EXAM
        # ----------------------------------------------------

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
                "Exam Error",
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
                "Exam Error",
                "Invalid exam data.",
                parent=self.root
            )

            return


        # ----------------------------------------------------
        # GET QUESTIONS
        # ----------------------------------------------------

        if "questions" not in exam_data:

            exam_data["questions"] = []


        if not isinstance(
            exam_data["questions"],
            list
        ):

            exam_data["questions"] = []


        # ----------------------------------------------------
        # CHECK DUPLICATE QUESTION NUMBER
        # ----------------------------------------------------

        for existing_question in exam_data[
            "questions"
        ]:

            if not isinstance(
                existing_question,
                dict
            ):

                continue


            existing_number = existing_question.get(
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


        # ----------------------------------------------------
        # ADD QUESTION
        # ----------------------------------------------------

        exam_data[
            "questions"
        ].append(
            question_data
        )


        # ----------------------------------------------------
        # UPDATE EXAM SUMMARY
        # ----------------------------------------------------

        exam_data[
            "total_questions"
        ] = len(
            exam_data["questions"]
        )


        total_marks = 0


        for question in exam_data[
            "questions"
        ]:

            try:

                total_marks += float(
                    question.get(
                        "marks",
                        0
                    )
                )

            except Exception:

                pass


        exam_data[
            "total_marks"
        ] = total_marks


        exam_data[
            "updated_at"
        ] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )


        # ----------------------------------------------------
        # SAVE EXAM
        # ----------------------------------------------------

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


            messagebox.showinfo(
                "Question Saved",
                (
                    "Question added successfully.\n\n"
                    f"Exam: {exam_id}\n"
                    f"Question No.: "
                    f"{question_data['question_no']}\n"
                    f"Status: "
                    f"{question_data['status']}"
                ),
                parent=self.root
            )


            # ------------------------------------------------
            # Prepare next question
            # ------------------------------------------------

            self.clear_question_fields(
                next_number=(
                    question_data["question_no"] + 1
                )
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


    # ========================================================
    # CLEAR QUESTION FIELDS
    # ========================================================

    def clear_question_fields(
        self,
        next_number=1
    ):

        self.question_number_entry.delete(
            0,
            tk.END
        )

        self.question_number_entry.insert(
            0,
            str(next_number)
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


        # Status always defaults to Active
        self.status_combo.set(
            "Active"
        )


        self.question_text.focus_set()


    # ========================================================
    # CLEAR
    # ========================================================

    def clear_form(self):

        selected_exam = self.exam_combo.get()


        self.clear_question_fields(
            next_number=1
        )


        if selected_exam:

            self.exam_combo.set(
                selected_exam
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
        # Remove any remaining mouse-wheel binding
        # ----------------------------------------------------

        try:

            self.root.unbind_all(
                "<MouseWheel>"
            )

        except Exception:

            pass


        # ----------------------------------------------------
        # Close Add Question
        # ----------------------------------------------------

        try:

            self.root.destroy()

        except Exception:

            pass


        # ----------------------------------------------------
        # Restore Question Management
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
# OPEN ADD QUESTION
# ============================================================

def open_add_question(
    parent_window=None
):

    window = tk.Toplevel(
        parent_window
    )


    maximize_window(
        window
    )


    AddQuestion(
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


    open_add_question(
        parent_window=root
    )


    root.mainloop()

