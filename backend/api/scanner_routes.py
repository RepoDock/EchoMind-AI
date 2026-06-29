from fastapi import APIRouter
from pydantic import BaseModel

from scanner.scanner import scan_folder
from database.crud import insert_file

router = APIRouter()


class ScanRequest(BaseModel):
    folder_path: str


@router.post("/scan")
def scan(request: ScanRequest):

    files = scan_folder(request.folder_path)

    for file in files:
        insert_file(file)

    return {
        "status": "success",
        "files_indexed": len(files)
    }