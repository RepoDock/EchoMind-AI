from pathlib import Path

# ===============================
# Project Information
# ===============================

APP_NAME = "AXON AI Backend"
APP_VERSION = "1.0.0"

# ===============================
# Base Directory
# ===============================

BASE_DIR = Path(__file__).resolve().parent

# ===============================
# Storage Directory
# ===============================

STORAGE_DIR = BASE_DIR / "storage"

# Create storage folder if it doesn't exist
STORAGE_DIR.mkdir(exist_ok=True)

# ===============================
# Database
# ===============================

DATABASE_NAME = "database.db"
DATABASE_PATH = STORAGE_DIR / DATABASE_NAME

# ===============================
# FAISS
# ===============================

FAISS_INDEX_NAME = "faiss.index"
FAISS_INDEX_PATH = STORAGE_DIR / FAISS_INDEX_NAME

# ===============================
# Supported File Types
# ===============================

SUPPORTED_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".pptx",
    ".txt",
    ".ppt"
]