from pathlib import Path
from datetime import datetime

from config import SUPPORTED_EXTENSIONS


def scan_folder(folder_path: str):
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError("Folder does not exist.")

    files = []

    for file in folder.rglob("*"):

        if file.is_file():

            if file.suffix.lower() in SUPPORTED_EXTENSIONS:

                metadata = {
                    "name": file.name,
                    "path": str(file),
                    "extension": file.suffix.lower(),
                    "size": file.stat().st_size,
                    "created_at": datetime.fromtimestamp(file.stat().st_ctime),
                    "modified_at": datetime.fromtimestamp(file.stat().st_mtime)
                }

                files.append(metadata)

    return files
