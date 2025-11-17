import reflex as rx
from app.states.main_state import MainState
from app.components.login import login_form
from app.components.dashboard import dashboard_view


def index() -> rx.Component:
    """The main app view, conditionally rendering login or dashboard."""
    return rx.el.div(
        rx.cond(MainState.is_authenticated, dashboard_view(), login_form()),
        class_name="font-['Roboto']",
    )


app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="sky",
        gray_color="gray",
        panel_background="solid",
        radius="large",
    ),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")