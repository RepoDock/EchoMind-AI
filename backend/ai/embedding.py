print("Loading embedding model...")

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


def generate_embedding(text: str):
    if not text:
        return None

    text = text.strip()

    if not text:
        return None

    embedding = model.encode(text)
    return embedding.tolist()