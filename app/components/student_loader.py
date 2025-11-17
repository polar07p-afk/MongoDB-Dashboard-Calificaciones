import reflex as rx
from app.states.main_state import MainState
from .add_activity_dialog import add_activity_dialog


def _grade_input(student: dict, activity: dict) -> rx.Component:
    """An input for a student's grade for a specific activity."""
    student_id = student["_id"].to_string()
    activity_id = activity["id"]
    return rx.el.td(
        rx.el.input(
            on_change=lambda grade: MainState.set_grade(student_id, activity_id, grade),
            on_blur=lambda grade: MainState.save_grade(student_id, activity_id, grade),
            placeholder="-",
            class_name="w-20 text-center bg-transparent border-gray-300 rounded-md focus:ring-sky-500 focus:border-sky-500 p-1",
            type="number",
            min=0,
            max=20,
            default_value=student["grades"].get(activity_id, ""),
        ),
        class_name="px-4 py-2",
    )


def _student_row(student: dict) -> rx.Component:
    """Displays a single student row in the table."""
    return rx.el.tr(
        rx.el.td(
            student["first_name"],
            class_name="px-4 py-3 text-sm text-gray-700 sticky left-0 bg-white z-10",
        ),
        rx.el.td(
            student["first_last_name"],
            class_name="px-4 py-3 text-sm text-gray-700 sticky left-[120px] bg-white z-10",
        ),
        rx.el.td(student["cedula"], class_name="px-4 py-3 text-sm text-gray-500"),
        rx.foreach(MainState.activities, lambda act: _grade_input(student, act)),
        class_name="border-b border-gray-200 bg-white hover:bg-gray-50",
    )


def student_loader_and_table() -> rx.Component:
    """Component for selecting an assignment and viewing students."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Assignment",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.select(
                        rx.el.option("Select an assignment", value="", disabled=True),
                        rx.foreach(
                            MainState.assignment_options,
                            lambda opt: rx.el.option(
                                opt.replace("|", " - "), value=opt
                            ),
                        ),
                        on_change=MainState.set_selected_assignment_str,
                        value=MainState.selected_assignment_str,
                        class_name="w-full p-2 border border-gray-300 rounded-lg bg-white shadow-sm",
                    ),
                    class_name="flex-1",
                ),
                rx.cond(
                    MainState.show_section_selector,
                    rx.el.div(
                        rx.el.label(
                            "Section",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.select(
                            rx.el.option("Select section", value="", disabled=True),
                            rx.el.option("A", value="A"),
                            rx.el.option("B", value="B"),
                            on_change=MainState.set_selected_section,
                            value=MainState.selected_section,
                            class_name="w-full p-2 border border-gray-300 rounded-lg bg-white shadow-sm",
                        ),
                        class_name="w-48",
                    ),
                    None,
                ),
                class_name="flex items-end gap-4",
            ),
            rx.el.button(
                rx.cond(
                    MainState.is_students_loading,
                    rx.el.div(
                        rx.spinner(class_name="h-4 w-4"),
                        "Loading...",
                        class_name="flex items-center gap-2",
                    ),
                    "Load Students",
                ),
                on_click=MainState.load_students,
                disabled=MainState.is_load_button_disabled
                | MainState.is_students_loading,
                class_name="mt-4 px-6 py-2 bg-sky-600 text-white font-semibold rounded-lg shadow-md hover:bg-sky-700 disabled:bg-sky-300 disabled:cursor-not-allowed transition-colors",
            ),
            class_name="p-6 bg-white border border-gray-200 rounded-xl shadow-sm",
        ),
        rx.cond(
            MainState.students.length() > 0,
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Student List", class_name="text-lg font-semibold text-gray-800"
                    ),
                    rx.el.div(
                        add_activity_dialog(),
                        rx.el.button(
                            rx.icon("circle_plus", class_name="mr-2 h-4 w-4"),
                            "Add Activity",
                            on_click=lambda: MainState.toggle_add_activity_dialog(True),
                            class_name="flex items-center px-4 py-2 bg-sky-600 text-white font-medium rounded-lg hover:bg-sky-700 transition-colors",
                        ),
                        class_name="flex justify-end",
                    ),
                    class_name="flex justify-between items-center mb-4",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "First Name",
                                    class_name="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sticky left-0 bg-gray-50 z-20",
                                ),
                                rx.el.th(
                                    "Last Name",
                                    class_name="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sticky left-[120px] bg-gray-50 z-20",
                                ),
                                rx.el.th(
                                    "ID Card",
                                    class_name="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                ),
                                rx.foreach(
                                    MainState.activities,
                                    lambda act: rx.el.th(
                                        rx.el.div(
                                            rx.el.p(
                                                act["description"],
                                                class_name="font-semibold text-gray-700 text-sm",
                                            ),
                                            rx.el.p(
                                                act["date"],
                                                class_name="font-normal text-gray-500 text-xs",
                                            ),
                                            class_name="flex flex-col text-center",
                                        ),
                                        class_name="px-4 py-2 min-w-[150px]",
                                    ),
                                ),
                                class_name="bg-gray-50",
                            )
                        ),
                        rx.el.tbody(rx.foreach(MainState.students, _student_row)),
                        class_name="min-w-full divide-y divide-gray-200",
                    ),
                    class_name="overflow-x-auto border border-gray-200 rounded-lg shadow-sm",
                ),
                class_name="mt-8",
            ),
            rx.cond(
                MainState.is_students_loading,
                rx.el.div(
                    rx.spinner(class_name="h-8 w-8 text-sky-500"),
                    rx.el.p("Loading students...", class_name="mt-2 text-gray-500"),
                    class_name="mt-8 flex flex-col items-center justify-center p-6 border-2 border-dashed rounded-lg",
                ),
                None,
            ),
        ),
    )