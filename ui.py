import reflex as rx
from .state import State

def index():
    return rx.container(
        rx.heading("🚀 AI Code Reviewer PRO", size="8"),

        rx.select(
            ["Python", "JavaScript", "Java", "C++"],
            value=State.language,
            on_change=State.set_language,
        ),

        rx.upload(
            rx.button("Upload File"),
            on_drop=State.upload_file,
        ),

        rx.text_area(
            value=State.code,
            on_change=State.set_code,
            height="300px",
        ),

        rx.button(
            "Analyze Code",
            on_click=State.analyze,
            loading=State.loading,
        ),

        rx.divider(),

        rx.heading("Syntax Result"),
        rx.text(State.syntax),

        rx.heading("Code Score"),
        rx.heading(State.score),

        rx.heading("Formatted Code"),
        rx.code_block(State.formatted),

        rx.heading("AI Review"),
        rx.text(State.review),

        rx.button(
            "Download PDF Report",
            on_click=State.generate_pdf,
        ),

        rx.cond(
            State.pdf_ready,
            rx.link("Download PDF", href="/downloads/review.pdf"),
        ),

        padding="40px",
        max_width="900px",
    )
