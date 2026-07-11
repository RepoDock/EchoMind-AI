"""
Universal Chunking Engine - Tokenizer

Provides a unified interface for counting tokens.

Priority:
1. tiktoken
2. HuggingFace Tokenizer
3. Fallback Estimator
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)


# ==========================================================
# Base Tokenizer
# ==========================================================

class BaseTokenizer(ABC):
    """
    Abstract tokenizer interface.
    """

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        pass


# ==========================================================
# TikToken Tokenizer
# ==========================================================

class TikTokenTokenizer(BaseTokenizer):

    def __init__(self):

        import tiktoken

        try:
            self.encoding = tiktoken.get_encoding("cl100k_base")

        except Exception:

            self.encoding = tiktoken.encoding_for_model(
                "gpt-4"
            )

    def count_tokens(self, text: str) -> int:

        if not text:
            return 0

        return len(self.encoding.encode(text))


# ==========================================================
# HuggingFace Tokenizer
# ==========================================================

class HFTokenizer(BaseTokenizer):

    def __init__(self):

        from transformers import AutoTokenizer

        self.tokenizer = AutoTokenizer.from_pretrained(
            "bert-base-uncased"
        )

    def count_tokens(self, text: str) -> int:

        if not text:
            return 0

        return len(
            self.tokenizer.encode(
                text,
                add_special_tokens=False,
            )
        )


# ==========================================================
# Fallback Tokenizer
# ==========================================================

class FallbackTokenizer(BaseTokenizer):

    def count_tokens(self, text: str) -> int:

        if not text:
            return 0

        words = len(text.split())

        return max(
            1,
            int(words * 1.3),
        )


# ==========================================================
# Factory
# ==========================================================

@lru_cache(maxsize=1)
def get_tokenizer() -> BaseTokenizer:

    try:

        logger.info(
            "Using TikToken tokenizer."
        )

        return TikTokenTokenizer()

    except Exception:

        logger.warning(
            "TikToken unavailable."
        )

    try:

        logger.info(
            "Using HuggingFace tokenizer."
        )

        return HFTokenizer()

    except Exception:

        logger.warning(
            "HF tokenizer unavailable."
        )

    logger.info(
        "Using fallback tokenizer."
    )

    return FallbackTokenizer()


# ==========================================================
# Public API
# ==========================================================

def count_tokens(text: str) -> int:
    """
    Count tokens using the best available tokenizer.
    """

    tokenizer = get_tokenizer()

    return tokenizer.count_tokens(text)