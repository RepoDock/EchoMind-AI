from extractor.txt import TXTExtractor

extractor = TXTExtractor()

result = extractor.extract_text(
    r"c:\Users\HP\Downloads\Arrays Basics.txt"
)

print(result["text"])