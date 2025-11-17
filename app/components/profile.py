import reflex as rx
from app.states.main_state import MainState


def _assignment_info_card(assignment: dict) -> rx.Component:
    """Displays a card for a single assigned course."""
    return rx.el.div(
        rx.el.div(
            rx.icon("book-text", class_name="h-5 w-5 text-sky-700"),
            class_name="p-3 bg-sky-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(assignment["subject"], class_name="font-semibold text-gray-900"),
            rx.el.span(
                f"{assignment['grade']} - Section {assignment['section']}",
                class_name="text-sm text-gray-600",
            ),
        ),
        class_name="flex items-center gap-4",
    )


def profile_view() -> rx.Component:
    """Displays the teacher's profile information."""
    return rx.el.div(
        rx.el.h2("Teacher Profile", class_name="text-2xl font-bold text-gray-800 mb-6"),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Personal Information",
                    class_name="text-lg font-semibold text-gray-800 border-b pb-2 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("First Name", class_name="font-medium text-gray-500"),
                        rx.el.p(
                            MainState.teacher_data["first_name"],
                            class_name="text-gray-900",
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        rx.el.p("Last Name", class_name="font-medium text-gray-500"),
                        rx.el.p(
                            MainState.teacher_data["first_last_name"],
                            class_name="text-gray-900",
                        ),
                        class_name="flex-1",
                    ),
                    class_name="flex gap-8",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.h3(
                    "Assigned Courses",
                    class_name="text-lg font-semibold text-gray-800 border-b pb-2 mb-4",
                ),
                rx.el.div(
                    rx.foreach(
                        MainState.teacher_data["high_school_assignments"],
                        _assignment_info_card,
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                ),
            ),
            class_name="p-6 bg-white border border-gray-200 rounded-xl shadow-sm",
        ),
        class_name="max-w-4xl mx-auto",
    )