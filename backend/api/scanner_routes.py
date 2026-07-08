from fastapi import APIRouter
from pydantic import BaseModel
import os
import json
from ai.chunker import chunk_text
from scanner.scanner import scan_folder
from database.connection import connection, cursor
from ai.extractor import extract_text
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

    files = scan_folder(request.folder_path)
    print("=" * 60)
    print("Detected Files:", len(files))

    for file in files:
        print(file["name"])

    print("=" * 60)

    for file in files:

        file_id = insert_file(file)

        print(file["path"])
        print(os.path.exists(file["path"]))
        try:
            document = extract_text(file["path"])
        except Exception as e:
            print(f" Failed to read {file['name']}: {e}")
            continue

        if document is None:
            print(f" Failed to read: {file['name']}")
            continue

        if not document["text"].strip():
            print(f" No text found in {file['name']}")
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
