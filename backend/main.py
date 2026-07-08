
print("MAIN STARTED")
print("0")

import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

print("1")

import uvicorn

print("2")

from config import APP_NAME, APP_VERSION

print("3")

import database.database

print("4")

from api.settings_routes import router as settings_router
import time

print("5")

t = time.perf_counter()

from api.search_routes import router as search_router

print("6")
print(f"Search routes import time: {time.perf_counter() - t:.3f} sec")

from api.scanner_routes import router as scanner_router

print("7")

from api.file_routes import router as file_router

print("8")

from api.ai_routes import router as ai_router

print("9")

from api.chat_routes import router as chat_router

print("10")

from api.setup_routes import router as setup_router

print("11")

from fastapi import FastAPI

print("12")

from fastapi.middleware.cors import CORSMiddleware

print("13")

from fastapi import Request

print("14")

from fastapi.responses import JSONResponse

print("15")

import traceback

print("16")
print("MAIN STARTED")
async def all_exceptions(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )
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
    setup_router,
    prefix="/setup",
    tags=["Setup"]
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

@app.exception_handler(Exception)
async def all_exceptions(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )


@app.get("/")
def home():
    return {
        "project": APP_NAME,
        "version": APP_VERSION,
        "status": "Running"
    }
if __name__ == "__main__":
    print("STARTING UVICORN")

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_config=None,
        access_log=False
    )
