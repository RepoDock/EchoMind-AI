from pathlib import Path


def normalize_path(path: str) -> str:
    return str(Path(path).resolve())