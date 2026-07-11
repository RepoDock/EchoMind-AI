"""
Universal Chunking Engine Configuration
"""

from pydantic import BaseModel


class ChunkingConfig(BaseModel):
    """
    Central configuration for the Universal Chunking Engine.
    """

    # -----------------------
    # Chunk Size
    # -----------------------

    target_tokens: int = 512
    max_tokens: int = 768
    min_tokens: int = 128

    # -----------------------
    # Overlap
    # -----------------------

    overlap_tokens: int = 64

    # -----------------------
    # Paragraph Rules
    # -----------------------

    merge_small_paragraphs: bool = True
    min_paragraph_length: int = 80

    # -----------------------
    # Heading Detection
    # -----------------------

    detect_headings: bool = True
    max_heading_depth: int = 6

    # -----------------------
    # Validation
    # -----------------------

    remove_duplicate_chunks: bool = True
    remove_empty_chunks: bool = True

    # -----------------------
    # Metadata
    # -----------------------

    link_adjacent_chunks: bool = True
    calculate_statistics: bool = True

    # -----------------------
    # Future Features
    # -----------------------

    enable_semantic_chunking: bool = False
    enable_table_chunking: bool = True
    enable_code_chunking: bool = True
    enable_markdown_chunking: bool = True


DEFAULT_CONFIG = ChunkingConfig()