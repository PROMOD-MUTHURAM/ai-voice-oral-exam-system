
import tkinter as tk
from tkinter import messagebox
import os
import sys
import json


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
# BACKEND DIRECTORY
# ============================================================

BACKEND_DIR = os.path.join(
    BASE_DIR,
    "backend"
)

os.makedirs(
    BACKEND_DIR,
    exist_ok=True
)


# ============================================================
# CONFIGURATION FILE
# ============================================================

CONFIG_FILE = os.path.join(
    BACKEND_DIR,
    "student_details_config.json"
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
# RESTORE WINDOW
# ============================================================

def restore_window(window):

    if window is None:
        return

    try:

        if window.winfo_exists():

            window.deiconify()

            maximize_window(
                window
            )

            window.lift()

            window.focus_force()

    except Exception as e:

        print(
            "Could not restore window:",
            e
        )


# ============================================================
# DEFAULT CONFIGURATION
# ============================================================

DEFAULT_CONFIG = {

    "fields": {

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
            "enabled": True,
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
}


# ============================================================
# LOAD CONFIGURATION
# ============================================================

def load_configuration():

    if not os.path.exists(CONFIG_FILE):

        return json.loads(
            json.dumps(DEFAULT_CONFIG)
        )

    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, dict):

            return json.loads(
                json.dumps(DEFAULT_CONFIG)
            )

        saved_fields = data.get(
            "fields",
            {}
        )

        if not isinstance(
            saved_fields,
            dict
        ):

            saved_fields = {}

        merged_fields = {}

        for field_id, default_field in DEFAULT_CONFIG[
            "fields"
        ].items():

            merged_field = default_field.copy()

            if isinstance(
                saved_fields.get(field_id),
                dict
            ):

                merged_field.update(
                    saved_fields[field_id]
                )

            merged_fields[field_id] = (
                merged_field
            )

        return {
            "fields": merged_fields
        }

    except Exception as e:

        print(
            "Could not load student details configuration:"
        )

        print(e)

        return json.loads(
            json.dumps(DEFAULT_CONFIG)
        )


# ============================================================
# SAVE CONFIGURATION
# ============================================================

def save_configuration(config):

    try:

        with open(
            CONFIG_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                config,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as e:

        print(
            "Could not save student details configuration:"
        )

        print(e)

        return False


# ============================================================
# STUDENT DETAILS CONFIGURATION
# ============================================================

class StudentDetailsConfiguration:

    def __init__(
        self,
        root,
        parent_window=None
    ):

        self.root = root

        # ----------------------------------------------------
        # Parent = Admin Control Panel
        # ----------------------------------------------------

        self.parent_window = (
            parent_window
        )

        # ----------------------------------------------------
        # Configuration
        # ----------------------------------------------------

        self.config = load_configuration()

        self.enabled_variables = {}

        self.required_variables = {}

        # ----------------------------------------------------
        # Window
        # ----------------------------------------------------

        self.root.title(
            "Student Details Configuration"
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

        maximize_window(
            self.root
        )

        # ----------------------------------------------------
        # Close
        # ----------------------------------------------------

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.back
        )

        # ----------------------------------------------------
        # Create GUI
        # ----------------------------------------------------

        self.create_interface()


    # ========================================================
    # CREATE INTERFACE
    # ========================================================

    def create_interface(self):

        # ====================================================
        # OUTER CONTAINER
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
        # CANVAS
        # ====================================================

        self.canvas = tk.Canvas(
            outer_frame,
            bg="#f4f6f8",
            highlightthickness=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        # ====================================================
        # VERTICAL SCROLLBAR
        # ====================================================

        scrollbar = tk.Scrollbar(
            outer_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )


        # ====================================================
        # SCROLLABLE FRAME
        # ====================================================

        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg="#f4f6f8"
        )


        self.canvas_window = (
            self.canvas.create_window(
                (0, 0),
                window=self.scrollable_frame,
                anchor="nw"
            )
        )


        # ====================================================
        # UPDATE SCROLL REGION
        # ====================================================

        self.scrollable_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )


        self.canvas.bind(
            "<Configure>",
            self.resize_scrollable_frame
        )


        # ====================================================
        # MOUSE WHEEL
        # ====================================================

        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_wheel
        )


        # Linux mouse wheel support

        self.canvas.bind_all(
            "<Button-4>",
            self.mouse_wheel_linux_up
        )

        self.canvas.bind_all(
            "<Button-5>",
            self.mouse_wheel_linux_down
        )


        # ====================================================
        # CREATE PAGE
        # ====================================================

        self.create_page()


    # ========================================================
    # UPDATE SCROLL REGION
    # ========================================================

    def update_scroll_region(
        self,
        event=None
    ):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )


    # ========================================================
    # RESIZE SCROLLABLE FRAME
    # ========================================================

    def resize_scrollable_frame(
        self,
        event
    ):

        try:

            self.canvas.itemconfigure(
                self.canvas_window,
                width=event.width
            )

        except Exception:

            pass


    # ========================================================
    # MOUSE WHEEL
    # ========================================================

    def mouse_wheel(
        self,
        event
    ):

        try:

            self.canvas.yview_scroll(
                int(
                    -1 * (event.delta / 120)
                ),
                "units"
            )

        except Exception:

            pass


    # ========================================================
    # LINUX SCROLL UP
    # ========================================================

    def mouse_wheel_linux_up(
        self,
        event
    ):

        try:

            self.canvas.yview_scroll(
                -3,
                "units"
            )

        except Exception:

            pass


    # ========================================================
    # LINUX SCROLL DOWN
    # ========================================================

    def mouse_wheel_linux_down(
        self,
        event
    ):

        try:

            self.canvas.yview_scroll(
                3,
                "units"
            )

        except Exception:

            pass


    # ========================================================
    # CREATE PAGE
    # ========================================================

    def create_page(self):

        # ====================================================
        # HEADER
        # ====================================================

        header_frame = tk.Frame(
            self.scrollable_frame,
            bg="#0f766e",
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
            text="STUDENT DETAILS CONFIGURATION",
            font=("Arial", 25, "bold"),
            bg="#0f766e",
            fg="white"
        ).pack(
            pady=(20, 5)
        )


        tk.Label(
            header_frame,
            text=(
                "Control which student details are "
                "displayed on the student-side form"
            ),
            font=("Arial", 11),
            bg="#0f766e",
            fg="#d1fae5"
        ).pack()


        # ====================================================
        # CONTENT
        # ====================================================

        content_frame = tk.Frame(
            self.scrollable_frame,
            bg="#f4f6f8"
        )

        content_frame.pack(
            fill="both",
            expand=False,
            padx=60,
            pady=25
        )


        # ====================================================
        # INFORMATION CARD
        # ====================================================

        info_frame = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        info_frame.pack(
            fill="x",
            pady=(0, 15)
        )


        tk.Label(
            info_frame,
            text="Student Details Fields",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#111827"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 3)
        )


        tk.Label(
            info_frame,
            text=(
                "Enable fields that should appear on the "
                "student-side Student Details form. "
                "Required fields must also be enabled."
            ),
            font=("Arial", 10),
            bg="white",
            fg="#6b7280",
            wraplength=900,
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )


        # ====================================================
        # FIELDS CARD
        # ====================================================

        fields_card = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        fields_card.pack(
            fill="x",
            expand=False
        )


        # ====================================================
        # TABLE HEADER
        # ====================================================

        table_header = tk.Frame(
            fields_card,
            bg="#e5e7eb",
            height=48
        )

        table_header.pack(
            fill="x"
        )

        table_header.pack_propagate(
            False
        )


        tk.Label(
            table_header,
            text="FIELD",
            font=("Arial", 11, "bold"),
            bg="#e5e7eb",
            fg="#111827",
            width=28,
            anchor="w"
        ).pack(
            side="left",
            padx=20
        )


        tk.Label(
            table_header,
            text="DISPLAY",
            font=("Arial", 11, "bold"),
            bg="#e5e7eb",
            fg="#111827",
            width=20
        ).pack(
            side="left"
        )


        tk.Label(
            table_header,
            text="REQUIRED",
            font=("Arial", 11, "bold"),
            bg="#e5e7eb",
            fg="#111827",
            width=18
        ).pack(
            side="left"
        )


        tk.Label(
            table_header,
            text="FIELD TYPE",
            font=("Arial", 11, "bold"),
            bg="#e5e7eb",
            fg="#111827",
            width=18
        ).pack(
            side="left"
        )


        # ====================================================
        # ROWS
        # ====================================================

        rows_frame = tk.Frame(
            fields_card,
            bg="white"
        )

        rows_frame.pack(
            fill="x"
        )


        for field_id, field_data in self.config[
            "fields"
        ].items():

            self.create_field_row(
                rows_frame,
                field_id,
                field_data
            )


        # ====================================================
        # SPACING
        # ====================================================

        tk.Frame(
            content_frame,
            bg="#f4f6f8",
            height=20
        ).pack(
            fill="x"
        )


        # ====================================================
        # BUTTON AREA
        # ====================================================

        button_card = tk.Frame(
            content_frame,
            bg="white",
            bd=1,
            relief="solid"
        )

        button_card.pack(
            fill="x"
        )


        # ====================================================
        # BUTTON BAR
        # ====================================================

        button_frame = tk.Frame(
            button_card,
            bg="white"
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )


        # ====================================================
        # BACK BUTTON
        # ====================================================

        back_button = tk.Button(
            button_frame,
            text="◀ BACK TO ADMIN CONTROL PANEL",
            font=("Arial", 11, "bold"),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            width=36,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.back
        )

        back_button.pack(
            side="left",
            padx=5
        )


        # ====================================================
        # RESET BUTTON
        # ====================================================

        reset_button = tk.Button(
            button_frame,
            text="RESET DEFAULTS",
            font=("Arial", 11, "bold"),
            bg="#f59e0b",
            fg="white",
            activebackground="#d97706",
            activeforeground="white",
            width=20,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.reset_defaults
        )

        reset_button.pack(
            side="left",
            padx=5
        )


        # ====================================================
        # SAVE BUTTON
        # ====================================================

        save_button = tk.Button(
            button_frame,
            text="SAVE CONFIGURATION",
            font=("Arial", 11, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=23,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.save
        )

        save_button.pack(
            side="right",
            padx=5
        )


        # ====================================================
        # BOTTOM SPACE
        # ====================================================

        tk.Frame(
            content_frame,
            bg="#f4f6f8",
            height=30
        ).pack(
            fill="x"
        )


        # ====================================================
        # START AT TOP
        # ====================================================

        self.root.after(
            100,
            lambda: self.canvas.yview_moveto(0)
        )


    # ========================================================
    # CREATE FIELD ROW
    # ========================================================

    def create_field_row(
        self,
        parent,
        field_id,
        field_data
    ):

        row = tk.Frame(
            parent,
            bg="white",
            height=55
        )

        row.pack(
            fill="x"
        )

        row.pack_propagate(
            False
        )


        # ====================================================
        # FIELD NAME
        # ====================================================

        tk.Label(
            row,
            text=field_data.get(
                "label",
                field_id
            ),
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#111827",
            width=28,
            anchor="w"
        ).pack(
            side="left",
            padx=20
        )


        # ====================================================
        # DISPLAY
        # ====================================================

        enabled_var = tk.BooleanVar(
            value=bool(
                field_data.get(
                    "enabled",
                    False
                )
            )
        )


        self.enabled_variables[
            field_id
        ] = enabled_var


        tk.Checkbutton(
            row,
            variable=enabled_var,
            bg="white",
            activebackground="white",
            cursor="hand2"
        ).pack(
            side="left",
            padx=70
        )


        # ====================================================
        # REQUIRED
        # ====================================================

        required_var = tk.BooleanVar(
            value=bool(
                field_data.get(
                    "required",
                    False
                )
            )
        )


        self.required_variables[
            field_id
        ] = required_var


        tk.Checkbutton(
            row,
            variable=required_var,
            bg="white",
            activebackground="white",
            cursor="hand2"
        ).pack(
            side="left",
            padx=55
        )


        # ====================================================
        # FIELD TYPE
        # ====================================================

        tk.Label(
            row,
            text=str(
                field_data.get(
                    "type",
                    "text"
                )
            ).upper(),
            font=("Arial", 10),
            bg="white",
            fg="#6b7280",
            width=18
        ).pack(
            side="left"
        )


        # ====================================================
        # SEPARATOR
        # ====================================================

        tk.Frame(
            parent,
            bg="#e5e7eb",
            height=1
        ).pack(
            fill="x"
        )


    # ========================================================
    # SAVE
    # ========================================================

    def save(self):

        # ----------------------------------------------------
        # Validate
        # ----------------------------------------------------

        for field_id in self.config[
            "fields"
        ]:

            enabled = self.enabled_variables[
                field_id
            ].get()

            required = self.required_variables[
                field_id
            ].get()


            if required and not enabled:

                field_label = self.config[
                    "fields"
                ][field_id].get(
                    "label",
                    field_id
                )


                messagebox.showwarning(
                    "Invalid Configuration",
                    (
                        f'"{field_label}" is marked as '
                        "required but DISPLAY is disabled.\n\n"
                        "Either enable the field or "
                        "remove REQUIRED."
                    ),
                    parent=self.root
                )

                return


        # ----------------------------------------------------
        # Update configuration
        # ----------------------------------------------------

        for field_id, field_data in self.config[
            "fields"
        ].items():

            field_data[
                "enabled"
            ] = self.enabled_variables[
                field_id
            ].get()


            field_data[
                "required"
            ] = self.required_variables[
                field_id
            ].get()


        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

        if not save_configuration(
            self.config
        ):

            messagebox.showerror(
                "Save Error",
                (
                    "Student Details Configuration "
                    "could not be saved."
                ),
                parent=self.root
            )

            return


        messagebox.showinfo(
            "Configuration Saved",
            (
                "Student Details Configuration "
                "saved successfully.\n\n"
                "The student-side Student Details "
                "form will use the new configuration "
                "the next time it is opened."
            ),
            parent=self.root
        )


    # ========================================================
    # RESET DEFAULTS
    # ========================================================

    def reset_defaults(self):

        answer = messagebox.askyesno(
            "Reset Defaults",
            (
                "Are you sure you want to reset "
                "all Student Details fields "
                "to the default configuration?"
            ),
            parent=self.root
        )


        if not answer:
            return


        self.config = json.loads(
            json.dumps(
                DEFAULT_CONFIG
            )
        )


        for field_id, field_data in DEFAULT_CONFIG[
            "fields"
        ].items():

            if field_id in self.enabled_variables:

                self.enabled_variables[
                    field_id
                ].set(
                    field_data.get(
                        "enabled",
                        False
                    )
                )


            if field_id in self.required_variables:

                self.required_variables[
                    field_id
                ].set(
                    field_data.get(
                        "required",
                        False
                    )
                )


        messagebox.showinfo(
            "Defaults Restored",
            (
                "Default configuration restored.\n\n"
                "Click SAVE CONFIGURATION to save it."
            ),
            parent=self.root
        )


    # ========================================================
    # BACK TO ADMIN CONTROL PANEL
    # ========================================================

    def back(self):

        answer = messagebox.askyesno(
            "Back to Admin Control Panel",
            (
                "Do you want to return to the "
                "Admin Control Panel?"
            ),
            parent=self.root
        )


        if not answer:
            return


        # ----------------------------------------------------
        # Save parent
        # ----------------------------------------------------

        parent = self.parent_window


        # ----------------------------------------------------
        # Unbind mouse wheel
        # ----------------------------------------------------

        try:

            self.canvas.unbind_all(
                "<MouseWheel>"
            )

            self.canvas.unbind_all(
                "<Button-4>"
            )

            self.canvas.unbind_all(
                "<Button-5>"
            )

        except Exception:

            pass


        # ----------------------------------------------------
        # Destroy this window only
        # ----------------------------------------------------

        try:

            if self.root.winfo_exists():

                self.root.destroy()

        except Exception as e:

            print(
                "Could not close Student Details "
                "Configuration:",
                e
            )


        # ----------------------------------------------------
        # Restore Admin Control Panel
        # ----------------------------------------------------

        if parent is not None:

            restore_window(
                parent
            )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.withdraw()


    configuration_window = tk.Toplevel(
        root
    )


    StudentDetailsConfiguration(
        configuration_window,
        parent_window=root
    )


    root.mainloop()
