from database.connection import connection, cursor

def get_recent_files():

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
def insert_file(file_data):

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

    cursor.execute("""
        INSERT OR REPLACE INTO settings(id, scan_folder)
        VALUES(1, ?)
    """, (folder,))

    connection.commit()


def get_scan_folder():

    cursor.execute("""
        SELECT scan_folder
        FROM settings
        WHERE id=1
    """)

    row = cursor.fetchone()

    if row:
        return row["scan_folder"]

    return ""

def insert_document_content(file_id, chunk_index, chunk_text, embedding):

    cursor.execute(
        """
        INSERT INTO document_content
        (
            file_id,
            chunk_index,
            chunk_text,
            embedding
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            file_id,
            chunk_index,
            chunk_text,
            embedding
        )
    )

    

    connection.commit()
    connection.commit()