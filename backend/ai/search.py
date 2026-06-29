import json
import numpy as np

from ai.embedding import generate_embedding
from database.connection import cursor


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def search_documents(query, top_k=5):

    query_embedding = generate_embedding(query)

    cursor.execute("""
        SELECT
            file_id,
            chunk_text,
            embedding
        FROM document_content
        WHERE embedding IS NOT NULL
    """)

    rows = cursor.fetchall()

    best_scores = {}

    for file_id, chunk_text, embedding_json in rows:

        embedding = json.loads(embedding_json)
        if len(embedding) == 0:
            continue

        similarity = cosine_similarity(
            query_embedding,
            embedding
        )

        if (
            file_id not in best_scores
            or similarity > best_scores[file_id][0]
        ):
            best_scores[file_id] = (
                similarity,
                chunk_text
            )

    results = []

    for file_id, (score, chunk) in best_scores.items():

        results.append(
            (
                file_id,
                score,
                chunk
            )
        )

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results[:top_k]