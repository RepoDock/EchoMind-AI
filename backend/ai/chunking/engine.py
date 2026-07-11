"""
Universal Chunking Engine

Main orchestration engine responsible for:

- Document Analysis
- Strategy Selection
- Chunk Generation
- Validation

Business logic does NOT belong here.
"""

from __future__ import annotations

import logging

from ai.chunking.analyzer import DocumentAnalyzer
from ai.chunking.config import ChunkingConfig, DEFAULT_CONFIG
from ai.chunking.factory import ChunkStrategyFactory
from ai.chunking.models import ChunkResult, DocumentInfo
from ai.chunking.validator import ChunkValidator

logger = logging.getLogger(__name__)


class UniversalChunkingEngine:
    """
    Enterprise-grade chunking engine.
    """

    def __init__(
        self,
        config: ChunkingConfig | None = None,
    ):

        self.config = config or DEFAULT_CONFIG

        self.analyzer = DocumentAnalyzer()

        self.factory = ChunkStrategyFactory(
            self.config
        )

        self.validator = ChunkValidator(
            self.config
        )

    def chunk_document(
        self,
        text: str,
        document: DocumentInfo,
    ) -> ChunkResult:
        """
        Chunk an entire document.
        """

        logger.info(
            "Chunking document: %s",
            document.file_name,
        )

        # ---------------------------------------
        # Analyze document
        # ---------------------------------------

        analysis = self.analyzer.analyze(
            text=text,
            document=document,
        )

        logger.info(
            "Detected strategy: %s",
            analysis.strategy,
        )

        # ---------------------------------------
        # Select strategy
        # ---------------------------------------

        strategy = self.factory.get_strategy(
            analysis.strategy
        )

        # ---------------------------------------
        # Chunk document
        # ---------------------------------------

        chunks = strategy.chunk(
            text=text,
            document=document,
        )

        # ---------------------------------------
        # Validate
        # ---------------------------------------

        chunks = self.validator.validate(
            chunks
        )

        logger.info(
            "Generated %d chunks",
            len(chunks),
        )

        return ChunkResult(
            document=document,
            chunks=chunks,
        )