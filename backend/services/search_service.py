from embedding.embedding_service import EmbeddingService
from vectorstore.faiss_manager import FAISSManager

from database.crud import get_file_by_id
from database.content_crud import get_document_content

print("🔥 SEARCH SERVICE RUNNING")
class SearchService:

    def __init__(self):

        self.embedder = EmbeddingService()

        self.faiss = FAISSManager()
    def search(self, query):

        # query_embedding = self.embedder.generate_embedding(query)

        # results = self.faiss.search(query_embedding)

        # best_results = {}

        # for result in results:

        #     file_info = get_file_by_id(result["file_id"])

        #     if file_info is None:
        #         continue

        #     document_text = get_document_content(result["file_id"])

        #     current = {
        #         "id": file_info["id"],
        #         "name": file_info["name"],
        #         "path": file_info["path"],
        #         "extension": file_info["extension"],
        #         "score": round(result["score"], 4),
        #         "snippet": document_text[:200]
        #     }

        #     file_id = file_info["id"]

        #     if (
        #         file_id not in best_results
        #         or current["score"] > best_results[file_id]["score"]
        #     ):
        #         best_results[file_id] = current

        # print("RESULT COUNT:", len(best_results))
        # print("BEST_RESULTS =", best_results)
        # print("VALUES =", list(best_results.values()))
        # return sorted(
        #     best_results.values(),
        #     key=lambda x: x["score"],
        #     reverse=True
        # )
        return [
            {
                "id": 999,
                "name": "TEST FILE",
                "path": "test",
                "extension": ".pdf",
                "score": 1,
                "snippet": "hello"
            }
        ]
