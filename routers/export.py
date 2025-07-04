import os, pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from services.memory_store import get as get_df
from services.file_status import update_status

UPLOAD_DIR = "uploads"
router = APIRouter()

@router.post("/export/{file_id}")
async def export_file(file_id: str):
    df = get_df(file_id)
    if df is None:
        raise HTTPException(status_code=404, detail="File not in memory.")

    path = os.path.join(UPLOAD_DIR, f"{file_id}.xlsx")
    df.to_excel(path, index=False)
    update_status(file_id, "exported")

    return FileResponse(
        path=path,
        filename=f"{file_id}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )