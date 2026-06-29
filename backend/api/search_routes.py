from fastapi import APIRouter
from pydantic import BaseModel
from database.crud import get_recent_files
from services.search_service import SearchService
from database.crud import get_all_files
router = APIRouter()

service = SearchService()


class SearchRequest(BaseModel):
    query: str

@router.get("/files")
def files():
    return get_all_files()
@router.post("/search")
def search(request: SearchRequest):

    return service.search(request.query)
@router.get("/recent")
def recent():
    return get_recent_files()