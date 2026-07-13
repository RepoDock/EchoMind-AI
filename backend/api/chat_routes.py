from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from ai.chat import ask_llm, ask_llm_stream

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
@router.post("/document-chat-stream")
def document_chat_stream(request: DocumentChatRequest):

    return StreamingResponse(
        ask_llm_stream(
            question=request.question,
            history=request.history,
            mode=request.mode,
            file_id=request.file_id
        ),
        media_type="text/plain"
    )
@router.post("/document-chat")
def document_chat(request: DocumentChatRequest):

    return ask_llm(
        question=request.question,
        history=request.history,
        mode=request.mode,
        file_id=request.file_id
    )

@router.post("/chat-stream")
def chat_stream(request: ChatRequest):

    return StreamingResponse(
        ask_llm_stream(
            question=request.question,
            history=request.history,
            mode=request.mode
        ),
        media_type="text/plain"
    )