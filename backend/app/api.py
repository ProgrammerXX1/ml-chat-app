# backend/app/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.ml_api import get_ml_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    response = get_ml_response(request.message)
    return {"response": response}
