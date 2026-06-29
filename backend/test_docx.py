from extractor.docx import DOCXExtractor

extractor = DOCXExtractor()

result = extractor.extract_text(
    r"c:\Users\HP\Downloads\FraudDetectionReport.docx"
)
print(result["text"])