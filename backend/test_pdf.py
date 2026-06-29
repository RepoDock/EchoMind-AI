from extractor.pdf import PDFExtractor

pdf = PDFExtractor()

result = pdf.extract_text(
    r"C:\Users\HP\Downloads\DBMS_Full_Notes.pdf"
)

print("Title :", result["title"])
print("Pages :", result["pages"])
print()
print(result["text"][:1000])