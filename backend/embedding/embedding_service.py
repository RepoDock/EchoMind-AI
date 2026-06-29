from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):

        print("Loading AI Model...")

        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

        print("Model Loaded!")

    def generate_embedding(self, text):

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding