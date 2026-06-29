from database.connection import connection, cursor


def insert_document_content(file_id, document):

    cursor.execute(
        """
        INSERT OR REPLACE INTO document_content
        (file_id, raw_text, pages, title)

        VALUES (?, ?, ?, ?)
        """,
        (
            file_id,
            document["text"],
            document["pages"],
            document["title"]
        )
    )

    connection.commit()

def get_document_content(file_id):

    cursor.execute(
        """
        SELECT raw_text
        FROM document_content
        WHERE file_id = ?
        """,
        (file_id,)
    )

    row = cursor.fetchone()

    if row is None:
        return ""

    return row[0]