import reflex as rx
from app.states.main_state import MainState


def login_form() -> rx.Component:
    """The login form component."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("book-marked", class_name="h-8 w-8 text-sky-500"),
                rx.el.h1(
                    "Teacher's Portal", class_name="text-2xl font-bold text-gray-800"
                ),
                class_name="flex items-center gap-3 mb-8",
            ),
            rx.el.p(
                "Welcome back! Please sign in to access your dashboard.",
                class_name="text-sm text-gray-600 mb-6",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Email",
                        html_for="email",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        id="email",
                        name="email",
                        type="email",
                        placeholder="carlos@gmail.com",
                        class_name="mt-1 w-full px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password",
                        html_for="password",
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        id="password",
                        name="password",
                        type="password",
                        placeholder="••••••••",
                        class_name="mt-1 w-full px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-sky-500 focus:border-sky-500 transition",
                    ),
                    class_name="mb-6",
                ),
                rx.cond(
                    MainState.login_error != "",
                    rx.el.div(
                        rx.icon("badge_alert", class_name="h-5 w-5 mr-2"),
                        rx.el.span(MainState.login_error),
                        class_name="flex items-center p-3 mb-4 text-sm text-red-700 bg-red-100 rounded-lg",
                    ),
                    None,
                ),
                rx.el.button(
                    rx.cond(
                        MainState.is_loading,
                        rx.el.div(
                            rx.spinner(class_name="text-white h-5 w-5"),
                            "Signing In...",
                            class_name="flex items-center gap-2",
                        ),
                        rx.el.div(
                            "Sign In",
                            rx.icon("arrow-right", class_name="ml-2 h-4 w-4"),
                            class_name="flex items-center",
                        ),
                    ),
                    type="submit",
                    disabled=MainState.is_loading,
                    class_name="w-full flex justify-center py-3 px-4 bg-sky-600 text-white font-semibold rounded-lg shadow-md hover:bg-sky-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 transition-all duration-200 disabled:bg-sky-300",
                ),
                on_submit=MainState.handle_login,
                reset_on_submit=False,
            ),
            class_name="w-full max-w-md p-8 bg-white rounded-2xl shadow-xl border border-gray-100",
        ),
        class_name="min-h-screen w-full flex items-center justify-center bg-gray-50",
    )