from scanner.scanner import scan_folder
from extractor.document_processor import DocumentProcessor

from database.crud import insert_file
from database.content_crud import insert_document_content

from embedding.embedding_service import EmbeddingService
from vectorstore.faiss_manager import FAISSManager


class IndexingService:

    def __init__(self):

        self.processor = DocumentProcessor()

        self.embedder = EmbeddingService()

        self.faiss = FAISSManager()

    def index_folder(self, folder_path):

        files = scan_folder(folder_path)

        indexed = 0

        for file in files:

            try:

                # Skip unsupported files
                if file["extension"] not in [".pdf", ".docx", ".pptx", ".txt"]:
                    continue

                # Save metadata
                file_id = insert_file(file)

                # Extract text
                document = self.processor.process_document(
                    file["path"]
                )

                # Save document content
                insert_document_content(
                    file_id,
                    document
                )

                # Generate embedding
                embedding = self.embedder.generate_embedding(
                    document["text"]
                )

                # Store embedding in FAISS
                self.faiss.add_embedding(
                    file_id,
                    embedding
                )

                indexed += 1

                print(f"✅ Indexed: {file['name']}")

            except Exception as e:

                print(f"❌ Error indexing {file['name']}")

                print(e)

        # Save FAISS index
        self.faiss.save()

        return {

            "total_files": len(files),

            "indexed_files": indexed

        }