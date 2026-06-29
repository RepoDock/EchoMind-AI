from embedding.embedding_service import EmbeddingService

service = EmbeddingService()

vector = service.generate_embedding(

"""
Database Management System

Normalization

BCNF

SQL
"""
)

print(type(vector))

print(len(vector))

print(vector[:10])