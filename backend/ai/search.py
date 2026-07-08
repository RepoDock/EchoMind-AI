# import json
# import numpy as np
import json
# from ai.embedding import generate_embedding
# from database.connection import cursor
import time

t = time.perf_counter()
import numpy as np
print("numpy:", time.perf_counter() - t)

t = time.perf_counter()
from ai.embedding import generate_embedding
print("embedding:", time.perf_counter() - t)

t = time.perf_counter()
from database.connection import cursor
print("database:", time.perf_counter() - t)
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
        dc.page_number,
        dc.chunk_text,
        dc.embedding,
        f.name
    FROM document_chunks dc
    JOIN files f
        ON dc.file_id = f.id
    WHERE dc.embedding IS NOT NULL
    """)

    rows = cursor.fetchall()

    results = []

    MIN_SCORE = 0.25

    for file_id, page_number, chunk_text, embedding_json, file_name in rows:

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
                file_name,
                page_number
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
def search_document(file_id, query, top_k=8):

    query_embedding = generate_embedding(query)

    cursor.execute("""
    SELECT
        dc.file_id,
        dc.page_number,
        dc.chunk_text,
        dc.embedding,
        f.name
    FROM document_chunks dc
    JOIN files f
        ON dc.file_id = f.id
    WHERE
        dc.embedding IS NOT NULL
        AND dc.file_id = ?
    """, (file_id,))

    rows = cursor.fetchall()

    results = []

    MIN_SCORE = 0.25

    for file_id, page_number, chunk_text, embedding_json, file_name in rows:

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
                file_name,
                page_number
            )
        )

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results[:top_k]
def get_document_context(file_id):

    cursor.execute("""
    SELECT raw_text
    FROM document_content
    WHERE file_id = ?
    """, (file_id,))

    row = cursor.fetchone()

    if row is None:
        return ""

    return row[0]