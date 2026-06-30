from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import APP_NAME, APP_VERSION
import database.database
from api.settings_routes import router as settings_router
from api.search_routes import router as search_router
from api.scanner_routes import router as scanner_router
from api.file_routes import router as file_router
from api.ai_routes import router as ai_router
from api.chat_routes import router as chat_router
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)
app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)
app.include_router(
    ai_router,
    prefix="/ai",
    tags=["AI"]
)
app.include_router(
    settings_router,
    prefix="/settings",
    tags=["Settings"]
)
app.include_router(
    file_router,
    prefix="/files",
    tags=["Files"]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router)

app.include_router(
    scanner_router,
    prefix="/scanner",
    tags=["Scanner"]
)

@app.get("/")
def home():
    return {
        "project": APP_NAME,
        "version": APP_VERSION,
        "status": "Running"
    }