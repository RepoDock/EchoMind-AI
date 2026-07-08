import re


def extract_metadata(text, filename=""):

    metadata = {
        "title": filename.replace(".pdf", ""),
        "subject": None,
        "course": None,
        "semester": None,
        "unit": None,
        "chapter": None,
        "language": "English",
        "document_type": "Document",
        "keywords": None
    }

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # -----------------------
    # Title
    # -----------------------
    if lines:
        metadata["title"] = lines[0]

    # -----------------------
    # Course Code
    # Example: CSE202
    # -----------------------
    match = re.search(r"\b([A-Z]{2,5}\d{2,4})\b", text)
    if match:
        metadata["course"] = match.group(1)

    # -----------------------
    # Semester
    # -----------------------
    match = re.search(r"Semester\s*[-:]?\s*(\d+)", text, re.IGNORECASE)
    if match:
        metadata["semester"] = match.group(1)

    # -----------------------
    # Unit
    # -----------------------
    match = re.search(r"Unit\s*[-:]?\s*(\d+)", text, re.IGNORECASE)
    if match:
        metadata["unit"] = match.group(1)

    # -----------------------
    # Chapter
    # -----------------------
    match = re.search(r"Chapter\s*[-:]?\s*(\d+)", text, re.IGNORECASE)
    if match:
        metadata["chapter"] = match.group(1)

    return metadata