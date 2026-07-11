"""
Compatibility wrapper for the Universal Chunking Engine.

Existing code can continue calling:

    chunk_text(text)

without knowing about the new engine.
"""
from __future__ import annotations

from ai.chunking.engine import UniversalChunkingEngine
from ai.chunking.models import DocumentInfo
import uuid


_engine = UniversalChunkingEngine()


def chunk_text(
    text: str,
    *,
    file_name: str = "document.txt",
    file_path: str = "",
    file_type: str = "txt",
):

    if not text.strip():
        return []

    document = DocumentInfo(

        document_id=str(uuid.uuid4()),

        file_name=file_name,

        file_path=file_path,

        file_type=file_type,

    )

    result = _engine.chunk_document(
        text=text,
        document=document,
    )

    return result.chunks