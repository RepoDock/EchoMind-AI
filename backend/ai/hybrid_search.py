from ai.embedding import generate_embedding
from ai.faiss_index import FAISSIndex
from ai.vector_store import get_chunk_ids
from ai.bm25_index import BM25Index

from database.connection import cursor
from ai.reranker import Reranker
from ai.query_rewriter import rewrite_query
class HybridSearch:

    def __init__(self):

        self.faiss = FAISSIndex()

        self.bm25 = BM25Index()

        self.reranker = Reranker()

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

            # Ek document se maximum 2 chunks

            if document_count[file_id] >= 2:
                continue

            key = (
                row["file_id"],
                row["page_number"]
            )

            if key in seen:
                continue

            seen.add(key)

            document_count[file_id] += 1

            results.append(
                (
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

        results = self.reranker.rerank(
            query,
            results
        )

        return results[:5]