from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from app.ml_api import get_ml_response, store_uploaded_text
from PyPDF2 import PdfReader
import docx
import io
router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    response = get_ml_response(request.message)
    return {"response": response}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    ext = file.filename.split(".")[-1].lower()

    if ext == "pdf":
        reader = PdfReader(io.BytesIO(contents))
        text = "\n".join([page.extract_text() for page in reader.pages])
    elif ext == "docx":
        doc = docx.Document(io.BytesIO(contents))  # 👈 обернули в BytesIO
        text = "\n".join([p.text for p in doc.paragraphs])
    else:
        return {"error": "Unsupported file type"}

    store_uploaded_text(text)
    return {"status": "Файл загружен", "length": len(text)}