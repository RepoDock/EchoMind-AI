import fitz  # PyMuPDF
from pathlib import Path


def extract_pdf_text(file_path):

    full_text = ""
    page_data = []

    try:
        doc = fitz.open(file_path)

        for page_no, page in enumerate(doc, start=1):

            text = page.get_text()

            full_text += text

            page_data.append({
                "page": page_no,
                "text": text
            })

        document = {
            "text": full_text,
            "pages": len(doc),
            "title": Path(file_path).name,
            "page_data": page_data
        }

        doc.close()

        return document

    except Exception as e:
        print(f"PDF Error: {e}")
        return None