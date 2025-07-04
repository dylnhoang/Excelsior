from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

OUTPUT_DIR = "outputs"

@router.get("/download/{file_id}")
async def download_file(file_id: str):
    file_path = os.path.join("uploads", f"{file_id}.xlsx")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Modified file not found.")

    return FileResponse(
        path=file_path,
        filename=f"{file_id}_modified.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )