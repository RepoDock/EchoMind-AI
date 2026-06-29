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
import os
from database.connection import cursor

@router.get("/stats")
def get_stats():

    cursor.execute("SELECT path FROM files")
    rows = cursor.fetchall()

    files = len(rows)

    folders = len(set(os.path.dirname(row[0]) for row in rows))

    return {
        "files": files,
        "folders": folders,
        "indexed": 100
    }
# from database.connection import cursor

# @router.get("/stats")
# def get_stats():

#     cursor.execute("SELECT COUNT(*) FROM files")
#     files = cursor.fetchone()[0]

#     cursor.execute("SELECT COUNT(DISTINCT path) FROM files")
#     folders = cursor.fetchone()[0]

#     return {
#         "files": files,
#         "folders": folders,
#         "indexed": 100
#     }
