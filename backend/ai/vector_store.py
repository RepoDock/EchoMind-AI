import faiss
import numpy as np

dimension = 384

index = faiss.IndexFlatL2(dimension)

file_ids = []


def add_embedding(file_id, embedding):

    vector = np.array([embedding], dtype="float32")

    index.add(vector)

    file_ids.append(file_id)


def search_embedding(query_embedding, k=5):

    vector = np.array([query_embedding], dtype="float32")

    distances, indices = index.search(vector, k)

    results = []

    for i in indices[0]:

        if i < len(file_ids):
            results.append(file_ids[i])

    return results