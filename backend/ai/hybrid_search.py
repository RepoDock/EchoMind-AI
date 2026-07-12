from ai.embedding import generate_embedding
from ai.faiss_index import FAISSIndex
from ai.vector_store import get_chunk_ids
from ai.bm25_index import BM25Index
from collections import OrderedDict
from database.connection import cursor
from ai.reranker import Reranker
from ai.query_rewriter import rewrite_query
class HybridSearch:

    def __init__(self):

        self.faiss = FAISSIndex()

        self.bm25 = BM25Index()

        self.reranker = Reranker()
 
    def expand_chunks(self, results):

        expanded = []

        for chunk_id, file_id, score, chunk, file_name, page_number in results:

            cursor.execute(
                """
                SELECT
                    chunk_index
                FROM document_chunks
                WHERE id = ?
                """,
                (chunk_id,)
            )

            row = cursor.fetchone()

            if row is None:

                expanded.append(
                    (
                        chunk_id,
                        file_id,
                        score,
                        chunk,
                        file_name,
                        page_number
                    )
                )

                continue

            chunk_index = row["chunk_index"]

            cursor.execute(
                """
                SELECT
                    id,
                    chunk_text
                FROM document_chunks
                WHERE
                    file_id = ?
                AND
                    chunk_index BETWEEN ? AND ?
                ORDER BY chunk_index
                """,
                (
                    file_id,
                    chunk_index - 1,
                    chunk_index + 1
                )
            )

            neighbours = cursor.fetchall()

            merged = "\n\n".join(
                n["chunk_text"]
                for n in neighbours
            )

            expanded.append(
                (
                    chunk_id,
                    file_id,
                    score,
                    merged,
                    file_name,
                    page_number
                )
            )

        return expanded
    def search(
        self,
        query,
        top_k=20
        ):

        queries = rewrite_query(query)

        fused = {}

        for q in queries:

            # -------------------------
            # FAISS
            # -------------------------

            embedding = generate_embedding(q)

            faiss_ids, faiss_scores = self.faiss.search_ids(
                embedding,
                top_k=30
            )

            faiss_mapping = get_chunk_ids(
                faiss_ids
            )

            for fid, score in zip(
                faiss_ids,
                faiss_scores
            ):

                if fid == -1:
                    continue

                chunk_id = faiss_mapping.get(
                    int(fid)
                )

                if chunk_id is None:
                    continue

                fused[chunk_id] = max(
                    fused.get(chunk_id, 0),
                    float(score) * 0.70
                )

            # -------------------------
            # BM25
            # -------------------------

            bm25 = self.bm25.search(
                q,
                top_k=30
            )

            if bm25:

                max_score = bm25[0][1]

                if max_score > 0:

                    for chunk_id, score in bm25:

                        fused[chunk_id] = max(

                            fused.get(chunk_id, 0),

                            (score / max_score) * 0.30

                        )

        ranked = sorted(
            fused.items(),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        seen = set()
        document_count = {}
        selected_pages = {}

        for chunk_id, score in ranked:

            cursor.execute(
                """
                SELECT
                    dc.file_id,
                    dc.page_number,
                    dc.chunk_text,
                    f.name
                FROM document_chunks dc
                JOIN files f
                    ON dc.file_id = f.id
                WHERE dc.id = ?
                """,
                (chunk_id,)
            )

            row = cursor.fetchone()

            if row is None:
                continue

            # Same page duplicate remove
            file_id = row["file_id"]

            document_count[file_id] = document_count.get(file_id, 0)
            selected_pages.setdefault(file_id, [])

            # Maximum 4 chunks per document
            if document_count[file_id] >= 4:
                continue

            # Avoid very distant pages
            if selected_pages[file_id]:

                nearest = min(
                    abs(row["page_number"] - p)
                    for p in selected_pages[file_id]
                )

                if nearest > 5:
                    continue

            key = (
                row["file_id"],
                row["page_number"]
            )

            if key in seen:
                continue

            seen.add(key)

            document_count[file_id] += 1
            selected_pages[file_id].append(
                row["page_number"]
            )

            results.append(
                (
                    chunk_id,
                    row["file_id"],
                    score,
                    row["chunk_text"],
                    row["name"],
                    row["page_number"]
                )
            )

            if len(results) >= top_k:
                break

        # -------------------------
    # Cross Encoder Reranking
    # -------------------------
        results = self.expand_chunks(results)
        results = self.reranker.rerank(
            query,
            results
        )

        return results[:5]