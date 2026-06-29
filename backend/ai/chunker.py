# def chunk_text(text, chunk_size=500, overlap=100):

#     if not text:
#         return []

#     chunks = []

#     start = 0

#     while start < len(text):

#         end = start + chunk_size

#         chunks.append(text[start:end])

#         start += chunk_size - overlap

#     return chunks
def chunk_text(
    text,
    chunk_size=500,
    overlap=100,
    max_chunks=300
):

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        if len(chunks) >= max_chunks:
            break

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks