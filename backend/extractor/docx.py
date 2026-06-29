from docx import Document

from extractor.base_extractor import BaseExtractor


class DOCXExtractor(BaseExtractor):

    def extract_text(self, file_path):

        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        text = "\n".join(paragraphs)

        return {
            "text": text,
            "pages": len(document.sections),
            "title": "",
        }