from extractor.ppt import PPTExtractor

extractor = PPTExtractor()

result = extractor.extract_text(
    r"c:\Users\HP\Downloads\69ac007f-ff4e-4c27-b8a8-310f958e0072.pptx"
)

print(result["pages"])
print(result["text"])