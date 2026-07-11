import json

from ai.faiss_index import FAISSIndex
from database.connection import cursor, connection

index = FAISSIndex()

cursor.execute("""
SELECT
    id,
    embedding
FROM document_chunks
WHERE embedding IS NOT NULL
ORDER BY id
""")

rows = cursor.fetchall()

count = 0

for row in rows:

    chunk_id = row["id"]

    embedding = json.loads(row["embedding"])

    index.add([embedding])

    faiss_id = index.total_vectors() - 1

    cursor.execute(
        """
        INSERT OR REPLACE INTO vector_index(
            faiss_id,
            chunk_id
        )
        VALUES(?,?)
        """,
        (
            faiss_id,
            chunk_id
        )
    )

    count += 1

connection.commit()

index.save()

print(f"{count} vectors indexed into FAISS.")