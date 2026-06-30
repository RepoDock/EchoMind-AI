import json
import numpy as np

from ai.embedding import generate_embedding
from database.connection import cursor

def keyword_score(query, text):

    query_words = query.lower().split()

    text = text.lower()

    score = 0

    for word in query_words:

        if word in text:
            score += 1

    return score / max(len(query_words), 1)

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

def search_documents(query, top_k=8):

    query_embedding = generate_embedding(query)

    cursor.execute("""
    SELECT
        dc.file_id,
        dc.chunk_text,
        dc.embedding,
        f.name
    FROM document_content dc
    JOIN files f
        ON dc.file_id = f.id
    WHERE dc.embedding IS NOT NULL
    """)

    rows = cursor.fetchall()

    results = []

    MIN_SCORE = 0.25

    for file_id, chunk_text, embedding_json, file_name in rows:

        embedding = json.loads(embedding_json)

        if len(embedding) == 0:
            continue

        semantic_score = cosine_similarity(
            query_embedding,
            embedding
        )

        keyword_boost = keyword_score(
            query,
            chunk_text
        )

        similarity = (
            semantic_score * 0.80
            + keyword_boost * 0.20
        )

        if similarity < MIN_SCORE:
            continue

        results.append(
            (
                file_id,
                similarity,
                chunk_text,
                file_name
            )
        )

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )
    print("\n======================")

    for r in results:
        print(r[3], "->", round(r[1], 3))

    print("======================\n")
    return results[:top_k]