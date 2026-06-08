from fastapi import APIRouter
from pydantic import BaseModel
from services.rag_service import chat_with_rag

router = APIRouter(prefix="/api/chat", tags=["Chatbot RAG"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/", response_model=ChatResponse)
def chat(req: ChatRequest):
    reply = chat_with_rag(req.message)
    return ChatResponse(reply=reply)
