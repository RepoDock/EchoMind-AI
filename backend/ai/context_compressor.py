import re


class ContextCompressor:
    def compress(self, results):

        if not results:
            return results

        compressed = []
        seen = set()

        for result in results:

            chunk_id, file_id, score, chunk, file_name, page, *extra = result

            chunk = re.sub(r"\s+", " ", chunk).strip()

            normalized = chunk.lower()

            if normalized in seen:
                continue

            seen.add(normalized)

            compressed.append(
                (
                    chunk_id,
                    file_id,
                    score,
                    chunk,
                    file_name,
                    page,
                    *extra
                )
            )

        return compressed