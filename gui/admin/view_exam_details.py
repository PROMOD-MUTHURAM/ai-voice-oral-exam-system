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
# VIEW EXAM DETAILS
# ============================================================

class ViewExamDetails:

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
            "View Exam Details - AI Oral Exam System"
        )

        self.root.geometry(
            "1100x750"
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
        # CLOSE
        # ----------------------------------------------------

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.back
        )


        # ----------------------------------------------------
        # CREATE GUI
        # ----------------------------------------------------

        self.create_interface()

        self.load_exam_list()


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
            text="VIEW EXAM DETAILS",
            font=("Arial", 27, "bold"),
            bg="#1f2937",
            fg="white"
        ).pack(
            pady=(18, 3)
        )


        tk.Label(
            header_frame,
            text="View complete examination information",
            font=("Arial", 11),
            bg="#1f2937",
            fg="#d1d5db"
        ).pack()


        # ====================================================
        # SELECT EXAM AREA
        # ====================================================

        select_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        select_frame.pack(
            fill="x",
            padx=45,
            pady=(15, 10)
        )


        tk.Label(
            select_frame,
            text="Select Exam:",
            font=("Arial", 11, "bold"),
            bg="#f4f6f8",
            fg="#374151"
        ).pack(
            side="left",
            padx=(0, 10)
        )


        self.exam_combo = ttk.Combobox(
            select_frame,
            width=40,
            state="readonly"
        )

        self.exam_combo.pack(
            side="left"
        )


        self.exam_combo.bind(
            "<<ComboboxSelected>>",
            self.on_exam_selected
        )


        tk.Button(
            select_frame,
            text="REFRESH",
            font=("Arial", 10, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=12,
            height=1,
            bd=0,
            cursor="hand2",
            command=self.load_exam_list
        ).pack(
            side="left",
            padx=12
        )


        # ====================================================
        # SCROLLABLE AREA
        # ====================================================

        scroll_container = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        scroll_container.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(5, 10)
        )


        # ----------------------------------------------------
        # CANVAS
        # ----------------------------------------------------

        self.canvas = tk.Canvas(
            scroll_container,
            bg="#f4f6f8",
            highlightthickness=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ----------------------------------------------------
        # VERTICAL SCROLLBAR
        # ----------------------------------------------------

        vertical_scrollbar = ttk.Scrollbar(
            scroll_container,
            orient="vertical",
            command=self.canvas.yview
        )

        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )


        self.canvas.configure(
            yscrollcommand=vertical_scrollbar.set
        )


        # ----------------------------------------------------
        # SCROLLABLE CONTENT FRAME
        # ----------------------------------------------------

        self.content_frame = tk.Frame(
            self.canvas,
            bg="#f4f6f8"
        )


        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.content_frame,
            anchor="nw"
        )


        self.content_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )


        self.canvas.bind(
            "<Configure>",
            self.resize_content
        )


        # ----------------------------------------------------
        # MOUSE WHEEL
        # ----------------------------------------------------

        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_wheel
        )


        # ====================================================
        # EXAM INFORMATION CARD
        # ====================================================

        self.info_card = tk.Frame(
            self.content_frame,
            bg="white",
            bd=1,
            relief="solid",
            padx=30,
            pady=25
        )

        self.info_card.pack(
            fill="x",
            pady=(0, 15)
        )


        tk.Label(
            self.info_card,
            text="EXAM INFORMATION",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#1f2937"
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            pady=(0, 18)
        )


        # ----------------------------------------------------
        # VALUES
        # ----------------------------------------------------

        self.exam_id_value = self.create_info_row(
            "Exam ID:",
            1,
            0
        )

        self.exam_name_value = self.create_info_row(
            "Exam Name:",
            1,
            2
        )

        self.subject_value = self.create_info_row(
            "Subject:",
            2,
            0
        )

        self.status_value = self.create_info_row(
            "Status:",
            2,
            2
        )

        self.duration_value = self.create_info_row(
            "Duration:",
            3,
            0
        )

        self.answer_time_value = self.create_info_row(
            "Answer Time:",
            3,
            2
        )

        self.pass_percentage_value = self.create_info_row(
            "Pass Percentage:",
            4,
            0
        )

        self.total_questions_value = self.create_info_row(
            "Total Questions:",
            4,
            2
        )

        self.total_marks_value = self.create_info_row(
            "Total Marks:",
            5,
            0
        )

        self.created_at_value = self.create_info_row(
            "Created At:",
            5,
            2
        )

        self.updated_at_value = self.create_info_row(
            "Updated At:",
            6,
            0
        )


        # ====================================================
        # DESCRIPTION
        # ====================================================

        description_card = tk.Frame(
            self.content_frame,
            bg="white",
            bd=1,
            relief="solid",
            padx=30,
            pady=20
        )

        description_card.pack(
            fill="x",
            pady=(0, 15)
        )


        tk.Label(
            description_card,
            text="DESCRIPTION",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(
            anchor="w",
            pady=(0, 10)
        )


        self.description_value = tk.Label(
            description_card,
            text="-",
            font=("Arial", 11),
            bg="white",
            fg="#374151",
            justify="left",
            anchor="w",
            wraplength=950
        )

        self.description_value.pack(
            fill="x"
        )


        # ====================================================
        # QUESTIONS
        # ====================================================

        tk.Label(
            self.content_frame,
            text="QUESTIONS",
            font=("Arial", 16, "bold"),
            bg="#f4f6f8",
            fg="#1f2937"
        ).pack(
            anchor="w",
            pady=(5, 10)
        )


        table_frame = tk.Frame(
            self.content_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        table_frame.pack(
            fill="both",
            expand=False,
            pady=(0, 20)
        )


        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        columns = (
            "question_no",
            "question",
            "expected_answer",
            "marks"
        )


        self.question_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )


        self.question_table.heading(
            "question_no",
            text="Question No."
        )

        self.question_table.heading(
            "question",
            text="Question"
        )

        self.question_table.heading(
            "expected_answer",
            text="Expected Answer"
        )

        self.question_table.heading(
            "marks",
            text="Marks"
        )


        self.question_table.column(
            "question_no",
            width=100,
            anchor="center"
        )

        self.question_table.column(
            "question",
            width=450,
            anchor="w"
        )

        self.question_table.column(
            "expected_answer",
            width=550,
            anchor="w"
        )

        self.question_table.column(
            "marks",
            width=80,
            anchor="center"
        )


        table_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.question_table.yview
        )


        self.question_table.configure(
            yscrollcommand=table_scrollbar.set
        )


        self.question_table.pack(
            side="left",
            fill="both",
            expand=True
        )


        table_scrollbar.pack(
            side="right",
            fill="y"
        )


        # ====================================================
        # BOTTOM BUTTONS
        # ====================================================

        button_frame = tk.Frame(
            main_frame,
            bg="#f4f6f8"
        )

        button_frame.pack(
            fill="x",
            pady=(0, 15)
        )


        tk.Button(
            button_frame,
            text="BACK",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=18,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        ).pack()


    # ========================================================
    # CREATE INFORMATION ROW
    # ========================================================

    def create_info_row(
        self,
        label_text,
        row,
        column
    ):

        tk.Label(
            self.info_card,
            text=label_text,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#374151"
        ).grid(
            row=row,
            column=column,
            sticky="w",
            padx=(0, 8),
            pady=7
        )


        value_label = tk.Label(
            self.info_card,
            text="-",
            font=("Arial", 11),
            bg="white",
            fg="#111827",
            anchor="w"
        )


        value_label.grid(
            row=row,
            column=column + 1,
            sticky="w",
            padx=(0, 35),
            pady=7
        )


        return value_label


    # ========================================================
    # SCROLL REGION
    # ========================================================

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )


    # ========================================================
    # RESIZE CONTENT
    # ========================================================

    def resize_content(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )


    # ========================================================
    # MOUSE WHEEL
    # ========================================================

    def mouse_wheel(self, event):

        try:

            self.canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        except Exception:

            pass


    # ========================================================
    # LOAD EXAM LIST
    # ========================================================

    def load_exam_list(self):

        exam_files = []


        if os.path.exists(EXAMS_DIR):

            for filename in os.listdir(
                EXAMS_DIR
            ):

                if filename.lower().endswith(
                    ".json"
                ):

                    exam_files.append(
                        filename
                    )


        exam_files.sort()


        self.exam_combo["values"] = exam_files


        if exam_files:

            self.exam_combo.current(0)

            self.load_selected_exam(
                exam_files[0]
            )

        else:

            self.exam_combo.set("")

            self.clear_details()

            messagebox.showinfo(
                "No Exams",
                "No exam files are available.",
                parent=self.root
            )


    # ========================================================
    # EXAM SELECTED
    # ========================================================

    def on_exam_selected(self, event=None):

        filename = self.exam_combo.get()

        if filename:

            self.load_selected_exam(
                filename
            )


    # ========================================================
    # LOAD SELECTED EXAM
    # ========================================================

    def load_selected_exam(
        self,
        filename
    ):

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
                "Invalid exam file format.",
                parent=self.root
            )

            return


        self.display_exam(
            exam_data
        )


    # ========================================================
    # DISPLAY EXAM
    # ========================================================

    def display_exam(
        self,
        exam_data
    ):

        exam_id = exam_data.get(
            "exam_id",
            exam_data.get(
                "id",
                "-"
            )
        )


        exam_name = exam_data.get(
            "exam_name",
            exam_data.get(
                "name",
                "-"
            )
        )


        subject = exam_data.get(
            "subject",
            "-"
        )


        description = exam_data.get(
            "description",
            "-"
        )


        duration = exam_data.get(
            "duration_minutes",
            "-"
        )


        answer_time = exam_data.get(
            "answer_time_seconds",
            "-"
        )


        pass_percentage = exam_data.get(
            "pass_percentage",
            "-"
        )


        status = exam_data.get(
            "status",
            "Inactive"
        )


        questions = exam_data.get(
            "questions",
            []
        )


        if not isinstance(
            questions,
            list
        ):

            questions = []


        # ----------------------------------------------------
        # TOTAL MARKS
        # ----------------------------------------------------

        total_marks = 0


        for question_data in questions:

            if not isinstance(
                question_data,
                dict
            ):

                continue


            try:

                total_marks += float(
                    question_data.get(
                        "marks",
                        0
                    )
                )

            except Exception:

                pass


        # ----------------------------------------------------
        # VALUES
        # ----------------------------------------------------

        self.exam_id_value.config(
            text=str(exam_id)
        )

        self.exam_name_value.config(
            text=str(exam_name)
        )

        self.subject_value.config(
            text=str(subject)
        )

        self.status_value.config(
            text=str(status).upper()
        )


        self.duration_value.config(
            text=f"{duration} minutes"
        )


        self.answer_time_value.config(
            text=f"{answer_time} seconds"
        )


        self.pass_percentage_value.config(
            text=f"{pass_percentage}%"
        )


        self.total_questions_value.config(
            text=str(len(questions))
        )


        if total_marks.is_integer():

            total_marks_text = str(
                int(total_marks)
            )

        else:

            total_marks_text = str(
                total_marks
            )


        self.total_marks_value.config(
            text=total_marks_text
        )


        self.created_at_value.config(
            text=str(
                exam_data.get(
                    "created_at",
                    "-"
                )
            )
        )


        self.updated_at_value.config(
            text=str(
                exam_data.get(
                    "updated_at",
                    "-"
                )
            )
        )


        self.description_value.config(
            text=str(description)
        )


        # ====================================================
        # CLEAR QUESTION TABLE
        # ====================================================

        for item in self.question_table.get_children():

            self.question_table.delete(
                item
            )


        # ====================================================
        # ADD QUESTIONS
        # ====================================================

        for index, question_data in enumerate(
            questions,
            start=1
        ):

            if not isinstance(
                question_data,
                dict
            ):

                continue


            question_no = question_data.get(
                "question_no",
                question_data.get(
                    "question_number",
                    index
                )
            )


            question = question_data.get(
                "question",
                ""
            )


            expected_answer = question_data.get(
                "expected_answer",
                ""
            )


            marks = question_data.get(
                "marks",
                0
            )


            self.question_table.insert(
                "",
                "end",
                values=(
                    question_no,
                    question,
                    expected_answer,
                    marks
                )
            )


        # ----------------------------------------------------
        # Reset scroll to top
        # ----------------------------------------------------

        self.canvas.after(
            50,
            lambda: self.canvas.yview_moveto(0)
        )


    # ========================================================
    # CLEAR DETAILS
    # ========================================================

    def clear_details(self):

        self.exam_id_value.config(
            text="-"
        )

        self.exam_name_value.config(
            text="-"
        )

        self.subject_value.config(
            text="-"
        )

        self.status_value.config(
            text="-"
        )

        self.duration_value.config(
            text="-"
        )

        self.answer_time_value.config(
            text="-"
        )

        self.pass_percentage_value.config(
            text="-"
        )

        self.total_questions_value.config(
            text="0"
        )

        self.total_marks_value.config(
            text="0"
        )

        self.created_at_value.config(
            text="-"
        )

        self.updated_at_value.config(
            text="-"
        )

        self.description_value.config(
            text="-"
        )


        for item in self.question_table.get_children():

            self.question_table.delete(
                item
            )


    # ========================================================
    # BACK
    # ========================================================

    def back(self):

        if self.parent_window is not None:

            try:

                if self.parent_window.winfo_exists():

                    self.root.destroy()

                    self.parent_window.deiconify()

                    maximize_window(
                        self.parent_window
                    )

                    self.parent_window.lift()

                    self.parent_window.focus_force()

                    return

            except Exception as e:

                print(
                    "Could not return to previous window:",
                    e
                )


        answer = messagebox.askyesno(
            "Exit",
            "Do you want to close this window?",
            parent=self.root
        )


        if answer:

            self.root.destroy()


# ============================================================
# OPEN VIEW EXAM DETAILS
# ============================================================

def open_view_exam_details(
    parent_window=None
):

    window = tk.Toplevel(
        parent_window
    )


    maximize_window(
        window
    )


    ViewExamDetails(
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


    open_view_exam_details(
        parent_window=root
    )


    root.mainloop()
