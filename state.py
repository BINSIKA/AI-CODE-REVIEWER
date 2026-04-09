import reflex as rx
from pathlib import Path

from .llm import ai_review
from .analyzer import syntax_check, format_code, calculate_score
from .pdf_generator import create_pdf

class State(rx.State):

    code: str = ""
    language: str = "Python"
    review: str = ""
    syntax: str = ""
    formatted: str = ""
    score: int = 0
    loading: bool = False
    pdf_ready: bool = False

    async def upload_file(self, files):
        file = files[0]
        content = await file.read()
        self.code = content.decode()

    async def analyze(self):
        self.loading = True
        self.syntax = syntax_check(self.code, self.language)
        self.formatted = format_code(self.code, self.language)
        self.review = ai_review(self.code, self.language)
        self.score = calculate_score(self.code, self.review)
        self.loading = False

    def generate_pdf(self):
        Path("downloads").mkdir(exist_ok=True)
        path = "downloads/review.pdf"
        create_pdf(path, self.review)
        self.pdf_ready = True
