import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.excel_parser import parse_excel_preview

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files are supported.")
    
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.xlsx")

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {"file_id": file_id, "message": "File uploaded successfully"}

@router.get("/preview-sheet/{file_id}")
def preview_sheet(file_id: str):
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.xlsx")
    print(f"Looking for file at: {file_path}")  # <-- add this line
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    
    return parse_excel_preview(file_path)