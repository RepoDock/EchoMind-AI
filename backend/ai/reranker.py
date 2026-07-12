from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query,
        results
    ):

        if not results:
            return []

        pairs = []

        for _, _, _, chunk, _, _ in results:

            pairs.append(
                (
                    query,
                    chunk
                )
            )

        scores = self.model.predict(
            pairs,
            batch_size=16,
            show_progress_bar=False
        )

        reranked = []

        for result, score in zip(
            results,
            scores
        ):

            reranked.append(
            (
                result[0],      # chunk_id
                result[1],      # file_id
                float(score),
                result[3],      # chunk
                result[4],      # file
                result[5]       # page
            )
        )

        reranked.sort(
            key=lambda x: x[2],
            reverse=True
        )

        return reranked