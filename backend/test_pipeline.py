from scanner.scanner import scan_folder
from database.crud import insert_file
from database.content_crud import insert_document_content
from extractor.document_processor import DocumentProcessor

processor = DocumentProcessor()

# Scan only sample-data
files = scan_folder("sample-data")

print(f"Found {len(files)} file(s)\n")

for file in files:

    print(f"Processing: {file['name']}")

    file_id = insert_file(file)

    if file["extension"] == ".pdf":

        document = processor.process_document(file["path"])

        insert_document_content(file_id, document)

        print("✓ Stored successfully\n")

print("🎉 Pipeline completed successfully!")