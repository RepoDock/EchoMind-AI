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

    response = []

    for file_id, score, chunk in results:

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

        if file:

            response.append({
                "id": file_id,
                "name": file[0],
                "path": file[1],
                "extension": file[2],
                "score": round(score, 4),
                "snippet": chunk[:250]
            })

    return response