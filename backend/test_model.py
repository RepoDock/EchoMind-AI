from sentence_transformers import SentenceTransformer

print("Start")

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5",
    device="cpu"
)

print("Loaded")