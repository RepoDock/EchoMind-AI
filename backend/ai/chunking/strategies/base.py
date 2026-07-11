"""
Base interface for all chunking strategies.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ai.chunking.config import ChunkingConfig
from ai.chunking.models import Chunk, DocumentInfo


class BaseChunkStrategy(ABC):
    """
    Abstract base class for every chunking strategy.

    Every strategy (paragraph, markdown, code, table, etc.)
    must inherit from this class.
    """

    def __init__(self, config: ChunkingConfig):
        self.config = config

    @abstractmethod
    def chunk(
        self,
        text: str,
        document: DocumentInfo,
    ) -> list[Chunk]:
        """
        Split the given document into chunks.

        Args:
            text: Extracted document text.
            document: Source document metadata.

        Returns:
            List of Chunk objects.
        """
        raise NotImplementedError