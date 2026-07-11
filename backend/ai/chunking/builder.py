"""
Universal Chunking Engine - Chunk Builder

Responsible for creating Chunk objects and attaching
metadata.

Author: AXON AI
"""

from __future__ import annotations

import uuid
from typing import List

from ai.chunking.metadata import MetadataBuilder
from ai.chunking.models import (
    Chunk,
    DocumentInfo,
    HeadingNode,
    TextSegment,
)


class ChunkBuilder:
    """
    Builds final Chunk objects.
    """

    def __init__(self):

        self.metadata_builder = MetadataBuilder()

    # --------------------------------------------------------
    # Public API
    # --------------------------------------------------------

    def build_chunk(
        self,
        *,
        text: str,
        document: DocumentInfo,
        headings: List[HeadingNode] | None = None,
        page: int | None = None,
        start_char: int = 0,
        end_char: int | None = None,
    ) -> Chunk:

        metadata = self.metadata_builder.build(
            text=text,
            document=document,
            headings=headings,
            page=page,
            start_char=start_char,
            end_char=end_char,
        )

        return Chunk(
            chunk_id=self._generate_chunk_id(),
            text=text.strip(),
            document=document,
            metadata=metadata,
        )

    # --------------------------------------------------------
    # Batch Builder
    # --------------------------------------------------------

    def build_segments(

    # -----------------------        
        self,
        segments: List[TextSegment],
        document: DocumentInfo,
    ) -> List[Chunk]:

        chunks: List[Chunk] = []

        for segment in segments:

            chunk = self.build_chunk(

                text=segment.text,

                document=document,

                headings=segment.headings,

                page=segment.page,

                start_char=segment.start_char,

                end_char=segment.end_char,

            )

            chunks.append(chunk)

        self.metadata_builder.link_chunks(chunks)

        return chunks
    
    
    # Chunk Cleanup
    # --------------------------------------------------------

    def remove_empty(
        self,
        chunks: List[Chunk],
    ) -> List[Chunk]:

        return [

            chunk

            for chunk in chunks

            if chunk.text.strip()

        ]

    def remove_duplicates(
        self,
        chunks: List[Chunk],
    ) -> List[Chunk]:

        unique = []

        seen = set()

        for chunk in chunks:

            fingerprint = chunk.metadata.extra[
                "content_hash"
            ]

            if fingerprint in seen:

                continue

            seen.add(fingerprint)

            unique.append(chunk)

        return unique

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    def statistics(
        self,
        chunks: List[Chunk],
    ) -> dict:

        return self.metadata_builder.statistics(
            chunks
        )

    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------

    def _generate_chunk_id(
        self,
    ) -> str:

        return str(uuid.uuid4())