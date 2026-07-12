from ai.search import get_document_context


class SummaryHandler:

    def __init__(self):

        self.summary_keywords = [

            "summarize",
            "summary",
            "overview",
            "explain this",
            "explain this document",
            "explain this ppt",
            "explain this pdf",
            "explain the document",
            "summarise",
            "describe this",
            "what is this document about",

        ]

    def is_summary_request(self, question):

        q = question.lower()

        return any(keyword in q for keyword in self.summary_keywords)

    def prepare(self, file_id):

        context = get_document_context(file_id)

        question = """
Summarize this document.

Your answer should include:

1. Main topic
2. Important concepts
3. Key points
4. Important sections
5. Final conclusion (if present)

Do NOT explain what a PDF, PPT or document is.

Explain only the CONTENT of the provided document.
"""

        return context, question