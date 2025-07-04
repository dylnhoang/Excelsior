from typing import Dict
import pandas as pd

# {file_id: DataFrame}
dataframes: Dict[str, pd.DataFrame] = {}

def put(file_id: str, df: pd.DataFrame):
    dataframes[file_id] = df

def get(file_id: str) -> pd.DataFrame | None:
    return dataframes.get(file_id)

def delete(file_id: str):
    dataframes.pop(file_id, None)