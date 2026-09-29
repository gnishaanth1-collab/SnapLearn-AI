from pathlib import Path
import fitz
from docx import Document
from pptx import Presentation

def extract_text(path: str) -> str:
    p = Path(path)
    ext = p.suffix.lower()
    if ext == ".pdf":
        doc = fitz.open(str(p))
        return "\n".join(page.get_text() for page in doc)
    if ext == ".docx":
        doc = Document(str(p))
        return "\n".join(x.text for x in doc.paragraphs)
    if ext == ".pptx":
        prs = Presentation(str(p))
        out = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    out.append(shape.text)
        return "\n".join(out)
    if ext == ".txt":
        return p.read_text(encoding="utf-8", errors="ignore")
    raise ValueError("Supported files: PDF, DOCX, PPTX, TXT")

def chunk_text(text: str, size=900, overlap=120):
    text = " ".join(text.split())
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks
