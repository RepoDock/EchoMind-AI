import os
import faiss
import numpy as np

from config import FAISS_INDEX_PATH


class FAISSIndex:

    def __init__(self, dimension=384):

        self.dimension = dimension

        if os.path.exists(FAISS_INDEX_PATH):

            self.index = faiss.read_index(
                str(FAISS_INDEX_PATH)
            )

        else:

            self.index = faiss.IndexFlatIP(
                dimension
            )

    def add(self, embeddings):

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32
        )

        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)

    def search(self, embedding, top_k=10):

        embedding = np.asarray(
            [embedding],
            dtype=np.float32
        )

        faiss.normalize_L2(embedding)

        scores, ids = self.index.search(
            embedding,
            top_k
        )

        return scores[0], ids[0]

    def save(self):

        faiss.write_index(
            self.index,
            str(FAISS_INDEX_PATH)
        )

    def load(self):

        if os.path.exists(FAISS_INDEX_PATH):

            self.index = faiss.read_index(
                str(FAISS_INDEX_PATH)
            )

        else:

            self.index = faiss.IndexFlatIP(
                self.dimension
            )

    def total_vectors(self):

        return self.index.ntotal
    
    def search_ids(self, embedding, top_k=50):

        embedding = np.asarray(
            [embedding],
            dtype=np.float32
        )

        faiss.normalize_L2(embedding)

        scores, ids = self.index.search(
            embedding,
            top_k
        )

        return ids[0], scores[0]