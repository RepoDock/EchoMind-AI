import faiss
import numpy as np
import os
import json


class FAISSManager:

    def __init__(self, dimension=384):

        self.dimension = dimension

        self.index_path = "storage/faiss.index"
        self.mapping_path = "storage/faiss_mapping.json"

        # Load or create FAISS index
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        else:
            self.index = faiss.IndexFlatIP(dimension)

        # Load or create mapping
        if os.path.exists(self.mapping_path):
            with open(self.mapping_path, "r") as f:
                self.file_ids = json.load(f)
        else:
            self.file_ids = []

    def add_embedding(self, file_id, embedding):

        embedding = np.array([embedding], dtype="float32")

        self.index.add(embedding)

        self.file_ids.append(file_id)

    def save(self):

        faiss.write_index(self.index, self.index_path)

        with open(self.mapping_path, "w") as f:
            json.dump(self.file_ids, f)

    def search(self, embedding, top_k=5):

        embedding = np.array([embedding], dtype="float32")

        scores, indices = self.index.search(embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            if idx >= len(self.file_ids):
                continue

            results.append({
                "file_id": self.file_ids[idx],
                "score": float(score)
            })

        return results