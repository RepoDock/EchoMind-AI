"""
Universal Chunking Engine - Document Analyzer

Analyzes a document before chunking.

Responsibilities:
- Detect document type
- Detect structure
- Detect headings
- Detect tables
- Detect code
- Recommend chunking strategy
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ai.chunking.models import DocumentInfo


@dataclass(slots=True)
class DocumentAnalysis:

    document_type: str

    strategy: str

    has_headings: bool

    has_tables: bool

    has_code: bool

    estimated_language: str

    paragraph_count: int

    line_count: int


class DocumentAnalyzer:

    HEADING_PATTERN = re.compile(
        r"^(#{1,6}\s+.+|[A-Z][A-Za-z0-9\s]{2,80}:?)$",
        re.MULTILINE,
    )

    TABLE_PATTERN = re.compile(
        r"\|.*\|"
    )

    CODE_PATTERN = re.compile(
        r"(class\s+\w+|def\s+\w+\(|public\s+class|#include)"
    )

    def analyze(
        self,
        text: str,
        document: DocumentInfo,
    ) -> DocumentAnalysis:

        file_type = (
            document.file_type.lower()
            if document.file_type
            else "txt"
        )

        return DocumentAnalysis(

            document_type=file_type,

            strategy=self._select_strategy(
                file_type,
            ),

            has_headings=self._has_headings(text),

            has_tables=self._has_tables(text),

            has_code=self._has_code(text),

            estimated_language=self._language(text),

            paragraph_count=self._paragraphs(text),

            line_count=len(text.splitlines()),
        )

    # -------------------------------------------------

    def _select_strategy(
        self,
        file_type: str,
    ) -> str:

        mapping = {

            "pdf": "paragraph",

            "docx": "paragraph",

            "doc": "paragraph",

            "txt": "paragraph",

            "md": "markdown",

            "py": "code",

            "java": "code",

            "cpp": "code",

            "c": "code",

            "html": "markdown",

            "htm": "markdown",

        }

        return mapping.get(
            file_type,
            "paragraph",
        )

    # -------------------------------------------------

    def _has_headings(
        self,
        text: str,
    ) -> bool:

        return bool(
            self.HEADING_PATTERN.search(text)
        )

    def _has_tables(
        self,
        text: str,
    ) -> bool:

        return bool(
            self.TABLE_PATTERN.search(text)
        )

    def _has_code(
        self,
        text: str,
    ) -> bool:

        return bool(
            self.CODE_PATTERN.search(text)
        )

    def _paragraphs(
        self,
        text: str,
    ) -> int:

        return len(
            [

                p

                for p in re.split(
                    r"\n\s*\n",
                    text,
                )

                if p.strip()

            ]
        )

    def _language(
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