from embedding.embedding_service import EmbeddingService

from vectorstore.faiss_manager import FAISSManager


embedder = EmbeddingService()

faiss_db = FAISSManager()

text1 = """
Database Management System

Normalization

SQL
"""

text2 = """
Machine Learning

Neural Networks

Deep Learning
"""

v1 = embedder.generate_embedding(text1)

v2 = embedder.generate_embedding(text2)

faiss_db.add_embedding(1, v1)

faiss_db.add_embedding(2, v2)

query = embedder.generate_embedding(
    "Normalization"
)

results = faiss_db.search(query)

print(results)