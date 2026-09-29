from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_report(path, student, summary, analytics, plan=""):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(path), pagesize=A4)
    safe = lambda x: x.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>")
    story = [
        Paragraph("SnapLearn AI - Student Learning Report", styles["Title"]),
        Paragraph(f"Student: {safe(student)}", styles["Normal"]),
        Spacer(1,12), Paragraph("AI Summary", styles["Heading2"]),
        Paragraph(safe(summary), styles["BodyText"]),
        Spacer(1,12), Paragraph("Analytics", styles["Heading2"]),
        Paragraph(safe(analytics), styles["BodyText"])
    ]
    if plan:
        story += [Spacer(1,12), Paragraph("Study Plan", styles["Heading2"]), Paragraph(safe(plan), styles["BodyText"])]
    doc.build(story)
