from ai.extract_all import extract_all_fields
from ai.extractor_ai import (
    is_extraction_query,
    extract_exact_value,
)
from ai.search import get_document_context


class ExtractionHandler:

    def handle(
        self,
        question,
        file_id,
        results,
        warning,
        confidence_info,
        citation_engine,
    ):

        q = question.lower()

        extract_all = (
            "extract" in q
            or ("all" in q and "information" in q)
            or ("all" in q and "details" in q)
            or ("key" in q and "information" in q)
            or ("important" in q and "information" in q)
            or ("summary" in q)
            or ("summarize" in q)
            or ("show" in q and "information" in q)
            or ("give" in q and "information" in q)
        )

        if extract_all:

            search_context = get_document_context(file_id)

            fields = extract_all_fields(search_context)

            if fields:

                answer = ""

                for key, value in fields.items():
                    answer += f"{key.replace('_',' ').title()}: {value}\n"

                return {
                    "answer": warning + answer,
                    "sources": citation_engine.build(results),
                    "confidence": confidence_info
                }

        if is_extraction_query(question):

            search_context = get_document_context(file_id)

            value = extract_exact_value(
                question,
                search_context
            )

            if value:

                return {
                    "answer": warning + value,
                    "sources": citation_engine.build(results),
                    "confidence": confidence_info
                }

        return None