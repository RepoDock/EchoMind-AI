import fitz

from extractor.base_extractor import BaseExtractor


class PDFExtractor(BaseExtractor):

    def extract_text(self, file_path: str):

        document = fitz.open(file_path)

        text = ""

        for i, page in enumerate(document):

            print(f"Reading page {i+1}/{len(document)}")
            text += page.get_text()
            

        # Read metadata BEFORE closing the document
        pages = len(document)
        title = document.metadata.get("title", "")

        document.close()

        return {
            "text": text,
            "pages": pages,
            "title": title,
        }