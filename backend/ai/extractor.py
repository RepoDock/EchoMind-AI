from pathlib import Path
import os

from ai.pdf_reader import extract_pdf_text
from ai.docx_reader import extract_docx_text
from ai.txt_reader import extract_txt_text
from ai.ppt_reader import extract_ppt_text
from ai.ppt_converter import convert_ppt_to_pptx


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

    elif extension == ".ppt":

        try:
            temp = convert_ppt_to_pptx(file_path)

            try:
                return extract_ppt_text(temp)
            finally:
                if os.path.exists(temp):
                    os.remove(temp)

        except Exception as e:
            print("❌ PPT Convert Failed:", e)
            return None

    return None