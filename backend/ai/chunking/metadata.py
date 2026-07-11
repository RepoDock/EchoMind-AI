"""
Universal Chunking Engine - Metadata Builder

Responsible for generating and enriching metadata
for every chunk.
"""

from __future__ import annotations

import hashlib
from typing import List

from ai.chunking.models import (
    Chunk,
    ChunkMetadata,
    DocumentInfo,
    HeadingNode,
)

from ai.chunking.tokenizer import count_tokens


class MetadataBuilder:
    """
    Builds metadata for chunk objects.
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def build(
        self,
        *,
        text: str,
        document: DocumentInfo,
        headings: List[HeadingNode] | None = None,
        chunk_index: int = 0,
        total_chunks: int = 0,
        page: int | None = None,
        start_char: int = 0,
        end_char: int | None = None,
    ) -> ChunkMetadata:

        if end_char is None:
            end_char = len(text)

        metadata = ChunkMetadata(

            page=page,

            start_char=start_char,
            end_char=end_char,

            chunk_index=chunk_index,
            total_chunks=total_chunks,

            token_count=count_tokens(text),
            character_count=len(text),

            paragraph_count=self._count_paragraphs(text),

            headings=headings or [],
        )

        metadata.extra = {

            "document_hash": self.document_hash(document),

            "content_hash": self.content_hash(text),

            "word_count": len(text.split()),

            "line_count": len(text.splitlines()),

            "language": self.detect_language(text),

        }

        return metadata

    # ---------------------------------------------------------
    # Hashes
    # ---------------------------------------------------------

    def document_hash(
        self,
        document: DocumentInfo,
    ) -> str:

        raw = (
            f"{document.file_path}|"
            f"{document.file_name}|"
            f"{document.file_type}"
        )

        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()

    def content_hash(
        self,
        text: str,
    ) -> str:

        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _count_paragraphs(
        self,
        text: str,
    ) -> int:

        paragraphs = [

            p

            for p in text.split("\n\n")

            if p.strip()

        ]

        return len(paragraphs)

    def detect_language(
        self,
        text: str,
    ) -> str:

        if not text:
            return "unknown"

        ascii_chars = sum(

            1

            for c in text

            if ord(c) < 128

        )

        ratio = ascii_chars / max(
            len(text),
            1,
        )

        if ratio > 0.90:
            return "english"

        return "multilingual"

    # ---------------------------------------------------------
    # Linking
    # ---------------------------------------------------------

    def link_chunks(
        self,
        chunks: List[Chunk],
    ) -> None:

        total = len(chunks)

        for index, chunk in enumerate(chunks):

            chunk.metadata.chunk_index = index + 1

            chunk.metadata.total_chunks = total

            if index > 0:

                chunk.metadata.previous_chunk = (

                    chunks[index - 1].chunk_id

                )

            if index < total - 1:

                chunk.metadata.next_chunk = (

                    chunks[index + 1].chunk_id

                )

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(
        self,
        chunks: List[Chunk],
    ) -> dict:

        if not chunks:

            return {}

        token_counts = [

            c.metadata.token_count

            for c in chunks

        ]

        char_counts = [

            c.metadata.character_count

            for c in chunks

        ]

        return {

            "total_chunks": len(chunks),

            "total_tokens": sum(token_counts),

            "average_tokens": (
                sum(token_counts) / len(token_counts)
            ),

            "largest_chunk": max(token_counts),

            "smallest_chunk": min(token_counts),

            "average_characters": (
                sum(char_counts) / len(char_counts)
            ),
        }