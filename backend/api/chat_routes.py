from fastapi import APIRouter
from pydantic import BaseModel

from ai.chat import ask_llm

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    history: list = []
    mode: str = "learn"
class DocumentChatRequest(BaseModel):
    file_id: int
    question: str
    history: list = []
    mode: str = "learn"
@router.post("/chat")
def chat(request: ChatRequest):

    return ask_llm(
    request.question,
    request.history,
    request.mode
)   
@router.post("/document-chat")
def document_chat(request: DocumentChatRequest):

    return ask_llm(
        question=request.question,
        history=request.history,
        mode=request.mode,
        file_id=request.file_id
    )