from fastapi import APIRouter
from pydantic import BaseModel
import os
import json
from ai.chunker import chunk_text
from scanner.scanner import scan_folder

from ai.extractor import extract_text
from ai.embedding import generate_embedding

from database.connection import cursor
from database.crud import (
    insert_file,
    insert_document_content,
)

router = APIRouter()


class ScanRequest(BaseModel):
    folder_path: str

@router.post("/scan")
def scan(request: ScanRequest):

    files = scan_folder(request.folder_path)

    for file in files:

        file_id = insert_file(file)

        text = extract_text(file["path"])

        if not text.strip():
            print(f"⚠ No text found in {file['name']}")
            continue

        chunks = chunk_text(text)

        print(f"📄 {file['name']} -> {len(chunks)} chunks")
        for index, chunk in enumerate(chunks):

            if not chunk.strip():
                continue

            embedding = generate_embedding(chunk)

            if not embedding:
                continue

            insert_document_content(
                file_id,
                index,
                chunk,
                json.dumps(embedding)
            )
        

        print(f"✅ Indexed {len(chunks)} chunks")

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