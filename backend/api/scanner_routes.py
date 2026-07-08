from utils.hashing import calculate_hash
from database.crud import update_file_hash
from fastapi import APIRouter
from pydantic import BaseModel
import os
from services.indexing_service import IndexingService
import json
from ai.chunker import chunk_text
from database.connection import connection, cursor
from ai.embedding import generate_embedding
from ai.metadata_extractor import extract_metadata
from database.connection import cursor
from database.crud import (
    insert_file,
    insert_document_chunk,
)

from database.content_crud import (
    insert_document_content,
)

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

        file_id = insert_file(file)

        print(file["path"])
        print(os.path.exists(file["path"]))

        if document is None:
            print(f" Failed to read: {file['name']}")
            continue

        if not document["text"].strip():
            print(f"No text found in {file['name']}")
            continue
        # -------------------------
        # Extract Metadata
        # -------------------------
        metadata = extract_metadata(
            document["text"],
            file["name"]
        )

        document.update(metadata)

        insert_document_content(
            file_id,
            document
        )

        total_chunks = 0

        for page in document["page_data"]:

            chunks = chunk_text(page["text"])

            for index, chunk in enumerate(chunks):

                if not chunk.strip():
                    continue

                embedding = generate_embedding(chunk)

                if not embedding:
                    continue

                chunk_id = insert_document_chunk(
                    file_id,
                    page["page"],
                    index,
                    chunk,
                    json.dumps(embedding)
                )


                total_chunks += 1

        print(f" Indexed {total_chunks} chunks")
        update_file_hash(
            file["path"],
            calculate_hash(file["path"])
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
