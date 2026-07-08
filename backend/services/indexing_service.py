from database.metadata import should_index
from scanner.scanner import scan_folder

from ai.extractor import extract_text
from ai.metadata_extractor import extract_metadata
from database.metadata import should_index
class IndexingService:

    def process_file(self, file):

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
            

            if not should_index(file):
                print(f"Skipping: {file['name']}")
                continue

            document = self.process_file(file)

            document = self.enrich_document(
                file,
                document
            )

            processed_files.append({
                "file": file,
                "document": document
            })
        
        return processed_files
    
    def enrich_document(self, file, document):

        metadata = extract_metadata(
            document["text"],
            file["name"]
        )

        document.update(metadata)

        return document