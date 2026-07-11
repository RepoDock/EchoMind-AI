"""
Universal Chunking Engine - Paragraph Strategy

Production Version
"""

from __future__ import annotations

import logging
import re
import uuid

from typing import List

from ai.chunking.builder import ChunkBuilder
from ai.chunking.models import (
    DocumentInfo,
    HeadingNode,
    TextSegment,
    Chunk,
)
from ai.chunking.strategies.base import BaseChunkStrategy
from ai.chunking.tokenizer import count_tokens

logger = logging.getLogger(__name__)


class ParagraphChunkStrategy(BaseChunkStrategy):

    PARAGRAPH_PATTERN = re.compile(r"\n\s*\n+")

    SENTENCE_PATTERN = re.compile(
        r"(?<=[.!?])\s+"
    )

    HEADING_PATTERN = re.compile(
        r"^(#{1,6}\s+.+|[A-Z][A-Za-z0-9\s\-\(\):]{3,100}:?)$"
    )

    def __init__(self, config):

        super().__init__(config)

        self.builder = ChunkBuilder()

    # -------------------------------------------------

    def chunk(
        self,
        text: str,
        document: DocumentInfo,
    ) -> list[Chunk]:

        if not text.strip():

            return []

        paragraphs = self._extract_paragraphs(
            text
        )

        paragraphs = self._normalize(
            paragraphs
        )

        segments = self._segmentize(
            paragraphs
        )

        chunks = self.builder.build_segments(
            segments,
            document,
        )

        return chunks

    # -------------------------------------------------

    def _extract_paragraphs(
        self,
        text: str,
    ) -> List[str]:

        return [

            p.strip()

            for p in self.PARAGRAPH_PATTERN.split(text)

            if p.strip()

        ]

    # -------------------------------------------------

    def _normalize(
        self,
        paragraphs: List[str],
    ) -> List[str]:

        cleaned = []

        for paragraph in paragraphs:

            paragraph = re.sub(
                r"[ \t]+",
                " ",
                paragraph,
            )

            paragraph = paragraph.strip()

            if paragraph:

                cleaned.append(
                    paragraph
                )

        return cleaned

    # -------------------------------------------------

    def _segmentize(
        self,
        paragraphs: List[str],
    ) -> List[TextSegment]:

        """
        Main segmentation pipeline.

        Remaining implementation
        continues in Part-2.
        """

        segments = []

        heading_stack: List[HeadingNode] = []

        current_buffer = []

        current_tokens = 0

        offset = 0

        for paragraph in paragraphs:

            heading = self._detect_heading(
                paragraph
            )

            if heading:

                heading_stack = self._update_heading_stack(
                    heading_stack,
                    heading,
                )

            paragraph_tokens = count_tokens(
                paragraph
            )

            # ------------------------------------------
            # Large paragraph -> recursive split
            # ------------------------------------------

            if (
                paragraph_tokens
                > self.config.max_tokens
            ):

                if current_buffer:

                    segments.append(

                        self._create_segment(

                            current_buffer,

                            heading_stack,

                            offset,

                        )

                    )

                    offset += len(
                        "\n\n".join(
                            current_buffer
                        )
                    )

                    current_buffer = []

                    current_tokens = 0

                recursive_segments = (
                    self._split_large_paragraph(
                        paragraph,
                        heading_stack,
                        offset,
                    )
                )

                segments.extend(
                    recursive_segments
                )

                offset += len(paragraph)

                continue

            # ------------------------------------------
            # Buffer Full
            # ------------------------------------------

            if (
                current_buffer
                and current_tokens
                + paragraph_tokens
                > self.config.target_tokens
            ):

                segments.append(

                    self._create_segment(

                        current_buffer,

                        heading_stack,

                        offset,

                    )

                )

                offset += len(
                    "\n\n".join(
                        current_buffer
                    )
                )

                current_buffer = []

                current_tokens = 0

            current_buffer.append(
                paragraph
            )

            current_tokens += (
                paragraph_tokens
            )

        if current_buffer:

            segments.append(

                self._create_segment(

                    current_buffer,

                    heading_stack,

                    offset,

                )

            )

        segments = self._merge_small_segments(
            segments
        )

        segments = self._remove_duplicate_segments(
            segments
        )

        return self._finalize(
            segments
        )

    # -------------------------------------------------
    # Heading Detection
    # -------------------------------------------------

    def _detect_heading(
        self,
        paragraph: str,
    ) -> HeadingNode | None:

        first_line = (
            paragraph
            .split("\n", 1)[0]
            .strip()
        )

        if not first_line:

            return None

        if not self.HEADING_PATTERN.match(
            first_line
        ):

            return None

        level = 1

        if first_line.startswith("#"):

            level = len(
                first_line.split()[0]
            )

            title = first_line[level:].strip()

        else:

            title = first_line.rstrip(":")

        return HeadingNode(

            level=level,

            title=title,

        )

    # -------------------------------------------------
    # Heading Stack
    # -------------------------------------------------

    def _update_heading_stack(

        self,

        stack: List[HeadingNode],

        heading: HeadingNode,

    ) -> List[HeadingNode]:

        while (

            stack

            and stack[-1].level >= heading.level

        ):

            stack.pop()

        stack.append(
            heading
        )

        return stack.copy()
    
        # -------------------------------------------------
    # Large Paragraph Splitter
    # -------------------------------------------------

    def _split_large_paragraph(
        self,
        paragraph: str,
        headings: List[HeadingNode],
        offset: int,
    ) -> List[TextSegment]:

        sentences = self._split_sentences(
            paragraph
        )

        if not sentences:
            return []

        return self._recursive_sentence_split(
            sentences,
            headings,
            offset,
        )

    # -------------------------------------------------
    # Recursive Sentence Split
    # -------------------------------------------------

    def _recursive_sentence_split(
        self,
        sentences: List[str],
        headings: List[HeadingNode],
        offset: int,
    ) -> List[TextSegment]:

        segments: List[TextSegment] = []

        buffer: List[str] = []

        token_count = 0

        start_offset = offset

        overlap = max(
            0,
            self.config.overlap_tokens,
        )

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            sentence_tokens = count_tokens(
                sentence
            )

            if (
                buffer
                and token_count + sentence_tokens
                > self.config.target_tokens
            ):

                text = " ".join(buffer).strip()

                segments.append(

                    TextSegment(

                        segment_id=str(
                            uuid.uuid4()
                        ),

                        text=text,

                        start_char=start_offset,

                        end_char=start_offset
                        + len(text),

                        headings=list(headings),

                        metadata={},
                    )

                )

                # ----------------------------
                # Adaptive Overlap
                # ----------------------------

                if overlap:

                    words = text.split()

                    overlap_words = words[-overlap:]

                    overlap_text = " ".join(
                        overlap_words
                    )

                    buffer = [
                        overlap_text
                    ]

                    token_count = count_tokens(
                        overlap_text
                    )

                    start_offset += (
                        len(text)
                        - len(overlap_text)
                    )

                else:

                    buffer = []

                    token_count = 0

                    start_offset += len(text)

            buffer.append(
                sentence
            )

            token_count += (
                sentence_tokens
            )

        if buffer:

            text = " ".join(buffer).strip()

            segments.append(

                TextSegment(

                    segment_id=str(
                        uuid.uuid4()
                    ),

                    text=text,

                    start_char=start_offset,

                    end_char=start_offset
                    + len(text),

                    headings=list(headings),

                    metadata={},
                )

            )

        return segments

    # -------------------------------------------------
    # Sentence Extraction
    # -------------------------------------------------

    def _split_sentences(
        self,
        text: str,
    ) -> List[str]:

        sentences = self.SENTENCE_PATTERN.split(
            text
        )

        return [

            sentence.strip()

            for sentence in sentences

            if sentence.strip()

        ]

    # -------------------------------------------------
    # Buffer → Segment
    # -------------------------------------------------

    def _create_segment(
        self,
        paragraphs: List[str],
        headings: List[HeadingNode],
        offset: int,
    ) -> TextSegment:

        text = "\n\n".join(
            paragraphs
        ).strip()

        return TextSegment(

            segment_id=str(
                uuid.uuid4()
            ),

            text=text,

            start_char=max(
                0,
                offset - len(text),
            ),

            end_char=offset,

            headings=list(headings),

            metadata={},
        )
        # -------------------------------------------------
    # Smart Segment Merge
    # -------------------------------------------------

    def _merge_small_segments(
        self,
        segments: List[TextSegment],
    ) -> List[TextSegment]:

        if len(segments) <= 1:
            return segments

        merged: List[TextSegment] = []

        current = segments[0]

        for nxt in segments[1:]:

            current_tokens = count_tokens(
                current.text
            )

            next_tokens = count_tokens(
                nxt.text
            )

            if (
                current_tokens < self.config.min_tokens
                and (
                    current_tokens + next_tokens
                    <= self.config.target_tokens
                )
            ):

                current.text += "\n\n" + nxt.text

                current.end_char = nxt.end_char

                current.metadata.update(
                    nxt.metadata
                )

            else:

                merged.append(current)

                current = nxt

        merged.append(current)

        return merged

    # -------------------------------------------------
    # Duplicate Removal
    # -------------------------------------------------

    def _remove_duplicate_segments(
        self,
        segments: List[TextSegment],
    ) -> List[TextSegment]:

        unique: List[TextSegment] = []

        seen = set()

        for segment in segments:

            fingerprint = (
                segment.text
                .strip()
                .lower()
            )

            if fingerprint in seen:
                continue

            seen.add(fingerprint)

            unique.append(segment)

        return unique

    # -------------------------------------------------
    # Quality Score
    # -------------------------------------------------

    def _quality_score(
        self,
        segment: TextSegment,
    ) -> float:

        tokens = count_tokens(
            segment.text
        )

        score = 1.0

        if tokens < self.config.min_tokens:
            score -= 0.25

        if tokens > self.config.max_tokens:
            score -= 0.25

        if len(segment.text.strip()) < 30:
            score -= 0.15

        if not segment.text.endswith(
            (".", "!", "?")
        ):
            score -= 0.05

        return max(
            0.0,
            round(score, 2),
        )

    # -------------------------------------------------
    # Diagnostics
    # -------------------------------------------------

    def _statistics(
        self,
        segments: List[TextSegment],
    ) -> dict:

        if not segments:
            return {}

        token_counts = [
            count_tokens(
                s.text
            )
            for s in segments
        ]

        return {

            "segments": len(segments),

            "total_tokens": sum(
                token_counts
            ),

            "average_tokens": round(

                sum(token_counts)
                / len(token_counts),

                2,

            ),

            "largest_segment": max(
                token_counts
            ),

            "smallest_segment": min(
                token_counts
            ),
        }

    # -------------------------------------------------
    # Finalize
    # -------------------------------------------------

    def _finalize(
        self,
        segments: List[TextSegment],
    ) -> List[TextSegment]:

        for segment in segments:

            segment.metadata[
                "token_count"
            ] = count_tokens(
                segment.text
            )

            segment.metadata[
                "quality_score"
            ] = self._quality_score(
                segment
            )

        stats = self._statistics(
            segments
        )

        logger.info(

            "Generated %d segments | "
            "Tokens=%d | "
            "Average=%s",

            stats.get(
                "segments",
                0,
            ),

            stats.get(
                "total_tokens",
                0,
            ),

            stats.get(
                "average_tokens",
                0,
            ),
        )

        return segments

    