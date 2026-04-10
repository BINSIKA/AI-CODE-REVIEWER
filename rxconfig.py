import reflex as rx

config = rx.Config(
    app_name="ai_reviewer_app",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)
