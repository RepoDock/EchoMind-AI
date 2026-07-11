"""
Universal Chunking Engine - Chunk Validator

Responsible for validating and cleaning generated chunks.
"""

from __future__ import annotations

from ai.chunking.config import ChunkingConfig
from ai.chunking.models import Chunk


class ChunkValidator:
    """
    Validates generated chunks before they are indexed.
    """

    def __init__(self, config: ChunkingConfig):
        self.config = config

    # --------------------------------------------------------
    # Public API
    # --------------------------------------------------------

    def validate(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:

        chunks = self._remove_empty(chunks)

        if self.config.remove_duplicate_chunks:
            chunks = self._remove_duplicates(chunks)

        chunks = self._remove_invalid(chunks)

        self._renumber(chunks)

        return chunks

    # --------------------------------------------------------
    # Empty Chunks
    # --------------------------------------------------------

    def _remove_empty(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:

        return [

            chunk

            for chunk in chunks

            if chunk.text.strip()

        ]

    # --------------------------------------------------------
    # Duplicate Chunks
    # --------------------------------------------------------

    def _remove_duplicates(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:

        seen = set()

        unique = []

        for chunk in chunks:

            fingerprint = chunk.metadata.extra.get(
                "content_hash"
            )

            if fingerprint in seen:
                continue

            seen.add(fingerprint)

            unique.append(chunk)

        return unique

    # --------------------------------------------------------
    # Invalid Chunks
    # --------------------------------------------------------

    def _remove_invalid(
        self,
        chunks: list[Chunk],
    ) -> list[Chunk]:

        valid = []

        for chunk in chunks:

            tokens = chunk.metadata.token_count


            if tokens > self.config.max_tokens:
                continue

            valid.append(chunk)

        return valid

    # --------------------------------------------------------
    # Re-number chunks
    # --------------------------------------------------------

    def _renumber(
        self,
        chunks: list[Chunk],
    ) -> None:

        total = len(chunks)

        for index, chunk in enumerate(chunks):

            chunk.metadata.chunk_index = index + 1

            chunk.metadata.total_chunks = total

            if index > 0:

                chunk.metadata.previous_chunk = (
                    chunks[index - 1].chunk_id
                )

            else:

                chunk.metadata.previous_chunk = None

            if index < total - 1:

                chunk.metadata.next_chunk = (
                    chunks[index + 1].chunk_id
                )

            else:

                chunk.metadata.next_chunk = None