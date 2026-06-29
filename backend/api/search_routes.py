from fastapi import APIRouter
from pydantic import BaseModel

from services.search_service import SearchService

router = APIRouter()

service = SearchService()


class SearchRequest(BaseModel):
    query: str


@router.post("/search")
def search(request: SearchRequest):

    return service.search(request.query)