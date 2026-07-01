from fastapi import APIRouter
from pydantic import BaseModel

from ai.search import search_documents
from database.connection import cursor

router = APIRouter()


class SearchRequest(BaseModel):
    query: str


@router.post("/search")
def ai_search(request: SearchRequest):

    results = search_documents(request.query)

    best_results = {}

    query = request.query.lower()

    for file_id, score, chunk, file_name, page_number in results:

        cursor.execute(
            """
            SELECT
                name,
                path,
                extension
            FROM files
            WHERE id = ?
            """,
            (file_id,)
        )

        file = cursor.fetchone()

        if not file:
            continue

        lower_chunk = chunk.lower()

        pos = lower_chunk.find(query)

        if pos != -1:

            start = max(0, pos - 60)
            end = min(len(chunk), pos + len(query) + 120)

            snippet = "..." + chunk[start:end] + "..."

        else:

            snippet = chunk[:180] + "..."

        current = {
            "id": file_id,
            "name": file[0],
            "path": file[1],
            "extension": file[2],
            "score": round(score, 4),
            "snippet": snippet
        }

        if (
            file_id not in best_results
            or
            current["score"] > best_results[file_id]["score"]
        ):
            best_results[file_id] = current

    return sorted(
        best_results.values(),
        key=lambda x: x["score"],
        reverse=True
    )