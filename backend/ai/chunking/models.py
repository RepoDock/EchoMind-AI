"""
Universal Chunking Engine - Data Models
Author: AXON AI

Shared models used across chunking, retrieval, embeddings,
reranking, citations and memory.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

class TextSegment(BaseModel):
    """
    Intermediate representation produced by chunking strategies
    before Chunk objects are created.
    """

    text: str

    page: int | None = None

    start_char: int = 0
    end_char: int = 0

    headings: list[HeadingNode] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)
    
class HeadingNode(BaseModel):
    """
    Represents one heading in the heading hierarchy.
    """

    level: int
    title: str


class DocumentInfo(BaseModel):
    """
    Information about the source document.
    """

    document_id: str
    file_name: str
    file_path: str
    file_type: str

    file_size: int | None = None
    last_modified: datetime | None = None


class ChunkMetadata(BaseModel):
    """
    Metadata attached to every chunk.
    """

    page: int | None = None

    start_char: int
    end_char: int

    chunk_index: int
    total_chunks: int

    token_count: int = 0
    character_count: int = 0
    paragraph_count: int = 0

    headings: list[HeadingNode] = Field(default_factory=list)

    previous_chunk: str | None = None
    next_chunk: str | None = None

    extra: dict[str, Any] = Field(default_factory=dict)


class Chunk(BaseModel):
    """
    Final chunk object produced by the engine.
    """

    chunk_id: str

    text: str

    document: DocumentInfo

    metadata: ChunkMetadata


class ChunkResult(BaseModel):
    """
    Returned after chunking a document.
    """

    document: DocumentInfo

    chunks: list[Chunk]

    created_at: datetime = Field(default_factory=datetime.utcnow)