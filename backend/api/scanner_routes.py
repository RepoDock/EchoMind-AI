from fastapi import APIRouter
from pydantic import BaseModel
import os
from services.indexing_service import IndexingService
from database.connection import connection, cursor
from database.connection import cursor
router = APIRouter()
class ScanRequest(BaseModel):
    folder_path: str

@router.post("/scan")
def scan(request: ScanRequest):

    service = IndexingService()

    files = service.index_folder(request.folder_path)

    for item in files:

        file = item["file"]
        document = item["document"]

        service.store_document(
            file,
            document
        )
    return {
        "status": "success",
        "files_indexed": len(files)
    }
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
@router.post("/clear-data")
def clear_data():

    cursor.execute("DELETE FROM document_content")
    cursor.execute("DELETE FROM embeddings")
    cursor.execute("DELETE FROM search_history")
    cursor.execute("DELETE FROM files")
    cursor.execute("DELETE FROM document_chunks")

    connection.commit()

    return {
        "success": True,
        "message": "All indexed data cleared."
    }
