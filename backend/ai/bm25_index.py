from rank_bm25 import BM25Okapi

from database.connection import cursor


class BM25Index:

    def __init__(self):

        self.documents = []
        self.chunk_ids = []

        self.bm25 = None

    def build(self):

        cursor.execute("""
        SELECT
            id,
            chunk_text
        FROM document_chunks
        """)

        rows = cursor.fetchall()

        corpus = []

        self.documents.clear()
        self.chunk_ids.clear()

        for row in rows:

            tokens = row["chunk_text"].lower().split()

            corpus.append(tokens)

            self.documents.append(
                row["chunk_text"]
            )

            self.chunk_ids.append(
                row["id"]
            )

        self.bm25 = BM25Okapi(corpus)

    def search(
        self,
        query,
        top_k=50
    ):

        if self.bm25 is None:

            self.build()

        scores = self.bm25.get_scores(
            query.lower().split()
        )

        ranked = sorted(
            [
                (chunk_id, float(score))
                for chunk_id, score in zip(self.chunk_ids, scores)
                if score > 0
            ],
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]