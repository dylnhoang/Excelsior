from fastapi import APIRouter, HTTPException, Query
from services.memory_store import get as get_df, put as put_df   # in-memory store
from pydantic import BaseModel
from services.file_status import update_status
import pandas as pd
import os

UPLOAD_DIR = "uploads"
router = APIRouter()

class PatchRequest(BaseModel):
    updates: list[dict]  # Each dict should have "row", "column", and "value"

class ColumnPatch(BaseModel):
    column: str
    value: str | int | float | None = None        # for “set”
    operation: str | None = None                  # upper, lower, title, add, sub
    delta: int | float | None = None  

@router.get("/data/{file_id}")
async def get_live_data(
    file_id: str,
    rows: int = Query(20, ge=1, le=1000, description="Number of rows to preview")
):
    """
    Return the top `rows` rows of the DataFrame for live preview.
    """
    df = get_df(file_id)
    if df is None:
        raise HTTPException(status_code=404, detail="File not loaded in memory.")

    # Convert DataFrame slice → JSON-serialisable list-of-dicts
    preview = df.head(rows).to_dict(orient="records")
    return {"file_id": file_id, "rows": preview}

@router.get("/data/{file_id}/preview")
async def get_file_data(file_id: str):
    df = get_df(file_id)
    if df is None:
        raise HTTPException(status_code=404, detail="File not found in memory.")
    
    # Convert DataFrame to list of dicts for JSON response
    return {
        "file_id": file_id,
        "rows": df.to_dict(orient="records"),
        "columns": df.columns.tolist()
    }

@router.patch("/data/{file_id}")
async def patch_file_data(file_id: str, patch: PatchRequest):
    """
    Apply in-place updates to the in-memory DataFrame.
    """
    df = get_df(file_id)
    if df is None:
        raise HTTPException(status_code=404, detail="File not loaded in memory.")

    for update in patch.updates:
        row_idx = update.get("row")
        col_name = update.get("column")
        new_val = update.get("value")

        if row_idx is None or col_name is None:
            raise HTTPException(status_code=400, detail="Missing row or column in update.")

        if col_name not in df.columns or not (0 <= row_idx < len(df)):
            raise HTTPException(status_code=400, detail=f"Invalid row index or column name: {row_idx}, {col_name}")

        df.at[row_idx, col_name] = new_val

    put_df(file_id, df)  # Save changes back into memory
    return {"file_id": file_id, "message": "Updates applied in memory."}


@router.post("/data/{file_id}/save")
async def save_live_data(file_id: str):
    df = get_df(file_id)
    if df is None:
        raise HTTPException(status_code=404, detail="File not found in memory.")

    # Save to disk
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.xlsx")
    df.to_excel(file_path, index=False)

    update_status(file_id, "modified")
    return {
        "file_id": file_id,
        "message": "Live data saved to disk."
    }

@router.patch("/data/{file_id}/column")
async def patch_column(file_id: str, patch: ColumnPatch):
    df = get_df(file_id)
    if df is None:
        raise HTTPException(status_code=404, detail="File not loaded in memory.")

    if patch.column not in df.columns:
        raise HTTPException(status_code=400, detail="Column not found.")

    col = patch.column
    if patch.operation is None:  # simple overwrite
        if patch.value is None:
            raise HTTPException(status_code=400, detail="Provide 'value' or 'operation'.")
        df[col] = patch.value

    elif patch.operation in {"upper", "lower", "title"}:
        if not pd.api.types.is_string_dtype(df[col]):
            raise HTTPException(status_code=400, detail="String operation on non-string column.")
        if patch.operation == "upper":
            df[col] = df[col].str.upper()
        elif patch.operation == "lower":
            df[col] = df[col].str.lower()
        elif patch.operation == "title":
            df[col] = df[col].str.title()

    elif patch.operation in {"add", "sub"}:
        if patch.delta is None:
            raise HTTPException(status_code=400, detail="Missing 'delta' for numeric operation.")
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise HTTPException(status_code=400, detail="Numeric operation on non-numeric column.")
        delta = patch.delta
        df[col] = df[col] + delta if patch.operation == "add" else df[col] - delta

    else:
        raise HTTPException(status_code=400, detail=f"Unsupported operation '{patch.operation}'.")

    put_df(file_id, df)
    update_status(file_id, "modified (column patch)")

    # return a preview so caller sees effect immediately
    return {
        "file_id": file_id,
        "message": "Column updated.",
        "preview": df.head(10).to_dict(orient="records")
    }

SUPPORTED_OPS = { "==", "!=", ">", "<", ">=", "<=" }

@router.get("/data/{file_id}/filter")
async def filter_data(
    file_id: str,
    column: str = Query(..., description="Column to filter on"),
    operator: str = Query("==", description="One of ==, !=, >, <, >=, <="),
    value: str = Query(..., description="Value to compare against"),
    rows: int = Query(100, ge=1, le=1000, description="Rows to return (preview)")
):
    df = get_df(file_id)
    if df is None:
        raise HTTPException(status_code=404, detail="File not loaded in memory.")

    if column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Column '{column}' not found.")

    if operator not in SUPPORTED_OPS:
        raise HTTPException(status_code=400, detail=f"Unsupported operator '{operator}'.")

    # Coerce value type to match column dtype
    col_dtype = df[column].dtype
    try:
        typed_value = pd.Series([value]).astype(col_dtype)[0]
    except Exception:
        raise HTTPException(status_code=400, detail=f"Cannot cast value to column type {col_dtype}")

    # Build boolean mask
    expr = f"`{column}` {operator} @typed_value"
    try:
        filtered = df.query(expr)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Bad filter expression: {e}")

    return {
        "file_id": file_id,
        "filter": { "column": column, "operator": operator, "value": value },
        "count": len(filtered),
        "rows": filtered.head(rows).to_dict(orient="records")
    }

@router.get("/data/{file_id}/sort")
async def sort_data(
    file_id: str,
    column: str = Query(..., description="Column to sort by"),
    order: str = Query("asc", regex="^(asc|desc)$", description="asc or desc"),
    rows: int = Query(100, ge=1, le=1000, description="Preview rows to return"),
    persist: bool = Query(False, description="True to commit sort into memory")
):
    """
    Return the DataFrame sorted by a given column.
    If persist=true the sorted frame is saved back into memory.
    """
    df = get_df(file_id)
    if df is None:
        raise HTTPException(status_code=404, detail="File not loaded in memory.")

    if column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Column '{column}' not found.")

    # Perform the sort (ascending unless order='desc')
    ascending = order.lower() == "asc"
    sorted_df = df.sort_values(by=column, ascending=ascending, inplace=False)

    # Persist if requested
    if persist:
        put_df(file_id, sorted_df)
        update_status(file_id, "modified (sort)")

    return {
        "file_id": file_id,
        "sort": {"column": column, "order": order, "persist": persist},
        "rows": sorted_df.head(rows).to_dict(orient="records")
    }