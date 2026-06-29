
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str):

    if not text:
        return None

    text = text.strip()

    if len(text) == 0:
        return None

    embedding = model.encode(text)

    return embedding.tolist()