from extractor.base_extractor import BaseExtractor


class TXTExtractor(BaseExtractor):

    def extract_text(self, file_path):

        with open(file_path, "r", encoding="utf-8") as file:

            text = file.read()

        return {

            "text": text,

            "pages": 1,

            "title": ""
        }