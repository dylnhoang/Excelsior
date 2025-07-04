from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.formula_generator import generate_excel_formula
from services.excel_modifier import apply_excel_action
from exceptions import FileNotFound, InvalidActionSchema, ExcelOperationError

router = APIRouter()

class PromptRequest(BaseModel):
    file_id: str
    prompt: str

@router.post("/generate-action")
async def generate_action(request: PromptRequest):
    action = generate_excel_formula(request.prompt)

    if "error" in action:
        raise HTTPException(status_code=400, detail=action["error"])

    try:
        apply_excel_action(request.file_id, action)
    except FileNotFound as e:
        raise HTTPException(status_code=404, detail=e.message)
    except InvalidActionSchema as e:
        raise HTTPException(status_code=422, detail=f"Invalid request: {e.message}")
    except ExcelOperationError as e:
        raise HTTPException(status_code=400, detail=f"Excel error: {e.message}")
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error occurred.")

    return { "message": "Action applied successfully", "action": action }