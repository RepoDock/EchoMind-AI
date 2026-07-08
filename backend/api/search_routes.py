from fastapi import APIRouter
from database.crud import get_recent_files
from database.crud import get_all_files
router = APIRouter()


@router.get("/files")
def files():
    return get_all_files()
@router.get("/recent")
def recent():
    return get_recent_files()