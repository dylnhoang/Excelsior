import os
import pandas as pd
from services.file_status import update_status
from exceptions import ExcelOperationError, InvalidActionSchema, FileNotFound
from services.memory_store import get as get_df, put as put_df
from services.file_status import update_status
from services.action_validator import validate_action_schema

UPLOAD_DIR = "uploads"

def apply_excel_action(file_id: str, action: dict):
    df = get_df(file_id)
    if df is None:
        raise ValueError("File not loaded in memory; upload first or reload.")

    is_valid, err = validate_action_schema(action, df.columns.tolist())
    if not is_valid:
        raise ValueError(err)

    op = action["operation"]
    if op == "sort":
        df.sort_values(
            by=action["column"],
            ascending=action.get("order", "asc").lower() == "asc",
            inplace=True,
        )
    elif op == "filter":
        cond = action["condition"]
        col, oper, val = action["column"], cond["operator"], cond["value"]
        expr = f"{col} {oper} @val"
        df.query(expr, inplace=True)
    elif op == "update":
        df[action["column"]] = action["value"]
    else:
        raise ValueError(f"Bad operation '{op}'")

    # Store back in memory
    put_df(file_id, df)
    update_status(file_id, "modified")