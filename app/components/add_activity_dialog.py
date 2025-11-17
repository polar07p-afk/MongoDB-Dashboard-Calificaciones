import reflex as rx
from app.states.main_state import MainState


def add_activity_dialog() -> rx.Component:
    """Dialog to add a new activity."""
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Add New Activity", class_name="text-lg font-semibold text-gray-800"
                ),
                rx.el.div(
                    rx.el.label(
                        "Description", class_name="text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        placeholder="E.g., Exam 1",
                        on_change=MainState.set_new_activity_description,
                        class_name="mt-1 w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:border-sky-500 transition",
                    ),
                    class_name="my-4",
                ),
                rx.el.div(
                    rx.el.label("Date", class_name="text-sm font-medium text-gray-700"),
                    rx.el.input(
                        type="date",
                        on_change=MainState.set_new_activity_date,
                        class_name="mt-1 w-full px-3 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=lambda: MainState.toggle_add_activity_dialog(False),
                        class_name="px-4 py-2 bg-gray-200 text-gray-700 font-medium rounded-lg hover:bg-gray-300 transition-colors",
                    ),
                    rx.el.button(
                        "Add Activity",
                        on_click=MainState.add_activity,
                        class_name="px-4 py-2 bg-sky-600 text-white font-semibold rounded-lg hover:bg-sky-700 transition-colors",
                    ),
                    class_name="flex justify-end gap-3",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-2xl p-6 w-full max-w-sm z-50",
            ),
        ),
        open=MainState.show_add_activity_dialog,
        on_open_change=MainState.toggle_add_activity_dialog,
    )