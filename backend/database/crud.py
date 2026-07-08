from database.connection import connection, get_cursor
from datetime import datetime
def get_recent_files():
    cursor = get_cursor()
    cursor.execute("""
        SELECT
            id,
            name,
            path,
            extension,
            size,
            modified_at
        FROM files
        ORDER BY modified_at DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    return [
        {
            "id": row["id"],
            "name": row["name"],
            "path": row["path"],
            "extension": row["extension"],
            "size": row["size"],
            "modified_at": row["modified_at"]
        }
        for row in rows
    ]
def get_file_by_path(path):
    cursor = get_cursor()

    cursor.execute(
        """
        SELECT
            id,
            path,
            modified_at,
            indexed_at
        FROM files
        WHERE path = ?
        """,
        (path,)
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row["id"],
        "path": row["path"],
        "modified_at": row["modified_at"],
        "indexed_at": row["indexed_at"]
    }
def update_file(file_id, file_data):
    cursor = get_cursor()

    cursor.execute(
        """
        UPDATE files
        SET
            name = ?,
            extension = ?,
            size = ?,
            created_at = ?,
            modified_at = ?
        WHERE id = ?
        """,
        (
            file_data["name"],
            file_data["extension"],
            file_data["size"],
            str(file_data["created_at"]),
            str(file_data["modified_at"]),
            file_id
        )
    )

    connection.commit()
def mark_indexed(file_id):
    cursor = get_cursor()

    cursor.execute(
        """
        UPDATE files
        SET indexed_at = ?
        WHERE id = ?
        """,
        (
            datetime.now().isoformat(),
            file_id
        )
    )

def insert_file(file_data):
    cursor = get_cursor()
    # Check if file already exists
    cursor.execute(
        """
        SELECT id
        FROM files
        WHERE path = ?
        """,
        (file_data["path"],)
    )

    row = cursor.fetchone()

    # If file already exists, return its ID
    if row is not None:
        return row[0]

    # Otherwise insert new file
    cursor.execute(
        """
        INSERT INTO files
        (
            name,
            path,
            extension,
            size,
            created_at,
            modified_at,
            hash,
            indexed_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            file_data["name"],
            file_data["path"],
            file_data["extension"],
            file_data["size"],
            str(file_data["created_at"]),
            str(file_data["modified_at"]),
            None,
            None
        )
    )

    connection.commit()

    return cursor.lastrowid


def get_file_by_id(file_id):
    cursor = get_cursor()
    cursor.execute(
        """
        SELECT
            id,
            name,
            path,
            extension
        FROM files
        WHERE id = ?
        """,
        (file_id,)
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "path": row[2],
        "extension": row[3]
    }
def get_all_files():
    cursor = get_cursor()
    cursor.execute("""
        SELECT
            id,
            name,
            path,
            extension,
            size,
            modified_at
        FROM files
        ORDER BY modified_at DESC
    """)

    rows = cursor.fetchall()

    return [
        {
            "id": row["id"],
            "name": row["name"],
            "path": row["path"],
            "extension": row["extension"],
            "size": row["size"],
            "modified_at": row["modified_at"]
        }
        for row in rows
    ]
def save_scan_folder(folder):
    cursor = get_cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO settings(id, scan_folder)
        VALUES(1, ?)
    """, (folder,))

    connection.commit()


def get_scan_folder():
    cursor = get_cursor()
    cursor.execute("""
        SELECT scan_folder
        FROM settings
        WHERE id=1
    """)

    row = cursor.fetchone()

    if row:
        return row["scan_folder"]

    return ""

def insert_document_chunk(
    file_id,
    page_number,
    chunk_index,
    chunk_text,
    embedding
):
    cursor = get_cursor()

    cursor.execute(
        """
        INSERT INTO document_chunks
        (
            file_id,
            page_number,
            chunk_index,
            chunk_text,
            embedding
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            file_id,
            page_number,
            chunk_index,
            chunk_text,
            embedding
        )
    )

    chunk_id = cursor.lastrowid

    connection.commit()

    return chunk_id

def get_file_hash(path):
    cursor = get_cursor()

    cursor.execute(
        """
        SELECT hash
        FROM files
        WHERE path = ?
        """,
        (path,)
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return row["hash"]


def update_file_hash(path, file_hash):
    cursor = get_cursor()

    cursor.execute(
        """
        UPDATE files
        SET hash = ?
        WHERE path = ?
        """,
        (
            file_hash,
            path
        )
    )

    connection.commit()