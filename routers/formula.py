from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.formula_generator import generate_excel_formula

router = APIRouter()

class FormulaRequest(BaseModel):
    file_id: str
    prompt: str

@router.post("/generate-formula")
async def generate_formula(request: FormulaRequest):
    try:
        formula = generate_excel_formula(request.file_id, request.prompt)
        return { "formula": formula }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))