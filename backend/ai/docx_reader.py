from docx import Document
from pathlib import Path


def extract_docx_text(file_path):

    try:
        doc = Document(file_path)

        full_text = ""

        for paragraph in doc.paragraphs:
            full_text += paragraph.text + "\n"

        return {
            "text": full_text,
            "pages": 1,
            "title": Path(file_path).name,
            "page_data": [
                {
                    "page": 1,
                    "text": full_text
                }
            ]
        }

    except Exception as e:
        print(f"DOCX Error: {e}")
        return None