# ================================================================
# TEACHER RESULT MANAGER PRO
# STANDARD PROFESSIONAL SINGLE FILE
# Android / Pydroid 3 / Windows / Linux / macOS
# ================================================================

import os
import re
import sqlite3
import traceback
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.image import Image

from kivy.graphics import Color, Rectangle, Line


# ================================================================
# ANDROID SAFE IMPORT
# ================================================================

ANDROID_OK = False
autoclass = None
activity = None

try:
    from jnius import autoclass
    from android import activity

    ANDROID_OK = True

except Exception:
    ANDROID_OK = False


# ================================================================
# COLORS
# ================================================================

BLUE = (0.05, 0.32, 0.70, 1)
BLUE2 = (0.03, 0.46, 0.78, 1)

GREEN = (0.08, 0.55, 0.28, 1)
RED = (0.82, 0.10, 0.10, 1)
ORANGE = (0.92, 0.48, 0.06, 1)

GRAY = (0.35, 0.39, 0.45, 1)

DARK = (0.06, 0.08, 0.12, 1)
WHITE = (1, 1, 1, 1)

BG = (0.95, 0.97, 1, 1)
LIGHT = (0.91, 0.94, 0.98, 1)
LIGHT_GRAY = (0.72, 0.76, 0.82, 1)

VERY_LIGHT_BLUE = (0.96, 0.98, 1, 1)


# ================================================================
# DEFAULT OPTIONS
# ================================================================

DEFAULT_CLASSES = [
    "6",
    "7",
    "8",
    "9",
    "10",
    "Other"
]

DEFAULT_SECTIONS = [
    "Science",
    "Business Studies",
    "Humanities",
    "Boy",
    "Girl",
    "Other"
]


# ================================================================
# GLOBAL PATHS
# ================================================================

DB_FILE = "teacher_result_manager.db"
PHOTO_DIR = "student_photos"
PDF_DIR = "Teacher_Result_PDF"


# ================================================================
# HELPERS
# ================================================================

def safe_float(value):

    try:

        if value is None:
            return 0.0

        text = str(value).strip()

        if text == "":
            return 0.0

        return float(text)

    except Exception:

        return 0.0


def blank_or_number(value):

    if value is None:
        return None

    text = str(value).strip()

    if text == "":
        return None

    try:

        number = float(text)

        if number.is_integer():
            return int(number)

        return number

    except Exception:

        return None


def clean_number(value):

    if value is None:
        return ""

    text = str(value).strip()

    if text == "":
        return ""

    try:

        number = float(text)

        if number.is_integer():

            return str(int(number))

        result = "{:.2f}".format(number)

        result = result.rstrip("0").rstrip(".")

        return result

    except Exception:

        return ""


def sanitize_filename(value):

    value = str(value or "student")

    value = re.sub(
        r'[\\/:*?"<>|]+',
        "_",
        value
    )

    value = value.strip()

    if not value:
        value = "student"

    return value


def grade_info(total):

    number = safe_float(total)

    if number >= 80:
        return "A+", 5.00

    if number >= 70:
        return "A", 4.00

    if number >= 60:
        return "A-", 3.50

    if number >= 50:
        return "B", 3.00

    if number >= 40:
        return "C", 2.00

    if number >= 33:
        return "D", 1.00

    return "F", 0.00


def db():

    con = sqlite3.connect(
        DB_FILE,
        timeout=15
    )

    con.execute(
        "PRAGMA busy_timeout=15000"
    )

    con.execute(
        "PRAGMA foreign_keys=ON"
    )

    return con


# ================================================================
# COLORED BOX
# ================================================================

class ColoredBox(BoxLayout):

    def __init__(
        self,
        bg_color=WHITE,
        border_color=LIGHT_GRAY,
        **kwargs
    ):

        self.bg_color = bg_color
        self.border_color = border_color

        super().__init__(**kwargs)

        with self.canvas.before:

            Color(*self.bg_color)

            self.rect = Rectangle(
                pos=self.pos,
                size=self.size
            )

            Color(*self.border_color)

            self.line = Line(
                rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height
                ),
                width=1
            )

        self.bind(
            pos=self.update_canvas,
            size=self.update_canvas
        )

    def update_canvas(self, *args):

        self.rect.pos = self.pos

        self.rect.size = self.size

        self.line.rectangle = (
            self.x,
            self.y,
            self.width,
            self.height
        )


# ================================================================
# TABLE CELL
# ================================================================

class TableCell(Label):

    def __init__(
        self,
        bg_color=WHITE,
        border_color=LIGHT_GRAY,
        **kwargs
    ):

        self.bg_color = bg_color
        self.border_color = border_color

        kwargs.setdefault(
            "color",
            DARK
        )

        kwargs.setdefault(
            "font_size",
            sp(14)
        )

        kwargs.setdefault(
            "halign",
            "center"
        )

        kwargs.setdefault(
            "valign",
            "middle"
        )

        super().__init__(**kwargs)

        with self.canvas.before:

            Color(*self.bg_color)

            self.rect = Rectangle(
                pos=self.pos,
                size=self.size
            )

            Color(*self.border_color)

            self.line = Line(
                rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height
                ),
                width=1
            )

        self.bind(
            pos=self.update_canvas,
            size=self.update_canvas
        )

        self.bind(
            width=self.update_text_size
        )

        Clock.schedule_once(
            lambda dt: self.update_text_size(),
            0
        )

    def update_canvas(self, *args):

        self.rect.pos = self.pos
        self.rect.size = self.size

        self.line.rectangle = (
            self.x,
            self.y,
            self.width,
            self.height
        )

    def update_text_size(self, *args):

        self.text_size = (
            max(1, self.width - dp(8)),
            max(1, self.height - dp(6))
        )


# ================================================================
# LABEL
# ================================================================

def make_label(
    text="",
    size=16,
    color=DARK,
    bold=False,
    halign="left"
):

    label = Label(
        text=str(text),
        font_size=sp(size),
        color=color,
        bold=bold,
        halign=halign,
        valign="middle"
    )

    return label


# ================================================================
# INPUT
# ================================================================

def make_input(
    hint="",
    text="",
    size=17
):

    return TextInput(
        text=str(text or ""),
        hint_text=hint,
        font_size=sp(size),
        foreground_color=DARK,
        hint_text_color=(
            0.35,
            0.38,
            0.43,
            1
        ),
        background_color=WHITE,
        cursor_color=BLUE,
        multiline=False,
        padding=[
            dp(12),
            dp(10)
        ],
        size_hint_y=None,
        height=dp(52)
    )


# ================================================================
# BUTTON
# ================================================================

def make_button(
    text,
    color=BLUE2,
    height=54,
    font=17
):

    return Button(
        text=text,
        font_size=sp(font),
        bold=True,
        color=WHITE,
        background_color=color,
        background_normal="",
        size_hint_y=None,
        height=dp(height)
    )


# ================================================================
# MAIN APP
# ================================================================

