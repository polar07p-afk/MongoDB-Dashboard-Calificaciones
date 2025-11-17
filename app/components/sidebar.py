import reflex as rx
from app.states.main_state import MainState


def _nav_item(icon: str, name: str, view: str) -> rx.Component:
    """A single navigation item in the sidebar."""
    is_active = MainState.current_view == view
    return rx.el.button(
        rx.icon(icon, class_name="h-5 w-5"),
        rx.el.span(name, class_name="font-medium"),
        on_click=lambda: MainState.set_view(view),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 px-3 py-2.5 text-sky-700 bg-sky-100 rounded-lg transition-colors",
            "flex items-center gap-3 px-3 py-2.5 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors",
        ),
        width="100%",
    )


def sidebar() -> rx.Component:
    """The main sidebar for navigation."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("book-marked", class_name="h-7 w-7 text-sky-600"),
                rx.el.h1(
                    "Teacher's Portal", class_name="text-xl font-bold text-gray-800"
                ),
                class_name="flex items-center gap-3 p-4 border-b border-gray-200",
            ),
            rx.el.nav(
                _nav_item("clipboard-list", "Cargar Calificaciones", "gradebook"),
                _nav_item("user", "Perfil", "profile"),
                class_name="flex flex-col gap-2 p-4",
            ),
            class_name="flex flex-col h-full",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    rx.cond(
                        MainState.teacher_data,
                        MainState.teacher_data["first_name"]
                        + " "
                        + MainState.teacher_data["first_last_name"],
                        "Loading...",
                    ),
                    class_name="font-semibold text-gray-700",
                ),
                rx.el.p(
                    MainState.teacher_data["email"], class_name="text-sm text-gray-500"
                ),
                class_name="text-left",
            ),
            rx.el.button(
                rx.icon("log-out", class_name="h-5 w-5"),
                on_click=MainState.logout,
                class_name="p-2 text-gray-600 hover:bg-gray-200 rounded-lg transition-colors",
            ),
            class_name="flex items-center justify-between p-4 border-t border-gray-200",
        ),
        class_name="flex flex-col justify-between w-64 h-screen bg-white border-r border-gray-200 sticky top-0",
    )