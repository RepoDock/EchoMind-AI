from database.connection import connection, cursor

# ==========================================
# Create Files Table
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (

    id INTEGER PRIMARY KEY,

    scan_folder TEXT

)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS files (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    path TEXT UNIQUE,

    extension TEXT,

    size INTEGER,

    created_at TEXT,

    modified_at TEXT,

    hash TEXT,

    indexed_at TEXT

)
""")

# ==========================================
# Create Files Table
# ==========================================
# ==========================================
# Create Document Content Table
# ==========================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS document_content (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    file_id INTEGER UNIQUE,

    raw_text TEXT,

    pages INTEGER,

    title TEXT,

    subject TEXT,

    course TEXT,

    semester TEXT,

    unit TEXT,

    chapter TEXT,

    language TEXT,

    document_type TEXT,

    keywords TEXT,

    FOREIGN KEY(file_id) REFERENCES files(id)

)
""")

# ==========================================
# Create Document Content Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS document_chunks (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    file_id INTEGER NOT NULL,

    page_number INTEGER NOT NULL,

    chunk_index INTEGER NOT NULL,

    chunk_uuid TEXT,

    chunk_text TEXT NOT NULL,

    token_count INTEGER,

    quality_score REAL,

    metadata_json TEXT,

    embedding TEXT,

    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(file_id)
    REFERENCES files(id)

)
""")


connection.commit()
# ==========================================
# Update document_content table (Migration)
# ==========================================

columns = [
    ("subject", "TEXT"),
    ("course", "TEXT"),
    ("semester", "TEXT"),
    ("unit", "TEXT"),
    ("chapter", "TEXT"),
    ("language", "TEXT"),
    ("document_type", "TEXT"),
    ("keywords", "TEXT")
]

for column, datatype in columns:
    try:
        cursor.execute(
            f"""
            ALTER TABLE document_content
            ADD COLUMN {column} {datatype}
            """
        )
    except:
        pass

connection.commit()
# ==========================================
# Create Embeddings Table
# ==========================================
# ==========================================
# Create Vector Index Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS vector_index (

    faiss_id INTEGER PRIMARY KEY,

    chunk_id INTEGER UNIQUE,

    FOREIGN KEY(chunk_id)
    REFERENCES document_chunks(id)

)
""")

connection.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER,
    vector_path TEXT,
    FOREIGN KEY(file_id) REFERENCES files(id)
)
""")

# ==========================================
# Create Search History Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    timestamp TEXT
)
""")

# Save Changes
connection.commit()


print("All database tables created successfully!")