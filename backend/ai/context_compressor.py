import re


class ContextCompressor:

    def compress(self, results):

        if not results:
            return results

        compressed = []
        seen = set()

        for result in results:

            file_id, score, chunk, file_name, page = result

            # Clean whitespace
            chunk = re.sub(r"\s+", " ", chunk).strip()

            # Remove exact duplicate chunks
            normalized = chunk.lower()

            if normalized in seen:
                continue

            seen.add(normalized)

            compressed.append(
                (
                    file_id,
                    score,
                    chunk,
                    file_name,
                    page
                )
            )

        return compressed