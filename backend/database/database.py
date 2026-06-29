from database.connection import connection, cursor

# ==========================================
# Create Files Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS document_content(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    file_id INTEGER UNIQUE,

    raw_text TEXT,

    pages INTEGER,

    title TEXT,

    FOREIGN KEY(file_id) REFERENCES files(id)

)
""")

# ==========================================
# Create Document Content Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS document_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER,
    raw_text TEXT,
    FOREIGN KEY(file_id) REFERENCES files(id)
)
""")

# ==========================================
# Create Embeddings Table
# ==========================================

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