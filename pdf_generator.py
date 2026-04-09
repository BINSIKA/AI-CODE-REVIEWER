from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(path, review):
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    story = []

    for line in review.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1,12))

    doc.build(story)
