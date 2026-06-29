from embedding.embedding_service import EmbeddingService
from vectorstore.faiss_manager import FAISSManager

from database.crud import get_file_by_id
from database.content_crud import get_document_content


class SearchService:

    def __init__(self):

        self.embedder = EmbeddingService()

        self.faiss = FAISSManager()

    def search(self, query):

        query_embedding = self.embedder.generate_embedding(query)

        results = self.faiss.search(query_embedding)

        final_results = []

        for result in results:

            file_info = get_file_by_id(result["file_id"])

            if file_info is None:
                continue

            document_text = get_document_content(result["file_id"])

            preview = document_text[:200]

            final_results.append({

                "id": file_info["id"],

                "file_name": file_info["name"],

                "path": file_info["path"],

                "extension": file_info["extension"],

                "score": round(result["score"], 3),

                "preview": preview

            })

        return final_results