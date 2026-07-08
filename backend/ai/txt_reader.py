from pathlib import Path


def extract_txt_text(file_path):

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as file:
            text = file.read()

    except Exception as e:
        print(f"TXT Error: {e}")
        return None

    return {
        "text": text,
        "pages": 1,
        "title": Path(file_path).name,
        "page_data": [
            {
                "page": 1,
                "text": text
            }
        ]
    }