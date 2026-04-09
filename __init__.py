import reflex as rx
from .ui import index
from .styles import base_style

app = rx.App(style=base_style)
app.add_page(index)
