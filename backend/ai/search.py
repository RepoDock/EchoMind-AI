import time
from ai.embedding import generate_embedding
from ai.faiss_index import FAISSIndex
from ai.vector_store import get_chunk_ids
from database.connection import cursor

t = time.perf_counter()
faiss_index = FAISSIndex()
print("Search Engine Loaded:", time.perf_counter() - t)


def keyword_score(query, text):
    query_words = query.lower().split()
    text = text.lower()
    score = 0
    for word in query_words:
        if word in text:
            score += 1
    return score / max(len(query_words), 1)


def _search(query, file_id=None, top_k=8):
    query_embedding = generate_embedding(query)

    faiss_ids, semantic_scores = faiss_index.search_ids(
        query_embedding,
        top_k=50
    )

    mapping = get_chunk_ids(faiss_ids)

    results = []

    for faiss_id, semantic_score in zip(faiss_ids, semantic_scores):

        if faiss_id == -1:
            continue

        chunk_id = mapping.get(int(faiss_id))

        if chunk_id is None:
            continue

        if file_id is None:
            cursor.execute("""
                SELECT
                    dc.file_id,
                    dc.page_number,
                    dc.chunk_text,
                    f.name
                FROM document_chunks dc
                JOIN files f
                    ON dc.file_id = f.id
                WHERE dc.id = ?
            """, (chunk_id,))
        else:
            cursor.execute("""
                SELECT
                    dc.file_id,
                    dc.page_number,
                    dc.chunk_text,
                    f.name
                FROM document_chunks dc
                JOIN files f
                    ON dc.file_id = f.id
                WHERE dc.id = ?
                  AND dc.file_id = ?
            """, (chunk_id, file_id))

        row = cursor.fetchone()

        if row is None:
            continue

        boost = keyword_score(query, row["chunk_text"])

        score = (
            float(semantic_score) * 0.80 +
            boost * 0.20
        )

        if score < 0.25:
            continue

        results.append((
            row["file_id"],
            score,
            row["chunk_text"],
            row["name"],
            row["page_number"]
        ))

    results.sort(key=lambda x: x[1], reverse=True)

    return results[:top_k]


def search_documents(query, top_k=8):
    return _search(
        query=query,
        file_id=None,
        top_k=top_k
    )


def search_document(file_id, query, top_k=8):
    return _search(
        query=query,
        file_id=file_id,
        top_k=top_k
    )


def get_document_context(file_id):
    cursor.execute("""
        SELECT raw_text
        FROM document_content
        WHERE file_id = ?
    """, (file_id,))

    row = cursor.fetchone()

    if row is None:
        return ""

    return row["raw_text"] if not isinstance(row, tuple) else row[0]
