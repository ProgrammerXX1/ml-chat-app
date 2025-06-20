
from pathlib import Path
import fitz  # PyMuPDF
import docx

def read_file(filepath: str) -> str:
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {filepath}")

    if path.suffix == ".txt":
        return path.read_text(encoding="utf-8")

    elif path.suffix == ".pdf":
        text = ""
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
        return text

    elif path.suffix == ".docx":
        doc = docx.Document(filepath)
        return "\n".join(p.text for p in doc.paragraphs)

    else:
        raise ValueError("Поддерживаются только .txt, .pdf, .docx")
