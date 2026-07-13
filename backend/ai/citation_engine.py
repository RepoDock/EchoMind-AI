class CitationEngine:

    def build(self, results):

        citations = []

        seen = set()

        for _, _, score, chunk, file_name, page_number, *extra in results:

            key = (file_name, page_number)

            if key in seen:
                continue

            seen.add(key)

            citations.append({

                "file": file_name,

                "page": page_number,

                "score": round(score, 3)

            })

        return citations