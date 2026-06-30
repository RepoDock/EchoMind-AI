from fastapi import APIRouter
from pydantic import BaseModel

from ai.chat import ask_llm

router = APIRouter()

class ChatRequest(BaseModel):
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