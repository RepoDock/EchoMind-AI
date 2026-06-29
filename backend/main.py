from fastapi import FastAPI
from api.search_routes import router as search_router
from config import APP_NAME, APP_VERSION

import database.database

from api.scanner_routes import router as scanner_router

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
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