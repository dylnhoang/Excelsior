from fastapi import APIRouter, HTTPException
from services.file_status import get_status

router = APIRouter()

@router.get("/status/{file_id}")
async def get_file_status(file_id: str):
    status_info = get_status(file_id)
    if status_info["status"] == "not_found":
        raise HTTPException(status_code=404, detail="File status not found.")
    return status_info