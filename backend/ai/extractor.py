from pathlib import Path

from ai.pdf_reader import extract_pdf_text
from ai.docx_reader import extract_docx_text
from ai.txt_reader import extract_txt_text
from ai.ppt_reader import extract_ppt_text

def extract_text(file_path):

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_pdf_text(file_path)

    elif extension == ".docx":
        return extract_docx_text(file_path)

    elif extension == ".txt":
        return extract_txt_text(file_path)
    elif extension == ".pptx":
        return extract_ppt_text(file_path)

    return ""