class TeacherResultManagerApp(App):

    title = "TEACHER RESULT MANAGER PRO"

    # ============================================================
    # BUILD
    # ============================================================

    def build(self):

        global DB_FILE
        global PHOTO_DIR
        global PDF_DIR

        try:

            base = self.user_data_dir

            os.makedirs(
                base,
                exist_ok=True
            )

            DB_FILE = os.path.join(
                base,
                "teacher_result_manager.db"
            )

            PHOTO_DIR = os.path.join(
                base,
                "student_photos"
            )

            PDF_DIR = os.path.join(
                base,
                "Teacher_Result_PDF"
            )

        except Exception:

            base = os.path.dirname(
                os.path.abspath(__file__)
            )

            DB_FILE = os.path.join(
                base,
                "teacher_result_manager.db"
            )

            PHOTO_DIR = os.path.join(
                base,
                "student_photos"
            )

            PDF_DIR = os.path.join(
                base,
                "Teacher_Result_PDF"
            )

        try:

            os.makedirs(
                PHOTO_DIR,
                exist_ok=True
            )

        except Exception:
            pass

        try:

            os.makedirs(
                PDF_DIR,
                exist_ok=True
            )

        except Exception:
            pass

        try:

            self.init_db()

        except Exception as error:

            Clock.schedule_once(
                lambda dt:
                self.message_popup(
                    "DATABASE ERROR",
                    str(error),
                    RED
                ),
                0
            )

        self.current_student_id = None

        self._android_request_code = 7812

        self._photo_callback = None

        if ANDROID_OK:

            try:

                activity.bind(
                    on_activity_result=
                    self._on_android_result
                )

            except Exception:
                pass

        Window.clearcolor = BG

        return self.dashboard()

    # ============================================================
    # STOP
    # ============================================================

    def on_stop(self):

        if ANDROID_OK:

            try:

                activity.unbind(
                    on_activity_result=
                    self._on_android_result
                )

            except Exception:
                pass

    # ============================================================
    # DATABASE
    # ============================================================

    def init_db(self):

        con = db()

        con.executescript(
            """
            CREATE TABLE IF NOT EXISTS students(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                roll TEXT,

                name TEXT,

                class_name TEXT,

                section TEXT,

                registration_class6 TEXT,

                birth_registration TEXT,

                father_name TEXT,

                mother_name TEXT,

                father_nid TEXT,

                mother_nid TEXT,

                phone TEXT,

                photo_path TEXT

            );


            CREATE TABLE IF NOT EXISTS subjects(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT UNIQUE,

                full_mark REAL DEFAULT 100

            );


            CREATE TABLE IF NOT EXISTS marks(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id INTEGER,

                subject_id INTEGER,

                cq REAL,

                mcq REAL,

                practical REAL,

                total REAL,

                marks REAL,

                UNIQUE(
                    student_id,
                    subject_id
                )

            );


            CREATE TABLE IF NOT EXISTS optional_subjects(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id INTEGER UNIQUE,

                subject_id INTEGER

            );


            CREATE TABLE IF NOT EXISTS settings(

                key TEXT PRIMARY KEY,

                value TEXT

            );

            """
        )

        self.ensure_columns(
            con,
            "students",
            {
                "roll": "TEXT",
                "name": "TEXT",
                "class_name": "TEXT",
                "section": "TEXT",
                "registration_class6": "TEXT",
                "birth_registration": "TEXT",
                "father_name": "TEXT",
                "mother_name": "TEXT",
                "father_nid": "TEXT",
                "mother_nid": "TEXT",
                "phone": "TEXT",
                "photo_path": "TEXT"
            }
        )

        self.ensure_columns(
            con,
            "subjects",
            {
                "full_mark":
                "REAL DEFAULT 100"
            }
        )

        self.ensure_columns(
            con,
            "marks",
            {
                "cq": "REAL",
                "mcq": "REAL",
                "practical": "REAL",
                "total": "REAL",
                "marks": "REAL"
            }
        )

        try:

            con.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS
                idx_student_class_section_roll
                ON students(
                    class_name,
                    section,
                    roll
                )
                """
            )

        except Exception:
            pass

        con.commit()

        con.close()

    # ============================================================
    # ENSURE COLUMNS
    # ============================================================

    def ensure_columns(
        self,
        con,
        table,
        columns
    ):

        try:

            existing = {
                row[1]
                for row in
                con.execute(
                    "PRAGMA table_info({})"
                    .format(table)
                ).fetchall()
            }

        except Exception:

            existing = set()

        for name, definition in columns.items():

            if name not in existing:

                try:

                    con.execute(
                        """
                        ALTER TABLE {}
                        ADD COLUMN {} {}
                        """.format(
                            table,
                            name,
                            definition
                        )
                    )

                except Exception:
                    pass

    # ============================================================
    # DASHBOARD
    # ============================================================

    def dashboard(self):

        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        # HEADER

        header = ColoredBox(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(2),
            size_hint_y=None,
            height=dp(100),
            bg_color=BLUE,
            border_color=BLUE
        )

        title = make_label(
            "TEACHER RESULT MANAGER PRO",
            24,
            WHITE,
            True,
            "center"
        )

        subtitle = make_label(
            "STANDARD PROFESSIONAL • ANDROID / PYDROID 3 / DESKTOP",
            14,
            WHITE,
            False,
            "center"
        )

        header.add_widget(title)
        header.add_widget(subtitle)

        root.add_widget(header)

        # MAIN BUTTONS

        scroll = ScrollView()

        box = GridLayout(
            cols=1,
            spacing=dp(11),
            padding=dp(8),
            size_hint_y=None
        )

        box.bind(
            minimum_height=
            box.setter("height")
        )

        buttons = [

            (
                "STUDENTS",
                BLUE2,
                self.student_list_popup
            ),

            (
                "ADD STUDENT",
                GREEN,
                lambda *a:
                self.student_form_popup()
            ),

            (
                "SUBJECT MANAGEMENT",
                ORANGE,
                self.subject_popup
            ),

            (
                "MARKS ENTRY",
                BLUE2,
                self.marks_popup
            ),

            (
                "OPTIONAL SUBJECT",
                ORANGE,
                self.optional_popup
            ),

            (
                "RESULT / GPA / MERIT",
                GREEN,
                self.result_popup
            ),

            (
                "EXIT",
                RED,
                self.confirm_exit
            )
        ]

        for text, color, callback in buttons:

            button = make_button(
                text,
                color,
                64,
                19
            )

            button.bind(
                on_release=callback
            )

            box.add_widget(button)

        scroll.add_widget(box)

        root.add_widget(scroll)

        return root

    # ============================================================
    # MESSAGE POPUP
    # ============================================================

    def message_popup(
        self,
        title,
        message,
        color=BLUE
    ):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(12)
        )

        scroll = ScrollView()

        label = Label(
            text=str(message),
            font_size=sp(17),
            color=DARK,
            halign="left",
            valign="top",
            size_hint_y=None
        )

        label.bind(
            texture_size=lambda instance, size:
            setattr(
                instance,
                "height",
                max(
                    dp(75),
                    size[1] + dp(20)
                )
            )
        )

        scroll.add_widget(label)

        content.add_widget(scroll)

        close = make_button(
            "OK",
            color,
            56,
            18
        )

        content.add_widget(close)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.92, 0.48),
            auto_dismiss=False
        )

        close.bind(
            on_release=popup.dismiss
        )

        popup.open()

        return popup

    # ============================================================
    # CUSTOM OTHER VALUE
    # ============================================================

    def ask_custom_value(
        self,
        title,
        spinner,
        is_class=True
    ):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(10)
        )

        content.add_widget(
            make_label(
                "Enter the actual value:",
                17,
                DARK,
                True
            )
        )

        field = make_input(
            "Type here",
            "",
            17
        )

        content.add_widget(field)

        buttons = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(56)
        )

        use_button = make_button(
            "USE",
            GREEN,
            56,
            17
        )

        cancel_button = make_button(
            "CANCEL",
            GRAY,
            56,
            17
        )

        buttons.add_widget(use_button)
        buttons.add_widget(cancel_button)

        content.add_widget(buttons)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.90, 0.38),
            auto_dismiss=False
        )

        def use_value(*args):

            value = field.text.strip()

            if not value:

                self.message_popup(
                    "INPUT",
                    "Please type a value.",
                    ORANGE
                )

                return

            values = list(
                spinner.values
            )

            if value not in values:

                values.insert(
                    max(
                        0,
                        len(values) - 1
                    ),
                    value
                )

            spinner.values = values

            spinner.text = value

            popup.dismiss()

        use_button.bind(
            on_release=use_value
        )

        cancel_button.bind(
            on_release=popup.dismiss
        )

        popup.open()

    # ============================================================
    # CLASSES
    # ============================================================

    def get_classes(self):

        values = list(
            DEFAULT_CLASSES
        )

        try:

            con = db()

            rows = con.execute(
                """
                SELECT DISTINCT class_name
                FROM students
                WHERE class_name IS NOT NULL
                AND TRIM(class_name) <> ''
                ORDER BY class_name
                """
            ).fetchall()

            con.close()

            for row in rows:

                value = row[0]

                if value and value not in values:

                    values.insert(
                        max(
                            0,
                            len(values) - 1
                        ),
                        value
                    )

        except Exception:
            pass

        return values

    # ============================================================
    # SECTIONS
    # ============================================================

    def get_sections(self):

        values = list(
            DEFAULT_SECTIONS
        )

        try:

            con = db()

            rows = con.execute(
                """
                SELECT DISTINCT section
                FROM students
                WHERE section IS NOT NULL
                AND TRIM(section) <> ''
                ORDER BY section
                """
            ).fetchall()

            con.close()

            for row in rows:

                value = row[0]

                if value and value not in values:

                    values.insert(
                        max(
                            0,
                            len(values) - 1
                        ),
                        value
                    )

        except Exception:
            pass

        return values

    # ============================================================
    # STUDENT LOOKUP
    # ============================================================

    def get_student_by_class_section_roll(
        self,
        cls,
        section,
        roll
    ):

        try:

            con = db()

            row = con.execute(
                """
                SELECT *
                FROM students
                WHERE class_name=?
                AND section=?
                AND roll=?
                LIMIT 1
                """,
                (
                    cls,
                    section,
                    roll
                )
            ).fetchone()

            con.close()

            return row

        except Exception:

            return None

    # ============================================================
    # STUDENT FORM
    # ============================================================

    def student_form_popup(
        self,
        student_id=None
    ):

        try:

            student = None

            if student_id:

                con = db()

                student = con.execute(
                    """
                    SELECT *
                    FROM students
                    WHERE id=?
                    """,
                    (student_id,)
                ).fetchone()

                con.close()

        except Exception as error:

            self.message_popup(
                "ERROR",
                str(error),
                RED
            )

            return

        content = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        scroll = ScrollView()

        form = GridLayout(
            cols=1,
            spacing=dp(8),
            padding=dp(5),
            size_hint_y=None
        )

        form.bind(
            minimum_height=
            form.setter("height")
        )

        # --------------------------------------------------------
        # PHOTO FIRST
        # --------------------------------------------------------

        form.add_widget(
            make_label(
                "PHOTO",
                19,
                DARK,
                True
            )
        )

        photo_box = ColoredBox(
            orientation="vertical",
            padding=dp(8),
            spacing=dp(6),
            size_hint_y=None,
            height=dp(245),
            bg_color=WHITE,
            border_color=LIGHT_GRAY
        )

        preview = Image(
            source="",
            allow_stretch=True,
            keep_ratio=True,
            size_hint_y=None,
            height=dp(175)
        )

        photo_name = make_label(
            "No photo selected",
            14,
            GRAY,
            False,
            "center"
        )

        photo_button = make_button(
            "SELECT PHOTO",
            BLUE2,
            50,
            17
        )

        photo_box.add_widget(preview)
        photo_box.add_widget(photo_name)
        photo_box.add_widget(photo_button)

        form.add_widget(photo_box)

        # --------------------------------------------------------
        # FIELDS
        # --------------------------------------------------------

        fields = {}

        specifications = [

            (
                "roll",
                "Roll"
            ),

            (
                "name",
                "Student Name"
            ),

            (
                "class_name",
                "Class"
            ),

            (
                "section",
                "Section"
            ),

            (
                "registration_class6",
                "Registration Number"
            ),

            (
                "birth_registration",
                "Birth Registration"
            ),

            (
                "father_name",
                "Father's Name"
            ),

            (
                "mother_name",
                "Mother's Name"
            ),

            (
                "father_nid",
                "Father's NID"
            ),

            (
                "mother_nid",
                "Mother's NID"
            ),

            (
                "phone",
                "Phone"
            )
        ]

        index_map = {

            "roll": 1,
            "name": 2,
            "registration_class6": 5,
            "birth_registration": 6,
            "father_name": 7,
            "mother_name": 8,
            "father_nid": 9,
            "mother_nid": 10,
            "phone": 11
        }

        for key, label_text in specifications:

            form.add_widget(
                make_label(
                    label_text,
                    17,
                    DARK,
                    True
                )
            )

            if key == "class_name":

                current = (
                    student[3]
                    if student
                    else self.get_classes()[0]
                )

                values = self.get_classes()

                if current not in values:
                    values.insert(
                        max(
                            0,
                            len(values) - 1
                        ),
                        current
                    )

                widget = Spinner(
                    text=current,
                    values=values,
                    font_size=sp(17),
                    color=DARK,
                    background_color=WHITE,
                    size_hint_y=None,
                    height=dp(54)
                )

            elif key == "section":

                current = (
                    student[4]
                    if student
                    else self.get_sections()[0]
                )

                values = self.get_sections()

                if current not in values:
                    values.insert(
                        max(
                            0,
                            len(values) - 1
                        ),
                        current
                    )

                widget = Spinner(
                    text=current,
                    values=values,
                    font_size=sp(17),
                    color=DARK,
                    background_color=WHITE,
                    size_hint_y=None,
                    height=dp(54)
                )

            else:

                index = index_map[key]

                old_text = (
                    student[index]
                    if student
                    else ""
                )

                widget = make_input(
                    label_text,
                    old_text,
                    17
                )

            fields[key] = widget

            form.add_widget(widget)

        form.add_widget(
            make_label(
                "English and Bangla text can be entered.",
                14,
                GRAY
            )
        )

        save = make_button(
            "UPDATE STUDENT"
            if student_id
            else "SAVE STUDENT",
            GREEN,
            60,
            18
        )

        close = make_button(
            "CLOSE",
            GRAY,
            60,
            18
        )

        form.add_widget(save)
        form.add_widget(close)

        scroll.add_widget(form)

        content.add_widget(scroll)

        popup = Popup(
            title=
            "EDIT STUDENT"
            if student_id
            else "ADD STUDENT",
            content=content,
            size_hint=(0.97, 0.96),
            auto_dismiss=False
        )

        photo_state = {
            "path":
            student[12]
            if student
            else ""
        }

        if (
            photo_state["path"]
            and
            os.path.exists(
                photo_state["path"]
            )
        ):

            preview.source = (
                photo_state["path"]
            )

            preview.reload()

            photo_name.text = os.path.basename(
                photo_state["path"]
            )

        # --------------------------------------------------------
        # OTHER CLASS
        # --------------------------------------------------------

        def class_other(instance, text):

            if text == "Other":

                self.ask_custom_value(
                    "ENTER CLASS",
                    instance,
                    True
                )

        # --------------------------------------------------------
        # OTHER SECTION
        # --------------------------------------------------------

        def section_other(instance, text):

            if text == "Other":

                self.ask_custom_value(
                    "ENTER SECTION",
                    instance,
                    False
                )

        fields["class_name"].bind(
            text=class_other
        )

        fields["section"].bind(
            text=section_other
        )

        # --------------------------------------------------------
        # PHOTO SELECT
        # --------------------------------------------------------

        def select_photo(*args):

            self._photo_callback = (
                lambda path:
                self.set_form_photo(
                    path,
                    preview,
                    photo_name,
                    photo_state
                )
            )

            if ANDROID_OK:

                try:

                    Intent = autoclass(
                        "android.content.Intent"
                    )

                    intent = Intent(
                        Intent.ACTION_OPEN_DOCUMENT
                    )

                    intent.setType(
                        "image/*"
                    )

                    intent.addCategory(
                        Intent.CATEGORY_OPENABLE
                    )

                    intent.addFlags(
                        Intent.FLAG_GRANT_READ_URI_PERMISSION
                    )

                    activity.startActivityForResult(
                        intent,
                        self._android_request_code
                    )

                    return

                except Exception:
                    pass

            self.desktop_photo_picker(
                self._photo_callback
            )

        photo_button.bind(
            on_release=select_photo
        )

        # --------------------------------------------------------
        # SAVE STUDENT
        # --------------------------------------------------------

        def save_student(*args):

            roll = fields[
                "roll"
            ].text.strip()

            name = fields[
                "name"
            ].text.strip()

            cls = fields[
                "class_name"
            ].text.strip()

            section = fields[
                "section"
            ].text.strip()

            if not roll:

                self.message_popup(
                    "STUDENT",
                    "Roll is required.",
                    ORANGE
                )

                return

            if not name:

                self.message_popup(
                    "STUDENT",
                    "Student Name is required.",
                    ORANGE
                )

                return

            if not cls:

                self.message_popup(
                    "STUDENT",
                    "Class is required.",
                    ORANGE
                )

                return

            if not section:

                self.message_popup(
                    "STUDENT",
                    "Section is required.",
                    ORANGE
                )

                return

            values = (

                roll,

                name,

                cls,

                section,

                fields[
                    "registration_class6"
                ].text.strip(),

                fields[
                    "birth_registration"
                ].text.strip(),

                fields[
                    "father_name"
                ].text.strip(),

                fields[
                    "mother_name"
                ].text.strip(),

                fields[
                    "father_nid"
                ].text.strip(),

                fields[
                    "mother_nid"
                ].text.strip(),

                fields[
                    "phone"
                ].text.strip(),

                photo_state["path"]
            )

            try:

                con = db()

                if student_id:

                    con.execute(
                        """
                        UPDATE students
                        SET
                            roll=?,
                            name=?,
                            class_name=?,
                            section=?,
                            registration_class6=?,
                            birth_registration=?,
                            father_name=?,
                            mother_name=?,
                            father_nid=?,
                            mother_nid=?,
                            phone=?,
                            photo_path=?
                        WHERE id=?
                        """,
                        values + (
                            student_id,
                        )
                    )

                else:

                    con.execute(
                        """
                        INSERT INTO students(
                            roll,
                            name,
                            class_name,
                            section,
                            registration_class6,
                            birth_registration,
                            father_name,
                            mother_name,
                            father_nid,
                            mother_nid,
                            phone,
                            photo_path
                        )
                        VALUES(
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?
                        )
                        """,
                        values
                    )

                con.commit()

                con.close()

                popup.dismiss()

                self.message_popup(
                    "SUCCESS",
                    "Student saved successfully.",
                    GREEN
                )

            except sqlite3.IntegrityError:

                self.message_popup(
                    "STUDENT",
                    "This Class + Section + Roll already exists.",
                    RED
                )

            except Exception as error:

                self.message_popup(
                    "STUDENT ERROR",
                    str(error),
                    RED
                )

        save.bind(
            on_release=save_student
        )

        close.bind(
            on_release=popup.dismiss
        )

        popup.open()

    # ============================================================
    # SET FORM PHOTO
    # ============================================================

    def set_form_photo(
        self,
        path,
        preview,
        label,
        state
    ):

        if (
            path
            and
            os.path.exists(path)
        ):

            state["path"] = path

            preview.source = path

            preview.reload()

            label.text = os.path.basename(
                path
            )

    # ============================================================
    # DESKTOP PHOTO PICKER
    # ============================================================

    def desktop_photo_picker(
        self,
        callback
    ):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(8),
            spacing=dp(8)
        )

        try:

            from kivy.uix.filechooser import (
                FileChooserListView
            )

            chooser = FileChooserListView(
                path=os.path.expanduser("~"),
                filters=[
                    "*.png",
                    "*.jpg",
                    "*.jpeg",
                    "*.webp"
                ]
            )

            content.add_widget(
                chooser
            )

            buttons = BoxLayout(
                spacing=dp(8),
                size_hint_y=None,
                height=dp(56)
            )

            select = make_button(
                "SELECT",
                GREEN,
                56,
                17
            )

            cancel = make_button(
                "CANCEL",
                GRAY,
                56,
                17
            )

            buttons.add_widget(select)
            buttons.add_widget(cancel)

            content.add_widget(buttons)

            popup = Popup(
                title="SELECT PHOTO",
                content=content,
                size_hint=(0.96, 0.90),
                auto_dismiss=False
            )

            def choose(*args):

                if not chooser.selection:

                    self.message_popup(
                        "PHOTO",
                        "Please select an image.",
                        ORANGE
                    )

                    return

                try:

                    callback(
                        chooser.selection[0]
                    )

                    popup.dismiss()

                except Exception as error:

                    self.message_popup(
                        "PHOTO ERROR",
                        str(error),
                        RED
                    )

            select.bind(
                on_release=choose
            )

            cancel.bind(
                on_release=popup.dismiss
            )

            popup.open()

        except Exception as error:

            self.message_popup(
                "PHOTO",
                str(error),
                RED
            )

    # ============================================================
    # ANDROID RESULT
    # ============================================================

    def _on_android_result(
        self,
        request_code,
        result_code,
        intent
    ):

        if request_code != getattr(
            self,
            "_android_request_code",
            7812
        ):

            return

        try:

            if result_code != -1:

                return

            if intent is None:

                return

            uri = intent.getData()

            if uri is None:

                return

            path = self.copy_android_uri(
                uri
            )

            callback = getattr(
                self,
                "_photo_callback",
                None
            )

            if callback and path:

                Clock.schedule_once(
                    lambda dt:
                    callback(path),
                    0
                )

        except Exception as error:

            Clock.schedule_once(
                lambda dt:
                self.message_popup(
                    "PHOTO ERROR",
                    str(error),
                    RED
                ),
                0
            )

    # ============================================================
    # COPY ANDROID URI
    # ============================================================

    def copy_android_uri(
        self,
        uri
    ):

        try:

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            resolver = (
                PythonActivity
                .mActivity
                .getContentResolver()
            )

            stream = resolver.openInputStream(
                uri
            )

            if stream is None:

                return ""

            filename = (
                "student_"
                +
                datetime.now().strftime(
                    "%Y%m%d_%H%M%S_%f"
                )
                +
                ".jpg"
            )

            destination = os.path.join(
                PHOTO_DIR,
                filename
            )

            output = open(
                destination,
                "wb"
            )

            try:

                buffer = bytearray(
                    8192
                )

                while True:

                    count = stream.read(
                        buffer
                    )

                    if (
                        count is None
                        or
                        count <= 0
                    ):

                        break

                    output.write(
                        bytes(
                            buffer[:count]
                        )
                    )

            finally:

                output.close()

                try:
                    stream.close()
                except Exception:
                    pass

            return destination

        except Exception:

            return ""

    # ============================================================
    # STUDENT LIST
    # ============================================================

    def student_list_popup(
        self,
        *args
    ):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        search = GridLayout(
            cols=4,
            spacing=dp(7),
            size_hint_y=None,
            height=dp(55)
        )

        cls = Spinner(
            text=self.get_classes()[0],
            values=self.get_classes(),
            font_size=sp(17),
            color=DARK,
            background_color=WHITE,
            size_hint_y=None,
            height=dp(54)
        )

        section = Spinner(
            text=self.get_sections()[0],
            values=self.get_sections(),
            font_size=sp(17),
            color=DARK,
            background_color=WHITE,
            size_hint_y=None,
            height=dp(54)
        )

        roll = make_input(
            "Roll",
            "",
            16
        )

        search_button = make_button(
            "SEARCH",
            BLUE2,
            54,
            16
        )

        search.add_widget(cls)
        search.add_widget(section)
        search.add_widget(roll)
        search.add_widget(search_button)

        content.add_widget(search)

        scroll = ScrollView()

        list_box = GridLayout(
            cols=1,
            spacing=dp(9),
            padding=dp(4),
            size_hint_y=None
        )

        list_box.bind(
            minimum_height=
            list_box.setter("height")
        )

        scroll.add_widget(
            list_box
        )

        content.add_widget(
            scroll
        )

        close = make_button(
            "CLOSE",
            GRAY,
            56,
            17
        )

        content.add_widget(
            close
        )

        popup = Popup(
            title="STUDENT LIST",
            content=content,
            size_hint=(0.98, 0.96),
            auto_dismiss=False
        )

        def refresh(*args):

            list_box.clear_widgets()

            try:

                con = db()

                if roll.text.strip():

                    rows = con.execute(
                        """
                        SELECT *
                        FROM students
                        WHERE class_name=?
                        AND section=?
                        AND roll=?
                        ORDER BY name
                        """,
                        (
                            cls.text.strip(),
                            section.text.strip(),
                            roll.text.strip()
                        )
                    ).fetchall()

                else:

                    rows = con.execute(
                        """
                        SELECT *
                        FROM students
                        WHERE class_name=?
                        AND section=?
                        ORDER BY
                            CASE
                                WHEN roll GLOB '[0-9]*'
                                THEN CAST(roll AS INTEGER)
                                ELSE 999999
                            END,
                            roll,
                            name
                        """,
                        (
                            cls.text.strip(),
                            section.text.strip()
                        )
                    ).fetchall()

                con.close()

                if not rows:

                    list_box.add_widget(
                        make_label(
                            "No student found.",
                            19,
                            RED,
                            True,
                            "center"
                        )
                    )

                    return

                for student in rows:

                    list_box.add_widget(
                        self.make_student_card(
                            student,
                            popup
                        )
                    )

            except Exception as error:

                list_box.add_widget(
                    make_label(
                        str(error),
                        17,
                        RED
                    )
                )

        cls.bind(
            text=lambda instance, text:
            self.ask_custom_value(
                "ENTER CLASS",
                instance,
                True
            )
            if text == "Other"
            else None
        )

        section.bind(
            text=lambda instance, text:
            self.ask_custom_value(
                "ENTER SECTION",
                instance,
                False
            )
            if text == "Other"
            else None
        )

        search_button.bind(
            on_release=refresh
        )

        close.bind(
            on_release=popup.dismiss
        )

        popup.open()

        refresh()

    # ============================================================
    # STUDENT CARD
    # ============================================================

    def make_student_card(
        self,
        student,
        parent_popup
    ):

        card = ColoredBox(
            orientation="horizontal",
            padding=dp(8),
            spacing=dp(9),
            size_hint_y=None,
            height=dp(155),
            bg_color=WHITE,
            border_color=LIGHT_GRAY
        )

        # PHOTO

        photo_source = ""

        if (
            student[12]
            and
            os.path.exists(
                student[12]
            )
        ):

            photo_source = student[12]

        photo = Image(
            source=photo_source,
            size_hint_x=None,
            width=dp(105),
            allow_stretch=True,
            keep_ratio=True
        )

        card.add_widget(
            photo
        )

        # INFORMATION

        info = BoxLayout(
            orientation="vertical",
            spacing=dp(2)
        )

        info.add_widget(
            make_label(
                student[2] or "",
                19,
                DARK,
                True
            )
        )

        info.add_widget(
            make_label(
                "Class: {}   Section: {}   Roll: {}"
                .format(
                    student[3] or "",
                    student[4] or "",
                    student[1] or ""
                ),
                16,
                DARK,
                True
            )
        )

        info.add_widget(
            make_label(
                "Father's Name: {}"
                .format(
                    student[7] or ""
                ),
                15,
                DARK
            )
        )

        info.add_widget(
            make_label(
                "Mother's Name: {}"
                .format(
                    student[8] or ""
                ),
                15,
                DARK
            )
        )

        card.add_widget(
            info
        )

        # BUTTONS

        buttons = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            size_hint_x=None,
            width=dp(125)
        )

        profile = make_button(
            "PROFILE",
            BLUE2,
            43,
            15
        )

        edit = make_button(
            "EDIT",
            GREEN,
            43,
            15
        )

        delete = make_button(
            "DELETE",
            RED,
            43,
            15
        )

        buttons.add_widget(profile)
        buttons.add_widget(edit)
        buttons.add_widget(delete)

        card.add_widget(
            buttons
        )

        profile.bind(
            on_release=lambda *a:
            self.show_profile(
                student[0]
            )
        )

        edit.bind(
            on_release=lambda *a:
            self.student_form_popup(
                student[0]
            )
        )

        delete.bind(
            on_release=lambda *a:
            self.confirm_delete_student(
                student[0],
                parent_popup
            )
        )

        return card

    # ============================================================
    # DELETE STUDENT
    # ============================================================

    def confirm_delete_student(
        self,
        student_id,
        parent_popup
    ):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(12)
        )

        content.add_widget(
            make_label(
                "Delete this student and all related marks?",
                18,
                DARK,
                True,
                "center"
            )
        )

        buttons = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(56)
        )

        yes = make_button(
            "DELETE",
            RED,
            56,
            17
        )

        no = make_button(
            "CANCEL",
            GRAY,
            56,
            17
        )

        buttons.add_widget(yes)
        buttons.add_widget(no)

        content.add_widget(buttons)

        popup = Popup(
            title="DELETE STUDENT",
            content=content,
            size_hint=(0.90, 0.34),
            auto_dismiss=False
        )

        def delete_now(*args):

            try:

                con = db()

                con.execute(
                    """
                    DELETE FROM marks
                    WHERE student_id=?
                    """,
                    (student_id,)
                )

                con.execute(
                    """
                    DELETE FROM optional_subjects
                    WHERE student_id=?
                    """,
                    (student_id,)
                )

                con.execute(
                    """
                    DELETE FROM students
                    WHERE id=?
                    """,
                    (student_id,)
                )

                con.commit()

                con.close()

                popup.dismiss()

                try:
                    parent_popup.dismiss()
                except Exception:
                    pass

                self.message_popup(
                    "SUCCESS",
                    "Student deleted successfully.",
                    GREEN
                )

            except Exception as error:

                self.message_popup(
                    "DELETE ERROR",
                    str(error),
                    RED
                )

        yes.bind(
            on_release=delete_now
        )

        no.bind(
            on_release=popup.dismiss
        )

        popup.open()

    # ============================================================
    # PROFILE
    # ============================================================

    def show_profile(
        self,
        student_id
    ):

        try:

            con = db()

            student = con.execute(
                """
                SELECT *
                FROM students
                WHERE id=?
                """,
                (student_id,)
            ).fetchone()

            con.close()

            if not student:

                self.message_popup(
                    "PROFILE",
                    "Student not found.",
                    RED
                )

                return

        except Exception as error:

            self.message_popup(
                "PROFILE ERROR",
                str(error),
                RED
            )

            return

        # MAIN PROFILE CONTENT
        content = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        # --------------------------------------------------------
        # TOP
        # --------------------------------------------------------

        top = ColoredBox(
            orientation="horizontal",
            padding=dp(10),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(205),
            bg_color=WHITE,
            border_color=LIGHT_GRAY
        )

        photo_source = ""

        if (
            student[12]
            and
            os.path.exists(
                student[12]
            )
        ):

            photo_source = student[12]

        profile_photo = Image(
            source=photo_source,
            size_hint_x=None,
            width=dp(165),
            allow_stretch=True,
            keep_ratio=True
        )

        top.add_widget(
            profile_photo
        )

        top_info = BoxLayout(
            orientation="vertical",
            spacing=dp(4)
        )

        top_info.add_widget(
            make_label(
                student[2] or "",
                23,
                DARK,
                True
            )
        )

        top_info.add_widget(
            make_label(
                "Class: {}"
                .format(
                    student[3] or ""
                ),
                17,
                DARK,
                True
            )
        )

        top_info.add_widget(
            make_label(
                "Section: {}"
                .format(
                    student[4] or ""
                ),
                17,
                DARK,
                True
            )
        )

        top_info.add_widget(
            make_label(
                "Roll: {}"
                .format(
                    student[1] or ""
                ),
                17,
                DARK,
                True
            )
        )

        top.add_widget(
            top_info
        )

        content.add_widget(
            top
        )

        # --------------------------------------------------------
        # DETAILS
        # --------------------------------------------------------

        scroll = ScrollView()

        details_box = GridLayout(
            cols=1,
            spacing=dp(6),
            padding=dp(4),
            size_hint_y=None
        )

        details_box.bind(
            minimum_height=
            details_box.setter(
                "height"
            )
        )

        details = [

            (
                "Registration Number",
                student[5]
            ),

            (
                "Birth Registration",
                student[6]
            ),

            (
                "Father's Name",
                student[7]
            ),

            (
                "Mother's Name",
                student[8]
            ),

            (
                "Father's NID",
                student[9]
            ),

            (
                "Mother's NID",
                student[10]
            ),

            (
                "Phone",
                student[11]
            )
        ]

        for label_text, value in details:

            row = ColoredBox(
                orientation="horizontal",
                padding=dp(8),
                spacing=dp(5),
                size_hint_y=None,
                height=dp(58),
                bg_color=WHITE,
                border_color=LIGHT_GRAY
            )

            label = make_label(
                label_text,
                16,
                DARK,
                True
            )

            value_label = make_label(
                str(value or ""),
                16,
                DARK,
                False
            )

            row.add_widget(
                label
            )

            row.add_widget(
                value_label
            )

            details_box.add_widget(
                row
            )

        scroll.add_widget(
            details_box
        )

        content.add_widget(
            scroll
        )

        # --------------------------------------------------------
        # CLOSE
        # --------------------------------------------------------

        close = make_button(
            "CLOSE",
            GRAY,
            56,
            18
        )

        content.add_widget(
            close
        )

        popup = Popup(
            title="STUDENT PROFILE",
            content=content,
            size_hint=(0.97, 0.95),
            auto_dismiss=False
        )

        close.bind(
            on_release=popup.dismiss
        )

        # Photo preview on touch
        def photo_touch(
            instance,
            touch
        ):

            if (
                instance.collide_point(
                    *touch.pos
                )
                and
                touch.button == "left"
            ):

                self.photo_preview(
                    student[12]
                )

                return True

            return False

        profile_photo.bind(
            on_touch_down=photo_touch
        )

        popup.open()

    # ============================================================
    # PHOTO PREVIEW
    # ============================================================

    def photo_preview(
        self,
        path
    ):

        if (
            not path
            or
            not os.path.exists(path)
        ):

            self.message_popup(
                "PHOTO",
                "No photo available.",
                ORANGE
            )

            return

        content = BoxLayout(
            orientation="vertical",
            padding=dp(8),
            spacing=dp(8)
        )

        image = Image(
            source=path,
            allow_stretch=True,
            keep_ratio=True
        )

        content.add_widget(
            image
        )

        close = make_button(
            "CLOSE",
            GRAY,
            56,
            18
        )

        content.add_widget(
            close
        )

        popup = Popup(
            title="STUDENT PHOTO",
            content=content,
            size_hint=(0.92, 0.90),
            auto_dismiss=False
        )

        close.bind(
            on_release=popup.dismiss
        )

        popup.open()

    # ============================================================
    # SUBJECT MANAGEMENT
    # ============================================================

    def subject_popup(
        self,
        *args
    ):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        add_row = BoxLayout(
            spacing=dp(7),
            size_hint_y=None,
            height=dp(55)
        )

        subject_input = make_input(
            "Subject Name",
            "",
            17
        )

        add_button = make_button(
            "ADD SUBJECT",
            GREEN,
            55,
            16
        )

        add_row.add_widget(
            subject_input
        )

        add_row.add_widget(
            add_button
        )

        content.add_widget(
            add_row
        )

        scroll = ScrollView()

        subject_box = GridLayout(
            cols=1,
            spacing=dp(6),
            padding=dp(4),
            size_hint_y=None
        )

        subject_box.bind(
            minimum_height=
            subject_box.setter("height")
        )

        scroll.add_widget(
            subject_box
        )

        content.add_widget(
            scroll
        )

        close = make_button(
            "CLOSE",
            GRAY,
            56,
            18
        )

        content.add_widget(
            close
        )

        popup = Popup(
            title="SUBJECT MANAGEMENT",
            content=content,
            size_hint=(0.95, 0.90),
            auto_dismiss=False
        )

        def refresh():

            subject_box.clear_widgets()

            try:

                con = db()

                rows = con.execute(
                    """
                    SELECT id,name,full_mark
                    FROM subjects
                    ORDER BY name
                    """
                ).fetchall()

                con.close()

                if not rows:

                    subject_box.add_widget(
                        make_label(
                            "No subjects yet.",
                            18,
                            GRAY,
                            False,
                            "center"
                        )
                    )

                    return

                for sid, name, full_mark in rows:

                    row = ColoredBox(
                        orientation="horizontal",
                        padding=dp(7),
                        spacing=dp(7),
                        size_hint_y=None,
                        height=dp(60),
                        bg_color=WHITE,
                        border_color=LIGHT_GRAY
                    )

                    row.add_widget(
                        make_label(
                            name,
                            17,
                            DARK,
                            True
                        )
                    )

                    row.add_widget(
                        make_label(
                            "Full Mark: {}"
                            .format(
                                clean_number(
                                    full_mark
                                )
                                or "100"
                            ),
                            15,
                            DARK
                        )
                    )

                    delete = make_button(
                        "DELETE",
                        RED,
                        48,
                        15
                    )

                    row.add_widget(
                        delete
                    )

                    delete.bind(
                        on_release=lambda *a,
                        subject_id=sid:
                        self.delete_subject(
                            subject_id,
                            popup,
                            refresh
                        )
                    )

                    subject_box.add_widget(
                        row
                    )

            except Exception as error:

                subject_box.add_widget(
                    make_label(
                        str(error),
                        17,
                        RED
                    )
                )

        def add_subject(*args):

            name = subject_input.text.strip()

            if not name:

                self.message_popup(
                    "SUBJECT",
                    "Enter subject name.",
                    ORANGE
                )

                return

            try:

                con = db()

                con.execute(
                    """
                    INSERT INTO subjects(
                        name,
                        full_mark
                    )
                    VALUES(
                        ?,
                        100
                    )
                    """,
                    (name,)
                )

                con.commit()

                con.close()

                subject_input.text = ""

                refresh()

            except sqlite3.IntegrityError:

                self.message_popup(
                    "SUBJECT",
                    "This subject already exists.",
                    ORANGE
                )

            except Exception as error:

                self.message_popup(
                    "SUBJECT ERROR",
                    str(error),
                    RED
                )

        add_button.bind(
            on_release=add_subject
        )

        close.bind(
            on_release=popup.dismiss
        )

        popup.open()

        refresh()

    # ============================================================
    # DELETE SUBJECT
    # ============================================================

    def delete_subject(
        self,
        subject_id,
        parent_popup,
        refresh
    ):

        try:

            con = db()

            con.execute(
                """
                DELETE FROM marks
                WHERE subject_id=?
                """,
                (subject_id,)
            )

            con.execute(
                """
                DELETE FROM optional_subjects
                WHERE subject_id=?
                """,
                (subject_id,)
            )

            con.execute(
                """
                DELETE FROM subjects
                WHERE id=?
                """,
                (subject_id,)
            )

            con.commit()

            con.close()

            refresh()

        except Exception as error:

            self.message_popup(
                "SUBJECT ERROR",
                str(error),
                RED
            )

    # ============================================================
    # OPTIONAL SUBJECT
    # ============================================================

    def optional_popup(
        self,
        *args
    ):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        # --------------------------------------------------------
        # CLASS / SECTION
        # --------------------------------------------------------

        search = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(120)
        )

        classes = self.get_classes()

        sections = self.get_sections()

        cls = Spinner(
            text=classes[0]
            if classes
            else "6",
            values=classes,
            font_size=sp(17),
            color=DARK,
            background_color=WHITE,
            size_hint_y=None,
            height=dp(54)
        )

        sec = Spinner(
            text=sections[0]
            if sections
            else "Science",
            values=sections,
            font_size=sp(17),
            color=DARK,
            background_color=WHITE,
            size_hint_y=None,
            height=dp(54)
        )

        search.add_widget(
            make_label(
                "Class",
                17,
                DARK,
                True
            )
        )

        search.add_widget(cls)

        search.add_widget(
            make_label(
                "Section",
                17,
                DARK,
                True
            )
        )

        search.add_widget(sec)

        content.add_widget(
            search
        )

        # --------------------------------------------------------
        # ROLL
        # --------------------------------------------------------

        roll_row = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(56)
        )

        roll = make_input(
            "Student Roll",
            "",
            17
        )

        open_student = make_button(
            "OPEN STUDENT",
            BLUE2,
            56,
            16
        )

        roll_row.add_widget(
            roll
        )

        roll_row.add_widget(
            open_student
        )

        content.add_widget(
            roll_row
        )

        # --------------------------------------------------------
        # STUDENT INFORMATION
        # --------------------------------------------------------

        info_box = ColoredBox(
            orientation="vertical",
            padding=dp(8),
            size_hint_y=None,
            height=dp(88),
            bg_color=WHITE,
            border_color=LIGHT_GRAY
        )

        info_label = make_label(
            "Enter Class + Section + Roll",
            16,
            DARK,
            True,
            "center"
        )

        info_box.add_widget(
            info_label
        )

        content.add_widget(
            info_box
        )

        # --------------------------------------------------------
        # SUBJECT
        # --------------------------------------------------------

        content.add_widget(
            make_label(
                "Optional Subject",
                17,
                DARK,
                True
            )
        )

        subject_spinner = Spinner(
            text="SELECT SUBJECT",
            values=[],
            font_size=sp(17),
            color=DARK,
            background_color=WHITE,
            size_hint_y=None,
            height=dp(56)
        )

        content.add_widget(
            subject_spinner
        )

        # --------------------------------------------------------
        # BUTTONS
        # --------------------------------------------------------

        buttons = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(120)
        )

        set_button = make_button(
            "SET OPTIONAL",
            GREEN,
            54,
            16
        )

        clear_button = make_button(
            "CLEAR OPTIONAL",
            RED,
            54,
            16
        )

        close_button = make_button(
            "CLOSE",
            GRAY,
            54,
            16
        )

        buttons.add_widget(
            set_button
        )

        buttons.add_widget(
            clear_button
        )

        buttons.add_widget(
            close_button
        )

        content.add_widget(
            buttons
        )

        popup = Popup(
            title="OPTIONAL SUBJECT",
            content=content,
            size_hint=(0.96, 0.86),
            auto_dismiss=False
        )

        state = {
            "student_id": None
        }

        # --------------------------------------------------------
        # LOAD SUBJECTS
        # --------------------------------------------------------

        def load_subjects(*args):

            try:

                con = db()

                rows = con.execute(
                    """
                    SELECT id,name
                    FROM subjects
                    ORDER BY name
                    """
                ).fetchall()

                con.close()

                names = [
                    row[1]
                    for row in rows
                ]

                subject_spinner.values = names

                if not names:

                    subject_spinner.text = (
                        "SELECT SUBJECT"
                    )

                    info_label.text = (
                        "No subjects found. "
                        "Add subjects first."
                    )

            except Exception as error:

                subject_spinner.values = []

                info_label.text = (
                    "Subject Error: "
                    +
                    str(error)
                )

        # --------------------------------------------------------
        # OPEN STUDENT
        # --------------------------------------------------------

        def open_student_action(*args):

            class_name = (
                cls.text.strip()
            )

            section_name = (
                sec.text.strip()
            )

            roll_number = (
                roll.text.strip()
            )

            if (
                not class_name
                or
                not section_name
                or
                not roll_number
            ):

                info_label.text = (
                    "Please enter Class, "
                    "Section and Roll."
                )

                state["student_id"] = None

                return

            if class_name == "Other":

                info_label.text = (
                    "Please enter the actual Class."
                )

                return

            if section_name == "Other":

                info_label.text = (
                    "Please enter the actual Section."
                )

                return

            try:

                student = (
                    self.get_student_by_class_section_roll(
                        class_name,
                        section_name,
                        roll_number
                    )
                )

                if not student:

                    state["student_id"] = None

                    info_label.text = (
                        "Student not found."
                    )

                    subject_spinner.text = (
                        "SELECT SUBJECT"
                    )

                    return

                state["student_id"] = (
                    student[0]
                )

                info_label.text = (
                    "Name: {}\n"
                    "Class: {}   Section: {}   Roll: {}"
                    .format(
                        student[2] or "",
                        student[3] or "",
                        student[4] or "",
                        student[1] or ""
                    )
                )

                # Existing optional
                con = db()

                existing = con.execute(
                    """
                    SELECT s.name
                    FROM optional_subjects o
                    JOIN subjects s
                    ON s.id=o.subject_id
                    WHERE o.student_id=?
                    """,
                    (
                        student[0],
                    )
                ).fetchone()

                con.close()

                if existing:

                    subject_spinner.text = (
                        existing[0]
                    )

                else:

                    subject_spinner.text = (
                        "SELECT SUBJECT"
                    )

            except Exception as error:

                state["student_id"] = None

                info_label.text = (
                    "Error: "
                    +
                    str(error)
                )

        # --------------------------------------------------------
        # SET OPTIONAL
        # --------------------------------------------------------

        def set_optional_action(*args):

            student_id = (
                state["student_id"]
            )

            if not student_id:

                self.message_popup(
                    "OPTIONAL SUBJECT",
                    "Open a student first.",
                    ORANGE
                )

                return

            subject_name = (
                subject_spinner.text.strip()
            )

            if (
                not subject_name
                or
                subject_name ==
                "SELECT SUBJECT"
            ):

                self.message_popup(
                    "OPTIONAL SUBJECT",
                    "Select a subject.",
                    ORANGE
                )

                return

            try:

                con = db()

                subject = con.execute(
                    """
                    SELECT id
                    FROM subjects
                    WHERE name=?
                    """,
                    (
                        subject_name,
                    )
                ).fetchone()

                if not subject:

                    con.close()

                    self.message_popup(
                        "OPTIONAL SUBJECT",
                        "Subject not found.",
                        RED
                    )

                    return

                # SQLite compatible UPSERT
                con.execute(
                    """
                    INSERT INTO optional_subjects(
                        student_id,
                        subject_id
                    )
                    VALUES(
                        ?,
                        ?
                    )
                    ON CONFLICT(student_id)
                    DO UPDATE SET
                        subject_id=
                        excluded.subject_id
                    """,
                    (
                        student_id,
                        subject[0]
                    )
                )

                con.commit()

                con.close()

                self.message_popup(
                    "SUCCESS",
                    "Optional subject set successfully.",
                    GREEN
                )

            except Exception as error:

                self.message_popup(
                    "OPTIONAL ERROR",
                    str(error),
                    RED
                )

        # --------------------------------------------------------
        # CLEAR OPTIONAL
        # --------------------------------------------------------

        def clear_optional_action(*args):

            student_id = (
                state["student_id"]
            )

            if not student_id:

                self.message_popup(
                    "OPTIONAL SUBJECT",
                    "Open a student first.",
                    ORANGE
                )

                return

            try:

                con = db()

                con.execute(
                    """
                    DELETE FROM optional_subjects
                    WHERE student_id=?
                    """,
                    (
                        student_id,
                    )
                )

                con.commit()

                con.close()

                subject_spinner.text = (
                    "SELECT SUBJECT"
                )

                self.message_popup(
                    "SUCCESS",
                    "Optional subject cleared.",
                    GREEN
                )

            except Exception as error:

                self.message_popup(
                    "OPTIONAL ERROR",
                    str(error),
                    RED
                )

        # --------------------------------------------------------
        # OTHER
        # --------------------------------------------------------

        cls.bind(
            text=lambda instance, text:
            self.ask_custom_value(
                "ENTER CLASS",
                instance,
                True
            )
            if text == "Other"
            else None
        )

        sec.bind(
            text=lambda instance, text:
            self.ask_custom_value(
                "ENTER SECTION",
                instance,
                False
            )
            if text == "Other"
            else None
        )

        open_student.bind(
            on_release=
            open_student_action
        )

        set_button.bind(
            on_release=
            set_optional_action
        )

        clear_button.bind(
            on_release=
            clear_optional_action
        )

        close_button.bind(
            on_release=
            popup.dismiss
        )

        popup.open()

        load_subjects()

    # ============================================================
    # MARKS ENTRY
    # ============================================================

    def marks_popup(
        self,
        *args
    ):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        search = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(120)
        )

        cls = Spinner(
            text=self.get_classes()[0],
            values=self.get_classes(),
            font_size=sp(17),
            color=DARK,
            background_color=WHITE,
            size_hint_y=None,
            height=dp(54)
        )

        sec = Spinner(
            text=self.get_sections()[0],
            values=self.get_sections(),
            font_size=sp(17),
            color=DARK,
            background_color=WHITE,
            size_hint_y=None,
            height=dp(54)
        )

        search.add_widget(
            make_label(
                "Class",
                17,
                DARK,
                True
            )
        )

        search.add_widget(cls)

        search.add_widget(
            make_label(
                "Section",
                17,
                DARK,
                True
            )
        )

        search.add_widget(sec)

        content.add_widget(
            search
        )

        # ROLL

        roll_row = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(56)
        )

        roll = make_input(
            "Student Roll",
            "",
            17
        )

        open_button = make_button(
            "OPEN STUDENT",
            BLUE2,
            56,
            16
        )

        roll_row.add_widget(
            roll
        )

        roll_row.add_widget(
            open_button
        )

        content.add_widget(
            roll_row
        )

        # STUDENT INFO

        info_box = ColoredBox(
            orientation="vertical",
            padding=dp(7),
            size_hint_y=None,
            height=dp(72),
            bg_color=WHITE,
            border_color=LIGHT_GRAY
        )

        student_info = make_label(
            "Enter Class + Section + Roll",
            16,
            DARK,
            True,
            "center"
        )

        info_box.add_widget(
            student_info
        )

        content.add_widget(
            info_box
        )

        # TABLE

        marks_scroll = ScrollView()

        table = GridLayout(
            cols=5,
            spacing=dp(1),
            size_hint_y=None
        )

        table.bind(
            minimum_height=
            table.setter("height")
        )

        marks_scroll.add_widget(
            table
        )

        content.add_widget(
            marks_scroll
        )

        # BOTTOM

        bottom = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(58)
        )

        save_button = make_button(
            "SAVE MARKS",
            GREEN,
            58,
            17
        )

        close_button = make_button(
            "CLOSE",
            GRAY,
            58,
            17
        )

        bottom.add_widget(
            save_button
        )

        bottom.add_widget(
            close_button
        )

        content.add_widget(
            bottom
        )

        popup = Popup(
            title="MARKS ENTRY",
            content=content,
            size_hint=(0.99, 0.96),
            auto_dismiss=False
        )

        state = {
            "student_id": None,
            "rows": []
        }

        # --------------------------------------------------------
        # HEADERS
        # --------------------------------------------------------

        def build_headers():

            table.clear_widgets()

            headers = [
                "SUBJECT",
                "CQ",
                "MCQ",
                "PRACTICAL",
                "TOTAL"
            ]

            widths = [
                0.30,
                0.15,
                0.15,
                0.20,
                0.20
            ]

            for index, text in enumerate(
                headers
            ):

                table.add_widget(
                    TableCell(
                        text=text,
                        font_size=sp(14),
                        bold=True,
                        color=WHITE,
                        bg_color=BLUE,
                        size_hint_x=
                        widths[index],
                        size_hint_y=None,
                        height=dp(48)
                    )
                )

        # --------------------------------------------------------
        # LOAD MARKS
        # --------------------------------------------------------

        def load_marks(
            student_id
        ):

            build_headers()

            state["rows"] = []

            try:

                con = db()

                subjects = con.execute(
                    """
                    SELECT id,name
                    FROM subjects
                    ORDER BY name
                    """
                ).fetchall()

                existing = con.execute(
                    """
                    SELECT
                        subject_id,
                        cq,
                        mcq,
                        practical,
                        total
                    FROM marks
                    WHERE student_id=?
                    """,
                    (
                        student_id,
                    )
                ).fetchall()

                con.close()

                old = {
                    row[0]: row
                    for row in existing
                }

                if not subjects:

                    for index in range(5):

                        table.add_widget(
                            TableCell(
                                text=
                                "No subjects. "
                                "Add subjects first."
                                if index == 0
                                else "",
                                font_size=sp(14),
                                size_hint_y=None,
                                height=dp(55)
                            )
                        )

                    return

                for subject_id, subject_name in subjects:

                    old_row = old.get(
                        subject_id
                    )

                    cq_value = (
                        clean_number(
                            old_row[1]
                        )
                        if old_row
                        else ""
                    )

                    mcq_value = (
                        clean_number(
                            old_row[2]
                        )
                        if old_row
                        else ""
                    )

                    practical_value = (
                        clean_number(
                            old_row[3]
                        )
                        if old_row
                        else ""
                    )

                    total_value = (
                        clean_number(
                            old_row[4]
                        )
                        if old_row
                        else ""
                    )

                    subject_label = TableCell(
                        text=subject_name,
                        font_size=sp(14),
                        halign="left",
                        size_hint_x=0.30,
                        size_hint_y=None,
                        height=dp(56)
                    )

                    cq = TextInput(
                        text=cq_value,
                        font_size=sp(15),
                        foreground_color=DARK,
                        background_color=WHITE,
                        cursor_color=BLUE,
                        multiline=False,
                        size_hint_x=0.15,
                        size_hint_y=None,
                        height=dp(56)
                    )

                    mcq = TextInput(
                        text=mcq_value,
                        font_size=sp(15),
                        foreground_color=DARK,
                        background_color=WHITE,
                        cursor_color=BLUE,
                        multiline=False,
                        size_hint_x=0.15,
                        size_hint_y=None,
                        height=dp(56)
                    )

                    practical = TextInput(
                        text=practical_value,
                        font_size=sp(15),
                        foreground_color=DARK,
                        background_color=WHITE,
                        cursor_color=BLUE,
                        multiline=False,
                        size_hint_x=0.20,
                        size_hint_y=None,
                        height=dp(56)
                    )

                    total = TableCell(
                        text=total_value,
                        font_size=sp(14),
                        size_hint_x=0.20,
                        size_hint_y=None,
                        height=dp(56)
                    )

                    row_data = {

                        "subject_id":
                        subject_id,

                        "subject_name":
                        subject_name,

                        "cq":
                        cq,

                        "mcq":
                        mcq,

                        "practical":
                        practical,

                        "total":
                        total
                    }

                    def update_total(
                        *args,
                        rd=row_data
                    ):

                        cq_text = (
                            rd["cq"].text.strip()
                        )

                        mcq_text = (
                            rd["mcq"].text.strip()
                        )

                        practical_text = (
                            rd[
                                "practical"
                            ].text.strip()
                        )

                        if (
                            not cq_text
                            and
                            not mcq_text
                            and
                            not practical_text
                        ):

                            rd["total"].text = ""

                        else:

                            total_number = (
                                safe_float(
                                    cq_text
                                )
                                +
                                safe_float(
                                    mcq_text
                                )
                                +
                                safe_float(
                                    practical_text
                                )
                            )

                            rd["total"].text = (
                                clean_number(
                                    total_number
                                )
                            )

                    cq.bind(
                        text=update_total
                    )

                    mcq.bind(
                        text=update_total
                    )

                    practical.bind(
                        text=update_total
                    )

                    table.add_widget(
                        subject_label
                    )

                    table.add_widget(cq)
                    table.add_widget(mcq)
                    table.add_widget(practical)
                    table.add_widget(total)

                    state["rows"].append(
                        row_data
                    )

            except Exception as error:

                student_info.text = (
                    str(error)
                )

        # --------------------------------------------------------
        # OPEN STUDENT
        # --------------------------------------------------------

        def open_marks_student(*args):

            class_name = (
                cls.text.strip()
            )

            section_name = (
                sec.text.strip()
            )

            roll_number = (
                roll.text.strip()
            )

            if (
                not class_name
                or
                not section_name
                or
                not roll_number
            ):

                student_info.text = (
                    "Please enter Class, "
                    "Section and Roll."
                )

                return

            if class_name == "Other":

                student_info.text = (
                    "Please enter actual Class."
                )

                return

            if section_name == "Other":

                student_info.text = (
                    "Please enter actual Section."
                )

                return

            try:

                student = (
                    self.get_student_by_class_section_roll(
                        class_name,
                        section_name,
                        roll_number
                    )
                )

                if not student:

                    state["student_id"] = None

                    student_info.text = (
                        "Student not found."
                    )

                    return

                state["student_id"] = (
                    student[0]
                )

                student_info.text = (
                    "Name: {}   |   "
                    "Class: {}   |   "
                    "Section: {}   |   "
                    "Roll: {}"
                    .format(
                        student[2] or "",
                        student[3] or "",
                        student[4] or "",
                        student[1] or ""
                    )
                )

                load_marks(
                    student[0]
                )

            except Exception as error:

                student_info.text = (
                    str(error)
                )

        # --------------------------------------------------------
        # SAVE MARKS
        # --------------------------------------------------------

        def save_marks(*args):

            student_id = (
                state["student_id"]
            )

            if not student_id:

                self.message_popup(
                    "MARKS",
                    "Open a student first.",
                    ORANGE
                )

                return

            try:

                con = db()

                for row_data in state["rows"]:

                    cq = blank_or_number(
                        row_data["cq"].text
                    )

                    mcq = blank_or_number(
                        row_data["mcq"].text
                    )

                    practical = blank_or_number(
                        row_data["practical"].text
                    )

                    if (
                        cq is None
                        and
                        mcq is None
                        and
                        practical is None
                    ):

                        total = None

                    else:

                        total = (
                            safe_float(cq)
                            +
                            safe_float(mcq)
                            +
                            safe_float(practical)
                        )

                    con.execute(
                        """
                        INSERT INTO marks(
                            student_id,
                            subject_id,
                            cq,
                            mcq,
                            practical,
                            total,
                            marks
                        )
                        VALUES(
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?
                        )
                        ON CONFLICT(
                            student_id,
                            subject_id
                        )
                        DO UPDATE SET

                            cq=excluded.cq,

                            mcq=excluded.mcq,

                            practical=
                            excluded.practical,

                            total=
                            excluded.total,

                            marks=
                            excluded.marks
                        """,
                        (
                            student_id,
                            row_data["subject_id"],
                            cq,
                            mcq,
                            practical,
                            total,
                            total
                        )
                    )

                con.commit()

                con.close()

                self.message_popup(
                    "SUCCESS",
                    "Marks saved successfully.",
                    GREEN
                )

            except Exception as error:

                self.message_popup(
                    "MARKS ERROR",
                    str(error),
                    RED
                )

        cls.bind(
            text=lambda instance, text:
            self.ask_custom_value(
                "ENTER CLASS",
                instance,
                True
            )
            if text == "Other"
            else None
        )

        sec.bind(
            text=lambda instance, text:
            self.ask_custom_value(
                "ENTER SECTION",
                instance,
                False
            )
            if text == "Other"
            else None
        )

        open_button.bind(
            on_release=
            open_marks_student
        )

        save_button.bind(
            on_release=
            save_marks
        )

        close_button.bind(
            on_release=
            popup.dismiss
        )

        popup.open()

        build_headers()

    # ============================================================
    # RESULT POPUP
    # ============================================================

    def result_popup(
        self,
        *args
    ):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        search = GridLayout(
            cols=2,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(120)
        )

        cls = Spinner(
            text=self.get_classes()[0],
            values=self.get_classes(),
            font_size=sp(17),
            color=DARK,
            background_color=WHITE,
            size_hint_y=None,
            height=dp(54)
        )

        sec = Spinner(
            text=self.get_sections()[0],
            values=self.get_sections(),
            font_size=sp(17),
            color=DARK,
            background_color=WHITE,
            size_hint_y=None,
            height=dp(54)
        )

        search.add_widget(
            make_label(
                "Class",
                17,
                DARK,
                True
            )
        )

        search.add_widget(cls)

        search.add_widget(
            make_label(
                "Section",
                17,
                DARK,
                True
            )
        )

        search.add_widget(sec)

        content.add_widget(
            search
        )

        roll_row = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(56)
        )

        roll = make_input(
            "Roll (optional)",
            "",
            17
        )

        show_button = make_button(
            "SHOW RESULT",
            BLUE2,
            56,
            16
        )

        roll_row.add_widget(
            roll
        )

        roll_row.add_widget(
            show_button
        )

        content.add_widget(
            roll_row
        )

        result_scroll = ScrollView()

        result_box = GridLayout(
            cols=1,
            spacing=dp(9),
            padding=dp(5),
            size_hint_y=None
        )

        result_box.bind(
            minimum_height=
            result_box.setter("height")
        )

        result_scroll.add_widget(
            result_box
        )

        content.add_widget(
            result_scroll
        )

        bottom = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(56)
        )

        download_all = make_button(
            "DOWNLOAD ALL PDF",
            GREEN,
            56,
            15
        )

        close = make_button(
            "CLOSE",
            GRAY,
            56,
            17
        )

        bottom.add_widget(
            download_all
        )

        bottom.add_widget(
            close
        )

        content.add_widget(
            bottom
        )

        popup = Popup(
            title="RESULT / GPA / MERIT",
            content=content,
            size_hint=(0.99, 0.97),
            auto_dismiss=False
        )

        def show_results(*args):

            result_box.clear_widgets()

            class_name = (
                cls.text.strip()
            )

            section_name = (
                sec.text.strip()
            )

            roll_number = (
                roll.text.strip()
            )

            if (
                class_name == "Other"
                or
                section_name == "Other"
            ):

                result_box.add_widget(
                    make_label(
                        "Please enter the actual "
                        "Class and Section.",
                        18,
                        ORANGE,
                        True,
                        "center"
                    )
                )

                return

            try:

                con = db()

                if roll_number:

                    students = con.execute(
                        """
                        SELECT *
                        FROM students
                        WHERE class_name=?
                        AND section=?
                        AND roll=?
                        """,
                        (
                            class_name,
                            section_name,
                            roll_number
                        )
                    ).fetchall()

                else:

                    students = con.execute(
                        """
                        SELECT *
                        FROM students
                        WHERE class_name=?
                        AND section=?
                        ORDER BY
                            CASE
                                WHEN roll GLOB '[0-9]*'
                                THEN CAST(roll AS INTEGER)
                                ELSE 999999
                            END,
                            roll,
                            name
                        """,
                        (
                            class_name,
                            section_name
                        )
                    ).fetchall()

                con.close()

                if not students:

                    result_box.add_widget(
                        make_label(
                            "No student found.",
                            19,
                            RED,
                            True,
                            "center"
                        )
                    )

                    return

                for student in students:

                    result_box.add_widget(
                        self.make_result_card(
                            student,
                            class_name,
                            section_name
                        )
                    )

            except Exception as error:

                result_box.add_widget(
                    make_label(
                        str(error),
                        17,
                        RED
                    )
                )

        cls.bind(
            text=lambda instance, text:
            self.ask_custom_value(
                "ENTER CLASS",
                instance,
                True
            )
            if text == "Other"
            else None
        )

        sec.bind(
            text=lambda instance, text:
            self.ask_custom_value(
                "ENTER SECTION",
                instance,
                False
            )
            if text == "Other"
            else None
        )

        show_button.bind(
            on_release=
            show_results
        )

        def download_all_action(*args):

            class_name = (
                cls.text.strip()
            )

            section_name = (
                sec.text.strip()
            )

            if (
                class_name == "Other"
                or
                section_name == "Other"
            ):

                self.message_popup(
                    "PDF",
                    "Please enter actual Class and Section.",
                    ORANGE
                )

                return

            try:

                con = db()

                students = con.execute(
                    """
                    SELECT id
                    FROM students
                    WHERE class_name=?
                    AND section=?
                    ORDER BY
                        CASE
                            WHEN roll GLOB '[0-9]*'
                            THEN CAST(roll AS INTEGER)
                            ELSE 999999
                        END,
                        roll,
                        name
                    """,
                    (
                        class_name,
                        section_name
                    )
                ).fetchall()

                con.close()

                if not students:

                    self.message_popup(
                        "PDF",
                        "No students found.",
                        ORANGE
                    )

                    return

                count = 0

                for row in students:

                    if self.generate_student_pdf(
                        row[0],
                        show_message=False
                    ):

                        count += 1

                self.message_popup(
                    "PDF",
                    "{} PDF file(s) generated successfully."
                    .format(count),
                    GREEN
                )

            except Exception as error:

                self.message_popup(
                    "PDF ERROR",
                    str(error),
                    RED
                )

        download_all.bind(
            on_release=
            download_all_action
        )

        close.bind(
            on_release=
            popup.dismiss
        )

        popup.open()

    # ============================================================
    # RESULT CARD
    # ============================================================

    def make_result_card(
        self,
        student,
        class_name,
        section_name
    ):

        data = self.calculate_result(
            student[0],
            class_name,
            section_name
        )

        card = ColoredBox(
            orientation="vertical",
            padding=dp(9),
            spacing=dp(7),
            size_hint_y=None,
            height=dp(540),
            bg_color=WHITE,
            border_color=LIGHT_GRAY
        )

        card.add_widget(
            make_label(
                "{} | Class {} | Section {} | Roll {}"
                .format(
                    student[2] or "",
                    student[3] or "",
                    student[4] or "",
                    student[1] or ""
                ),
                19,
                DARK,
                True
            )
        )

        summary = BoxLayout(
            spacing=dp(6),
            size_hint_y=None,
            height=dp(48)
        )

        summary.add_widget(
            make_label(
                "Total: {}"
                .format(
                    clean_number(
                        data["grand_total"]
                    )
                ),
                16,
                DARK,
                True
            )
        )

        summary.add_widget(
            make_label(
                "GPA: {:.2f}"
                .format(
                    data["gpa"]
                ),
                16,
                DARK,
                True
            )
        )

        summary.add_widget(
            make_label(
                "Merit: {}"
                .format(
                    data["merit"]
                ),
                16,
                DARK,
                True
            )
        )

        card.add_widget(
            summary
        )

        # --------------------------------------------------------
        # TABLE
        # --------------------------------------------------------

        table_scroll = ScrollView(
            size_hint_y=None,
            height=dp(325)
        )

        table = GridLayout(
            cols=5,
            spacing=dp(1),
            size_hint_y=None
        )

        table.bind(
            minimum_height=
            table.setter("height")
        )

        table_scroll.add_widget(
            table
        )

        headers = [
            "SUBJECT",
            "CQ",
            "MCQ",
            "PRACTICAL",
            "TOTAL"
        ]

        for header in headers:

            table.add_widget(
                TableCell(
                    text=header,
                    font_size=sp(14),
                    bold=True,
                    color=WHITE,
                    bg_color=BLUE,
                    size_hint_y=None,
                    height=dp(46)
                )
            )

        for row in data["rows"]:

            values = [

                (
                    row["subject"],
                    "left"
                ),

                (
                    clean_number(
                        row["cq"]
                    ),
                    "center"
                ),

                (
                    clean_number(
                        row["mcq"]
                    ),
                    "center"
                ),

                (
                    clean_number(
                        row["practical"]
                    ),
                    "center"
                ),

                (
                    clean_number(
                        row["total"]
                    ),
                    "center"
                )
            ]

            for value, align in values:

                table.add_widget(
                    TableCell(
                        text=value,
                        font_size=sp(14),
                        halign=align,
                        size_hint_y=None,
                        height=dp(46)
                    )
                )

        card.add_widget(
            table_scroll
        )

        status = (
            "FAILED"
            if data["failed"]
            else "PASSED"
        )

        card.add_widget(
            make_label(
                "Status: {}   |   Optional: {}"
                .format(
                    status,
                    data["optional_name"]
                    or "None"
                ),
                16,
                RED
                if data["failed"]
                else GREEN,
                True
            )
        )

        buttons = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(54)
        )

        profile = make_button(
            "PROFILE",
            BLUE2,
            54,
            16
        )

        pdf = make_button(
            "SAVE PDF",
            GREEN,
            54,
            16
        )

        buttons.add_widget(
            profile
        )

        buttons.add_widget(
            pdf
        )

        card.add_widget(
            buttons
        )

        profile.bind(
            on_release=lambda *a:
            self.show_profile(
                student[0]
            )
        )

        pdf.bind(
            on_release=lambda *a:
            self.generate_student_pdf(
                student[0]
            )
        )

        return card

    # ============================================================
    # CALCULATE RESULT
    # ============================================================

    def calculate_result(
        self,
        student_id,
        class_name=None,
        section_name=None
    ):

        try:

            con = db()

            rows = con.execute(
                """
                SELECT
                    s.id,
                    s.name,
                    m.cq,
                    m.mcq,
                    m.practical,
                    m.total
                FROM subjects s
                LEFT JOIN marks m
                ON m.subject_id=s.id
                AND m.student_id=?
                ORDER BY s.name
                """,
                (
                    student_id,
                )
            ).fetchall()

            optional = con.execute(
                """
                SELECT
                    s.id,
                    s.name
                FROM optional_subjects o
                JOIN subjects s
                ON s.id=o.subject_id
                WHERE o.student_id=?
                """,
                (
                    student_id,
                )
            ).fetchone()

            con.close()

        except Exception:

            return {
                "rows": [],
                "grand_total": 0.0,
                "gpa": 0.0,
                "merit": "-",
                "failed": False,
                "optional_name": ""
            }

        optional_id = (
            optional[0]
            if optional
            else None
        )

        optional_name = (
            optional[1]
            if optional
            else ""
        )

        result_rows = []

        compulsory_points = []

        optional_gp = 0.0

        failed = False

        grand_total = 0.0

        for row in rows:

            subject_id = row[0]

            subject_name = row[1]

            cq = row[2]

            mcq = row[3]

            practical = row[4]

            total = row[5]

            numeric_total = safe_float(
                total
            )

            grand_total += numeric_total

            grade, gp = grade_info(
                numeric_total
            )

            if subject_id == optional_id:

                optional_gp = gp

            else:

                compulsory_points.append(
                    gp
                )

                if grade == "F":

                    failed = True

            result_rows.append(
                {
                    "subject":
                    subject_name,

                    "cq":
                    cq,

                    "mcq":
                    mcq,

                    "practical":
                    practical,

                    "total":
                    total,

                    "grade":
                    grade,

                    "gp":
                    gp
                }
            )

        if compulsory_points:

            base_gpa = (
                sum(compulsory_points)
                /
                len(compulsory_points)
            )

        else:

            base_gpa = 0.0

        if failed:

            gpa = 0.0

        else:

            bonus = 0.0

            if optional_gp > 2:

                bonus = (
                    optional_gp - 2
                )

            gpa = (
                base_gpa
                +
                bonus
            )

            if gpa > 5:

                gpa = 5.0

        merit = "-"

        if (
            class_name
            and
            section_name
        ):

            merit = self.calculate_merit(
                student_id,
                class_name,
                section_name
            )

        return {

            "rows":
            result_rows,

            "grand_total":
            grand_total,

            "gpa":
            gpa,

            "merit":
            merit,

            "failed":
            failed,

            "optional_name":
            optional_name
        }

    # ============================================================
    # MERIT
    # ============================================================

    def calculate_merit(
        self,
        current_student_id,
        class_name,
        section_name
    ):

        try:

            con = db()

            students = con.execute(
                """
                SELECT id
                FROM students
                WHERE class_name=?
                AND section=?
                """,
                (
                    class_name,
                    section_name
                )
            ).fetchall()

            con.close()

            ranking = []

            for row in students:

                student_id = row[0]

                result = self.calculate_result(
                    student_id,
                    None,
                    None
                )

                ranking.append(
                    (
                        student_id,
                        result["gpa"],
                        result["grand_total"]
                    )
                )

            ranking.sort(
                key=lambda x: (
                    -x[1],
                    -x[2]
                )
            )

            for position, item in enumerate(
                ranking,
                start=1
            ):

                if (
                    item[0]
                    ==
                    current_student_id
                ):

                    return str(position)

        except Exception:

            pass

        return "-"

    # ============================================================
    # PDF DIRECTORY
    # ============================================================

    def get_pdf_directory(self):

        candidates = [

            "/storage/emulated/0/Download/"
            "Teacher_Result_Manager",

            "/storage/emulated/0/Download",

            PDF_DIR
        ]

        for path in candidates:

            try:

                os.makedirs(
                    path,
                    exist_ok=True
                )

                test_file = os.path.join(
                    path,
                    ".write_test"
                )

                with open(
                    test_file,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write("ok")

                try:

                    os.remove(
                        test_file
                    )

                except Exception:
                    pass

                return path

            except Exception:

                continue

        return PDF_DIR

    # ============================================================
    # PDF GENERATOR
    # ============================================================

    def generate_student_pdf(
        self,
        student_id,
        show_message=True
    ):

        try:

            from reportlab.lib import colors

            from reportlab.lib.pagesizes import A4

            from reportlab.lib.styles import (
                getSampleStyleSheet,
                ParagraphStyle
            )

            from reportlab.lib.enums import (
                TA_CENTER
            )

            from reportlab.platypus import (
                SimpleDocTemplate,
                Paragraph,
                Spacer,
                Table,
                TableStyle,
                Image as PDFImage
            )

            from reportlab.pdfbase import (
                pdfmetrics
            )

            from reportlab.pdfbase.ttfonts import (
                TTFont
            )

        except Exception as error:

            if show_message:

                self.message_popup(
                    "PDF",
                    "ReportLab is not installed.\n\n{}"
                    .format(error),
                    RED
                )

            return False

        try:

            con = db()

            student = con.execute(
                """
                SELECT *
                FROM students
                WHERE id=?
                """,
                (
                    student_id,
                )
            ).fetchone()

            con.close()

            if not student:

                if show_message:

                    self.message_popup(
                        "PDF",
                        "Student not found.",
                        RED
                    )

                return False

            # ----------------------------------------------------
            # FONT
            # ----------------------------------------------------

            font_name = "Helvetica"

            base_dir = os.path.dirname(
                os.path.abspath(__file__)
            )

            font_candidates = [

                os.path.join(
                    base_dir,
                    "NotoSansBengali-Regular.ttf"
                ),

                os.path.join(
                    base_dir,
                    "fonts",
                    "NotoSansBengali-Regular.ttf"
                ),

                os.path.join(
                    base_dir,
                    "HindSiliguri-Regular.ttf"
                ),

                os.path.join(
                    base_dir,
                    "fonts",
                    "HindSiliguri-Regular.ttf"
                ),

                "/storage/emulated/0/Download/"
                "NotoSansBengali-Regular.ttf",

                "/storage/emulated/0/Download/"
                "HindSiliguri-Regular.ttf"
            ]

            for font_path in font_candidates:

                if os.path.exists(
                    font_path
                ):

                    try:

                        pdfmetrics.registerFont(
                            TTFont(
                                "BanglaFont",
                                font_path
                            )
                        )

                        font_name = (
                            "BanglaFont"
                        )

                        break

                    except Exception:

                        pass

            result = self.calculate_result(
                student_id,
                student[3],
                student[4]
            )

            folder = (
                self.get_pdf_directory()
            )

            filename = (
                sanitize_filename(
                    student[2]
                    or
                    "student"
                )
                +
                "_"
                +
                sanitize_filename(
                    student[1]
                    or
                    "roll"
                )
                +
                ".pdf"
            )

            filepath = os.path.join(
                folder,
                filename
            )

            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=28,
                leftMargin=28,
                topMargin=28,
                bottomMargin=28
            )

            styles = (
                getSampleStyleSheet()
            )

            title_style = ParagraphStyle(
                "TitleCustom",
                parent=styles["Title"],
                fontName=font_name,
                fontSize=20,
                leading=24,
                alignment=TA_CENTER,
                textColor=
                colors.HexColor(
                    "#123A66"
                )
            )

            normal = ParagraphStyle(
                "NormalCustom",
                parent=styles["Normal"],
                fontName=font_name,
                fontSize=10,
                leading=14,
                textColor=colors.black
            )

            small = ParagraphStyle(
                "SmallCustom",
                parent=normal,
                fontSize=9,
                leading=12
            )

            story = []

            story.append(
                Paragraph(
                    "TEACHER RESULT MANAGER PRO",
                    title_style
                )
            )

            story.append(
                Spacer(1, 5)
            )

            story.append(
                Paragraph(
                    "Student Result Report",
                    normal
                )
            )

            story.append(
                Spacer(1, 10)
            )

            # ----------------------------------------------------
            # DETAILS
            # ----------------------------------------------------

            details = [

                [
                    Paragraph(
                        "<b>Student Name</b>",
                        normal
                    ),

                    Paragraph(
                        str(
                            student[2]
                            or
                            ""
                        ),
                        normal
                    )
                ],

                [
                    Paragraph(
                        "<b>Class</b>",
                        normal
                    ),

                    Paragraph(
                        str(
                            student[3]
                            or
                            ""
                        ),
                        normal
                    )
                ],

                [
                    Paragraph(
                        "<b>Section</b>",
                        normal
                    ),

                    Paragraph(
                        str(
                            student[4]
                            or
                            ""
                        ),
                        normal
                    )
                ],

                [
                    Paragraph(
                        "<b>Roll</b>",
                        normal
                    ),

                    Paragraph(
                        str(
                            student[1]
                            or
                            ""
                        ),
                        normal
                    )
                ],

                [
                    Paragraph(
                        "<b>Registration Number</b>",
                        normal
                    ),

                    Paragraph(
                        str(
                            student[5]
                            or
                            ""
                        ),
                        normal
                    )
                ],

                [
                    Paragraph(
                        "<b>Birth Registration</b>",
                        normal
                    ),

                    Paragraph(
                        str(
                            student[6]
                            or
                            ""
                        ),
                        normal
                    )
                ],

                [
                    Paragraph(
                        "<b>Father's Name</b>",
                        normal
                    ),

                    Paragraph(
                        str(
                            student[7]
                            or
                            ""
                        ),
                        normal
                    )
                ],

                [
                    Paragraph(
                        "<b>Mother's Name</b>",
                        normal
                    ),

                    Paragraph(
                        str(
                            student[8]
                            or
                            ""
                        ),
                        normal
                    )
                ],

                [
                    Paragraph(
                        "<b>Father's NID</b>",
                        normal
                    ),

                    Paragraph(
                        str(
                            student[9]
                            or
                            ""
                        ),
                        normal
                    )
                ],

                [
                    Paragraph(
                        "<b>Mother's NID</b>",
                        normal
                    ),

                    Paragraph(
                        str(
                            student[10]
                            or
                            ""
                        ),
                        normal
                    )
                ],

                [
                    Paragraph(
                        "<b>Phone</b>",
                        normal
                    ),

                    Paragraph(
                        str(
                            student[11]
                            or
                            ""
                        ),
                        normal
                    )
                ]
            ]

            detail_table = Table(
                details,
                colWidths=[
                    155,
                    330
                ]
            )

            detail_table.setStyle(
                TableStyle(
                    [

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
                            "MIDDLE"
                        ),

                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, -1),
                            colors.whitesmoke
                        ),

                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, -1),
                            font_name
                        )
                    ]
                )
            )

            # ----------------------------------------------------
            # PHOTO + DETAILS
            # ----------------------------------------------------

            if (
                student[12]
                and
                os.path.exists(
                    student[12]
                )
            ):

                try:

                    photo = PDFImage(
                        student[12],
                        width=90,
                        height=105
                    )

                    profile_table = Table(
                        [
                            [
                                photo,
                                detail_table
                            ]
                        ],
                        colWidths=[
                            100,
                            385
                        ]
                    )

                    profile_table.setStyle(
                        TableStyle(
                            [
                                (
                                    "VALIGN",
                                    (0, 0),
                                    (-1, -1),
                                    "TOP"
                                )
                            ]
                        )
                    )

                    story.append(
                        profile_table
                    )

                except Exception:

                    story.append(
                        detail_table
                    )

            else:

                story.append(
                    detail_table
                )

            story.append(
                Spacer(1, 12)
            )

            # ----------------------------------------------------
            # SUMMARY
            # ----------------------------------------------------

            summary = Table(
                [
                    [
                        "Total",
                        clean_number(
                            result[
                                "grand_total"
                            ]
                        ),

                        "GPA",
                        "{:.2f}".format(
                            result["gpa"]
                        ),

                        "Merit",
                        str(
                            result["merit"]
                        )
                    ]
                ],
                colWidths=[
                    50,
                    75,
                    50,
                    75,
                    50,
                    75
                ]
            )

            summary.setStyle(
                TableStyle(
                    [
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.7,
                            colors.black
                        ),

                        (
                            "ALIGN",
                            (0, 0),
                            (-1, -1),
                            "CENTER"
                        ),

                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, -1),
                            font_name
                        )
                    ]
                )
            )

            story.append(
                summary
            )

            story.append(
                Spacer(1, 12)
            )

            # ----------------------------------------------------
            # MARKS TABLE
            # ----------------------------------------------------

            marks_data = [

                [
                    "Subject",
                    "CQ",
                    "MCQ",
                    "Practical",
                    "Total",
                    "Grade",
                    "GP"
                ]
            ]

            for row in result["rows"]:

                marks_data.append(
                    [

                        row["subject"],

                        clean_number(
                            row["cq"]
                        ),

                        clean_number(
                            row["mcq"]
                        ),

                        clean_number(
                            row["practical"]
                        ),

                        clean_number(
                            row["total"]
                        ),

                        row["grade"],

                        "{:.2f}".format(
                            row["gp"]
                        )
                    ]
                )

            marks_table = Table(
                marks_data,
                repeatRows=1,
                colWidths=[
                    130,
                    50,
                    50,
                    70,
                    50,
                    50,
                    40
                ]
            )

            marks_table.setStyle(
                TableStyle(
                    [

                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.black
                        ),

                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.lightgrey
                        ),

                        (
                            "FONTNAME",
                            (0, 0),
                            (-1, -1),
                            font_name
                        ),

                        (
                            "FONTSIZE",
                            (0, 0),
                            (-1, -1),
                            8
                        ),

                        (
                            "ALIGN",
                            (1, 1),
                            (-1, -1),
                            "CENTER"
                        )
                    ]
                )
            )

            story.append(
                marks_table
            )

            story.append(
                Spacer(1, 12)
            )

            story.append(
                Paragraph(
                    "Optional Subject: {}"
                    .format(
                        result[
                            "optional_name"
                        ]
                        or
                        "None"
                    ),
                    normal
                )
            )

            story.append(
                Paragraph(
                    "Status: {}"
                    .format(
                        "FAILED"
                        if result["failed"]
                        else
                        "PASSED"
                    ),
                    normal
                )
            )

            story.append(
                Spacer(1, 8)
            )

            story.append(
                Paragraph(
                    "Generated: {}"
                    .format(
                        datetime.now().strftime(
                            "%d-%m-%Y %I:%M %p"
                        )
                    ),
                    small
                )
            )

            doc.build(
                story
            )

            if show_message:

                self.message_popup(
                    "PDF SAVED",
                    "PDF saved successfully:\n\n{}"
                    .format(
                        filepath
                    ),
                    GREEN
                )

            return True

        except Exception as error:

            if show_message:

                self.message_popup(
                    "PDF ERROR",
                    "{}\n\n{}"
                    .format(
                        str(error),
                        traceback.format_exc()
                    ),
                    RED
                )

            return False

    # ============================================================
    # EXIT
    # ============================================================

    def confirm_exit(
        self,
        *args
    ):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(12)
        )

        content.add_widget(
            make_label(
                "Do you want to exit the application?",
                19,
                DARK,
                True,
                "center"
            )
        )

        buttons = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(56)
        )

        yes = make_button(
            "EXIT",
            RED,
            56,
            18
        )

        no = make_button(
            "CANCEL",
            GRAY,
            56,
            18
        )

        buttons.add_widget(
            yes
        )

        buttons.add_widget(
            no
        )

        content.add_widget(
            buttons
        )

        popup = Popup(
            title="EXIT",
            content=content,
            size_hint=(0.90, 0.34),
            auto_dismiss=False
        )

        yes.bind(
            on_release=lambda *a:
            self.stop_application(
                popup
            )
        )

        no.bind(
            on_release=
            popup.dismiss
        )

        popup.open()

    # ============================================================
    # STOP APPLICATION
    # ============================================================

    def stop_application(
        self,
        popup=None
    ):

        try:

            if popup:

                popup.dismiss()

        except Exception:
            pass

        try:

            self.stop()

        except Exception:
            pass

    # ============================================================
    # ANDROID BACK BUTTON
    # ============================================================

    def on_request_close(
        self,
        *args
    ):

        self.confirm_exit()

        return True


# ================================================================
# RUN
# ================================================================

if __name__ == "__main__":

    try:

        TeacherResultManagerApp().run()

    except Exception as error:

        print()
        print("=" * 65)
        print("TEACHER RESULT MANAGER PRO ERROR")
        print("=" * 65)
        print(str(error))
        print()
        print(traceback.format_exc())
        print("=" * 65)