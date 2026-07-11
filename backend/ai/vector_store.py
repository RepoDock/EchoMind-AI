import json

from ai.faiss_index import FAISSIndex
from database.connection import connection, cursor

index = FAISSIndex()


def add_chunk(chunk_id, embedding):

    index.add([embedding])

    faiss_id = index.total_vectors() - 1

    cursor.execute(
        """
        INSERT OR REPLACE INTO vector_index(
            faiss_id,
            chunk_id
        )
        VALUES(?, ?)
        """,
        (
            faiss_id,
            chunk_id
        )
    )

    connection.commit()

    index.save()


def get_chunk_id(faiss_id):

    cursor.execute(
        """
        SELECT chunk_id
        FROM vector_index
        WHERE faiss_id = ?
        """,
        (int(faiss_id),)
    )

    row = cursor.fetchone()

    if row is None:
        return None

    return row["chunk_id"]


def total_vectors():

    return index.total_vectors()

def get_chunk_ids(faiss_ids):

    valid_ids = [int(i) for i in faiss_ids if i >= 0]

    if len(valid_ids) == 0:
        return {}

    placeholders = ",".join(["?"] * len(valid_ids))

    cursor.execute(
        f"""
        SELECT
            faiss_id,
            chunk_id
        FROM vector_index
        WHERE faiss_id IN ({placeholders})
        """,
        tuple(valid_ids)
    )

    rows = cursor.fetchall()

    mapping = {}

    for row in rows:
        mapping[row["faiss_id"]] = row["chunk_id"]

    return mapping