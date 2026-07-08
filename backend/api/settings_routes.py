from fastapi import APIRouter
from pydantic import BaseModel

from database.crud import (
    save_scan_folder,
    get_scan_folder
)
from tkinter import Tk
from tkinter.filedialog import askdirectory

router = APIRouter()


class FolderRequest(BaseModel):
    folder: str

@router.get("/scan-folder")
def scan_folder():

    return {
        "folder": get_scan_folder()
    }
@router.get("/folder")
def folder():

    return {
        "folder": get_scan_folder()
    }


@router.post("/folder")
def save(request: FolderRequest):

    save_scan_folder(request.folder)

    return {
        "status": "saved"
    }
@router.get("/browse")
def browse_folder():

    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    folder = askdirectory()

    root.destroy()

    return {
        "folder": folder
    }