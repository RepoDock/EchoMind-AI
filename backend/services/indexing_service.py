from database.metadata import should_index
from scanner.scanner import scan_folder
import os
from pathlib import Path
from ai.extractor import extract_text
from ai.metadata_extractor import extract_metadata
import json

from ai.chunker import chunk_text
from ai.embedding import generate_embedding

from database.crud import (
    insert_file,
    insert_document_chunk,
    update_file_hash
)

from database.content_crud import (
    insert_document_content
)

from utils.hashing import calculate_hash

class IndexingService:
    def index_file(self, file_path):

        file = self.create_file_object(file_path)

        result = self.prepare_document(file)

        if result is None:
            return

        self.store_document(
            result["file"],
            result["document"]
        )
   
    def extract_document(self, file):

        document = extract_text(file["path"])

        return document

    def index_folder(self, folder_path):
        files = scan_folder(folder_path)

        print("=" * 60)
        print("Detected Files:", len(files))

        for file in files:
            print(file["name"])

        print("=" * 60)

        processed_files = []

        for file in files:

            result = self.prepare_document(file)

            if result is None:
                continue

            processed_files.append(result)

        return processed_files
    
    def extract_metadata_from_document(self, file, document):

        metadata = extract_metadata(
            document["text"],
            file["name"]
        )

        document.update(metadata)

        return document
    def prepare_document(self, file):

        if not should_index(file):
            print(f"Skipping: {file['name']}")
            return None

        document = self.extract_document(file)

        document = self.extract_metadata_from_document(
            file,
            document
        )

        return {
            "file": file,
            "document": document
        }



    def create_file_object(self, file_path):

        path = Path(file_path)

        return {
            "name": path.name,
            "path": str(path),
            "extension": path.suffix.lower(),
            "size": os.path.getsize(file_path),
            "created_at": os.path.getctime(file_path),
            "modified_at": os.path.getmtime(file_path)
        }
    def store_document(self, file, document):

        file_id = insert_file(file)

        print(file["path"])
        print(os.path.exists(file["path"]))

        if document is None:
            print(f" Failed to read: {file['name']}")
            return
            

        if not document["text"].strip():
            print(f"No text found in {file['name']}")
            return
            
        # -------------------------
        # Extract Metadata
        # -------------------------
       

        insert_document_content(
            file_id,
            document
        )

        total_chunks = 0

        for page in document["page_data"]:

            chunks = chunk_text(page["text"])

            for index, chunk in enumerate(chunks):

                if not chunk.strip():
                    continue

                embedding = generate_embedding(chunk)

                if not embedding:
                    continue

                chunk_id = insert_document_chunk(
                    file_id,
                    page["page"],
                    index,
                    chunk,
                    json.dumps(embedding)
                )


                total_chunks += 1

        print(f" Indexed {total_chunks} chunks")
        update_file_hash(
            file["path"],
            calculate_hash(file["path"])
        )
