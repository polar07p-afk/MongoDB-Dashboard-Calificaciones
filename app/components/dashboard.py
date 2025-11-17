import reflex as rx
from app.states.main_state import MainState
from app.components.student_loader import student_loader_and_table
from app.components.sidebar import sidebar
from app.components.profile import profile_view


def gradebook_view() -> rx.Component:
    """The gradebook view, containing student loading and table."""
    return rx.el.div(
        rx.el.h2("Gradebook", class_name="text-2xl font-bold text-gray-800 mb-6"),
        student_loader_and_table(),
    )


def dashboard_view() -> rx.Component:
    """The main view for the authenticated teacher, including sidebar and content."""
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.match(
                MainState.current_view,
                ("gradebook", gradebook_view()),
                ("profile", profile_view()),
                rx.el.p("Invalid view selected."),
            ),
            class_name="flex-1 p-6 sm:p-8 bg-gray-50 overflow-y-auto",
        ),
        class_name="flex w-full min-h-screen",
    )