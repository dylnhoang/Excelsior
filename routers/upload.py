import os
import uuid
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException

from services.memory_store import put            # in-memory DataFrame cache
from services.file_status import update_status   # status + timestamp helper

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    # 1. quick extension check
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files are supported.")

    # 2. generate UUID and disk path
    file_id   = str(uuid.uuid4())
    disk_path = os.path.join(UPLOAD_DIR, f"{file_id}.xlsx")

    # 3. save raw bytes to disk (backup / later export)
    with open(disk_path, "wb") as f:
        f.write(await file.read())

    # 4. load into a pandas DataFrame
    try:
        df = pd.read_excel(disk_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read Excel: {e}")

    # 5. store in-memory for real-time edits
    put(file_id, df)

    # 6. update status
    update_status(file_id, "uploaded")

    # 7. return file_id for subsequent calls
    return {
        "file_id": file_id,
        "message": "File uploaded, parsed, and ready for live editing."
    }