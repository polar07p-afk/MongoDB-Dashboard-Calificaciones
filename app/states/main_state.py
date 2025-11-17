import reflex as rx
from typing import TypedDict, Any
import pymongo
import logging

MONGO_URI = "mongodb+srv://ender:ender2024@cluster0.oarsibs.mongodb.net/"
DATABASE_NAME = "enderavila"
GRADE_MAP = {
    "Grupo 1": 1,
    "Grupo 2": 2,
    "1er Grado": 3,
    "2do Grado": 4,
    "3er Grado": 5,
    "4to Grado": 6,
    "5to Grado": 7,
    "6to Grado": 8,
    "1er Año": 9,
    "2do Año": 10,
    "3er Año": 11,
    "4to Año": 12,
    "5to Año": 13,
}


class Assignment(TypedDict):
    grade: str
    section: str
    subject: str


class Teacher(TypedDict):
    first_name: str
    first_last_name: str
    email: str
    high_school_assignments: list[Assignment]


class Student(TypedDict):
    _id: str
    first_name: str
    first_last_name: str
    cedula: str
    grades: dict[str, str]


class Activity(TypedDict):
    id: str
    description: str
    date: str


class MainState(rx.State):
    """Manages app-wide state, including authentication and teacher data."""

    is_authenticated: bool = False
    is_loading: bool = False
    is_students_loading: bool = False
    login_error: str = ""
    teacher_data: Teacher | None = None
    selected_assignment_str: str = ""
    selected_section: str = ""
    students: list[Student] = []
    activities: list[Activity] = []
    show_add_activity_dialog: bool = False
    new_activity_description: str = ""
    new_activity_date: str = ""
    current_view: str = "gradebook"

    @rx.event
    def set_view(self, view: str):
        """Sets the current view in the dashboard."""
        self.current_view = view

    @rx.var
    def assignment_options(self) -> list[str]:
        """Returns a list of assignment strings for the select dropdown."""
        if not self.teacher_data:
            return []
        return [
            f"{a['grade']}|{a['section']}|{a['subject']}"
            for a in self.teacher_data["high_school_assignments"]
        ]

    @rx.var
    def selected_assignment_details(self) -> Assignment | None:
        """Parses the selected assignment string into a dictionary."""
        if not self.selected_assignment_str:
            return None
        parts = self.selected_assignment_str.split("|")
        if len(parts) != 3:
            return None
        return Assignment(grade=parts[0], section=parts[1], subject=parts[2])

    @rx.var
    def show_section_selector(self) -> bool:
        """Determines if the A/B section selector should be shown."""
        if not self.selected_assignment_details:
            return False
        return self.selected_assignment_details["section"] == "Ambas"

    @rx.var
    def is_load_button_disabled(self) -> bool:
        """Checks if the load students button should be disabled."""
        if not self.selected_assignment_str:
            return True
        if self.show_section_selector and (not self.selected_section):
            return True
        return False

    @rx.event
    def set_selected_assignment_str(self, value: str):
        """Resets dependent fields when a new assignment is selected."""
        self.selected_assignment_str = value
        self.selected_section = ""
        self.students = []
        self.activities = []

    @rx.event(background=True)
    async def load_students(self):
        """Loads students from the '2025-2026' collection based on selection."""
        if self.is_load_button_disabled:
            return
        async with self:
            self.is_students_loading = True
            self.students = []
        try:
            grade_str = self.selected_assignment_details["grade"]
            grade_numeric = GRADE_MAP.get(grade_str)
            section = (
                self.selected_section
                if self.show_section_selector
                else self.selected_assignment_details["section"]
            )
            if not grade_numeric or not section:
                raise ValueError("Invalid grade or section for query.")
            client = pymongo.MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            students_collection = db["2025-2026"]
            query = {"estudiante_grado": grade_numeric, "estudiante_seccion": section}
            student_docs = list(students_collection.find(query))
            client.close()
            loaded_students = [
                Student(
                    _id=str(doc["_id"]),
                    first_name=doc.get("estudiante_primer_nombre", ""),
                    first_last_name=doc.get("estudiante_primer_apellido", ""),
                    cedula=doc.get("estudiante_cedula", ""),
                    grades={},
                )
                for doc in student_docs
            ]
            async with self:
                self.students = loaded_students
        except Exception as e:
            logging.exception(f"Error loading students: {e}")
            pass
        finally:
            async with self:
                self.is_students_loading = False

    @rx.event
    def toggle_add_activity_dialog(self, open: bool):
        """Toggle the add activity dialog."""
        self.show_add_activity_dialog = open
        self.new_activity_description = ""
        self.new_activity_date = ""

    @rx.event
    def add_activity(self):
        """Adds a new activity column to the gradebook."""
        if self.new_activity_description and self.new_activity_date:
            import time

            new_id = str(int(time.time() * 1000))
            self.activities.append(
                Activity(
                    id=new_id,
                    description=self.new_activity_description,
                    date=self.new_activity_date,
                )
            )
            self.show_add_activity_dialog = False

    @rx.event
    def set_grade(self, student_id: str, activity_id: str, grade: str):
        """Updates the grade in the local state for a controlled input."""
        for i, student in enumerate(self.students):
            if student["_id"] == student_id:
                self.students[i]["grades"][activity_id] = grade
                break

    @rx.event(background=True)
    async def save_grade(self, student_id: str, activity_id: str, grade: str):
        """Saves a single grade to the database and updates local state."""
        async with self:
            for i, student in enumerate(self.students):
                if student["_id"] == student_id:
                    self.students[i]["grades"][activity_id] = grade
                    break
        try:
            assignment = self.selected_assignment_details
            if not assignment:
                return
            client = pymongo.MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            grades_collection = db["grades"]
            query = {
                "student_id": student_id,
                "grade_subject": assignment["subject"],
                "grade_level": GRADE_MAP[assignment["grade"]],
            }
            update = {"$set": {f"activities.{activity_id}": {"grade": grade}}}
            grades_collection.update_one(query, update, upsert=True)
            client.close()
        except Exception as e:
            logging.exception(f"Error saving grade: {e}")

    @rx.event(background=True)
    async def handle_login(self, form_data: dict[str, str]):
        """Authenticates the user and fetches teacher data from MongoDB."""
        async with self:
            self.is_loading = True
            self.login_error = ""
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "").strip()
        if not email or not password:
            async with self:
                self.login_error = "Email and password are required."
                self.is_loading = False
            return
        try:
            client = pymongo.MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            docentes_collection = db["docentes"]
            docente_doc = docentes_collection.find_one(
                {"email": email, "password": password}
            )
            client.close()
            if docente_doc:
                assignments = [
                    Assignment(
                        grade=a["grade"], section=a["section"], subject=a["subject"]
                    )
                    for a in docente_doc.get("high_school_assignments", [])
                ]
                async with self:
                    self.teacher_data = Teacher(
                        first_name=docente_doc.get("first_name", "N/A"),
                        first_last_name=docente_doc.get("first_last_name", "N/A"),
                        email=email,
                        high_school_assignments=assignments,
                    )
                    self.is_authenticated = True
            else:
                async with self:
                    self.login_error = "Invalid credentials. Please try again."
        except Exception as e:
            logging.exception(f"Error during login: {e}")
            async with self:
                self.login_error = "An error occurred. Please try again later."
        finally:
            async with self:
                self.is_loading = False

    @rx.event
    def logout(self):
        """Logs the user out and resets the state."""
        self.reset()