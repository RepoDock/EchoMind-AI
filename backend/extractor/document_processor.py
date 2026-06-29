import os

from extractor.pdf import PDFExtractor
from extractor.docx import DOCXExtractor
from extractor.ppt import PPTExtractor
from extractor.txt import TXTExtractor


class DocumentProcessor:

    def __init__(self):

        self.extractors = {
            ".pdf": PDFExtractor(),
            ".docx": DOCXExtractor(),
            ".pptx": PPTExtractor(),
            ".txt": TXTExtractor(),
        }

    def process_document(self, file_path):

        extension = os.path.splitext(file_path)[1].lower()

        extractor = self.extractors.get(extension)

        if extractor is None:
            raise ValueError(f"Unsupported file type: {extension}")

        return extractor.extract_text(file_path)