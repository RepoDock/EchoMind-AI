"""
Universal Chunking Engine - Strategy Factory

Responsible for selecting the appropriate chunking strategy.
"""

from __future__ import annotations

from ai.chunking.config import ChunkingConfig
from ai.chunking.strategies.base import BaseChunkStrategy
from ai.chunking.strategies.paragraph import ParagraphChunkStrategy


class ChunkStrategyFactory:
    """
    Factory responsible for creating chunking strategies.
    """

    def __init__(self, config: ChunkingConfig):
        self.config = config

        self._strategies = {
            "paragraph": ParagraphChunkStrategy,
            # Future Strategies
            # "markdown": MarkdownChunkStrategy,
            # "code": CodeChunkStrategy,
            # "table": TableChunkStrategy,
            # "recursive": RecursiveChunkStrategy,
        }

    def get_strategy(
        self,
        strategy_name: str,
    ) -> BaseChunkStrategy:
        """
        Return a strategy instance.

        Args:
            strategy_name:
                Name returned by DocumentAnalyzer.

        Returns:
            BaseChunkStrategy
        """

        strategy_name = (
            strategy_name or "paragraph"
        ).lower()

        strategy_cls = self._strategies.get(
            strategy_name,
            ParagraphChunkStrategy,
        )

        return strategy_cls(self.config)

    def register_strategy(
        self,
        name: str,
        strategy: type[BaseChunkStrategy],
    ) -> None:
        """
        Register a new strategy at runtime.
        """

        self._strategies[name.lower()] = strategy

    def available_strategies(
        self,
    ) -> list[str]:
        """
        Return all registered strategies.
        """

        return sorted(self._strategies.keys())