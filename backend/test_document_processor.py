from extractor.document_processor import DocumentProcessor

processor = DocumentProcessor()

result = processor.process_document(
    r"C:\Users\HP\Downloads\DBMS_Full_Notes.pdf"
)

print(result["pages"])
print(result["text"][:1000])