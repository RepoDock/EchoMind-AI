from fastapi import APIRouter
from pydantic import BaseModel
import os
import subprocess

router = APIRouter()

class FileRequest(BaseModel):
    path: str


@router.post("/open")
def open_file(request: FileRequest):
    os.startfile(request.path)
    return {"status": "opened"}


@router.post("/show")
def show_file(request: FileRequest):
    subprocess.run([
        "explorer",
        "/select,",
        request.path
    ])
    return {"status": "shown"}